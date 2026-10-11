"""SPDX-License-Identifier: GPL-3.0-or-later
Final disposable thread-control diagnosis; NOT an acquisition candidate.
Reads pinned project source/0.1.4 fixtures and installed MSVC/SDK. Builds only in
a new ignored directory; attaches only its own hash-checked event_fixture.exe.
Diagnostic source derives from the pinned project adapter by exact substitutions.
Writes private API/context traces and original WAL; never changes the baseline.
Uses only Python stdlib and the original project bounded read-only verifier.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'debugger/event-oracle'
OLD = ROOT / '.local-work/event-instrumentation/startup-candidate-014-03'
PIN = '6606a9b77991d3f1333eda33b213cf5449c42fb4b1b67f15dae0da7b25578497'
sys.path.insert(0, str(ROOT / 'debugger/exp0002a'))
sys.path.insert(0, str(SOURCE))
from process_read import ProcessRead
from materialize_epochs import decode


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def guard():
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    if min(free.values()) < 40_000_000_000:
        raise RuntimeError('both-drive disk guard')
    return free


def save(path, value):
    guard()
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def replace_once(text, old, new):
    assert text.count(old) == 1, old[:100]
    return text.replace(old, new)


TRACE = r'''
    void trace(const std::string& fields){
        auto saved=GetLastError();
        if(disk()){std::fprintf(stderr,"TRACE {%s}\n",fields.c_str());std::fflush(stderr);}
        SetLastError(saved);
    }
    void thread_trace(const char* phase,DWORD tid,HANDLE h,DWORD result,DWORD error){
        auto saved=GetLastError();
        PUBLIC_OBJECT_BASIC_INFORMATION info{};ULONG size{};
        using Query=NTSTATUS(NTAPI*)(HANDLE,OBJECT_INFORMATION_CLASS,PVOID,ULONG,PULONG);
        auto query=(Query)GetProcAddress(GetModuleHandleW(L"ntdll.dll"),"NtQueryObject");
        auto status=query?query(h,ObjectBasicInformation,&info,sizeof info,&size):NTSTATUS(-1);
        DWORD old_exit=0;SetLastError(0);auto old_ok=GetExitCodeThread(h,&old_exit);auto old_error=old_ok?0:GetLastError();
        SetLastError(0);auto other=OpenThread(SYNCHRONIZE|THREAD_QUERY_LIMITED_INFORMATION,FALSE,tid);auto open_error=other?0:GetLastError();
        DWORD other_exit=0;BOOL other_ok=FALSE;DWORD other_error=0,wait=WAIT_FAILED;
        if(other){SetLastError(0);other_ok=GetExitCodeThread(other,&other_exit);other_error=other_ok?0:GetLastError();wait=WaitForSingleObject(other,0);CloseHandle(other);}
        trace("\"kind\":\"thread_api\",\"phase\":"+quote(phase)+",\"tid\":"+std::to_string(tid)+",\"handle\":"+quote(hex((uint64_t)h))+
            ",\"result\":"+std::to_string(result)+",\"error\":"+std::to_string(error)+",\"query_status\":"+std::to_string((long)status)+",\"granted_access\":"+std::to_string(info.GrantedAccess)+
            ",\"same_query_ok\":"+std::to_string(old_ok)+",\"same_query_error\":"+std::to_string(old_error)+",\"same_exit\":"+std::to_string(old_exit)+
            ",\"open_query_error\":"+std::to_string(open_error)+",\"independent_query_ok\":"+std::to_string(other_ok)+",\"independent_query_error\":"+std::to_string(other_error)+",\"independent_exit\":"+std::to_string(other_exit)+",\"wait\":"+std::to_string(wait)+",\"owned_increments\":"+std::to_string(std::count(suspended.begin(),suspended.end(),tid)));
        SetLastError(saved);
    }
'''


def diagnostic_source(query_handles, defer_queued=False, minimum_handles=False):
    assert sha(SOURCE / 'adapter.cpp') == PIN
    text = (SOURCE / 'adapter.cpp').read_text()
    text = replace_once(text, '#include <TlHelp32.h>', '#include <TlHelp32.h>\n#include <winternl.h>')
    text = replace_once(text, '    void require(bool ok', TRACE + '\n    void require(bool ok')
    text = replace_once(text, 'if(SuspendThread(h)==DWORD(-1)){',
                        'SetLastError(0);auto sr=SuspendThread(h);auto se=sr==DWORD(-1)?GetLastError():0;thread_trace("suspend",tid,h,sr,se);SetLastError(se);if(sr==DWORD(-1)){')
    text = replace_once(text, 'require(GetExitCodeThread(h,&status)&&status!=STILL_ACTIVE,"suspend_live_thread");',
                        'SetLastError(0);auto ok=GetExitCodeThread(h,&status);auto qe=ok?0:GetLastError();thread_trace("exit_query_after_failed_suspend",tid,h,ok,qe);SetLastError(qe);require(ok&&status!=STILL_ACTIVE,"suspend_live_thread");')
    text = replace_once(text, 'if(threads.count(tid))require(ResumeThread(threads.at(tid))!=DWORD(-1),"resume");',
                        'if(threads.count(tid)){SetLastError(0);auto rr=ResumeThread(threads.at(tid));auto re=rr==DWORD(-1)?GetLastError():0;thread_trace("resume",tid,threads.at(tid),rr,re);SetLastError(re);require(rr!=DWORD(-1),"resume");}')
    text = replace_once(text, 'auto code=e.dwDebugEventCode,tid=e.dwThreadId;',
                        'auto code=e.dwDebugEventCode,tid=e.dwThreadId;trace("\\\"kind\\\":\\\"debug_event\\\",\\\"code\\\":"+std::to_string(code)+",\\\"tid\\\":"+std::to_string(tid)+",\\\"pending\\\":"+quote(pending?pending->name:"") +",\\\"stepping\\\":"+std::to_string(stepping));')
    text = replace_once(text, 'disposition=DBG_EXCEPTION_NOT_HANDLED;\n                    if(!ready', r'''disposition=DBG_EXCEPTION_NOT_HANDLED;
                    auto observed=context(tid);
                    auto owned=std::find_if(sites.begin(),sites.end(),[&](auto& s){return s.address==address;});
                    trace("\"kind\":\"exception\",\"code\":"+std::to_string(ex.ExceptionRecord.ExceptionCode)+",\"address\":"+quote(hex(address))+",\"rip\":"+quote(hex(observed.Rip))+",\"flags\":"+std::to_string(observed.EFlags)+",\"dr6\":"+quote(hex(observed.Dr6))+",\"dr7\":"+quote(hex(observed.Dr7))+",\"first\":"+std::to_string(ex.dwFirstChance)+",\"tid\":"+std::to_string(tid)+",\"pending\":"+quote(pending?pending->name:"") +",\"pending_address\":"+quote(hex(pending?pending->address:0))+",\"stepping\":"+std::to_string(stepping)+",\"matching_site\":"+quote(owned==sites.end()?"":owned->name)+",\"installed\":"+std::to_string(owned!=sites.end()&&owned->installed));
                    if(!ready''')
    text = replace_once(text, '        // Called only while a debug event',
                        '        trace("\\\"kind\\\":\\\"retire_begin\\\",\\\"pending\\\":"+quote(pending?pending->name:"") +",\\\"stepping\\\":"+std::to_string(stepping)+",\\\"suspended\\\":"+std::to_string(suspended.size()));\n        // Called only while a debug event')
    text = replace_once(text, 'require(latency::continued(e.dwProcessId,tid,disposition)!=0,"continue");',
                        'trace("\\\"kind\\\":\\\"continue\\\",\\\"tid\\\":"+std::to_string(tid)+",\\\"disposition\\\":"+std::to_string(disposition));require(latency::continued(e.dwProcessId,tid,disposition)!=0,"continue");')
    text = replace_once(text, 'if(!exited&&(fs::exists(root/L"STOP")||!disk()))stop=true;',
                        'if(fixture&&pending&&GetEnvironmentVariableW(L"SOR_DIAGNOSTIC_STOP_REPLAY",nullptr,0))stop=true;\n                if(!exited&&(fs::exists(root/L"STOP")||!disk()))stop=true;')
    if query_handles:
        # Experimental local repair, never release/package a diagnostic build.
        for assignment in ['threads[tid]=e.u.CreateProcessInfo.hThread;', 'threads[tid]=e.u.CreateThread.hThread;']:
            text = replace_once(text, assignment, assignment + 'auto diagnostic_handle=OpenThread(THREAD_GET_CONTEXT|THREAD_SET_CONTEXT|THREAD_SUSPEND_RESUME|THREAD_QUERY_LIMITED_INFORMATION|SYNCHRONIZE,FALSE,tid);require(diagnostic_handle!=nullptr,"diagnostic_open_thread");threads[tid]=diagnostic_handle;')
    if minimum_handles:
        assert not query_handles
        for assignment in ['threads[tid]=e.u.CreateProcessInfo.hThread;', 'threads[tid]=e.u.CreateThread.hThread;']:
            text = replace_once(text, assignment, assignment + 'HANDLE minimum{};require(DuplicateHandle(GetCurrentProcess(),threads[tid],GetCurrentProcess(),&minimum,THREAD_GET_CONTEXT|THREAD_SET_CONTEXT|THREAD_SUSPEND_RESUME,FALSE,0)!=0,"diagnostic_minimum_handle");threads[tid]=minimum;')
    if defer_queued:
        # Bounded experimental repair: rewind a confirmed other-thread owned
        # queued trap, retain its owned suspension, recapture after rearming.
        # This intentionally does NOT assert that all teardown debts are solved.
        text = replace_once(text, '}else if(pending&&tid==stepping&&ex.dwFirstChance', r'''}else if(pending&&tid!=stepping&&ex.dwFirstChance&&ex.ExceptionRecord.ExceptionCode==EXCEPTION_BREAKPOINT&&owned!=sites.end()&&owned->armed_once){
                        require(observed.Rip==address+1&&!(observed.EFlags&0x100)&&!(observed.Dr7&0xff),"diagnostic_queued_debug_state");
                        require(std::count(suspended.begin(),suspended.end(),tid)==1,"diagnostic_queued_suspend_ownership");
                        observed.Rip=address;control(tid,observed);disposition=DBG_CONTINUE;
                        trace("\"kind\":\"queued_rewound\",\"tid\":"+std::to_string(tid)+",\"address\":"+quote(hex(address)));
                        if(GetEnvironmentVariableW(L"SOR_DIAGNOSTIC_STOP_QUEUED",nullptr,0))stop=true;
                    }else if(pending&&tid==stepping&&ex.dwFirstChance''')
    return text


def build(out, query_handles, defer_queued=False, minimum_handles=False):
    source = diagnostic_source(query_handles, defer_queued, minimum_handles)
    # Absolute project include retains original dependency resolution; no copying
    # SDK/OS code or binary inputs into authored implementation.
    source = source.replace('#include "capture_epoch.h"', '#include "' + (SOURCE / 'capture_epoch.h').as_posix() + '"')
    (out / 'diagnostic.cpp').write_text(source, encoding='utf-8', newline='\n')
    shutil.copyfile(OLD / 'retail.generated.h', out / 'retail.generated.h')
    vcvars = Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')
    cmd = out / 'build.cmd'
    cmd.write_text(f'@echo off\ncall "{vcvars}"\nif errorlevel 1 exit /b 1\ncl /Bv /nologo /std:c++20 /EHsc /W4 /O2 /MD /DUNICODE /D_UNICODE /I"{out}" "{out / "diagnostic.cpp"}" /Fe:diagnostic.exe /Fo:diagnostic.obj /link /INCREMENTAL:NO bcrypt.lib\n', encoding='utf-8', newline='\r\n')
    process = subprocess.run(['cmd.exe', '/d', '/c', str(cmd)], cwd=out, capture_output=True)
    (out / 'build.log').write_bytes(process.stdout + process.stderr)
    if process.returncode:
        raise RuntimeError('diagnostic build failed: ' + str(out / 'build.log'))
    save(out / 'build.json', {'diagnostic_only': True, 'query_handles': query_handles, 'defer_queued': defer_queued, 'minimum_handles': minimum_handles, 'baseline_source': PIN, 'generated_source': sha(out / 'diagnostic.cpp'), 'executable': sha(out / 'diagnostic.exe'), 'vcvars': sha(vcvars)})


def build_fixture(out):
    text = (SOURCE / 'fixture.cpp').read_text()
    text = replace_once(text, 'if(r->mode==3)throw', 'if(r->mode==6)DebugBreak();\n    if(r->mode==3)throw')
    text = replace_once(text, 'LONG WINAPI handler(EXCEPTION_POINTERS* e){return',
                        'LONG WINAPI handler(EXCEPTION_POINTERS* e){if(e->ExceptionRecord->ExceptionCode==EXCEPTION_BREAKPOINT){++exceptions;if(*(unsigned char*)e->ExceptionRecord->ExceptionAddress==0xcc&&e->ContextRecord->Rip==(DWORD64)e->ExceptionRecord->ExceptionAddress)++e->ContextRecord->Rip;return EXCEPTION_CONTINUE_EXECUTION;}return')
    text = replace_once(text, '    if(mode=="retire-active"){', r'''    if(mode=="target-exit"){ExitProcess(27);
    }else if(mode=="foreign-break"){one(6,0);
    }else if(mode=="queue-burst"||mode=="exit-burst"||mode=="stop-queued"){
        std::atomic<unsigned> arrived{};std::atomic<bool> launch{};
        std::vector<std::thread> workers;
        for(unsigned i=0;i<32;++i)workers.emplace_back([&,i]{
            SetThreadAffinityMask(GetCurrentThread(),DWORD_PTR(1)<<(i%8));
            ++arrived;while(!launch.load())YieldProcessor();
            if(mode!="exit-burst"||i>=24)one(2,0);
        });
        while(arrived.load()!=32)Sleep(1);launch=true;
        for(auto& t:workers)t.join();
    }else if(mode=="retire-active"){''')
    text = text.replace('#include <array>', '#include <array>\n#include <vector>')
    path = out / 'fixture-diagnostic.cpp'
    path.write_text(text, encoding='utf-8', newline='\n')
    vcvars = 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat'
    cmd = out / 'fixture-build.cmd'
    cmd.write_text(f'@echo off\ncall "{vcvars}"\nif errorlevel 1 exit /b 1\ncl /nologo /std:c++20 /EHs /W4 /O2 /MD "{path}" "{OLD / "fixture-asm.obj"}" /Fe:event_fixture.exe /Fo:fixture.obj /link /INCREMENTAL:NO\n', encoding='utf-8', newline='\r\n')
    result = subprocess.run(['cmd.exe', '/d', '/c', str(cmd)], cwd=out, capture_output=True)
    (out / 'fixture-build.log').write_bytes(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('fixture build failed')
    return out / 'event_fixture.exe'


def wait(path, fixture, seconds=300):
    end = time.monotonic() + seconds
    while not path.exists():
        if fixture.poll() is not None:
            raise RuntimeError('fixture exited before ' + path.name)
        if time.monotonic() > end:
            raise TimeoutError(str(path))
        time.sleep(.02)


def run_case(out, mode, adapter, fixture_exe, number):
    guard()
    run = out / (str(number).zfill(2) + '-' + mode)
    run.mkdir()
    result = {'mode': mode, 'adapter_sha256': sha(adapter), 'fixture_sha256': sha(fixture_exe), 'start_ns': time.time_ns(), 'failures': []}
    with (run / 'fixture.log').open('wb') as fl, (run / 'adapter.log').open('wb') as al:
        fixture = subprocess.Popen([str(fixture_exe), str(run), mode], stdout=fl, stderr=fl)
        debugger = None
        try:
            wait(run / 'fixture.plan', fixture)
            plan = run / 'fixture.plan'
            if mode == 'center-only':
                plan = run / 'center.plan'
                plan.write_text('\n'.join(l for l in (run / 'fixture.plan').read_text().splitlines() if l.startswith('center_')) + '\n')
            if mode == 'grid-guard-failure':
                plan = run / 'bad-grid.plan'
                plan.write_text('\n'.join(l.rsplit(' ', 1)[0] + ' 90909090' if l.startswith('grid_result ') else l for l in (run / 'fixture.plan').read_text().splitlines()) + '\n')
            env = os.environ.copy()
            if mode == 'writer-failure':
                env['SOR_DISPOSABLE_WRITER_FAILURE'] = '1'
            if mode == 'stop-replay':
                env['SOR_DIAGNOSTIC_STOP_REPLAY'] = '1'
            if mode == 'stop-queued':
                env['SOR_DIAGNOSTIC_STOP_QUEUED'] = '1'
            command = [str(adapter), '--fixture', str(fixture.pid), str(run), sha(fixture_exe), str(plan)]
            result.update(command=command, fixture_pid=fixture.pid)
            debugger = subprocess.Popen(command, stdout=al, stderr=al, env=env)
            result['adapter_pid'] = debugger.pid
            wait(run / 'READY', fixture, 30)
            (run / 'GO').touch()
            if mode == 'target-exit':
                fixture.wait(timeout=30)
            else:
                wait(run / ('ACTIVE' if mode == 'retire-active' else 'counts.json'), fixture)
        except Exception:
            result['failures'].append(traceback.format_exc())
        finally:
            (run / 'STOP').touch()
            (run / 'GO').touch()
            if debugger:
                try:
                    debugger.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    result['failures'].append('adapter stalled; cooperative STOP failed')
            # Run these checks regardless of adapter exit status. They precede
            # workload release and do not depend on the adapter's restored claim.
            try:
                if fixture.poll() is not None:
                    rows, receipt = decode(run / 'evidence/epochs.wal')
                    result['wal'] = receipt
                    result['terminal'] = [row for row in rows if row.get('kind') in ('target_exit', 'terminal')]
                    result['restoration_detach_verified'] = None
                    result['postflight_limit'] = 'target exited: live byte/debugger queries unavailable; original Popen exit code and durable target_exit/terminal retained'
                    raise StopIteration
                reader = ProcessRead(fixture.pid)
                try:
                    result['postflight_path'] = reader.path()
                    result['postflight_debugged'] = reader.debugged()
                    wal = run / 'evidence/epochs.wal'
                    rows, receipt = decode(wal)
                    result['wal'] = receipt
                    base = int(next(row['base'] for row in rows if row.get('kind') == 'ready'), 16)
                    windows = []
                    for line in (run / 'fixture.plan').read_text().splitlines():
                        name, rva, data = line.split()
                        actual = reader.read(base + int(rva, 16), len(bytes.fromhex(data))).hex()
                        windows.append({'site': name, 'expected': data, 'actual': actual, 'equal': actual == data})
                    result['postflight_windows'] = windows
                    result['restoration_detach_verified'] = not result['postflight_debugged'] and all(w['equal'] for w in windows)
                    result['boundary_counts'] = {site: sum(row.get('kind') == 'boundary' and row.get('site') == site for row in rows) for site in ('center_entry', 'center_exit')}
                    result['terminal'] = [row for row in rows if row.get('kind') in ('terminal', 'retired', 'exception')]
                finally:
                    reader.close()
            except StopIteration:
                pass
            except Exception:
                result['restoration_detach_verified'] = False
                result['failures'].append(traceback.format_exc())
            (run / 'CONTINUE').touch()
            (run / 'RELEASE').touch()
            try:
                fixture.wait(timeout=15)
            except subprocess.TimeoutExpired:
                # Only this Popen-created disposable may be terminated; never a
                # PID lookup. Retain failure, not a successful target-survival.
                result['failures'].append('owned disposable required termination')
                fixture.terminate()
                fixture.wait(timeout=10)
            result.update(adapter_exit=debugger.poll() if debugger else None, fixture_exit=fixture.poll(), end_ns=time.time_ns())
            if (run / 'counts.json').exists():
                result['counts'] = json.loads((run / 'counts.json').read_text())
            result['elapsed_ms'] = (result['end_ns'] - result['start_ns']) / 1e6
            counts = result.get('counts', {})
            expected_exceptions = {'full': 2, 'center-only': 2, 'grid-guard-failure': 2, 'zero': 0, 'retire-active': 0, 'writer-failure': 2, 'exit-burst': 0, 'queue-burst': 0, 'stop-queued': 0, 'foreign-break': 1, 'stop-replay': 2}
            expected = (result['adapter_exit'] == (1 if mode == 'writer-failure' else 0))
            if mode == 'target-exit':
                expected &= result['fixture_exit'] == 27 and any(row.get('kind') == 'target_exit' and row.get('exit_code') == 27 for row in result.get('terminal', []))
            else:
                expected &= result['fixture_exit'] == 0 and result['restoration_detach_verified'] is True and counts.get('bad') == 0 and counts.get('exceptions') == expected_exceptions[mode]
                if mode in ('full', 'center-only', 'grid-guard-failure', 'exit-burst', 'queue-burst', 'foreign-break'):
                    expected &= result.get('boundary_counts', {}) == {'center_entry': counts.get('entered'), 'center_exit': counts.get('completed')}
            result['diagnostic_expectations_met'] = bool(expected and not result['failures'])
            result['candidate_qualification'] = False
            save(run / 'result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    parser.add_argument('--query-handles', action='store_true')
    parser.add_argument('--minimum-handles', action='store_true')
    parser.add_argument('--defer-queued', action='store_true')
    parser.add_argument('--adversarial', action='store_true')
    parser.add_argument('--modes', nargs='+', default=['full', 'center-only', 'grid-guard-failure', 'zero', 'retire-active', 'writer-failure'])
    args = parser.parse_args()
    assert args.run.replace('-', '').isalnum()
    free = guard()
    out = ROOT / '.local-work/thread-control' / args.run
    out.mkdir(exist_ok=False)
    shutil.copyfile(__file__, out / 'harness.py')
    build(out, args.query_handles, args.defer_queued, args.minimum_handles)
    fixture = build_fixture(out) if args.adversarial else OLD / 'event_fixture.exe'
    matrix = []
    for number, mode in enumerate(args.modes):
        result = run_case(out, mode, out / 'diagnostic.exe', fixture, number)
        matrix.append(result)
        save(out / 'matrix.json', {'diagnostic_only': True, 'query_handles': args.query_handles, 'free_initial': free, 'free_final': guard(), 'cases': matrix})
        print(mode, result.get('adapter_exit'), result.get('fixture_exit'), result.get('restoration_detach_verified'), result.get('boundary_counts'), flush=True)


if __name__ == '__main__':
    main()
