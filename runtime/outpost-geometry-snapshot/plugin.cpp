// SPDX-License-Identifier: GPL-3.0-or-later
// Offline candidate only. Seven startup owner/source sites; no consumer hook.
// No generator/scheduler/lock/console-initializer hook exists.
#include "hooks.h"
#include "capture.h"
#include "writer.h"
#include "qualification.h"
#include "startup.h"
#include "startup_fixture.h"
#include "startup_stack.h"
#include "lifecycle_ranges.h"
#include "lifecycle_gate.h"
#include "direct_reader.h"
#include "lifecycle_fixture.h"
#include "source_lifetime_fixture.h"
#include "identity.generated.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include <memory>
#include <fstream>
#include <mutex>
#include <intrin.h>

extern "C" {uint64_t d5ar_callback_original{},d5ar_area_callback_original{},d5ar_area_dispatch{},d5ar_selection_release_original{},d5ar_source_free_original{};void d5ar_callback_bridge();void d5ar_area_callback_bridge();void d5ar_area_entry_bridge();void d5ar_selection_release_bridge();void d5ar_source_free_bridge();}
extern "C" void d5ar_capture_callback(uint64_t,uint64_t,uint64_t,uint64_t);
namespace d5ar {
using Four=uint64_t(*)(uint64_t,uint64_t,uint64_t,uint64_t);
using Area=uint64_t(*)(uint64_t,uint64_t,float,float);
inline Hook hooks[7];inline Four destructor_original{},point_original{},initializer_original{},installer_original{},reset_original{},manager_destructor_original{},operation_original{};inline Area area_original{};
inline std::array<std::string,7> relay_hashes{};inline bool patches_live{};
// Only the identity-guarded fixture can select the historical callback path.
inline bool direct_capture=true;
// Intentionally retained until OS process teardown; no static destructor races hooks.
inline SourceRecorder& source_recorder=*new SourceRecorder;
inline std::atomic<uint64_t> epoch{1},hazards{},operation_sequence{};
inline LifecycleGate lifecycle_gate(epoch,hazards);inline std::atomic<uint64_t> last_copy_reads{};inline std::atomic<bool> lifetime_phase_failed{};
enum State:unsigned {Idle,Armed,Copying,Owned,Writing};
// Claim a phase and its command identity in one atomic operation. A native
// scope may outlive another scope's completed copy and a subsequent command.
struct CaptureState {
 std::atomic<uint64_t> word{};
 static uint64_t pack(uint64_t generation,State phase){return (generation<<3)|phase;}
 State load()const{return State(word.load()&7);}
 uint64_t generation()const{return word.load()>>3;}
 operator State()const{return load();}
 void operator=(State phase){word.store(pack(generation(),phase));}
 bool at(uint64_t generation,State phase)const{return word.load()==pack(generation,phase);}
 bool claim(uint64_t generation,State from,State to){auto expected=pack(generation,from);return word.compare_exchange_strong(expected,pack(generation,to));}
 bool advance(){auto value=word.load();if((value>>3)==(UINT64_MAX>>3))return false;return word.compare_exchange_strong(value,value+8);}
};
inline CaptureState state;inline std::atomic<bool> ready{},broken{},registered{},capture_cancelled{};inline std::atomic<unsigned> cancel_reason{};
inline uint64_t module_base{},memory_budget{};inline HANDLE completed{},active_worker{};inline SFSETaskInterface* tasks{};
inline SRWLOCK command_admission=SRWLOCK_INIT;
inline HANDLE offline_command_entered{},offline_command_resume{};
inline HANDLE registration_worker{};inline uint64_t registration_started{};
inline std::atomic<HANDLE> registration_wait{};
inline std::atomic<bool> registration_service_exited{},registration_task_done{},registration_wait_cleanup{},registration_wait_callback_done{},ready_announced{},ready_published{};
inline StackAdmission admission_stack{};inline bool admission_stack_observed{};
inline Metadata metadata;inline std::filesystem::path output_directory;inline std::unique_ptr<Capture> pending;
inline std::filesystem::path config_path,self_module_path;inline std::string config_hash;
inline thread_local uint64_t current_point{},scope_epoch{},scope_hazards{},scope_command{};inline thread_local unsigned point_depth{},area_depth{};inline thread_local bool captured_here{};
inline thread_local OwnedOperation entry_operation{},active_operation{};
inline thread_local SelectedLease selected_scope{},entry_selected{},active_selected{};inline thread_local unsigned selected_depth{};
inline thread_local bool selected_established{},entry_area_eligible{};
inline thread_local uint64_t entry_operation_epoch{},entry_operation_hazards{};
inline uint64_t increment_epoch(){auto value=epoch.fetch_add(1);if(value==UINT64_MAX){broken=true;ready=false;}return value;}
inline uint64_t precise_filetime(){FILETIME value{};GetSystemTimePreciseAsFileTime(&value);return (uint64_t(value.dwHighDateTime)<<32)|value.dwLowDateTime;}
inline bool runtime_guards(){
 for(const auto& site:site_guards){
  uint8_t bytes[216]{};if(site.size>sizeof bytes||!checked_read(nullptr,module_base+site.rva,bytes,site.size))return false;
  for(size_t i=0;i<std::size(hooks);++i)if(reinterpret_cast<uint64_t>(hooks[i].at)==module_base+site.rva){
   if(std::memcmp(bytes,hooks[i].after,hooks[i].length)||sha_bytes(hooks[i].page,4096)!=relay_hashes[i])return false;
   std::memcpy(bytes,hooks[i].before,hooks[i].length);
  }
  if(sha_bytes(bytes,site.size)!=site.hash)return false;
 }return true;
}
inline std::string path_diagnostic(const std::filesystem::path& path){auto bytes=path.u8string();return std::string(reinterpret_cast<const char*>(bytes.data()),bytes.size());}
inline void debug_status(const std::string& message){OutputDebugStringA(("SorOutpostGeometrySnapshot: "+message+"\n").c_str());}
inline void console_status(const std::string& message){
 uint64_t console{};if(!module_base||!checked_read(nullptr,module_base+0x61df7a0,&console,8)||!console){debug_status(message);return;}
 auto print=reinterpret_cast<void(*)(uint64_t,const char*,...)>(module_base+0x1eaa950);
 print(console,"SorOutpostGeometrySnapshot: %s",message.c_str());
}
inline void feedback(const std::string& text){
 // SFSE task execution is not assumed to be a unique UI/main thread.
 // Owned file results and this debugger diagnostic carry worker completion.
 debug_status(text);
}
inline int startup_stop(void*);
inline void run_direct_attempt();
inline const char* direct_publication_check(bool before_rename);
inline const char* cancelled_status(){switch(cancel_reason.load()){case 1:return "OPERATOR_STOP";case 2:return "DISK_QUERY_OR_FLOOR_FAILED";default:return "CONTROL_QUERY_FAILED";}}
inline DWORD WINAPI worker(void*){
 try{
 if(direct_capture){
  // Command setup and console response finish before the worker can claim.
  AcquireSRWLockShared(&command_admission);
  const auto generation=state.generation();
  const auto owns=state.claim(generation,Armed,Copying);
  ReleaseSRWLockShared(&command_admission);
  if(owns){run_direct_attempt();state=Owned;}
  else if(!state.at(generation,Owned)){broken=true;ready=false;return 1;}
 }else{
 for(;;){
  auto wait=WaitForSingleObject(completed,250);if(wait==WAIT_OBJECT_0)break;
  if(wait!=WAIT_TIMEOUT){broken=true;feedback("WORKER_WAIT_FAILED");return 1;}
  if(lifecycle_gate.faulted()){
   if(state.claim(state.generation(),Armed,Copying)){
    pending->status=lifetime_phase_failed?"LIFECYCLE_PHASE_EXCEPTION":"LIFECYCLE_PROTECTION_DISABLED";
    state=Owned;if(!SetEvent(completed))return 1;
   }
  }
  auto stop=startup_stop(nullptr);if(stop||!disk_floors()){
   cancel_reason=stop>0?1:stop<0?3:2;capture_cancelled=true;broken=true;ready=false;
   if(state.claim(state.generation(),Armed,Copying)){pending->status=cancelled_status();state=Owned;if(!SetEvent(completed))return 1;}
  }
 }
 }
 state=Writing;
 try{
  if(!pending){broken=true;feedback("NO_OWNED_CAPTURE");state=Idle;return 1;}
  if(capture_cancelled&&cancel_reason.load())pending->status=cancelled_status();
  auto publication=publish_snapshot(*pending,metadata,output_directory,
    direct_capture&&pending->status!="OPERATOR_STOP"?direct_publication_check:nullptr);
  auto protected_refusal=pending->status!="COPIED_UNQUALIFIED"&&pending->status!="NO_FRESH_RESIDENT_CALLBACK"&&pending->status!="NO_ESTABLISHED_RESIDENT_CONSUMER"&&pending->status!="LIFECYCLE_COPY_NOT_ADMITTED"&&pending->status!="CURRENT_BINDING_NOT_ADMITTED"&&pending->status!="NATIVE_READER_BUSY"&&pending->status!="NO_CURRENT_OWNER"&&pending->status!="NO_ATTACHED_PROCGEN"&&pending->status!="NO_RESIDENT_HOLDERS";
  feedback(publication.status+" capture="+metadata.capture_id+" path="+path_diagnostic(publication.path));
  pending.reset();if(!publication.success||protected_refusal)broken=true;
 }catch(...){broken=true;feedback("WORKER_EXCEPTION");}
 state=Idle;return broken?1:0;
 }catch(...){broken=true;ready=false;capture_cancelled=true;OutputDebugStringA("SorOutpostGeometrySnapshot: WORKER_EXCEPTION\n");return 1;}
}
inline uint64_t phase_hook(Four original,uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 auto error=GetLastError();
 auto admission=lifecycle_gate.admit_phase();
 if(admission==LifecycleGate::Phase::SelfUpgrade){
  broken=true;ready=false;SetLastError(error);
  // Unsupported current-thread shared-to-phase upgrade: abort before mutation.
  RaiseException(0xe0424447,0,0,nullptr);return 0;
 }
 if(admission==LifecycleGate::Phase::Inert){broken=true;ready=false;SetLastError(error);return original(a,b,c,d);}
 uint64_t result{};SetLastError(error);
 __try{result=original(a,b,c,d);error=GetLastError();}
 __finally{
  if(AbnormalTermination()){error=GetLastError();lifetime_phase_failed=true;broken=true;ready=false;lifecycle_gate.disable_copying();}
  lifecycle_gate.phase_end();SetLastError(error);
 }
 return result;
}
inline uint64_t destroy_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return phase_hook(destructor_original,a,b,c,d);}
inline uint64_t initializer_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return phase_hook(initializer_original,a,b,c,d);}
inline uint64_t installer_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return phase_hook(installer_original,a,b,c,d);}
inline uint64_t reset_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return phase_hook(reset_original,a,b,c,d);}
inline uint64_t manager_destructor_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return phase_hook(manager_destructor_original,a,b,c,d);}
inline bool lifecycle_ancestor(void* base,uint64_t pc){
 auto image=reinterpret_cast<uint64_t>(base);if(pc<image)return false;auto rva=pc-image;
 for(const auto& range:lifecycle_ranges)if(rva>=range.begin&&rva<range.end)return true;return false;
}
inline void finish_scope(bool abnormal,uint64_t proc,const OwnedOperation* operation)noexcept{
 try{
  if(!captured_here){
   if(state.claim(scope_command,Armed,Copying)){
    captured_here=true;
    pending->status=abnormal?"CONSUMER_EXCEPTION":"NO_FRESH_RESIDENT_CALLBACK";pending->proc=proc;pending->epoch_begin=scope_epoch;pending->epoch_end=epoch.load();
    if(operation){pending->operation=*operation;pending->selected_reference=active_selected;}captured_here=true;
   }
  }
  if(captured_here){
   if(abnormal){
    // Failure accounting owns only the command's identity and copied buffers.
    // No claim is made that the exceptional native unwind released its reader.
    broken=true;ready=false;if(pending){pending->status="CONSUMER_EXCEPTION";pending->holders.clear();}
    state=Owned;if(!SetEvent(completed))broken=true;
   }
   else{
    if(pending&&pending->status!="LIFECYCLE_COPY_NOT_ADMITTED"&&(scope_hazards||hazards.load()||scope_epoch!=epoch.load()))pending->status="LIFETIME_CHANGED_DURING_CONSUMER";
    if(pending&&lifetime_phase_failed)pending->status="LIFECYCLE_PHASE_EXCEPTION";
    if(pending&&capture_cancelled)pending->status=cancelled_status();
    state=Owned;if(!SetEvent(completed)){broken=true;ready=false;}
   }
  }
 }catch(...){broken=true;ready=false;if(captured_here){if(pending){pending->status="COPY_EXCEPTION";pending->holders.clear();}state=Owned;SetEvent(completed);}}
}
inline uint64_t point_hook(uint64_t proc,uint64_t query,uint64_t output,uint64_t extra){
 const auto generation=state.generation();
 if(!state.at(generation,Armed)||!ready||broken||point_depth||area_depth)return point_original(proc,query,output,extra);
 auto previous=current_point,previous_epoch=scope_epoch,previous_hazards=scope_hazards,previous_command=scope_command;auto previously_captured=captured_here;
 current_point=proc;captured_here=false;scope_epoch=epoch.load();scope_hazards=hazards.load();scope_command=generation;++point_depth;
 uint64_t result{};auto error=GetLastError();
 __try{result=point_original(proc,query,output,extra);error=GetLastError();}
 __finally{
  // The original point function has now returned through its own reader release.
  auto abnormal=AbnormalTermination()!=FALSE;if(abnormal)error=GetLastError();
  finish_scope(abnormal,proc,nullptr);
  --point_depth;current_point=previous;captured_here=previously_captured;scope_epoch=previous_epoch;scope_hazards=previous_hazards;scope_command=previous_command;
  SetLastError(error);
 }
 return result;
}
inline uint64_t nested_area_forward(uint64_t context,uint64_t query,float radius,float upper){
 ++area_depth;uint64_t result{};auto error=GetLastError();
 __try{result=area_original(context,query,radius,upper);error=GetLastError();}
 __finally{if(AbnormalTermination()!=FALSE)error=GetLastError();--area_depth;SetLastError(error);}
 return result;
}
inline uint64_t area_hook(uint64_t context,uint64_t query,float radius,float upper){
 if(area_depth&&state.load()==Armed&&ready&&!broken)return nested_area_forward(context,query,radius,upper);
 if(!state.at(selected_scope.command,Armed)||!ready||broken||point_depth||area_depth||!entry_area_eligible||selected_depth!=1||!selected_established||!selected_scope.active)return area_original(context,query,radius,upper);
 auto previously_captured=captured_here;auto previous_epoch=scope_epoch,previous_hazards=scope_hazards,previous_command=scope_command;auto previous_operation=active_operation;auto previous_selected=active_selected;
 captured_here=false;scope_epoch=entry_operation_epoch;scope_hazards=entry_operation_hazards;scope_command=selected_scope.command;active_operation=entry_operation;active_selected=entry_selected;++area_depth;uint64_t result{};auto error=GetLastError();
 __try{result=area_original(context,query,radius,upper);error=GetLastError();}
 __finally{
  auto abnormal=AbnormalTermination()!=FALSE;if(abnormal)error=GetLastError();
  finish_scope(abnormal,0,&active_operation);
  --area_depth;captured_here=previously_captured;scope_epoch=previous_epoch;scope_hazards=previous_hazards;scope_command=previous_command;active_operation=previous_operation;active_selected=previous_selected;
  SetLastError(error);
 }
 return result;
}
inline void finish_operation_selection(bool abnormal) noexcept {
 if(selected_depth!=1||!state.claim(selected_scope.command,Armed,Copying))return;
 try{pending->selected_reference=selected_scope;pending->status=abnormal?"OPERATION_EXCEPTION":!selected_established?"OPERATION_SCOPE_READ_FAILED":"NO_ESTABLISHED_RESIDENT_CONSUMER";}
 catch(...){pending->status="COPY_EXCEPTION";broken=true;ready=false;}
 if(abnormal||!selected_established){broken=true;ready=false;}state=Owned;if(!SetEvent(completed)){broken=true;ready=false;}
}
inline uint64_t operation_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 const auto generation=state.generation();
 if(!state.at(generation,Armed)||!ready||broken)return operation_original(a,b,c,d);
 auto error=GetLastError();uint8_t mode{};
 bool readable=b>=0x10000&&b<=UINT64_MAX-0x631&&checked_read(nullptr,b+0x630,&mode,1);
 if(readable&&mode&&selected_depth==0){SetLastError(error);return operation_original(a,b,c,d);}
 auto prior=selected_scope;auto depth=selected_depth;auto prior_established=selected_established;
 if(depth)selection_ambiguous(prior);
 auto invocation=operation_sequence.fetch_add(1)+1;
 if(!invocation){broken=true;ready=false;return operation_original(a,b,c,d);}
 selected_scope=begin_selection(invocation,generation,epoch.load());selected_depth=depth+1;selected_established=readable&&!mode;
 if(!readable)selected_scope.status="OPERATION_SCOPE_READ_FAILED";
 if(selected_depth!=1)selection_ambiguous(selected_scope);
 uint64_t result{};SetLastError(error);
 __try{result=operation_original(a,b,c,d);error=GetLastError();}
 __finally{
  auto abnormal=AbnormalTermination()!=FALSE;if(abnormal)error=GetLastError();finish_operation_selection(abnormal);
  end_selection(selected_scope);selected_scope=prior;selected_depth=depth;selected_established=prior_established;SetLastError(error);
 }
 return result;
}
inline bool command_admitted(float* result){
 try{
  if(result)*result=0;
  if(offline_command_entered&&(!SetEvent(offline_command_entered)||WaitForSingleObject(offline_command_resume,10000)!=WAIT_OBJECT_0))return true;
  if(!ready||broken||(patches_live&&!ready_published)){console_status("NOT_READY; no capture armed");return true;}
  if(registration_worker&&WaitForSingleObject(registration_worker,0)!=WAIT_OBJECT_0){console_status("STARTUP_REGISTRATION_STILL_ACTIVE; no capture armed");return true;}
  if(patches_live&&!runtime_guards()){ready=false;broken=true;console_status("INSTRUCTION_OR_RELAY_GUARD_FAILED");return true;}
  if(active_worker){if(WaitForSingleObject(active_worker,0)!=WAIT_OBJECT_0){console_status("WORKER_STILL_ACTIVE; no new invocation accepted");return true;}CloseHandle(active_worker);active_worker=nullptr;}
  if(!state.claim(state.generation(),Idle,Copying)){console_status("BUSY_OR_ARMED; no new invocation accepted");return true;}
  if(!disk_floors()){state=Idle;broken=true;console_status("DISK_QUERY_OR_FLOOR_FAILED");return true;}
  MEMORYSTATUSEX memory{sizeof memory};if(!GlobalMemoryStatusEx(&memory)){state=Idle;console_status("MEMORY_QUERY_FAILED");return true;}
  memory_budget=(std::min)(memory.ullAvailPhys,memory.ullAvailVirtual);
  metadata.capture_id=random_uuid();metadata.utc=precise_utc();pending=std::make_unique<Capture>();pending->status.reserve(128);capture_cancelled=false;cancel_reason=0;if(!ResetEvent(completed)){state=Idle;broken=true;console_status("EVENT_RESET_FAILED");return true;}
  if(!state.advance()){broken=true;ready=false;state=Idle;return true;}
  auto arm_message="ARMED capture="+metadata.capture_id+" output_directory="+path_diagnostic(output_directory)+
   (direct_capture?"; one worker capture attempt queued":"; waiting for established outpost initialization; remains armed until a qualifying operation or STOP");
  auto thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);
  if(!thread){state=Idle;broken=true;console_status("WORKER_CREATE_FAILED");return true;}active_worker=thread;
  state=Armed;if(result)*result=1;
  console_status(arm_message);
  return true;
 }catch(...){
  broken=true;ready=false;capture_cancelled=true;
  if(state.claim(state.generation(),Armed,Copying)){if(pending)pending->status="COPY_EXCEPTION";state=Owned;SetEvent(completed);}
  else if(!active_worker)state=Idle;
  OutputDebugStringA("SorOutpostGeometrySnapshot: COMMAND_EXCEPTION\n");return true;
 }
}
inline bool command(const void*,const char*,void*,void*,void*,void*,float* result,uint32_t*){
 // Protect the worker handle and owned setup even if native dispatch overlaps.
 // A contender never waits or calls back into the native console to report busy.
 if(!TryAcquireSRWLockExclusive(&command_admission)){
  if(result)*result=0;
  OutputDebugStringA("SorOutpostGeometrySnapshot: COMMAND_ADMISSION_BUSY; no new invocation accepted\n");
  return true;
 }
 bool accepted{};
 __try{accepted=command_admitted(result);}
 __finally{ReleaseSRWLockExclusive(&command_admission);}
 return accepted;
}
inline bool register_command(){
 if(!ready||broken||registered)return registered;
 uint8_t published{};if(!checked_read(nullptr,module_base+0x621a2d0,&published,1)||published!=1)return false;
 auto row=module_base+0x5eb1050+0x49*0x58;uint8_t bytes[0x58]{};
 if(!checked_read(nullptr,row,bytes,sizeof bytes))return false;
 uint64_t name{},execute{};uint32_t opcode{};std::memcpy(&name,bytes,8);std::memcpy(&execute,bytes+0x30,8);std::memcpy(&opcode,bytes+0x10,4);
 char label[12]{};if(!checked_read(nullptr,name,label,sizeof label)||std::memcmp(label,"GameComment",12)||opcode!=0x149||execute!=module_base+0x2b75d0||bytes[0x20]||bytes[0x38])return false;
 uint16_t parameters{};uint64_t definitions{},compiler{};std::memcpy(&parameters,bytes+0x22,2);std::memcpy(&definitions,bytes+0x28,8);std::memcpy(&compiler,bytes+0x40,8);
 if(parameters!=1||definitions!=module_base+0x590e6d0||compiler!=module_base+0xc16dd0)return false;
 for(size_t i=0x48;i<0x58;++i)if(bytes[i])return false;
 // Native constructor/publication/lookup/dispatch evidence defines these fields.
 // Publication is complete; the operator must not use the console before READY.
 static const char title[]="SORSnapshot",empty[]="",help[]="Attempt one resident geometry snapshot after ordinary arrival.";
 static const char historical_help[]="Arm snapshot for established outpost initialization; may remain pending.";
 auto ptr=[&](size_t offset,const void* value){InterlockedExchangePointer(reinterpret_cast<void* volatile*>(row+offset),const_cast<void*>(value));};
 ptr(8,empty);ptr(0x18,direct_capture?help:historical_help);ptr(0x28,nullptr);InterlockedExchange16(reinterpret_cast<volatile SHORT*>(row+0x22),0);
 ptr(0x30,reinterpret_cast<void*>(&command));ptr(0,title);registered=true;debug_status("REGISTERED SORSnapshot; no resource query performed");return true;
}
inline bool startup_receipt(const char*,uint64_t);
inline void announce_ready(){
 if(broken||!registered||!registration_service_exited||!registration_task_done||!registration_wait_cleanup)return;
 bool expected=false;if(ready_announced.compare_exchange_strong(expected,true)){
  if(!registration_worker||WaitForSingleObject(registration_worker,0)!=WAIT_OBJECT_0||!startup_receipt("COMMAND_READY",GetTickCount64()-registration_started)){ready=false;broken=true;}
  else ready_published=true;
 }
}
inline void cancel_registration_wait(){
 auto wait=registration_wait.exchange(nullptr);
 if(wait){if(UnregisterWaitEx(wait,nullptr)||GetLastError()==ERROR_IO_PENDING)registration_wait_cleanup=true;else{ready=false;broken=true;}}
}
inline VOID CALLBACK registration_service_exit(void*,BOOLEAN timed_out){
 if(timed_out||!registration_worker||WaitForSingleObject(registration_worker,0)!=WAIT_OBJECT_0){ready=false;broken=true;return;}
 registration_service_exited=true;cancel_registration_wait();registration_wait_callback_done=true;announce_ready();
}
struct RegistrationTask:SFSETaskInterface::ITaskDelegate{
 void Run()override{
  try{if(!register_command()){ready=false;broken=true;startup_receipt("CONSOLE_REGISTRATION_REFUSED",GetTickCount64()-registration_started);}
   registration_task_done=true;announce_ready();
  }catch(...){ready=false;broken=true;}
 }
 void Destroy()override{delete this;}
};
inline DWORD WINAPI wait_registration(void*);
inline bool start_registration(){
 registration_started=GetTickCount64();registration_worker=CreateThread(nullptr,0,wait_registration,nullptr,CREATE_SUSPENDED,nullptr);
 if(!registration_worker){ready=false;broken=true;return false;}
 HANDLE wait{};
 if(!RegisterWaitForSingleObject(&wait,registration_worker,registration_service_exit,nullptr,INFINITE,WT_EXECUTEONLYONCE)){ready=false;broken=true;ResumeThread(registration_worker);return false;}
 registration_wait=wait;if(ResumeThread(registration_worker)==DWORD(-1)){ready=false;broken=true;return false;}
 if(registration_wait_callback_done){cancel_registration_wait();announce_ready();}return true;
}
inline bool private_config(){
 HMODULE self{};wchar_t path[32768]{};
 if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&private_config),&self)||!GetModuleFileNameW(self,path,32768))return false;
 self_module_path=std::filesystem::path(path);config_path=self_module_path;config_path.replace_extension(L"output-path");
 std::ifstream file(config_path,std::ios::binary|std::ios::ate);auto length=file.tellg();if(!file||length<=0||length>32768)return false;
 std::string destination(size_t(length),'\0');file.seekg(0);file.read(destination.data(),length);if(!file||destination.back()!='\n')return false;
 config_hash=sha_bytes(destination.data(),destination.size());if(config_hash.size()!=64)return false;
 destination.pop_back();output_directory=std::filesystem::path(std::u8string(reinterpret_cast<const char8_t*>(destination.data()),destination.size()));
 if(!output_directory.is_absolute()||output_directory.lexically_normal()!=output_directory||!std::filesystem::is_directory(output_directory))return false;
 for(auto ancestor=output_directory;!ancestor.empty();){auto flags=GetFileAttributesW(ancestor.c_str());if(flags==INVALID_FILE_ATTRIBUTES||(flags&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto parent=ancestor.parent_path();if(parent==ancestor)break;ancestor=parent;}
 return true;
}
inline bool startup_receipt(const char* status,uint64_t wait_ms){
 if(!disk_floors())return false;
 auto utc=precise_utc(),id=random_uuid();std::string data="{\"source_history_startup_premise\":\"FRESH_PROCESS_OFFICIAL_SFSE_PRELOAD_BEFORE_ORDINARY_SOURCE_HISTORY\",\"source_address_reuse\":\"PERMANENT_REFUSAL\",\"stack_admission_observed\":"+std::string(admission_stack_observed?"true":"false")+",\"stack_admission_complete\":"+std::string(admission_stack_observed&&admission_stack.status==StackStatus::Complete?"true":"false")+",\"stack_admission_code\":"+std::to_string(unsigned(admission_stack.status))+",\"stack_frames\":"+std::to_string(admission_stack.frames)+",\"evidence_basis\":\""+metadata.evidence_basis+"\",\"schema\":\"sor-d5ar-startup/1\",\"status\":\""+std::string(status)+"\",\"session_id\":\""+metadata.session_id+"\",\"pid\":"+std::to_string(metadata.pid)+",\"creation_filetime\":"+std::to_string(metadata.creation_filetime)+",\"thread\":"+std::to_string(GetCurrentThreadId())+",\"source_lock_sha256\":\""+std::string(source_lock_hash)+"\",\"game_exe_sha256\":\""+metadata.game_exe_sha256+"\",\"sfse_sha256\":\""+metadata.sfse_sha256+"\",\"plugin_sha256\":\""+metadata.plugin_sha256+"\",\"config_sha256\":\""+config_hash+"\",\"utc\":\""+utc+"\",\"wait_ms\":"+std::to_string(wait_ms)+"}\n";
 auto partial=output_directory/("startup-"+id+".partial"),final=output_directory/("startup-"+id+".startup.json");
 HANDLE file=CreateFileW(partial.c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL|FILE_FLAG_WRITE_THROUGH,nullptr);if(file==INVALID_HANDLE_VALUE)return false;
 DWORD written{};bool ok=WriteFile(file,data.data(),DWORD(data.size()),&written,nullptr)&&written==data.size()&&FlushFileBuffers(file);bool closed=CloseHandle(file)!=FALSE;
 return ok&&closed&&sha_file(partial)==sha_bytes(data.data(),data.size())&&disk_floors()&&MoveFileExW(partial.c_str(),final.c_str(),MOVEFILE_WRITE_THROUGH);
}
inline int startup_owner(void*){uint64_t manager{};if(!checked_read(nullptr,module_base+0x5fd9c30,&manager,8))return -1;return manager?1:0;}
inline bool startup_sole(void*){return sole_thread();}
inline bool startup_disk(void*){return disk_floors();}
inline int startup_stop(void*){
 for(const auto* name:{L"STARTUP_STOP",L"STOP"}){auto flags=GetFileAttributesW((output_directory/name).c_str());if(flags!=INVALID_FILE_ATTRIBUTES)return 1;auto error=GetLastError();if(error!=ERROR_FILE_NOT_FOUND)return -1;}
 return 0;
}
inline void startup_pause(void*){Sleep(100);}
inline DWORD WINAPI wait_registration(void*){
 try{
  for(;;){
   if(broken)return 1;
   if(!disk_floors()||startup_stop(nullptr)!=0){ready=false;broken=true;startup_receipt("CONSOLE_WAIT_STOP_OR_DISK_FAILURE",GetTickCount64()-registration_started);return 1;}
   uint8_t published{};if(!checked_read(nullptr,module_base+0x621a2d0,&published,1)){ready=false;broken=true;return 1;}
   if(published==1){tasks->AddTask(new RegistrationTask());return 0;}
   if(published!=0){ready=false;broken=true;return 1;}Sleep(100);
  }
 }catch(...){ready=false;broken=true;return 1;}
}
inline bool prepare_direct_hooks(){
 if(!runtime_guards())return false;
 if(!prepare_hook(hooks[0],module_base+0x79d910,reinterpret_cast<void*>(&destroy_hook),destroy_bytes,8)||
    !prepare_hook(hooks[1],module_base+0x1881660,reinterpret_cast<void*>(&initializer_hook),initializer_bytes,-1)||
    !prepare_hook(hooks[2],module_base+0x789ce0,reinterpret_cast<void*>(&installer_hook),installer_bytes,8)||
    !prepare_hook(hooks[3],module_base+0x788e70,reinterpret_cast<void*>(&reset_hook),reset_bytes,-2)||
    !prepare_hook(hooks[4],module_base+0x788bc0,reinterpret_cast<void*>(&manager_destructor_hook),manager_destructor_bytes,8)||
    !prepare_call(hooks[5],module_base+0x982af8,reinterpret_cast<void*>(&d5ar_source_free_bridge),source_clear_free_bytes,module_base+0x365cdb0)||
    !prepare_call(hooks[6],module_base+0x982c32,reinterpret_cast<void*>(&d5ar_source_free_bridge),source_retire_free_bytes,module_base+0x365cdb0)){
  for(auto& hook:hooks)discard_prepared(hook);return false;
 }
 destructor_original=reinterpret_cast<Four>(hooks[0].original);
 initializer_original=reinterpret_cast<Four>(hooks[1].original);
 installer_original=reinterpret_cast<Four>(hooks[2].original);reset_original=reinterpret_cast<Four>(hooks[3].original);manager_destructor_original=reinterpret_cast<Four>(hooks[4].original);
 d5ar_source_free_original=reinterpret_cast<uint64_t>(hooks[5].original);
 for(size_t i=0;i<std::size(hooks);++i)relay_hashes[i]=sha_bytes(hooks[i].page,4096);
 return true;
}
inline bool initialize(const SFSEInterface* api){
 if(!api||api->interfaceVersion!=1||api->runtimeVersion!=game_version||!disk_floors())return false;
 wchar_t path[32768]{};if(!GetModuleFileNameW(nullptr,path,32768)||sha_file(path)!=expected_game)return false;
 auto game_path=std::filesystem::path(path);
 auto sfse=GetModuleHandleW(L"sfse_1_16_244.dll");if(!sfse||!GetModuleFileNameW(sfse,path,32768)||sha_file(path)!=expected_sfse)return false;
 module_base=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));
 if(!private_config())return false;metadata.session_id=random_uuid();metadata.pid=GetCurrentProcessId();
 FILETIME birth{},exit{},kernel{},user{};if(!GetProcessTimes(GetCurrentProcess(),&birth,&exit,&kernel,&user))return false;
 metadata.creation_filetime=(uint64_t(birth.dwHighDateTime)<<32)|birth.dwLowDateTime;
 metadata.game_exe_sha256=expected_game;metadata.sfse_sha256=expected_sfse;metadata.source_lock_sha256=source_lock_hash;metadata.plugin_sha256=sha_file(self_module_path);
 if(!startup_receipt("WAITING_STARTUP_ADMISSION",0))return false;auto started=GetTickCount64();
 auto admission=await_startup(nullptr,{startup_owner,startup_sole,startup_disk,startup_stop,startup_pause});
 if(admission!=StartupResult::Ready){startup_receipt("STARTUP_ADMISSION_REFUSED",GetTickCount64()-started);return false;}
 if(sha_file(game_path)!=expected_game||sha_file(config_path)!=config_hash||sha_file(std::filesystem::path(path))!=expected_sfse||startup_owner(nullptr)!=0||!disk_floors()||!sole_thread())return false;
 if(!prepare_direct_hooks())return false;
 admission_stack=startup_stack(lifecycle_ancestor,reinterpret_cast<void*>(module_base));admission_stack_observed=true;
 if(admission_stack.status!=StackStatus::Complete||startup_owner(nullptr)!=0||!sole_thread()){for(auto& hook:hooks)discard_prepared(hook);startup_receipt("LIFECYCLE_ANCESTOR_OR_STACK_UNQUALIFIED",GetTickCount64()-started);return false;}
 HMODULE pinned{};
 if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_PIN,reinterpret_cast<LPCWSTR>(&initialize),&pinned)){
  for(auto& hook:hooks)discard_prepared(hook);return false;
 }
 // Supported invocation is fresh SFSEPreload; owner-null alone is not history proof.
 source_recorder.begin(true);
 bool dirty=false;if(!install_hooks(hooks,std::size(hooks),dirty)){broken=true;patches_live=dirty;if(!dirty)for(auto& hook:hooks)discard_prepared(hook);return dirty;}
 patches_live=true;
 ready=true;if(!startup_receipt("STARTUP_HOOKS_INSTALLED",GetTickCount64()-started)){ready=false;broken=true;}return true;
}

