// SPDX-License-Identifier: GPL-3.0-or-later
// Includes the real plugin worker in a disposable executable. Synthetic table
// slots replace retail guard inputs only; no SFSE/game executes or is loaded.
#include "plugin.cpp"
#include <iostream>
using namespace history;
void demand(bool v,const char* msg){if(!v)throw std::runtime_error(msg);std::cout<<"PASS "<<msg<<"\n";}
int main(int argc,char** argv){
    try{
        if(argc!=3)return 2;session=fs::path(argv[1]);fs::create_directory(session);std::string scenario=argv[2];session_identity="{\"version\":\"0.8.0\",\"schema\":8,\"fixture\":true";
        auto* memory=static_cast<unsigned char*>(VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE));demand(memory!=nullptr,"fixture native table allocation");image_base=reinterpret_cast<uint64_t>(memory);
        for(size_t i=0;i<count;++i){auto& s=sites[i];s.rva=i*8;s.target=0x800;s.length=8;auto before=image_base+s.target,after=reinterpret_cast<uint64_t>(s.hook);memcpy(memory+i*8,&before,8);auto& e=edits[i];e.address=memory+i*8;e.size=8;memcpy(e.before,&before,8);memcpy(e.after,&after,8);}
        std::string zero_hash=sha_bytes(memory+0x800,32);for(auto& g:target_guards){g.rva=0x800;g.hash=zero_hash.c_str();}
        verify(false);demand(install(edits,count,true,mutated),"all synthetic table slots installed");verify(true);
        demand(spool.open(session)&&prepare_emergency()&&write_new(session/L"operator-stop.flag","RUN\n"),"real worker spool and emergency page open");
        if(scenario=="before-ready-stop"){spool.stop();write_new(session/L"STOP","STOP\n");}
        HANDLE h=CreateThread(nullptr,0,worker,nullptr,0,nullptr);demand(h!=nullptr,"real plugin worker start");
        while(!fs::exists(session/L"ready.json")&&!fs::exists(session/L"failure.json")&&!fs::exists(session/L"retired.json"))Sleep(10);
        demand(scenario=="before-ready-stop"?!fs::exists(session/L"ready.json"):fs::exists(session/L"ready.json"),"real READY or pre-READY STOP");
        if(scenario=="normal"){
            demand(write_new(session/L"control-0123456789abcdef0123456789abcdef.request","ACK\n"),"fresh ACK request");while(!fs::is_regular_file(session/L"ack-0123456789abcdef0123456789abcdef.json"))Sleep(10);demand(true,"real worker fresh nonce ACK");
        }
        if(scenario=="disk-failure"){fixture_disk_query_failure=true;}
        else if(scenario=="terminal-failure"){fs::create_directory(session/L"retired.json");write_new(session/L"STOP","STOP\n");}
        else if(scenario=="guard-failure"){unsigned char bad=0;DWORD old{};VirtualProtect(memory,4096,PAGE_READWRITE,&old);memcpy(memory,&bad,1);VirtualProtect(memory,4096,old,&old);}
        else if(scenario=="writer-failure"){CloseHandle(spool.raw);spool.raw=INVALID_HANDLE_VALUE;preview::Invocation s(1,preview::queue,0,0,0,0);s.send(before,0);s.finish(false,0);}
        else if(scenario=="pending-stop"){
            preview::Invocation s(1,preview::queue,0,0,0,0);s.send(before,0);write_new(session/L"STOP","STOP\n");while(!spool.stopping)Sleep(10);demand(spool.active==1&&WaitForSingleObject(h,0)==WAIT_TIMEOUT,"worker waits for pending native invocation");s.finish(false,0);
        }else if(scenario!="before-ready-stop")write_new(session/L"STOP","STOP\n");
        WaitForSingleObject(h,INFINITE);CloseHandle(h);
        bool failed=scenario=="guard-failure"||scenario=="writer-failure"||scenario=="disk-failure"||scenario=="terminal-failure";
        if(failed){std::string page;demand(read_small(session/L"emergency-status.json",page,4096)&&page.find("\"error\":\"\"")==std::string::npos&&page.find("\"error\":")!=std::string::npos,"durable preallocated failure page");}
        else demand(fs::is_regular_file(session/L"retired.json"),"accurate retirement receipt");
        demand(spool.raw==INVALID_HANDLE_VALUE&&spool.active==0,"worker closed only after pending calls");
        if(!failed){verify(true);demand(true,"resident patches retained after STOP");}
        demand(install(nullptr,0,false,mutated)==false,"running-thread admission refuses edits");
        return 0;
    }catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
