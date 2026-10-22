// SPDX-License-Identifier: GPL-3.0-or-later
#include <windows.h>
#include "decode.h"
#include <thread>
#include <string>
extern "C" void fixture_run(void*,void*,void*,uint64_t);
template<class T>void put(unsigned char* p,size_t at,T v){memcpy(p+at,&v,sizeof v);}
int main(int argc,char** argv){
    if(argc!=3)return 2;
    HANDLE gate=OpenEventA(SYNCHRONIZE,FALSE,argv[2]);if(!gate)return 4;
    std::string ready_name=std::string(argv[2])+"-ready";
    HANDLE ready=OpenEventA(EVENT_MODIFY_STATE,FALSE,ready_name.c_str());if(!ready||!SetEvent(ready))return 7;CloseHandle(ready);
    if(WaitForSingleObject(gate,INFINITE)!=WAIT_OBJECT_0)return 5;CloseHandle(gate);
    uint64_t base=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));
    // A fixture-owned page at the native-relative cache location. No game access.
    auto page=static_cast<unsigned char*>(VirtualAlloc(reinterpret_cast<void*>(base+0x5f50000),0x10000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
    if(!page || reinterpret_cast<uint64_t>(page)!=base+0x5f50000)return 3;
    auto op=page+0xd2e0;
    unsigned char reference[0xd0]{},definition[0x30]{},extra[0xa0]{},list[0x20]{};
    unsigned char il[0x38]{},cu[0x38]{};
    auto sources_page=static_cast<unsigned char*>(VirtualAlloc(reinterpret_cast<void*>(base+0x5e80000),0x10000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
    if(!sources_page||reinterpret_cast<uint64_t>(sources_page)!=base+0x5e80000)return 6;
    unsigned char file[0x370]{},entry[16]{};
    uint64_t file_pointer=reinterpret_cast<uint64_t>(file),entry_pointer=reinterpret_cast<uint64_t>(entry);
    put<uint32_t>(sources_page,0x81e8,1);put<uint64_t>(sources_page,0x81f0,reinterpret_cast<uint64_t>(&entry_pointer));
    put<uint64_t>(entry,0,reinterpret_cast<uint64_t>(&file_pointer));put<int32_t>(entry,8,1);
    put<uint64_t>(file,0,base+0x4b29b80);memcpy(file+0x38,"Starfield.esm",14);memcpy(file+0x268,"Data",5);
    put<uint32_t>(definition,0x28,0x2c60e9);put<uint8_t>(definition,0x2e,0x1e);
    put<uint8_t>(reference,0x2e,0x4a);put<uint32_t>(reference,0x28,0xff001234);
    put<uint64_t>(reference,0x98,reinterpret_cast<uint64_t>(definition));put<uint64_t>(reference,0xc8,reinterpret_cast<uint64_t>(list));
    put<uint64_t>(list,8,reinterpret_cast<uint64_t>(extra));put<uint8_t>(extra,0x12,0xbc);
    put<uint64_t>(extra,0,base+0x4c24e60);put<uint64_t>(extra,0x98,0x85f5fc4c6f86a5c3ULL);
    put<uint64_t>(op,0x268,reinterpret_cast<uint64_t>(extra));
    put<uint32_t>(il,0x28,0x57d4);put<uint8_t>(il,0x2e,0x9f);
    put<uint32_t>(cu,0x28,0x57cf);put<uint8_t>(cu,0x2e,0x9f);
    uint64_t members[]={reinterpret_cast<uint64_t>(il),reinterpret_cast<uint64_t>(cu)};
    retail::Header payload{reinterpret_cast<uint64_t>(members),reinterpret_cast<uint64_t>(members+2),reinterpret_cast<uint64_t>(members+2)};
    for(int i=0;i<3;++i)put(op,0x520+i*24,payload);
    std::string mode=argv[1];
    if(mode=="wrong-workshop")put<uint64_t>(extra,0x98,1);
    if(mode=="invalid")payload.begin=8;
    if(mode=="partial-prelude"||mode=="unrelated-partial")put(op,0x538,retail::Header{8,16,16});
    if(mode=="crash-before")RaiseException(0xe0c1d000,0,0,nullptr);
    auto run=[&]{fixture_run(reference,op,&payload,mode=="wrong-return"?1:mode=="stale-transfer"?2:0);};
    if(mode=="threads"){for(int i=0;i<3;++i){std::thread t(run);t.join();}}else run();
    if(mode=="crash-after")RaiseException(0xe0c1d001,0,0,nullptr);
    VirtualFree(page,0,MEM_RELEASE);VirtualFree(sources_page,0,MEM_RELEASE);return 0;
}
