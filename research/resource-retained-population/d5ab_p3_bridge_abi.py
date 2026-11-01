# SPDX-License-Identifier: GPL-3.0-or-later
"""Link the exact final bridge object into an independent disposable ABI caller.

Reads a completed build's bridges.obj and uses installed MSVC/MASM/SDK. Writes
only a fresh ignored test directory with original generated caller/stub source,
compiler logs, executable and measured results. Capture stubs deliberately
clobber volatile state; they do not fabricate observer events. No game, saves,
analysis database, network, external dependency or Git mutation is involved.
This is an object-level ABI test, separately labeled from full observer hosts.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
ASM = r'''; SPDX-License-Identifier: GPL-3.0-or-later
EXTERN selected_bridge:PROC
EXTERN visited_bridge:PROC
EXTERN birth_bridge:PROC
EXTERN published_bridge:PROC
EXTERN stored_bridge:PROC
.code
clobber MACRO name
PUBLIC name
name PROC
 xor eax,eax
 stc
 mov rcx,1234h
 mov rdx,5678h
 mov r8,1111h
 mov r9,2222h
 mov r10,3333h
 mov r11,4444h
 pxor xmm0,xmm0
 pxor xmm1,xmm1
 pxor xmm2,xmm2
 pxor xmm3,xmm3
 pxor xmm4,xmm4
 pxor xmm5,xmm5
 ret
name ENDP
ENDM
clobber selected_capture
clobber visited_capture
clobber birth_capture
clobber published_capture
clobber stored_capture
PUBLIC abi_caller
abi_caller PROC FRAME
 push rbx
 .pushreg rbx
 push rsi
 .pushreg rsi
 push rdi
 .pushreg rdi
 push rbp
 .pushreg rbp
 push r12
 .pushreg r12
 push r13
 .pushreg r13
 push r14
 .pushreg r14
 push r15
 .pushreg r15
 sub rsp,208h
 .allocstack 208h
 .endprolog
 mov r15,rcx
 lea rbp,[rsp+100h]
 mov rbx,1111222233334444h
 mov r13,112233445566h
 mov r14,1234560000h
 mov [rsp+80h],r14
 lea rdx,[rsp+80h]
 xor eax,eax
 call selected_bridge
 mov [r15],rdx
 mov rax,[rsp+38h]
 mov [r15+8],rax
 pushfq
 pop rax
 mov [r15+16],rax
 mov [r15+24],rbp
 lea rax,[rsp+100h]
 mov [r15+32],rax
 mov rax,777788889999aaaah
 mov [rbp+10h],rax
 xor esi,esi
 mov rdi,5555666677778888h
 call visited_bridge
 pushfq
 pop rax
 mov [r15+40],rax
 mov rax,[rbp+10h]
 mov [r15+48],rax
 mov rax,777788889999aaaah
 mov [rbp+10h],rax
 mov esi,1
 call visited_bridge
 pushfq
 pop rax
 mov [r15+56],rax
 mov rax,[rbp+10h]
 mov [r15+64],rax
 lea r12,[rsp+160h]
 call birth_bridge
 pushfq
 pop rax
 mov [r15+120],rax
 mov [r15+72],rcx
 mov [r15+80],rdx
 lea rax,[rsp+90h]
 mov [r15+88],rax
 lea rax,[rsp+180h]
 mov [r12+8],rax
 mov eax,2
 call published_bridge
 mov rax,[rsp+190h]
 mov [r15+96],rax
 mov eax,3
 call stored_bridge
 mov rax,[rsp+198h]
 mov [r15+104],rax
 mov [r15+112],rbp
 add rsp,208h
 pop r15
 pop r14
 pop r13
 pop r12
 pop rbp
 pop rdi
 pop rsi
 pop rbx
 ret
abi_caller ENDP
END
'''
CPP = r'''// SPDX-License-Identifier: GPL-3.0-or-later
#include <Windows.h>
#include <cstdint>
#include <cstdio>
extern "C" void abi_caller(uint64_t*);
int main(){SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);uint64_t result[16]{};
 abi_caller(result);std::printf("[");for(unsigned i=0;i<16;++i)std::printf("%s%llu",i?",":"",(unsigned long long)result[i]);std::printf("]\n");return 0;}
'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build, out = ((ROOT / name).resolve() for name in sys.argv[1:3])
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    assert min(shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')) >= 40_000_000_000
    out.mkdir(parents=True, exist_ok=False)
    (out / 'source.py').write_bytes(Path(__file__).read_bytes())
    (out / 'caller.asm').write_text(ASM, encoding='utf8', newline='\n')
    (out / 'caller.cpp').write_text(CPP, encoding='utf8', newline='\n')
    obj = build / 'bridges.obj'
    expected_obj = sha(obj)
    script = '@echo off\n' + f'call "{VC}"\nif errorlevel 1 exit /b 1\n'
    script += 'ml64 /nologo /c /Focaller-asm.obj caller.asm\nif errorlevel 1 exit /b 1\n'
    script += f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD caller.cpp caller-asm.obj "{obj}" /Fe:bridge-abi.exe /link /Brepro /INCREMENTAL:NO\n'
    (out / 'build.cmd').write_text(script, encoding='utf8', newline='\r\n')
    compilation = subprocess.run(['cmd', '/d', '/c', str(out / 'build.cmd')], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(compilation.stdout + compilation.stderr)
    assert compilation.returncode == 0
    execution = subprocess.run([str(out / 'bridge-abi.exe')], cwd=out, capture_output=True)
    (out / 'execution.log').write_bytes(execution.stdout + execution.stderr)
    assert execution.returncode == 0
    values = json.loads(execution.stdout)
    checks = {
        'selected-displaced-load-and-original-stack-slot': values[0] == values[1] == 0x1234560000,
        'selected-native-flags': values[2] & 0x8c5 == 0x44,
        'native-rbp-preserved': values[3] == values[4] == values[14],
        'visited-unvisited-test-flags': values[5] & 0x8c5 == 0x44,
        'visited-unvisited-relocated-native-store': values[6] == 0x1111222233334444,
        'visited-bypass-test-flags': values[7] & 0x8c5 == 0,
        'visited-bypass-native-slot-unchanged': values[8] == 0x777788889999aaaa,
        'birth-displaced-rcx': values[9] == 0x1234560070,
        'birth-displaced-rdx-original-frame': values[10] == values[11],
        'birth-displaced-lea-flags': values[15] & 0x8c5 == 0,
        'publication-actual-slot': values[12] == 0x1234560000,
        'visited-store-actual-slot': values[13] == 0x5555666677778888,
        'exact-final-object-unchanged': sha(obj) == expected_obj,
    }
    receipt = dict(schema='sor-d5ab-p3-bridge-object-abi/1', scope='Exact compiled bridge object with independent caller and clobber stubs; not full observer.',
                   object=str(obj), object_sha256=expected_obj, source_sha256=sha(__file__),
                   values=values, checks=checks, passed=all(checks.values()),
                   outputs={p.name: sha(p) for p in out.iterdir() if p.is_file()})
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(out=str(out), checks=len(checks), failures=[name for name, ok in checks.items() if not ok])))
    return not receipt['passed']


if __name__ == '__main__':
    raise SystemExit(main())
