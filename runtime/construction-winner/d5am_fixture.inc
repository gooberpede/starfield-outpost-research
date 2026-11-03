// SPDX-License-Identifier: GPL-3.0-or-later
// Admitted disposable host only. Original lock instructions run on private pages;
// imported waits/wakes are explicit controlled substitutions, not OS fairness.
#include "d5am_native.generated.h"
namespace {
using winner::U;
unsigned char* d5am_private{};
U d5am_fixture_lock{};
bool d5am_provider_link{};
thread_local U d5am_provider_held{};
std::atomic<U> d5am_waits{},d5am_wakes{};
LONG CALLBACK d5am_private_fault(EXCEPTION_POINTERS* fault){
 auto* c=fault->ContextRecord;
 std::string s="{\"code\":"+std::to_string(fault->ExceptionRecord->ExceptionCode)+",\"rip\":"+std::to_string(c->Rip)+",\"rsp\":"+std::to_string(c->Rsp)+",\"rax\":"+std::to_string(c->Rax)+",\"rcx\":"+std::to_string(c->Rcx)+",\"r14\":"+std::to_string(c->R14)+",\"rdi\":"+std::to_string(c->Rdi)+",\"private_page\":"+std::to_string(U(d5am_private))+"}\n";
 sor::write_new(winner::session/L"d5am-private-fault.json",s);return EXCEPTION_CONTINUE_SEARCH;
}
void d5am_stage(const char* text){
 auto path=winner::session/L"d5am-native-stages.txt";
 HANDLE h=CreateFileW(path.c_str(),FILE_APPEND_DATA,FILE_SHARE_READ,nullptr,OPEN_ALWAYS,FILE_ATTRIBUTE_NORMAL,nullptr);check(h!=INVALID_HANDLE_VALUE);
 DWORD n{};check(WriteFile(h,text,DWORD(strlen(text)),&n,nullptr)&&n==strlen(text));check(FlushFileBuffers(h));CloseHandle(h);
}
void d5am_enable_provider(bool enabled){d5am_provider_link=enabled;}
void d5am_fixture_shared_phase(U proc){
 if(!d5am_provider_link)return;winner::PreserveError preserve;
 ((void(*)(U))d5am_private)(proc+0x40);
 ((void(*)(U,U))(d5am_private+1024))(proc+0x44,0xffffffff);
}
void d5am_fixture_writer(U proc){
 if(!d5am_provider_link)return;winner::PreserveError preserve;check(!d5am_provider_held);
 ((void(*)(U))(d5am_private+1216))(proc+0x40);d5am_provider_held=proc+0x40;
}
void d5am_fixture_finish(){
 if(!d5am_provider_link||!d5am_provider_held)return;winner::PreserveError preserve;
 ((void(*)(U))(d5am_private+512))(d5am_provider_held);d5am_provider_held=0;
}
bool d5am_fixture_geometry_acquire(U lock){
 if(!d5am_provider_link)return false;winner::PreserveError preserve;
 ((void(*)(U))d5am_private)(lock);return true;
}
void d5am_fixture_geometry_release(U proc){
 if(!d5am_provider_link)return;winner::PreserveError preserve;
 ((void(*)(U,U))(d5am_private+1152))(proc+0x44,0xffffffff);
}
BOOL WINAPI d5am_wait(void* address,void*,SIZE_T size,DWORD timeout){
 check(U(address)==d5am_fixture_lock+4&&size==4&&timeout==INFINITE);++d5am_waits;
 *(DWORD*)d5am_fixture_lock=0;
 InterlockedExchangeAdd((volatile LONG*)(d5am_fixture_lock+4),-0x401000);
 return TRUE;
}
void WINAPI d5am_wake(void* address){check(U(address)==d5am_fixture_lock+4);++d5am_wakes;}
void d5am_setup_native(){
 using namespace winner;
 check(AddVectoredExceptionHandler(1,d5am_private_fault)!=nullptr);
 d5am_private=(unsigned char*)VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(d5am_private!=nullptr);
 memset(d5am_private,0x90,4096);
 const unsigned char* code[]{d5am_original_reader,d5am_original_writer,d5am_original_release};
 const unsigned sizes[]{126,216,81},offsets[]{0,256,512};
 const U vas[]{0x1422cc350,0x1422cc3d0,0x1402c45a0};unsigned slot=2048;
 for(unsigned j=0;j<3;++j){
  auto* p=d5am_private+offsets[j];memcpy(p,code[j],sizes[j]);
  for(unsigned i=0;i+5<sizes[j];++i)if(p[i]==0xff&&(p[i+1]==0x15||p[i+1]==0x25)){
   int32_t displacement{};memcpy(&displacement,p+i+2,4);U target=vas[j]+i+6+displacement,value{};
   if(target==0x143a3f418)value=U(&GetCurrentThreadId);
   else if(target==0x143a402d0)value=U(&d5am_wait);
   else if(target==0x143a402c8||target==0x143a402d8)value=U(&d5am_wake);
   else check(false);
   memcpy(d5am_private+slot,&value,8);int32_t relative=int32_t(slot-(offsets[j]+i+6));memcpy(p+i+2,&relative,4);slot+=8;i+=5;
  }
 }
 for(unsigned offset:{1024,1088,1152,1280,1344,1408}){
  const unsigned char release[]{0x48,0x83,0xec,0x28,0xf0,0x0f,0xc1,0x11,0x8b,0xc2,0x48,0x83,0xc4,0x28,0xc3};memcpy(d5am_private+offset,release,sizeof release);
 }
 const unsigned char call_stub[]{0x48,0x83,0xec,0x28,0xe8,0,0,0,0,0x48,0x83,0xc4,0x28,0xc3};memcpy(d5am_private+1216,call_stub,sizeof call_stub);
 int32_t target=256-(1220+5);memcpy(d5am_private+1221,&target,4);
 for(unsigned j=0;j<2;++j){
  unsigned char inline_release[]{0x57,0x48,0x83,0xec,0x20,0x48,0x8b,0xf9,0xb9,0x00,0xf0,0xbf,0xff,0xf0,0x0f,0xc1,0x4f,0x04,0x8b,0xc1,0x48,0x83,0xc4,0x20,0x5f,0xc3};
  if(j){inline_release[10]=0;inline_release[11]=0xc0;}
  memcpy(d5am_private+1472+j*64,inline_release,sizeof inline_release);
 }
 U locations[]{U(d5am_private+320),U(d5am_private+447),U(d5am_private+290),U(d5am_private+22),
  U(d5am_private+546),U(d5am_private+583),U(d5am_private+1028),U(d5am_private+1092),
  U(d5am_private+1156),U(d5am_private+1220),U(d5am_private+115),
  U(d5am_private+1284),U(d5am_private+1348),U(d5am_private+1412),U(d5am_private+1485),U(d5am_private+1549)};
 std::string hashes[causal::site_count];const char* text[causal::site_count]{};
 for(unsigned i=0;i<causal::site_count;++i){hashes[i]=sor::sha_bytes((void*)locations[i],32);text[i]=hashes[i].c_str();}
 std::string body_hashes[3];const char* body_text[3]{};const unsigned starts[]{0,256,512},lengths[]{126,216,81};
 for(unsigned i=0;i<3;++i){body_hashes[i]=sor::sha_bytes(d5am_private+starts[i],lengths[i]);body_text[i]=body_hashes[i].c_str();}
 check(causal::configure(locations,text,body_text));
 DWORD old{};check(VirtualProtect(d5am_private,4096,PAGE_EXECUTE_READ,&old));check(FlushInstructionCache(GetCurrentProcess(),d5am_private,4096));
}
void d5am_publish_crossing(U receiver,U kind){
 check(kind==winner::causal::Reader);
 D5AM_causal_fixture_before_operation=0;
 winner::causal::register_owner(receiver-4-0x40);
}
void d5am_run_native(U proc){
 using namespace winner;
 d5am_stage("begin\n");
 auto lock=proc+0x40;d5am_fixture_lock=lock;auto* words=(uint32_t*)lock;check(words[0]==0&&words[1]==0);
 causal::lifecycle(proc,causal::Retire);
 D5AM_causal_fixture_before_operation=U(&d5am_publish_crossing);
 ((void(*)(U))d5am_private)(lock);
 check(!D5AM_causal_fixture_before_operation&&D5AM_watched_lock.load()==lock&&words[1]==1);
 ((void(*)(U,U))(d5am_private+1024))(lock+4,0xffffffff);
 check(words[1]==0&&causal::uncertain.load()>0);
 d5am_stage("watch-published-between-native-snapshot-and-atomic-emits-old-lifetime-uncertainty\n");
 causal::register_owner(proc);
 auto reader=(void(*)(U))(d5am_private);
 auto writer=(void(*)(U))(d5am_private+1216);
 auto release=(void(*)(U))(d5am_private+512);
 auto read_release=[&](unsigned offset){((void(*)(U,U))(d5am_private+offset))(lock+4,0xffffffff);};
 reader(lock);d5am_stage("reader\n");check(words[1]==1);read_release(1024);d5am_stage("reader-release\n");check(words[1]==0);
 reader(lock);reader(lock);reader(lock);check(words[1]==3);
 read_release(1024);read_release(1088);read_release(1152);check(words[1]==0);
 for(unsigned offset:{1280,1344,1408}){reader(lock);read_release(offset);check(words[1]==0);}
 d5am_stage("reader-six-sites\n");
 writer(lock);check(words[0]==GetCurrentThreadId()&&words[1]==0x401000);
 writer(lock);check(words[1]==0x801000);release(lock);check(words[1]==0x401000);release(lock);check(words[0]==0&&words[1]==0);
 writer(lock);words[0]=0;((void(*)(U))(d5am_private+1472))(lock);check(words[1]==0);
 writer(lock);writer(lock);((void(*)(U))(d5am_private+1536))(lock);check(words[1]==0x401000);release(lock);check(words[0]==0&&words[1]==0);
 d5am_stage("writer-recursion-and-inline-map-mutator-releases\n");
 // Positively exercise an unscoped same-owner native user, independent of
 // provider TLS, then a foreign lock that must execute without a callback.
 uint32_t foreign[2]{};reader(U(foreign));check(foreign[1]==1);
 ((void(*)(U,U))(d5am_private+1024))(U(foreign)+4,0xffffffff);check(foreign[1]==0);
 d5am_stage("foreign-lock\n");
 // The wait import models a foreign final release; its substituted transition
 // is an explicit negative-control gap, not a complete retail lock history.
 words[0]=GetCurrentThreadId()^0x80000000u;words[1]=0x401000;
 writer(lock);check(d5am_waits==1&&words[0]==GetCurrentThreadId());release(lock);check(words[1]==0);
 d5am_stage("wait\n");
 // A has already registered and published Pending when B approaches. The
 // declared observer hold allows B's later non-ticket writer to acquire first.
 causal::fixture_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 causal::fixture_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(causal::fixture_entered&&causal::fixture_resume);
 causal::fixture_hold_after_emit=true;std::atomic<U> winner{};U a_thread{},b_thread=GetCurrentThreadId();
 std::thread delayed([&]{a_thread=GetCurrentThreadId();causal::fixture_hold_thread=a_thread;writer(lock);U zero=0;winner.compare_exchange_strong(zero,a_thread);release(lock);});
 check(WaitForSingleObject(causal::fixture_entered,10000)==WAIT_OBJECT_0);
 writer(lock);U zero=0;winner.compare_exchange_strong(zero,b_thread);release(lock);check(winner==b_thread);
 check(SetEvent(causal::fixture_resume));delayed.join();check(words[1]==0&&a_thread!=b_thread);
 causal::fixture_hold_thread=0;causal::fixture_hold_after_emit=false;
 CloseHandle(causal::fixture_entered);CloseHandle(causal::fixture_resume);causal::fixture_entered=nullptr;causal::fixture_resume=nullptr;
 d5am_stage("registered-earlier-loses-after-declared-probe-delay\n");
 // Hold the actual pending bridge after its atomic and native generation
 // snapshot. Retire/re-register equal address while the callback is paused.
 causal::fixture_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 causal::fixture_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(causal::fixture_entered&&causal::fixture_resume);
 U old_generation=D5AM_generation.load();
 std::thread paused([&]{causal::fixture_hold_thread=GetCurrentThreadId();writer(lock);release(lock);});
 check(WaitForSingleObject(causal::fixture_entered,10000)==WAIT_OBJECT_0);
 causal::lifecycle(proc,causal::Retire);causal::register_owner(proc);check(D5AM_generation.load()!=old_generation);
 check(SetEvent(causal::fixture_resume));paused.join();causal::fixture_hold_thread=0;
 CloseHandle(causal::fixture_entered);CloseHandle(causal::fixture_resume);causal::fixture_entered=nullptr;causal::fixture_resume=nullptr;
 check(causal::uncertain.load()>0&&causal::baseline_unknown.load()>0&&words[1]==0);
 d5am_stage("aba\n");
 check(causal::guards());
}
void d5am_run_counter_faults(){
 using namespace winner;
 std::atomic<U>* counters[]{&causal::tokens,&D5AM_registry_serial,&causal::uncertain,
  &causal::baseline_unknown,&causal::multiowner,&causal::drops,&causal::reentrant,&causal::active,&winner::active};
 for(auto* value:counters){
  U saved=value->exchange(UINT64_MAX);check(!causal::bump(*value));check(value->load()==UINT64_MAX);
  value->store(saved); // Explicit private fault-fixture restoration, not retail recovery.
  check(causal::counter_overflow.load()&&causal::failed.load());
 }
 check(causal::active==0&&winner::active==0);
 d5am_stage("nine-saturating-counter-faults-retain-overflow-failure\n");
}
void d5am_run_loss_faults(U proc){
 using namespace winner;
 causal::fixture_worker_held=false;causal::fixture_drain_hold=true;
 for(unsigned i=0;i<10000&&!causal::fixture_worker_held.load();++i)Sleep(1);
 check(causal::fixture_worker_held.load());
 U admitted=causal::enqueue.load()-causal::dequeue.load(),before=causal::drops.load();
 for(U i=admitted;i<=causal::capacity;++i)causal::emit(causal::event(causal::VisitedDone,proc+0x40));
 check(causal::drops.load()==before+1&&causal::enqueue.load()-causal::dequeue.load()==causal::capacity);
 causal::recording=true;check(!causal::emit(causal::event(causal::VisitedDone,proc+0x40)));causal::recording=false;
 check(causal::reentrant.load()==1&&causal::drops.load()==before+2&&causal::failed.load());
 causal::fixture_drain_hold=false;
 for(unsigned i=0;i<10000&&causal::written.load()!=causal::enqueue.load();++i)Sleep(1);
 check(causal::written.load()==causal::enqueue.load());
 d5am_stage("queue-saturation-and-reentrancy-accounted-with-worker-quiescence\n");
}
HANDLE d5am_admission_entered{},d5am_admission_resume{};
std::atomic<U> d5am_admission_thread{};
void d5am_pause_before_admission(U,U){
 if(d5am_admission_thread.load()!=GetCurrentThreadId())return;
 check(winner::causal::active.load()==0&&D5AM_causal_bridge_active.load()==0);
 check(SetEvent(d5am_admission_entered));check(WaitForSingleObject(d5am_admission_resume,180000)==WAIT_OBJECT_0);
}
void d5am_run_stop_fault(U proc,HANDLE worker){
 using namespace winner;U lock=proc+0x40;d5am_fixture_lock=lock;
 d5am_admission_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);d5am_admission_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 check(d5am_admission_entered&&d5am_admission_resume);D5AM_causal_fixture_before_admission=U(&d5am_pause_before_admission);
 std::thread late([&]{d5am_admission_thread=GetCurrentThreadId();((void(*)(U))d5am_private)(lock);((void(*)(U,U))(d5am_private+1024))(lock+4,0xffffffff);});
 check(WaitForSingleObject(d5am_admission_entered,60000)==WAIT_OBJECT_0);
 causal::fixture_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);causal::fixture_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 check(causal::fixture_entered&&causal::fixture_resume);causal::fixture_hold_after_emit=false;
 std::thread producer([&]{causal::fixture_hold_thread=GetCurrentThreadId();((void(*)(U))(d5am_private+256))(lock);((void(*)(U))(d5am_private+512))(lock);});
 check(WaitForSingleObject(causal::fixture_entered,10000)==WAIT_OBJECT_0);check(causal::active.load()==0&&D5AM_causal_bridge_active.load()>0&&active.load()>0);
 check(sor::write_new(session/L"STOP","Owned STOP with admitted D5AM native producer\n"));
 for(unsigned i=0;i<10000&&enabled.load();++i)Sleep(1);check(!enabled.load());
 check(WaitForSingleObject(worker,0)==WAIT_TIMEOUT);
 U before_resume=causal::enqueue.load();
 check(SetEvent(causal::fixture_resume));producer.join();
 DWORD terminal_wait=WaitForSingleObject(worker,60000);
 d5am_stage(("stop-resume wait="+std::to_string(terminal_wait)+" before="+std::to_string(before_resume)+" after="+std::to_string(causal::enqueue.load())+"\n").c_str());
 check(terminal_wait==WAIT_OBJECT_0);check(causal::enqueue.load()>before_resume);
 U count=causal::enqueue.load();check(SetEvent(d5am_admission_resume));late.join();
 check(causal::enqueue.load()==count&&D5AM_causal_bridge_active.load()==0&&active.load()==0&&((uint32_t*)lock)[1]==0);
 D5AM_causal_fixture_before_admission=0;d5am_admission_thread=0;CloseHandle(d5am_admission_entered);CloseHandle(d5am_admission_resume);d5am_admission_entered=nullptr;d5am_admission_resume=nullptr;
 d5am_stage("stop-terminal-precedes-late-native-admission-without-postterminal-enqueue\n");
 causal::capture(lock,0,causal::Pending,D5AM_generation.load(),D5AM_registry_serial.load(),U(d5am_private+320));
 check(causal::enqueue.load()==count&&causal::active.load()==0&&active.load()==0);
 causal::fixture_hold_thread=0;CloseHandle(causal::fixture_entered);CloseHandle(causal::fixture_resume);causal::fixture_entered=nullptr;causal::fixture_resume=nullptr;
 d5am_stage("owned-stop-waits-admitted-native-producer-then-remains-inert\n");
}
void d5am_run_owner_scope(U proc){
 using namespace winner;
 alignas(16) unsigned char second_proc[0x140]{};U before=causal::multiowner.load();
 check(!causal::failed.load()&&!broken.load());causal::register_owner(U(second_proc));
 check(causal::multiowner.load()==before+1&&D5AM_watched_lock.load()==proc+0x40&&!causal::failed.load()&&!broken.load());
 Event ready{};ready.kind=Ready;ready.epoch=epoch;check(emit(ready));wait_durable();
 causal::lifecycle(proc,causal::Retire);before=causal::baseline_unknown.load();
 causal::register_owner(0x10000); // Deliberately inaccessible private-host input.
 check(causal::baseline_unknown.load()>before&&!causal::failed.load()&&!broken.load());
 ready.kind=Ready;check(emit(ready));wait_durable();
 d5am_stage("second-owner-and-unreadable-baseline-refuse-scope-with-healthy-byte-recorder\n");
}
void d5am_run_body_guard(HANDLE worker){
 using namespace winner;
 check(causal::guards());DWORD old{},unused{};
 check(VirtualProtect(d5am_private,4096,PAGE_EXECUTE_READWRITE,&old));
 unsigned char original=d5am_private[0];d5am_private[0]^=1;
 check(VirtualProtect(d5am_private,4096,old,&unused));check(FlushInstructionCache(GetCurrentProcess(),d5am_private,4096));
 // Never execute the modified helper. The actual worker must reject a changed
 // unhooked byte through its full-body guard and persist the protective failure.
 check(!causal::guards());check(WaitForSingleObject(worker,10000)==WAIT_OBJECT_0);
 check(broken.load()&&!enabled.load());
 check(VirtualProtect(d5am_private,4096,PAGE_EXECUTE_READWRITE,&old));d5am_private[0]=original;
 check(VirtualProtect(d5am_private,4096,old,&unused));check(FlushInstructionCache(GetCurrentProcess(),d5am_private,4096));
 check(causal::guards());
 d5am_stage("unhooked-helper-byte-mismatch-protective-worker-stop-retained\n");
}
}
extern "C" void d5am_fixture_provider_finish(){d5am_fixture_finish();}

