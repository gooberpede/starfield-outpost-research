// SPDX-License-Identifier: GPL-3.0-or-later
// Loads the exact candidate DLL only inside this owned disposable process.
#define NOMINMAX
#include <Windows.h>
#include "qualification.h"
#include <array>
#include <cstring>
#include <filesystem>
#include <iostream>
#include <fstream>
#include <TlHelp32.h>
static void thread_inventory(const char* phase){
 using Query=LONG(WINAPI*)(HANDLE,ULONG,void*,ULONG,ULONG*);
 auto query=reinterpret_cast<Query>(GetProcAddress(GetModuleHandleW(L"ntdll.dll"),"NtQueryInformationThread"));
 HANDLE view=CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,0);THREADENTRY32 row{sizeof row};
 std::cout<<"THREAD_PHASE "<<phase<<'\n';
 if(view==INVALID_HANDLE_VALUE){std::cout<<"THREAD_QUERY_FAILED "<<GetLastError()<<'\n';return;}
 if(Thread32First(view,&row))do{if(row.th32OwnerProcessID!=GetCurrentProcessId())continue;
  auto thread=OpenThread(THREAD_QUERY_INFORMATION,FALSE,row.th32ThreadID);void* start{};
  auto status=thread&&query?query(thread,9,&start,sizeof start,nullptr):LONG(-1);
  if(thread)CloseHandle(thread);HMODULE owner{};wchar_t path[32768]{};
  if(start&&GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(start),&owner))GetModuleFileNameW(owner,path,32768);
  std::cout<<"THREAD "<<row.th32ThreadID<<" start="<<reinterpret_cast<uint64_t>(start)<<" module="<<std::filesystem::path(path).filename().string()<<" rva="<<(reinterpret_cast<uint64_t>(start)-reinterpret_cast<uint64_t>(owner))<<" status="<<status<<'\n';
 }while(Thread32Next(view,&row));CloseHandle(view);
}
template<class T,size_t N>static void put(std::array<uint8_t,N>& into,size_t offset,T value){std::memcpy(into.data()+offset,&value,sizeof value);}
int wmain(int argc,wchar_t** argv){
 SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
 if(argc!=4)return 2;
 auto mode=std::wcstoul(argv[3],nullptr,10);
 if(mode==11){std::ofstream stop(std::filesystem::path(argv[2])/L"STOP",std::ios::binary);stop<<"Owned startup STOP control\n";if(!stop)return 7;}
 auto image=VirtualAlloc(nullptr,0x6230000,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);if(!image)return 3;
 thread_inventory("before-dll-load");
 auto dll=LoadLibraryW(argv[1]);if(!dll)return 4;
 thread_inventory("after-dll-load");
 auto qualify=reinterpret_cast<d5ar::OfflineQualify>(GetProcAddress(dll,"D5AR_OfflineQualify"));if(!qualify)return 5;
 std::array<uint8_t,0x60> proc{};std::array<uint8_t,24> map{},resources{},collection{};std::array<uint8_t,0x40> holder{};
 std::array<uint8_t,48> region{};std::array<uint8_t,16> points{};std::array<uint8_t,0x70> source{};
 std::array<uint8_t,0x200> manager{};std::array<uint8_t,0xb8> reference{};std::array<uint8_t,0x30> base{},cell{};std::array<uint8_t,24> area_query{};std::array<uint8_t,0x638> operation_state{};
 auto ptr=[](auto& value){return reinterpret_cast<uint64_t>(value.data());};
 put(proc,0x20,ptr(map));put(proc,0x28,uint64_t(1));put(proc,0x44,uint32_t(mode==2?0xffc00001:1));
 put(map,0,ptr(source));put(map,8,ptr(holder));put(holder,0x20,ptr(resources));put(holder,0x28,uint64_t(1));
 put(resources,0,uint32_t(7));put(resources,8,ptr(collection));put(collection,8,uint32_t(1));put(collection,12,uint32_t(1));put(collection,16,ptr(region));
 put(region,16,uint32_t(7));put(region,24,uint32_t(1));put(region,28,uint32_t(1));put(region,32,ptr(points));
 float data[]{1,2,3,4};std::memcpy(points.data(),data,sizeof data);
 put(reference,0x28,uint32_t(0x12345));put(reference,0x2e,uint8_t(0x49));put(reference,0x98,ptr(base));put(reference,0xb0,ptr(cell));
 put(base,0x28,uint32_t(0x34567));put(base,0x2e,uint8_t(0x1e));put(cell,0x28,uint32_t(0x45678));put(cell,0x2e,uint8_t(0x49));
 put(area_query,12,uint32_t(UINT32_MAX));put(area_query,16,ptr(cell));
 if(mode==7){
  put(resources,0,uint32_t(23));put(region,16,uint32_t(23));put(reference,0x28,uint32_t(0x99887));
  float alternate[]{-10,20,0,40};std::memcpy(points.data(),alternate,sizeof alternate);
  put(source,0,uint32_t(0x112233));put(source,0x38,uint32_t(3));put(source,0x10,uint32_t(2));put(source,0x20,uint32_t(4));
 }
 if(mode>=24){
  put(resources,0,uint32_t(43));put(region,16,uint32_t(43));
  float planar[]{-150,-150,0,1};std::memcpy(points.data(),planar,sizeof planar);std::memcpy(region.data(),planar,sizeof planar);
  put(source,0,uint32_t(0x112233));put(source,0x38,uint8_t(3));put(source,0x20,uint32_t(2));put(source,0x24,uint32_t(2));put(source,0x68,uint64_t(0x100000001));
  put(manager,0x20,uint8_t(2));std::memcpy(manager.data()+0xc8,source.data()+0x38,44);
 }
 put(manager,0x130,ptr(proc));put(manager,0x80,uint32_t(mode==7||mode>=24?0x556677:0x223344));
 if(mode==38){auto inaccessible=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_NOACCESS);if(!inaccessible)return 9;put(map,0,reinterpret_cast<uint64_t>(inaccessible));put(manager,0x130,uint64_t(ptr(proc)+16));}
 if(mode==46||mode==47){auto owned=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);if(!owned)return 12;std::memcpy(owned,source.data(),source.size());put(map,0,reinterpret_cast<uint64_t>(owned));}
 auto manager_pointer=ptr(manager);std::memcpy(static_cast<uint8_t*>(image)+0x5fd9c30,&manager_pointer,8);
 if(mode>=11&&mode<=13)std::memset(static_cast<uint8_t*>(image)+0x5fd9c30,0,8);
 if(mode==3)put(region,24,uint32_t(2));
 auto operation_reference=ptr(reference);
 if(mode==35){auto owned=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);if(!owned)return 8;std::memcpy(owned,reference.data(),reference.size());operation_reference=reinterpret_cast<uint64_t>(owned);}
 if(mode==40){auto owned=static_cast<uint8_t*>(VirtualAlloc(nullptr,8192,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE));if(!owned)return 10;DWORD old{};if(!VirtualProtect(owned+4096,4096,PAGE_NOACCESS,&old))return 10;operation_reference=reinterpret_cast<uint64_t>(owned+4096-0x28);}
 auto proc_pointer=ptr(proc);
 if(mode==54||mode==55){auto inaccessible=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_NOACCESS);if(!inaccessible)return 13;proc_pointer=reinterpret_cast<uint64_t>(inaccessible);
  if(mode==54)std::memset(static_cast<uint8_t*>(image)+0x5fd9c30,0,8);
 }
 if(mode==56||mode==57){auto owned=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);if(!owned)return 14;std::memcpy(owned,proc.data(),proc.size());proc_pointer=reinterpret_cast<uint64_t>(owned);put(manager,0x130,proc_pointer);}
 auto operation_state_pointer=ptr(operation_state);
 if(mode==42){auto inaccessible=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_NOACCESS);if(!inaccessible)return 11;operation_state_pointer=reinterpret_cast<uint64_t>(inaccessible);}
 d5ar::OfflineInput input{reinterpret_cast<uint64_t>(image),proc_pointer,ptr(holder),argv[2],unsigned(mode),operation_reference,ptr(area_query),operation_state_pointer};
 auto started=GetTickCount64();auto checks=qualify(&input);auto elapsed=GetTickCount64()-started;
 auto error=GetLastError();thread_inventory("after-qualification");
 if(!checks){std::cerr<<"Offline exact-DLL qualification refused or failed; Win32 error="<<error<<"\n";return 6;}
 std::cout<<"{\"schema\":\"sor-d5ar-exact-dll-fixture/1\",\"mode\":"<<mode<<",\"checks\":"<<checks<<",\"elapsed_ms\":"<<elapsed<<"}\n";
 // The DLL remains resident until process exit; production hooks are never
 // hot-unloaded. This path only used owned image/objects and a private output.
 return 0;
}
