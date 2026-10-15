// SPDX-License-Identifier: GPL-3.0-or-later
#include "capture.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
#include <exception>
namespace {
using namespace history;
constexpr size_t count=sizeof(sites)/sizeof(sites[0]);Edit edits[count];unsigned char* relays{};bool mutated{};fs::path session;std::string session_identity;
HANDLE emergency=INVALID_HANDLE_VALUE;
bool prepare_emergency(){emergency=CreateFileW((session/L"emergency-status.json").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);if(emergency==INVALID_HANDLE_VALUE)return false;std::string empty="{}";empty.resize(4096,' ');return Spool::append(emergency,empty.data(),empty.size());}
bool emergency_failure(const std::string& error){
    // Fixed preallocated status page: overwrite only after an actual failure,
    // never grow the file or rewrite raw evidence. Usable when disk query fails.
    auto data=session_identity+",\"error\":"+quote(error)+","+spool.counts()+"}\n";if(data.size()>4096)return false;data.resize(4096,' ');LARGE_INTEGER zero{};return emergency!=INVALID_HANDLE_VALUE&&SetFilePointerEx(emergency,zero,nullptr,FILE_BEGIN)&&Spool::append(emergency,data.data(),data.size());
}
bool output_ok(const fs::path& p){if(p!=fs::path(L"D:/Projects/starfield-outpost-research/.local-work/continuous-beacon-preview/live"))return false;for(auto c=p;!c.empty();){auto a=GetFileAttributesW(c.c_str());if(a!=INVALID_FILE_ATTRIBUTES&&(a&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto next=c.parent_path();if(next==c)break;c=next;}return true;}
void verify(bool installed){
    for(auto& g:target_guards){Blob b;if(!copy(b,image_base+g.rva,32))throw std::runtime_error("target_guard_read");if(installed)original_window(b.bytes,image_base+g.rva,32,edits,count);if(sha_bytes(b.bytes,32)!=g.hash)throw std::runtime_error("native_target_entry_changed");}
    for(size_t i=0;i<count;++i){auto& s=sites[i];if(installed&&!match(edits[i],true))throw std::runtime_error("owned_site_changed");
        Blob b;if(!copy(b,image_base+s.rva,32))throw std::runtime_error("native_guard_unreadable");
        if(s.length==8){uint64_t expected=installed?reinterpret_cast<uint64_t>(s.hook):image_base+s.target;if(field<uint64_t>(b,0)!=expected)throw std::runtime_error("relocated_vtable_guard");}
        else{if(installed){original_window(b.bytes,image_base+s.rva,32,edits,count);if(!relay_guard(relays+i*16,reinterpret_cast<uint64_t>(s.hook)))throw std::runtime_error("relay_guard");}if(sha_bytes(b.bytes,32)!=s.hash)throw std::runtime_error("native_preimage_guard");}
    }
}
bool loaded_hash(HMODULE h,const char* expected){wchar_t p[32768]{};return h&&GetModuleFileNameW(h,p,32768)&&sha_file(p)==expected;}
DWORD WINAPI worker(void*){
    std::string error;HANDLE health=INVALID_HANDLE_VALUE;uint64_t serial{};
    try{
        health=CreateFileW((session/L"health.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);if(health==INVALID_HANDLE_VALUE)throw std::runtime_error("health_open");
        verify(true);if(!spool.flush())throw std::runtime_error("ready_transport_flush");
        std::string initial_stop;if(!read_small(session/L"operator-stop.flag",initial_stop,4))throw std::runtime_error("initial_stop_flag_read");
        if(initial_stop=="STOP"||fs::exists(session/L"STOP"))spool.stop();else if(initial_stop!="RUN\n")throw std::runtime_error("initial_stop_flag_payload");
        if(!spool.stopping&&!write_new(session/L"ready.json",session_identity+",\"capture_active\":true,\"group_flush_spool\":true}\n"))throw std::runtime_error("ready_write");
        while(true){
            if(!disk())throw std::runtime_error("disk_query_or_floor");verify(true);
            std::string stop_flag;if(!read_small(session/L"operator-stop.flag",stop_flag,4))throw std::runtime_error("stop_flag_read");
            if(stop_flag=="STOP"||fs::exists(session/L"STOP"))spool.stop();else if(stop_flag!="RUN\n")throw std::runtime_error("stop_flag_payload");
            if(!spool.flush())throw std::runtime_error("group_flush");
            auto line=session_identity+",\"health_sequence\":"+std::to_string(++serial)+",\"tick\":"+std::to_string(GetTickCount64())+",\"stopping\":"+(spool.stopping?"true":"false")+","+spool.counts()+"}\n";
            if(!disk(line.size())||!Spool::append(health,line.data(),line.size()))throw std::runtime_error("health_write_flush");
            for(auto& p:fs::directory_iterator(session)){
                auto n=p.path().filename().string();
                if(n.size()!=48||n.substr(0,8)!="control-"||n.substr(40)!=".request")continue;
                bool valid=true;for(size_t i=8;i<40;++i)valid&=isxdigit(static_cast<unsigned char>(n[i]))!=0;
                if(!valid)throw std::runtime_error("control_nonce_name");auto ack=session/("ack-"+n.substr(8,32)+".json");if(fs::exists(ack))continue;
                std::string payload;if(!read_small(p.path(),payload)||payload!="ACK\n")throw std::runtime_error("control_payload");
                auto receipt=session_identity+",\"nonce\":"+quote(n.substr(8,32))+",\"ack_utc\":"+quote(utc())+","+spool.counts()+"}\n";
                if(!disk(receipt.size())||!write_new(ack,receipt))throw std::runtime_error("ack_write");
            }
            if(spool.broken)throw std::runtime_error("spool_integrity_failure");
            if(spool.stopping&&spool.active==0)break;
            Sleep(1000); // heartbeat telemetry, never an acquisition timeout
        }
    }catch(const std::exception& e){error=e.what();spool.stop();}
    // STOP never closes handles underneath an in-flight invocation. Resident
    // wrappers remain callable and inert until normal process exit.
    while(spool.active.load()!=0)Sleep(10);
    if(!spool.flush()&&error.empty())error="final_group_flush";
    try{
        if(!disk())throw std::runtime_error("terminal_disk_query_or_floor");
        auto inventory=module_inventory();if(!disk(inventory.size())||!write_new(session/L"modules-final.jsonl",inventory,MAXDWORD))throw std::runtime_error("terminal_module_receipt");
        auto terminal=session_identity+",\"utc_end\":"+quote(utc())+",\"resident_inert_until_exit\":true,"+spool.counts()+",\"error\":"+quote(error)+"}\n";
        if(!disk(terminal.size())||!write_new(session/(error.empty()?L"retired.json":L"failure.json"),terminal))throw std::runtime_error("terminal_receipt_write");
    }catch(const std::exception& e){if(error.empty())error=e.what();spool.broken=true;++spool.failed;}
    if(!error.empty()){spool.broken=true;emergency_failure(error);}
    spool.close();if(health!=INVALID_HANDLE_VALUE)CloseHandle(health);if(emergency!=INVALID_HANDLE_VALUE){CloseHandle(emergency);emergency=INVALID_HANDLE_VALUE;}return 0;
}
}
extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={SFSEPluginVersionData::kVersion,0x00070000,"SOR Native Position Oracle","Starfield Outpost Systems Research",0,0,{sor::game_version,0},0,0,0};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* api){
    using namespace history;
    try{
        if(!api||api->runtimeVersion!=game_version||api->interfaceVersion!=1||!disk())return false;
        HMODULE self{};if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&SFSEPlugin_Load),&self))return false;
        image_base=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));preview::base=image_base;
        if(!loaded_hash(reinterpret_cast<HMODULE>(image_base),game_hash)||!loaded_hash(GetModuleHandleW(L"sfse_1_16_244.dll"),sfse_hash))return false;
        wchar_t dll[32768]{};if(!GetModuleFileNameW(self,dll,32768))return false;
        fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/continuous-beacon-preview/live";if(!output_ok(root))return false;fs::create_directories(root);
        session=root/("session-"+std::to_string(GetCurrentProcessId())+"-"+std::to_string(GetTickCount64()));if(!fs::create_directory(session))return false;
        FILETIME created{},exit{},kernel{},user{};LARGE_INTEGER frequency{};
        if(!GetProcessTimes(GetCurrentProcess(),&created,&exit,&kernel,&user)||!QueryPerformanceFrequency(&frequency))throw std::runtime_error("process_clock_identity");
        session_identity="{\"version\":\"0.7.0\",\"schema\":7,\"event_size\":"+std::to_string(sizeof(Event))+",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"process_creation_filetime\":"+std::to_string((uint64_t(created.dwHighDateTime)<<32)|created.dwLowDateTime)+",\"module_base\":"+quote(hex(image_base))+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"utc\":"+quote(utc())+",\"game_sha256\":"+quote(game_hash)+",\"sfse_sha256\":"+quote(sfse_hash)+",\"sfse_reported_version\":"+std::to_string(api->sfseVersion)+",\"dll_sha256\":"+quote(sha_file(dll));
        if(!write_new(session/L"session.json",session_identity+"}\n"))throw std::runtime_error("session_identity");
        if(!write_new(session/L"operator-stop.flag","RUN\n"))throw std::runtime_error("stop_flag_prepare");
        verify(false);relays=islands(image_base+sites[0].rva);if(!relays)throw std::runtime_error("relay_allocation");
        for(size_t i=0;i<count;++i){auto& s=sites[i];island(relays+i*16,reinterpret_cast<uint64_t>(s.hook));auto& e=edits[i];e.address=reinterpret_cast<unsigned char*>(image_base+s.rva);e.size=s.length;
            if(s.length==5){if(!call_edit(e,image_base+s.rva,reinterpret_cast<uint64_t>(relays+i*16)))throw std::runtime_error("call_range");memcpy(e.before,s.original,5);}
            else{auto before=image_base+s.target,after=reinterpret_cast<uint64_t>(s.hook);memcpy(e.before,&before,8);memcpy(e.after,&after,8);}}
        DWORD old{};if(!VirtualProtect(relays,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),relays,4096))throw std::runtime_error("relay_protect");
        auto waited=await_admission(session,session_identity);verify(false);
        if(!disk()||!write_new(session/L"modules-pre-edit.jsonl",module_inventory(),MAXDWORD)||!spool.open(session)||!prepare_emergency())throw std::runtime_error("pre_edit_transport");
        std::string patches=session_identity+",\"patches\":[";
        for(size_t i=0;i<count;++i){auto& e=edits[i];if(i)patches+=",";patches+="{\"rva\":"+std::to_string(sites[i].rva)+",\"length\":"+std::to_string(e.size)+",\"original_sha256\":"+quote(sha_bytes(e.before,e.size))+",\"installed_sha256\":"+quote(sha_bytes(e.after,e.size))+"}";}patches+="]}\n";
        if(!write_new(session/L"patches.json",patches,MAXDWORD)||!sole_thread())throw std::runtime_error("admission_guard");
        if(!write_new(session/L"admission.json",session_identity+",\"startup_wait_ms\":"+std::to_string(waited)+",\"sole_thread_observed\":true,\"owned_sites_original\":true,\"patches_installed_at_receipt\":false}\n"))throw std::runtime_error("admission_receipt");
        if(!install(edits,count,true,mutated))throw std::runtime_error(mutated?"install_rollback_failed":"install_refused_restored");
        HANDLE h=CreateThread(nullptr,0,worker,nullptr,0,nullptr);if(!h)throw std::runtime_error("worker_create");CloseHandle(h);return true;
    }catch(const std::exception& e){spool.stop();try{if(!session.empty()&&disk())write_new(session/L"not-ready.json",session_identity+",\"error\":"+quote(e.what())+",\"may_have_patches\":"+(mutated?"true":"false")+","+spool.counts()+"}\n");}catch(...){}return mutated;}
}
