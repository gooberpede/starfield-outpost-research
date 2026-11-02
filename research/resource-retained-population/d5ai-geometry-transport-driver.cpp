// SPDX-License-Identifier: GPL-3.0-or-later
// Isolate the exact retained geometry worker function from earlier journal I/O.
// The supplied header is transport-only; it is not an available population.
#include "d5ai_geometry.h"
#include <filesystem>
#include <cstdio>
namespace winner {extern std::filesystem::path session;extern std::string identity_hash;extern std::atomic<unsigned> fixture_fault;}
extern "C" uint64_t d5ai_native_acquire(uint64_t,uint64_t,uint64_t,uint64_t){return 0;}
DWORD WINAPI write_geometry(void*){return winner::geometry::drain_sidecar()?0:1;}
int wmain(int count,wchar_t** args){
 using namespace winner;namespace g=geometry;
 if(count!=2)return 80;SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
 auto directory=std::filesystem::absolute(args[1]);std::filesystem::create_directory(directory);
 for(unsigned mode=0;mode<4;++mode){
  session=directory/std::to_wstring(mode);if(!std::filesystem::create_directory(session))return 1;
  identity_hash=std::string(64,'a');broken=false;g::failed=false;g::completed=0;fixture_fault=mode==1?2:mode==2?3:0;g::fixture_receipt_fault=mode==3;
  auto& slot=g::slots[0];slot.header=g::Header{};slot.header.request=1;slot.header.snapshot=1;slot.state=g::Queued;
  HANDLE thread=CreateThread(nullptr,0,write_geometry,nullptr,0,nullptr);if(!thread)return 2;
  if(WaitForSingleObject(thread,INFINITE)!=WAIT_OBJECT_0)return 3;DWORD code{};if(!GetExitCodeThread(thread,&code))return 4;CloseHandle(thread);
  auto binary=session/L"geometry-1.bin";bool receipt=std::filesystem::exists(session/L"geometry-1.json"),request=std::filesystem::exists(session/L"geometry-request-1.json");
  if(mode==0){if(code||g::failed||broken||g::completed!=1||!receipt||!request||slot.state!=g::Free)return 5;}
  else if(code!=1||!g::failed||!broken||g::completed!=0||receipt||request||slot.state!=g::Queued)return 6;
  if(!std::filesystem::exists(binary)||std::filesystem::file_size(binary)!=(mode==1?0:sizeof(g::Header)))return 7;
  slot.state=g::Free;
 }
 printf("{\"status\":\"PASS\",\"actual_geometry_worker_thread_cases\":4,\"normal_write\":true,\"targeted_write_failure\":true,\"targeted_flush_failure\":true,\"targeted_receipt_failure\":true}\n");return 0;
}
