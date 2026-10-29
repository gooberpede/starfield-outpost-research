// SPDX-License-Identifier: GPL-3.0-or-later
#include "observer.h"
#include "patch.h"
#include "../exp0002/win_support.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
#include <string>
#include <filesystem>
extern "C" {uint64_t visited_fall{},visited_taken{};void visited_bridge();
 void visited_capture(uint64_t w,uint64_t proc,uint64_t rsi) noexcept {retained::capture_visited(w,proc,rsi);}}
namespace retained {
namespace fs=std::filesystem;
inline Patch edits[11];inline unsigned char* relays{};inline fs::path session;
inline HANDLE raw=INVALID_HANDLE_VALUE,ack=INVALID_HANDLE_VALUE;
inline std::atomic<U> written{},flushed{},acknowledged{},bytes{};
inline U output_faults{},write_calls{},flush_calls{},max_write_ticks{},max_flush_ticks{};
inline const char* output_fault="none";
// Disposable fixture fault injection, set only by the host-checked entry.
inline unsigned fixture_fault{};
inline std::string identity,identity_hash;
std::string metrics(){LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);return ",\"enqueued_snapshot\":"+std::to_string(enqueue.load())+",\"dequeued_snapshot\":"+std::to_string(dequeue.load())+",\"acknowledged\":"+std::to_string(acknowledged.load())+",\"output_faults\":"+std::to_string(output_faults)+",\"write_calls\":"+std::to_string(write_calls)+",\"flush_calls\":"+std::to_string(flush_calls)+",\"max_write_ticks\":"+std::to_string(max_write_ticks)+",\"max_flush_ticks\":"+std::to_string(max_flush_ticks)+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"drops\":"+std::to_string(drops.load())+",\"queue_full\":"+std::to_string(full_losses.load())+",\"contention_exhausted\":"+std::to_string(contention_losses.load())+",\"producer_retries\":"+std::to_string(retries.load())+",\"queue_high_water_lower_bound\":"+std::to_string(high_water.load())+",\"first_loss_sampled_admission\":"+std::to_string(first_loss.load())+",\"last_loss_sampled_admission\":"+std::to_string(last_loss.load())+",\"loss_generation\":"+std::to_string(loss_generation.load())+",\"counter_overflow\":"+(counter_overflow?"true":"false")+",\"output_fault\":"+sor::quote(output_fault);}

bool disk(U reserve=65536){ULARGE_INTEGER free{};for(auto p:{L"C:/",L"D:/"})if(fixture_fault==1||reserve>UINT64_MAX-40000000000ULL||!GetDiskFreeSpaceExW(p,&free,nullptr,nullptr)||free.QuadPart<40000000000ULL+reserve){output_fault="disk_guard";++output_faults;return false;}return true;}
inline uint32_t rolling_crc{};
uint32_t crc(const void* data,size_t size,uint32_t seed=0){uint32_t v=~seed;auto* p=(const unsigned char*)data;
 for(size_t i=0;i<size;++i){v^=p[i];for(int j=0;j<8;++j)v=(v>>1)^(0xedb88320U&uint32_t(-int(v&1)));}return ~v;
}
bool append(HANDLE h,const void* p,DWORD n){DWORD got{};LARGE_INTEGER begin{},end{};QueryPerformanceCounter(&begin);
 bool ok=fixture_fault!=2&&!(fixture_fault==5&&h==ack)&&WriteFile(h,p,n,&got,nullptr)&&got==n;QueryPerformanceCounter(&end);++write_calls;max_write_ticks=std::max(max_write_ticks,U(end.QuadPart-begin.QuadPart));
 if(!ok){output_fault=h==ack?"ack_write":"write";++output_faults;}return ok;}
bool flush(HANDLE h,bool receipt){LARGE_INTEGER begin{},end{};QueryPerformanceCounter(&begin);
 bool ok=fixture_fault!=(receipt?4u:3u)&&FlushFileBuffers(h);QueryPerformanceCounter(&end);++flush_calls;max_flush_ticks=std::max(max_flush_ticks,U(end.QuadPart-begin.QuadPart));
 if(!ok){output_fault=receipt?"ack_flush":"raw_flush";++output_faults;}return ok;}

