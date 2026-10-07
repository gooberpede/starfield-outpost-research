// SPDX-License-Identifier: GPL-3.0-or-later
// Original disposable target. No game, save, plugin or debugger dependency.
#define NOMINMAX
#include <windows.h>
#include <filesystem>
#include <fstream>
#include <thread>
#include <atomic>
#include <array>
#include <string>
namespace fs=std::filesystem;
static std::atomic<bool> stop=false,go=false;
static std::atomic<unsigned long long> pulse[3]{},calls=0;
static std::atomic<DWORD> tids[3]{},caller=0;
static std::array<unsigned char,256> manager{};
static char name[260]="disposable-name";
extern "C" __declspec(dllexport) __declspec(noinline)
unsigned long long Request(void* object,const char* text,unsigned long long slot,unsigned long long option,unsigned long long stack_arg) {
    calls.fetch_add(1);
    caller=GetCurrentThreadId();
    return (unsigned long long)object+(unsigned long long)text+slot+option+stack_arg;
}
static void worker(unsigned index,bool call,const char* text) {
    bool done=false;
    tids[index]=GetCurrentThreadId();
    while(!stop) {
        ++pulse[index];
        if(call && go && !done) {Request(manager.data(),text,0xffffffff,0,0x1122334455667788ULL);done=true;}
        Sleep(2);
    }
}
int wmain(int argc,wchar_t** argv) {
    if(argc!=3) return 2;
    fs::path prefix=argv[1];std::wstring mode=argv[2];
    if(mode!=L"fixed-existing"&&mode!=L"unarmed-only") return 2;
    manager[0x50]=42;manager[0x8c]=7;
    std::ofstream out(prefix.wstring()+L".fixture.jsonl");if(!out) return 3;
    out<<"{\"kind\":\"identity\",\"pid\":"<<GetCurrentProcessId()<<",\"tick_ms\":"<<GetTickCount64()<<"}\n";out.flush();
    std::thread first(worker,0,mode==L"fixed-existing",nullptr),second,third;
    bool triggered=false,created=false,exit37=false;auto start=GetTickCount64(),next=start;
    while(GetTickCount64()<start+90000 && !fs::exists(prefix.wstring()+L".stop")) {
        if(fs::exists(prefix.wstring()+L".exit37")) {exit37=true;break;}
        if(!created&&fs::exists(prefix.wstring()+L".newthreads")) {
            created=true;
            second=std::thread(worker,1,mode==L"unarmed-only",name);
            third=std::thread(worker,2,false,nullptr);
        }
        if(!triggered&&fs::exists(prefix.wstring()+L".trigger")) {
            triggered=true;
            out<<"{\"kind\":\"trigger\",\"tick_ms\":"<<GetTickCount64()<<"}\n";out.flush();
            go=true;
        }
        if(GetTickCount64()>=next) {
            out<<"{\"kind\":\"heartbeat\",\"tick_ms\":"<<GetTickCount64()<<",\"pulse\":["<<pulse[0]<<","<<pulse[1]<<","<<pulse[2]<<"],\"tids\":["<<tids[0]<<","<<tids[1]<<","<<tids[2]<<"],\"calls\":"<<calls<<",\"caller_tid\":"<<caller<<"}\n";out.flush();next=GetTickCount64()+100;
        }
        Sleep(5);
    }
    stop=true;first.join();if(second.joinable())second.join();if(third.joinable())third.join();
    out<<"{\"kind\":\"exit\",\"tick_ms\":"<<GetTickCount64()<<"}\n";out.flush();return exit37?37:0;
}
