// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "lifecycle_gate.h"
#include <thread>
#include <stdexcept>
namespace d5ar::fixture {
inline bool lifecycle_phase_seh(LifecycleGate* gate){
 if(!gate->phase_begin())return false;
 __try {RaiseException(0xe0424448,0,0,nullptr);}
 __finally {gate->phase_end();}
 return false;
}
inline bool lifecycle_copy_seh(LifecycleGate* gate){
 LifecycleGate::Lease lease;if(!gate->try_copy(lease))return false;
 __try {RaiseException(0xe0424448,0,0,nullptr);}
 __finally {gate->end_copy(lease);}return false;
}
inline bool lifecycle_seh_probe(LifecycleGate* gate,bool phase){
 __try {if(phase)lifecycle_phase_seh(gate);else lifecycle_copy_seh(gate);}
 __except(GetExceptionCode()==0xe0424448?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline void lifecycle_throw_cpp(){throw std::runtime_error("Owned lifecycle C++ unwind");}
inline void lifecycle_phase_cpp(LifecycleGate* gate){
 if(!gate->phase_begin())return;
 __try {lifecycle_throw_cpp();} __finally {gate->phase_end();}
}
inline void lifecycle_copy_cpp(LifecycleGate* gate){
 LifecycleGate::Lease lease;if(!gate->try_copy(lease))return;
 __try {lifecycle_throw_cpp();} __finally {gate->end_copy(lease);}
}
inline bool lifecycle_cpp_probe(LifecycleGate* gate,bool phase){
 try{if(phase)lifecycle_phase_cpp(gate);else lifecycle_copy_cpp(gate);}
 catch(const std::runtime_error&){return true;}return false;
}
inline bool lifecycle_owned_read(void* context,uint64_t,void*,size_t){++*static_cast<unsigned*>(context);return true;}
inline unsigned lifecycle_controls(){
 unsigned checks=0;auto require=[&](bool okay){if(!okay)throw std::runtime_error("Lifecycle admission control failed");++checks;};
 {std::atomic<uint64_t> epoch{1},active{};LifecycleGate gate(epoch,active);LifecycleGate::Lease a,b;unsigned reads=0;
  require(!gate.read(a,lifecycle_owned_read,&reads,1,nullptr,0)&&!reads);
  require(gate.try_copy(a)&&gate.read(a,lifecycle_owned_read,&reads,1,nullptr,0)&&reads==1);
  auto stale=a;require(!gate.try_copy(b));gate.end_copy(a);
  require(!gate.read(stale,lifecycle_owned_read,&reads,1,nullptr,0)&&reads==1);
  require(gate.try_copy(b)&&!gate.read(stale,lifecycle_owned_read,&reads,1,nullptr,0)&&reads==1);gate.end_copy(b);
  require(gate.phase_begin()&&active==1&&epoch==2);
  require(!gate.try_copy(a)&&!gate.read(a,lifecycle_owned_read,&reads,1,nullptr,0)&&reads==1);
  require(gate.phase_begin()&&active==2&&epoch==3);gate.phase_end();gate.phase_end();
  require(!active&&epoch==5&&gate.try_copy(a));gate.end_copy(a);
  require(lifecycle_seh_probe(&gate,true)&&!active&&epoch==7);
  require(lifecycle_seh_probe(&gate,false)&&gate.try_copy(a));gate.end_copy(a);
  require(lifecycle_cpp_probe(&gate,true)&&!active&&epoch==9&&gate.offline_probe_unlocked());
  require(lifecycle_cpp_probe(&gate,false)&&gate.try_copy(a));gate.end_copy(a);
 }
 {std::atomic<uint64_t> epoch{1},active{};LifecycleGate gate(epoch,active);LifecycleGate::Lease lease;
  require(gate.try_copy(lease));std::atomic<bool> trying{},mutation{},admitted{};
  std::thread phase([&]{trying=true;admitted=gate.phase_begin();mutation=true;if(admitted)gate.phase_end();});
  while(!trying)SwitchToThread();Sleep(20);bool blocked=!mutation;gate.end_copy(lease);phase.join();
  require(blocked&&mutation&&admitted&&!active&&epoch==3);
 }
 // Two ordinary mutators have opposite engine-lock entry ordering. Admission
 // releases the observer gate before either original can wait on the engine.
 {std::atomic<uint64_t> epoch{1},active{};LifecycleGate gate(epoch,active);SRWLOCK engine=SRWLOCK_INIT;
  HANDLE engine_owned=CreateEventW(nullptr,TRUE,FALSE,nullptr),b_admitted=CreateEventW(nullptr,TRUE,FALSE,nullptr);
  if(!engine_owned||!b_admitted)throw std::runtime_error("Owned event failure");
  std::atomic<bool> a_ok{},b_ok{},callback_refused{};
  std::thread a([&]{AcquireSRWLockExclusive(&engine);SetEvent(engine_owned);WaitForSingleObject(b_admitted,10000);
   a_ok=gate.phase_begin();LifecycleGate::Lease lease;callback_refused=!gate.try_copy(lease);if(a_ok)gate.phase_end();ReleaseSRWLockExclusive(&engine);});
  std::thread b([&]{WaitForSingleObject(engine_owned,10000);b_ok=gate.phase_begin();SetEvent(b_admitted);
   AcquireSRWLockExclusive(&engine);ReleaseSRWLockExclusive(&engine);if(b_ok)gate.phase_end();});
  a.join();b.join();CloseHandle(engine_owned);CloseHandle(b_admitted);require(a_ok&&b_ok&&callback_refused&&!active&&epoch==5);
 }
 // Existing native reader can return without waiting for a phase that needs it.
 {std::atomic<uint64_t> epoch{1},active{};LifecycleGate gate(epoch,active);SRWLOCK native=SRWLOCK_INIT;
  HANDLE entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);if(!entered)throw std::runtime_error("Owned event failure");
  AcquireSRWLockShared(&native);std::atomic<bool> completed{},admitted{};
  std::thread phase([&]{admitted=gate.phase_begin();SetEvent(entered);AcquireSRWLockExclusive(&native);ReleaseSRWLockExclusive(&native);if(admitted)gate.phase_end();completed=true;});
  bool observed=WaitForSingleObject(entered,10000)==WAIT_OBJECT_0;LifecycleGate::Lease lease;
  bool refused=!gate.try_copy(lease);ReleaseSRWLockShared(&native);phase.join();CloseHandle(entered);
  require(observed&&refused&&admitted&&completed&&!active);
 }
 {std::atomic<uint64_t> epoch{1},active{};LifecycleGate gate(epoch,active);LifecycleGate::Lease lease;
  require(gate.try_copy(lease));require(!gate.phase_begin()&&gate.faulted());gate.end_copy(lease);require(!gate.try_copy(lease)&&!active);
 }
 {std::atomic<uint64_t> epoch{UINT64_MAX},active{};LifecycleGate gate(epoch,active);require(!gate.phase_begin()&&gate.faulted()&&!active);}
 // A pending admission rechecks a fault raised while waiting for this copy.
 {std::atomic<uint64_t> epoch{1},active{};LifecycleGate gate(epoch,active);LifecycleGate::Lease lease;
  require(gate.try_copy(lease));std::atomic<bool> attempting{},forwarded{};LifecycleGate::Phase admission{};
  std::thread phase([&]{attempting=true;admission=gate.admit_phase();forwarded=true;if(admission==LifecycleGate::Phase::Observed)gate.phase_end();});
  while(!attempting)SwitchToThread();Sleep(20);bool blocked=!forwarded;
  require(gate.admit_phase()==LifecycleGate::Phase::SelfUpgrade);gate.end_copy(lease);phase.join();
  require(blocked&&forwarded&&admission==LifecycleGate::Phase::Inert&&!active&&epoch==1&&gate.offline_probe_unlocked());
  require(gate.admit_phase()==LifecycleGate::Phase::Inert&&!active&&epoch==1);
 }
 return checks;
}
}
