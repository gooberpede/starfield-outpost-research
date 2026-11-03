// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Offline D5AM component, not a retail plugin. Queue method is source-informed
// by this project's observer.h (SOR-P-0002); no historical source is modified.
#define NOMINMAX
#include <Windows.h>
#include <atomic>
#include <cstdint>
namespace d5am {
using U=uint64_t;
constexpr U capacity=1024;
struct Event {U sequence{},kind{},thread{},ticks{},lock{},generation{},old_state{},new_state{};};
struct Cell {Event event{};std::atomic<U> ticket{};};
inline Cell cells[capacity];
inline std::atomic<U> enqueue{},dequeue{},active{},drops{},reentrant{},generation{};
inline std::atomic<U> watched{},unregistered{},held_tid{};
inline std::atomic<bool> enabled{},failed{},hold_pending{},pending_held{};
inline thread_local bool busy{};
inline U tick() noexcept {LARGE_INTEGER t{};QueryPerformanceCounter(&t);return U(t.QuadPart);}
inline void initialize(U address,U lifetime) noexcept {
 enabled=false;
 enqueue=0;dequeue=0;active=0;drops=0;reentrant=0;unregistered=0;
 failed=false;hold_pending=false;pending_held=false;held_tid=0;
 for(U i=0;i<capacity;++i)cells[i].ticket=i;
 watched=address;generation=lifetime;enabled=true;
}
inline bool pop(Event& e) noexcept {
 U n=dequeue.load();auto& c=cells[n%capacity];
 if(c.ticket.load(std::memory_order_acquire)!=n+1)return false;
 e=c.event;c.ticket.store(n+capacity,std::memory_order_release);dequeue=n+1;return true;
}
inline void collect(U address,U old,U kind) noexcept {
 DWORD error=GetLastError();++active;
 struct Leave {DWORD error;~Leave(){--active;SetLastError(error);}} leave{error};
 if(!enabled.load())return;
 if(address!=watched.load()) {++unregistered;return;}
 if(busy){++reentrant;++drops;failed=true;return;}
 busy=true;struct Busy {~Busy(){busy=false;}} reset;
 Event e{};e.kind=kind;e.thread=GetCurrentThreadId();e.ticks=tick();
 e.lock=address;e.generation=generation.load();e.old_state=uint32_t(old);
 e.new_state=uint32_t(old+(kind==1?0x1000:0x400000));
 U n=enqueue.load();bool published=false;
 for(unsigned tries=0;tries<32;++tries){
  if(n>U(INT64_MAX)-capacity)break;
  auto& c=cells[n%capacity];auto delta=int64_t(c.ticket.load(std::memory_order_acquire))-int64_t(n);
  if(delta<0)break;
  if(delta>0){n=enqueue.load();continue;}
  if(enqueue.compare_exchange_weak(n,n+1)){
   e.sequence=n+1;c.event=e;c.ticket.store(n+1,std::memory_order_release);published=true;break;
  }
 }
 if(!published){++drops;failed=true;}
 // Explicit private-fixture intervention, never part of the proposed native
 // probe's production behavior. It demonstrates observer-induced overtaking.
 if(kind==1&&hold_pending.load()&&held_tid.load()==e.thread){
  pending_held=true;while(hold_pending.load())YieldProcessor();
 }
}
}
