// SPDX-License-Identifier: GPL-3.0-or-later
// Exact retained shared worker plus owned core producers, geometry bridges and
// typed entry hooks. Core guard windows are supplied, not eighteen engine hooks.
#include "transport.h"
#include "d5ai_geometry.h"
#include <thread>
#include <vector>
#include <shared_mutex>
#include <cstdio>
#include <stdexcept>
using namespace winner;
namespace g=winner::geometry;namespace life=winner::lifetime;
namespace winner {extern std::atomic<bool> fixture_pause;}
extern "C" {U d5ai_fixture_life_holder(U,U,U,U);U d5ai_fixture_life_collection(U,U,U,U);U d5ai_fixture_life_mutation(U,U,U,U);U d5ai_invoke(U,U,U,uint32_t,uint32_t);U d5ai_preunlock_invoke(uint32_t);U d5ai_complete_invoke(U,U,uint32_t);void d5ai_area_capture(U,U,U,uint32_t,uint32_t) noexcept;void d5ai_at_acquire();void d5ai_at_preunlock();void d5ai_at_complete();}
constexpr unsigned producers=4;
struct Operation {alignas(8) unsigned char allocation[64]{};std::atomic<unsigned> calls{};bool accepted[2]{};};
std::vector<Operation> operations;unsigned calls_per_thread{};bool overload{},paced_callbacks{};
HANDLE first_all{},release_first{},oracle_failure{};std::atomic<unsigned> first_count{},body_active{},body_peak{};std::atomic<bool> oracle_bad{};
U tids[producers]{};
std::shared_mutex native_mutex;std::atomic<unsigned> readers{};
void check(bool yes){if(!yes)throw std::runtime_error("integrated concurrency invariant");}
void bad(){oracle_bad=true;SetEvent(oracle_failure);}
U original_body(unsigned kind,U receiver,U thread,U ordinal,U marker){
 if(thread>=producers||ordinal>=calls_per_thread||marker!=0xc0ffee){bad();return 0;}
 auto& op=operations[size_t(thread)*calls_per_thread+ordinal];
 if(receiver!=U(op.allocation)+(kind==0?16:8)||kind!=ordinal%3||op.calls.fetch_add(1)!=0){bad();return 0;}
 auto active_now=++body_active;auto old=body_peak.load();while(active_now>old&&!body_peak.compare_exchange_weak(old,active_now)){}
 if(!ordinal){if(++first_count==producers)SetEvent(first_all);WaitForSingleObject(release_first,INFINITE);}
 if(paced_callbacks)Sleep(1);--body_active;return 0x9000+kind;
}
extern "C" U d5ai_native_life_holder(U a,U b,U c,U d){return original_body(0,a,b,c,d);}
extern "C" U d5ai_native_life_collection(U a,U b,U c,U d){return original_body(1,a,b,c,d);}
extern "C" U d5ai_native_life_mutation(U a,U b,U c,U d){return original_body(2,a,b,c,d);}
extern "C" U d5ai_native_owner(U,U,U,U){return 0;}
extern "C" U d5ai_native_context_reset(U,U,U,U){return 0;}
extern "C" U d5ai_native_acquire(U lock,U,U,U){native_mutex.lock_shared();uint32_t owner=0,state=++readers;memcpy((void*)lock,&owner,4);memcpy((void*)(lock+4),&state,4);return 0x12345678;}
struct Population {
 alignas(16) unsigned char proc[0x80]{},manager[0x210]{},holder[64]{},collection[24]{},map[48]{},resources[48]{},region[48]{},points[32]{},query[24]{};
 template<class T>static void put(void* p,size_t at,T value){memcpy((unsigned char*)p+at,&value,sizeof value);}
 Population(){
  put(proc,0x20,U(map));put(proc,0x28,U(2));put(map,0,U(0x10001));put(map,8,U(holder));put(map,16,uint32_t(0));put(map,40,UINT32_MAX);
  put(holder,0x20,U(resources));put(holder,0x28,U(2));put(resources,0,uint32_t(0x57d4));put(resources,8,U(collection));put(resources,16,uint32_t(0));put(resources,40,UINT32_MAX);
  put(collection,8,uint32_t(1));put(collection,12,uint32_t(1));put(collection,16,U(region));put(region,16,uint32_t(0x57d4));put(region,24,uint32_t(2));put(region,28,uint32_t(2));put(region,32,U(points));
  const float data[]{1,2,3,4,5,6,7,8};memcpy(points,data,32);put(manager,0x20,uint8_t(2));put(manager,0x80,uint32_t(0x5e0de));put(manager,0x130,U(proc));g::fixture_manager=U(manager);
 }
 void capture(U id){check(g::arm(id));check(d5ai_invoke(U(proc)+0x40,U(query),0xabcdef,0x43160000,0x447a0000)==0x12345678);check(d5ai_preunlock_invoke(1)==UINT32_MAX);uint32_t state=--readers;memcpy(proc+0x44,&state,4);native_mutex.unlock_shared();check(d5ai_complete_invoke(2,2,99)==0x12345678);}
};
int wmain(int argc,wchar_t** argv){
 SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
 if(argc!=3)return 80;
 try {
  std::wstring mode=argv[2];check(mode==L"normal"||mode==L"held"||mode==L"overload"||mode==L"short");overload=mode==L"overload";bool held=mode==L"held"||overload;paced_callbacks=mode==L"normal"||mode==L"held";
  calls_per_thread=overload?5000:held?128:512;operations=std::vector<Operation>(size_t(producers)*calls_per_thread);
  std::filesystem::path output=std::filesystem::absolute(argv[1]);check(std::filesystem::create_directory(output));session=output/L"session";check(std::filesystem::create_directory(session));
  check(disk(64*1024*1024));
  first_all=CreateEventW(nullptr,TRUE,FALSE,nullptr);release_first=CreateEventW(nullptr,TRUE,FALSE,nullptr);oracle_failure=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(first_all&&release_first&&oracle_failure);
  // Actual retained geometry and typed entry instruction objects are hooked.
  check(g::configure_acquire((void*)&d5ai_at_acquire,sor::sha_bytes((void*)&d5ai_at_acquire,32),sor::sha_bytes((void*)&d5ai_native_acquire,32)));
  check(g::configure_completion((void*)&d5ai_at_complete,sor::sha_bytes((void*)&d5ai_at_complete,32)));check(g::configure_preunlock((void*)&d5ai_at_preunlock,sor::sha_bytes((void*)&d5ai_at_preunlock,32)));
  check(life::configure((void*)&d5ai_fixture_life_holder,(void*)&d5ai_fixture_life_collection,(void*)&d5ai_fixture_life_mutation,sor::sha_bytes((void*)&d5ai_fixture_life_holder,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_life_collection,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_life_mutation,32).c_str()));
  for(unsigned i=0;i<10000&&!sole_thread();++i)Sleep(1);bool dirty=false;check(install(g::edits,3,dirty));check(install(life::edits,3,dirty));
  auto* windows=(unsigned char*)VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(windows!=nullptr);memset(windows,0x90,4096);
  std::string sites="[";for(unsigned i=0;i<18;++i){auto& p=winner::edits[i];p.at=windows+i*32;p.n=5;memset(p.before,0x90,5);memset(p.after,0x90,5);if(i)sites+=",";sites+="{\"index\":"+std::to_string(i)+",\"va\":"+std::to_string(U(p.at))+",\"guard_sha256\":"+sor::quote(sor::sha_bytes(p.at,32))+"}";}sites+="]";
  relay_page=windows;relay_sha256=sor::sha_bytes(windows,4096);for(unsigned i=0;i<7;++i){guarded_targets[i]=U(windows+1024+i*32);guarded_hashes[i]=sor::sha_bytes((void*)guarded_targets[i],32);}
  wchar_t image[32768]{};check(GetModuleFileNameW(nullptr,image,32768)!=0);FILETIME birth{},exit{},kernel{},user{};check(GetProcessTimes(GetCurrentProcess(),&birth,&exit,&kernel,&user));LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);
  identity="{\"schema\":\"sor-d5x/4\",\"retail\":false,\"nonce\":\""+std::string(64,'e')+"\",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"creation_filetime\":"+std::to_string((U(birth.dwHighDateTime)<<32)|birth.dwLowDateTime)+",\"dll_sha256\":"+sor::quote(sor::sha_file(image))+",\"host_sha256\":"+sor::quote(sor::sha_file(image))+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"sites\":"+sites+g::identity_metadata()+life::metadata();
  auto id=identity+"}\n";identity_hash=sor::sha_bytes(id.data(),id.size());check(sor::write_new(session/L"identity.json",id));
  raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);ack=CreateFileW((session/L"flush.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);check(raw!=INVALID_HANDLE_VALUE&&ack!=INVALID_HANDLE_VALUE);
  initialize_queue();check(life::begin());enabled=true;Event ready{};ready.kind=Ready;ready.epoch=epoch;check(emit(ready));HANDLE worker_thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);check(worker_thread!=nullptr);
  while(!std::filesystem::exists(session/L"ready.json")){check(enabled&&!broken);Sleep(1);}
  fixture_pause=held;life::fixture_hold=held;g::held=held;Population population;
  U started=g::tick();std::vector<std::thread> threads;
  Four original_calls[]{&d5ai_fixture_life_holder,&d5ai_fixture_life_collection,&d5ai_fixture_life_mutation};
  for(unsigned t=0;t<producers;++t)threads.emplace_back([&,t]{tids[t]=GetCurrentThreadId();for(unsigned n=0;n<calls_per_thread;++n){auto& op=operations[size_t(t)*calls_per_thread+n];for(unsigned sub=0;sub<2;++sub){Event e{};e.kind=Ready;e.epoch=epoch;e.a=t+1;e.b=n;e.c=U(op.allocation);e.d=sub;op.accepted[sub]=emit(e);}auto result=original_calls[n%3](U(op.allocation)+(n%3==0?16:8),t,n,0xc0ffee);if(result!=0x9000+n%3)bad();}});
  std::thread geometry_thread([&]{unsigned target=overload?4:32;for(U n=1;n<=target&&enabled.load();++n){bool free=false;while(enabled.load()){for(auto& s:g::slots)if(s.state==g::Free){free=true;break;}if(free)break;Sleep(1);}if(!enabled.load())break;population.capture(n);}});
  HANDLE waits[]{first_all,oracle_failure};check(WaitForMultipleObjects(2,waits,FALSE,INFINITE)==WAIT_OBJECT_0);while(g::captured<1&&enabled.load())Sleep(1);check(body_active==producers&&g::captured>=1);bool overlap=true;check(SetEvent(release_first));
  for(auto& thread:threads)thread.join();U produced=g::tick();check(!oracle_bad&&body_peak>=producers);U core_pending=enqueue.load()-dequeue.load(),life_pending=life::enqueue.load()-life::dequeue.load();
  if(held&&!overload)check(!drops&&!life::drops&&core_pending==U(producers)*calls_per_thread*2&&life_pending==U(producers)*calls_per_thread*2);
  if(overload)check(drops>0&&life::drops>0&&life::failed);
  fixture_pause=false;life::fixture_hold=false;g::held=false;geometry_thread.join();
  U durable=0;if(!overload){check(!drops&&!life::drops&&!broken);while(g::completed<32){check(enabled&&!broken);Sleep(1);}population.capture(33);while(g::completed<33){check(enabled&&!broken);Sleep(1);}check(sor::write_new(session/L"request.txt",std::string(32,'d')));while(!std::filesystem::exists(session/(L"ack-"+std::wstring(32,L'd')+L".json"))){check(enabled&&!broken);Sleep(1);}durable=g::tick();check(sor::write_new(session/L"STOP","finite integrated concurrency STOP\n"));}
  check(WaitForSingleObject(worker_thread,INFINITE)==WAIT_OBJECT_0);FILETIME worker_birth{},worker_exit{},worker_kernel{},worker_user{};check(GetThreadTimes(worker_thread,&worker_birth,&worker_exit,&worker_kernel,&worker_user));U worker_cpu_100ns=(U(worker_kernel.dwHighDateTime)<<32|worker_kernel.dwLowDateTime)+(U(worker_user.dwHighDateTime)<<32|worker_user.dwLowDateTime);CloseHandle(worker_thread);check(!life::active&&!winner::active&&!g::active_capture);
  std::string rows="[";for(unsigned t=0;t<producers;++t)for(unsigned n=0;n<calls_per_thread;++n){auto& op=operations[size_t(t)*calls_per_thread+n];check(op.calls==1);if(t||n)rows+=",";rows+="{\"thread_index\":"+std::to_string(t)+",\"ordinal\":"+std::to_string(n)+",\"kind\":"+std::to_string(n%3+1)+",\"allocation\":"+std::to_string(U(op.allocation))+",\"thread\":"+std::to_string(tids[t])+",\"callback_count\":1,\"core_accepted\":["+(op.accepted[0]?"true":"false")+","+(op.accepted[1]?"true":"false")+"]}";}rows+="]";
  U image_base=U(GetModuleHandleW(nullptr));auto rva=[&](auto function){return std::to_string(U(function)-image_base);};
  std::string origins="{\"shared_worker\":"+rva(&winner::worker)+",\"core_drain\":"+rva(&winner::drain)+",\"geometry_drain\":"+rva(&g::drain_sidecar)+",\"lifetime_drain\":"+rva(&life::drain)+",\"area_capture\":"+rva(&d5ai_area_capture)+",\"lifetime_hook0\":"+rva(&life::hook<0>)+",\"lifetime_hook1\":"+rva(&life::hook<1>)+",\"lifetime_hook2\":"+rva(&life::hook<2>)+",\"typed_entry0\":"+rva(&d5ai_fixture_life_holder)+",\"typed_entry1\":"+rva(&d5ai_fixture_life_collection)+",\"typed_entry2\":"+rva(&d5ai_fixture_life_mutation)+"}";
  const char* mode_name=mode==L"normal"?"normal":mode==L"short"?"short":mode==L"held"?"held":"overload";
  auto oracle="{\"schema\":\"sor-d5ai-integrated-concurrency/1\",\"mode\":"+sor::quote(mode_name)+",\"producers\":4,\"calls_per_thread\":"+std::to_string(calls_per_thread)+",\"core_offers\":"+std::to_string(1+U(producers)*calls_per_thread*2)+",\"lifetime_offers\":"+std::to_string(U(producers)*calls_per_thread*2)+",\"peak_original_callbacks\":"+std::to_string(body_peak.load())+",\"geometry_during_four_callbacks\":"+(overlap?"true":"false")+",\"started_ticks\":"+std::to_string(started)+",\"producers_done_ticks\":"+std::to_string(produced)+",\"all_durable_ack_observed_ticks\":"+std::to_string(durable)+",\"core_pending_before_release\":"+std::to_string(core_pending)+",\"lifetime_pending_before_release\":"+std::to_string(life_pending)+",\"worker_cpu_100ns\":"+std::to_string(worker_cpu_100ns)+",\"core_cell_bytes\":"+std::to_string(sizeof(winner::Cell))+",\"core_queue_bytes\":"+std::to_string(sizeof(winner::queue))+",\"lifetime_cell_bytes\":"+std::to_string(sizeof(life::Cell))+",\"lifetime_queue_bytes\":"+std::to_string(sizeof(life::queue))+",\"geometry_slot_bytes\":"+std::to_string(sizeof(g::Slot))+",\"image_base\":"+std::to_string(image_base)+",\"function_rvas\":"+origins+",\"operations\":"+rows+"}\n";
  check(sor::write_new(output/L"oracle.json",oracle,oracle.size()+1));CloseHandle(first_all);CloseHandle(release_first);CloseHandle(oracle_failure);return 0;
 }catch(const std::exception& error){fprintf(stderr,"%s\n",error.what());return 1;}
}
