# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate D5AB native fixtures and independently specified counterexamples.

Reads a completed ignored build and original schema-2 B1 evidence; writes only a
fresh ignored receipt directory and explicitly damaged copies of synthetic test
sessions. Standard library only. No native execution, live reads, save/database
changes, deployment, downloads or Git effects. Original evidence is never edited.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import shutil
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    build = (ROOT / sys.argv[1]).resolve()
    out = (ROOT / sys.argv[2]).resolve()
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    development='--development' in sys.argv[3:]
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['compilation']['pass_exit'] and manifest['source_unchanged']
    assert all(sha(build / p) == h for p, h in manifest['outputs'].items())
    reader_root=ROOT/'runtime/construction-winner' if '--current-reader' in sys.argv[3:] else build/'package-runtime'
    reader = module('d5ab_packaged_reader', reader_root / 'read_capture.py')
    reducer = module('d5ab_packaged_reducer', reader_root / 'reduce_v3.py')
    dll = sha(build / 'package-runtime/SorConstructionWinner.dll')
    native = []
    reductions = {}
    for case in manifest['cases']:
        if development and not case['pass_exit']:
            native.append(dict(case=case['case'],passed=False,preserved_failure=case['actual']))
            continue
        assert case['pass_exit'], case
        name = case['case']
        if name == 'guard-mismatch':
            assert json.loads((build / name / 'refused.json').read_text())['installed'] is False
            native.append(dict(case=name, passed=True))
            continue
        result = reader.inspect(build / name, dll)
        ready=json.loads((build/name/'ready.json').read_bytes())
        if 'worker_thread_id' in ready:
            assert ready['worker_thread_id']>0 and ready['worker_creation_filetime']>0
            challenge=json.loads((build/name/'ack-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json').read_bytes())
            assert all(challenge[k]==ready[k] for k in ('worker_thread_id','worker_creation_filetime'))
        reductions[name] = result
        # Primary oracle: explicit fixture actions, not reducer-inferred labels.
        expected = {'normal': 1, 'mask-zero': 1, 'later-bypass': 1,
                    'reserve-fail': 0, 'unknown-birth': 0, 'visited': 0,
                    'map-hit': 0, 'skip-sample': 0, 'interrupt': 0,
                    'in-flight-loss': 0, 'overlap-reset': 0, 'ready-only': 0,
                    'conflicting-mask':0,'unexpected-mask':0,'descriptor-change':1,'temporary-descriptor':0,
                    'unrelated-conversion':0,'post-reset-old-provider':0,'schedule-old-first':0,'schedule-fresh-first':1,
                    'reset-closeout':0,'edge':0,'corner':0,'null-cell':0,'orphan-sample':0,'bad-read':0,
                    'bad-source':0,'bad-descriptor':0,'source-absent':0,'selection-only':0,'nested':1,
                    'missing-lookup':0,'missing-descriptor':0,'missing-generator':0,'missing-sample':0,'prior-unknown':0,
                    'descriptor-collision':0,'reused-pointer':1,'reset':2,'clear':1,'destroy':1,'erase':1,
                    'representative':1,'concurrent':1,'competing':1,'loss-one':1,'loss-many':1,'saturation':1,'timing':1,
                    'stop-under-production':1,'burst':1,'write-fault':1,'flush-fault':1,'ack-fault':1,
                    'disk-fault':1,'ack-write-fault':1,'crash-before':0,'crash-after':1,'crash-sample':0,'sequence-wrap':1}
        if name in expected:
            assert len(result['chains']) == expected[name], (name, result['diagnostics'])
        if name == 'later-bypass':
            assert result['chains'][0]['later_bypass']
            assert len(result['identities'])==2 and len({j['allocation'] for j in result['identities']})==1
        if name == 'normal':
            assert not result['chains'][0]['later_bypass']
            assert result['chains'][0]['allocation']==result['identities'][0]['allocation']
        if name in ('write-fault', 'flush-fault', 'ack-fault', 'disk-fault', 'ack-write-fault'):
            assert not result['terminal_success'] and not result['complete_session']
        if name.startswith('crash-'):
            assert not result['complete_session']
        if name in ('burst','representative'):
            assert result['terminal']['drops'] == 0 and result['complete_session']
            if name=='representative':
                content=(build/name/'events.bin').read_bytes()
                observed={reader.decode(content[p+16:p+328])['kind'] for p in range(0,len(content),328)}
                assert observed==set(range(1,18)),observed
                assert result['terminal']['worker_timing_ticks'][3]['max']>=3*result['terminal']['qpc_frequency']
        native.append(dict(case=name, passed=True, chains=len(result['chains']),
                           complete_session=result['complete_session'],
                           fixture=json.loads((build/name/'fixture.json').read_bytes()) if (build/name/'fixture.json').exists() else None,
                           losses=result['terminal']['drops'] if result['terminal'] else None))
    base = build / 'normal'
    raw = (base / 'events.bin').read_bytes()
    events = [reader.decode(raw[p + 16:p + 328]) for p in range(0, len(raw), 328)]
    assert len(reducer.reduce(events, reader.reduce, reader.source_key)['chains']) == 1
    results = []

    def run(name, change, expected, loss=(0, 0)):
        values = copy.deepcopy(events)
        change(values)
        begin = time.perf_counter()
        result = reducer.reduce(values, reader.reduce, reader.source_key, *loss)
        actual = len(result['chains'])
        passed = actual == expected
        results.append(dict(case=name, expected=expected, actual=actual, passed=passed,
                            seconds=time.perf_counter() - begin,
                            input_sha256=hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest()))
        with (out/'semantic-progress.jsonl').open('a',encoding='utf8',newline='\n') as stream:
            stream.write(json.dumps(results[-1])+'\n');stream.flush()
        assert passed, (name, result)

    def boundary(values, kind):
        return next(e for e in values if e['kind'] == kind)

    def field(kind, name, value):
        return lambda values: boundary(values, kind).__setitem__(name, value)

    def omit(kind):
        def change(values):
            values[:] = [e for e in values if e['kind'] != kind]
            for n, e in enumerate(values, 1):
                e['sequence'] = n
        return change

    def interleaved_unknown(values):
        extra=copy.deepcopy(boundary(values,2));extra['source']=1;extra['invocation']=990;extra['selection']=991
        at=next(i for i,e in enumerate(values) if e['kind']==2)+1
        values.insert(at,extra)
        for n,e in enumerate(values,1):e['sequence'],e['ticks']=n,n*100
    run('interleaved-unknown-selection',interleaved_unknown,0)
    def rebirth(values):
        copied=[copy.deepcopy(boundary(values,k)) for k in (14,15)]
        copied[0]['selection']=777
        at=next(i for i,e in enumerate(values) if e['kind']==1)+1
        values[at:at]=copied
        for n,e in enumerate(values,1):e['sequence'],e['ticks']=n,n*100
    run('same-pointer-rebirth-after-entry',rebirth,0)
    run('same-thread-equal-birth-publication-ticks',lambda values:boundary(values,15).__setitem__('ticks',boundary(values,14)['ticks']),1)
    run('same-thread-publication-equals-entry-ticks',lambda values:boundary(values,15).__setitem__('ticks',boundary(values,1)['ticks']),1)
    def ambiguous_ticks(values):
        for kind in (14,15):boundary(values,kind).update(ticks=boundary(values,1)['ticks'],thread=999)
    run('cross-thread-ambiguous-birth-order',ambiguous_ticks,0)
    run('unmatched-lifecycle-before-birth',field(14,'hazards',1),0)
    def unmatched_fence(values):
        e=copy.deepcopy(boundary(values,10));e['a']=4
        at=next(i for i,row in enumerate(values) if row['kind']==14)
        values.insert(at,e)
        for n,row in enumerate(values,1):row['sequence'],row['ticks']=n,n*100
    run('unmatched-lifecycle-contradicts-zero-hazard',unmatched_fence,0)
    run('zero-allocation-identity',field(14,'selection',0),0)
    run('cold-loss-generation-mismatch',field(12,'c',1),0)
    run('positive-no-later-bypass', lambda values: None, 1)
    run('direct-mask-zero', field(7, 'a', 0), 1)
    for kind in (1, 2, 3, 4, 5, 6, 7, 8, 12, 14, 15, 16, 17):
        run(f'missing-kind-{kind}', omit(kind), 0)
    for name, kind, key, value in (
        ('reserve-failure', 16, 'a', 0xffffffff), ('count-corrupt', 16, 'c', 0),
        ('store-wrong-token', 17, 'b', 999), ('store-wrong-address', 17, 'a', 1),
        ('reset-before-append', 17, 'epoch', 999), ('overlapping-epoch', 3, 'epoch', 999),
        ('store-wrong-frame', 17, 'frame', 1), ('store-wrong-thread', 17, 'thread', 1),
        ('store-invalid-lifetime', 17, 'status', 8), ('lifetime-loss', 3, 'c', 1),
        ('post-sample-loss', 17, 'c', 1), ('unknown-birth-status', 14, 'status', 1),
        ('constructor-not-published', 15, 'a', 0), ('unvisited-map-hit', 4, 'a', 0),
        ('unexpected-mask', 7, 'a', 255)):
        run(name, field(kind, key, value), 0)
    def altered_definition(values):
        e=boundary(values,4);data=bytearray.fromhex(e['source_bytes']);data[0x44]^=1;e['source_bytes']=data.hex()
    run('same-key-token-different-ancestry',altered_definition,0)
    def non_target(values):
        for e in values:
            if e['kind'] in (4,5,6,7,8,9,14,16,17):
                data=bytearray.fromhex(e['source_bytes']);struct.pack_into('<I',data,0,0x12345);e['source_bytes']=data.hex()
    run('complete-non-target-lifecycle',non_target,1)
    run('duplicate-sequence', lambda values: values.append(copy.deepcopy(values[0])), 0)
    run('missing-admission', lambda values: values.pop(4), 0)
    run('out-of-order-arrival', lambda values: random.Random(547).shuffle(values), 1)
    store = boundary(events, 17)['sequence']
    cold = boundary(events, 12)['sequence']
    run('loss-before-first-selection', lambda values: None, 0, (cold + 1, cold + 1))
    run('loss-before-append', lambda values: None, 0, (store - 1, store - 1))
    run('loss-after-append-keeps-earlier-proof', lambda values: None, 1, (store + 1, store + 1))
    run('loss-before-new-empty-boundary', lambda values: None, 1, (1, 1))

    def insert_prior(values, same_token):
        # Independent explicit earlier source lifecycle: a prior bypass on the
        # same geography/different token, or another geography/equal token.
        copied = [copy.deepcopy(boundary(values, k)) for k in (14, 15, 1, 2, 3)]
        for e in copied:
            e['source'] = 0x12340000
            e['selection'] = 900 if e['kind'] in (14, 15) else 901
            if e['kind'] in (1, 2, 3):
                e['invocation'] = 902
        copied[1]['thread'] = copied[0]['thread']
        token = copied[0]['a'] if same_token else copied[0]['a'] + 1
        data = bytearray.fromhex(copied[0]['source_bytes'])
        struct.pack_into('<Q', data, 0x68, token)
        if same_token:
            struct.pack_into('<I', data, 0, 0x12345)
        copied[0]['source_bytes'] = data.hex()
        copied[0]['a'] = token
        copied[-1]['a'], copied[-1]['b'] = 1, token
        at = next(i for i, e in enumerate(values) if e['kind'] == 14)
        values[at:at] = copied
        # This is a deliberately reconstructed causal fixture, never native data.
        for n, e in enumerate(values, 1):
            e['sequence'], e['ticks'] = n, n * 100
    run('equal-token-different-source', lambda values: insert_prior(values, True), 0)
    run('different-token-same-geography', lambda values: insert_prior(values, False), 0)
    for cause in (1, 2, 3, 4):
        def retirement(values, cause=cause):
            extra = copy.deepcopy(boundary(values, 10))
            extra['a'] = cause
            at = next(i for i, e in enumerate(values) if e['kind'] == 3)
            values.insert(at, extra)
            for n, e in enumerate(values, 1):
                e['sequence'], e['ticks'] = n, n * 100
        run(f'lifecycle-before-visited-{cause}', retirement, 0)

    damage = []
    for name in ('raw-truncated', 'raw-corrupt', 'ack-truncated', 'ack-corrupt', 'duplicate-frame', 'schema-mismatch', 'stale-identity'):
        dest = out / name
        shutil.copytree(base, dest)
        if name.startswith('raw-'):
            value = bytearray(raw)
            if name.endswith('truncated'):
                value = value[:(store-1)*328+10]
            else:
                value[20] ^= 1
            (dest / 'events.bin').write_bytes(value)
        elif name.startswith('ack-'):
            value = (dest / 'flush.jsonl').read_bytes()
            (dest / 'flush.jsonl').write_bytes(value.splitlines(keepends=True)[0][:-1] if name.endswith('truncated') else b'{broken}\n')
        elif name == 'duplicate-frame':
            (dest / 'events.bin').write_bytes(raw[:328] + raw)
        else:
            value = json.loads((dest / 'identity.json').read_bytes())
            value['schema' if name == 'schema-mismatch' else 'nonce'] = 'mismatched'
            (dest / 'identity.json').write_text(json.dumps(value), encoding='utf8')
        rejected = False
        try:
            result = reader.inspect(dest, dll)
            rejected = not result['complete_session'] and not result['chains']
        except (AssertionError, ValueError):
            rejected = True
        damage.append(dict(case=name, rejected=rejected))
        assert rejected, name
    ack_only=out/'crash-ack-only-loss'
    shutil.copytree(base,ack_only)
    (ack_only/'terminal.json').unlink()
    lines=[json.loads(line) for line in (ack_only/'flush.jsonl').read_text().splitlines()]
    for line in lines:
        line.update(first_loss_sampled_admission=5,last_loss_sampled_admission=9,loss_generation=1,drops=1)
    (ack_only/'flush.jsonl').write_text(''.join(json.dumps(line)+'\n' for line in lines),encoding='utf8',newline='\n')
    ack_result=reader.inspect(ack_only,dll)
    assert not ack_result['chains'] and not ack_result['complete_session']
    damage.append(dict(case='crash-ack-only-loss',rejected=True))
    # Historical B1 must retain exactly the frozen schema-2 interpretation.
    b1=ROOT/'.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'
    assert sha(b1/'events.bin')=='cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c'
    old=module('d5ab_historical_reader',ROOT/'.local-work/d5x/build24/package-runtime/read_capture.py')
    b1dll='20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb'
    old_result=old.inspect(b1,b1dll);new_result=reader.inspect(b1,b1dll)
    assert old_result==new_result
    compatibility=dict(schema='sor-d5x/2',raw_sha256=sha(b1/'events.bin'),byte_equivalent_result=True,
                       durable_records=new_result['durable_records'],chains=len(new_result['chains']))
    receipt = dict(schema='sor-d5ab-qualification/1', build=str(build), build_sha256=sha(build / 'build.json'),
                   reader_sha256=sha(reader_root / 'read_capture.py'),
                   reducer_sha256=sha(reader_root / 'reduce_v3.py'),
                   native=native, semantic_controls=results, damaged_sessions=damage, compatibility=compatibility,
                   oracle='Explicit fixture actions and independent expected constants; CRC implementation is zlib versus native bitwise CRC.',
                   native_game_validation=False, development_only=development)
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(native=len(native), semantic=len(results), damaged=len(damage), passed=not development)))


if __name__ == '__main__':
    main()
