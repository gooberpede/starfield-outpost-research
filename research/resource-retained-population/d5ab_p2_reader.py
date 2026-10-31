# SPDX-License-Identifier: GPL-3.0-or-later
"""Qualify P2 consumers against a pinned disposable build and damaged copies.

Reads owned consumers, completed native build receipts and pinned historical B1.
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
    reducer = load('p2_reducer', src / 'reduce_v3.py')
    inputs = {str(p): sha(p) for p in (src / 'read_capture.py', src / 'reduce_v3.py', Path(__file__))}
    manifest = json.loads((build / 'build.json').read_bytes())
    assert manifest['compilation']['pass_exit'] and manifest['source_unchanged']
    assert all(sha(build / p) == digest for p, digest in manifest['outputs'].items())
    dll = sha(build / 'package-runtime/SorConstructionWinner.dll')
    consumer_match = all(sha(build/'package-runtime'/name)==sha(src/name)
                         for name in ('read_capture.py','reduce_v3.py'))
    development = '--development' in sys.argv[3:]
    assert development or consumer_match, 'Final qualification requires the exact packaged consumers'
    rows = []

    def record(case, passed, **details):
        row = dict(case=case, passed=bool(passed), **details)
        rows.append(row)
        with (out / 'progress.jsonl').open('a', encoding='utf8', newline='\n') as stream:
            stream.write(json.dumps(row) + '\n')
            stream.flush()
        assert passed, row

    positives = {'normal', 'mask-zero', 'descriptor-change', 'schedule-fresh-first',
                 'nested', 'reused-pointer', 'reset', 'clear', 'destroy', 'erase',
                 'representative', 'later-bypass', 'sequence-wrap', 'burst'}
    for native in manifest['cases']:
        name = native['case']
        assert native['pass_exit']
        if name == 'guard-mismatch':
            record('native-' + name, not json.loads((build / name / 'refused.json').read_bytes())['installed'])
            continue
        result = reader.inspect(build / name, dll)
        if name in positives:
            expected = 2 if name == 'reset' else 1
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

    b1=ROOT/'.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'
    assert sha(b1/'events.bin')=='cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c'
    old=load('p2_original_schema2',ROOT/'.local-work/d5x/build24/package-runtime/read_capture.py')
    b1dll='20160e2ccdf183c84baddae0214c0438eb471b3eb0ec34dee0632bb5880ddaeb'
    old_result,new_result=old.inspect(b1,b1dll),reader.inspect(b1,b1dll)
    record('schema2-b1-byte-equivalent-result',old_result==new_result,
           raw_sha256=sha(b1/'events.bin'),durable_records=new_result['durable_records'])
    assert all(sha(path)==digest for path,digest in inputs.items())
    receipt=dict(schema='sor-d5ab-p2-reader/1',passed=True,build=str(build),
                 build_sha256=sha(build/'build.json'),dll_sha256=dll,inputs=inputs,
                 rows=rows,tests=len(rows),native_source_lifetime_qualified=False,
                 development_only=development,final_build_consumer_match=consumer_match)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(tests=len(rows),passed=True,out=str(out),final_build_consumer_match=receipt['final_build_consumer_match'])))


if __name__=='__main__':
    main()
