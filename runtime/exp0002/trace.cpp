// SPDX-License-Identifier: GPL-3.0-or-later
// Future separately approved diagnostic ONLY. Never run against a game in Gate A.
#include "win_support.h"
#include "trace_state.h"
#include "observation_policy.h"
#include "site_guards.generated.h"
#include <TlHelp32.h>
#include <iostream>
using namespace sor;
struct Handle {HANDLE h{};~Handle(){if(h&&h!=INVALID_HANDLE_VALUE)CloseHandle(h);}operator HANDLE()const{return h;}};
int wmain(int argc,wchar_t** argv) {
    // Refuse before process access unless the future operator explicitly opts in.
    if(argc!=8 || std::wstring(argv[1])!=L"--gate-b-approved") {
        std::cerr<<"Requires reviewed Gate B diagnostic approval; use trace.py after A2R.\n";return 2;
    }
    DWORD pid{},tid{};std::uint64_t selected{},wanted_id{};fs::path session;
    try {pid=std::stoul(argv[2]);tid=std::stoul(argv[3]);selected=std::stoull(argv[4],nullptr,0);wanted_id=std::stoull(argv[5],nullptr,0);session=argv[6];}
    catch(const std::exception&){return 2;}
    if(std::wstring(argv[7])!=L"one-operation" || !allowed_root(session.parent_path()) || session.lexically_normal()!=session)return 2;
    auto session_attrs=GetFileAttributesW(session.c_str());
    if(session_attrs==INVALID_FILE_ATTRIBUTES||(session_attrs&FILE_ATTRIBUTE_REPARSE_POINT)||!(session_attrs&FILE_ATTRIBUTE_DIRECTORY))return 2;
    if(auto reason=disk_issue(disk_space())) {
        write_new(session/L"trace-disk-failure.json","{\"terminal\":\"INCOMPLETE\",\"reason\":"+quote(reason)+"}\n");return 3;
    }
    Handle process{OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION|PROCESS_VM_READ,FALSE,pid)};
    if(!process.h)return 3;wchar_t path[32768]{};DWORD length=32768;
    if(!QueryFullProcessImageNameW(process,0,path,&length)||sha_file(path)!="7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28")return 3;
    ProcessReader r;r.process=process;Identity initial{};
    if(!identity(r,selected,initial)||initial.base_id!=storage_base||initial.id!=wanted_id)return 3;
    std::uint64_t base{},image_size{},ntdll{},observer_base{},observer_end{};
    Handle modules{CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,pid)};
    MODULEENTRY32W m{};m.dwSize=sizeof m;
    if(modules.h==INVALID_HANDLE_VALUE||!Module32FirstW(modules,&m))return 3;
    do {
        if(!_wcsicmp(m.szModule,L"Starfield.exe")){base=reinterpret_cast<std::uint64_t>(m.modBaseAddr);image_size=m.modBaseSize;}
        if(!_wcsicmp(m.szModule,L"ntdll.dll"))ntdll=reinterpret_cast<std::uint64_t>(m.modBaseAddr);
        if(!_wcsicmp(m.szModule,L"SorExp0002.dll")){observer_base=reinterpret_cast<std::uint64_t>(m.modBaseAddr);observer_end=observer_base+m.modBaseSize;}
    }while(Module32NextW(modules,&m));
    if(!base||!ntdll||!observer_base)return 3;
    for(auto guard:site_guards){std::array<unsigned char,32> b{};if(guard.rva+32>image_size||!r.bytes(base+guard.rva,b.data(),b.size())||sha_bytes(b.data(),b.size())!=guard.sha256)return 3;}
    auto local_ntdll=GetModuleHandleW(L"ntdll.dll");
    auto attach_break=ntdll+reinterpret_cast<std::uint64_t>(GetProcAddress(local_ntdll,"DbgBreakPoint"))-reinterpret_cast<std::uint64_t>(local_ntdll);
    Handle thread{OpenThread(THREAD_GET_CONTEXT|THREAD_SET_CONTEXT|THREAD_SUSPEND_RESUME|THREAD_QUERY_INFORMATION,FALSE,tid)};
    if(!thread.h||GetProcessIdOfThread(thread)!=pid)return 3;
    auto output=session/L"trace.jsonl";
    Handle file{CreateFileW(output.c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr)};
    if(file.h==INVALID_HANDLE_VALUE)return 3;
    unsigned records{};std::size_t total{};bool output_ok=true;
    auto emit=[&](const std::string& kind,const std::string& fields)->bool {
        std::string line="{\"kind\":\"RUNTIME\",\"checkpoint\":\"TRACE\",\"event\":"+quote(kind)+",\"sequence\":"+std::to_string(records)+",\"utc\":"+quote(utc())+",\"module_base\":"+quote(hex(base))+fields+"}\n";
        if(line.size()>4096||records>=300||total+line.size()>1250000){output_ok=false;return false;}
        DWORD n{};bool ok=WriteFile(file,line.data(),static_cast<DWORD>(line.size()),&n,nullptr)&&n==line.size()&&FlushFileBuffers(file);
        ++records;total+=line.size();output_ok=output_ok&&ok;return ok;
    };
    if(!emit("PRE_ATTACH",",\"selected_storage\":"+quote(hex(selected))+",\"form_id\":"+quote(hex(wanted_id,8))+",\"thread_id\":"+std::to_string(tid)))return 3;
    if(!DebugActiveProcess(pid)){emit("TERMINAL",",\"complete\":false,\"reason\":\"attach_failed\"");return 4;}
    bool attached=true,armed=false,changed=false,exited=false,stop=false;CONTEXT prior{};TraceState state{};
    std::string reason="setup_timeout";auto setup=GetTickCount64();unsigned events{};
    if(!DebugSetProcessKillOnExit(FALSE)) {
        bool detached=DebugActiveProcessStop(pid)!=0;
        emit("TERMINAL",",\"complete\":false,\"reason\":\"kill_policy_failed\",\"detached\":"+std::string(detached?"true":"false"));
        if(!detached) {
            // Exiting this debugger with the default policy could kill Starfield.
            // Acquisition has ended. Keep debugger alive for explicit recovery.
            std::cerr<<"RECOVERY REQUIRED: kill policy and detach failed. Do not close this debugger; no further acquisition.\n";
            for(;;)Sleep(1000);
        }
        return 4;
    }
    while(!stop) {
        if(auto disk_reason=disk_issue(disk_space())){reason=disk_reason;break;}
        auto now=GetTickCount64();
        if((armed&&state.expired(now))||(!armed&&now-setup>=5000)){reason="deadline_or_hit_bound";break;}
        DEBUG_EVENT event{};
        if(!WaitForDebugEventEx(&event,50)) {if(GetLastError()==ERROR_SEM_TIMEOUT)continue;reason="wait_failed";break;}
        DWORD continuation=DBG_CONTINUE;++events;
        if(events>1000){reason="debug_event_bound";stop=true;}
        if(event.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT) {
            if(event.u.CreateProcessInfo.hFile)CloseHandle(event.u.CreateProcessInfo.hFile);
            CloseHandle(event.u.CreateProcessInfo.hProcess);CloseHandle(event.u.CreateProcessInfo.hThread);
        } else if(event.dwDebugEventCode==CREATE_THREAD_DEBUG_EVENT)CloseHandle(event.u.CreateThread.hThread);
        else if(event.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT){if(event.u.LoadDll.hFile)CloseHandle(event.u.LoadDll.hFile);}
        else if(event.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT){exited=true;reason="target_exited";stop=true;}
        else if(event.dwDebugEventCode==EXIT_THREAD_DEBUG_EVENT&&event.dwThreadId==tid){reason="selected_thread_exited";stop=true;}
        else if(event.dwDebugEventCode==EXCEPTION_DEBUG_EVENT) {
            continuation=DBG_EXCEPTION_NOT_HANDLED;
            auto& exception=event.u.Exception.ExceptionRecord;auto address=reinterpret_cast<std::uint64_t>(exception.ExceptionAddress);
            if(!armed&&!stop&&exception.ExceptionCode==EXCEPTION_BREAKPOINT&&address==attach_break) {
                prior.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                if(!GetThreadContext(thread,&prior)||(prior.Dr7&0xff)){reason="debug_registers_unavailable_or_occupied";stop=true;}
                else {
                    auto c=prior;c.Dr0=base+0x2073cf0;c.Dr1=base+0x517d60;c.Dr2=0;c.Dr3=0;c.Dr6=0;c.Dr7=5;
                    if(!SetThreadContext(thread,&c)){reason="arm_failed";stop=true;}
                    else {changed=true;armed=true;state.armed=GetTickCount64();
                        if(!emit("ARMED",",\"thread_id\":"+std::to_string(tid))||!write_new(session/L"trace-armed.json","{\"terminal\":\"ARMED\"}\n")){reason="armed_flush_failed";stop=true;}}
                }
                continuation=DBG_CONTINUE; // Only Windows' identified attach breakpoint.
            } else if(armed&&!stop&&event.dwThreadId==tid&&exception.ExceptionCode==EXCEPTION_SINGLE_STEP) {
                CONTEXT c{};c.ContextFlags=CONTEXT_CONTROL|CONTEXT_INTEGER|CONTEXT_DEBUG_REGISTERS;
                if(!GetThreadContext(thread,&c)){reason="context_read_failed";stop=true;}
                else if((c.Dr6&7) && !(c.Dr6&0xe008) && (c.Rip==base+0x2073cf0||c.Rip==base+0x517d60||c.Rip==state.return_site)) {
                    continuation=DBG_CONTINUE;bool correlated=true;std::uint64_t operand{},key{},ret{};
                    std::string kind="UNSELECTED";
                    if(c.Rip==base+0x2073cf0) {
                        ++state.hits;
                        if(c.R8==selected) {
                            --state.hits;Identity fresh{};
                            correlated=identity(r,selected,fresh)&&fresh.id==initial.id&&fresh.base_id==initial.base_id&&r.get(c.Rsp,ret)
                                &&ret>=observer_base&&ret<observer_end&&state.entry(c.Rsp,ret)&&r.get(selected+0xc8,operand)&&r.get(base+0x5f0b3d8,key);
                            kind="CALLBACK";if(correlated){c.Dr2=ret;c.Dr7|=16;}
                        }
                    } else if(c.Rip==base+0x517d60) {if(state.phase){kind="TAIL";correlated=state.tail(c.Rsp);}}
                    else {kind="RETURN";correlated=state.returned(c.Rsp);}
                    auto fields=",\"thread_id\":"+std::to_string(tid)+",\"elapsed_ms\":"+std::to_string(GetTickCount64()-state.armed)+
                        ",\"rip\":"+quote(hex(c.Rip))+",\"rcx\":"+quote(hex(c.Rcx))+",\"rdx\":"+quote(hex(c.Rdx))+",\"r8\":"+quote(hex(c.R8))+",\"r9\":"+quote(hex(c.R9))+",\"rsp\":"+quote(hex(c.Rsp))+
                        ",\"return_site\":"+quote(hex(state.return_site))+",\"return_rax\":"+(kind=="RETURN"?quote(hex(c.Rax)):"null")+
                        ",\"selected_r8_plus_c8\":"+(kind=="CALLBACK"?quote(hex(operand)):"null")+",\"key_global\":"+(kind=="CALLBACK"?quote(hex(key)):"null")+",\"correlated\":"+(correlated?"true":"false");
                    if(!correlated){reason="correlation_or_read_failed";stop=true;}
                    if(kind!="UNSELECTED"&&!emit(kind,fields)){reason="record_flush_failed";stop=true;}
                    if(state.phase==3){reason="one_operation_complete";stop=true;}
                    c.EFlags|=0x10000;c.Dr6&=~7ULL; // RF is debugger resume control, no gameplay registers changed.
                    if(!SetThreadContext(thread,&c)){reason="resume_context_failed";stop=true;}
                } else {reason="unexpected_single_step";stop=true;}
            } else {reason="unexpected_exception";stop=true;}
        }
        // Prefer restoration while Windows already has the process paused,
        // avoiding another breakpoint between completion and cleanup suspend.
        if(stop&&changed&&!exited&&SetThreadContext(thread,&prior))changed=false;
        if(!ContinueDebugEvent(event.dwProcessId,event.dwThreadId,continuation)){reason="continue_failed";stop=true;}
    }
    bool within_bound=armed&&GetTickCount64()-state.armed<=5000;
    bool restored=!changed||exited;
    if(changed&&!exited) {
        if(SuspendThread(thread)!=DWORD(-1)) {
            restored=SetThreadContext(thread,&prior)!=0;
            if(ResumeThread(thread)==DWORD(-1))restored=false;
        }
    }
    bool detached=exited||DebugActiveProcessStop(pid)!=0;attached=!detached;
    bool complete=state.phase==3&&within_bound&&output_ok&&restored&&detached;
    emit("TERMINAL",",\"complete\":"+std::string(complete?"true":"false")+",\"reason\":"+quote(reason)+",\"context_restored_or_process_exited\":"+(restored?"true":"false")+
        ",\"detached_or_process_exited\":"+(detached?"true":"false")+",\"target_outcome\":"+quote(exited?"EXITED":"RUNNING_OR_UNASSESSED")+",\"scientific_result\":\"UNASSESSED\"");
    if(attached)std::cerr<<"Detach failed; no automatic kill/retry. Operator recovery required.\n";
    return complete&&output_ok?0:5;
}
