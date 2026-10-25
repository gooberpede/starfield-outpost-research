// SPDX-License-Identifier: GPL-3.0-or-later
// Included after the owned D5B controller utilities by build.py.
// Fixture and native builds have separate explicit entry points.
struct Packet {
    uint64_t magic, manager, source, manager_epoch, source_epoch, invocation, parent, visited_key, wrapper, lookup, capacity;
    int32_t query[2]; uint32_t mask, branch, inserted, complete, geo, ready;
};
struct DecisionThread { HANDLE handle; uint64_t lifetime; };
int wmain(int argc,wchar_t** argv){
    PROCESS_INFORMATION pi{};
    try{
        disk_guard();
#ifdef RETAIL_FIXTURE
        require(argc==4&&std::wstring(argv[1])==L"--synthetic-fixture","synthetic-only authority");
        std::string expected;for(auto p=argv[2];*p;++p){require(*p>=32&&*p<=126,"ASCII hash");expected+=char(*p);}
        wchar_t own[32768]; require(GetModuleFileNameW(nullptr,own,32768)>0,"own path");
        std::wstring target=own; target=target.substr(0,target.find_last_of(L"\\/")+1)+L"sor-d5e-fixture.exe";
        auto image=file(target);require(sha(image)==expected,"fixture hash");
        const char* names[]={"decision_visited","decision_lookup","decision_mask","decision_terminal"};
        uint32_t sites[4];for(unsigned j=0;j<4;++j)sites[j]=exported(image,names[j]);
        std::wstring mode=argv[3];
        auto event_name=L"Local\\sor-d5e-"+std::to_wstring(GetCurrentProcessId())+L"-"+std::to_wstring(GetTickCount64());
        fixture_gate=CreateEventW(nullptr,TRUE,FALSE,event_name.c_str());require(fixture_gate!=nullptr,"fixture barrier");
        fixture_ready=CreateEventW(nullptr,TRUE,FALSE,(event_name+L"-ready").c_str());require(fixture_ready!=nullptr,"fixture ready");
        auto command=L"\""+target+L"\" "+mode+L" "+event_name;
        STARTUPINFOW si{};si.cb=sizeof si;
        require(CreateProcessW(target.c_str(),command.data(),nullptr,nullptr,FALSE,CREATE_NO_WINDOW,nullptr,nullptr,&si,&pi),"create gated fixture");
        disposal_allowed=true;
        require(WaitForSingleObject(fixture_ready,10000)==WAIT_OBJECT_0,"fixture main readiness");
#else
        require(argc==3&&std::wstring(argv[1])==L"--retail-pilot","explicit retail PID required");
        std::wstring target=L"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Starfield\\Starfield.exe";
        std::string expected="7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28";
        require(sha(file(target))==expected,"pinned retail image");
        uint32_t sites[4]={0x79fca3,0x79fcd0,0x79b8ed,0x79feaf};
        wchar_t* end=nullptr;auto pid=wcstoul(argv[2],&end,10);require(end&&!*end&&pid,"PID domain");
        pi.dwProcessId=pid;pi.hProcess=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION|PROCESS_VM_READ|PROCESS_TERMINATE,FALSE,pid);
        require(pi.hProcess!=nullptr,"retail rights");
        wchar_t before_path[32768];DWORD before_size=32768;
        require(QueryFullProcessImageNameW(pi.hProcess,0,before_path,&before_size)&&!_wcsicmp(before_path,target.c_str())&&sha(file(before_path))==expected,"pre-attach identity");
        // This path requires the separately approved crash-tolerant run card.
        disposal_allowed=true;
#endif
        require(DebugActiveProcess(pi.dwProcessId),"attach disposable fixture");attached=true;
        require(DebugSetProcessKillOnExit(TRUE),"synthetic kill-on-exit");
        std::map<DWORD,DecisionThread> threads;
        uint64_t base=0,sequence=0,lifetime=0; bool started=false;
        unsigned char guards[4][16]{};
        auto arm=[&](HANDLE h,bool initial){
            CONTEXT c{};c.ContextFlags=CONTEXT_ALL;require(GetThreadContext(h,&c),"arm context");
            if(initial)require((!(c.Dr7&0xffff00ff)||((c.Dr7&0xffff00ff)==0x55&&c.Dr0==base+sites[0]&&c.Dr1==base+sites[1]&&c.Dr2==base+sites[2]&&c.Dr3==base+sites[3]))&&!(c.EFlags&0x100),"slot pressure or TF");
            c.Dr0=base+sites[0];c.Dr1=base+sites[1];c.Dr2=base+sites[2];c.Dr3=base+sites[3];
            c.Dr6=0;c.Dr7=(c.Dr7&~0xffff00ffULL)|0x55;
            require(SetThreadContext(h,&c),"arm");
            CONTEXT v{};v.ContextFlags=CONTEXT_DEBUG_REGISTERS;
            require(GetThreadContext(h,&v)&&v.Dr0==c.Dr0&&v.Dr1==c.Dr1&&v.Dr2==c.Dr2&&v.Dr3==c.Dr3&&(v.Dr7&0xffff00ff)==0x55,"arm readback");
        };
        for(;;){
            disk_guard();DEBUG_EVENT ev{};
            if(!WaitForDebugEvent(&ev,1000)){
                require(GetLastError()==ERROR_SEM_TIMEOUT,"debug wait");
                DWORD available=0;
                require(PeekNamedPipe(GetStdHandle(STD_INPUT_HANDLE),nullptr,0,nullptr,&available,nullptr),"idle control pipe closed");
                if(available){
                    require(input_line()=="STOP","idle STOP");require(terminate_once(pi.hProcess,0xd5e0),"idle disposal");}
                continue;
            }
            pending=ev;pending_owned=true;pending_disposition=DBG_CONTINUE;
            require(ev.dwProcessId==pi.dwProcessId,"PID");
            if(terminal&&ev.dwDebugEventCode!=EXIT_PROCESS_DEBUG_EVENT){
                if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT&&ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);
                if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT&&ev.u.CreateProcessInfo.hFile)CloseHandle(ev.u.CreateProcessInfo.hFile);
                if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT)pending_disposition=DBG_EXCEPTION_NOT_HANDLED;
                std::cout<<"{\"kind\":\"TERMINAL_EVENT\",\"event\":"<<ev.dwDebugEventCode<<"}"<<std::endl;
                require(continue_pending(),"terminal continue");continue;
            }
            if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT){
                process=ev.u.CreateProcessInfo.hProcess;base=reinterpret_cast<uint64_t>(ev.u.CreateProcessInfo.lpBaseOfImage);
                wchar_t actual[32768];DWORD n=32768;require(QueryFullProcessImageNameW(process,0,actual,&n)&&!_wcsicmp(actual,target.c_str())&&sha(file(actual))==expected,"actual identity");
                auto mapped=LoadLibraryExW(target.c_str(),nullptr,LOAD_LIBRARY_AS_IMAGE_RESOURCE);require(mapped!=nullptr,"map image");
                auto local=reinterpret_cast<uint64_t>(mapped)&~uint64_t(3);
                for(unsigned j=0;j<4;++j)require(read(base+sites[j],guards[j],16)&&!memcmp(guards[j],reinterpret_cast<void*>(local+sites[j]),16),"instruction guard");
                FreeLibrary(mapped);if(ev.u.CreateProcessInfo.hFile)CloseHandle(ev.u.CreateProcessInfo.hFile);
                threads.emplace(ev.dwThreadId,DecisionThread{ev.u.CreateProcessInfo.hThread,++lifetime});
                std::cout<<"{\"kind\":\"SESSION\",\"pid\":"<<pi.dwProcessId<<",\"module_base\":"<<base<<",\"image_sha256\":\""<<expected<<"\",\"schema\":\"sor-d5e/1\",\"synthetic\":";
#ifdef RETAIL_FIXTURE
                std::cout<<"true";
#else
                std::cout<<"false";
#endif
                std::cout<<"}"<<std::endl;
            }else if(ev.dwDebugEventCode==CREATE_THREAD_DEBUG_EVENT){
                require(!terminal,"post-stop thread");
                arm(ev.u.CreateThread.hThread,true);
                threads.emplace(ev.dwThreadId,DecisionThread{ev.u.CreateThread.hThread,++lifetime});
                std::cout<<"{\"kind\":\"THREAD_ARMED\",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<lifetime<<"}"<<std::endl;
            }else if(ev.dwDebugEventCode==EXIT_THREAD_DEBUG_EVENT){
                auto it=threads.find(ev.dwThreadId);if(it!=threads.end()){CloseHandle(it->second.handle);threads.erase(it);}
            }else if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT){if(ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);
            }else if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT){
                auto x=ev.u.Exception;auto code=x.ExceptionRecord.ExceptionCode;
                pending_disposition=DBG_EXCEPTION_NOT_HANDLED;
                if(code==EXCEPTION_BREAKPOINT&&!started){
#ifdef RETAIL_FIXTURE
                    if(mode==L"slot-pressure"){
                        auto h=threads.begin()->second.handle;CONTEXT pressure{};pressure.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                        require(GetThreadContext(h,&pressure),"pressure read");pressure.Dr0=base+sites[0]+1;pressure.Dr7=1;
                        require(SetThreadContext(h,&pressure),"synthetic foreign slot");}
#endif
                    for(auto& [id,t]:threads)arm(t.handle,true);
                    started=true;pending_disposition=DBG_CONTINUE;
                    std::cout<<"{\"kind\":\"ARM_BARRIER\",\"all_threads\":"<<threads.size()<<",\"slots\":4,\"readback\":true}"<<std::endl;
                    require(input_line()=="ARM_ACK","durable arm ACK");
#ifdef RETAIL_FIXTURE
                    require(SetEvent(fixture_gate),"release pre-load barrier");
#endif
                }else if(code==EXCEPTION_SINGLE_STEP&&!terminal){
                    auto& t=threads.at(ev.dwThreadId);CONTEXT c{};c.ContextFlags=CONTEXT_ALL;
                    require(GetThreadContext(t.handle,&c),"sample context");
                    int slot=retail::owned_slot(base,c.Rip,c.Dr6,sites);
                    require(slot>=0&&(c.Dr6&15)==(1ULL<<slot)&&!(c.Dr6&0x6000)&&c.Dr0==base+sites[0]&&c.Dr1==base+sites[1]&&c.Dr2==base+sites[2]&&c.Dr3==base+sites[3]&&(c.Dr7&0xffff00ff)==0x55,"coverage loss");
                    reads=bytes=0;unsigned char guard[16]{};
                    require(read(c.Rip,guard,16)&&!memcmp(guard,guards[slot],16),"hit guard");
                    FILETIME utc{};GetSystemTimeAsFileTime(&utc);
                    std::cout<<"{\"kind\":\"SAMPLE\",\"capture\":"<<++sequence<<",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<t.lifetime<<",\"site\":"<<slot<<",\"rip\":"<<c.Rip<<",\"rsp\":"<<c.Rsp<<",\"utc_filetime_100ns\":"<<((uint64_t(utc.dwHighDateTime)<<32)|utc.dwLowDateTime)<<",\"raw_context\":\""<<hex(&c,sizeof c)<<"\"";
#ifdef RETAIL_FIXTURE
                    Packet p{};bool ok=read(c.Rcx,&p,sizeof p)&&p.magic==0x4435455041434b31;
                    std::cout<<",\"native_read_complete\":"<<(ok?"true":"false")<<",\"raw_packet\":\""<<(ok?hex(&p,sizeof p):std::string())<<"\"";
#else
                    #include "native.inc"
#endif
                    std::cout<<"}"<<std::endl;
                    auto ack=input_line();require(ack=="ACK "+std::to_string(sequence)||ack=="ACK "+std::to_string(sequence)+" STOP","capture ACK");
                    if(ack.find(" STOP")!=std::string::npos){require(terminate_once(process,0xd5e0),"fixture STOP");}
                    else{
                        auto before=c;c.ContextFlags=CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;c.Dr6=0;c.EFlags|=0x10000;
                        require(SetThreadContext(t.handle,&c),"RF resume");
                        CONTEXT v{};v.ContextFlags=CONTEXT_ALL;require(GetThreadContext(t.handle,&v),"resume readback");
                        require(!memcmp(&before.Rax,&v.Rax,17*sizeof(DWORD64))&&!memcmp(&before.FltSave,&v.FltSave,sizeof v.FltSave)&&before.MxCsr==v.MxCsr&&(before.EFlags&~0x10002UL)==(v.EFlags&~0x10002UL)&&v.Dr0==c.Dr0&&v.Dr1==c.Dr1&&v.Dr2==c.Dr2&&v.Dr3==c.Dr3&&(v.Dr7&0xffff00ff)==0x55,"CPU/coverage readback");
#ifdef RETAIL_FIXTURE
                        if(mode==L"lost-slot"&&sequence==1){v.ContextFlags=CONTEXT_DEBUG_REGISTERS;v.Dr3+=1;
                            require(SetThreadContext(t.handle,&v),"synthetic slot loss");}
#endif
                    }
                    pending_disposition=DBG_CONTINUE;
                }else{
                    std::cout<<"{\"kind\":\"GAP\",\"reason\":\"unowned-exception\",\"code\":"<<code<<"}"<<std::endl;
                }
            }else if(ev.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT){
                if(ev.u.ExitProcess.dwExitCode&&!terminal)std::cout<<"{\"kind\":\"GAP\",\"reason\":\"unexpected_target_exit\"}"<<std::endl;
                std::cout<<"{\"kind\":\"EXIT\",\"code\":"<<ev.u.ExitProcess.dwExitCode<<",\"captures\":"<<sequence<<"}"<<std::endl;
                require(continue_pending(),"exit continue");attached=false;break;
            }
            require(continue_pending(),"continue");
        }
        for(auto& [id,t]:threads)CloseHandle(t.handle);
        CloseHandle(pi.hThread);CloseHandle(pi.hProcess);CloseHandle(fixture_gate);CloseHandle(fixture_ready);return 0;
    }catch(const std::exception& e){
        std::cerr<<e.what()<<std::endl;
        std::cout<<"{\"kind\":\"GAP\",\"reason\":\"controller-fatal\"}"<<std::endl;
        if(disposal_allowed&&pi.hProcess)drain_failure(pi.hProcess,pi.dwProcessId);
        return 2;
    }
}
