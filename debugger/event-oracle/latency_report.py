"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline exclusive-QPC comparison. Reads timing receipts, writes only
a NEW output. No target/process access; no claim of pure kernel transport cost.
"""
import argparse,json,statistics
from pathlib import Path

def distribution(values):
    v=sorted(values)
    return {'n':len(v),'sum':sum(v),'median':statistics.median(v),'p95_nearest_rank':v[(95*len(v)+99)//100-1],'max':max(v)} if v else {'n':0,'sum':0}

def summarize(path):
    import hashlib
    data=Path(path).read_bytes();d=json.loads(data);f=d['qpc_frequency'];assert f>0
    samples=d['samples'];boundaries=[s for s in samples if s['site'].startswith('center_')]
    assert all(len(s['ticks'])==len(d['parts']) and min(s['ticks'])>=0 for s in samples)
    assert len(boundaries)==83 and sum(s['site']=='center_entry' for s in boundaries)==42
    # These comparison inputs are explicitly center-only: every replay belongs
    # to one of those83 boundaries. Grid-enabled timing can be reported separately.
    assert not any(s['site'].startswith('grid_') for s in samples)
    steps=[s for s in samples if s['exception']==0x80000004];assert len(steps)==83
    components={name:sum(s['ticks'][i] for s in boundaries)/f for i,name in enumerate(d['parts'])}
    handler=distribution([sum(s['ticks'])/f for s in boundaries])
    step_components={name:sum(s['ticks'][i] for s in steps)/f for i,name in enumerate(d['parts'])}
    cont=sum(s['continuation'] for s in boundaries+steps)/f
    replay=distribution([s['replay_delivery']/f for s in steps])
    return {'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'seconds':{'boundary_handler':handler,'exclusive_boundary_components':components,'exclusive_replay_handler_components':step_components,'ContinueDebugEvent_API_sum':cont,'replay_delivery_upper_bound':replay,'event_delivering_wait_sum_includes_native_work':sum(s['wait'] for s in samples)/f,'measured_boundary_plus_replay_pause_sum':handler['sum']+sum(step_components.values())+cont+replay['sum']},'writer_fraction_of_boundary_handler':components['writer']/handler['sum'],'boundary_sites':{'center_entry':42,'center_exit':41}}

def compare(baseline,candidate):
    a=summarize(baseline);b=summarize(candidate)
    old=a['seconds']['boundary_handler'];new=b['seconds']['boundary_handler']
    return {'baseline':a,'candidate':b,'handler_sum_reduction_fraction':1-new['sum']/old['sum'],'median_reduction_fraction':1-new['median']/old['median'],'handler_sum_speedup':old['sum']/new['sum'],'limits':['serial on same machine, no other task-controlled bulk I/O during these runs; OS/storage variance remains','profiling derivative is separate from unchanged0.1.2 baseline','notification delay before Wait returns unmeasured; replay delivery includes OS/scheduling/one instruction','field durability retained; residual synchronous WAL writes still stop target','no live Starfield timing/behavior established']}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    result=compare(a.baseline,a.candidate)
    with a.output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
