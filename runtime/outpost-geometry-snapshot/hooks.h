// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Adapted from project-owned construction-winner/patch.h and D5AI context
// trampoline qualification. Sole-thread startup only; never hot-unpatch.
#define NOMINMAX
#include <Windows.h>
#include <TlHelp32.h>
#include <cstdint>
#include <cstring>
#include <initializer_list>

namespace d5ar {
struct Hook {uint8_t* at{};uint8_t before[16]{},after[16]{};size_t length{};uint8_t* page{};void* original{};bool function_table{};};
inline void discard_prepared(Hook& hook){
 if(hook.function_table)RtlDeleteFunctionTable(reinterpret_cast<RUNTIME_FUNCTION*>(hook.page+3072));
 if(hook.page)VirtualFree(hook.page,0,MEM_RELEASE);hook={};
}
inline bool checked_read(void*,uint64_t address,void* into,size_t bytes){
 SIZE_T got{};return address&&ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(address),into,bytes,&got)&&got==bytes;
}
inline bool sole_thread(){
 HANDLE view=CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);if(view==INVALID_HANDLE_VALUE)return false;
 THREADENTRY32 entry{sizeof entry};unsigned count=0;bool ok=Thread32First(view,&entry)!=FALSE;
 if(ok){do{if(entry.th32OwnerProcessID==GetCurrentProcessId())++count;}while(Thread32Next(view,&entry));ok=GetLastError()==ERROR_NO_MORE_FILES;}
 CloseHandle(view);return ok&&count==1;
}
inline void absolute_jump(uint8_t* at,uint64_t target){at[0]=0xff;at[1]=0x25;std::memset(at+2,0,4);std::memcpy(at+6,&target,8);}
// R11 is dead at each pinned original continuation (native input-liveness
// audit required). A register jump avoids Windows classifying FF25/E9 as an
// epilogue and skipping saved-nonvolatile restoration in this trampoline.
inline void continuation_jump(uint8_t* at,uint64_t target){at[0]=0x49;at[1]=0xbb;std::memcpy(at+2,&target,8);at[10]=0x41;at[11]=0xff;at[12]=0xe3;}
inline uint8_t* allocate_relay(uint64_t at){
 uint8_t* page{}; SYSTEM_INFO system{};GetSystemInfo(&system);uint64_t step=system.dwAllocationGranularity,anchor=at&~(step-1);
 for(uint64_t distance=step;!page&&distance<0x70000000;distance+=step)for(int sign:{1,-1}){
  uint64_t candidate=uint64_t(int64_t(anchor)+sign*int64_t(distance));if(candidate<0x10000||candidate>0x7fffffff0000ULL)continue;
  page=static_cast<uint8_t*>(VirtualAlloc(reinterpret_cast<void*>(candidate),4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE));if(page)break;
 }
 return page;
}
template<size_t N>inline bool prepare_hook(Hook& hook,uint64_t at,void* replacement,const uint8_t(&expected)[N],int saved_rbx_offset){
 static_assert(N>=5&&N<=16);hook.length=N;
 hook.at=reinterpret_cast<uint8_t*>(at);
 if(!checked_read(nullptr,at,hook.before,N)||std::memcmp(hook.before,expected,N))return false;
 hook.page=allocate_relay(at);
 if(!hook.page)return false;
 absolute_jump(hook.page,reinterpret_cast<uint64_t>(replacement));auto displacement=int64_t(reinterpret_cast<uint64_t>(hook.page))-int64_t(at+5);
 if(displacement<INT32_MIN||displacement>INT32_MAX)return false;
 std::memset(hook.after,0x90,N);hook.after[0]=0xe9;auto relative=int32_t(displacement);std::memcpy(hook.after+1,&relative,4);
 auto trampoline=hook.page+32;std::memcpy(trampoline,hook.before,N);
 continuation_jump(trampoline+N,at+N);
 hook.original=trampoline;
 auto function=reinterpret_cast<RUNTIME_FUNCTION*>(hook.page+3072);function->BeginAddress=32;function->EndAddress=DWORD(32+N+13);function->UnwindData=3104;
 auto unwind=hook.page+3104;unwind[0]=1;unwind[1]=uint8_t(N);
 if(saved_rbx_offset>=0){unwind[2]=2;unwind[4]=uint8_t(N);unwind[5]=0x34;unwind[6]=uint8_t(saved_rbx_offset/8);}
 else if(saved_rbx_offset==-3){unwind[2]=2;const uint8_t codes[]{5,0x30,4,0x50};std::memcpy(unwind+4,codes,sizeof codes);}
 else if(saved_rbx_offset==-2){unwind[2]=4;const uint8_t codes[]{5,0x70,4,0x60,3,0x50,2,0x30};std::memcpy(unwind+4,codes,sizeof codes);}
 if(!RtlAddFunctionTable(function,1,reinterpret_cast<DWORD64>(hook.page)))return false;hook.function_table=true;
 DWORD previous{};return VirtualProtect(hook.page,4096,PAGE_EXECUTE_READ,&previous)&&FlushInstructionCache(GetCurrentProcess(),hook.page,4096);
}
template<size_t N>inline bool prepare_call(Hook& hook,uint64_t at,void* replacement,const uint8_t(&expected)[N],uint64_t original_target){
 static_assert(N==5);hook.length=5;hook.at=reinterpret_cast<uint8_t*>(at);
 if(expected[0]!=0xe8||!checked_read(nullptr,at,hook.before,5)||std::memcmp(hook.before,expected,5))return false;
 int32_t old_relative{};std::memcpy(&old_relative,expected+1,4);
 if(uint64_t(int64_t(at+5)+old_relative)!=original_target)return false;
 hook.page=allocate_relay(at);if(!hook.page)return false;absolute_jump(hook.page,reinterpret_cast<uint64_t>(replacement));
 auto distance=int64_t(reinterpret_cast<uint64_t>(hook.page))-int64_t(at+5);if(distance<INT32_MIN||distance>INT32_MAX)return false;
 hook.after[0]=0xe8;auto relative=int32_t(distance);std::memcpy(hook.after+1,&relative,4);hook.original=reinterpret_cast<void*>(original_target);
 DWORD previous{};return VirtualProtect(hook.page,4096,PAGE_EXECUTE_READ,&previous)&&FlushInstructionCache(GetCurrentProcess(),hook.page,4096);
}
inline bool write_hook(Hook& hook,bool installed){
 DWORD previous{},ignored{};if(!VirtualProtect(hook.at,hook.length,PAGE_EXECUTE_READWRITE,&previous))return false;
 std::memcpy(hook.at,installed?hook.after:hook.before,hook.length);
 bool restored=VirtualProtect(hook.at,hook.length,previous,&ignored)!=FALSE;
 uint8_t actual[16]{};return FlushInstructionCache(GetCurrentProcess(),hook.at,hook.length)&&restored&&
  checked_read(nullptr,reinterpret_cast<uint64_t>(hook.at),actual,hook.length)&&!std::memcmp(actual,installed?hook.after:hook.before,hook.length);
}
using HookWrite=bool(*)(Hook&,bool);
inline bool install_hooks(Hook* hooks,size_t count,bool& dirty,HookWrite write=write_hook){
 dirty=false;if(!sole_thread())return false;
 for(size_t i=0;i<count;++i){uint8_t bytes[16]{};if(!checked_read(nullptr,reinterpret_cast<uint64_t>(hooks[i].at),bytes,hooks[i].length)||std::memcmp(bytes,hooks[i].before,hooks[i].length))return false;}
 for(size_t i=0;i<count;++i){dirty=true;if(!write(hooks[i],true)){
  bool restored=true;for(size_t j=0;j<=i;++j)restored=write(hooks[j],false)&&restored;dirty=!restored;return false;
 }}return true;
}
}
