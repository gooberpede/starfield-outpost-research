# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline MSVC build/test/package. No downloads, installation or game access.

Reads pinned game bytes to generate hashes, not copied native code. Writes a new
ignored build directory. Executes only MSVC and original synthetic fixture.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/exp0002'))
from prepare import GAME_HASH, pe_layout, file_offset

# RVAs are independently checked instruction locations, not library bindings.
SITES={
    'GetWorkshop':0x2073cf0,'WorkshopTail':0x517d60,'GetCurrentLocation':0x208b8f0,
    'CurrentLocationTail':0xb4e650,'GetPlayer':0x177a1f0,'GetParentCell':0x208b990,
    'GetWorldSpace':0x208b9e0,'PositionX':0x2072580,'PositionY':0x2072590,
    'PositionZ':0x20725a0,'AngleX':0x20702e0,'AngleY':0x2070300,'AngleZ':0x2070320,
    'StoredBase':0x20706b7,'CellCount':0xb1e22e,'CellArray':0xb1e2d9,
    'InstallWorldspaceCell':0xbbdf70,'GetFormID':0x204d600,
}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_package(path,plugin_sha256):
    """Check actual ZIP bytes, including the observer's exact LF path contract."""
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None or len(z.namelist())!=len(set(z.namelist())):
            raise ValueError('Corrupt or duplicate package members')
        config=z.read('Data/SFSE/Plugins/SorExp0002.config')
        if config!=(str(ROOT/'.local-work/exp0002-live')+'\n').encode('utf-8'):
            raise ValueError('Config must be the exact approved UTF-8 path plus one LF')
        if hashlib.sha256(z.read('Data/SFSE/Plugins/SorExp0002.dll')).hexdigest()!=plugin_sha256:
            raise ValueError('Packaged observer differs from reviewed DLL')
def run(args,cwd,log):
    p=subprocess.run(args,cwd=cwd,capture_output=True)
    log.write_bytes(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError(f'Failed ({p.returncode}): {log}')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path,required=True)
    parser.add_argument('--vcvars',type=Path,required=True)
    parser.add_argument('--name',required=True)
    a=parser.parse_args()
    if not a.name.replace('-','').isalnum():raise ValueError('Simple build name required')
    out=ROOT/'.local-work/exp0002-builds'/a.name
    out.mkdir(parents=True,exist_ok=False)
    data=a.game.read_bytes()
    if hashlib.sha256(data).hexdigest()!=GAME_HASH:raise ValueError('Wrong executable')
    _,size,sections=pe_layout(data)
    guards=[]
    for name,rva in SITES.items():
        pos=file_offset(sections,rva,32)
        guards.append(dict(name=name,rva=rva,file_offset=pos,size=32,sha256=hashlib.sha256(data[pos:pos+32]).hexdigest()))
    (out/'site_guards.generated.h').write_text('#pragma once\nstruct SiteGuard { unsigned rva; const char* sha256; };\ninline constexpr SiteGuard site_guards[]={\n'+''.join('{'+hex(g['rva'])+',"'+g['sha256']+'"},\n' for g in guards)+'};\n',encoding='utf-8')
    (out/'site-guards.json').write_text(json.dumps(guards,indent=2)+'\n',encoding='utf-8')
    source=Path(__file__).parent
    shared=['/nologo','/std:c++20','/EHsc','/W4','/MD','/O2','/DUNICODE','/D_UNICODE',f'/I"{out}"',f'/I"{source}"']
    for target,flags in [('observer',['/LD','/Fe:SorExp0002.dll']),('trace',['/Fe:workshop-trace.exe']),('tests',['/Fe:offline-tests.exe'])]:
        rsp=out/(target+'.rsp')
        rsp.write_text('\n'.join(shared+flags+[f'"{source/(target+".cpp")}"','/link','/INCREMENTAL:NO','bcrypt.lib'])+'\n',encoding='utf-8')
        # Fixed tool call: no downloads/deployment, only a scoped MSVC environment.
        command=out/(target+'-build.cmd')
        command.write_text(f'@echo off\ncall "{a.vcvars}"\nif errorlevel 1 exit /b 1\nwhere cl.exe\nwhere link.exe\nset WindowsSDKVersion\ncl.exe /Bv @{rsp.name}\n',encoding='utf-8',newline='\r\n')
        run(['cmd.exe','/d','/c',str(command)],out,out/(target+'-build.txt'))
    run([str(out/'offline-tests.exe'),str(out/'fixtures'),str(out/'SorExp0002.dll')],out,out/'tests.txt')
    run([sys.executable,str(source/'test_output.py'),str(out/'fixtures/native-identity.json')],out,out/'output-tests.txt')
    package=out/'package/Data/SFSE/Plugins';package.mkdir(parents=True)
    (package/'SorExp0002.dll').write_bytes((out/'SorExp0002.dll').read_bytes())
    # Binary reader removes exactly one LF; Windows newline translation would
    # leave CR in the path and make the observer reject the packaged config.
    (package/'SorExp0002.config').write_text(str(ROOT/'.local-work/exp0002-live')+'\n',encoding='utf-8',newline='\n')
    notices=out/'package/ResearchNotices';notices.mkdir()
    (notices/'SFSE-PluginAPI-LICENSE.txt').write_bytes((source/'third_party/sfse/LICENSE.txt').read_bytes())
    (notices/'PROJECT-LICENSE.txt').write_bytes((ROOT/'LICENSE').read_bytes())
    with zipfile.ZipFile(out/'SorExp0002-local-test.zip','x',zipfile.ZIP_DEFLATED) as z:
        for p in (out/'package').rglob('*'):
            if p.is_file():z.write(p,p.relative_to(out/'package'))
    verify_package(out/'SorExp0002-local-test.zip',sha(out/'SorExp0002.dll'))
    tool_paths=[Path(line.strip()) for line in (out/'observer-build.txt').read_text(errors='replace').splitlines() if line.strip().lower().endswith(('\\cl.exe','\\link.exe'))]
    manifest=dict(utc=datetime.now(timezone.utc).isoformat(),game_sha256=GAME_HASH,image_size=size,
        authority='OFFLINE_ONLY_NOT_DEPLOYED',plugin_sha256=sha(out/'SorExp0002.dll'),trace_sha256=sha(out/'workshop-trace.exe'),package_sha256=sha(out/'SorExp0002-local-test.zip'),
        sources=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in source.rglob('*') if p.is_file() and '__pycache__' not in str(p)],
        vcvars_path=str(a.vcvars),vcvars_sha256=sha(a.vcvars),toolchain=[dict(path=str(p),sha256=sha(p)) for p in tool_paths],guards=guards)
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(build=str(out),plugin_sha256=manifest['plugin_sha256'],package_sha256=manifest['package_sha256'])))

if __name__=='__main__':main()
