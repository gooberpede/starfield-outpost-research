// SPDX-License-Identifier: GPL-3.0-or-later
#include "observer.h"
#include "patch.h"
#include "../exp0002/win_support.h"
#include <string>
#include <filesystem>
extern "C" {uint64_t visited_fall{},visited_taken{},selected_fall{},birth_fall{},published_fall{},stored_fall{};void visited_bridge();void selected_bridge();
 void visited_capture(uint64_t w,uint64_t proc,uint64_t rsi,uint64_t consumed) noexcept {winner::visited_capture(w,proc,rsi,consumed);}
 void selected_capture(uint64_t w,uint64_t proc,uint64_t source) noexcept {winner::selected_capture(w,proc,source);}}
extern "C" {
 void birth_capture(uint64_t source,uint64_t grid,uint64_t consumed) noexcept {winner::birth_capture(source,grid,consumed);}
 void published_capture(uint64_t source,uint64_t grid,uint64_t destination,uint64_t index) noexcept {winner::published_capture(source,grid,destination,index);}
 void stored_capture(uint64_t frame,uint64_t proc,uint64_t destination,uint64_t consumed) noexcept {winner::stored_capture(frame,proc,destination,consumed);}
}
namespace winner {
namespace fs=std::filesystem;
inline Patch edits[18];inline unsigned char* relays{};inline fs::path session;
inline unsigned char* relay_page{};inline std::string relay_sha256;
inline U guarded_targets[7]{};inline std::string guarded_hashes[7];
inline HANDLE raw=INVALID_HANDLE_VALUE,ack=INVALID_HANDLE_VALUE;
inline std::atomic<U> written{},flushed{},acknowledged{},bytes{};
inline U output_faults{},write_calls{},flush_calls{},max_write_ticks{},max_flush_ticks{};
inline const char* output_fault="none";
// Disposable fixture fault injection, set only by the host-checked entry.
inline std::atomic<unsigned> fixture_fault{};
inline std::atomic<bool> fixture_pause{};
inline std::string identity,identity_hash;
enum Phase {Wake,Drain,Write,RawFlush,AckFlush,Guard,Disk,Shutdown,PhaseCount};
// Single worker owns these fixed counters. They never enter the event queue.
struct Timing {U count{},total{},maximum{};};
inline Timing timing[PhaseCount]{};
inline U blocked_head{},drain_high_water{},last_wake{},worker_tid{},worker_created{};
inline std::atomic<unsigned> fixture_flush_pause_ms{};
inline U clock_ticks(){LARGE_INTEGER t{};QueryPerformanceCounter(&t);return U(t.QuadPart);}
struct Measure {unsigned phase;U begin=clock_ticks();~Measure(){auto elapsed=clock_ticks()-begin;auto& t=timing[phase];++t.count;t.total+=elapsed;t.maximum=std::max(t.maximum,elapsed);}};
std::string diagnostic_metrics(){
 std::string result=",\"worker_thread_id\":"+std::to_string(worker_tid)+",\"worker_creation_filetime\":"+std::to_string(worker_created)+",\"worker_timing_ticks\":[";
 for(unsigned i=0;i<PhaseCount;++i){if(i)result+=",";auto& t=timing[i];result+="{\"count\":"+std::to_string(t.count)+",\"total\":"+std::to_string(t.total)+",\"max\":"+std::to_string(t.maximum)+"}";}
 return result+"],\"blocked_unpublished_head\":"+std::to_string(blocked_head)+",\"drain_snapshot_high_water\":"+std::to_string(drain_high_water)+",\"cell_bytes\":"+std::to_string(sizeof(Cell))+",\"capacity\":"+std::to_string(capacity);
}
std::string metrics(){LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);return ",\"loss_bounds_uncertain\":"+std::string(loss_bounds_uncertain?"true":"false")+diagnostic_metrics()+",\"enqueued_snapshot\":"+std::to_string(enqueue.load())+",\"dequeued_snapshot\":"+std::to_string(dequeue.load())+",\"acknowledged\":"+std::to_string(acknowledged.load())+",\"output_faults\":"+std::to_string(output_faults)+",\"write_calls\":"+std::to_string(write_calls)+",\"flush_calls\":"+std::to_string(flush_calls)+",\"max_write_ticks\":"+std::to_string(max_write_ticks)+",\"max_flush_ticks\":"+std::to_string(max_flush_ticks)+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"drops\":"+std::to_string(drops.load())+",\"queue_full\":"+std::to_string(full_losses.load())+",\"contention_exhausted\":"+std::to_string(contention_losses.load())+",\"reentrant_losses\":"+std::to_string(reentrant_losses.load())+",\"producer_retries\":"+std::to_string(retries.load())+",\"queue_high_water_lower_bound\":"+std::to_string(high_water.load())+",\"first_loss_sampled_admission\":"+std::to_string(first_loss.load())+",\"last_loss_sampled_admission\":"+std::to_string(last_loss.load())+",\"loss_generation\":"+std::to_string(loss_generation.load())+",\"counter_overflow\":"+(counter_overflow?"true":"false")+",\"output_fault\":"+sor::quote(output_fault);}

