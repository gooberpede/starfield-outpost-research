// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Offline D5AM derivative. Owned observer/transport methods reused under SOR-P-0002.
// All target bytes are copied by the producer. The worker writes owned events only.
#include "transport.h"
#include <intrin.h>
namespace winner::scheduler {
constexpr U capacity=32768,registry_capacity=32768,probe_limit=64;
enum Kind:U {Published=1,Activated,Dispatch,Retire,ReadyTreeBefore,DependencyDecrement,
 CallbackBegin,CallbackEnd,Provider,ClaimReturn,QueueBefore,QueueReturn};
enum Status:U {ReadFault=1,NoBirth=2,IdentityChanged=4,RegistryBusy=8,DuplicateBirth=16,
 RegistryFull=32,Exceptional=64,NoTask=128,CounterOverflow=256};
struct Event {
 U sequence{},kind{},thread{},ticks{},node{},allocation{},family{},server{},rank{},serial{},
 dependencies{},registered{},state_flags{},pool{},mode{},status{},core_invocation{},core_selection{},
 source{},claim_context{},route{},epoch{},hazards{},extra{};
 int32_t request[2]{};uint32_t native_key[3]{},discriminator[3]{};U queue[6]{};
};
static_assert(sizeof(Event)==272);
struct RegistryCell {
 std::atomic<U> node{},serial{},allocation{},key_low{},key_high{},live{},vtable{},server{};
};
static_assert(sizeof(RegistryCell)==64&&offsetof(RegistryCell,serial)==8&&offsetof(RegistryCell,allocation)==16);
struct Cookie {U key_low{},key_high{},vtable{},allocation{},serial{},slot=UINT64_MAX;};
static_assert(sizeof(Cookie)==48);
}
extern "C" {
inline winner::scheduler::RegistryCell D5AM_sched_registry[32768];
inline uint64_t D5AM_sched_vtables[3]{},D5AM_sched_falls[3]{};
inline uint64_t D5AM_sched_callback_target{};
__declspec(selectany) uint64_t D5AM_sched_core_active=uint64_t(&winner::active),D5AM_sched_enabled=uint64_t(&winner::enabled);
inline std::atomic<uint64_t> D5AM_sched_bridge_active{};
inline std::atomic<uint64_t> D5AM_sched_counter_faults{};
__declspec(selectany) uint64_t D5AM_sched_fixture_admission{};
void D5AM_sched_activated();void D5AM_sched_dispatch();void D5AM_sched_retire();
void D5AM_sched_ready();void D5AM_sched_dependency();
uint64_t D5AM_sched_claim_entry(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t D5AM_sched_queue_entry(uint64_t,uint64_t,uint64_t,uint64_t);
__declspec(dllexport) uint64_t D5AM_sched_claim_proxy(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
__declspec(dllexport) uint64_t D5AM_sched_queue_proxy(uint64_t,uint64_t,uint64_t,uint64_t);
__declspec(dllexport) void D5AM_sched_capture_admitted(uint64_t,uint64_t,uint64_t,const winner::scheduler::Cookie*) noexcept;
__declspec(dllexport) void D5AM_sched_dispatch_admitted(uint64_t,uint64_t,const winner::scheduler::Cookie*,uint64_t) noexcept;
__declspec(dllexport) void D5AM_sched_ready_admitted(uint64_t,uint64_t,const winner::scheduler::Cookie*,uint64_t) noexcept;
bool D5AM_sched_command(uint64_t,uint64_t,uint64_t,uint64_t,winner::scheduler::Event*) noexcept;
__declspec(dllexport) bool D5AM_sched_command_capture(uint64_t,uint64_t,uint64_t,uint64_t,winner::scheduler::Event*) noexcept;
}
namespace winner::scheduler {
struct Cell {Event event{};std::atomic<U> ticket{};};
inline Cell queue[capacity];
inline std::atomic<U> enqueue{},dequeue{},active{},drops{},reentrant{},tokens{},registry_faults{},identity_faults{};
inline std::atomic<bool> failed{};
inline thread_local bool recording{};
inline bool begun{},configured{};
inline HANDLE raw=INVALID_HANDLE_VALUE;
inline U written{},callback_target{},vtable_image_base{};
inline Patch edits[13]{};
inline unsigned char* pages[13]{};
inline std::string page_hash[13],original_hash[13],target_hash[6],vtable_hash[3],callback_hash;
inline U guarded_targets[6]{};
inline unsigned char original_window[13][32]{};
inline Four registration_original[4]{},density_original{},layer_original{},queue_original{};
using Claim=U(*)(U,U,U,U,U);
inline Claim claim_original{};
// Task scope is per native thread, including nested inline work.
inline thread_local Event* task_scope{};
inline thread_local const Cookie* scope_cookie{};
inline U tick() noexcept {LARGE_INTEGER t{};QueryPerformanceCounter(&t);return U(t.QuadPart);}
inline bool next(std::atomic<U>& counter,U& result) noexcept {
 U value=counter.load();for(unsigned attempt=0;attempt<32;++attempt){
  if(value==UINT64_MAX){D5AM_sched_counter_faults.fetch_or(1);failed=true;counter_overflow=true;return false;}
  if(counter.compare_exchange_weak(value,value+1)){result=value+1;return true;}
 }D5AM_sched_counter_faults.fetch_or(2);failed=true;return false;
}
inline void increment(std::atomic<U>& counter) noexcept {U result{};next(counter,result);}
inline void admission_probe(U phase) noexcept {
 if(D5AM_sched_fixture_admission)reinterpret_cast<void(*)(U) noexcept>(D5AM_sched_fixture_admission)(phase);
}
struct Producer {bool core{},own{},admitted{};explicit Producer(bool inherited=false){
 admission_probe(0);U result{};core=next(winner::active,result);if(!core)return;
 own=next(active,result);if(!own)return;
 admitted=begun&&(inherited||winner::enabled.load());if(admitted)admission_probe(1);
 }
 ~Producer(){if(own)--active;if(core)--winner::active;}};
inline void lose() noexcept {increment(drops);failed=true;}
inline bool emit(Event e) noexcept {
 PreserveError preserve;
 if(recording){increment(reentrant);lose();return false;}
 recording=true;struct Reset{~Reset(){recording=false;}} reset;
 e.thread=GetCurrentThreadId();e.ticks=tick();U n=enqueue.load();
 for(unsigned tries=0;tries<32;++tries){
  if(n>U(INT64_MAX)-capacity){lose();return false;}
  auto& cell=queue[n%capacity];auto d=int64_t(cell.ticket.load(std::memory_order_acquire))-int64_t(n);
  if(d<0){lose();return false;}if(d>0){n=enqueue.load();continue;}
  if(enqueue.compare_exchange_weak(n,n+1)){e.sequence=n+1;cell.event=e;cell.ticket.store(n+1,std::memory_order_release);return true;}
 }lose();return false;
}
inline bool pop(Event& e) noexcept {
 U n=dequeue.load();auto& cell=queue[n%capacity];if(cell.ticket.load(std::memory_order_acquire)!=n+1)return false;
 e=cell.event;cell.ticket.store(n+capacity,std::memory_order_release);dequeue=n+1;return true;
}
inline U family(U vtable) noexcept {
 for(unsigned i=0;i<3;++i)if(vtable&&vtable==D5AM_sched_vtables[i])return i==2?2:1;
 return 0;
}
inline Cookie cookie(U node) noexcept {
 Cookie c{};uint32_t high{};
 if(!field(node,c.vtable)||!family(c.vtable)||!field(node+8,c.key_low)||!field(node+16,high))return c;
 c.key_high=high;U first=(node>>4)&(registry_capacity-1);
 for(U offset=0;offset<probe_limit;++offset){U index=(first+offset)&(registry_capacity-1);auto& slot=D5AM_sched_registry[index];
  U stored=slot.node.load(std::memory_order_acquire);if(!stored)return c;
  if(stored==node){c.serial=slot.serial.load(std::memory_order_acquire);c.allocation=slot.allocation.load();c.slot=index;return c;}
 }return c;
}
inline U identity(U node,const Cookie& c,Event& e,bool publish=false,bool retire=false) noexcept {
 if(publish){
  U first=(node>>4)&(registry_capacity-1);
  for(U offset=0;offset<probe_limit;++offset){U index=(first+offset)&(registry_capacity-1);auto& slot=D5AM_sched_registry[index];
   U stored=slot.node.load();if(!stored){U empty=0;if(!slot.node.compare_exchange_strong(empty,node))stored=empty;else stored=node;}
   if(stored!=node)continue;
   U serial=slot.serial.load();if(serial>UINT64_MAX-2){e.status|=CounterOverflow;D5AM_sched_counter_faults.fetch_or(1);failed=true;counter_overflow=true;increment(registry_faults);return 0;}
   if((serial&1)||!slot.serial.compare_exchange_strong(serial,serial+1)){
    e.status|=RegistryBusy;increment(registry_faults);return 0;
   }
   if(slot.live.load()){
    e.status|=DuplicateBirth;slot.live=0;slot.serial=serial+2;increment(identity_faults);return 0;
   }
   U id{};if(!next(tokens,id)){e.status|=CounterOverflow;failed=true;}
   slot.key_low=c.key_low;slot.key_high=c.key_high;slot.allocation=id;slot.vtable=c.vtable;slot.server=e.server;slot.live=bool(id);
   slot.serial.store(serial+2,std::memory_order_release);return id;
  }e.status|=RegistryFull;increment(registry_faults);return 0;
 }
 if(c.slot>=registry_capacity||!c.allocation){e.status|=NoBirth;increment(identity_faults);return 0;}
 auto& slot=D5AM_sched_registry[c.slot];U serial=slot.serial.load(std::memory_order_acquire);
 if((c.serial&1)||serial!=c.serial||slot.node.load()!=node||slot.allocation.load()!=c.allocation||
    slot.key_low.load()!=c.key_low||slot.key_high.load()!=c.key_high||slot.vtable.load()!=c.vtable||!slot.live.load()){
  e.status|=IdentityChanged;increment(identity_faults);return 0;
 }
 if(!e.server)e.server=slot.server.load();
 if(retire){
  if(serial>UINT64_MAX-2){e.status|=CounterOverflow;D5AM_sched_counter_faults.fetch_or(1);failed=true;counter_overflow=true;increment(registry_faults);return 0;}
  if(!slot.serial.compare_exchange_strong(serial,serial+1)){e.status|=RegistryBusy;increment(registry_faults);return 0;}
  slot.live=0;slot.serial.store(serial+2,std::memory_order_release);
 }else if(slot.serial.load(std::memory_order_acquire)!=serial){e.status|=IdentityChanged;increment(identity_faults);return 0;}
 return c.allocation;
}
inline bool snapshot(U node,U kind,U server,const Cookie& consumed,Event& e) noexcept {
 e.kind=kind;e.node=node;e.server=server;e.epoch=winner::epoch;e.hazards=winner::hazards;
 U vtable{};uint32_t rank{},dependencies{},state{};uint16_t registered{};uint8_t mode{};
 if(!field(node,vtable))return false;e.family=family(vtable);if(!e.family)return false;
 if(!read(node+8,e.native_key,12)||!read(node+0xb0,e.request,8)||!read(node+0xb8,e.discriminator,12)||
    !field(node+0x80,rank)||!field(node+0x88,e.serial)||!field(node+0x90,dependencies)||
    !field(node+0x94,registered)||!field(node+0x98,e.pool)||!field(node+0xa0,mode)||!field(node+0xa8,state))e.status|=ReadFault;
 e.rank=rank;e.dependencies=dependencies;e.registered=registered;e.mode=mode;e.state_flags=state;
 U low{};memcpy(&low,e.native_key,8);
 if(consumed.vtable!=vtable||consumed.key_low!=low||consumed.key_high!=e.native_key[2]){e.status|=IdentityChanged;increment(identity_faults);}
 e.allocation=identity(node,consumed,e,kind==Published,kind==Retire);
 return true;
}
inline void capture(U node,U kind,U server,const Cookie* consumed,bool native_admitted=false,U native_operand=0) noexcept {
 PreserveError preserve;Producer producer(native_admitted);if(!producer.admitted)return;
 Event e{};Cookie c=consumed?*consumed:cookie(node);
 if(snapshot(node,kind,server,c,e)){
  if(kind==Dispatch)e.extra=native_operand&255;else if(kind==ReadyTreeBefore)e.extra=native_operand;
  emit(e);}
}
template<unsigned N> inline U registration(U a,U b,U node,U d){
 if(!winner::enabled.load()||!begun)return registration_original[N](a,b,node,d);
 Producer producer;if(!producer.admitted)return registration_original[N](a,b,node,d);Cookie c=cookie(node);Event e{};
 if(snapshot(node,Published,a,c,e)){e.extra=N;emit(e);}
 return registration_original[N](a,b,node,d);
}
template<unsigned N> inline U callback(U a,U b,U c,U d){
 auto original=N==0?density_original:layer_original;
 if(!winner::enabled.load()||!begun)return original(a,b,c,d);
 Producer producer;if(!producer.admitted)return original(a,b,c,d);U node=a>=0xb0?a-0xb0:0;Cookie consumed=cookie(node);Event e{};
 bool observed=snapshot(node,CallbackBegin,0,consumed,e);
 auto* previous=task_scope;auto* previous_cookie=scope_cookie;if(observed){emit(e);task_scope=&e;scope_cookie=&consumed;}
 struct Restore {Event* prior;const Cookie* prior_cookie;Event captured;bool observed;int exceptions=std::uncaught_exceptions();
  ~Restore(){if(observed){captured.kind=CallbackEnd;if(std::uncaught_exceptions()>exceptions)captured.status|=Exceptional;emit(captured);}task_scope=prior;scope_cookie=prior_cookie;}
 } restore{previous,previous_cookie,e,observed};
 return original(a,b,c,d);
}
inline void provider() noexcept {
 PreserveError preserve;Producer producer;if(!producer.admitted)return;
 Event e=task_scope?*task_scope:Event{};e.kind=Provider;if(!task_scope)e.status|=NoTask;
 if(task_scope&&scope_cookie)e.allocation=identity(e.node,*scope_cookie,e);
 if(winner::current){auto& core=winner::current->e;e.core_invocation=core.invocation;e.core_selection=core.selection;e.source=core.source;
  if(task_scope&&memcmp(core.request,e.request,8))e.status|=IdentityChanged;
 }else e.status|=NoTask;
 emit(e);
}
inline bool command_event(U context,U address,U kind,U route,Event& e) noexcept {
 U tagged{},function{},node{},server{};if(!field(address,tagged)||!tagged)return false;U command=tagged&~U(1);
 if(!field(command+8,function)||function!=callback_target)return false;
 if(!field(command+0x10,node)||!field(command+0x18,server))return false;
 Cookie c=cookie(node);if(!snapshot(node,kind,server,c,e))return false;
 e.claim_context=context;e.route=route;e.extra=tagged;
 const U offsets[]{0,0x40,0x80,0x88,0x90,0x98};
 for(unsigned i=0;i<6;++i)if(!field(context+offsets[i],e.queue[i]))e.status|=ReadFault;
 return true;
}
inline U claim(U a,U b,U c,U d,U fifth){
 Producer producer;
 auto result=claim_original(a,b,c,d,fifth);PreserveError preserve;
 if(producer.admitted){Event e{};if(D5AM_sched_command(c,result,ClaimReturn,(d&255)|((fifth&255)<<8),&e)){e.pool=a;emit(e);}}
 return result;
}
inline U publish_queue(U a,U b,U c,U d){
 if(!winner::enabled.load()||!begun)return queue_original(a,b,c,d);
 Producer producer;if(!producer.admitted)return queue_original(a,b,c,d);Event e{};bool observed=D5AM_sched_command(a,b,QueueBefore,0,&e);if(observed)emit(e);
 auto result=queue_original(a,b,c,d);if(observed){e.kind=QueueReturn;emit(e);}return result;
}
inline uint32_t crc(const void* data,size_t n) noexcept {
 uint32_t value=0xffffffff;auto bytes=(const unsigned char*)data;
 for(size_t i=0;i<n;++i){value^=bytes[i];for(unsigned j=0;j<8;++j)value=(value>>1)^(0xedb88320u&uint32_t(-int(value&1)));}return ~value;
}
inline bool begin(bool fixture=false){
 if((!configured&&!fixture)||identity_hash.size()!=64)return false;
 for(U i=0;i<capacity;++i)queue[i].ticket=i;
 raw=CreateFileW((session/L"scheduler.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
 if(raw==INVALID_HANDLE_VALUE)return false;
 struct Header {U magic=0x314843534d413544ULL,version=1,event_bytes=sizeof(Event),reserved{};char identity[64]{};} header;
 static_assert(sizeof(Header)==96);memcpy(header.identity,identity_hash.data(),64);DWORD count{};
 if(!WriteFile(raw,&header,sizeof header,&count,nullptr)||count!=sizeof header||!FlushFileBuffers(raw))return false;
 begun=true;return true;
}
inline bool advance_written() noexcept {
 if(written==UINT64_MAX){D5AM_sched_counter_faults.fetch_or(1);counter_overflow=true;failed=true;return false;}++written;return true;
}
inline bool drain(){
 if(!begun)return true;U limit=enqueue.load();if(!winner::disk((limit-dequeue.load())*(sizeof(Event)+8)+65536))return false;
 Event e{};while(dequeue.load()<limit){if(!pop(e))break;unsigned char packet[sizeof(Event)+8]{};
  uint32_t size=sizeof(Event),digest=crc(&e,sizeof e);memcpy(packet,&size,4);memcpy(packet+4,&digest,4);memcpy(packet+8,&e,sizeof e);DWORD count{};
  if(!WriteFile(raw,packet,sizeof packet,&count,nullptr)||count!=sizeof packet){failed=true;return false;}
  if(!advance_written())return false;
 }if(!FlushFileBuffers(raw)){failed=true;return false;}return true;
}
inline std::string metrics(){return ",\"scheduler_written\":"+std::to_string(written)+",\"scheduler_enqueued\":"+std::to_string(enqueue.load())+
 ",\"scheduler_active\":"+std::to_string(active.load())+",\"scheduler_drops\":"+std::to_string(drops.load())+",\"scheduler_reentrant\":"+std::to_string(reentrant.load())+
 ",\"scheduler_bridge_active\":"+std::to_string(D5AM_sched_bridge_active.load())+
 ",\"scheduler_counter_overflow\":"+((D5AM_sched_counter_faults.load()&1)?"true":"false")+
 ",\"scheduler_counter_contention\":"+((D5AM_sched_counter_faults.load()&2)?"true":"false")+
 ",\"scheduler_registry_faults\":"+std::to_string(registry_faults.load())+",\"scheduler_identity_faults\":"+std::to_string(identity_faults.load())+
 ",\"scheduler_failed\":"+((failed||D5AM_sched_counter_faults.load())?"true":"false");}
inline void close(){if(raw!=INVALID_HANDLE_VALUE){CloseHandle(raw);raw=INVALID_HANDLE_VALUE;}}
inline bool avx_ready(){int cpu[4]{};__cpuid(cpu,1);return (cpu[2]&(1<<27))&&(cpu[2]&(1<<28))&&(_xgetbv(0)&6)==6;}
// All four qwords in each of the three pinned VT windows are exact PE DIR64
// relocation slots. Canonicalize only those proven image-pointer fields; never
// learn a replacement baseline from runtime bytes. The static SHA remains the
// independently pinned PE preimage. Other guarded code windows have no DIR64.
inline std::string vtable_digest(U address,U image_base){
 if(image_base<0x10000||image_base>0x7ffeffffffffULL)return {};
 U words[4]{};if(!read(address,words,sizeof words))return {};
 for(auto& word:words){if(word<image_base||word-image_base>=0x100000000ULL)return {};
  word=word-image_base+0x140000000ULL;}
 return sor::sha_bytes(words,sizeof words);
}
inline bool target_guard(U address,const char* expected){
 unsigned char bytes[32]{};return expected&&read(address,bytes,32)&&sor::sha_bytes(bytes,32)==expected;
}
inline bool configure(const U* locations,const char* const* hashes,const U* vtables,const char* const* vtable_hashes,
 U command_callback,const char* command_hash,const char* const* expected_target_hashes){
 if(!avx_ready())return false;
 if(locations[0]<0x76cea4)return false;vtable_image_base=locations[0]-0x76cea4;
 for(unsigned i=0;i<3;++i){
  if(vtable_digest(vtables[i],vtable_image_base)!=vtable_hashes[i])return false;
  D5AM_sched_vtables[i]=vtables[i];vtable_hash[i]=vtable_hashes[i];
 }
 unsigned char command[32]{};if(!read(command_callback,command,32)||sor::sha_bytes(command,32)!=command_hash)return false;
 callback_target=command_callback;D5AM_sched_callback_target=command_callback;callback_hash=command_hash;
 void* hooks[]{(void*)&registration<0>,(void*)&registration<1>,(void*)&registration<2>,(void*)&registration<3>,
  (void*)&D5AM_sched_activated,(void*)&D5AM_sched_dispatch,(void*)&D5AM_sched_retire,(void*)&D5AM_sched_ready,
  (void*)&D5AM_sched_dependency,(void*)&callback<0>,(void*)&callback<1>,(void*)&D5AM_sched_claim_entry,(void*)&D5AM_sched_queue_entry};
 const unsigned lengths[]{5,5,5,5,5,5,5,8,7,5,5,5,5};
 const char* expected[]{nullptr,nullptr,nullptr,nullptr,"\x48\x89\x5c\x24\x08","\x48\x89\x5c\x24\x10",
  "\x48\x89\x5c\x24\x08","\x4c\x8b\x49\x50\x49\x89\x53\x08","\x83\x80\x90\x00\x00\x00\xff",
  nullptr,nullptr,"\x48\x89\x5c\x24\x20","\x48\x89\x5c\x24\x18"};
 unsigned target=0;
 for(unsigned i=0;i<13;++i){auto& p=edits[i];p.at=(unsigned char*)locations[i];p.n=lengths[i];unsigned char bytes[32]{};
  if(!read(U(p.at),bytes,32)||sor::sha_bytes(bytes,32)!=hashes[i])return false;
  if(expected[i]&&memcmp(bytes,expected[i],p.n))return false;
  memcpy(p.before,bytes,p.n);memcpy(original_window[i],bytes,32);original_hash[i]=hashes[i];
  auto* page=near_page(U(p.at));if(!page)return false;pages[i]=page;jump(page,U(hooks[i]));
  bool call=i<4||i==7||i==8||i==9||i==10;
  if(!relative(p,U(page),call?0xe8:0xe9))return false;
  if(i<4||i==9||i==10){
   if(bytes[0]!=0xe8)return false;int32_t displacement{};memcpy(&displacement,bytes+1,4);U destination=U(p.at)+5+displacement;
   if(!target_guard(destination,expected_target_hashes[target]))return false;
   guarded_targets[target]=destination;target_hash[target]=expected_target_hashes[target];++target;
   if(i<4)registration_original[i]=(Four)destination;else if(i==9)density_original=(Four)destination;else layer_original=(Four)destination;
  }else if(i==11||i==12){auto* trampoline=page+32;memcpy(trampoline,bytes,5);jump(trampoline+5,U(p.at)+5);
   if(i==11)claim_original=(Claim)trampoline;else queue_original=(Four)trampoline;
  }else if(i>=4&&i<=6)D5AM_sched_falls[i-4]=U(p.at)+5;
  DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;
  page_hash[i]=sor::sha_bytes(page,4096);
 }
 configured=true;return true;
}
inline bool guards(){
 if(D5AM_sched_counter_faults.load())return false;if(!configured)return true;
 for(unsigned i=0;i<13;++i){unsigned char expected[32]{},actual[32]{};memcpy(expected,original_window[i],32);
  for(unsigned j=0;j<13;++j)for(unsigned k=0;k<edits[j].n;++k){U address=U(edits[j].at)+k;
   if(address>=U(edits[i].at)&&address<U(edits[i].at)+32)expected[address-U(edits[i].at)]=edits[j].after[k];
  }
  if(!read(U(edits[i].at),actual,32)||memcmp(expected,actual,32)||sor::sha_bytes(pages[i],4096)!=page_hash[i])return false;
 }
 for(unsigned i=0;i<6;++i)if(!target_guard(guarded_targets[i],target_hash[i].c_str()))return false;
 for(unsigned i=0;i<3;++i)if(vtable_digest(D5AM_sched_vtables[i],vtable_image_base)!=vtable_hash[i])return false;
 unsigned char command[32]{};return read(callback_target,command,32)&&sor::sha_bytes(command,32)==callback_hash;
}
inline std::string metadata(){
 std::string s=",\"scheduler_schema\":\"sor-d5am-scheduler/1\",\"scheduler_bridge_admission_schema\":\"sor-d5am-scheduler-bridge/1\",\"scheduler_dispatch_argument_schema\":\"r8-low-byte/1\",\"scheduler_ready_serial_schema\":\"consumed-r9/1\",\"scheduler_event_bytes\":272,\"scheduler_vtable_guard_basis\":"+sor::quote(configured?"preferred-image-vtable64/1":"unconfigured-fixture/1")+",\"scheduler_sites\":[";
 for(unsigned i=0;i<13;++i){if(i)s+=",";s+="{\"va\":"+std::to_string(U(edits[i].at))+",\"bytes\":"+std::to_string(edits[i].n)+",\"guard_sha256\":"+sor::quote(original_hash[i])+"}";}
 s+="],\"scheduler_targets\":[";const unsigned indices[]{0,1,2,3,9,10};
 for(unsigned i=0;i<6;++i){if(i)s+=",";s+="{\"site_index\":"+std::to_string(indices[i])+",\"va\":"+std::to_string(guarded_targets[i])+",\"guard_sha256\":"+sor::quote(target_hash[i])+"}";}
 s+="],\"scheduler_vtables\":[";for(unsigned i=0;i<3;++i){if(i)s+=",";s+="{\"va\":"+std::to_string(D5AM_sched_vtables[i])+",\"guard_sha256\":"+sor::quote(vtable_hash[i])+"}";}
 return s+"],\"scheduler_callback\":{\"va\":"+std::to_string(callback_target)+",\"guard_sha256\":"+sor::quote(callback_hash)+"}";
}
}
#ifndef SOR_SCHED_EXTERNAL_CAPTURE
extern "C" __declspec(dllexport) inline void D5AM_sched_capture_admitted(uint64_t node,uint64_t kind,uint64_t server,
 const winner::scheduler::Cookie* cookie) noexcept {winner::scheduler::capture(node,kind,server,cookie,true);}
extern "C" __declspec(dllexport) inline void D5AM_sched_dispatch_admitted(uint64_t node,uint64_t server,
 const winner::scheduler::Cookie* cookie,uint64_t argument) noexcept {winner::scheduler::capture(node,winner::scheduler::Dispatch,server,cookie,true,argument);}
extern "C" __declspec(dllexport) inline void D5AM_sched_ready_admitted(uint64_t node,uint64_t server,
 const winner::scheduler::Cookie* cookie,uint64_t serial) noexcept {winner::scheduler::capture(node,winner::scheduler::ReadyTreeBefore,server,cookie,true,serial);}
extern "C" __declspec(dllexport) inline bool D5AM_sched_command_capture(uint64_t context,uint64_t address,uint64_t kind,
 uint64_t route,winner::scheduler::Event* out) noexcept {
 winner::PreserveError preserve;
 return out&&winner::scheduler::command_event(context,address,kind,route,*out);
}
#endif
extern "C" __declspec(dllexport) inline uint64_t D5AM_sched_claim_proxy(uint64_t a,uint64_t b,uint64_t c,uint64_t d,uint64_t fifth){
 return winner::scheduler::claim(a,b,c,d,fifth);
}
extern "C" __declspec(dllexport) inline uint64_t D5AM_sched_queue_proxy(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 return winner::scheduler::publish_queue(a,b,c,d);
}
