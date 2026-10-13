// SPDX-License-Identifier: GPL-3.0-or-later
#include "health.h"
#include <thread>
#include <vector>
#include <iostream>
using namespace oracle;
extern "C" uint64_t abi_probe(Callback,uint64_t,uint64_t);
// Link-only symbols for the retained generic ABI probe's object. Never called.
extern "C" uint64_t fixture_center(uint64_t,uint64_t){return 0;}
extern "C" uint64_t fixture_selector(uint64_t,uint64_t,uint64_t){return 0;}
extern "C" uint32_t fixture_query_body(uint64_t,uint64_t){return 0;}
extern "C" uint32_t fixture_enum_body(uint64_t,uint64_t,uint64_t){return 0;}
#define ENTRY(N) extern "C" uint64_t branch_entry_##N(uint64_t,uint64_t,uint64_t,uint64_t);extern "C" unsigned char branch_call_##N[];
ENTRY(0) ENTRY(1) ENTRY(2) ENTRY(3) ENTRY(4) ENTRY(5) ENTRY(6)
thread_local unsigned scenario{};
thread_local unsigned char form[0x30]{},overlay_bytes[0x34]{},land[0x58]{};
thread_local uint64_t expected[4]{};
thread_local unsigned native_calls{};
alignas(16) thread_local unsigned char native_fp[512]{};
extern "C" void branch_fp_mutate(const uint16_t*);
unsigned checks{};
void require(bool b,const char* label){if(!b)throw std::runtime_error(label);++checks;std::cout<<"PASS "<<label<<'\n';}
uint64_t addr(const void* p){return reinterpret_cast<uint64_t>(p);}
void arguments(uint64_t a,uint64_t b=0,uint64_t c=0,uint64_t d=0){if(a!=expected[0]||b!=expected[1]||c!=expected[2]||d!=expected[3])throw std::runtime_error("argument forwarding");++native_calls;}
extern "C" uint64_t branch_native_0(uint64_t a,uint64_t b,uint64_t c){arguments(a,b,c);if(scenario==8)throw std::runtime_error("original C++ fault");return scenario<2?0:addr(form);}
extern "C" uint64_t branch_native_1(uint64_t a){arguments(a);return scenario==0?0:addr(form);}
extern "C" uint64_t branch_native_2(uint64_t a,uint64_t b){arguments(a,b);return scenario==2?0:addr(overlay_bytes);}
extern "C" uint64_t branch_native_3(uint64_t a,uint64_t b,uint64_t c){arguments(a,b,c);memset(reinterpret_cast<void*>(b),0,44);return 0x1111222233334444;}
extern "C" uint64_t branch_native_4(uint64_t a,uint64_t b,uint64_t c){arguments(a,b,c);memset(reinterpret_cast<void*>(b),0,44);if(scenario==4)*reinterpret_cast<unsigned char*>(b)=1;if(scenario==12){uint16_t cw=0x0b7f;branch_fp_mutate(&cw);_mm_setcsr((_mm_getcsr()&~0x6000)|0x4001);SetLastError(0xbeef);_fxsave64(native_fp);}return 0xaaaabbbbccccdddd;}
extern "C" uint64_t branch_native_5(uint64_t a,uint64_t b,uint64_t c){arguments(a,b,c);memset(reinterpret_cast<void*>(b),0x5a,44);return 0xabcddcba12344321;}
extern "C" uint64_t branch_native_6(uint64_t a,uint64_t b,uint64_t c,uint64_t d){arguments(a,b,c,d);if(scenario==9)RaiseException(0xe1234567,0,0,nullptr);int delta[2]{-17,23};memcpy(reinterpret_cast<void*>(b),delta,8);return 0xfedcba9876543210;}
uint64_t call(unsigned n,uint64_t a,uint64_t b=0,uint64_t c=0,uint64_t d=0){
    expected[0]=a;expected[1]=b;expected[2]=c;expected[3]=d;
    Helper4 entries[]{branch_entry_0,branch_entry_1,branch_entry_2,branch_entry_3,branch_entry_4,branch_entry_5,branch_entry_6};auto v=entries[n](a,b,c,d);
    uint64_t wanted=n==0?(scenario<2?0:addr(form)):n==1?(scenario==0?0:addr(form)):n==2?(scenario==2?0:addr(overlay_bytes)):n==3?0x1111222233334444:n==4?0xaaaabbbbccccdddd:n==5?0xabcddcba12344321:0xfedcba9876543210;
    if(v!=wanted)throw std::runtime_error("helper RAX forwarding");return v;
}
uint32_t natural_query(uint64_t ctx,uint64_t candidate){
    auto finish=[&]{return static_cast<uint32_t>(*reinterpret_cast<uint8_t*>(*reinterpret_cast<uint64_t*>(ctx+8))!=0);};
    auto v=call(0,pointer(ctx+16),0x87654321,candidate);
    if(!v){v=call(1,0x87654321);if(!v||form[0x2e]!=0x56)return finish();}
    if(!call(2,pointer(ctx),v)||scenario==3)return finish();
    unsigned char a[44]{},b[44]{};call(3,addr(land),addr(a),candidate);
    if(scenario==10)gate.stop();
    call(4,addr(land),addr(b),0x02b20e7843e090c0);
    if(scenario==11){auto saved=scenario;scenario=0;query_hook(ctx,candidate);scenario=saved;}
    if(scenario>=6&&scenario!=8&&scenario!=10&&scenario!=11)q_enum_entry(0x99,0x88,0);
    if(scenario==7||scenario==9||scenario==10){
        auto source=pointer(ctx+32);call(5,addr(land),addr(a),source);int delta[2]{};
        call(6,addr(land),addr(delta),addr(a),addr(b));
    }
    return finish();
}
bool seh_query(uint64_t c,uint64_t d){__try{query_hook(c,d);return false;}__except(GetExceptionCode()==0xe1234567?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}}
int main(int argc,char** argv){try{
    queue=new Queue<4096>();original_query=natural_query;
    original_resolver=branch_native_0;original_fallback=branch_native_1;original_overlay=branch_native_2;
    original_a=branch_native_3;original_b=branch_native_4;original_angular=branch_native_5;original_delta=branch_native_6;
    unsigned char* sites[]{branch_call_0,branch_call_1,branch_call_2,branch_call_3,branch_call_4,branch_call_5,branch_call_6};
    uint64_t targets[]{addr(&resolver_hook),addr(&fallback_hook),addr(&overlay_hook),addr(&a_hook),addr(&b_hook),addr(&angular_hook),addr(&delta_hook)};
    auto page=islands(addr(sites[0]));require(page!=nullptr,"seven helper relays allocated");Edit edits[7];
    for(unsigned i=0;i<7;++i){island(page+i*16,targets[i]);require(sites[i][0]==0xe8&&call_edit(edits[i],addr(sites[i]),addr(page+i*16)),"complete synthetic helper CALL");memcpy(edits[i].before,sites[i],5);}
    unsigned char windows[7][32]{};for(unsigned i=0;i<7;++i)memcpy(windows[i],sites[i],32);
    DWORD old{};require(VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)&&FlushInstructionCache(GetCurrentProcess(),page,4096),"RX relays published");
    auto start=GetTickCount64();while(!sole_thread()&&GetTickCount64()-start<120000)Sleep(100);
    bool dirty{};edits[6].before[1]^=1;
    require(sole_thread()&&!install(edits,7,true,dirty)&&!dirty&&match(edits[0],false),"last helper preimage conflict refuses entire transaction");edits[6].before[1]^=1;
    require(install(edits,7,true,dirty),"seven helper edits installed in sole-thread disposable process");
    for(unsigned i=0;i<7;++i)require(match(edits[i],true)&&relay_guard(page+i*16,targets[i]),"helper edit and relay integrity");
    for(unsigned i=0;i<7;++i){unsigned char b[32]{};memcpy(b,sites[i],32);original_window(b,addr(sites[i]),32,edits,7);require(!memcmp(b,windows[i],32),"overlapping guard restores all owned CALL bytes");b[31]^=1;require(memcmp(b,windows[i],32)!=0,"unowned guard drift remains detectable");}
    unsigned char world[0x390]{},candidate[24]{},source[24]{};uint64_t packed=0x02b20e7843e090c0;memcpy(world+0x310,&packed,8);
    uint8_t latch=1;int rect[4]{0,1,2,3};uint32_t key=0x87654321;memcpy(candidate+16,&key,4);
    uint64_t owner{},ctx[5]{addr(&owner),addr(&latch),addr(world),addr(rect),addr(source)};
    std::vector<Event> all;Event e;
    for(unsigned n=0;n<=11;++n){
        gate.state=0;scenario=n;form[0x2e]=n==1?0x55:0x56;native_calls=0;latch=(n==4||n==5||n==6||n==11)?0:1;SetLastError(0x123456);auto fp=_mm_getcsr();
        bool fault=false;try{if(n==9)fault=seh_query(addr(ctx),addr(candidate));else query_hook(addr(ctx),addr(candidate));}catch(const std::runtime_error&){fault=true;}
        require(fault==(n==8||n==9),"native normal C++ and SEH outcomes preserved");
        require(depth==0&&suppressed==0&&(gate.state.load()&~stop_bit)==0,"helper and Q unwind lifetime drained");
        require(GetLastError()==0x123456&&_mm_getcsr()==fp,"helper FP and LastError preservation");
        std::vector<Event> run;while(queue->pop(e)){run.push_back(e);all.push_back(e);}
        require(run.front().kind==query_begin&&run.back().kind==(fault?query_unwind:query_end),"ordered Q association boundaries");
        require(field<uint64_t>(run.front().floor_xy,0)==packed&&run.front().source.ok&&run.front().source.address==addr(source),"packed key and context4 pointee domains");
        for(auto& ev:run)if(ev.kind>=13){require(ev.thread==run.front().thread,"helper thread association");if(ev.kind==q_b)require(ev.candidate.ok&&ev.source.ok&&ev.candidate.length==44&&ev.source.length==44,"both private hierarchy buffers captured after B");if(ev.kind==q_delta)require(field<int>(ev.translation,0)==-17&&field<int>(ev.translation,4)==23&&field<uint64_t>(ev.result,0)==0xfedcba9876543210,"four arguments output bytes and full RAX");}
        if(n==10)require(run.size()==8&&run[4].kind==q_b&&run[6].kind==q_delta,"admitted Q continues observations after STOP");
        if(n==11)require(run[5].parent==run[0].invocation&&run[5].invocation!=run[0].invocation,"nested Q ancestry independent of matching input values");
    }
    gate.state=0;scenario=7;form[0x2e]=0x56;
    require(abi_probe(reinterpret_cast<Callback>(&query_hook),addr(ctx),addr(candidate))==0,"helper chain all nonvolatile GPR XMM sentinels");while(queue->pop(e)){}
    alignas(16) unsigned char saved_fp[512]{},after_fp[512]{};_fxsave64(saved_fp);
    for(unsigned rounding=0;rounding<4;++rounding){
        scenario=12;_mm_setcsr((0x1f80|(rounding<<13))^(rounding&1?0x8040:0));SetLastError(0x2222);
        query_hook(addr(ctx),addr(candidate));_fxsave64(after_fp);
        require(GetLastError()==0xbeef&&!memcmp(after_fp,native_fp,5)&&!memcmp(after_fp+24,native_fp+24,4),"native x87 control status MXCSR LastError effects survive observer in all rounding modes");while(queue->pop(e)){}
    }
    _fxrstor64(saved_fp);
    // Unreadable source has explicit failed status; no unchecked dereference by observer.
    ctx[4]=1;scenario=0;query_hook(addr(ctx),addr(candidate));queue->pop(e);require(!e.source.ok&&e.source.address==1,"unreadable pointee explicitly recorded");while(queue->pop(e)){}ctx[4]=addr(source);
    std::vector<std::thread> threads;for(int j=0;j<4;++j)threads.emplace_back([&]{scenario=7;form[0x2e]=0x56;for(int k=0;k<20;++k)query_hook(addr(ctx),addr(candidate));});for(auto& t:threads)t.join();
    unsigned count{};while(queue->pop(e))++count;require(count==720&&lost==0,"four concurrent Q helper chains no loss");
    if(argc>1){HANDLE h=CreateFileA(argv[1],GENERIC_WRITE,0,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);require(h!=INVALID_HANDLE_VALUE,"exclusive synthetic evidence file");for(auto& ev:all)require(durable_append(h,&ev,sizeof ev,true),"each synthetic branch record flushed");CloseHandle(h);}
    for(auto& edit:edits)require(write(edit,false)&&match(edit,false),"disposable helper sites restored");
    std::cout<<"TOTAL "<<checks<<'\n';return 0;
}catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