bool disk(U reserve=65536){Measure measure{Disk};ULARGE_INTEGER free{};for(auto p:{L"C:/",L"D:/"})if(fixture_fault==1||reserve>UINT64_MAX-40000000000ULL||!GetDiskFreeSpaceExW(p,&free,nullptr,nullptr)||free.QuadPart<40000000000ULL+reserve){output_fault="disk_guard";++output_faults;return false;}return true;}
inline uint32_t rolling_crc{};
uint32_t crc(const void* data,size_t size,uint32_t seed=0){uint32_t v=~seed;auto* p=(const unsigned char*)data;
 for(size_t i=0;i<size;++i){v^=p[i];for(int j=0;j<8;++j)v=(v>>1)^(0xedb88320U&uint32_t(-int(v&1)));}return ~v;
}
bool append(HANDLE h,const void* p,DWORD n){Measure measure{Write};DWORD got{};LARGE_INTEGER begin{},end{};QueryPerformanceCounter(&begin);
 bool ok=fixture_fault!=2&&!(fixture_fault==5&&h==ack)&&WriteFile(h,p,n,&got,nullptr)&&got==n;QueryPerformanceCounter(&end);++write_calls;max_write_ticks=std::max(max_write_ticks,U(end.QuadPart-begin.QuadPart));
 if(!ok){output_fault=h==ack?"ack_write":"write";++output_faults;}return ok;}
bool flush(HANDLE h,bool receipt){Measure measure{receipt?AckFlush:RawFlush};
 if(!receipt){auto pause=fixture_flush_pause_ms.exchange(0);if(pause)Sleep(pause);}LARGE_INTEGER begin{},end{};QueryPerformanceCounter(&begin);
 bool ok=fixture_fault!=(receipt?4u:3u)&&FlushFileBuffers(h);QueryPerformanceCounter(&end);++flush_calls;max_flush_ticks=std::max(max_flush_ticks,U(end.QuadPart-begin.QuadPart));
 if(!ok){output_fault=receipt?"ack_flush":"raw_flush";++output_faults;}return ok;}

bool drain(){Measure measure{Drain};Event e{};bool changed=false;U limit=enqueue.load();drain_high_water=std::max(drain_high_water,limit-dequeue.load());
 if(!disk((limit-dequeue.load())*(sizeof(Event)+16)+65536))return false;
 // Snapshot batch: continuous producers cannot starve flush, health or STOP.
 unsigned char batch[64*(sizeof(Event)+16)]{};
 while(dequeue.load()<limit){
  size_t used=0;U records=0;
  while(records<64&&dequeue.load()<limit&&pop(e)){
   uint32_t header[4]{0x31505253,sizeof e,uint32_t(e.sequence),crc(&e,sizeof e)};
   memcpy(batch+used,header,sizeof header);used+=sizeof header;memcpy(batch+used,&e,sizeof e);used+=sizeof e;++records;
  }
  if(!records){++blocked_head;break;}
  if(!append(raw,batch,DWORD(used)))return false;
  rolling_crc=crc(batch,used,rolling_crc);written+=records;bytes+=used;changed=true;
 }
 if(changed){if(!flush(raw,false))return false;flushed=written.load();
  auto line="{\"records\":"+std::to_string(flushed)+",\"bytes\":"+std::to_string(bytes)+",\"identity_sha256\":"+sor::quote(identity_hash)+",\"prefix_crc32\":"+std::to_string(rolling_crc)+metrics()+"}\n";
  if(!append(ack,line.data(),DWORD(line.size())))return false;
  if(!flush(ack,true))return false;acknowledged=flushed.load();
 }return true;
}
bool guards(){Measure measure{Guard};if(fixture_fault==7){output_fault="fixture_guard";return false;}for(auto& p:edits)if(!match(p,true)){output_fault="hook_guard";return false;}
 if(!relay_page||sor::sha_bytes(relay_page,4096)!=relay_sha256){output_fault="relay_guard";return false;}
 for(unsigned i=0;i<7;++i){unsigned char bytes[32]{};if(!read(guarded_targets[i],bytes,32)||sor::sha_bytes(bytes,32)!=guarded_hashes[i]){output_fault="target_guard";return false;}}
 return true;}
