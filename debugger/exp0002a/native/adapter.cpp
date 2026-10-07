// SPDX-License-Identifier: GPL-3.0-or-later
// Maintainer-core adaptation; see ../maintainer/PROVENANCE.md.
// Never launches a target. S1/S2 controls authorized by SOR-D-0019; no all-thread mode.
#include "rf_core.h"
#include <algorithm>
#include <cwctype>
#include <array>
static ULONG64 image_base=0, breakin=0;
static bool attach_break_seen=false, game=false;
static fs::path prefix;
static std::string expected_window;
static bool capture_durable=false, safety_low_disk=false, identity_verified=false, terminated=false;
static fs::path verified_path;
static std::string verified_hash;
static ULONG64 verified_creation=0;

static std::string digest(const std::vector<unsigned char>& data) {
    BCRYPT_ALG_HANDLE alg=nullptr; BCRYPT_HASH_HANDLE hash=nullptr;
    if (BCryptOpenAlgorithmProvider(&alg,BCRYPT_SHA256_ALGORITHM,nullptr,0)<0)
        throw std::runtime_error("SHA provider");
    std::array<unsigned char,32> result{};
    auto status=BCryptCreateHash(alg,&hash,nullptr,0,nullptr,0,0);
    if (status>=0) status=BCryptHashData(hash,const_cast<PUCHAR>(data.data()),ULONG(data.size()),0);
    if (status>=0) status=BCryptFinishHash(hash,result.data(),ULONG(result.size()),0);
    if(hash) BCryptDestroyHash(hash);
    BCryptCloseAlgorithmProvider(alg,0);
    if(status<0) throw std::runtime_error("SHA operation");
    std::ostringstream out;
    for(auto b:result) out<<std::hex<<std::setw(2)<<std::setfill('0')<<unsigned(b);
    return out.str();
}
static std::string file_hash(const fs::path& path) {
    std::ifstream in(path,std::ios::binary);
    if(!in) throw std::runtime_error("image file unreadable");
    auto size=fs::file_size(path);
    if(size>200000000) throw std::runtime_error("image size bound");
    std::vector<unsigned char> data{std::istreambuf_iterator<char>(in),{}};
    if(data.size()!=size) throw std::runtime_error("image read incomplete");
    return digest(data);
}
static std::string memory_hash(ULONG64 address) {
    std::vector<unsigned char> data(32); SIZE_T used=0;
    require(ReadProcessMemory(process,(void*)address,data.data(),data.size(),&used)&&used==data.size(),"code read");
    return digest(data);
}
static std::wstring lower(std::wstring value) {
    std::transform(value.begin(),value.end(),value.begin(),[](wchar_t c){return wchar_t(towlower(c));});
    return value;
}
static bool forbidden(const std::wstring& name) {
    auto n=lower(name);
    return n.rfind(L"sfse",0)==0 || n.rfind(L"sorexp0002",0)==0;
}
static void module_check() {
    HANDLE list=INVALID_HANDLE_VALUE;
    for(unsigned retry=0;retry<3;++retry) {
        list=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE|TH32CS_SNAPMODULE32,pid);
        if(list!=INVALID_HANDLE_VALUE || GetLastError()!=ERROR_BAD_LENGTH) break;
    }
    require(list!=INVALID_HANDLE_VALUE,"module snapshot");
    MODULEENTRY32W m{}; m.dwSize=sizeof(m);
    if(!Module32FirstW(list,&m)) {CloseHandle(list);throw std::runtime_error("module inventory empty");}
    unsigned count=0; bool rejected=false, ntdll=false;
    do {
        ++count;
        if(count==1) image_base=(ULONG64)m.modBaseAddr;
        rejected |= forbidden(m.szModule);
        if(lower(m.szModule)==L"ntdll.dll") {
            wchar_t local_path[32768]; auto local=GetModuleHandleW(L"ntdll.dll");
            if(!GetModuleFileNameW(local,local_path,32768) || lower(local_path)!=lower(m.szExePath)) {
                CloseHandle(list);throw std::runtime_error("ntdll identity mismatch");
            }
            breakin=(ULONG64)m.modBaseAddr+(ULONG64)GetProcAddress(local,"DbgBreakPoint")-(ULONG64)local;
            unsigned char byte=0; SIZE_T used=0;
            if(!ReadProcessMemory(process,(void*)breakin,&byte,1,&used)||used!=1||byte!=0xcc) {
                CloseHandle(list);throw std::runtime_error("attach break-in byte mismatch");
            }
            ntdll=true;
        }
        if(count>1024) {CloseHandle(list);throw std::runtime_error("module inventory bound");}
    } while(Module32NextW(list,&m));
    DWORD end=GetLastError();CloseHandle(list);
    require(end==ERROR_NO_MORE_FILES,"complete module inventory");
    log("module_preflight",",\"count\":"+std::to_string(count)+",\"sfse_and_sorexp0002_absent\":"+(rejected?"false":"true"));
    if(rejected||!ntdll) throw std::runtime_error("forbidden module or missing ntdll");
}
static bool owned_breakin() {
    return !attach_break_seen && event.dwDebugEventCode==EXCEPTION_DEBUG_EVENT &&
        event.u.Exception.dwFirstChance && event.u.Exception.ExceptionRecord.ExceptionCode==EXCEPTION_BREAKPOINT &&
        (ULONG64)event.u.Exception.ExceptionRecord.ExceptionAddress==breakin;
}
static bool owned_hit() {
    if(event.dwDebugEventCode!=EXCEPTION_DEBUG_EVENT || !threads.count(event.dwThreadId)) return false;
    auto c=context(event.dwThreadId);
    return event.u.Exception.dwFirstChance && event.u.Exception.ExceptionRecord.ExceptionCode==EXCEPTION_SINGLE_STEP &&
        (ULONG64)event.u.Exception.ExceptionRecord.ExceptionAddress==site && c.Rip==site &&
        (c.Dr6&0xf)==1 && !(c.EFlags&0x100) && threads.at(event.dwThreadId).armed;
}
static bool complete_threads() {
    HANDLE list=CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);
    require(list!=INVALID_HANDLE_VALUE,"thread snapshot");
    THREADENTRY32 t{};t.dwSize=sizeof(t);bool complete=true;unsigned count=0;
    if(!Thread32First(list,&t)) {CloseHandle(list);throw std::runtime_error("thread inventory");}
    do {if(t.th32OwnerProcessID==pid) {
        ++count;complete &= threads.count(t.th32ThreadID) != 0;
    }} while(Thread32Next(list,&t));
    DWORD end=GetLastError();CloseHandle(list);
    require(end==ERROR_NO_MORE_FILES,"complete thread enumeration");
    return complete && count>0;
}
static std::string optional_read(ULONG64 address,SIZE_T count) {
    std::vector<unsigned char> data(count);SIZE_T used=0;
    BOOL ok=address && ReadProcessMemory(process,(void*)address,data.data(),count,&used);
    DWORD error=ok?0:GetLastError();
    std::ostringstream out;
    for(SIZE_T i=0;i<used;++i) out<<std::hex<<std::setw(2)<<std::setfill('0')<<unsigned(data[i]);
    return "{\"address\":"+hex(address)+",\"requested\":"+std::to_string(count)+",\"read\":"+std::to_string(used)+
        ",\"valid\":"+(ok&&used==count?"true":"false")+",\"winerror\":"+std::to_string(error)+",\"hex\":"+quote(out.str())+"}";
}
static void capture_one(bool confirmed) {
    auto c=context(event.dwThreadId);ULONG64 ret=0;SIZE_T used=0;
    bool valid=ReadProcessMemory(process,(void*)c.Rsp,&ret,sizeof(ret),&used)&&used==sizeof(ret);
    log("first_hit",",\"provisional\":"+std::string(confirmed?"false":"true"));
    log("capture",",\"label\":\"REQUEST_ENTRY\",\"hit\":1,\"tid\":"+std::to_string(event.dwThreadId)+
        ",\"base\":"+hex(image_base)+",\"rip\":"+hex(c.Rip)+",\"rva\":"+hex(c.Rip-image_base)+
        ",\"rsp\":"+hex(c.Rsp)+",\"rcx\":"+hex(c.Rcx)+",\"rdx\":"+hex(c.Rdx)+",\"r8\":"+hex(c.R8)+",\"r9\":"+hex(c.R9)+
        ",\"rax\":"+hex(c.Rax)+",\"eflags\":"+hex(c.EFlags)+",\"dr6\":"+hex(c.Dr6)+
        ",\"return_valid\":"+(valid?"true":"false")+",\"return_address\":"+hex(ret)+
        ",\"expected_game_return\":"+hex(image_base+0x166c1c3)+",\"game_return_matches\":"+(game&&valid&&ret==image_base+0x166c1c3?"true":"false")+
        ",\"stack\":"+optional_read(c.Rsp,96)+",\"manager_50\":"+optional_read(c.Rcx+0x50,4)+
        ",\"manager_8c\":"+optional_read(c.Rcx+0x8c,1)+",\"name\":"+(c.Rdx?optional_read(c.Rdx,260):"{\"null\":true}")+
        ",\"unwind\":\"not_requested_raw_return_primary\"");
    log("capture_durable",",\"required_record_flushed\":true,\"method\":\"WriteFile_then_FlushFileBuffers\"");
    capture_durable=true; // Irreversible evidence fact; cleanup never resets this.
    // Evidence is FlushFileBuffers-complete before target mutation/retirement.
    c.ContextFlags=CONTEXT_CONTROL|CONTEXT_DEBUG_REGISTERS;
    c.EFlags|=0x10000;c.Dr6&=~1ULL;
    require(SetThreadContext(threads.at(event.dwThreadId).handle,&c),"owned event RF");
    log("resume_rf",",\"tid\":"+std::to_string(event.dwThreadId));
}
static void check_space() {
    for(auto volume:{L"C:\\",L"D:\\"}) {
        ULARGE_INTEGER free{};
        require(GetDiskFreeSpaceExW(volume,&free,nullptr,nullptr),"free disk space");
        if(free.QuadPart<40000000000ULL) {safety_low_disk=true;throw std::runtime_error("disk space guard");}
    }
}
static void safe_log(const char* kind,const std::string& fields="") noexcept {
    try {log(kind,fields);} catch(...) {}
}
static ULONG64 process_creation(HANDLE handle) {
    FILETIME creation{},exit{},kernel{},user{};
    require(GetProcessTimes(handle,&creation,&exit,&kernel,&user),"process creation time");
    return (ULONG64(creation.dwHighDateTime)<<32)|creation.dwLowDateTime;
}
static bool termination_allowed(bool durable,bool safety,bool identity) {
    return identity && (durable || safety);
}
static bool terminate_verified(const char* reason) {
    if(!termination_allowed(capture_durable,safety_low_disk,identity_verified)) {
        safe_log("termination_denied",",\"reason\":\"no_durable_capture_or_machine_safety\"");
        return false;
    }
    // Never reopen by PID: this retained handle cannot select a reused PID.
    wchar_t path[32768];DWORD length=32768;
    require(GetProcessId(process)==pid && process_creation(process)==verified_creation,"termination process identity");
    require(QueryFullProcessImageNameW(process,0,path,&length),"termination image path");
    require(lower(fs::path(path).lexically_normal().wstring())==lower(verified_path.lexically_normal().wstring()),"termination path matches");
    require(file_hash(path)==verified_hash,"termination image hash matches");
    safe_log("termination_authorized",",\"pid\":"+std::to_string(pid)+",\"created_filetime\":"+std::to_string(verified_creation)+
        ",\"evidence_complete\":"+(capture_durable?"true":"false")+",\"machine_safety\":"+(safety_low_disk?"true":"false")+
        ",\"reason\":"+quote(reason));
    require(TerminateProcess(process,0xe0000111),"TerminateProcess exact experimental handle");
    terminated=true;
    // Exit completion is asynchronous; attached exit events must be continued.
    const ULONG64 deadline=GetTickCount64()+10000;
    unsigned events=0;
    if(attached && held) continue_event(event.dwDebugEventCode==EXCEPTION_DEBUG_EVENT?DBG_EXCEPTION_NOT_HANDLED:DBG_CONTINUE);
    while(GetTickCount64()<deadline && (attached || WaitForSingleObject(process,0)!=WAIT_OBJECT_0)) {
        if(!attached) {Sleep(10);continue;}
        if(!wait_event(50)) continue;
        if(++events>1024) throw std::runtime_error("termination event bound");
        bool exited=event.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT;
        if(event.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT && event.u.LoadDll.hFile) CloseHandle(event.u.LoadDll.hFile);
        if(event.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT && event.u.CreateProcessInfo.hFile) CloseHandle(event.u.CreateProcessInfo.hFile);
        continue_event(event.dwDebugEventCode==EXCEPTION_DEBUG_EVENT?DBG_EXCEPTION_NOT_HANDLED:DBG_CONTINUE);
        if(exited) attached=false;
    }
    require(!attached && WaitForSingleObject(process,0)==WAIT_OBJECT_0,"termination completed");
    safe_log("termination_completed",",\"pid\":"+std::to_string(pid));
    return true;
}
static void recovery_hold() {
    safe_log("recovery_required",",\"evidence_complete\":"+std::string(capture_durable?"true":"false"));
    try {touch(prefix.wstring()+L".recovery-required");} catch(...) {}
    while(process && WaitForSingleObject(process,1000)==WAIT_TIMEOUT) {}
}
static bool freeze_population(ULONG64& armed_at) {
    if(!complete_threads()) return false;
    module_check();require(memory_hash(site)==expected_window,"armed code hash");check_space();
    if(!control_s1) {
        require(threads.count(selected_tid)!=0,"selected existing TID present");
        auto& t=threads.at(selected_tid);
        require(SuspendThread(t.handle)!=DWORD(-1),"selected thread suspend");t.suspended=true;
        auto c=context(selected_tid);
        require(!(c.Dr7&~0x400ULL) && !(c.Dr6&0xe00fULL) && !(c.EFlags&0x100),"selected clean debug state");
        arm(selected_tid);
    }
    std::string members="[";
    for(auto& [tid,t]:threads) {
        if(members.size()>1) members+=",";
        members+="{\"tid\":"+std::to_string(tid)+",\"created_filetime\":"+std::to_string(t.created)+",\"owns_dr0\":"+(t.armed?"true":"false")+"}";
    }
    population_frozen=true;armed_at=GetTickCount64();
    log("armed",",\"control\":"+quote(control_s1?"S1":"S2")+",\"selected_tid\":"+std::to_string(selected_tid)+",\"members\":"+members+"]");
    resume_owned();touch(prefix.wstring()+L".armed");
    return true;
}
int wmain(int argc,wchar_t** argv) {
    if(argc==2 && std::wstring(argv[1])==L"--self-check") {
        bool names=forbidden(L"SFSE_1_16_244.dll")&&forbidden(L"SorExp0002.dll")&&!forbidden(L"steam_api64.dll");
        bool gate=!termination_allowed(false,false,true) && !termination_allowed(true,false,false) &&
            !termination_allowed(false,true,false) && termination_allowed(true,false,true) && termination_allowed(false,true,true);
        return names&&gate?0:1;
    }
    if(argc<4 || argc>5) return 2;
    std::wstring mode=argv[1];
    game=mode==L"--starfield-s1" || mode==L"--starfield-s2";
    control_s1=mode==L"--starfield-s1" || mode==L"--fixture-s1";
    bool s2=mode==L"--starfield-s2" || mode==L"--fixture-s2";
    if(!control_s1 && !s2) return 2; // Old --starfield/all-population mode is disabled.
    if(argc!=(s2?5:4)) return 2;
    if(s2) {selected_tid=std::stoul(argv[4]);if(!selected_tid) return 2;}
    pid=std::stoul(argv[2]);prefix=fs::absolute(argv[3]);
    for(auto suffix:{L".confirm",L".armed",L".start",L".active"}) if(fs::exists(prefix.wstring()+suffix)) return 2;
    output=CreateFileW((prefix.wstring()+L".native.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
    if(output==INVALID_HANDLE_VALUE) return 3;
    bool confirmed=false,no_hit=false,alive=false,window_active=false;unsigned pending=0;
    std::string cleanup_status="NOT_ATTEMPTED";
    ULONG64 armed_at=0,active_at=0;
    const ULONG64 setup_deadline=GetTickCount64()+300000;
    try {
        log("setup_started",",\"pid\":"+std::to_string(pid)+",\"mode\":"+quote(game?"starfield_late_attach":"disposable_late_attach"));
        check_space();
        process=OpenProcess(PROCESS_QUERY_INFORMATION|PROCESS_VM_READ|SYNCHRONIZE|PROCESS_TERMINATE,FALSE,pid);
        require(process!=nullptr,"OpenProcess");
        wchar_t path[32768];DWORD size=32768;BOOL debugging=FALSE;
        require(QueryFullProcessImageNameW(process,0,path,&size),"process path");
        wchar_t self[32768];require(GetModuleFileNameW(nullptr,self,32768)!=0,"adapter path");
        fs::path expected=game?fs::path(L"C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe"):fs::path(self).parent_path()/L"request_fixture.exe";
        if(lower(fs::path(path).lexically_normal().wstring())!=lower(expected.lexically_normal().wstring())) throw std::runtime_error("target path");
        auto hash=file_hash(path);
        if(hash!=(game?SOR_GAME_SHA:SOR_FIXTURE_SHA)) throw std::runtime_error("target image hash");
        verified_path=path;verified_hash=hash;verified_creation=process_creation(process);identity_verified=true;
        require(CheckRemoteDebuggerPresent(process,&debugging)&&!debugging,"no existing debugger");
        module_check();site=image_base+(game?0x183c590:SOR_FIXTURE_RVA);
        expected_window=game?SOR_GAME_WINDOW:SOR_FIXTURE_WINDOW;
        require(memory_hash(site)==expected_window,"preflight site hash");
        log("identity",",\"pid\":"+std::to_string(pid)+",\"created_filetime\":"+std::to_string(verified_creation)+
            ",\"image_sha256\":"+quote(hash)+",\"base\":"+hex(image_base)+",\"site\":"+hex(site)+",\"site_sha256\":"+quote(expected_window));
        require(DebugActiveProcess(pid),"DebugActiveProcess");attached=true;
        require(DebugSetProcessKillOnExit(FALSE),"DebugSetProcessKillOnExit");
        unsigned quiet=0;
        // Configure at OS-owned create events; UI pause is not a debugger stop.
        // Readiness does not require initial break-in to have arrived.
        while(!population_frozen) {
            if(GetTickCount64()>=setup_deadline) throw std::runtime_error("setup deadline");
            if(!wait_event(100)) {
                quiet=complete_threads()?quiet+1:0;
                if(quiet>=2 && !freeze_population(armed_at)) quiet=0;
                continue;
            }
            quiet=0;
            if(administration(true)) continue;
            if(!owned_breakin()) throw std::runtime_error("unowned setup exception");
            attach_break_seen=true;log("attach_breakin");continue_event(DBG_CONTINUE);
        }
        ULONG64 next_space_check=GetTickCount64()+1000;
        while(true) {
            if(GetTickCount64()>=next_space_check) {check_space();next_space_check=GetTickCount64()+1000;}
            if(!window_active && fs::exists(prefix.wstring()+L".start")) {
                window_active=true;active_at=GetTickCount64();
                log("capture_started",",\"anchor_kind\":\"before_click_now\",\"deadline_tick_ms\":"+std::to_string(active_at+10000));
                touch(prefix.wstring()+L".active");
            }
            if(!confirmed && fs::exists(prefix.wstring()+L".confirm")) {
                confirmed=true;log("operator_confirm_received",",\"clock_effect\":\"none_correlation_only\"");
            }
            if(window_active && GetTickCount64()>=active_at+10000) {
                no_hit=true;
                log("capture_finished",",\"reason\":"+quote(control_s1?"S1_WINDOW_ENDED":"NO_HIT")+",\"new_unarmed_threads\":"+std::to_string(new_unarmed_threads));
                break;
            }
            if(!window_active && GetTickCount64()>=armed_at+120000) {log("capture_finished",",\"reason\":\"NO_ACTION\"");break;}
            if(!wait_event(50)) continue;
            if(administration(false)) continue;
            if(owned_breakin()) {attach_break_seen=true;log("attach_breakin");continue_event(DBG_CONTINUE);continue;}
            if(!owned_hit()) {
                log("application_exception_forwarded");
                continue_event(DBG_EXCEPTION_NOT_HANDLED);continue;
            }
            if(!window_active) throw std::runtime_error("request before active window");
            capture_one(confirmed);log("capture_finished",",\"reason\":\"one_request\"");break;
        }
        cleanup_status="ATTEMPTING_BOUNDED_CLEAN_RETIREMENT";
        log("retirement_started",",\"evidence_complete\":"+std::string(capture_durable?"true":"false"));
        if(control_s1) {
            // S1 installed no research register state and owns no suspensions.
            require(DebugActiveProcessStop(pid),"S1 detach");attached=false;log("detached");
        } else retire(true,pending);
        require(memory_hash(site)==expected_window,"retired code hash");
        require(CheckRemoteDebuggerPresent(process,&debugging)&&!debugging,"detached verification");
        log("cleanup_finished",",\"site_unchanged\":true,\"debugger_absent\":true,\"pending_events\":"+std::to_string(pending));
        cleanup_status="CLEAN_API_CHECKS_EVENT_STATE_NOT_PROVEN";
    } catch(const TargetExited&) {
        cleanup_status="TARGET_EXIT_EVENT_CONTINUED";
    } catch(const std::exception& e) {
        safe_log("failure",",\"message\":"+quote(e.what())+",\"evidence_complete\":"+(capture_durable?"true":"false"));
        cleanup_status="CLEAN_RETIREMENT_NOT_ESTABLISHED";
        if(target_exited) {cleanup_status="TARGET_EXIT_NO_DEAD_TARGET_RECOVERY";}
        else if(termination_allowed(capture_durable,safety_low_disk,identity_verified)) {
            try {
                if(terminate_verified(e.what())) cleanup_status="EXACT_TARGET_TERMINATED";
            } catch(const std::exception& recovery) {
                safe_log("termination_failed",",\"message\":"+quote(recovery.what()));
                recovery_hold();
            }
        } else if(attached) {
            try {
                const ULONG64 recovery_deadline=GetTickCount64()+15000;
                for(auto& [tid,t]:threads) {
                    if(GetTickCount64()>=recovery_deadline) throw std::runtime_error("pre-capture recovery deadline");
                    if(!t.suspended) {require(SuspendThread(t.handle)!=DWORD(-1),"recovery suspend");t.suspended=true;}
                    if(t.armed) disarm(tid);
                }
                if(held) continue_event(event.dwDebugEventCode==EXCEPTION_DEBUG_EVENT?DBG_EXCEPTION_NOT_HANDLED:DBG_CONTINUE);
                require(DebugActiveProcessStop(pid),"recovery detach");attached=false;resume_owned();
                safe_log("recovery_detached_unqualified");
            } catch(...) {
                recovery_hold(); // No pre-capture destructive fallback absent machine safety.
            }
        }
    }
    if(!confirmed && fs::exists(prefix.wstring()+L".confirm")) confirmed=true;
    safe_log("correlation",",\"confirmed\":"+std::string(confirmed?"true":"false")+",\"requires_operator_causality_review\":true");
    if(process) {
        ULONG64 after=GetTickCount64();
        for(unsigned delay:{0,1,5,15}) {
            while(GetTickCount64()<after+delay*1000ULL) Sleep(10);
            DWORD code=0;BOOL known=GetExitCodeProcess(process,&code);
            alive=known && code==STILL_ACTIVE;
            safe_log("health",",\"delay\":"+std::to_string(delay)+",\"status_known\":"+(known?"true":"false")+
                ",\"alive\":"+(alive?"true":"false")+",\"exit_code\":"+std::to_string(code));
        }
        CloseHandle(process);
    }
    for(auto& [tid,t]:threads) CloseHandle(t.handle);
    std::string acquisition=capture_durable?"DURABLE_REQUEST":(target_exited?"INCOMPLETE_PRE_CAPTURE_TARGET_EXIT":(no_hit?(control_s1?"S1_WINDOW_COMPLETE_REQUIRES_OPERATOR_AND_SAVE_VALIDATION":(new_unarmed_threads?"NO_HIT_NEW_THREADS_PRESENT":"NO_HIT")):"INCOMPLETE_OR_NO_ACTION"));
    safe_log("complete",",\"evidence_complete\":"+std::string(capture_durable?"true":"false")+
        ",\"acquisition_status\":"+quote(acquisition)+",\"cleanup_status\":"+quote(cleanup_status)+
        ",\"target_outcome\":"+quote(terminated?"TERMINATED_EXACT_TARGET":(alive?"ALIVE_FUNCTIONAL_HEALTH_SEPARATE":"EXITED_OR_UNAVAILABLE"))+
        ",\"target_exit_code\":"+(target_exited?std::to_string(target_exit_code):"null")+",\"control\":"+quote(control_s1?"S1":"S2")+",\"hits\":"+std::to_string(capture_durable?1:0)+",\"new_unarmed_threads\":"+std::to_string(new_unarmed_threads));
    CloseHandle(output);return capture_durable||no_hit?0:1;
}
