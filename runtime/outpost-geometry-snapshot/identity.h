// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Original checked-read diagnostic helper. Field provenance: D5AB P1 source
// identity/lifetime L02/L06 and constructor 0x140982d90 on retail 1.16.244.0.
// Raw observations do not certify source ownership, body, frame or outpost.
#include <array>
#include <cstddef>
#include <cstdint>

namespace d5ar {
using IdentityRead=bool(*)(void*,std::uint64_t,void*,std::size_t);
struct SourceDiagnostics {
    const char* status="NOT_CAPTURED";
    std::array<std::uint8_t,29> semantic{};
    std::uint64_t visited{};
    bool complete{};
    std::array<std::uint8_t,16> origin_words{};
    bool origin_complete{};
    const char* origin_status="NOT_CAPTURED";
    std::array<std::uint8_t,44> descriptor_bytes{};
    bool descriptor_complete{};
    const char* descriptor_status="NOT_CAPTURED";
};
inline SourceDiagnostics read_source_diagnostics(IdentityRead reader,void* context,std::uint64_t source) noexcept {
    SourceDiagnostics result;
    result.status="READ_FAILED";
    result.origin_status="READ_FAILED";
    result.descriptor_status="READ_FAILED";
    if(!reader||source<0x10000||source>UINT64_MAX-0x70)return result;
    // Exact concatenation: terrain FormID, chart byte, then six original
    // coordinate words; padding and mutable dimensions are not read.
    constexpr std::array<std::uint64_t,8> offsets{0,0x38,0x3c,0x40,0x4c,0x50,0x5c,0x60};
    constexpr std::array<std::size_t,8> sizes{4,1,4,4,4,4,4,4};
    std::size_t at=0;
    bool geography_ok=true;
    try {
        for(std::size_t n=0;n<offsets.size();++n) {
            if(!reader(context,source+offsets[n],result.semantic.data()+at,sizes[n])){geography_ok=false;break;}
            at+=sizes[n];
        }
        if(geography_ok&&!reader(context,source+0x68,&result.visited,sizeof result.visited))geography_ok=false;
    }catch(...){geography_ok=false;}
    if(geography_ok){result.status="SOURCE_BYTES_UNQUALIFIED";result.complete=true;}
    else {result.semantic={};result.visited=0;}
    // Provider 0x14079fab8..fad6 consumes these four words as origin input.
    // This independent raw group is not a construction/frame certificate.
    constexpr std::array<std::uint64_t,4> origin_offsets{0x10,0x14,0x20,0x24};
    bool origin_ok=true;
    try {
        for(std::size_t n=0;n<origin_offsets.size();++n)
            if(!reader(context,source+origin_offsets[n],result.origin_words.data()+4*n,4)){origin_ok=false;break;}
    }catch(...){origin_ok=false;}
    if(origin_ok){result.origin_complete=true;result.origin_status="SOURCE_ORIGIN_WORDS_UNQUALIFIED";}
    else result.origin_words={};
    // Preserve the complete constructor-copied descriptor, including raw padding
    // and non-geographic words. A semantic projection requires separate proof.
    try {
        if(reader(context,source+0x38,result.descriptor_bytes.data(),result.descriptor_bytes.size())) {
            result.descriptor_complete=true;
            result.descriptor_status="SOURCE_DESCRIPTOR_UNQUALIFIED";
        }else result.descriptor_bytes={};
    }catch(...){result.descriptor_bytes={};}
    return result;
}
}
