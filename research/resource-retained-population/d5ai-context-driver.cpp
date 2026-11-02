// SPDX-License-Identifier: GPL-3.0-or-later
// Independent caller for the exact retained context-entry object and pinned
// context/fence source. Original entry instructions, argument forwarding,
// exception fences, guards and registered partial unwind are actually executed.
#include "d5ai_context.h"
#include <cstdio>
#include <stdexcept>
#include <source_location>
using namespace winner;
extern "C" {U d5ai_fixture_owner(U,U,U,U) noexcept(false);U d5ai_fixture_context_reset(U,U,U,U) noexcept(false);}
extern "C" U d5ai_native_life_holder(U,U,U,U){return 0;}
extern "C" U d5ai_native_life_collection(U,U,U,U){return 0;}
extern "C" U d5ai_native_life_mutation(U,U,U,U){return 0;}
unsigned checks{},unwind_checks{};bool throw_owner{},throw_reset{};
void check(bool yes,std::source_location where=std::source_location::current()){++checks;if(!yes){fprintf(stderr,"line %u\n",where.line());throw std::runtime_error("context oracle assertion");}}
extern "C" U d5ai_native_owner(U a,U b,U c,U d) noexcept(false){check(a==0x1111&&b==0x2222&&c==0x3333&&d==0x4444);if(throw_owner)throw std::runtime_error("owned owner throw");return 0x5555;}
extern "C" U d5ai_native_context_reset(U a,U b,U c,U d) noexcept(false){check(a==0x9999&&b==1&&c==0xaaaa&&d==0xbbbb);if(throw_reset)throw std::runtime_error("owned reset throw");return 0xccdd;}
void check_pair(U reason,bool exception){Event a{},b{};check(pop(a)&&pop(b));check(a.kind==10&&b.kind==11&&a.a==reason&&b.a==reason);check(a.hazards==1&&b.hazards==0&&b.epoch==a.epoch+1);check(bool(b.status&Exception)==exception);check(hazards==0&&active==0);}
void partial_unwind(){
 U code=U(context::pages[1])+32;const unsigned char expected[]{0x40,0x53,0x55,0x56,0x57,0x48,0xb8};check(!memcmp((void*)code,expected,sizeof expected));
 const unsigned offsets[]{0,2,3,4,5,15};const unsigned counts[]{0,1,2,3,4,4};
 for(unsigned i=0;i<6;++i){alignas(16) U stack[64]{};U sp=U(stack)+256;*(U*)sp=0x12345678;*(U*)(sp-8)=0x3030;*(U*)(sp-16)=0x5050;*(U*)(sp-24)=0x6060;*(U*)(sp-32)=0x7070;
  CONTEXT c{};c.ContextFlags=CONTEXT_FULL;c.Rip=code+offsets[i];c.Rsp=sp-counts[i]*8;c.Rbx=0x3030;c.Rbp=0x5050;c.Rsi=0x6060;c.Rdi=0x7070;
  DWORD64 image_base{};auto* f=RtlLookupFunctionEntry(c.Rip,&image_base,nullptr);check(f!=nullptr);void* handler{};DWORD64 establisher{};RtlVirtualUnwind(UNW_FLAG_NHANDLER,image_base,c.Rip,f,&c,&handler,&establisher,nullptr);
  check(c.Rip==0x12345678&&c.Rsp==sp+8&&c.Rbx==0x3030&&c.Rbp==0x5050&&c.Rsi==0x6060&&c.Rdi==0x7070);++unwind_checks;
 }
 DWORD64 image_base{};check(RtlLookupFunctionEntry(U(context::pages[0])+32,&image_base,nullptr)==nullptr);
 check(!memcmp(context::pages[0]+32,"\x48\x89\x5c\x24\x08\xff\x25",7));
}
void byte_change(unsigned char* p,unsigned char value){DWORD old{},unused{};check(VirtualProtect(p,1,PAGE_EXECUTE_READWRITE,&old));*p=value;check(VirtualProtect(p,1,old,&unused));check(FlushInstructionCache(GetCurrentProcess(),p,1));}
int main(){SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);try{
 check(context::configure((void*)&d5ai_fixture_owner,(void*)&d5ai_fixture_context_reset,sor::sha_bytes((void*)&d5ai_fixture_owner,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_context_reset,32).c_str()));bool dirty=false;for(unsigned i=0;i<10000&&!sole_thread();++i)Sleep(1);check(sole_thread());check(install(context::edits,2,dirty));check(context::guards());
 initialize_queue();enabled=true;
 check(d5ai_fixture_owner(0x1111,0x2222,0x3333,0x4444)==0x5555);check_pair(5,false);
 check(d5ai_fixture_context_reset(0x9999,1,0xaaaa,0xbbbb)==0xccdd);check_pair(6,false);
 throw_owner=true;try{d5ai_fixture_owner(0x1111,0x2222,0x3333,0x4444);check(false);}catch(const std::runtime_error&){}check_pair(5,true);
 throw_reset=true;try{d5ai_fixture_context_reset(0x9999,1,0xaaaa,0xbbbb);check(false);}catch(const std::runtime_error&){}check_pair(6,true);
 partial_unwind();auto* body=context::edits[0].at+20;auto old=*body;byte_change(body,static_cast<unsigned char>(old^1));check(!context::guards());byte_change(body,old);check(context::guards());
 auto* relay=context::pages[1];old=*relay;byte_change(relay,static_cast<unsigned char>(old^1));check(!context::guards());byte_change(relay,old);check(context::guards());
 printf("{\"status\":\"PASS\",\"checks\":%u,\"partial_unwind_contexts\":%u}\n",checks,unwind_checks);return 0;
 }catch(const std::exception& e){fprintf(stderr,"%s checks=%u unwind=%u\n",e.what(),checks,unwind_checks);return 1;}}
