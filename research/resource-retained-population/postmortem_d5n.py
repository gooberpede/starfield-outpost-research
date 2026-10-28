# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline D5N diagnostic reduction; no process or protected-input operations.

Reads a completed local capture, its authenticated reduction and pinned generated
controller source. Uses only the standard library. Writes one fresh local JSON;
does not modify the observer, replace receipt authentication, or infer missing DR
values. Invoke only after independently establishing target absence.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-retained-population'


def pin(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def analyze(capture, review, controller):
    def read(path):
        return json.loads(path.read_text(encoding='utf8'))

    events = [json.loads(s) for s in (capture/'events.jsonl').read_text().splitlines()]
    control = [json.loads(s) for s in (capture/'control.jsonl').read_text().splitlines()]
    session = events[0]
    assert session['synthetic'] is False and session['schema'] == 'sor-d5n-hybrid/1'
    assert [r['sequence'] for r in control] == list(range(1, len(control)+1))
    # CONTROL_START precedes target binding; every subsequent row is bound.
    assert control[0]['action'] == 'CONTROL_START'
    assert control[0]['pid'] == control[0]['process_creation'] == 0
    assert all(r['pid'] == session['pid'] and
               r['process_creation'] == session['creation_filetime_100ns'] for r in control[1:])
    source = controller.read_text(encoding='utf8')
    assert pin(controller) == 'afd544830bf732837a36531afd0bbda05a4ceb89525e12da3e0d8401259c544d'
    assert 'GetThreadContext(peer.handle,&v)&&hardware_context(v,base+sites[10]),"continuous hardware coverage"' in source
    stderr = (capture/'stderr.txt').read_text().strip()
    assert stderr == 'continuous hardware coverage win32=0'
    traps = [r for r in control if r['action'] == 'TRAP_CONTEXT']
    fatal = [r for r in control if r['action'] == 'CONTROLLER_FATAL']
    assert len(traps) == len(fatal) == 1
    trap = traps[0]
    assert trap['site'] == 7 and trap['rip'] == session['sites'][7]+1
    assert trap['exception_address']-session['module_base'] == 0x79de92
    assert trap['exception_code'] == 0x80000003 and not trap['eflags'] & 0x100
    assert fatal[0]['debug_event_sequence'] == trap['debug_event_sequence']
    byte = next(r for r in control if r['action'] == 'TRAP_BYTE')
    assert byte['site'] == 7 and byte['actual'] == byte['expected'] == 0xcc
    peers = [r for r in control if r['action'] == 'PEER_SUSPENDED']
    assert len({(r['peer_tid'], r['peer_lifetime']) for r in peers}) == len(peers) == 85
    assert not any(r['action'] in ('SITES_VERIFIED', 'PATCH_RESTORED', 'HARDWARE_RESUMED') for r in control)
    assert not any(r['kind'] == 'SAMPLE' for r in events)
    intents = [r for r in control if r['action'] == 'CONTINUE_INTENT']
    results = [r for r in control if r['action'] == 'CONTINUE_RESULT']
    assert len(intents) == len(results) == 346
    assert [(r['debug_event_sequence'], r['disposition']) for r in intents] == [
        (r['debug_event_sequence'], r['disposition']) for r in results]
    assert all(r['ok'] and not r['error'] for r in results)
    assert control[-1]['action'] == 'CONTROL_END'
    assert control[-1]['owned_remaining'] == control[-1]['plain_remaining'] == 0
    cleanup = events[-1]
    assert cleanup == dict(kind='FAILURE_CLEANUP', termination_requested=True,
                           continued=True, exit_observed=True)
    reduced = read(review)
    assert reduced['journal_sha256'] == pin(capture/'events.jsonl')
    assert reduced['receipts'] == 1 and not reduced['reduction']['synthetic']
    assert not reduced['reduction']['decisions'] and not reduced['reduction']['chains']
    assert read(capture/'controller-exit.json') == dict(exit_code=2, requested_stop=False)
    paths = [capture/n for n in ('events.jsonl', 'control.jsonl', 'stderr.txt', 'controller-exit.json')]
    paths += [review, controller, Path(__file__)]
    return dict(schema='sor-d5n-postmortem/1',
        inputs=[dict(path=str(p.resolve()), sha256=pin(p)) for p in paths],
        session_identity={k: session[k] for k in ('pid', 'creation_filetime_100ns', 'module_base')},
        event_rows=len(events), control_rows=len(control),
        event_counts=dict(Counter(r['kind'] for r in events)),
        control_counts=dict(Counter(r['action'] for r in control)),
        trap=trap, trap_byte=byte, fatal=fatal[0], peer_count=len(peers),
        continuation_pairs=len(results), cleanup=cleanup, control_end=control[-1],
        scientific_result='INCOMPLETE; barrier only; zero samples, decisions and chains',
        target_outcome='Controller failure followed by authorized termination/drain',
        failure_boundary='Combined peer GetThreadContext and hardware_context requirement',
        unresolved=['Affected peer identity and actual debug-register values were not recorded.',
                    'API failure versus hardware-state mismatch and its onset remain UNKNOWN.',
                    'LastError zero is not proof that every context API succeeded.',
                    'No Grid-clear exception/sample or historical missing-delivery mechanism is established.'],
        limits='Diagnostic reduction of this completed session; receipt authentication is a separate method.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('capture', 'review', 'controller', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    assert all(p.resolve().is_relative_to(LOCAL.resolve()) for p in vars(args).values())
    result = analyze(args.capture, args.review, args.controller)
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(result['scientific_result'])
    print(result['target_outcome'])


if __name__ == '__main__':
    main()