bool publish(const fs::path& path,const std::string& payload){auto pending=path;pending+=L".pending";
 return sor::write_new(pending,payload)&&MoveFileExW(pending.c_str(),path.c_str(),MOVEFILE_WRITE_THROUGH);}
bool read_request(std::string& nonce){
 HANDLE file=CreateFileW((session/L"request.txt").c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr);
 if(file==INVALID_HANDLE_VALUE)return false;LARGE_INTEGER length{};char bytes[32]{};DWORD count{};
 bool ok=GetFileSizeEx(file,&length)&&length.QuadPart==32&&ReadFile(file,bytes,32,&count,nullptr)&&count==32;
 CloseHandle(file);if(ok)nonce.assign(bytes,32);return ok;
}
DWORD worker_body(){
 std::string last_nonce;
 bool ok=drain()&&guards()&&disk();
 if(ok&&enabled&&!broken)ok=publish(session/L"ready.json",identity+",\"hooks\":18,\"coverage\":\"scoped-native\",\"ready\":true,\"worker_thread_id\":"+std::to_string(worker_tid)+",\"worker_creation_filetime\":"+std::to_string(worker_created)+"}\n");
 else ok=false;
 while(ok&&enabled){
  U now=clock_ticks();if(last_wake){auto elapsed=now-last_wake;auto& t=timing[Wake];++t.count;t.total+=elapsed;t.maximum=std::max(t.maximum,elapsed);}last_wake=now;
  ok=disk()&&guards()&&(fixture_pause.load()||drain());
  // Disposable worker-exit control: no terminal receipt can be inferred from it.
  if(fixture_fault==6){enabled=false;broken=true;return 90;}
  std::error_code error;if(fs::exists(session/L"STOP",error))enabled=false;if(error)ok=false;
  std::error_code request_error;
  if(ok&&enabled&&fs::exists(session/L"request.txt",request_error)){
   std::string nonce;if(!read_request(nonce)){output_fault="request_read_or_size";ok=false;}
   else if(nonce!=last_nonce){bool valid=true;for(char c:nonce)valid&=(c>='0'&&c<='9')||(c>='a'&&c<='f');
    if(!valid||!drain()||!enabled||broken||!guards()||!disk()||fs::exists(session/L"STOP"))ok=false;
    else if(!publish(session/("ack-"+nonce+".json"),identity+",\"request_nonce\":"+sor::quote(nonce)+",\"flushed\":"+std::to_string(flushed)+",\"hooks_intact\":true,\"capture_active\":true"+metrics()+"}\n")){output_fault="challenge_publish";++output_faults;ok=false;}
    last_nonce=nonce;
   }
  }
  if(request_error)ok=false;
  Sleep(20);
 }
 enabled=false;if(!ok)broken=true;
 {Measure shutdown{Shutdown};while(active.load())Sleep(10);
 if(!drain())broken=true;}
 auto terminal=identity+",\"written\":"+std::to_string(written)+",\"flushed\":"+std::to_string(flushed)+",\"enqueued\":"+std::to_string(enqueue.load())+metrics()+",\"failed\":"+(broken?"true":"false")+",\"resident_inert\":true}\n";
 if(fixture_fault!=8)sor::write_new(session/L"terminal.json",terminal);CloseHandle(raw);CloseHandle(ack);return 0;
}
DWORD WINAPI worker(void*){
 FILETIME created{},exited{},kernel{},user{};worker_tid=GetCurrentThreadId();
 if(!GetThreadTimes(GetCurrentThread(),&created,&exited,&kernel,&user)){enabled=false;broken=true;return 1;}
 worker_created=(U(created.dwHighDateTime)<<32)|created.dwLowDateTime;
 try{return worker_body();}catch(...){enabled=false;broken=true;
  // Best-effort exception closeout can itself fail, including allocation failure.
  // Missing closeout leaves an incomplete prefix, never a success receipt.
  try{sor::write_new(session/L"worker-exception.json","{\"failed\":true}\n");}catch(...){}
  return 1;
 }
}
}
