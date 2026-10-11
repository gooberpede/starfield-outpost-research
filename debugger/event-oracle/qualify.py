"""SPDX-License-Identifier: GPL-3.0-or-later
Build and qualify original disposable processes only. Reads installed MSVC/SDK,
source, pinned retail bytes and frozen inputs; writes a NEW ignored run directory.
Launches only event_fixture.exe/adapter.exe. No game/deployment/database access
beyond read-only executable hashing. No downloads or dependencies. stdlib only.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PYTHON=Path(sys.executable)

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def wait(path,processes,seconds=1200):
    until=time.monotonic()+seconds
    while not path.exists():
        if any(p.poll() is not None for p in processes):raise RuntimeError(f'premature exit waiting for {path}')
        if time.monotonic()>until:raise TimeoutError(str(path))
        time.sleep(.03)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run',required=True)
    ap.add_argument('--vcvars',type=Path,required=True)
    ap.add_argument('--keep-going',action='store_true',help='retain failed disposable controls and run remaining cases; never classify failures as PASS')
    a=ap.parse_args()
    if not a.run.replace('-','').isalnum():raise ValueError('simple run name')
    free={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    if min(free.values())<40_000_000_000:raise RuntimeError('disk guard')
    out=ROOT/'.local-work/event-instrumentation'/a.run;out.mkdir(exist_ok=False)
    snapshot=out/'sources';snapshot.mkdir()
    for p in HERE.iterdir():
        if p.is_file():shutil.copyfile(p,snapshot/p.name)
    (out/'before.json').write_text(json.dumps({'sources':{p.name:sha(p) for p in snapshot.iterdir()},'vcvars_sha256':sha(a.vcvars),'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()},indent=2)+'\n')
    sys.path.insert(0,str(ROOT/'research/exp0002'))
    from prepare import pe_layout,file_offset,GAME_HASH
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    assert sha(game)==GAME_HASH
    data=game.read_bytes();_,_,sections=pe_layout(data)
    sites={'center_entry':(0xf4ab80,'48895c2408'),'center_exit':(0xf4ac44,'488b5c2440'),
           'grid_entry':(0xad0b90,'48895c2418'),'grid_x':(0xad0c93,'c5fa59cc'),'grid_y':(0xad0c9c,'c5fa59d4'),'grid_result':(0xad0d3b,'488b4610'),'grid_exit':(0xad0e94,'4c8d9c24c0000000')}
    native={}
    for name,(rva,expected) in sites.items():
        offset=file_offset(sections,rva,32);b=data[offset:offset+32]
        assert b.startswith(bytes.fromhex(expected)),name
        native[name]={'rva':rva,'file_offset':offset,'instruction_hex':expected,'sha256_32':hashlib.sha256(b).hexdigest()}
    header='#pragma once\ninline constexpr char retail_hash[]="'+GAME_HASH+'";\nstruct RetailSite{const char* name;unsigned rva;const char* sha256;};\ninline constexpr RetailSite retail_sites[]={\n'+''.join('{"'+n+'",'+hex(r['rva'])+',"'+r['sha256_32']+'"},\n' for n,r in native.items())+'};\n'
    (out/'retail.generated.h').write_text(header,encoding='utf-8')
    (out/'native-sites.json').write_text(json.dumps({'game_sha256':GAME_HASH,'sites':native},indent=2)+'\n')
    batch=out/'build.cmd'
    batch.write_text(f'@echo off\ncall "{a.vcvars}"\nif errorlevel 1 exit /b 1\nwhere cl.exe\nwhere ml64.exe\nwhere link.exe\n'
        f'ml64 /nologo /c /Fo"{out / "fixture-asm.obj"}" "{HERE / "fixture.asm"}"\nif errorlevel 1 exit /b 1\n'
        f'cl /nologo /std:c++20 /EHs /W4 /O2 /MD "{HERE / "fixture.cpp"}" "{out / "fixture-asm.obj"}" /Fe:event_fixture.exe /Fo:fixture.obj /link /INCREMENTAL:NO\nif errorlevel 1 exit /b 1\n'
        f'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD /DUNICODE /D_UNICODE /I"{out}" "{HERE / "adapter.cpp"}" /Fe:adapter.exe /Fo:adapter.obj /link /INCREMENTAL:NO bcrypt.lib\nif errorlevel 1 exit /b 1\n'
        f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD /DUNICODE /D_UNICODE "{HERE / "health_tests.cpp"}" /Fe:health_tests.exe /Fo:health_tests.obj /link /INCREMENTAL:NO bcrypt.lib\n',encoding='utf-8',newline='\r\n')
    p=subprocess.run(['cmd.exe','/d','/c',str(batch)],cwd=out,capture_output=True)
    (out/'build.log').write_bytes(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('build failed '+str(out/'build.log'))
    assert subprocess.check_output([str(out/'adapter.exe'),'--version'])==b'0.1.4\r\n'
    health=subprocess.run([str(out/'health_tests.exe'),str(out/'health')],capture_output=True)
    (out/'health.log').write_bytes(health.stdout+health.stderr);assert health.returncode==0
    from materialize_epochs import decode
    retained,retained_receipt=decode(out/'health/wal-guarded/epochs.wal')
    assert retained[0]=={'kind':'durable_before_guard'} and retained[1]['data_hex']=='010203'
    assert len(retained)==2 and not retained_receipt['incomplete_tail_bytes']
    (out/'wal-health.json').write_text(json.dumps(retained_receipt,indent=2)+'\n')
    inspector_tests=subprocess.run([str(PYTHON),'-B','-m','unittest','discover','-s',str(HERE),'-p','test_*.py'],capture_output=True)
    (out/'inspector-tests.log').write_bytes(inspector_tests.stdout+inspector_tests.stderr);assert inspector_tests.returncode==0
    cases={}
    for mode in ('full','center-only','grid-guard-failure','zero','retire-active','writer-failure'):
        run=out/mode;run.mkdir()
        with (run/'fixture.log').open('wb') as fl,(run/'adapter.log').open('wb') as al:
            fixture=subprocess.Popen([str(out/'event_fixture.exe'),str(run),mode],stdout=fl,stderr=fl)
            adapter=None
            try:
                wait(run/'fixture.plan',[fixture])
                plan=run/'fixture.plan'
                if mode=='center-only':
                    plan=run/'center.plan';plan.write_text('\n'.join(l for l in (run/'fixture.plan').read_text().splitlines() if l.startswith('center_'))+'\n')
                if mode=='grid-guard-failure':
                    plan=run/'bad-grid.plan';plan.write_text('\n'.join(l.rsplit(' ',1)[0]+' 90909090' if l.startswith('grid_result ') else l for l in (run/'fixture.plan').read_text().splitlines())+'\n')
                env=os.environ.copy()
                if mode=='writer-failure':env['SOR_DISPOSABLE_WRITER_FAILURE']='1'
                adapter=subprocess.Popen([str(out/'adapter.exe'),'--fixture',str(fixture.pid),str(run),sha(out/'event_fixture.exe'),str(plan)],stdout=al,stderr=al,env=env)
                wait(run/'READY',[fixture,adapter]);(run/'GO').write_text('disposable\n')
                wait(run/('ACTIVE' if mode=='retire-active' else 'counts.json'),[fixture] if mode=='writer-failure' else [fixture,adapter]);(run/'STOP').write_text('STOP\n')
                adapter.wait(timeout=30)
                assert adapter.returncode==(1 if mode=='writer-failure' else 0)
                # Target already detached: traditional file expansion is offline.
                from materialize_epochs import materialize
                materialize(run/'evidence',run/'materialized')
                # Independent original project OS query, rather than adapter assertion.
                sys.path.insert(0,str(ROOT/'debugger/exp0002a'))
                from process_read import ProcessRead
                reader=ProcessRead(fixture.pid)
                assert not reader.debugged()
                rows=[json.loads(l) for l in (run/'materialized/records.jsonl').read_text().splitlines()]
                base=int(next(r['base'] for r in rows if r.get('kind')=='ready'),16)
                for line in (run/'fixture.plan').read_text().splitlines():
                    _,rva,b=line.split();expected=bytes.fromhex(b);assert reader.read(base+int(rva,16),len(expected))==expected
                reader.close()
                if mode=='retire-active':(run/'CONTINUE').touch();wait(run/'counts.json',[fixture])
                (run/'RELEASE').write_text('normal exit\n');fixture.wait(timeout=15)
                assert fixture.returncode==0
                from inspect_events import inspect
                report=inspect(run/'materialized')
                counts=json.loads((run/'counts.json').read_text())
                if mode=='writer-failure':
                    assert counts['bad']==0 and not report['boundaries']
                    cases[mode]={'injected_real_WriteFile_failure':True,'adapter_exit':adapter.returncode,'restoration_and_detach_independently_verified':True,'fixture_counts':counts,'fixture_exit':fixture.returncode}
                    continue
                if mode=='retire-active':
                    assert counts=={'entered':1,'completed':1,'exceptions':0,'bad':0}
                    assert len(report['centers'])==0 and report['unpaired']==1
                    cases[mode]={'scope_retired_before_exit':True,'unpaired':1,'fixture_counts':counts,'restoration_and_detach_independently_verified':True,'fixture_exit':fixture.returncode}
                    continue
                entries=[r for r in report['boundaries'] if r['site']=='center_entry']
                exits=[r for r in report['boundaries'] if r['site']=='center_exit' and r['pairing']=='paired']
                assert len(entries)==counts['entered'] and len(exits)==counts['completed']
                assert len({r['thread'] for r in entries})>=9 if mode!='zero' else not entries
                assert counts['bad']==0
                assert len(report['grid_results'])==(1 if mode=='full' else 0)
                if mode=='grid-guard-failure':assert any(r['kind']=='grid_disabled' for r in report['rows'])
                if mode=='full':
                    g=report['grid_results'][0];assert g['floor']==[3,24] and g['center_hex']=='0369b243f0b019457220ffc1'
                    assert g['pairing']=='scoped_result' and g['body']==0x3f59f and g['resolution']==256
                    assert g['axes']['x']['native_translated_hex']=='0369b243' and g['axes']['y']['native_translated_hex']=='f0b01945'
                    assert all(v['pairing']=='scoped_result' for v in g['axes'].values())
                    assert any(c['parent']==g['invocation'] and c['center_hex']==g['center_hex'] for c in report['centers'])
                if mode!='zero':assert any(r.get('kind')=='unpaired' for r in report['rows'])
                expected_centers={'00a0a04300002ac200008841','00a0a143000036c20000a841','0369b243f0b019457220ffc1'}
                assert all(r['center_hex'] in expected_centers for r in report['centers'])
                assert all(c['identity_fields_equal'] and c['entry_identity']['workshop_identifier_hex']=='0efca066ee4c7b9b' and c['entry_identity']['base_formid']==0x2c60e9 for c in report['centers'])
                cases[mode]={'counts':counts,'paired':len(exits),'unpaired':report['unpaired'],'detached_independently':True,'fixture_exit':fixture.returncode,'journal_sha256':sha(run/'materialized/records.jsonl'),'raw_sections':report['raw_sections']}
                (run/'inspection.json').write_text(json.dumps(report,indent=2)+'\n')
            except Exception as error:
                if not a.keep_going:raise
                import traceback
                (run/'failure.log').write_text(traceback.format_exc(),encoding='utf-8')
                cases[mode]={'failure':str(error),'adapter_exit_at_failure':adapter.poll() if adapter else None,'fixture_exit_at_failure':fixture.poll(),'disposition':'FAILED_CONTROL_RETAINED_NOT_QUALIFIED'}
            finally:
                # Never terminate a target/debugger. On failure request cooperative
                # restoration/detach, then let the fixture exit normally.
                (run/'STOP').touch();(run/'GO').touch();(run/'CONTINUE').touch()
                if adapter and adapter.poll() is None:
                    try:adapter.wait(timeout=15)
                    except subprocess.TimeoutExpired:print('CLEANUP NEEDS REVIEW',run)
                if not adapter or adapter.poll() is not None:
                    (run/'RELEASE').touch()
                    try:fixture.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        # This is the original disposable Popen process handle,
                        # never a looked-up PID or a game. Preserve diagnostics.
                        fixture.terminate();fixture.wait(timeout=15)
                        (run/'forced-fixture-cleanup.json').write_text(json.dumps({'fixture_pid':fixture.pid,'fixture_sha256':sha(out/'event_fixture.exe'),'reason':'failed disposable did not exit after cooperative release','exit':fixture.returncode})+'\n')
            if 'failure' in cases.get(mode,{}):
                cases[mode].update(adapter_exit=adapter.poll() if adapter else None,fixture_exit=fixture.poll())
    built_sources=json.loads((out/'before.json').read_text())['sources']
    assert all(sha(HERE/name)==digest for name,digest in built_sources.items()),'source changed during qualification'
    assert sha(game)==GAME_HASH
    toolchain={line:sha(Path(line)) for line in (out/'build.log').read_text(errors='replace').splitlines() if line.lower().endswith(('\\cl.exe','\\ml64.exe','\\link.exe')) and Path(line).is_file()}
    result={'version':'0.1.4','cases':cases,'live_game_qualification':False,'free_initial':free,'free_final':{d:shutil.disk_usage(d).free for d in ('C:/','D:/')},'sources':built_sources,'toolchain':toolchain,'adapter_sha256':sha(out/'adapter.exe'),'fixture_sha256':sha(out/'event_fixture.exe')}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['cases']))
    if any('failure' in case for case in cases.values()):raise RuntimeError('failed disposable controls retained; see result.json')

if __name__=='__main__':main()
