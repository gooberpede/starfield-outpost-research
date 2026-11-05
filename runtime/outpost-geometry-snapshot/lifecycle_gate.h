// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <Windows.h>
#include <atomic>
#include <cstdint>
#include "identity.h"
namespace d5ar {
// Admission barrier only: no observer mutex is held across a native phase.
class LifecycleGate {
 SRWLOCK gate_=SRWLOCK_INIT;
 std::atomic<std::uint64_t>& epoch_;std::atomic<std::uint64_t>& active_;
 std::atomic<bool> fault_{};
 inline static thread_local LifecycleGate* copy_owner_{};
 inline static thread_local LifecycleGate* phase_owner_{};
 inline static thread_local std::uint64_t generation_{};
 inline static thread_local unsigned phase_depth_{};
 bool advance(std::atomic<std::uint64_t>& value) noexcept {
  auto prior=value.load();while(prior!=UINT64_MAX){if(value.compare_exchange_weak(prior,prior+1))return true;}
  fault_=true;return false;
 }
public:
 struct Lease {LifecycleGate* owner{};std::uint64_t generation{},reads{};};
 LifecycleGate(std::atomic<std::uint64_t>& epoch,std::atomic<std::uint64_t>& active):epoch_(epoch),active_(active){}
 enum class Phase {Observed,Inert,SelfUpgrade};
 Phase admit_phase() noexcept {
  if(copy_owner_==this){fault_=true;return Phase::SelfUpgrade;}
  if(phase_depth_==UINT_MAX||(phase_depth_&&phase_owner_!=this))fault_=true;
  bool outer=phase_depth_==0;if(outer)AcquireSRWLockExclusive(&gate_);
  // A fault may have been raised by a copy while this admission waited.
  bool admitted=!fault_&&advance(active_);
  if(admitted&&!advance(epoch_)){--active_;admitted=false;}
  if(admitted){phase_owner_=this;++phase_depth_;}
  if(outer)ReleaseSRWLockExclusive(&gate_);
  return admitted?Phase::Observed:Phase::Inert;
 }
 bool phase_begin() noexcept {return admit_phase()==Phase::Observed;}
 void phase_end() noexcept {
  if(!phase_depth_||phase_owner_!=this){fault_=true;return;}
  advance(epoch_);--active_;if(!--phase_depth_)phase_owner_=nullptr;
 }
 bool try_copy(Lease& lease) noexcept {
  lease={};if(generation_==UINT64_MAX)fault_=true;
  if(fault_||copy_owner_||phase_depth_)return false;
  if(!TryAcquireSRWLockShared(&gate_))return false;
  if(fault_||active_.load()){ReleaseSRWLockShared(&gate_);return false;}
  copy_owner_=this;lease={this,++generation_,0};return true;
 }
 bool owns(const Lease& lease) const noexcept {return !fault_&&lease.owner==this&&copy_owner_==this&&lease.generation==generation_;}
 bool read(Lease& lease,IdentityRead reader,void* context,std::uint64_t at,void* into,std::size_t size){
  if(!owns(lease)||lease.reads==UINT64_MAX||!reader)return false;
  ++lease.reads;return reader(context,at,into,size);
 }
 void end_copy(Lease& lease) noexcept {
  // Even a protection fault must release a previously owned shared scope.
  if(lease.owner!=this||copy_owner_!=this||lease.generation!=generation_){fault_=true;return;}
  copy_owner_=nullptr;lease.owner=nullptr;ReleaseSRWLockShared(&gate_);
 }
 bool offline_probe_unlocked() noexcept {if(!TryAcquireSRWLockExclusive(&gate_))return false;ReleaseSRWLockExclusive(&gate_);return true;}
 void disable_copying() noexcept {fault_=true;}
 bool faulted() const noexcept{return fault_.load();}
};
}
