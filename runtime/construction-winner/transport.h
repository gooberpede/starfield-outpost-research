// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "patch.h"
#include "../exp0002/win_support.h"
#include <filesystem>
#include <string>
extern "C" {extern uint64_t visited_fall,visited_taken,selected_fall;void visited_bridge();void selected_bridge();void birth_bridge();void published_bridge();void stored_bridge();extern uint64_t birth_fall,published_fall,stored_fall;}
namespace winner {
extern Patch edits[18];
extern std::filesystem::path session;
extern HANDLE raw,ack;
extern std::string identity,identity_hash;
extern std::atomic<U> written,flushed,acknowledged,bytes;
extern std::atomic<unsigned> fixture_fault;
extern const char* output_fault;
extern unsigned char* relay_page;extern std::string relay_sha256;
extern U guarded_targets[7];extern std::string guarded_hashes[7];
bool drain();bool disk(U reserve);bool guards();DWORD WINAPI worker(void*);
// Identical patch assembly for production and disposable sites. CALL destinations
// are decoded from the checked original instruction; prologues use trampolines.
inline bool configure(void** locations,const unsigned* lengths,const char** hashes){
 auto* page=near_page(U(locations[0]));if(!page)return false;
 void* hooks[]{(void*)&provider_hook,(void*)&selected_bridge,(void*)&visited_bridge,
  (void*)&lookup_hook,(void*)&descriptor_hook,(void*)&generate_hook,(void*)&sample_hook,
  (void*)&fence_hook<0>,(void*)&fence_hook<1>,(void*)&fence_hook<2>,(void*)&fence_hook<3>,(void*)&fence_hook<4>,(void*)&cold_hook,(void*)&normalizer_hook,(void*)&birth_bridge,(void*)&published_bridge,(void*)&reserve_hook,(void*)&stored_bridge};
 U targets[18]{};
 unsigned guarded=0;
 for(unsigned i=0;i<18;++i){auto& p=edits[i];p.at=(unsigned char*)locations[i];p.n=lengths[i];unsigned char window[32]{};
  if(!read(U(p.at),window,32)||sor::sha_bytes(window,32)!=hashes[i])return false;
  memcpy(p.before,window,p.n);auto* island=page+i*128;jump(island,U(hooks[i]));
  bool call=(i>=3&&i<=6)||i==12||i==13||i==16;
  // Inline bridges are CALL-entered so Windows unwinds to the original native
  // frame at a real site return PC; their own FRAME metadata handles saves.
  bool inline_bridge=i==1||i==2||i==14||i==15||i==17;
  if(!relative(p,U(island),(call||inline_bridge)?0xe8:0xe9))return false;
  if(i==2){
   // Preserve the conditional transfer in the original image, so RET never
   // rewrites a CALL return address (including with CET shadow stacks).
   if(p.n!=13||memcmp(window,"\x40\x84\xf6\x0f\x85",5)||memcmp(window+9,"\x48\x89\x5d\x10",4))return false;
   int32_t native_displacement{};memcpy(&native_displacement,window+5,4);
   U taken=U(p.at)+9+native_displacement;
   auto relocated=int64_t(taken)-int64_t(U(p.at)+11);
   if(relocated<INT32_MIN||relocated>INT32_MAX)return false;
   p.after[5]=0x0f;p.after[6]=0x85;auto branch=int32_t(relocated);memcpy(p.after+7,&branch,4);
  }
  if(call){if(window[0]!=0xe8)return false;int32_t displacement{};memcpy(&displacement,window+1,4);targets[i]=U(p.at)+5+displacement;
   unsigned char bytes[32]{};if(!read(targets[i],bytes,32))return false;guarded_targets[guarded]=targets[i];guarded_hashes[guarded++]=sor::sha_bytes(bytes,32);}
  else if(i==0||(i>=7&&i<=11)){auto* trampoline=island+32;memcpy(trampoline,p.before,p.n);jump(trampoline+p.n,U(p.at)+p.n);targets[i]=U(trampoline);}
 }
 provider_original=(Four)targets[0];lookup_original=(Four)targets[3];descriptor_original=(Four)targets[4];generate_original=(Generate)targets[5];sample_original=(Four)targets[6];
 for(unsigned i=0;i<5;++i)fences[i]=(Four)targets[7+i];cold_original=(Four)targets[12];
 normalizer_original=(Four)targets[13];
 birth_fall=U(locations[14])+12;published_fall=U(locations[15])+11;stored_fall=U(locations[17])+11;reserve_original=(Four)targets[16];
 selected_fall=U(locations[1])+8;visited_fall=U(locations[2])+9;
 int32_t displacement{};memcpy(&displacement,edits[2].before+5,4);visited_taken=visited_fall+displacement;
 // The erase trampoline executes three pushes and SUB RSP,0x30 before its
 // tail jump. Register its partial-prologue unwind metadata; the remaining
 // entry trampolines and jump relays make no stack change.
 const unsigned char erase_prologue[]{0x40,0x53,0x56,0x57,0x48,0x83,0xec,0x30};
 if(lengths[9]!=sizeof erase_prologue||memcmp(edits[9].before,erase_prologue,sizeof erase_prologue))return false;
 // The pinned native body defines RAX at +0x0c before using its entry value;
 // the fixture body likewise defines RAX immediately after this prologue.
 // A register tail jump avoids Windows mistaking FF25 for an epilogue while
 // the stolen native frame is still allocated.
 auto* erase_tail=page+9*128+32+8;erase_tail[0]=0x48;erase_tail[1]=0xb8;
 U erase_return=U(locations[9])+8;memcpy(erase_tail+2,&erase_return,8);erase_tail[10]=0xff;erase_tail[11]=0xe0;
 auto* function=(RUNTIME_FUNCTION*)(page+3072);
 function->BeginAddress=9*128+32;function->EndAddress=function->BeginAddress+8+12;function->UnwindData=3104;
 const unsigned char unwind[]{1,8,4,0,8,0x52,4,0x70,3,0x60,2,0x30};
 memcpy(page+3104,unwind,sizeof unwind);
 if(!RtlAddFunctionTable(function,1,U(page)))return false;
 DWORD old{};if(!VirtualProtect(page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),page,4096))return false;
 relay_page=page;relay_sha256=sor::sha_bytes(page,4096);return relay_sha256.size()==64;
}
}
