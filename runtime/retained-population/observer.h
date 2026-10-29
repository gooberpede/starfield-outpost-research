// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#define NOMINMAX
#include <Windows.h>
#include <atomic>
#include <array>
#include <cstdint>
#include <cstring>
#include <intrin.h>
#include <exception>
namespace retained {
using U=uint64_t;
using Four=U(*)(U,U,U,U);
using Generate=void(*)(U,U,U,uint32_t,U,U);
enum Kind:U {Visited=1,Lookup,Query,Mask,Copy,Completed,Fence,Loss,Ready,Stopped,Temporary};
// Fixed native-word payload. Read failure is explicit; zero is never a substitute.
struct Event {
 U sequence{},kind{},invocation{},parent{},thread{},epoch{},hazards{},status{};
 U frame{},manager{},proc{},source{},wrapper{},collection{},index{},resource{};
 U args[6]{};uint32_t count{},owner{};
 unsigned char source_bytes[0x70]{},descriptor[0x2c]{},region[0x30]{},points[1024]{};
 // Schema 2 suffix. Operands are diagnostic VAs/words, never stable identities.
 U reason{},read_address{},read_requested{},read_returned{},read_error{};
 U actual_proc{},proc_type{},source_index{},grid{},grid_type{},members{},grid_count{},grid_capacity{},retained_grid{};
};
static_assert(sizeof(Event)==1528);
inline std::atomic<U> epoch{1},hazards{},tokens{},drops{},active{};
inline std::atomic<bool> enabled{},broken{};
inline std::atomic<U> full_losses{},contention_losses{},retries{},high_water{},first_loss{},last_loss{},loss_generation{};
inline std::atomic<bool> counter_overflow{};
inline void increment(std::atomic<U>& counter) noexcept {
 if(counter.fetch_add(1)==UINT64_MAX){counter_overflow=true;broken=true;enabled=false;}
}
inline U next_token() noexcept {U old=tokens.fetch_add(1);if(old==UINT64_MAX){counter_overflow=true;broken=true;enabled=false;return 0;}return old+1;}
struct ActiveScope {ActiveScope(){++active;}~ActiveScope(){--active;}};
inline U base{};
inline Four lookup_original{},query_original{},mask_original{},copy_original{},fences[5]{};
inline Generate generate_original{};
inline bool read(U p,void* out,size_t n) noexcept {
 SIZE_T got{};return p>=0x10000 && p<0x7fffffffffffULL-n && ReadProcessMemory(GetCurrentProcess(),(void*)p,out,n,&got)&&got==n;
}
template<class T> bool field(U p,T& out) noexcept {return read(p,&out,sizeof out);}
struct Cell {Event event{};std::atomic<U> ticket{};};
// Reusable MPSC ring with per-cell publication. Producers never wait for space.
// Ordinary admission loss advances continuity but never disables acquisition.
constexpr U capacity=1024;
inline Cell queue[capacity];inline std::atomic<U> enqueue{},dequeue{};
inline void initialize_queue(){for(U i=0;i<capacity;++i)queue[i].ticket=i;}
inline void lose(bool full) noexcept {
 increment(drops);increment(full?full_losses:contention_losses);increment(loss_generation);increment(epoch);
 U boundary=enqueue.load()+1,zero=0;first_loss.compare_exchange_strong(zero,boundary);last_loss=boundary;
}
inline bool emit(Event e) noexcept {
 if(!enabled)return false;
 U n=enqueue.load();
 if(n>U(INT64_MAX)-capacity){counter_overflow=true;broken=true;enabled=false;return false;}
 for(unsigned tries=0;tries<32;++tries){
  if(n>U(INT64_MAX)-capacity){counter_overflow=true;broken=true;enabled=false;return false;}
  auto& c=queue[n%capacity];auto ticket=c.ticket.load(std::memory_order_acquire);
  auto difference=int64_t(ticket)-int64_t(n);
  if(difference>0){increment(retries);n=enqueue.load();continue;}
  if(difference<0){lose(true);return false;}
  if(enqueue.compare_exchange_weak(n,n+1)){
   e.sequence=n+1;e.thread=GetCurrentThreadId();c.event=e;c.ticket.store(n+1,std::memory_order_release);
   U occupied=n+1-dequeue.load(),peak=high_water.load();
   if(occupied<=capacity&&occupied>peak)high_water.compare_exchange_strong(peak,occupied);
   return true;
  }
  increment(retries);
 }
 lose(false);return false;
}
inline bool pop(Event& e) noexcept {
 U n=dequeue.load();auto& c=queue[n%capacity];if(c.ticket.load(std::memory_order_acquire)!=n+1)return false;
 e=c.event;c.ticket.store(n+capacity,std::memory_order_release);dequeue=n+1;return true;
}
struct Context {Event e{};bool valid{};};
inline thread_local Context pending{};
inline thread_local Context* generating{};
inline Event current(Kind kind){Event e=generating?generating->e:pending.e;e.kind=kind;e.count=0;return e;}
inline bool stable(const Event& e){return !hazards.load()&&e.epoch==epoch.load()&&!broken.load();}
enum Reason:U {ContextOK=0,SingletonRead=1,SourcePointerRead,QueryPointerRead,ManagerProcRead,ManagerProcMismatch,
 ModeRead,SourceBytesRead,QueryWordsRead,OwnerRead,DescriptorRead,ProcTypeRead,ProcTypeMismatch,
 IndexRead,GridPointerRead,GridTypeRead,GridTypeMismatch,GridCountRead,GridCapacityRead,GridExtent,
 GridDataRead,MemberRead,NotMember,ContextLifetime,GridCoverageLimit,RetainedGridRead,GridChanged};
inline bool context_read(Event& e,U address,void* out,size_t size,Reason reason) noexcept {
 SIZE_T got{};SetLastError(0);
 bool ok=address>=0x10000&&address<0x7fffffffffffULL-size&&ReadProcessMemory(GetCurrentProcess(),(void*)address,out,size,&got)&&got==size;
 if(!ok){e.reason=reason;e.status|=1;e.read_address=address;e.read_requested=size;e.read_returned=got;e.read_error=GetLastError();}
 return ok;
}
template<class T> bool context_field(Event& e,U address,T& out,Reason reason) noexcept {return context_read(e,address,&out,sizeof out,reason);}
inline void source_context(Event& e,U w,U proc) noexcept {
 e.frame=w;e.proc=proc;e.epoch=epoch;e.hazards=hazards;
 U singleton{},query{};uint8_t mode{};
 bool ok=context_field(e,base+0x5fd9c30,singleton,SingletonRead)&&context_field(e,w+0x38,e.source,SourcePointerRead)&&context_field(e,w+0x3d8,query,QueryPointerRead);
 e.manager=singleton;
 auto predicate=[&](bool pass,Reason r){if(!pass){e.reason=r;e.status|=1;}return pass;};
 ok=ok&&context_field(e,singleton+0x130,e.actual_proc,ManagerProcRead)&&predicate(e.actual_proc==proc,ManagerProcMismatch)&&context_field(e,singleton+0x20,mode,ModeRead);
 ok=ok&&context_read(e,e.source,e.source_bytes,sizeof e.source_bytes,SourceBytesRead)&&context_read(e,query,e.args,8,QueryWordsRead);
 ok=ok&&context_field(e,singleton+0x80,e.owner,OwnerRead)&&context_read(e,singleton+(mode==3?0x1c0:0xc8),e.descriptor,sizeof e.descriptor,DescriptorRead);
 e.args[4]=mode;
 uint32_t n{},grid_capacity{};bool member=false;
 ok=ok&&context_field(e,proc,e.proc_type,ProcTypeRead)&&predicate(e.proc_type==base+0x4b3f3a8,ProcTypeMismatch)&&context_field(e,singleton+0x120,e.source_index,IndexRead)&&context_field(e,e.source_index+0x10,e.grid,GridPointerRead);
 ok=ok&&context_field(e,e.grid,e.grid_type,GridTypeRead)&&predicate(e.grid_type==base+0x4b67f48,GridTypeMismatch)&&context_field(e,e.grid+0x10,n,GridCountRead)&&context_field(e,e.grid+0x14,grid_capacity,GridCapacityRead);
 e.grid_count=n;e.grid_capacity=grid_capacity;
 ok=ok&&predicate(n<=grid_capacity,GridExtent)&&predicate(n<=256,GridCoverageLimit)&&context_field(e,e.grid+0x18,e.members,GridDataRead);
 for(uint32_t i=0;ok&&i<n;++i){U value{};ok=context_field(e,e.members+i*8,value,MemberRead);member|=ok&&value==e.source;}
 ok=ok&&predicate(member,NotMember);
 ok=ok&&context_field(e,w+0x100,e.retained_grid,RetainedGridRead)&&predicate(e.retained_grid==e.grid,GridChanged);
 ok=ok&&predicate(!e.hazards&&stable(e),ContextLifetime);
 if(!ok)e.status|=1;
}
inline void capture_visited(U w,U proc,U saved_rsi) noexcept {
 if(!enabled)return;
 ++active;Context c{};c.e.invocation=next_token();c.e.parent=generating?generating->e.invocation:0;
 source_context(c.e,w,proc);c.e.kind=Visited;c.e.args[1]=saved_rsi&255;c.valid=!c.e.status&&!c.e.hazards;
 pending=c;emit(c.e);--active;
}
inline bool region(Event& e,U address) noexcept {
 uint32_t n{},cap{};U points{};
 if(!read(address,e.region,sizeof e.region))return false;
 memcpy(&n,e.region+0x18,4);memcpy(&cap,e.region+0x1c,4);memcpy(&points,e.region+0x20,8);
 if(!n||n>64||n>cap||!read(points,e.points,n*16))return false;
 e.count=n;e.args[5]=address;return true;
}
// Scan only bounded native owned tables under the provider's existing lock.
// A found region is a witness, never a census of all generated regions.
inline bool owned(Event& e,U wanted_collection=0,U wanted_index=0) noexcept {
 U slots{},cap{};if(!field(e.proc+0x20,slots)||!field(e.proc+0x28,cap)||cap>256)return false;
 for(U i=0;i<cap;++i){U row[3]{};if(!read(slots+i*24,row,sizeof row))return false;
  if(uint32_t(row[2])==0xffffffff||row[0]!=e.source)continue;
  e.wrapper=row[1];U resources{},rcap{};int32_t references{};
  if(!field(e.wrapper,references)||references<=0||!field(e.wrapper+0x20,resources)||!field(e.wrapper+0x28,rcap)||rcap>256)return false;
  for(U j=0;j<rcap;++j){U r[3]{};if(!read(resources+j*24,r,sizeof r))return false;
   if(uint32_t(r[2])==0xffffffff||!r[1]||(wanted_collection&&r[1]!=wanted_collection))continue;
   uint32_t n{},c{};U data{};
   if(!field(r[1],references)||references<=0||!field(r[1]+8,n)||!field(r[1]+12,c)||!field(r[1]+16,data)||n>c||n>256)return false;
   if(!n||wanted_index>=n)continue;
   Event candidate=e;candidate.collection=r[1];candidate.index=wanted_index;candidate.resource=uint32_t(r[0]);
   if(region(candidate,data+wanted_index*0x30)){e=candidate;return true;}
  }
 }return false;
}
__declspec(noinline) inline U lookup_hook(U a,U b,U c,U d){
 if(!enabled)return lookup_original(a,b,c,d);
 ActiveScope active_scope;U w=b-0x38;Context saved=pending;
 if(!pending.valid||pending.e.frame!=w||pending.e.proc!=a-0x10){pending={};source_context(pending.e,w,a-0x10);pending.e.status|=2;}
 auto result=lookup_original(a,b,c,d);Event e=pending.e;e.kind=Lookup;e.args[2]=result;U cap{};
 if(!field(e.proc+0x28,cap))e.status|=1;e.args[3]=cap;
 if(result!=cap&&!owned(e))e.status|=4;
 if(!stable(e))e.status|=8;emit(e);pending.e.wrapper=e.wrapper;
 // Nested generation uses its own scope; the outer context is restored by it.
 (void)saved;return result;
}
inline U query_hook(U a,U b,U c,U d){
 if(!enabled)return query_original(a,b,c,d);
 ActiveScope active_scope;auto result=query_original(a,b,c,d);Event e=pending.e;e.kind=Query;e.args[2]=c;e.args[3]=d;
 if(!read(d,e.args,8)||!read(c,e.descriptor,sizeof e.descriptor))e.status|=1;emit(e);return result;
}
inline U mask_hook(U a,U b,U c,U d){
 if(!enabled)return mask_original(a,b,c,d);
 auto result=mask_original(a,b,c,d);if(generating){Event e=current(Mask);e.args[2]=result&255;e.args[3]=a;
 if(!read(b,e.args,8))e.status|=1;emit(e);}return result;
}
inline U copy_hook(U a,U b,U c,U d){
 if(!enabled)return copy_original(a,b,c,d);
 U copy_token=next_token();Event before{};bool sampled=false;if(generating){before=current(Temporary);before.collection=a-8;before.args[3]=copy_token;sampled=region(before,b);if(!sampled)before.status|=16;emit(before);}
 auto result=copy_original(a,b,c,d);
 if(generating){Event e=current(Copy);e.collection=a-8;e.index=uint32_t(result);e.args[2]=uint32_t(result);e.args[3]=copy_token;
  uint32_t n{};U data{};
  bool ok=sampled&&uint32_t(result)!=0xffffffff&&field(a,n)&&result<n&&field(a+8,data)&&region(e,data+result*0x30);
  if(!ok)e.status|=16;
  else if(before.count!=e.count||memcmp(before.region,e.region,0x15)||memcmp(before.points,e.points,e.count*16))e.status|=32;
  if(!stable(e))e.status|=8;emit(e);
 }return result;
}
inline void generate_hook(U a,U b,U c,uint32_t d,U definition,U out){
 if(!enabled){generate_original(a,b,c,d,definition,out);return;}
 ++active;Context local=pending;auto* previous=generating;generating=&local;
 struct Restore {Context* p;Context old;int exceptions=std::uncaught_exceptions();~Restore(){if(std::uncaught_exceptions()>exceptions){auto e=current(Loss);e.status|=64;emit(e);}generating=p;pending=old;--active;}} restore{previous,pending};
 if(!local.valid||local.e.source!=a)local.e.status|=2;
 generate_original(a,b,c,d,definition,out);
 Event e=local.e;e.kind=Completed;e.args[2]=d;e.args[3]=definition;
 if(e.owner!=d)e.status|=128;
 if(!owned(e))e.status|=4;if(!stable(e))e.status|=8;emit(e);
}
template<unsigned N> U fence_hook(U a,U b,U c,U d){
 if(!enabled)return fences[N](a,b,c,d);
 ++hazards;increment(epoch);++active;Event e{};e.kind=Fence;e.epoch=epoch;e.args[0]=N;e.args[1]=a;emit(e);
 struct End {~End(){increment(epoch);--hazards;--active;}} end;
 return fences[N](a,b,c,d);
}
}