inline HANDLE offline_copy_entered{},offline_copy_resume{};inline uint64_t offline_copy_fault_at{};inline std::atomic<bool> offline_copy_pause{};
inline bool lifecycle_read(void* context,uint64_t at,void* into,size_t size){
 auto& lease=*static_cast<LifecycleGate::Lease*>(context);
 if(offline_copy_pause.exchange(false)){SetEvent(offline_copy_entered);if(WaitForSingleObject(offline_copy_resume,10000)!=WAIT_OBJECT_0)return false;}
 if(offline_copy_fault_at&&at==offline_copy_fault_at){offline_copy_fault_at=0;destroy_hook(0,0,0,0);}
 return lifecycle_gate.read(lease,checked_read,nullptr,at,into,size);
}
inline unsigned offline_direct_case{};
inline HANDLE offline_direct_entered{},offline_direct_resume{},offline_direct_cancelled{};
inline HANDLE offline_writer_waiting{};
inline std::atomic<unsigned> offline_direct_map_reads{};
inline const char* direct_publication_check(bool before_rename){
 if(before_rename&&offline_direct_case==78){
  SetEvent(offline_direct_entered);
  if(WaitForSingleObject(offline_direct_resume,10000)!=WAIT_OBJECT_0)return "OWNED_PUBLICATION_CONTROL_TIMEOUT";
 }
 const auto stop=startup_stop(nullptr);
 return stop>0?"OPERATOR_STOP_DURING_PUBLICATION":stop<0?"CONTROL_QUERY_FAILED":nullptr;
}
inline BOOL WINAPI offline_writer_wait(volatile VOID* address,PVOID expected,SIZE_T size,DWORD timeout){
 SetEvent(offline_writer_waiting);
 return WaitOnAddress(address,expected,size,timeout);
}
inline DWORD WINAPI offline_queued_writer(void* lock){
 using NativeLock=void(*)(void*);
 reinterpret_cast<NativeLock>(module_base+0x22cc3d0)(lock);
 auto owner=static_cast<volatile LONG*>(lock);
 const bool exclusive=InterlockedCompareExchange(owner,0,0)==LONG(GetCurrentThreadId())&&
  InterlockedCompareExchange(owner+1,0,0)==0x401000;
 reinterpret_cast<NativeLock>(module_base+0x2c45a0)(lock);
 return exclusive?0:1;
}
inline bool offline_queued_writer_control(uint64_t proc,volatile LONG* word){
 const SiteGuard spans[]{{0x22cc3d0,0xd8,offline_writer_lock_hash},{0x2c45a0,0x51,offline_writer_release_hash}};
 for(const auto& span:spans){
  auto start=reinterpret_cast<void*>(module_base+span.rva);DWORD old{};
  if(sha_bytes(start,span.size)!=span.hash||!VirtualProtect(start,span.size,PAGE_EXECUTE_READ,&old)||
     !FlushInstructionCache(GetCurrentProcess(),start,span.size)){
   SetEvent(offline_direct_resume);return false;
  }
 }
 offline_writer_waiting=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 if(!offline_writer_waiting){SetEvent(offline_direct_resume);return false;}
 *reinterpret_cast<decltype(&GetCurrentThreadId)*>(module_base+0x3a3f418)=GetCurrentThreadId;
 *reinterpret_cast<decltype(&WaitOnAddress)*>(module_base+0x3a402d0)=offline_writer_wait;
 *reinterpret_cast<decltype(&WakeByAddressSingle)*>(module_base+0x3a402c8)=WakeByAddressSingle;
 *reinterpret_cast<decltype(&WakeByAddressAll)*>(module_base+0x3a402d8)=WakeByAddressAll;
 auto writer=CreateThread(nullptr,0,offline_queued_writer,reinterpret_cast<void*>(proc+0x40),0,nullptr);
 const bool queued=writer&&WaitForSingleObject(offline_writer_waiting,5000)==WAIT_OBJECT_0&&
   WaitForSingleObject(writer,100)==WAIT_TIMEOUT&&InterlockedCompareExchange(word,0,0)==0x1001;
 SetEvent(offline_direct_resume);
 DWORD result{};
 const bool joined=writer&&WaitForSingleObject(writer,5000)==WAIT_OBJECT_0;
 const bool clean=joined&&GetExitCodeThread(writer,&result)&&result==0&&
   InterlockedCompareExchange(reinterpret_cast<volatile LONG*>(proc+0x40),0,0)==0&&InterlockedCompareExchange(word,0,0)==0;
 if(writer)CloseHandle(writer);
 if(joined||!writer)CloseHandle(offline_writer_waiting);
 return queued&&clean;
}
inline bool direct_read(void* context,uint64_t at,void* into,size_t size){
 if(capture_cancelled)return false;
 if(offline_direct_case&&at==pending->proc+0x20){
  ++offline_direct_map_reads;
  if(offline_direct_case==69)throw std::runtime_error("Owned direct read fault");
  if(offline_direct_case==70)destroy_hook(0,0,0,0);
  if(offline_direct_case==79)RaiseException(EXCEPTION_ACCESS_VIOLATION,0,0,nullptr);
 }
 return lifecycle_read(context,at,into,size);
}
inline bool same_direct_binding(const OwnedBinding& first,const OwnedBinding& next) noexcept {
 return next.complete&&first.manager==next.manager&&first.attached_proc==next.attached_proc&&
  first.owner_formid==next.owner_formid&&first.mode==next.mode&&first.descriptor==next.descriptor;
}
inline void copy_direct_locked(const OwnedBinding& before,LifecycleGate::Lease& lease){
 if(offline_direct_entered&&offline_direct_case!=78){SetEvent(offline_direct_entered);if(WaitForSingleObject(offline_direct_resume,10000)!=WAIT_OBJECT_0){pending->status="COPY_EXCEPTION";return;}}
 if(offline_direct_case==67){
  uint64_t replacement=before.attached_proc+0x10;
  std::memcpy(reinterpret_cast<void*>(before.manager+0x130),&replacement,8);
 }
 const auto begin=precise_filetime();
 const auto admitted=read_binding(direct_read,&lease,module_base);
 pending->binding_before=before;
 if(!same_direct_binding(before,admitted)){pending->status="CURRENT_BINDING_NOT_ADMITTED";return;}
 *pending=copy_resident(direct_read,&lease,before.attached_proc,memory_budget,epoch,hazards,&capture_cancelled,true,&source_recorder);
 pending->binding_before=admitted;
 pending->binding_after=read_binding(direct_read,&lease,module_base);
 pending->copy_begin_filetime=begin;
 pending->copy_end_filetime=precise_filetime();
 if(pending->status=="COPIED_UNQUALIFIED"){
  if(!same_direct_binding(admitted,pending->binding_after))pending->status="CURRENT_BINDING_CHANGED_DURING_COPY";
  else if(pending->holders.empty())pending->status="NO_RESIDENT_HOLDERS";
 }
}
inline void direct_under_lease(LifecycleGate::Lease& lease){
 const auto before=read_binding(direct_read,&lease,module_base);
 pending->binding_before=before;
 if(!before.complete){pending->status=std::strcmp(before.status,"NO_MANAGER")==0?"NO_CURRENT_OWNER":"CURRENT_BINDING_NOT_ADMITTED";return;}
 if(!before.owner_formid){pending->status="NO_CURRENT_OWNER";return;}
 if(!before.attached_proc){pending->status="NO_ATTACHED_PROCGEN";return;}
 if(capture_cancelled)return;
 auto word=direct_reader_word(before.attached_proc);
 if(!word){pending->status="NATIVE_READER_UNAVAILABLE";return;}
 if(!try_direct_reader(word)){pending->status="NATIVE_READER_BUSY";return;}
 pending->proc=before.attached_proc;
 bool released{};
 __try{copy_direct_locked(before,lease);}
 __finally{released=release_direct_reader(word);}
 if(!released){pending->status="NATIVE_READER_RELEASE_UNQUALIFIED";broken=true;ready=false;}
}
inline void guarded_direct_attempt(){
 LifecycleGate::Lease lease;
 last_copy_reads=0;
 if(lifecycle_gate.faulted()){
  pending->status=lifetime_phase_failed?"LIFECYCLE_PHASE_EXCEPTION":"LIFECYCLE_PROTECTION_DISABLED";
  return;
 }
 if(!lifecycle_gate.try_copy(lease)){pending->status="LIFECYCLE_COPY_NOT_ADMITTED";return;}
 __try{direct_under_lease(lease);}
 __finally{last_copy_reads=lease.reads;lifecycle_gate.end_copy(lease);}
}
inline int direct_fault_filter(unsigned code) noexcept {
 // These faults originate on the observer-owned worker. Native hook exceptions
 // on original game threads continue through their original handlers.
 return code==EXCEPTION_ACCESS_VIOLATION||code==0xe0424447?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH;
}
inline bool direct_fault_boundary(){
 __try{guarded_direct_attempt();}
 __except(direct_fault_filter(GetExceptionCode())){return false;}
 return true;
}
inline void poll_direct_control() noexcept {
 try{
  const auto stop=startup_stop(nullptr);
  const unsigned reason=stop>0?1:stop<0?3:!disk_floors()?2:0;
  if(reason){
   unsigned unset=0;cancel_reason.compare_exchange_strong(unset,reason);
   capture_cancelled=true;
   if(offline_direct_cancelled)SetEvent(offline_direct_cancelled);
  }
 }catch(...){unsigned unset=0;cancel_reason.compare_exchange_strong(unset,3);capture_cancelled=true;}
}
inline VOID CALLBACK direct_control_timer(PTP_CALLBACK_INSTANCE,void*,PTP_TIMER){poll_direct_control();}
inline bool direct_timer_attempt(PTP_TIMER timer){
 __try{return direct_fault_boundary();}
 __finally{
  SetThreadpoolTimer(timer,nullptr,0,0);
  WaitForThreadpoolTimerCallbacks(timer,TRUE);
  CloseThreadpoolTimer(timer);
 }
}
inline void run_direct_attempt(){
 poll_direct_control();
 if(capture_cancelled)return;
 auto timer=CreateThreadpoolTimer(direct_control_timer,nullptr,nullptr);
 if(!timer){pending->status="CONTROL_WATCHER_CREATE_FAILED";return;}
 FILETIME due{0xfff85ee0,0xffffffff}; // Relative 50 ms in 100 ns units.
 SetThreadpoolTimer(timer,&due,50,0);
 try{
  if(!direct_timer_attempt(timer)){pending->status="DIRECT_OBSERVER_EXCEPTION";broken=true;ready=false;}
 }catch(...){pending->status="COPY_EXCEPTION";broken=true;ready=false;}
 poll_direct_control();
 if(capture_cancelled||pending->status!="COPIED_UNQUALIFIED")pending->holders.clear();
}
inline void copy_callback_owned(uint64_t operand,uint64_t proc,bool area,LifecycleGate::Lease& lease){
 try{
  pending->selected_reference=active_selected;
  if(scope_hazards||hazards.load()||scope_epoch!=epoch.load()){pending->status="LIFETIME_CHANGED_BEFORE_CALLBACK";captured_here=true;return;}
  auto begin=precise_filetime();auto before=read_binding(lifecycle_read,&lease,module_base);
  pending->binding_before=before;
  if(!before.complete||before.attached_proc!=proc){pending->status="CURRENT_BINDING_NOT_ADMITTED";pending->proc=proc;pending->copy_begin_filetime=begin;pending->copy_end_filetime=precise_filetime();return;}
  uint64_t holder{};bool read_holder=!area||lifecycle_read(&lease,operand,&holder,8);
  *pending=copy_resident(lifecycle_read,&lease,proc,memory_budget,epoch,hazards,&capture_cancelled,before.complete&&before.attached_proc==proc&&!hazards.load()&&epoch.load()==scope_epoch,&source_recorder);
  pending->binding_before=before;pending->binding_after=read_binding(lifecycle_read,&lease,module_base);
  pending->copy_begin_filetime=begin;pending->copy_end_filetime=precise_filetime();
  if(area){pending->operation=active_operation;pending->selected_reference=active_selected;}
  bool matched=false;for(const auto& value:pending->holders)if(value.holder&&(area?value.holder==holder:value.holder+0x10==operand))matched=true;
  if(!read_holder||!matched)pending->status=area?"AREA_CALLBACK_HOLDER_NOT_IN_CENSUS":"CALLBACK_HOLDER_NOT_IN_CENSUS";
  captured_here=true;
 }catch(...){broken=true;ready=false;pending->status="COPY_EXCEPTION";captured_here=true;}
}
inline void guarded_copy_callback(uint64_t operand,uint64_t proc,bool area){
 auto error=GetLastError();captured_here=true;LifecycleGate::Lease lease;last_copy_reads=0;
 if(!lifecycle_gate.try_copy(lease)){
  pending->status="LIFECYCLE_COPY_NOT_ADMITTED";captured_here=true;
  if(lifecycle_gate.faulted()){broken=true;ready=false;}SetLastError(error);return;
 }
 __try{copy_callback_owned(operand,proc,area,lease);}
 __finally{last_copy_reads=lease.reads;lifecycle_gate.end_copy(lease);SetLastError(error);}
}
extern "C" void d5ar_capture_area_callback(uint64_t holder_slot,uint64_t,uint64_t proc,uint64_t return_address){
 using namespace d5ar;auto error=GetLastError();
 if(ready&&!broken&&area_depth==1&&return_address==module_base+0x21e0a4b){
  if(state.claim(scope_command,Armed,Copying))guarded_copy_callback(holder_slot,proc,true);
 }SetLastError(error);
}
}

