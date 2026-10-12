// SPDX-License-Identifier: GPL-3.0-or-later
#include "health.h"
#include <thread>
#include <vector>
#include <iostream>
using namespace oracle;
#define ENTRY(N) extern "C" uint64_t route_entry_##N(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);extern "C" unsigned char route_call_##N[];
ENTRY(0) ENTRY(1) ENTRY(2) ENTRY(3) ENTRY(4) ENTRY(5) ENTRY(6) ENTRY(7) ENTRY(8) ENTRY(9) ENTRY(10)
extern "C" uint64_t test_producer_entry(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
extern "C" void route_fp_mutate(const uint16_t*);
alignas(16) thread_local unsigned char native_fp[512]{};
extern "C" uint64_t abi_probe(Callback,uint64_t,uint64_t);
extern "C" uint64_t fixture_center(uint64_t,uint64_t){return 0;}
extern "C" uint64_t fixture_selector(uint64_t,uint64_t,uint64_t){return 0;}
extern "C" uint32_t fixture_query_body(uint64_t,uint64_t){return 0;}
extern "C" uint32_t fixture_enum_body(uint64_t,uint64_t,uint64_t){return 0;}
unsigned checks{};void require(bool b,const char* name){if(!b)throw std::runtime_error(name);++checks;std::cout<<"PASS "<<name<<'\n';}
uint64_t addr(const void* p){return reinterpret_cast<uint64_t>(p);}
thread_local unsigned scenario{},recursion{};thread_local bool selection_produces{};
struct Fixture {alignas(8) unsigned char owner[0x30]{},angles[16]{},request[64]{},selected[0x390]{},ref[0xd0]{},base[0x30]{},cell[0x118]{},world[0x390]{},land[0x60]{},source[44]{};int xy[2]{-17,23};
 Fixture(){uint64_t b=addr(base);memcpy(ref+0x98,&b,8);b=addr(cell);memcpy(ref+0xb0,&b,8);b=addr(world);memcpy(cell+0x110,&b,8);uint32_t id=0x2c60e9;memcpy(base+0x28,&id,4);id=0xff010203;memcpy(ref+0x28,&id,4);id=256;memcpy(land+0x50,&id,4);id=0x3f59f;memcpy(land+0x54,&id,4);id=88327;memcpy(land+0x58,&id,4);id=15;memcpy(land+0x5c,&id,4);float xyz[]{-1701.25f,2311.5f,12.75f};memcpy(ref+0x8c,xyz,12);double a[]{-.219,-.511};memcpy(request,a,16);}
 uint64_t call(){return route_entry_0(addr(owner),addr(angles),addr(request),addr(selected),addr(ref),0x1122334455667788,1);}
};
thread_local Fixture* current{};
extern "C" uint64_t route_native_1(uint64_t a,uint64_t b,uint64_t c){if(a!=addr(current->ref)||b!=0x5566||c!=0x7788)throw std::runtime_error("eligibility args");return scenario==0?0xaabbccdd00000001:0;}
extern "C" uint64_t route_native_2(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t f,uint64_t g){if(a!=addr(current->ref)||b!=addr(current->request)||c!=b||d!=0x99||g)throw std::runtime_error("search six channels");memcpy(reinterpret_cast<void*>(f),current->ref+0x8c,12);return scenario==1?addr(current->ref):0;}
extern "C" uint64_t route_native_3(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t f){if(a!=addr(current->owner)||b!=addr(current->request)||c!=b||d!=0x99)throw std::runtime_error("fallback stack channel");memcpy(reinterpret_cast<void*>(f),current->ref+0x8c,12);return scenario==2?addr(current->ref):0;}
extern "C" uint64_t route_native_4(uint64_t a,uint64_t b,uint64_t c){if(a!=addr(current->land)||c!=addr(current->request))throw std::runtime_error("source args");memset(reinterpret_cast<void*>(b),0,44);*reinterpret_cast<uint8_t*>(b)=1;int v=54;memcpy(reinterpret_cast<void*>(b+4),&v,4);v=110;memcpy(reinterpret_cast<void*>(b+8),&v,4);return b;}
extern "C" uint64_t route_native_5(uint64_t a,uint64_t b,uint64_t c){if(a!=addr(current->land)||b!=addr(current->source)||c!=addr(current->xy))throw std::runtime_error("grid args");if(scenario==4)throw std::runtime_error("native C++ exception");if(scenario==5)RaiseException(0xe1234567,0,0,nullptr);if(scenario==6&&!recursion){++recursion;current->call();--recursion;}if(scenario==7)gate.stop();int x=54*192+current->xy[0],y=110*192+current->xy[1];int fields[]{x/192,y/192,x%192/12,y%192/12,x%12,y%12};unsigned offsets[]{4,8,0x14,0x18,0x24,0x28};for(unsigned i=0;i<6;++i)memcpy(reinterpret_cast<void*>(b+offsets[i]),fields+i,4);if(scenario==8){uint16_t cw=0x0b7f;route_fp_mutate(&cw);_mm_setcsr((_mm_getcsr()&~0x6000)|0x4001);SetLastError(0xbeef);_fxsave64(native_fp);}return 0xfedcba9876543210;}
extern "C" uint64_t route_native_6(uint64_t a,uint64_t b,uint64_t c,uint64_t d){if(a!=addr(current->land)||c!=addr(current->source)||d!=c)throw std::runtime_error("delta args");int v[]{-17,23};memcpy(reinterpret_cast<void*>(b),v,8);return b;}
extern "C" uint64_t route_native_7(uint64_t a,uint64_t b,uint64_t c){if(a!=addr(current->selected))throw std::runtime_error("identity arg");uint32_t v=0x3f59f;memcpy(reinterpret_cast<void*>(b),&v,4);memcpy(reinterpret_cast<void*>(c),current->request,16);return 1;}
extern "C" uint64_t route_native_8(uint64_t a,uint64_t b,uint64_t c,uint64_t d){if(a!=addr(current->selected)||b!=0x123||c!=0x456||d!=0x789)throw std::runtime_error("selection args");if(selection_produces)current->call();return 0xabc;}
extern "C" uint64_t route_native_10(uint64_t a,uint64_t b,uint64_t c){return route_native_7(a,b,c);}
uint64_t natural_producer(uint64_t a,uint64_t b,uint64_t c,uint64_t d){if(a!=addr(current->owner)||b!=addr(current->angles)||c!=0x3f59f||d!=addr(current->request))throw std::runtime_error("producer args");return current->call();}
extern "C" uint64_t route_native_9(uint64_t a,uint64_t b,uint64_t c){return route_native_7(a,b,c);}
extern "C" uint64_t route_native_0(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t f,uint64_t g,uint64_t h){
 if(a!=addr(current->owner)||b!=addr(current->angles)||c!=addr(current->request)||d!=addr(current->selected)||f!=addr(current->ref)||g!=0x1122334455667788||h!=1)throw std::runtime_error("route seven args");
 unsigned char translated[12]{};auto eligible=scenario==9?1:route_entry_1(f,0x5566,0x7788,0,0,0,0);uint64_t chosen=eligible&0xff?f:route_entry_2(f,c,c,0x99,addr(translated),0,0);
 if(!chosen)chosen=route_entry_3(a,c,c,0x99,addr(translated),0,0);
 if(!chosen&&scenario!=4&&scenario!=5&&scenario!=6&&scenario!=7&&scenario!=8)return b;
 if(!chosen)chosen=f;memcpy(current->owner+0x18,&chosen,8);memcpy(current->owner+0x20,current->ref+0x8c,12);
 uint32_t body{};unsigned char angles[16]{};if(scenario==9)route_entry_10(d,addr(&body),addr(angles),0,0,0,0);else route_entry_7(d,addr(&body),addr(angles),0,0,0,0);
 route_entry_4(addr(current->land),addr(current->source),c,0,0,0,0);int delta[2]{};route_entry_6(addr(current->land),addr(delta),addr(current->source),addr(current->source),0,0,0);
 route_entry_5(addr(current->land),addr(current->source),addr(current->xy),0,0,0,0);memcpy(current->angles,current->request,16);return b;
}
bool seh(){__try{current->call();return false;}__except(GetExceptionCode()==0xe1234567?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}}
bool producer_seh(){__try{test_producer_entry(addr(current->owner),addr(current->angles),0x3f59f,addr(current->request),addr(current->selected),addr(current->request));return false;}__except(GetExceptionCode()==0xe1234567?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}}
uint64_t producer_abi_thunk(uint64_t a,uint64_t,uint64_t){current=reinterpret_cast<Fixture*>(a);return test_producer_entry(addr(current->owner),addr(current->angles),0x3f59f,addr(current->request),addr(current->selected),addr(current->request));}
uint64_t abi_thunk(uint64_t a,uint64_t,uint64_t){current=reinterpret_cast<Fixture*>(a);return current->call();}
int main(int argc,char** argv){try{
 unsigned block=10,merge=2;float scale=.01f;settings_addresses[0]=addr(&block);settings_addresses[1]=addr(&merge);settings_addresses[2]=addr(&scale);queue=new Queue<4096>();original_route=route_native_0;original_eligible=route_native_1;original_search=route_native_2;original_route_fallback=route_native_3;original_route_source=route_native_4;original_route_grid=route_native_5;original_route_delta=route_native_6;original_identity=route_native_7;original_selected=route_native_8;original_selected_body=route_native_9;original_producer=natural_producer;
 unsigned char* sites[]{route_call_0,route_call_1,route_call_2,route_call_3,route_call_4,route_call_5,route_call_6,route_call_7,route_call_8,route_call_9,route_call_10};uint64_t hooks[]{addr(&route_hook),addr(&eligible_hook),addr(&search_hook),addr(&route_fallback_hook),addr(&route_source_hook),addr(&route_grid_hook),addr(&route_delta_hook),addr(&identity_hook),addr(&selected_hook),addr(&selected_body_hook),addr(&direct_identity_hook)};
 auto page=islands(addr(sites[0]));require(page!=nullptr,"route relay allocation");Edit edits[11];for(unsigned i=0;i<11;++i){island(page+i*16,hooks[i]);require(sites[i][0]==0xe8&&call_edit(edits[i],addr(sites[i]),addr(page+i*16)),"complete CALL encoding");memcpy(edits[i].before,sites[i],5);}DWORD old{};require(VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)&&FlushInstructionCache(GetCurrentProcess(),page,4096),"route RX relay publish");
 auto start=GetTickCount64();while(!sole_thread()&&GetTickCount64()-start<120000)Sleep(100);bool dirty{};edits[9].before[1]^=1;require(sole_thread()&&!install(edits,11,true,dirty)&&!dirty&&match(edits[0],false),"last route guard rejects all writes");edits[9].before[1]^=1;require(install(edits,11,true,dirty),"eleven disposable observation sites installed");
 std::vector<Event> all;Event e;Fixture fixture;current=&fixture;
 for(unsigned n=0;n<10;++n){scenario=n;gate.state=0;SetLastError(0x1234);auto mx=_mm_getcsr();bool fault=false;try{if(n==5)fault=seh();else require(current->call()==addr(current->angles),"route full RAX return");}catch(const std::runtime_error&){fault=true;}
 require(fault==(n==4||n==5),"route native exception propagation");require(depth==0&&suppressed==0&&(gate.state.load()&~stop_bit)==0,"route unwind and STOP lifetime drain");require(GetLastError()==(n==8?0xbeef:0x1234),"route native LastError effects preserved");require(_mm_getcsr()==(n==8?((mx&~0x6000)|0x4001):mx),"route native MXCSR effects preserved");if(n==8){alignas(16) unsigned char after[512]{};_fxsave64(after);require(!memcmp(after,native_fp,5)&&!memcmp(after+24,native_fp+24,4),"native x87 control status and MXCSR effects preserved");}_mm_setcsr(mx);
 std::vector<Event> run;while(queue->pop(e)){run.push_back(e);all.push_back(e);}require(run.front().kind==22&&run.back().kind==(fault?24:23),"route boundary pairing");unsigned grid_count=0;for(auto& ev:run){if(ev.kind==33){++grid_count;require(ev.candidate.ok&&ev.floor_xy.ok&&ev.landscape.ok&&ev.landscape.length==0x60,"fresh generic grid native operands");require(ev.ref.address==addr(fixture.ref)&&field<uint64_t>(ev.context_raw,0x18)==addr(fixture.ref),"chosen native ref owner binding");require(field<uint64_t>(ev.block,8)==addr(route_call_5)+5,"actual source CALL return address");}if(ev.kind==34)require(field<int>(ev.candidate,4)==53&&field<int>(ev.candidate,8)==110&&field<int>(ev.candidate,0x24)==7&&field<int>(ev.candidate,0x28)==11&&field<uint64_t>(ev.result,0)==0xfedcba9876543210,"in-place grid output and RAX separate");}
 require(grid_count==(n==3?0:n==6?2:1),"no-hit nested and positive generic observations");if(n==6){bool nested=false;for(auto& ev:run)nested|=ev.kind==22&&ev.parent==run[0].invocation;require(nested,"nested route ancestry");}}
 scenario=0;gate.state=0;require(abi_probe(abi_thunk,addr(current),0)==0,"route eight GPR ten XMM nonvolatile preservation");while(queue->pop(e)){}
 for(unsigned rounding=0;rounding<4;++rounding){auto mx=_mm_getcsr();_mm_setcsr((0x1f80|(rounding<<13))^(rounding&1?0x8040:0));scenario=0;auto before=_mm_getcsr();current->call();require(_mm_getcsr()==before,"route rounding FTZ DAZ control survives");_mm_setcsr(mx);while(queue->pop(e)){}}
 gate.state=0;require(route_entry_8(addr(fixture.selected),0x123,0x456,0x789,0,0,0)==0xabc,"standalone sentinel selection preserved");uint32_t body{};unsigned char a[16]{};require(route_entry_9(addr(fixture.selected),addr(&body),addr(a),0,0,0,0)==1,"standalone explicit selection preserved");while(queue->pop(e)){all.push_back(e);require(e.ref.ok&&e.ref.length==0x390,"selected reference identity raw bytes");}
 // Actual producer bridge transports native RDI/RSI without changing them.
 selection_produces=true;gate.state=0;scenario=0;route_entry_8(addr(fixture.selected),0x123,0x456,0x789,0,0,0);selection_produces=false;
 uint64_t selected_invocation{};bool sentinel_bound=false;while(queue->pop(e)){all.push_back(e);if(e.kind==40)selected_invocation=e.invocation;if(e.kind==22)sentinel_bound=e.parent==selected_invocation;}require(sentinel_bound,"sentinel selection encloses actual route ancestry");
 gate.state=0;require(test_producer_entry(addr(fixture.owner),addr(fixture.angles),0x3f59f,addr(fixture.request),addr(fixture.selected),addr(fixture.request))==addr(fixture.angles),"explicit producer bridge native return");
 uint64_t producer_invocation{};bool producer_bound=false;while(queue->pop(e)){all.push_back(e);if(e.kind==48){producer_invocation=e.invocation;require(e.reference==addr(fixture.selected)&&field<uint64_t>(e.input_hierarchy,24)==addr(fixture.request),"bridge selected reference and exact request preserved");}if(e.kind==22)producer_bound=e.parent==producer_invocation;}require(producer_bound,"explicit selection producer encloses route ancestry");
 gate.state=0;scenario=0;require(abi_probe(producer_abi_thunk,addr(current),0)==0,"producer bridge all nonvolatile GPR XMM preserved");while(queue->pop(e)){}
 for(unsigned kind:{4u,5u}){gate.state=0;scenario=kind;bool caught=false;try{if(kind==5)caught=producer_seh();else producer_abi_thunk(addr(current),0,0);}catch(const std::runtime_error&){caught=true;}require(caught&&depth==0&&(gate.state.load()&~stop_bit)==0,"producer bridge C++ SEH unwind metadata and lifetime");while(queue->pop(e))all.push_back(e);}
 // Optional reads fail explicitly; the healthy acquisition and native call survive.
 manager_slot=1;gate.state=0;scenario=0;current->call();bool unreadable=false;while(queue->pop(e)){unreadable|=!e.world.ok;all.push_back(e);}require(unreadable&&lost==0,"unreadable optional manager is nonfatal");manager_slot=0;
 // Failed native setting must remain invalid independently of readable call attribution.
 settings_addresses[0]=1;merge=12;gate.state=0;scenario=0;current->call();bool invalid_setting=false;while(queue->pop(e)){if(e.kind==33)invalid_setting=e.block.ok&&e.block.address==1&&field<uint32_t>(e.block,4)==0&&field<uint64_t>(e.block,8)==addr(route_call_5)+5;all.push_back(e);}require(invalid_setting,"unreadable block retains false native validity independent of callsite");settings_addresses[0]=addr(&block);merge=2;
 // Cyclic optional lists set sampled status bits; unwind discriminator stays exact.
 alignas(8) unsigned char list[16]{},node[24]{};uint64_t np=addr(node),lp=addr(list);memcpy(list+8,&np,8);memcpy(node+8,&np,8);memcpy(fixture.ref+0xc8,&lp,8);memcpy(fixture.selected+0xc8,&lp,8);
 for(uint64_t observed_node:{addr(node),uint64_t(1)}){memcpy(list+8,&observed_node,8);gate.state=0;scenario=4;try{producer_abi_thunk(addr(current),0,0);}catch(const std::runtime_error&){}bool child_tag=false,selection_tag=false;while(queue->pop(e)){if(e.kind==39)child_tag=e.status==33;if(e.kind==44)selection_tag=e.status==48;all.push_back(e);}require(child_tag&&selection_tag&&depth==0,"cyclic or unreadable optional metadata cannot corrupt child or selection unwind tag");}lp=0;memcpy(fixture.ref+0xc8,&lp,8);memcpy(fixture.selected+0xc8,&lp,8);

 std::vector<std::thread> threads;for(unsigned i=0;i<4;++i)threads.emplace_back([i]{Fixture f;f.xy[0]-=int(i);current=&f;scenario=i%3;for(unsigned j=0;j<10;++j)f.call();});for(auto& t:threads)t.join();unsigned count{};while(queue->pop(e)){++count;all.push_back(e);}require(count>400&&lost==0&&depth==0,"concurrent distinct reference frame coordinates no loss");
 for(auto& edit:edits)require(write(edit,false)&&match(edit,false),"disposable fixture restoration");
 if(argc>1){std::ofstream f(argv[1],std::ios::binary);for(auto& ev:all)f.write(reinterpret_cast<const char*>(&ev),sizeof ev);require(f.good(),"fixture primary raw evidence written");}
 std::cout<<"PASS checks="<<checks<<'\n';return 0;
 }catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
