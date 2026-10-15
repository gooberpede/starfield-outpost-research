// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable in-process native fixture, never loads/opens Starfield or SFSE.
#include "capture.h"
#include <thread>
#include <vector>
#include <cassert>
using namespace preview;
struct Form {unsigned char bytes[0x30]{};Form(uint32_t id){memcpy(bytes+0x28,&id,4);bytes[0x2e]=0x9f;}};
Form iron(0x57c7),alkanes(0x57c9),helium(0x57f5),domain(0x123456),fixture_beacon_base(0xabc123),water(0x83ec);
unsigned char actor_header[0xd8]{};
uint64_t simple[]={reinterpret_cast<uint64_t>(&iron)},mixed[]={reinterpret_cast<uint64_t>(&iron),reinterpret_cast<uint64_t>(&alkanes)},air[]={reinterpret_cast<uint64_t>(&helium)};
struct State {uint64_t v[9]{};unsigned char padding[0x20]{};};
struct Position {float x,y,z;uint32_t frame;uint64_t domain;};
unsigned char native(uint64_t a,uint64_t b,float radius,float geometry){
    assert(radius==150.f&&geometry==23.f);assert(GetLastError()==0x2468);auto& s=*reinterpret_cast<State*>(a);auto& p=*reinterpret_cast<Position*>(b);
    auto data=p.x<10?simple:mixed;unsigned n=p.x<10?1:2;s.v[0]=reinterpret_cast<uint64_t>(data);s.v[1]=s.v[0]+n*8;s.v[2]=s.v[1];
    s.v[3]=reinterpret_cast<uint64_t>(air);s.v[4]=s.v[3]+8;s.v[5]=s.v[4];SetLastError(0x7654);return 1;
}
unsigned char throwing(uint64_t,uint64_t,float,float){throw std::runtime_error("fixture_native_exception");}
unsigned char cached(uint64_t,uint64_t,float,float){return 0;}
uint64_t allocate_command(uint64_t a,uint64_t,uint64_t,uint64_t){return a;}
unsigned char seh_fault(uint64_t,uint64_t,float,float){RaiseException(0xe0123456,0,0,nullptr);return 0;}
void propagate_seh(uint64_t a,uint64_t b){__try{produce(85,seh_fault,a,b,150,23);}__except(GetExceptionCode()==0xe0123456?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){}}
std::atomic<unsigned> barrier{};
unsigned char simultaneous(uint64_t,uint64_t,float,float){++barrier;while(barrier<2)std::this_thread::yield();Sleep(2);return 0;}
unsigned char nested(uint64_t a,uint64_t b,float c,float d){produce(81,throwing,a,b,c,d);return 0;}
extern "C" unsigned char preview_producer(uint64_t a,uint64_t b,float c,float d,uint64_t actor){assert(actor==reinterpret_cast<uint64_t>(actor_header));return produce(0x21b42e3,native,a,b,c,d,actor);}
extern "C" unsigned char invoke_preview(uint64_t,uint64_t,float,float,uint64_t);
extern "C" uint64_t invoke_fast(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
extern "C" uint64_t invoke_grow(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
extern "C" uint32_t abi_probe(Four,uint64_t,uint64_t);
extern "C" uint64_t fixture_writer(uint64_t,uint64_t,uint64_t,uint64_t){return 0;}
uint64_t mixed_abi(uint64_t a,uint64_t b,uint64_t,uint64_t){return invoke_preview(a,b,150,23,reinterpret_cast<uint64_t>(actor_header));}
struct Display {unsigned char bytes[0x170]{};};
Display storage[8];uint64_t ui_model[0x200/8]{};
uint64_t union_noop(uint64_t,uint64_t,uint64_t,uint64_t){return 0;}
uint64_t ctor(uint64_t,uint64_t dest,uint64_t source,uint64_t){memcpy(reinterpret_cast<void*>(dest),reinterpret_cast<void*>(source),sizeof(Display));return dest;}
uint64_t grow(uint64_t container,uint64_t dest,uint64_t source,uint64_t d){
    auto p=reinterpret_cast<uint64_t*>(container);auto r=ctor(0,dest,source,d);p[1]+=0x170;return r;
}
extern "C" uint64_t row_fast(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t resource,uint64_t payload){return integral(0x15787e9,row,ctor,a,b,c,d,resource,payload);}
extern "C" uint64_t row_grow(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t resource,uint64_t payload){return integral(0x15787fc,row,grow,a,b,c,d,resource,payload);}
uint64_t native_ui(uint64_t,uint64_t modelptr,uint64_t c,uint64_t d){
    assert(c==0x1234&&d==0x5678);
    auto ptrs=reinterpret_cast<uint64_t*>(base+0x5f5d800);
    auto payload=modelptr+0x58;auto vec=reinterpret_cast<uint64_t*>(payload+0x38);
    vec[0]=reinterpret_cast<uint64_t>(storage);vec[1]=vec[0];vec[2]=vec[0]+sizeof(storage);
    integral(0x15785c9,region,union_noop,1,ptrs[0],ptrs[1],0);
    integral(0x15785e8,atmosphere,union_noop,2,ptrs[3],ptrs[4],0);
    std::vector<uint64_t> merged;
    for(unsigned k:{0U,3U})for(auto p=ptrs[k];p<ptrs[k+1];p+=8){auto r=*reinterpret_cast<uint64_t*>(p);if(r&&std::find(merged.begin(),merged.end(),r)==merged.end())merged.push_back(r);}
    for(auto p=ptrs[6];p<ptrs[7];p+=8){auto r=*reinterpret_cast<uint64_t*>(p);auto selector=*reinterpret_cast<uint64_t*>(base+0x5efb1f0);
        if(selector&&*reinterpret_cast<uint32_t*>(r+0x28)==*reinterpret_cast<uint32_t*>(selector+0x28)){
            integral(0x157862e,water_append,union_noop,0,reinterpret_cast<uint64_t>(&r),0,0);merged.push_back(r);}}
    for(auto r:merged){Display temp;memcpy(temp.bytes,"fixture display",15);auto index=(vec[1]-vec[0])/0x170;
        bool expanding=index%2!=0;(expanding?invoke_grow:invoke_fast)(expanding?reinterpret_cast<uint64_t>(vec):0,vec[1],reinterpret_cast<uint64_t>(&temp),0,r,payload);
        if(!expanding)vec[1]+=0x170;
    }
    *reinterpret_cast<unsigned char*>(payload+0x90)=1;return 0;
}
int main(int argc,char** argv){
    assert(argc==2);auto root=fs::path(argv[1]);fs::create_directories(root);assert(spool.open(root));
    State s;Position p{0,0,0,7,reinterpret_cast<uint64_t>(&domain)};domain.bytes[0x2e]=0x49;auto bp=reinterpret_cast<uint64_t>(&fixture_beacon_base);memcpy(actor_header+0x98,&bp,8);
    // Stationary player is deliberately absent from the observation interface.
    // A,A,A,B,C have position changes; C restores SET A at a different point.
    for(float x:{1.f,2.f,3.f,20.f,4.f}){p.x=x;SetLastError(0x2468);auto fp=_mm_getcsr();assert(invoke_preview(reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p),150,23,reinterpret_cast<uint64_t>(actor_header))==1);assert(GetLastError()==0x7654&&_mm_getcsr()==fp);}
    p.x=5;assert(produce(0x21b42e3,cached,reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p),150,23,reinterpret_cast<uint64_t>(actor_header))==0);
    // Two queued command identities are delivered in reverse order. Neither
    // contains resources or position; delivery uses the then-current vectors.
    uint64_t command_a[4]{},command_b[4]{};auto qa=reinterpret_cast<uint64_t>(command_a),qb=reinterpret_cast<uint64_t>(command_b);
    integral(0x15784a0,queue,allocate_command,qa,0,0,0);integral(0x15784a0,queue,allocate_command,qb,0,0,0);
    // Independent UI-consumer and final-row channel. UI delivery can occur
    // after B then C; it consumes C, never a fabricated enqueue snapshot.
    base=reinterpret_cast<uint64_t>(VirtualAlloc(nullptr,0x6000000,MEM_RESERVE,PAGE_READWRITE));assert(base);
    assert(VirtualAlloc(reinterpret_cast<void*>(base+0x5f5d000),0x1000,MEM_COMMIT,PAGE_READWRITE));
    assert(VirtualAlloc(reinterpret_cast<void*>(base+0x5efb000),0x2000,MEM_COMMIT,PAGE_READWRITE));
    assert(VirtualAlloc(reinterpret_cast<void*>(base+0x4c75000),0x2000,MEM_COMMIT,PAGE_READWRITE));
    *reinterpret_cast<uint64_t*>(base+0x4c75d40)=base+0x38a050;ui_model[0x30/8]=base+0x4c75ce8;
    memcpy(reinterpret_cast<void*>(base+0x5f5d800),s.v,0x48);
    integral(0x1581a96,ui,native_ui,qb,reinterpret_cast<uint64_t>(ui_model),0x1234,0x5678);
    SetLastError(0x2468);assert(abi_probe(mixed_abi,reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p))==0);
    // Third-source selected water duplicates are kept; unrelated biome form is
    // filtered. A second pointer for the same common FormID remains distinct.
    uint64_t special[]={reinterpret_cast<uint64_t>(&water),reinterpret_cast<uint64_t>(&alkanes),reinterpret_cast<uint64_t>(&water)};
    auto vectors=reinterpret_cast<uint64_t*>(base+0x5f5d800);vectors[6]=reinterpret_cast<uint64_t>(special);vectors[7]=vectors[6]+sizeof(special);vectors[8]=vectors[7];*reinterpret_cast<uint64_t*>(base+0x5efb1f0)=reinterpret_cast<uint64_t>(&water);
    integral(0x1581a96,ui,native_ui,qa,reinterpret_cast<uint64_t>(ui_model),0x1234,0x5678);
    integral(0x1581a96,ui,native_ui,qa,reinterpret_cast<uint64_t>(ui_model),0x1234,0x5678);
    uint64_t unknown_common[]={1};vectors[0]=reinterpret_cast<uint64_t>(unknown_common);vectors[1]=vectors[0]+8;vectors[2]=vectors[1];
    integral(0x1581a96,ui,native_ui,0,reinterpret_cast<uint64_t>(ui_model),0x1234,0x5678);
    VirtualFree(reinterpret_cast<void*>(base),0,MEM_RELEASE);base=0;
    bool caught=false;try{produce(0x21b42e3,throwing,reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p),150,23);}catch(const std::runtime_error&){caught=true;}assert(caught&&spool.active==0&&parent==0);
    caught=false;try{produce(82,nested,reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p),150,23);}catch(const std::runtime_error&){caught=true;}assert(caught&&spool.active==0&&parent==0);
    auto concurrent=[&](){produce(83,simultaneous,reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p),150,23);};std::thread overlap(concurrent);concurrent();overlap.join();
    propagate_seh(reinterpret_cast<uint64_t>(&s),reinterpret_cast<uint64_t>(&p));assert(spool.active==0&&parent==0&&evaluating==0);
    // Unknown ID and invalid/partial input are explicit population records.
    Invocation missing(77,region,0,0,0,0);missing.e.phase=before;
    forms(missing,0,1,9);missing.send(before,0);missing.finish(false,0);
    uint64_t badresource[]={1};Invocation unknown(80,region,0,0,0,0);unknown.e.phase=before;
    forms(unknown,0,reinterpret_cast<uint64_t>(badresource),reinterpret_cast<uint64_t>(badresource)+8);unknown.send(before,0);unknown.finish(false,0);
    auto pages=static_cast<unsigned char*>(VirtualAlloc(nullptr,8192,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));assert(pages);DWORD old{};assert(VirtualProtect(pages+4096,4096,PAGE_NOACCESS,&old));
    uint64_t partialresource[]={reinterpret_cast<uint64_t>(pages+4096-0x20)};Invocation partial(86,region,0,0,0,0);partial.e.phase=before;
    forms(partial,0,reinterpret_cast<uint64_t>(partialresource),reinterpret_cast<uint64_t>(partialresource)+8);partial.send(before,0);partial.finish(false,0);VirtualFree(pages,0,MEM_RELEASE);
    // High rate, nested/concurrent scopes: no deduplication/sample quotas.
    auto run=[](){for(int i=0;i<1000;++i){Invocation outer(78,queue,0,0,0,0);outer.send(before,0);Invocation inner(79,queue,0,0,0,0);inner.send(before,0);inner.finish(false,42);outer.finish(false,43);}};
    std::thread t(run);run();t.join();
    spool.stop();assert(spool.active==0&&spool.flush()&&spool.failed==0);
    assert(write_new(root/L"retired.json","{"+spool.counts()+"}\n"));spool.close();
    // Storage faults are exercised against fresh disposable files.
    auto fault=root/L"fault";fs::create_directory(fault);Spool broken;assert(broken.open(fault));broken.fail_sequence=1;Event e{};assert(!broken.emit(e)&&broken.failed==1&&broken.stopping&&broken.broken);broken.close();
    auto diskfail=root/L"disk-fault";fs::create_directory(diskfail);Spool diskbroken;assert(diskbroken.open(diskfail));fixture_disk_query_failure=true;assert(!diskbroken.emit(e)&&diskbroken.failed==1);fixture_disk_query_failure=false;diskbroken.close();
    assert(evaluating==0);puts("PASS five set controls, ABI mixed floats, exception propagation, 2000 nested concurrent scopes, explicit reads, high-rate WAL and storage faults");
}
