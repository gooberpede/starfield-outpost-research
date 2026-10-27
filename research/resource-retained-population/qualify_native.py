# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the actual native reader on a source-shaped disposable Windows target.

Reads a hash-bound native-shaped fixture build; writes fresh task-local durable
SRO1/ACKs, raw contexts, native-layout reads and reductions. No retail process,
save, analysis, network, dependency or Git effects. Uses owned transport/decoder.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
from build import LOCAL,pin
from qualify import transport,decoder,old_qualification
from native_reduce import reduce


def main():
    build,out=(Path(x).resolve() for x in sys.argv[1:3])
    assert build.is_relative_to(LOCAL) and out.is_relative_to(LOCAL)
    manifest=json.loads((build/'build.json').read_text());assert manifest['exit_code']==0
    for p,h in manifest['files'].items():
        assert pin(p)==h,p
    out.mkdir(exist_ok=False)
    transport.write(out/'method-pins.json',{str(p):pin(p) for p in Path(__file__).parent.glob('*.py')})
    modes=sys.argv[3:] or ['basic','reuse','reset','owner-aba','reset-window','destroy-window','grid-window','source-window','query-change-hit','alternate-frame','failed','copy-failed','partial','prereq','concurrent','nested','bad-read','crash','stop','pre-arm-stop','step-stop','bad-ack','guard-loss','defer-peer','new-peer-step','exception','contrary']
    results=[]
    image=pin(build/'sor-d5l-native-fixture.exe')
    for mode in modes:
        dest=out/mode;dest.mkdir();rows=[];receipts=[];session=None
        with (dest/'stderr.txt').open('xb') as err,(dest/'events.jsonl').open('x',encoding='utf8',newline='\n') as journal:
            p=subprocess.Popen([str(build/'sor-d5l-native-fixture-controller.exe'),'--synthetic-fixture',image,mode],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
            try:
                for line in p.stdout:
                    row=json.loads(line);rows.append(row);journal.write(json.dumps(row)+'\n');journal.flush();os.fsync(journal.fileno())
                    if row['kind']=='SESSION':session=row
                    if row['kind'] in ('SAMPLE','ARM_BARRIER'):
                        payload=[session,dict(kind='SAMPLE',event=row),dict(kind='END',complete=row.get('read_complete',True))]
                        path=dest/f'capture-{len(receipts):05d}.bin';ack=transport.persist(path,payload,synthetic=True)
                        assert decoder.independent(path)==payload;receipts.append(dict(path=str(path),**ack))
                        answer='ARM_ACK' if row['kind']=='ARM_BARRIER' else f'ACK {row["capture"]}'
                        if mode=='pre-arm-stop' and row['kind']=='ARM_BARRIER':answer='STOP'
                        if mode=='bad-ack' and row['kind']=='SAMPLE':answer='REJECT'
                        if mode=='stop' and row.get('capture')==6:answer+=' STOP'
                        p.stdin.write(answer+'\n');p.stdin.flush()
                code=p.wait(timeout=15)
            finally:
                if p.poll() is None:p.terminate();p.wait(timeout=15)
        reduction=reduce(rows,image,synthetic=True)
        checks=dict(controller_exit=code==(2 if mode in ('bad-ack','guard-loss') else 0),target_absent=bool(session and old_qualification.target_absent(session['pid'])))
        if mode in ('failed','copy-failed','prereq','bad-read'):
            checks['no_false_success']=not reduction['chains']
            checks['incomplete_preserved']=any(not c['qualified'] and c['decision']=='MISS' for c in reduction['decisions'])
        elif mode not in ('stop','pre-arm-stop','step-stop','bad-ack','guard-loss'):
            checks['copied_region_retained_reused']=bool(reduction['chains'])
        if mode in ('reuse','reset','owner-aba','reset-window','destroy-window','grid-window','source-window'):
            checks['distinct_masks_lifetimes']=[c['mask'] for c in reduction['chains']]==[0,3] and len({tuple(c['lifetime']) for c in reduction['chains']})==2
        if mode in ('partial','exception'):
            checks['surrounding_failure_preserved']=bool(reduction['chains'] and reduction['chains'][0]['population_partial'])
        if mode=='concurrent':
            checks['all_decisions']=len(reduction['decisions'])==11
            checks['unrelated_traffic']=sum(x['reason']=='unrelated_source_or_owner' for x in reduction['rejected'])>=4
        if mode=='nested':checks['nested_contexts_distinct']=len(reduction['decisions'])==4 and len({tuple(c['context']) for c in reduction['decisions']})>=3
        if mode=='defer-peer':checks['deferred_retrap_exercised']=any(r['kind']=='DEFERRED_TRAP' for r in rows)
        if mode=='new-peer-step':checks['new_peer_fenced_in_rearm']=any(r['kind']=='THREAD_ARMED' and r.get('rearm_window') for r in rows)
        if mode in ('destroy-window','grid-window','source-window'):
            checks['teardown_window_not_rejoined']=any(x['reason']=='inactive_owner' for x in reduction['rejected']) and len(reduction['chains'])==2
        if mode=='reset-window':
            fences=[r for r in rows if r.get('event')=='native_reset'];masks=[r for r in rows if r.get('event')=='native_mask']
            checks['post_clear_fence']=len(fences)==1 and fences[0]['empty_source_map'] and fences[0]['fixture_oracle']['reset_phase']==2
            checks['actual_preclear_construction']=bool(masks) and masks[0]['fixture_oracle']['reset_phase']==1 and masks[-1]['fixture_oracle']['reset_phase']==2
        if mode=='query-change-hit':
            checks['different_later_query_same_population']=bool(reduction['chains'] and reduction['chains'][0]['construction_query']!=reduction['chains'][0]['reuse_query'])
            checks['only_first_mask_sampled']=[r['operand'] for r in rows if r.get('event')=='native_mask']==[0]
        if mode=='alternate-frame':checks['alternate_descriptor_branch']=all(c['owner_mode']==3 for c in reduction['decisions'])
        if mode=='contrary':checks['contrary_geometry_not_fitted']=bool(reduction['chains']) and reduction['chains'][0]['mask']==3 and reduction['chains'][0]['regions'][0]['shape']['points'].startswith('00000000')
        if mode in ('stop','pre-arm-stop','step-stop','bad-ack','guard-loss'):
            at=next((i for i,r in enumerate(rows) if r['kind']=='STOP_COMMITTED'),None)
            checks['monotonic_stop']=at is not None and not any(r['kind']=='SAMPLE' for r in rows[at+1:])
            checks['no_incomplete_chain']=not reduction['chains']
        checks['never_intended_census']=reduction['complete_intended_census'] is False
        transport.write(dest/'reduction.json',reduction);transport.write(dest/'receipts.json',receipts)
        result=dict(mode=mode,checks=checks,passed=all(checks.values()),receipts=len(receipts),events=len(rows),build_sha256=pin(build/'build.json'))
        transport.write(dest/'result.json',result);results.append(result);print(json.dumps(result),flush=True)
    transport.write(out/'results.json',results)
    return 0 if all(x['passed'] for x in results) else 1


if __name__=='__main__':
    raise SystemExit(main())
