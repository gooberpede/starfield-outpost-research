// SPDX-License-Identifier: GPL-3.0-or-later
// Original native-shaped disposable memory, not a retail generator implementation.
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <cstddef>
#include <array>
#include <vector>
#include <thread>
#include <mutex>
#include <barrier>
#include <string>
#include <set>
struct Region {float bounds[4]{};uint32_t tag=0;uint8_t kind=0,pad[3]{};uint32_t count=0,capacity=0;float* points=nullptr;uint64_t padding=0;};
static_assert(sizeof(Region)==48&&offsetof(Region,count)==0x18);
struct Collection {uint64_t refcount=1;uint32_t count=0,capacity=4;Region* data=nullptr;};
struct Slot {uint64_t key=0,holder=0;uint32_t next=0xffffffff,pad=0;};
template<size_t N>struct Raw {std::array<unsigned char,N> b{};template<class T>void put(size_t at,T value){memcpy(b.data()+at,&value,sizeof value);}};
struct State;struct Bundle;
struct Env {
    void* procgen;void* source;void* grid;int32_t* query;void* descriptor;void* geographic;
    uint32_t mask=0,branch=0;uint64_t lookup=0,wrapper=0,collection=0,resource=0x57d4;
    uint32_t flags=0,pass=0;State* state=nullptr;std::barrier<>* race=nullptr;bool nested=false;
    Bundle* bundle=nullptr;
    HANDLE first_done=nullptr;bool await_first=false;
};
static_assert(offsetof(Env,flags)==88&&offsetof(Env,collection)==72);
extern "C" void native_execute(Env*);
extern "C" void fixture_init(void*);
extern "C" void fixture_reset(void*);
extern "C" void native_source_retire(void*);
extern "C" void fixture_grid_init(void*);
extern "C" void native_destroy(void*);
extern "C" void native_grid_clear(void*);
extern "C" void fixture_source_init(void*,void*,void*);
extern "C" void native_erase(void*,uint64_t);
extern "C" __declspec(dllexport) uint64_t native_singleton=0;
extern "C" __declspec(dllexport) uint64_t native_grid_table[9]{};
extern "C" __declspec(dllexport) uint64_t native_procgen_table[6]{};
extern "C" __declspec(dllexport) uint64_t fixture_reset_phase=0;
extern "C" __declspec(dllexport) DWORD WINAPI fixture_thread_start(void*){return 0;}
extern "C" void fixture_handled_exception(){__try{RaiseException(0xe0d51003,0,0,nullptr);}__except(EXCEPTION_EXECUTE_HANDLER){}}
struct Source :Raw<0x1a0>{};
struct Bundle {
    Raw<0x40> wrapper;std::array<Slot,8> resource_slots;std::array<Region,4> regions{};Collection collection;
    std::array<std::array<float,8>,4> copied{};float input[8]{};
    Bundle(){wrapper.put<uint64_t>(0x20,reinterpret_cast<uint64_t>(resource_slots.data()));wrapper.put<uint64_t>(0x28,8);wrapper.put<uint32_t>(0,1);
        collection.data=regions.data();resource_slots[2]={0x57d4,reinterpret_cast<uint64_t>(&collection),8,0};}
};
struct State {
    Raw<0x200> manager;Raw<0x138> procgen;Raw<0x70> grid;Raw<0x20> root;
    Source source;std::array<Source,4> extras;Raw<0x50> definition;std::array<Slot,32> source_slots;
    std::array<uint64_t,16> sources{};Bundle primary;std::array<Bundle,4> extra_bundles;
    unsigned char geographic[24]{};int32_t query[2]={4,-1};
    std::recursive_mutex mutex;std::set<uint64_t> seen;
    State(){
        native_singleton=reinterpret_cast<uint64_t>(manager.b.data());
        grid.put<uint64_t>(0,reinterpret_cast<uint64_t>(native_grid_table));procgen.put<uint64_t>(0,reinterpret_cast<uint64_t>(native_procgen_table));
        manager.put<uint64_t>(0x130,reinterpret_cast<uint64_t>(procgen.b.data()));
        manager.put<uint64_t>(0x120,reinterpret_cast<uint64_t>(root.b.data()));
        manager.put<uint32_t>(0x80,0x5e0de);
        manager.put<int32_t>(0xcc,195);manager.put<int32_t>(0xd0,109);manager.put<int32_t>(0xdc,8);
        root.put<uint64_t>(0x10,reinterpret_cast<uint64_t>(grid.b.data()));
        procgen.put<uint64_t>(0x20,reinterpret_cast<uint64_t>(source_slots.data()));procgen.put<uint64_t>(0x28,32);
        source.put<uint32_t>(0,0x29d20e);source.put<uint64_t>(0x68,77);
        sources[0]=reinterpret_cast<uint64_t>(source.b.data());grid.put<uint32_t>(0x10,1);grid.put<uint32_t>(0x14,16);grid.put<uint64_t>(0x18,reinterpret_cast<uint64_t>(sources.data()));
        for(unsigned i=0;i<4;++i){extras[i].put<uint32_t>(0,0x29d20e);extras[i].put<int32_t>(0x10,12*(i+1));extras[i].put<uint64_t>(0x68,78+i);sources[i+1]=reinterpret_cast<uint64_t>(extras[i].b.data());}
        grid.put<uint32_t>(0x10,5);
    }
    Env env(){Env p={procgen.b.data(),source.b.data(),grid.b.data(),query,manager.b.data()+0xc8,geographic,0,0,0,
        reinterpret_cast<uint64_t>(primary.wrapper.b.data()),reinterpret_cast<uint64_t>(&primary.collection),0x57d4,0,0,this};p.bundle=&primary;return p;}
    void clear(){for(auto& s:source_slots)s=Slot{};primary.collection.count=0;for(auto& b:extra_bundles)b.collection.count=0;seen.clear();}
    void clear_grid(){native_grid_clear(grid.b.data());for(unsigned i=0;i<32;++i)if(source_slots[i].next!=0xffffffff){native_erase(procgen.b.data()+0x10,i);source_slots[i]=Slot{};}clear();}
    void recreate_procgen(){procgen.~Raw<0x138>();new(&procgen)Raw<0x138>();procgen.put<uint64_t>(0,reinterpret_cast<uint64_t>(native_procgen_table));procgen.put<uint64_t>(0x20,reinterpret_cast<uint64_t>(source_slots.data()));procgen.put<uint64_t>(0x28,32);}
    void recreate_grid(){grid.~Raw<0x70>();new(&grid)Raw<0x70>();grid.put<uint64_t>(0,reinterpret_cast<uint64_t>(native_grid_table));grid.put<uint32_t>(0x10,5);grid.put<uint32_t>(0x14,16);grid.put<uint64_t>(0x18,reinterpret_cast<uint64_t>(sources.data()));}
};
extern "C" uint64_t fixture_native_visit(Env* p){
    uint64_t key=0;memcpy(&key,static_cast<unsigned char*>(p->source)+0x68,8);
    bool seen;{std::lock_guard<std::recursive_mutex> h(p->state->mutex);seen=p->state->seen.count(key)!=0;}
    if(p->race)p->race->arrive_and_wait();
    if(p->await_first&&WaitForSingleObject(p->first_done,15000)!=WAIT_OBJECT_0)RaiseException(0xe0d51004,0,0,nullptr);
    p->branch=seen?1:0;return p->branch;
}
extern "C" uint64_t fixture_native_lookup(Env* p){
    auto& s=*p->state;s.mutex.lock();p->lookup=32;
    for(unsigned i=0;i<32;++i)if(s.source_slots[i].next!=0xffffffff&&s.source_slots[i].key==reinterpret_cast<uint64_t>(p->source)){p->lookup=i;break;}
    return p->lookup;
}
extern "C" void fixture_native_insert(Env* p){auto& s=*p->state;for(unsigned i=0;i<32;++i)if(s.source_slots[i].next==0xffffffff){s.source_slots[i]={reinterpret_cast<uint64_t>(p->source),p->wrapper,32,0};break;}p->bundle->collection.count=0;}
extern "C" void fixture_native_release(Env* p){uint64_t key=0;memcpy(&key,static_cast<unsigned char*>(p->source)+0x68,8);p->state->seen.insert(key);p->state->mutex.unlock();if(p->first_done&&!p->await_first)SetEvent(p->first_done);}
extern "C" uint32_t fixture_native_append(Env* p,Region* temporary){
    auto& s=*p->bundle;for(unsigned i=0;i<8;++i)s.input[i]=float(i+((p->flags&128)?0:p->mask)+p->pass*10);
    temporary->bounds[0]=1;temporary->bounds[1]=2;temporary->bounds[2]=3;temporary->bounds[3]=4;
    temporary->tag=9;temporary->kind=1;temporary->count=temporary->capacity=2;temporary->points=s.input;
    if((p->flags&1)||((p->flags&4)&&p->pass))return 0xffffffff;
    auto index=s.collection.count++;s.regions[index]=*temporary;memcpy(s.copied[index].data(),s.input,sizeof s.input);
    s.regions[index].points=s.copied[index].data();if(p->flags&2)s.regions[index].count=1;
    if(p->flags&16)s.regions[index].points=reinterpret_cast<float*>(1);
    if(p->flags&64)fixture_handled_exception();
    if(p->nested){auto child=*p;child.race=nullptr;child.nested=false;native_execute(&child);}
    return index;
}
static void pair(Env p){std::barrier race(2);p.race=&race;
    std::thread a([p]()mutable{native_execute(&p);});std::thread b([p]()mutable{native_execute(&p);});a.join();b.join();p.race=nullptr;native_execute(&p);}
