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
    initial=guard();out=ROOT/'.local-work/native-oracle-050/builds'/a.name;out.mkdir(parents=True,exist_ok=False)
    baseline=json.loads((ROOT/'.local-work/ship-relocation-050/baseline.json').read_text(encoding='utf8'))
    protected={p:sha(p) for p in baseline['protected']}
    assert protected==baseline['protected'],'protected input changed before build'
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    assert sha(game)==GAME_HASH and sha(a.sfse)==SFSE_HASH
    sources=[p for p in SRC.iterdir() if p.is_file()]+[ROOT/'runtime/exp0002/win_support.h',ROOT/'runtime/exp0002/core.h',ROOT/'runtime/exp0002/third_party/sfse/PluginAPI.h']
    sources += [ROOT/'save-analysis/scripts'/name for name in ('durable_position_v2.py','audit_activated_grid.py','beacon_terrain_projection.py','durable_position_model.py')]
    sources += [ROOT/'docs/experiments/engine-oracle/predictions.json',ROOT/'research/exp0002/prepare.py']
    source_before={p.relative_to(ROOT).as_posix():sha(p) for p in sources}
    pe=game.read_bytes();base,size,sections=pe_layout(pe);assert base==0x140000000
    guards=[]
    call_pairs=((0x78b877,0x77fc20),(0x7800a6,0x77def0),(0x7801b3,0x77f900),(0x780264,0x77e350),(0x77fe91,0x96eb90),(0x77fec0,0x96f5c0),(0x77fd45,0x96f940),(0x780132,0x96f940),(0x77fce9,0xad3b20),(0x7800d6,0xad3b20),(0xad93fa,0xad08d0),(0xad0ab5,0xb1e190),(0x17df421,0x17dfdf0),(0x17df48d,0xad3b20),(0x17df4e2,0x78b030),(0x17dee5b,0x78b030),(0x17df168,0x1a67830),(0xad0c36,0xf4ab80),(0xad0d36,0x96f5c0))
    import struct
    for rva,target in call_pairs:
        off=file_offset(sections,rva,32)
        assert pe[off]==0xe8 and rva+5+struct.unpack_from('<i',pe,off+1)[0]==target
        guards.append(dict(name=hex(rva),rva=rva,file_offset=off,sha256=hashlib.sha256(pe[off:off+32]).hexdigest()))
    for rva in (0x77fc20,0x77def0,0x77f900,0x77e350,0x96eb90,0x96f5c0,0x96f940,0xad3b20,0xad08d0,0xb1e190,0x17dfdf0,0x78b030,0x1a67830,0xad8ec0,0xad0b90,0xf4ab80,0x4b916e8):
        off=file_offset(sections,rva,32);guards.append(dict(name=hex(rva),rva=rva,file_offset=off,sha256=hashlib.sha256(pe[off:off+32]).hexdigest()))
    h=f'#pragma once\ninline constexpr char expected_game_hash[]="{GAME_HASH}";\ninline constexpr char expected_sfse_hash[]="{SFSE_HASH}";\nstruct Guard{{unsigned rva;const char* hash;}};\ninline constexpr Guard guards[]={{\n'+''.join('{'+hex(g['rva'])+',"'+g['sha256']+'"},\n' for g in guards)+'};\n'
    h+='struct CallSite{unsigned rva;unsigned char bytes[5];};\ninline constexpr CallSite call_sites[]={\n'+''.join('{'+hex(rva)+',{'+','.join(hex(v) for v in pe[file_offset(sections,rva,5):file_offset(sections,rva,5)+5])+'}},\n' for rva,target in call_pairs)+'};\n'
    (out/'identity.generated.h').write_text(h,encoding='utf8',newline='\n')
    def run(args,label):
        guard();r=subprocess.run(args,cwd=out,capture_output=True);(out/label).write_bytes(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError(f'{label}: exit {r.returncode}')
    def command(label,lines):
        p=out/(label+'.cmd');p.write_text('@echo off\ncall "'+str(a.vcvars)+'"\nif errorlevel 1 exit /b 1\n'+lines+'\n',encoding='utf8',newline='\r\n');run(['cmd.exe','/d','/c',str(p)],label+'.txt')
    command('assemble',f'where ml64.exe\nml64.exe /nologo /c /Fo fixture.obj "{SRC/"fixture.asm"}"')
    command('travel-assemble',f'ml64.exe /nologo /c /Fo travel_bridge.obj "{SRC/"travel_bridge.asm"}"')
    command('producer-assemble',f'ml64.exe /nologo /c /Fo producer_bridge.obj "{SRC/"producer_bridge.asm"}"')
    for label,source,extra in [('plugin','plugin.cpp','producer_bridge.obj travel_bridge.obj /LD /Fe:SorNativePositionOracle.dll'),('tests','tests.cpp','fixture.obj /Fe:tests.exe')]:
        runtime_flag='/MD'
        command(label,f'where cl.exe\nwhere link.exe\ncl.exe /Bv /nologo /std:c++20 /EHa /W4 {runtime_flag} /O2 /I"{out}" "{SRC/source}" {extra} /link /INCREMENTAL:NO bcrypt.lib')
    command('dependencies','where dumpbin.exe\ndumpbin.exe /DEPENDENTS SorNativePositionOracle.dll')
    dependency_text=(out/'dependencies.txt').read_text(encoding='utf8',errors='replace')
    import re
    imported=re.findall(r'^\s+([A-Za-z0-9_.-]+\.dll)\s*$',dependency_text,re.M|re.I)
    external_runtime={str(Path('C:/Windows/System32')/n):sha(Path('C:/Windows/System32')/n)
                      for n in ('msvcp140.dll','vcruntime140.dll','vcruntime140_1.dll','ucrtbase.dll')}
    allowed={'kernel32.dll','bcrypt.dll','msvcp140.dll','vcruntime140.dll','vcruntime140_1.dll'}
    assert imported and all(n.lower() in allowed or n.lower().startswith('api-ms-win-crt-') for n in imported),imported
    compiler_tools={}
    for label in ('assemble','plugin','dependencies'):
        for line in (out/(label+'.txt')).read_text(encoding='utf8',errors='replace').splitlines():
            p=Path(line.strip())
            if p.name.lower() in ('cl.exe','ml64.exe','link.exe','dumpbin.exe') and p.is_file():compiler_tools[str(p)]=sha(p)
    assert len(compiler_tools)>=3
    run([str(out/'tests.exe'),str(out/'fixtures')],'qualification.txt')
    run([sys.executable,'-B',str(SRC/'test_inspect.py'),str(out/'fixtures')],'inspection-tests.txt')
    command('branch-assemble',f'ml64.exe /nologo /c /Fo branch_fixture.obj "{SRC/"branch_fixture.asm"}"')
    command('branch-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"branch_tests.cpp"}" fixture.obj branch_fixture.obj /Fe:branch-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'branch-tests.exe'),str(out/'branch-events.bin')],'branch-qualification.txt')
    run([sys.executable,'-B',str(SRC/'qualify_branch.py'),str(out/'branch-events.bin'),str(out/'branch-cases')],'branch-decoder-qualification.txt')
    run([sys.executable,'-B','-m','unittest','discover','-s',str(SRC),'-p','test_branch.py'],'branch-inspection-tests.txt')
    command('route-assemble',f'ml64.exe /nologo /c /Fo route_fixture.obj "{SRC/"route_fixture.asm"}"')
    command('route-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"route_tests.cpp"}" fixture.obj route_fixture.obj producer_bridge.obj /Fe:route-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'route-tests.exe'),str(out/'route-events.bin')],'route-qualification.txt')
    run([sys.executable,'-B',str(SRC/'test_route.py'),str(out/'route-events.bin')],'route-decoder-tests.txt')
    command('travel-fixture',f'ml64.exe /nologo /c /Fo travel_fixture.obj "{SRC/"travel_fixture.asm"}"')
    command('travel-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"travel_tests.cpp"}" fixture.obj travel_fixture.obj travel_bridge.obj /Fe:travel-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'travel-tests.exe'),str(out/'travel-events.bin')],'travel-qualification.txt')
    command('admission-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"admission_tests.cpp"}" /Fe:admission-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'admission-tests.exe'),str(out/'admission-stop')],'admission-qualification.txt')
    command('lifecycle-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"lifecycle_tests.cpp"}" producer_bridge.obj travel_bridge.obj /Fe:lifecycle-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    for scenario in ('normal','no-hit','writer-failure','guard-failure'):
        run([str(out/'lifecycle-tests.exe'),str(out/('lifecycle-'+scenario)),str(game),scenario],'lifecycle-'+scenario+'.txt')
    run([sys.executable,'-B',str(SRC/'test_capture.py'),str(out)],'capture-inspection-tests.txt')
    package=out/'package'  ;plugins=package/'Data/SFSE/Plugins';plugins.mkdir(parents=True)
    (plugins/'SorNativePositionOracle.dll').write_bytes((out/'SorNativePositionOracle.dll').read_bytes())
    notices=package/'ResearchNotices';notices.mkdir()
    for dest,src in [('SFSE-PluginAPI-LICENSE.txt',ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt'),('PROJECT-LICENSE.txt',ROOT/'LICENSE')]:
        (notices/dest).write_bytes(src.read_bytes())
    (notices/'READ-ME.txt').write_text('SorNativePositionOracle 0.5.0. OFFLINE REVIEW CANDIDATE. No live authorization.\nRequires reviewed sole-thread SFSE pre-main Load; otherwise refuses all hooks.\nNo dynamic unhook/unload. Retire capture then exit normally; user removes via Vortex.\nSee docs/experiments/ship-relocation-050/run-card.md. DLL-only runtime payload; no live authority.\n',encoding='utf8',newline='\n')
    archive=out/'SorNativePositionOracle-0.5.0.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(package.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(package).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert not z.testzip() and len(z.namelist())==len(set(z.namelist()))
        for p in package.rglob('*'):
            if p.is_file():assert z.read(p.relative_to(package).as_posix())==p.read_bytes()
    assert protected=={p:sha(p) for p in protected}
    assert source_before=={p.relative_to(ROOT).as_posix():sha(p) for p in sources},'source changed during build'
    manifest=dict(imported_system_dlls=imported,external_runtime_prerequisites=external_runtime,runtime_linkage='/MD; installed Microsoft runtime only, not bundled',runtime_essential=['Data/SFSE/Plugins/SorNativePositionOracle.dll'],call_pairs=call_pairs,component='SorNativePositionOracle',version='0.5.0',authority='OFFLINE_REVIEW_ONLY',game_hash=GAME_HASH,sfse_path=str(a.sfse),sfse_hash=SFSE_HASH,image_size=size,guards=guards,
        sources={p.relative_to(ROOT).as_posix():sha(p) for p in sources},protected=protected,initial_disk=initial,final_disk=guard(),
        files={p.relative_to(package).as_posix():dict(size=p.stat().st_size,sha256=sha(p)) for p in package.rglob('*') if p.is_file()},zip_sha256=sha(archive),vcvars=str(a.vcvars),vcvars_sha256=sha(a.vcvars),compiler_tools=compiler_tools)
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(output=str(out),zip_sha256=sha(archive))))
if __name__=='__main__':main()