namespace {
void d5am_run_operand_fault(U proc){
 using namespace winner;U lock=proc+0x40;auto* words=(uint32_t*)lock;
 check(!causal::failed.load()&&words[0]==0&&words[1]==0);
 ((void(*)(U))(d5am_private+1216))(lock);words[0]=0; // Exact original pre-release owner-clear effect on this owned object.
 DWORD old{};check(VirtualProtect(d5am_private,4096,PAGE_EXECUTE_READWRITE,&old));
 uint32_t expected=0xffbff000,wrong=0xffffffff;check(!memcmp(d5am_private+1481,&expected,4));
 memcpy(d5am_private+1481,&wrong,4);check(FlushInstructionCache(GetCurrentProcess(),d5am_private,4096));
 ((void(*)(U))(d5am_private+1472))(lock);
 check(words[1]==0x400fff&&causal::failed.load());
 memcpy(d5am_private+1481,&expected,4);DWORD ignored{};check(VirtualProtect(d5am_private,4096,old,&ignored));
 check(FlushInstructionCache(GetCurrentProcess(),d5am_private,4096));
 d5am_stage("owned-wrong-input-delta-executed-once-recorded-and-refused-sticky-failure\n");
 // Deliberately invalid owned lock is discarded at process exit; no retail recovery or later engine use.
}
}
