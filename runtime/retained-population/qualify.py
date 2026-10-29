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
    source=root/'normal'
    controls={}
    for mode in ('torn-header','torn-payload','corrupt','torn-ack','wrong-identity','wrong-session','wrong-dll','wrong-terminal'):
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
        if mode=='wrong-terminal':shutil.copyfile(root/'worker-stop/terminal.json',target/'terminal.json')
        try:
            r=inspect(target,'0'*64 if mode=='wrong-dll' else dll)
            assert r['errors'] and (mode=='torn-header' or not r['complete_chains']),(mode,r)
            controls[mode]='REFUSED_OR_QUALIFIED_PREFIX'
        except ValueError:controls[mode]='REFUSED'
        shutil.rmtree(target)
    output=dict(schema='sor-d5p-qualification/1',dll_sha256=dll,results=results,damage_controls=controls)
    (root/'qualification.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf8',newline='\n')
    print('Independent native receipt oracles PASS:',len(results),'cases;',len(controls),'damage controls')


if __name__=='__main__':main()
