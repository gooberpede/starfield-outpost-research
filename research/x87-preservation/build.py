# SPDX-License-Identifier: GPL-3.0-or-later
"""Extend the owned baseline without modifying it; run only a disposable fixture.

Reads sibling sources and installed MSVC/MASM; writes a new exclusive ignored
run directory, generated source/assembly, binaries, raw synthetic records and
hash receipts. No network, game, other process, saves, index or ref operations.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).parent
BASE = SRC.parent / 'internal-observation-qualification'
VC = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def sources(corrected=False):
    spec = importlib.util.spec_from_file_location('owned_build', BASE / 'build.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    asm = module.assembly()
    asm = replace_once(asm, '.code\n', 'seed_control WORD 077fh\n.code\nEXTERN diagnostic_handler:PROC\n')
    asm = replace_once(asm, 'fninit\nfld1\nfldpi',
                       'fninit\nfldcw seed_control\nfld1\nfldz\nfldpi\nfchs\nfld qword ptr [rsi+16]\nftst\nffree st(2)\nfadd qword ptr [rsi+16]')
    # This CPU leaves FDP zero after the arithmetic above. Seed a known full-width
    # FDP using an explicit restore, then measure the architectural result rather
    # than treating the authored image as evidence of successful restoration.
    asm = asm.replace('228h', '428h').replace('rsp+220h', 'rsp+420h')
    asm = replace_once(asm, 'fadd qword ptr [rsi+16]', '''fadd qword ptr [rsi+16]
fxsave64 [rsp+220h]
mov [rsp+408h],rax
lea rax,[rsi+16]
mov [rsp+230h],rax
mov word ptr [rsp+226h],321h
mov word ptr [rsp+222h],6501h
mov rax,[rsp+408h]
fxrstor64 [rsp+220h]''')
    # Adjacent repeated saves qualify the measurement itself. No x87 arithmetic
    # occurs between the pre-trap saves, trap and controlled post boundary.
    asm = asm.replace('fxsave64 [r15+704]', 'fxsave64 [r15+704]\nfxsave64 [r15+4096]\nfxsave [r15+4608]')
    asm = replace_once(asm, 'END\n', '''entry_handler PROC FRAME
sub rsp,228h
.allocstack 228h
.endprolog
fxsave64 [rsp+20h]
lea rdx,[rsp+20h]
call diagnostic_handler
add rsp,228h
ret
entry_handler ENDP
PUBLIC entry_handler
END
''')
    native = (BASE / 'native.cpp').read_text()
    native = replace_once(native, '#include <chrono>', '#include <chrono>\n#include "diagnostic.h"')
    native = replace_once(native, 'static std::atomic<bool> admitting{true};',
                          'static std::atomic<bool> admitting{true}, stop_hold{}, stop_entered{}, stop_release{};')
    native = replace_once(native, 'bytes[3072]', 'bytes[5184]')
    native = native.replace('closure[2]{0,0x22334455}', 'closure[3]{0,0x22334455,0x3ff4000000000000ull}')
    native = replace_once(native, 'static LONG CALLBACK handler(EXCEPTION_POINTERS* e)',
                         'extern "C" LONG diagnostic_handler(EXCEPTION_POINTERS* e, const void* entry)')
    native = replace_once(native, 'auto saved_error = GetLastError();', '''auto state = reinterpret_cast<unsigned char*>(e->ContextRecord->R15);
    std::memcpy(state+3072,entry,512);
    std::memcpy(state+3584,&e->ContextRecord->FltSave,512);
    auto saved_error = GetLastError();
    if (diagnostic_condition == 1) {
        e->ContextRecord->Rip = reinterpret_cast<DWORD64>(
            site == reinterpret_cast<void*>(accept_site) ? accept_resume : reject_resume);
        return EXCEPTION_CONTINUE_EXECUTION;
    }''')
    native = replace_once(native, 'probe(&child,closure,0); ++nested;',
                         'probe(&child,closure,0); diagnostic_write(child.bytes,0,1); ++nested;')
    native = replace_once(native, 'probe(&state,closure,mode);',
                         'probe(&state,closure,mode); diagnostic_write(state.bytes,mode,0);')
    native = replace_once(native, '--depth; --live;', '''if (stop_hold) {
        stop_entered=true;
        while(!stop_release) std::this_thread::yield();
    }
    --depth; --live;''')
    native = replace_once(native, 'admitting=false; exit_workers=true;', '''stop_hold=true;
    while(!stop_entered) std::this_thread::yield();
    check(live>0,"STOP with handler in flight");
    std::printf("STOP_inflight_confirmed=true\\n");
    admitting=false; stop_hold=false; stop_release=true; exit_workers=true;''')
    native = replace_once(native, 'int main() {', 'int main(int argc, char** argv) {\n    diagnostic_open(argc,argv);')
    native = replace_once(native, 'auto h=AddVectoredExceptionHandler(1,handler);',
                         'diagnostic_condition = diagnostic_requested;\n    auto h=AddVectoredExceptionHandler(1,entry_handler);')
    native = replace_once(native, 'inject_nested=true; run(1); inject_nested=false;', '''if (diagnostic_requested == 1) {
        for(unsigned repeat=0;repeat<32;++repeat)
            for(unsigned mode=0;mode<3;++mode) run(mode);
        patch(false); check(RemoveVectoredExceptionHandler(h)!=0,"minimal retirement");
        diagnostic_condition=0;
        for(unsigned mode=0;mode<3;++mode) run(mode);
        diagnostic_close();
        std::printf("minimal mapped failures=%u x87 pointer losses=%u\\n",failures.load(),x87_pointer_losses.load());
        return failures ? 2 : 0;
    }
    inject_nested=true; run(1); inject_nested=false;''')
    native = replace_once(native, 'for(unsigned mode=0;mode<3;++mode) run(mode);\n    std::printf',
                         'diagnostic_condition=0;\n    for(unsigned mode=0;mode<3;++mode) run(mode);\n    diagnostic_close();\n    std::printf')
    geometry = (BASE/'geometry.cpp').read_text()
    geometry = replace_once(geometry, 'state[3072]', 'state[5184]')
    geometry = replace_once(geometry, 'closure[2]{r->h.token+(fault==13 ? 1 : 0),0x22334455}',
                            'closure[3]{r->h.token+(fault==13 ? 1 : 0),0x22334455,0x3ff4000000000000ull}')
    if corrected:
        # Exactly one correction: the raw CONTEXT stays untouched; a separate
        # invocation-owned image combines its SIMD state with captured pointers.
        # Keep the original entry and CONTEXT images intact for comparison.
        native = replace_once(native, 'std::memcpy(state+3584,&e->ContextRecord->FltSave,512);',
                              '''std::memcpy(state+3584,&e->ContextRecord->FltSave,512);
    std::memcpy(state+5120,&e->ContextRecord->FltSave,512);
    std::memcpy(state+5128,static_cast<const unsigned char*>(entry)+8,16);''')
        native = replace_once(native, 'bytes[5184]', 'bytes[5696]')
        geometry = replace_once(geometry, 'state[5184]', 'state[5696]')
        # The two instructions preserve GP/flags and AVX upper halves. This
        # restore image is fixture-owned, never a borrowed CONTEXT pointer.
        for label in ('accept_resume', 'reject_resume'):
            asm = replace_once(asm, label+' PROC\n', label+' PROC\nfxrstor64 [r15+5120]\n')
    return asm, native, geometry


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name', required=True)
    ap.add_argument('--corrected', action='store_true')
    args = ap.parse_args()
    assert args.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.name)
    out = ROOT / '.local-work/x87-preservation' / args.name
    out.mkdir(parents=True, exist_ok=False)
    for drive in ('C:/', 'D:/'):
        import shutil
        assert shutil.disk_usage(drive).free >= 40_000_000_000, 'DISK_GUARD'
    asm, native, geometry = sources(args.corrected)
    (out/'fixture.asm').write_text(asm, encoding='utf8', newline='\n')
    (out/'native.cpp').write_text(native, encoding='utf8', newline='\n')
    (out/'geometry.cpp').write_text(geometry, encoding='utf8', newline='\n')
    for p in [*SRC.glob('*'), BASE/'capture.h', BASE/'build.py', BASE/'native.cpp', BASE/'geometry.cpp']:
        if p.is_file():
            name = 'baseline-'+p.name if p.parent == BASE and p.name in ('build.py','native.cpp','geometry.cpp') else p.name
            (out/name).write_bytes(p.read_bytes())
    commands = [f'call "{VC}"', 'if errorlevel 1 exit /b 1',
                'ml64 /nologo /c /Flfixture.lst fixture.asm', 'if errorlevel 1 exit /b 1',
                f'cl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /arch:AVX /DDIAGNOSTIC_CORRECTED={int(args.corrected)} native.cpp diagnostic.cpp geometry.cpp fixture.obj /Fe:fixture.exe /link /INCREMENTAL:NO',
                'if errorlevel 1 exit /b 1']
    for condition in ('minimal', 'adversarial'):
        commands += [f'mkdir {condition}', f'pushd {condition}', f'..\\fixture.exe {condition}',
                     'if not "%errorlevel%"=="0" exit /b %errorlevel%', 'popd']
    commands += ['exit /b 0']
    (out/'run.cmd').write_text('@echo off\n'+'\n'.join(commands)+'\n', encoding='utf8', newline='\r\n')
    run = subprocess.run(['cmd','/c',str(out/'run.cmd')],cwd=out,capture_output=True)
    (out/'run.log').write_bytes(run.stdout+run.stderr)
    files = [p for p in out.rglob('*') if p.is_file()]
    files += [VC, *BASE.glob('*')]
    toolroot = VC.parents[2]/'Tools/MSVC/14.51.36231/bin/Hostx64/x64'
    files += [toolroot/n for n in ('cl.exe','ml64.exe','link.exe')]
    manifest = dict(exit_code=run.returncode, corrected=args.corrected, python=sys.version,
                    platform=platform.platform(), win32_version=platform.win32_ver(),
                    files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()})
    (out/'build.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
    print((run.stdout+run.stderr).decode(errors='replace')[-6000:])
    raise SystemExit(run.returncode)


if __name__ == '__main__':
    main()
