// SPDX-License-Identifier: GPL-3.0-or-later
// SFSE startup adapted from the owned D5P observer; approved pinned header only.
#include "transport.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={SFSEPluginVersionData::kVersion,0x00040000,"SOR Construction Winner","Starfield Outpost Systems Research",0,0,{winner::game_version,0},0,0,0};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* api){
 using namespace winner;namespace fs=std::filesystem;bool dirty=false;
 try {
  if(!api||api->interfaceVersion!=1||api->runtimeVersion!=game_version||!disk(65536))return false;
  auto image=GetModuleHandleW(nullptr);wchar_t image_path[32768]{};
  if(!GetModuleFileNameW(image,image_path,32768)||fs::path(image_path).filename()!=L"Starfield.exe"||sor::sha_file(image_path)!=game_hash)return false;
  auto game=fs::path(image_path).parent_path();
  if(sor::sha_file(game/L"Data/Starfield.esm")!=esm_hash||sor::sha_file(game/L"Data/Starfield - PlanetData.ba2")!=planet_hash)return false;
  auto sfse=GetModuleHandleW(L"sfse_1_16_244.dll");wchar_t path[32768]{};
  if(!sfse||!GetModuleFileNameW(sfse,path,32768)||sor::sha_file(path)!=sfse_hash)return false;
  HMODULE self{};
  if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,(LPCWSTR)&SFSEPlugin_Load,&self)||!GetModuleFileNameW(self,path,32768))return false;
  auto self_hash=sor::sha_file(path);if(self_hash.size()!=64)return false;
  fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/d5x/live";
  for(auto p=root;!p.empty();){auto attributes=GetFileAttributesW(p.c_str());if(attributes!=INVALID_FILE_ATTRIBUTES&&(attributes&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto parent=p.parent_path();if(parent==p)break;p=parent;}
  fs::create_directories(root);unsigned char nonce[16]{};
  if(BCryptGenRandom(nullptr,nonce,16,BCRYPT_USE_SYSTEM_PREFERRED_RNG)<0)return false;
  auto nonce_hex=sor::sha_bytes(nonce,16);session=root/("session-"+nonce_hex);
  if(!fs::create_directory(session))return false;
  FILETIME created{},ended{},kernel{},user{};if(!GetProcessTimes(GetCurrentProcess(),&created,&ended,&kernel,&user))return false;
  LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);base=U(image);
  std::string site_json="[";void* locations[18]{};unsigned lengths[18]{};const char* hashes[18]{};
  for(unsigned i=0;i<18;++i){const auto& site=sites[i];locations[i]=(void*)(base+site.rva);lengths[i]=site.length;hashes[i]=site.hash;
   if(i)site_json+=",";site_json+="{\"index\":"+std::to_string(i)+",\"rva\":"+std::to_string(site.rva)+",\"va\":"+std::to_string(U(locations[i]))+",\"guard_sha256\":"+sor::quote(site.hash)+"}";}
  site_json+="]";
  identity="{\"schema\":\"sor-d5x/4\",\"retail\":true,\"nonce\":"+sor::quote(nonce_hex)+",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"creation_filetime\":"+std::to_string((U(created.dwHighDateTime)<<32)|created.dwLowDateTime)+",\"module_base\":"+std::to_string(base)+",\"dll_sha256\":"+sor::quote(self_hash)+",\"host_sha256\":"+sor::quote(game_hash)+",\"sfse_sha256\":"+sor::quote(sfse_hash)+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"sites\":"+site_json;
  auto id=identity+"}\n";identity_hash=sor::sha_bytes(id.data(),id.size());if(!sor::write_new(session/L"identity.json",id))return false;
  while(!sole_thread()){
   if(!disk(65536)||fs::exists(session/L"STOP")){sor::write_new(session/L"not-ready.json",identity+",\"error\":\"admission_STOP_or_disk\"}\n");return false;}
   Sleep(100);
  }
  for(const auto& target:target_guards){unsigned char bytes[32]{};if(!read(base+target.rva,bytes,32)||sor::sha_bytes(bytes,32)!=target.hash){sor::write_new(session/L"not-ready.json",identity+",\"error\":\"target_guard\"}\n");return false;}}
  if(!configure(locations,lengths,hashes)){sor::write_new(session/L"not-ready.json",identity+",\"error\":\"site_or_relocation\"}\n");return false;}
  raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  ack=CreateFileW((session/L"flush.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
  if(raw==INVALID_HANDLE_VALUE||ack==INVALID_HANDLE_VALUE)return false;
  initialize_queue();enabled=true;if(!install(edits,18,dirty)){enabled=false;return dirty;}
  Event ready{};ready.kind=Ready;ready.epoch=epoch;emit(ready);
  HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);
  if(!thread){enabled=false;broken=true;sor::write_new(session/L"not-ready.json",identity+",\"error\":\"worker_create\"}\n");return true;}
  CloseHandle(thread);return true;
 }catch(...){enabled=false;broken=true;return dirty;}
}
