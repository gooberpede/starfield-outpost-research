// SPDX-License-Identifier: GPL-3.0-or-later
// Linked into the same DLL: qualification entry refuses the retail host name.
#include "observer.h"
#include "patch.h"
#include "../exp0002/win_support.h"
#include <thread>
#include <vector>
#include <filesystem>
#include <stdexcept>
#include <source_location>
#include <cstdio>
#include <mutex>
extern "C" {uint64_t fixture_grid{};extern uint64_t visited_fall,visited_taken;void visited_bridge();
 uint64_t fixture_provider(uint64_t,uint64_t,uint64_t,uint64_t);
 uint64_t invoke_lookup(uint64_t,uint64_t,uint64_t,uint64_t);
 uint64_t invoke_query(uint64_t,uint64_t,uint64_t,uint64_t);
 uint64_t invoke_mask(uint64_t,uint64_t,uint64_t,uint64_t);
 uint64_t invoke_copy(uint64_t,uint64_t,uint64_t,uint64_t);
 void invoke_generate(uint64_t,uint64_t,uint64_t,uint32_t,uint64_t,uint64_t);
 void at_lookup(),at_query(),at_generate(),at_mask(),at_copy(),at_visited(),after_visited(),bypass();
 uint64_t fixture_reset(uint64_t,uint64_t,uint64_t,uint64_t),fixture_destroy(uint64_t,uint64_t,uint64_t,uint64_t),fixture_erase(uint64_t,uint64_t,uint64_t,uint64_t),fixture_clear(uint64_t,uint64_t,uint64_t,uint64_t),fixture_retire(uint64_t,uint64_t,uint64_t,uint64_t);
}
namespace retained {extern HANDLE raw,ack;extern std::filesystem::path session;extern std::string identity,identity_hash;extern Patch edits[11];extern std::atomic<U> flushed;extern unsigned fixture_fault;extern std::string metrics();bool drain();DWORD WINAPI worker(void*);}
namespace {
using namespace retained;
inline thread_local struct Model* model{};
std::recursive_mutex owner_lock;
struct Model {
 alignas(8) unsigned char manager[0x210]{},proc[0x138]{},source[0x1a0]{},wrapper[0x40]{},collection[0x18]{},geometry[0x30]{},temp[0x30]{},source_index[0x18]{},grid[0x20]{};
 U source_member{};
 U slots[3]{},resources[3]{};uint32_t points[256]{1,2,3,4,5,6,7,8},destination[256]{};int query[2]{37540,20929};
 bool in_flight_loss{},hit{},partial{},failed_copy{},torn_copy{},nested{},did_nested{},raise{},descriptor_change{};U mask=3,hit_index{};
 template<class T>void put(unsigned char* p,unsigned off,T v){memcpy(p+off,&v,sizeof v);}
 Model(){
  put(proc,0,base+0x4b3f3a8);put(grid,0,base+0x4b67f48);put(manager,0x120,U(source_index));put(source_index,0x10,U(grid));
  put(grid,0x10,uint32_t(1));put(grid,0x14,uint32_t(1));source_member=U(source);put(grid,0x18,U(&source_member));
  put(manager,0x130,U(proc));put(source,0x10,uint32_t(37536));put(source,0x14,uint32_t(20928));put(source,0,uint32_t(0x29d20e));
  put(manager,0x80,uint32_t(0x5e0de));
  put(proc,0x20,U(slots));put(proc,0x28,U(1));slots[0]=U(source);slots[1]=U(wrapper);slots[2]=0xffffffff;
  put(wrapper,0,uint32_t(1));put(wrapper,0x20,U(resources));put(wrapper,0x28,U(1));resources[0]=0x57cf;resources[1]=U(collection);resources[2]=0;
  put(collection,0,U(1));put(collection,8,uint32_t(0));put(collection,12,uint32_t(1));put(collection,16,U(geometry));
  put(temp,0,uint32_t(0x3f800000));put(temp,0x18,uint32_t(2));put(temp,0x1c,uint32_t(2));put(temp,0x20,U(points));
 }
};
U singleton_slot{};
void set_model(Model& m){model=&m;fixture_grid=U(m.grid);singleton_slot=U(m.manager);memcpy((void*)(base+0x5fd9c30),&singleton_slot,8);}
void check(bool v,std::source_location where=std::source_location::current()){if(!v){fprintf(stderr,"fixture assertion at line %u\n",where.line());throw std::runtime_error("fixture assertion");}}
}
extern "C" uint64_t native_lookup(uint64_t,uint64_t,uint64_t,uint64_t){U cap{};memcpy(&cap,model->proc+0x28,8);return model->hit?model->hit_index:cap;}
extern "C" uint64_t native_query(uint64_t,uint64_t,uint64_t c,uint64_t d){if(model->descriptor_change)*(unsigned char*)c^=1;return d;}
extern "C" uint64_t native_mask(uint64_t,uint64_t,uint64_t,uint64_t){return model->mask;}
extern "C" uint64_t native_copy(uint64_t,uint64_t,uint64_t,uint64_t){
 auto& m=*model;
 if(m.in_flight_loss){m.in_flight_loss=false;U n=enqueue.load();queue[n%capacity].ticket=n+1;Event lost{};lost.kind=Copy;check(!emit(lost));queue[n%capacity].ticket=n;}
 if(m.failed_copy)return 0xffffffff;
 memcpy(m.geometry,m.temp,0x30);memcpy(m.destination,m.points,sizeof m.points);
 if(m.torn_copy)m.destination[3]^=1;
 m.put(m.geometry,0x20,U(m.destination));m.put(m.collection,8,uint32_t(1));return 0;
}
extern "C" void native_generate(uint64_t,uint64_t,uint64_t,uint32_t,uint64_t,uint64_t){
 auto* outer=model;auto& m=*outer;
 if(m.descriptor_change)m.manager[0xc8]=0;
 if(m.nested&&!m.did_nested){m.did_nested=true;Model inner;set_model(inner);fixture_provider(U(inner.source),U(inner.proc),U(inner.query),0);set_model(m);}
 if(!m.partial){invoke_mask(U(m.source),U(m.query),0,0);invoke_copy(U(m.collection)+8,U(m.temp),0,0);}
 if(m.partial==false&&m.mask==254){m.failed_copy=true;invoke_copy(U(m.collection)+8,U(m.temp),0,0);m.failed_copy=false;}
 if(m.raise)throw std::runtime_error("intentional native generation exception");
}
extern "C" uint64_t fixture_driver(uint64_t w,uint64_t proc){
 std::lock_guard lock(owner_lock);
 auto& m=*model;auto result=invoke_lookup(proc+0x10,w+0x38,0,0);
 U cap{};memcpy(&cap,m.proc+0x28,8);if(result==cap){m.slots[2]=0;invoke_query(0,0,U(m.manager)+0xc8,U(m.query));invoke_generate(U(m.source),U(m.query),0,0x5e0de,0,U(m.wrapper));m.hit=true;}
 return result;
}
extern "C" __declspec(dllexport) int D5P_Qualify(const wchar_t* folder,const char* scenario){
 using namespace retained;
 try {
  wchar_t host[32768]{};if(!GetModuleFileNameW(nullptr,host,32768)||std::filesystem::path(host).filename()!=L"sor-d5p-fixture.exe")return 90;
  session=folder;std::filesystem::create_directories(session);
  auto* memory=(unsigned char*)VirtualAlloc(nullptr,0x6000000,MEM_RESERVE,PAGE_NOACCESS);check(memory!=nullptr);base=U(memory);
  check(VirtualAlloc(memory+0x5fd9000,4096,MEM_COMMIT,PAGE_READWRITE)!=nullptr);
  auto* page=near_page(U(&at_lookup));check(page!=nullptr);
  Four originals[]{&native_lookup,&native_query,nullptr,&native_mask,&native_copy};
  lookup_original=originals[0];query_original=originals[1];generate_original=&native_generate;mask_original=originals[3];copy_original=originals[4];
  void* locations[]{(void*)&at_lookup,(void*)&at_query,(void*)&at_generate,(void*)&at_mask,(void*)&at_copy,(void*)&at_visited,(void*)&fixture_reset,(void*)&fixture_destroy,(void*)&fixture_erase,(void*)&fixture_clear,(void*)&fixture_retire};
  void* hooks[]{(void*)&lookup_hook,(void*)&query_hook,(void*)&generate_hook,(void*)&mask_hook,(void*)&copy_hook,(void*)&visited_bridge,(void*)&fence_hook<0>,(void*)&fence_hook<1>,(void*)&fence_hook<2>,(void*)&fence_hook<3>,(void*)&fence_hook<4>};
  Patch patches[11]{};
  for(unsigned i=0;i<11;++i){auto& p=patches[i];p.at=(unsigned char*)locations[i];p.n=i==5?9:i==8?8:5;check(read(U(p.at),p.before,p.n));
   if(i<5)check(p.before[0]==0xe8);else if(i==5)check(p.before[0]==0x40&&p.before[1]==0x84&&p.before[2]==0xf6&&p.before[3]==0x0f&&p.before[4]==0x85);
   else if(i==8)check(!memcmp(p.before,"\x40\x53\x56\x57\x48\x83\xec\x30",8));
   else check(p.before[0]==0x48&&p.before[1]==0x89);
   jump(page+i*64,U(hooks[i]));check(relative(p,U(page+i*64),i<5?0xe8:0xe9));
   if(i>=6){auto* trampoline=page+i*64+16;memcpy(trampoline,p.before,p.n);jump(trampoline+p.n,U(p.at)+p.n);fences[i-6]=(Four)trampoline;}
  }
  visited_fall=U(&after_visited);visited_taken=U(&bypass);
  DWORD old{};check(VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)&&FlushInstructionCache(GetCurrentProcess(),page,4096));
  bool dirty{};
  std::string s=scenario;
  auto began=GetTickCount64();while(!sole_thread()&&GetTickCount64()-began<60000)Sleep(100);
  if(s=="guard-reject"){check(sole_thread());patches[0].before[0]^=1;check(!install(patches,11,dirty)&&!dirty);return 0;}
  check(install(patches,11,dirty));initialize_queue();enabled=true;
  for(unsigned i=0;i<11;++i)edits[i]=patches[i];
  HMODULE self{};check(GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,(LPCWSTR)&D5P_Qualify,&self)!=0);
  wchar_t dll[32768]{};check(GetModuleFileNameW(self,dll,32768)!=0);
  identity="{\"schema\":\"sor-d5p/2\",\"fixture\":true,\"session_name\":"+sor::quote(session.filename().string())+",\"dll_sha256\":"+sor::quote(sor::sha_file(dll))+",\"pid\":"+std::to_string(GetCurrentProcessId());
  auto id_bytes=identity+"}\n";identity_hash=sor::sha_bytes(id_bytes.data(),id_bytes.size());check(sor::write_new(session/L"identity.json",id_bytes));
  raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  ack=CreateFileW((session/L"flush.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  check(raw!=INVALID_HANDLE_VALUE&&ack!=INVALID_HANDLE_VALUE);
  if(s=="worker-stop"||s=="worker-failure"||s=="worker-guard"||s=="worker-continuous"){
   Event ready_event{};ready_event.kind=Ready;ready_event.epoch=epoch;emit(ready_event);
   if(s=="worker-failure"){CloseHandle(raw);raw=INVALID_HANDLE_VALUE;Event e{};e.kind=Ready;emit(e);}
   const std::string nonce="1234567890abcdef1234567890abcdef";
   auto request=[&](){auto temporary=session/L"fixture-request.tmp";check(sor::write_new(temporary,nonce));check(MoveFileExW(temporary.c_str(),(session/L"request.txt").c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)!=0);};
   if(s=="worker-guard"){Patch damage=edits[0];damage.after[4]^=1;check(write(damage,true));request();}
   HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);check(thread!=nullptr);
   if(s=="worker-stop"||s=="worker-continuous"){
    auto ready_began=GetTickCount64();while(!std::filesystem::exists(session/L"ready.json")&&GetTickCount64()-ready_began<60000)Sleep(10);
    check(std::filesystem::exists(session/L"ready.json"));Model m;set_model(m);fixture_provider(U(m.source),U(m.proc),U(m.query),0);fixture_provider(U(m.source),U(m.proc),U(m.query),0);
    if(s=="worker-continuous"){
     std::atomic<bool> producing{true};std::vector<std::thread> producers;
     for(unsigned i=0;i<4;++i)producers.emplace_back([&](){model=&m;while(producing){fixture_provider(U(m.source),U(m.proc),U(m.query),0);Sleep(5);}});
     auto started=GetTickCount64();while(flushed.load()<capacity*3&&GetTickCount64()-started<60000)Sleep(5);
     check(flushed.load()>=capacity*3);check(sor::write_new(session/L"STOP","STOP\n"));request();
     check(WaitForSingleObject(thread,60000)==WAIT_OBJECT_0);producing=false;for(auto& producer:producers)producer.join();
     check(!std::filesystem::exists(session/("ack-"+nonce+".json")));
    }else{
     request();auto requested=GetTickCount64();
     while(!std::filesystem::exists(session/("ack-"+nonce+".json"))&&GetTickCount64()-requested<60000)Sleep(10);
     check(std::filesystem::exists(session/("ack-"+nonce+".json")));check(sor::write_new(session/L"STOP","STOP\n"));
    }
   }
   check(WaitForSingleObject(thread,60000)==WAIT_OBJECT_0);CloseHandle(thread);check(std::filesystem::exists(session/L"terminal.json"));
   if(s=="worker-guard")check(!std::filesystem::exists(session/("ack-"+nonce+".json"))&&!std::filesystem::exists(session/L"ready.json"));return 0;
  }
  if(s=="context-reasons"){
   Model m;set_model(m);alignas(8) unsigned char frame[0x400]{};
   auto sample=[&](U expected){Event e{};source_context(e,U(frame),U(m.proc));check(e.reason==expected);e.kind=Visited;emit(e);};
   auto restore=[&](){m.put(frame,0x100,U(m.grid));m.put(frame,0x38,U(m.source));m.put(frame,0x3d8,U(m.query));m.put(m.manager,0x130,U(m.proc));m.put(m.proc,0,base+0x4b3f3a8);m.put(m.manager,0x120,U(m.source_index));m.put(m.source_index,0x10,U(m.grid));m.put(m.grid,0,base+0x4b67f48);m.put(m.grid,0x10,uint32_t(1));m.put(m.grid,0x14,uint32_t(1));m.put(m.grid,0x18,U(&m.source_member));m.source_member=U(m.source);};
   restore();sample(ContextOK); // A valid ordinary context, with no target key filter.
   m.put(m.manager,0x130,U(1));sample(ManagerProcMismatch);restore();
   m.put(frame,0x38,U(1));sample(SourceBytesRead);restore();
   m.put(frame,0x3d8,U(1));sample(QueryWordsRead);restore();
   m.put(m.proc,0,U(1));sample(ProcTypeMismatch);restore();
   m.put(m.manager,0x120,U(1));sample(GridPointerRead);restore();
   m.put(m.source_index,0x10,U(1));sample(GridTypeRead);restore();
   m.put(m.grid,0,U(1));sample(GridTypeMismatch);restore();
   m.put(m.grid,0x10,uint32_t(2));sample(GridExtent);restore();
   m.put(m.grid,0x18,U(1));sample(MemberRead);restore();
   m.source_member=1;sample(NotMember);restore();
   ++hazards;sample(ContextLifetime);--hazards;
   m.put(frame,0x100,U(1));sample(GridChanged);restore();
   std::vector<U> large(257,U(m.source));m.put(m.grid,0x10,uint32_t(257));m.put(m.grid,0x14,uint32_t(257));m.put(m.grid,0x18,U(large.data()));sample(GridCoverageLimit);restore();
   m.put(m.source,0,uint32_t(0x123456));sample(ContextOK);
   // A genuine cross-page partial read retains the returned byte count.
   auto* partial=(unsigned char*)VirtualAlloc(nullptr,8192,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);check(partial!=nullptr);DWORD previous{};check(VirtualProtect(partial+4096,4096,PAGE_NOACCESS,&previous)!=0);
   Event e{};unsigned char copied[16]{};check(!context_read(e,U(partial+4090),copied,16,SourceBytesRead));check(e.reason==SourceBytesRead&&e.read_requested==16&&e.read_returned<16);e.kind=Visited;emit(e);VirtualFree(partial,0,MEM_RELEASE);
   check(drain());enabled=false;CloseHandle(raw);CloseHandle(ack);return 0;
  }
  if(s=="in-flight-loss"||s=="loss-cross"||s=="loss-fence"||s=="loss-rebuild"||s=="hook-bounds"||s=="hook-timing"||s=="loss-one"||s=="loss-many"||s=="retry-one"||s=="retry-many"||s=="late-disk-fault"||s=="late-write-fault"||s=="late-flush-fault"||s=="late-ack-fault"||s=="late-ack-write-fault"||s=="ack-write-fault"||s=="hook-stress"||s=="stress"||s=="disk-fault"||s=="write-fault"||s=="flush-fault"||s=="ack-fault"){
   auto force_retry=[&](){U n=enqueue.load();queue[n%capacity].ticket=n+1;Event e{};check(!emit(e));queue[n%capacity].ticket=n;};
   if(s.starts_with("retry-")){for(unsigned i=0;i<(s=="retry-one"?1u:37u);++i)force_retry();check(enabled&&!broken&&full_losses==0);}
   if(s=="loss-one"||s=="loss-many"){for(U i=0;i<capacity;++i){Event e{};e.kind=Ready;check(emit(e));}for(unsigned i=0;i<(s=="loss-one"?1u:37u);++i){Event e{};check(!emit(e));}check(enabled&&!broken&&contention_losses==0);check(drain());}
   if(s=="stress"||s=="hook-stress"){
    Event ready{};ready.kind=Ready;emit(ready);HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);check(thread!=nullptr);
    auto started=GetTickCount64();while(!std::filesystem::exists(session/L"ready.json")&&GetTickCount64()-started<60000)Sleep(1);check(std::filesystem::exists(session/L"ready.json"));
    Model burst;set_model(burst);fixture_provider(U(burst.source),U(burst.proc),U(burst.query),0);
    std::atomic<bool> produce{true};std::vector<std::thread> threads;
    for(unsigned i=0;i<8;++i)threads.emplace_back([&](){model=&burst;while(produce){if(s=="hook-stress")fixture_provider(U(burst.source),U(burst.proc),U(burst.query),0);else {Event e{};e.kind=Mask;e.epoch=epoch;emit(e);}}});
    Sleep(250);produce=false;for(auto& t:threads)t.join();
    while(dequeue.load()!=enqueue.load())Sleep(1);
    Model m;set_model(m);fixture_provider(U(m.source),U(m.proc),U(m.query),0);fixture_provider(U(m.source),U(m.proc),U(m.query),0);
    check(enabled&&!broken);if(s=="stress")check(drops>0);check(sor::write_new(session/L"STOP","STOP\n"));check(WaitForSingleObject(thread,60000)==WAIT_OBJECT_0);CloseHandle(thread);return 0;
   }
   Model m;set_model(m);m.nested=s=="loss-many";m.in_flight_loss=s=="in-flight-loss";
   std::vector<U> members(256,0);std::vector<std::array<U,3>> map_slots(256),resource_slots(256);
   if(s=="hook-bounds"){
    members.back()=U(m.source);m.put(m.grid,0x10,uint32_t(256));m.put(m.grid,0x14,uint32_t(256));m.put(m.grid,0x18,U(members.data()));
    for(auto& row:map_slots)row[2]=0xffffffff;for(auto& row:resource_slots)row[2]=0xffffffff;
    map_slots.back()={U(m.source),U(m.wrapper),0};resource_slots.back()={0x57cf,U(m.collection),0};
    m.put(m.proc,0x20,U(map_slots.data()));m.put(m.proc,0x28,U(256));m.hit_index=255;m.put(m.wrapper,0x20,U(resource_slots.data()));m.put(m.wrapper,0x28,U(256));
    m.put(m.temp,0x18,uint32_t(64));m.put(m.temp,0x1c,uint32_t(64));
   }
   fixture_provider(U(m.source),U(m.proc),U(m.query),0);
   if(s=="loss-cross"||s=="loss-fence"||s=="loss-rebuild"){
    check(drain());for(U i=0;i<capacity;++i){Event e{};e.kind=Ready;check(emit(e));}
    if(s=="loss-fence")fixture_reset(U(m.proc),0,0,0);else {Event e{};check(!emit(e));}
    check(drain());if(s=="loss-rebuild")m.hit=false;
   }
   fixture_provider(U(m.source),U(m.proc),U(m.query),0);
   if(s=="loss-rebuild")fixture_provider(U(m.source),U(m.proc),U(m.query),0);
   if(s=="loss-one"){
    std::vector<std::thread> threads;for(unsigned i=0;i<8;++i)threads.emplace_back([&](){model=&m;for(unsigned j=0;j<4;++j)fixture_provider(U(m.source),U(m.proc),U(m.query),0);});for(auto& t:threads)t.join();
   }
   if(s=="hook-timing"||s=="hook-bounds"){
    check(drain());LARGE_INTEGER frequency{},begin{},end{};QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&begin);for(unsigned i=0;i<64;++i)fixture_provider(U(m.source),U(m.proc),U(m.query),0);QueryPerformanceCounter(&end);double observed=double(end.QuadPart-begin.QuadPart)*1000000/frequency.QuadPart/64;
    check(drain());enabled=false;QueryPerformanceCounter(&begin);for(unsigned i=0;i<64;++i)fixture_provider(U(m.source),U(m.proc),U(m.query),0);QueryPerformanceCounter(&end);double bypassed=double(end.QuadPart-begin.QuadPart)*1000000/frequency.QuadPart/64;enabled=true;
    check(sor::write_new(session/L"timing.json","{\"samples\":64,\"observed_mean_us\":"+std::to_string(observed)+",\"bypassed_mean_us\":"+std::to_string(bypassed)+"}\n"));
   }
   if(s.ends_with("-fault")){if(s.starts_with("late-")){check(drain());Event tail{};tail.kind=Ready;tail.epoch=epoch;check(emit(tail));}fixture_fault=s.find("disk")!=std::string::npos?1:s.find("ack-write")!=std::string::npos?5:s.find("write")!=std::string::npos?2:s.find("flush")!=std::string::npos?3:4;HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);check(thread!=nullptr);check(WaitForSingleObject(thread,60000)==WAIT_OBJECT_0);CloseHandle(thread);return 0;}
   check(drain());check(enabled&&!broken);
   auto terminal=identity+",\"written\":"+std::to_string(enqueue.load())+",\"flushed\":"+std::to_string(flushed.load())+",\"enqueued\":"+std::to_string(enqueue.load())+metrics()+",\"failed\":false,\"resident_inert\":true}\n";
   check(sor::write_new(session/L"terminal.json",terminal));enabled=false;CloseHandle(raw);CloseHandle(ack);return 0;
  }
  Model m;set_model(m);m.partial=s=="partial"||s=="inserted-empty";m.failed_copy=s=="failed-copy";m.torn_copy=s=="contrary";m.nested=s=="nested";m.raise=s=="generation-exception";m.descriptor_change=s=="descriptor-change";if(s=="mask-zero")m.mask=0;if(s=="unexpected-mask")m.mask=127;if(s=="mixed-partial")m.mask=254;
  if(s=="owner-mismatch")m.put(m.manager,0x80,uint32_t(0x5e0df));
  if(s=="bad-read")m.source_member=1;
  if(s=="hit-only"){native_copy(0,0,0,0);m.hit=true;m.slots[2]=0;}
  if(s=="overflow"){for(unsigned i=0;i<capacity+2;++i){Event e{};e.kind=Mask;emit(e);}check(drops==2&&!broken&&enabled);}
  else {
   if(s!="concurrent-miss"){
    bool threw=false;try{fixture_provider(U(m.source),U(m.proc),U(m.query),s=="bypass");}catch(const std::runtime_error&){threw=true;}
    check(threw==(s=="generation-exception"));if(threw){m.raise=false;m.hit=true;}
   }
   if(s=="reset"||s=="aba"||s=="destroy"||s=="erase"||s=="clear"||s=="retire"){
    Four funcs[]{&fixture_reset,&fixture_destroy,&fixture_erase,&fixture_clear,&fixture_retire};
    unsigned index=s=="destroy"?1:s=="erase"?2:s=="clear"?3:s=="retire"?4:0;
    check(funcs[index](U(m.proc),0,0,0)==U(m.proc));
    if(s=="aba"){m.~Model();new(&m)Model;set_model(m);native_copy(0,0,0,0);m.hit=true;m.slots[2]=0;}
   }
   if(s=="concurrent"||s=="concurrent-miss"){
    std::vector<std::thread> threads;for(int i=0;i<8;++i)threads.emplace_back([&](){model=&m;for(int j=0;j<4;++j)fixture_provider(U(m.source),U(m.proc),U(m.query),0);});
    for(auto& thread:threads)thread.join();
   }
   m.query[1]+=2;
   if(s=="owner-change")m.put(m.manager,0x80,uint32_t(0x5e0df));
   if(s=="mode-change")m.manager[0x20]=1;
   if(s!="bypass"&&s!="partial"&&s!="failed-copy"&&s!="hit-only")fixture_provider(U(m.source),U(m.proc),U(m.query),0);
  }
  if(s=="crash-before")TerminateProcess(GetCurrentProcess(),71);
  if(s=="output-failure"){CloseHandle(raw);raw=INVALID_HANDLE_VALUE;check(!drain());return 0;}
  check(drain());
  if(s=="crash-after")TerminateProcess(GetCurrentProcess(),72);
  enabled=false;CloseHandle(raw);CloseHandle(ack);return 0;
 }catch(...){return 91;}
}
