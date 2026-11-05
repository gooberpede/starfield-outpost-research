// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Owned structural copier controls. These do not replace original-instruction
// lock/destructor tests or establish actual retail outpost/area attribution.
#include "capture.h"
#include <iostream>

namespace d5ar::fixture {
struct Memory {
    std::array<unsigned char,0x60> proc{};
    std::array<unsigned char,48> map{},resources{};
    std::array<unsigned char,0x40> holder{};
    std::array<unsigned char,24> collection{};
    std::array<unsigned char,48> region{};
    std::array<unsigned char,32> points{};
    std::array<unsigned char,0x70> source{},other_source{};
    std::atomic<std::uint64_t> epoch{1},hazards{};
    std::uint64_t fail_at{},change_epoch_at{};
    bool diagnostics_fail{};
    unsigned reads{},source_reads{};
    template<class T,std::size_t N> static void put(std::array<unsigned char,N>& data,std::size_t offset,T value) {
        if(offset+sizeof value>N)throw std::runtime_error("Fixture field out of bounds");
        std::memcpy(data.data()+offset,&value,sizeof value);
    }
    template<std::size_t N> static std::uint64_t ptr(std::array<unsigned char,N>& data) {
        return reinterpret_cast<std::uint64_t>(data.data());
    }
    Memory() {
        put(proc,0x20,ptr(map));put(proc,0x28,std::uint64_t(2));put(proc,0x44,std::uint32_t(1));
        put(map,0,ptr(source));put(map,8,ptr(holder));put(map,16,std::uint32_t(0));
        put(map,24,ptr(other_source));put(map,32,std::uint64_t(0));put(map,40,std::uint32_t(0));
        put(holder,0x20,ptr(resources));put(holder,0x28,std::uint64_t(2));
        put(resources,0,std::uint32_t(7));put(resources,8,ptr(collection));put(resources,16,std::uint32_t(0));
        put(resources,40,std::uint32_t(UINT32_MAX));
        put(collection,8,std::uint32_t(1));put(collection,12,std::uint32_t(1));put(collection,16,ptr(region));
        put(region,16,std::uint32_t(7));put(region,24,std::uint32_t(2));put(region,28,std::uint32_t(2));put(region,32,ptr(points));
        for(std::size_t i=0;i<points.size();++i)points[i]=static_cast<unsigned char>(i);
        put(source,0,std::uint32_t(123));put(source,0x38,std::uint8_t(2));put(source,0x68,std::uint32_t(456));
    }
    template<std::size_t N> static bool copy(std::array<unsigned char,N>& data,std::uint64_t at,void* output,std::size_t size) {
        auto start=ptr(data);
        if(at<start||at-start>N||size>N-(at-start))return false;
        std::memcpy(output,data.data()+(at-start),size);return true;
    }
    static bool read(void* context,std::uint64_t at,void* output,std::size_t size) {
        auto& value=*static_cast<Memory*>(context);++value.reads;
        if((at>=ptr(value.source)&&at-ptr(value.source)<value.source.size())||
           (at>=ptr(value.other_source)&&at-ptr(value.other_source)<value.other_source.size()))++value.source_reads;
        if(value.change_epoch_at==at)++value.epoch;
        if(value.fail_at==at)return false;
        if(value.diagnostics_fail&&at>=ptr(value.source)&&at<ptr(value.source)+value.source.size())return false;
        return copy(value.proc,at,output,size)||copy(value.map,at,output,size)||copy(value.resources,at,output,size)||
            copy(value.holder,at,output,size)||copy(value.collection,at,output,size)||copy(value.region,at,output,size)||
            copy(value.points,at,output,size)||copy(value.source,at,output,size)||copy(value.other_source,at,output,size);
    }
    Capture run(std::uint64_t budget=1000000,bool source_admitted=true) {
        // These arrays remain owned by this fixture object for the entire call.
        return copy_resident(read,this,ptr(proc),budget,epoch,hazards,nullptr,source_admitted);
    }
};
inline int execute() {
    unsigned checks=0;
    auto check=[&](bool condition,const char* label) {
        if(!condition)throw std::runtime_error(label);++checks;
    };
    {
        Memory m;auto result=m.run();check(result.status=="COPIED_UNQUALIFIED","complete owned copy");
        check(result.holders.size()==2&&result.holders[0].complete&&!result.holders[1].complete,"all holder dispositions");
        check(result.holders[0].resources[0].regions[0].points==std::vector<std::uint8_t>(m.points.begin(),m.points.end()),"all point words");
        check(result.required_bytes>32,"measured complete required capacity");
        check(result.holders[0].source_diagnostics.complete&&result.holders[0].source_diagnostics.visited==456,"separate source token diagnostics");
    }
    {Memory m;Memory::put(m.proc,0x28,std::uint64_t(0));auto r=m.run();check(r.status=="COPIED_UNQUALIFIED"&&r.holders.empty(),"empty represented map");}
    {Memory m;auto r=m.run(1000000,false);check(r.status=="COPIED_UNQUALIFIED"&&r.holders[0].complete&&
        std::string(r.holders[0].source_diagnostics.status)=="NOT_CAPTURED"&&!m.source_reads,
        "unadmitted source lifetime never followed; healthy geometry retained");}
    {Memory m;Memory::put(m.proc,0x44,std::uint32_t(0));check(m.run().status=="NOT_FOREIGN_READER_CONTEXT","missing reader refuses");}
    {Memory m;Memory::put(m.proc,0x44,std::uint32_t(0xffc00001));check(m.run().status=="NOT_FOREIGN_READER_CONTEXT","exclusive recursion refuses");}
    {Memory m;m.hazards=1;auto r=m.run();check(r.status=="LIFETIME_UNQUALIFIED"&&m.reads==0,"active destruction before any borrowed read");}
    {Memory m;m.change_epoch_at=Memory::ptr(m.points);check(m.run().status=="LIFETIME_OVERLAP","destruction epoch overlap");}
    {Memory m;m.fail_at=Memory::ptr(m.points);auto r=m.run();check(r.status=="READ_FAILED"&&(r.holders.empty()||!r.holders[0].complete),"partial copy never complete");}
    {Memory m;Memory::put(m.region,24,std::uint32_t(3));check(m.run().status=="MALFORMED_POINT_COUNT_OR_FORM","malformed nested count");}
    {Memory m;Memory::put(m.region,16,std::uint32_t(8));check(m.run().status=="MALFORMED_POINT_COUNT_OR_FORM","wrong region resource");}
    {Memory m;Memory::put(m.collection,8,std::uint32_t(2));check(m.run().status=="MALFORMED_REGION_COUNT","malformed outer count");}
    {Memory m;Memory::put(m.map,24,Memory::ptr(m.source));check(m.run().status=="DUPLICATE_SOURCE_KEY","source ABA duplicate refuses");}
    {Memory m;std::memcpy(m.resources.data()+24,m.resources.data(),24);check(m.run().status=="DUPLICATE_RESOURCE","rehash duplicate refuses");}
    {Memory m;check(m.run(1).status=="MEASURED_CAPACITY_EXCEEDED","measured memory capacity refusal");}
    {Memory m;m.diagnostics_fail=true;auto r=m.run();check(r.status=="COPIED_UNQUALIFIED"&&std::string(r.holders[0].source_diagnostics.status)=="READ_FAILED","unknown source preserves healthy geometry");}
    {Memory m;Memory::put(m.holder,0x28,std::uint64_t(0));auto r=m.run();check(r.holders[0].complete&&r.holders[0].disposition=="EMPTY","empty holder explicit");}
    {Memory m;Memory::put(m.resources,8,std::uint64_t(0));check(m.run().status=="MALFORMED_ADDRESS","missing nested collection refuses");}
    {Memory m;Memory::put(m.proc,0x28,std::uint64_t(UINT64_MAX));check(m.run().status=="MALFORMED_ADDRESS","overflowing map extent refusal");}
    {Memory m;Memory::put(m.collection,12,std::uint32_t(UINT32_MAX));Memory::put(m.region,28,std::uint32_t(UINT32_MAX));
        check(m.run().status=="COPIED_UNQUALIFIED","unused native capacity never truncates healthy represented geometry");}
    std::cout<<"PASS owned capture controls "<<checks<<'\n';return 0;
}
}
