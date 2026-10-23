// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
// Source: C1B dataflow/output-contract, pinned retail 1.16.244.0 only.
// Reader returns true only for an exact external copy. No target dereferences.
namespace retail {
constexpr uint64_t last_user=0x7fffffffffffULL;
inline bool range(uint64_t p,size_t n) {
    return n && p>=0x10000 && p<=last_user && n-1<=last_user-p;
}
inline std::string hex(const void* p,size_t n) {
    std::ostringstream s;s<<std::hex<<std::setfill('0');
    auto b=static_cast<const unsigned char*>(p);
    for(size_t i=0;i<n;++i)s<<std::setw(2)<<unsigned(b[i]);return s.str();
}
template<class T>T field(const unsigned char* p,size_t o){T v{};memcpy(&v,p+o,sizeof v);return v;}
struct Header {uint64_t begin{},end{},capacity{};};
struct Member {uint64_t pointer{};unsigned char raw[0x30]{};};
struct Population {
    Header header{};std::vector<Member> members;std::string reason;
    bool complete=false;
    std::string json()const {
        std::ostringstream s;s<<"{\"begin\":"<<header.begin<<",\"end\":"<<header.end<<",\"capacity\":"<<header.capacity
          <<",\"status\":\""<<(complete?"COMPLETE":"INCOMPLETE")<<"\",\"reason\":\""<<reason<<"\",\"members\":";
        if(!complete)s<<"null";else {s<<'[';for(size_t i=0;i<members.size();++i){if(i)s<<',';auto& m=members[i];
            s<<"{\"pointer\":"<<m.pointer<<",\"runtime_formid\":"<<field<uint32_t>(m.raw,0x28)
             <<",\"type\":"<<unsigned(m.raw[0x2e])<<",\"raw\":\""<<hex(m.raw,0x30)<<"\"}";}s<<']';}s<<'}';return s.str();
    }
};
template<class Reader>Population population(Reader& read,uint64_t at,bool initialized) {
    Population p;auto fail=[&](const char* why){p.reason=why;p.members.clear();return p;};
    if(!range(at,24)||!read(at,&p.header,24))return fail("header-read");
    auto h=p.header;
    if(h.begin>h.end||h.end>h.capacity||h.begin%8||h.end%8||h.capacity%8)return fail("range");
    uint64_t count=(h.end-h.begin)/8,capacity=(h.capacity-h.begin)/8;
    if(count>4096||capacity>4096)return fail("budget");
    if(!initialized && !h.begin && !h.end && !h.capacity)return fail("unqualified-null-header");
    if(h.capacity && !range(h.begin,static_cast<size_t>(h.capacity-h.begin)))return fail("pointer-range");
    std::vector<uint64_t> pointers(static_cast<size_t>(count));
    if(count && (!range(h.begin,static_cast<size_t>(count)*8)||!read(h.begin,pointers.data(),pointers.size()*8)))return fail("pointer-read");
    for(auto ptr:pointers){Member m;m.pointer=ptr;
        if(!range(ptr,0x30)||!read(ptr,m.raw,0x30))return fail("resource-read");
        if(m.raw[0x2e]!=0x9f)return fail("resource-type");p.members.push_back(m);}
    Header again{};if(!read(at,&again,24)||memcmp(&h,&again,24))return fail("header-changed");
    p.complete=true;return p;
}
constexpr uint32_t sites[]={0x21b26bc,0x21e0bf4,0x21f6b58,0x15796fc};
inline int owned_slot(uint64_t base,uint64_t rip,uint64_t dr6,const uint32_t* map=sites) {
    for(int i=0;i<4;++i)if(rip==base+map[i]&&(dr6&15)==(1ULL<<i)&&!(dr6&0x6000))return i;
    return -1;
}
inline const char* selector(uint64_t base,uint64_t pointer){
    return pointer==base+0x5f5d800?"spatial":pointer==base+0x5f5d818?"atmosphere":pointer==base+0x5f5d830?"biome":"UNKNOWN";
}
// A per-thread observation is not an owner epoch or all-writer interval.
struct Join {uint64_t lifetime{},rsp{},node{};bool active=false;
    bool matches(uint64_t t,uint64_t stack)const{return active&&t==lifetime&&stack==rsp;}
};
struct Identity {
    unsigned char ref[0xd0]{},base[0x30]{},extra[0xa0]{},cell[0x118]{};
    uint64_t extra_pointer{};bool bound=false;std::string reason="unreadable";
};
template<class Reader>Identity identity(Reader& read,uint64_t reference,uint64_t base,uint64_t expected_workshop) {
    Identity id;
    if(!range(reference,sizeof id.ref)||!read(reference,id.ref,sizeof id.ref))return id;
    auto bp=field<uint64_t>(id.ref,0x98),list=field<uint64_t>(id.ref,0xc8);uint64_t node{};
    if(id.ref[0x2e]!=0x4a||!range(bp,0x30)||!read(bp,id.base,0x30)||
       field<uint32_t>(id.base,0x28)!=0x2c60e9||id.base[0x2e]!=0x1e){id.reason="reference-base";return id;}
    if(!range(list,0x10)||!read(list+8,&node,8))return id;
    std::vector<uint64_t> seen;
    for(unsigned n=0;node && n<64;++n){
        for(auto v:seen)if(v==node){id.reason="extra-cycle";return id;}seen.push_back(node);
        unsigned char h[0x18]{};
        if(!range(node,sizeof h)||!read(node,h,sizeof h))return id;
        if(h[0x12]==0xbc){
            id.extra_pointer=node;
            if(!read(node,id.extra,sizeof id.extra))return id;
            const auto uuid=expected_workshop;
            // Concrete BC vtable, never an untyped byte search.
            if(field<uint64_t>(id.extra,0)!=base+0x4c24e60){id.reason="extra-vtable";return id;}
            id.bound=!memcmp(id.extra+0x98,&uuid,8);id.reason=id.bound?"EXPECTED-BC-ID":"other-workshop";
            if(id.bound){
                auto cell=field<uint64_t>(id.ref,0xb0);
                if(!range(cell,sizeof id.cell)||!read(cell,id.cell,sizeof id.cell)||id.cell[0x2e]!=0x49||(field<uint32_t>(id.cell,0x48)&1)){
                    id.bound=false;id.reason="unqualified-stored-exterior-cell";
                }
            }
            return id;
        }
        node=field<uint64_t>(h,8);
    }
    id.reason=node?"extra-budget":"no-workshop";return id;
}
}
