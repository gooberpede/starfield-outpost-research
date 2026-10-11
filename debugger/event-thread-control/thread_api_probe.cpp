// SPDX-License-Identifier: GPL-3.0-or-later
// Original disposable self-process API experiment, never an acquisition tool.
// Reads handle metadata; controls only its own explicitly created worker thread.
// No files, remote process, security policy or target memory access.
#define NOMINMAX
#include <windows.h>
#include <winternl.h>
#include <cstdio>
DWORD WINAPI worker(void* gate){WaitForSingleObject((HANDLE)gate,INFINITE);return 23;}
void probe(const char* name,HANDLE h){
    PUBLIC_OBJECT_BASIC_INFORMATION info{};ULONG length{};
    using Query=NTSTATUS(NTAPI*)(HANDLE,OBJECT_INFORMATION_CLASS,PVOID,ULONG,PULONG);
    auto query=(Query)GetProcAddress(GetModuleHandleW(L"ntdll.dll"),"NtQueryObject");
    auto nt=query(h,ObjectBasicInformation,&info,sizeof info,&length);
    DWORD code=0;SetLastError(0);auto before=GetExitCodeThread(h,&code);auto before_error=before?0:GetLastError();
    SetLastError(0);auto sr=SuspendThread(h);auto se=sr==DWORD(-1)?GetLastError():0;
    DWORD after_code=0;SetLastError(0);auto after=GetExitCodeThread(h,&after_code);auto after_error=after?0:GetLastError();
    DWORD rr=DWORD(-1),re=0;if(sr!=DWORD(-1)){SetLastError(0);rr=ResumeThread(h);re=rr==DWORD(-1)?GetLastError():0;}
    std::printf("{\"name\":\"%s\",\"nt_status\":%ld,\"access\":%lu,\"before_ok\":%d,\"before_error\":%lu,\"before_exit\":%lu,\"suspend\":%lu,\"suspend_error\":%lu,\"after_ok\":%d,\"after_error\":%lu,\"after_exit\":%lu,\"resume\":%lu,\"resume_error\":%lu}\n",name,(long)nt,info.GrantedAccess,before,before_error,code,sr,se,after,after_error,after_code,rr,re);
}
int main(){
    auto gate=CreateEventW(nullptr,TRUE,FALSE,nullptr);DWORD tid{};
    auto h=CreateThread(nullptr,0,worker,gate,0,&tid);if(!h||!gate)return 2;
    HANDLE reduced{};if(!DuplicateHandle(GetCurrentProcess(),h,GetCurrentProcess(),&reduced,THREAD_SUSPEND_RESUME|THREAD_GET_CONTEXT|THREAD_SET_CONTEXT,FALSE,0))return 3;
    probe("running-full",h);probe("running-debug-minimum-rights",reduced);
    // This increment belongs to this probe, not to the later probe() calls.
    auto outer=SuspendThread(h);if(outer!=0)return 4;
    probe("running-existing-suspend",h);
    if(ResumeThread(h)!=1)return 5;
    SetEvent(gate);if(WaitForSingleObject(h,10000)!=WAIT_OBJECT_0)return 6;
    probe("exited-full",h);probe("exited-debug-minimum-rights",reduced);
    CloseHandle(reduced);CloseHandle(h);CloseHandle(gate);return 0;
}
