// SPDX-License-Identifier: GPL-3.0-or-later
#define NOMINMAX
#include <windows.h>
#include "../resource-tungsten-acquisition/ancestry.h"
#include <thread>
#include <string>
#include <cmath>
#include <vector>
static void* fixture_allocate(void* at,SIZE_T size,DWORD type,DWORD protect){
    MEMORY_BASIC_INFORMATION m{};if(at&&VirtualQuery(at,&m,sizeof m)&&m.State==MEM_COMMIT)return at;
    return VirtualAlloc(at,size,type,protect);
}
static void* linked_source=nullptr;static unsigned char* linked_output=nullptr;static void* linked_resource=nullptr;
void set_population(void* source,void* output,void* resource){linked_source=source;linked_output=static_cast<unsigned char*>(output);linked_resource=resource;}
static DWORD WINAPI terminal_worker(void*){Sleep(INFINITE);return 0;}
extern "C" void con_diagnostic_run(void*,void*,void*,uint64_t);
extern "C" void con_fixture_run(void*,void*,void*,void*);
template<class T>void put(unsigned char* p,size_t at,T v){memcpy(p+at,&v,sizeof v);}
struct Packet{void* resource;void* region;void* slot;void* procgen;Packet* nested;uint32_t reserved=0;uint32_t flags=0;Packet* next=nullptr;uint64_t ordinal=0;};
extern "C" void con_fixture_next(Packet* p){
    if(p->flags&8)put<uint32_t>(static_cast<unsigned char*>(p->resource),0x24,0xdeadbeef);
    if(p->flags&4){
        auto slot=static_cast<unsigned char*>(p->slot);
        auto next=p->next;
        auto source=static_cast<unsigned char*>(next->slot);
        memcpy(slot,source,8);memcpy(slot-8,source-8,8);
        next->slot=p->slot;
    }
}
static void* reference;static void* operation;static void* payload;
extern "C" void con_fixture_nested(Packet* p){if(p->nested){if(p->reserved==2){std::thread child([&]{con_fixture_run(reference,operation,payload,p->nested);});child.join();}else con_fixture_run(reference,operation,payload,p->nested);}}
extern "C" void con_fixture_insert(retail::Header* h,uint64_t p){
    for(auto at=h->begin;at<h->end;at+=8)if(*reinterpret_cast<uint64_t*>(at)==p)return;
    if(h->end>=h->capacity)RaiseException(0xe0c1e099,0,0,nullptr);
    *reinterpret_cast<uint64_t*>(h->end)=p;h->end+=8;
}
// Independent fixture geometry, not a retail implementation/oracle. It executes
// disk and consecutive segment branches using actual target-owned words. Its
// segment/disk union is intentionally narrower than retail tapered/height logic.
extern "C" int con_fixture_skip(Packet* p,const unsigned char* closure){
    auto h=retail::field<const retail::Header*>(closure,8);
    for(auto at=h->begin;at<h->end;at+=8)if(*reinterpret_cast<void**>(at)==p->resource)return 1;
    return 0;
}
extern "C" int con_fixture_decide(Packet* p,const unsigned char* closure){
    auto r=static_cast<unsigned char*>(p->region);
    auto d=retail::field<const float*>(closure,0);
    float radius=retail::field<float>(closure,16);
    float x=retail::field<float>(r,0)-d[0],y=retail::field<float>(r,4)-d[1];
    float bound=retail::field<float>(r,12)+radius;
    if(x*x+y*y>bound*bound)return 0;
    auto n=retail::field<uint32_t>(r,24),cap=retail::field<uint32_t>(r,28);
    if(!n || n>cap || cap>4096)return 0;
    if(n==1)return 1;
    auto points=retail::field<const float*>(r,32);
    for(uint32_t j=1;j<n;++j){
        auto a=points+4*(j-1),b=points+4*j;
        double dx=b[0]-a[0],dy=b[1]-a[1],len=dx*dx+dy*dy;
        double t=len?((d[0]-a[0])*dx+(d[1]-a[1])*dy)/len:0;
        t=std::max(0.0,std::min(1.0,t));
        double qx=d[0]-(a[0]+t*dx),qy=d[1]-(a[1]+t*dy);
        double rr=radius+std::max(a[3],b[3]);
        if(qx*qx+qy*qy<=rr*rr)return 1;
    }
    return 0;
}
int consumer_main(int argc,char** argv){
    if(argc!=3)return 2;
    HANDLE gate=OpenEventA(SYNCHRONIZE,FALSE,argv[2]);if(!gate)return 4;
    auto ready_name=std::string(argv[2])+"-ready";
    HANDLE ready=OpenEventA(EVENT_MODIFY_STATE,FALSE,ready_name.c_str());
    if(!ready||!SetEvent(ready))return 7;CloseHandle(ready);
    if(WaitForSingleObject(gate,INFINITE)!=WAIT_OBJECT_0)return 5;CloseHandle(gate);
    uint64_t base=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));
    auto page=static_cast<unsigned char*>(fixture_allocate(reinterpret_cast<void*>(base+0x5f50000),0x10000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
    auto sf=static_cast<unsigned char*>(fixture_allocate(reinterpret_cast<void*>(base+0x5e80000),0x10000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
    if(!page||!sf)return 3;
    auto op=page+0xd2e0;operation=op;
    unsigned char cell[0x118]{};
    unsigned char ref[0xd0]{},def[48]{},extra[0xa0]{},list[32]{},il[0x38]{},cu[0x38]{};
    reference=ref;
    put<uint8_t>(cell,0x2e,0x49);put<uint32_t>(cell,0x28,0xff123456);
    put<uint64_t>(ref,0xb0,reinterpret_cast<uint64_t>(cell));
    put<uint8_t>(ref,0x2e,0x4a);put<uint64_t>(ref,0x98,reinterpret_cast<uint64_t>(def));
    put<uint64_t>(ref,0xc8,reinterpret_cast<uint64_t>(list));put<uint64_t>(list,8,reinterpret_cast<uint64_t>(extra));
    put<uint32_t>(def,0x28,0x2c60e9);put<uint8_t>(def,0x2e,0x1e);
    put<uint64_t>(extra,0,base+0x4c24e60);put<uint8_t>(extra,0x12,0xbc);put<uint64_t>(extra,0x98,0xb6c1e2dec207e2b0ULL);
    put<uint64_t>(op,0x268,reinterpret_cast<uint64_t>(extra));
    put<uint32_t>(op,0x344,0xffffffffU);
    put<uint32_t>(il,0x28,0x57d4);put<uint8_t>(il,0x2e,0x9f);
    put<uint32_t>(cu,0x28,0x57d5);put<uint8_t>(cu,0x2e,0x9f);
    uint64_t members[]={reinterpret_cast<uint64_t>(il),reinterpret_cast<uint64_t>(cu)};
    retail::Header transfer{reinterpret_cast<uint64_t>(members),reinterpret_cast<uint64_t>(members+2),reinterpret_cast<uint64_t>(members+2)};payload=&transfer;
    unsigned char file[0x370]{},entry[16]{};
    uint64_t fp=reinterpret_cast<uint64_t>(file),ep=reinterpret_cast<uint64_t>(entry);
    put<uint32_t>(sf,0x81e8,1);put<uint64_t>(sf,0x81f0,reinterpret_cast<uint64_t>(&ep));
    put<uint64_t>(entry,0,reinterpret_cast<uint64_t>(&fp));put<int32_t>(entry,8,1);
    put<uint64_t>(file,0,base+0x4b29b80);memcpy(file+0x38,"Starfield.esm",14);memcpy(file+0x268,"Data",5);
    float points[][4]={{10,20,0,3},{30,40,0,5},{50,60,0,7}};
    std::vector<float> large(4096*4,1.0f);
    unsigned char regions[2][48]{},collection[24]{},resources[24]{},source[48]{},sources[48]{},procgen[48]{};
    unsigned char resources2[24]{},source2[48]{};
    unsigned char geographic[0x70]{},geographic2[0x70]{},manager[0x200]{};
    auto global=static_cast<unsigned char*>(fixture_allocate(reinterpret_cast<void*>(base+0x5fd0000),0x10000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
    if(!global)return 9;
    put<uint64_t>(global,0x9c30,reinterpret_cast<uint64_t>(manager));
    put<uint64_t>(manager,0x130,reinterpret_cast<uint64_t>(procgen));
    put<uint32_t>(manager,0x80,0x5e0de);
    for(auto at:{0xc8,0x1c0}){put<int32_t>(manager,at+4,195);put<int32_t>(manager,at+8,109);put<int32_t>(manager,at+0x14,8);}
    put<uint32_t>(geographic,0,0x29d20e);put<int32_t>(geographic,0x10,0);put<int32_t>(geographic,0x14,0);
    put<int32_t>(geographic,0x18,10);put<int32_t>(geographic,0x1c,10);
    put<int32_t>(geographic,0x20,2);put<int32_t>(geographic,0x24,2);
    put<int32_t>(geographic,0x28,14);put<int32_t>(geographic,0x2c,14);
    put<uint64_t>(geographic,0x68,0x12345678);
    memcpy(geographic2,geographic,sizeof geographic);put<int32_t>(geographic2,0x10,0);
    for(auto& r:regions){put<float>(r,0,10);put<float>(r,4,20);put<float>(r,12,3);
        put<uint32_t>(r,0x18,1);put<uint32_t>(r,0x1c,3);put<uint64_t>(r,0x20,reinterpret_cast<uint64_t>(points));}
    put<uint32_t>(collection,8,2);put<uint32_t>(collection,12,2);put<uint64_t>(collection,16,reinterpret_cast<uint64_t>(regions));
    put<uint32_t>(resources,0,0x57d4);put<uint64_t>(resources,8,reinterpret_cast<uint64_t>(collection));
    put<uint64_t>(source,0x20,reinterpret_cast<uint64_t>(resources));put<uint64_t>(source,0x28,1);
    put<uint64_t>(sources,0,reinterpret_cast<uint64_t>(geographic));put<uint64_t>(sources,8,reinterpret_cast<uint64_t>(source));
    put<uint64_t>(procgen,0x20,reinterpret_cast<uint64_t>(sources));put<uint64_t>(procgen,0x28,1);
    Packet p{il,regions[0],sources+8,procgen,nullptr,1},inner=p;
    std::string mode=argv[1];
    if(mode=="no-hit")return 0;
    if(mode=="context-partial")put<uint64_t>(sources,0,8);
    if(mode=="context-owner")put<uint64_t>(manager,0x130,8);
    if(mode=="wrong-cell")put<uint32_t>(cell,0x48,1);
    if(mode=="generic-resource"){put<uint32_t>(il,0x28,0x123456);put<uint32_t>(resources,0,0x123456);}
    if(mode=="rothicite"){put<uint32_t>(il,0x28,0x5df1);put<uint32_t>(resources,0,0x5df1);}
    if(mode=="partial-page"){
        auto m=static_cast<unsigned char*>(fixture_allocate(nullptr,8192,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
        DWORD old;VirtualProtect(m+4096,4096,PAGE_NOACCESS,&old);
        put<uint64_t>(regions[0],0x20,reinterpret_cast<uint64_t>(m+4088));
    }
    if(mode=="short-circuit")p.next=&inner;
    if(mode=="multi")put<uint32_t>(regions[0],0x18,3);
    if(mode=="multi-reject"){
        put<uint32_t>(regions[0],0x18,3);put<float>(regions[0],12,1000);
        for(auto& point:points){point[0]+=500;point[1]+=500;}
    }
    if(mode=="byte-budget")put<uint32_t>(regions[0],0x18,3);
    if(mode=="maximum"){put<uint32_t>(regions[0],0x18,4096);put<uint32_t>(regions[0],0x1c,4096);put<uint64_t>(regions[0],0x20,reinterpret_cast<uint64_t>(large.data()));}
    if(mode=="reject")put<float>(regions[0],0,10000);
    if(mode=="indexed-query"){p.flags=32;put<uint32_t>(op,0x344,0);}
    if(mode=="empty-transfer")p.flags=16;
    if(mode=="pointer-reuse")p.flags=8;
    if(mode=="wrong-body")put<uint32_t>(manager,0x80,1);
    if(mode=="unrelated-source")put<uint64_t>(sources,8,reinterpret_cast<uint64_t>(source2));
    if(mode=="new-thread"){p.nested=&inner;p.reserved=2;}
    if(mode=="nonfinite")points[0][3]=NAN;
    if(mode=="chlorine-only"){p.resource=cu;put<uint32_t>(resources,0,0x57d5);}
    if(mode=="wrong-workshop")put<uint64_t>(extra,0x98,1);
    if(mode=="wrong-source")put<uint32_t>(sources,16,0xffffffffU);
    if(mode=="invalid-source")put<uint64_t>(sources,8,8);
    if(mode=="source-budget")put<uint64_t>(procgen,0x28,4097);
    if(mode=="empty-collection")put<uint32_t>(collection,8,0);
    if(mode=="corrupt-collection")put<uint32_t>(collection,8,3);
    if(mode=="invalid-collection")put<uint64_t>(resources,8,8);
    if(mode=="wrong-resource")put<uint32_t>(resources,0,0x57d5);
    if(mode=="alkanes"){p.resource=cu;put<uint32_t>(resources,0,0x57d5);}
    if(mode=="wrong-caller")p.flags=1;
    if(mode=="stale-transfer")p.flags=2;
    if(mode=="outside-region")p.region=regions[1]+16;
    if(mode=="empty")put<uint32_t>(regions[0],0x18,0);
    if(mode=="partial")put<uint64_t>(regions[0],0x20,0x10000);
    if(mode=="corrupt")put<uint32_t>(regions[0],0x18,4);
    if(mode=="oversized")put<uint32_t>(regions[0],0x1c,0xffffffffU);
    if(mode=="nested"){p.nested=&inner;inner.region=regions[1];put<float>(regions[1],0,10000);}
    if(mode=="mixed"){put<float>(regions[0],0,10000);p.next=&inner;inner.region=regions[1];}
    if(mode=="sources"||mode=="source-reuse"){
        memcpy(resources2,resources,24);put<uint32_t>(resources2,0,0x57d5);
        put<uint64_t>(source2,0x20,reinterpret_cast<uint64_t>(resources2));put<uint64_t>(source2,0x28,1);
        put<uint64_t>(sources,24,reinterpret_cast<uint64_t>(geographic2));put<uint64_t>(sources,32,reinterpret_cast<uint64_t>(source2));put<uint64_t>(procgen,0x28,2);
        p.next=&inner;inner.resource=cu;inner.region=regions[1];inner.slot=sources+32;inner.ordinal=1;
        if(mode=="source-reuse"){p.flags=4;inner.ordinal=0;}
    }
    if(mode=="invalid-procgen")p.procgen=reinterpret_cast<void*>(8);
    if(mode=="crash-before")RaiseException(0xe0c1e000,0,0,nullptr);
    if(mode=="unrelated-first")con_diagnostic_run(geographic,geographic+0x10,geographic,0x5e0de);
    if(linked_output){
        put<uint64_t>(sources,0,reinterpret_cast<uint64_t>(linked_source));
        put<uint64_t>(sources,8,reinterpret_cast<uint64_t>(linked_output));
        p.resource=linked_resource;p.region=reinterpret_cast<void*>(retail::field<uint64_t>(linked_output,0x58));
    }
    auto run=[&]{con_fixture_run(ref,op,&transfer,&p);};
    // D4B: retain several real native threads until debugger disposal, so STOP
    // must drain EXIT_THREAD before EXIT_PROCESS after transfer retirement.
    bool teardown=mode=="stop-threads"||mode=="stop-many"||mode=="terminate-failure"||mode=="continue-failure"||
        mode=="duplicate-continue"||mode=="pending-stop";
    if(teardown){for(int i=0;i<(mode=="stop-many"?96:3);++i){
        HANDLE worker=CreateThread(nullptr,0,terminal_worker,nullptr,0,nullptr);
        if(!worker)return 11;CloseHandle(worker);
    }}
    if(mode=="pending-stop"){
        std::thread worker(run);worker.join();Sleep(INFINITE);
    }
    if(mode=="threads"){for(int i=0;i<3;++i){std::thread t(run);t.join();points[0][0]=float(100+i);}}
    else if(mode=="stack-reuse"){run();run();}
    else if(mode=="contention"){std::thread a(run),b(run);a.join();b.join();}
    else run();
    if(mode=="crash-after")RaiseException(0xe0c1e001,0,0,nullptr);
    return 0;
}
