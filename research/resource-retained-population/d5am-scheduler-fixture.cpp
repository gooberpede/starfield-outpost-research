// SPDX-License-Identifier: GPL-3.0-or-later
// Owned disposable host only. Models native-owned task backing and callback
// operands; it does not execute retail tasks or model their scheduling frequency.
#define SOR_SCHED_EXTERNAL_CAPTURE
#include "../../runtime/construction-winner/d5am_scheduler.h"
#include <thread>
#include <vector>
namespace winner {
std::filesystem::path session;
std::string identity_hash;
bool disk(U){return true;}
}
extern "C" {void D5AM_sched_fixture_clobber();void D5AM_sched_probe_fall();
__declspec(dllexport) void D5AM_sched_probe(uint64_t,uint64_t,void*);
unsigned char D5AM_fixture_server[256]{},D5AM_fixture_tree[256]{},D5AM_fixture_write[16]{};
unsigned char D5AM_fixture_context[256]{};
uint64_t D5AM_fixture_command[4]{},D5AM_fixture_command_pointer=uint64_t(D5AM_fixture_command)|1;
uint64_t D5AM_fixture_server_pointer=uint64_t(D5AM_fixture_server),D5AM_fixture_node_pointer{};
uint64_t D5AM_fixture_dispatch_argument=0x8888888888888888ULL;
}
namespace {
using namespace winner;namespace sched=winner::scheduler;
U tables[3][4]{},nested_node{},invocations{},backtrace_count{};bool synchronous{};
bool mismatched_request{};
bool mutate_ready_tree{};U replacement_serial{};
std::atomic<HANDLE> pause_ready{},pause_continue{};
std::atomic<HANDLE> admission_ready{},admission_continue{};
std::atomic<U> admission_phase{},original_calls{};
std::atomic<bool> admission_once{};
void admission_wait(U phase) noexcept {
 PreserveError preserve;
 if(phase!=admission_phase.load()||!admission_once.exchange(false))return;
 auto ready=admission_ready.load(),next=admission_continue.load();
 D5AM_sched_fixture_clobber();SetEvent(ready);WaitForSingleObject(next,INFINITE);
}
U worker(U a,U,U,U){
 ++original_calls;
 Scope scope{};Scope* previous=current;scope.e.invocation=++invocations;scope.e.selection=invocations+100;
 scope.e.source=0x111111;read(a,scope.e.request,8);current=&scope;
 if(mismatched_request)scope.e.request[0]^=1;
 sched::provider();if(nested_node){U inner=nested_node;nested_node=0;sched::callback<1>(inner+0xb0,0,0,0);sched::provider();}
 current=previous;return 0x55;
}
U registration(U a,U,U node,U){
 ++original_calls;
 if(synchronous){auto c=sched::cookie(node);sched::capture(node,sched::Activated,a,&c);sched::capture(node,sched::Dispatch,a,&c);sched::callback<0>(node+0xb0,0,0,0);}
 return 0x123456;
}
U claim(U,U result,U,U,U){++original_calls;return result;}
U publish(U,U,U,U){++original_calls;return 0x123;}
}
extern "C" __declspec(dllexport) void D5AM_sched_capture_admitted(uint64_t node,uint64_t kind,uint64_t server,
 const winner::scheduler::Cookie* consumed) noexcept {
 winner::PreserveError preserve;
 if(auto ready=pause_ready.load()){auto next=pause_continue.load();SetEvent(ready);WaitForSingleObject(next,INFINITE);}
 D5AM_sched_fixture_clobber();void* stack[16]{};backtrace_count=RtlCaptureStackBackTrace(0,16,stack,nullptr);
 winner::scheduler::capture(node,kind,server,consumed,true);
}
extern "C" __declspec(dllexport) void D5AM_sched_dispatch_admitted(uint64_t node,uint64_t server,
 const winner::scheduler::Cookie* consumed,uint64_t argument) noexcept {
 winner::PreserveError preserve;
 if(auto ready=pause_ready.load()){auto next=pause_continue.load();SetEvent(ready);WaitForSingleObject(next,INFINITE);}
 D5AM_sched_fixture_clobber();void* stack[16]{};backtrace_count=RtlCaptureStackBackTrace(0,16,stack,nullptr);
 winner::scheduler::capture(node,winner::scheduler::Dispatch,server,consumed,true,argument);
}
extern "C" __declspec(dllexport) void D5AM_sched_ready_admitted(uint64_t node,uint64_t server,
 const winner::scheduler::Cookie* consumed,uint64_t serial) noexcept {
 winner::PreserveError preserve;
 if(mutate_ready_tree)memcpy(D5AM_fixture_tree+0x50,&replacement_serial,8);
 D5AM_sched_fixture_clobber();void* stack[16]{};backtrace_count=RtlCaptureStackBackTrace(0,16,stack,nullptr);
 winner::scheduler::capture(node,winner::scheduler::ReadyTreeBefore,server,consumed,true,serial);
}
extern "C" __declspec(dllexport) bool D5AM_sched_command_capture(uint64_t context,uint64_t address,uint64_t kind,
 uint64_t route,winner::scheduler::Event* out) noexcept {
 winner::PreserveError preserve;D5AM_sched_fixture_clobber();
 return out&&winner::scheduler::command_event(context,address,kind,route,*out);
}
extern "C" __declspec(dllexport) uint64_t D5AM_initialize(){
 using namespace winner;
 if(!sched::avx_ready())return 0;
 enabled=false;winner::active=0;sched::enqueue=0;sched::dequeue=0;sched::active=0;sched::drops=0;sched::reentrant=0;sched::tokens=0;sched::registry_faults=0;sched::identity_faults=0;sched::failed=false;counter_overflow=false;D5AM_sched_counter_faults=0;
 for(U i=0;i<sched::capacity;++i)sched::queue[i].ticket=i;
 for(auto& slot:D5AM_sched_registry){slot.node=0;slot.serial=0;slot.allocation=0;slot.key_low=0;slot.key_high=0;slot.live=0;slot.vtable=0;slot.server=0;}
 for(unsigned i=0;i<3;++i){D5AM_sched_vtables[i]=U(tables[i]);D5AM_sched_falls[i]=U(&D5AM_sched_probe_fall);}
 for(auto& original:sched::registration_original)original=&registration;
 sched::density_original=&worker;sched::layer_original=&worker;sched::claim_original=&claim;sched::queue_original=&publish;
 sched::callback_target=0x123456780;D5AM_sched_callback_target=sched::callback_target;
 sched::begun=true;enabled=true;invocations=0;synchronous=false;nested_node=0;sched::task_scope=nullptr;sched::scope_cookie=nullptr;
 pause_ready=nullptr;pause_continue=nullptr;uint64_t serial=0x123456789;memcpy(D5AM_fixture_tree+0x50,&serial,8);
 D5AM_sched_bridge_active=0;
 D5AM_sched_fixture_admission=0;
 D5AM_fixture_dispatch_argument=0x8888888888888888ULL;
 mismatched_request=false;
 mutate_ready_tree=false;replacement_serial=0;memset(D5AM_fixture_write,0,sizeof D5AM_fixture_write);
 admission_once=false;admission_ready=nullptr;admission_continue=nullptr;original_calls=0;
 D5AM_fixture_command[1]=0x123456780;D5AM_fixture_command[3]=uint64_t(D5AM_fixture_server);
 return 1;
}
extern "C" __declspec(dllexport) uint64_t D5AM_vtable(unsigned i){return i<3?D5AM_sched_vtables[i]:0;}
extern "C" __declspec(dllexport) uint64_t D5AM_vtable_guard(uint64_t address,uint64_t base,const char* hash){return hash&&winner::scheduler::vtable_digest(address,base)==hash;}
extern "C" __declspec(dllexport) uint64_t D5AM_target_guard(uint64_t address,const char* hash){return winner::scheduler::target_guard(address,hash);}
extern "C" __declspec(dllexport) void D5AM_dispatch_argument(uint64_t value){D5AM_fixture_dispatch_argument=value;}
extern "C" __declspec(dllexport) void D5AM_ready_serial(uint64_t value,uint64_t replacement,unsigned mutate){
 memcpy(D5AM_fixture_tree+0x50,&value,8);replacement_serial=replacement;mutate_ready_tree=bool(mutate);
}
extern "C" __declspec(dllexport) uint64_t D5AM_register(uint64_t node,unsigned sync){synchronous=bool(sync);auto result=winner::scheduler::registration<0>(U(D5AM_fixture_server),0,node,0);synchronous=false;return result;}
extern "C" __declspec(dllexport) void D5AM_stage(uint64_t node,uint64_t kind){auto c=winner::scheduler::cookie(node);winner::scheduler::capture(node,kind,0,&c);}
extern "C" __declspec(dllexport) void D5AM_cookie(uint64_t node,winner::scheduler::Cookie* out){*out=winner::scheduler::cookie(node);}
extern "C" __declspec(dllexport) void D5AM_stale(uint64_t node,const winner::scheduler::Cookie* c){winner::scheduler::capture(node,winner::scheduler::Dispatch,0,c);}
extern "C" __declspec(dllexport) uint64_t D5AM_callback(uint64_t node,uint64_t nested){nested_node=nested;return winner::scheduler::callback<0>(node+0xb0,0,0,0);}
extern "C" __declspec(dllexport) uint64_t D5AM_request_mismatch(uint64_t node){mismatched_request=true;auto result=winner::scheduler::callback<0>(node+0xb0,0,0,0);mismatched_request=false;return result;}
extern "C" __declspec(dllexport) uint64_t D5AM_claim(uint64_t context,uint64_t result){return D5AM_sched_claim_entry(0,result,context,1,0);}
extern "C" __declspec(dllexport) uint64_t D5AM_claim_pool(uint64_t context,uint64_t result,uint64_t pool){return D5AM_sched_claim_entry(pool,result,context,1,0);}
extern "C" __declspec(dllexport) uint64_t D5AM_publish(uint64_t context,uint64_t command){return D5AM_sched_queue_entry(context,command,0,0);}
extern "C" __declspec(dllexport) void D5AM_admission_pause(uint64_t ready,uint64_t next,uint64_t phase){
 admission_phase=phase;admission_ready=(HANDLE)ready;admission_continue=(HANDLE)next;admission_once=true;
 D5AM_sched_fixture_admission=uint64_t(&admission_wait);
}
extern "C" __declspec(dllexport) uint64_t D5AM_action(unsigned action,uint64_t node,uint64_t context,uint64_t command){
 using namespace winner::scheduler;
 switch(action){
  case 0:return winner::scheduler::registration<0>(U(D5AM_fixture_server),0,node,0);
  case 1:return winner::scheduler::registration<1>(U(D5AM_fixture_server),0,node,0);
  case 2:return winner::scheduler::registration<2>(U(D5AM_fixture_server),0,node,0);
  case 3:return winner::scheduler::registration<3>(U(D5AM_fixture_server),0,node,0);
  case 4:return callback<0>(node+0xb0,0,0,0);
  case 5:return callback<1>(node+0xb0,0,0,0);
  case 6:return publish_queue(context,command,0,0);
  case 7:return winner::scheduler::claim(U(D5AM_fixture_server),command,context,1,0);
  case 8:{Scope scope{};scope.e.invocation=77;scope.e.selection=88;scope.e.source=0x111111;
   read(node+0xb0,scope.e.request,8);auto previous=current;current=&scope;provider();current=previous;return 0x88;}
  default:{auto consumed=cookie(node);capture(node,Dispatch,0,&consumed);return 0x99;}
 }
}
extern "C" __declspec(dllexport) uint64_t D5AM_pop(winner::scheduler::Event* out){return winner::scheduler::pop(*out);}
extern "C" __declspec(dllexport) uint64_t D5AM_metric(unsigned n){
 using namespace winner::scheduler;
 switch(n){case 0:return sched::enqueue;case 1:return sched::dequeue;case 2:return sched::drops;case 3:return sched::active;case 4:return registry_faults;
 case 5:return identity_faults;case 6:return failed||D5AM_sched_counter_faults.load();case 7:return reentrant;case 8:return backtrace_count;case 9:return D5AM_sched_bridge_active;
 case 10:return sched::tokens;case 11:return D5AM_sched_counter_faults;case 12:return winner::active;case 13:return sched::written;case 14:return original_calls;
 case 15:{U value{};memcpy(&value,D5AM_fixture_write+8,8);return value;}
 case 16:{U value{};memcpy(&value,D5AM_fixture_tree+0x50,8);return value;}default:return 0;}
}
extern "C" __declspec(dllexport) void D5AM_enabled(unsigned value){winner::enabled=bool(value);}
extern "C" __declspec(dllexport) void D5AM_registry_busy(uint64_t node,unsigned value){
 auto c=winner::scheduler::cookie(node);if(c.slot<32768){auto& cell=D5AM_sched_registry[c.slot];auto serial=cell.serial.load();cell.serial=value?(serial|1):(serial+(serial&1));}
}
extern "C" __declspec(dllexport) void D5AM_offer(uint64_t count,unsigned threads){
 std::vector<std::thread> workers;
 for(unsigned i=0;i<threads;++i)workers.emplace_back([=]{for(U n=0;n<count;++n){winner::scheduler::Event e{};e.kind=winner::scheduler::Provider;e.status=winner::scheduler::NoTask;winner::scheduler::emit(e);}});
 for(auto& worker:workers)worker.join();
}
extern "C" __declspec(dllexport) void D5AM_recursive_offer(){winner::scheduler::recording=true;winner::scheduler::emit({});winner::scheduler::recording=false;}
extern "C" __declspec(dllexport) void D5AM_pause(uint64_t ready,uint64_t next){pause_ready=(HANDLE)ready;pause_continue=(HANDLE)next;}
extern "C" __declspec(dllexport) void D5AM_counter(unsigned n,uint64_t value){
 switch(n){case 0:sched::tokens=value;break;case 1:sched::registry_faults=value;break;case 2:sched::identity_faults=value;break;
 case 3:sched::drops=value;break;case 4:sched::reentrant=value;break;case 5:sched::active=value;break;
 case 6:winner::active=value;break;case 7:D5AM_sched_bridge_active=value;break;case 8:sched::written=value;break;}
}
extern "C" __declspec(dllexport) void D5AM_serial(uint64_t node,uint64_t value){auto c=sched::cookie(node);if(c.slot<32768)D5AM_sched_registry[c.slot].serial=value;}
extern "C" __declspec(dllexport) uint64_t D5AM_written(){return sched::advance_written();}
