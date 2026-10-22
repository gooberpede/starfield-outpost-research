// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "../resource-oracle-retail/decode.h"
#include <algorithm>
// Retail 1.16.244.0 only. Static provenance: ui15/ui16; see sources.csv.
// External readers only. Object offsets are not VAs or saved identifiers.
namespace ancestry {
constexpr uint32_t sites[]={0x21e07d0,0x21e1772,0x21e174e,0x21e0bf4};
struct Invocation {
    uint64_t token{},updater_token{},parent{},bp{},closure{},slot{},source{},key{},temporary{},reference{},callback_bp{};
    bool frame=false, source_ok=false;
};
struct State {
    uint64_t serial=0;
    std::vector<Invocation> stack;
    Invocation begin(uint64_t bp) {
        // Sequential source callbacks share an updater frame; nested updater
        // calls have lower stack addresses. No timestamp or pointer epoch.
        while(!stack.empty() && stack.back().bp<=bp)stack.pop_back();
        Invocation i;i.token=++serial;i.updater_token=i.token;
        i.parent=stack.empty()?0:stack.back().token;i.bp=bp;
        return i;
    }
    Invocation* find(uint64_t bp){
        for(auto i=stack.rbegin();i!=stack.rend();++i)if(i->bp==bp)return &*i;
        return nullptr;
    }
    void finish(uint64_t bp){
        auto i=std::find_if(stack.begin(),stack.end(),[&](auto& v){return v.bp==bp;});
        if(i!=stack.end())stack.erase(i,stack.end());
    }
};
struct Geometry {
    unsigned char header[0x30]{};
    std::vector<unsigned char> points;
    bool complete=false;
    std::string reason="region-read";
    std::string json()const{
        std::ostringstream s;s<<"{\"status\":\""<<(complete?"COMPLETE":"INCOMPLETE")
          <<"\",\"reason\":\""<<reason<<"\",\"raw_region\":\""<<retail::hex(header,sizeof header)
          <<"\",\"ordered_xyzw\":";
        if(complete)s<<'"'<<retail::hex(points.data(),points.size())<<'"';else s<<"null";
        s<<'}';return s.str();
    }
};
template<class R>Geometry geometry(R& read,uint64_t p,size_t budget=65536){
    Geometry g;if(!retail::range(p,48)||!read(p,g.header,48))return g;
    auto n=retail::field<uint32_t>(g.header,0x18),cap=retail::field<uint32_t>(g.header,0x1c);
    auto data=retail::field<uint64_t>(g.header,0x20);
    auto fail=[&](const char* why){g.reason=why;g.points.clear();return g;};
    if(n>cap)return fail("count-capacity");
    if(n>4096 || cap>4096 || size_t(n)*16>budget)return fail("point-budget");
    if(n && (!retail::range(data,size_t(n)*16)||data%4))return fail("point-pointer");
    g.points.resize(size_t(n)*16);
    if(n && !read(data,g.points.data(),g.points.size()))return fail("point-read");
    unsigned char again[48]{};
    if(!read(p,again,48)||memcmp(again,g.header,48))return fail("region-changed");
    g.complete=true;g.reason="copied-at-stop-not-epoch";return g;
}
// Resolve the actually selected resource slot and region ordinal, not an
// independently searched same-FormID candidate. Failed reads remain INCOMPLETE.
template<class R>std::string decision(R& read,uint64_t source,uint64_t displacement,
                                     uint64_t resource,uint64_t region){
    uint64_t slots=0,capacity=0,collection=0;unsigned char slot[24]{},col[24]{},res[48]{};
    std::string reason="ancestry-read";bool ok=false;uint64_t ordinal=0;
    if(retail::range(source,0x30)&&read(source+0x20,&slots,8)&&read(source+0x28,&capacity,8)){
        if(capacity>4096 || displacement%24 || displacement/24>=capacity)reason="resource-slot-budget";
        else if(retail::range(slots,capacity*24)&&read(slots+displacement,slot,24)
             && retail::field<uint32_t>(slot,16)!=0xffffffffU
             && retail::range(resource,48)&&read(resource,res,48)){
            collection=retail::field<uint64_t>(slot,8);
            if(res[0x2e]!=0x9f||retail::field<uint32_t>(res,0x28)!=retail::field<uint32_t>(slot,0))reason="resource-key-type";
            else if(retail::range(collection,24)&&read(collection,col,24)){
                auto n=retail::field<uint32_t>(col,8),cap=retail::field<uint32_t>(col,12);
                auto data=retail::field<uint64_t>(col,16);
                if(n>cap||cap>4096)reason="collection-budget";
                else if(n && retail::range(data,size_t(n)*48)&&region>=data && (region-data)%48==0 && (region-data)/48<n){
                    ordinal=(region-data)/48;ok=true;reason="selected-slot-region";
                }else reason="region-outside-collection";
            }
        }
    }
    std::ostringstream s;s<<"{\"status\":\""<<(ok?"COMPLETE":"INCOMPLETE")<<"\",\"reason\":\""<<reason
      <<"\",\"source_wrapper\":"<<source<<",\"slot_displacement\":"<<displacement
      <<",\"slot_pointer\":"<<(slots+displacement)<<",\"collection_pointer\":"<<collection
      <<",\"region_pointer\":"<<region<<",\"ordinal\":";
    if(ok)s<<ordinal;else s<<"null";
    s<<",\"raw_slot\":\""<<retail::hex(slot,24)<<"\",\"raw_collection\":\""<<retail::hex(col,24)
      <<"\",\"raw_resource\":\""<<retail::hex(res,48)<<"\"}";return s.str();
}
}
