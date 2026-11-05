// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Original D5AR copier, informed by the project-owned D5AI native ownership
// record. Reads only through the supplied checked reader; owns every output.
// Caller must prove the actual native reader callback and destructor coverage.
#include <array>
#include <algorithm>
#include <atomic>
#include <cstdint>
#include <cstring>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
#include "identity.h"
#include "source_lifetime.h"
#include "operation.h"
#include "binding.h"
#include "selection.h"

namespace d5ar {
using Read=bool(*)(void*,uint64_t,void*,size_t);
struct Region {std::array<uint8_t,24> header{};uint32_t count{};std::vector<uint8_t> points;};
struct Resource {uint32_t form{};std::vector<Region> regions;};
struct Holder {uint64_t source{},holder{},map_index{};std::string disposition="ALLOCATION_UNKNOWN";std::vector<Resource> resources;bool complete{};SourceDiagnostics source_diagnostics{};};
struct Capture {std::string status="REFUSED";uint64_t proc{},epoch_begin{},epoch_end{},lock_state{},required_bytes{},copy_begin_filetime{},copy_end_filetime{};std::vector<Holder> holders;OwnedOperation operation{};OwnedBinding binding_before{},binding_after{};SelectedLease selected_reference{};};
struct CopyFailure:std::runtime_error {using std::runtime_error::runtime_error;};

class Copier {
 Read read_;void* context_;uint64_t budget_,planned_holders_{};Capture& capture_;std::atomic<uint64_t>& epoch_;std::atomic<uint64_t>& hazards_;std::atomic<bool>* cancelled_;bool source_admitted_;SourceRecorder* source_recorder_;
public:
 Copier(Read reader,void* context,uint64_t budget,Capture& capture,std::atomic<uint64_t>& epoch,std::atomic<uint64_t>& hazards,std::atomic<bool>* cancelled,bool source_admitted,SourceRecorder* recorder):read_(reader),context_(context),budget_(budget),capture_(capture),epoch_(epoch),hazards_(hazards),cancelled_(cancelled),source_admitted_(source_admitted),source_recorder_(recorder){}
 uint64_t address(uint64_t base,uint64_t offset){
  if(base<0x10000||offset>UINT64_MAX-base)throw CopyFailure("MALFORMED_ADDRESS");return base+offset;
 }
 void bytes(uint64_t at,void* into,size_t size){
  if(cancelled_&&cancelled_->load())throw CopyFailure("OPERATOR_OR_GUARD_STOP");
  if(hazards_.load()||epoch_.load()!=capture_.epoch_begin)throw CopyFailure("LIFETIME_OVERLAP");
  if(size&&(!at||size>UINT64_MAX-at||!read_(context_,at,into,size)))throw CopyFailure("READ_FAILED");
 }
 template<class T>T value(uint64_t base,uint64_t offset){T result{};bytes(address(base,offset),&result,sizeof result);return result;}
 void extent(uint64_t data,uint64_t count,uint64_t stride){
  if((stride&&count>UINT64_MAX/stride)||(count&&(!data||data<0x10000||count*stride>UINT64_MAX-data)))throw CopyFailure("MALFORMED_ADDRESS");
 }
 void reserve_bytes(uint64_t count,uint64_t stride){
  if(stride&&count>(budget_-capture_.required_bytes)/stride)throw CopyFailure("MEASURED_CAPACITY_EXCEEDED");
  capture_.required_bytes+=count*stride;
 }
 static bool source_read(void* context,uint64_t at,void* into,size_t size){auto& self=*static_cast<Copier*>(context);
  if((self.cancelled_&&self.cancelled_->load())||self.hazards_.load()||self.epoch_.load()!=self.capture_.epoch_begin||!at||size>UINT64_MAX-at)return false;
  return self.read_(self.context_,at,into,size);}
 void preflight(uint64_t proc){
  // Read every native header and point range before any count-driven vector
  // allocation. A malformed large count cannot trigger a speculative arena.
  auto data=value<uint64_t>(proc,0x20),count=value<uint64_t>(proc,0x28);extent(data,count,24);
  std::array<uint8_t,4096> probe{};
  for(uint64_t i=0;i<count;++i){
   std::array<uint8_t,24> entry{};bytes(address(data,i*24),entry.data(),24);uint32_t state{};std::memcpy(&state,entry.data()+16,4);if(state==UINT32_MAX)continue;
   reserve_bytes(1,sizeof(Holder));++planned_holders_;
   uint64_t source{},holder{};std::memcpy(&source,entry.data(),8);std::memcpy(&holder,entry.data()+8,8);if(!source||holder<0x10000)continue;
   auto resources=value<uint64_t>(holder,0x20),resource_capacity=value<uint64_t>(holder,0x28);extent(resources,resource_capacity,24);
   for(uint64_t j=0;j<resource_capacity;++j){
    std::array<uint8_t,24> slot{};bytes(address(resources,j*24),slot.data(),24);std::memcpy(&state,slot.data()+16,4);if(state==UINT32_MAX)continue;
    reserve_bytes(1,sizeof(Resource));
    uint32_t form{};uint64_t collection{};std::memcpy(&form,slot.data(),4);std::memcpy(&collection,slot.data()+8,8);
    auto regions=value<uint32_t>(collection,8),region_capacity=value<uint32_t>(collection,12);auto region_data=value<uint64_t>(collection,16);
    if(regions>region_capacity)throw CopyFailure("MALFORMED_REGION_COUNT");extent(region_data,regions,48);reserve_bytes(regions,sizeof(Region));
    for(uint32_t k=0;k<regions;++k){
     std::array<uint8_t,48> region{};bytes(address(region_data,uint64_t(k)*48),region.data(),48);
     uint32_t points{},point_capacity{},header_form{};uint64_t point_data{};
     std::memcpy(&points,region.data()+24,4);std::memcpy(&point_capacity,region.data()+28,4);std::memcpy(&header_form,region.data()+16,4);std::memcpy(&point_data,region.data()+32,8);
     if(points>point_capacity||header_form!=form)throw CopyFailure("MALFORMED_POINT_COUNT_OR_FORM");extent(point_data,points,16);reserve_bytes(points,16);
     auto remaining=uint64_t(points)*16;uint64_t offset=0;
     while(remaining){auto amount=size_t((std::min)(remaining,uint64_t(probe.size())));bytes(address(point_data,offset),probe.data(),amount);offset+=amount;remaining-=amount;}
    }
   }
  }
  capture_.required_bytes=0;
 }
 void map(uint64_t proc){
  auto data=value<uint64_t>(proc,0x20),count=value<uint64_t>(proc,0x28);
  extent(data,count,24);reserve_bytes(planned_holders_,sizeof(Holder));capture_.holders.reserve(size_t(planned_holders_));
  for(uint64_t i=0;i<count;++i){
   std::array<uint8_t,24> entry{};bytes(address(data,i*24),entry.data(),entry.size());
   uint32_t state{};std::memcpy(&state,entry.data()+16,4);if(state==UINT32_MAX)continue;
   capture_.holders.emplace_back();auto& holder=capture_.holders.back();holder.map_index=i;
   std::memcpy(&holder.source,entry.data(),8);std::memcpy(&holder.holder,entry.data()+8,8);
   for(size_t n=0;n+1<capture_.holders.size();++n)if(holder.source&&capture_.holders[n].source==holder.source)throw CopyFailure("DUPLICATE_SOURCE_KEY");
   if(!holder.source||holder.holder<0x10000){holder.disposition="ALLOCATION_UNKNOWN";continue;}
   if(source_admitted_)holder.source_diagnostics=source_recorder_?source_recorder_->copy(source_read,this,holder.source):read_source_diagnostics(source_read,this,holder.source);
   auto resources=value<uint64_t>(holder.holder,0x20),resource_capacity=value<uint64_t>(holder.holder,0x28);
   extent(resources,resource_capacity,24);uint64_t occupied_resources=0;
   for(uint64_t j=0;j<resource_capacity;++j){auto resource_state=value<uint32_t>(address(resources,j*24),16);if(resource_state!=UINT32_MAX)++occupied_resources;}
   reserve_bytes(occupied_resources,sizeof(Resource));holder.resources.reserve(size_t(occupied_resources));
   for(uint64_t j=0;j<resource_capacity;++j){
    std::array<uint8_t,24> slot{};bytes(address(resources,j*24),slot.data(),slot.size());
    std::memcpy(&state,slot.data()+16,4);if(state==UINT32_MAX)continue;
    holder.resources.emplace_back();auto& resource=holder.resources.back();
    std::memcpy(&resource.form,slot.data(),4);uint64_t collection{};std::memcpy(&collection,slot.data()+8,8);
    for(size_t n=0;n+1<holder.resources.size();++n)if(holder.resources[n].form==resource.form)throw CopyFailure("DUPLICATE_RESOURCE");
    auto regions=value<uint32_t>(collection,8),region_capacity=value<uint32_t>(collection,12);
    auto region_data=value<uint64_t>(collection,16);
    if(regions>region_capacity)throw CopyFailure("MALFORMED_REGION_COUNT");
    extent(region_data,regions,48);reserve_bytes(regions,sizeof(Region));resource.regions.resize(regions);
    for(uint32_t k=0;k<regions;++k){
     std::array<uint8_t,48> native{};bytes(address(region_data,uint64_t(k)*48),native.data(),native.size());
     auto& region=resource.regions[k];std::memcpy(region.header.data(),native.data(),24);
     uint32_t points_capacity{},header_form{};uint64_t points{};
     std::memcpy(&region.count,native.data()+24,4);std::memcpy(&points_capacity,native.data()+28,4);std::memcpy(&points,native.data()+32,8);
     std::memcpy(&header_form,native.data()+16,4);
     if(region.count>points_capacity||header_form!=resource.form)throw CopyFailure("MALFORMED_POINT_COUNT_OR_FORM");
     extent(points,region.count,16);reserve_bytes(region.count,16);region.points.resize(size_t(region.count)*16);
     bytes(points,region.points.data(),region.points.size());
    }
   }
   holder.complete=true;holder.disposition=holder.resources.empty()?"EMPTY":"ALLOCATION_UNKNOWN";
  }
 }
};

inline Capture copy_resident(Read reader,void* context,uint64_t proc,uint64_t budget,
                             std::atomic<uint64_t>&epoch,std::atomic<uint64_t>&hazards,std::atomic<bool>* cancelled=nullptr,bool source_admitted=false,SourceRecorder* recorder=nullptr){
 Capture result;result.proc=proc;result.epoch_begin=epoch.load();
 if(!reader||!budget||hazards.load()){result.status="LIFETIME_UNQUALIFIED";return result;}
 try{
  Copier copy(reader,context,budget,result,epoch,hazards,cancelled,source_admitted,recorder);result.lock_state=copy.value<uint32_t>(proc,0x44);
  if((result.lock_state&0xffc00000)||!(result.lock_state&0xfff))throw CopyFailure("NOT_FOREIGN_READER_CONTEXT");
  copy.preflight(proc);copy.map(proc);result.epoch_end=epoch.load();
  if(hazards.load()||result.epoch_begin!=result.epoch_end)throw CopyFailure("LIFETIME_OVERLAP");
  result.status="COPIED_UNQUALIFIED";
 }catch(const CopyFailure& failure){result.status=failure.what();}
 catch(const std::bad_alloc&){result.status="ALLOCATION_FAILED";}
 catch(const std::exception&){result.status="COPY_EXCEPTION";}
 result.epoch_end=epoch.load();
 return result;
}
}
