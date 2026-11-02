// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Baseline content endings only. No dereference of an ended receiver is made.
#include "patch.h"
#include "../exp0002/win_support.h"
namespace winner::lifetime {
constexpr U capacity=32768;
struct Event {U sequence{},kind{},phase{},invocation{},parent{},thread{},ticks{},receiver{},allocation{},status{},epoch{},hazards{};};
struct Mark {U cursor{},ticks{},generation_before{},generation_after{},active_before{},active_after{},loss{},failed{};};
struct FileHeader {U magic=0x31464c4941493544ULL,version=1,header_bytes=96,event_bytes=96,armed_ticks{},armed_thread{},epoch_at_arm{},reserved{};unsigned char identity_sha256[32]{};};
static_assert(sizeof(Event)==96&&sizeof(Mark)==64&&sizeof(FileHeader)==96);
struct Cell {Event event{};std::atomic<U> ticket{};};
inline Cell queue[capacity];
inline std::atomic<U> enqueue{},dequeue{},active{},generation{},drops{},tokens{},unlogged_cutoff{};
inline std::atomic<bool> failed{},counter_overflow{};
inline bool configured{};inline FileHeader file_header{};
inline Patch edits[3]{};inline Four originals[3]{};inline unsigned char* pages[3]{};
inline std::string original_hash[3],body_hash[3],page_hash[3];
inline thread_local U current{};
inline HANDLE fixture_reserved{},fixture_publish{};
inline std::atomic<bool> fixture_hold{};
inline U tick() noexcept {LARGE_INTEGER t{};QueryPerformanceCounter(&t);return U(t.QuadPart);}
inline Mark mark() noexcept {
 Mark m{};m.generation_before=generation.load();m.active_before=active.load();m.cursor=enqueue.load();m.ticks=tick();
 m.active_after=active.load();m.generation_after=generation.load();m.loss=drops.load();m.failed=failed.load();return m;
}
inline bool coherent(const Mark& m) noexcept {return !m.active_before&&!m.active_after&&!m.loss&&!m.failed&&m.generation_before==m.generation_after;}
inline U increment(std::atomic<U>& counter) noexcept {U old=counter.fetch_add(1);if(old==UINT64_MAX){counter_overflow=true;failed=true;}return old+1;}
inline void lose() noexcept {increment(drops);failed=true;}
inline bool emit(Event e) noexcept {
 U n=enqueue.load();
 for(unsigned tries=0;tries<32;++tries){
  if(n>U(INT64_MAX)-capacity){lose();return false;}
  auto& c=queue[n%capacity];auto difference=int64_t(c.ticket.load(std::memory_order_acquire))-int64_t(n);
  if(difference>0){n=enqueue.load();continue;}if(difference<0){lose();return false;}
  if(enqueue.compare_exchange_weak(n,n+1)){
   if(fixture_reserved){SetEvent(fixture_reserved);WaitForSingleObject(fixture_publish,INFINITE);}
   e.sequence=n+1;c.event=e;c.ticket.store(n+1,std::memory_order_release);return true;
  }
 }lose();return false;
}
inline bool pop(Event& e) noexcept {U n=dequeue.load();auto& c=queue[n%capacity];if(c.ticket.load(std::memory_order_acquire)!=n+1)return false;e=c.event;c.ticket.store(n+capacity,std::memory_order_release);dequeue=n+1;return true;}
template<unsigned I> U hook(U receiver,U b,U c,U d){
 DWORD incoming_error=GetLastError();
 ++winner::active;increment(active);increment(generation);
 struct Leave {~Leave(){increment(generation);--active;--winner::active;}} leave;
 if(!enabled.load()){U zero=0;unlogged_cutoff.compare_exchange_strong(zero,tick());SetLastError(incoming_error);return originals[I](receiver,b,c,d);}
 Event e{};e.kind=I+1;e.invocation=increment(tokens);e.parent=current;e.thread=GetCurrentThreadId();e.ticks=tick();e.receiver=receiver;
 e.allocation=receiver-(I==0?16:8);e.epoch=winner::epoch.load();e.hazards=winner::hazards.load();
 U previous=current;current=e.invocation;struct Current {U previous;~Current(){current=previous;}} restore{previous};
 if(e.invocation)emit(e);
 SetLastError(incoming_error);
 try {U result=originals[I](receiver,b,c,d);DWORD outgoing_error=GetLastError();e.phase=1;e.ticks=tick();e.epoch=winner::epoch.load();e.hazards=winner::hazards.load();if(e.invocation)emit(e);SetLastError(outgoing_error);return result;}
 catch(...){DWORD outgoing_error=GetLastError();e.phase=1;e.status=Exception;e.ticks=tick();e.epoch=winner::epoch.load();e.hazards=winner::hazards.load();if(e.invocation)emit(e);SetLastError(outgoing_error);throw;}
}
inline bool configure(void* holder,void* collection,void* mutation,const char* h,const char* c,const char* m){
 void* sites[]{holder,collection,mutation};const char* hashes[]{h,c,m};void* hooks[]{(void*)&hook<0>,(void*)&hook<1>,(void*)&hook<2>};
 for(unsigned i=0;i<3;++i){
  unsigned char bytes[32]{};const unsigned char expected[]{0x48,0x89,0x5c,0x24,(unsigned char)(i==2?16:8)};
  if(!read(U(sites[i]),bytes,32)||memcmp(bytes,expected,5)||sor::sha_bytes(bytes,32)!=hashes[i])return false;
  auto& p=edits[i];p.at=(unsigned char*)sites[i];p.n=5;memcpy(p.before,bytes,5);original_hash[i]=hashes[i];body_hash[i]=sor::sha_bytes(bytes+5,27);
  auto* page=near_page(U(p.at));if(!page)return false;pages[i]=page;jump(page,U(hooks[i]));if(!relative(p,U(page),0xe9))return false;
  memcpy(page+32,bytes,5);jump(page+37,U(p.at)+5);originals[i]=(Four)(page+32);
  DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;page_hash[i]=sor::sha_bytes(page,4096);
 }configured=true;return true;
}
inline bool guards(){if(!configured)return true;for(unsigned i=0;i<3;++i){unsigned char bytes[27]{};if(!match(edits[i],true)||!read(U(edits[i].at)+5,bytes,27)||sor::sha_bytes(bytes,27)!=body_hash[i]||sor::sha_bytes(pages[i],4096)!=page_hash[i])return false;}return true;}
inline std::string metadata(){
 const char* names[]{"HOLDER_RESOURCE_MAP","COLLECTION_GEOMETRY","COLLECTION_MUTATION"};
 std::string s=",\"lifetime_schema\":\"sor-d5ai-lifetime/1\",\"lifetime_header_bytes\":96,\"lifetime_event_bytes\":96,\"lifetime_capacity\":32768,\"lifetime_sites\":[";
 if(configured)for(unsigned i=0;i<3;++i){if(i)s+=",";s+="{\"va\":"+std::to_string(U(edits[i].at))+",\"bytes\":5,\"kind\":"+sor::quote(names[i])+",\"allocation_adjustment\":"+std::to_string(i==0?16:8)+",\"guard_sha256\":"+sor::quote(original_hash[i])+"}";}
 return s+"]";
}
bool begin();bool drain();void close();std::string metrics();
}
