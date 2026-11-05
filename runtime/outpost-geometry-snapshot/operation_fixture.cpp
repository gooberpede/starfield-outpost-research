// SPDX-License-Identifier: GPL-3.0-or-later
// Owned operation-operand diagnostics only; no engine call or memory access.
#include "operation.h"
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {
constexpr std::uint64_t module=0x140000000,reference=0x20000,base=0x30000,cell=0x40000,indexed=0x60000,table=0x70000;
struct Span {std::uint64_t at;std::vector<std::uint8_t> bytes;};
struct Input {std::vector<Span> spans;unsigned calls{},fail_call{},forbidden{};bool change_binding{},throws{};};
template<class T> void put(std::vector<std::uint8_t>& bytes,std::size_t offset,T value) {std::memcpy(bytes.data()+offset,&value,sizeof value);}
bool read(void* context,std::uint64_t address,void* into,std::size_t size) {
    auto& input=*static_cast<Input*>(context);++input.calls;
    if(input.throws)throw std::runtime_error("owned-reader-exception");
    if(input.calls==input.fail_call)return false;
    for(auto start:{reference,base,cell,table})if(address>=start&&address-start<0x100){++input.forbidden;return false;}
    if(input.change_binding&&input.calls==3&&address==module+0x61fae88)
        put(input.spans[4].bytes,0,std::uint32_t(3));
    for(const auto& span:input.spans)if(address>=span.at&&address-span.at<=span.bytes.size()&&size<=span.bytes.size()-(address-span.at)) {
        std::memcpy(into,span.bytes.data()+std::size_t(address-span.at),size);return true;
    }
    return false;
}
Input setup(unsigned world=1) {
    Input result;result.spans={{reference,std::vector<std::uint8_t>(0xc0)},{base,std::vector<std::uint8_t>(0x40)},
        {cell,std::vector<std::uint8_t>(0x40)},{indexed,std::vector<std::uint8_t>(24)},
        {module+0x61fae80,std::vector<std::uint8_t>(4)},{module+0x61fae88,std::vector<std::uint8_t>(8)},
        {table,std::vector<std::uint8_t>(24)}};
    put(result.spans[0].bytes,0x28,std::uint32_t(100+world));result.spans[0].bytes[0x2e]=0x40;
    put(result.spans[0].bytes,0x98,base);put(result.spans[0].bytes,0xb0,cell);
    put(result.spans[1].bytes,0x28,std::uint32_t(200+world));result.spans[1].bytes[0x2e]=0x1e;
    put(result.spans[2].bytes,0x28,std::uint32_t(300+world));result.spans[2].bytes[0x2e]=0x3c;
    put(result.spans[3].bytes,0,float(world*10));put(result.spans[3].bytes,4,float(world*20));
    put(result.spans[3].bytes,8,float(world*30));put(result.spans[3].bytes,12,std::uint32_t(0));
    put(result.spans[3].bytes,16,std::uint64_t(0x80000+world));
    put(result.spans[4].bytes,0,std::uint32_t(2));put(result.spans[5].bytes,0,table);
    put(result.spans[6].bytes,0,-float(world*10));put(result.spans[6].bytes,4,-float(world*20));
    put(result.spans[6].bytes,8,-float(world*30));return result;
}
void require(bool test,const char* reason) {if(!test)throw std::runtime_error(reason);}
d5ar::OwnedOperation call(Input& input,std::uint64_t ret=module+0x21b26c1,std::uint64_t ref=reference) {
    return d5ar::capture_operation(read,&input,module,ret,ref,0x50000,indexed,0x43160000,0x42cd0000);
}
}
int main() {
    try {
        unsigned count=0;auto input=setup();auto before=input.spans;
        auto operation=call(input);
        require(operation.complete&&std::strcmp(operation.status,"ACTIVE_ESTABLISHED_OPERATION_REFERENCE")==0,"native-callsite-gate");++count;
        require(operation.indexed==std::array<std::uint8_t,24>{0,0,0x20,0x41,0,0,0xa0,0x41,0,0,0xf0,0x41,0,0,0,0,1,0,8,0,0,0,0,0},"lossless-indexed-input");++count;
        require(!operation.reference_identity_complete&&!operation.reference_formid&&!operation.base_formid&&!operation.cell_formid&&input.calls==3&&!input.forbidden,"unleased-reference-base-cell-not-followed");++count;
        require(!operation.translation_applied&&operation.translation==std::array<std::uint8_t,12>{}&&operation.translation_count==2&&operation.translation_pointer==table&&std::strcmp(operation.translation_status,"HEADER_ONLY_UNQUALIFIED")==0,"module-header-only-not-vector-or-application");++count;
        auto second=setup(2);auto other=call(second,module+0x21b26c1,reference+0x1000);
        require(other.reference!=operation.reference&&other.domain!=operation.domain&&other.indexed!=operation.indexed,"two-distinct-world-contexts");++count;
        for(std::size_t n=0;n<before.size();++n)require(before[n].bytes==input.spans[n].bytes,"input-preservation");++count;
        input=setup();operation=call(input,module+0x21b42e8);
        require(!operation.complete&&input.calls==0&&std::strcmp(operation.status,"OTHER_AREA_CALLSITE")==0,"preview-callsite-refused");++count;
        operation=d5ar::capture_operation(nullptr,nullptr,module,module+0x21b26c1,reference,0,indexed,0,0);
        require(!operation.complete,"missing-reader-refused");++count;
        input=setup();input.fail_call=1;operation=call(input);
        require(!operation.complete&&std::strcmp(operation.status,"OPERATION_INPUT_READ_FAILED")==0,"indexed-read-failure");++count;
        for(unsigned fail=2;fail<=3;++fail) {
            input=setup();input.fail_call=fail;operation=call(input);
            require(operation.complete&&std::strcmp(operation.translation_status,"TRANSLATION_READ_FAILED")==0,"translation-read-failure-retains-request");++count;
        }
        input=setup();input.change_binding=true;operation=call(input);
        require(operation.complete&&input.calls==3&&!input.forbidden&&operation.translation_count==2&&std::strcmp(operation.translation_status,"HEADER_ONLY_UNQUALIFIED")==0,"header-observation-never-binding-certificate");++count;
        input=setup();put(input.spans[3].bytes,12,std::uint32_t(99));operation=call(input);
        require(operation.complete&&!operation.translation_applied&&input.calls==3&&std::strcmp(operation.translation_status,"HEADER_ONLY_UNQUALIFIED")==0,"out-of-range-index-not-a-consumption-certificate");++count;
        input=setup();input.fail_call=4;operation=call(input);
        require(operation.complete&&!operation.reference_identity_complete&&input.calls==3&&!input.forbidden,"no-fourth-unleased-read");++count;
        input=setup();input.throws=true;operation=call(input);
        require(!operation.complete&&std::strcmp(operation.status,"OPERATION_READ_EXCEPTION")==0,"reader-exception-refused");++count;
        operation=d5ar::capture_operation(read,&input,UINT64_MAX,module+0x21b26c1,reference,0,indexed,0,0);
        require(!operation.complete&&std::strcmp(operation.status,"OTHER_AREA_CALLSITE")==0,"module-overflow-refused");++count;
        input=setup();put(input.spans[4].bytes,0,std::uint32_t(0));put(input.spans[5].bytes,0,std::uint64_t(0));operation=call(input);
        require(operation.complete&&input.calls==3&&!operation.translation_applied&&!input.forbidden,"empty-header-is-not-geographical-absence");++count;
        input=setup();operation=d5ar::capture_operation(read,&input,module,module+0x21b26c1,0,0,indexed,0,0);
        require(!operation.complete&&!input.calls,"missing-reference-operand");++count;
        input=setup();operation=d5ar::capture_operation(read,&input,module,module+0x21b26c1,reference,0,UINT64_MAX,0,0);
        require(!operation.complete&&!input.calls,"indexed-extent-overflow");++count;
        input=setup();operation=d5ar::capture_operation(read,&input,0,module+0x21b26c1,reference,0,indexed,0,0);
        require(!operation.complete&&!input.calls,"missing-module");++count;
        std::cout<<"{\"status\":\"PASS\",\"controls\":"<<count<<",\"scope\":\"owned_operation_diagnostics_only\"}\n";return 0;
    }catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
}
