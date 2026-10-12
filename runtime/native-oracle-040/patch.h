// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "route.h"
#include <TlHelp32.h>
namespace oracle {
inline bool sole_thread(){
    HANDLE h=CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);if(h==INVALID_HANDLE_VALUE)return false;
    THREADENTRY32 t{};t.dwSize=sizeof t;unsigned count=0;bool own=false,ok=Thread32First(h,&t)!=0;
    if(ok){do{if(t.th32OwnerProcessID==GetCurrentProcessId()){++count;own|=t.th32ThreadID==GetCurrentThreadId();}}while(Thread32Next(h,&t));ok=GetLastError()==ERROR_NO_MORE_FILES;}
    CloseHandle(h);return ok&&own&&count==1;
}
struct Edit {unsigned char* address{};size_t size{};unsigned char before[8]{},after[8]{};DWORD original_protection{};};
// Normalize every intersecting owned CALL, including a neighboring CALL inside
// a 32-byte guard window. Leaves all unowned bytes untouched for hashing.
inline void original_window(unsigned char* bytes,uint64_t start,size_t size,const Edit* edits,size_t n){
    for(size_t i=0;i<n;++i){auto at=reinterpret_cast<uint64_t>(edits[i].address);
        for(size_t j=0;j<edits[i].size;++j)if(at+j>=start&&at+j-start<size)bytes[at+j-start]=edits[i].before[j];}
}
inline bool match(const Edit& e,bool after){unsigned char b[8]{};SIZE_T n{};return ReadProcessMemory(GetCurrentProcess(),e.address,b,e.size,&n)&&n==e.size&&!memcmp(b,after?e.after:e.before,e.size);}
inline void worker_control(const fs::path& session,Edit* edits,size_t n){
    if(!disk())throw std::runtime_error("disk_guard");
    for(size_t i=0;i<n;++i)if(!match(edits[i],true))throw std::runtime_error("patch_integrity");
    if(fs::exists(session/L"STOP"))gate.stop();
}
template<class Consume> inline void drain_controlled(Queue<4096>& q,const fs::path& session,Edit* edits,size_t n,Consume consume){
    Event e;
    for(;;){worker_control(session,edits,n);if(!q.pop(e))break;consume(e);}
}
inline bool write(Edit& e,bool after){
    DWORD old{},dummy{};if(!VirtualProtect(e.address,e.size,PAGE_EXECUTE_READWRITE,&old))return false;
    if(!e.original_protection)e.original_protection=old;
    memcpy(e.address,after?e.after:e.before,e.size);
    bool restored=VirtualProtect(e.address,e.size,e.original_protection,&dummy)!=0;
    bool flushed=FlushInstructionCache(GetCurrentProcess(),e.address,e.size)!=0;
    return restored&&flushed&&match(e,after);
}
// All preimages verified before any write. Only callable in a controlled sole-
// thread pre-main/disposable phase, never in a running-game worker or on retry.
inline bool install(Edit* edits,size_t n,bool quiescent,bool& dirty){
    dirty=false;if(!quiescent)return false;
    for(size_t i=0;i<n;++i)if(!match(edits[i],false))return false;
    for(size_t i=0;i<n;++i){dirty=true;if(!write(edits[i],true)){
        bool clean=true;for(size_t j=0;j<=i;++j)clean=write(edits[j],false)&&clean;dirty=!clean;return false;
    }}return true;
}
inline bool call_edit(Edit& e,uint64_t site,uint64_t target){
    auto delta=int64_t(target)-int64_t(site+5);if(delta<INT32_MIN||delta>INT32_MAX)return false;
    e.address=reinterpret_cast<unsigned char*>(site);e.size=5;e.after[0]=0xe8;auto d=static_cast<int32_t>(delta);memcpy(e.after+1,&d,4);return true;
}
// Six-byte indirect JMP island with adjacent absolute pointer. No modified
// instructions execute in island; it is a leaf tail jump with unchanged stack.
inline unsigned char* islands(uint64_t site){
    SYSTEM_INFO si{};GetSystemInfo(&si);uint64_t step=si.dwAllocationGranularity;
    auto anchor=site&~(step-1);
    for(uint64_t d=step;d<0x70000000;d+=step){for(int sign:{1,-1}){
        auto at=uint64_t(int64_t(anchor)+sign*int64_t(d));
        if(at<0x10000||at>0x7fffffff0000ULL)continue;
        if(auto p=VirtualAlloc(reinterpret_cast<void*>(at),4096,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE))return static_cast<unsigned char*>(p);
    }}return nullptr;
}
inline bool relay_guard(const unsigned char* p,uint64_t destination){
    unsigned char actual[14]{},expected[14]{0xff,0x25};memcpy(expected+6,&destination,8);SIZE_T got{};MEMORY_BASIC_INFORMATION info{};
    return VirtualQuery(p,&info,sizeof info)==sizeof info&&info.State==MEM_COMMIT&&info.Protect==PAGE_EXECUTE_READ&&ReadProcessMemory(GetCurrentProcess(),p,actual,14,&got)&&got==14&&!memcmp(actual,expected,14);
}

inline void island(unsigned char* p,uint64_t destination){p[0]=0xff;p[1]=0x25;memset(p+2,0,4);memcpy(p+6,&destination,8);}
}
