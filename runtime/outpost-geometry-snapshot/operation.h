// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Checked observations of the existing established-operation area request.
// Native sources: D5AR identity01, D5V export01, and owned EXP0002 core fields.
// Reads only caller-live indexed input and module-owned header scalars. No
// unleased reference/base/cell or translation-vector pointer is followed.
// Selected identity is copied separately under the native pre-release lease.
#include "identity.h"
#include <array>
#include <cstring>

namespace d5ar {
struct OwnedOperation {
    const char* status="NOT_CAPTURED";
    std::uint64_t caller_return{},reference{},query_state{},domain{};
    std::array<std::uint8_t,24> indexed{};
    std::uint32_t radius_word{},upper_word{},translation_index{},translation_count{};
    std::uint64_t translation_pointer{},base_pointer{},cell_pointer{};
    std::array<std::uint8_t,12> translation{};
    const char* translation_status="NOT_CAPTURED";
    std::uint32_t reference_formid{},base_formid{},cell_formid{};
    std::uint8_t reference_type{},base_type{},cell_type{};
    bool translation_applied{},reference_identity_complete{},complete{};
};
inline OwnedOperation capture_operation(IdentityRead reader,void* context,std::uint64_t module_base,
        std::uint64_t caller_return,std::uint64_t reference,std::uint64_t query_state,
        std::uint64_t indexed_pointer,std::uint32_t radius_word,std::uint32_t upper_word) noexcept {
    OwnedOperation result;
    result.caller_return=caller_return;result.reference=reference;result.query_state=query_state;
    result.radius_word=radius_word;result.upper_word=upper_word;
    if(!module_base||module_base>UINT64_MAX-0x61fae90||caller_return!=module_base+0x21b26c1) {
        result.status="OTHER_AREA_CALLSITE";return result;
    }
    if(!reader||indexed_pointer<0x10000||indexed_pointer>UINT64_MAX-24||reference<0x10000) {
        result.status="OPERATION_INPUT_UNAVAILABLE";return result;
    }
    auto read=[&](std::uint64_t pointer,std::uint64_t offset,void* into,std::size_t size) {
        return pointer>=0x10000&&offset<=UINT64_MAX-pointer&&size<=UINT64_MAX-pointer-offset&&
               reader(context,pointer+offset,into,size);
    };
    try {
        if(!read(indexed_pointer,0,result.indexed.data(),result.indexed.size())) {
            result.status="OPERATION_INPUT_READ_FAILED";return result;
        }
        std::memcpy(&result.translation_index,result.indexed.data()+12,4);
        std::memcpy(&result.domain,result.indexed.data()+16,8);
        if(!read(module_base,0x61fae80,&result.translation_count,4)||
           !read(module_base,0x61fae88,&result.translation_pointer,8)) {
            result.translation_status="TRANSLATION_READ_FAILED";
        }else result.translation_status="HEADER_ONLY_UNQUALIFIED";
        // A readable header cannot prove vector lifetime, binding stability or
        // later predicate consumption. Reference/cell identity is not read here.
        result.status="ACTIVE_ESTABLISHED_OPERATION_REFERENCE";
        result.complete=true;
    }catch(...) {result.status="OPERATION_READ_EXCEPTION";result.complete=false;}
    return result;
}
}
