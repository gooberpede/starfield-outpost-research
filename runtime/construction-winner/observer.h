// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#define NOMINMAX
#include <Windows.h>
#include <atomic>
#include <cstdint>
#include <cstring>
#include <exception>
namespace winner {
using U=uint64_t;
using Four=U(*)(U,U,U,U);
using Generate=void(*)(U,U,U,uint32_t,U,U);
enum Kind:U {Entry=1,Selected,Visited,Lookup,Descriptor,Generating,Sample,Generated,Returned,FenceBegin,FenceEnd,Cold,Ready};
enum Status:U {ReadFailure=1,NoInvocation=2,ContextMismatch=4,LifetimeInvalid=8,Exception=16,MapOperandsUnavailable=32};
// All addresses are runtime VAs. request contains the original signed Int2.
struct Event {
 U sequence{},kind{},invocation{},parent{},thread{},ticks{},epoch{},hazards{},status{};
 U proc{},source{},frame{},holder{},a{},b{},c{},d{},selection{};
 int32_t request[2]{};
 unsigned char source_bytes[0x70]{},descriptor[0x2c]{};
 uint32_t reserved{};
};
static_assert(sizeof(Event)==312);
constexpr U capacity=1024;
struct Cell {Event event{};std::atomic<U> ticket{};};
inline Cell queue[capacity];
inline std::atomic<U> enqueue{},dequeue{},epoch{1},hazards{},tokens{},active{},drops{},full_losses{},contention_losses{},retries{},high_water{},first_loss{},last_loss{},loss_generation{};
inline std::atomic<bool> enabled{},broken{},counter_overflow{};
// Set only by the host-checked disposable entry. Never for retail acquisition.
inline thread_local unsigned fixture_retry_failures{};
inline U base{};
struct PreserveError {DWORD value=GetLastError();~PreserveError(){SetLastError(value);}};
inline Four provider_original{},lookup_original{},descriptor_original{},normalizer_original{},sample_original{},cold_original{},fences[5]{};
inline Generate generate_original{};
inline bool read(U p,void* out,size_t n) noexcept {
 PreserveError preserve;
 SIZE_T got{};return p>=0x10000&&p<0x7fffffffffffULL-n&&ReadProcessMemory(GetCurrentProcess(),(void*)p,out,n,&got)&&got==n;
}
template<class T> bool field(U p,T& out) noexcept {return read(p,&out,sizeof out);}
inline void increment(std::atomic<U>& n) noexcept {if(n.fetch_add(1)==UINT64_MAX){counter_overflow=true;broken=true;enabled=false;}}
inline U token() noexcept {U n=tokens.fetch_add(1);if(n==UINT64_MAX){counter_overflow=true;broken=true;enabled=false;return 0;}return n+1;}
inline void initialize_queue(U origin=0){enqueue=origin;dequeue=origin;for(U i=0;i<capacity;++i)queue[(origin+i)%capacity].ticket=origin+i;}
inline void lose(bool full) noexcept {
 increment(drops);increment(full?full_losses:contention_losses);increment(loss_generation);increment(epoch);
 U boundary=enqueue.load()+1,zero=0;first_loss.compare_exchange_strong(zero,boundary);last_loss=boundary;
}
inline bool emit(Event e) noexcept {
 PreserveError preserve;
 // Include orphan/diagnostic producers in STOP's publication handshake.
 struct Producer {Producer(){++active;}~Producer(){--active;}} producer;
 if(!enabled)return false;
 if(fixture_retry_failures){--fixture_retry_failures;for(unsigned i=0;i<32;++i)increment(retries);lose(false);return false;}
 e.thread=GetCurrentThreadId();LARGE_INTEGER t{};QueryPerformanceCounter(&t);e.ticks=U(t.QuadPart);
 U n=enqueue.load();
 for(unsigned tries=0;tries<32;++tries){
  if(n>U(INT64_MAX)-capacity){counter_overflow=true;broken=true;enabled=false;return false;}
  auto& cell=queue[n%capacity];auto difference=int64_t(cell.ticket.load(std::memory_order_acquire))-int64_t(n);
  if(difference>0){increment(retries);n=enqueue.load();continue;}
  if(difference<0){lose(true);return false;}
  if(enqueue.compare_exchange_weak(n,n+1)){
   e.sequence=n+1;cell.event=e;cell.ticket.store(n+1,std::memory_order_release);
   U used=n+1-dequeue.load(),peak=high_water.load();if(used<=capacity&&used>peak)high_water.compare_exchange_strong(peak,used);
   return true;
  }increment(retries);
 }lose(false);return false;
}
inline bool pop(Event& e) noexcept {
 U n=dequeue.load();auto& cell=queue[n%capacity];if(cell.ticket.load(std::memory_order_acquire)!=n+1)return false;
 e=cell.event;cell.ticket.store(n+capacity,std::memory_order_release);dequeue=n+1;return true;
}
struct Scope {Event e{},original{};Scope* previous{};};
inline thread_local Scope* current{};
struct Conversion {Scope* owner{};U input{},manager{};Conversion* previous{};};
inline thread_local Conversion* conversion{};
inline thread_local bool generating{};
inline thread_local unsigned reset_depth{};
inline Event event(Kind kind) noexcept {Event e=current?current->e:Event{};e.kind=kind;if(!current){e.status|=NoInvocation;e.epoch=epoch;e.hazards=hazards;}return e;}
inline bool stable(const Event& e) noexcept {return !hazards.load()&&!e.hazards&&e.epoch==epoch.load()&&!broken.load();}
struct Active {Active(){++active;}~Active(){--active;}};
inline U provider_hook(U proc,U query,U holder,U extra){
 if(!enabled)return provider_original(proc,query,holder,extra);
 Active activity;Scope scope{};scope.previous=current;scope.e.invocation=token();scope.e.parent=current?current->e.invocation:0;
 scope.e.proc=proc;scope.e.holder=holder;scope.e.epoch=epoch;scope.e.hazards=hazards;
 if(!read(query,scope.e.request,8))scope.e.status|=ReadFailure;
 scope.original=scope.e;
 current=&scope;auto e=event(Entry);e.a=query;emit(e);
 struct Restore {Scope* old;int exceptions=std::uncaught_exceptions();~Restore(){auto e=event(Returned);if(std::uncaught_exceptions()>exceptions)e.status|=Exception;if(!stable(e))e.status|=LifetimeInvalid;emit(e);current=old;}} restore{scope.previous};
 return provider_original(proc,query,holder,extra);
}
inline void selected_capture(U frame,U proc,U source) noexcept {
 if(!enabled)return;
 auto e=current?current->original:event(Selected);e.kind=Selected;e.frame=frame;e.source=source;e.selection=token();
 if(e.proc!=proc)e.status|=ContextMismatch;if(!stable(e))e.status|=LifetimeInvalid;
 // The pointer has just been selected by native code; do not dereference it here.
 if(current){current->e=e;current->e.kind=0;}emit(e);
}
inline void visited_capture(U frame,U proc,U visited) noexcept {
 if(!enabled)return;auto e=event(Visited);e.a=visited&255;
 if(e.frame!=frame||e.proc!=proc)e.status|=ContextMismatch;
 if(!stable(e))e.status|=LifetimeInvalid;emit(e);
}
inline U lookup_hook(U a,U b,U c,U d){
 if(!enabled)return lookup_original(a,b,c,d);
 Active activity;auto result=lookup_original(a,b,c,d);auto e=event(Lookup);U source{},capacity_word{},expected_proc=e.proc;
 e.a=result;e.d=epoch;e.proc=a-0x10;
 if(!field(b,source)||!field(e.proc+0x28,capacity_word))e.status|=ReadFailure|MapOperandsUnavailable;
 e.b=capacity_word;e.c=source;
 if(expected_proc!=e.proc||source!=e.source)e.status|=ContextMismatch;
 if(!stable(e))e.status|=LifetimeInvalid;
 // Native caller holds ProcGen exclusive protection here. No observer lock/scan.
 if(!e.status&&!read(source,e.source_bytes,sizeof e.source_bytes))e.status|=ReadFailure;
 if(current){current->e.status|=e.status;memcpy(current->e.source_bytes,e.source_bytes,sizeof e.source_bytes);}
 emit(e);return result;
}
inline U descriptor_hook(U a,U b,U c,U d){
 if(!enabled)return descriptor_original(a,b,c,d);
 Conversion local{current,c,a,conversion};conversion=&local;
 struct Restore {Conversion* previous;~Restore(){conversion=previous;}} restore{local.previous};
 return descriptor_original(a,b,c,d);
}
inline U normalizer_hook(U a,U b,U c,U d){
 if(!enabled||!conversion||!current||conversion->owner!=current)return normalizer_original(a,b,c,d);
 auto e=event(Descriptor);int32_t request[2]{};e.a=a;e.b=b;e.c=c;e.d=conversion->input;e.holder=conversion->manager;
 // These are the engine's consumed stack copies, not mutable manager storage.
 if(!read(b,e.descriptor,sizeof e.descriptor)||!read(c,request,8))e.status|=ReadFailure;
 if(memcmp(request,e.request,8))e.status|=ContextMismatch;
 if(!stable(e))e.status|=LifetimeInvalid;
 if(current){current->e.status|=e.status;memcpy(current->e.descriptor,e.descriptor,sizeof e.descriptor);}emit(e);
 return normalizer_original(a,b,c,d);
}
inline void generate_hook(U source,U origin,U geographic,uint32_t owner,U biome,U out){
 if(!enabled){generate_original(source,origin,geographic,owner,biome,out);return;}
 Active activity;auto e=event(Generating);e.a=owner;e.b=biome;e.c=geographic;e.d=out;
 if(e.source!=source)e.status|=ContextMismatch;if(!stable(e))e.status|=LifetimeInvalid;emit(e);
 bool previous=generating;generating=true;
 struct Restore {bool old;int exceptions=std::uncaught_exceptions();~Restore(){auto e=event(Generated);if(std::uncaught_exceptions()>exceptions)e.status|=Exception;if(!stable(e))e.status|=LifetimeInvalid;emit(e);generating=old;}} restore{previous};
 generate_original(source,origin,geographic,owner,biome,out);
}
inline U sample_hook(U a,U b,U c,U d){
 auto result=sample_original(a,b,c,d);
 if(enabled){auto e=event(Sample);e.a=result&255;e.b=a;e.c=b;if(!generating)e.status|=ContextMismatch;if(!stable(e))e.status|=LifetimeInvalid;emit(e);}
 return result;
}
template<unsigned N> U fence_hook(U a,U b,U c,U d){
 if(!enabled)return fences[N](a,b,c,d);
 Active activity;++hazards;increment(epoch);if constexpr(N==0)++reset_depth;
 Event e{};e.kind=FenceBegin;e.a=N;e.proc=a;e.epoch=epoch;e.hazards=hazards;emit(e);
 struct End {U proc;int exceptions=std::uncaught_exceptions();~End(){if constexpr(N==0)--reset_depth;else increment(epoch);--hazards;Event e{};e.kind=FenceEnd;e.a=N;e.proc=proc;e.epoch=epoch;e.hazards=hazards;if(std::uncaught_exceptions()>exceptions)e.status|=Exception;emit(e);}} end{a};
 return fences[N](a,b,c,d);
}
inline U cold_hook(U a,U b,U c,U d){
 if(enabled){Event e{};e.kind=Cold;e.proc=a-0x40;e.epoch=epoch;e.hazards=hazards;
  // Exact checked native site follows both clears while exclusive ownership holds.
  // Record the direct visited fields; map emptiness follows the pinned reset CFG.
  if(reset_depth!=1||hazards.load()!=1)e.status|=LifetimeInvalid;
  U visited{},data{};if(!field(e.proc+0x48,visited)||!field(e.proc+0x50,data))e.status|=ReadFailure;
  e.a=visited;e.b=data;if(visited||data)e.status|=ContextMismatch;emit(e);
 }return cold_original(a,b,c,d);
}
}
