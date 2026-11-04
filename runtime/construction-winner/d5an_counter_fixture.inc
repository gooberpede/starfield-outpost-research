// SPDX-License-Identifier: GPL-3.0-or-later
// Owned disposable fixture only. The adversarial seam runs between the actual
// counter load and CAS. Each interference is a real competing causal Producer
// admitted on the same shared core counter. No claim of retail timing follows.
#include <memory>
extern "C" void D5AN_dispatch_node(uint64_t,uint64_t),D5AN_dispatch_fall();
extern "C" __declspec(dllexport) uint64_t D5AN_registration_entry(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 return winner::scheduler::registration<0>(a,b,c,d);
}
namespace {
winner::Patch d5an_registration_patch{};unsigned char* d5an_registration_relay{};std::string d5an_registration_relay_hash;
void d5an_registration_prepare(){
 using namespace winner;check(!enabled);DWORD old{},unused{};
 check(VirtualProtect(d5am_private+1728,128,PAGE_EXECUTE_READWRITE,&old));
 unsigned char stub[]{0x48,0x83,0xec,0x28,0xe8,55,0,0,0,0x48,0x83,0xc4,0x28,0xc3};
 memcpy(d5am_private+1728,stub,sizeof stub);unsigned char original[]{0x33,0xc0,0xc3};memcpy(d5am_private+1792,original,sizeof original);
 check(FlushInstructionCache(GetCurrentProcess(),d5am_private+1728,128));check(VirtualProtect(d5am_private+1728,128,old,&unused));
 auto& patch=d5an_registration_patch;patch.at=d5am_private+1732;patch.n=5;memcpy(patch.before,patch.at,5);
 d5an_registration_relay=near_page(U(patch.at));check(d5an_registration_relay);jump(d5an_registration_relay,U(&D5AN_registration_entry));
 check(VirtualProtect(d5an_registration_relay,4096,PAGE_EXECUTE_READ,&old));check(FlushInstructionCache(GetCurrentProcess(),d5an_registration_relay,4096));
 d5an_registration_relay_hash=sor::sha_bytes(d5an_registration_relay,4096);check(relative(patch,U(d5an_registration_relay),0xe8));
}
void d5an_registration_install(){
 using namespace winner;check(!enabled&&sole_thread());bool dirty{};
 check(install(&d5an_registration_patch,1,dirty));check(match(d5an_registration_patch,true));
}
struct D5anNode {alignas(16) unsigned char bytes[256]{};};
void d5an_node(D5anNode& node,U key){
 using namespace winner;U table=D5AM_sched_vtables[0];memcpy(node.bytes,&table,8);
 memcpy(node.bytes+8,&key,8);int32_t request[]{10,11};memcpy(node.bytes+0xb0,request,8);
 scheduler::registration_original[0]=&scheduler_fixture::registration_noop;
 scheduler::registration<0>(U(scheduler_fixture::server),0,U(node.bytes),0);
 check(scheduler::cookie(U(node.bytes)).allocation!=0);
 D5AM_sched_falls[1]=U(&D5AN_dispatch_fall);
}
HANDLE d5an_request{},d5an_done{};
std::atomic<U> d5an_target_thread{},d5an_steps{};
std::atomic<bool> d5an_quit{};
void d5an_interfere(std::atomic<U>* object,U,U) noexcept {
 if(object!=&winner::active||GetCurrentThreadId()!=d5an_target_thread||d5an_steps>=40)return;
 check(SetEvent(d5an_request));check(WaitForSingleObject(d5an_done,10000)==WAIT_OBJECT_0);++d5an_steps;
}
bool d5an_old_next(std::atomic<U>& object,U& result){
 U old=object.load();for(unsigned attempt=0;attempt<32;++attempt){
  if(old==UINT64_MAX)return false;
  d5an_interfere(&object,old,0);
  if(object.compare_exchange_weak(old,old+1)){result=old+1;return true;}
 }return false;
}
void d5an_comparative(){
 using namespace winner;
 // This instrumented copy preserves the original 32-CAS algorithm and inserts
 // only the adversarial scheduling seam. The original source is separately
 // pinned by the build/preservation manifests; this is not historical replay.
 for(unsigned repaired=0;repaired<2;++repaired){
  d5an_request=CreateEventW(nullptr,FALSE,FALSE,nullptr);d5an_done=CreateEventW(nullptr,FALSE,FALSE,nullptr);check(d5an_request&&d5an_done);
  d5an_quit=false;d5an_steps=0;U baseline=active.load();
  std::thread competitor([&]{std::vector<std::unique_ptr<causal::Producer>> held;
   for(;;){check(WaitForSingleObject(d5an_request,10000)==WAIT_OBJECT_0);if(d5an_quit.load())break;
    auto item=std::make_unique<causal::Producer>();check(item->admitted);held.push_back(std::move(item));check(SetEvent(d5an_done));
   }
  });
  d5an_target_thread=GetCurrentThreadId();U result{};bool admitted{};
  if(repaired){D5AN_fixture_before_cas=U(&d5an_interfere);scheduler::Producer producer;admitted=producer.admitted;D5AN_fixture_before_cas=0;}
  else admitted=d5an_old_next(active,result);
  check(admitted==bool(repaired));check(d5an_steps==(repaired?40:32));
  if(!repaired){check(active.load()==baseline+32);d5am_stage("pre-repair-shared-counter-refuses-after-32-real-interferences-no-capacity-pressure\n");}
  d5an_target_thread=0;d5an_quit=true;check(SetEvent(d5an_request));competitor.join();
  // The old path never increments on failed CAS. The competitor destructor
  // has removed all held admissions; no rollback belongs to the old path.
  check(active.load()==baseline&&causal::active==0&&scheduler::active==0);
  CloseHandle(d5an_request);CloseHandle(d5an_done);d5an_request=nullptr;d5an_done=nullptr;
  if(repaired)d5am_stage("post-repair-integrated-producer-admits-after-40-real-interferences-balanced-counters\n");
 }
 check(!D5AM_sched_counter_faults&&!D5AM_causal_counter_faults);
}
void d5an_run_matrix(U proc){
 using namespace winner;
 d5an_comparative();
 for(unsigned count:{2u,4u,8u,16u}){
 HANDLE start=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(start);std::atomic<U> arrived{};std::vector<std::thread> threads;
 std::vector<D5anNode> nodes(count);for(unsigned i=0;i<count;++i)d5an_node(nodes[i],0xd5a10000+i+count*100);
  for(unsigned n=0;n<count;++n)threads.emplace_back([&,n]{
   uint32_t foreign[2]{};U random=0xd5a00000u+n;arrived.fetch_add(1);check(WaitForSingleObject(start,10000)==WAIT_OBJECT_0);
   for(unsigned iteration=0;iteration<256;++iteration){
    random^=random<<13;random^=random>>7;random^=random<<17;if(random&1)YieldProcessor();
    scheduler::Producer first;check(first.admitted);causal::Producer second;check(second.admitted);
    {scheduler::Producer recursive;check(recursive.admitted);causal::Producer nested;check(nested.admitted);}
    ((void(*)(U))d5am_private)(U(foreign));
    ((void(*)(U,U))(d5am_private+1024))(U(foreign)+4,0xffffffff);check(!foreign[1]);
    D5AN_dispatch_node(U(nodes[n].bytes),U(scheduler_fixture::server));
   }
  });
  while(arrived.load()!=count)Sleep(1);check(SetEvent(start));for(auto& item:threads)item.join();CloseHandle(start);
  for(auto& node:nodes){auto cookie=scheduler::cookie(U(node.bytes));scheduler::Event retirement{};
   check(scheduler::snapshot(U(node.bytes),scheduler::Retire,0,cookie,retirement));check(retirement.allocation&&!retirement.status);check(scheduler::emit(retirement));
  }
  check(scheduler::identity_faults==0&&scheduler::registry_faults==0);
  check(!active&&!scheduler::active&&!causal::active&&!D5AM_causal_bridge_active&&!D5AM_sched_bridge_active);
  d5am_stage(("integrated-matrix threads="+std::to_string(count)+" iterations=256 seed-base=0xd5a00000 balanced-healthy\n").c_str());
 }
 // All channels execute the established native construction path on the same
 // private owner/helper pages; the generic task policy remains a typed seam.
 d5am_enable_provider(true);check(scheduler_fixture::invoke([&]{d5ai_fixture(*model,L"d5ai-native-mask3a",nullptr);},10,11));d5am_enable_provider(false);
 check(!D5AM_sched_counter_faults&&!D5AM_causal_counter_faults&&!scheduler::failed&&!causal::failed);
 check(sor::write_new(session/L"counter-matrix.json","{\"schema\":\"sor-d5an-matrix/1\",\"old_refused_after\":32,\"new_admitted_after\":40,\"threads\":[2,4,8,16],\"iterations\":256,\"seed_base\":3584032768,\"balanced\":true}\n"));
}
void d5an_run_fault(const std::wstring& scenario,HANDLE worker){
 using namespace winner;
 // Fault injection is explicit private-host state mutation, restored only once
 // the fault has been captured. It is never a retail recovery algorithm.
 D5anNode node;U expected{};
 if(scenario.find(L"asm")!=std::wstring::npos||scenario.starts_with(L"d5an-serial"))d5an_node(node,0xd5af0000);
 if(scenario==L"d5an-overflow-own"){
  scheduler::active=UINT64_MAX;{scheduler::Producer refused;check(!refused.admitted&&refused.core&&!refused.own);}
  check(active==0&&scheduler::active==UINT64_MAX);scheduler::active=0;expected=2;
 }else if(scenario==L"d5an-overflow-core"||scenario==L"d5an-before-owner"){
  active=UINT64_MAX;{scheduler::Producer refused;check(!refused.admitted&&!refused.core&&!refused.own);}
  check(active==UINT64_MAX);active=0;expected=1;
 }else if(scenario==L"d5an-overflow-causal"){
  causal::active=UINT64_MAX;{causal::Producer refused;check(!refused.admitted);}
  check(active==0&&causal::active==UINT64_MAX);causal::active=0;expected=32;
 }else if(scenario==L"d5an-causal-core"){
  active=UINT64_MAX;{causal::Producer refused;check(!refused.admitted);}
  check(causal::active==0&&active==UINT64_MAX);active=0;expected=33;
 }else if(scenario==L"d5an-asm-core"||scenario==L"d5an-asm-bridge"){
  auto& target=scenario==L"d5an-asm-core"?active:D5AM_sched_bridge_active;target=UINT64_MAX;
  D5AN_dispatch_node(U(node.bytes),U(scheduler_fixture::server));check(target==UINT64_MAX);target=0;
  check(active==0&&D5AM_sched_bridge_active==0);expected=scenario==L"d5an-asm-core"?1:8;
 }else if(scenario==L"d5an-causal-asm-core"||scenario==L"d5an-causal-asm-bridge"){
  auto& target=scenario==L"d5an-causal-asm-core"?active:D5AM_causal_bridge_active;target=UINT64_MAX;
  uint32_t foreign[2]{};((void(*)(U))d5am_private)(U(foreign));check(foreign[1]==1&&target==UINT64_MAX);target=0;
  check(active==0&&D5AM_causal_bridge_active==0);expected=scenario==L"d5an-causal-asm-core"?33:42;
 }else if(scenario==L"d5an-serial-publish"||scenario==L"d5an-serial-retire"){
  auto cookie=scheduler::cookie(U(node.bytes));check(cookie.slot<scheduler::registry_capacity);
  auto& slot=D5AM_sched_registry[cookie.slot];slot.serial=UINT64_MAX-1;cookie.serial=UINT64_MAX-1;
  scheduler::Event e{};check(!scheduler::identity(U(node.bytes),cookie,e,scenario==L"d5an-serial-publish",scenario==L"d5an-serial-retire"));
  expected=scenario==L"d5an-serial-publish"?9:10;
 }else if(scenario==L"d5an-teardown"){
  {causal::Producer admitted;check(admitted.admitted&&active==1);causal::active=0;}
  check(active==0&&causal::active==0);expected=32;
 }else if(scenario==L"d5an-teardown-scheduler"){
  {scheduler::Producer admitted;check(admitted.admitted&&active==1);scheduler::active=0;}
  check(active==0&&scheduler::active==0);expected=2;
 }else if(scenario==L"d5an-teardown-core"){
  {causal::Producer admitted;check(admitted.admitted&&active==1);active=0;}
  check(active==0&&causal::active==0);expected=33;
 }else if(scenario==L"d5an-token-scheduler"){
  scheduler::tokens=UINT64_MAX;U value{};check(!scheduler::next(scheduler::tokens,value)&&scheduler::tokens==UINT64_MAX);expected=5;
 }else check(false);
 check(counter::publication==2&&counter::first_thread==GetCurrentThreadId());
 check(counter::first_id==expected);
 check(counter::first_return.load()!=0&&counter::first_counter.load()!=0);
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);check(broken&&!enabled);
 d5am_stage("specific-counter-fault-captured-before-sticky-worker-terminal\n");
}
void d5an_startup_written(){
 using namespace winner;check(sole_thread());U saved=scheduler::written;
 scheduler::written=UINT64_MAX;check(!scheduler::advance_written());check(scheduler::written==UINT64_MAX);
 scheduler::written=saved;
 check(counter::publication==2&&counter::first_id==11&&counter::first_producer==9);
 d5am_stage("sole-thread-written-saturation-before-worker-exact-saved-value-restored\n");
}
HANDLE d5an_fault_entered{},d5an_fault_resume{};
void d5an_hold_fault() noexcept {
 check(SetEvent(d5an_fault_entered));check(WaitForSingleObject(d5an_fault_resume,60000)==WAIT_OBJECT_0);
}
void d5an_pending_fault(HANDLE worker){
 using namespace winner;
 d5an_fault_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);d5an_fault_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(d5an_fault_entered&&d5an_fault_resume);
 D5AN_fixture_fault_reserved=U(&d5an_hold_fault);scheduler::tokens=UINT64_MAX;
 std::thread first([]{winner::scheduler::increment(winner::scheduler::tokens);});
 check(WaitForSingleObject(d5an_fault_entered,10000)==WAIT_OBJECT_0);check(counter::publication==1);
 causal::tokens=UINT64_MAX;check(!causal::bump(causal::tokens));
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);
 // The completed terminal must explicitly retain publication=1. Independent
 // readers refuse all partial first-fault fields, even after the late writer
 // subsequently finishes in memory. There is no invented complete diagnostic.
 check(counter::publication==1&&broken&&!enabled);
 check(SetEvent(d5an_fault_resume));first.join();D5AN_fixture_fault_reserved=0;
 CloseHandle(d5an_fault_entered);CloseHandle(d5an_fault_resume);
 d5am_stage("paused-first-fault-second-fault-terminal-diagnostic-explicitly-incomplete\n");
}
void d5an_scheduler_loss(HANDLE worker){
 using namespace winner;
 fixture_pause=true;Sleep(60);U before=scheduler::drops.load();
 U occupied=scheduler::enqueue.load()-scheduler::dequeue.load();
 scheduler::Event e{};e.kind=scheduler::Provider;
 for(U i=occupied;i<=scheduler::capacity;++i)scheduler::emit(e);
 check(scheduler::drops==before+1&&scheduler::failed);
 scheduler::recording=true;check(!scheduler::emit(e));scheduler::recording=false;
 check(scheduler::drops==before+2&&scheduler::reentrant==1);
 fixture_pause=false;check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);check(broken&&!enabled);
 check(!D5AM_sched_counter_faults&&!D5AM_causal_counter_faults);
 d5am_stage("scheduler-full-queue-and-reentrant-loss-refuse-worker-health-without-counter-fault\n");
}
void d5an_scheduler_exhaustion(HANDLE worker){
 using namespace winner;
 U before=scheduler::drops.load();scheduler::fixture_queue_collisions=32;
 scheduler::Event e{};e.kind=scheduler::Provider;check(!scheduler::emit(e));
 check(scheduler::fixture_queue_collisions==0&&scheduler::drops==before+1&&scheduler::failed);
 check(!D5AM_sched_counter_faults&&!D5AM_causal_counter_faults);
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);check(broken&&!enabled);
 d5am_stage("queue-attempt-exhaustion-remains-loss-and-worker-failure-not-counter-contention\n");
}
void d5an_stop_teardown(HANDLE worker){
 using namespace winner;
 HANDLE entered=CreateEventW(nullptr,TRUE,FALSE,nullptr),resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(entered&&resume);
 std::thread admitted([&]{scheduler::Producer producer;check(producer.admitted);
  check(SetEvent(entered));check(WaitForSingleObject(resume,60000)==WAIT_OBJECT_0);
  scheduler::active=0; // Explicit private-host corruption of this owned count.
 });
 check(WaitForSingleObject(entered,10000)==WAIT_OBJECT_0);check(active==1&&scheduler::active==1);
 check(sor::write_new(session/L"STOP","Owned STOP before the held producer fails during teardown\n"));
 for(unsigned i=0;i<10000&&enabled.load();++i)Sleep(1);check(!enabled&&WaitForSingleObject(worker,0)==WAIT_TIMEOUT);
 check(SetEvent(resume));admitted.join();check(!active&&!scheduler::active);
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);check(broken&&counter::first_id==2&&counter::first_class==2);
 CloseHandle(entered);CloseHandle(resume);
 d5am_stage("stop-after-last-guard-held-producer-teardown-fault-rechecked-before-terminal\n");
}
void d5an_native_serial(HANDLE worker){
 using namespace winner;
 D5anNode node;d5an_node(node,0xd5af1000);auto cookie=scheduler::cookie(U(node.bytes));check(cookie.slot<scheduler::registry_capacity);
 D5AM_sched_registry[cookie.slot].serial=UINT64_MAX-1;
 check(match(d5an_registration_patch,true)&&sor::sha_bytes(d5an_registration_relay,4096)==d5an_registration_relay_hash);
 ((Four)(d5am_private+1728))(U(scheduler_fixture::server),0,U(node.bytes),0);
 check(counter::publication==2&&counter::first_id==9&&counter::first_producer==7);
 MEMORY_BASIC_INFORMATION producer{},helper{};
 check(VirtualQuery(reinterpret_cast<const void*>(counter::first_return.load()),&producer,sizeof producer));
 check(VirtualQuery(reinterpret_cast<const void*>(&D5AN_counter_next),&helper,sizeof helper));
 check(producer.AllocationBase==helper.AllocationBase);
 check(match(d5an_registration_patch,true)&&sor::sha_bytes(d5an_registration_relay,4096)==d5an_registration_relay_hash);
 std::string guard="{\"schema\":\"sor-d5an-registration-fixture/1\",\"site_va\":"+std::to_string(U(d5an_registration_patch.at))+
  ",\"original_patch_sha256\":"+sor::quote(sor::sha_bytes(d5an_registration_patch.before,5))+
  ",\"installed_patch_sha256\":"+sor::quote(sor::sha_bytes(d5an_registration_patch.after,5))+
  ",\"relay_sha256\":"+sor::quote(d5an_registration_relay_hash)+",\"guards_before_after\":true}\n";
 check(sor::write_new(session/L"registration-native-guard.json",guard));
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);check(broken&&!active&&!scheduler::active);
 d5am_stage("owned-native-patched-registration-overflow-records-observer-callsite-domain\n");
}
void d5an_timing(const std::vector<U>& baseline){
 using namespace winner;std::vector<U> samples;
 for(unsigned burst=0;burst<20;++burst){
  check(enabled&&!broken&&!scheduler::failed&&!causal::failed);
  for(unsigned i=0;i<32;++i){model->hit=false;LARGE_INTEGER before{},after{};
   QueryPerformanceCounter(&before);call(*model);QueryPerformanceCounter(&after);samples.push_back(U(after.QuadPart-before.QuadPart));
  }
  wait_durable();check(enabled&&!broken&&!scheduler::failed&&!causal::failed);
 }
 auto old=baseline;check(old.size()==1000&&samples.size()==640);std::sort(old.begin(),old.end());std::sort(samples.begin(),samples.end());
 LARGE_INTEGER frequency{};check(QueryPerformanceFrequency(&frequency));
 std::string text="{\"schema\":\"sor-d5an-owned-timing/1\",\"healthy_throughout\":true,\"bursts\":20,\"per_burst\":32,\"baseline_count\":1000,\"observed_count\":640,\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+
  ",\"baseline_p50_ticks\":"+std::to_string(old[499])+",\"observed_p50_ticks\":"+std::to_string(samples[319])+",\"observed_p95_ticks\":"+std::to_string(samples[607])+",\"observed_max_ticks\":"+std::to_string(samples.back())+"}\n";
 check(sor::write_new(session/L"counter-timing.json",text));
 d5am_stage("bounded-burst-owned-observer-timing-enabled-and-healthy-throughout\n");
}
void d5an_overload(HANDLE worker){
 using namespace winner;
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);check(broken&&!enabled);
 U causal_drops=causal::drops.load(),scheduler_drops=scheduler::drops.load();check(causal_drops||scheduler_drops);
 check(!D5AM_causal_counter_faults&&!D5AM_sched_counter_faults&&!causal::counter_overflow&&!counter_overflow&&counter::publication==0);
 check(!causal::reentrant&&!scheduler::reentrant&&!scheduler::registry_faults&&!scheduler::identity_faults&&!reentrant_losses);
 check(!active&&!causal::active&&!scheduler::active&&!D5AM_causal_bridge_active&&!D5AM_sched_bridge_active&&!geometry::active_capture&&!lifetime::active);
 check(causal::written==causal::enqueue&&scheduler::written==scheduler::enqueue&&enqueue==dequeue);
 check(std::string(output_fault)=="causal_or_scheduler_guard");
 std::string family=causal_drops?(scheduler_drops?"causal+scheduler":"causal"):"scheduler";
 std::string text="{\"schema\":\"sor-d5an-overload-control/1\",\"protective_failure\":true,\"healthy_timing_eligible\":false,\"loss_family\":"+sor::quote(family)+
  ",\"pressure_class\":\"queue loss reported; full queue versus bounded CAS exhaustion not distinguished\",\"balanced\":true,\"unexpected_counter_faults\":0,\"registry_faults\":0,\"identity_faults\":0,\"reentrant\":0,\"causal_capacity\":"+std::to_string(causal::capacity)+
  ",\"scheduler_capacity\":"+std::to_string(scheduler::capacity)+",\"causal_drops\":"+std::to_string(causal_drops)+",\"scheduler_drops\":"+std::to_string(scheduler_drops)+
  ",\"causal_enqueued\":"+std::to_string(causal::enqueue.load())+",\"causal_written\":"+std::to_string(causal::written.load())+
  ",\"scheduler_enqueued\":"+std::to_string(scheduler::enqueue.load())+",\"scheduler_written\":"+std::to_string(scheduler::written)+"}\n";
 check(sor::write_new(session/L"overload-control.json",text));
}
}