static void pair_queries(Env p){std::barrier race(2);auto event=CreateEventW(nullptr,TRUE,FALSE,nullptr);
    int32_t first_query[2]={4,-1},later_query[2]={4,1};auto later=p;
    p.query=first_query;p.race=&race;p.first_done=event;
    later.query=later_query;later.mask=3;later.race=&race;later.first_done=event;later.await_first=true;
    std::thread a([p]()mutable{native_execute(&p);});std::thread b([later]()mutable{native_execute(&later);});a.join();b.join();CloseHandle(event);
    p.race=nullptr;p.first_done=nullptr;native_execute(&p);}
extern "C" __declspec(noinline) void fixture_reset_entry(){fixture_reset_phase=1;volatile int marker=1;(void)marker;}
int wmain(int argc,wchar_t** argv){
    if(argc!=3)return 3;auto gate=OpenEventW(SYNCHRONIZE,FALSE,argv[2]);
    auto ready=OpenEventW(EVENT_MODIFY_STATE,FALSE,(std::wstring(argv[2])+L"-ready").c_str());
    if(!gate||!ready)return 4;SetEvent(ready);CloseHandle(ready);if(WaitForSingleObject(gate,15000)!=WAIT_OBJECT_0)return 5;CloseHandle(gate);
    if(std::wstring(argv[1])==L"idle"){Sleep(INFINITE);return 0;}
    State state;auto p=state.env();fixture_init(p.procgen);fixture_grid_init(p.grid);fixture_source_init(p.source,p.grid,state.definition.b.data());
    std::wstring mode=argv[1];
    if(mode==L"alternate-frame"){state.manager.b[0x20]=3;memcpy(state.manager.b.data()+0x1c0,state.manager.b.data()+0xc8,0x2c);p.descriptor=state.manager.b.data()+0x1c0;}
    if(mode==L"reset-window")fixture_reset_entry();
    if(mode==L"nested")p.nested=true;
    if(mode==L"contrary"){p.mask=3;p.flags=128;}
    if(mode==L"failed"||mode==L"copy-failed"||mode==L"partial"||mode==L"prereq"||mode==L"bad-read"||mode==L"exception"){
        p.flags=mode==L"failed"?1:mode==L"copy-failed"?2:mode==L"partial"?4:mode==L"bad-read"?16:mode==L"exception"?64:8;pair(p);
    }else if(mode==L"query-change-hit")pair_queries(p);else pair(p);
    if(mode==L"reuse"||mode==L"reset"||mode==L"owner-aba"||mode==L"reset-window"||mode==L"destroy-window"||mode==L"grid-window"||mode==L"source-window"){
        if(mode==L"reuse"){
            state.clear_grid();state.recreate_grid();state.source.~Source();new(&state.source)Source();state.source.put<uint32_t>(0,0x29d20e);state.source.put<uint64_t>(0x68,77);
            fixture_grid_init(p.grid);fixture_source_init(p.source,p.grid,state.definition.b.data());
        }else if(mode==L"source-window"){
            native_source_retire(p.source);native_erase(static_cast<unsigned char*>(p.procgen)+0x10,0);state.clear();pair(p);state.clear();
            state.source.~Source();new(&state.source)Source();state.source.put<uint32_t>(0,0x29d20e);state.source.put<uint64_t>(0x68,77);
            fixture_source_init(p.source,p.grid,state.definition.b.data());
        }else if(mode==L"owner-aba"||mode==L"destroy-window"){
            native_destroy(p.procgen);state.clear();if(mode==L"destroy-window")pair(p);
            state.clear();state.recreate_procgen();fixture_init(p.procgen);
        }else if(mode==L"grid-window"){
            state.clear_grid();fixture_source_init(p.source,p.grid,state.definition.b.data());pair(p);state.clear();state.recreate_grid();fixture_grid_init(p.grid);
            state.source.~Source();new(&state.source)Source();state.source.put<uint32_t>(0,0x29d20e);state.source.put<uint64_t>(0x68,77);
            fixture_source_init(p.source,p.grid,state.definition.b.data());
        }else{std::lock_guard<std::recursive_mutex> h(state.mutex);state.clear();fixture_reset_phase=2;fixture_reset(p.procgen);}
        p.mask=3;state.query[1]=1;pair(p);
    }else if(mode==L"concurrent"){
        for(auto& s:state.extras)fixture_source_init(s.b.data(),p.grid,state.definition.b.data());
        std::vector<std::thread> workers;for(unsigned i=0;i<4;++i)workers.emplace_back([p,i]()mutable{
            int32_t query[2]={int32_t(4+12*(i+1)),-1};
            for(int n=0;n<3;++n){auto q=p;if(n%2){auto& b=q.state->extra_bundles[i];q.source=q.state->extras[i].b.data();q.query=query;q.bundle=&b;q.wrapper=reinterpret_cast<uint64_t>(b.wrapper.b.data());q.collection=reinterpret_cast<uint64_t>(&b.collection);}native_execute(&q);}
        });for(auto& w:workers)w.join();
    }
    if(mode==L"crash")RaiseException(0xe0d51002,0,0,nullptr);
    state.clear_grid();native_destroy(p.procgen);return 0;
}
