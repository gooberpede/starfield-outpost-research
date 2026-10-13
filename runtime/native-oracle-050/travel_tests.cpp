// SPDX-License-Identifier: GPL-3.0-or-later
#include "travel.h"
#include <thread>
#include <vector>
#include <fstream>
#include <iostream>
#include <stdexcept>
using namespace oracle;
extern "C" uint64_t test_travel_producer(uint64_t,uint64_t,uint64_t,uint64_t,const uint64_t*);
extern "C" uint64_t test_travel_command(uint64_t,uint64_t,uint64_t,uint64_t,const uint64_t*);
extern "C" uint64_t abi_probe(Callback,uint64_t,uint64_t);
extern "C" void travel_fp_mutate(const uint16_t*);
alignas(16) thread_local unsigned char native_fp[512]{};
extern "C" uint64_t fixture_center(uint64_t,uint64_t){return 0;}
extern "C" uint64_t fixture_selector(uint64_t,uint64_t,uint64_t){return 0;}
extern "C" uint32_t fixture_query_body(uint64_t,uint64_t){return 0;}
extern "C" uint32_t fixture_enum_body(uint64_t,uint64_t,uint64_t){return 0;}
unsigned checks{};void require(bool b,const char* text){if(!b)throw std::runtime_error(text);++checks;std::cout<<"PASS "<<text<<'\n';}
uint64_t address(const void* p){return reinterpret_cast<uint64_t>(p);}
struct Fixture {unsigned char request[64]{},output[40]{},target[0xd0]{},angles[16]{},candidate[0xd0]{},command[0x98]{},state[0x98]{};
 uint64_t observed[12]{};
 Fixture(){observed[0]=0x12345678;observed[2]=1;observed[3]=address(target);observed[4]=address(angles);observed[5]=address(candidate);observed[6]=0x777;observed[7]=0x888;observed[8]=0x55;observed[9]=2;observed[10]=0x999;request[0x38]=1;command[0x8d]=1;command[0x8e]=2;}
 uint64_t producer(){return test_travel_producer(0xabc,address(output),0x3f59f,address(request),observed);}
 uint64_t handoff(){return test_travel_command(address(state),address(command),0,0,observed);}
};
thread_local Fixture* current{};thread_local unsigned mode{},nested{};
uint64_t native_route(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t){return 0x123;}
uint64_t native_producer(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 if(a!=0xabc||b!=address(current->output)||c!=0x3f59f||d!=address(current->request))throw std::runtime_error("native producer channels");
 if(mode==1)throw std::runtime_error("native failure");if(mode==2)RaiseException(0xe1234567,0,0,nullptr);
 if(mode==3&&!nested){++nested;current->producer();--nested;}
 if(mode==4)gate.stop();
 if(mode==6)route_hook(address(current->output),address(current->angles),address(current->request),address(current->target),0,0,0);
 if(mode==5){uint16_t cw=0x0b7f;travel_fp_mutate(&cw);_mm_setcsr((_mm_getcsr()&~0x6000)|0x4001);SetLastError(0xcafe);_fxsave64(native_fp);}
 current->output[0]=0xaa;return 0xfedcba9876543210;
}
uint64_t native_command(uint64_t a,uint64_t b){if(a!=address(current->state)||b!=address(current->command))throw std::runtime_error("native command channels");if(mode==1)throw std::runtime_error("command failure");if(mode==2)RaiseException(0xe1234567,0,0,nullptr);memcpy(current->state,current->command,0x98);return 0x9876543210abcdef;}
uint64_t thunk(uint64_t a,uint64_t b,uint64_t){current=reinterpret_cast<Fixture*>(a);return b?current->handoff():current->producer();}
bool seh(bool command){__try{if(command)current->handoff();else current->producer();return false;}__except(GetExceptionCode()==0xe1234567?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}}
int main(int argc,char** argv){try{
 queue=new Queue<4096>();original_travel_producer=native_producer;original_travel_command=native_command;
 std::vector<Event> all;Event e;Fixture f;current=&f;
 for(bool command:{false,true})for(unsigned scenario=0;scenario<6;++scenario){mode=scenario;gate.state=0;auto mx=_mm_getcsr();SetLastError(0x1234);bool fault=false;
  try{if(mode==2)fault=seh(command);else require((command?f.handoff():f.producer())==(command?0x9876543210abcdefULL:0xfedcba9876543210ULL),"full native return");}catch(const std::runtime_error&){fault=true;}
  require(fault==(mode==1||mode==2),"C++ and SEH propagate");require(!depth&&!suppressed&&!(gate.state.load()&~stop_bit),"unwind and STOP drain");
  require(GetLastError()==(!command&&mode==5?0xcafe:0x1234),"native LastError effects preserved");require(_mm_getcsr()==(!command&&mode==5?((mx&~0x6000)|0x4001):mx),"native MXCSR effects preserved");
  if(!command&&mode==5){alignas(16) unsigned char after[512]{};_fxsave64(after);require(!memcmp(after,native_fp,5)&&!memcmp(after+24,native_fp+24,4),"native x87 control status and MXCSR effects survive");}_mm_setcsr(mx);
  std::vector<Event> rows;while(queue->pop(e)){all.push_back(e);rows.push_back(e);}
  uint64_t tag=command?53:50;require(rows.front().kind==tag&&rows.back().kind==tag+(fault?2:1),"boundaries paired or explicit unwind");
  auto& start=rows.front();require(field<uint64_t>(start.block,0)==0x12345678&&field<uint64_t>(start.block,16)==1&&field<uint64_t>(start.block,64)==0x55&&field<uint64_t>(start.block,72)==2&&field<uint64_t>(start.block,80)==0x999,"bridge caller decision and native stack values");
  require(start.parent==0,"post-return command and standalone producer are unassociated");
  if(!command&&mode==3)require(rows.size()==4&&rows[1].parent==start.invocation,"nested producer parent retained");
  if(!fault)require(rows.back().candidate.ok&&rows.back().candidate.bytes[0]==(command?0:0xaa),"output capture readable");
 }
 mode=6;gate.state=0;original_route=native_route;f.producer();uint64_t parent{};bool route_bound=false;while(queue->pop(e)){all.push_back(e);if(e.kind==50)parent=e.invocation;if(e.kind==22)route_bound=parent&&e.parent==parent;}require(route_bound,"native route scope enclosed by travel producer");
 mode=0;gate.state=0;require(abi_probe(thunk,address(&f),0)==0&&abi_probe(thunk,address(&f),1)==0,"bridges preserve all nonvolatile GPR and XMM channels");while(queue->pop(e))all.push_back(e);
 for(unsigned r=0;r<4;++r){auto mx=_mm_getcsr();_mm_setcsr(0x1f80|(r<<13)|(r&1?0x8040:0));auto before=_mm_getcsr();f.producer();f.handoff();require(_mm_getcsr()==before,"rounding FTZ DAZ survive observation");_mm_setcsr(mx);while(queue->pop(e))all.push_back(e);}
 gate.stop();auto prior=invocations.load();f.producer();f.handoff();require(invocations.load()==prior&&!queue->pop(e),"inert STOP still executes originals");
 gate.state=0;f.observed[3]=1;f.producer();bool unreadable=false;while(queue->pop(e)){all.push_back(e);unreadable|=!e.ref.ok;}require(unreadable,"unreadable target remains explicitly invalid");f.observed[3]=address(f.target);
 gate.state=0;std::vector<std::thread> threads;for(unsigned i=0;i<4;++i)threads.emplace_back([]{Fixture local;current=&local;mode=0;for(unsigned j=0;j<8;++j){local.producer();local.handoff();}});for(auto& t:threads)t.join();unsigned count{};while(queue->pop(e)){++count;all.push_back(e);}require(count==128&&!lost,"concurrent independent scopes no loss");
 if(argc>1){std::ofstream file(argv[1],std::ios::binary);for(auto& row:all)file.write(reinterpret_cast<const char*>(&row),sizeof row);require(file.good(),"primary fixture events written");}
 std::cout<<"PASS checks="<<checks<<'\n';return 0;
 }catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
