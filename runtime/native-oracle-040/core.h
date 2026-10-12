// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "../exp0002/win_support.h"
#include <atomic>
#include <array>
#include <intrin.h>
#include <immintrin.h>

namespace oracle {
using namespace sor;
constexpr uint64_t stop_bit=1ULL<<63;
constexpr uint64_t disk_floor=40'000'000'000ULL;
inline std::atomic<uint64_t> worker_tick{},health_timeouts{};
inline std::atomic<bool> worker_required{false};
inline bool disk(){ULARGE_INTEGER c{},d{};return GetDiskFreeSpaceExW(L"C:\\",&c,nullptr,nullptr)&&GetDiskFreeSpaceExW(L"D:\\",&d,nullptr,nullptr)&&c.QuadPart>=disk_floor+1048576&&d.QuadPart>=disk_floor+1048576;}
inline bool durable_append(HANDLE h,const void* p,size_t n,bool space_available){if(!space_available||n>MAXDWORD)return false;DWORD wrote{};return WriteFile(h,p,static_cast<DWORD>(n),&wrote,nullptr)&&wrote==n&&FlushFileBuffers(h);}
struct Gate {
    std::atomic<uint64_t> state{stop_bit};
    bool enter(){if(worker_required.load()&&GetTickCount64()-worker_tick.load()>15000){if(!(state.fetch_or(stop_bit)&stop_bit))health_timeouts.fetch_add(1);return false;}auto s=state.load();while(!(s&stop_bit)){if(state.compare_exchange_weak(s,s+1))return true;}return false;}
    void leave(){state.fetch_sub(1);}
    void stop(){state.fetch_or(stop_bit);}
    bool drained()const{return state.load()==stop_bit;}
};
// Every raw field has its own explicit read status. Zero bytes never imply a
// successful zero-valued native observation. Domains are defined in schema.md.
struct Blob {uint64_t address{};uint32_t length{},ok{};unsigned char bytes[0x400]{};};
struct Event {
    uint64_t sequence{},invocation{},parent{},qpc{},reference{},context{},thread{},kind{},status{},mxcsr{},last_error{};
    Blob ref,base,extra,cell,world,context_raw,source,candidate,translation,landscape,center,input_hierarchy,floor_xy,result,block,merge,scale;
};
enum Kind:uint64_t {begin=1,center=2,grid=3,end=4,unwind=5,grid_begin=6,query_begin=7,query_end=8,query_unwind=9,enum_begin=10,enum_end=11,enum_unwind=12};
// Bounded nonblocking MPSC queue. Reservation is published only after a full
// record copy; consumer never reads an unfinished slot. Saturation is a health
// failure, not a scientific count limit. No heap/locks/files on engine threads.
template<size_t N> struct Queue {
    struct Slot {std::atomic<uint64_t> turn{};Event event;};
    std::array<Slot,N> slots;
    std::atomic<uint64_t> put{};uint64_t take{};
    Queue(){for(size_t i=0;i<N;++i)slots[i].turn.store(i);}
    bool push(const Event& e){
        auto p=put.load(std::memory_order_relaxed);
        for(unsigned attempt=0;attempt<16;++attempt){auto& s=slots[p%N];auto t=s.turn.load(std::memory_order_acquire);
            if(t==p){if(put.compare_exchange_weak(p,p+1)){s.event=e;s.turn.store(p+1,std::memory_order_release);return true;}}
            else if(t<p)return false;else p=put.load(std::memory_order_relaxed);
        }return false;
    }
    bool pop(Event& e){auto& s=slots[take%N];if(s.turn.load(std::memory_order_acquire)!=take+1)return false;e=s.event;s.turn.store(take+N,std::memory_order_release);++take;return true;}
};
inline bool copy(Blob& b,uint64_t p,size_t n){
    b.address=p;b.length=static_cast<uint32_t>(n);b.ok=0;memset(b.bytes,0,sizeof b.bytes);
    SIZE_T got{};
    if(p>=0x10000 && p<=0x7fffffffffffULL && n<=sizeof b.bytes && n && n-1<=0x7fffffffffffULL-p)
        b.ok=ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(p),b.bytes,n,&got)&&got==n;
    return b.ok!=0;
}
template<class T> T field(const Blob& b,size_t offset){T v{};if(b.ok&&offset+sizeof v<=b.length)memcpy(&v,b.bytes+offset,sizeof v);return v;}
inline uint64_t pointer(uint64_t p){uint64_t v{};SIZE_T got{};return ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(p),&v,8,&got)&&got==8?v:0;}
struct Environment {
    DWORD error=GetLastError();alignas(16) unsigned char fp[512];
    Environment(){_fxsave64(fp);}
    ~Environment(){_fxrstor64(fp);SetLastError(error);}
};
struct Scope {uint64_t id{},parent{},ref{},ctx{},stage{};bool has_center{};Blob native_center;uint64_t q_overlay{},q_landscape{},q_a{};};
using Callback=uint64_t(*)(uint64_t,uint64_t,uint64_t);
using Center=uint64_t(*)(uint64_t,uint64_t);
using Selector=uint64_t(*)(uint64_t,uint64_t,uint64_t);
inline Callback original_callback{};inline Center original_center{};inline Selector original_selector{};
using Query=uint32_t(*)(uint64_t,uint64_t);
using Enumerate=uint32_t(*)(uint64_t,uint64_t,uint64_t);
inline Query original_query{};inline Enumerate original_enum{};
inline Queue<4096>* queue{}; // ~60 MiB; allocated before activation, stays resident.
inline Gate gate;inline std::atomic<uint64_t> sequences{},invocations{},lost{},depth_errors{};
inline std::atomic<uint64_t> active_stages[3]{},entered_stages[3]{};
inline std::atomic<bool> center_channel{true},grid_channel{true};
inline uint64_t settings_addresses[3]{};
inline thread_local Scope scopes[32];inline thread_local unsigned depth{},suppressed{};
inline thread_local Event pending_grid[32];
inline void emit(Event& e){e.sequence=sequences.fetch_add(1)+1;if(!queue||!queue->push(e)){lost.fetch_add(1);gate.stop();}}
inline void stamp(Event& e,const Scope& s,Kind k){
    e.invocation=s.id;e.parent=s.parent;e.reference=s.ref;e.context=s.ctx;e.thread=GetCurrentThreadId();e.kind=k;
    LARGE_INTEGER q{};QueryPerformanceCounter(&q);e.qpc=q.QuadPart;e.mxcsr=_mm_getcsr();e.last_error=GetLastError();
}
inline void context(Event& e,const Scope& s){
    copy(e.block,settings_addresses[0],4);copy(e.merge,settings_addresses[1],4);copy(e.scale,settings_addresses[2],4);
    copy(e.context_raw,s.ctx,48);
    if(e.context_raw.ok){copy(e.candidate,field<uint64_t>(e.context_raw,8),44);copy(e.source,field<uint64_t>(e.context_raw,24),44);copy(e.translation,field<uint64_t>(e.context_raw,32),12);copy(e.landscape,pointer(field<uint64_t>(e.context_raw,16)),0x58);}
    copy(e.ref,s.ref,0xd0);
    if(e.ref.ok){
        copy(e.base,field<uint64_t>(e.ref,0x98),0x30);copy(e.cell,field<uint64_t>(e.ref,0xb0),0x118);
        if(e.cell.ok && !(field<uint32_t>(e.cell,0x48)&1))copy(e.world,field<uint64_t>(e.cell,0x110),0x390);
        auto list=field<uint64_t>(e.ref,0xc8);auto node=pointer(list+8);uint64_t seen[64]{};
        for(unsigned n=0;node && n<64;++n){
            bool cycle=false;for(unsigned j=0;j<n;++j)cycle|=seen[j]==node;if(cycle){e.status|=1;break;}seen[n]=node;
            Blob header; if(!copy(header,node,0x18)){e.status|=2;break;}
            if(header.bytes[0x12]==0xbc){copy(e.extra,node,0xa0);break;}
            node=field<uint64_t>(header,8);if(n==63&&node)e.status|=4;
        }
        // Detect some races without claiming native ownership/atomic snapshots.
        Blob again;copy(again,s.ref,0xd0);
        if(!again.ok || memcmp(again.bytes+0x24,e.ref.bytes+0x24,12)||memcmp(again.bytes+0x98,e.ref.bytes+0x98,8)||memcmp(again.bytes+0xc8,e.ref.bytes+0xc8,8))e.status|=8;
    }
}
struct Lease {
    bool acquired{},stacked{},suppression{};Scope* scope{};
    Lease(uint64_t object,uint64_t reference_slot){
        Environment env;
        if(suppressed){++suppressed;suppression=true;return;}
        acquired=gate.enter();if(!acquired){++suppressed;suppression=true;return;}
        if(depth==32){++suppressed;suppression=true;depth_errors.fetch_add(1);gate.stop();return;}
        stacked=true;scope=&scopes[depth++];*scope={};scope->id=invocations.fetch_add(1)+1;
        scope->parent=depth>1?scopes[depth-2].id:0;scope->ref=pointer(reference_slot);scope->ctx=pointer(object+8);
        scope->stage=2;active_stages[2].fetch_add(1);entered_stages[2].fetch_add(1);
        capture_begin(*scope);
    }
    static __declspec(noinline) void capture_begin(Scope& s){Event e;stamp(e,s,begin);context(e,s);emit(e);}
    static __declspec(noinline) void capture_end(Scope& s,bool abnormal,uint64_t value){Event e;stamp(e,s,abnormal?unwind:end);if(!abnormal)copy(e.result,reinterpret_cast<uint64_t>(&value),8);emit(e);}
    void finish(bool abnormal,uint64_t value){Environment env;if(stacked){capture_end(*scope,abnormal,value);active_stages[2].fetch_sub(1);--depth;}else if(suppression)--suppressed;if(acquired)gate.leave();}
};
// Q/E scopes are transport/diagnostic evidence, never ordinary reference IDs.
// Their header reference/context fields preserve argument1/argument2 verbatim.
struct DiagnosticLease {
    bool acquired{},stacked{},suppression{};Scope* scope{};uint64_t third{};
    DiagnosticLease(uint64_t a,uint64_t b,uint64_t c,unsigned stage):third(c){
        Environment env;
        if(suppressed){++suppressed;suppression=true;return;}
        acquired=gate.enter();if(!acquired){++suppressed;suppression=true;return;}
        if(depth==32){++suppressed;suppression=true;depth_errors.fetch_add(1);gate.stop();return;}
        stacked=true;scope=&scopes[depth++];*scope={};scope->id=invocations.fetch_add(1)+1;
        scope->parent=depth>1?scopes[depth-2].id:0;scope->ref=a;scope->ctx=b;scope->stage=stage;
        active_stages[stage].fetch_add(1);entered_stages[stage].fetch_add(1);capture(false,false,0);
    }
    __declspec(noinline) void capture(bool completion,bool abnormal,uint32_t value){
        Event e;auto& s=*scope;auto k=s.stage==0?(completion?(abnormal?query_unwind:query_end):query_begin):(completion?(abnormal?enum_unwind:enum_end):enum_begin);
        stamp(e,s,k);uint64_t args[3]{s.ref,s.ctx,third};copy(e.input_hierarchy,reinterpret_cast<uint64_t>(args),sizeof args);
        if(s.stage==0){
            copy(e.context_raw,s.ref,40);copy(e.candidate,s.ctx,24);
            copy(e.center,field<uint64_t>(e.context_raw,8),1);copy(e.translation,field<uint64_t>(e.context_raw,24),16);
            copy(e.world,field<uint64_t>(e.context_raw,16),0x390);
            copy(e.source,field<uint64_t>(e.context_raw,32),24);
            copy(e.floor_xy,field<uint64_t>(e.context_raw,16)+0x310,8); // packed value, not pointer
        }else{
            copy(e.ref,s.ref,0x90);copy(e.base,s.ctx,16);auto ctx=pointer(s.ctx+8);copy(e.context_raw,ctx,48);
            if(e.context_raw.ok){copy(e.candidate,field<uint64_t>(e.context_raw,8),44);copy(e.source,field<uint64_t>(e.context_raw,24),44);copy(e.translation,field<uint64_t>(e.context_raw,32),12);copy(e.landscape,pointer(field<uint64_t>(e.context_raw,16)),0x58);}
        }
        if(completion&&!abnormal)copy(e.result,reinterpret_cast<uint64_t>(&value),4);emit(e);
    }
    void finish(bool abnormal,uint32_t value){Environment env;if(stacked){capture(true,abnormal,value);active_stages[scope->stage].fetch_sub(1);--depth;}else if(suppression)--suppressed;if(acquired)gate.leave();}
};
inline uint32_t query_hook(uint64_t a,uint64_t b){DiagnosticLease lease(a,b,0,0);uint32_t result{};
    __try{result=original_query(a,b);}__finally{lease.finish(AbnormalTermination()!=0,result);}return result;}