extern "C" void d5ar_capture_selection(uint64_t reference,uint64_t release_return,uint64_t resolver_slot,uint64_t){
 using namespace d5ar;auto error=GetLastError();
 if(ready&&!broken&&selected_established&&selected_scope.active&&state.at(selected_scope.command,Armed)){
  if(selected_depth!=1)selection_ambiguous(selected_scope);
  else if(hazards.load())selected_scope.status="SELECTION_PHASE_CHANGED";
  else{uint64_t caller{};if(!checked_read(nullptr,resolver_slot,&caller,8))selected_scope.status="SELECTED_CALLER_READ_FAILED";
   else copy_selected_lease(selected_scope,checked_read,nullptr,module_base,release_return,caller,reference,epoch.load());}
 }
 SetLastError(error);
}

extern "C" void d5ar_area_entry(uint64_t context,uint64_t query,uint64_t reference,uint64_t return_address,uint32_t radius,uint32_t upper){
 using namespace d5ar;auto error=GetLastError();
 entry_area_eligible=ready&&!broken&&selected_depth==1&&selected_established&&selected_scope.active&&selected_scope.observations&&state.at(selected_scope.command,Armed)&&return_address==module_base+0x21b26c1;
 if(!entry_area_eligible){SetLastError(error);return;}
 entry_operation_epoch=epoch.load();entry_operation_hazards=hazards.load();
 if(entry_area_eligible)entry_operation=capture_operation(checked_read,nullptr,module_base,return_address,reference,context,query,radius,upper);
 else entry_operation={};
 entry_selected={};
 if(entry_area_eligible){
  auto candidate=selected_scope;
  link_selected_operation(candidate,selected_scope.invocation,selected_scope.command,epoch.load(),module_base,return_address,reference);

  entry_selected=candidate;
 }
 SetLastError(error);
}

