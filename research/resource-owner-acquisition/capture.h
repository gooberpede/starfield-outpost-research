// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "../resource-tungsten-acquisition/decode.h"
#include <map>
// All pointers here are stopped-target runtime VAs. The reader enforces exact
// foreign copies and the inherited per-sample byte budget. No target writes.
namespace owner_capture {
struct Frame { uint64_t entry{},token{},source{},owner{},map{},loops{}; unsigned phase{}; };
template<class R>std::string array(R& read,uint64_t at,unsigned width=4,unsigned pointer_offset=8){
    unsigned char h[24]{},again[24]{};size_t header_size=pointer_offset+8;
    bool ok=header_size<=sizeof h&&read(at,h,header_size);
    auto count=retail::field<uint32_t>(h,0),capacity=retail::field<uint32_t>(h,4);
    auto ptr=retail::field<uint64_t>(h,pointer_offset);
    ok=ok&&count<=capacity&&capacity<=4096;
    std::vector<unsigned char> b(ok?size_t(count)*width:0);
    if(ok&&count)ok=read(ptr,b.data(),b.size());
    if(ok)ok=read(at,again,header_size)&&!memcmp(h,again,header_size);
    std::ostringstream out;
    out<<"{\"status\":\""<<(ok?"COMPLETE":"INCOMPLETE")<<"\",\"header_address\":"<<at
       <<",\"header_raw\":\""<<retail::hex(h,header_size)<<"\",\"count\":"<<count<<",\"capacity\":"<<capacity
       <<",\"pointer\":"<<ptr<<",\"width\":"<<width<<",\"raw\":";
    if(ok)out<<'"'<<retail::hex(b.data(),b.size())<<'"';else out<<"null";
    out<<'}';return out.str();
}
template<class R>std::string map(R& read,uint64_t at){
    unsigned char h[0x30]{},again[0x30]{};
    bool ok=read(at,h,sizeof h);
    auto ptr=retail::field<uint64_t>(h,0x18),capacity=retail::field<uint64_t>(h,0x20);
    ok=ok&&capacity<=1024&&(!capacity||!(capacity&(capacity-1)));
    std::vector<unsigned char> buckets(ok?size_t(capacity)*32:0);
    if(ok&&capacity)ok=read(ptr,buckets.data(),buckets.size());
    std::ostringstream entries;entries<<'[';bool first=true;
    if(ok)for(size_t j=0;j<capacity;++j){
        auto p=buckets.data()+j*32;
        if(retail::field<uint32_t>(p,0x18)==0xffffffffU)continue;
        if(!first)entries<<',';first=false;
        entries<<"{\"bucket\":"<<j<<",\"key\":"<<retail::field<uint32_t>(p,0)
               <<",\"array\":"<<array(read,ptr+j*32+8)<<'}';
    }
    entries<<']';
    if(ok)ok=read(at,again,sizeof again)&&!memcmp(h,again,sizeof h);
    // A second bucket copy detects mutation during the stopped snapshot. This
    // does not establish an all-writer lifetime or historical generation epoch.
    std::vector<unsigned char> verify(buckets.size());
    if(ok&&capacity)ok=read(ptr,verify.data(),verify.size())&&verify==buckets;
    std::ostringstream out;
    out<<"{\"status\":\""<<(ok?"COMPLETE":"INCOMPLETE")<<"\",\"address\":"<<at
       <<",\"header_raw\":\""<<retail::hex(h,sizeof h)<<"\",\"capacity\":"<<capacity
       <<",\"buckets_raw\":";
    if(ok)out<<'"'<<retail::hex(buckets.data(),buckets.size())<<'"';else out<<"null";
    out<<",\"entries\":"<<entries.str()<<'}';return out.str();
}
}
