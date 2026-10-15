# SPDX-License-Identifier: GPL-3.0-or-later
"""Build/run only original disposable x64 fixtures; see README.md for effects.

No downloads, SFSE, target invocation, target writes, or Git mutations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).parent
OUT = ROOT / '.local-work/internal-observation-qualification/native'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def assembly():
    # All machine code is original fixture code. No game instructions/bytes copied.
    regs = 'rax rbx rcx rdx rbp rsi rdi r8 r9 r10 r11 r12 r13 r14 r15 rsp'.split()
    def snapshot(base):
        lines = [f'mov [r15+{base+i*8}],{reg}' for i, reg in enumerate(regs)]
        lines += ['pushfq', f'pop qword ptr [r15+{base+128}]']
        lines += [f'vmovdqu ymmword ptr [r15+{base+160+i*32}],ymm{i}' for i in range(16)]
        lines += [f'fxsave64 [r15+{base+704}]']
        return '\n'.join(lines)
    pro = ['OPTION NOSCOPED', '.const', 'ALIGN 16', 'lane_patterns LABEL DWORD']
    for i in range(16):
        pro += ['DWORD '+','.join(f'{0x3f000000+i*16+j:08x}h' for j in range(8))]
    pro += ['.code', 'PUBLIC probe, accept_site, reject_site, accept_resume, reject_resume, disturb',
           'probe PROC FRAME']
    for reg in 'rbx rbp rsi rdi r12 r13 r14 r15'.split():
        pro += [f'push {reg}', f'.pushreg {reg}']
    pro += ['sub rsp,228h', '.allocstack 228h', '.endprolog',
            'fxsave64 [rsp+20h]', 'mov [rsp+220h],r8', 'mov r15,rcx', 'mov rsi,rdx']
    for i, reg in enumerate('rax rbx rcx rdx rbp rdi r8 r9 r10 r11 r12 r13 r14'.split()):
        pro += [f'mov {reg},{0x11110000+i*0x100}']
    for i in range(16):
        pro += [f'vmovups ymm{i},ymmword ptr [lane_patterns+{i*32}]']
    pro += ['fninit', 'fld1', 'fldpi', 'cmp qword ptr [rsp+220h],0', 'jz reject_path',
            # Two entry routes to the accept join, including a cleanup-like call.
            'cmp qword ptr [rsp+220h],2', 'jne accept_path', 'call cleanup_fixture',
            'accept_path:', 'cmp qword ptr [rsp+220h],2', 'je alternate_flags',
            'push 0ad7h', 'jmp flags_ready', 'alternate_flags:', 'push 202h',
            'flags_ready:', 'popfq', snapshot(0),
            'accept_site:', 'mov rbx,[rsi+8]', 'accept_cont:', snapshot(1536), 'jmp finished',
            'reject_path:', 'push 0ad7h', 'popfq', snapshot(0),
            'reject_site:', 'add rbx,30h', 'reject_cont:', snapshot(1536),
            'finished:', 'fxrstor64 [rsp+20h]', 'add rsp,228h']
    for reg in reversed('rbx rbp rsi rdi r12 r13 r14 r15'.split()):
        pro += [f'pop {reg}']
    pro += ['ret', 'probe ENDP', 'cleanup_fixture PROC', 'ret', 'cleanup_fixture ENDP',
            # Leaf continuations do not change RSP or call helpers.
            'accept_resume PROC', 'mov rbx,[rsi+8]', 'jmp accept_cont', 'accept_resume ENDP',
            'reject_resume PROC', 'add rbx,30h', 'jmp reject_cont', 'reject_resume ENDP',
            'disturb PROC', 'mov rax,999', 'mov rcx,888', 'mov rdx,777',
            'mov r8,666', 'mov r9,555', 'mov r10,444', 'mov r11,333']
    for i in range(6):
        pro += [f'vxorps xmm{i},xmm{i},xmm{i}']
    pro += ['vzeroupper', 'fninit', 'sub rsp,8', 'stmxcsr [rsp]',
            'xor dword ptr [rsp],6000h', 'ldmxcsr [rsp]', 'add rsp,8', 'clc', 'ret', 'disturb ENDP', 'END']
    return '\n'.join(pro) + '\n'


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    name = parser.parse_args().name
    if not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in name):
        raise ValueError('invalid disposable run name')
    OUT = OUT.parent / name
    OUT.mkdir(parents=True, exist_ok=False)
    for name in ('build.py','native.cpp','geometry.cpp','capture.h'):
        (OUT/name).write_bytes((SRC/name).read_bytes())
    (OUT/'fixture.asm').write_text(assembly(), encoding='utf-8', newline='\n')
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1',
                'ml64 /nologo /c fixture.asm', 'if errorlevel 1 exit /b 1',
                f'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /arch:AVX "{SRC / "native.cpp"}" "{SRC / "geometry.cpp"}" fixture.obj /Fe:fixture.exe /link /INCREMENTAL:NO',
                'if errorlevel 1 exit /b 1', 'fixture.exe', 'exit /b %errorlevel%']
    (OUT/'run.cmd').write_text('@echo off\n'+'\n'.join(commands)+'\n', encoding='utf-8', newline='\r\n')
    run = subprocess.run(['cmd', '/c', str(OUT/'run.cmd')], cwd=OUT, capture_output=True)
    (OUT/'run.log').write_bytes(run.stdout + run.stderr)
    files = [SRC/n for n in ('build.py','native.cpp','geometry.cpp','capture.h')]+[OUT/'fixture.asm',VC]
    toolroot = VC.parents[2]/'Tools/MSVC/14.51.36231/bin/Hostx64/x64'
    files += [toolroot/n for n in ('cl.exe', 'ml64.exe', 'link.exe')]
    files += [p for p in OUT.iterdir() if p.is_file() and p.name != 'build.json']
    manifest = {'exit_code': run.returncode, 'python': sys.version,
                'files': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (OUT/'build.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(run.stdout.decode(errors='replace')[-4000:])
    print(run.stderr.decode(errors='replace')[-1000:])
    raise SystemExit(run.returncode)


if __name__ == '__main__':
    main()
