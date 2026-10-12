// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "branch.h"
namespace oracle {
// Version 4 adds no raw struct fields. Tags distinguish the new contracts.
enum RKind:uint64_t {route_begin=22,route_end=23,route_unwind=24,eligible_in=25,eligible_out=26,search_in=27,search_out=28,fallback_in=29,fallback_out=30,source_in=31,source_out=32,native_grid_in=33,native_grid_out=34,delta_in=35,delta_out=36,identity_in=37,identity_out=38,child_unwind=39,direct_identity_in=45};
using Route=uint64_t(*)(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
using Five=uint64_t(*)(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
using Six=uint64_t(*)(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
inline Route original_route{};inline Helper3 original_eligible{},original_route_source{},original_route_grid{},original_identity{};
inline Six original_search{};inline Five original_route_fallback{};inline Helper4 original_route_delta{};
inline uint64_t manager_slot{};
struct RouteState {uint64_t args[7]{};};
inline thread_local RouteState routes[32];
inline Scope* route_scope(){return depth&&!suppressed&&scopes[depth-1].stage==3?&scopes[depth-1]:nullptr;}
__declspec(noinline) inline void route_snapshot(Event& e,Scope& s){
    auto& r=routes[&s-scopes];copy(e.context_raw,s.ctx,0x30);copy(e.source,r.args[2],0x40);
    // Output +18 is native-selected ref after FDCD; at entry it can be stale.
    auto ref=field<uint64_t>(e.context_raw,0x18);Scope actual=s;actual.ref=ref;actual.ctx=0;
    context(e,actual); // Shared identity/world/Workshop copies, explicitly samples.
    copy(e.context_raw,s.ctx,0x30);copy(e.source,r.args[2],0x40);
    copy(e.candidate,r.args[3],0x30); // selected/source metadata, not assumed TESObjectREFR
    auto manager=pointer(manager_slot);
    auto world=pointer(manager+0x120);copy(e.world,world,0x390);
    copy(e.translation,s.ctx+0x20,12);copy(e.center,r.args[1],16);
    copy(e.block,settings_addresses[0],4);copy(e.merge,settings_addresses[1],4);copy(e.scale,settings_addresses[2],4);
}
struct RouteLease {
    bool acquired{},stacked{},suppression{};Scope* scope{};
    RouteLease(const uint64_t* args){Environment env;
        if(suppressed){++suppressed;suppression=true;return;}
        acquired=gate.enter();if(!acquired){++suppressed;suppression=true;return;}
        if(depth==32){++suppressed;suppression=true;depth_errors.fetch_add(1);gate.stop();return;}
        auto index=depth++;stacked=true;scope=&scopes[index];*scope={};scope->id=invocations.fetch_add(1)+1;scope->parent=index?scopes[index-1].id:0;scope->stage=3;scope->ref=args[3];scope->ctx=args[0];memcpy(routes[index].args,args,56);
        active_stages[2].fetch_add(1);entered_stages[2].fetch_add(1);capture(route_begin,0);
    }
    __declspec(noinline) void capture(RKind kind,uint64_t value){Event e;stamp(e,*scope,static_cast<Kind>(kind));route_snapshot(e,*scope);copy(e.input_hierarchy,reinterpret_cast<uint64_t>(routes[scope-scopes].args),56);if(kind==route_end)copy(e.result,reinterpret_cast<uint64_t>(&value),8);emit(e);}
    void finish(bool abnormal,uint64_t value){Environment env;if(stacked){capture(abnormal?route_unwind:route_end,value);active_stages[2].fetch_sub(1);--depth;}else if(suppression)--suppressed;if(acquired)gate.leave();}
};
// Each helper has a distinct invocation even if repeated/nested in one route.
struct RouteChild {
    Scope* owner{};Scope child{};RKind kind;uint64_t args[6]{};uint64_t callsite{};
    RouteChild(RKind k,const uint64_t* a,unsigned n,uint64_t site):kind(k),callsite(site){Environment env;owner=route_scope();if(!owner)return;child=*owner;child.parent=owner->id;child.id=invocations.fetch_add(1)+1;memcpy(args,a,n*8);capture(false,false,0);}
    __declspec(noinline) void capture(bool completion,bool abnormal,uint64_t value){if(!owner)return;Event e;stamp(e,child,static_cast<Kind>(abnormal?child_unwind:kind+(completion?1:0)));e.status=abnormal?kind:0;route_snapshot(e,*owner);copy(e.input_hierarchy,reinterpret_cast<uint64_t>(args),48);
        if(kind==native_grid_in||kind==source_in||kind==delta_in){copy(e.landscape,args[0],0x60);}
        if(kind==native_grid_in){copy(e.candidate,args[1],44);copy(e.floor_xy,args[2],8);copy(e.center,field<uint64_t>(e.cell,0x110),0x390);}
        if(kind==source_in){copy(e.candidate,args[1],44);copy(e.center,args[2],16);}
        if(kind==delta_in){copy(e.candidate,args[2],44);copy(e.floor_xy,args[3],44);copy(e.center,args[1],8);}
        if(kind==search_in){copy(e.candidate,args[1],16);copy(e.floor_xy,args[2],16);copy(e.center,args[4],12);}
        if(kind==fallback_in){copy(e.candidate,args[1],16);copy(e.floor_xy,args[2],16);copy(e.center,args[4],12);}
        if(kind==identity_in||kind==direct_identity_in){copy(e.candidate,args[0],0x30);copy(e.floor_xy,args[1],4);copy(e.center,args[2],16);}
        if(completion&&!abnormal){copy(e.result,reinterpret_cast<uint64_t>(&value),8);if(kind==search_in||kind==fallback_in)copy(e.ref,value,0xd0);}
        unsigned char contract[16]{};auto setting_address=e.block.address;uint32_t setting_ok=e.block.ok;if(setting_ok)memcpy(contract,e.block.bytes,4);memcpy(contract+4,&setting_ok,4);memcpy(contract+8,&callsite,8);copy(e.block,reinterpret_cast<uint64_t>(contract),16);e.block.address=setting_address;if(abnormal)e.status=kind;emit(e);
    }
    void finish(bool abnormal,uint64_t value){Environment env;capture(true,abnormal,value);}
};
inline uint64_t route_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t f,uint64_t g,uint64_t h){uint64_t args[]{a,b,c,d,f,g,h};RouteLease lease(args);uint64_t v{};__try{v=original_route(a,b,c,d,f,g,h);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t eligible_hook(uint64_t a,uint64_t b,uint64_t c){uint64_t args[]{a,b,c};RouteChild lease(eligible_in,args,3,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_eligible(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t search_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t f,uint64_t g){uint64_t args[]{a,b,c,d,f,g};RouteChild lease(search_in,args,6,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_search(a,b,c,d,f,g);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t route_fallback_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t f){uint64_t args[]{a,b,c,d,f};RouteChild lease(fallback_in,args,5,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_route_fallback(a,b,c,d,f);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t route_source_hook(uint64_t a,uint64_t b,uint64_t c){uint64_t args[]{a,b,c};RouteChild lease(source_in,args,3,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_route_source(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t route_grid_hook(uint64_t a,uint64_t b,uint64_t c){uint64_t args[]{a,b,c};RouteChild lease(native_grid_in,args,3,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_route_grid(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t route_delta_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){uint64_t args[]{a,b,c,d};RouteChild lease(delta_in,args,4,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_route_delta(a,b,c,d);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t identity_hook(uint64_t a,uint64_t b,uint64_t c){uint64_t args[]{a,b,c};RouteChild lease(identity_in,args,3,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_identity(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t direct_identity_hook(uint64_t a,uint64_t b,uint64_t c){uint64_t args[]{a,b,c};RouteChild lease(direct_identity_in,args,3,reinterpret_cast<uint64_t>(_ReturnAddress()));uint64_t v{};__try{v=original_identity(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
// Upstream selected-reference boundaries. Standalone event lifetimes do not
// fabricate ancestry across asynchronous work or post-return explicit travel.
inline Helper4 original_selected{};inline Helper3 original_selected_body{};
struct SelectionLease {
    bool acquired{},stacked{},suppression{};Scope s{};uint64_t args[6]{};unsigned tag{};
    SelectionLease(unsigned k,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t native_body=0,uint64_t native_out=0):tag(k){Environment env;
        if(suppressed){++suppressed;suppression=true;return;}acquired=gate.enter();if(!acquired){++suppressed;suppression=true;return;}
        if(depth==32){++suppressed;suppression=true;depth_errors.fetch_add(1);gate.stop();return;}
        s.id=invocations.fetch_add(1)+1;s.parent=depth?scopes[depth-1].id:0;s.ref=a;s.ctx=b;s.stage=4;scopes[depth++]=s;stacked=true;active_stages[2].fetch_add(1);entered_stages[2].fetch_add(1);
        args[0]=a;args[1]=b;args[2]=c;args[3]=d;args[4]=native_body;args[5]=native_out;capture(false,false,0);}
    __declspec(noinline) void capture(bool completion,bool abnormal,uint64_t value){Event e;stamp(e,s,static_cast<Kind>(abnormal?44:tag+(completion?1:0)));e.status=abnormal?tag:0;context(e,s);copy(e.ref,args[0],0x390);copy(e.input_hierarchy,reinterpret_cast<uint64_t>(args),48);if(tag==42){copy(e.floor_xy,args[1],4);copy(e.center,args[2],16);}if(tag==48){copy(e.floor_xy,reinterpret_cast<uint64_t>(&args[4]),4);copy(e.source,args[3],64);copy(e.candidate,args[2],0x90);}if(completion&&!abnormal)copy(e.result,reinterpret_cast<uint64_t>(&value),8);if(abnormal)e.status=tag;emit(e);}
    void finish(bool abnormal,uint64_t value){Environment env;if(stacked){capture(true,abnormal,value);--depth;active_stages[2].fetch_sub(1);}else if(suppression)--suppressed;if(acquired)gate.leave();}
};
inline uint64_t selected_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){SelectionLease lease(40,a,b,c,d);uint64_t v{};__try{v=original_selected(a,b,c,d);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
inline uint64_t selected_body_hook(uint64_t a,uint64_t b,uint64_t c){SelectionLease lease(42,a,b,c,0);uint64_t v{};__try{v=original_selected_body(a,b,c);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}

inline Helper4 original_producer{};
extern "C" __declspec(noinline) uint64_t producer_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t selected,uint64_t operation){SelectionLease lease(48,selected,a,operation,d,c,b);uint64_t v{};__try{v=original_producer(a,b,c,d);}__finally{lease.finish(AbnormalTermination()!=0,v);}return v;}
extern "C" uint64_t producer_bridge(uint64_t,uint64_t,uint64_t,uint64_t);

}
