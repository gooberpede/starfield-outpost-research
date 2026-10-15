// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Owned 070 capture and 060 patch/module support adapted with bounded snapshots
// and worker-only queue transport. See lineage.json and the schema8 contract.
#include "modules.h"
#include <stdexcept>
namespace preview {
using namespace history;
inline uint64_t base{};
enum Tag:uint64_t { evaluation=101,ui=102,region=103,atmosphere=104,
    water_append=105,row=106,queue=107,population=108,member=109,model_row=110,source_visit=111,provider=112 };
inline thread_local uint64_t parent{};
inline std::atomic<uint64_t> evaluating{},writer_epoch{};
inline uint64_t tick(){LARGE_INTEGER q{};QueryPerformanceCounter(&q);return q.QuadPart;}
inline void failed(){++spool.failed;spool.broken=true;spool.stop();}
struct Invocation {
    Event e{};uint64_t outer{},epoch{};bool admitted{};
    Invocation(uint64_t site,Tag tag,uint64_t a,uint64_t b,uint64_t c,uint64_t d){
        Environment preserve;
        admitted=spool.enter();if(!admitted)return;
        outer=parent;epoch=writer_epoch.load();e.invocation=++spool.next_invocation;parent=e.invocation;
        e.parent=outer;e.site=site;e.kind=tag;e.thread=GetCurrentThreadId();
        e.args[0]=a;e.args[1]=b;e.args[2]=c;e.args[3]=d;
    }
    void send(uint64_t phase,uint64_t result){
        if(!admitted)return;e.phase=phase;e.result=result;e.qpc=tick();
        if(evaluating.load()>(e.kind==evaluation?1ULL:0ULL))e.status|=0x200;
        if(epoch!=writer_epoch.load())e.status|=0x200;
        if(spool.stopping.load())e.status|=0x800;
        spool.emit(e);
    }
    void finish(bool abnormal,uint64_t result){
        Environment preserve;
        if(!admitted)return;
        e.status|=abnormal?0x100:0;send(abnormal?unwind:after,result);
        parent=outer;--spool.active;admitted=false;
    }
};
inline void forms(Invocation& s,unsigned source,uint64_t begin,uint64_t end){
    if(!s.admitted)return;
    Event e=s.e;e.kind=population;e.phase=s.e.phase;e.args[0]=source;
    e.args[1]=begin;e.args[2]=end;e.args[3]=0;e.qpc=tick();
    bool valid=end>=begin&&((end-begin)%8)==0&&
        ((begin==0&&end==0)||(begin>=0x10000&&end<=0x7fffffffffffULL));
    e.status=valid?0:1;
    if(valid&&(end-begin)/8>256){e.status=0x2000;spool.emit(e);failed();return;}
    spool.emit(e);if(!valid)return;
    // Each operand within the integrity bound is owned in its own record.
    // A failed read is explicit, not an empty list or silently dropped suffix.
    for(uint64_t p=begin;p<end;p+=8){
        e.kind=member;e.args[3]=(p-begin)/8;e.qpc=tick();e.operand={};e.output={};
        copy(e.operand,p,8);auto resource=field<uint64_t>(e.operand,0);
        if(resource)copy(e.output,resource,0x30);
        e.reference=resource;e.status=!e.operand.ok?2:(resource&&!e.output.ok?4:0);
        if(!spool.emit(e))break; // failure is sticky, counts/terminal expose tail
    }
}
inline void state(Invocation& s,uint64_t address,uint64_t position,uint64_t actor=0){
    if(!s.admitted)return;
    s.e.ref={};s.e.base={};s.e.extra={};s.e.cell={};s.e.world={};s.e.output={};
    copy(s.e.ref,position,0x18);copy(s.e.base,address,0x68);
    auto domain=field<uint64_t>(s.e.ref,0x10);s.e.reference=domain;s.e.command=actor;
    s.e.operand={};if(domain)copy(s.e.operand,domain,0x30);
    if(actor){copy(s.e.extra,actor,0xd8);copy(s.e.output,field<uint64_t>(s.e.extra,0x98),0x30);auto cell=field<uint64_t>(s.e.extra,0xb0);
        if(cell){copy(s.e.cell,cell,0x118);if(s.e.cell.ok&&!(field<uint32_t>(s.e.cell,0x48)&1))copy(s.e.world,field<uint64_t>(s.e.cell,0x110),0x180);}}
    // +10 is CELL/world/sentinel domain, never blindly a TESObjectREFR.
    // RBX at preview CALL is the retained resolved ref. Walks are non-atomic.
}
inline void populations(Invocation& s,uint64_t address){
    if(!s.admitted)return;
    auto epoch=writer_epoch.load();Blob h;copy(h,address,0x48);s.e.aux=h;
    if(!h.ok){s.e.status|=2;return;}
    for(unsigned i=0;i<3;++i)forms(s,i,field<uint64_t>(h,i*24),field<uint64_t>(h,i*24+8));
    Blob again;copy(again,address,0x48);
    if(!again.ok||memcmp(h.bytes,again.bytes,0x48))s.e.status|=8;
    if(epoch!=writer_epoch.load()||evaluating.load()>(s.e.kind==evaluation?1ULL:0ULL))s.e.status|=0x200;
}
using Producer=unsigned char(*)(uint64_t,uint64_t,float,float);
inline void observe_producer(Invocation& s,uint64_t a,uint64_t b,uint64_t actor,uint64_t phase){
    Environment preserve;try{state(s,a,b,actor);s.e.phase=phase;populations(s,a);if(phase==before)s.send(before,0);}catch(...){failed();}
}
inline unsigned char produce(uint64_t site,Producer original,uint64_t a,uint64_t b,float radius,float geometry,uint64_t actor=0){
    uint32_t r{},g{};memcpy(&r,&radius,4);memcpy(&g,&geometry,4);
    ++evaluating;++writer_epoch; // writer visibility survives stopped admission
    Invocation s(site,evaluation,a,b,r,g);observe_producer(s,a,b,actor,before);
    unsigned char result{};
    __try{result=original(a,b,radius,geometry);}
    __finally{if(!AbnormalTermination())observe_producer(s,a,b,actor,after);s.finish(AbnormalTermination()!=0,result);++writer_epoch;--evaluating;}
    return result;
}
inline void model(Invocation& s,uint64_t payload){
    if(!s.admitted)return;
    auto vtable=pointer(payload-0x28);
    if(vtable!=base+0x4c75ce8||pointer(vtable+0x58)!=base+0x38a050){s.e.status|=0x1000;s.e.output={};return;}
    copy(s.e.output,payload,0x98);
    // Payload header read is non-atomic. The actual constructed row boundary
    // below supplies IRES association; this read alone never does.
}
inline void rows(Invocation& s,uint64_t payload){
    model(s,payload);auto begin=field<uint64_t>(s.e.output,0x38),end=field<uint64_t>(s.e.output,0x40);
    if(!s.e.output.ok||end<begin||(end-begin)%0x170||(end&&(!begin||end>0x7fffffffffffULL))){s.e.status|=0x400;return;}
    if((end-begin)/0x170>256){s.e.status|=0x2000;failed();return;}
    Event e=s.e;e.kind=model_row;e.phase=after;
    for(auto p=begin;p<end;p+=0x170){e.operand={};copy(e.operand,p,0x170);e.args[3]=(p-begin)/0x170;e.status=e.operand.ok?0:2;e.qpc=tick();if(!spool.emit(e))break;}
}
inline void observe_integral_before(Invocation& s,Tag tag,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t resource,uint64_t payload){
    if(!s.admitted)return;
    Environment preserve;try{
        s.e.phase=before;
        s.e.reference=resource;if(resource)copy(s.e.base,resource,0x30);
        if(tag==source_visit){
            copy(s.e.ref,a,0x18);copy(s.e.operand,c,8);
            auto source=field<uint64_t>(s.e.operand,0);s.e.reference=source;
            if(source)copy(s.e.base,source,0x40);
            // The native caller holds ProcGen's shared lock. No geometry walk.
        }
        if(tag==provider){
            copy(s.e.ref,b,8);copy(s.e.base,a,0x78);copy(s.e.output,c,8);
            // Pre/post headers are samples outside the provider's inner lock.
        }
        if(tag==ui){s.e.command=a;copy(s.e.aux,a,0x20);copy(s.e.extra,b,0x40);
            populations(s,base+0x5f5d800);copy(s.e.operand,base+0x5efb1f0,8);copy(s.e.cell,field<uint64_t>(s.e.operand,0),0x30);model(s,b+0x58);}
        if(tag==region||tag==atmosphere){s.e.phase=before;forms(s,tag==region?0:1,b,c);copy(s.e.aux,d,0x18);}
        if(tag==water_append){copy(s.e.operand,b,8);auto p=field<uint64_t>(s.e.operand,0);if(p)copy(s.e.base,p,0x30);}
        if(tag==row){model(s,payload);auto start=field<uint64_t>(s.e.output,0x38),end=field<uint64_t>(s.e.output,0x40);
            s.e.command=s.e.output.ok&&end>=start&&(end-start)%0x170==0?(end-start)/0x170:UINT64_MAX;}
        s.send(before,0);
    }catch(...){failed();}
}
inline void observe_integral_after(Invocation& s,uint64_t site,Tag tag,uint64_t a,uint64_t b,uint64_t d,uint64_t payload,uint64_t result){
    if(!s.admitted)return;
    Environment preserve;try{
            s.e.phase=after;
            if(tag==queue)s.e.command=result;
            if(tag==provider){copy(s.e.base,a,0x78);copy(s.e.output,s.e.args[2],8);}
            if(tag==region||tag==atmosphere)copy(s.e.output,d,0x18);
            if(tag==water_append)copy(s.e.output,a,0x18);
            if(tag==row){model(s,payload);
                // Existing-capacity constructor destination is RDX. Growth
                // path returns the inserted destination. Final ordinal census
                // handles relocation of earlier rows.
                copy(s.e.operand,site==0x15787e9?b:result,0x170);}
            if(tag==ui){populations(s,base+0x5f5d800);copy(s.e.extra,b,0x40);rows(s,b+0x58);}
    }catch(...){failed();}
}
inline uint64_t integral(uint64_t site,Tag tag,Four original,uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t resource=0,uint64_t payload=0){
    Invocation s(site,tag,a,b,c,d);observe_integral_before(s,tag,a,b,c,d,resource,payload);
    uint64_t result{};
    __try{result=original(a,b,c,d);}
    __finally{if(!AbnormalTermination())observe_integral_after(s,site,tag,a,b,d,payload,result);s.finish(AbnormalTermination()!=0,result);}
    return result;
}
}
