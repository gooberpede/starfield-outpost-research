// SPDX-License-Identifier: GPL-3.0-or-later
#include "capture.h"
#include <array>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <thread>

extern "C" void probe(void*,void*,unsigned long long);
namespace {
using namespace capture;
std::array<Record,64> records{};
std::atomic<unsigned> cursor{}, pool_losses{};
thread_local Group* pending{};
struct PendingScope {
    Group* previous;
    explicit PendingScope(Group* g):previous(pending) { pending=g; }
    ~PendingScope() { pending=previous; }
};
std::array<Point,max_points+1> large{};
Point single[]{ {999,999,999,0} };
Point strip[]{ {-5,0,20,2},{5,0,20,2} };
Point late[]{ {-10,-10,0,1},{10,-10,0,1},{10,10,0,1} };
void require(bool value) { if(!value) std::abort(); }
Record* reserve() {
    auto index=cursor.fetch_add(1);
    if(index>=records.size()) { ++pool_losses; overflow=true; return nullptr; }
    return &records[index];
}
Use operands(unsigned case_id,unsigned ordinal) {
    Use u{}; u.ordinal=ordinal; u.kind=ordinal; u.radius=1; u.upper=0;
    u.translation[0]=1024; u.translation[1]=-2048; u.translation[2]=32;
    if(case_id==2) u.resolved[0]=12;
    if(case_id==3) { u.resolved[2]=-900; u.radius=0; u.upper=-100; }
    if(case_id==4) { u.resolved[0]=5; u.resolved[1]=3; u.resolved[2]=-100; u.radius=2; u.upper=20; }
    if(case_id==5) { u.resolved[1]=3; u.resolved[2]=20; u.radius=1.1f; u.upper=-10; }
    if(case_id==6) { u.resolved[1]=8; u.resolved[2]=20; }
    if(case_id==8) { u.resolved[0]=10; u.resolved[1]=5; u.radius=0; }
    for(unsigned i=0;i<3;++i) u.indexed[i]=u.resolved[i]-u.translation[i];
    u.index=7; u.domain=0x123456789abcdef0;
    return u;
}
// Finite, fixed-rectangle arithmetic fixture, not resource/strip reconstruction.
// Each use snapshot is the actual local value immediately consumed below.
bool decision(unsigned case_id,Group& g,unsigned fault) {
    auto consume=[&](unsigned kind) {
        auto u=operands(case_id,g.r.h.uses); u.kind=kind;
        if(fault==5 && u.ordinal==1) u.resolved[0]+=1;
        if(fault==6 && u.ordinal==1) u.ordinal=99;
        g.use(u); return u;
    };
    auto broad=consume(1); auto q=broad.resolved;
    float dx=q[0],dy=q[1], reach=g.r.h.radius+broad.radius;
    if(dx*dx+dy*dy>reach*reach) return false;
    if(g.r.h.count==1) return true;
    if(g.r.h.count==0) return false;
    for(unsigned strip_index=0;strip_index<(case_id==8 ? 2u : 1u);++strip_index) {
        // Declared original fixture constants are part of the input contract.
        float quad[4][3]{{-5,2,20},{5,2,20},{5,-2,20},{-5,-2,20}};
        if(case_id==8) {
            float first[4][3]{{-10,-9,0},{10,-9,0},{10,-11,0},{-10,-11,0}};
            float second[4][3]{{9,-10,0},{9,10,0},{11,10,0},{11,-10,0}};
            std::memcpy(quad,strip_index ? second:first,sizeof(quad));
        }
        if(case_id==7) {
            float large_first[4][3]{{-1,1,2},{2,0,2},{1,-2,2},{-2,-1,2}};
            std::memcpy(quad,large_first,sizeof(quad));
        }
        auto u=consume(2); bool inside=true;
        for(unsigned i=0;i<4;++i) {
            auto a=quad[i], b=quad[(i+1)%4];
            float cross=(u.resolved[1]-a[1])*(b[0]-a[0])-(b[1]-a[1])*(u.resolved[0]-a[0]);
            if(cross>0) { inside=false; break; }
        }
        if(inside) return true;
        for(unsigned i=0;i<4;++i) {
            u=consume(3); dx=u.resolved[0]-quad[i][0]; dy=u.resolved[1]-quad[i][1];
            if(dx*dx+dy*dy<=u.radius*u.radius && quad[i][2]<=u.upper) return true;
        }
        // One new resolved position is consumed by all four closed edge checks.
        u=consume(4);
        for(unsigned i=0;i<4;++i) {
            auto a=quad[i], b=quad[(i+1)%4]; float v[3],w[3],dot=0,length=0;
            for(unsigned j=0;j<3;++j) { v[j]=b[j]-a[j]; w[j]=u.resolved[j]-a[j]; dot+=v[j]*w[j]; length+=v[j]*v[j]; }
            float t=length ? dot/length:0; if(t<0) t=0; if(t>1) t=1;
            float distance=0;
            for(unsigned j=0;j<3;++j) { float d=w[j]-t*v[j]; distance+=d*d; }
            if(distance<=u.radius*u.radius) return true;
        }
    }
    return false;
}
void evaluate(unsigned case_id,unsigned fault=0,uint64_t parent=0,bool nest=false) {
    auto r=reserve(); if(!r) return;
    Source source;
    source.points=case_id==1 || case_id==2 ? single : case_id==8 ? late : strip;
    source.count=case_id==0 ? 0 : case_id<=2 ? 1 : case_id==8 ? 3 : 2;
    void* ephemeral=nullptr;
    if(case_id==9) {
        ephemeral=VirtualAlloc(nullptr,sizeof(strip),MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);
        require(ephemeral!=nullptr); std::memcpy(ephemeral,strip,sizeof(strip));
        source.points=static_cast<Point*>(ephemeral);
    }
    if(case_id==7) { source.points=large.data(); source.count=max_points; }
    if(fault==1) source.count=max_points+1;
    if(fault==2) source.points=reinterpret_cast<Point*>(1);
    if(fault==3) source.certified=false;
    if(fault==4) source.lease.test_and_set();
    if(fault==12) source.during_copy=[](Source& s) { ++s.version; strip[0].x+=1; strip[0].x-=1; ++s.version; };
    Group group(*r,source); group.begin(case_id,parent);
    r->h.radius=case_id==8 ? 30.f : 10.f;
    PendingScope scope(&group);
    if(nest) evaluate(1,0,r->h.token);
    bool accept=decision(case_id,group,fault);
    if(fault==17) throw 17;
    if(fault==7) stopping=true;
    if(fault==8) group.fail(interrupted);
    if(fault==9) {
        for(unsigned i=2;i<max_uses+1;++i) group.use(operands(case_id,i));
    }
    if(fault==10) group.finish(r->h.token+1,1);
    if(fault!=11) {
        alignas(64) unsigned char state[3072]{};
        unsigned long long closure[2]{r->h.token+(fault==13 ? 1 : 0),0x22334455};
        probe(state,closure,accept ? 1 : 0);
        if(fault==14) group.finish(r->h.token,accept ? 2 : 1);
        if(fault==15) group.use(operands(case_id,2));
    }
    if(fault==16) { group.close(); group.finish(r->h.token,1); }
    group.close(); stopping=false;
    if(fault==4) source.lease.clear();
    require(fault ? r->h.status!=complete : r->h.status==complete);
    // Destroy source pointer and fixture-local source; worker must own all bytes.
    source.points=nullptr; source.count=0;
    if(ephemeral) require(VirtualFree(ephemeral,0,MEM_RELEASE)!=0);
}
}
void capture_terminal(unsigned terminal,unsigned depth,const void* closure) {
    uint64_t observed{};
    if(pending && depth==1) {
        if(!capture::read(&observed,closure,sizeof(observed))) pending->fail(capture::read_failed);
        else pending->finish(observed,terminal);
    }
}
void geometry_tests() {
    for(unsigned i=0;i<large.size();++i) large[i]=Point{float(i),float(-int(i)),2,1};
    for(unsigned id=0;id<9;++id) evaluate(id);
    evaluate(9);
    for(unsigned fault=1;fault<=16;++fault) evaluate(3,fault);
    try { evaluate(3,17); require(false); } catch(int code) { require(code==17 && pending==nullptr); }
    evaluate(3,0,0,true);
    stopping=true;
    {
        auto r=reserve(); Source s; Group g(*r,s); g.begin(1); g.close();
        require(r->h.status==not_evaluated);
    }
    stopping=false;
    std::array<std::thread,4> threads;
    for(auto& t:threads) t=std::thread([]{for(unsigned i=0;i<4;++i) evaluate(i);});
    for(auto& t:threads) t.join();
    // A finite storage stress, not a session/event quota. Every excess admission is reported.
    while(cursor<records.size()) evaluate(1);
    evaluate(1); require(pool_losses==1 && overflow);
    FILE* f{}; require(fopen_s(&f,"geometry.bin","wb")==0 && f);
    for(const auto& r:records) {
        uint32_t length=sizeof(Header)+r.h.bytes+r.h.uses*sizeof(Use)+4;
        uint32_t end=0x454e4f44;
        require(std::fwrite(&length,4,1,f)==1);
        require(std::fwrite(&r.h,sizeof(Header),1,f)==1);
        if(r.h.bytes) require(std::fwrite(r.points,r.h.bytes,1,f)==1);
        if(r.h.uses) require(std::fwrite(r.uses,r.h.uses*sizeof(Use),1,f)==1);
        require(std::fwrite(&end,4,1,f)==1);
    }
    require(std::fflush(f)==0); require(std::fclose(f)==0);
    // Timing controls use a reusable scratch slot; no allocation, IO, waits in Group.
    static Record scratch;
    long long costs[3]{}, allocation_cost{}; unsigned counts[]{0,2,max_points};
    for(unsigned k=0;k<3;++k) {
        Source s; s.points=large.data(); s.count=counts[k];
        auto start=std::chrono::steady_clock::now();
        for(unsigned i=0;i<1000;++i) {
            Group g(scratch,s); g.begin(7); g.use(operands(7,0)); g.finish(g.r.h.token,1); g.close();
            require(scratch.h.status==complete);
        }
        costs[k]=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now()-start).count()/1000;
    }
    // An allocating alternative is measured outside callbacks, then rejected for hot-path use.
    auto start=std::chrono::steady_clock::now();
    volatile float sink=0;
    for(unsigned i=0;i<1000;++i) {
        auto p=static_cast<Point*>(std::malloc(max_points*sizeof(Point))); require(p!=nullptr);
        std::memcpy(p,large.data(),max_points*sizeof(Point)); sink=p[i%max_points].x; std::free(p);
    }
    allocation_cost=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now()-start).count()/1000;
    std::printf("{\"geometry_records\":64,\"pool_losses\":%u,\"sticky_overflow\":true,\"copy_ns_mean_0_2_8192\":[%lld,%lld,%lld],\"allocating_copy_8192_ns\":%lld}\n",
                pool_losses.load(),costs[0],costs[1],costs[2],allocation_cost);
}
