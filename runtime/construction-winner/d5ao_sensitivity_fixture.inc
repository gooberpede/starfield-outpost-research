// SPDX-License-Identifier: GPL-3.0-or-later
// D5AO owned sensitivity experiment. Scheduling seams are deliberate fixture
// interventions, not observations of ordinary Windows or retail frequencies.
namespace {
std::atomic<U> d5ao_subject{},d5ao_collisions{};
HANDLE d5ao_interference{},d5ao_changed{};
std::atomic<std::atomic<U>*> d5ao_object{};
void d5ao_collision(std::atomic<U>* object,U,U) noexcept {
 auto* watched=d5ao_object.load();
 if(object!=watched||GetCurrentThreadId()!=d5ao_subject.load()||d5ao_collisions.load())return;
 ++d5ao_collisions;
 check(SetEvent(d5ao_interference));
 check(WaitForSingleObject(d5ao_changed,10000)==WAIT_OBJECT_0);
}
U d5ao_now(){LARGE_INTEGER t{};check(QueryPerformanceCounter(&t));return U(t.QuadPart);}
void d5ao_until(U time){while(d5ao_now()<time)YieldProcessor();}

// Independent unhooked original-instruction page uses real Windows waits/wakes.
// Only proven RIP-relative import slots are relocated. Original bytes remain
// pinned by the parent builder's executable/site hashes and generated header.
unsigned char* d5ao_reference(){
 auto* page=(unsigned char*)VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(page);
 const unsigned char* codes[]{d5am_original_reader,d5am_original_writer,d5am_original_release};
 const unsigned sizes[]{126,216,81},offsets[]{0,256,512};
 const U vas[]{0x1422cc350,0x1422cc3d0,0x1402c45a0};unsigned slot=2048;
 for(unsigned j=0;j<3;++j){auto* p=page+offsets[j];memcpy(p,codes[j],sizes[j]);
  for(unsigned i=0;i+5<sizes[j];++i)if(p[i]==0xff&&(p[i+1]==0x15||p[i+1]==0x25)){
   int32_t displacement{};memcpy(&displacement,p+i+2,4);U target=vas[j]+i+6+displacement,value{};
   if(target==0x143a3f418)value=U(&GetCurrentThreadId);
   else if(target==0x143a402d0)value=U(&WaitOnAddress);
   else if(target==0x143a402c8)value=U(&WakeByAddressSingle);
   else if(target==0x143a402d8)value=U(&WakeByAddressAll);
   else check(false);
   memcpy(page+slot,&value,8);int32_t relative=int32_t(slot-(offsets[j]+i+6));memcpy(p+i+2,&relative,4);slot+=8;i+=5;
  }
 }
 DWORD old{};check(VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old));check(FlushInstructionCache(GetCurrentProcess(),page,4096));return page;
}