extern "C" void d5ar_capture_callback(uint64_t holder_map,uint64_t,uint64_t proc,uint64_t return_address){
 using namespace d5ar;auto error=GetLastError();
 if(ready&&!broken&&point_depth==1&&current_point==proc&&return_address==module_base+0x79dff7){
  if(state.claim(scope_command,Armed,Copying))guarded_copy_callback(holder_map,proc,false);
 }SetLastError(error);
}

extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={SFSEPluginVersionData::kVersion,0x00020000,"SOR Outpost Geometry Snapshot 0.2.0 - NOT AUTHORIZED","Starfield Outpost Systems Research",0,0,{d5ar::game_version,0},0,0,0};
extern "C" __declspec(dllexport) bool SFSEPlugin_Preload(const SFSEInterface* api){
 try{return d5ar::initialize(api);}catch(...){d5ar::broken=true;if(!d5ar::patches_live)for(auto& hook:d5ar::hooks)d5ar::discard_prepared(hook);return d5ar::patches_live;}
}
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* api){
 using namespace d5ar;
 try{
  if(!ready||!api)return broken.load();
  tasks=static_cast<SFSETaskInterface*>(api->QueryInterface(kInterface_Task));
  if(!tasks||tasks->interfaceVersion!=1||!tasks->AddTask){broken=true;ready=false;return true;}
  HMODULE self{};wchar_t path[32768]{};
  if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&SFSEPlugin_Load),&self)||!GetModuleFileNameW(self,path,32768)){broken=true;ready=false;return true;}
  metadata.plugin_sha256=sha_file(path);metadata.game_exe_sha256=expected_game;metadata.sfse_sha256=expected_sfse;metadata.source_lock_sha256=source_lock_hash;
  metadata.pid=GetCurrentProcessId();
  FILETIME birth{},exit{},kernel{},user{};if(!GetProcessTimes(GetCurrentProcess(),&birth,&exit,&kernel,&user)){broken=true;ready=false;return true;}
  metadata.creation_filetime=(uint64_t(birth.dwHighDateTime)<<32)|birth.dwLowDateTime;
  if(sha_file(config_path)!=config_hash){broken=true;ready=false;return true;}
  completed=CreateEventW(nullptr,FALSE,FALSE,nullptr);if(!completed){broken=true;ready=false;}
  if(ready){
   start_registration();
  }
  return true;
 }catch(...){broken=true;ready=false;return true;}
}

