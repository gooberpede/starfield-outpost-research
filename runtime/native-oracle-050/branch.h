// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "core.h"
namespace oracle {
enum QKind:uint64_t {q_resolver=13,q_fallback=14,q_overlay=15,q_a=16,q_b=17,q_angular=18,q_delta=19,q_e_entry=20,q_helper_unwind=21};
using Helper1=uint64_t(*)(uint64_t);
using Helper2=uint64_t(*)(uint64_t,uint64_t);
using Helper3=uint64_t(*)(uint64_t,uint64_t,uint64_t);
using Helper4=uint64_t(*)(uint64_t,uint64_t,uint64_t,uint64_t);
inline Helper3 original_resolver{},original_a{},original_b{},original_angular{};
inline Helper1 original_fallback{};inline Helper2 original_overlay{};inline Helper4 original_delta{};
inline Scope* q_scope(){return depth&&!suppressed&&scopes[depth-1].stage==0?&scopes[depth-1]:nullptr;}
// No pointer escapes its owning Q scope. Copies occur synchronously before the
// caller resumes; records own bytes. Shared objects are sampled, not locked.
__declspec(noinline) inline void q_observe(Scope* s,QKind k,bool abnormal,uint64_t value,uint64_t a,uint64_t b=0,uint64_t c=0,uint64_t d=0){
    if(!s)return;Environment env;Event e;stamp(e,*s,static_cast<Kind>(abnormal?q_helper_unwind:k));
    if(abnormal)e.status=k;
    uint64_t args[4]{a,b,c,d};copy(e.input_hierarchy,reinterpret_cast<uint64_t>(args),sizeof args);
    if(!abnormal&&k!=q_e_entry)copy(e.result,reinterpret_cast<uint64_t>(&value),8);
    copy(e.context_raw,s->ref,40);copy(e.world,field<uint64_t>(e.context_raw,16),0x390);
    copy(e.floor_xy,field<uint64_t>(e.context_raw,16)+0x310,8);
    copy(e.block,settings_addresses[0],4);copy(e.merge,settings_addresses[1],4);copy(e.scale,settings_addresses[2],4);
    if(!abnormal){
        if(k==q_resolver||k==q_fallback)copy(e.ref,value,0x30);
        if(k==q_overlay)s->q_overlay=value;
        if(k==q_a){s->q_landscape=a;s->q_a=b;copy(e.candidate,b,44);}
        if(k==q_b){copy(e.candidate,s->q_a,44);copy(e.source,b,44);}
        if(k==q_angular){copy(e.center,c,24);copy(e.source,b,44);}
        if(k==q_delta){copy(e.translation,b,8);copy(e.source,c,44);copy(e.candidate,d,44);}
    }
    copy(e.extra,s->q_overlay,0x34);copy(e.landscape,s->q_landscape,0x58);emit(e);
}
inline uint64_t resolver_hook(uint64_t a,uint64_t b,uint64_t c){auto s=q_scope();uint64_t v{};__try{v=original_resolver(a,b,c);}__finally{q_observe(s,q_resolver,AbnormalTermination()!=0,v,a,b,c);}return v;}
inline uint64_t fallback_hook(uint64_t a){auto s=q_scope();uint64_t v{};__try{v=original_fallback(a);}__finally{q_observe(s,q_fallback,AbnormalTermination()!=0,v,a);}return v;}
inline uint64_t overlay_hook(uint64_t a,uint64_t b){auto s=q_scope();uint64_t v{};__try{v=original_overlay(a,b);}__finally{q_observe(s,q_overlay,AbnormalTermination()!=0,v,a,b);}return v;}
inline uint64_t a_hook(uint64_t a,uint64_t b,uint64_t c){auto s=q_scope();uint64_t v{};__try{v=original_a(a,b,c);}__finally{q_observe(s,q_a,AbnormalTermination()!=0,v,a,b,c);}return v;}
inline uint64_t b_hook(uint64_t a,uint64_t b,uint64_t c){auto s=q_scope();uint64_t v{};__try{v=original_b(a,b,c);}__finally{q_observe(s,q_b,AbnormalTermination()!=0,v,a,b,c);}return v;}
inline uint64_t angular_hook(uint64_t a,uint64_t b,uint64_t c){auto s=q_scope();uint64_t v{};__try{v=original_angular(a,b,c);}__finally{q_observe(s,q_angular,AbnormalTermination()!=0,v,a,b,c);}return v;}
inline uint64_t delta_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){auto s=q_scope();uint64_t v{};__try{v=original_delta(a,b,c,d);}__finally{q_observe(s,q_delta,AbnormalTermination()!=0,v,a,b,c,d);}return v;}
inline void q_enum_entry(uint64_t a,uint64_t b,uint64_t c){q_observe(q_scope(),q_e_entry,false,0,a,b,c);}
}
