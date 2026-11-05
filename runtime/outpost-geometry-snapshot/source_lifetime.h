// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <Windows.h>
#include <set>
#include <atomic>
#include "identity.h"
namespace d5ar {
// Process-lifetime history. No eviction or address-reuse reset is permitted.
// Admission requires the separately reviewed fresh-process pre-owner preload.
class SourceRecorder {
 SRWLOCK gate_=SRWLOCK_INIT;
 std::set<std::uint64_t> retired_;
 bool started_{};std::atomic<bool> healthy_{true};
 inline static thread_local SourceRecorder* held_{};
 static SourceDiagnostics refused(const char* status) noexcept {
  SourceDiagnostics value;value.status=value.origin_status=value.descriptor_status=status;return value;
 }
 struct Reader {SourceRecorder* owner;IdentityRead read;void* context;};
 static bool guarded_read(void* raw,std::uint64_t at,void* into,std::size_t size){auto& r=*static_cast<Reader*>(raw);return r.owner->healthy_.load()&&r.read&&r.read(r.context,at,into,size);}
public:
 SourceRecorder()=default;SourceRecorder(const SourceRecorder&)=delete;
 void begin(bool fresh_prehistory) noexcept {
  AcquireSRWLockExclusive(&gate_);
  if(started_||!fresh_prehistory)healthy_=false;
  started_=true;ReleaseSRWLockExclusive(&gate_);
 }
 // Failure injection is an owned-host control of the same sticky loss path.
 void unavailable() noexcept {
  if(held_==this){healthy_=false;return;}
  AcquireSRWLockExclusive(&gate_);healthy_=false;ReleaseSRWLockExclusive(&gate_);
 }
private:
 void mark_locked(std::uint64_t source,bool force_allocation_failure) noexcept {
  if(!started_||source<0x10000||source>UINT64_MAX-0x1a0||force_allocation_failure)healthy_=false;
  else if(healthy_)try{retired_.insert(source);}catch(...){healthy_=false;}
 }
public:
 void mark(std::uint64_t source,bool force_allocation_failure=false) noexcept {
  if(held_==this){healthy_=false;return;}
  AcquireSRWLockExclusive(&gate_);held_=this;
  __try {mark_locked(source,force_allocation_failure);}
  __finally {if(AbnormalTermination())healthy_=false;held_=nullptr;ReleaseSRWLockExclusive(&gate_);}
 }
 SourceDiagnostics copy(IdentityRead read,void* context,std::uint64_t source) noexcept {
  if(held_==this){healthy_=false;return refused("SOURCE_RECORDER_UNAVAILABLE");}
  AcquireSRWLockShared(&gate_);held_=this;
  SourceDiagnostics result;
  __try {
   if(!started_||!healthy_)result=refused("SOURCE_RECORDER_UNAVAILABLE");
   else if(retired_.contains(source))result=refused("SOURCE_LIFETIME_RETIRED");
   else {Reader reader{this,read,context};result=read_source_diagnostics(guarded_read,&reader,source);}
   if(!healthy_)result=refused("SOURCE_RECORDER_UNAVAILABLE");
  } __finally {if(AbnormalTermination())healthy_=false;held_=nullptr;ReleaseSRWLockShared(&gate_);}
  return result;
 }
};
}
