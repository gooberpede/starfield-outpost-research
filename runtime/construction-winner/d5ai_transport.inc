// SPDX-License-Identifier: GPL-3.0-or-later
// Included after the unchanged transport implementation in the derived candidate.
extern "C" {
 uint64_t d5ai_acquire_original{};
 void d5ai_area_capture(uint64_t proc,uint64_t query,uint64_t consumer,uint32_t radius,uint32_t upper) noexcept {
  winner::geometry::snapshot(proc,query,consumer,radius,upper);
 }
 void d5ai_complete_capture(uint64_t iterator,uint64_t capacity,uint64_t result) noexcept {winner::geometry::complete(iterator,capacity,result);}
 void d5ai_preunlock_capture(uint64_t result) noexcept {winner::geometry::preunlock(result);}
}
namespace winner::geometry {
std::string metrics(){
 return ",\"geometry_offers\":"+std::to_string(offers.load())+
  ",\"geometry_captured\":"+std::to_string(captured.load())+",\"geometry_completed\":"+std::to_string(completed.load())+
  ",\"geometry_no_slot\":"+std::to_string(no_slot.load())+",\"geometry_arena_full\":"+std::to_string(overflow.load())+
  ",\"geometry_read_failures\":"+std::to_string(read_failures.load())+",\"geometry_failed\":"+(failed?"true":"false")+
  ",\"geometry_busy_skips\":"+std::to_string(busy_skips.load())+
  ",\"geometry_armed\":"+std::to_string(armed.load())+",\"geometry_slot_bytes\":"+std::to_string(sizeof(Slot))+
  ",\"geometry_slot_count\":"+std::to_string(slot_count);
}
bool drain_sidecar(){
 if(held.load())return true;
 for(auto& slot:slots){unsigned expected=Queued;if(!slot.state.compare_exchange_strong(expected,Writing,std::memory_order_acquire))continue;
  auto& h=slot.header;bool ok=disk(h.payload_bytes+sizeof h+65536);
  auto worker_begin=clock_ticks();
  auto stem=L"geometry-"+std::to_wstring(h.snapshot);auto path=session/(stem+L".bin");
  HANDLE file=INVALID_HANDLE_VALUE;
  if(ok)file=CreateFileW(path.c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  ok=ok&&file!=INVALID_HANDLE_VALUE;
  if(ok)ok=append(file,&h,sizeof h)&&append(file,slot.payload,DWORD(h.payload_bytes))&&flush(file,false);
  if(file!=INVALID_HANDLE_VALUE)CloseHandle(file);
  if(ok){
   auto digest=sor::sha_file(path);
   auto receipt="{\"schema\":\"sor-d5ai-raw/2\",\"identity_sha256\":"+sor::quote(identity_hash)+
    ",\"snapshot_id\":"+std::to_string(h.snapshot)+",\"request_id\":"+std::to_string(h.request)+
    ",\"sha256\":"+sor::quote(digest)+",\"bytes\":"+std::to_string(sizeof h+h.payload_bytes)+
    ",\"capture_status\":"+std::to_string(h.status)+",\"native_quality\":\"UNKNOWN\",\"worker_begin_ticks\":"+std::to_string(worker_begin)+
    ",\"worker_flushed_ticks\":"+std::to_string(clock_ticks())+",\"flushed\":true}\n";
   ok=!fixture_receipt_fault.load()&&digest.size()==64&&publish(session/(stem+L".json"),receipt)&&publish(session/(L"geometry-request-"+std::to_wstring(h.request)+L".json"),receipt);
  }
  if(!ok){failed=true;broken=true;slot.state.store(Queued,std::memory_order_release);return false;}
  ++completed;slot.state.store(Free,std::memory_order_release);
 }
 return !failed.load();
}
bool poll_request(){
 // The existing exclusive session controller publishes the identity-bound arm
 // command. Decimal requests increase monotonically; partial/stale files fail.
 auto path=session/L"geometry-arm.txt";std::error_code ec;
 if(!fs::exists(path,ec))return !ec;
 HANDLE file=CreateFileW(path.c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr);
 if(file==INVALID_HANDLE_VALUE)return false;
 LARGE_INTEGER length{};char data[128]{};DWORD count{};
 bool ok=GetFileSizeEx(file,&length)&&length.QuadPart>65&&length.QuadPart<128&&ReadFile(file,data,DWORD(length.QuadPart),&count,nullptr)&&count==length.QuadPart;
 CloseHandle(file);if(!ok)return false;
 std::string text(data,count);auto split=text.find('\n');if(split!=64||text.substr(0,64)!=identity_hash)return false;
 U request=0;if(split+1==text.size())return false;
 for(size_t i=split+1;i<text.size();++i){char c=text[i];if(c<'0'||c>'9'||request>(UINT64_MAX-U(c-'0'))/10)return false;request=request*10+U(c-'0');}
 if(!request)return false;if(request==last_request.load())return true;
 return arm(request);
}
}
