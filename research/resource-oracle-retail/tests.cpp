// SPDX-License-Identifier: GPL-3.0-or-later
#include "decode.h"
#include "sourcefiles.h"
#include <map>
#include <iostream>
#include <stdexcept>
#include <algorithm>
struct Memory {
    std::map<uint64_t,std::vector<unsigned char>> blocks;bool short_read=false,change=false;int headers=0;
    bool operator()(uint64_t p,void* out,size_t n){
        if(short_read&&p==0x20000)return false;
        if(change&&p==0x10000&&++headers==2)return false;
        for(auto& [a,b]:blocks)if(p>=a&&p-a<=b.size()&&n<=b.size()-(p-a)){memcpy(out,b.data()+p-a,n);return true;}return false;
    }
    template<class T>void put(uint64_t p,size_t off,T v){auto& b=blocks[p];b.resize(std::max(b.size(),off+sizeof v));memcpy(b.data()+off,&v,sizeof v);}
};
Memory fixture(){Memory m; m.put(0x10000,0,retail::Header{0x20000,0x20010,0x20010});
    m.put<uint64_t>(0x20000,0,0x30000);m.put<uint64_t>(0x20000,8,0x40000);
    for(auto p:{0x30000ULL,0x40000ULL}){m.blocks[p].resize(0x30);m.put<uint32_t>(p,0x28,p==0x30000?0x57d4:0x57cf);m.put<uint8_t>(p,0x2e,0x9f);}return m;}
