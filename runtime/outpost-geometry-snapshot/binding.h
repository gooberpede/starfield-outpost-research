// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Current manager observations are diagnostics, not historical construction or
// source-lease certificates. Reads are checked and never invoke engine methods.
// Field provenance: D5AI owner-context rework and original provider 0x14079fe81.
#include "identity.h"
#include <array>

namespace d5ar {
struct OwnedBinding {
    const char* status="NOT_CAPTURED";
    std::uint64_t manager{},attached_proc{};
    std::uint32_t owner_formid{};
    std::uint8_t mode{};
    std::array<std::uint8_t,44> descriptor{};
    bool complete{};
};
inline OwnedBinding read_binding(IdentityRead reader,void* context,std::uint64_t module_base) noexcept {
    OwnedBinding result;result.status="READ_FAILED";
    if(!reader||module_base<0x10000||module_base>UINT64_MAX-0x5fd9c38)return result;
    try {
        if(!reader(context,module_base+0x5fd9c30,&result.manager,8))return result;
        if(!result.manager){result.status="NO_MANAGER";return result;}
        if(result.manager<0x10000||result.manager>UINT64_MAX-0x1ec)return result;
        if(!reader(context,result.manager+0x130,&result.attached_proc,8)||
           !reader(context,result.manager+0x80,&result.owner_formid,4)||
           !reader(context,result.manager+0x20,&result.mode,1)||
           !reader(context,result.manager+(result.mode==3?0x1c0:0xc8),result.descriptor.data(),44))return result;
    }catch(...){result.status="READ_EXCEPTION";return result;}
    result.status="OBSERVED_UNQUALIFIED";result.complete=true;return result;
}
}
