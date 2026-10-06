// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "initialization.h"
#include <thread>

// Exercises the same startup sequencing/publication code as the observer,
// with injected service failures and private, synthetic Windows-thread I/O.
void initialization_tests(const sor::fs::path& root) {
    using namespace sor;
    auto make=[&](const char* name){auto p=root/name;fs::create_directory(p);return p;};
    auto marker="{\"kind\":\"SYNTHETIC\",\"terminal\":\"READY\"}\n";
    auto write=[](const fs::path& p,const std::string& s){return write_new(p,s);};
    auto scenario=[&](const char* name,bool listener,bool thread,bool throws) {
        auto path=make(name);Initialization init;bool start_called=false;std::string reason;
        auto failure=[&](const char* value){reason=value;write_new(path/L"failure.json","{\"kind\":\"SYNTHETIC\",\"reason\":"+quote(value)+"}\n");};
        auto resident=init.start([&]{return listener;},[&]()->bool {start_called=true;if(throws)throw std::runtime_error("injected");return thread;},failure);
        require(resident==listener,"resident status follows listener lifetime");
        require(start_called==listener,"worker never requested before listener success");
        require(!fs::exists(path/L"ready.json"),"service failure cannot publish READY");
        require(fs::is_regular_file(path/L"failure.json"),"service failure artifact");
        require(reason==(!listener?"listener_registration_failed":throws?"initialization_cpp_failure":"worker_start_failed"),"specific initialization failure");
    };
    scenario("listener-failure",false,false,false);
    scenario("thread-failure",true,false,false);
    scenario("thread-exception",true,false,true);
    {
        Initialization init;bool published=false;std::string reason;
        require(!init.worker_ready([&]{published=true;return true;},[&](const char* s){reason=s;}),"reject worker before listener");
        require(!published&&reason=="worker_without_listener","precondition blocks publication");
    }
    {
        auto path=make("worker-success");Initialization init;std::thread thread;
        HANDLE entered=CreateEventW(nullptr,TRUE,FALSE,nullptr),release=CreateEventW(nullptr,TRUE,FALSE,nullptr);
        require(entered&&release,"fixture synchronization events");
        bool result=false;std::string reason;
        auto failure=[&](const char* s){reason=s;};
        require(init.start([]{return true;},[&]{thread=std::thread([&]{
            SetEvent(entered);WaitForSingleObject(release,5000);
            result=init.worker_ready([&]{return publish_ready(path,marker,write);},failure);
        });return true;},failure),"successful service startup");
        auto arrived=WaitForSingleObject(entered,5000);
        bool absent=!fs::exists(path/L"ready.json");
        SetEvent(release);thread.join();CloseHandle(entered);CloseHandle(release);
        require(arrived==WAIT_OBJECT_0&&absent,"READY absent until worker publishes");
        require(result&&reason.empty()&&fs::is_regular_file(path/L"ready.json"),"READY after both services initialize");
        require(!fs::exists(path/L"ready.pending"),"successful publication renames pending file");
        std::string bytes;require(read_small(path/L"ready.json",bytes)&&bytes==marker,"complete marker readback");
        require(!publish_ready(path,"replacement",write),"READY cannot be overwritten");
        require(read_small(path/L"ready.json",bytes)&&bytes==marker,"existing marker preserved");
    }
    for(bool fail_write:{true,false}) {
        auto path=make(fail_write?"flush-failure":"rename-failure");Initialization init;
        init.listener_registered=true;std::string reason;
        auto failure=[&](const char* s){reason=s;write_new(path/L"failure.json","{\"kind\":\"SYNTHETIC\",\"reason\":"+quote(s)+"}\n");};
        auto injected=[&](const fs::path& p,const std::string& s){
            require(!fs::exists(path/L"ready.json"),"READY absent while writing pending");
            if(fail_write){write_new(p,"partial");return false;} // write/flush failure
            (void)s;return true; // missing pending file forces rename failure
        };
        require(!init.worker_ready([&]{return publish_ready(path,marker,injected);},failure),"publication failure propagates");
        require(!fs::exists(path/L"ready.json")&&fs::is_regular_file(path/L"failure.json"),"failed publication leaves only failure evidence");
        require(reason=="ready_publication_failed","publication failure reason");
    }
}
