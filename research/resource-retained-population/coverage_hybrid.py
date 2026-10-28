# SPDX-License-Identifier: GPL-3.0-or-later
"""D5O bounded adapter; reads owned sources, returns generated C++ in memory.

No process or file writes. Keeps historical D5N sources unchanged. The header
adds durable coverage operands; lifecycle handling excludes only proven exits.
"""
import hybrid
SRC = hybrid.SRC


def controller(text):
    text = hybrid.controller(text)
    text = hybrid.replace(text, 'int wmain(int argc,wchar_t** argv){',
                          '#include "coverage-hybrid.h"\nint wmain(int argc,wchar_t** argv){')
    text = hybrid.replace(text, 'bool injected_fault=false;',
                          'bool injected_fault=false,coverage_injected=false;')
    old = '''for(auto& [tid,peer]:threads){CONTEXT v{};v.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                            require(GetThreadContext(peer.handle,&v)&&hardware_context(v,base+sites[10]),"continuous hardware coverage");}'''
    text = hybrid.replace(text, old, '''for(auto& [tid,peer]:threads)
                            check_coverage(tid,peer,base+sites[10],site,mode,coverage_injected);''')
    # Exit-code 259 can be a real termination value. A signalled retained thread
    # handle proves termination; a denied suspend alone never does.
    text = hybrid.replace(text, 'auto suspend=[&](DWORD except){', '''auto terminated_peer=[&](DWORD tid,const ProbeThread& peer,const char* phase){
            auto result=WaitForSingleObject(peer.handle,0);auto error=result==WAIT_FAILED?GetLastError():0;
            diagnostic("PEER_STATE",",\\"peer_tid\\":"+std::to_string(tid)+",\\"peer_lifetime\\":"+std::to_string(peer.lifetime)
                +",\\"phase\\":\\""+phase+"\\",\\"wait\\":"+std::to_string(result)+",\\"error\\":"+std::to_string(error));
            require(result==WAIT_OBJECT_0||result==WAIT_TIMEOUT,"peer state query");return result==WAIT_OBJECT_0;
        };
        auto suspend=[&](DWORD except){''')
    text = hybrid.replace(text, 'if(GetExitCodeThread(t.handle,&exit_code)&&exit_code!=STILL_ACTIVE){', '''if(terminated_peer(i->first,t,"suspend")){
                        BOOL exit_ok=GetExitCodeThread(t.handle,&exit_code);auto exit_error=exit_ok?0:GetLastError();
                        diagnostic("PEER_EXIT_CODE",",\\"peer_tid\\":"+std::to_string(i->first)+",\\"peer_lifetime\\":"+std::to_string(t.lifetime)
                            +",\\"ok\\":"+(exit_ok?"true":"false")+",\\"error\\":"+std::to_string(exit_error)+",\\"exit_code\\":"+std::to_string(exit_code));
                        require(exit_ok!=FALSE,"proven exit code query");''')
    text = hybrid.replace(text, '+" exit="+std::to_string(exit_code)+" error="', '+" exit=UNKNOWN error="')
    text = hybrid.replace(text, 'close_owned(i->second.handle);threads.erase(i);', '''
#ifndef D5L_RETAIL_TARGET
                    // Deliberately retain an exited identity after continuing
                    // its EXIT event, to exercise the real signalled-object path.
                    if(mode==L"coverage-exit")diagnostic("FIXTURE_RETAIN_EXITED",",\\"exit_code\\":"+std::to_string(ev.u.ExitThread.dwExitCode));else
#endif
                    {close_owned(i->second.handle);threads.erase(i);}''')
    text = hybrid.replace(text, 'if(t.suspended){auto prior=ResumeThread(t.handle);', '''if(t.suspended){
            if(terminated_peer(tid,t,"resume")){t.suspended=false;
                diagnostic("EXITED_PEER_RELEASE",",\\"peer_tid\\":"+std::to_string(tid)+",\\"peer_lifetime\\":"+std::to_string(t.lifetime));continue;}
            auto prior=ResumeThread(t.handle);''')
    return text


def fixture(text):
    text = hybrid.fixture(text)
    text = hybrid.replace(text, 'int wmain(int argc,wchar_t** argv){',
                          'static DWORD WINAPI exit259(void*){return 259;}\nint wmain(int argc,wchar_t** argv){')
    return hybrid.replace(text, '    if(mode==L"foreign-first")', '''
    if(mode==L"coverage-exit"){
        auto exiting=CreateThread(nullptr,0,exit259,nullptr,0,nullptr);if(!exiting)return 11;
        WaitForSingleObject(exiting,INFINITE);CloseHandle(exiting);
    }
    if(mode==L"coverage-exit-race"){
        HANDLE release=CreateEventW(nullptr,TRUE,FALSE,nullptr);if(!release)return 12;
        std::vector<std::thread> peers;
        for(int i=0;i<96;++i)peers.emplace_back([&]{WaitForSingleObject(release,INFINITE);});
        SetEvent(release);
        for(int n=0;n<32;++n){state.clear();fixture_reset_phase=2;fixture_reset(p.procgen);}
        for(auto& peer:peers)peer.join();CloseHandle(release);
    }
    if(mode==L"coverage-stress"||mode==L"coverage-api-failure"||mode==L"coverage-dr0-loss"||mode==L"coverage-dr7-loss"||mode==L"coverage-dr7-type-loss"||mode==L"coverage-gd-sanitized"||mode==L"coverage-gd-return-fault"){
        HANDLE release=CreateEventW(nullptr,TRUE,FALSE,nullptr);if(!release)return 10;
        std::vector<std::thread> peers;
        std::barrier admitted(97);
        for(int i=0;i<96;++i)peers.emplace_back([&]{admitted.arrive_and_wait();WaitForSingleObject(release,INFINITE);});
        // Reaching user-mode startup proves each CREATE event was continued.
        // Do not let Reset race ahead of admission of the intended peer set.
        admitted.arrive_and_wait();
        for(int n=0;n<(mode==L"coverage-stress"?32:1);++n){
            state.clear();fixture_reset_phase=2;fixture_reset(p.procgen);
            native_grid_clear(p.grid);fixture_grid_init(p.grid);fixture_source_init(p.source,p.grid,state.definition.b.data());
        }
        SetEvent(release);for(auto& peer:peers)peer.join();CloseHandle(release);
    }
    if(mode==L"foreign-first")''')
