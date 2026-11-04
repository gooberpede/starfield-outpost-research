# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare owned native scheduling controls without operating any target.

Reads three completed D5AO build/session trees, source/PE pins and actual
counter/causal/scheduler journals. Writes one exclusive ignored receipt.
Uses project-owned readers and Python stdlib; no native execution, deployment,
save/configuration/database mutation, download, network or Git writes.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')
import argparse
import json
from pathlib import Path
from statistics import median
from collections import Counter
from d5am_lock_qualify import ROOT,guard,sha
sys.path.insert(0,str(ROOT/'runtime/construction-winner'))
from d5an_read_counter import read as counter_read
from d5an_read_causal import read as causal_read
from d5am_read_scheduler import read as scheduler_read


def require(value,message):
    if not value:raise RuntimeError(message)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('bounded','sleep','new','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();out=a.out.resolve();free=guard()
    require(out.is_relative_to(ROOT/'.local-work/d5ao') and not out.exists(),'Exclusive task-local receipt required')
    results={};pins={str(Path(__file__)):sha(__file__)};sources={}
    for label in ('bounded','sleep','new'):
        build=getattr(a,label).resolve();require(build.is_relative_to(ROOT/'.local-work/d5ao'),'Task-local build required')
        receipt=json.loads((build/'build.json').read_bytes());session=build/'d5ao-sensitivity'
        dll=build/'SorConstructionWinner.dll';digest=sha(dll)
        require(receipt['compilation']==0 and receipt['source_unchanged'] and receipt['dll_sha256']==digest,'Completed exact-source build required')
        require(all(row['pass_exit'] for row in receipt['cases']),'Native case failure remains')
        for path,h in receipt['inputs'].items():require(sha(path)==h,'Build input changed: '+path)
        for name,h in receipt['derived'].items():require(sha(build/'candidate'/name)==h,'Derived source changed: '+name)
        sources[label]={name.replace(chr(92),'/'):h for name,h in receipt['derived'].items()}
        for path in (build/'build.json',dll,*[x for x in session.rglob('*') if x.is_file()]):pins[str(path)]=sha(path)
        counter=counter_read(session,digest,dll);causal=causal_read(session,digest);scheduler=scheduler_read(session,digest)
        require(counter['complete'] and counter['disposition']=='NO_COUNTER_FAULT_RECORDED','Counter failure in sensitivity control')
        require(causal['native_bridge_accounting_complete'] and scheduler['native_bridge_accounting_complete'],'Native frame accounting incomplete')
        kinds=Counter(row['kind'] for row in causal['events'])
        require({1,2,3,4,5,6,7,8,9,10,15}<=set(kinds),'Matched owner/native reader/writer/recursive event coverage missing')
        terminal=json.loads((session/'terminal.json').read_bytes());require(terminal['failed'] is False,'Unhealthy timing cannot qualify')
        data=json.loads((session/'sensitivity.json').read_bytes());require(data['frequency']>0 and data['real_reader_writer'] is True,'Native reader/writer control missing')
        require(data['reader_writer_wait_calls']>=1 and data['reader_writer_pending_bits']>0,'Actual native wait branch/pending writer witness missing')
        rows=data['rows'];require(len(rows)==48 and all(row['winner'] in (1,2) and row['forced_collisions']==row['observed'] for row in rows),'Unexpected schedule/collision inventory')
        by_gap={}
        for gap in (250,20000):
            off={r['repeat']:r for r in rows if r['gap_us']==gap and not r['observed']}
            on={r['repeat']:r for r in rows if r['gap_us']==gap and r['observed']}
            require(set(off)==set(on)==set(range(12)),'Paired schedule missing')
            reversed_pairs=[i for i in off if off[i]['winner']==1 and on[i]['winner']==2]
            stable_pairs=[i for i in off if off[i]['winner']==on[i]['winner']==1]
            durations=[r['counter_ticks']*1000000/data['frequency'] for r in on.values()]
            by_gap[str(gap)]=dict(reversed_pairs=reversed_pairs,stable_A_pairs=stable_pairs,
                off_winners=[r['winner'] for r in off.values()],on_winners=[r['winner'] for r in on.values()],
                instrumented_elapsed_us=dict(min=min(durations),median=median(durations),max=max(durations)))
        require(by_gap['20000']['stable_A_pairs'],'No separated contrary control')
        primitive=[dict(id=r['id'],next_ns=r['next_ticks']*1e9/data['frequency']/r['operations'],
                        leave_ns=r['leave_ticks']*1e9/data['frequency']/r['operations']) for r in data['latency']]
        require(len(primitive)==19 and len(data['paths'])==20,'Primitive/actual-path latency inventory missing')
        results[label]=dict(dll_sha256=digest,mode=receipt.get('counter_mode','UNKNOWN'),paired=by_gap,
            primitive_batch_ns=primitive,path_batches=data['paths'],qpc_frequency=data['frequency'],
            counter=counter,causal_frames=len(causal['events']),causal_kind_counts=dict(kinds),scheduler_frames=len(scheduler['events']))
    require(results['sleep']['paired']['250']['reversed_pairs'],'Required observed sleep-induced close-race reversal missing')
    require(results['new']['paired']['250']['stable_A_pairs'],'New implementation never preserves close-race reference winner')
    differences={label:[name for name in sources['new'] if sources[label].get(name)!=sources['new'][name]] for label in ('bounded','sleep')}
    # Version metadata and counter primitive may differ. Scheduling/lock/page
    # fixture code must be exactly identical across the three builds.
    require(all(set(names)<={'runtime/construction-winner/d5an_counter.h','runtime/construction-winner/plugin.cpp'} for names in differences.values()),'Non-counter comparison envelope drift')
    require(all(sha(path)==h for path,h in pins.items()),'Input changed during comparison')
    result=dict(schema='sor-d5ao-sensitivity-qualification/1',result='PASS',results=results,
        envelope_differences=differences,inputs=pins,initial_free=free,final_free=guard(),
        scope='Controlled native original-instruction and integrated hooked paths; induced schedules, not retail frequency or a no-effect bound. Primitive batch times are shared-helper measurements, actual-path times group the stated C++/ASM operations. QPC/event seams contribute to elapsed intervals.')
    with out.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(result='PASS',results={k:v['paired'] for k,v in results.items()})))


if __name__=='__main__':main()
