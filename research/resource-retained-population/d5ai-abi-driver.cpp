// SPDX-License-Identifier: GPL-3.0-or-later
// Independent exact-object ABI and Windows unwind oracle. No game or other
// process is opened; only the linked disposable object runs.
#define NOMINMAX
#include <Windows.h>
#include <cstdint>
#include <cstring>
#include <cstdio>
#include <stdexcept>
#include <vector>
#include <algorithm>
using U=uint64_t;
extern "C" {
 void d5ai_area_acquire(),d5ai_area_complete(),d5ai_area_preunlock(),d5ai_at_acquire();
 void d5ai_clobber(),d5ai_probe_complete(void*),d5ai_probe_preunlock(void*);
 U d5ai_invoke(U,U,U,uint32_t,uint32_t);
 U d5ai_acquire_original{};
}
unsigned checks{},unwind_checks{};bool complete_called{},preunlock_called{},area_called{};
void check(bool value){++checks;if(!value)throw std::runtime_error("independent ABI assertion");}
extern "C" U d5ai_native_acquire(U lock,U,U,U){check(lock==0x4040);return 0xabcdef12;}
extern "C" void d5ai_area_capture(U proc,U query,U consumer,uint32_t radius,uint32_t upper){
 check(proc==0x4000&&query==0x5050&&consumer==0x6060&&radius==0x11223344&&upper==0x55667788);area_called=true;d5ai_clobber();
}
extern "C" void d5ai_complete_capture(U iterator,U capacity,U diagnostic){check(iterator==0x9090&&capacity==0x1212&&diagnostic==0x103);complete_called=true;d5ai_clobber();}
extern "C" void d5ai_preunlock_capture(U result){check(result==0x103);preunlock_called=true;d5ai_clobber();}
U word(const unsigned char* p){U v{};memcpy(&v,p,8);return v;}
void abi(){
 alignas(16) unsigned char result[256]{};
 for(unsigned variant=0;variant<2;++variant){
  memset(result,0,sizeof result);if(variant)d5ai_probe_preunlock(result);else d5ai_probe_complete(result);
  const U wanted[]{0x101,variant?U(0x7004):U(0x102),variant?U(0xffffffff):U(0x103),0x108,0x109,0x110,0x111,0x7000,variant?U(0x9090):U(0x7777),0x1212,0x1313,0x1414,U(result),word(result+224)};
  for(unsigned i=0;i<14;++i)check(word(result+i*8)==wanted[i]);
  check((word(result+112)&1)==1);check(word(result+232)==word(result+240));check(word(result+248)==0x6161);
  for(unsigned i=128;i<224;++i)check(result[i]==0xff);
 }
 check(complete_called&&preunlock_called);
 d5ai_acquire_original=U(&d5ai_native_acquire);
 auto* call=(unsigned char*)&d5ai_at_acquire;check(call[0]==0xe8);
 auto delta=int64_t(U(&d5ai_area_acquire))-int64_t(U(call)+5);check(delta>=INT32_MIN&&delta<=INT32_MAX);
 DWORD old{},unused{};check(VirtualProtect(call,5,PAGE_EXECUTE_READWRITE,&old));int32_t displacement=int32_t(delta);memcpy(call+1,&displacement,4);check(VirtualProtect(call,5,old,&unused));check(FlushInstructionCache(GetCurrentProcess(),call,5));
 check(d5ai_invoke(0x4040,0x5050,0x6060,0x11223344,0x55667788)==0xabcdef12);check(area_called);
}
void virtual_context(U entry,U pc,unsigned pushes,unsigned allocation,bool frame,unsigned frame_offset=0,bool extra_push=false){
 alignas(16) U stack[256]{};const U sp=U(stack)+1024,old_rbp=0x12345000,caller=0x123456789;
 *(U*)sp=caller;*(U*)(sp-8)=old_rbp;
 CONTEXT context{};context.ContextFlags=CONTEXT_FULL;context.Rip=pc;context.Rsp=sp-pushes*8-allocation-(extra_push?8:0);context.Rbp=frame?sp-pushes*8-allocation+frame_offset:old_rbp;
 DWORD64 image{};auto* function=RtlLookupFunctionEntry(pc,&image,nullptr);check(function!=nullptr);
 void* handler{};DWORD64 establisher{};RtlVirtualUnwind(UNW_FLAG_NHANDLER,image,pc,function,&context,&handler,&establisher,nullptr);
 check(context.Rip==caller&&context.Rsp==sp+8&&context.Rbp==old_rbp);++unwind_checks;(void)entry;
}
void unwind(void(*function)(),bool acquire){
 U entry=U(function);DWORD64 image{};auto* table=RtlLookupFunctionEntry(entry,&image,nullptr);check(table!=nullptr);
 auto* info=(unsigned char*)(image+table->UnwindData);unsigned prologue=info[1];
 auto* p=(unsigned char*)entry;
 if(acquire){
  const unsigned char bytes[]{0x55,0x48,0x83,0xec,0x50,0x48,0x8d,0x6c,0x24,0x50};check(!memcmp(p,bytes,sizeof bytes));check(prologue==sizeof bytes);
  virtual_context(entry,entry,0,0,false);virtual_context(entry,entry+1,1,0,false);virtual_context(entry,entry+5,1,80,false);virtual_context(entry,entry+10,1,80,true,80);
 }else {
  const unsigned char bytes[]{0x55,0x9c,0x50,0x51,0x52,0x41,0x50,0x41,0x51,0x41,0x52,0x41,0x53,0x48,0x81,0xec,0x80,0,0,0,0x48,0x8b,0xec};check(!memcmp(p,bytes,sizeof bytes));check(prologue==sizeof bytes);
  const unsigned offsets[]{0,1,2,3,4,5,7,9,11,13};
  for(unsigned i=0;i<10;++i)virtual_context(entry,entry+offsets[i],i,0,false);
  virtual_context(entry,entry+20,9,128,false);virtual_context(entry,entry+23,9,128,true);
  const unsigned char flags_push[]{0xff,0xb4,0x24,0xb8,0,0,0};
  auto* end=(unsigned char*)(image+table->EndAddress);auto* found=std::search(p+prologue,end,std::begin(flags_push),std::end(flags_push));check(found!=end&&found[7]==0x9d);
  virtual_context(entry,U(found)+7,9,128,true,0,true);
 }
 auto* end=(unsigned char*)(image+table->EndAddress);
 for(auto* q=p+prologue;q<end;++q){
  if(acquire&&q+6<=end&&!memcmp(q,"\x48\x8d\x65\x00\x5d\xc3",6)){
   virtual_context(entry,U(q),1,80,true,80);virtual_context(entry,U(q)+4,1,0,true);break;
  }
  if(!acquire&&q+9<=end&&!memcmp(q,"\x48\x8d\xa5\xc0\x00\x00\x00\x5d\xc3",9)){
   virtual_context(entry,U(q),9,128,true);virtual_context(entry,U(q)+7,1,0,true);break;
  }
 }
}
int main(){SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);try{abi();unwind(&d5ai_area_acquire,true);unwind(&d5ai_area_complete,false);unwind(&d5ai_area_preunlock,false);printf("{\"checks\":%u,\"unwind_contexts\":%u,\"status\":\"PASS\"}\n",checks,unwind_checks);return 0;}catch(const std::exception& e){fprintf(stderr,"%s checks=%u unwind=%u\n",e.what(),checks,unwind_checks);return 1;}}
