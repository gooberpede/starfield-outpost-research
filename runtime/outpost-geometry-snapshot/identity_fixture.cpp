// SPDX-License-Identifier: GPL-3.0-or-later
// Owned diagnostic-reader controls; no native process, source lease or game.
#include "identity.h"
#include <cstring>
#include <iostream>
#include <stdexcept>

namespace {
struct Input {
    std::array<std::uint8_t,0x70> bytes{};
    unsigned calls{},fail_call{},throw_call{};
    std::array<std::uint64_t,14> offsets{};
    bool throws{};
};
bool read(void* context,std::uint64_t address,void* into,std::size_t size) {
    auto& input=*static_cast<Input*>(context);
    ++input.calls;
    if(input.calls<=input.offsets.size())input.offsets[input.calls-1]=address-0x20000;
    if(input.throws||input.calls==input.throw_call)throw std::runtime_error("owned-reader-fault");
    if(input.calls==input.fail_call||address<0x20000||address-0x20000+size>input.bytes.size())return false;
    std::memcpy(into,input.bytes.data()+std::size_t(address-0x20000),size);
    return true;
}
void require(bool condition,const char* name) {
    if(!condition)throw std::runtime_error(name);
}
}
int main() {
    try {
        Input input;
        for(std::size_t n=0;n<input.bytes.size();++n)input.bytes[n]=std::uint8_t(n);
        auto value=d5ar::read_source_diagnostics(read,&input,0x20000);
        const std::array<std::uint8_t,29> expected{0,1,2,3,0x38,0x3c,0x3d,0x3e,0x3f,
            0x40,0x41,0x42,0x43,0x4c,0x4d,0x4e,0x4f,0x50,0x51,0x52,0x53,
            0x5c,0x5d,0x5e,0x5f,0x60,0x61,0x62,0x63};
        const std::array<std::uint8_t,16> origins{0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,
            0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27};
        std::array<std::uint8_t,44> descriptor{};
        for(std::size_t n=0;n<descriptor.size();++n)descriptor[n]=std::uint8_t(0x38+n);
        require(value.complete&&value.semantic==expected&&value.visited==0x6f6e6d6c6b6a6968ULL&&input.calls==14,
                "exact-fourteen-read-byte-order");
        require(value.origin_complete&&value.origin_words==origins&&
            std::strcmp(value.origin_status,"SOURCE_ORIGIN_WORDS_UNQUALIFIED")==0,"origin-raw-not-certificate");
        require(input.offsets==std::array<std::uint64_t,14>{0,0x38,0x3c,0x40,0x4c,0x50,0x5c,0x60,0x68,0x10,0x14,0x20,0x24,0x38},
            "exact-selected-offset-order");
        require(value.descriptor_complete&&value.descriptor_bytes==descriptor&&
            std::strcmp(value.descriptor_status,"SOURCE_DESCRIPTOR_UNQUALIFIED")==0,"complete-raw-descriptor");
        require(std::strcmp(value.status,"SOURCE_BYTES_UNQUALIFIED")==0,"raw-not-certificate");
        unsigned controls=5;
        for(unsigned fail=1;fail<=9;++fail) {
            input.calls=0;input.fail_call=fail;
            value=d5ar::read_source_diagnostics(read,&input,0x20000);
            require(!value.complete&&std::strcmp(value.status,"READ_FAILED")==0&&value.visited==0&&
                    value.semantic==std::array<std::uint8_t,29>{}&&value.origin_complete&&value.origin_words==origins&&
                    value.descriptor_complete&&value.descriptor_bytes==descriptor,
                    "geography-failure-preserves-independent-origin");
            ++controls;
        }
        for(unsigned fail=10;fail<=13;++fail) {
            input.calls=0;input.fail_call=fail;
            value=d5ar::read_source_diagnostics(read,&input,0x20000);
            require(value.complete&&value.semantic==expected&&!value.origin_complete&&
                std::strcmp(value.origin_status,"READ_FAILED")==0&&value.origin_words==std::array<std::uint8_t,16>{}&&
                value.descriptor_complete&&value.descriptor_bytes==descriptor,
                "origin-failure-preserves-geography");++controls;
        }
        input.calls=0;input.fail_call=14;
        value=d5ar::read_source_diagnostics(read,&input,0x20000);
        require(value.complete&&value.origin_complete&&!value.descriptor_complete&&
            std::strcmp(value.descriptor_status,"READ_FAILED")==0&&value.descriptor_bytes==std::array<std::uint8_t,44>{},
            "descriptor-failure-preserves-other-groups");++controls;
        input.calls=0;input.fail_call=0;input.throw_call=14;
        value=d5ar::read_source_diagnostics(read,&input,0x20000);
        require(value.complete&&value.origin_complete&&!value.descriptor_complete,"descriptor-exception-preserves-other-groups");++controls;
        input.calls=0;input.fail_call=0;input.throw_call=10;
        value=d5ar::read_source_diagnostics(read,&input,0x20000);
        require(value.complete&&!value.origin_complete,"origin-exception-preserves-geography");++controls;
        input.throw_call=0;
        input.calls=0;input.fail_call=0;input.throws=true;
        value=d5ar::read_source_diagnostics(read,&input,0x20000);
        require(!value.complete&&!value.origin_complete&&!value.descriptor_complete&&input.calls==3,"independent-reader-exception-refusals");++controls;
        input.calls=0;
        value=d5ar::read_source_diagnostics(read,&input,UINT64_MAX-0x20);
        require(!value.complete&&input.calls==0,"overflow-before-read");++controls;
        value=d5ar::read_source_diagnostics(read,&input,0);
        require(!value.complete&&input.calls==0,"invalid-address-before-read");++controls;
        value=d5ar::read_source_diagnostics(nullptr,&input,0x20000);
        require(!value.complete&&input.calls==0,"missing-reader-refusal");++controls;
        std::cout<<"{\"status\":\"PASS\",\"controls\":"<<controls
                 <<",\"scope\":\"owned_diagnostic_reader_only\"}\n";
        return 0;
    }catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
}