void check(bool ok,const char* name){if(!ok)throw std::runtime_error(name);std::cout<<name<<" PASS\n";}
int main(){try{
    auto m=fixture();auto p=retail::population(m,0x10000,true);
    check(p.complete&&p.members.size()==2&&retail::field<uint32_t>(p.members[0].raw,0x28)==0x57d4,"native-resource-header");
    m.put(0x10000,0,retail::Header{});check(retail::population(m,0x10000,true).complete,"initialized-empty");
    check(!retail::population(m,0x10000,false).complete,"null-unqualified");
    m=fixture();m.put(0x10000,0,retail::Header{0xfffffffffffffff8ULL,0,8});check(!retail::population(m,0x10000,true).complete,"overflow");
    m=fixture();m.put(0x10000,0,retail::Header{0x20000,0x28008,0x28008});check(!retail::population(m,0x10000,true).complete,"large-count");
    m=fixture();m.put<uint64_t>(0x20000,8,8);p=retail::population(m,0x10000,true);check(!p.complete&&p.members.empty(),"invalid-pointer-no-prefix");
    m=fixture();m.short_read=true;check(!retail::population(m,0x10000,true).complete,"short-read");
    m=fixture();m.blocks[0x40000].resize(0x2f);check(!retail::population(m,0x10000,true).complete,"resource-short-read");
    m=fixture();m.put<uint8_t>(0x40000,0x2e,0x1e);check(!retail::population(m,0x10000,true).complete,"wrong-type");
    m=fixture();m.change=true;check(!retail::population(m,0x10000,true).complete,"header-alias-change");
    const uint64_t base=0x7ff600000000;
    for(int i=0;i<4;++i)check(retail::owned_slot(base,base+retail::sites[i],1ULL<<i)==i,"four-slot-map");
    check(retail::owned_slot(base,base+retail::sites[0],3)==-1,"multiple-trap-refusal");
    check(retail::owned_slot(base,base+retail::sites[0]+1,1)==-1,"wrong-instruction-PC");
    check(std::string(retail::selector(base,base+0x5f5d830))=="biome"&&std::string(retail::selector(base,0))=="UNKNOWN","native-selector");
    retail::Join j{7,0x100000,0x22222,true};check(j.matches(7,0x100000)&&!j.matches(8,0x100000)&&!j.matches(7,0x100008),"thread-stack-join");
    // Independently construct native BC/reference layout, not fixture magic ABI.
    m={};m.blocks[0x50000].resize(0xd0);m.put<uint8_t>(0x50000,0x2e,0x4a);m.put<uint64_t>(0x50000,0x98,0x60000);m.put<uint64_t>(0x50000,0xc8,0x70000);
    m.blocks[0x60000].resize(0x30);m.put<uint32_t>(0x60000,0x28,0x2c60e9);m.put<uint8_t>(0x60000,0x2e,0x1e);
    m.put<uint64_t>(0x70000,8,0x80000);m.blocks[0x80000].resize(0xa0);m.put<uint8_t>(0x80000,0x12,0xbc);m.put<uint64_t>(0x80000,0,base+0x4c24e60);m.put<uint64_t>(0x80000,0x98,0x85f5fc4c6f86a5c3ULL);
    check(retail::identity(m,0x50000,base).bound,"BC-identity-positive");
    m.put<uint64_t>(0x80000,0x98,1);check(!retail::identity(m,0x50000,base).bound,"wrong-workshop");
    m.put<uint8_t>(0x80000,0x12,1);m.put<uint64_t>(0x80000,8,0x80000);check(!retail::identity(m,0x50000,base).bound,"extra-cycle");
    auto source_fixture=[&]{Memory f;f.put<uint16_t>(0x90000,0x30,0);f.put<uint32_t>(base+0x5e881e8,0,1);
        f.put<uint64_t>(base+0x5e881f0,0,0xa0000);f.put<uint64_t>(0xa0000,0,0xb0000);
        f.blocks[0xb0000].resize(16);f.put<uint64_t>(0xb0000,0,0xc0000);f.put<int32_t>(0xb0000,8,1);f.put<uint64_t>(0xc0000,0,0xd0000);
        f.blocks[0xd0000].resize(0x370);f.put<uint64_t>(0xd0000,0,base+0x4b29b80);
        memcpy(f.blocks[0xd0000].data()+0x38,"Starfield.esm",14);return f;};
    auto source=source_fixture();auto proof=retail::provenance(source,0x90000,base,0x57d4);
    check(proof.complete&&proof.main_identity&&proof.files[0].name=="Starfield.esm","resource-file-positive");
    source=source_fixture();source.put<uint16_t>(0x90000,0x30,0xffff);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-sentinel");
    source=source_fixture();source.put<uint16_t>(0x90000,0x30,1);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-index-range");
    source=source_fixture();source.blocks[0x90000].resize(0x30);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-index-unreadable");
    source=source_fixture();source.put<uint64_t>(base+0x5e881f0,0,0);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-null-table");
    source=source_fixture();source.put<uint64_t>(0xa0000,0,0);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-null-slot");
    for(int count:{0,-1,129}){source=source_fixture();source.put<int32_t>(0xb0000,8,count);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-count-refusal");}
    source=source_fixture();source.blocks[0xc0000].resize(7);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-short-list");
    source=source_fixture();source.put<uint64_t>(0xd0000,0,1);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-wrong-vtable");
    source=source_fixture();source.blocks[0xd0000].resize(0x36f);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-short-file");
    source=source_fixture();memset(source.blocks[0xd0000].data()+0x38,'A',0x104);check(!retail::provenance(source,0x90000,base,0x57d4).complete,"source-nonterminated-string");
    source=source_fixture();source.blocks[0xd0000][0x38]='X';check(!retail::provenance(source,0x90000,base,0x57d4).main_identity,"source-other-file");
    source=source_fixture();source.put<uint8_t>(0xd0000,0x218,1);check(!retail::provenance(source,0x90000,base,0x57d4).main_identity,"source-other-namespace");
    for(uint32_t flag:{0x100,0x200,0x400}){source=source_fixture();source.put<uint32_t>(0xd0000,0x1b8,flag);check(!retail::provenance(source,0x90000,base,0x57d4).main_identity,"source-special-branch-unknown");}
    source=source_fixture();int seen=0;auto changing=[&](uint64_t at,void* out,size_t size){if(at==0xa0000&&++seen==2)return false;return source(at,out,size);};
    auto changed=retail::provenance(changing,0x90000,base,0x57d4);
    check(!changed.complete&&!changed.main_identity,"source-slot-alias-change");
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
