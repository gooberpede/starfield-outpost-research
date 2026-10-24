// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "decode.h"
// Original C2B bounded external reads. All addresses are runtime VAs.
// The caller is stopped at a qualified consumer site. Equal copies certify
// retained bytes at this stop; they cannot certify a historical producer epoch.
namespace context_capture {
template<class R>std::string capture(R& read,uint64_t base,uint64_t procgen,
                                    uint64_t slot,uint64_t key,uint64_t wrapper){
    unsigned char manager[0x200]{},source[0x70]{},slot_bytes[24]{};
    unsigned char again_manager[0x200]{},again_source[0x70]{},again_slot[24]{};
    uint64_t owner=0,owner_again=0;
    auto copy=[&](uint64_t at,void* dest,size_t size){
        return retail::range(at,size)&&read(at,dest,size);
    };
    bool ok=slot>=8&&copy(base+0x5fd9c30,&owner,8)&&
        copy(owner,manager,sizeof manager)&&copy(key,source,sizeof source)&&
        copy(slot-8,slot_bytes,sizeof slot_bytes);
    if(ok)ok=retail::field<uint64_t>(manager,0x130)==procgen&&
        retail::field<uint64_t>(slot_bytes,0)==key&&
        retail::field<uint64_t>(slot_bytes,8)==wrapper&&
        retail::field<uint32_t>(slot_bytes,16)!=0xffffffffU;
    if(ok)ok=copy(base+0x5fd9c30,&owner_again,8)&&owner==owner_again&&
        copy(owner,again_manager,sizeof again_manager)&&
        copy(key,again_source,sizeof again_source)&&
        copy(slot-8,again_slot,sizeof again_slot)&&
        !memcmp(manager,again_manager,sizeof manager)&&
        !memcmp(source,again_source,sizeof source)&&
        !memcmp(slot_bytes,again_slot,sizeof slot_bytes);
    std::ostringstream s;
    s<<"{\"status\":\""<<(ok?"COMPLETE":"INCOMPLETE")
     <<"\",\"scope\":\"CONSUMPTION_STOP_ONLY\",\"manager_pointer\":"<<owner
     <<",\"source_pointer\":"<<key<<",\"raw_manager\":";
    if(ok)s<<'"'<<retail::hex(manager,sizeof manager)<<'"';else s<<"null";
    s<<",\"raw_source\":";
    if(ok)s<<'"'<<retail::hex(source,sizeof source)<<'"';else s<<"null";
    s<<",\"owner_key_u32\":";
    if(ok)s<<retail::field<uint32_t>(manager,0x80);else s<<"null";
    s<<",\"source_grid_i32\":";
    if(ok){s<<'[';for(unsigned j=0;j<8;++j){if(j)s<<',';s<<retail::field<int32_t>(source,0x10+4*j);}s<<']';}
    else s<<"null";
    s<<",\"generation_epoch\":null,\"historical_inputs\":null}";
    return s.str();
}
}
