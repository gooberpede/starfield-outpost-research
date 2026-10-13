// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "route.h"
namespace oracle {
// Source: retained static-exhaustion-23 17DEC70 CALL windows; see specialist.md.
// obs: caller return, frame, R14B, RBX, R13, RSI, R15, R12,
// caller param5, caller param6, prior-ship local, original CALL return.
inline Helper4 original_travel_producer{};
inline Helper2 original_travel_command{};
struct TravelLease {
    bool acquired{},stacked{},suppression{};Scope s{};
    uint64_t args[4]{},observed[12]{};unsigned tag{};
    TravelLease(unsigned k,uint64_t a,uint64_t b,uint64_t c,uint64_t d,const uint64_t* o):tag(k){Environment env;
        if(suppressed){++suppressed;suppression=true;return;}
        acquired=gate.enter();if(!acquired){++suppressed;suppression=true;return;}
        if(depth==32){++suppressed;suppression=true;depth_errors.fetch_add(1);gate.stop();return;}
        memcpy(observed,o,sizeof observed);args[0]=a;args[1]=b;args[2]=c;args[3]=d;
        s.id=invocations.fetch_add(1)+1;s.parent=depth?scopes[depth-1].id:0;
        s.ref=k==50?observed[3]:observed[4];s.stage=5;
        scopes[depth++]=s;stacked=true;active_stages[2].fetch_add(1);entered_stages[2].fetch_add(1);capture(false,false,0);
    }
    __declspec(noinline) void capture(bool completion,bool abnormal,uint64_t result){Event e;stamp(e,s,static_cast<Kind>(abnormal?tag+2:tag+(completion?1:0)));
        context(e,s);copy(e.input_hierarchy,reinterpret_cast<uint64_t>(args),sizeof args);
        copy(e.block,reinterpret_cast<uint64_t>(observed),sizeof observed);
        // Fixed-length snapshots, not new structure interpretations. Per-blob
        // read validity distinguishes zero/null/unreadable values.
        if(tag==50){copy(e.source,args[3],0x40);copy(e.candidate,args[1],0x28);copy(e.center,observed[4],16);copy(e.context_raw,observed[5],0xd0);}
        else {copy(e.source,args[1],0x98);copy(e.candidate,args[0],0x98);copy(e.context_raw,observed[3],0xd0);}
        if(completion&&!abnormal)copy(e.result,reinterpret_cast<uint64_t>(&result),8);
        if(abnormal)e.status=tag;emit(e);
    }
    void finish(bool abnormal,uint64_t value){Environment env;
        if(stacked){capture(true,abnormal,value);--depth;active_stages[2].fetch_sub(1);}
        else if(suppression)--suppressed;if(acquired)gate.leave();
    }
};
extern "C" __declspec(noinline) uint64_t travel_producer_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d,const uint64_t* observed){
    TravelLease lease(50,a,b,c,d,observed);uint64_t value{};
    __try{value=original_travel_producer(a,b,c,d);}__finally{lease.finish(AbnormalTermination()!=0,value);}return value;
}
extern "C" __declspec(noinline) uint64_t travel_command_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d,const uint64_t* observed){
    TravelLease lease(53,a,b,c,d,observed);uint64_t value{};
    __try{value=original_travel_command(a,b);}__finally{lease.finish(AbnormalTermination()!=0,value);}return value;
}
extern "C" uint64_t travel_producer_bridge(uint64_t,uint64_t,uint64_t,uint64_t);
extern "C" uint64_t travel_command_bridge(uint64_t,uint64_t);
}
