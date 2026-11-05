// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Original conservative startup stack admission, informed only by Microsoft's
// API contracts. No sample implementation copied. Does not execute handlers.
#include "hooks.h"
#include <algorithm>
namespace d5ar {
enum class StackStatus {Complete,ForbiddenAncestor,OutsideStack,UnreadableStack,MissingMetadata,MalformedMetadata,UnwindException,Nonprogress};
struct StackAdmission {StackStatus status=StackStatus::MalformedMetadata;uint64_t frames{},first_pc{};};
using ForbiddenFrame=bool(*)(void*,uint64_t);
inline bool unwind_step(CONTEXT& context,DWORD64 image,PRUNTIME_FUNCTION entry) noexcept {
 __try {PVOID handler{};DWORD64 establisher{};RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,context.Rip,entry,&context,&handler,&establisher,nullptr);return true;}
 __except(EXCEPTION_EXECUTE_HANDLER){return false;}
}
inline PRUNTIME_FUNCTION lookup_step(uint64_t pc,DWORD64& image) noexcept {
 __try {return RtlLookupFunctionEntry(pc,&image,nullptr);}
 __except(EXCEPTION_EXECUTE_HANDLER){return nullptr;}
}
inline StackAdmission walk_startup_stack(CONTEXT context,uint64_t low,uint64_t high,ForbiddenFrame forbidden,void* argument) noexcept {
 StackAdmission result;result.first_pc=context.Rip;
 if(low>=high||context.Rsp<low||context.Rsp>=high){result.status=StackStatus::OutsideStack;return result;}
 // Validate every committed stack extent that an unwind may read, not a fixed
 // number of frames. Guard/no-access, stack locations outside reported current-thread limits and bad metadata
 // refuse; a missing entry is never guessed to be a genuine leaf.
 for(uint64_t cursor=context.Rsp;cursor<high;){
  MEMORY_BASIC_INFORMATION region{};
  if(!VirtualQuery(reinterpret_cast<void*>(cursor),&region,sizeof region)||region.State!=MEM_COMMIT||(region.Protect&(PAGE_GUARD|PAGE_NOACCESS))||!region.Protect){result.status=StackStatus::UnreadableStack;return result;}
  auto start=reinterpret_cast<uint64_t>(region.BaseAddress);
  if(region.RegionSize>UINT64_MAX-start||start+region.RegionSize<=cursor){result.status=StackStatus::UnreadableStack;return result;}
  cursor=(std::min)(high,start+region.RegionSize);
 }
 while(context.Rip){
  if(forbidden&&forbidden(argument,context.Rip)){result.status=StackStatus::ForbiddenAncestor;return result;}
  if(context.Rsp<low||context.Rsp>high-8){result.status=StackStatus::OutsideStack;return result;}
  DWORD64 image{};auto entry=lookup_step(context.Rip,image);RUNTIME_FUNCTION owned{};
  if(!entry){result.status=StackStatus::MissingMetadata;return result;}
  if(!checked_read(nullptr,reinterpret_cast<uint64_t>(entry),&owned,sizeof owned)||owned.BeginAddress>=owned.EndAddress||image>context.Rip||context.Rip-image<owned.BeginAddress||context.Rip-image>=owned.EndAddress){result.status=StackStatus::MalformedMetadata;return result;}
  auto previous=context.Rsp;
  if(!unwind_step(context,image,entry)){result.status=StackStatus::UnwindException;return result;}
  ++result.frames;
  if(context.Rsp<=previous||context.Rsp>high){result.status=StackStatus::Nonprogress;return result;}
 }
 result.status=StackStatus::Complete;return result;
}
__declspec(noinline) inline StackAdmission startup_stack(ForbiddenFrame forbidden,void* argument) noexcept {
 ULONG_PTR low{},high{};GetCurrentThreadStackLimits(&low,&high);CONTEXT context{};RtlCaptureContext(&context);
 return walk_startup_stack(context,low,high,forbidden,argument);
}
}
