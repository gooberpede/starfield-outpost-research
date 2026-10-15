# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline build only. Reads own sources, pinned PE/SFSE and protected inputs;
compiles original disposable fixtures and DLL, writes exclusive ignored build
and Vortex archive. No game, deployment, network, download, save/DB/Git change.
Requires installed CPython/MSVC/MASM/SDK and existing approved SFSE header.
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

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).parent
sys.path.insert(0, str(ROOT/'research/exp0002'))
from prepare import GAME_HASH, pe_layout, file_offset
SFSE_HASH = '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'

def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def guard():
    sys.path.insert(0, str(ROOT/'runtime/session-tools'))
    from common import guard as caller_guard
    values = caller_guard()
    if min(values.values()) < 40_000_000_000:
        raise RuntimeError('caller_available_disk_guard')
    return values

HOOKS = [(0x21b26bc,0x21e07d0,'producer_init'),
         (0x21b42e3,0x21e07d0,'producer_preview'),
         (0x21b6931,0x21e07d0,'producer_operation'),
         (0x1581a96,0x1578500,'ui'),
         (0x15785c9,0x21f8120,'region'),
         (0x15785e8,0x21f8120,'atmosphere'),
         (0x157862e,0x42e250,'water_append'),
         (0x15787e9,0x157fcf0,'row_fast_bridge'),
         (0x15787fc,0x157fde0,'row_grow_bridge'),
         (0x15784a0,0x22cdf60,'queue'),
         (0x21e0a46,0x21e0f50,'source_visit'),
         (0x7b526a,0x79f860,'provider'),
         (0x7a1a3c,0x79f860,'provider_alt')]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name', required=True)
    a = ap.parse_args()
    if not re.fullmatch('[a-zA-Z0-9-]+', a.name):
        raise ValueError('build_name')
    initial = guard()
    out = ROOT/'.local-work/local-readiness/builds'/a.name
    out.mkdir(parents=True, exist_ok=False)
    baseline = json.loads((ROOT/'.local-work/local-readiness/baseline.json').read_text())
    protected = baseline['protected']
    if protected != {p:sha(p) for p in protected}:
        raise RuntimeError('protected_changed')
    prior = json.loads((ROOT/'.local-work/native-oracle-050/builds/qualification-03/build.json').read_text())
    game = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    sfse, vcvars = Path(prior['sfse_path']), Path(prior['vcvars'])
    if sha(game) != GAME_HASH or sha(sfse) != SFSE_HASH:
        raise RuntimeError('pinned_image_mismatch')
    pe = game.read_bytes()
    base, size, sections = pe_layout(pe)
    if base != 0x140000000:
        raise RuntimeError('image_base')
    generated = '#pragma once\ninline constexpr char game_hash[]="'+GAME_HASH+'";\ninline constexpr char sfse_hash[]="'+SFSE_HASH+'";\nnamespace history { inline uint64_t image_base{};\n'
    guards = []
    for site, target, kind in HOOKS:
        off = file_offset(sections,site,32)
        b = pe[off:off+32]
        if b[0] != 0xe8 or site+5+struct.unpack_from('<i',b,1)[0] != target:
            raise RuntimeError('native_CALL_guard')
        guards.append(dict(site=site,target=target,kind=kind,length=5,original=b[:5].hex(),window_sha256=hashlib.sha256(b).hexdigest()))
        if kind=='producer_preview':
            generated += f'extern "C" unsigned char preview_producer(uint64_t a,uint64_t b,float c,float d,uint64_t actor){{return preview::produce({site},reinterpret_cast<preview::Producer>(image_base+{target}),a,b,c,d,actor);}}\nextern "C" void producer_preview_bridge();\n'
        elif kind.startswith('producer'):
            generated += f'inline unsigned char {kind}(uint64_t a,uint64_t b,float c,float d){{return preview::produce({site},reinterpret_cast<preview::Producer>(image_base+{target}),a,b,c,d);}}\n'
        elif not kind.endswith('bridge'):
            generated += f'inline uint64_t {kind}_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){{return preview::integral({site},preview::{"provider" if kind=="provider_alt" else kind},reinterpret_cast<Four>(image_base+{target}),a,b,c,d);}}\n'
    for name,site,target in [('row_fast',0x15787e9,0x157fcf0),('row_grow',0x15787fc,0x157fde0)]:
        generated += f'extern "C" uint64_t {name}(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t resource,uint64_t payload){{return preview::integral({site},preview::row,reinterpret_cast<Four>(image_base+{target}),a,b,c,d,resource,payload);}}\n'
        generated += f'extern "C" void {name}_bridge();\n'
    generated += 'struct Site{uint64_t rva,target;unsigned length;unsigned char original[8];const char* hash;Four hook;};\ninline Site sites[]={\n'
    for g in guards:
        kind=g['kind']; hook='producer_preview_bridge' if kind=='producer_preview' else kind if kind.startswith('producer') or kind.endswith('bridge') else kind+'_hook'
        generated += '{'+f'{g["site"]},{g["target"]},5,'+'{'+','.join(str(v) for v in bytes.fromhex(g['original']))+'},"'+g['window_sha256']+'",reinterpret_cast<Four>(&'+hook+')},\n'
    generated += '};\nstruct TargetGuard{uint64_t rva;const char* hash;};inline TargetGuard target_guards[]={\n'
    for target in sorted({g['target'] for g in guards}|{0x38a050}):
        off=file_offset(sections,target,32)
        generated += '{'+str(target)+',"'+hashlib.sha256(pe[off:off+32]).hexdigest()+'"},\n'
    generated += '};}\n'
    (out/'identity.generated.h').write_text(generated,encoding='utf8',newline='\n')
    paths=list(SRC.glob('*'))+[SRC/n for n in ('history.h','modules.h','patch.h')]+[ROOT/'runtime/exp0002'/n for n in ('core.h','win_support.h','third_party/sfse/PluginAPI.h','third_party/sfse/LICENSE.txt')]+[ROOT/'runtime/session-tools'/n for n in ('common.py','adapter080.py','session.py')]
    sources={str(p):sha(p) for p in paths if p.is_file()}
    (out/'build-inputs.json').write_text(json.dumps(dict(sources=sources,protected_baseline_sha256=sha(ROOT/'.local-work/local-readiness/baseline.json'),game_sha256=sha(game),sfse_sha256=sha(sfse)),indent=2)+'\n',encoding='utf8',newline='\n')
    def run(args,label):
        guard()
        r=subprocess.run(args,cwd=out,capture_output=True)
        (out/label).write_bytes(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError(f'{label}: exit {r.returncode}; log retained')
    def cmd(label,line):
        p=out/(label+'.cmd')
        p.write_text('@echo off\ncall "'+str(vcvars)+'"\nif errorlevel 1 exit /b 1\n'+line+'\n',encoding='utf8',newline='\r\n')
        run(['cmd.exe','/d','/c',str(p)],label+'.txt')
    cmd('assemble',f'where ml64.exe\nml64.exe /nologo /c /Fo bridges.obj "{SRC/"bridges.asm"}"')
    cmd('plugin',f'where cl.exe\nwhere link.exe\ncl.exe /Bv /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"plugin.cpp"}" bridges.obj /LD /Fe:SorNativePositionOracle.dll /link /INCREMENTAL:NO bcrypt.lib')
    cmd('fixture-assemble',f'ml64.exe /nologo /c /Fo fixture.obj "{SRC/"fixture.asm"}"')
    cmd('abi-assemble',f'ml64.exe /nologo /c /Fo abi.obj "{SRC/"abi_fixture.asm"}"')
    cmd('tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 "{SRC/"tests.cpp"}" bridges.obj fixture.obj abi.obj /Fe:tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'tests.exe'),str(out/'fixtures')],'qualification.txt')
    cmd('readiness-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 "{SRC/"readiness_tests.cpp"}" /Fe:readiness-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'readiness-tests.exe'),str(out/'readiness-fixtures')],'readiness-tests.txt')
    run([str(out/'readiness-tests.exe'),str(out/'bounded-fixtures'),'snapshot-limit'],'snapshot-limit-tests.txt')
    run([sys.executable,'-B',str(SRC/'test_inspect.py'),str(out/'fixtures')],'inspector-tests.txt')
    run([sys.executable,'-B',str(SRC/'test_readiness.py'),str(out/'readiness-fixtures')],'readiness-inspector-tests.txt')
    cmd('patch-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 "{SRC/"patch_tests.cpp"}" /Fe:patch-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    run([str(out/'patch-tests.exe')],'patch-qualification.txt')
    cmd('lifecycle-tests',f'cl.exe /nologo /std:c++20 /EHa /W4 /MD /O2 /I"{out}" "{SRC/"lifecycle_tests.cpp"}" bridges.obj /Fe:lifecycle-tests.exe /link /INCREMENTAL:NO bcrypt.lib')
    for scenario in ('normal','pending-stop','before-ready-stop','guard-failure','writer-failure','disk-failure','terminal-failure'):
        run([str(out/'lifecycle-tests.exe'),str(out/('lifecycle-'+scenario)),scenario],'lifecycle-'+scenario+'.txt')
    cmd('dependencies','where dumpbin.exe\ndumpbin.exe /DEPENDENTS SorNativePositionOracle.dll')
    imports=re.findall(r'^\s+([A-Za-z0-9_.-]+\.dll)\s*$',(out/'dependencies.txt').read_text(errors='replace'),re.M|re.I)
    allowed={'kernel32.dll','bcrypt.dll','msvcp140.dll','vcruntime140.dll','vcruntime140_1.dll'}
    if not imports or any(n.lower() not in allowed and not n.lower().startswith('api-ms-win-crt-') for n in imports):raise RuntimeError('unexpected_dependency')
    package=out/'package';plugins=package/'Data/SFSE/Plugins';plugins.mkdir(parents=True)
    shutil.copyfile(out/'SorNativePositionOracle.dll',plugins/'SorNativePositionOracle.dll')
    notices=package/'ResearchNotices';notices.mkdir()
    shutil.copyfile(ROOT/'runtime/exp0002/third_party/sfse/LICENSE.txt',notices/'SFSE-PluginAPI-LICENSE.txt')
    shutil.copyfile(ROOT/'LICENSE',notices/'PROJECT-LICENSE.txt')
    (notices/'README.txt').write_text('0.8.0 OFFLINE_REVIEW_ONLY. See local-readiness report/run-card.\n',encoding='utf8',newline='\n')
    archive=out/'SorNativePositionOracle-0.8.0.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(package.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(package).as_posix())
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise RuntimeError('zip_integrity')
        for p in package.rglob('*'):
            if p.is_file() and z.read(p.relative_to(package).as_posix())!=p.read_bytes():raise RuntimeError('zip_bytes')
    if protected!={p:sha(p) for p in protected} or sources!={p:sha(p) for p in sources}:raise RuntimeError('post_build_preservation')
    runtime={str(Path('C:/Windows/System32')/n):sha(Path('C:/Windows/System32')/n) for n in ('msvcp140.dll','vcruntime140.dll','vcruntime140_1.dll','ucrtbase.dll')}
    compiler_tools={}
    for label in ('assemble','plugin','dependencies'):
        for line in (out/(label+'.txt')).read_text(errors='replace').splitlines():
            p=Path(line.strip())
            if p.name.lower() in ('ml64.exe','cl.exe','link.exe','dumpbin.exe') and p.is_file():compiler_tools[str(p)]=sha(p)
    manifest=dict(version='0.8.0',schema=8,authority='OFFLINE_REVIEW_ONLY',game_path=str(game),game_hash=GAME_HASH,sfse_path=str(sfse),sfse_hash=SFSE_HASH,image_base=base,image_size=size,guards=guards,sources=sources,protected=protected,initial_disk=initial,final_disk=guard(),vcvars=str(vcvars),vcvars_sha256=sha(vcvars),compiler_tools=compiler_tools,external_runtime=runtime,imported_dlls=imports,runtime_essential=['Data/SFSE/Plugins/SorNativePositionOracle.dll'],files={p.relative_to(package).as_posix():dict(size=p.stat().st_size,sha256=sha(p)) for p in package.rglob('*') if p.is_file()},zip_sha256=sha(archive),generated_header_sha256=sha(out/'identity.generated.h'))
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
    run([sys.executable,'-B',str(SRC/'test_operate.py'),str(out)],'operational-tests.txt')
    if sources!={p:sha(p) for p in sources}:raise RuntimeError('post_operational_source_drift')
    print(json.dumps(dict(output=str(out),zip_sha256=sha(archive))))

if __name__=='__main__':main()
