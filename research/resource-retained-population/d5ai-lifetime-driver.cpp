// SPDX-License-Identifier: GPL-3.0-or-later
// Independent typed caller and exception oracle for exact retained entry object.
#include "d5ai_lifetime.h"
#include <cstdio>
#include <stdexcept>
#include <source_location>
#include <algorithm>
#include <vector>
using namespace winner;
extern "C" {U d5ai_fixture_life_holder(U,U,U,U) noexcept(false);U d5ai_fixture_life_collection(U,U,U,U) noexcept(false);U d5ai_fixture_life_mutation(U,U,U,U) noexcept(false);}
unsigned checks{};bool throwing{},nested{};
void check(bool yes,std::source_location where=std::source_location::current()){++checks;if(!yes){fprintf(stderr,"line %u\n",where.line());throw std::runtime_error("lifetime oracle assertion");}}
extern "C" U d5ai_native_owner(U,U,U,U){return 0;}
extern "C" U d5ai_native_context_reset(U,U,U,U){return 0;}
U body(unsigned kind,U a,U b,U c,U d){check(a==0x10000+kind*16&&b==0x2222&&c==0x3333&&d==0x4444);check(GetLastError()==123);if(throwing)throw std::runtime_error("owned body throw");if(nested){nested=false;check(d5ai_fixture_life_collection(0x10010,0x2222,0x3333,0x4444)==0x5556);}SetLastError(456);return 0x5555+kind;}
extern "C" U d5ai_native_life_holder(U a,U b,U c,U d) noexcept(false){return body(0,a,b,c,d);}
extern "C" U d5ai_native_life_collection(U a,U b,U c,U d) noexcept(false){return body(1,a,b,c,d);}
extern "C" U d5ai_native_life_mutation(U a,U b,U c,U d) noexcept(false){return body(2,a,b,c,d);}
void pair(unsigned kind,bool exceptional){lifetime::Event a{},b{};check(lifetime::pop(a)&&lifetime::pop(b));check(a.kind==kind+1&&b.kind==a.kind&&a.phase==0&&b.phase==1&&a.invocation==b.invocation&&a.thread==b.thread&&a.ticks<=b.ticks);check(a.receiver==0x10000+kind*16&&a.allocation==a.receiver-(kind==0?16:8));check(b.status==(exceptional?16:0));check(!lifetime::active&&!active&&hazards==0);}
int main(){SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);try{
 check(lifetime::configure((void*)&d5ai_fixture_life_holder,(void*)&d5ai_fixture_life_collection,(void*)&d5ai_fixture_life_mutation,sor::sha_bytes((void*)&d5ai_fixture_life_holder,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_life_collection,32).c_str(),sor::sha_bytes((void*)&d5ai_fixture_life_mutation,32).c_str()));
 bool dirty=false;for(unsigned i=0;i<10000&&!sole_thread();++i)Sleep(1);check(sole_thread());check(install(lifetime::edits,3,dirty));check(lifetime::guards());for(U i=0;i<lifetime::capacity;++i)lifetime::queue[i].ticket=i;enabled=true;
 Four calls[]{&d5ai_fixture_life_holder,&d5ai_fixture_life_collection,&d5ai_fixture_life_mutation};
 for(unsigned i=0;i<3;++i){SetLastError(123);check(calls[i](0x10000+i*16,0x2222,0x3333,0x4444)==0x5555+i);check(GetLastError()==456);pair(i,false);}
 throwing=true;for(unsigned i=0;i<3;++i){SetLastError(123);try{calls[i](0x10000+i*16,0x2222,0x3333,0x4444);check(false);}catch(const std::runtime_error&){}pair(i,true);}throwing=false;
 nested=true;SetLastError(123);check(calls[0](0x10000,0x2222,0x3333,0x4444)==0x5555);lifetime::Event rows[4]{};for(auto& e:rows)check(lifetime::pop(e));check(rows[0].phase==0&&rows[1].parent==rows[0].invocation&&rows[2].invocation==rows[1].invocation&&rows[3].invocation==rows[0].invocation);
 auto before=lifetime::mark();check(lifetime::coherent(before));for(unsigned i=0;i<3;++i){DWORD64 base{};check(RtlLookupFunctionEntry(U(lifetime::pages[i])+32,&base,nullptr)==nullptr);check(!memcmp(lifetime::pages[i]+37,"\xff\x25",2));}
 for(unsigned i=0;i<3;++i){
  for(auto* target:{lifetime::edits[i].at+20,lifetime::pages[i]}){DWORD old{},unused{};check(VirtualProtect(target,1,PAGE_EXECUTE_READWRITE,&old));auto saved=*target;*target^=1;check(VirtualProtect(target,1,old,&unused));check(FlushInstructionCache(GetCurrentProcess(),target,1));check(!lifetime::guards());check(VirtualProtect(target,1,PAGE_EXECUTE_READWRITE,&old));*target=saved;check(VirtualProtect(target,1,old,&unused));check(FlushInstructionCache(GetCurrentProcess(),target,1));check(lifetime::guards());}
 }
 std::vector<U> baseline,observed;
 for(unsigned i=0;i<1000;++i){SetLastError(123);U start=lifetime::tick();auto result=d5ai_native_life_mutation(0x10020,0x2222,0x3333,0x4444);baseline.push_back(lifetime::tick()-start);check(result==0x5557);SetLastError(123);start=lifetime::tick();result=calls[2](0x10020,0x2222,0x3333,0x4444);observed.push_back(lifetime::tick()-start);check(result==0x5557);pair(2,false);}
 std::sort(baseline.begin(),baseline.end());std::sort(observed.begin(),observed.end());LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);
 enabled=false;SetLastError(123);check(calls[0](0x10000,0x2222,0x3333,0x4444)==0x5555);check(lifetime::unlogged_cutoff>before.ticks);check(!lifetime::pop(rows[0]));
 printf("{\"status\":\"PASS\",\"checks\":%u,\"typed_entries\":3,\"leaf_trampolines\":3,\"cost_calls\":1000,\"frequency\":%llu,\"baseline_p95_ticks\":%llu,\"hook_p50_ticks\":%llu,\"hook_p95_ticks\":%llu,\"hook_max_ticks\":%llu}\n",checks,(unsigned long long)frequency.QuadPart,(unsigned long long)baseline[949],(unsigned long long)observed[499],(unsigned long long)observed[949],(unsigned long long)observed.back());return 0;
 }catch(const std::exception& e){fprintf(stderr,"%s checks=%u\n",e.what(),checks);return 1;}}
