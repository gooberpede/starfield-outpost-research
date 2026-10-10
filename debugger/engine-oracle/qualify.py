"""SPDX-License-Identifier: GPL-3.0-or-later
Build and disposable-qualify v0.1.0 natural-output acquisition format.
Reads original sources, installed MSVC/SDK/x64dbg. Writes NEW ignored run root,
compiler outputs and flushed debugger logs. Launches/attaches ONLY the freshly
built original fixture; inserts/removes one software breakpoint, verifies bytes
and detach, waits for normal fixture exit. No game/save/config/database access,
native-save automation, downloads or deployment. Stdlib and project transport.
Run from repository root; --run is a new simple name. No live-target option.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'debugger/exp0002a'))
from transport import Transport
from process_read import ProcessRead
from contract import VERSION,decode_line,log_format


def disk():
    values={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    if min(values.values())<40000000000:raise RuntimeError('DISK_GUARD')
    return values


class OracleTransport(Transport):
    """Retain project command transport; replace old tiny volume cap with disk guard."""
    def _read(self):
        from datetime import datetime,timezone
        try:
            for line in self.process.stdout:
                disk()
                record={'utc':datetime.now(timezone.utc).isoformat(),'text':line.rstrip('\n')}
                self.stream.write(json.dumps(record)+'\n');self.stream.flush()
                if line.startswith(('SOR_','[FAIL]')):os.fsync(self.stream.fileno())
                self.lines.append(line);self.events.put(line)
        except Exception as error:self.error=repr(error)


def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run',required=True)
    ap.add_argument('--debugger',type=Path,required=True)
    ap.add_argument('--vcvars',type=Path,required=True)
    ap.add_argument('--zero-hit',action='store_true')
    a=ap.parse_args()
    if not re.fullmatch('[a-z0-9-]+',a.run):raise ValueError('SIMPLE_RUN_NAME')
    free=disk();out=ROOT/'.local-work/engine-oracle'/a.run;out.mkdir()
    manifest=dict(version=VERSION,evidence_kind='SYNTHETIC',live_game_qualification=False,
                  free_before=free,sources={str(p.relative_to(ROOT)):sha(p) for p in HERE.glob('*') if p.is_file()},
                  transport_sha256=sha(ROOT/'debugger/exp0002a/transport.py'),
                  debugger=dict(path=str(a.debugger),sha256=sha(a.debugger)))
    (out/'before.json').write_text(json.dumps(manifest,indent=2)+'\n')
    batch=out/'build.cmd'
    batch.write_text(f'@echo off\ncall "{a.vcvars}"\nif errorlevel 1 exit /b %errorlevel%\n'
        f'ml64 /nologo /c /Fo"{out/"fixture-asm.obj"}" "{HERE/"fixture.asm"}"\n'
        'if errorlevel 1 exit /b %errorlevel%\n'
        f'cl /nologo /W4 /WX /O2 /EHsc /std:c++17 "{HERE/"fixture.cpp"}" "{out/"fixture-asm.obj"}" '
        f'/Fe:"{out/"oracle_fixture.exe"}" /Fo:"{out/"fixture-cpp.obj"}" /link /INCREMENTAL:NO /EXPORT:OracleMarker\n'
        'exit /b %errorlevel%\n',encoding='utf8',newline='\r\n')
    build=subprocess.run(['cmd.exe','/d','/c',str(batch)],cwd=out,capture_output=True,timeout=60)
    (out/'build.log').write_bytes(build.stdout+build.stderr)
    if build.returncode:raise RuntimeError('BUILD_FAILED')
    fixture=out/'oracle_fixture.exe';manifest['fixture_sha256']=sha(fixture)
    trigger=out/'trigger';target=subprocess.Popen([str(fixture),str(trigger)],creationflags=0x08000000)
    transport=OracleTransport(a.debugger,out/'debugger')
    reader=ProcessRead(target.pid);detached=False;address=None;original=None
    try:
        transport.command(f'attach .{target.pid}',10)
        context=transport.command('log "SOR_STOPPED {p:cip}"')
        if not reader.debugged() or not any(s.startswith('SOR_STOPPED ') for s in context):raise RuntimeError('NOT_ATTACHED')
        lines=transport.command('log "SOR_ADDRESS {p:oracle_fixture.exe:OracleMarker}"')
        address=int(next(s.split()[1] for s in lines if s.startswith('SOR_ADDRESS ')),16)
        original=reader.read(address,32)
        transport.command('bp oracle_fixture.exe:OracleMarker')
        if reader.read(address,1)!=b'\xcc':raise RuntimeError('BREAKPOINT_NOT_INSTALLED')
        transport.command('SetBreakpointLog oracle_fixture.exe:OracleMarker, "'+log_format()+'"')
        transport.command('SetBreakpointCondition oracle_fixture.exe:OracleMarker, "0"')
        transport.command('run')
        if not a.zero_hit:trigger.write_text('synthetic only\n')
        deadline=time.monotonic()+(1 if a.zero_hit else 10)
        while time.monotonic()<deadline:
            if transport.error:raise RuntimeError(transport.error)
            if sum(s.startswith('SOR_POSITION ') for s in transport.lines)>=2:break
            time.sleep(.05)
        transport.command('pause');transport.command('bc oracle_fixture.exe:OracleMarker')
        restored=reader.read(address,32)==original
        if not restored:raise RuntimeError('RESTORATION_FAILED')
        transport.command('detach',10)
        deadline=time.monotonic()+3
        while reader.debugged() and time.monotonic()<deadline:time.sleep(.05)
        detached=not reader.debugged()
        if not detached:raise RuntimeError('DETACH_NOT_CONFIRMED')
        transport.exit_detached()
        if a.zero_hit:trigger.write_text('synthetic after detach\n')
        trigger.with_name(trigger.name+'.release').write_text('normal exit\n')
        target.wait(timeout=10)
        hits=[decode_line(s.strip(),'SYNTHETIC') for s in transport.lines if s.startswith('SOR_POSITION ')]
        passed=(target.returncode==0 and restored and detached and ((len(hits)==0) if a.zero_hit else
                (len(hits)==2 and len({r['thread_id'] for r in hits})==2
                and all(r['cell']==[1,10467,21144] and r['native_floor']==[3,24]
                        and r['center_hex']=='0369b243f0b019457220ffc1' and r['body']=='0003F59F' for r in hits))))
        manifest.update(passed=passed,hits=hits,target_exit=target.returncode,
                        cleanup='32-byte restoration verified; detach independently verified; normal fixture exit',
                        zero_hit=a.zero_hit,site_bytes_restored=restored,detached=detached,
                        free_after=disk(),original_site_sha256=hashlib.sha256(original).hexdigest())
        (out/'result.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
        print(json.dumps({k:manifest[k] for k in ('passed','version','target_exit','live_game_qualification')}))
        if not passed:raise RuntimeError('QUALIFICATION_FAILED')
    except Exception:
        if target.poll() is None:
            try:
                if address is not None:
                    transport.command('pause');transport.command('bc oracle_fixture.exe:OracleMarker')
                    if original is not None and reader.read(address,32)!=original:raise RuntimeError('RESTORATION_FAILED')
                transport.command('detach',10);detached=not reader.debugged()
            except Exception:pass
        else:detached=True
        if detached and transport.process.poll() is None:transport.exit_detached()
        if detached and target.poll() is None:
            trigger.write_text('normal cleanup release\n')
            trigger.with_name(trigger.name+'.release').write_text('normal exit\n')
        print('Failure receipts retained:',out,'detach verified:',detached)
        raise
    finally:
        reader.close()


if __name__=='__main__':main()
