# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently read actual D5AN diagnostics and adverse disposable copies.

Reads the exact completed native build and emitted identity/terminal files.
Writes fresh local reader receipts and explicitly mutated copies only. Uses
Python stdlib and the separately authored counter reader; never changes native
evidence, protected saves, a process, deployment, databases, Git or network.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
from d5am_lock_qualify import ROOT,guard,sha
from d5an_pe import inspect as inspect_pe

def require(value,message):
    if not value:raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build',type=Path);parser.add_argument('out',type=Path)
    args=parser.parse_args();build=args.build.resolve();out=args.out.resolve()
    require(all(p.is_relative_to(ROOT/'.local-work/d5an') for p in (build,out)),'Task-local paths required')
    free=guard();out.mkdir(exist_ok=False)
    source=ROOT/'runtime/construction-winner/d5an_read_counter.py'
    spec=importlib.util.spec_from_file_location('d5an_independent_counter_reader',source)
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    causal_source=ROOT/'runtime/construction-winner/d5an_read_causal.py'
    spec=importlib.util.spec_from_file_location('d5an_independent_causal_reader',causal_source)
    causal_reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(causal_reader)
    scheduler_source=ROOT/'runtime/construction-winner/d5am_read_scheduler.py'
    spec=importlib.util.spec_from_file_location('d5an_independent_scheduler_reader',scheduler_source)
    scheduler_reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(scheduler_reader)
    native=json.loads((build/'build.json').read_bytes());dll=sha(build/'SorConstructionWinner.dll')
    pe=inspect_pe(build/'SorConstructionWinner.dll')
    require(native['compilation']==0 and native['source_unchanged'] and dll==native['dll_sha256'],'Exact completed candidate required')
    require(all(c['pass_exit'] for c in native['cases']),'Native case failure remains')
    checks=[];results={};pins={str(source):sha(source),str(causal_source):sha(causal_source),str(Path(__file__)):sha(__file__),str(build/'build.json'):sha(build/'build.json'),str(build/'SorConstructionWinner.dll'):dll,str(Path(__file__).with_name('d5an_pe.py')):sha(Path(__file__).with_name('d5an_pe.py'))}
    pins[str(scheduler_source)]=sha(scheduler_source)
    def check(label,value):checks.append(dict(name=label,passed=bool(value)));require(value,label)
    expected={
        'd5an-overflow-core':(1,1,1),'d5an-before-owner':(1,1,1),'d5an-overflow-own':(2,1,1),
        'd5an-overflow-causal':(32,4,1),'d5an-causal-core':(33,4,1),
        'd5an-asm-core':(1,2,1),'d5an-asm-bridge':(8,3,1),
        'd5an-causal-asm-core':(33,5,1),'d5an-causal-asm-bridge':(42,6,1),
        'd5an-serial-publish':(9,7,1),'d5an-serial-retire':(10,8,1),
        'd5an-teardown':(32,10,2),'d5an-teardown-scheduler':(2,12,2),
        'd5an-teardown-core':(33,11,2),'d5an-written-scheduler':(11,9,1),
        'd5an-token-scheduler':(5,1,1),'d5an-stop-teardown':(2,12,2),
        'd5an-serial-native':(9,7,1)}
    roster={c['case'] for c in native['cases']}
    require(set(expected)<=roster,'Mandatory injected-source cases missing')
    for case in sorted(c for c in roster if c.startswith('d5an-')):
        session=build/case
        for p in session.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        value=reader.read(session,dll,build/'SorConstructionWinner.dll');results[case]=value
        identity=json.loads((session/'identity.json').read_bytes());module=identity['counter_dll_base']
        check(case+'-exact-helper-export-domain',identity['counter_helper_rva']==pe['exports']['D5AN_counter_next'] and identity['counter_leave_rva']==pe['exports']['D5AN_counter_leave'])
        if value['disposition']=='PUBLISHED_COUNTER_FAULT':
            check(case+'-exact-observer-object-return-domain',all(module<=value['first'][key]<module+pe['image_bytes'] for key in ('address','return_va')))
        if case in expected:
            check(case+'-specific-published-producer',value['disposition']=='PUBLISHED_COUNTER_FAULT' and
                tuple(value['first'][k] for k in ('id','producer','class'))==expected[case])
        elif case=='d5an-provenance-pending':
            check(case+'-partial-provenance-not-interpreted',value['disposition']=='INCOMPLETE_PUBLICATION' and not value['complete'] and 'first' not in value)
        else:
            check(case+'-valid-reader-disposition',case in ('d5an-contention','d5an-timing','d5an-scheduler-loss','d5an-scheduler-exhaustion') and value['disposition']=='NO_COUNTER_FAULT_RECORDED')
        terminal=json.loads((session/'terminal.json').read_bytes())
        frames=causal_reader.read(session,dll)
        task_frames=scheduler_reader.read(session,dll)
        check(case+'-actual-causal-frames-authenticated',frames['integrity']=='AUTHENTICATED_FRAMES')
        check(case+'-actual-scheduler-framing-read',isinstance(task_frames['events'],list))
        if terminal['failed']:
            check(case+'-hard-failure-refuses-causal-completeness',not frames['native_bridge_accounting_complete'])
            check(case+'-hard-failure-refuses-scheduler-completeness',not task_frames['native_bridge_accounting_complete'])
        if case in ('d5an-contention','d5an-timing'):
            check(case+'-actual-positive-health-and-causal-accounting',terminal['failed'] is False and frames['native_bridge_accounting_complete'] and task_frames['native_bridge_accounting_complete'])
        if case in ('d5an-scheduler-loss','d5an-scheduler-exhaustion'):
            check('queue-loss-failed-terminal-without-invented-counter-origin',terminal['failed'] and terminal['scheduler_failed'] and value['disposition']=='NO_COUNTER_FAULT_RECORDED')
    # Adverse copies retain real producer metadata; only the named diagnostic
    # field changes. A reader PASS is distinct from raw byte authenticity.
    base=build/'d5an-overflow-own'
    def mutate(label,fn,expected_disposition=None):
        destination=out/label;destination.mkdir()
        for name in ('identity.json','terminal.json'):shutil.copyfile(base/name,destination/name)
        terminal=json.loads((destination/'terminal.json').read_bytes());fn(terminal)
        (destination/'terminal.json').write_text(json.dumps(terminal)+'\n',encoding='utf8',newline='\n')
        try:value=reader.read(destination,dll,build/'SorConstructionWinner.dll')
        except ValueError:
            check(label,expected_disposition is None)
        else:check(label,expected_disposition is not None and value['disposition']==expected_disposition)
    for key,value in [('publication',3),('id',62),('producer',99),('class',3),('value',42),('thread',0),('return_va',0),('address',0),('ids',0),('enabled',2)]:
        mutate('refuse-'+key,lambda row,key=key,value=value:row.update({'counter_fault_'+key:value}))
    mutate('partial-publication-explicit',lambda row:row.update(counter_fault_publication=1),'INCOMPLETE_PUBLICATION')
    mutate('missing-field-refused',lambda row:row.pop('counter_fault_producer'))
    mutate('boolean-integer-refused',lambda row:row.update(counter_fault_id=True))
    mutate('top-level-health-lie-refused',lambda row:row.update(failed=False))
    mutate('unknown-source-bitmap-refused',lambda row:row.update(counter_fault_ids=row['counter_fault_ids']|1))
    mutate('contradictory-native-aggregate-refused',lambda row:row.update(counter_fault_scheduler_bits=0,scheduler_counter_overflow=False))
    mutate('native-flag-mismatch-refused',lambda row:row.update(scheduler_counter_overflow=False))
    def erased(row):
        for name in ('publication','ids','id','producer','class','value','thread','address','return_va','enabled'):row['counter_fault_'+name]=0
    mutate('native-fault-with-erased-provenance-refused',erased)
    legacy=ROOT/'.local-work/d5am/live/session-838701ec716cd8bccf0929c4beb9f7e8bfe816b5fb77328007ba9e1cb77b06a8'
    check('original-N1-legacy-no-invented-provenance',reader.read(legacy)['disposition']=='LEGACY_NO_PROVENANCE')
    check('all-inputs-preserved',all(sha(p)==h for p,h in pins.items()))
    value=dict(schema='sor-d5an-counter-qualification/1',result='PASS',dll_sha256=dll,checks=checks,results=results,
        inputs=pins,initial_free=free,final_free=guard(),scope='Actual owned emitted diagnostics and adverse copies; no retail reliability or complete event coverage proof')
    with (out/'qualification.json').open('x',encoding='utf8',newline='\n') as stream:json.dump(value,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(result='PASS',checks=len(checks),native_cases=len(results))))

if __name__=='__main__':main()
