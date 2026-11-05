// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Immutable reference identity copied during original F3DF70's resolved lease.
// Original 0x1402b7070 acquires it; original 0x140f3e0c2 releases it.
// No native query/AddRef/release, reference pointer dereference, or allocation
// continuity after release is claimed by this owned fixed-buffer state machine.
#include "identity.h"
#include <cstring>
namespace d5ar {
struct SelectedLease {
    const char* status="NOT_CAPTURED";
    std::uint64_t invocation{},command{},epoch{},reference{};
    std::uint32_t formid{};
    std::uint8_t type{};
    unsigned observations{};
    bool active{},copied{},ambiguous{},linked{};
};
inline SelectedLease begin_selection(std::uint64_t invocation,std::uint64_t command,std::uint64_t epoch) noexcept {
    SelectedLease result;result.invocation=invocation;result.command=command;result.epoch=epoch;
    result.active=invocation&&command;result.status=result.active?"SELECTION_PENDING":"SELECTION_SCOPE_UNAVAILABLE";return result;
}
inline void selection_ambiguous(SelectedLease& value) noexcept {
    value.ambiguous=true;value.linked=false;value.status="SELECTION_AMBIGUOUS";
}
inline void copy_selected_lease(SelectedLease& value,IdentityRead read,void* context,std::uint64_t module,
        std::uint64_t release_return,std::uint64_t resolver_caller_return,std::uint64_t reference,std::uint64_t epoch) noexcept {
    if(!value.active)return;
    if(!module||module>UINT64_MAX-0x21b26c1||release_return!=module+0xf3e0c7||resolver_caller_return!=module+0x21b25dd)return;
    ++value.observations;
    if(value.observations!=1||value.ambiguous){selection_ambiguous(value);return;}
    if(epoch!=value.epoch){value.status="SELECTION_PHASE_CHANGED";return;}
    if(!read||reference<0x10000||reference>UINT64_MAX-0x2f){value.status="SELECTED_IDENTITY_UNAVAILABLE";return;}
    std::uint32_t id{};std::uint8_t type{};
    try {
        if(!read(context,reference+0x28,&id,4)||!read(context,reference+0x2e,&type,1)){
            value.status="SELECTED_IDENTITY_READ_FAILED";return;
        }
    }catch(...){value.status="SELECTED_IDENTITY_READ_EXCEPTION";return;}
    value.reference=reference;value.formid=id;value.type=type;value.copied=true;
    value.status="SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME";
}
inline bool link_selected_operation(SelectedLease& value,std::uint64_t invocation,std::uint64_t command,
        std::uint64_t epoch,std::uint64_t module,std::uint64_t area_return,std::uint64_t operand) noexcept {
    value.linked=false;
    if(!value.active||!value.copied||value.ambiguous||value.observations!=1)return false;
    if(value.invocation!=invocation||value.command!=command||value.epoch!=epoch||
       !module||module>UINT64_MAX-0x21b26c1||area_return!=module+0x21b26c1||operand!=value.reference)return false;
    value.linked=true;return true;
}
inline void end_selection(SelectedLease& value) noexcept {value.active=false;value.linked=false;}
}
