// SPDX-License-Identifier: GPL-3.0-or-later
// Original D5L disposable target. These fields are not retail engine members.
#include <windows.h>
#include <cstdint>
#include <map>
#include <mutex>
#include <thread>
#include <vector>
#include <string>
#include <set>
#include <barrier>
#include <memory>
struct Population { uint64_t count=0; float points[8]{}; };
struct Slot {uint64_t source;Population* wrapper;uint32_t occupied=0,padding=0;};
struct Packet {
    uint64_t magic=0x44354c5041434b31,manager=0,source=0,wrapper=0,slot=0;
    int32_t query[2]={37536,20928}; uint32_t mask=0,branch=0;
};
#define PROBE(n) extern "C" __declspec(noinline) void n(Packet* p){volatile auto v=p;(void)v;}
PROBE(owner_init) PROBE(source_init) PROBE(provider_entry) PROBE(visited)
PROBE(lookup) PROBE(inserted) PROBE(query) PROBE(mask) PROBE(completed)
PROBE(owner_reset) PROBE(owner_destroy) PROBE(provider_exit)
static std::recursive_mutex lock;
static int owner,source;
static std::map<uint64_t,Slot> populations;
static std::set<uint64_t> seen;
static std::vector<std::unique_ptr<Population>> allocations;
static void clear(){populations.clear();seen.clear();allocations.clear();}
static void request(Packet p,bool fail=false,bool nested=false,std::barrier<>* race=nullptr){
    provider_entry(&p);
    {std::lock_guard<std::recursive_mutex> hold(lock);p.branch=seen.count(p.source)?2:0;}
    visited(&p);
    if(race)race->arrive_and_wait();
    if(p.branch!=2){
        std::lock_guard<std::recursive_mutex> hold(lock);
        auto found=populations.find(p.source);p.branch=found==populations.end()?0:1;
        p.wrapper=found==populations.end()?0:reinterpret_cast<uint64_t>(found->second.wrapper);
        p.slot=found==populations.end()?0:reinterpret_cast<uint64_t>(&found->second);lookup(&p);
        if(p.branch==0){
            allocations.push_back(std::make_unique<Population>());auto& value=*allocations.back();
            auto& slot=populations.emplace(p.source,Slot{p.source,&value}).first->second;
            p.wrapper=reinterpret_cast<uint64_t>(&value);p.slot=reinterpret_cast<uint64_t>(&slot);
            inserted(&p);query(&p);
            if(nested){auto q=p;q.source+=64;q.query[0]+=1;source_init(&q);request(q);}
            mask(&p);
            for(int i=0;i<(fail?4:8);++i)value.points[i]=float(i+p.mask);
            value.count=fail?1:2;
            completed(&p);
            seen.insert(p.source);
        }
    }
    provider_exit(&p);
}
static void pair(Packet p){std::barrier race(2);std::thread a([&]{request(p,false,false,&race);});
    std::thread b([&]{request(p,false,false,&race);});a.join();b.join();request(p);}
int wmain(int argc,wchar_t** argv){
    if(argc!=3)return 3;
    auto gate=OpenEventW(SYNCHRONIZE,FALSE,argv[2]);
    auto ready=OpenEventW(EVENT_MODIFY_STATE,FALSE,(std::wstring(argv[2])+L"-ready").c_str());
    if(!gate||!ready)return 4;SetEvent(ready);CloseHandle(ready);
    if(WaitForSingleObject(gate,15000)!=WAIT_OBJECT_0)return 5;CloseHandle(gate);
    std::wstring mode=argv[1];Packet p;p.manager=reinterpret_cast<uint64_t>(&owner);p.source=reinterpret_cast<uint64_t>(&source);
    owner_init(&p);source_init(&p);
    if(mode==L"idle"){Sleep(INFINITE);return 0;}
    pair(p);
    if(mode==L"reuse"||mode==L"reset"||mode==L"owner-aba"){
        if(mode==L"owner-aba"){owner_destroy(&p);owner_init(&p);}
        else if(mode==L"reset")owner_reset(&p);else source_init(&p);
        clear();p.mask=3;pair(p);
    }else if(mode==L"failed"){
        owner_reset(&p);clear();request(p,true);request(p);
    }else if(mode==L"nested"){
        owner_reset(&p);clear();request(p,false,true);request(p);
    }else if(mode==L"concurrent"){
        std::vector<std::thread> workers;
        for(int t=0;t<4;++t)workers.emplace_back([=]{for(int n=0;n<3;++n){auto q=p;
            if(n%3){q.source+=0x1000+t*256+n*8;source_init(&q);}
            request(q);}});
        for(auto& w:workers)w.join();request(p);
    }else if(mode==L"crash"){RaiseException(0xe0d51001,0,0,nullptr);
    }else if(mode==L"invalid"){completed(reinterpret_cast<Packet*>(1));}
    owner_destroy(&p);clear();return 0;
}
