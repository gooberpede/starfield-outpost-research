// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Initial configure retains the exact original target32 check before installation.
// Only the documented shared-helper overlap may be reconstructed at runtime.
namespace winner::guardrepair {
inline bool target(U address,const std::string& original_hash){
 unsigned char bytes[32]{};if(!read(address,bytes,sizeof bytes))return false;
 if(causal::configured){
  for(unsigned i=0;i<causal::site_count;++i){auto& p=causal::edits[i];U at=U(p.at);
   if(at>=address+32||at+p.n<=address)continue;
   if(i!=3||address!=causal::helper_locations[0]||at!=address+22||p.n!=9)return false;
   if(!match(p,true)||!causal::guards())return false;
   for(unsigned k=0;k<p.n;++k)bytes[at-address+k]=p.before[k];
  }
 }
 return sor::sha_bytes(bytes,sizeof bytes)==original_hash;
}
inline std::string metadata(){return ",\"geometry_target_guard_basis\":\"original32-exact-causal-overlap/1\"";}
}
