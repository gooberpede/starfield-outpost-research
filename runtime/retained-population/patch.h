// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "observer.h"
#include <TlHelp32.h>
namespace retained {
struct Patch {unsigned char* at{};unsigned n{};unsigned char before[16]{},after[16]{};};
inline bool match(const Patch& p,bool after){unsigned char b[16]{};return read(U(p.at),b,p.n)&&!memcmp(b,after?p.after:p.before,p.n);}
inline bool write(Patch& p,bool after){DWORD old{},unused{};if(!VirtualProtect(p.at,p.n,PAGE_EXECUTE_READWRITE,&old))return false;
 memcpy(p.at,after?p.after:p.before,p.n);bool ok=VirtualProtect(p.at,p.n,old,&unused)!=0;
 return FlushInstructionCache(GetCurrentProcess(),p.at,p.n)&&ok&&match(p,after);
}
inline bool sole_thread(){HANDLE h=CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);if(h==INVALID_HANDLE_VALUE)return false;
 THREADENTRY32 e{sizeof e};unsigned n=0;bool ok=Thread32First(h,&e)!=0;
 if(ok){do{if(e.th32OwnerProcessID==GetCurrentProcessId())++n;}while(Thread32Next(h,&e));ok=GetLastError()==ERROR_NO_MORE_FILES;}
 CloseHandle(h);return ok&&n==1;
}
inline void jump(unsigned char* p,U target){p[0]=0xff;p[1]=0x25;memset(p+2,0,4);memcpy(p+6,&target,8);}
inline unsigned char* near_page(U address){SYSTEM_INFO s{};GetSystemInfo(&s);U step=s.dwAllocationGranularity,anchor=address&~(step-1);
 for(U d=step;d<0x70000000;d+=step)for(int sign:{1,-1}){
  U at=U(int64_t(anchor)+sign*int64_t(d));if(at<0x10000||at>0x7fffffff0000ULL)continue;
  if(auto p=VirtualAlloc((void*)at,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE))return (unsigned char*)p;
 }return nullptr;
}
inline bool relative(Patch& p,U target,unsigned char opcode){auto d=int64_t(target)-int64_t(U(p.at)+5);if(d<INT32_MIN||d>INT32_MAX)return false;
 memset(p.after,0x90,p.n);p.after[0]=opcode;auto v=int32_t(d);memcpy(p.after+1,&v,4);return true;
}
// Sole-thread admission only. Keep relay/trampoline memory resident until exit.
// All preimages are checked before the first write. Never hot-unpatch.
inline bool install(Patch* p,size_t n,bool& dirty){dirty=false;if(!sole_thread())return false;
 for(size_t i=0;i<n;++i)if(!match(p[i],false))return false;
 for(size_t i=0;i<n;++i){dirty=true;if(!write(p[i],true)){
  bool restored=true;for(size_t j=0;j<=i;++j)restored=write(p[j],false)&&restored;dirty=!restored;return false;
 }}return true;
}
}
