# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify schema-4 consumers against disposable hosts and independent adverse oracles.

Reads owned consumers, completed native build receipts, pinned P2 schema-3 sessions and historical B1.
Adapted from owned d5ab_p2_reader.py; original P2 assertions remain preserved there.
Writes only a fresh ignored local receipt directory. Standard library only;
no game execution, process access, saves, network or Git mutation. Derivatives
are synthetic controls, never replacements for their original capture inputs.
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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    build, out = ((ROOT / value).resolve() for value in sys.argv[1:3])
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    out.mkdir(parents=True, exist_ok=False)
    src = ROOT / 'runtime/construction-winner'
    reader = load('p2_reader', src / 'read_capture.py')
    reducer = load('p1_reducer', src / 'reduce_v4.py')
    inputs = {str(p): sha(p) for p in (src / 'read_capture.py', src / 'reduce_v3.py', src / 'reduce_v4.py', Path(__file__))}
    manifest = json.loads((build / 'build.json').read_bytes())
    assert manifest['compilation']['pass_exit'] and manifest['source_unchanged']
    assert all(sha(build / p) == digest for p, digest in manifest['outputs'].items())
    dll = sha(build / 'package-runtime/SorConstructionWinner.dll')
    consumer_match = all(sha(build/'package-runtime'/name)==sha(src/name)
                         for name in ('read_capture.py','reduce_v3.py','reduce_v4.py'))
    development = '--development' in sys.argv[3:]
    assert development or consumer_match, 'Final qualification requires the exact packaged consumers'
    native_cases=manifest['cases']
    if '--original-case-regressions' in sys.argv[3:]:
        # P3 runs its new cases with an independent native-state oracle driver.
        # Reuse this full historical suite without guessing new case verdicts.
        original_build=ROOT/'.local-work/d5x/p1-native03/build.json'
        original_names={row['case'] for row in json.loads(original_build.read_bytes())['cases']}
        assert original_names <= {row['case'] for row in native_cases}
        native_cases=[row for row in native_cases if row['case'] in original_names]
    rows = []

    def record(case, passed, **details):
        row = dict(case=case, passed=bool(passed), **details)
        rows.append(row)
        with (out / 'progress.jsonl').open('a', encoding='utf8', newline='\n') as stream:
            stream.write(json.dumps(row) + '\n')
            stream.flush()
        assert passed, row

    positives = {'p1-noaccess-lookup', 'normal', 'mask-zero', 'descriptor-change', 'schedule-fresh-first',
                 'nested', 'reused-pointer', 'reset', 'clear', 'destroy', 'erase',
                 'representative', 'later-bypass', 'sequence-wrap', 'burst'}
    for native in native_cases:
        name = native['case']
        assert native['pass_exit']
        if name == 'guard-mismatch':
            record('native-' + name, not json.loads((build / name / 'refused.json').read_bytes())['installed'])
            continue
        result = reader.inspect(build / name, dll)
        if name in positives:
            # A schema-4 join cannot cross a reset without a new birth witness.
            expected = 1
            record('native-positive-' + name, len(result['chains']) == expected,
                   chains=len(result['chains']), records=result['durable_records'])
        elif name in ('concurrent', 'competing', 'loss-one', 'loss-many', 'saturation', 'timing',
                      'stop-under-production', 'write-fault', 'flush-fault', 'ack-fault',
                      'disk-fault', 'ack-write-fault', 'crash-before', 'crash-after', 'crash-sample'):
            # These fixtures may preserve an earlier valid witness prefix, but
            # loss/fault/incomplete closeout must suppress finalized firstness.
            if result['firstness_refusals']:
                record('native-refusal-' + name, not result['chains'],
                       refusals=result['firstness_refusals'], candidates=len(result['candidate_chains']))
            else:
                record('native-complete-' + name, result['complete_session'], chains=len(result['chains']))
        else:
            record('native-negative-' + name, not result['chains'], records=result['durable_records'])
        record('native-lifetime-unqualified-' + name,
               result['native_source_lifetime_qualified'] is False and result['scientific_firstness_qualified'] is False)
        if name in ('normal','later-bypass','p1-noaccess-lookup','p1-retire-lookup',
                    'p1-reset-lookup','p1-unpublished','p1-constructor-exception'):
            payload=(build/name/'events.bin').read_bytes()
            observed=[reader.decode(payload[i+16:i+328]) for i in range(0,len(payload),328)]
            counts={kind:sum(e['kind']==kind for e in observed) for kind in (1,3,4,14,15,17)}
            expected={1:1,3:1,4:1,14:1,15:1,17:1}
            if name=='later-bypass':expected.update({1:2,3:2})
            if name=='p1-unpublished':expected[15]=0
            if name=='p1-constructor-exception':expected.update({1:0,3:0,4:0,15:0,17:0})
            record('native-explicit-boundaries-'+name,counts==expected,actual=counts,expected=expected)
            record('native-zero-lookup-source-payload-'+name,
                   all(bytes.fromhex(e['source_bytes'])==bytes(0x70) for e in observed if e['kind']==4))
            if name in ('p1-retire-lookup','p1-reset-lookup'):
                record('native-lookup-invalidates-'+name,
                       any(e['kind']==4 and e['status']&8 for e in observed) and not result['chains']
                       and len(result['identities'])==1,
                       scope='The earlier visited identity survives; continuity through lookup does not.')

    base = build / 'normal'
    raw = (base / 'events.bin').read_bytes()
    events = [reader.decode(raw[p + 16:p + 328]) for p in range(0, len(raw), 328)]

    def boundary(values, kind):
        return next(e for e in values if e['kind'] == kind)

    def semantic(name, change, expected=0, loss=(0, 0)):
        values = copy.deepcopy(events)
        change(values)
        result = reducer.reduce(values, reader.reduce, reader.source_key, *loss)
        record('semantic-' + name, len(result['chains']) == expected,
               expected=expected, actual=len(result['chains']),
               derivative_sha256=hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest())

    semantic('no-artificial-later-bypass', lambda values: None, 1)
    semantic('mask-zero', lambda values: boundary(values, 7).__setitem__('a', 0), 1)
    for kind in (1,2,3,4,5,6,7,8,12,14,15,16,17):
        def omit(values, kind=kind):
            values[:] = [e for e in values if e['kind'] != kind]
            for index, event in enumerate(values, 1):
                event['sequence'] = index
        semantic('missing-boundary-' + str(kind), omit)
    for name, kind, field, value in (
        ('failed-reserve',16,'a',0xffffffff), ('invalid-capacity',16,'c',0),
        ('unexecuted-store-token',17,'b',1), ('wrong-store-destination',17,'a',1),
        ('cross-epoch-store',17,'epoch',999), ('cross-thread-store',17,'thread',999),
        ('cross-epoch-visited',3,'epoch',999), ('store-hazard',17,'hazards',1),
        ('missing-publication',15,'a',0), ('birth-ambiguity',14,'status',1),
        ('unknown-allocation',14,'selection',0), ('low-pointer',14,'source',1),
        ('map-hit',4,'a',0), ('visited-bypass',3,'a',1), ('outside-mask',7,'a',255),
        ('reverse-store-clock',17,'ticks',1), ('store-loss-generation',17,'c',1)):
        semantic(name, lambda values,k=kind,f=field,v=value: boundary(values,k).__setitem__(f,v))
    for field,value in (('status',16),('hazards',1),('epoch',999),('proc',1),('source',1),
                        ('thread',1),('request',[999,999]),('frame',1),('parent',999)):
        semantic('generated-' + field,
                 lambda values,f=field,v=value: boundary(values,8).__setitem__(f,v))
    for kind, label in ((1,'entry'),(2,'selection'),(14,'allocation')):
        def duplicate(values, kind=kind):
            at = next(i for i,e in enumerate(values) if e['kind']==kind)
            values.insert(at, copy.deepcopy(values[at]))
            for index,event in enumerate(values,1):
                event['sequence'],event['ticks']=index,index*100
        semantic('duplicate-' + label, duplicate)
    store = boundary(events,17)['sequence']
    semantic('loss-before-append',lambda values: None,loss=(store-1,store-1))
    semantic('loss-after-append-prefix-only',lambda values: None,1,loss=(store+1,store+1))
    semantic('cross-thread-birth-clock-tie',lambda values: boundary(values,14).update(
        ticks=boundary(values,1)['ticks'],thread=999))
    for schedule in ('before-store','tied-store','after-store'):
        def delayed_retirement(values,schedule=schedule):
            store=boundary(values,17)
            fence=copy.deepcopy(boundary(values,10))
            ticks=((store['ticks']+boundary(values,3)['ticks'])//2 if schedule=='before-store'
                   else store['ticks'] if schedule=='tied-store' else values[-1]['ticks']+1)
            fence.update(a=4,sequence=values[-1]['sequence']+1,thread=999,epoch=store['epoch'],ticks=ticks)
            values.append(fence)
        # This models ambiguous evidence, not a proved feasible native schedule.
        semantic('delayed-admission-retirement-'+schedule,delayed_retirement,
                 1 if schedule=='after-store' else 0)

    def derivative(name, mutation):
        dest = out / name
        dest.mkdir()
        for file in ('identity.json','ready.json','terminal.json','events.bin','flush.jsonl'):
            shutil.copyfile(base / file,dest / file)
        mutation(dest)
        hashes={p.name:sha(p) for p in dest.iterdir()}
        try:
            result = reader.inspect(dest,dll)
        except (AssertionError, ValueError, TypeError, KeyError):
            record('damage-' + name,True,identity_or_schema_rejected=True,inputs=hashes)
        else:
            record('damage-' + name,not result['chains'] and bool(result['firstness_refusals']),
                   durable=result['durable_records'],candidates=len(result['candidate_chains']),
                   damage=result['damage'],refusals=result['firstness_refusals'],inputs=hashes)
            if name in ('duplicate-ack','regressing-ack','torn-tail-after-valid-prefix','missing-terminal','late-loss',
                        'missing-ready','terminal-output-fault-count','terminal-output-fault-name'):
                record('lower-evidence-retained-' + name,
                       result['durable_records']==len(events) and len(result['candidate_chains'])==1)

    def alter_json(folder,file,key,value):
        path=folder/file
        data=json.loads(path.read_bytes());data[key]=value
        path.write_text(json.dumps(data)+'\n',encoding='utf8',newline='\n')

    def alter_ack(folder,key,value):
        path=folder/'flush.jsonl'
        lines=path.read_bytes().splitlines(keepends=True)
        data=json.loads(lines[0]);data[key]=value
        path.write_bytes((json.dumps(data)+'\n').encode()+b''.join(lines[1:]))

    def conflicting_ack_loss(folder):
        path=folder/'flush.jsonl'
        lines=[json.loads(line) for line in path.read_bytes().splitlines()]
        for line in lines:
            line.update(drops=1,queue_full=1,first_loss_sampled_admission=0,last_loss_sampled_admission=0)
        path.write_text(''.join(json.dumps(line)+'\n' for line in lines),encoding='utf8',newline='\n')

    for name, mutation in (
        ('duplicate-ack',lambda p:(p/'flush.jsonl').write_bytes((p/'flush.jsonl').read_bytes()*2)),
        ('regressing-ack',lambda p:(p/'flush.jsonl').write_bytes(b''.join(reversed((p/'flush.jsonl').read_bytes().splitlines(keepends=True))))),
        ('malformed-ack',lambda p:(p/'flush.jsonl').write_bytes(b'null\n')),
        ('boolean-ack-count',lambda p: alter_ack(p,'records',True)),
        ('negative-ack-count',lambda p: alter_ack(p,'records',-1)),
        ('ack-loss-type',lambda p: alter_ack(p,'drops','unknown')),
        ('ack-loss-terminal-denial',conflicting_ack_loss),
        ('torn-ack',lambda p:(p/'flush.jsonl').write_bytes((p/'flush.jsonl').read_bytes()[:-1])),
        ('crc-damage-first-frame',lambda p:(p/'events.bin').write_bytes(raw[:20]+bytes([raw[20]^1])+raw[21:])),
        ('torn-tail-after-valid-prefix',lambda p:(p/'events.bin').write_bytes(raw+b'x')),
        ('missing-terminal',lambda p:(p/'terminal.json').unlink()),
        ('missing-ready',lambda p:(p/'ready.json').unlink()),
        ('terminal-output-fault-count',lambda p:alter_json(p,'terminal.json','output_faults',1)),
        ('terminal-output-fault-name',lambda p:alter_json(p,'terminal.json','output_fault','write')),
        ('terminal-not-final',lambda p:alter_json(p,'terminal.json','acknowledged',0)),
        ('terminal-failed',lambda p:alter_json(p,'terminal.json','failed',True)),
        ('terminal-negative-count',lambda p:alter_json(p,'terminal.json','written',-1)),
        ('terminal-loss-accounting',lambda p:alter_json(p,'terminal.json','queue_full',1)),
        ('late-loss',lambda p:alter_json(p,'terminal.json','drops',1)),
        ('stale-session',lambda p:alter_json(p,'identity.json','nonce','f'*64)),
        ('unsupported-schema',lambda p:alter_json(p,'identity.json','schema','sor-d5x/999')),
        ('mismatched-terminal-identity',lambda p:alter_json(p,'terminal.json','nonce','f'*64))):
        derivative(name,mutation)

    # The bypass oracle uses the separately recorded native later-bypass case.
    SIZE=reader.SIZE+16
    bypass_raw=(build/'later-bypass/events.bin').read_bytes()
    bypass_events=[reader.decode(bypass_raw[i+16:i+SIZE]) for i in range(0,len(bypass_raw),SIZE)]
    bypass_invocation=[e['invocation'] for e in bypass_events if e['kind']==3 and e['a']==1][0]

    def bypass_case(name, change, expected_chains=1, expected_later=False, expected_identities=1):
        values=copy.deepcopy(bypass_events)
        change(values)
        for index,event in enumerate(values,1):event['sequence']=index
        result=reducer.reduce(values,reader.reduce,reader.source_key)
        passed=(len(result['chains'])==expected_chains and
                len(result['identities'])==expected_identities and
                all(c['later_bypass']==expected_later for c in result['chains']))
        record('bypass-'+name,passed,chains=len(result['chains']),identities=len(result['identities']),
               expected=[expected_chains,expected_later,expected_identities])

    def bypass_boundary(values,kind):
        return next(e for e in values if e['invocation']==bypass_invocation and e['kind']==kind)

    bypass_case('qualified-positive',lambda values:None,expected_later=True,expected_identities=2)
    for kind in (1,2,3):
        bypass_case('missing-'+str(kind),lambda values,k=kind:values.__setitem__(slice(None),[
            e for e in values if not(e['invocation']==bypass_invocation and e['kind']==k)]))
    for kind in (1,2,3):
        bypass_case('duplicate-'+str(kind),lambda values,k=kind:values.append(copy.deepcopy(bypass_boundary(values,k))))
    for kind,field,value in ((1,'proc',1),(1,'thread',999),(2,'frame',1),(2,'source',1),
                             (2,'thread',999),(3,'a',255),(3,'frame',1),(3,'ticks',1)):
        bypass_case(str(kind)+'-'+field,lambda values,k=kind,f=field,v=value:bypass_boundary(values,k).__setitem__(f,v))
    for tie in (False,True):
        def invert(values,tie=tie):
            store=boundary(values,17)
            for e in values:
                if e['invocation']==bypass_invocation:
                    e['thread']=999
                    e['ticks']=store['ticks']-(0 if tie else 10)+(e['kind']-3)
        bypass_case('native-tie' if tie else 'native-admission-inversion',invert,
                    expected_chains=0,expected_identities=2)

    semantic('padding-excluded',lambda values:boundary(values,14).__setitem__(
        'source_bytes',(bytes.fromhex(boundary(values,14)['source_bytes'])[:0x39]+bytes([1,2,3])+
                        bytes.fromhex(boundary(values,14)['source_bytes'])[0x3c:]).hex()),1)
    semantic('unexpected-lookup-copy',lambda values:boundary(values,4).__setitem__(
        'source_bytes',boundary(values,14)['source_bytes']))
    for kind in (1,3,4):
        semantic('unobserved-invalidation-epoch-'+str(kind),lambda values,k=kind:boundary(values,k).__setitem__('epoch',999))
    semantic('publication-wrong-epoch',lambda values:boundary(values,15).__setitem__('epoch',999))

    def prior_collision(values, same_token, same_geography):
        # Independently authored second allocation and earlier eligible decision.
        copied=[copy.deepcopy(boundary(values,k)) for k in (14,15,1,2,3)]
        token=copied[0]['a'] if same_token else copied[0]['a']+1
        for event in copied:
            event['source']=0x12340000
            event['selection']=900 if event['kind'] in (14,15) else 901
            if event['kind'] in (1,2,3):event['invocation']=902
        data=bytearray.fromhex(copied[0]['source_bytes'])
        struct.pack_into('<Q',data,0x68,token)
        if not same_geography:struct.pack_into('<I',data,0,0x12345)
        copied[0].update(source_bytes=data.hex(),a=token)
        copied[-1].update(a=1,b=token)
        at=next(i for i,event in enumerate(values) if event['kind']==14)
        values[at:at]=copied
        for index,event in enumerate(values,1):event['sequence'],event['ticks']=index,index*100

    semantic('equal-token-different-geography',lambda values:prior_collision(values,True,False))
    semantic('equal-geography-different-token',lambda values:prior_collision(values,False,True))
    semantic('equal-geography-token-different-allocation',lambda values:prior_collision(values,True,True))

    def reallocate(values):
        copied=[copy.deepcopy(boundary(values,k)) for k in (14,15)]
        copied[0]['selection']=777
        at=next(i for i,event in enumerate(values) if event['kind']==1)+1
        values[at:at]=copied
        for index,event in enumerate(values,1):event['sequence'],event['ticks']=index,index*100
    semantic('same-address-reallocation-in-flight',reallocate)
    semantic('non-target-positive',lambda values:boundary(values,14).__setitem__(
        'source_bytes',(struct.pack('<I',0x12345)+bytes.fromhex(boundary(values,14)['source_bytes'])[4:]).hex()),1)

    # Current schema-3 interpretation must equal the accepted pinned P2 reader
    # for every retained native session, including intentionally damaged cases.
    old_build=ROOT/'.local-work/d5x/p2-native06'
    old_manifest=json.loads((old_build/'build.json').read_bytes())
    old_reader=load('p1_original_p2_reader',old_build/'package-runtime/read_capture.py')
    old_dll=sha(old_build/'package-runtime/SorConstructionWinner.dll')
    for native in old_manifest['cases']:
        if native['case']=='guard-mismatch':continue
        folder=old_build/native['case']
        record('schema3-equivalence-'+native['case'],reader.inspect(folder,old_dll)==old_reader.inspect(folder,old_dll))
    b1=ROOT/'.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'
    assert sha(b1/'events.bin')=='cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c'
    old=load('p2_original_schema2',ROOT/'.local-work/d5x/build24/package-runtime/read_capture.py')
    b1dll='20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb'
    old_result,new_result=old.inspect(b1,b1dll),reader.inspect(b1,b1dll)
    record('schema2-b1-byte-equivalent-result',old_result==new_result,
           raw_sha256=sha(b1/'events.bin'),durable_records=new_result['durable_records'])
    assert all(sha(path)==digest for path,digest in inputs.items())
    receipt=dict(schema='sor-d5ab-p1-reader/1',passed=True,build=str(build),
                 build_sha256=sha(build/'build.json'),dll_sha256=dll,inputs=inputs,
                 rows=rows,tests=len(rows),native_source_lifetime_qualified=False,
                 native_case_inventory=[row['case'] for row in native_cases],
                 development_only=development,final_build_consumer_match=consumer_match)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(tests=len(rows),passed=True,out=str(out),final_build_consumer_match=receipt['final_build_consumer_match'])))


if __name__=='__main__':
    main()
