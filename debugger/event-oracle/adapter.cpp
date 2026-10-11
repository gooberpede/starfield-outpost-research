// SPDX-License-Identifier: GPL-3.0-or-later
// Scoped event acquisition. See README.md for reads, writes and intervention.
#include "capture_epoch.h"
#include <map>
#include <iostream>
#include <algorithm>
#include <cstdio>
#include <TlHelp32.h>
#include "retail.generated.h"
using namespace beacon;
struct Site {std::string name; uint64_t address; std::vector<unsigned char> original; bool installed{};std::string expected_hash;bool armed_once{};};
struct Remote:Reader {HANDLE process{}; bool bytes(uint64_t a,void* b,size_t n) override {
    latency::Phase timing(latency::memory);SIZE_T k{};return range(a,n)&&ReadProcessMemory(process,(void*)a,b,n,&k)&&k==n;
}};
struct Scope {uint64_t id,sp,caller,reference,output,parent;};
struct Adapter {
    Remote r; std::map<DWORD,HANDLE> threads; std::vector<Site> sites;
    std::map<DWORD,std::vector<Scope>> centers,grids;
    std::vector<DWORD> suspended; DWORD pid{},stepping{}; Site* pending{};
    uint64_t serial{},invocation{},base{},breakin{}; bool ready{},stop{},attached{},exited{},stop_break{},fixture{},fail_writer{};
    fs::path root; EpochWriter* w{};
    void require(bool ok,const char* why){if(!ok)throw std::runtime_error(std::string(why)+":"+std::to_string(GetLastError()));}
    CONTEXT context(DWORD id){latency::Phase timing(latency::control);CONTEXT c{};c.ContextFlags=CONTEXT_ALL;require(GetThreadContext(threads.at(id),&c)!=0,"context");return c;}
    void control(DWORD id,CONTEXT c){latency::Phase timing(latency::control);c.ContextFlags=CONTEXT_CONTROL;require(SetThreadContext(threads.at(id),&c)!=0,"control");}
    uint64_t pointer(uint64_t a){uint64_t v{};r.get(a,v);return v;}
    void event(const std::string& kind,const std::string& fields=""){
        LARGE_INTEGER q{};require(QueryPerformanceCounter(&q)!=0,"qpc");
        w->event("{\"kind\":"+quote(kind)+",\"version\":\"0.1.4\",\"sequence\":"+std::to_string(++serial)+",\"qpc\":"+std::to_string(q.QuadPart)+",\"utc\":"+quote(utc())+fields+"}");
    }
    void raw(const std::string& name,uint64_t a,size_t n){std::vector<unsigned char>b(n);
        if(r.bytes(a,b.data(),n))w->raw(name,a,b.data(),n,"stopped_debug_event_runtime_VA");
        else event("partial",",\"field\":"+quote(name)+",\"address\":"+quote(hex(a))+",\"bytes\":"+std::to_string(n));
    }
    void identity(uint64_t ref,const std::string& prefix){
        EpochCapture capture(r,*w,base);capture.reference(prefix,ref);
        raw(prefix+".base",pointer(ref+0x98),0x30);
        // Same stopped epoch: owner/frame state independent of output numerics.
        capture.terrain();
    }
    void patch(Site& s,bool install){latency::Phase timing(latency::control);
        unsigned char before{};require(r.bytes(s.address,&before,1),"patch_read");
        require(before==(s.installed?0xcc:s.original[0]),"patch_preimage");
        unsigned char value=install?0xcc:s.original[0];DWORD old{},unused{};SIZE_T n{};
        require(VirtualProtectEx(r.process,(void*)s.address,1,PAGE_EXECUTE_READWRITE,&old)!=0,"protect");
        bool wrote=WriteProcessMemory(r.process,(void*)s.address,&value,1,&n)&&n==1;
        bool protected_again=VirtualProtectEx(r.process,(void*)s.address,1,old,&unused)!=0;
        if(wrote){s.installed=install;if(install)s.armed_once=true;}require(wrote&&protected_again,"patch_write");
        require(FlushInstructionCache(r.process,(void*)s.address,1)!=0,"flush_instruction_cache");
        require(r.bytes(s.address,&before,1)&&before==value,"patch_verify");
    }
    void suspend_others(DWORD id){latency::Phase timing(latency::suspension);for(auto [tid,h]:threads)if(tid!=id){
        if(SuspendThread(h)==DWORD(-1)){
            DWORD status{};require(GetExitCodeThread(h,&status)&&status!=STILL_ACTIVE,"suspend_live_thread");
            // An exit can be pending delivery while another thread's breakpoint
            // is reported. A proven exited thread cannot traverse restored code.
            continue;
        }suspended.push_back(tid);
    }}
    void resume(){latency::Phase timing(latency::suspension);for(auto tid:suspended)if(threads.count(tid))require(ResumeThread(threads.at(tid))!=DWORD(-1),"resume");suspended.clear();}
    void missing(std::vector<Scope>& stack,const char* reason){for(auto s:stack)event("unpaired",",\"invocation\":"+std::to_string(s.id)+",\"reason\":"+quote(reason));stack.clear();}
    void hit(Site& s,DWORD tid,CONTEXT c){
        auto label="event-"+std::to_string(serial+1);uint64_t id{},parent{};std::string pairing="boundary";
        event("capture_begin",",\"label\":"+quote(label)+",\"site\":"+quote(s.name)+",\"thread\":"+std::to_string(tid));
        auto& cs=centers[tid];auto& gs=grids[tid];
        if(s.name=="center_entry"||s.name=="grid_entry"){
            auto& stack=s.name=="center_entry"?cs:gs;
            // Stack grows down. Equal/higher entry SP proves old scope has unwound.
            while(!stack.empty()&&c.Rsp>=stack.back().sp){auto old=stack.back();stack.pop_back();event("unpaired",",\"invocation\":"+std::to_string(old.id)+",\"reason\":\"stack_reuse_or_unwind\"");}
            parent=std::max(cs.empty()?0:cs.back().id,gs.empty()?0:gs.back().id);
            id=++invocation;Scope sc{id,c.Rsp,pointer(c.Rsp),s.name=="center_entry"?c.Rcx:c.Rdx,s.name=="center_entry"?c.Rdx:c.Rcx,parent};stack.push_back(sc);
            identity(sc.reference,label+".reference");raw(label+".output_before",sc.output,s.name=="center_entry"?12:48);
            pairing="entered";
        }else if(s.name=="center_exit"){
            auto token=c.Rsp+0x38;
            auto found=std::find_if(cs.rbegin(),cs.rend(),[&](auto a){return a.sp==token&&a.reference==c.Rbx&&a.output==c.Rdi&&a.caller==pointer(token);});
            if(found!=cs.rend()){
                auto index=size_t(std::distance(cs.begin(),found.base())-1);id=cs[index].id;parent=cs[index].parent;
                for(size_t i=index+1;i<cs.size();++i)event("unpaired",",\"invocation\":"+std::to_string(cs[i].id)+",\"reason\":\"exit_skipped_inner_scope\"");
                cs.resize(index);pairing="paired";
            }else pairing="unmatched_exit";
            raw(label+".native_center",c.Rdi,12);identity(c.Rbx,label+".reference");
        }else if(s.name=="grid_result"||s.name=="grid_x"||s.name=="grid_y"){
            // Retail prologue: entry SP=RBP+0x5f. Never join by XYZ/time.
            auto token=c.Rbp+0x5f;
            if(!gs.empty()&&gs.back().sp==token&&gs.back().reference==c.Rbx&&gs.back().output==c.Rsi){id=gs.back().id;parent=gs.back().parent;pairing="scoped_result";}
            else pairing="unassociated_result";
            if(s.name=="grid_result"){
            identity(c.Rbx,label+".reference");raw(label+".center_local",c.Rbp-0x49,12);raw(label+".hierarchy",c.Rbp-9,44);raw(label+".floor",c.Rbp+0x6f,8);
            raw(label+".context",c.Rsi,48);
            for(auto [offset,name,size]:std::vector<std::tuple<int,const char*,size_t>>{{0,"boolean",1},{8,"candidate",44},{0x18,"source",44},{0x20,"translation",12},{0x28,"bounds",16}})raw(label+"."+name,pointer(c.Rsi+offset),size);
            raw(label+".landscape",pointer(pointer(c.Rsi+0x10)),0x58);
            raw(label+".native_scale",base+0x4f03eec,4);raw(label+".native_one",base+0x4f044e8,4);raw(label+".native_margin",base+0x5ead218,4);
            }else{
                w->raw(label+".translated_axis",0,&c.Xmm0,4,"native_XMM0_low_binary32; register_not_memory_address");
                w->raw(label+".scale",0,&c.Xmm4,4,"native_XMM4_low_binary32; register_not_memory_address");
                if(s.name=="grid_y")w->raw(label+".scaled_x",0,&c.Xmm1,4,"native_XMM1_low_binary32; register_not_memory_address");
            }
        }else if(s.name=="grid_exit"){
            if(!gs.empty()&&gs.back().sp==c.Rsp+0xc8&&gs.back().caller==pointer(c.Rsp+0xc8)){id=gs.back().id;parent=gs.back().parent;gs.pop_back();pairing="paired";}else pairing="unmatched_exit";
        }
        // CONTEXT includes GPRs, EFlags, MXCSR and XMM0..15; no XSTATE assertion.
        w->raw(label+".context_windows",0,&c,sizeof c,"Windows_x64_CONTEXT_ALL; RIP_before_INT3_replay; not_XSTATE");
        raw(label+".stack",c.Rsp,128);
        event("boundary",",\"label\":"+quote(label)+",\"site\":"+quote(s.name)+",\"rva\":"+quote(hex(s.address-base))+",\"thread\":"+std::to_string(tid)+",\"invocation\":"+std::to_string(id)+",\"parent\":"+std::to_string(parent)+",\"pairing\":"+quote(pairing)+",\"sp\":"+quote(hex(c.Rsp))+",\"rcx\":"+quote(hex(c.Rcx))+",\"rdx\":"+quote(hex(c.Rdx))+",\"rbx\":"+quote(hex(c.Rbx))+",\"rdi\":"+quote(hex(c.Rdi))+",\"rbp\":"+quote(hex(c.Rbp))+",\"mxcsr\":"+std::to_string(c.MxCsr));
    }
    void retire(){
        // Called only while a debug event has stopped the entire target.
        if(pending){auto c=context(stepping);c.EFlags&=~0x100u;control(stepping,c);pending=nullptr;stepping=0;}
        for(auto& s:sites)if(s.installed)patch(s,false);
        for(auto& s:sites)if(s.armed_once){std::vector<unsigned char>b(s.original.size());require(r.bytes(s.address,b.data(),b.size())&&b==s.original,"retired_code_integrity");}
        resume();
    }
    void loop(){
        DEBUG_EVENT e{};bool have=false;DWORD disposition=DBG_CONTINUE;
        try{
            while(!exited){
                latency::profiler.wait_start=latency::now();
                if(!WaitForDebugEvent(&e,100)){
                    require(GetLastError()==ERROR_SEM_TIMEOUT,"wait");
                    if(!stop&&(fs::exists(root/L"STOP")||!disk())){stop=true;require(DebugBreakProcess(r.process)!=0,"stop_break");stop_break=true;}
                    continue;
                }
                latency::profiler.start(e);have=true;disposition=DBG_CONTINUE;
                auto code=e.dwDebugEventCode,tid=e.dwThreadId;
                if(code==CREATE_PROCESS_DEBUG_EVENT){base=(uint64_t)e.u.CreateProcessInfo.lpBaseOfImage;CloseHandle(e.u.CreateProcessInfo.hFile);CloseHandle(e.u.CreateProcessInfo.hProcess);threads[tid]=e.u.CreateProcessInfo.hThread;}
                if(code==CREATE_THREAD_DEBUG_EVENT){threads[tid]=e.u.CreateThread.hThread;if(pending&&tid!=stepping){require(SuspendThread(threads.at(tid))!=DWORD(-1),"new_thread_suspend");suspended.push_back(tid);}}
                if(code==LOAD_DLL_DEBUG_EVENT&&e.u.LoadDll.hFile)CloseHandle(e.u.LoadDll.hFile);
                if(code==EXIT_THREAD_DEBUG_EVENT){missing(centers[tid],"thread_exit");missing(grids[tid],"thread_exit");threads.erase(tid);suspended.erase(std::remove(suspended.begin(),suspended.end(),tid),suspended.end());require(tid!=stepping,"stepping_thread_exit");}
                if(code==EXIT_PROCESS_DEBUG_EVENT){event("target_exit",",\"exit_code\":"+std::to_string(e.u.ExitProcess.dwExitCode));exited=true;attached=false;}
                if(code==EXCEPTION_DEBUG_EVENT){
                    auto& ex=e.u.Exception;auto address=(uint64_t)ex.ExceptionRecord.ExceptionAddress;
                    disposition=DBG_EXCEPTION_NOT_HANDLED;
                    if(!ready&&ex.dwFirstChance&&ex.ExceptionRecord.ExceptionCode==EXCEPTION_BREAKPOINT&&address==breakin){
                        disposition=DBG_CONTINUE;
                        // Initial debugger break-in after all existing thread events.
                        bool grid_valid=true;
                        for(auto& s:sites){s.address+=base;std::vector<unsigned char>b(s.expected_hash.empty()?s.original.size():32);bool read=r.bytes(s.address,b.data(),b.size());
                            bool valid=read&&(s.expected_hash.empty()?b==s.original:sha_bytes(b.data(),b.size())==s.expected_hash);
                            if(s.name.starts_with("center_"))require(valid,"center_site_guard");else grid_valid&=valid;
                            if(valid&&!s.expected_hash.empty())s.original=b;
                        }
                        if(!grid_valid){event("grid_disabled",",\"reason\":\"grid_site_preimage_or_read_failure_before_install\"");sites.erase(std::remove_if(sites.begin(),sites.end(),[](auto& s){return s.name.starts_with("grid_");}),sites.end());}
                        for(auto& s:sites)patch(s,true);
                        ready=true;event("ready",",\"base\":"+quote(hex(base)));require(write_new(root/L"READY","0.1.4\n"),"ready_write");disposition=DBG_CONTINUE;
                    }else if(pending&&tid==stepping&&ex.dwFirstChance&&ex.ExceptionRecord.ExceptionCode==EXCEPTION_SINGLE_STEP){
                        auto c=context(tid);unsigned length=(pending->name=="grid_exit"?8:pending->name=="grid_x"||pending->name=="grid_y"||pending->name=="grid_result"?4:5);
                        require((c.Dr6&0xf)==0&&c.Rip==pending->address+length,"foreign_or_unexpected_step");
                        // Windows did not expose DR6.BS in the failed disposable
                        // control. Ownership uses pending TID, TF provenance and
                        // the verified next instruction, never assumed DR6.BS.
                        disposition=DBG_CONTINUE;c.EFlags&=~0x100u;control(tid,c);patch(*pending,true);pending=nullptr;stepping=0;resume();
                    }else if(ex.dwFirstChance&&ex.ExceptionRecord.ExceptionCode==EXCEPTION_BREAKPOINT){
                        auto it=std::find_if(sites.begin(),sites.end(),[&](auto& s){return s.installed&&s.address==address;});
                        if(it!=sites.end()){
                            require(!pending,"overlapping_replay");auto c=context(tid);require(c.Rip==address+1&&!(c.EFlags&0x100)&&!(c.Dr7&0xff),"foreign_debug_state");
                            c.Rip=address;
                            // Establish rollback before any collector/writer can fail.
                            control(tid,c);pending=&*it;stepping=tid;disposition=DBG_CONTINUE;
                            if(fail_writer){CloseHandle(w->log);w->log=INVALID_HANDLE_VALUE;}
                            latency::profiler.current.site=it->name;hit(*it,tid,c);suspend_others(tid);patch(*it,false);c.EFlags|=0x100;control(tid,c);disposition=DBG_CONTINUE;
                        }else if(stop_break&&address==breakin){disposition=DBG_CONTINUE;stop_break=false;}
                    }
                    if(disposition==DBG_EXCEPTION_NOT_HANDLED){event("exception",",\"thread\":"+std::to_string(tid)+",\"code\":"+std::to_string(ex.ExceptionRecord.ExceptionCode)+",\"first_chance\":"+std::to_string(ex.dwFirstChance));if(pending)stop=true;}
                }
                if(!exited&&(fs::exists(root/L"STOP")||!disk()))stop=true;
                if(stop&&!exited){retire();require(latency::continued(e.dwProcessId,tid,disposition)!=0,"continue_retired");have=false;require(DebugActiveProcessStop(pid)!=0,"detach");attached=false;event("retired",",\"restored\":true");break;}
                require(latency::continued(e.dwProcessId,tid,disposition)!=0,"continue");have=false;
            }
        }catch(...){
            // Writer failure cannot prevent the stopped-state rollback.
            if(have&&!exited){retire();require(latency::continued(e.dwProcessId,e.dwThreadId,disposition)!=0,"failure_continue");have=false;require(DebugActiveProcessStop(pid)!=0,"failure_detach");attached=false;}
            throw;
        }
        for(auto& [tid,stack]:centers)missing(stack,"retirement_or_process_exit");
        for(auto& [tid,stack]:grids)missing(stack,"retirement_or_process_exit");
    }
    static bool disk(){latency::Phase timing(latency::guard);ULARGE_INTEGER c{},d{};bool ok=GetDiskFreeSpaceExW(L"C:\\",&c,nullptr,nullptr)&&GetDiskFreeSpaceExW(L"D:\\",&d,nullptr,nullptr);return space_safe(c.QuadPart,d.QuadPart,ok);}
};
int wmain(int argc,wchar_t** argv){
    Adapter a;bool timing_ready=false;const char* stage="arguments";
    try{
    if(argc==2&&std::wstring(argv[1])==L"--version"){std::cout<<"0.1.4\n";return 0;}
    // --reviewed-retail is prospective only; execution requires the separate
    // approved live card. No launch, gameplay, saving or injection capability.
    if(argc!=6)return 2;
    a.fixture=std::wstring(argv[1])==L"--fixture";
    if(!a.fixture&&std::wstring(argv[1])!=L"--reviewed-retail")return 2;
    std::wstring pid_text(argv[2]);
    if(pid_text.empty()||!std::all_of(pid_text.begin(),pid_text.end(),[](wchar_t c){return c>=L'0'&&c<=L'9';}))throw std::invalid_argument("pid_argument");
    auto parsed_pid=std::stoull(pid_text);
    if(!parsed_pid||parsed_pid>MAXDWORD)throw std::out_of_range("pid_argument");
    a.pid=static_cast<DWORD>(parsed_pid);a.root=argv[3];
        stage="process_open";
        a.r.process=OpenProcess(PROCESS_ALL_ACCESS,FALSE,a.pid);a.require(a.r.process!=nullptr,"open");
        stage="image_query";
        wchar_t image[32768]{};DWORD n=32768;a.require(QueryFullProcessImageNameW(a.r.process,0,image,&n)!=0,"image");
        stage="output_validation";
        a.require(a.root.is_absolute()&&a.root.lexically_normal()==a.root,"output_root");
        for(auto cur=a.root;!cur.empty();){auto attrs=GetFileAttributesW(cur.c_str());a.require(attrs==INVALID_FILE_ATTRIBUTES||!(attrs&FILE_ATTRIBUTE_REPARSE_POINT),"output_reparse");auto parent=cur.parent_path();if(parent==cur)break;cur=parent;}
        stage="target_identity";
        if(a.fixture){
            a.require(fs::path(image).filename()==L"event_fixture.exe"&&sha_file(image)==std::string(fs::path(argv[4]).string()),"fixture_identity");
            std::ifstream plan(argv[5]);std::string name,bytes;uint64_t rva;
            while(plan>>name>>std::hex>>rva>>bytes){Site s{name,rva,{}};for(size_t i=0;i<bytes.size();i+=2)s.original.push_back((unsigned char)std::stoul(bytes.substr(i,2),nullptr,16));a.sites.push_back(s);}
            a.fail_writer=GetEnvironmentVariableW(L"SOR_DISPOSABLE_WRITER_FAILURE",nullptr,0)!=0;
        }else{
            a.require(fs::path(image).filename()==L"Starfield.exe"&&sha_file(image)==retail_hash&&fs::path(argv[4]).string()==retail_hash,"retail_identity");
            a.require(a.root.parent_path().filename()==L"event-oracle-live"&&a.root.parent_path().parent_path().filename()==L".local-work","retail_output_root");
            bool grid=std::wstring(argv[5])==L"--center-and-grid";a.require(grid||std::wstring(argv[5])==L"--center-only","retail_branch");
            for(auto s:retail_sites)if(grid||std::string(s.name).starts_with("center_"))a.sites.push_back({s.name,s.rva,{},false,s.sha256});
        }
        stage="site_plan";
        a.require(!a.sites.empty()&&a.sites.size()<=7,"scoped_sites");
        stage="module_identity";
        auto snap=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,a.pid);a.require(snap!=INVALID_HANDLE_VALUE,"module_snapshot");MODULEENTRY32W m{};m.dwSize=sizeof m;
        if(Module32FirstW(snap,&m))do {if(_wcsicmp(m.szModule,L"ntdll.dll")==0){auto local=GetModuleHandleW(L"ntdll.dll");wchar_t local_path[32768]{};
            a.require(GetModuleFileNameW(local,local_path,32768)!=0&&sha_file(local_path)==sha_file(m.szExePath),"ntdll_identity");
            a.breakin=(uint64_t)m.modBaseAddr+(uint64_t)GetProcAddress(local,"DbgBreakPoint")-(uint64_t)local;}}
        while(Module32NextW(snap,&m));CloseHandle(snap);a.require(a.breakin!=0,"breakin_identity");
        stage="output_create";
        fs::create_directories(a.root);timing_ready=true;stage="wal_create";EpochWriter w(a.root/L"evidence",Adapter::disk);a.w=&w;
        LARGE_INTEGER frequency{};a.require(QueryPerformanceFrequency(&frequency)!=0,"qpc_frequency");
        stage="session_write";
        a.event("session",",\"evidence_kind\":"+quote(a.fixture?"DISPOSABLE":"RUNTIME")+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"pid\":"+std::to_string(a.pid)+",\"image_sha256\":"+quote(sha_file(image)));
        stage="attach";
        a.require(DebugActiveProcess(a.pid)!=0,"attach");a.attached=true;
        stage="kill_on_exit_policy";a.require(DebugSetProcessKillOnExit(FALSE)!=0,"kill_on_exit_false");
        stage="event_loop";a.loop();
        stage="timing_write";a.require(Adapter::disk(),"timing_disk_guard");latency::profiler.save((a.root/L"timing.json").wstring());
        stage="terminal_write";w.finish(a.exited?"TARGET_EXIT":"RETIRED");CloseHandle(a.r.process);return 0;
    }catch(const std::exception& e){
        // Report the primary failure before best-effort telemetry. Never create
        // an unvalidated output path or let telemetry replace the original error.
        std::fprintf(stderr,"%s stage=%s attached=%d\n",e.what(),stage,int(a.attached));std::fflush(stderr);
        if(timing_ready)try{a.require(Adapter::disk(),"timing_disk_guard");latency::profiler.end();latency::profiler.save((a.root/L"timing.json").wstring());}
        catch(...){std::fputs("secondary_timing_failure\n",stderr);std::fflush(stderr);}
        if(a.r.process)CloseHandle(a.r.process);return 1;
    }catch(...){
        std::fprintf(stderr,"unknown_failure stage=%s attached=%d\n",stage,int(a.attached));std::fflush(stderr);
        if(a.r.process)CloseHandle(a.r.process);return 1;
    }
}
