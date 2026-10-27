// SPDX-License-Identifier: GPL-3.0-or-later
// D5B utilities precede the controller. Retail support is compiled separately
// and requires a future approved admission; Phase A executes only fixtures.
#include <cstddef>
static_assert(offsetof(CONTEXT,Rip)==0xf8&&offsetof(CONTEXT,Rsp)==0x98,"Windows x64 context layout");
struct Packet {uint64_t magic,manager,source,wrapper,slot;int32_t query[2];uint32_t mask,branch;};
#ifdef NATIVE_ABI
#include "native-capture.h"
#endif
#ifdef NATIVE_ABI
static constexpr unsigned SiteCount=d5l_native::site_count;
#else
static constexpr unsigned SiteCount=12;
#endif
struct ProbeThread {HANDLE handle;uint64_t lifetime;bool suspended=false;};
static bool set_owned_control(HANDLE thread,const CONTEXT& context,bool debug_status=false){
    // Request only observer-owned control changes, never write back floating
    // point/vector or integer groups merely because they were sampled.
    CONTEXT control=context;control.ContextFlags=CONTEXT_CONTROL|(debug_status?CONTEXT_DEBUG_REGISTERS:0);
    return SetThreadContext(thread,&control)!=FALSE;
}
int wmain(int argc,wchar_t** argv){
    PROCESS_INFORMATION pi{};
    try{
        disk_guard();
#ifdef D5L_RETAIL_TARGET
        require(argc==4&&std::wstring(argv[1])==L"--retail-pilot","separate Phase B admission required");
        std::wstring target=L"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Starfield\\Starfield.exe";
        std::string expected="7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28";
        std::wstring mode=L"retail";
#else
        require(argc==4&&std::wstring(argv[1])==L"--synthetic-fixture","disposable-only authority");
        std::string expected;for(auto p=argv[2];*p;++p)expected+=char(*p);
        wchar_t own[32768];require(GetModuleFileNameW(nullptr,own,32768)>0,"own path");
        std::wstring target=own;target=target.substr(0,target.find_last_of(L"\\/")+1)+
#ifdef NATIVE_ABI
          L"sor-d5l-native-fixture.exe";
#else
          L"sor-d5l-fixture.exe";
#endif
#endif
        auto image=file(target);require(sha(image)==expected,"target image pin");
        const char* names[SiteCount]={"owner_init","source_init","provider_entry","visited","lookup","inserted","query","mask","completed","owner_reset","owner_destroy","provider_exit"};
#ifdef NATIVE_ABI
        for(unsigned j=0;j<SiteCount;++j)names[j]=d5l_native::names[j];
        d5l_native::Config native_config;
#ifndef D5L_RETAIL_TARGET
        native_config.singleton=exported(image,"native_singleton");
        native_config.inner_return=exported(image,"native_inner_return");
        native_config.outer_returns[0]=exported(image,"native_outer_return");
        native_config.outer_returns[1]=native_config.outer_returns[2]=exported(image,"native_outer_return2");
        native_config.complete=exported(image,"native_complete");
        native_config.grid_vtable=exported(image,"native_grid_table");native_config.procgen_vtable=exported(image,"native_procgen_table");
#endif
#endif
        uint32_t sites[SiteCount];for(int j=0;j<SiteCount;++j)
#ifdef D5L_RETAIL_TARGET
            sites[j]=d5l_native::rvas[j];
        wchar_t* end=nullptr;pi.dwProcessId=wcstoul(argv[2],&end,10);require(end&&!*end&&pi.dwProcessId,"PID");
        pi.hProcess=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION|PROCESS_VM_READ|PROCESS_TERMINATE,FALSE,pi.dwProcessId);
        require(pi.hProcess!=nullptr,"future research target handle");
        wchar_t actual_path[32768];DWORD path_size=32768;
        require(QueryFullProcessImageNameW(pi.hProcess,0,actual_path,&path_size)&&!_wcsicmp(actual_path,target.c_str()),"pre-attach target identity");
#else
            sites[j]=exported(image,names[j]);
        auto event=L"Local\\sor-d5l-"+std::to_wstring(GetCurrentProcessId())+L"-"+std::to_wstring(GetTickCount64());
        fixture_gate=CreateEventW(nullptr,TRUE,FALSE,event.c_str());
        fixture_ready=CreateEventW(nullptr,TRUE,FALSE,(event+L"-ready").c_str());
        require(fixture_gate&&fixture_ready,"fixture gates");
        std::wstring mode=argv[3];auto command=L"\""+target+L"\" "+mode+L" "+event;
        STARTUPINFOW si{};si.cb=sizeof si;
        require(CreateProcessW(target.c_str(),command.data(),nullptr,nullptr,FALSE,CREATE_NO_WINDOW,nullptr,nullptr,&si,&pi),"create disposable");
        disposal_allowed=true;require(WaitForSingleObject(fixture_ready,10000)==WAIT_OBJECT_0,"main ready");
#endif
        FILETIME born{},exited{},kernel{},user{};require(GetProcessTimes(pi.hProcess,&born,&exited,&kernel,&user),"process creation identity");
        uint64_t creation=(uint64_t(born.dwHighDateTime)<<32)|born.dwLowDateTime;
#ifdef D5L_RETAIL_TARGET
        wchar_t* creation_end=nullptr;auto expected_creation=_wcstoui64(argv[3],&creation_end,10);
        require(creation_end&&!*creation_end&&expected_creation==creation,"admitted process lifetime");
        disposal_allowed=true;
#endif
        require(DebugActiveProcess(pi.dwProcessId),"fixture attach");attached=true;
        require(DebugSetProcessKillOnExit(TRUE),"kill disposable on debugger loss");
        std::map<DWORD,ProbeThread> threads;uint64_t base=0,serial=0,lifetime=0;
        bool started=false;DWORD stepping=0;int step_site=-1;unsigned char originals[SiteCount]{},guards[SiteCount][16]{};uint32_t next_rvas[SiteCount]{};
        bool injected_defer=false,injected_thread=false;
        auto patch=[&](int site,unsigned char byte){
            auto at=reinterpret_cast<void*>(base+sites[site]);DWORD prior=0;SIZE_T wrote=0;
            require(VirtualProtectEx(process,at,1,PAGE_EXECUTE_READWRITE,&prior),"scratch code protection");
            bool ok=WriteProcessMemory(process,at,&byte,1,&wrote)&&wrote==1;
            DWORD unused=0;bool restored=VirtualProtectEx(process,at,1,prior,&unused);
            require(ok&&restored&&FlushInstructionCache(process,at,1),"scratch breakpoint write");
            unsigned char actual=0;SIZE_T got=0;
            require(ReadProcessMemory(process,at,&actual,1,&got)&&got==1&&actual==byte,"code readback");
        };
        auto suspend=[&](DWORD except){for(auto i=threads.begin();i!=threads.end();){auto& t=i->second;
            if(i->first!=except&&!t.suspended){
                if(SuspendThread(t.handle)==DWORD(-1)){
                    DWORD error=GetLastError(),exit_code=259;
                    if(GetExitCodeThread(t.handle,&exit_code)&&exit_code!=STILL_ACTIVE){
                        std::cout<<"{\"kind\":\"DEAD_PEER\",\"tid\":"<<i->first<<",\"code\":"<<exit_code<<"}"<<std::endl;
                        CloseHandle(t.handle);i=threads.erase(i);continue;
                    }
                    if(error==ERROR_ACCESS_DENIED)return false;
                    throw std::runtime_error("peer suspend tid="+std::to_string(i->first)+" exit="+std::to_string(exit_code)+" error="+std::to_string(error));
                }t.suspended=true;
            }++i;}return true;};
        auto resume=[&](){for(auto& [tid,t]:threads)if(t.suspended){require(ResumeThread(t.handle)!=DWORD(-1),"peer resume");t.suspended=false;}};
        for(;;){
            disk_guard();DEBUG_EVENT ev{};
            if(!WaitForDebugEvent(&ev,500)){
                require(GetLastError()==ERROR_SEM_TIMEOUT,"debug wait");DWORD available=0;
                require(PeekNamedPipe(GetStdHandle(STD_INPUT_HANDLE),nullptr,0,nullptr,&available,nullptr),"control pipe");
                if(available){require(input_line()=="STOP","idle STOP");require(terminate_once(pi.hProcess,0xd510),"idle disposal");}
                continue;
            }
            pending=ev;pending_owned=true;pending_disposition=DBG_CONTINUE;
            require(ev.dwProcessId==pi.dwProcessId,"PID");
            if(ev.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT){
                if(ev.u.ExitProcess.dwExitCode&&!terminal)std::cout<<"{\"kind\":\"GAP\",\"reason\":\"unexpected_exit\"}"<<std::endl;
                std::cout<<"{\"kind\":\"EXIT\",\"code\":"<<ev.u.ExitProcess.dwExitCode<<",\"captures\":"<<serial<<"}"<<std::endl;
                require(continue_pending(),"exit continue");attached=false;break;
            }
            if(terminal){
                if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT&&ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);
                if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT)pending_disposition=DBG_EXCEPTION_NOT_HANDLED;
                std::cout<<"{\"kind\":\"TERMINAL_EVENT\"}"<<std::endl;
                require(continue_pending(),"terminal drain");continue;
            }
            if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT){
                process=ev.u.CreateProcessInfo.hProcess;base=reinterpret_cast<uint64_t>(ev.u.CreateProcessInfo.lpBaseOfImage);
                wchar_t actual[32768];DWORD size=32768;
                require(QueryFullProcessImageNameW(process,0,actual,&size)&&!_wcsicmp(actual,target.c_str())&&sha(file(actual))==expected,"stopped process identity");
                FILETIME actual_birth{};require(GetProcessTimes(process,&actual_birth,&exited,&kernel,&user)&&creation==((uint64_t(actual_birth.dwHighDateTime)<<32)|actual_birth.dwLowDateTime),"stopped process lifetime");
                threads.emplace(ev.dwThreadId,ProbeThread{ev.u.CreateProcessInfo.hThread,++lifetime});
                if(ev.u.CreateProcessInfo.hFile)CloseHandle(ev.u.CreateProcessInfo.hFile);
                auto mapped=LoadLibraryExW(target.c_str(),nullptr,LOAD_LIBRARY_AS_IMAGE_RESOURCE);require(mapped!=nullptr,"map fixture");
                auto local=reinterpret_cast<uint64_t>(mapped)&~uint64_t(3);
                for(int j=0;j<SiteCount;++j){unsigned char guard[16]{};reads=bytes=0;
                    require(read(base+sites[j],guard,16)&&!memcmp(guard,reinterpret_cast<void*>(local+sites[j]),16)&&guard[0]!=0xcc,"original instruction guard");originals[j]=guard[0];memcpy(guards[j],guard,16);
                    const unsigned char mov_rcx[]={0x48,0x89,0x4c,0x24,0x08};
#ifdef NATIVE_ABI
#ifdef D5L_RETAIL_TARGET
                    const uint32_t next[]={0x79fca6,0x79fcd4,0x78d660,0x79b8f1,0x79acf5,0x79ff24,0x79d8b5,0x79de96,0x79d915,0x975032,0x9829b5,0x983148,0x9828d8,0x982b75};
                    next_rvas[j]=next[j];
#else
                    next_rvas[j]=exported(image,(std::string("after_")+names[j]).c_str());
#endif
#else
                    require(!memcmp(guard,mov_rcx,5),"qualified fixture first instruction");
                    next_rvas[j]=sites[j]+5;
#endif
                }
                FreeLibrary(mapped);
                std::cout<<"{\"kind\":\"SESSION\",\"synthetic\":"
#ifdef D5L_RETAIL_TARGET
                    <<"false"
#else
                    <<"true"
#endif
                    <<",\"schema\":\""
#ifdef NATIVE_ABI
                    <<"sor-d5l-native/2"
#else
                    <<"sor-d5l/1"
#endif
                    <<"\",\"pid\":"<<pi.dwProcessId<<",\"creation_filetime_100ns\":"<<creation<<",\"image_sha256\":\""<<expected<<"\",\"module_base\":"<<base;
#ifdef NATIVE_ABI
                std::cout<<",\"sites\":[";for(unsigned j=0;j<SiteCount;++j){if(j)std::cout<<',';std::cout<<base+sites[j];}std::cout<<"],\"step_targets\":[";
                for(unsigned j=0;j<SiteCount;++j){if(j)std::cout<<',';std::cout<<base+next_rvas[j];}std::cout<<']';
#endif
                std::cout<<"}"<<std::endl;
            }else if(ev.dwDebugEventCode==CREATE_THREAD_DEBUG_EVENT){
                auto h=ev.u.CreateThread.hThread;threads.emplace(ev.dwThreadId,ProbeThread{h,++lifetime});
                if(stepping)require(suspend(stepping),"cannot fence new thread during rearm");
                std::cout<<"{\"kind\":\"THREAD_ARMED\",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<lifetime<<",\"rearm_window\":"<<(stepping?"true":"false")<<",\"process_wide_sites\":"<<SiteCount<<"}"<<std::endl;
            }else if(ev.dwDebugEventCode==EXIT_THREAD_DEBUG_EVENT){
                require(ev.dwThreadId!=stepping,"stepping thread exited");auto i=threads.find(ev.dwThreadId);
                if(i!=threads.end()){
                    std::cout<<"{\"kind\":\"THREAD_EXIT\",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<i->second.lifetime<<"}"<<std::endl;
                    CloseHandle(i->second.handle);threads.erase(i);}
            }else if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT){if(ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);
            }else if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT){
                auto code=ev.u.Exception.ExceptionRecord.ExceptionCode;pending_disposition=DBG_EXCEPTION_NOT_HANDLED;
                if(code==EXCEPTION_BREAKPOINT&&!started){
                    for(int j=0;j<SiteCount;++j)patch(j,0xcc);started=true;
                    std::cout<<"{\"kind\":\"ARM_BARRIER\",\"sites\":"<<SiteCount<<",\"readback\":true,\"all_threads\":"<<threads.size()<<",\"threads\":[";
                    bool comma=false;for(auto& [tid,t]:threads){CONTEXT c{};c.ContextFlags=CONTEXT_ALL;require(GetThreadContext(t.handle,&c)&&!(c.EFlags&0x100)&&!(c.Dr7&0xff),"barrier foreign control state");
                        if(comma)std::cout<<',';comma=true;std::cout<<"{\"tid\":"<<tid<<",\"lifetime\":"<<t.lifetime<<"}";}std::cout<<"]}"<<std::endl;
                    auto ack=input_line();if(ack=="STOP")require(terminate_once(pi.hProcess,0xd510),"pre-arm stop");
                    else{require(ack=="ARM_ACK","arm ACK");
#ifndef D5L_RETAIL_TARGET
                        require(SetEvent(fixture_gate),"release fixture");
#endif
                    }
                    pending_disposition=DBG_CONTINUE;
                }else if(code==EXCEPTION_SINGLE_STEP&&stepping==ev.dwThreadId){
                    auto& t=threads.at(stepping);CONTEXT c{};c.ContextFlags=CONTEXT_ALL;
                    require(GetThreadContext(t.handle,&c)&&!(c.Dr6&15)&&c.Rip==base+next_rvas[step_site],"owned step");
                    patch(step_site,0xcc);c.EFlags&=~0x100UL;c.Dr6=0;
                    require(set_owned_control(t.handle,c,true),"clear owned TF");stepping=0;step_site=-1;resume();pending_disposition=DBG_CONTINUE;
                }else if(code==EXCEPTION_BREAKPOINT&&started){
                    auto& t=threads.at(ev.dwThreadId);CONTEXT c{};c.ContextFlags=CONTEXT_ALL;
                    require(GetThreadContext(t.handle,&c),"trap context");int site=-1;
                    for(int j=0;j<SiteCount;++j)if(c.Rip==base+sites[j]+1)site=j;
                    require(site>=0,"owned software breakpoint");
                    // A peer may have executed INT3 before all-stop was delivered.
                    // Rewind its queued trap while it remains suspended. Once the
                    // current step rearms the site, this peer will trap again.
                    if(stepping){
                        require(stepping!=ev.dwThreadId&&t.suspended,"queued peer must remain fenced");c.Rip--;
                        require(set_owned_control(t.handle,c),"queued peer rewind");
                        CONTEXT check{};check.ContextFlags=CONTEXT_ALL;require(GetThreadContext(t.handle,&check),"queued peer context readback");
                        bool gpr=!memcmp(&check.Rax,&c.Rax,17*sizeof(DWORD64)),fp=!memcmp(&check.FltSave,&c.FltSave,sizeof c.FltSave),flags=(check.EFlags&~2UL)==(c.EFlags&~2UL);
                        if(!gpr||!fp||!flags)std::cerr<<"queued context mismatch gpr="<<gpr<<" fp="<<fp<<" flags="<<flags<<" actual="<<check.EFlags<<" expected="<<c.EFlags<<" rip="<<check.Rip<<" expected_rip="<<c.Rip<<std::endl;
                        require(gpr&&fp&&flags&&check.MxCsr==c.MxCsr,"queued peer CPU preservation");
                        std::cout<<"{\"kind\":\"PARKED_TRAP\",\"tid\":"<<ev.dwThreadId<<"}"<<std::endl;
                    }else{
                        require(!(c.EFlags&0x100)&&!(c.Dr7&0xff),"foreign TF or hardware slots");
                        bool peers_fenced=true;
                        if(mode==L"defer-peer"&&!injected_defer){suspend(ev.dwThreadId);peers_fenced=false;injected_defer=true;}
                        else peers_fenced=suspend(ev.dwThreadId);
                        if(!peers_fenced){
                            // No instruction has been restored and no sample has
                            // been acknowledged. Rewind this trap, undo only our
                            // suspensions, and drain normal debug events. A peer
                            // with denied suspend rights is never assumed dead.
                            c.Rip--;require(set_owned_control(t.handle,c),"deferred trap rewind");resume();
                            std::cout<<"{\"kind\":\"DEFERRED_TRAP\",\"tid\":"<<ev.dwThreadId<<"}"<<std::endl;
                            pending_disposition=DBG_CONTINUE;require(continue_pending(),"deferred continue");continue;
                        }
                        reads=bytes=0;for(int j=0;j<SiteCount;++j){unsigned char b[16]{};require(read(base+sites[j],b,16),"continuous instruction read");
                            for(unsigned k=0;k<16;++k){unsigned char expected_byte=guards[j][k];for(unsigned m=0;m<SiteCount;++m)if(sites[j]+k==sites[m])expected_byte=0xcc;
                                require(b[k]==expected_byte,"continuous instruction guard");}}
#ifdef NATIVE_ABI
                        std::cout<<"{\"kind\":\"SAMPLE\",\"capture\":"<<++serial<<",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<t.lifetime
                            <<",\"site\":"<<site<<",\"rip\":"<<c.Rip<<",\"rsp\":"<<c.Rsp<<",\"raw_context\":\""<<hex(&c,sizeof c)<<'"';
                        d5l_native::capture(site,c,base,native_config);
#ifndef D5L_RETAIL_TARGET
                        uint64_t phase=0;bool oracle=read(base+exported(image,"fixture_reset_phase"),&phase,8);
                        std::cout<<",\"fixture_oracle\":{\"read_complete\":"<<(oracle?"true":"false")<<",\"reset_phase\":"<<phase<<"}";
#endif
                        FILETIME utc{};GetSystemTimeAsFileTime(&utc);
                        std::cout<<",\"utc_filetime_100ns\":"<<((uint64_t(utc.dwHighDateTime)<<32)|utc.dwLowDateTime)<<"}"<<std::endl;
#else
                        Packet p{};bool ok=read(c.Rcx,&p,sizeof p)&&p.magic==0x44354c5041434b31;
                        unsigned char population[40]{};bool population_ok=ok&&p.wrapper&&read(p.wrapper,population,40);
                        unsigned char slot_bytes[24]{};bool slot_ok=ok&&p.slot&&read(p.slot,slot_bytes,24);
                        std::cout<<"{\"kind\":\"SAMPLE\",\"capture\":"<<++serial<<",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<t.lifetime
                            <<",\"site\":"<<site<<",\"rsp\":"<<c.Rsp<<",\"packet_address\":"<<c.Rcx<<",\"raw_context\":\""<<hex(&c,sizeof c)<<"\",\"read_complete\":"<<(ok?"true":"false")
                            <<",\"raw_packet\":\""<<(ok?hex(&p,sizeof p):std::string())<<"\",\"slot_read\":"<<(slot_ok?"true":"false")<<",\"slot\":\""<<(slot_ok?hex(slot_bytes,24):std::string())<<"\",\"population_complete_read\":"<<(population_ok?"true":"false")<<",\"population\":\""<<(population_ok?hex(population,40):std::string())<<"\"}"<<std::endl;
#endif
                        auto ack=input_line();require(ack=="ACK "+std::to_string(serial)||ack=="ACK "+std::to_string(serial)+" STOP","durable sample ACK");
                        if(ack.find(" STOP")!=std::string::npos)require(terminate_once(process,0xd510),"STOP disposal");
                        else{
                            if(mode==L"guard-loss"&&serial==1)patch(11,originals[11]);
                            patch(site,originals[site]);c.Rip--;c.EFlags|=0x100;
                            require(set_owned_control(t.handle,c),"owned rewind and TF");stepping=ev.dwThreadId;step_site=site;
                            CONTEXT v{};v.ContextFlags=CONTEXT_ALL;require(GetThreadContext(t.handle,&v),"resume context readback");
                            require(!memcmp(&v.Rax,&c.Rax,17*sizeof(DWORD64))&&!memcmp(&v.FltSave,&c.FltSave,sizeof c.FltSave)&&v.MxCsr==c.MxCsr&&(v.EFlags&~2UL)==(c.EFlags&~2UL),"CPU preservation");
#if defined(NATIVE_ABI) && !defined(D5L_RETAIL_TARGET)
                            if(mode==L"new-peer-step"&&!injected_thread){
                                DWORD tid=0;auto at=base+exported(image,"fixture_thread_start");
                                auto h=CreateRemoteThread(process,nullptr,0,reinterpret_cast<LPTHREAD_START_ROUTINE>(at),nullptr,0,&tid);
                                require(h!=nullptr,"synthetic peer creation");CloseHandle(h);injected_thread=true;
                                std::cout<<"{\"kind\":\"SYNTHETIC_THREAD_REQUEST\",\"tid\":"<<tid<<"}"<<std::endl;
                            }
#endif
                            if(mode==L"step-stop"){
                                std::cout<<"{\"kind\":\"GAP\",\"reason\":\"synthetic_interrupted_rearm\"}"<<std::endl;
                                require(terminate_once(process,0xd510),"interrupted step disposal");
                            }
                        }
                    }
                    pending_disposition=DBG_CONTINUE;
                }else{
#ifdef NATIVE_ABI
                    require(!stepping&&code!=EXCEPTION_SINGLE_STEP,"exception during rearm or foreign single step");
                    auto& t=threads.at(ev.dwThreadId);
                    std::cout<<"{\"kind\":\"TARGET_EXCEPTION\",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<t.lifetime<<",\"code\":"<<code
                        <<",\"first_chance\":"<<ev.u.Exception.dwFirstChance<<"}"<<std::endl;
#else
                    std::cout<<"{\"kind\":\"GAP\",\"reason\":\"unowned_exception\"}"<<std::endl;
#endif
                }
            }
            require(continue_pending(),"debug continue");
        }
        for(auto& [tid,t]:threads)CloseHandle(t.handle);
        CloseHandle(pi.hThread);CloseHandle(pi.hProcess);CloseHandle(fixture_gate);CloseHandle(fixture_ready);return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<std::endl;
        std::cout<<"{\"kind\":\"GAP\",\"reason\":\"controller_fatal\"}"<<std::endl;
        if(disposal_allowed&&pi.hProcess)drain_failure(pi.hProcess,pi.dwProcessId);return 2;}
}