bool drain(){Event e{};bool changed=false;U limit=enqueue.load();
 if(!disk((limit-dequeue.load())*(sizeof(Event)+16)+65536))return false;
 // Snapshot batch: continuous producers cannot starve flush, health or STOP.
 unsigned char batch[64*(sizeof(Event)+16)]{};
 while(dequeue.load()<limit){
  size_t used=0;U records=0;
  while(records<64&&dequeue.load()<limit&&pop(e)){
   uint32_t header[4]{0x31505253,sizeof e,uint32_t(e.sequence),crc(&e,sizeof e)};
   memcpy(batch+used,header,sizeof header);used+=sizeof header;memcpy(batch+used,&e,sizeof e);used+=sizeof e;++records;
  }
  if(!records)break;
  if(!append(raw,batch,DWORD(used)))return false;
  rolling_crc=crc(batch,used,rolling_crc);written+=records;bytes+=used;changed=true;
 }
 if(changed){if(!flush(raw,false))return false;flushed=written.load();
  auto line="{\"records\":"+std::to_string(flushed)+",\"bytes\":"+std::to_string(bytes)+",\"identity_sha256\":"+sor::quote(identity_hash)+",\"prefix_crc32\":"+std::to_string(rolling_crc)+metrics()+"}\n";
  if(!append(ack,line.data(),DWORD(line.size())))return false;
  if(!flush(ack,true))return false;acknowledged=flushed.load();
 }return true;
}
bool guards(){for(auto& p:edits)if(!match(p,true)){output_fault="hook_guard";return false;}return true;}
DWORD worker_body(){
 std::string last_nonce;
 bool ok=drain()&&guards()&&disk();
 if(ok&&enabled&&!broken)ok=sor::write_new(session/L"ready.json",identity+",\"hooks\":11,\"coverage\":\"scoped-native\",\"ready\":true}\n");
 else ok=false;
 while(ok&&enabled){
  ok=disk()&&guards()&&drain();
  std::error_code error;if(fs::exists(session/L"STOP",error))enabled=false;if(error)ok=false;
  std::error_code request_error;
  if(ok&&enabled&&fs::exists(session/L"request.txt",request_error)){
   std::string nonce;if(!sor::read_small(session/L"request.txt",nonce,32)||nonce.size()!=32)ok=false;
   else if(nonce!=last_nonce){bool valid=true;for(char c:nonce)valid&=(c>='0'&&c<='9')||(c>='a'&&c<='f');
    if(!valid||!drain()||!enabled||broken||!guards()||!disk()||fs::exists(session/L"STOP")||!sor::write_new(session/("ack-"+nonce+".json"),identity+",\"nonce\":"+sor::quote(nonce)+",\"flushed\":"+std::to_string(flushed)+",\"hooks_intact\":true,\"capture_active\":true"+metrics()+"}\n"))ok=false;
    last_nonce=nonce;
   }
  }
  if(request_error)ok=false;
  Sleep(20);
 }
 enabled=false;if(!ok)broken=true;
 while(active.load())Sleep(10);
 if(!drain())broken=true;
 auto terminal=identity+",\"written\":"+std::to_string(written)+",\"flushed\":"+std::to_string(flushed)+",\"enqueued\":"+std::to_string(enqueue.load())+metrics()+",\"failed\":"+(broken?"true":"false")+",\"resident_inert\":true}\n";
 sor::write_new(session/L"terminal.json",terminal);CloseHandle(raw);CloseHandle(ack);return 0;
}
DWORD WINAPI worker(void*){
 try{return worker_body();}catch(...){enabled=false;broken=true;
  // Best-effort exception closeout can itself fail, including allocation failure.
  // Missing closeout leaves an incomplete prefix, never a success receipt.
  try{sor::write_new(session/L"worker-exception.json","{\"failed\":true}\n");}catch(...){}
  return 1;
 }
}
bool configure(U module){
 base=module;relays=near_page(module+sites[0].rva);if(!relays)return false;
 void* hooks[]{(void*)&lookup_hook,(void*)&query_hook,(void*)&generate_hook,(void*)&mask_hook,(void*)&copy_hook,(void*)&visited_bridge,
  (void*)&fence_hook<0>,(void*)&fence_hook<1>,(void*)&fence_hook<2>,(void*)&fence_hook<3>,(void*)&fence_hook<4>};
 for(unsigned i=0;i<11;++i){auto& s=sites[i];auto& p=edits[i];p.at=(unsigned char*)(module+s.rva);p.n=s.length;
  unsigned char window[32]{};if(!read(U(p.at),window,sizeof window)||sor::sha_bytes(window,sizeof window)!=s.hash)return false;
  memcpy(p.before,window,p.n);auto* island=relays+i*64;jump(island,U(hooks[i]));
  if(!relative(p,U(island),i<5?0xe8:0xe9))return false;
  U target=module+s.target;
  if(i>=6){auto* trampoline=island+16;memcpy(trampoline,p.before,p.n);jump(trampoline+p.n,U(p.at)+p.n);target=U(trampoline);fences[i-6]=(Four)target;}
  if(i==0)lookup_original=(Four)target;if(i==1)query_original=(Four)target;if(i==2)generate_original=(Generate)target;
  if(i==3)mask_original=(Four)target;if(i==4)copy_original=(Four)target;
 }
 for(auto& g:target_guards){unsigned char b[32]{};if(!read(module+g.rva,b,32)||sor::sha_bytes(b,32)!=g.hash)return false;}
 visited_fall=module+0x79fcac;visited_taken=module+0x79ffaa;
 DWORD old{};return VirtualProtect(relays,4096,PAGE_EXECUTE_READ,&old)&&FlushInstructionCache(GetCurrentProcess(),relays,4096);
}
}
extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={SFSEPluginVersionData::kVersion,0x00020000,"SOR Retained Population","Starfield Outpost Systems Research",0,0,{retained::game_version,0},0,0,0};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* api){
 using namespace retained;
 bool dirty=false;
 try{
  if(!api||api->interfaceVersion!=1||api->runtimeVersion!=game_version||!disk())return false;
  auto image=GetModuleHandleW(nullptr);wchar_t path[32768]{};if(!GetModuleFileNameW(image,path,32768)||sor::sha_file(path)!=game_hash)return false;
  auto sfse=GetModuleHandleW(L"sfse_1_16_244.dll");if(!sfse||!GetModuleFileNameW(sfse,path,32768)||sor::sha_file(path)!=sfse_hash)return false;
  HMODULE self{};if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,(LPCWSTR)&SFSEPlugin_Load,&self)||!GetModuleFileNameW(self,path,32768))return false;
  std::string self_hash=sor::sha_file(path);
  fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/d5p/live";
  for(auto p=root;!p.empty();){auto a=GetFileAttributesW(p.c_str());if(a!=INVALID_FILE_ATTRIBUTES&&(a&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto next=p.parent_path();if(next==p)break;p=next;}
  fs::create_directories(root);session=root/("session-"+std::to_string(GetCurrentProcessId())+"-"+std::to_string(GetTickCount64()));
  if(!fs::create_directory(session))return false;
  FILETIME created{},exited{},kernel{},user{};if(!GetProcessTimes(GetCurrentProcess(),&created,&exited,&kernel,&user))return false;
  identity="{\"schema\":\"sor-d5p/2\",\"session_name\":"+sor::quote(session.filename().string())+",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"creation_filetime\":"+std::to_string((U(created.dwHighDateTime)<<32)|created.dwLowDateTime)+",\"dll_sha256\":"+sor::quote(self_hash)+",\"game_sha256\":"+sor::quote(game_hash)+",\"sfse_sha256\":"+sor::quote(sfse_hash);
  auto identity_bytes=identity+"}\n";identity_hash=sor::sha_bytes(identity_bytes.data(),identity_bytes.size());
  if(!sor::write_new(session/L"identity.json",identity+"}\n"))return false;
  if(!sole_thread()&&!sor::write_new(session/L"waiting-sole-thread.json",identity+",\"waiting\":true}\n"))return false;
  // Existing observer admission pattern: loader workers may still be retiring.
  // Never patch a peer thread or impose an arbitrary live startup deadline.
  while(!sole_thread()){
   if(!disk()||fs::exists(session/L"STOP")){sor::write_new(session/L"not-ready.json",identity+",\"error\":\"startup_guard_or_STOP\"}\n");return false;}
   Sleep(100);
  }
  if(!configure(U(image)))return false;
  // Group durability is enforced by drain's raw FlushFileBuffers, followed by
  // the separately flushed ACK. Individual header/payload writes are buffered.
  raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  ack=CreateFileW((session/L"flush.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  if(raw==INVALID_HANDLE_VALUE||ack==INVALID_HANDLE_VALUE)return false;
  initialize_queue();enabled=true;
  if(!install(edits,11,dirty)){enabled=false;return dirty;}
  Event e{};e.kind=Ready;e.epoch=epoch;emit(e);
  HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);
  if(!thread){enabled=false;broken=true;sor::write_new(session/L"not-ready.json",identity+",\"error\":\"worker_create\"}\n");return true;}
  CloseHandle(thread);return true;
 }catch(...){enabled=false;broken=true;return dirty;}
}
