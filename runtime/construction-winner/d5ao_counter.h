// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// D5AN owned repair of the D5AM bounded counter helpers, SOR-P-0002.
// D5AO preserves the D5AN diagnostic ABI in a separately versioned candidate.
// No allocation, target reads, file I/O or voluntary descheduling occur here.
// Strong CAS preserves MAX/zero refusal without transient wrapping. A failed
// comparison witnesses another mutation; retry has no arbitrary fatal quota.
// Shared-object progress is lock-free; individual progress is not wait-free.
// Callers may retain native locks and observer gates; retry/cache-line traffic
// remains a measurement influence even after OS backoff is removed.
#include <Windows.h>
#include <atomic>
#include <cstdint>
#include <intrin.h>
#include <string>
extern "C" {
extern std::atomic<uint64_t> D5AM_sched_counter_faults,D5AM_causal_counter_faults;
inline std::atomic<uint64_t> D5AN_fixture_before_cas{}; // Zero in retail.
inline std::atomic<uint64_t> D5AN_fixture_fault_reserved{}; // Private fixture.
}
namespace winner {extern std::atomic<bool> enabled;}
namespace winner::counter {
using N=uint64_t;
// Stable IDs: scheduler 1..31; causal 32..63. The address identifies the exact
// live object; the helper return VA identifies its actual compiled producer.
inline std::atomic<N> publication{},fault_ids{},first_id{},first_producer{},first_class{},first_value{},first_thread{},first_counter{},first_return{},first_enabled{};
__declspec(noinline) inline void fault(N id,N producer,N kind,N value,N address,N return_address) noexcept {
 if(!return_address)return_address=N(_ReturnAddress());
 N zero=0;bool enabled_at_fault=winner::enabled.load();
 if(publication.compare_exchange_strong(zero,1)){
  auto reserved=D5AN_fixture_fault_reserved.load();if(reserved)reinterpret_cast<void(*)() noexcept>(reserved)();
  first_id=id;first_producer=producer;first_class=kind;first_value=value;
  first_thread=GetCurrentThreadId();first_counter=address;first_return=return_address;first_enabled=enabled_at_fault;
  fault_ids.fetch_or(N(1)<<(id&63));
  (id<32?D5AM_sched_counter_faults:D5AM_causal_counter_faults).fetch_or(kind==2?4:1);
  publication.store(2,std::memory_order_release);
 }
 fault_ids.fetch_or(N(1)<<(id&63));
 // The winning writer publishes complete fields, its bitmap and sticky bit
 // before publication=2. A competing fault can stop it at publication=1; that
 // explicitly has INCOMPLETE diagnostic provenance and readers must refuse it.
 (id<32?D5AM_sched_counter_faults:D5AM_causal_counter_faults).fetch_or(kind==2?4:1);
}
inline std::string metrics(){
 auto p=publication.load(std::memory_order_acquire);
 return ",\"counter_fault_schema\":\"sor-d5an-counter/1\",\"counter_fault_publication\":"+std::to_string(p)+
  ",\"counter_fault_ids\":"+std::to_string(fault_ids.load())+
  ",\"counter_fault_id\":"+std::to_string(first_id.load())+
  ",\"counter_fault_producer\":"+std::to_string(first_producer.load())+
  ",\"counter_fault_class\":"+std::to_string(first_class.load())+
  ",\"counter_fault_value\":"+std::to_string(first_value.load())+
  ",\"counter_fault_thread\":"+std::to_string(first_thread.load())+
  ",\"counter_fault_address\":"+std::to_string(first_counter.load())+
  ",\"counter_fault_return_va\":"+std::to_string(first_return.load())+
  ",\"counter_fault_enabled\":"+std::to_string(first_enabled.load())+
  ",\"counter_fault_scheduler_bits\":"+std::to_string(D5AM_sched_counter_faults.load())+
  ",\"counter_fault_causal_bits\":"+std::to_string(D5AM_causal_counter_faults.load());
}
}
extern "C" __declspec(dllexport) __declspec(noinline) inline bool D5AN_counter_next(
 std::atomic<uint64_t>* counter,uint64_t id,uint64_t producer,uint64_t* result) noexcept {
 DWORD error=GetLastError();uint64_t value=counter->load();
 for(;;){
  if(value==UINT64_MAX){winner::counter::fault(id,producer,1,value,uint64_t(counter),uint64_t(_ReturnAddress()));SetLastError(error);return false;}
  auto before=D5AN_fixture_before_cas.load();if(before)reinterpret_cast<void(*)(std::atomic<uint64_t>*,uint64_t,uint64_t) noexcept>(before)(counter,value,producer);
  if(counter->compare_exchange_strong(value,value+1)){
   if(result)*result=value+1;SetLastError(error);return true;
  }
  // Strong CAS failure updates value. Retry without OS waits or a quota.
 }
}
extern "C" __declspec(dllexport) __declspec(noinline) inline bool D5AN_counter_leave(
 std::atomic<uint64_t>* counter,uint64_t id,uint64_t producer) noexcept {
 DWORD error=GetLastError();uint64_t value=counter->load();
 for(;;){
  if(value==0){winner::counter::fault(id,producer,2,value,uint64_t(counter),uint64_t(_ReturnAddress()));SetLastError(error);return false;}
  if(counter->compare_exchange_strong(value,value-1)){SetLastError(error);return true;}
  // Retry without voluntary descheduling; native caller ownership is retained.
 }
}
namespace winner::counter {
inline std::string metadata(){
 MEMORY_BASIC_INFORMATION region{};
 if(!VirtualQuery(reinterpret_cast<const void*>(&D5AN_counter_next),&region,sizeof region))return {};
 N module=N(region.AllocationBase);
 return ",\"counter_schema\":\"sor-d5an-counter/1\",\"counter_dll_base\":"+std::to_string(module)+
  ",\"counter_helper_rva\":"+std::to_string(N(&D5AN_counter_next)-module)+
  ",\"counter_leave_rva\":"+std::to_string(N(&D5AN_counter_leave)-module);
}
}
