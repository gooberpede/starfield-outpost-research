# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline native build and disposable host qualification; no game/deployment.

Reads pinned installed inputs, owned source and approved SFSE header. Writes a
fresh task-local build and receipts. Runs MSVC/MASM and disposable fixtures only.
Uses installed Windows SDK/CPython stdlib; no downloads or dependency installation.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).parent
LOCAL = ROOT/'.local-work/d5p'
GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
GAME_HASH = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
SFSE_HASH = '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b'
SITES = [(0x79fccb,0x3499f0,5),(0x79feaf,0x78d660,5),(0x79ff18,0x79b520,5),
         (0x79b8e8,0x2339340,5),(0x79aced,0x7ac2f0,5),(0x79fca3,0,9),
         (0x79ddf0,0,5),(0x79d910,0,5),(0x975030,0,8),(0x9829b0,0,5),(0x982b70,0,5)]


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def guard():
    free = {p:shutil.disk_usage(p).free for p in ('C:/','D:/')}
    if min(free.values()) < 40_000_000_000:
        raise RuntimeError('disk floor')
    return free


def pe_read(data, rva, size):
    at = struct.unpack_from('<I',data,0x3c)[0]
    assert data[at:at+4] == b'PE\0\0'
    n, opt = struct.unpack_from('<H',data,at+6)[0], struct.unpack_from('<H',data,at+20)[0]
    for i in range(n):
        p = at+24+opt+i*40
        virtual_size, va, raw_size, raw = struct.unpack_from('<4I',data,p+8)
        if va <= rva and rva+size <= va+raw_size:
            return data[raw+rva-va:raw+rva-va+size]
    raise ValueError('unbacked RVA')


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+',label)
    start = guard()
    out = LOCAL/label
    out.mkdir(parents=True,exist_ok=False)
    prior = json.loads((ROOT/'.local-work/native-oracle-050/builds/qualification-03/build.json').read_text())
    sfse = Path(prior['sfse_path'])
    pins = {GAME/'Starfield.exe':GAME_HASH, sfse:SFSE_HASH,
            GAME/'Data/Starfield.esm':'1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7',
            GAME/'Data/Starfield - PlanetData.ba2':'2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'}
    assert all(sha(p)==h for p,h in pins.items())
    data = (GAME/'Starfield.exe').read_bytes()
    generated = '#pragma once\nnamespace retained {\n'
    generated += f'inline constexpr uint32_t game_version=(1u<<24)|(16u<<16)|(244u<<4);\ninline constexpr char game_hash[]="{GAME_HASH}",sfse_hash[]="{SFSE_HASH}";\n'
    generated += 'struct Site {uint64_t rva,target;unsigned length;const char* hash;};inline Site sites[]={\n'
    rows = []
    for i,(rva,target,n) in enumerate(SITES):
        b = pe_read(data,rva,32)
        if i<5:
            assert b[0]==0xe8 and rva+5+struct.unpack_from('<i',b,1)[0]==target
        elif i==5:
            assert b[:5]==bytes.fromhex('4084f60f85') and rva+9+struct.unpack_from('<i',b,5)[0]==0x79ffaa
        elif i==8:
            assert b[:8]==bytes.fromhex('405356574883ec30')
        else:
            assert b[:4] in (bytes.fromhex('48895c24'),)
        h=hashlib.sha256(b).hexdigest()
        rows.append(dict(rva=rva,target=target,length=n,sha256=h))
        generated += f'{{{rva},{target},{n},"{h}"}},\n'
    generated += '};struct Target {uint64_t rva;const char* hash;};inline Target target_guards[]={\n'
    for target in sorted({t for _,t,_ in SITES if t}):
        generated += f'{{{target},"{hashlib.sha256(pe_read(data,target,32)).hexdigest()}"}},\n'
    generated += '};}\n'
    (out/'identity.generated.h').write_text(generated,encoding='utf8',newline='\n')
    sources = {str(p):sha(p) for p in SRC.iterdir() if p.is_file()}
    for name in ('core.h','win_support.h','third_party/sfse/PluginAPI.h','third_party/sfse/LICENSE.txt'):
        p=ROOT/'runtime/exp0002'/name;sources[str(p)]=sha(p)
    def run(cmd, log, expected=0):
        guard()
        r=subprocess.run(cmd,cwd=out,capture_output=True)
        (out/log).write_bytes(r.stdout+r.stderr)
        assert r.returncode==expected,(log,r.returncode)
        return r.returncode
    def compile(name,lines):
        p=out/(name+'.cmd')
        p.write_text('@echo off\ncall "'+str(VC)+'"\nif errorlevel 1 exit /b 1\n'+
                     '\nif errorlevel 1 exit /b 1\n'.join(lines)+'\n',encoding='utf8',newline='\r\n')
        run(['cmd','/d','/c',str(p)],name+'.log')
    compile('compile',[
        'where cl.exe','where ml64.exe','where link.exe',
        f'ml64 /nologo /c /Fo visited.obj "{SRC/"visited.asm"}"',
        f'ml64 /nologo /c /Fo native-fixture.obj "{SRC/"fixture.asm"}"',
        f'cl /Bv /nologo /std:c++20 /EHa /W4 /O2 /MD /I"{out}" "{SRC/"plugin.cpp"}" "{SRC/"fixture.cpp"}" visited.obj native-fixture.obj /LD /Fe:SorRetainedPopulation.dll /link /INCREMENTAL:NO bcrypt.lib',
        f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD "{SRC/"host.cpp"}" /Fe:sor-d5p-fixture.exe /link /INCREMENTAL:NO',
        'dumpbin /DEPENDENTS SorRetainedPopulation.dll'])
    def qualify(scenario):
        code={'crash-before':71,'crash-after':72}.get(scenario,0)
        run([str(out/'sor-d5p-fixture.exe'),str(out/'SorRetainedPopulation.dll'),str(out/scenario),scenario],scenario+'.log',code)
        return dict(scenario=scenario,exit=code)
    with ThreadPoolExecutor(max_workers=8) as pool:
        cases=list(pool.map(qualify,('normal','mask-zero','unexpected-mask','mixed-partial','owner-change','mode-change','owner-mismatch','descriptor-change','guard-reject','partial','inserted-empty','bad-read','generation-exception','failed-copy','contrary','nested','concurrent','concurrent-miss','hit-only','bypass','reset','aba','destroy','erase','clear','retire','overflow','output-failure','crash-before','crash-after','worker-stop','worker-failure','worker-guard','worker-continuous')))
    run([sys.executable,'-B',str(SRC/'qualify.py'),str(out)],'reader-qualification.log')
    assert all(sha(p)==h for p,h in sources.items())
    assert all(sha(p)==h for p,h in pins.items())
    result=dict(schema='sor-d5p-build/1',authority='PHASE_A_ONLY',initial_free=start,final_free=guard(),
                installed={str(p):h for p,h in pins.items()},sources=sources,sites=rows,vcvars_sha256=sha(VC),
                dll_sha256=sha(out/'SorRetainedPopulation.dll'),host_sha256=sha(out/'sor-d5p-fixture.exe'),cases=cases)
    (out/'build.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(out=str(out),dll_sha256=result['dll_sha256'],cases=len(cases))))


if __name__=='__main__':
    main()
