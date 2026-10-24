# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise only owned disposable Windows targets through the real debugger.

Reads pinned build files and target-owned memory; writes new ignored receipts.
Uses installed Python stdlib and the owned SRO1 transport. Never opens retail,
saves or configuration. No network, installation, Git mutation or live approval.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
from readiness import Tracker

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-selection-context'
spec = importlib.util.spec_from_file_location('transport', ROOT / 'research/resource-oracle-retail/collect.py')
transport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)


def independent(path):
    """Check receipt bytes independently of the writer before acknowledging."""
    raw = path.read_bytes()
    at, rows = 0, []
    while at < len(raw):
        magic, seq, n, digest = struct.unpack_from('<4sQI32s', raw, at)
        at += 48
        assert magic == b'SRO1' and seq == len(rows) + 1 and n <= 1048576
        body = raw[at:at+n]
        at += n
        assert len(body) == n and hashlib.sha256(body).digest() == digest
        rows.append(json.loads(body))
    ack = json.loads(path.with_suffix('.ack.json').read_text())
    assert at == len(raw) and ack['sha256'] == transport.pin(path) and ack['bytes'] == len(raw)
    assert [r['kind'] for r in rows] == ['SESSION', 'SAMPLE', 'END']
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    build, out = a.build.resolve(), a.output.resolve()
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['exit_code'] == 0
    for p, h in manifest['files'].items():
        assert transport.pin(p) == h, p
    out.mkdir(exist_ok=False)
    results = []
    modes = ('inactive', 'active', 'alternate', 'candidate-reversed', 'first-success', 'current-precedence', 'rnam-precedence', 'fallback', 'nonuniform-mask', 'same-biom', 'wrong-family', 'nested', 'threads', 'wrong-workshop',
             'wrong-owner', 'wrong-source', 'wrong-query', 'partial-descriptor',
             'partial-dnam', 'bad-count', 'bad-rnam', 'bad-node', 'bad-index',
             'byte-budget', 'guard-mismatch', 'injected-context-failure', 'ackfail',
             'no-hit', 'cache-only', 'cache-then-generation', 'crash-before', 'crash-after', 'crash-during', 'completion')
    for mode in modes:
        folder = out / mode
        folder.mkdir()
        command = [str(build / 'sor-d4-fixture-controller.exe'), '--synthetic-fixture',
                   transport.pin(build / 'sor-d4-fixture.exe'), mode]
        transport.write(folder / 'config.json', dict(command=command, synthetic=True))
        rows = []
        tracker=Tracker('0005e0de')
        ready=[]
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        for line in p.stdout:
            row = json.loads(line)
            rows.append(row)
            if row['kind']!='SAMPLE':tracker.observe(row)
            if row['kind'] == 'SAMPLE':
                path = folder / f'capture-{row["capture"]:05d}.bin'
                transport.persist(path, [rows[0], row, dict(kind='END', complete=row['required_reads_complete'])], synthetic=True)
                assert independent(path)[1] == row
                ack = 'REJECT' if mode == 'ackfail' else f'ACK {row["capture"]}'
                useful=tracker.observe(row)
                ready.append(useful)
                if mode == 'completion' and useful:
                    ack += ' STOP'
                p.stdin.write(ack + '\n')
                p.stdin.flush()
        code = p.wait(timeout=15)
        stderr = p.stderr.read()
        transport.write(folder / 'events.json', rows)
        errors = []

        def check(ok, why):
            if not ok:
                errors.append(why)

        samples = [r for r in rows if r['kind'] == 'SAMPLE']
        calls = [r for r in samples if r['site'] == 'resource_call']
        stages = [r for r in samples if r['site'] == 'selection_stage']
        check(code == (2 if mode in ('guard-mismatch', 'injected-context-failure') else 0), 'controller exit')
        if mode in ('no-hit', 'crash-before', 'guard-mismatch', 'injected-context-failure'):
            check(not samples, 'no invented samples')
        elif mode=='cache-only':
            check([r['site'] for r in samples]==['provider_entry','selection_stage'] and not calls,'cache bypass remains unbound')
        elif mode == 'ackfail':
            check(len(samples) == 1 and rows[-1]['stopped'], 'reject ACK disposes target')
        elif mode == 'crash-during':
            check(not calls and any(r.get('invalidated_invocations') == 1 for r in rows), 'partial invocation disclosed')
        else:
            check(bool(calls), 'resource calls acquired')
            if mode not in ('nested', 'byte-budget', 'wrong-query', 'wrong-source', 'partial-descriptor', 'partial-dnam', 'wrong-owner', 'bad-count', 'bad-rnam', 'bad-node', 'bad-index'):
                check(all(r['required_reads_complete'] for r in samples), 'all required reads complete')
                check(all(r['selection_chain_complete'] for r in calls), 'complete upstream component mask chain')
            if mode in ('bad-count', 'bad-rnam', 'bad-node', 'bad-index', 'byte-budget', 'wrong-query', 'wrong-source', 'partial-descriptor', 'partial-dnam', 'wrong-owner'):
                check(any(not r['required_reads_complete'] for r in samples), 'invalid reads or identity reported')
            if mode not in ('byte-budget', 'wrong-query', 'wrong-source', 'nested'):
                initial = [r for r in stages if r['selection_stage'] == 0]
                check(all(struct.unpack('<ii', bytes.fromhex(r['initial_query_xy_i32']['raw'])) == (101, -201) for r in initial), 'initial query differs from later cells')
            if mode == 'threads':
                check(len({r['thread_lifetime'] for r in calls}) == 3, 'three thread lifetimes')
            if mode == 'nested':
                check([r['parent_token'] for r in calls] == [1, 0], 'nested generation tokens')
                check(any(not r['selection_chain_complete'] for r in calls), 'multiplex blind interval is explicit')
            if mode == 'wrong-workshop':
                check(all(r['workshop_binding'].startswith('UNKNOWN') for r in samples), 'unrelated matching bytes do not bind Workshop')
            if mode == 'completion':
                check(rows[-1]['stopped'] and sum(ready)==1, 'durable selected return receipt before disposal')
        if mode in ('inactive','active'):
            check([r['construction_mask_raw_u8'] for r in stages if r['selection_stage']==4]==[3 if mode=='active' else 8], 'initial sampled mask acquired at return')
        if mode in ('inactive', 'candidate-reversed', 'first-success', 'current-precedence', 'rnam-precedence', 'fallback', 'nonuniform-mask', 'same-biom', 'wrong-family'):
            candidates = [r for r in stages if r['selection_stage'] == 5]
            values = [struct.unpack_from('<I', bytes.fromhex(r['candidate_record']['raw']), 0x60)[0] for r in candidates]
            expected = ([] if mode in ('current-precedence','rnam-precedence') else [0x8ae7b] if mode=='first-success' else [0x95092] if mode == 'candidate-reversed' else [1332288, 0x95092] if mode == 'same-biom' else [0x8ae7b, 0x95092])
            check(values == expected, 'actual native-shaped iterator order')
            check([r['candidate_eligible_static_predicate'] for r in candidates] == ([False, True] if mode in ('same-biom', 'wrong-family') else [True]*len(expected)), 'candidate exclusion predicates')
        winners={'inactive':303,'candidate-reversed':303,'first-success':202,'current-precedence':101,'rnam-precedence':202,'fallback':101}
        if mode in winners:
            check(all(struct.unpack_from('<I',bytes.fromhex(r['selected_dnam']['raw']))[0]==winners[mode] for r in calls),'independent selected descriptor marker')
            descriptors={}
            for r in samples:
                for group in ('current_biom','alternate_biom'):
                    context=r.get(group,{})
                    for record in context.get('rsgds',[])+context.get('ordered_rnam',[]):
                        entries=record.get('ordered_entries',{})
                        if entries.get('status')=='COMPLETE':
                            data=bytes.fromhex(entries['raw'])
                            for i in range(0,len(data),0x238):descriptors[entries['address']+i+8]=data[i+8:i+0x238]
            check(all(descriptors.get(r['selected_dnam']['address'])==bytes.fromhex(r['selected_dnam']['raw']) for r in calls),'selected pointer and full bytes match acquired candidate entry')
            visits=[r for r in stages if r['selection_stage']==5]
            check(len(visits)==(0 if mode in ('current-precedence','rnam-precedence') else 1 if mode in ('candidate-reversed','first-success') else 2),'first-success or direct precedence visit count')
        if mode=='nonuniform-mask':
            check([r['construction_mask_raw_u8'] for r in stages if r['selection_stage']==4]==[1],'position-indexed initial mask')
            check(all(r['mask_register_raw']==1 for r in calls),'later mask does not replace initial multiplier mask')
            terminal=next(r for r in samples if r['site']=='provider_return')
            check(struct.unpack_from('<QQ',bytes.fromhex(terminal['output_map_prefix_at_return']['raw']))==(1,4),'target-owned initial and later mask table samples differ')
        if mode=='cache-then-generation':
            entries=[r for r in samples if r['site']=='provider_entry']
            generation=next(r for r in samples if r['site']=='generation_entry')
            check([r['provider_token'] for r in entries]==[1,2] and entries[0]['provider_entry_rsp']==entries[1]['provider_entry_rsp'],'same-frame provider reuse observed')
            check(generation['provider_token']==generation['upstream_provider_token']==2 and generation['upstream_biom_capture']>entries[1]['capture'] and generation['upstream_join'],'no cached pending record inherited')
        check(sum(r['kind'] == 'ACK_ACCEPTED' for r in rows) == len(samples), 'ACK accounting')
        if mode in ('guard-mismatch', 'injected-context-failure'):
            check(any(r['kind'] == 'LOSS' for r in rows), 'fatal loss explicit')
        result = dict(mode=mode, passed=not errors, errors=errors, exit=code,
                      samples=len(samples), stderr=stderr,
                      files={str(f): transport.pin(f) for f in folder.iterdir() if f.is_file()})
        transport.write(folder / 'result.json', result)
        results.append(result)
        print(mode, not errors, errors, stderr.strip(), flush=True)
    # Negative transport controls use separate corrupted derivatives only.
    original=next((out/'inactive').glob('capture-*.bin'))
    for label, payload in (('truncated',original.read_bytes()[:-1]),('digest',original.read_bytes()[:60]+bytes([original.read_bytes()[60]^1])+original.read_bytes()[61:])):
        derivative=out/(label+'.bin');derivative.write_bytes(payload)
        try:independent(derivative)
        except (AssertionError,struct.error):pass
        else:raise AssertionError('corrupt receipt accepted')
    transport.write(out / 'qualification.json' , dict(synthetic=True, build_sha256=transport.pin(build / 'build.json'), cases=results))
    return 0 if all(r['passed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
