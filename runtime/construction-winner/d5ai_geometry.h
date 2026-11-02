// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// D5AI sidecar candidate. Called only after the native point consumer acquires
// ProcGen's shared map lock. No borrowed address escapes into the worker.
#include "patch.h"
#include "d5ai_lifetime.h"
#include "../exp0002/win_support.h"
#include <limits>
extern "C" {extern uint64_t d5ai_acquire_original;void d5ai_area_acquire();void d5ai_area_complete();void d5ai_area_preunlock();}
namespace winner::geometry {
constexpr size_t slot_count=4, arena_bytes=2*1024*1024;
enum State:unsigned {Free,Capturing,Queued,Writing,AwaitConsumer};
enum Error:U {Okay,ReadFault,Malformed,ArenaFull,Interrupted,ExclusiveRecursion,ConsumerUnfinished,ConsumerPartial};
struct Header {
 U magic=0x3149413544524f53ULL,version=2,request{},snapshot{},proc{},epoch{},hazards{},loss{};
 U ticks_begin{},ticks_end{},status{},map_capacity{},holders{},resources{},regions{},points{},payload_bytes{},lock_owner{},lock_state{},thread{},boundary{},consumer{};
 unsigned char query[24]{};uint32_t radius_bits{},upper_bits{};
 U completion_ticks{},completion_epoch{},completion_hazards{},iterator{},scan_capacity{},scan_result{};
 U manager{},mode{},owner_formid{};unsigned char descriptor[44]{};uint32_t preunlock_seen{};
 lifetime::Mark life_begin{},life_end{};
};
struct Holder {U source{},holder{},capacity{},resources{};uint32_t opaque[2]{};};
struct Resource {uint32_t form{},reserved{};U collection{},regions{},region_capacity{},region_data{};};
struct Region {unsigned char header[24]{};U points{},point_capacity{},point_data{},region_address{};};
static_assert(sizeof(Header)==456 && sizeof(Holder)==40 && sizeof(Resource)==40 && sizeof(Region)==56);
struct Slot {std::atomic<unsigned> state{Free};Header header{};alignas(16) unsigned char payload[arena_bytes]{};};
inline Slot slots[slot_count];
inline std::atomic<U> armed{},serial{},offers{},captured{},overflow{},no_slot{},completed{},read_failures{},last_request{},active_capture{},busy_skips{};
inline std::atomic<bool> failed{},held{},fixture_receipt_fault{};
inline Four acquire_original{};
inline Patch edits[3]{};inline unsigned char* relay{};inline U guarded_target{};
inline std::string target_hash,relay_hash;
inline unsigned char* extra_relays[2]{};inline std::string extra_hashes[2];
inline bool configured{};
inline thread_local bool inside{};
inline thread_local Slot* pending{};
// Set only by the disposable test export; null during prospective retail use.
inline HANDLE fixture_entered{},fixture_resume{};
inline HANDLE fixture_admission_entered{},fixture_admission_resume{};
inline U fixture_manager{};
inline U tick() noexcept {LARGE_INTEGER t{};QueryPerformanceCounter(&t);return U(t.QuadPart);}
inline bool arm(U request) noexcept {
 if(!request||request<=last_request.load()||failed.load()||!enabled.load())return false;
 U empty=0;if(!armed.compare_exchange_strong(empty,request))return false;
 last_request=request;return true;
}
struct Writer {
 Slot& slot;size_t used{};
 bool append(const void* p,size_t n) noexcept {
  if(n>arena_bytes-used){slot.header.status=ArenaFull;return false;}
  memcpy(slot.payload+used,p,n);used+=n;return true;
 }
 bool copy(U p,size_t n) noexcept {
  if(n>arena_bytes-used){slot.header.status=ArenaFull;return false;}
  if(n&&!read(p,slot.payload+used,n)){slot.header.status=ReadFault;return false;}
  used+=n;return true;
 }
 template<class T> bool value(U p,T& v) noexcept {
  if(!field(p,v)){slot.header.status=ReadFault;return false;}return true;
 }
 bool invalid() noexcept {slot.header.status=Malformed;return false;}
};
// Every traversal budget follows from owned memory capacity. An exceeded budget
// creates an explicit invalid snapshot; it never silently truncates a population.
inline bool copy_population(U proc,Writer& w) noexcept {
 U data{},capacity{};
 if(!w.value(proc+0x20,data)||!w.value(proc+0x28,capacity))return false;
 w.slot.header.map_capacity=capacity;
 if(capacity>arena_bytes/24||(capacity&&data<0x10000))return w.invalid();
 for(U i=0;i<capacity;++i){
  unsigned char entry[24]{};if(!read(data+i*24,entry,24)){w.slot.header.status=ReadFault;return false;}
  uint32_t occupied{};memcpy(&occupied,entry+16,4);if(occupied==UINT32_MAX)continue;
  Holder h{};memcpy(&h.source,entry,8);memcpy(&h.holder,entry+8,8);
  if(!h.source||h.holder<0x10000)return w.invalid();
  if(!read(h.holder+8,h.opaque,8)){w.slot.header.status=ReadFault;return false;}
  U resource_data{};if(!w.value(h.holder+0x20,resource_data)||!w.value(h.holder+0x28,h.capacity))return false;
  if(h.capacity>arena_bytes/24||(h.capacity&&resource_data<0x10000))return w.invalid();
  const auto holder_at=w.used;if(!w.append(&h,sizeof h))return false;++w.slot.header.holders;
  for(U j=0;j<h.capacity;++j){
   unsigned char slot[24]{};if(!read(resource_data+j*24,slot,24)){w.slot.header.status=ReadFault;return false;}
   memcpy(&occupied,slot+16,4);if(occupied==UINT32_MAX)continue;
   Resource r{};memcpy(&r.form,slot,4);memcpy(&r.collection,slot+8,8);
   if(r.collection<0x10000)return w.invalid();
   uint32_t count{},cap{};U region_data{};
   if(!w.value(r.collection+8,count)||!w.value(r.collection+12,cap)||!w.value(r.collection+16,region_data))return false;
   if(count>cap||count>arena_bytes/sizeof(Region)||(count&&region_data<0x10000))return w.invalid();
   r.regions=count;r.region_capacity=cap;r.region_data=region_data;if(!w.append(&r,sizeof r))return false;++h.resources;++w.slot.header.resources;
   for(uint32_t k=0;k<count;++k){
    unsigned char native[48]{};if(!read(region_data+U(k)*48,native,48)){w.slot.header.status=ReadFault;return false;}
    Region region{};memcpy(region.header,native,24);uint32_t n{},point_capacity{};U points{};
    memcpy(&n,native+24,4);memcpy(&point_capacity,native+28,4);memcpy(&points,native+32,8);
    if(n>point_capacity||n>arena_bytes/16||(n&&points<0x10000))return w.invalid();
    region.points=n;region.point_capacity=point_capacity;region.point_data=points;region.region_address=region_data+U(k)*48;if(!w.append(&region,sizeof region)||!w.copy(points,size_t(n)*16))return false;
    ++w.slot.header.regions;w.slot.header.points+=n;
   }
  }
  memcpy(w.slot.payload+holder_at,&h,sizeof h);
 }
 return true;
}
inline void snapshot(U proc,U query=0,U consumer=0,uint32_t radius=0,uint32_t upper=0) noexcept {
 PreserveError preserve;
 if(!enabled.load()||inside||!armed.load())return;
 if(pending){++busy_skips;return;}
 if(fixture_admission_entered){SetEvent(fixture_admission_entered);WaitForSingleObject(fixture_admission_resume,INFINITE);}
 ++active_capture;struct ActiveEnd {~ActiveEnd(){--active_capture;}} active_end;
 // STOP may have passed the earlier fast-path check before this producer joined
 // the active handshake. Never reserve an arm or slot after admission closes.
 if(!enabled.load())return;
 U request=armed.exchange(0);if(!request)return;++offers;
 Slot* selected=nullptr;
 for(auto& s:slots){unsigned expected=Free;if(s.state.compare_exchange_strong(expected,Capturing)){selected=&s;break;}}
 if(!selected){++no_slot;failed=true;return;}
 inside=true;struct Exit {~Exit(){inside=false;}} exit;
 auto& s=*selected;s.header=Header{};auto& h=s.header;
 h.request=request;h.snapshot=++serial;h.proc=proc;h.epoch=epoch.load();h.hazards=hazards.load();h.loss=loss_generation.load();h.ticks_begin=tick();h.life_begin=lifetime::mark();
 h.boundary=query?2:1;h.consumer=consumer;h.radius_bits=radius;h.upper_bits=upper;
 h.thread=GetCurrentThreadId();uint32_t owner{},state{};Writer w{s};
 U manager=fixture_manager,attached{};uint32_t body{};unsigned char mode{};
 if((!manager&&(!base||!field(base+0x5fd9c30,manager)))||!manager||!field(manager+0x130,attached)||attached!=proc||
    !field(manager+0x20,mode)||!field(manager+0x80,body)||!read(manager+(mode==3?0x1c0:0xc8),h.descriptor,sizeof h.descriptor))h.status=ReadFault;
 h.manager=manager;h.mode=mode;h.owner_formid=body;
 if(query&&!read(query,h.query,sizeof h.query))h.status=ReadFault;
 else if(!h.status&&(!w.value(proc+0x40,owner)||!w.value(proc+0x44,state)))h.status=ReadFault;
 else if(!h.status){h.lock_owner=owner;h.lock_state=state;
  if((state&0xffc00000U)||owner==h.thread)h.status=ExclusiveRecursion;
  else {
   if(fixture_entered){SetEvent(fixture_entered);WaitForSingleObject(fixture_resume,INFINITE);}
   copy_population(proc,w);
  }
 }
 h.payload_bytes=w.used;h.ticks_end=tick();
 unsigned char after[44]{},after_mode{};U after_proc{};uint32_t after_owner{};
 if(!h.status&&(!field(manager+0x20,after_mode)||!field(manager+0x80,after_owner)||!field(manager+0x130,after_proc)||
   !read(manager+(mode==3?0x1c0:0xc8),after,sizeof after)||after_mode!=mode||after_owner!=body||after_proc!=proc||memcmp(after,h.descriptor,sizeof after)))h.status=Interrupted;
 if(h.epoch!=epoch.load()||h.hazards||hazards.load()||h.loss!=loss_generation.load())h.status=Interrupted;
 if(h.status==ArenaFull)++overflow;if(h.status==ReadFault)++read_failures;
 ++captured;pending=&s;s.state.store(AwaitConsumer,std::memory_order_release);
}
inline void complete(U iterator,U capacity,U result) noexcept {
 ++active_capture;struct End {~End(){--active_capture;}} end;
 if(!enabled.load()){pending=nullptr;return;}
 PreserveError preserve;auto* slot=pending;pending=nullptr;if(!slot)return;
 unsigned expected=AwaitConsumer;if(!slot->state.compare_exchange_strong(expected,Capturing,std::memory_order_acquire))return;
 auto& h=slot->header;h.completion_ticks=tick();h.completion_epoch=epoch.load();h.completion_hazards=hazards.load();
 h.life_end=lifetime::mark();
 h.iterator=iterator;h.scan_capacity=capacity;(void)result;
 if(!h.status&&(h.completion_epoch!=h.epoch||h.completion_hazards||h.loss!=loss_generation.load()))h.status=Interrupted;
 // Iterator equality alone is insufficient: false on the last callback can
 // still reach capacity. The earlier pre-unlock witness preserves real EDX.
 if(!h.status&&(iterator!=capacity||!h.preunlock_seen||h.scan_result!=1))h.status=ConsumerPartial;
 slot->state.store(Queued,std::memory_order_release);
}
inline void preunlock(U result) noexcept {
 ++active_capture;struct End {~End(){--active_capture;}} end;
 if(!enabled.load()||!pending||pending->state.load()!=AwaitConsumer)return;
 pending->header.scan_result=result;pending->header.preunlock_seen=1;
}
inline void finish_uncompleted() noexcept {
 for(auto& s:slots){unsigned expected=AwaitConsumer;if(s.state.compare_exchange_strong(expected,Capturing,std::memory_order_acquire)){
   s.header.status=ConsumerUnfinished;s.state.store(Queued,std::memory_order_release);
 }}
}
// This call-site wrapper returns only after original acquire has succeeded.
// Its native caller performs the unchanged reader release after traversal.
inline U acquire_hook(U lock,U b,U c,U d) {
 U result=acquire_original(lock,b,c,d);if(enabled.load())snapshot(lock-0x40);return result;
}
inline bool configure_acquire(void* call,const std::string& call_hash,const std::string& expected_target,bool area=true) {
 unsigned char window[32]{};if(!read(U(call),window,32)||sor::sha_bytes(window,32)!=call_hash||window[0]!=0xe8)return false;
 int32_t displacement{};memcpy(&displacement,window+1,4);guarded_target=U(call)+5+displacement;
 unsigned char target[32]{};if(!read(guarded_target,target,32)||sor::sha_bytes(target,32)!=expected_target)return false;
 auto& edit=edits[0];edit.at=(unsigned char*)call;edit.n=5;memcpy(edit.before,window,5);relay=near_page(U(call));if(!relay)return false;
 jump(relay,area?U(&d5ai_area_acquire):U(&acquire_hook));if(!relative(edit,U(relay),0xe8))return false;
 DWORD old{};if(!VirtualProtect(relay,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),relay,4096))return false;
 target_hash=expected_target;relay_hash=sor::sha_bytes(relay,4096);acquire_original=(Four)guarded_target;d5ai_acquire_original=guarded_target;configured=true;return true;
}
inline bool configure_completion(void* at,const std::string& expected){
 unsigned char b[32]{};if(!read(U(at),b,32)||sor::sha_bytes(b,32)!=expected||memcmp(b,"\x48\x8b\x7c\x24\x70",5))return false;
 auto& p=edits[1];p.at=(unsigned char*)at;p.n=5;memcpy(p.before,b,5);
 auto* page=near_page(U(at));if(!page)return false;jump(page,U(&d5ai_area_complete));if(!relative(p,U(page),0xe8))return false;
 DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;
 extra_relays[0]=page;extra_hashes[0]=sor::sha_bytes(page,4096);return true;
}
inline bool configure_preunlock(void* at,const std::string& expected){
 unsigned char b[32]{};if(!read(U(at),b,32)||sor::sha_bytes(b,32)!=expected||memcmp(b,"\x48\x8d\x4b\x04\xba\xff\xff\xff\xff",9))return false;
 auto& p=edits[2];p.at=(unsigned char*)at;p.n=9;memcpy(p.before,b,9);
 auto* page=near_page(U(at));if(!page)return false;jump(page,U(&d5ai_area_preunlock));if(!relative(p,U(page),0xe8))return false;
 DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;
 extra_relays[1]=page;extra_hashes[1]=sor::sha_bytes(page,4096);return true;
}
inline bool guards(){
 if(!configured)return true;
 for(unsigned i=0;i<2;++i)if(extra_relays[i]&&sor::sha_bytes(extra_relays[i],4096)!=extra_hashes[i])return false;
 unsigned char original[32]{};return match(edits[0],true)&&(!edits[1].at||match(edits[1],true))&&(!edits[2].at||match(edits[2],true))&&read(guarded_target,original,32)&&sor::sha_bytes(original,32)==target_hash&&sor::sha_bytes(relay,4096)==relay_hash;
}
bool drain_sidecar();bool poll_request();std::string metrics();
inline std::string identity_metadata(){
 std::string s=",\"geometry_schema\":\"sor-d5ai-raw/2\",\"geometry_header_bytes\":"+std::to_string(sizeof(Header))+",\"geometry_sites\":[";
 if(configured){for(unsigned i=0;i<3;++i){if(i)s+=",";s+="{\"va\":"+std::to_string(U(edits[i].at))+",\"bytes\":"+std::to_string(edits[i].n)+",\"preimage_sha256\":"+sor::quote(sor::sha_bytes(edits[i].before,edits[i].n))+"}";}}
 return s+"]";
}
}
