# SPDX-License-Identifier: GPL-3.0-or-later
"""0.1.3 bounded disposable S1/S2/exit/synchronization qualification.
Reads explicit build/source manifest, launches only paired local fixture/adapter
hidden, writes create-new ignored records and cooperative fixture signal files.
No game discovery/access, downloads or runner force-kill. Failures stop the suite.
"""
import argparse,hashlib,json,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
EVIDENCE=ROOT/'.local-work/exp0002a-adapter-0.1.3'
def rows(path):
    if not path.exists():return []
    b=path.read_bytes();return [json.loads(x) for x in b[:b.rfind(b'\n')+1].splitlines()]
def wait(fn,seconds):
    end=time.monotonic()+seconds
    while not fn():
        if time.monotonic()>end:raise TimeoutError('bounded qualification wait')
        time.sleep(.025)
def qualify(build,out):
    assert all(p.resolve().is_relative_to(EVIDENCE.resolve()) for p in [build,out])
    m=json.loads((build/'manifest.json').read_text());assert m['version']=='0.1.3'
    for n,h in m['sources'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
    for n,h in m['binaries'].items():assert hashlib.sha256((build/n).read_bytes()).hexdigest()==h
    out.mkdir();adapter=build/m['adapter_executable'];fixture=build/'request_fixture.exe'
    subprocess.run([adapter,'--self-check'],check=True,timeout=5)
    assert subprocess.run([adapter,'--starfield','1',out/'forbidden'],timeout=5).returncode==2
    assert not (out/'forbidden.native.jsonl').exists()
    results={}
    for case in ['s1','exit37','s2-hit','s2-nohit']:
        prefix=out/case
        signal=lambda s:Path(str(prefix)+s)
        target=debugger=None
        try:
            with (out/(case+'.console.txt')).open('xb') as log:
                target=subprocess.Popen([fixture,prefix,'unarmed-only' if case=='s2-nohit' else 'fixed-existing'],stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
                wait(lambda:any(x['kind']=='heartbeat' and x['tids'][0] for x in rows(signal('.fixture.jsonl'))),5)
                tid=next(x['tids'][0] for x in rows(signal('.fixture.jsonl')) if x['kind']=='heartbeat' and x['tids'][0])
                time.sleep(1.5)
                s1=case in ['s1','exit37']
                args=[adapter,'--fixture-s1' if s1 else '--fixture-s2',str(target.pid),prefix]+([] if s1 else [str(tid)])
                debugger=subprocess.Popen(args,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
                wait(lambda:signal('.armed').exists() or debugger.poll() is not None,25)
                assert signal('.armed').exists(),'failed setup'
                time.sleep(1)
                assert not any(x['kind']=='capture_started' for x in rows(signal('.native.jsonl')))
                signal('.newthreads').touch(exist_ok=False)
                wait(lambda:sum(x['kind']=='new_thread_unarmed' for x in rows(signal('.native.jsonl')))>=2,10)
                signal('.start').touch(exist_ok=False)
                wait(lambda:signal('.active').exists(),3)
                active=next(x for x in rows(signal('.native.jsonl')) if x['kind']=='capture_started')
                # This simulates CLICK NOW only after native durable activation.
                time.sleep(.3)
                signal('.exit37' if case=='exit37' else '.trigger').touch(exist_ok=False)
                time.sleep(.2);signal('.confirm').touch(exist_ok=False)
                debugger.wait(timeout=40)
                if target.poll() is None:signal('.stop').touch(exist_ok=False)
                target.wait(timeout=10)
            n=rows(signal('.native.jsonl'));f=rows(signal('.fixture.jsonl'));get=lambda k:[x for x in n if x['kind']==k]
            final=get('complete')[-1]
            assert not get('failure') and not get('recovery_required') and not get('termination_authorized')
            assert all(x['version']=='0.1.3' and x['source_id']==m['source_id'] for x in n)
            armed=get('armed')[0];owners=[x for x in armed['members'] if x['owns_dr0']]
            assert len(owners)==(0 if s1 else 1)
            contexts=get('context');assert {x['tid'] for x in contexts if x['boundary']=='armed'}==(set() if s1 else {tid})
            if s1:assert not get('suspend') and not get('resume') and not any(x['boundary']=='retired' for x in contexts)
            if case=='exit37':
                assert target.returncode==37 and debugger.returncode==1
                assert get('target_exit')[0]['exit_code']==37 and get('target_exit_continued')
                assert final['target_exit_code']==37 and final['cleanup_status']=='TARGET_EXIT_EVENT_CONTINUED'
                assert not get('retirement_started') and not get('error')
            else:
                trigger=next(x for x in f if x['kind']=='trigger');assert active['tick_ms']<trigger['tick_ms']<active['deadline_tick_ms']
                assert target.returncode==debugger.returncode==0
                assert [x['delay'] for x in get('health')]==[0,1,5,15] and all(x['alive'] for x in get('health'))
                assert get('cleanup_finished')[-1]['debugger_absent']
                beats=[x for x in f if x['kind']=='heartbeat'];assert beats[-1]['calls']==1
                assert all(beats[-1]['pulse'][i]>100 for i in range(3))
                if case=='s2-hit':
                    assert len(get('capture'))==1 and get('capture')[0]['tid']==tid
                    assert n.index(get('capture_durable')[0])<n.index(get('retirement_started')[0])
                else:
                    assert not get('capture')
                    assert 10000<=get('capture_finished')[0]['tick_ms']-active['tick_ms']<11500
            results[case]={'passed':True,'target_pid':target.pid,'adapter_pid':debugger.pid,'terminal':final}
            print(json.dumps({case:results[case]}),flush=True)
        except Exception as e:
            if target and target.poll() is None:signal('.stop').touch(exist_ok=True)
            results[case]={'passed':False,'error':str(e),'target_pid':target.pid if target else None,'adapter_pid':debugger.pid if debugger else None}
            raise
        finally:(out/'qualification.json').write_text(json.dumps(results,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();qualify(a.build.resolve(),a.output.resolve())
