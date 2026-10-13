# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline only: read pinned PE/SFSE/protected inputs and own sources, compile
and run disposable fixtures, write a new ignored build and Vortex ZIP. No game,
deployment, database modification, downloads or Git writes. Windows CPython,
installed MSVC/SDK and unchanged approved SFSE interface header required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[2]
SRC=Path(__file__).parent
sys.path.insert(0,str(ROOT/'research/exp0002'))
from prepare import GAME_HASH, pe_layout, file_offset
SFSE_HASH='28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def guard():
    values={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    if min(values.values())<40_000_000_000:raise RuntimeError('caller_available_disk_guard')
    return values
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--name',required=True)
    a=ap.parse_args();assert re.fullmatch('[a-zA-Z0-9-]+',a.name)
    initial=guard();out=ROOT/'.local-work/position-write-history/builds'/a.name;out.mkdir(parents=True,exist_ok=False)
    previous=json.loads((ROOT/'.local-work/native-oracle-050/builds/qualification-03/build.json').read_text())
    baseline=json.loads((ROOT/'.local-work/position-write-history/baseline.json').read_text())
    protected=baseline['protected'];assert protected=={p:sha(p) for p in protected}
    game=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    sfse=Path(previous['sfse_path']);vcvars=Path(previous['vcvars'])
    assert sha(game)==GAME_HASH and sha(sfse)==SFSE_HASH
    pe=game.read_bytes();base,size,sections=pe_layout(pe);assert base==0x140000000
    audit=ROOT/'.local-work/position-write-history/writer-audit.tsv'
    text=audit.read_text();assert text.startswith('SHA256\t'+GAME_HASH+'\nBASE\t140000000\n')
    # Reverify actual complete CALL opcodes/targets; metadata references excluded.
    hooks=[]
    for source,target in re.findall(r'XREF\tFrom: ([0-9a-f]+) To: ([0-9a-f]+) Type: UNCONDITIONAL_CALL',text):
        source,target=int(source,16)-base,int(target,16)-base
        if target in (0xb4e410,0xb73310,0xf4ab80):hooks.append((source,target,'restoration' if source==0x5a14da else {0xb4e410:'replace',0xb73310:'apply',0xf4ab80:'center'}[target],5))
    hooks += [(0xacd2c0,0xb4a0b0,'producer',5),(0xacd2d8,0x18c28b0,'enqueue',5),(0x18c2982,0x22cdf60,'allocation',5),(0x18ce315,0xb4a0b0,'application',5)]
    # Only independently traced ordinary-reference virtual slot. Other subclass
    # slots remain explicitly uncovered rather than inferred from equal qwords.
    hooks.append((0x4b967b0,0xb734c0,'convert',8))
    hooks=sorted(set(hooks));assert len(hooks)>100 and len(hooks)*16<4096
    guards=[];generated='#pragma once\n'
    generated+=f'inline constexpr char game_hash[]="{GAME_HASH}";\ninline constexpr char sfse_hash[]="{SFSE_HASH}";\n'
    generated+='namespace history { inline uint64_t image_base{};\n'
    wrappers=[]
    for i,(site,target,kind,length) in enumerate(hooks):
        off=file_offset(sections,site,32);original=pe[off:off+length]
        if length==5:assert original[0]==0xe8 and site+5+struct.unpack_from('<i',original,1)[0]==target
        else:assert struct.unpack('<Q',original)[0]==base+target
        guards.append(dict(site=site,target=target,kind=kind,length=length,original=original.hex(),window_sha256=hashlib.sha256(pe[off:off+32]).hexdigest()))
        wrappers.append(f'inline uint64_t hook_{i}(uint64_t a,uint64_t b,uint64_t c,uint64_t d){{return invoke<{site},{kind}>(reinterpret_cast<Four>(image_base+{target}),a,b,c,d);}}\n')
    generated+=''.join(wrappers)+'struct Site{uint64_t rva,target;unsigned length;unsigned char original[8];const char* hash;Four hook;};\ninline Site sites[]={\n'
    for i,g in enumerate(guards):generated+='{'+f'{g["site"]},{g["target"]},{g["length"]},'+ '{'+','.join(str(x) for x in bytes.fromhex(g['original']))+'},"'+g['window_sha256']+'",hook_'+str(i)+'},\n'
    generated+='};\nstruct TargetGuard{uint64_t rva;const char* hash;};\ninline TargetGuard target_guards[]={\n'
    for target in sorted({g['target'] for g in guards}):
        off=file_offset(sections,target,32);generated+='{'+str(target)+',"'+hashlib.sha256(pe[off:off+32]).hexdigest()+'"},\n'
    generated+='};}\n';(out/'identity.generated.h').write_text(generated,encoding='utf8',newline='\n')
    sources=[p for p in SRC.iterdir() if p.is_file()]+[ROOT/'runtime/exp0002/win_support.h',ROOT/'runtime/exp0002/core.h',ROOT/'runtime/exp0002/third_party/sfse/PluginAPI.h',ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt',ROOT/'research/exp0002/prepare.py',audit]
    sources_before={str(p):sha(p) for p in sources}
    def run(args,label):
        guard();r=subprocess.run(args,cwd=out,capture_output=True);(out/label).write_bytes(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError(f'{label}: exit {r.returncode}; primary log retained')
    def cmd(label,lines):
        p=out/(label+'.cmd');p.write_text('@echo off\ncall "'+str(vcvars)+'"\nif errorlevel 1 exit /b 1\n'+lines+'\n',encoding='utf8',newline='\r\n');run(['cmd.exe','/d','/c',str(p)],label+'.txt')
    cmd('plugin',f'where cl.exe\nwhere link.exe\ncl.exe /Bv /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"plugin.cpp"}" /LD /Fe:SorNativePositionOracle.dll /link /INCREMENTAL:NO bcrypt.lib')
    cmd('fixture-assemble',f'where ml64.exe\nml64.exe /nologo /c /Fo fixture.obj "{SRC/"fixture.asm"}"')
    cmd('tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"tests.cpp"}" fixture.obj /Fe:tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'tests.exe'),str(out/'fixtures')],'qualification.txt')
    run([sys.executable,'-B',str(SRC/'test_inspect.py'),str(out/'fixtures')],'inspector-qualification.txt')
    cmd('lifecycle-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"lifecycle_tests.cpp"}" /Fe:lifecycle-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    for scenario in ('normal','pending-stop','before-ready-stop','guard-failure','writer-failure','disk-failure','terminal-failure'):
        run([str(out/'lifecycle-tests.exe'),str(out/('lifecycle-'+scenario)),scenario],'lifecycle-'+scenario+'.txt')
    cmd('dependencies','where dumpbin.exe\ndumpbin.exe /DEPENDENTS SorNativePositionOracle.dll')
    imported=re.findall(r'^\s+([A-Za-z0-9_.-]+\.dll)\s*$',(out/'dependencies.txt').read_text(errors='replace'),re.M|re.I)
    allowed={'kernel32.dll','bcrypt.dll','msvcp140.dll','vcruntime140.dll','vcruntime140_1.dll'}
    assert imported and all(n.lower() in allowed or n.lower().startswith('api-ms-win-crt-') for n in imported)
    package=out/'package';plugins=package/'Data/SFSE/Plugins';plugins.mkdir(parents=True)
    shutil.copyfile(out/'SorNativePositionOracle.dll',plugins/'SorNativePositionOracle.dll')
    notices=package/'ResearchNotices';notices.mkdir()
    shutil.copyfile(ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt',notices/'SFSE-PluginAPI-LICENSE.txt');shutil.copyfile(ROOT/'LICENSE',notices/'PROJECT-LICENSE.txt')
    (notices/'README.txt').write_text('SorNativePositionOracle 0.6.0 offline review candidate. DLL-only runtime payload.\nSee docs/experiments/position-write-history/run-card.md. No deployment/live authority.\n',encoding='utf8',newline='\n')
    archive=out/'SorNativePositionOracle-0.6.0.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(package.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(package).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        for p in package.rglob('*'):
            if p.is_file():assert z.read(p.relative_to(package).as_posix())==p.read_bytes()
    assert protected=={p:sha(p) for p in protected}
    assert sources_before=={str(p):sha(p) for p in sources}
    tools={}
    for label in ('plugin','fixture-assemble','dependencies'):
        for line in (out/(label+'.txt')).read_text(errors='replace').splitlines():
            p=Path(line.strip())
            if p.name.lower() in ('cl.exe','ml64.exe','link.exe','dumpbin.exe') and p.is_file():tools[str(p)]=sha(p)
    runtime={str(Path('C:/Windows/System32')/n):sha(Path('C:/Windows/System32')/n) for n in ('msvcp140.dll','vcruntime140.dll','vcruntime140_1.dll','ucrtbase.dll')}
    manifest=dict(version='0.6.0',schema=6,authority='OFFLINE_REVIEW_ONLY',game_path=str(game),game_hash=GAME_HASH,sfse_path=str(sfse),sfse_hash=SFSE_HASH,image_base=base,image_size=size,guards=guards,sources=sources_before,protected=protected,initial_disk=initial,final_disk=guard(),vcvars=str(vcvars),vcvars_sha256=sha(vcvars),compiler_tools=tools,external_runtime=runtime,imported_dlls=imported,runtime_essential=['Data/SFSE/Plugins/SorNativePositionOracle.dll'],files={p.relative_to(package).as_posix():dict(size=p.stat().st_size,sha256=sha(p)) for p in package.rglob('*') if p.is_file()},zip_sha256=sha(archive),generated_header_sha256=sha(out/'identity.generated.h'))
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
    run([sys.executable,'-B',str(SRC/'test_operate.py'),str(out)],'operational-qualification.txt')
    assert protected=={p:sha(p) for p in protected}
    print(json.dumps(dict(output=str(out),zip_sha256=sha(archive))))
if __name__=='__main__':main()
