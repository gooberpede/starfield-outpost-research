// SPDX-License-Identifier: GPL-3.0-or-later
// The same compiled hooks, patch installer, queue and worker run in this host.
#include "transport.h"
#include <psapi.h>

#include <thread>
#include <mutex>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <cstdio>
#include <source_location>
#include <array>
#include "emitters.generated.h"
extern "C" {
uint64_t fixture_provider(uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t invoke_lookup(uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t invoke_descriptor(uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t invoke_normalizer(uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t invoke_sample(uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t invoke_cold(uint64_t,uint64_t,uint64_t,uint64_t);
void invoke_generate(uint64_t,uint64_t,uint64_t,uint32_t,uint64_t,uint64_t);
uint64_t fixture_reset(uint64_t,uint64_t,uint64_t,uint64_t),fixture_destroy(uint64_t,uint64_t,uint64_t,uint64_t),fixture_erase(uint64_t,uint64_t,uint64_t,uint64_t),fixture_clear(uint64_t,uint64_t,uint64_t,uint64_t),fixture_retire(uint64_t,uint64_t,uint64_t,uint64_t);
uint64_t invoke_reserve(uint64_t,uint64_t,uint64_t,uint64_t);
void fixture_birth(uint64_t,uint64_t,uint64_t,uint64_t);
void at_birth(),at_published(),at_reserve(),at_stored();
void at_selected(),at_visited(),at_lookup(),at_descriptor(),at_generate(),at_sample(),at_cold(),at_normalizer();
extern uint64_t bridge_pc_table_begin[],bridge_pc_table_end[];
}
namespace winner {extern std::atomic<bool> fixture_pause;extern std::atomic<unsigned> fixture_flush_pause_ms;}
namespace {
using namespace winner;
std::recursive_mutex native_lock;
std::mutex oracle_lock;
std::vector<std::string> oracle_rows;
std::atomic<U> host_allocations{};
std::atomic<U> host_resets{};
bool oracle_enabled{};
bool offer_oracle_enabled{};
std::atomic<U> host_offers[18]{};
struct Model {
 alignas(8) unsigned char proc[0x140]{},source_bytes[0x70]{},descriptor[0x2c]{};
 unsigned char additional_sources[3][0x70]{};
 alignas(8) unsigned char replacement_proc[0x140]{};
 U proc_identity=U(proc);U source=U(source_bytes);int32_t query[2]{10,11};
 std::atomic<U> installed_owner{U(proc)};
 int32_t source_origin[2]{0,0};double geographic[2]{1.25,-2.5};
 unsigned cursor_count=1;
 U mask=3;bool hit{},skip{},absent{},bad_read{},nested{},did_nested{},interrupted{},loss_inside{},bad_descriptor{};
 unsigned birth_behavior{};bool noaccess{},retire_lookup{},reset_lookup{};
 U host_allocation=++host_allocations,geometry{};
 unsigned generation_outcome{};bool reserve_throw{},skip_store{},retire_before_store{},reset_before_generate{},store_fault{},owner_replace{};
 bool* shared_hit=&hit;
 bool omit_lookup{},omit_descriptor{},omit_generate{},omit_sample{};
 bool crash_sample{},double_sample{},reset_overlap{},descriptor_change{},reset_before_lookup{},temporary_descriptor{};
 bool pause_before_lookup{},delay_reset_closeout{};
 HANDLE entered_event{},resume_event{};
 std::atomic<unsigned>* arrivals{};unsigned expected_arrivals=1;
 U visited{};bool born{},reserve_fail{};U visits[256]{},grid[8]{},publication{};
 template<class T> void put(unsigned char* p,unsigned offset,T value){memcpy(p+offset,&value,sizeof value);}
 Model(){grid[3]=U(&publication);put(proc,0x28,U(8));put(source_bytes,0,uint32_t(0x29d20e));put(source_bytes,0x10,int32_t(0));put(source_bytes,0x14,int32_t(0));
  put(source_bytes,0x38,uint8_t(0));put(source_bytes,0x3c,int32_t(195));put(source_bytes,0x40,int32_t(109));put(source_bytes,0x4c,int32_t(8));
  put(source_bytes,0x68,U(0x123456));put(descriptor,0,uint8_t(0));put(descriptor,4,int32_t(195));put(descriptor,8,int32_t(109));put(descriptor,20,int32_t(8));}
};
thread_local Model* model{};
thread_local unsigned cursor_index{};
struct Cursor {alignas(8) unsigned char cell[0x40]{},context[0x40]{},chunk[0x108]{};};
thread_local Cursor cursor{};
unsigned char* native_emitters{};
std::thread overlap_worker;
U fixture_origin{};
std::atomic<U> bridge_checks{};
void check(bool ok,std::source_location location=std::source_location::current()){if(!ok){fprintf(stderr,"fixture assertion line %u\n",location.line());throw std::runtime_error("native fixture assertion");}}
void oracle(const char* operation,Model& m,U a=0,U b=0,U c=0,U d=0){
 if(offer_oracle_enabled){
  struct Correspondence {const char* operation;unsigned kind;};
  const Correspondence kinds[]{{"provider-begin",1},{"selected-native",2},{"visited-native",3},{"protected-map",4},{"descriptor-consumed",5},{"generator-begin",6},{"ordinary-sample",7},{"generator-output",8},{"provider-return",9},{"native-empty-reset",12},{"constructor-begin",14},{"publication-store",15},{"reserve-success",16},{"reserve-failed",16},{"visited-store",17}};
  for(const auto& kind:kinds)if(!strcmp(kind.operation,operation)){++host_offers[kind.kind];break;}
 }
 if(!oracle_enabled)return;
 LARGE_INTEGER ticks{};QueryPerformanceCounter(&ticks);
 std::lock_guard lock(oracle_lock);
 oracle_rows.push_back("{\"operation\":"+sor::quote(operation)+",\"host_allocation\":"+std::to_string(m.host_allocation)+",\"host_reset_serial\":"+std::to_string(host_resets.load())+",\"source\":"+std::to_string(m.source)+",\"proc\":"+std::to_string(m.proc_identity)+",\"thread\":"+std::to_string(GetCurrentThreadId())+",\"ticks\":"+std::to_string(ticks.QuadPart)+",\"query\":["+std::to_string(m.query[0])+","+std::to_string(m.query[1])+"],\"a\":"+std::to_string(a)+",\"b\":"+std::to_string(b)+",\"c\":"+std::to_string(c)+",\"d\":"+std::to_string(d)+"}");
}
U call(Model& m){
 auto* saved=model;unsigned saved_index=cursor_index;Cursor saved_cursor=cursor;model=&m;cursor_index=0;cursor={};
 struct Restore {Model* saved;unsigned index;Cursor cursor;~Restore(){model=saved;cursor_index=index;::cursor=cursor;}} restore{saved,saved_index,saved_cursor};
 if(!m.born&&m.source>=0x10000){oracle("constructor-begin",m);fixture_birth(m.source,U(m.grid),*(U*)(m.source+0x68),m.birth_behavior);for(unsigned i=1;i<m.cursor_count;++i){memcpy(m.additional_sources[i-1],m.source_bytes,0x70);m.put(m.additional_sources[i-1],0,uint32_t(0x29d20e+i));fixture_birth(U(m.additional_sources[i-1]),U(m.grid),*(U*)(m.additional_sources[i-1]+0x68),0);}m.born=true;}
 oracle("provider-begin",m,m.visited);U result=fixture_provider(m.proc_identity,m.bad_read?1:U(m.query),U(&m),m.visited);oracle("provider-return",m,result);check(result==0x12345);return result;
}
void forced_retry(){fixture_retry_failures=1;Event e{};e.kind=Ready;check(!emit(e));}
void wait_durable(){U limit=enqueue.load()-fixture_origin;for(unsigned i=0;i<60000&&acknowledged.load()<limit&&!broken.load();++i)Sleep(1);check(acknowledged.load()>=limit);}
void unwind_probe(){
 // Independent stack contents describe fixture_provider's declared assembly
 // frame. No exception is raised or suppressed by this metadata experiment.
 alignas(16) U stack[512]{};U original_sp=U(stack)+256;
 const U expected_rip=0x123456789abcULL;
 *(U*)(original_sp+0x3d8)=0x13131313;*(U*)(original_sp+0x3e0)=0x12121212;
 *(U*)(original_sp+0x3e8)=0xd1d1d1d1;*(U*)(original_sp+0x3f0)=0x51515151;
 *(U*)(original_sp+0x3f8)=expected_rip;
 DWORD64 image{};auto* entry=RtlLookupFunctionEntry(U(&at_selected),&image,nullptr);check(entry!=nullptr);
 *(U*)(original_sp+0x3d0)=0xb0b0b0b0;
 CONTEXT context{};context.ContextFlags=CONTEXT_FULL;context.Rip=U(&at_selected);context.Rsp=original_sp;context.Rbp=original_sp;
 PVOID handler{};DWORD64 establisher{};
 RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,context.Rip,entry,&context,&handler,&establisher,nullptr);
 bool original_ok=context.Rip==expected_rip&&context.Rsp==original_sp+0x400&&context.Rbp==0xb0b0b0b0&&context.R13==0x13131313&&context.R12==0x12121212&&context.Rdi==0xd1d1d1d1&&context.Rsi==0x51515151;
 check(original_ok);
 std::string rows="[{\"case\":\"original-provider\",\"actual_RtlVirtualUnwind\":true,\"correct\":true}";
 void* bridges[]{(void*)&selected_bridge,(void*)&visited_bridge,(void*)&birth_bridge,(void*)&published_bridge,(void*)&stored_bridge};
 const char* names[]{"selected-bridge","visited-bridge","birth-bridge","published-bridge","stored-bridge"};
 for(unsigned i=0;i<5;++i){
  auto* bytes=(unsigned char*)bridges[i];unsigned offset=0;
  for(unsigned n=0;n<128;++n)if(bytes[n]==0x48&&bytes[n+1]==0x81&&bytes[n+2]==0xec&&bytes[n+3]==0x80&&bytes[n+4]==0&&bytes[n+5]==0&&bytes[n+6]==0){offset=n+7;break;}
  check(offset!=0);U pc=U(bytes)+offset+3;auto* metadata=RtlLookupFunctionEntry(pc,&image,nullptr);
  U bridge_sp=U(stack)+2048;*(U*)(bridge_sp+192)=0xb0b0b0b0;*(U*)(bridge_sp+200)=expected_rip;
  CONTEXT bridge_context{};bridge_context.ContextFlags=CONTEXT_FULL;bridge_context.Rip=pc;bridge_context.Rsp=bridge_sp;bridge_context.Rbp=bridge_sp;
  bool correct=false;
  if(metadata){RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,pc,metadata,&bridge_context,&handler,&establisher,nullptr);
   correct=bridge_context.Rip==expected_rip&&bridge_context.Rsp==bridge_sp+208&&bridge_context.Rbp==0xb0b0b0b0;}
  rows+=",{\"case\":"+sor::quote(names[i])+",\"pc\":"+std::to_string(pc)+",\"metadata_present\":"+(metadata?"true":"false")+",\"actual_RtlVirtualUnwind\":"+(metadata?"true":"false")+",\"correct\":"+(correct?"true":"false")+",\"active_bridge_save_bytes\":200}";
 }
 // Walk every assembler-labeled instruction boundary. The context oracle is
 // built from actual PUSH/SUB/MOV/LEA/POP instruction bytes, not unwind codes.
 U previous_begin=0,entry_sp=U(stack)+2048;CONTEXT simulated{};
 for(auto* item=bridge_pc_table_begin;item<bridge_pc_table_end;++item){
  U pc=*item;auto* metadata=RtlLookupFunctionEntry(pc,&image,nullptr);check(metadata!=nullptr);
  U begin=image+metadata->BeginAddress;
  if(begin!=previous_begin){simulated={};simulated.ContextFlags=CONTEXT_FULL;simulated.Rsp=entry_sp;simulated.Rbp=0xb0b0b0b0;*(U*)entry_sp=expected_rip;previous_begin=begin;}
  auto test=simulated;test.Rip=pc;RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,pc,metadata,&test,&handler,&establisher,nullptr);
  bool correct=test.Rip==expected_rip&&test.Rsp==entry_sp+8&&test.Rbp==0xb0b0b0b0;
  rows+=",{\"case\":\"bridge-instruction-boundary\",\"pc\":"+std::to_string(pc)+",\"offset\":"+std::to_string(pc-begin)+",\"actual_RtlVirtualUnwind\":true,\"correct\":"+(correct?"true":"false")+"}";
  const auto* instruction=(const unsigned char*)pc;
  if(instruction[0]>=0x50&&instruction[0]<=0x57){simulated.Rsp-=8;*(U*)simulated.Rsp=instruction[0]==0x55?simulated.Rbp:0x11111111;}
  else if(instruction[0]==0x41&&instruction[1]>=0x50&&instruction[1]<=0x57){simulated.Rsp-=8;*(U*)simulated.Rsp=0x11111111;}
  else if(instruction[0]==0x9c){simulated.Rsp-=8;*(U*)simulated.Rsp=0x202;}
  else if(instruction[0]==0x9d)simulated.Rsp+=8;
  else if(instruction[0]==0x48&&instruction[1]==0x81&&instruction[2]==0xec){uint32_t amount{};memcpy(&amount,instruction+3,4);simulated.Rsp-=amount;}
  else if(instruction[0]==0x48&&((instruction[1]==0x8b&&instruction[2]==0xec)||(instruction[1]==0x89&&instruction[2]==0xe5)))simulated.Rbp=simulated.Rsp;
  else if(instruction[0]==0xff&&instruction[1]==0xb4&&instruction[2]==0x24){simulated.Rsp-=8;*(U*)simulated.Rsp=0x202;}
  else if(instruction[0]==0x48&&instruction[1]==0x8d&&instruction[2]==0xa5){int32_t displacement{};memcpy(&displacement,instruction+3,4);simulated.Rsp=simulated.Rbp+displacement;}
  else if(instruction[0]==0x5d){simulated.Rbp=*(U*)simulated.Rsp;simulated.Rsp+=8;}
 }
 // The sole stack-changing generated entry trampoline mirrors the exact
 // independently pinned erase prologue, then jumps into the original frame.
 U trampoline=U(fences[2]);U trampoline_entry=U(stack)+2048;
 const unsigned offsets[]{0,2,3,4,8,18};const unsigned used[]{0,8,16,24,72,72};
 for(unsigned i=0;i<6;++i){
  CONTEXT value{};value.ContextFlags=CONTEXT_FULL;value.Rip=trampoline+offsets[i];value.Rsp=trampoline_entry-used[i];
  value.Rbx=0xb3b3b3b3;value.Rsi=0x51515151;value.Rdi=0xd1d1d1d1;
  *(U*)trampoline_entry=expected_rip;*(U*)(trampoline_entry-8)=0xb3b3b3b3;*(U*)(trampoline_entry-16)=0x51515151;*(U*)(trampoline_entry-24)=0xd1d1d1d1;
  auto* metadata=RtlLookupFunctionEntry(value.Rip,&image,nullptr);bool correct=false;
  if(metadata){RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,value.Rip,metadata,&value,&handler,&establisher,nullptr);correct=value.Rip==expected_rip&&value.Rsp==trampoline_entry+8&&value.Rbx==0xb3b3b3b3&&value.Rsi==0x51515151&&value.Rdi==0xd1d1d1d1;}
  rows+=",{\"case\":\"erase-trampoline-boundary\",\"offset\":"+std::to_string(offsets[i])+",\"actual_RtlVirtualUnwind\":"+(metadata?"true":"false")+",\"correct\":"+(correct?"true":"false")+"}";
 }
 rows+="]\n";check(sor::write_new(session/L"unwind-probe.json",rows));
}
}
extern "C" void fixture_bridge_check(uint64_t* words,unsigned phase){
 for(unsigned i=0;i<6;++i)check(words[i]==0x1111111111111111ULL*(i+1));
 check(words[6]==model->source);check((words[7]&0x8c5)==((phase==0||!model->visited)?0x44:0));
 for(unsigned i=0;i<12;++i)check(words[8+i]==0x0101010101010101ULL*(i/2+1));
 check(GetLastError()==0x9abc);++bridge_checks;
}
extern "C" uint64_t fixture_cursor(){
 auto& m=*model;if(m.absent||cursor_index>=m.cursor_count)return 0;
 if(!cursor_index){
  for(unsigned i=0;i<m.cursor_count;++i){
   U source=m.source;
   if(m.cursor_count>1){auto* selected=i?m.additional_sources[i-1]:m.source_bytes;memcpy(selected,m.source_bytes,0x70);m.put(selected,0,uint32_t(0x29d20e+i));source=U(selected);}
   m.put(cursor.cell,0x18+i*8,source);
  }
  m.put(cursor.context,0x10,U(cursor.context+8));m.put(cursor.context,0x20,U(cursor.chunk));
  using Emitter=void(*)(U,U);unsigned offset=m.cursor_count==1?0x240:m.cursor_count==2?0x330:0x760;
  ((Emitter)(native_emitters+offset))(U(cursor.cell),U(cursor.context));
  uint32_t count{};memcpy(&count,cursor.context+0x38,4);check(count==(m.source?m.cursor_count:0));
  U tail{};memcpy(&tail,cursor.context+0x28,8);check(tail==(count?U(cursor.chunk)+8*count:0));
  if(!count)return 0;
 }
 U selected{};memcpy(&selected,cursor.chunk+cursor_index*8,8);if(m.cursor_count>1){m.source=selected;m.hit=false;}
 oracle("selected-native",m,selected);SetLastError(0x9abc);return U(cursor.chunk+cursor_index++*8);
}
extern "C" uint64_t native_reserve(uint64_t a,uint64_t,uint64_t,uint64_t){
 auto& m=*model;auto* count=(uint32_t*)a;
 if(m.reserve_throw){oracle("reserve-throw",m);throw std::runtime_error("disposable reserve exception");}
 if(m.reserve_fail||*count>=256){oracle("reserve-failed",m);return 0xffffffff;}
 *(U*)(a+8)=U(m.visits);((uint32_t*)a)[1]=256;
 U result=(*count)++;oracle("reserve-success",m,result,*count);return result;
}
extern "C" void fixture_publication_oracle(uint64_t source){check(model->publication==source);oracle("publication-store",*model,model->publication);}
extern "C" void fixture_store_oracle(uint64_t destination,uint64_t token){check(*(U*)destination==token);oracle("visited-store",*model,destination,token);}
extern "C" uint64_t fixture_publication_decision(uint64_t behavior){
 if(behavior==2)throw std::runtime_error("modeled constructor exception");
 return behavior;
}
extern "C" void fixture_after_token(uint64_t source){
 U consumed{};if(source>=0x10000)memcpy(&consumed,(void*)(source+0x68),8);
 oracle("visited-native",*model,model->visited&255,consumed);
 if(model->noaccess){DWORD old{};check(VirtualProtect((void*)source,4096,PAGE_NOACCESS,&old));}
}
extern "C" uint64_t native_lookup(uint64_t a,uint64_t b,uint64_t,uint64_t){
 check(a==model->proc_identity+0x10&&*(U*)b==model->source);
 if(model->retire_lookup)fixture_retire(model->source,0,0,0);
 if(model->reset_lookup)fixture_reset(model->proc_identity,0,0,0);
 U result=*model->shared_hit?2:8;oracle("protected-map",*model,result);SetLastError(0x1234);return result;
}
extern "C" uint64_t native_normalizer(uint64_t,uint64_t b,uint64_t,uint64_t){SetLastError(0x3456);return b;}
extern "C" uint64_t native_descriptor(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
 unsigned char copied[0x2c]{};int32_t request[2]{};
 if(!model->bad_descriptor){
  int32_t coarse{};memcpy(&coarse,(void*)(c+4),4);
  if(model->descriptor_change){int32_t changed=coarse+1;memcpy((void*)(c+4),&changed,4);}
  memcpy(copied,(void*)c,sizeof copied);memcpy((void*)(c+4),&coarse,4);
  copied[1]=0xa5;copied[2]=0x5a;copied[3]=0xc3;
 }
 memcpy(request,(void*)d,8);
 oracle("descriptor-consumed",*model,U(copied),U(request));
 invoke_normalizer(a,model->bad_descriptor?1:U(copied),U(request),0);
 SetLastError(0x3456);return b;
}
extern "C" uint64_t native_sample(uint64_t a,uint64_t b,uint64_t c,uint64_t d){check(a==0x10000&&b==U(model->geographic)&&c==0x3333&&d==0x4444);oracle("ordinary-sample",*model,model->mask,b);SetLastError(0x5678);return 0x1234567800000000ULL|model->mask;}
extern "C" uint64_t native_cold(uint64_t a,uint64_t b,uint64_t c,uint64_t d){check(a==model->proc_identity+0x40&&b==0x22&&c==0x33&&d==0x44);return 0xabc;}
extern "C" void reset_body(uint64_t proc){std::unique_lock lock(native_lock);check(proc==model->proc_identity);memset((void*)(proc+0x48),0,16);*model->shared_hit=false;++host_resets;oracle("native-empty-reset",*model,*(U*)(proc+0x48),*(U*)(proc+0x50));check(invoke_cold(proc+0x40,0x22,0x33,0x44)==0xabc);
 if(model->delay_reset_closeout){lock.unlock();check(SetEvent(model->entered_event));check(WaitForSingleObject(model->resume_event,60000)==WAIT_OBJECT_0);}}
extern "C" void native_generate(uint64_t source,uint64_t origin,uint64_t geographic,uint32_t owner,uint64_t biome,uint64_t output){
 auto& m=*model;check(source==m.source&&origin==U(m.source_origin)&&geographic==U(m.geographic)&&owner==0x5e0de&&biome==0x1111&&output==0x2222);
 check(origin!=U(m.query)&&geographic!=U(m.query)&&origin!=geographic);
 oracle("generator-begin",m,owner,biome,geographic,output);
 if(m.generation_outcome==3){oracle("generator-throw",m);throw std::runtime_error("disposable generator exception");}
 if(m.nested&&!m.did_nested){m.did_nested=true;Model inner;inner.mask=0;call(inner);}
 if(m.loss_inside)forced_retry();
 if(m.reset_overlap){overlap_worker=std::thread([&]{model=&m;fixture_reset(m.proc_identity,0,0,0);});
  for(unsigned i=0;i<2000&&!hazards.load();++i)Sleep(1);check(hazards.load()>0);}
 if(!m.skip&&!m.omit_sample){check(invoke_sample(0x10000,U(m.geographic),0x3333,0x4444)==(0x1234567800000000ULL|m.mask));check(GetLastError()==0x5678);}
 if(m.double_sample){U old=m.mask;m.mask=0;invoke_sample(0x10000,U(m.geographic),0x3333,0x4444);m.mask=old;}
 if(m.crash_sample){wait_durable();TerminateProcess(GetCurrentProcess(),73);}
 m.geometry=m.generation_outcome==1?0:m.generation_outcome==2?1:3;
 oracle("generator-output",m,m.geometry,m.generation_outcome);
}
extern "C" uint64_t fixture_driver(uint64_t frame,uint64_t proc){
 check(GetLastError()==0x9abc);
 auto& m=*model;
 if(m.pause_before_lookup){if(!m.arrivals||m.arrivals->fetch_add(1)+1==m.expected_arrivals)check(SetEvent(m.entered_event));check(WaitForSingleObject(m.resume_event,60000)==WAIT_OBJECT_0);}
 if(m.reset_before_lookup)fixture_reset(m.proc_identity,0,0,0);
 if(m.owner_replace){
  U previous=m.installed_owner.load();check(previous==proc);oracle("owner-component-retire",m,previous);
  fixture_destroy(previous,0,0,0);memcpy(m.replacement_proc,m.proc,sizeof m.proc);
  m.installed_owner.store(U(m.replacement_proc));U replacement=m.installed_owner.load();check(replacement!=previous);
  oracle("owner-component-replacement",m,replacement,previous);
 }
 if(m.interrupted)fixture_retire(m.source,0,0,0);
 std::lock_guard lock(native_lock);
 U result=m.omit_lookup?native_lookup(proc+0x10,frame+0x38,0,0):invoke_lookup(proc+0x10,frame+0x38,0,0);
 check(GetLastError()==0x1234);
 if(result==8){
  if(!m.omit_descriptor)invoke_descriptor(U(m.descriptor)-(m.temporary_descriptor?0x1c0:0xc8),0x20000,U(m.descriptor),U(m.query));
  if(m.reset_before_generate)fixture_reset(m.proc_identity,0,0,0);
  if(!m.omit_generate)invoke_generate(m.source,U(m.source_origin),U(m.geographic),0x5e0de,0x1111,0x2222);
  *m.shared_hit=true;
  U index=invoke_reserve(proc+0x48,0,*(uint32_t*)(proc+0x4c),8);
  if(m.store_fault){
   void* inaccessible=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_NOACCESS);check(inaccessible!=nullptr);
   m.put(m.proc,0x50,U(inaccessible));oracle("store-destination-inaccessible",m,U(inaccessible));wait_durable();
   std::string history;for(const auto& row:oracle_rows)history+=row+"\n";
   check(sor::write_new(session/L"host-oracle-before-store.jsonl",history));
  }
  if(m.retire_before_store){oracle("retirement-before-store",m);fixture_retire(m.source,0,0,0);}
  if(m.skip_store){oracle("store-skipped-after-reserve",m,index);return 0xffffffff;}
  return index;
 }return 0xffffffff;
}
extern "C" __declspec(dllexport) int D5X_Qualify(const wchar_t* output,const wchar_t* scenario){
 using namespace winner;
 try {
  wchar_t host[32768]{};check(GetModuleFileNameW(nullptr,host,32768));check(std::filesystem::path(host).filename()==L"sor-d5x-fixture.exe");
  session=output;check(!std::filesystem::exists(session));check(std::filesystem::create_directories(session));
  std::wstring s=scenario;
  oracle_enabled=s.starts_with(L"p3-");
  offer_oracle_enabled=s==L"representative"||s==L"burst";
  U sequence_origin=s==L"sequence-wrap"?(1ULL<<32)-2:0;
  fixture_origin=sequence_origin;
  HMODULE fixture_module{};wchar_t fixture_path[32768]{};
  check(GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,(LPCWSTR)&D5X_Qualify,&fixture_module));
  check(GetModuleFileNameW(fixture_module,fixture_path,32768));
  auto input=std::filesystem::path(fixture_path).parent_path()/L"emitter-input.bin";
  HANDLE input_file=CreateFileW(input.c_str(),GENERIC_READ,FILE_SHARE_READ,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr);
  check(input_file!=INVALID_HANDLE_VALUE);unsigned char emitter_input[4096]{};LARGE_INTEGER input_size{};DWORD input_read{};
  bool input_ok=GetFileSizeEx(input_file,&input_size)&&input_size.QuadPart==4096&&ReadFile(input_file,emitter_input,4096,&input_read,nullptr)&&input_read==4096;
  CloseHandle(input_file);check(input_ok&&sor::sha_bytes(emitter_input,4096)==emitter_expected_hash);
  native_emitters=(unsigned char*)VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(native_emitters!=nullptr);
  memcpy(native_emitters,emitter_input,4096);DWORD old{};check(VirtualProtect(native_emitters,4096,PAGE_EXECUTE_READ,&old));check(FlushInstructionCache(GetCurrentProcess(),native_emitters,4096));
  std::vector<U> baseline;
  if(s==L"timing"){Model local;model=&local;for(unsigned i=0;i<1000;++i){local.hit=false;LARGE_INTEGER a{},b{};QueryPerformanceCounter(&a);call(local);QueryPerformanceCounter(&b);baseline.push_back(b.QuadPart-a.QuadPart);}}
  void* locations[]{(void*)&fixture_provider,(void*)&at_selected,(void*)&at_visited,(void*)&at_lookup,(void*)&at_descriptor,(void*)&at_generate,(void*)&at_sample,(void*)&fixture_reset,(void*)&fixture_destroy,(void*)&fixture_erase,(void*)&fixture_clear,(void*)&fixture_retire,(void*)&at_cold,(void*)&at_normalizer,(void*)&at_birth,(void*)&at_published,(void*)&at_reserve,(void*)&at_stored};
 unsigned lengths[]{7,8,13,5,5,5,5,5,5,8,5,5,5,5,12,11,5,11};std::string strings[18];const char* hashes[18]{};
  std::string sites="[";
  for(unsigned i=0;i<18;++i){strings[i]=sor::sha_bytes(locations[i],32);hashes[i]=strings[i].c_str();if(i)sites+=",";sites+="{\"index\":"+std::to_string(i)+",\"va\":"+std::to_string(U(locations[i]))+",\"guard_sha256\":"+sor::quote(strings[i])+"}";}
  sites+="]";
  if(s==L"guard-mismatch"){hashes[1]="invalid";check(!configure(locations,lengths,hashes));check(sor::write_new(session/L"refused.json","{\"boundary\":\"site_guard\",\"installed\":false}\n"));return 0;}
  check(configure(locations,lengths,hashes));
  if(s==L"p3-unwind-probe"){unwind_probe();return 0;}
  unsigned char nonce[16]{};check(BCryptGenRandom(nullptr,nonce,16,BCRYPT_USE_SYSTEM_PREFERRED_RNG)>=0);
  HMODULE self{};wchar_t path[32768]{};check(GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,(LPCWSTR)&D5X_Qualify,&self));check(GetModuleFileNameW(self,path,32768));
  LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);
  FILETIME process_created{},process_exited{},process_kernel{},process_user{};
  check(GetProcessTimes(GetCurrentProcess(),&process_created,&process_exited,&process_kernel,&process_user));
  identity="{\"schema\":\"sor-d5x/4\",\"retail\":false,\"sequence_origin\":"+std::to_string(sequence_origin)+",\"nonce\":"+sor::quote(sor::sha_bytes(nonce,16))+",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"dll_sha256\":"+sor::quote(sor::sha_file(path))+",\"host_sha256\":"+sor::quote(sor::sha_file(host))+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"sites\":"+sites;
  identity+=",\"creation_filetime\":"+std::to_string((U(process_created.dwHighDateTime)<<32)|process_created.dwLowDateTime);
  auto id=identity+"}\n";identity_hash=sor::sha_bytes(id.data(),id.size());check(sor::write_new(session/L"identity.json",id));
  raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  ack=CreateFileW((session/L"flush.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);check(raw!=INVALID_HANDLE_VALUE&&ack!=INVALID_HANDLE_VALUE);
  initialize_queue(sequence_origin);bool dirty=false;
  for(unsigned i=0;i<6000&&!sole_thread();++i)Sleep(10);
  check(install(edits,18,dirty));enabled=true;
  Event ready{};ready.kind=Ready;ready.epoch=epoch;emit(ready);
  HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);check(thread!=nullptr);
  for(unsigned i=0;i<3000&&!std::filesystem::exists(session/L"ready.json");++i)Sleep(1);
  check(std::filesystem::exists(session/L"ready.json"));
  check(sor::write_new(session/L"request.pending",std::string(32,'a')));
  check(MoveFileExW((session/L"request.pending").c_str(),(session/L"request.txt").c_str(),MOVEFILE_WRITE_THROUGH));
  std::string probe;bool probe_ok=sor::read_small(session/L"request.txt",probe,32);
  check(sor::write_new(session/L"request-reader-diagnostic.json","{\"inherited_stream_ok\":"+std::string(probe_ok?"true":"false")+",\"bytes\":"+std::to_string(probe.size())+"}\n"));
  for(unsigned i=0;i<60000&&!std::filesystem::exists(session/L"ack-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json")&&!broken.load();++i)Sleep(1);
  check(std::filesystem::exists(session/L"ack-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json"));
  if(s==L"controller-host"){
   // Commands affect this disposable host only. No new native hook semantics.
   check(sor::write_new(session/L"host-online.json","{\"disposable\":true}\n"));
   while(enabled.load()){
    auto command=session/L"fixture-command.txt";
    if(std::filesystem::exists(command)){
     HANDLE command_file=INVALID_HANDLE_VALUE;
     // Atomic publication can overlap a transient rename/scan handle. Match the
     // recorder request reader's sharing policy; never retry other error classes.
     for(unsigned attempt=0;attempt<200;++attempt){
      command_file=CreateFileW(command.c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr);
      if(command_file!=INVALID_HANDLE_VALUE)break;
      DWORD error=GetLastError();fprintf(stderr,"fixture command open error %lu attempt %u\n",error,attempt);
      if(error!=ERROR_SHARING_VIOLATION&&error!=ERROR_LOCK_VIOLATION)break;
      Sleep(5);
     }
     check(command_file!=INVALID_HANDLE_VALUE);LARGE_INTEGER command_size{};char command_bytes[128]{};DWORD command_read{};
     bool command_ok=GetFileSizeEx(command_file,&command_size)&&command_size.QuadPart>0&&command_size.QuadPart<=128&&ReadFile(command_file,command_bytes,DWORD(command_size.QuadPart),&command_read,nullptr)&&command_read==command_size.QuadPart;
     CloseHandle(command_file);check(command_ok);std::string action(command_bytes,command_read);
     check(std::filesystem::remove(command));
     if(action=="pause")fixture_flush_pause_ms=3000;
     else if(action=="write")fixture_fault=2;
     else if(action=="raw-flush")fixture_fault=3;
     else if(action=="ack-flush")fixture_fault=4;
     else if(action=="ack-write")fixture_fault=5;
     else if(action=="disk")fixture_fault=1;
     else if(action=="exit")fixture_fault=6;
     else if(action=="guard")fixture_fault=7;
     else if(action=="missing-terminal")fixture_fault=8;
     else if(action=="loss")forced_retry();
     else check(false);
     check(sor::write_new(session/(L"command-"+std::wstring(action.begin(),action.end())+L".json"),"{\"accepted\":true}\n"));
    }
    Event event{};event.kind=Ready;event.epoch=epoch;emit(event);Sleep(2);
   }
   check(WaitForSingleObject(thread,60000)==WAIT_OBJECT_0);CloseHandle(thread);return 0;
  }
  Model m;model=&m;
  if(s!=L"prior-unknown"&&s!=L"ready-only")fixture_reset(m.proc_identity,0,0,0);
  std::vector<U> timing;
  void* protected_source{};
  if(s==L"p3-real-reuse"||s==L"p3-detached-retirement"){
   protected_source=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(protected_source!=nullptr);
   memcpy(protected_source,m.source_bytes,0x70);m.source=U(protected_source);
  }
  if(s==L"p3-empty-output")m.generation_outcome=1;
  if(s==L"p3-partial-output")m.generation_outcome=2;
  if(s==L"p3-generator-throw")m.generation_outcome=3;
  if(s==L"p3-reserve-throw")m.reserve_throw=true;
  if(s==L"p3-reserve-fail")m.reserve_fail=true;
  if(s==L"p3-skipped-store")m.skip_store=true;
  if(s==L"p3-store-access-fault")m.store_fault=true;
  if(s==L"p3-owner-replacement-selected")m.owner_replace=true;
  if(s==L"p3-retire-before-store")m.retire_before_store=true;
  if(s==L"p3-reset-before-generate")m.reset_before_generate=true;
  if(s==L"p3-prerequisite-failure")m.skip=true;
  if(s==L"p3-map-hit"||s==L"p3-density-reuse")m.hit=true;
  if(s==L"p1-noaccess-lookup"||s==L"p1-retire-lookup"||s==L"p1-reset-lookup"){
   protected_source=VirtualAlloc(nullptr,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(protected_source!=nullptr);
   memcpy(protected_source,m.source_bytes,0x70);m.source=U(protected_source);m.noaccess=true;
   m.retire_lookup=s==L"p1-retire-lookup";m.reset_lookup=s==L"p1-reset-lookup";
  }
  if(s==L"p1-unpublished")m.birth_behavior=1;
  if(s==L"p1-constructor-exception")m.birth_behavior=2;
  if(s==L"reserve-fail")m.reserve_fail=true;
  if(s==L"unknown-birth")m.born=true;
  if(s==L"mask-zero")m.mask=0;
  if(s==L"unexpected-mask")m.mask=254;
  if(s==L"descriptor-change")m.descriptor_change=true;
  if(s==L"temporary-descriptor")m.temporary_descriptor=true;
  if(s==L"post-reset-old-provider")m.reset_before_lookup=true;
  if(s==L"conflicting-mask")m.double_sample=true;
  if(s==L"overlap-reset")m.reset_overlap=true;
  if(s==L"null-cell")m.source=0;
  if(s==L"edge")m.cursor_count=2;
  if(s==L"corner")m.cursor_count=4;
  if(s==L"conflicting-mask")m.mask=3;
  if(s==L"bad-read")m.bad_read=true;
  if(s==L"bad-source")m.source=1;
  if(s==L"bad-descriptor")m.bad_descriptor=true;
  if(s==L"source-absent")m.absent=true;
  if(s==L"selection-only")m.visited=2;
  if(s==L"visited")m.visited=1;
  if(s==L"map-hit")m.hit=true;
  if(s==L"skip-sample")m.skip=true;
  if(s==L"nested")m.nested=true;
  if(s==L"interrupt")m.interrupted=true;
  if(s==L"in-flight-loss")m.loss_inside=true;
  if(s==L"missing-lookup")m.omit_lookup=true;
  if(s==L"missing-descriptor")m.omit_descriptor=true;
  if(s==L"missing-generator")m.omit_generate=true;
  if(s==L"missing-sample")m.omit_sample=true;
  if(s==L"crash-sample")m.crash_sample=true;
  if(s==L"crash-before")TerminateProcess(GetCurrentProcess(),71);
  if(s==L"unrelated-conversion")native_descriptor(0x10000,0x20000,U(m.descriptor),U(m.query));
  else if(s==L"orphan-sample")invoke_sample(0x10000,U(m.geographic),0x3333,0x4444);
  else if(s==L"p1-constructor-exception"){
   bool caught=false;try{call(m);}catch(const std::runtime_error&){caught=true;}check(caught&&!m.publication);
  }
  else if(s==L"p3-generator-throw"||s==L"p3-reserve-throw"){
   bool caught=false;try{call(m);}catch(const std::runtime_error&){caught=true;oracle("exception-caught",m);}
   check(caught&&current==nullptr&&conversion==nullptr&&!generating&&active.load()==0);
   check(*(uint32_t*)(m.proc+0x48)==0);oracle("unwind-state-restored",m);
  }
  else if(s!=L"ready-only"&&s!=L"schedule-old-first"&&s!=L"schedule-fresh-first"&&s!=L"reset-closeout"&&s!=L"p3-competing-map"&&s!=L"p3-detached-retirement"&&s!=L"p3-loss-recovery"&&s!=L"p3-loss-after-reset"&&s!=L"p3-loss-unknown-bounds"&&s!=L"p3-density-reuse")call(m);
  if(s==L"p3-density-reuse")oracle("density-aggregate-reuse-without-provider",m);
  if(s==L"p3-loss-recovery"||s==L"p3-loss-after-reset"||s==L"p3-loss-unknown-bounds"){
   oracle("forced-retry-loss",m);fixture_bounds_failure=s==L"p3-loss-unknown-bounds";forced_retry();fixture_bounds_failure=false;
   if(s==L"p3-loss-recovery"){oracle("recovery-reset",m);fixture_reset(m.proc_identity,0,0,0);}
   call(m);
  }
  if(s==L"p3-competing-map"){
   oracle("constructor-begin",m);fixture_birth(m.source,U(m.grid),*(U*)(m.source+0x68),0);m.born=true;
   std::array<Model,4> requests;std::vector<std::thread> workers;
   HANDLE entered=CreateEventW(nullptr,TRUE,FALSE,nullptr),resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(entered&&resume);std::atomic<unsigned> arrivals{};
   for(unsigned i=0;i<4;++i){auto& request=requests[i];request.born=true;request.source=m.source;request.host_allocation=m.host_allocation;request.proc_identity=m.proc_identity;request.shared_hit=&m.hit;
    request.query[0]=10+int(i);request.query[1]=11+int(i);request.pause_before_lookup=true;request.entered_event=entered;request.resume_event=resume;request.arrivals=&arrivals;request.expected_arrivals=4;
    workers.emplace_back([&,i]{call(requests[i]);});}
   check(WaitForSingleObject(entered,60000)==WAIT_OBJECT_0);check(SetEvent(resume));for(auto& worker:workers)worker.join();CloseHandle(entered);CloseHandle(resume);model=&m;
  }
  if(s==L"p3-detached-retirement"){
   m.pause_before_lookup=true;m.entered_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);m.resume_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(m.entered_event&&m.resume_event);
   std::thread detached([&]{call(m);});check(WaitForSingleObject(m.entered_event,60000)==WAIT_OBJECT_0);
   oracle("detached-retirement",m);fixture_retire(m.source,0,0,0);check(VirtualFree(protected_source,0,MEM_RELEASE));protected_source=nullptr;oracle("allocation-free",m);
   check(SetEvent(m.resume_event));detached.join();CloseHandle(m.entered_event);CloseHandle(m.resume_event);model=&m;
  }
  if(s==L"p3-positive-bypass"){
   U token{};memcpy(&token,m.source_bytes+0x68,8);
   auto count=*(uint32_t*)(m.proc+0x48);check(count==1&&m.visits[0]==token);
   m.visited=std::find(m.visits,m.visits+count,token)!=m.visits+count;
   oracle("visited-membership",m,m.visited,token);call(m);
  }
  if(s==L"p3-token-collision"||s==L"p3-same-geography-other-owner"){
   Model other;
   if(s==L"p3-token-collision"){other.proc_identity=m.proc_identity;other.shared_hit=&m.hit;m.hit=false;other.put(other.source_bytes,0x3c,int32_t(196));}
   oracle("distinct-allocation-same-token",other);call(other);model=&m;
  }
  if(s==L"p3-real-reuse"){
   oracle("allocation-retire",m);fixture_retire(m.source,0,0,0);
   check(VirtualFree(protected_source,0,MEM_RELEASE));oracle("allocation-free",m);
   auto replacement=VirtualAlloc(protected_source,4096,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);check(replacement==protected_source);
   m.host_allocation=++host_allocations;memcpy(replacement,m.source_bytes,0x70);m.born=false;m.hit=false;
   oracle("allocation-reused",m);call(m);
  }
  if(protected_source){check(VirtualFree(protected_source,0,MEM_RELEASE));protected_source=nullptr;}
  if(s==L"later-bypass"){m.visited=1;call(m);}
  if(overlap_worker.joinable())overlap_worker.join();
  if(s==L"post-reset-old-provider"){Model other;other.proc_identity=m.proc_identity;call(other);}
  if(s==L"descriptor-collision"){Model other;other.proc_identity=m.proc_identity;other.mask=0;call(other);}
  if(s==L"reused-pointer"||s==L"reset"||s==L"clear"||s==L"destroy"||s==L"erase"){
   if(s==L"reset")fixture_reset(m.proc_identity,0,0,0);
   else if(s==L"clear")fixture_clear(m.proc_identity,0,0,0);
   else if(s==L"destroy")fixture_destroy(m.proc_identity,0,0,0);
   else if(s==L"erase")fixture_erase(m.proc_identity,0,0,0);
   else fixture_retire(m.source,0,0,0);
   m.hit=false;m.mask=0;call(m);
  }
  if(s==L"concurrent"||s==L"competing"){
   fixture_reset(m.proc_identity,0,0,0);std::vector<std::thread> workers;std::array<Model,8> locals;
   HANDLE entered=CreateEventW(nullptr,TRUE,FALSE,nullptr),resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(entered&&resume);std::atomic<unsigned> arrivals{};
   for(int i=0;i<8;++i){auto& local=locals[i];local.proc_identity=m.proc_identity;local.pause_before_lookup=true;local.entered_event=entered;local.resume_event=resume;local.arrivals=&arrivals;local.expected_arrivals=8;
    if(s==L"competing"){local.source=m.source;local.shared_hit=&m.hit;}else local.put(local.source_bytes,0x3c,int32_t(195+i));
    if(i%2){local.mask=0;local.query[0]=-2;local.query[1]=-2;}workers.emplace_back([&,i]{call(locals[i]);});}
   check(WaitForSingleObject(entered,60000)==WAIT_OBJECT_0);check(SetEvent(resume));for(auto& t:workers)t.join();CloseHandle(entered);CloseHandle(resume);
  }
  if(s==L"schedule-old-first"||s==L"schedule-fresh-first"){
   Model old;old.proc_identity=m.proc_identity;old.query[0]=-2;old.query[1]=-2;old.mask=0;old.pause_before_lookup=true;
   old.entered_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);old.resume_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(old.entered_event&&old.resume_event);
   std::thread delayed([&]{call(old);});check(WaitForSingleObject(old.entered_event,60000)==WAIT_OBJECT_0);
   fixture_reset(m.proc_identity,0,0,0);if(s==L"schedule-fresh-first")call(m);
   check(SetEvent(old.resume_event));delayed.join();if(s==L"schedule-old-first")call(m);
   CloseHandle(old.entered_event);CloseHandle(old.resume_event);
  }
  if(s==L"reset-closeout"){
   m.delay_reset_closeout=true;m.entered_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);m.resume_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(m.entered_event&&m.resume_event);
   std::thread resetter([&]{model=&m;fixture_reset(m.proc_identity,0,0,0);});check(WaitForSingleObject(m.entered_event,60000)==WAIT_OBJECT_0);
   Model during;during.proc_identity=m.proc_identity;call(during);
   check(SetEvent(m.resume_event));resetter.join();m.delay_reset_closeout=false;call(m);
   CloseHandle(m.entered_event);CloseHandle(m.resume_event);
  }
  if(s==L"loss-one"||s==L"loss-many"){
   fixture_pause=true;Sleep(30);for(int i=0;i<(s==L"loss-one"?1:37);++i)forced_retry();fixture_pause=false;Sleep(30);
   fixture_reset(m.proc_identity,0,0,0);m.mask=0;call(m);
  }
  if(s==L"stop-under-production"){
   wait_durable();std::vector<std::thread> producers;std::atomic<unsigned> started{};
   HANDLE started_event=CreateEventW(nullptr,TRUE,FALSE,nullptr);check(started_event!=nullptr);
   for(unsigned i=0;i<8;++i)producers.emplace_back([&]{if(started.fetch_add(1)+1==8)SetEvent(started_event);while(enabled.load()){Event e{};e.kind=Ready;e.epoch=epoch;emit(e);}});
   check(WaitForSingleObject(started_event,60000)==WAIT_OBJECT_0);check(sor::write_new(session/L"STOP","fixture STOP during active production\n"));
   for(auto& producer:producers)producer.join();CloseHandle(started_event);
  }
  if(s==L"representative"){
   wait_durable();fixture_flush_pause_ms=3000;Event trigger{};trigger.kind=Ready;emit(trigger);Sleep(100);
   std::vector<std::thread> producers;
   for(unsigned j=0;j<4;++j)producers.emplace_back([&]{Model local;model=&local;for(unsigned i=0;i<500;++i){local.hit=false;call(local);Sleep(1);}});
   for(auto& producer:producers)producer.join();model=&m;
   fixture_reset(m.proc_identity,0,0,0);fixture_destroy(m.proc_identity,0,0,0);fixture_erase(m.proc_identity,0,0,0);
   fixture_clear(m.proc_identity,0,0,0);fixture_retire(m.source,0,0,0);wait_durable();if(capacity==32768)check(drops==0);
  }
  if(s==L"burst"){
   wait_durable();fixture_flush_pause_ms=3000;
   Event trigger{};trigger.kind=Ready;emit(trigger);Sleep(100);
   std::vector<std::thread> producers;
   for(unsigned j=0;j<4;++j)producers.emplace_back([&]{for(unsigned i=0;i<3000;++i){Event e{};e.kind=Ready;emit(e);if(i%6==0)Sleep(1);}});
   for(auto& producer:producers)producer.join();wait_durable();
  }
  if(s==L"saturation"||s==L"timing"){
   fixture_pause=(s==L"saturation");std::vector<std::thread> producers;
   for(int j=0;j<8;++j)producers.emplace_back([&]{Model local;model=&local;for(int i=0;i<10000;++i){local.hit=false;call(local);}});
   for(auto& p:producers)p.join();fixture_pause=false;wait_durable();model=&m;
   fixture_reset(m.proc_identity,0,0,0);call(m);wait_durable();
   for(int i=0;i<1000;++i){if(i%10==0)wait_durable();m.hit=false;LARGE_INTEGER a{},b{};QueryPerformanceCounter(&a);call(m);QueryPerformanceCounter(&b);timing.push_back(b.QuadPart-a.QuadPart);}
  }
  wait_durable();
  if(s==L"crash-after")TerminateProcess(GetCurrentProcess(),72);
  if(s==L"write-fault"||s==L"flush-fault"||s==L"ack-fault"||s==L"disk-fault"||s==L"ack-write-fault"){
   fixture_fault=s==L"disk-fault"?1:s==L"write-fault"?2:s==L"flush-fault"?3:s==L"ack-write-fault"?5:4;Event e{};e.kind=Ready;emit(e);Sleep(80);
  }
  if(!std::filesystem::exists(session/L"STOP"))check(sor::write_new(session/L"STOP","operator fixture STOP\n"));check(WaitForSingleObject(thread,60000)==WAIT_OBJECT_0);CloseHandle(thread);
  std::sort(timing.begin(),timing.end());auto quantile=[&](size_t n){return timing.empty()?U(0):timing[(timing.size()-1)*n/100];};
  std::sort(baseline.begin(),baseline.end());auto base_quantile=[&](size_t n){return baseline.empty()?U(0):baseline[(baseline.size()-1)*n/100];};
  std::string scenario_ascii;for(wchar_t ch:s){check(ch>=0&&ch<128);scenario_ascii.push_back(char(ch));}
  PROCESS_MEMORY_COUNTERS memory{};memory.cb=sizeof memory;check(K32GetProcessMemoryInfo(GetCurrentProcess(),&memory,sizeof memory));
  check(sor::write_new(session/L"fixture.json","{\"scenario\":"+sor::quote(scenario_ascii)+",\"peak_working_set_bytes\":"+std::to_string(memory.PeakWorkingSetSize)+",\"peak_pagefile_bytes\":"+std::to_string(memory.PeakPagefileUsage)+",\"p50_ticks\":"+std::to_string(quantile(50))+",\"p95_ticks\":"+std::to_string(quantile(95))+",\"p99_ticks\":"+std::to_string(quantile(99))+",\"max_ticks\":"+std::to_string(quantile(100))+",\"baseline_p50_ticks\":"+std::to_string(base_quantile(50))+",\"baseline_p95_ticks\":"+std::to_string(base_quantile(95))+",\"baseline_p99_ticks\":"+std::to_string(base_quantile(99))+",\"baseline_max_ticks\":"+std::to_string(base_quantile(100))+",\"timing_count\":"+std::to_string(timing.size())+",\"abi_checks\":true,\"grid_traversals\":0}\n"));
  if(oracle_enabled){
   std::string history;for(const auto& row:oracle_rows)history+=row+"\n";
   check(sor::write_new(session/L"host-oracle.jsonl",history));
   check(sor::write_new(session/L"host-state.json","{\"publication\":"+std::to_string(m.publication)+",\"source\":"+std::to_string(m.source)+",\"host_allocation\":"+std::to_string(m.host_allocation)+",\"installed_owner\":"+std::to_string(m.installed_owner.load())+",\"visited_count\":"+std::to_string(*(uint32_t*)(m.proc+0x48))+",\"visited_first\":"+std::to_string(m.visits[0])+",\"geometry_units\":"+std::to_string(m.geometry)+",\"expected_geometry\":\"emulated host output, not retail geometry\"}\n"));
  }
  if(offer_oracle_enabled){
   // READY and lifecycle wrappers are counted from this finite host program,
   // separately from recorder telemetry or admitted record interpretation.
   host_offers[13]=s==L"burst"?12002:2;
   host_offers[10]=host_offers[11]=s==L"representative"?6:1;
   std::string rows="{\"scope\":\"independent finite host actions; not queue telemetry\",\"per_kind\":[";U total=0;
   for(unsigned i=0;i<18;++i){if(i)rows+=",";rows+=std::to_string(host_offers[i].load());total+=host_offers[i].load();}
   rows+="],\"total\":"+std::to_string(total)+"}\n";check(sor::write_new(session/L"host-offers.json",rows));
   check(total==enqueue.load()-fixture_origin+drops.load());
  }
  return 0;
 }catch(const std::exception& e){fprintf(stderr,"%s\n",e.what());return 91;}
}
