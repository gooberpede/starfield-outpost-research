// SPDX-License-Identifier: GPL-3.0-or-later
// Synthetic target-owned nodes, map buckets and displaced arrays. This fixture
// implements its own literal test operations; no production decoder is linked.
#include <windows.h>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <algorithm>
#include <barrier>
static std::barrier concurrent_boundary(2);
struct Array { uint32_t count{},capacity{};uint32_t* words{}; };
struct Bucket { uint32_t key{},pad{};Array a{};uint32_t link=0xffffffffU,tail{}; };
static_assert(sizeof(Bucket)==32);
static thread_local unsigned char page[0x4000];
static thread_local std::vector<std::vector<uint32_t>> allocations;
static thread_local Bucket buckets[16];
static thread_local uint32_t roots[8],slots[8][6],population=0,cursor=0;
static thread_local std::string mode;
static thread_local unsigned char resources[4][0x118];
static thread_local uint64_t candidates[32];
static thread_local void* generation_frame;
static thread_local unsigned char* retained_source;
extern "C" void diagnostic_run(void*,void*,void*,uint64_t);
template<class T>static void put(void* p,size_t n,T v){memcpy(static_cast<char*>(p)+n,&v,sizeof v);}
extern "C" void map_fixture_config(const char* value){mode=value;}
extern "C" void map_fixture_source(void* value){retained_source=static_cast<unsigned char*>(value);}
extern "C" void map_fixture_begin(void* frame){
    if(mode=="map-concurrent")concurrent_boundary.arrive_and_wait();
    generation_frame=frame;cursor=0;population=3;allocations.clear();
    memset(roots,0,sizeof roots);memset(slots,0,sizeof slots);memset(page,0,sizeof page);
    for(auto& b:buckets)b=Bucket{};
    // Exact authored reference history: zero-root Water carrier, Tungsten direct
    // supply, then Chlorine. A distinct exchange fixture reaches the same map.
    roots[0]=0;slots[0][0]=0x83ec;slots[0][2]=0x83ec;
    roots[1]=0x57d5;slots[1][1]=0x57c4;
    roots[2]=0x99;slots[2][5]=0x1234;
    if(mode=="map-exchange"){
        population=4;roots[1]=0x123;roots[2]=0x123;slots[2][5]=0;
        roots[3]=0x57d5;
    }
    if(mode=="map-order"){
        std::swap(roots[0],roots[1]);for(int k=0;k<6;++k)std::swap(slots[0][k],slots[1][k]);
    }
    if(mode=="map-null")memset(slots,0,sizeof slots);
    if(mode=="map-duplicate-root"){roots[2]=roots[1];slots[2][5]=0;}
    if(mode=="map-empty"||mode=="map-cache")population=0;
    if(mode=="map-malformed")population=1;
    for(uint32_t j=0;j<population;++j){
        uint16_t displacement=uint16_t(0x100+j*0x100);
        put(page,0x12+j*4,displacement);
        auto node=page+displacement;
        put(node,0x10,uint64_t(0x5de4c00010001ULL));put(node,0x18,uint64_t(j+1));
        if(mode=="map-wrong-owner")put(node,0x10,uint64_t(0x100010001ULL));
        if(mode=="map-wrong-type")put(node,0x10,uint64_t(0x5de4c00010002ULL));
        if(mode=="map-out-of-range")put(node,0x18,uint64_t(0x1000000000000ULL+j));
        put(node,0x60,uint32_t(0x1000+j));put(node,0x70,roots[j]);
        memcpy(node+0x74,slots[j],24);
    }
    // Preserve the caller's 32-byte Windows argument home area: the compiler
    // may retain this function's own frame argument there at /Od.
    memset(static_cast<char*>(frame)+0x20,0,0x260);
    put(frame,0x130,uint32_t(0x57d5));
    put(frame,0x210+0x18,reinterpret_cast<uint64_t>(buckets));
    put(frame,0x210+0x20,uint64_t(16));
    for(int k=0;k<4;++k){memset(resources[k],0,sizeof resources[k]);
        put(resources[k],0x28,uint32_t(k==0?0x83ec:k==1?0x57c4:k==2?0x57d5:0x1234));
        resources[k][0x2e]=0x9f;resources[k][0x110]=uint8_t(k==0?6:k==1?1:0);}
}
extern "C" int map_fixture_next(void* iterator){
    if(cursor>=population)return 0;
    put(iterator,0x18,reinterpret_cast<uint64_t>(page));put(iterator,0x20,uint64_t(cursor++));
    put(iterator,0x28,uint64_t(0x5de4c00010001ULL));put(iterator,0x30,uint64_t(0xffffffffffffULL));
    if(mode=="map-malformed")put(iterator,0x18,uint64_t(8));
    if(mode=="map-incomplete"&&cursor>1)put(iterator,0x18,uint64_t(8));
    return 1;
}
static Array make_array(const std::vector<uint32_t>& v){
    allocations.push_back(v);auto& a=allocations.back();
    return Array{uint32_t(a.size()),uint32_t(a.size()),a.data()};
}
extern "C" void map_fixture_step(void*,Array* stage,void*){
    uint32_t j=cursor-1;
    if(mode=="map-nested"&&j==0){
        unsigned char old_page[sizeof page];memcpy(old_page,page,sizeof page);
        Bucket old_buckets[16];memcpy(old_buckets,buckets,sizeof buckets);
        uint32_t old_roots[8],old_slots[8][6];memcpy(old_roots,roots,sizeof roots);memcpy(old_slots,slots,sizeof slots);
        auto old_allocations=std::move(allocations);auto old_cursor=cursor,old_population=population;
        mode="map-direct";
        diagnostic_run(retained_source,retained_source+0x10,retained_source,0x5de4c);
        mode="map-nested";allocations=std::move(old_allocations);cursor=old_cursor;population=old_population;
        memcpy(page,old_page,sizeof page);memcpy(buckets,old_buckets,sizeof buckets);
        memcpy(roots,old_roots,sizeof roots);memcpy(slots,old_slots,sizeof slots);
    }
    if(mode=="map-source-reuse"&&j==0)put(retained_source,0,uint32_t(0x112233));
    std::vector<uint32_t> values;
    for(uint32_t k=0;k<stage->count;++k)values.push_back(stage->words[k]);
    for(int k=0;k<6;++k)if(slots[j][k])values.push_back(slots[j][k]);
    *stage=make_array(values);
    if(roots[j]){
        Bucket* found=nullptr;
        for(auto& b:buckets)if(b.link!=0xffffffffU&&b.key==roots[j])found=&b;
        if(!found)for(auto& b:buckets)if(b.link==0xffffffffU){found=&b;b.key=roots[j];b.link=16;break;}
        std::swap(*stage,found->a);
    }
    if(mode=="map-corrupt")stage->count=5000;
}
extern "C" uint64_t map_fixture_candidates(void* frame){
    if(mode=="map-concurrent")concurrent_boundary.arrive_and_wait();
    uint32_t n=0;
    for(auto& b:buckets)if(b.link!=0xffffffffU&&b.key==0x57d5){
        for(uint32_t k=0;k<b.a.count&&k<16;++k){
            auto id=b.a.words[k];for(int r=0;r<4;++r)if(*reinterpret_cast<uint32_t*>(resources[r]+0x28)==id)candidates[n++]=reinterpret_cast<uint64_t>(resources[r]);
        }
        candidates[n++]=reinterpret_cast<uint64_t>(resources[2]);break;
    }
    std::stable_sort(candidates,candidates+n,[](uint64_t a,uint64_t b){return *reinterpret_cast<unsigned char*>(a+0x110)>*reinterpret_cast<unsigned char*>(b+0x110);});
    put(frame,0x40,n);put(frame,0x44,n);put(frame,0x50,reinterpret_cast<uint64_t>(candidates));put(frame,0x58,uint32_t(0x57d5));
    return reinterpret_cast<uint64_t>(candidates);
}
extern "C" int map_fixture_has_descriptor(){return mode!="map-bypass";}
