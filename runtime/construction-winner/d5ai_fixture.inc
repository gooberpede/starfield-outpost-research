// SPDX-License-Identifier: GPL-3.0-or-later
// Owned disposable memory, genuine C++ reader/writer exclusion and the candidate
// assembly acquire wrapper. This is not a retail scheduler or generator.
#include <shared_mutex>
#include <functional>
#include "d5ai_population.generated.h"
extern "C" {uint64_t d5ai_invoke(uint64_t,uint64_t,uint64_t,uint32_t,uint32_t);uint64_t d5ai_complete_invoke(uint64_t,uint64_t,uint32_t);uint32_t d5ai_preunlock_invoke(uint32_t);void d5ai_at_acquire();void d5ai_at_complete();void d5ai_at_preunlock();}
extern "C" {uint64_t d5ai_fixture_owner(uint64_t,uint64_t,uint64_t,uint64_t);uint64_t d5ai_fixture_context_reset(uint64_t,uint64_t,uint64_t,uint64_t);}
extern "C" {uint64_t d5ai_fixture_life_holder(uint64_t,uint64_t,uint64_t,uint64_t);uint64_t d5ai_fixture_life_collection(uint64_t,uint64_t,uint64_t,uint64_t);uint64_t d5ai_fixture_life_mutation(uint64_t,uint64_t,uint64_t,uint64_t);}
extern "C" uint64_t d5ai_native_life_collection(uint64_t receiver,uint64_t,uint64_t,uint64_t){memset((void*)receiver,0,16);return 0xc011;}
extern "C" uint64_t d5ai_native_life_mutation(uint64_t receiver,uint64_t,uint64_t,uint64_t){U data{};memcpy(&data,(void*)(receiver+8),8);if(data){U points{};memcpy(&points,(void*)(data+32),8);if(points){float changed=99;memcpy((void*)points,&changed,4);}}return 0xc012;}
extern "C" uint64_t d5ai_native_life_holder(uint64_t receiver,uint64_t,uint64_t,uint64_t){U data{},cap{};memcpy(&data,(void*)(receiver+16),8);memcpy(&cap,(void*)(receiver+24),8);for(U i=0;i<cap;++i){uint32_t used{};U collection{};memcpy(&used,(void*)(data+i*24+16),4);memcpy(&collection,(void*)(data+i*24+8),8);if(used!=UINT32_MAX&&collection){if(InterlockedDecrement((LONG*)collection)==0)d5ai_fixture_life_collection(collection+8,0,0,0);uint32_t empty=UINT32_MAX;memcpy((void*)(data+i*24+16),&empty,4);}}return 0xc013;}
namespace {
std::shared_mutex d5ai_native_mutex;
std::atomic<unsigned> d5ai_readers{};
bool d5ai_exclusive{};
std::function<void()> d5ai_gap_action;
U d5ai_lock_result=0x12345678;
}
extern "C" uint64_t d5ai_native_acquire(uint64_t lock,uint64_t,uint64_t,uint64_t){
 d5ai_native_mutex.lock_shared();auto readers=++d5ai_readers;
 uint32_t owner=d5ai_exclusive?GetCurrentThreadId():0;
 InterlockedExchange((LONG*)lock,LONG(owner));InterlockedExchange((LONG*)(lock+4),LONG(d5ai_exclusive?0x400000:readers));return d5ai_lock_result;
}
extern "C" uint64_t d5ai_native_owner(uint64_t manager,uint64_t owner,uint64_t descriptor,uint64_t marker){
 check(marker==0x1234&&descriptor==manager+0xc8);uint32_t value=uint32_t(owner);memcpy((void*)(manager+0x80),&value,4);return 0xaabb;
}
extern "C" uint64_t d5ai_native_context_reset(uint64_t manager,uint64_t flag,uint64_t descriptor,uint64_t marker){
 check(flag==1&&descriptor==manager+0xc8&&marker==0x5678);U data{},capacity{};memcpy(&data,model->proc+0x20,8);memcpy(&capacity,model->proc+0x28,8);
 for(U i=0;i<capacity;++i){uint32_t empty=UINT32_MAX;memcpy((void*)(data+i*24+16),&empty,4);}fixture_reset(model->proc_identity,0,0,0);
 if(d5ai_gap_action)d5ai_gap_action();uint32_t zero=0;memcpy((void*)(manager+0x80),&zero,4);return 0xccdd;
}
namespace {
void d5ai_fixture_publish(Model& m){
 U data{};memcpy(&data,m.proc+0x20,8);uint32_t occupied{};memcpy(&occupied,(void*)(data+16),4);check(occupied==UINT32_MAX);
 U holder=m.d5ai_output-8;memcpy((void*)data,&m.source,8);memcpy((void*)(data+8),&holder,8);occupied=0;memcpy((void*)(data+16),&occupied,4);
 oracle("d5ai-map-publication",m,data,holder,m.d5ai_output);
}
void d5ai_setup(){
 check(lifetime::configure((void*)&d5ai_fixture_life_holder,(void*)&d5ai_fixture_life_collection,(void*)&d5ai_fixture_life_mutation,sor::sha_bytes((void*)&d5ai_fixture_life_holder,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_life_collection,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_life_mutation,32).c_str()));
 check(geometry::configure_acquire((void*)&d5ai_at_acquire,sor::sha_bytes((void*)&d5ai_at_acquire,32),sor::sha_bytes((void*)&d5ai_native_acquire,32)));
 check(geometry::configure_completion((void*)&d5ai_at_complete,sor::sha_bytes((void*)&d5ai_at_complete,32)));
 check(geometry::configure_preunlock((void*)&d5ai_at_preunlock,sor::sha_bytes((void*)&d5ai_at_preunlock,32)));
 check(context::configure((void*)&d5ai_fixture_owner,(void*)&d5ai_fixture_context_reset,sor::sha_bytes((void*)&d5ai_fixture_owner,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_context_reset,32).c_str()));
}
void d5ai_fixture(Model& m,const std::wstring& scenario,HANDLE recorder_worker){
 namespace g=geometry;
 wait_durable();
 struct Native {
  alignas(8) unsigned char holder[64]{},collection[24]{},resources[48]{},map[48]{},region[48]{},points[32]{},query[24]{};
  Native(Model& m){
   auto put=[](void* p,size_t n,const auto& v){memcpy((unsigned char*)p+n,&v,sizeof v);};
   put(holder,0,uint32_t(1));put(holder,8,int32_t(-200));put(holder,12,int32_t(-200));
   put(holder,0x20,U(resources));put(holder,0x28,U(2));
   put(resources,0,uint32_t(0x57d4));put(resources,8,U(collection));put(resources,16,uint32_t(0));put(resources,40,UINT32_MAX);
   put(collection,0,uint32_t(1));put(collection,8,uint32_t(1));put(collection,12,uint32_t(1));put(collection,16,U(region));
   const float p[]{1,2,3,4,5,6,7,8};memcpy(points,p,sizeof p);
   const float bound[]{-10,-10,10,10};memcpy(region,bound,sizeof bound);put(region,16,uint32_t(0x57d4));put(region,20,uint32_t(0xa5a5a501));
   put(region,24,uint32_t(2));put(region,28,uint32_t(2));put(region,32,U(points));
   put(map,0,m.source);put(map,8,U(holder));put(map,16,uint32_t(0));put(map,40,UINT32_MAX);
   put(m.proc,0x20,U(map));put(m.proc,0x28,U(2));
   const float query_p[]{300,300,0};memcpy(query,query_p,sizeof query_p);put(query,12,uint32_t(0));put(query,16,U(0x12340000));
  }
 } n(m);
 std::vector<std::vector<unsigned char>> population_backing;
 if(scenario.starts_with(L"d5ai-native-")){
  unsigned run=scenario==L"d5ai-native-mask0"?0:scenario==L"d5ai-native-mask3a"?1:2;
  const auto* data=d5ai_population_data[run];const auto length=d5ai_population_size[run];size_t pos=0;
  auto word=[&](){check(pos+4<=length);uint32_t value{};memcpy(&value,data+pos,4);pos+=4;return value;};
  auto allocation=[&](size_t size){population_backing.emplace_back(size,0);return population_backing.back().data();};
  auto put=[](void* p,size_t at,const auto& value){memcpy((unsigned char*)p+at,&value,sizeof value);};
  auto resource_count=word();U capacity=1;while(capacity<=resource_count)capacity*=2;
  auto resources=allocation(size_t(capacity)*24);for(U i=0;i<capacity;++i)put(resources,size_t(i)*24+16,UINT32_MAX);
  put(n.holder,0x20,U(resources));put(n.holder,0x28,capacity);
  for(uint32_t i=0;i<resource_count;++i){auto form=word(),regions=word();auto collection=allocation(24),region_data=allocation(size_t(regions)*48);
   put(resources,size_t(i)*24,form);put(resources,size_t(i)*24+8,U(collection));put(resources,size_t(i)*24+16,uint32_t(0));
   put(collection,0,uint32_t(1));put(collection,8,regions);put(collection,12,regions);put(collection,16,U(region_data));
   for(uint32_t j=0;j<regions;++j){auto region=region_data+size_t(j)*48;check(pos+24<=length);memcpy(region,data+pos,24);pos+=24;auto count=word();
    auto points=allocation(size_t(count)*16);check(pos+size_t(count)*16<=length);memcpy(points,data+pos,size_t(count)*16);pos+=size_t(count)*16;
    put(region,24,count);put(region,28,count);put(region,32,U(points));
   }
  }check(pos==length);
 }
 unsigned char manager[0x210]{};manager[0x20]=2;uint32_t body=0x5e0de;U attached=U(m.proc);memcpy(manager+0x80,&body,4);memcpy(manager+0x130,&attached,8);memcpy(manager+0xc8,m.descriptor,44);g::fixture_manager=U(manager);
 fixture_reset(m.proc_identity,0,0,0);uint32_t empty_slot=UINT32_MAX;memcpy(n.map+16,&empty_slot,4);m.born=false;m.d5ai_output=U(n.holder)+8;m.hit=false;m.visited=0;call(m);wait_durable();
 auto finish=[&]{U capacity{};memcpy(&capacity,m.proc+0x28,8);if(scenario!=L"d5ai-missing-preunlock")check(d5ai_preunlock_invoke(scenario==L"d5ai-consumer-partial"||scenario==L"d5ai-last-false"?0:1)==UINT32_MAX);--d5ai_readers;d5ai_native_mutex.unlock_shared();if(scenario!=L"d5ai-unfinished")check(d5ai_complete_invoke(scenario==L"d5ai-consumer-partial"?0:capacity,capacity,99)==d5ai_lock_result);};
 auto request=[&](U id){check(g::arm(id));U result=d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000);check(result==d5ai_lock_result);finish();};
 auto await=[&](U count){for(unsigned i=0;i<10000&&g::completed.load()<count&&!broken;++i)Sleep(1);check(g::completed.load()>=count);};
 if(scenario==L"d5ai-controller-host"){
  check(sor::write_new(session/L"fixture-controller-ready.json","{\"owned_world_ready\":true}\n"));U next=1;
  while(enabled.load()){
   auto command=session/(L"fixture-query-"+std::to_wstring(next));
   if(std::filesystem::exists(command)){check(g::armed.load()==next);check(d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000)==d5ai_lock_result);finish();await(next);++next;}
   if(std::filesystem::exists(session/L"fixture-controller-done"))break;Sleep(1);
  }
 }else if(scenario==L"d5ai-life-write-fault"||scenario==L"d5ai-life-flush-fault"||scenario==L"d5ai-life-ack-fault"){
  request(1);await(1);lifetime::fixture_hold=true;check(d5ai_fixture_life_mutation(U(n.collection)+8,0,0,0)==0xc012);
  fixture_fault=scenario==L"d5ai-life-write-fault"?2:scenario==L"d5ai-life-flush-fault"?3:4;lifetime::fixture_hold=false;
  check(WaitForSingleObject(recorder_worker,INFINITE)==WAIT_OBJECT_0);check(lifetime::failed&&broken);
 }else if(scenario==L"d5ai-life-stop-admitted"){
  request(1);await(1);lifetime::fixture_reserved=CreateEventW(nullptr,TRUE,FALSE,nullptr);lifetime::fixture_publish=CreateEventW(nullptr,TRUE,FALSE,nullptr);
  std::thread producer([&]{d5ai_fixture_life_mutation(U(n.collection)+8,0,0,0);});check(WaitForSingleObject(lifetime::fixture_reserved,60000)==WAIT_OBJECT_0);
  check(sor::write_new(session/L"STOP","STOP with admitted lifetime producer\n"));for(unsigned i=0;i<10000&&enabled.load();++i)Sleep(1);check(!enabled.load());
  check(WaitForSingleObject(recorder_worker,0)==WAIT_TIMEOUT);check(SetEvent(lifetime::fixture_publish));producer.join();check(WaitForSingleObject(recorder_worker,INFINITE)==WAIT_OBJECT_0);
  check(lifetime::enqueue==2&&!lifetime::failed);CloseHandle(lifetime::fixture_reserved);CloseHandle(lifetime::fixture_publish);lifetime::fixture_reserved=lifetime::fixture_publish=nullptr;
 }else if(scenario.starts_with(L"d5ai-life-")){
  unsigned char collection2[24]{},region2[48]{},points2[32]{};
  auto put=[](void* p,size_t at,const auto& value){memcpy((unsigned char*)p+at,&value,sizeof value);};
  if(scenario==L"d5ai-life-empty-null"){put(n.collection,8,uint32_t(0));put(n.collection,12,uint32_t(0));put(n.collection,16,U(0));}
  if(scenario==L"d5ai-life-empty-spare")put(n.collection,8,uint32_t(0));
  if(scenario==L"d5ai-life-partial"){
   memcpy(collection2,n.collection,24);memcpy(region2,n.region,48);memcpy(points2,n.points,32);put(collection2,0,uint32_t(2));put(collection2,16,U(region2));put(region2,32,U(points2));put(region2,16,uint32_t(0x57d5));
   put(n.resources,24,uint32_t(0x57d5));put(n.resources,32,U(collection2));put(n.resources,40,uint32_t(0));
  }
  request(1);await(1);
  if(scenario==L"d5ai-life-external-collection")put(n.collection,0,uint32_t(2));
  if(scenario==L"d5ai-life-final"||scenario==L"d5ai-life-external-collection"||scenario==L"d5ai-life-partial"||scenario==L"d5ai-life-aba")check(d5ai_fixture_life_holder(U(n.holder)+16,1,2,3)==0xc013);
  if(scenario==L"d5ai-life-mutation")check(d5ai_fixture_life_mutation(U(n.collection)+8,1,2,3)==0xc012);
  if(scenario==L"d5ai-life-aba"){
   // Same numeric address contains a new graph; the old BEGIN is irreversible.
   put(n.resources,0,uint32_t(0x57d4));put(n.resources,8,U(n.collection));put(n.resources,16,uint32_t(0));put(n.collection,0,uint32_t(1));put(n.collection,8,uint32_t(1));put(n.collection,12,uint32_t(1));put(n.collection,16,U(n.region));
  }
  if(scenario==L"d5ai-life-stalled"){
   lifetime::fixture_reserved=CreateEventW(nullptr,TRUE,FALSE,nullptr);lifetime::fixture_publish=CreateEventW(nullptr,TRUE,FALSE,nullptr);
   std::thread producer([&]{d5ai_fixture_life_mutation(U(n.collection)+8,0,0,0);});check(WaitForSingleObject(lifetime::fixture_reserved,60000)==WAIT_OBJECT_0);
   auto marker=lifetime::mark();check(!lifetime::coherent(marker)&&marker.active_before>0);check(SetEvent(lifetime::fixture_publish));producer.join();CloseHandle(lifetime::fixture_reserved);CloseHandle(lifetime::fixture_publish);lifetime::fixture_reserved=lifetime::fixture_publish=nullptr;
  }
  if(scenario==L"d5ai-life-stop"){
   enabled=false;check(d5ai_fixture_life_holder(U(n.holder)+16,0,0,0)==0xc013);check(lifetime::unlogged_cutoff>0);enabled=true;
  }
  if(scenario==L"d5ai-life-overflow"||scenario.starts_with(L"d5ai-life-counter-")){
   lifetime::fixture_hold=true;g::held=true;
   if(scenario==L"d5ai-life-counter-token"){lifetime::tokens=UINT64_MAX;d5ai_fixture_life_mutation(U(n.collection)+8,0,0,0);}
   else if(scenario==L"d5ai-life-counter-generation"){lifetime::generation=UINT64_MAX;d5ai_fixture_life_mutation(U(n.collection)+8,0,0,0);}
   else if(scenario==L"d5ai-life-counter-loss"){lifetime::drops=UINT64_MAX;lifetime::lose();}
   else for(U i=0;i<lifetime::capacity/2+1;++i)d5ai_fixture_life_mutation(U(n.collection)+8,0,0,0);
   check(lifetime::failed);if(scenario.starts_with(L"d5ai-life-counter-"))check(lifetime::counter_overflow);else check(lifetime::drops>0);
  }
  uint32_t empty=UINT32_MAX;memcpy(n.map+16,&empty,4);request(2);
  if(scenario==L"d5ai-life-overflow"||scenario.starts_with(L"d5ai-life-counter-")){lifetime::fixture_hold=false;g::held=false;check(WaitForSingleObject(recorder_worker,INFINITE)==WAIT_OBJECT_0);check(lifetime::failed&&broken);}
  else await(2);
 }else if(scenario.starts_with(L"d5ai-context-")){
  request(1);await(1);
  if(scenario==L"d5ai-context-owner-change")check(d5ai_fixture_owner(U(manager),0x23456,U(manager)+0xc8,0x1234)==0xaabb);
  else if(scenario==L"d5ai-context-clean"){
   check(d5ai_fixture_owner(U(manager),0x5e0de,U(manager)+0xc8,0x1234)==0xaabb);
   uint32_t empty=UINT32_MAX;memcpy(n.map+16,&empty,4);fixture_reset(m.proc_identity,0,0,0);m.born=false;m.hit=false;m.visited=0;call(m);
  }else {
   if(scenario==L"d5ai-context-mid-gap")d5ai_gap_action=[&]{m.born=false;m.hit=false;m.visited=0;call(m);request(2);await(2);};
   check(d5ai_fixture_context_reset(U(manager),1,U(manager)+0xc8,0x5678)==0xccdd);d5ai_gap_action={};
  }
  if(scenario!=L"d5ai-context-mid-gap"){request(2);await(2);}
 }else if(scenario==L"d5ai-stop-admission"){
  wait_durable();g::fixture_admission_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);g::fixture_admission_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(g::fixture_admission_entered&&g::fixture_admission_resume);check(g::arm(1));
  std::thread reader([&]{check(d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000)==d5ai_lock_result);finish();});
  check(WaitForSingleObject(g::fixture_admission_entered,10000)==WAIT_OBJECT_0);check(g::active_capture==0);
  check(sor::write_new(session/L"STOP","fixture STOP before geometry admission\n"));
  for(unsigned i=0;i<10000&&!std::filesystem::exists(session/L"terminal.json");++i)Sleep(1);check(std::filesystem::exists(session/L"terminal.json"));
  check(SetEvent(g::fixture_admission_resume));reader.join();check(g::captured==0&&g::active_capture==0);
  CloseHandle(g::fixture_admission_entered);CloseHandle(g::fixture_admission_resume);g::fixture_admission_entered=g::fixture_admission_resume=nullptr;
 }else if(scenario==L"d5ai-file-arm"||scenario==L"d5ai-foreign-arm"){
  wait_durable();auto payload=(scenario==L"d5ai-foreign-arm"?std::string(64,'a'):identity_hash)+"\n1";
  check(sor::write_new(session/L"geometry-arm.txt",payload));
  for(unsigned i=0;i<10000&&!g::armed.load()&&enabled.load();++i)Sleep(1);
  if(scenario==L"d5ai-foreign-arm")check(!enabled.load()&&!g::armed.load());
  else {check(g::armed==1);check(d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000)==d5ai_lock_result);finish();}
 }else if(scenario==L"d5ai-write-fault"||scenario==L"d5ai-flush-fault"||scenario==L"d5ai-receipt-fault"||scenario==L"d5ai-worker-exit"||scenario==L"d5ai-process-exit"){
  wait_durable();g::held=true;request(1);
  if(scenario==L"d5ai-process-exit")TerminateProcess(GetCurrentProcess(),74);
  if(scenario==L"d5ai-receipt-fault")g::fixture_receipt_fault=true;
  else fixture_fault=scenario==L"d5ai-write-fault"?2:scenario==L"d5ai-flush-fault"?3:6;
  g::held=false;for(unsigned i=0;i<10000&&enabled.load();++i)Sleep(1);check(!enabled.load());
 }else if(scenario==L"d5ai-stop-during"){
  wait_durable();g::fixture_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);g::fixture_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(g::fixture_entered&&g::fixture_resume);check(g::arm(1));
  std::thread reader([&]{check(d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000)==d5ai_lock_result);finish();});
  check(WaitForSingleObject(g::fixture_entered,10000)==WAIT_OBJECT_0);check(sor::write_new(session/L"STOP","fixture STOP during geometry copy\n"));
  for(unsigned i=0;i<10000&&enabled.load();++i)Sleep(1);check(!enabled.load());check(SetEvent(g::fixture_resume));reader.join();
  CloseHandle(g::fixture_entered);CloseHandle(g::fixture_resume);g::fixture_entered=g::fixture_resume=nullptr;
 }else if(scenario==L"d5ai-retained"||scenario==L"d5ai-rebuilt-equal"||scenario==L"d5ai-rebuilt-different"||scenario==L"d5ai-unavailable"){
  request(1);await(1);
  if(scenario==L"d5ai-retained"){m.visited=1;call(m);request(2);}
  else {
   fixture_retire(m.source,0,0,0);
   memcpy(m.additional_sources[0],m.source_bytes,0x70);m.source=U(m.additional_sources[0]);m.born=false;m.hit=false;
   unsigned char replacement_holder[64]{};memcpy(replacement_holder,n.holder,64);
   memcpy(n.map,&m.source,8);U holder=U(replacement_holder);memcpy(n.map+8,&holder,8);
   if(scenario==L"d5ai-unavailable"){
    uint32_t empty=UINT32_MAX;memcpy(n.map+16,&empty,4);m.visited=1;call(m);
   }else {
    fixture_reset(m.proc_identity,0,0,0);m.visited=0;m.d5ai_output=holder+8;
    uint32_t empty=UINT32_MAX;memcpy(n.map+16,&empty,4);
    if(scenario==L"d5ai-rebuilt-different"){float changed=99;memcpy(n.points,&changed,4);}
    call(m);
   }
   request(2);await(2);fixture_retire(m.source,0,0,0);
  }
 }else if(scenario==L"d5ai-read-fault"){
  U bad=0x10000;memcpy(n.region+32,&bad,8);request(1);
 }else if(scenario==L"d5ai-malformed"){
  uint32_t bad=3;memcpy(n.region+24,&bad,4);request(1);
 }else if(scenario==L"d5ai-empty"){
  U zero=0;memcpy(m.proc+0x28,&zero,8);request(1);
 }else if(scenario==L"d5ai-arena-full"){
  uint32_t count=uint32_t(g::arena_bytes/16);memcpy(n.region+24,&count,4);memcpy(n.region+28,&count,4);request(1);
 }else if(scenario==L"d5ai-overflow"){
  g::held=true;for(U i=1;i<=5;++i)request(i);check(g::no_slot==1&&g::captured==4);g::held=false;
  // Deliberate sticky failure triggers shutdown. Let the actual worker finish
  // its drain/flush/terminal before normal fixture cleanup or wait_durable's
  // fail-fast broken-worker predicate; otherwise the test itself kills evidence.
  check(WaitForSingleObject(recorder_worker,INFINITE)==WAIT_OBJECT_0);
  check(g::failed&&broken&&g::completed==4&&acknowledged.load()==enqueue.load());
  check(std::filesystem::exists(session/L"terminal.json"));
 }else if(scenario==L"d5ai-retire-during"){
  g::fixture_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);g::fixture_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(g::fixture_entered&&g::fixture_resume);
  check(g::arm(1));std::atomic<bool> retired{},writer_started{};
  std::thread reader([&]{check(d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000)==d5ai_lock_result);finish();});
  check(WaitForSingleObject(g::fixture_entered,10000)==WAIT_OBJECT_0);
  std::thread writer([&]{writer_started=true;++hazards;++epoch;std::unique_lock lock(d5ai_native_mutex);U zero=0;memcpy(m.proc+0x28,&zero,8);memset(n.points,0xcc,sizeof n.points);++epoch;--hazards;retired=true;});
  while(!writer_started)Sleep(1);Sleep(10);check(!retired);check(SetEvent(g::fixture_resume));reader.join();writer.join();check(retired);
  CloseHandle(g::fixture_entered);CloseHandle(g::fixture_resume);g::fixture_entered=g::fixture_resume=nullptr;
  await(1);request(2);
 }else if(scenario==L"d5ai-concurrent"){
  // One arm may be consumed by only one of these actual concurrent readers.
  check(g::arm(1));std::vector<std::thread> readers;
  for(unsigned i=0;i<8;++i)readers.emplace_back([&]{check(d5ai_invoke(U(m.proc)+0x40,U(n.query),0xabcdef,0x43160000,0x447a0000)==d5ai_lock_result);finish();});
  for(auto& t:readers)t.join();check(g::captured==1);
 }else if(scenario==L"d5ai-exclusive"){
  d5ai_exclusive=true;request(1);d5ai_exclusive=false;
 }else if(scenario==L"d5ai-interrupted"){
  ++hazards;request(1);--hazards;
 }else if(scenario==L"d5ai-stale-arm"){
  request(1);check(!g::arm(1)&&!g::arm(0));
 }else if(scenario==L"d5ai-held-worker"){
  g::held=true;request(1);check(g::captured==1&&g::completed==0);memset(n.points,0xcc,sizeof n.points);g::held=false;
 }else request(1);
 if(!scenario.starts_with(L"d5ai-life-counter-")&&scenario!=L"d5ai-life-overflow"&&scenario!=L"d5ai-overflow"&&scenario!=L"d5ai-unfinished"&&scenario!=L"d5ai-write-fault"&&scenario!=L"d5ai-flush-fault"&&scenario!=L"d5ai-receipt-fault")await(g::captured.load());
 check(sor::write_new(session/L"d5ai-host-oracle.json","{\"schema\":\"d5ai-host/1\",\"scenario\":"+sor::quote(std::string(scenario.begin(),scenario.end()))+
  ",\"source\":"+std::to_string(m.source)+",\"holder\":"+std::to_string(U(n.holder))+",\"collection\":"+std::to_string(U(n.collection))+
  ",\"expected_points_hex\":\"0000803f0000004000004040000080400000a0400000c0400000e04000000041\",\"copied_under_shared_reader\":true}\n"));
 fixture_destroy(m.proc_identity,0,0,0);g::fixture_manager=0;
}
}
