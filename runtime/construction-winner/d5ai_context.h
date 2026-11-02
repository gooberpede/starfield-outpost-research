// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Included only by the derived D5AI candidate, whose owned observer snapshot
// expands the original fence table to seven entries. Historical source remains.
#include "patch.h"
#include "../exp0002/win_support.h"
namespace winner::context {
inline Patch edits[2]{};
inline unsigned char* pages[2]{};
inline std::string page_hash[2],body_hash[2],original_hash[2];
inline bool configured{};
inline bool configure(void* owner,void* reset,const char* owner_hash,const char* reset_hash){
 void* sites[]{owner,reset};const char* hashes[]{owner_hash,reset_hash};
 const unsigned char expected[][5]{{0x48,0x89,0x5c,0x24,0x08},{0x40,0x53,0x55,0x56,0x57}};
 void* hooks[]{(void*)&fence_hook<5>,(void*)&fence_hook<6>};
 for(unsigned i=0;i<2;++i){
  auto& p=edits[i];p.at=(unsigned char*)sites[i];p.n=5;unsigned char bytes[32]{};
  if(!read(U(p.at),bytes,32)||sor::sha_bytes(bytes,32)!=hashes[i]||memcmp(bytes,expected[i],5))return false;
  memcpy(p.before,bytes,5);original_hash[i]=hashes[i];body_hash[i]=sor::sha_bytes(bytes+5,27);
  auto* page=near_page(U(p.at));if(!page)return false;pages[i]=page;jump(page,U(hooks[i]));if(!relative(p,U(page),0xe9))return false;
  auto* trampoline=page+32;memcpy(trampoline,p.before,5);
  if(i==0)jump(trampoline+5,U(p.at)+5);
  else {
   // Entry RAX is dead before the pinned reset body's first call. Register-tail
   // transfer avoids FF25 epilogue interpretation with four stolen pushes.
   trampoline[5]=0x48;trampoline[6]=0xb8;U destination=U(p.at)+5;memcpy(trampoline+7,&destination,8);trampoline[15]=0xff;trampoline[16]=0xe0;
   auto* function=(RUNTIME_FUNCTION*)(page+3072);function->BeginAddress=32;function->EndAddress=49;function->UnwindData=3104;
   const unsigned char unwind[]{1,5,4,0,5,0x70,4,0x60,3,0x50,2,0x30};memcpy(page+3104,unwind,sizeof unwind);
   if(!RtlAddFunctionTable(function,1,U(page)))return false;
  }
  fences[i+5]=(Four)trampoline;
  DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;
  page_hash[i]=sor::sha_bytes(page,4096);
 }
 configured=true;return true;
}
inline bool guards(){
 if(!configured)return true;
 for(unsigned i=0;i<2;++i){unsigned char bytes[27]{};
  if(!match(edits[i],true)||!read(U(edits[i].at)+5,bytes,27)||sor::sha_bytes(bytes,27)!=body_hash[i]||sor::sha_bytes(pages[i],4096)!=page_hash[i])return false;
 }return true;
}
inline std::string metadata(){
 std::string result=",\"context_schema\":\"sor-d5ai-context/1\",\"context_sites\":[";
 if(configured)for(unsigned i=0;i<2;++i){if(i)result+=",";result+="{\"va\":"+std::to_string(U(edits[i].at))+",\"bytes\":5,\"reason\":"+std::to_string(i+5)+",\"guard_sha256\":"+sor::quote(original_hash[i])+"}";}
 return result+"]";
}
}
