// SPDX-License-Identifier: GPL-3.0-or-later
// Independent exact-object register, atomic, argument and Windows unwind oracle.
#define NOMINMAX
#include <Windows.h>
#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <stdexcept>
#include <algorithm>
using U=uint64_t;
namespace winner {std::atomic<bool> enabled{true};}
#include "d5an_counter.h"
extern "C" {
 std::atomic<U> D5AM_watched_lock{},D5AM_watched_state{},D5AM_generation{17},D5AM_registry_serial{2};
 std::atomic<U> D5AM_sched_counter_faults{};
 std::atomic<U> abi_core_active{},D5AM_causal_bridge_active{},D5AM_causal_counter_faults{};
 std::atomic<bool> abi_enabled{true};
 U D5AM_causal_core_active=U(&abi_core_active),D5AM_causal_enabled=U(&abi_enabled),D5AM_causal_fixture_before_operation{},D5AM_causal_fixture_before_admission{};
 std::atomic<U> D5AM_recursive_release_site{0xabc123};
 void D5AM_pending(),D5AM_acquired(),D5AM_recursive(),D5AM_reader(),D5AM_reader_release(),D5AM_writer_release(),D5AM_recursive_release(),D5AM_reader_ready();
 void D5AM_inline_writer_release(),D5AM_inline_recursive_release();
 void d5am_probe_inline_writer_release(void*,void*),d5am_probe_inline_recursive_release(void*,void*);
 void d5am_probe_pending(void*,void*),d5am_probe_acquired(void*,void*),d5am_probe_recursive(void*,void*),d5am_probe_reader(void*,void*),d5am_probe_reader_release(void*,void*),d5am_probe_writer_release(void*,void*),d5am_probe_recursive_release(void*,void*),d5am_probe_reader_ready(void*,void*);
}
unsigned checks{},unwinds{},calls{};U observed_lock{},observed_old{},observed_kind{},observed_generation{},observed_serial{},observed_site{},observed_delta{},observed_owner{};
void check(bool value){++checks;if(!value)throw std::runtime_error("D5AM independent ABI assertion");}
extern "C" void D5AM_record(U lock,U old,U kind,U generation,U serial,U site){
 ++calls;observed_lock=lock;observed_old=uint32_t(old);observed_owner=old>>32;observed_kind=uint32_t(kind);observed_delta=kind>>32;observed_generation=generation;observed_serial=serial;observed_site=site;
}
U word(const unsigned char* p){U value{};memcpy(&value,p,8);return value;}
struct Test {void(*probe)(void*,void*);void(*bridge)();unsigned kind;uint32_t state,after;U rax,rsi;bool release;};
Test tests[]{
 {d5am_probe_pending,D5AM_pending,2,0x1000,0x2000,0x1000,0x6161,false},
 {d5am_probe_acquired,D5AM_acquired,3,0x401000,0x401000,0x1000,0x6161,false},
 {d5am_probe_recursive,D5AM_recursive,4,0x401000,0x801000,0x101,0x401000,false},
 {d5am_probe_reader,D5AM_reader,5,0x1000,0x1001,0x1000,0x6161,false},
 {d5am_probe_reader_release,D5AM_reader_release,6,0x1001,0x1000,0x1001,0x6161,true},
 {d5am_probe_writer_release,D5AM_writer_release,7,0x401000,0,0x401000,0x6161,true},
 {d5am_probe_recursive_release,D5AM_recursive_release,8,0x801000,0x401000,0x801000,0x6161,true},
 {d5am_probe_reader_ready,D5AM_reader_ready,15,0,0,0x101,0x6161,false},
 {d5am_probe_inline_writer_release,D5AM_inline_writer_release,17,0x401000,0,0x101,0x6161,false},
 {d5am_probe_inline_recursive_release,D5AM_inline_recursive_release,18,0x801000,0x401000,0x101,0x6161,false}
};
void abi(){
 for(unsigned watched=0;watched<3;++watched)for(const auto& t:tests){
  alignas(16) unsigned char result[256]{};uint32_t lock[2]{0,t.state};calls=0;
  abi_enabled=watched!=2;D5AM_watched_lock=watched?U(lock):0;D5AM_watched_state=watched?U(lock)+4:0;
  t.probe(result,lock);
  const U expected[]{t.rax,t.kind>=17?U(t.state):t.release?U(lock)+4:U(0x102),t.kind==6?U(t.state):U(0x103),
   0x108,0x109,0x110,0x111,t.kind==15?U(0x7777):U(0x7000),U(lock)+(t.kind>=17?0:4),0x1212,0x1313,U(lock),U(result),0x4545};
  for(unsigned i=0;i<14;++i)check(word(result+i*8)==expected[i]);
  check(word(result+224)==word(result+240));check(word(result+248)==t.rsi);
  check(lock[1]==t.after);check(lock[0]==(t.kind==3?0x4545u:0u));
  for(unsigned i=128;i<224;++i)check(result[i]==0xff);
  check(calls==(watched==1?1u:0u));
  if(watched==1){check(observed_lock==U(lock));check(observed_kind==(t.kind>=17?t.kind-10:t.kind));
   if(t.kind>=17)check(observed_owner==0);
   if(t.kind>=17)check(observed_delta==(t.kind==17?0xffbff000u:0xffc00000u));check(observed_generation==17&&observed_serial==2);
   check(observed_site!=0);
   check(observed_old==(t.kind==15?U(0):t.kind==3?U(0x1000):U(t.state)));}
  U flags=word(result+112);
  if(t.kind==3||t.kind==5||t.kind==7)check((flags&0x8d5)==0x44);
  if(t.kind==6||t.kind==8||t.kind>=17)check((flags&1)==1);
 }
 abi_enabled=true;
}
void publish_during_operation(U receiver,U kind){
 check(abi_core_active==1&&D5AM_causal_bridge_active==1);
 U lock=kind==5||kind==6||kind==7||kind==8||kind==15?receiver-4:receiver;
 D5AM_watched_lock=lock;D5AM_watched_state=lock+4;D5AM_generation=19;D5AM_registry_serial=4;
}
void disable_before_admission(U,U){check(abi_core_active==0&&D5AM_causal_bridge_active==0);abi_enabled=false;}
void transition_and_counters(){
 const auto& t=tests[0];alignas(16) unsigned char result[256]{};uint32_t lock[2]{0,t.state};
 calls=0;D5AM_watched_lock=0;D5AM_watched_state=0;D5AM_generation=17;D5AM_registry_serial=2;
 D5AM_causal_fixture_before_operation=U(&publish_during_operation);t.probe(result,lock);D5AM_causal_fixture_before_operation=0;
 check(calls==1&&observed_generation==17&&observed_serial==2&&D5AM_generation==19&&D5AM_registry_serial==4);
 check(lock[1]==t.after&&abi_core_active==0&&D5AM_causal_bridge_active==0);
 D5AM_generation=17;D5AM_registry_serial=2;
 for(auto* counter:{&abi_core_active,&D5AM_causal_bridge_active}){
  *counter=UINT64_MAX;calls=0;lock[1]=t.state;D5AM_causal_counter_faults=0;t.probe(result,lock);
  check(counter->load()==UINT64_MAX&&D5AM_causal_counter_faults==1&&calls==0&&lock[1]==t.after);
  *counter=0;check(abi_core_active==0&&D5AM_causal_bridge_active==0);
 }
 D5AM_causal_counter_faults=0;
 calls=0;lock[1]=t.state;D5AM_causal_fixture_before_admission=U(&disable_before_admission);
 t.probe(result,lock);D5AM_causal_fixture_before_admission=0;
 check(!abi_enabled&&calls==0&&lock[1]==t.after&&abi_core_active==0&&D5AM_causal_bridge_active==0&&D5AM_causal_counter_faults==0);
 abi_enabled=true;
 calls=0;lock[0]=0x11223344;lock[1]=0x401000;tests[8].probe(result,lock);
 check(calls==1&&observed_owner==0x11223344&&observed_delta==0xffbff000&&observed_old==0x401000&&lock[0]==0x11223344&&lock[1]==0);
}
void virtual_context(U pc,unsigned pushes,unsigned allocation,bool framed,bool extra=false){
 alignas(16) U stack[256]{};U sp=U(stack)+1024,caller=0x123456789,old_rbp=0x12345000;
 *(U*)sp=caller;*(U*)(sp-8)=old_rbp;
 CONTEXT c{};c.ContextFlags=CONTEXT_FULL;c.Rip=pc;c.Rsp=sp-pushes*8-allocation-(extra?8:0);c.Rbp=framed?sp-pushes*8-allocation:old_rbp;
 DWORD64 image{};auto* table=RtlLookupFunctionEntry(pc,&image,nullptr);check(table!=nullptr);
 void* handler{};DWORD64 establisher{};RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,pc,table,&c,&handler,&establisher,nullptr);
 check(c.Rip==caller&&c.Rsp==sp+8&&c.Rbp==old_rbp);++unwinds;
}
void unwind(){
 for(const auto& t:tests){
  U entry=U(t.bridge);DWORD64 image{};auto* table=RtlLookupFunctionEntry(entry,&image,nullptr);check(table!=nullptr);
  auto* info=(unsigned char*)(image+table->UnwindData);auto* code=(unsigned char*)entry;
  unsigned allocation=(t.kind==7||t.kind==8)?168:160;
  unsigned char save[]{0x55,0x9c,0x50,0x51,0x52,0x41,0x50,0x41,0x51,0x41,0x52,0x41,0x53,0x48,0x81,0xec,0x90,0,0,0,0x48,0x8b,0xec};save[16]=(unsigned char)allocation;
  auto* end=(unsigned char*)(image+table->EndAddress);auto* begin=std::search(code,end,std::begin(save),std::end(save));check(begin!=end);
  check(info[1]==U(begin+sizeof save)-entry);
  virtual_context(entry,0,0,false);
  const unsigned offsets[]{0,1,2,3,4,5,7,9,11,13};
  for(unsigned i=0;i<10;++i)virtual_context(U(begin)+offsets[i],i,0,false);
  virtual_context(U(begin)+20,9,allocation,false);virtual_context(U(begin)+23,9,allocation,true);
  unsigned char flags[]{0xff,0xb4,0x24,0xc8,0,0,0};flags[3]=(unsigned char)(allocation+56);
  auto* restore=std::search(begin+23,end,std::begin(flags),std::end(flags));check(restore!=end&&restore[7]==0x9d);
  virtual_context(U(restore)+7,9,allocation,true,true);
  unsigned char epilogue[]{0x48,0x8d,0xa5,0xd0,0,0,0,0x5d,0xc3};epilogue[3]=(unsigned char)(allocation+64);
  auto* tail=std::search(begin+23,end,std::begin(epilogue),std::end(epilogue));check(tail!=end);
  virtual_context(U(tail),9,allocation,true);virtual_context(U(tail)+7,1,0,true);
 }
}
int main(){SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);try{abi();transition_and_counters();unwind();printf("{\"checks\":%u,\"unwind_contexts\":%u,\"bridges\":10,\"watched_and_unwatched\":true,\"disabled_native_paths\":true,\"status\":\"PASS\"}\n",checks,unwinds);return 0;}catch(const std::exception& e){fprintf(stderr,"%s checks=%u unwind=%u kind=%llu\n",e.what(),checks,unwinds,(unsigned long long)observed_kind);return 1;}}
