# SPDX-License-Identifier: GPL-3.0-or-later
"""Assert real DLL receipt outcomes and damage controls. Never runs the game.

Reads one completed task build. Writes a qualification summary and disposable
damaged copies under it; originals are retained. Python stdlib only.
"""
import hashlib
import json
from pathlib import Path
import shutil
import sys
from read_capture import inspect
from operate import session_closed


def main():
    root=Path(sys.argv[1]).resolve()
    assert root.is_relative_to(Path(__file__).resolve().parents[2]/'.local-work/d5p')
    dll=hashlib.sha256((root/'SorRetainedPopulation.dll').read_bytes()).hexdigest()
    results={}
    for name in ('normal','mask-zero','unexpected-mask','mixed-partial','owner-change','mode-change','owner-mismatch','descriptor-change','partial','inserted-empty','bad-read','generation-exception','failed-copy','contrary','nested','concurrent','concurrent-miss','hit-only','bypass','reset','aba','destroy','erase','clear','retire','overflow','output-failure','crash-before','crash-after','worker-stop','worker-failure','worker-guard','worker-continuous'):
        r=inspect(root/name,dll);results[name]=r
        chains=r['complete_chains']
        positive=name in ('normal','mask-zero','unexpected-mask','mixed-partial','nested','concurrent','concurrent-miss','crash-after','worker-stop','worker-continuous')
        assert bool(chains)==positive,(name,r)
        if name in ('owner-mismatch','descriptor-change','partial','inserted-empty','bad-read','generation-exception','failed-copy','contrary','hit-only','bypass','overflow','output-failure','crash-before','worker-failure','worker-guard'):
            assert r['construction_witnesses']==0,(name,r)
        if name in ('reset','aba','destroy','erase','clear','retire'):
            assert r['construction_witnesses']==1,(name,r)
        if name in ('bad-read','generation-exception','failed-copy','contrary'):
            assert r['failed_observations']>0,(name,r)
        if name=='nested':
            assert r['construction_witnesses']==2,r
        if name=='concurrent-miss':
            assert r['construction_witnesses']==1 and r['hit_observations']==32,r
        if name=='bypass':assert r['bypass']==1 and not r['hit_observations'],r
        if name=='worker-stop':assert r['acquisition']=='RETIRED',r
        if name in ('worker-failure','worker-guard'):assert r['errors'],r
        if name=='mask-zero':assert r['ordinary_masks']==[0],r
        if name=='unexpected-mask':assert r['ordinary_masks']==[127],r
        if name=='contrary':assert r['contrary_geometry']==1,r
        if name=='worker-continuous':assert r['raw_records']>3072 and r['acquisition']=='RETIRED' and session_closed(root/name),r
        if name=='mixed-partial':assert r['complete_chains'][0]['population_partial'] and r['failed_observations'],r
    damage=root/'damaged';damage.mkdir(exist_ok=False)
    resilience={}
    for name in ('context-reasons','in-flight-loss','hook-stress','loss-cross','loss-fence','loss-rebuild','hook-timing','hook-bounds','late-disk-fault','late-write-fault','late-flush-fault','late-ack-fault','late-ack-write-fault','ack-write-fault','loss-one','loss-many','retry-one','retry-many','stress','disk-fault','write-fault','flush-fault','ack-fault'):
        r=inspect(root/name,dll);resilience[name]=r
        positive=name.startswith('late-') or name in ('hook-bounds','hook-stress','loss-rebuild','hook-timing','loss-one','loss-many','retry-one','retry-many','stress')
        assert bool(r['complete_chains'])==positive,(name,r)
        if name in ('loss-one','loss-many','retry-one','retry-many','stress','loss-cross','loss-fence','loss-rebuild'):
            terminal=r['loss_diagnostics'];assert terminal['failed'] is False and terminal['drops']>0,(name,r)
            assert terminal['drops']==terminal['queue_full']+terminal['contention_exhausted']
            assert terminal['enqueued']==r['independently_verified_durable_records'] and not terminal['counter_overflow']
        if name in ('loss-one','retry-one'):assert r['loss_diagnostics']['drops']==1
        if name in ('loss-many','retry-many'):assert r['loss_diagnostics']['drops']==37
        if name=='context-reasons':
            reasons=r['context_first_failures'];assert set(map(int,reasons))=={0,5,7,8,12,14,15,16,19,21,22,23,24,26},reasons
            assert r['failed_observations']==14,r
        if name=='loss-many':assert r['construction_witnesses']==2,r
        if name=='loss-one':assert r['hit_observations']==33,r
        if name=='in-flight-loss':assert not r['construction_witnesses'] and r['hit_observations']==1 and r['known_ordinary_drops']==1,r
        if name.endswith('-fault'):
            terminal=r['loss_diagnostics'];assert terminal['failed'] and terminal['output_faults']>0 and bool(r['complete_chains'])==name.startswith('late-'),r
            assert terminal['output_fault']=={'disk-fault':'disk_guard','write-fault':'write','flush-fault':'raw_flush','ack-fault':'ack_flush','ack-write-fault':'ack_write'}[name.removeprefix('late-')],r
    source=root/'normal'
    controls={}
    for mode in ('torn-header','torn-payload','corrupt','torn-ack','wrong-identity','wrong-session','wrong-dll','wrong-terminal','negative-ack'):
        target=damage/('foreign' if mode=='wrong-session' else 'normal')
        target.mkdir()
        for n in ('events.bin','flush.jsonl','identity.json'):shutil.copyfile(source/n,target/n)
        raw=(target/'events.bin').read_bytes()
        if mode=='torn-header':(target/'events.bin').write_bytes(raw+b'abc')
        if mode=='torn-payload':(target/'events.bin').write_bytes(raw[:-3])
        if mode=='corrupt':
            b=bytearray(raw);b[100]^=1;(target/'events.bin').write_bytes(b)
        if mode=='torn-ack':
            p=target/'flush.jsonl';p.write_bytes(p.read_bytes()[:-2])
        if mode=='wrong-identity':
            p=target/'identity.json';p.write_text(p.read_text().replace('"pid":','"pid":1'),encoding='utf8')
        if mode=='negative-ack':
            terminal=json.loads((target/'identity.json').read_text());terminal.update(drops=0,failed=False,enqueued=9,flushed=9,acknowledged=-1)
            (target/'terminal.json').write_text(json.dumps(terminal),encoding='utf8')
        if mode=='wrong-terminal':shutil.copyfile(root/'worker-stop/terminal.json',target/'terminal.json')
        try:
            r=inspect(target,'0'*64 if mode=='wrong-dll' else dll)
            assert r['errors'] and (mode=='torn-header' or not r['complete_chains']),(mode,r)
            controls[mode]='REFUSED_OR_QUALIFIED_PREFIX'
        except ValueError:controls[mode]='REFUSED'
        shutil.rmtree(target)
    # Offline lossless segmentation: each part is hash-bound and ordered, with
    # the original identity/flush stream unchanged. No writer rotation is used.
    segmented=damage/'normal';segmented.mkdir()
    for n in ('identity.json','flush.jsonl'):shutil.copyfile(source/n,segmented/n)
    raw=(source/'events.bin').read_bytes();parts=[];offset=0;previous=None
    for index,data in enumerate((raw[:1000],raw[1000:5000],raw[5000:])):
        name=f'part-{index}.bin';digest=hashlib.sha256(data).hexdigest();(segmented/name).write_bytes(data)
        parts.append(dict(name=name,bytes=len(data),offset=offset,sha256=digest,previous_sha256=previous));offset+=len(data);previous=digest
    manifest=dict(schema='sor-d5p-segments/1',identity_sha256=hashlib.sha256((segmented/'identity.json').read_bytes()).hexdigest(),segments=parts)
    (segmented/'segments.json').write_text(json.dumps(manifest),encoding='utf8')
    assert inspect(segmented,dll)['complete_chains']==results['normal']['complete_chains']
    (segmented/'part-1.bin').write_bytes(b'corrupt')
    segmented_result=inspect(segmented,dll)
    assert segmented_result['errors'] and not segmented_result['complete_chains'] and segmented_result['recovered_after_damage']['records']>0
    controls['segment-corrupt']='AUTHENTIC_LATER_ORPHANS_NO_JOINS'
    output=dict(schema='sor-d5p-qualification/2',dll_sha256=dll,results=results,resilience=resilience,damage_controls=controls)
    (root/'qualification.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf8',newline='\n')
    print('Independent native receipt oracles PASS:',len(results)+len(resilience),'cases;',len(controls),'damage controls')


if __name__=='__main__':main()