void d5ao_sensitivity(U proc,HANDLE){
 using namespace winner;
 LARGE_INTEGER frequency{};check(QueryPerformanceFrequency(&frequency));U hz=U(frequency.QuadPart);
 auto* reference=d5ao_reference();
 d5ao_interference=CreateEventW(nullptr,FALSE,FALSE,nullptr);d5ao_changed=CreateEventW(nullptr,FALSE,FALSE,nullptr);check(d5ao_interference&&d5ao_changed);
 std::string rows="[";bool first=true;
 D5AO_real_wait=true;
 // Paired close contenders have a 250 microsecond offset; separated controls
 // have 20 milliseconds. These are workload inputs, never safety cutoffs.
 for(U gap_us:{250ULL,20000ULL})for(unsigned repeat=0;repeat<12;++repeat)for(unsigned observed=0;observed<2;++observed){
  alignas(8) uint32_t local_lock[2]{};U lock=observed?proc+0x40:U(local_lock);
  auto writer=(void(*)(U))(observed?d5am_private+1216:reference+256);
  auto release=(void(*)(U))(observed?d5am_private+512:reference+512);
  auto* words=(uint32_t*)lock;check(!words[0]&&!words[1]);
  std::atomic<U> object{},winner_id{},go{},counter_begin{},counter_end{};d5ao_object=&object;d5ao_collisions=0;
  std::thread rival([&]{
   check(WaitForSingleObject(d5ao_interference,10000)==WAIT_OBJECT_0);
   object.fetch_add(1);U start=d5ao_now();check(SetEvent(d5ao_changed));
   d5ao_until(start+hz*gap_us/1000000);writer(lock);U zero=0;winner_id.compare_exchange_strong(zero,2);release(lock);
  });
  d5ao_subject=GetCurrentThreadId();D5AN_fixture_before_cas=U(&d5ao_collision);
  counter_begin=d5ao_now();
  if(observed){U result{};check(D5AN_counter_next(&object,1,1,&result));check(result==2);}
  else {check(SetEvent(d5ao_interference));check(WaitForSingleObject(d5ao_changed,10000)==WAIT_OBJECT_0);}
  counter_end=d5ao_now();D5AN_fixture_before_cas=0;
  writer(lock);U zero=0;winner_id.compare_exchange_strong(zero,1);release(lock);rival.join();
  check(!words[0]&&!words[1]&&winner_id.load());
  if(!first)rows+=",";first=false;
  rows+="{\"observed\":"+std::to_string(observed)+",\"gap_us\":"+std::to_string(gap_us)+",\"repeat\":"+std::to_string(repeat)+",\"winner\":"+std::to_string(winner_id.load())+",\"counter_ticks\":"+std::to_string(counter_end-counter_begin)+",\"forced_collisions\":"+std::to_string(d5ao_collisions.load())+"}";
 }
 rows+="]";D5AN_fixture_before_cas=0;d5ao_subject=0;d5ao_object=nullptr;
 // Real original reader/writer contention: hold a native reader, admit a
 // competing writer, then release. The fixture uses real WaitOnAddress.
 auto lock=proc+0x40;auto* words=(uint32_t*)lock;
 ((void(*)(U))d5am_private)(lock);check(words[1]==1);
 std::atomic<bool> entered{},acquired{};U waits_before=D5AO_real_wait_calls.load();
 std::thread waiter([&]{entered=true;((void(*)(U))(d5am_private+1216))(lock);acquired=true;((void(*)(U))(d5am_private+512))(lock);});
 while(D5AO_real_wait_calls.load()==waits_before)YieldProcessor();
 U wait_calls=D5AO_real_wait_calls.load()-waits_before;
 U pending=U(uint32_t(InterlockedCompareExchange((volatile LONG*)(lock+4),0,0)))&0x3ff000;
 check(entered.load()&&!acquired.load()&&pending);
 ((void(*)(U,U))(d5am_private+1024))(lock+4,0xffffffff);
 // This private typed-release stub ends at XADD/MOV/RET. The real native
 // callsite has a subsequent conditional wake; model that omitted continuation
 // explicitly so the original infinite WaitOnAddress can resume.
 WakeByAddressAll((void*)(lock+4));waiter.join();check(acquired&&!words[0]&&!words[1]);
 D5AO_real_wait=false;
 CloseHandle(d5ao_interference);CloseHandle(d5ao_changed);check(VirtualFree(reference,0,MEM_RELEASE));
 // Per-ID fast-path observations bracket batches, so QPC is outside each
 // update. No timing telemetry is added to the production helper itself.
 std::string latency="[";first=true;
 for(U id:{1ULL,2ULL,3ULL,4ULL,5ULL,6ULL,7ULL,8ULL,32ULL,33ULL,34ULL,35ULL,36ULL,37ULL,38ULL,39ULL,40ULL,41ULL,42ULL}){
  std::atomic<U> object{};U result{},start=d5ao_now();
  for(unsigned i=0;i<4096;++i)check(D5AN_counter_next(&object,id,1,&result));U after_next=d5ao_now();
  for(unsigned i=0;i<4096;++i)check(D5AN_counter_leave(&object,id,12));U end=d5ao_now();check(object==0);
  if(!first)latency+=",";first=false;
  latency+="{\"id\":"+std::to_string(id)+",\"operations\":4096,\"next_ticks\":"+std::to_string(after_next-start)+",\"leave_ticks\":"+std::to_string(end-after_next)+"}";
 }
 latency+="]";
 // End-to-end paths include actual C++ producer and assembly bridge calls.
 // Drain between finite batches to distinguish healthy latency from overload.
 // Native operations group multiple sites; no individual bridge duration is
 // inferred by subtraction from an independently scheduled reference run.
 std::string paths="[";first=true;
 for(unsigned repeat=0;repeat<20;++repeat){
  U start=d5ao_now();for(unsigned i=0;i<16;++i){scheduler::Producer p;check(p.admitted);}U cpp=d5ao_now();
  for(unsigned i=0;i<16;++i){causal::Producer p;check(p.admitted);}U causal_cpp=d5ao_now();
  for(unsigned i=0;i<16;++i){
   ((void(*)(U))d5am_private)(lock);
   ((void(*)(U,U))(d5am_private+1024))(lock+4,0xffffffff);
  }U reader=d5ao_now();
  for(unsigned i=0;i<16;++i){
   ((void(*)(U))(d5am_private+1216))(lock);
   ((void(*)(U))(d5am_private+1216))(lock);
   ((void(*)(U))(d5am_private+512))(lock);
   ((void(*)(U))(d5am_private+512))(lock);
  }U writer=d5ao_now();
  if(!first)paths+=",";first=false;
  paths+="{\"repeat\":"+std::to_string(repeat)+",\"operations\":16,\"scheduler_producer_ticks\":"+std::to_string(cpp-start)+",\"causal_producer_ticks\":"+std::to_string(causal_cpp-cpp)+",\"reader_release_ticks\":"+std::to_string(reader-causal_cpp)+",\"writer_recursive_release_ticks\":"+std::to_string(writer-reader)+"}";
  Sleep(2);
 }
 paths+="]";
 check(!scheduler::failed&&!causal::failed&&!D5AM_sched_counter_faults&&!D5AM_causal_counter_faults);
 check(sor::write_new(session/L"sensitivity.json","{\"schema\":\"sor-d5ao-sensitivity/1\",\"frequency\":"+std::to_string(hz)+",\"rows\":"+rows+",\"latency\":"+latency+",\"paths\":"+paths+",\"real_reader_writer\":true,\"reader_writer_wait_calls\":"+std::to_string(wait_calls)+",\"reader_writer_pending_bits\":"+std::to_string(pending)+"}\n"));
}
}
