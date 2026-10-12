# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline build of original SFSE instrument and disposable ABI fixture.
Reads installed game, explicit SFSE, protected Save25/26, project/header sources,
installed MSVC/SDK. Writes a fresh ignored directory; runs compiler/linker/MASM,
original tests only. No game/SFSE execution, download, install or deployment.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
SRC=Path(__file__).parent
sys.path.insert(0,str(ROOT/'research/exp0002'))
from prepare import GAME_HASH,pe_layout,file_offset
SFSE_HASH='28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
CONFIG=b'D:/Projects/starfield-outpost-research/.local-work/native-oracle-live\ngrid=1\ncenter=1\n'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def guard():
    # shutil uses GetDiskFreeSpaceEx caller-available bytes on Windows.
    space={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    if min(space.values())<40_000_000_000+100_000_000:raise RuntimeError('disk_guard with build reserve')
    return space
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name',required=True);ap.add_argument('--sfse',type=Path,required=True);ap.add_argument('--vcvars',type=Path,required=True);a=ap.parse_args()
    assert a.name.replace('-','').isalnum()
    initial=guard();out=ROOT/'.local-work/native-oracle/builds'/a.name;out.mkdir(parents=True,exist_ok=False)
    baseline=json.loads((ROOT/'.local-work/native-oracle/baseline.json').read_text())
    protected={r['path']:sha(r['path']) for r in baseline['protected']}
    assert all(protected[r['path']]==r['expected'] for r in baseline['protected'])
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    assert sha(game)==GAME_HASH and sha(a.sfse)==SFSE_HASH
    sources=[p for p in SRC.iterdir() if p.is_file()]+[ROOT/'runtime/exp0002/win_support.h',ROOT/'runtime/exp0002/core.h',ROOT/'runtime/exp0002/third_party/sfse/PluginAPI.h']
    sources += [ROOT/'save-analysis/scripts'/name for name in ('durable_position_v2.py','audit_activated_grid.py','beacon_terrain_projection.py','durable_position_model.py')]
    sources += [ROOT/'docs/experiments/engine-oracle/predictions.json']
    source_before={p.relative_to(ROOT).as_posix():sha(p) for p in sources}
    pe=game.read_bytes();base,size,sections=pe_layout(pe);assert base==0x140000000
    guards=[]
    for name,rva in [('center_call',0xad0c36),('grid_call',0xad0d36),('callback',0xad0b90),('thunk',0xad8ec0),('center',0xf4ab80),('selector',0x96f5c0),('vtable',0x4b916e8)]:
        off=file_offset(sections,rva,32);guards.append(dict(name=name,rva=rva,file_offset=off,sha256=hashlib.sha256(pe[off:off+32]).hexdigest()))
    h=f'#pragma once\ninline constexpr char expected_game_hash[]="{GAME_HASH}";\ninline constexpr char expected_sfse_hash[]="{SFSE_HASH}";\nstruct Guard{{unsigned rva;const char* hash;}};\ninline constexpr Guard guards[]={{\n'+''.join('{'+hex(g['rva'])+',"'+g['sha256']+'"},\n' for g in guards)+'};\n'
    (out/'identity.generated.h').write_text(h,encoding='utf8',newline='\n')
    def run(args,label):
        guard();r=subprocess.run(args,cwd=out,capture_output=True);(out/label).write_bytes(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError(f'{label}: exit {r.returncode}')
    def command(label,lines):
        p=out/(label+'.cmd');p.write_text('@echo off\ncall "'+str(a.vcvars)+'"\nif errorlevel 1 exit /b 1\n'+lines+'\n',encoding='utf8',newline='\r\n');run(['cmd.exe','/d','/c',str(p)],label+'.txt')
    command('assemble',f'where ml64.exe\nml64.exe /nologo /c /Fo fixture.obj "{SRC/"fixture.asm"}"')
    for label,source,extra in [('plugin','plugin.cpp','/LD /Fe:SorNativePositionOracle.dll'),('tests','tests.cpp','fixture.obj /Fe:tests.exe')]:
        command(label,f'where cl.exe\nwhere link.exe\ncl.exe /Bv /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/source}" {extra} /link /INCREMENTAL:NO bcrypt.lib')
    compiler_tools={}
    for label in ('assemble','plugin'):
        for line in (out/(label+'.txt')).read_text(errors='replace').splitlines():
            p=Path(line.strip())
            if p.name.lower() in ('cl.exe','ml64.exe','link.exe') and p.is_file():compiler_tools[str(p)]=sha(p)
    assert len(compiler_tools)>=3
    run([str(out/'tests.exe'),str(out/'fixtures')],'qualification.txt')
    run([sys.executable,'-B',str(SRC/'test_inspect.py'),str(out/'fixtures')],'inspection-tests.txt')
    package=out/'package';plugins=package/'Data/SFSE/Plugins';plugins.mkdir(parents=True)
    (plugins/'SorNativePositionOracle.dll').write_bytes((out/'SorNativePositionOracle.dll').read_bytes());(plugins/'SorNativePositionOracle.config').write_bytes(CONFIG)
    notices=package/'ResearchNotices';notices.mkdir()
    for dest,src in [('SFSE-PluginAPI-LICENSE.txt',ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt'),('PROJECT-LICENSE.txt',ROOT/'LICENSE')]:
        (notices/dest).write_bytes(src.read_bytes())
    (notices/'READ-ME.txt').write_text('SorNativePositionOracle 0.1.0. OFFLINE REVIEW CANDIDATE. No live authorization.\nRequires reviewed sole-thread SFSE pre-main Load; otherwise refuses all hooks.\nNo dynamic unhook/unload. Retire capture then exit normally; user removes via Vortex.\nSee docs/experiments/native-oracle/run-card.md in the source/review package.\n',encoding='utf8',newline='\n')
    archive=out/'SorNativePositionOracle-0.1.0.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(package.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(package).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert not z.testzip() and len(z.namelist())==len(set(z.namelist()))
        for p in package.rglob('*'):
            if p.is_file():assert z.read(p.relative_to(package).as_posix())==p.read_bytes()
    assert protected=={p:sha(p) for p in protected}
    assert source_before=={p.relative_to(ROOT).as_posix():sha(p) for p in sources},'source changed during build'
    manifest=dict(component='SorNativePositionOracle',version='0.1.0',authority='OFFLINE_REVIEW_ONLY',game_hash=GAME_HASH,sfse_path=str(a.sfse),sfse_hash=SFSE_HASH,image_size=size,guards=guards,
        sources={p.relative_to(ROOT).as_posix():sha(p) for p in sources},protected=protected,initial_disk=initial,final_disk=guard(),
        files={p.relative_to(package).as_posix():dict(size=p.stat().st_size,sha256=sha(p)) for p in package.rglob('*') if p.is_file()},zip_sha256=sha(archive),vcvars=str(a.vcvars),vcvars_sha256=sha(a.vcvars),compiler_tools=compiler_tools)
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(output=str(out),zip_sha256=sha(archive))))
if __name__=='__main__':main()