inline void q_enum_entry(uint64_t,uint64_t,uint64_t);
inline uint32_t enum_hook(uint64_t a,uint64_t b,uint64_t c){q_enum_entry(a,b,c);DiagnosticLease lease(a,b,c,1);uint32_t result{};
    __try{result=original_enum(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,result);}return result;}
// Ordinary Windows x64 ABI calls at complete CALL boundaries. Compiler-generated
// unwind metadata covers these functions. No stolen prologue, return rewriting,
// fabricated native input or exception handler that swallows game faults.
inline uint64_t callback_hook(uint64_t object,uint64_t slot,uint64_t arg){
    Lease lease(object,slot);uint64_t result{};
    __try{result=original_callback(object,slot,arg);}
    __finally{lease.finish(AbnormalTermination()!=0,result);}
    return result;
}
inline uint64_t center_hook(uint64_t ref,uint64_t out){
    auto value=original_center(ref,out);
    {Environment env;if(depth&&!suppressed&&scopes[depth-1].stage==2&&center_channel.load()){
        auto& s=scopes[depth-1];Event e;stamp(e,s,center);context(e,s);copy(e.center,out,12);
        if(ref!=s.ref)e.status|=16;s.native_center=e.center;s.has_center=ref==s.ref&&e.center.ok;emit(e);
    }}return value;
}
inline uint64_t selector_hook(uint64_t landscape,uint64_t hierarchy,uint64_t xy){
    Event* event{};bool observe=depth&&!suppressed&&scopes[depth-1].stage==2&&grid_channel.load();
    if(observe){Environment env;auto& s=scopes[depth-1];event=&pending_grid[depth-1];*event={};auto& e=*event;stamp(e,s,grid_begin);context(e,s);copy(e.input_hierarchy,hierarchy,44);copy(e.floor_xy,xy,8);copy(e.landscape,landscape,0x58);if(s.has_center)e.center=s.native_center;else e.status|=32;emit(e);}
    auto value=original_selector(landscape,hierarchy,xy);
    if(observe){Environment env;auto& e=*event;e.kind=grid;LARGE_INTEGER q{};QueryPerformanceCounter(&q);e.qpc=q.QuadPart;copy(e.result,hierarchy,44);emit(e);}return value;
}
}
