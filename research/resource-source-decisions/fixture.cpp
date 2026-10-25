// SPDX-License-Identifier: GPL-3.0-or-later
// Original disposable D5E oracle. Epoch fields are fixture-only witnesses.
#include <windows.h>
#include <cstdint>
#include <string>
#include <vector>
#include <thread>
#include <mutex>
#include <map>
#include <array>
#include <memory>
struct Packet {
    uint64_t magic=0x4435455041434b31, manager=1, source=0x1000, manager_epoch=1, source_epoch=1;
    uint64_t invocation=0, parent=0, visited_key=77, wrapper=0, lookup=0, capacity=8;
    int32_t query[2]={37536,20928};
    uint32_t mask=0, branch=0, inserted=0, complete=1, geo=1, ready=0;
};
extern "C" __declspec(noinline) void decision_visited(Packet* p){ volatile auto v=p; (void)v; }
extern "C" __declspec(noinline) void decision_lookup(Packet* p){ volatile auto v=p; (void)v; }
extern "C" __declspec(noinline) void decision_mask(Packet* p){ volatile auto v=p; (void)v; }
extern "C" __declspec(noinline) void decision_terminal(Packet* p){ volatile auto v=p; (void)v; }
static std::mutex gate;
struct Population {int32_t query[2];uint32_t mask;bool complete;};
static std::map<std::array<uint64_t,4>,std::unique_ptr<Population>> retained;
static void request(Packet p, unsigned branch=0, bool nested=false){
    decision_visited(&p);
    if(p.branch==2)return;
    std::lock_guard<std::mutex> lock(gate);
    auto key=std::array<uint64_t,4>{p.manager,p.manager_epoch,p.source,p.source_epoch};
    // Explicit synthetic branch control supplies a retained entry when needed.
    // The actual lookup, allocation and insertion below run in target memory.
    if(branch==1&&!retained.count(key))retained[key]=std::make_unique<Population>(Population{{1,2},15,false});
    if(branch==0)retained.erase(key);
    auto found=retained.find(key);
    p.branch=found==retained.end()?0:1; p.lookup=p.branch==1?0:p.capacity;
    p.wrapper=p.branch==1?reinterpret_cast<uint64_t>(found->second.get()):0;
    decision_lookup(&p);
    if(p.branch==0){
        bool fail_insert=p.inserted==99;
        auto population=std::make_unique<Population>(Population{{p.query[0],p.query[1]},p.mask,false});
        p.wrapper=fail_insert?0:reinterpret_cast<uint64_t>(population.get());p.inserted=fail_insert?0:1;
        if(!fail_insert)retained.emplace(key,std::move(population));
        if(nested){auto child=p; child.invocation+=100000; child.parent=p.invocation; child.source+=32;
            // Nested probe sequence has independent identity; no recursive lock.
            decision_visited(&child); child.lookup=0; child.branch=1; decision_lookup(&child); decision_terminal(&child);}
        decision_mask(&p);
        if(!fail_insert){retained.at(key)->complete=bool(p.complete);p.ready=retained.at(key)->complete;}
    }
    decision_terminal(&p);
}
int wmain(int argc,wchar_t** argv){
    if(argc!=3)return 3;
    auto event=OpenEventW(SYNCHRONIZE,FALSE,argv[2]); if(!event)return 4;
    auto ready=OpenEventW(EVENT_MODIFY_STATE,FALSE,(std::wstring(argv[2])+L"-ready").c_str());
    if(!ready)return 6;SetEvent(ready);CloseHandle(ready);
    if(WaitForSingleObject(event,10000)!=WAIT_OBJECT_0)return 5; CloseHandle(event);
    std::wstring mode=argv[1]; Packet p;
    if(mode==L"idle"){Sleep(INFINITE);return 0;}
    p.invocation=1; request(p); p.invocation=2; request(p,1); p.invocation=3;p.branch=2; request(p);
    p.branch=0;
    if(mode==L"reuse" || mode==L"reset" || mode==L"replacement"){
        if(mode==L"reset")p.manager_epoch=2;
        else if(mode==L"replacement")p.manager=2;
        else p.source_epoch=2;
        p.invocation=4;p.mask=3;request(p);
    }else if(mode==L"interleave" || mode==L"threads"){
        std::vector<std::thread> workers;
        for(unsigned t=0;t<4;++t)workers.emplace_back([=]{for(unsigned n=0;n<80;++n){auto q=p;
            q.invocation=1000+t*100+n;q.geo=n%8==0;
            if(!q.geo)q.source+=0x100+t*1024+n*8;
            request(q,q.geo?1:n%3==0?0:1,n%11==0);}});
        for(auto& w:workers)w.join();
        p.invocation=4;request(p,1);
    }else if(mode==L"nested"){p.invocation=4;request(p,0,true);
    }else if(mode==L"partial"){p.invocation=4;p.complete=0;request(p);
    }else if(mode==L"failed-insert"){p.invocation=4;p.inserted=99;request(p);
    }else if(mode==L"stale"){p.invocation=4;p.source_epoch=0;request(p);
    }else if(mode==L"misleading"){p.invocation=4;p.geo=0;request(p);
    }else if(mode==L"invalid"){decision_lookup(reinterpret_cast<Packet*>(1));
    }else if(mode==L"crash"){RaiseException(0xe0d5e001,0,0,nullptr);
    }else if(mode==L"bypass-incomplete"){p.invocation=4;p.branch=2;p.ready=0;request(p);
    }else if(mode==L"hit-unknown"){p.invocation=4;p.ready=0;request(p,1);}
    return 0;
}
