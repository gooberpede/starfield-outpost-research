// SPDX-License-Identifier: GPL-3.0-or-later
#include "selection.h"
#include <iostream>
#include <stdexcept>
namespace {
constexpr std::uint64_t module=0x140000000,reference=0x20000;
struct Input {std::uint32_t id=0x12345678;std::uint8_t type=0x40;unsigned calls{},fail{};bool throws{};};
bool read(void* p,std::uint64_t at,void* out,std::size_t size) {
    auto& i=*static_cast<Input*>(p);++i.calls;if(i.throws)throw std::runtime_error("owned");if(i.calls==i.fail)return false;
    if(at==reference+0x28&&size==4){std::memcpy(out,&i.id,4);return true;}
    if(at==reference+0x2e&&size==1){std::memcpy(out,&i.type,1);return true;}return false;
}
void require(bool v,const char* why){if(!v)throw std::runtime_error(why);}
void copy(d5ar::SelectedLease& v,Input& i,std::uint64_t epoch=3){d5ar::copy_selected_lease(v,read,&i,module,module+0xf3e0c7,module+0x21b25dd,reference,epoch);}
bool link(d5ar::SelectedLease& v,std::uint64_t invocation=1,std::uint64_t command=2,std::uint64_t epoch=3,std::uint64_t operand=reference){return d5ar::link_selected_operation(v,invocation,command,epoch,module,module+0x21b26c1,operand);}
}
int main(){try {
unsigned count=0;Input i;auto v=d5ar::begin_selection(1,2,3);copy(v,i);
require(v.copied&&v.formid==i.id&&v.type==0x40&&i.calls==2&&link(v),"positive selected lease/invocation");++count;
require(std::strcmp(v.status,"SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME")==0,"scope status");++count;
for(unsigned failure=1;failure<=2;++failure){Input x;x.fail=failure;auto a=d5ar::begin_selection(1,2,3);copy(a,x);require(!a.copied&&!link(a),"partial identity refusal");++count;}
{Input x;x.throws=true;auto a=d5ar::begin_selection(1,2,3);copy(a,x);require(!a.copied&&!link(a),"exception refusal");++count;}
{Input x;auto a=d5ar::begin_selection(1,2,3);require(!link(a),"absent candidate");d5ar::end_selection(a);copy(a,x);require(x.calls==0&&!link(a),"early/ended scope");count+=2;}
for(auto pair: {std::pair<std::uint64_t,std::uint64_t>{0,2},{1,0}}){Input x;auto a=d5ar::begin_selection(pair.first,pair.second,3);copy(a,x);require(!a.copied&&x.calls==0,"unarmed scope");++count;}
{Input x;auto a=d5ar::begin_selection(1,2,3);copy(a,x,4);require(!a.copied&&!link(a),"phase mismatch");++count;}
{Input x;auto a=d5ar::begin_selection(1,2,3);copy(a,x);copy(a,x);require(a.ambiguous&&!link(a),"multiple selections");++count;}
{Input x;auto a=d5ar::begin_selection(1,2,3);d5ar::selection_ambiguous(a);copy(a,x);require(!a.copied&&!link(a),"nested ambiguity");++count;}
for(unsigned gate=0;gate<2;++gate){Input x;auto a=d5ar::begin_selection(1,2,3);d5ar::copy_selected_lease(a,read,&x,module,module+0xf3e0c7+gate,module+0x21b25dd+(1-gate),reference,3);require(!a.copied&&x.calls==0,"exact native caller gates");++count;}
for(unsigned mismatch=0;mismatch<4;++mismatch){auto a=v;require(!link(a,1+(mismatch==0),2+(mismatch==1),3+(mismatch==2),reference+(mismatch==3)),"same invocation/generation/epoch/operand only");++count;}
{auto a=v;d5ar::end_selection(a);require(!link(a),"aborted scope cannot link later samepointer");++count;}
{Input x;x.id=0x87654321;auto a=d5ar::begin_selection(4,5,3);copy(a,x);require(a.formid!=v.formid&&!link(a),"new operation different identity");++count;}
// Same-address/same-ID recycling after release is inherently unobservable here.
// The only certified record remains the earlier lease-time identity; no field
// or status represents allocation continuity at area time.
{auto a=v;require(link(a)&&std::strcmp(a.status,"SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME")==0,"samepointer reuse must not upgrade historical scope");++count;}
std::cout<<"{\"status\":\"PASS\",\"controls\":"<<count<<",\"scope\":\"owned_selection_time_identity_only\"}\n";return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
