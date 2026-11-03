// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// D5AM 0.9.0 derivative only. Source-informed by the owned observer/lifetime
// queues and context patcher under SOR-P-0002. Historical inputs stay immutable.
#include "transport.h"
extern "C" {
extern std::atomic<uint64_t> D5AM_watched_lock;
extern std::atomic<uint64_t> D5AM_watched_state;
extern std::atomic<uint64_t> D5AM_generation,D5AM_registry_serial;
extern std::atomic<uint64_t> D5AM_recursive_release_site;
__declspec(selectany) uint64_t D5AM_causal_core_active=uint64_t(&winner::active),D5AM_causal_enabled=uint64_t(&winner::enabled);
__declspec(selectany) uint64_t D5AM_causal_fixture_before_operation{},D5AM_causal_fixture_before_admission{}; // Owned ABI host only; always zero in retail.
inline std::atomic<uint64_t> D5AM_causal_bridge_active{},D5AM_causal_counter_faults{};
void D5AM_pending();void D5AM_acquired();void D5AM_recursive();
void D5AM_reader();void D5AM_reader_release();void D5AM_writer_release();
void D5AM_recursive_release();
void D5AM_reader_ready();void D5AM_inline_writer_release();void D5AM_inline_recursive_release();
}
namespace winner::causal {
static_assert(sizeof(std::atomic<U>)==8&&std::atomic<U>::is_always_lock_free);
constexpr U capacity=32768;
constexpr unsigned site_count=16;
enum Kind:U {Register=1,Pending,Acquired,Recursive,Reader,ReaderRelease,WriterRelease,
 RecursiveRelease,Approach,HelperReturn,VisitedDone,ResetBegin,ResetEnd,Retire,ReaderReady};
struct Event {
 U sequence{},kind{},thread{},ticks{},lock{},generation{},invocation{},selection{},source{},
 epoch{},hazards{},old_state{},new_state{},status{},site{};
 int32_t request[2]{};
};
static_assert(sizeof(Event)==128);
struct Header {U magic=0x31434c4d41354453ULL,version=1,event_bytes=128,reserved{};char identity[64]{};};
static_assert(sizeof(Header)==96);
struct Cell {Event event{};std::atomic<U> ticket{};};
inline Cell queue[capacity];
inline std::atomic<U> enqueue{},dequeue{},active{},drops{},reentrant{},tokens{},baseline_unknown{},multiowner{},uncertain{};
inline std::atomic<bool> failed{},counter_overflow{};
inline std::atomic_flag registering=ATOMIC_FLAG_INIT;
inline thread_local bool recording{};
// Enabled only by the admitted disposable fixture. Zero handles in retail.
inline HANDLE fixture_entered{},fixture_resume{};
inline std::atomic<U> fixture_hold_thread{};
inline std::atomic<bool> fixture_hold_after_emit{};
inline Patch edits[site_count]{};
inline Four exclusive_original{};
inline HANDLE raw=INVALID_HANDLE_VALUE;
inline std::atomic<U> written{};
inline std::atomic<bool> fixture_drain_hold{},fixture_worker_held{};
inline bool configured{},begun{};
inline unsigned char* page{};
inline std::string relay_hash;
inline std::string original_hash[site_count];
inline unsigned char original_window[site_count][32]{};
inline U helper_locations[3]{};
inline unsigned helper_lengths[3]{126,216,81};
inline unsigned char helper_original[3][216]{};
inline std::string helper_hash[3];
inline U tick() noexcept {LARGE_INTEGER t{};QueryPerformanceCounter(&t);return U(t.QuadPart);}
inline bool bump(std::atomic<U>& value,U* result=nullptr) noexcept {
 U old=value.load();
 for(unsigned attempt=0;attempt<32;++attempt){
  if(old==UINT64_MAX){counter_overflow=true;failed=true;return false;}
  if(value.compare_exchange_weak(old,old+1)){if(result)*result=old+1;return true;}
 }failed=true;return false;
}
inline void lose() noexcept {bump(drops);failed=true;}
inline bool emit(Event e) noexcept {
 if(recording){bump(reentrant);lose();return false;}
 recording=true;struct Restore {~Restore(){recording=false;}} restore;
 e.thread=GetCurrentThreadId();e.ticks=tick();
 U n=enqueue.load();
 for(unsigned tries=0;tries<32;++tries){
  if(n>U(INT64_MAX)-capacity){lose();return false;}
  auto& c=queue[n%capacity];auto d=int64_t(c.ticket.load(std::memory_order_acquire))-int64_t(n);
  if(d<0){lose();return false;}if(d>0){n=enqueue.load();continue;}
  if(enqueue.compare_exchange_weak(n,n+1)){
   e.sequence=n+1;c.event=e;c.ticket.store(n+1,std::memory_order_release);return true;
  }
 }lose();return false;
}
inline bool pop(Event& e) noexcept {
 U n=dequeue.load();auto& c=queue[n%capacity];if(c.ticket.load(std::memory_order_acquire)!=n+1)return false;
 e=c.event;c.ticket.store(n+capacity,std::memory_order_release);dequeue=n+1;return true;
}
inline Event event(U kind,U lock) noexcept {
 auto context=winner::event(winner::Entry);Event e{};e.kind=kind;e.lock=lock;e.generation=D5AM_generation.load();
 e.invocation=context.invocation;e.selection=context.selection;e.source=context.source;
 e.epoch=winner::epoch.load();e.hazards=winner::hazards.load();
 memcpy(e.request,context.request,8);return e;
}
struct Producer {
 bool admitted{};
 Producer(){if(bump(active)){if(bump(winner::active))admitted=true;else --active;}}
 ~Producer(){if(admitted){if(!active.fetch_sub(1)||!winner::active.fetch_sub(1)){counter_overflow=true;failed=true;}}}
};
inline void capture(U lock,U old,U kind,U native_generation,U native_serial,U site,bool native_admitted=false,uint32_t native_delta=0,uint32_t native_owner=0) noexcept {
 PreserveError preserve;
 if(kind==Pending&&!fixture_hold_after_emit.load()&&fixture_hold_thread.load()==GetCurrentThreadId()&&fixture_entered&&fixture_resume){
  SetEvent(fixture_entered);WaitForSingleObject(fixture_resume,INFINITE);
 }
 Producer producer;if(!producer.admitted)return;
 if((!native_admitted&&!winner::enabled.load())||!begun)return;
 auto e=event(kind,lock);e.generation=native_generation;e.old_state=uint32_t(old);e.site=site;
 if(!native_generation||(native_serial&1)||D5AM_registry_serial.load()!=native_serial||D5AM_watched_lock.load()!=lock||D5AM_generation.load()!=native_generation){e.status|=8;bump(uncertain);}
 switch(kind){
  case Pending:e.new_state=uint32_t(old+0x1000);break;
  case Acquired:case Recursive:e.new_state=uint32_t(old+0x400000);break;
  case Reader:e.new_state=uint32_t(old+1);break;
  case ReaderRelease:e.new_state=uint32_t(old-1);break;
  case WriterRelease:e.new_state=uint32_t(old-0x401000);break;
  case RecursiveRelease:e.new_state=uint32_t(old-0x400000);break;
  case ReaderReady:break;
  default:e.status|=4;failed=true;
 }
 if(kind==WriterRelease||kind==RecursiveRelease){
  for(unsigned index=14;index<site_count;++index)if(site==U(edits[index].at)){
   uint32_t expected=kind==WriterRelease?0xffbff000u:0xffc00000u;
   e.new_state=uint32_t(old+native_delta);
   if(native_delta!=expected||native_owner!=(kind==WriterRelease?0:GetCurrentThreadId())){e.status|=4;failed=true;}
  }
 }
 emit(e);
 if(kind==Pending&&fixture_hold_after_emit.load()&&fixture_hold_thread.load()==GetCurrentThreadId()&&fixture_entered&&fixture_resume){
  SetEvent(fixture_entered);WaitForSingleObject(fixture_resume,INFINITE);
 }
}
inline void register_owner(U proc) noexcept {
 PreserveError preserve;Producer producer;
 if(!producer.admitted)return;
 if(!winner::enabled.load()||!begun)return;
 U lock=proc+0x40;
 if(D5AM_watched_lock.load()==lock)return;
 if(registering.test_and_set()){bump(baseline_unknown);return;}
 struct Registration {~Registration(){registering.clear();}} registration;
 U previous=D5AM_watched_lock.load();
 if(!previous){
  if(!bump(D5AM_registry_serial))return;
  U next{};if(!bump(tokens,&next))return;D5AM_generation=next;
  D5AM_watched_state=lock+4;D5AM_watched_lock=lock;
  auto e=event(Register,lock);uint32_t state{},owner{};
  // Publish the native gate before sampling initial state. A nonzero baseline
  // explicitly refuses complete earlier-holder history; no later pointer walk.
  if(!field(lock,owner)||!field(lock+4,state)){e.status|=2;bump(baseline_unknown);}
  e.old_state=state;e.new_state=owner;
  if(state||owner){e.status|=1;bump(baseline_unknown);}
  emit(e);
  bump(D5AM_registry_serial);
 }else if(previous!=lock){bump(multiowner);}
}
inline void lifecycle(U proc,U kind) noexcept {
 PreserveError preserve;Producer producer;if(!producer.admitted||!winner::enabled.load()||!begun)return;
 U lock=proc+0x40;
 if(D5AM_watched_lock.load()!=lock)return;
 if(kind==Retire&&!bump(D5AM_registry_serial))return;
 emit(event(kind,lock));
 if(kind==Retire){U expected=lock;D5AM_watched_lock.compare_exchange_strong(expected,0);D5AM_watched_state=0;bump(D5AM_registry_serial);}
}
inline U exclusive_hook(U a,U b,U c,U d){
 DWORD incoming=GetLastError();Producer producer;
 if(!producer.admitted)return exclusive_original(a,b,c,d);
 if(winner::enabled.load()&&begun&&D5AM_watched_lock.load()==a)emit(event(Approach,a));
 SetLastError(incoming);
 U result=exclusive_original(a,b,c,d);
 DWORD outgoing=GetLastError();
 if(winner::enabled.load()&&begun&&D5AM_watched_lock.load()==a)emit(event(HelperReturn,a));
 SetLastError(outgoing);
 return result;
}
inline void visited_done() noexcept {
 PreserveError preserve;Producer producer;
 if(!producer.admitted)return;
 if(winner::enabled.load()&&begun&&current&&D5AM_watched_lock.load()==current->e.proc+0x40)
  emit(event(VisitedDone,current->e.proc+0x40));
}
inline bool configure(const U* locations,const char* const* hashes,const char* const* helper_hashes){
 void* bridges[]{(void*)&D5AM_pending,(void*)&D5AM_acquired,(void*)&D5AM_recursive,
  (void*)&D5AM_reader,(void*)&D5AM_writer_release,(void*)&D5AM_recursive_release,
  (void*)&D5AM_reader_release,(void*)&D5AM_reader_release,(void*)&D5AM_reader_release,(void*)&exclusive_hook,(void*)&D5AM_reader_ready,
  (void*)&D5AM_reader_release,(void*)&D5AM_reader_release,(void*)&D5AM_reader_release,
  (void*)&D5AM_inline_writer_release,(void*)&D5AM_inline_recursive_release};
 const unsigned length[]{6,6,6,9,9,9,6,6,6,5,5,6,6,6,5,5};
 const char* expected[]{"\xf0\x41\x0f\xc1\x46\x04","\x41\x89\x2e\x0f\xae\xf0","\xf0\x41\x0f\xc1\x76\x04",
  "\xf0\x0f\xc1\x07\xa9\x00\x00\xc0\xff","\xf0\x0f\xc1\x01\xa9\xff\x0f\x00\x00","\xb8\x00\x00\xc0\xff\xf0\x0f\xc1\x01",
  "\xf0\x0f\xc1\x11\x8b\xc2","\xf0\x0f\xc1\x11\x8b\xc2","\xf0\x0f\xc1\x11\x8b\xc2",nullptr,"\x48\x8b\x5c\x24\x38",
  "\xf0\x0f\xc1\x11\x8b\xc2","\xf0\x0f\xc1\x11\x8b\xc2","\xf0\x0f\xc1\x11\x8b\xc2",
  "\xf0\x0f\xc1\x4f\x04","\xf0\x0f\xc1\x4f\x04"};
 page=near_page(locations[0]);if(!page)return false;
 helper_locations[0]=locations[3]-0x16;helper_locations[1]=locations[0]-0x40;helper_locations[2]=locations[4]-0x22;
 for(unsigned i=0;i<3;++i){
  if(!read(helper_locations[i],helper_original[i],helper_lengths[i])||sor::sha_bytes(helper_original[i],helper_lengths[i])!=helper_hashes[i])return false;
  helper_hash[i]=helper_hashes[i];
 }
 D5AM_recursive_release_site=locations[5];
 for(unsigned i=0;i<site_count;++i){
  auto& p=edits[i];p.at=(unsigned char*)locations[i];p.n=length[i];unsigned char bytes[32]{};
  if(!read(U(p.at),bytes,32)||sor::sha_bytes(bytes,32)!=hashes[i])return false;
  if(i!=9&&memcmp(bytes,expected[i],p.n))return false;
  if(i==9){if(bytes[0]!=0xe8)return false;int32_t d{};memcpy(&d,bytes+1,4);exclusive_original=(Four)(U(p.at)+5+d);}
  memcpy(p.before,bytes,p.n);memcpy(original_window[i],bytes,32);original_hash[i]=hashes[i];
  jump(page+i*32,U(bridges[i]));if(!relative(p,U(page+i*32),0xe8))return false;
 }
 DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;
 relay_hash=sor::sha_bytes(page,4096);configured=true;return true;
}
inline bool guards(){
 if(!configured)return true;if(sor::sha_bytes(page,4096)!=relay_hash)return false;
 for(unsigned i=0;i<site_count;++i){unsigned char expected[32]{},actual[32]{};auto& p=edits[i];memcpy(expected,original_window[i],32);
  auto overlay=[&](const Patch* patches,unsigned count){for(unsigned j=0;j<count;++j)for(unsigned k=0;k<patches[j].n;++k){U address=U(patches[j].at)+k;if(address>=U(p.at)&&address<U(p.at)+32)expected[address-U(p.at)]=patches[j].after[k];}};
  overlay(winner::edits,18);overlay(geometry::edits,3);overlay(context::edits,2);overlay(lifetime::edits,3);overlay(edits,site_count);
  if(!read(U(p.at),actual,32)||memcmp(expected,actual,32))return false;
 }
 for(unsigned i=0;i<3;++i){unsigned char expected[216]{},actual[216]{};memcpy(expected,helper_original[i],helper_lengths[i]);
  for(unsigned j=0;j<site_count;++j)for(unsigned k=0;k<edits[j].n;++k){U address=U(edits[j].at)+k;
   if(address>=helper_locations[i]&&address<helper_locations[i]+helper_lengths[i])expected[address-helper_locations[i]]=edits[j].after[k];
  }
  if(!read(helper_locations[i],actual,helper_lengths[i])||memcmp(expected,actual,helper_lengths[i]))return false;
 }return true;
}
inline std::string metadata(){
 std::string s=",\"causal_bridge_admission_schema\":\"sor-d5am-causal-bridge/1\",\"causal_schema\":\"sor-d5am-causal/1\",\"causal_sites\":[";
 for(unsigned i=0;i<site_count;++i){if(i)s+=",";s+="{\"va\":"+std::to_string(U(edits[i].at))+",\"bytes\":"+std::to_string(edits[i].n)+",\"guard_sha256\":"+sor::quote(original_hash[i])+"}";}
 s+="],\"causal_helpers\":[";
 for(unsigned i=0;i<3;++i){if(i)s+=",";s+="{\"va\":"+std::to_string(helper_locations[i])+",\"bytes\":"+std::to_string(helper_lengths[i])+",\"guard_sha256\":"+sor::quote(helper_hash[i])+"}";}
 return s+"]";
}
inline bool begin(bool fixture=false){
 if((!configured&&!fixture)||identity_hash.size()!=64)return false;
 for(U i=0;i<capacity;++i)queue[i].ticket=i;
 raw=CreateFileW((session/L"causal.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
 if(raw==INVALID_HANDLE_VALUE)return false;
 Header h{};memcpy(h.identity,identity_hash.data(),64);DWORD n{};
 if(!WriteFile(raw,&h,sizeof h,&n,nullptr)||n!=sizeof h||!FlushFileBuffers(raw))return false;
 begun=true;return true;
}
inline uint32_t crc(const void* data,size_t n){
 uint32_t v=0xffffffff;auto p=(const unsigned char*)data;
 for(size_t i=0;i<n;++i){v^=p[i];for(unsigned j=0;j<8;++j)v=(v>>1)^(0xedb88320u&uint32_t(-int(v&1)));}return ~v;
}
inline bool drain(){
 if(!begun)return true;
 if(fixture_drain_hold.load()){fixture_worker_held=true;return true;}
 U limit=enqueue.load();Event e{};
 if(!winner::disk((limit-dequeue.load())*136+65536))return false;
 while(dequeue.load()<limit){if(!pop(e))break;unsigned char packet[136]{};
  uint32_t size=128,digest=crc(&e,128);memcpy(packet,&size,4);memcpy(packet+4,&digest,4);memcpy(packet+8,&e,128);
  DWORD n{};if(written==UINT64_MAX){counter_overflow=true;failed=true;return false;}
  if(!WriteFile(raw,packet,sizeof packet,&n,nullptr)||n!=sizeof packet){failed=true;return false;}bump(written);
 }if(!FlushFileBuffers(raw)){failed=true;return false;}return true;
}
inline std::string metrics(){return ",\"causal_bridge_active\":"+std::to_string(D5AM_causal_bridge_active.load())+",\"causal_native_counter_faults\":"+std::to_string(D5AM_causal_counter_faults.load())+",\"causal_written\":"+std::to_string(written.load())+",\"causal_enqueued\":"+std::to_string(enqueue.load())+",\"causal_active\":"+std::to_string(active.load())+",\"causal_drops\":"+std::to_string(drops.load())+",\"causal_reentrant\":"+std::to_string(reentrant.load())+",\"causal_failed\":"+((failed||D5AM_causal_counter_faults.load())?"true":"false")+",\"causal_counter_overflow\":"+(counter_overflow?"true":"false")+",\"causal_baseline_unknown\":"+std::to_string(baseline_unknown.load())+",\"causal_multiowner\":"+std::to_string(multiowner.load())+",\"causal_uncertain\":"+std::to_string(uncertain.load());}
inline void close(){if(raw!=INVALID_HANDLE_VALUE){CloseHandle(raw);raw=INVALID_HANDLE_VALUE;}}
}
