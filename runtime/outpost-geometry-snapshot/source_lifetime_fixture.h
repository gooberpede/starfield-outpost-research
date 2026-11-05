// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "source_lifetime.h"
#include <array>
#include <thread>
#include <stdexcept>
#include <cstring>
namespace d5ar::fixture {
struct SourceInput {
 std::array<unsigned char,0x70> bytes{};
 unsigned calls{},fail_at{};bool throws{},seh{};SourceRecorder* reenter{};
 HANDLE entered{},resume{};
 static bool read(void* raw,uint64_t at,void* into,size_t size){
  auto& x=*static_cast<SourceInput*>(raw);++x.calls;
  if(x.reenter){auto recorder=x.reenter;x.reenter=nullptr;recorder->mark(reinterpret_cast<uint64_t>(x.bytes.data()));}
  if(x.entered&&x.calls==1){SetEvent(x.entered);if(WaitForSingleObject(x.resume,10000)!=WAIT_OBJECT_0)return false;}
  if(x.seh)RaiseException(0xe0424445,0,0,nullptr);
  if(x.throws)throw std::runtime_error("Owned RPM exception");
  if(x.fail_at==x.calls)return false;
  auto base=reinterpret_cast<uint64_t>(x.bytes.data());if(at<base||size>x.bytes.size()||at-base>x.bytes.size()-size)return false;
  std::memcpy(into,x.bytes.data()+at-base,size);return true;
 }
 uint64_t ptr(){return reinterpret_cast<uint64_t>(bytes.data());}
 SourceDiagnostics copy(SourceRecorder& r){return r.copy(read,this,ptr());}
};
inline bool source_seh_probe(SourceRecorder* r,SourceInput* input){
 __try {input->copy(*r);}
 __except(GetExceptionCode()==0xe0424445?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}return false;
}
inline unsigned source_lifetime_controls(){
 unsigned checks=0;auto require=[&](bool ok){if(!ok)throw std::runtime_error("Source-ending control failed");++checks;};
 auto refused=[](const SourceDiagnostics& x,const char* status){return !x.complete&&!x.origin_complete&&!x.descriptor_complete&&std::strcmp(x.status,status)==0&&std::strcmp(x.origin_status,status)==0&&std::strcmp(x.descriptor_status,status)==0;};
 {SourceRecorder r;SourceInput x;require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);}
 {SourceRecorder r;r.begin(false);SourceInput x;require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x;r.mark(x.ptr());require(refused(x.copy(r),"SOURCE_LIFETIME_RETIRED")&&!x.calls);r.mark(x.ptr());x.bytes.fill(42);require(refused(x.copy(r),"SOURCE_LIFETIME_RETIRED")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x,y;r.mark(y.ptr());auto value=x.copy(r);require(value.complete&&value.origin_complete&&value.descriptor_complete&&x.calls==14);require(refused(y.copy(r),"SOURCE_LIFETIME_RETIRED")&&!y.calls);r.mark(x.ptr());require(value.complete&&value.semantic[0]==0);}
 {SourceRecorder r;r.begin(true);SourceInput x;x.fail_at=2;auto v=x.copy(r);require(!v.complete&&v.origin_complete&&v.descriptor_complete);x.fail_at=0;require(x.copy(r).complete);}
 {SourceRecorder r;r.begin(true);SourceInput x;x.throws=true;auto v=x.copy(r);require(!v.complete&&!v.origin_complete&&!v.descriptor_complete);x.throws=false;require(x.copy(r).complete);}
 {SourceRecorder r;r.begin(true);SourceInput x;r.mark(x.ptr(),true);require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);r.mark(x.ptr());require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x;r.mark(0);require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x;x.seh=true;require(source_seh_probe(&r,&x));x.seh=false;x.calls=0;require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);r.mark(x.ptr());require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x;x.reenter=&r;require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&x.calls==1);}
 {SourceRecorder r;r.begin(true);r.begin(true);SourceInput x;require(refused(x.copy(r),"SOURCE_RECORDER_UNAVAILABLE")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x;std::thread a([&]{r.mark(x.ptr());}),b([&]{r.mark(x.ptr());});a.join();b.join();require(refused(x.copy(r),"SOURCE_LIFETIME_RETIRED")&&!x.calls);}
 {SourceRecorder r;r.begin(true);SourceInput x;x.entered=CreateEventW(nullptr,TRUE,FALSE,nullptr);x.resume=CreateEventW(nullptr,TRUE,FALSE,nullptr);if(!x.entered||!x.resume)throw std::runtime_error("Owned event allocation failed");
  SourceDiagnostics value;std::atomic<bool> attempting{},forwarded{};
  std::thread reader([&]{value=x.copy(r);});bool entered=WaitForSingleObject(x.entered,10000)==WAIT_OBJECT_0;
  std::thread ending([&]{attempting=true;r.mark(x.ptr());forwarded=true;});while(!attempting)SwitchToThread();Sleep(20);bool blocked=!forwarded;
  SetEvent(x.resume);reader.join();ending.join();CloseHandle(x.entered);CloseHandle(x.resume);x.entered=nullptr;
  require(entered&&blocked&&forwarded&&value.complete&&value.origin_complete&&value.descriptor_complete&&x.calls==14);
  x.calls=0;require(refused(x.copy(r),"SOURCE_LIFETIME_RETIRED")&&!x.calls);
 }
 return checks;
}
}