namespace d5ar {
inline OfflineInput offline_input;
inline unsigned offline_write_calls{};inline bool offline_rollback_failure{};
inline bool offline_failing_write(Hook& hook,bool install){
 if(install&&offline_write_calls++==2){write_hook(hook,true);return false;}
 if(!install&&offline_rollback_failure){offline_rollback_failure=false;return false;}
 return write_hook(hook,install);
}
inline uint64_t offline_cpp_error{};
inline uint64_t offline_phase_cpp(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 if(a!=0xaaaa||b!=0xbbbb||c!=0xcccc||d!=0xdddd)return 0;
 std::runtime_error failure("Owned original phase C++ exception");SetLastError(0x9988ff11);throw failure;
}
inline bool offline_phase_cpp_probe(Four hook){
 try{hook(0xaaaa,0xbbbb,0xcccc,0xdddd);}
 catch(const std::runtime_error& failure){offline_cpp_error=GetLastError();return std::strcmp(failure.what(),"Owned original phase C++ exception")==0;}return false;
}
inline unsigned offline_inert_visits{};
inline uint64_t offline_inert_phase(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 if(a!=0xaaaa||b!=0xbbbb||c!=0xcccc||d!=0xdddd)return 0;++offline_inert_visits;SetLastError(0x1122ccaa);return a;
}
inline unsigned offline_free_visits{};inline bool offline_free_gate_released{};
inline uint64_t offline_free_exception(uint64_t source,uint64_t size,uint64_t,uint64_t){
 ++offline_free_visits;
 auto value=source_recorder.copy(nullptr,nullptr,source);
 offline_free_gate_released=size==0x1a0&&!std::strcmp(value.status,"SOURCE_LIFETIME_RETIRED");
 // Repeated/nested ending after the first mark must not retain exclusive ownership.
 source_recorder.mark(source);source_recorder.mark(source+0x1000);
 SetLastError(0x99557711);RaiseException(0xe0424446,0,0,nullptr);return 0;
}
inline bool offline_free_exception_probe(Four call){
 __try {call(0x123450,0x1a0,0,0);}
 __except(GetExceptionCode()==0xe0424446?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline uint64_t offline_point(uint64_t proc,uint64_t query,uint64_t,uint64_t){
 if(offline_input.mode==19){if(query)return 11;if(point_hook(proc,1,0,0)!=11)return 0;}
 if(offline_input.mode==1)increment_epoch();
 if(offline_input.mode==17){SetLastError(0xabcdef01);RaiseException(0xe0424442,0,0,nullptr);}
 if(offline_input.mode==5)return 11;
 auto error=GetLastError();
 d5ar_capture_callback(offline_input.holder+0x10,0,proc,module_base+0x79dff7);
 if(GetLastError()!=error){broken=true;}
 if(offline_input.mode==16){SetLastError(0xabcdef01);RaiseException(0xe0424442,0,0,nullptr);}
 return 11;
}
inline bool offline_proc_reused{};
inline uint64_t offline_proc_replacement(uint64_t,uint64_t,uint64_t,uint64_t){
 auto address=reinterpret_cast<void*>(offline_input.proc);std::array<uint8_t,0x60> prior{};std::memcpy(prior.data(),address,prior.size());
 if(!VirtualFree(address,0,MEM_RELEASE)||VirtualAlloc(address,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE)!=address)return 0;
 std::memcpy(address,prior.data(),prior.size());offline_proc_reused=true;return 3;
}
inline uint64_t offline_phase_callback(uint64_t,uint64_t,uint64_t,uint64_t){
 auto holder=offline_input.holder;d5ar_capture_area_callback(reinterpret_cast<uint64_t>(&holder),0,offline_input.proc,module_base+0x21e0a4b);return 3;
}
inline std::atomic<bool> offline_phase_mutated{},offline_phase_done{};
inline SRWLOCK offline_native_reader=SRWLOCK_INIT;inline HANDLE offline_native_phase_entered{};
inline uint64_t offline_phase_native_wait(uint64_t,uint64_t,uint64_t,uint64_t){SetEvent(offline_native_phase_entered);AcquireSRWLockExclusive(&offline_native_reader);ReleaseSRWLockExclusive(&offline_native_reader);return 3;}
inline uint64_t offline_phase_mutation(uint64_t,uint64_t,uint64_t,uint64_t){offline_phase_mutated=true;return 3;}
inline thread_local SelectedLease offline_seen_selection{};
inline thread_local bool offline_stale_scope{};
inline HANDLE offline_scope_entered{},offline_scope_resume{};
inline bool offline_recycled{},offline_area_nested{},offline_nested_area_ignored{};
inline uint64_t offline_area(uint64_t,uint64_t,float,float){
 offline_seen_selection=active_selected;
 if(offline_stale_scope&&(!SetEvent(offline_scope_entered)||WaitForSingleObject(offline_scope_resume,10000)!=WAIT_OBJECT_0))return 0;
 if(offline_input.mode==41&&!offline_area_nested){
  offline_area_nested=true;d5ar_area_entry(0,offline_input.area_query,offline_input.operation_reference,module_base+0x21b26c2,0x43160000,0x40000000);
  auto result=area_hook(0,offline_input.area_query,150.0f,2.0f);offline_area_nested=false;
  if(result!=12||state.load()!=Armed)return 0;offline_nested_area_ignored=true;
 }
 if(offline_input.mode==6)return 12;
 if(offline_input.mode==56){destructor_original=offline_proc_replacement;if(destroy_hook(0,0,0,0)!=3)return 0;}
 if(offline_input.mode==49){destructor_original=offline_phase_callback;if(destroy_hook(0,0,0,0)!=3)return 0;}
 if(offline_input.mode==51){
  AcquireSRWLockShared(&offline_native_reader);offline_native_phase_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);if(!offline_native_phase_entered)return 0;
  destructor_original=offline_phase_native_wait;std::atomic<bool> phase_ok{};
  std::thread phase([&]{phase_ok=destroy_hook(0,0,0,0)==3;});
  bool entered=WaitForSingleObject(offline_native_phase_entered,10000)==WAIT_OBJECT_0;
  auto slot=offline_input.holder;d5ar_capture_area_callback(reinterpret_cast<uint64_t>(&slot),0,offline_input.proc,module_base+0x21e0a4b);
  bool refused=last_copy_reads==0&&state==Copying;ReleaseSRWLockShared(&offline_native_reader);phase.join();CloseHandle(offline_native_phase_entered);offline_native_phase_entered=nullptr;
  return entered&&refused&&phase_ok?12:0;
 }
 auto holder=offline_input.holder;
 d5ar_capture_area_callback(reinterpret_cast<uint64_t>(&holder),0,offline_input.proc,module_base+0x21e0a4b);
 if(offline_input.mode==50)while(!offline_phase_done)SwitchToThread();
 return 12;
}
inline bool offline_exception_probe(uint64_t proc){
 __try{point_hook(proc,0,0,0);}
 __except(GetExceptionCode()==0xe0424442?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline uint64_t offline_initializer(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 if(a!=0xaaaa||b!=0xbbbb||c!=0xcccc||d!=0xdddd||(hazards.load()!=1&&!lifecycle_gate.faulted()))return 0;
 if(offline_input.mode==22){SetLastError(0x87654321);RaiseException(0xe0424443,0,0,nullptr);}
 // Owned constructor/final-store gap: real original publication instructions
 // have their own separate native control; this tests the production fence.
 uint64_t owner{};auto root=reinterpret_cast<uint64_t*>(module_base+0x5fd9c30);owner=*root;
 *root=owner+16;*root=owner;
 if(point_hook(offline_input.proc,0,0,0)!=11)return 0;
 *root=owner;SetLastError(0x87654321);return a;
}
inline bool offline_initializer_exception(Four hook){
 __try{hook(0xaaaa,0xbbbb,0xcccc,0xdddd);}
 __except(GetExceptionCode()==0xe0424443?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline uint64_t offline_phase_return(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 if(a!=0xaaaa||b!=0xbbbb||c!=0xcccc||d!=0xdddd||hazards.load()!=1)return 0;SetLastError(0x87654321);return a;
}
inline bool all_frames(void*,uint64_t){return true;}
inline std::atomic<SFSETaskInterface::ITaskDelegate*> offline_task{};
inline std::atomic<unsigned> offline_task_count{};
inline void offline_add_task(SFSETaskInterface::ITaskDelegate* task){++offline_task_count;if(offline_input.mode==15){task->Run();task->Destroy();}else offline_task=task;}
inline unsigned offline_destructor_visits{};
using OfflineCommand=bool(*)(const void*,const char*,void*,void*,void*,void*,float*,uint32_t*);
inline OfflineCommand offline_invoke{};
inline uint64_t offline_arm_mid_operation(uint64_t,uint64_t,uint64_t,uint64_t){
 float result{};if(!offline_invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&result,nullptr)||result!=1||state!=Armed)return 0;
 auto capture_id=metadata.capture_id;result=99;if(!offline_invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&result,nullptr)||result||capture_id!=metadata.capture_id)return 0;
 uint64_t caller=module_base+0x21b25dd;d5ar_capture_selection(offline_input.operation_reference,module_base+0xf3e0c7,reinterpret_cast<uint64_t>(&caller),0);
 d5ar_area_entry(0,offline_input.area_query,offline_input.operation_reference,module_base+0x21b26c1,0x43160000,0x40000000);
 if(area_hook(0,offline_input.area_query,150.0f,2.0f)!=12)return 0;SetLastError(0x12345678);return 77;
}
inline thread_local bool offline_nested{};
inline uint64_t offline_operation(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 if(a!=0xaaaa||b!=offline_input.operation_state||c!=0xcccc||d!=0xdddd)return 0;
 if(offline_input.mode==29&&!offline_nested){offline_nested=true;auto result=operation_hook(a,b,c,d);offline_nested=false;if(result!=77)return 0;}
 uint64_t caller=module_base+(offline_input.mode==33?0x21b25de:0x21b25dd);
 auto release=module_base+(offline_input.mode==27?0xf3e0c8:0xf3e0c7);
 auto slot=offline_input.mode==34?uint64_t(1):reinterpret_cast<uint64_t>(&caller);
 d5ar_capture_selection(offline_input.operation_reference,release,slot,0);
 if(offline_input.mode==28)d5ar_capture_selection(offline_input.operation_reference,release,slot,0);
 if(offline_input.mode==26){uint32_t changed=0x99887;std::memcpy(reinterpret_cast<void*>(offline_input.operation_reference+0x28),&changed,4);}
 if(offline_input.mode==35){
  auto reference=reinterpret_cast<void*>(offline_input.operation_reference);MEMORY_BASIC_INFORMATION information{};std::array<uint8_t,0xb8> prior{};
  if(!VirtualQuery(reference,&information,sizeof information)||information.Type!=MEM_PRIVATE||information.AllocationBase!=reference||!checked_read(nullptr,offline_input.operation_reference,prior.data(),prior.size()))return 0;
  if(!VirtualFree(reference,0,MEM_RELEASE)||VirtualAlloc(reference,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE)!=reference)return 0;
  std::memcpy(reference,prior.data(),prior.size());offline_recycled=true;
 }
 if(offline_input.mode==32&&!state.advance())return 0;
 if(offline_input.mode==36)increment_epoch();
 if(offline_input.mode==31){SetLastError(0xabcdef02);RaiseException(0xe0424444,0,0,nullptr);}
 if(offline_input.mode==57){destructor_original=offline_proc_replacement;if(destroy_hook(0,0,0,0)!=3)return 0;}
 if(offline_input.mode!=30){
  d5ar_area_entry(0,offline_input.area_query,offline_input.operation_reference,module_base+0x21b26c1,0x43160000,0x40000000);
  if(area_hook(0,offline_input.area_query,150.0f,2.0f)!=12)return 0;
 }
 SetLastError(0x12345678);return 77;
}
inline bool offline_lifecycle_exception(){
 __try {operation_hook(0xaaaa,offline_input.operation_state,0xcccc,0xdddd);}
 __except(GetExceptionCode()==0xe0424447?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline uint64_t offline_scoped_area(uint64_t,uint64_t,uint64_t,uint64_t){
 uint64_t caller=module_base+0x21b25dd;d5ar_capture_selection(offline_input.operation_reference,module_base+0xf3e0c7,reinterpret_cast<uint64_t>(&caller),0);
 d5ar_area_entry(0,offline_input.area_query,offline_input.operation_reference,module_base+0x21b26c1,0x43160000,0x40000000);
 return area_hook(0,offline_input.area_query,150.0f,2.0f);
}
inline bool offline_operation_exception(){
 __try{operation_hook(0xaaaa,offline_input.operation_state,0xcccc,0xdddd);}
 __except(GetExceptionCode()==0xe0424444?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline uint64_t offline_destructor(uint64_t depth,uint64_t,uint64_t,uint64_t){
 if(hazards.load()!=2-depth)return 0;++offline_destructor_visits;
 return depth?destroy_hook(0,0,0,0):3;
}
inline uint64_t observed_call_return{};
__declspec(noinline) inline uint64_t offline_call_replacement(uint64_t,uint64_t,uint64_t,uint64_t){observed_call_return=reinterpret_cast<uint64_t>(_ReturnAddress());return 5;}
inline uint64_t offline_replacement(uint64_t,uint64_t,uint64_t,uint64_t){return 5;}
}
extern "C" __declspec(dllexport) unsigned D5AR_OfflineQualify(const d5ar::OfflineInput* input){
 using namespace d5ar;
 try{
  wchar_t host[32768]{};if(!GetModuleFileNameW(nullptr,host,32768)||std::filesystem::path(host).filename()!=L"d5ar-plugin-fixture.exe"||
    sha_file(host)!=expected_fixture_host||GetModuleHandleW(L"sfse_1_16_244.dll"))return 0;
  OfflineInput request{};if(!checked_read(nullptr,reinterpret_cast<uint64_t>(input),&request,sizeof request)||request.mode>80)return 0;
  MEMORY_BASIC_INFORMATION memory{};if(!VirtualQuery(reinterpret_cast<void*>(request.image_base),&memory,sizeof memory)||memory.AllocationBase!=reinterpret_cast<void*>(request.image_base)||memory.Type!=MEM_PRIVATE)return 0;
  offline_input=request;module_base=request.image_base;unsigned checks=0;
  direct_capture=request.mode>=62;
  if(request.mode==10)return fixture::startup_controls();
  if(request.mode==20){
   auto full=startup_stack(nullptr,nullptr);if(full.status!=StackStatus::Complete||!full.frames){SetLastError(5000+unsigned(full.status));return 0;}
   if(startup_stack(all_frames,nullptr).status!=StackStatus::ForbiddenAncestor)return 0;
   ULONG_PTR low{},high{};GetCurrentThreadStackLimits(&low,&high);CONTEXT context{};RtlCaptureContext(&context);context.Rsp=high;
   if(walk_startup_stack(context,low,high,nullptr,nullptr).status!=StackStatus::OutsideStack)return 0;
   RtlCaptureContext(&context);context.Rip=1;
   if(walk_startup_stack(context,low,high,nullptr,nullptr).status!=StackStatus::MissingMetadata)return 0;return 4;
  }
  if(request.mode==22||request.mode==23){
   initializer_original=installer_original=reset_original=manager_destructor_original=request.mode==22?offline_initializer:offline_phase_return;
   for(auto hook:{initializer_hook,installer_hook,reset_hook,manager_destructor_hook}){
    auto before=epoch.load();bool was_fault=lifecycle_gate.faulted();bool success=request.mode==22?offline_initializer_exception(hook):hook(0xaaaa,0xbbbb,0xcccc,0xdddd)==0xaaaa;
    if(!success||GetLastError()!=0x87654321||hazards.load()||epoch.load()!=before+(was_fault?0:2)||(request.mode==22&&(!broken||ready||!lifecycle_gate.faulted())))return 0;
   }return 16;
  }
  if(request.mode==18){destructor_original=offline_destructor;auto before=epoch.load();if(destroy_hook(1,0,0,0)!=3||hazards.load()||epoch.load()!=before+4||offline_destructor_visits!=2)return 0;return 4;}
  if(request.mode>=11&&request.mode<=13){
   output_directory=std::filesystem::path(request.output_directory);
   if(request.mode==12)*reinterpret_cast<uint64_t*>(module_base+0x5fd9c30)=0x12345;
   if(request.mode==13){DWORD prior{};if(!VirtualProtect(reinterpret_cast<void*>(module_base+0x5fd9000),4096,PAGE_NOACCESS,&prior))return 0;}
   auto result=await_startup(nullptr,{startup_owner,startup_sole,startup_disk,startup_stop,startup_pause});
   auto expected=request.mode==11?StartupResult::Stopped:request.mode==12?StartupResult::OwnerPresent:StartupResult::OwnerReadFailed;
   return result==expected?1:0;
  }
  if(request.mode==43)return fixture::source_lifetime_controls();
  if(request.mode==48)return fixture::lifecycle_controls();
  if(request.mode==58){
   if(!offline_phase_cpp_probe(offline_phase_cpp))return 0;auto native_error=offline_cpp_error;
   destructor_original=initializer_original=installer_original=reset_original=manager_destructor_original=offline_phase_cpp;
   for(auto hook:{destroy_hook,initializer_hook,installer_hook,reset_hook,manager_destructor_hook}){
    auto before=epoch.load();bool was_fault=lifecycle_gate.faulted();if(!offline_phase_cpp_probe(hook)||offline_cpp_error!=native_error||hazards.load()||epoch.load()!=before+(was_fault?0:2)||!lifecycle_gate.faulted()||!broken||ready||!lifecycle_gate.offline_probe_unlocked())return 0;
   }
   auto before=epoch.load();destructor_original=reset_original=offline_inert_phase;
   if(destroy_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||GetLastError()!=0x1122ccaa||reset_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||GetLastError()!=0x1122ccaa||offline_inert_visits!=2||epoch.load()!=before||hazards.load())return 0;
   return 24;
  }
  if(request.mode==4){
   const uint64_t offsets[]{0x1000,0x2000,0x3000,0x4000,0x5000,0x6000,0x7000,0x8000};
   Hook local[11];
   auto create=[&](unsigned n,const auto& preimage,int saved){
    auto address=module_base+offsets[n];std::memcpy(reinterpret_cast<void*>(address),preimage,sizeof preimage);
    auto body=reinterpret_cast<uint8_t*>(address+sizeof preimage);
    if(saved==-2){const uint8_t pops[]{0x5f,0x5e,0x5d,0x5b};std::memcpy(body,pops,sizeof pops);body+=sizeof pops;}
    if(saved==-3){const uint8_t pops[]{0x5b,0x5d};std::memcpy(body,pops,sizeof pops);body+=sizeof pops;}
    const uint8_t tail[]{0xb8,3,0,0,0,0xc3};std::memcpy(body,tail,sizeof tail);
    DWORD old{};if(!VirtualProtect(reinterpret_cast<void*>(address),4096,PAGE_EXECUTE_READ,&old))return false;
    return prepare_hook(local[n],address,reinterpret_cast<void*>(&offline_replacement),preimage,saved);
   };
   if(!create(0,destroy_bytes,8)||!create(1,area_bytes,8)||!create(2,area_callback_bytes,8)||!create(3,initializer_bytes,-1)||!create(4,installer_bytes,8)||!create(5,reset_bytes,-2)||!create(6,manager_destructor_bytes,8)||!create(7,operation_bytes,-3)){SetLastError(4000);return 0;}
   uint64_t call_functions[3]{},call_sites[3]{};
   for(unsigned n=0;n<3;++n){
    auto call_function=n?module_base+(n==1?0x982af4:0x982c2e):module_base+0xb000;auto call_site=call_function+4,call_target=n?module_base+0x365cdb0:module_base+0xc000;
    DWORD writable{};if(!VirtualProtect(reinterpret_cast<void*>(call_function&~uint64_t(4095)),4096,PAGE_EXECUTE_READWRITE,&writable)||!VirtualProtect(reinterpret_cast<void*>(call_target),4096,PAGE_EXECUTE_READWRITE,&writable))return 0;
    call_functions[n]=call_function;call_sites[n]=call_site;
    uint8_t call_preimage[5]{0xe8};auto relative=int32_t(call_target-(call_site+5));std::memcpy(call_preimage+1,&relative,4);
    const uint8_t prefix[]{0x48,0x83,0xec,0x28},suffix[]{0x48,0x83,0xc4,0x28,0xc3};
    std::memcpy(reinterpret_cast<void*>(call_function),prefix,4);std::memcpy(reinterpret_cast<void*>(call_site),call_preimage,5);std::memcpy(reinterpret_cast<void*>(call_site+5),suffix,5);
    auto entry=reinterpret_cast<RUNTIME_FUNCTION*>(call_function+0x400);*entry={0,14,0x420};
    const uint8_t unwind[]{1,4,1,0,4,0x42,0,0};std::memcpy(reinterpret_cast<void*>(call_function+0x420),unwind,sizeof unwind);
    if(!RtlAddFunctionTable(entry,1,call_function)){SetLastError(4010);return 0;}
    const uint8_t body[]{0xb8,3,0,0,0,0xc3};std::memcpy(reinterpret_cast<void*>(call_target),body,sizeof body);
    DWORD old_call{},old_target{};
    if(!VirtualProtect(reinterpret_cast<void*>(call_function&~uint64_t(4095)),4096,PAGE_EXECUTE_READ,&old_call)||!VirtualProtect(reinterpret_cast<void*>(call_target),4096,PAGE_EXECUTE_READ,&old_target)||
       !prepare_call(local[8+n],call_site,n?reinterpret_cast<void*>(&d5ar_source_free_bridge):reinterpret_cast<void*>(&offline_call_replacement),call_preimage,call_target)){SetLastError(4008);return 0;}
   }
   auto started=GetTickCount64();while(!sole_thread()){
    // Finite owned-host loader-drain control; production never waits here.
    if(GetTickCount64()-started>60000){SetLastError(4001);return 0;}Sleep(100);
   }
   source_recorder.begin(true);d5ar_source_free_original=reinterpret_cast<uint64_t>(local[9].original);
   bool dirty=false;
   local[10].before[0]^=1;
   bool mismatch=install_hooks(local,11,dirty);local[10].before[0]^=1;
   if(mismatch||dirty)return 0;
   for(auto& hook:local)if(std::memcmp(hook.at,hook.before,hook.length))return 0;++checks;
   offline_write_calls=0;
   if(install_hooks(local,11,dirty,offline_failing_write)||dirty)return 0;
   for(auto& hook:local)if(std::memcmp(hook.at,hook.before,hook.length))return 0;++checks;
   offline_write_calls=0;offline_rollback_failure=true;
   if(install_hooks(local,11,dirty,offline_failing_write)||!dirty)return 0;
   // Owned fixture recovery only; production returns dirty and retains its module.
   for(auto& hook:local)if(!write_hook(hook,false))return 0;++checks;
   if(!install_hooks(local,11,dirty)){SetLastError(4002);return 0;}++checks;
   for(auto& hook:local){auto index=size_t(&hook-local);auto current=reinterpret_cast<Four>(index>=8?call_functions[index-8]:reinterpret_cast<uint64_t>(hook.at)),original=reinterpret_cast<Four>(hook.original);
    if(current(index>8?0x123450+uint64_t(index-9)*0x2000:0,index>8?0x1a0:0,0,0)!=(index>8?3:5)||original(0,0,0,0)!=3){SetLastError(4003);return 0;}
    if(index>=8){DWORD64 leaf_base{};if((index==8&&observed_call_return!=call_sites[index-8]+5)||RtlLookupFunctionEntry(reinterpret_cast<DWORD64>(hook.page),&leaf_base,nullptr)){SetLastError(4009);return 0;}++checks;continue;}
    DWORD64 base{};auto entry=RtlLookupFunctionEntry(reinterpret_cast<DWORD64>(hook.original),&base,nullptr);if(!entry){SetLastError(4004);return 0;}
    ++checks;
    for(size_t continuation:{size_t(0),size_t(10)}){
    alignas(16) std::array<uint64_t,16> stack{};CONTEXT context{};context.ContextFlags=CONTEXT_FULL;
    auto start=reinterpret_cast<uint64_t>(stack.data()),resume=reinterpret_cast<uint64_t>(&offline_replacement);
    context.Rip=reinterpret_cast<uint64_t>(hook.original)+hook.length+continuation;context.Rsp=start;
    if(index==5){stack[0]=0xd1;stack[1]=0x51;stack[2]=0xb1;stack[3]=0xb2;stack[4]=resume;}
    else if(index==7){stack[0]=0xb2;stack[1]=0xb1;stack[2]=resume;}
    else{stack[0]=resume;stack[1]=0xb2;}
    if(!unwind_step(context,base,entry)||context.Rip!=resume||context.Rsp!=start+(index==5?40:index==7?24:8)){SetLastError(4005);return 0;}
    if(index==5){if(context.Rdi!=0xd1||context.Rsi!=0x51||context.Rbp!=0xb1||context.Rbx!=0xb2){SetLastError(4006);return 0;}}
    else if(index==7){if(context.Rbp!=0xb1||context.Rbx!=0xb2){SetLastError(4006);return 0;}}
    else if(index!=3&&context.Rbx!=0xb2){SetLastError(4007);return 0;}
    ++checks;
    }
   }
   for(auto source:{uint64_t(0x123450),uint64_t(0x125450)}){
    auto denied=source_recorder.copy(nullptr,nullptr,source);
    if(std::strcmp(denied.status,"SOURCE_LIFETIME_RETIRED"))return 0;
   }++checks;
   // Same production installed CALL relay, concurrent with the complete group.
   fixture::SourceInput live;live.entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);live.resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);
   if(!live.entered||!live.resume)return 0;SourceDiagnostics copied;
   std::atomic<bool> attempting{},forwarded{};
   std::thread reader([&]{copied=live.copy(source_recorder);});
   bool entered=WaitForSingleObject(live.entered,10000)==WAIT_OBJECT_0;
   std::thread ending([&]{attempting=true;auto result=reinterpret_cast<Four>(call_functions[1])(live.ptr(),0x1a0,0,0);forwarded=result==3;});
   while(!attempting)SwitchToThread();Sleep(20);bool blocked=!forwarded;
   SetEvent(live.resume);reader.join();ending.join();CloseHandle(live.entered);CloseHandle(live.resume);live.entered=nullptr;
   if(!entered||!blocked||!forwarded||!copied.complete||!copied.origin_complete||!copied.descriptor_complete||live.calls!=14)return 0;++checks;
   live.calls=0;if(std::strcmp(live.copy(source_recorder).status,"SOURCE_LIFETIME_RETIRED")||live.calls)return 0;++checks;
   auto free_target=reinterpret_cast<void*>(d5ar_source_free_original);DWORD previous{},ignored{};
   if(!VirtualProtect(free_target,14,PAGE_EXECUTE_READWRITE,&previous))return 0;
   absolute_jump(static_cast<uint8_t*>(free_target),reinterpret_cast<uint64_t>(&offline_free_exception));
   if(!VirtualProtect(free_target,14,previous,&ignored)||!FlushInstructionCache(GetCurrentProcess(),free_target,14))return 0;
   for(unsigned n=1;n<3;++n){
    if(!offline_free_exception_probe(reinterpret_cast<Four>(call_functions[n]))||GetLastError()!=0x99557711||!offline_free_gate_released||offline_free_visits!=n)return 0;++checks;
   }
   return checks;
  }
  auto root=std::filesystem::path(request.output_directory);if(!root.is_absolute()||!std::filesystem::is_directory(root))return 0;
  ready=true;broken=false;registered=false;state=Idle;tasks=nullptr;output_directory=root;
  source_recorder.begin(true);
  if(request.mode==44){uint64_t map{},source{};if(!checked_read(nullptr,request.proc+0x20,&map,8)||!checked_read(nullptr,map,&source,8))return 0;source_recorder.mark(source);}
  if(request.mode==45)source_recorder.unavailable();
  if(request.mode==46||request.mode==47){
   uint64_t map{},source{};if(!checked_read(nullptr,request.proc+0x20,&map,8)||!checked_read(nullptr,map,&source,8))return 0;
   std::array<uint8_t,0x70> saved{};if(!checked_read(nullptr,source,saved.data(),saved.size()))return 0;
   uint32_t vacant=UINT32_MAX;std::memcpy(reinterpret_cast<void*>(map+16),&vacant,4);
   source_recorder.mark(source);
   if(!VirtualFree(reinterpret_cast<void*>(source),0,MEM_RELEASE))return 0;
   auto reused=VirtualAlloc(reinterpret_cast<void*>(source),4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);
   if(reinterpret_cast<uint64_t>(reused)!=source)return 0;
   std::memcpy(reused,saved.data(),saved.size());
   if(request.mode==47){DWORD old{};if(!VirtualProtect(reused,4096,PAGE_NOACCESS,&old))return 0;}
   uint32_t occupied=0;std::memcpy(reinterpret_cast<void*>(map),&source,8);std::memcpy(reinterpret_cast<void*>(map+16),&occupied,4); // Owned late publication after ending/reuse.
  }
  if(request.mode==7||request.mode==76){if(!private_config()||output_directory!=root)return 0;++checks;}
  metadata={};metadata.evidence_basis="SYNTHETIC";metadata.session_id=random_uuid();metadata.pid=GetCurrentProcessId();metadata.game_exe_sha256=expected_game;metadata.sfse_sha256=expected_sfse;metadata.source_lock_sha256=source_lock_hash;
  HMODULE self{};wchar_t path[32768]{};
  if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&D5AR_OfflineQualify),&self)||!GetModuleFileNameW(self,path,32768))return 0;
  metadata.plugin_sha256=sha_file(path);FILETIME birth{},exit{},kernel{},user{};if(!GetProcessTimes(GetCurrentProcess(),&birth,&exit,&kernel,&user))return 0;
  metadata.creation_filetime=(uint64_t(birth.dwHighDateTime)<<32)|birth.dwLowDateTime;
  static char original_name[]="GameComment";auto row=module_base+0x5eb1050+0x49*0x58;
  auto name=reinterpret_cast<uint64_t>(original_name),handler=module_base+0x2b75d0,parameters=module_base+0x590e6d0,compiler=module_base+0xc16dd0;uint32_t opcode=0x149;uint16_t parameter_count=1;
  std::memcpy(reinterpret_cast<void*>(row),&name,8);std::memcpy(reinterpret_cast<void*>(row+0x10),&opcode,4);std::memcpy(reinterpret_cast<void*>(row+0x30),&handler,8);
  std::memcpy(reinterpret_cast<void*>(row+0x22),&parameter_count,2);std::memcpy(reinterpret_cast<void*>(row+0x28),&parameters,8);std::memcpy(reinterpret_cast<void*>(row+0x40),&compiler,8);
  *reinterpret_cast<uint8_t*>(module_base+0x621a2d0)=1;
  if(request.mode==8||request.mode==9){
   if(request.mode==8){auto wrong=module_base+0x2b75d1;std::memcpy(reinterpret_cast<void*>(row+0x30),&wrong,8);}
   else *reinterpret_cast<uint8_t*>(module_base+0x621a2d0)=0;
   std::array<uint8_t,0x58> before{};std::memcpy(before.data(),reinterpret_cast<void*>(row),before.size());
   if(register_command()||std::memcmp(before.data(),reinterpret_cast<void*>(row),before.size()))return 0;
   return 2;
  }
  if(request.mode==14||request.mode==15){
   SFSETaskInterface owned_tasks{};owned_tasks.interfaceVersion=1;owned_tasks.AddTask=offline_add_task;tasks=&owned_tasks;
   *reinterpret_cast<uint8_t*>(module_base+0x621a2d0)=0;
   if(!start_registration())return 0;Sleep(150);
   if(offline_task_count||registered||ready_announced)return 0;++checks;
   *reinterpret_cast<uint8_t*>(module_base+0x621a2d0)=1;
   if(WaitForSingleObject(registration_worker,10000)!=WAIT_OBJECT_0)return 0;++checks;
   if(request.mode==14){auto task=offline_task.exchange(nullptr);if(!task||ready_announced)return 0;task->Run();task->Destroy();}
   auto started=GetTickCount64();while(!ready_published&&!broken){if(GetTickCount64()-started>10000)return 0;Sleep(10);}
   if(broken||!registered||offline_task_count!=1||!registration_service_exited||!registration_task_done||!registration_wait_cleanup||!ready_published)return 0;++checks;
   return checks;
  }
  RegistrationTask registration;registration.Run();if(!registered)return 0;++checks;
  uint64_t installed{};std::memcpy(&installed,reinterpret_cast<void*>(row+0x30),8);
  using Command=bool(*)(const void*,const char*,void*,void*,void*,void*,float*,uint32_t*);
  auto invoke=reinterpret_cast<Command>(installed);completed=CreateEventW(nullptr,FALSE,FALSE,nullptr);if(!completed)return 0;
  if(direct_capture){
   offline_direct_case=request.mode;
   if(request.mode==76){
    auto started=GetTickCount64();
    while(!sole_thread()){if(GetTickCount64()-started>60000)return 0;Sleep(100);}
    if(!prepare_direct_hooks()){SetLastError(7601);return 0;}
    bool dirty=false;
    if(!install_hooks(hooks,std::size(hooks),dirty)){SetLastError(7602);return 0;}
    if(!runtime_guards()){SetLastError(7603);return 0;}
    constexpr uint64_t sites[]{0x79d910,0x1881660,0x789ce0,0x788e70,0x788bc0,0x982af8,0x982c32};
    for(size_t i=0;i<std::size(hooks);++i)
     if(reinterpret_cast<uint64_t>(hooks[i].at)!=module_base+sites[i]||hooks[i].length!=5)return 0;
    patches_live=true;
    float denied=99;
    if(!invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&denied,nullptr)||denied||active_worker)return 0;
    if(!startup_receipt("COMMAND_READY",0))return 0;
    ready_published=true;
    ++checks;
   }
   const auto pause=request.mode==71||request.mode==72||request.mode==75||request.mode==77||request.mode==78;
   if(pause){
    offline_direct_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);
    offline_direct_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);
    offline_direct_cancelled=CreateEventW(nullptr,TRUE,FALSE,nullptr);
    if(!offline_direct_entered||!offline_direct_resume||!offline_direct_cancelled)return 0;
   }
   if(request.mode==68&&!lifecycle_gate.phase_begin())return 0;
   float scalar{};
   const bool accepted=invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&scalar,nullptr)&&scalar==1;
   if(!accepted||!active_worker)return 0;
   ++checks;
   auto word=direct_reader_word(request.proc);
   if(pause){
    const bool entered=WaitForSingleObject(offline_direct_entered,10000)==WAIT_OBJECT_0;
    bool correct=entered&&word&&InterlockedCompareExchange(word,0,0)==(request.mode==78?0:1);
    if(request.mode==71){
     std::ofstream stop(output_directory/L"STOP",std::ios::binary);stop<<"Owned STOP during direct read\n";stop.close();
     correct=correct&&bool(stop)&&WaitForSingleObject(offline_direct_cancelled,10000)==WAIT_OBJECT_0;
     SetEvent(offline_direct_resume);
    }else if(request.mode==72){
     destructor_original=offline_proc_replacement;
     std::atomic<bool> attempting{},finished{};
     bool replaced{};
     std::thread phase([&]{attempting=true;replaced=destroy_hook(0,0,0,0)==3;finished=true;});
     while(!attempting)SwitchToThread();Sleep(20);
     correct=correct&&!finished;
     SetEvent(offline_direct_resume);phase.join();
     correct=correct&&replaced&&offline_proc_reused;
    }else if(request.mode==77){
     if(correct)correct=offline_queued_writer_control(request.proc,word);
     else SetEvent(offline_direct_resume);
    }else if(request.mode==78){
     correct=correct&&lifecycle_gate.offline_probe_unlocked();
     std::ofstream stop(output_directory/L"STOP",std::ios::binary);stop<<"Owned STOP before rename\n";stop.close();
     correct=correct&&bool(stop);SetEvent(offline_direct_resume);
    }else{
     float rejected=99;
     correct=correct&&invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&rejected,nullptr)&&rejected==0;
     SetEvent(offline_direct_resume);
    }
    if(!correct)return 0;
    checks+=2;
   }
   if(WaitForSingleObject(active_worker,20000)!=WAIT_OBJECT_0||state!=Idle)return 0;
   if(request.mode==68)lifecycle_gate.phase_end();
   if(hazards.load()||!lifecycle_gate.offline_probe_unlocked())return 0;
   if(word&&InterlockedCompareExchange(word,0,0)!=(request.mode==63?0x1000:0))return 0;
   const bool map_read=request.mode==62||request.mode==66||request.mode==69||request.mode==70||request.mode==72||request.mode==74||request.mode>=75;
   if(bool(offline_direct_map_reads)!=map_read)return 0;
   if(request.mode==70&&(!lifecycle_gate.faulted()||!broken||ready))return 0;
   if(request.mode==78&&!broken)return 0;
   if(request.mode==79&&(lifecycle_gate.faulted()||!broken||ready))return 0;
   CloseHandle(active_worker);CloseHandle(completed);
   if(pause){CloseHandle(offline_direct_entered);CloseHandle(offline_direct_resume);CloseHandle(offline_direct_cancelled);}
   return checks+4;
  }
  if(request.mode==39){
   offline_invoke=invoke;operation_original=offline_arm_mid_operation;area_original=offline_area;
   if(operation_hook(0xaaaa,request.operation_state,0xcccc,0xdddd)!=77||GetLastError()!=0x12345678||state!=Armed||selected_scope.active||selected_depth||offline_seen_selection.copied)return 0;
   {std::ofstream stop(output_directory/L"STOP",std::ios::binary);stop<<"Owned pre-arm operation cancellation\n";if(!stop)return 0;}
   if(!active_worker||WaitForSingleObject(active_worker,20000)!=WAIT_OBJECT_0||state!=Idle||!broken)return 0;
   CloseHandle(active_worker);active_worker=nullptr;CloseHandle(completed);completed=nullptr;return checks+4;
  }
  float scalar{};
  if(request.mode==60){
   offline_command_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);offline_command_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);
   if(!offline_command_entered||!offline_command_resume)return 0;
   auto generation=state.generation();bool first_ok{};
   std::thread first([&]{first_ok=invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&scalar,nullptr);});
   bool entered=WaitForSingleObject(offline_command_entered,10000)==WAIT_OBJECT_0;
   float rejected=99;
   bool refused=entered&&invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&rejected,nullptr)&&rejected==0;
   bool untouched=state.at(generation,Idle)&&!active_worker&&!pending;
   SetEvent(offline_command_resume);first.join();CloseHandle(offline_command_entered);CloseHandle(offline_command_resume);
   offline_command_entered=offline_command_resume=nullptr;
   if(!refused||!untouched||!first_ok||scalar!=1||!state.at(generation+1,Armed)||!active_worker)return 0;
   checks+=4;
  }else if(!invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&scalar,nullptr)||scalar!=1||state!=Armed)return 0;
  ++checks;
  auto capture_id=metadata.capture_id;scalar=99;
  if(!invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&scalar,nullptr)||scalar!=0||capture_id!=metadata.capture_id||state!=Armed)return 0;++checks;
  SetLastError(0x12345678);
  if(request.mode==61){
   operation_original=offline_operation;area_original=offline_area;
   offline_scope_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);offline_scope_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);
   if(!offline_scope_entered||!offline_scope_resume)return 0;
   auto generation=state.generation();bool stale_ok{};
   auto run_operation=[&]{return operation_hook(0xaaaa,request.operation_state,0xcccc,0xdddd)==77;};
   std::thread stale([&]{offline_stale_scope=true;stale_ok=run_operation();});
   bool entered=WaitForSingleObject(offline_scope_entered,10000)==WAIT_OBJECT_0;
   bool first=entered&&run_operation()&&WaitForSingleObject(active_worker,10000)==WAIT_OBJECT_0&&state.at(generation,Idle);
   bool rearmed=first&&invoke(nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,&scalar,nullptr)&&scalar==1&&state.at(generation+1,Armed)&&metadata.capture_id!=capture_id;
   auto second_id=metadata.capture_id;last_copy_reads=0;
   SetEvent(offline_scope_resume);stale.join();CloseHandle(offline_scope_entered);CloseHandle(offline_scope_resume);
   offline_scope_entered=offline_scope_resume=nullptr;
   if(!rearmed||!stale_ok||!state.at(generation+1,Armed)||last_copy_reads||metadata.capture_id!=second_id||!run_operation()||!last_copy_reads)return 0;
   checks+=6;
  }else if(request.mode==59){
   initializer_original=offline_phase_cpp;if(!offline_phase_cpp_probe(initializer_hook)||!lifetime_phase_failed||!broken||ready||!lifecycle_gate.faulted()||hazards.load()||last_copy_reads)return 0;
   auto before=epoch.load();destructor_original=reset_original=offline_inert_phase;
   if(destroy_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||reset_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||epoch.load()!=before||offline_inert_visits!=2)return 0;
  }else if(request.mode==50){
   offline_copy_entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);offline_copy_resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);if(!offline_copy_entered||!offline_copy_resume)return 0;
   offline_copy_pause=true;destructor_original=offline_phase_mutation;operation_original=offline_operation;area_original=offline_area;
   std::atomic<bool> attempting{},blocked{},phase_ok{};
   std::thread phase([&]{WaitForSingleObject(offline_copy_entered,10000);attempting=true;phase_ok=destroy_hook(0,0,0,0)==3;offline_phase_done=true;});
   std::thread release([&]{WaitForSingleObject(offline_copy_entered,10000);while(!attempting)SwitchToThread();Sleep(20);blocked=!offline_phase_mutated;SetEvent(offline_copy_resume);});
   bool operation_ok=operation_hook(0xaaaa,request.operation_state,0xcccc,0xdddd)==77;
   phase.join();release.join();CloseHandle(offline_copy_entered);CloseHandle(offline_copy_resume);offline_copy_entered=offline_copy_resume=nullptr;
   if(!operation_ok||!blocked||!phase_ok||!offline_phase_mutated||!last_copy_reads||!lifecycle_gate.offline_probe_unlocked())return 0;
  }else if(request.mode==52||request.mode==53){
   uint64_t map{},source{};if(!checked_read(nullptr,request.proc+0x20,&map,8)||!checked_read(nullptr,map,&source,8))return 0;
   offline_copy_fault_at=request.mode==52?request.proc+0x20:source;destructor_original=offline_phase_mutation;operation_original=offline_operation;area_original=offline_area;
   if(!offline_lifecycle_exception()){SetLastError(5601);return 0;}
   if(offline_phase_mutated){SetLastError(5602);return 0;}
   if(!lifecycle_gate.faulted()){SetLastError(5603);return 0;}
   if(!lifecycle_gate.offline_probe_unlocked()){SetLastError(5604);return 0;}
   if(hazards.load()){SetLastError(5605);return 0;}
   std::thread source_cleanup([&]{source_recorder.mark(source);});source_cleanup.join();
   auto before=epoch.load();destructor_original=reset_original=offline_inert_phase;
   if(destroy_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||GetLastError()!=0x1122ccaa||reset_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||GetLastError()!=0x1122ccaa||offline_inert_visits!=2||hazards.load()||epoch.load()!=before||!lifecycle_gate.faulted()||!lifecycle_gate.offline_probe_unlocked()){SetLastError(5606);return 0;}
  }else if(request.mode>=24){
   operation_original=offline_operation;area_original=offline_area;
   if(request.mode==37){
    d5ar_area_entry(0,request.area_query,request.operation_reference,module_base+0x21b26c1,0x43160000,0x40000000);
    if(area_hook(0,request.area_query,150.0f,2.0f)!=12||state!=Armed)return 0;++checks;
    *reinterpret_cast<uint8_t*>(request.operation_state+0x630)=1;
    if(operation_hook(0xaaaa,request.operation_state,0xcccc,0xdddd)!=77||state!=Armed||selected_scope.active)return 0;++checks;
    *reinterpret_cast<uint8_t*>(request.operation_state+0x630)=0;
   }
   if(request.mode==31){if(!offline_operation_exception()||GetLastError()!=0xabcdef02)return 0;}
   else if(operation_hook(0xaaaa,request.operation_state,0xcccc,0xdddd)!=77||GetLastError()!=0x12345678)return 0;
   if(selected_depth||selected_scope.active)return 0;
   if((request.mode==25||request.mode==37)&&(!offline_seen_selection.copied||!offline_seen_selection.linked||offline_seen_selection.ambiguous))return 0;
   if(request.mode==36&&(!offline_seen_selection.copied||offline_seen_selection.linked))return 0;
   if(request.mode==26&&(!offline_seen_selection.copied||!offline_seen_selection.linked||offline_seen_selection.formid!=0x12345))return 0;
   if((request.mode==27||request.mode==32||request.mode==33||request.mode==34||request.mode==40)&&offline_seen_selection.copied)return 0;
   if((request.mode==28||request.mode==29)&&(!offline_seen_selection.ambiguous||offline_seen_selection.linked))return 0;
   if(request.mode==35&&(!offline_recycled||!offline_seen_selection.copied||!offline_seen_selection.linked))return 0;
   if(request.mode==41&&(!offline_nested_area_ignored||!offline_seen_selection.copied||!offline_seen_selection.linked))return 0;
   if(request.mode==32){if(state!=Armed)return 0;std::ofstream stop(output_directory/L"STOP",std::ios::binary);stop<<"Owned stale-generation cancellation control\n";if(!stop)return 0;}
  }else if(request.mode==21){point_original=offline_point;initializer_original=offline_initializer;auto before=epoch.load();if(initializer_hook(0xaaaa,0xbbbb,0xcccc,0xdddd)!=0xaaaa||GetLastError()!=0x87654321||hazards.load()||epoch.load()!=before+2)return 0;}else if(request.mode==16||request.mode==17){point_original=offline_point;if(!offline_exception_probe(request.proc)||GetLastError()!=0xabcdef01)return 0;}else if(request.mode>=6&&request.mode!=19&&request.mode!=24){
   area_original=offline_area;operation_original=offline_scoped_area;
   if(operation_hook(0xaaaa,request.operation_state,0xcccc,0xdddd)!=12||GetLastError()!=0x12345678)return 0;
  }else{point_original=offline_point;if(point_hook(request.proc,0,0,0)!=11||GetLastError()!=0x12345678)return 0;}
  ++checks;
  if((request.mode==49||request.mode==51||request.mode==56)&&last_copy_reads)return 0;
  if((request.mode==38||request.mode==55)&&last_copy_reads!=5)return 0;
  if(request.mode==54&&last_copy_reads!=1)return 0;
  if((request.mode==56||request.mode==57)&&!offline_proc_reused)return 0;
  bool expected_disabled=request.mode==1||request.mode==2||request.mode==3||request.mode==16||request.mode==17||request.mode==31||request.mode==32||request.mode==42||request.mode==52||request.mode==53||request.mode==50||request.mode==56||request.mode==59;
  if(!active_worker||WaitForSingleObject(active_worker,20000)!=WAIT_OBJECT_0||state!=Idle||broken.load()!=expected_disabled)return 0;++checks;
  CloseHandle(active_worker);active_worker=nullptr;CloseHandle(completed);completed=nullptr;
  return checks;
 }catch(...){return 0;}
}

extern "C" void d5ar_capture_source_free(uint64_t source,uint64_t size,uint64_t caller_return,uint64_t) noexcept {
 auto saved=GetLastError();
 __try {
  if(size!=0x1a0||(caller_return!=d5ar::module_base+0x982afd&&caller_return!=d5ar::module_base+0x982c37))d5ar::source_recorder.unavailable();
  else d5ar::source_recorder.mark(source);
 } __finally {SetLastError(saved);}
}
