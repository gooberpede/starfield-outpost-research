# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge schema-4 chronology with independently specified counterexamples.

Reads a completed owned disposable build and current consumers. Writes fresh
ignored receipts and every mutated event input; no target/process/save/network
or Git effects. Uses stdlib only. Adapted conceptually from the owned P1 reader
driver; expected results below are explicit contract oracles, not derived from
the consumer's verdict. Synthetic mutations are not claimed native schedules.
Use --development only while consumers differ from the packaged candidate.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    build, out = [(ROOT / a).resolve() for a in sys.argv[1:3]]
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'runtime/construction-winner'
    reader = load('p3_reader', source / 'read_capture.py')
    reducer = load('p3_reducer', source / 'reduce_v4.py')
    paths = [source / n for n in ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py')]
    paths.append(Path(__file__))
    pins = {str(p): sha(p) for p in paths}
    for p in paths:
        (out / p.name).write_bytes(p.read_bytes())
    match = all(sha(source / p.name) == sha(build / 'package-runtime' / p.name) for p in paths[:3])
    assert match or '--development' in sys.argv[3:]
    raw = (build / 'normal/events.bin').read_bytes()
    original = [reader.decode(raw[i+16:i+328]) for i in range(0, len(raw), 328)]
    rows = []

    def one(values, kind):
        return next(e for e in values if e['kind'] == kind)

    def test(name, edit, expected=0, losses=(0, 0)):
        values = copy.deepcopy(original)
        edit(values)
        for i, e in enumerate(values, 1):
            e['sequence'] = i
        path = out / (name + '.json')
        path.write_text(json.dumps(values, indent=2)+'\n', encoding='utf8', newline='\n')
        result = reducer.reduce(values, reader.reduce, reader.source_key, *losses)
        passed = len(result['chains']) == expected
        rows.append(dict(case=name, passed=passed, expected_chains=expected,
                         actual_chains=len(result['chains']), input_sha256=sha(path),
                         diagnostics=result['diagnostics'], identities=len(result['identities'])))

    test('positive-no-bypass', lambda v: None, 1)
    required = (1, 2, 3, 4, 5, 6, 7, 8, 12, 14, 15, 16, 17)
    for kind in required:
        test('missing-'+str(kind), lambda v, k=kind: v.__setitem__(slice(None), [e for e in v if e['kind'] != k]))
        def duplicate(v, k=kind):
            index = next(i for i,e in enumerate(v) if e['kind'] == k)
            v.insert(index, copy.deepcopy(v[index]))
        test('duplicate-'+str(kind), duplicate)
        def late_duplicate(v, k=kind):
            late = copy.deepcopy(one(v,k))
            late['ticks'] = max(e['ticks'] for e in v)+1
            v.append(late)
        test('late-duplicate-'+str(kind), late_duplicate)
    # Changing native time alone preserves admission order and challenges the
    # actual chronology premise rather than merely failing sequence validation.
    for kind in (1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17):
        test('native-time-reversed-'+str(kind), lambda v,k=kind: one(v,k).__setitem__('ticks', 1))
    test('birth-after-publication', lambda v: one(v,14).__setitem__('ticks',one(v,15)['ticks']+1))
    test('return-before-selection', lambda v: one(v,9).__setitem__('ticks',one(v,2)['ticks']-1))
    test('return-before-store', lambda v: one(v,9).__setitem__('ticks',one(v,17)['ticks']-1))
    test('duplicate-return', lambda v: v.append(copy.deepcopy(one(v,9))))
    test('missing-return-valid-store-prefix', lambda v: v.__setitem__(slice(None),[e for e in v if e['kind']!=9]),1)
    for kind in (3, 4, 5, 6, 7, 8, 16, 17):
        for field in ('proc', 'thread', 'frame', 'source', 'epoch', 'parent'):
            test('context-'+str(kind)+'-'+field, lambda v,k=kind,f=field: one(v,k).__setitem__(f, 999))
        test('context-'+str(kind)+'-request', lambda v,k=kind: one(v,k).__setitem__('request', [999, -999]))
    for field in ('selection', 'holder', 'source', 'epoch', 'thread'):
        test('publication-'+field, lambda v,f=field: one(v,15).__setitem__(f,999))
    for kind in (10, 11):
        # The ordinary empty reset needs both its begin and end fence.
        test('missing-empty-reset-'+str(kind), lambda v,k=kind: v.__setitem__(slice(None), [e for e in v if e['kind'] != k]))
    # A counterfeit early empty certificate must not borrow a much later end.
    test('reset-end-after-store', lambda v: one(v,11).__setitem__('ticks',one(v,17)['ticks']+100))
    test('reset-begin-after-cold', lambda v: one(v,10).__setitem__('ticks',one(v,12)['ticks']+100))
    test('cold-loss-generation', lambda v: one(v,12).__setitem__('c',1))
    test('reserve-destination', lambda v: one(v,16).__setitem__('d',1))
    test('store-token', lambda v: one(v,17).__setitem__('b',1))
    test('mask-zero-not-geometry', lambda v: one(v,7).__setitem__('a',0),1)
    test('loss-before-store',lambda v:None,losses=(one(original,17)['sequence']-1,one(original,17)['sequence']))
    test('loss-after-store-prefix-only',lambda v:None,1,losses=(one(original,17)['sequence']+1,one(original,17)['sequence']+1))
    for name in ('positive-loss-without-bounds','positive-loss-without-generation',
                 'terminal-zero-overrides-ack-loss','missing-zero-loss-generation','impossible-loss-bound',
                 'sampled-cause-incoherence'):
        dest=out/name;dest.mkdir()
        for file in ('identity.json','ready.json','terminal.json','events.bin','flush.jsonl'):
            shutil.copyfile(build/'normal'/file,dest/file)
        terminal=json.loads((dest/'terminal.json').read_bytes())
        acks=[json.loads(line) for line in (dest/'flush.jsonl').read_bytes().splitlines()]
        for e in [terminal,*acks]:
            if name!='missing-zero-loss-generation':
                e.update(drops=1,queue_full=1,contention_exhausted=0,reentrant_losses=0,
                         loss_generation=1,first_loss_sampled_admission=0,last_loss_sampled_admission=0,
                         loss_bounds_uncertain=False)
            if name in ('positive-loss-without-generation','missing-zero-loss-generation'):
                e.pop('loss_generation',None)
            if name=='impossible-loss-bound':
                e.update(first_loss_sampled_admission=terminal['enqueued']+2,
                         last_loss_sampled_admission=terminal['enqueued']+2)
            if name=='sampled-cause-incoherence':
                e.update(first_loss_sampled_admission=terminal['enqueued']+1,
                         last_loss_sampled_admission=terminal['enqueued']+1)
        if name=='sampled-cause-incoherence':acks[0]['queue_full']=0
        if name=='terminal-zero-overrides-ack-loss':
            for e in acks:
                e.update(first_loss_sampled_admission=one(original,17)['sequence'],
                         last_loss_sampled_admission=one(original,17)['sequence'])
        (dest/'terminal.json').write_text(json.dumps(terminal)+'\n',encoding='utf8',newline='\n')
        (dest/'flush.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in acks),encoding='utf8',newline='\n')
        result=reader.inspect(dest,sha(build/'package-runtime/SorConstructionWinner.dll'))
        rows.append(dict(case=name,passed=not result['reset_scoped_chains'] and
                         (name!='sampled-cause-incoherence' or result['durable_records']==len(original)),
                         expected_scoped_chains=0,actual_scoped_chains=len(result['reset_scoped_chains']),
                         retained_durable_records=result['durable_records'],
                         damage=result['damage'],refusals=result['firstness_refusals']))
    unchanged = all(sha(p)==digest for p,digest in pins.items())
    receipt = dict(schema='sor-d5ab-p3-reader/1', build=str(build),
                   build_sha256=sha(build/'build.json'), inputs=pins,
                   final_packaged_consumer_match=match, source_unchanged=unchanged,
                   scope='Synthetic semantic counterexamples; native scenarios qualified separately.',
                   tests=len(rows), failures=[r['case'] for r in rows if not r['passed']],rows=rows)
    receipt['passed'] = unchanged and not receipt['failures']
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('inputs','rows')},indent=2))
    return 0 if receipt['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
