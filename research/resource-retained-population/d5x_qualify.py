# SPDX-License-Identifier: GPL-3.0-or-later
"""Check actual packaged native receipts and adversarial evidence derivatives.

Reads a completed D5X build and its packaged independent reader. Writes only a
fresh ignored qualification directory, explicit damaged copies and results. No
native execution here, no repairs to originals, no game/save/database/network or
Git mutation. CPython stdlib only. Altered semantic records are labelled derived
adversarial controls, never authentic native observations.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    assert build.is_relative_to(ROOT / '.local-work/d5x') and out.is_relative_to(ROOT / '.local-work/d5x')
    out.mkdir(exist_ok=False)
    manifest = json.loads((build / 'build.json').read_text())
    assert manifest['compilation']['pass_exit'] and manifest['source_unchanged']
    assert all(row['pass_exit'] for row in manifest['cases'])
    assert all(sha(build / name) == digest for name, digest in manifest['outputs'].items())
    reader_path = build / 'package-runtime/read_capture.py'
    spec = importlib.util.spec_from_file_location('packaged_reader', reader_path)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    dll = sha(build / 'package-runtime/SorConstructionWinner.dll')
    expected_counts = dict(normal=1, **{'mask-zero':1,'conflicting-mask':0,'unexpected-mask':0,'descriptor-change':1,'temporary-descriptor':0,'unrelated-conversion':0,'post-reset-old-provider':0,'edge':2,'corner':4,
        'null-cell':0,'overlap-reset':0,'orphan-sample':0,'bad-read':0,'bad-source':0,'bad-descriptor':0,
        'source-absent':0,'selection-only':0,'visited':0,'map-hit':0,'skip-sample':0,'nested':1,'interrupt':0,
        'in-flight-loss':0,'missing-lookup':0,'missing-descriptor':0,'missing-generator':0,'missing-sample':0,
        'prior-unknown':0,'ready-only':0,'descriptor-collision':0,'reused-pointer':1,'reset':2,'clear':1,
        'destroy':1,'erase':1,'concurrent':9,'competing':2,'schedule-old-first':0,'schedule-fresh-first':1,'reset-closeout':0,'loss-one':2,'loss-many':2,'saturation':2,'timing':2,'stop-under-production':1,
        'write-fault':1,'flush-fault':1,'ack-fault':1,'disk-fault':1,'ack-write-fault':1,
        'crash-before':0,'crash-after':1,'crash-sample':1,'sequence-wrap':1})
    assert {row['case'] for row in manifest['cases']} == set(expected_counts) | {'guard-mismatch'}
    results = []
    reductions = {}
    nonces=set()
    for row in manifest['cases']:
        case = row['case']
        if case == 'guard-mismatch':
            refused = json.loads((build / case / 'refused.json').read_text())
            assert refused == dict(boundary='site_guard',installed=False)
            results.append(dict(case=case, passed=True, boundary='guard_refusal'))
            continue
        result = reader.inspect(build / case, dll)
        challenge = json.loads((build / case / 'ack-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json').read_bytes())
        identity = json.loads((build / case / 'identity.json').read_bytes())
        assert identity['nonce'] not in nonces
        nonces.add(identity['nonce'])
        assert challenge['request_nonce'] == 'a' * 32 and challenge['nonce'] == identity['nonce']
        assert challenge['hooks_intact'] and challenge['capture_active']
        reductions[case] = result
        (out / (case + '.json')).write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
        actual = len(result['chains'])
        expected = expected_counts[case]
        outcomes = sorted({entry['outcome'] for entry in result['diagnostics']})
        check = actual == expected
        if case == 'normal':
            check &= result['chains'][0]['mask'] == 3 and result['chains'][0]['target_identity']
        if case == 'mask-zero':
            check &= result['chains'][0]['mask'] == 0
        if case in ('normal','nested'):
            check &= all(chain['request']==[10,11] and chain['mask']==3 and chain['target_identity'] for chain in result['chains'])
        if case in ('concurrent','competing'):
            count=9 if case=='concurrent' else 2
            check &= all((tuple(chain['request']),chain['mask']) in (((10,11),3),((-2,-2),0)) for chain in result['chains'])
            check &= sum(chain['target_identity'] for chain in result['chains'])==2
            check &= len({chain['invocation'] for chain in result['chains']})==count
            check &= len({chain['selection'] for chain in result['chains']})==count
            check &= len({chain['thread'] for chain in result['chains']})==count
            raw=(build/case/'events.bin').read_bytes()
            records=[reader.decode(raw[offset+16:offset+328]) for offset in range(0,len(raw),328)]
            newest=max(e['epoch'] for e in records if e['kind']==1)
            calls={e['invocation'] for e in records if e['kind']==1 and e['epoch']==newest}
            check &= len(calls)==8
            check &= max(e['sequence'] for e in records if e['kind']==3 and e['invocation'] in calls)<min(e['sequence'] for e in records if e['kind']==4 and e['invocation'] in calls)
        if case in ('schedule-old-first','schedule-fresh-first'):
            raw=(build/case/'events.bin').read_bytes()
            records=[reader.decode(raw[offset+16:offset+328]) for offset in range(0,len(raw),328)]
            old=next(e for e in records if e['kind']==1 and e['request']==[-2,-2])
            fresh=next(e for e in records if e['kind']==1 and e['request']==[10,11])
            old_map=next(e for e in records if e['kind']==4 and e['invocation']==old['invocation'])
            fresh_map=next(e for e in records if e['kind']==4 and e['invocation']==fresh['invocation'])
            check &= old['epoch']<old_map['d']==fresh['epoch']==fresh_map['d']
            check &= old_map['sequence']<fresh_map['sequence'] if case=='schedule-old-first' else fresh_map['sequence']<old_map['sequence']
            if case=='schedule-fresh-first':check &= result['chains'][0]['invocation']==fresh['invocation'] and result['chains'][0]['mask']==3
        if case=='sequence-wrap':
            check &= result['complete_session'] and not result['damage'] and result['chains'][0]['sample_sequence']>2**32
        if case=='reset-closeout':
            raw=(build/case/'events.bin').read_bytes()
            records=[reader.decode(raw[offset+16:offset+328]) for offset in range(0,len(raw),328)]
            entries=[e for e in records if e['kind']==1]
            end=next(e for e in records if e['kind']==11 and e['sequence']>entries[0]['sequence'])
            during_map=next(e for e in records if e['kind']==4 and e['invocation']==entries[0]['invocation'])
            check &= len(entries)==2 and entries[0]['hazards']==1 and entries[1]['hazards']==0
            check &= during_map['sequence']<end['sequence']<entries[1]['sequence']
            check &= entries[0]['epoch']==during_map['d']==entries[1]['epoch']
        if case=='descriptor-change':
            check &= struct.unpack_from('<i',bytes.fromhex(result['chains'][0]['effective_descriptor']),4)[0]==196
        if case in ('loss-one', 'loss-many'):
            check &= result['terminal']['contention_exhausted'] == (1 if case == 'loss-one' else 37)
        if case == 'saturation':
            check &= result['terminal']['queue_full'] > 0 and result['complete_session']
        if case=='stop-under-production':
            check &= result['complete_session'] and result['durable_records']>13
        if case == 'crash-sample':
            check &= not result['complete_session'] and not result['chains'][0]['returned']
        if case == 'ready-only':
            check &= result['ready_installed'] and not result['native_activity_absence_proven']
        if case.endswith('fault'):
            check &= not result['complete_session'] and result['terminal']['output_faults'] > 0
        results.append(dict(case=case, expected=expected, actual=actual, outcomes=outcomes, passed=bool(check)))
    # Damage controls retain original bytes. No repaired derivative becomes evidence.
    damage = []
    for mode in ('torn-frame','payload-flip','torn-ack','wrong-identity','bad-sequence','truncated-prefix'):
        folder = out / mode
        shutil.copytree(build / 'normal', folder)
        raw = bytearray((folder / 'events.bin').read_bytes())
        if mode == 'torn-frame':
            raw = raw[:-7]
        elif mode == 'payload-flip':
            raw[16 + 8] ^= 1
        elif mode == 'bad-sequence':
            struct.pack_into('<I',raw,8,9)
        elif mode == 'truncated-prefix':
            raw = raw[:328]
        elif mode == 'torn-ack':
            (folder / 'flush.jsonl').write_bytes((folder / 'flush.jsonl').read_bytes()[:-3])
        elif mode == 'wrong-identity':
            identity = json.loads((folder / 'identity.json').read_bytes())
            identity['nonce'] = '0' * 64
            (folder / 'identity.json').write_text(json.dumps(identity) + '\n',encoding='utf8',newline='\n')
        (folder / 'events.bin').write_bytes(raw)
        try:
            result = reader.inspect(folder,dll)
            passed = not result['chains'] and not result['complete_session']
        except (AssertionError, ValueError):
            passed = True
        damage.append(dict(mode=mode,passed=passed))
    events = []
    original = (build / 'normal/events.bin').read_bytes()
    for offset in range(0,len(original),328):
        events.append(reader.decode(original[offset+16:offset+328]))
    adversarial = []
    for name, mutate in [
        ('sample-query-mismatch',lambda rows: next(e for e in rows if e['kind']==7).__setitem__('c',1)),
        ('source-mismatch',lambda rows: next(e for e in rows if e['kind']==7).__setitem__('source',1)),
        ('owner-context-mismatch',lambda rows: next(e for e in rows if e['kind']==7).__setitem__('proc',1)),
        ('request-mismatch',lambda rows: next(e for e in rows if e['kind']==7).__setitem__('request',[99,99])),
        ('missing-cold',lambda rows: rows.__setitem__(slice(None),[e for e in rows if e['kind']!=12])),
        ('missing-entry',lambda rows: rows.__setitem__(slice(None),[e for e in rows if e['kind']!=1])),
        ('epoch-mismatch',lambda rows: next(e for e in rows if e['kind']==7).__setitem__('epoch',999)),
        ('thread-mismatch',lambda rows: next(e for e in rows if e['kind']==7).__setitem__('thread',999999)),
    ]:
        rows = copy.deepcopy(events)
        mutate(rows)
        reduced = reader.reduce(rows)
        adversarial.append(dict(name=name,passed=not reduced['chains'],outcomes=[r['outcome'] for r in reduced['diagnostics']]))
    rows=copy.deepcopy(events)
    earlier=[copy.deepcopy(e) for e in events if e['kind'] in (1,2,3,4)]
    for e in earlier:
        e['invocation']=999;e['selection']=1000 if e['kind']!=1 else 0
        if e['kind']==4:e['a']=0
    returned=copy.deepcopy(earlier[-1]);returned['kind']=9;earlier.append(returned)
    index=next(i for i,e in enumerate(rows) if e['kind']==1)
    rows[index:index]=earlier
    for i,e in enumerate(rows):e['sequence']=i+1
    reduced=reader.reduce(rows)
    adversarial.append(dict(name='prior-hit-before-later-miss',passed=not reduced['chains'],outcomes=[r['outcome'] for r in reduced['diagnostics']]))
    rows=copy.deepcopy(events)
    orphan=copy.deepcopy(next(e for e in rows if e['kind']==7))
    orphan.update(invocation=0,parent=0,selection=0,proc=0,source=0,status=6)
    rows.append(orphan)
    for i,e in enumerate(rows):e['sequence']=i+1
    reduced=reader.reduce(rows)
    adversarial.append(dict(name='unscoped-native-activity',passed=not reduced['chains'],outcomes=[r['outcome'] for r in reduced['diagnostics']]))
    try:
        reader.inspect(build / 'normal','0'*64)
        wrong_dll = False
    except AssertionError:
        wrong_dll = True
    receipt = dict(schema='sor-d5x-qualification/1', build_sha256=sha(build/'build.json'),
                   dll_sha256=dll, reader_sha256=sha(reader_path), qualifier_sha256=sha(__file__),
                   native=results, damage=damage, semantic_derivatives=adversarial, wrong_dll_refused=wrong_dll,
                   passed=all(r['passed'] for r in results+damage+adversarial) and wrong_dll,
                   scope='Disposable native observation only; no retail qualification or historical winner')
    (out/'qualification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=receipt['passed'],native_failures=[r for r in results if not r['passed']],
                          damage=damage,semantic_derivatives=adversarial),indent=2))
    return 0 if receipt['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
