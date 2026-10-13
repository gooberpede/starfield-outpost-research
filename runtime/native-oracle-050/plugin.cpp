// SPDX-License-Identifier: GPL-3.0-or-later
#include "health.h"
#include "travel.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
#include <exception>

namespace {
using namespace oracle;
fs::path session;constexpr unsigned calls=19,edit_count=21;Edit edits[edit_count];uint64_t module{};std::string session_identity;bool mutated{};unsigned char* relay_page{};
uint64_t relay_targets[]={reinterpret_cast<uint64_t>(&route_hook),reinterpret_cast<uint64_t>(&eligible_hook),reinterpret_cast<uint64_t>(&search_hook),reinterpret_cast<uint64_t>(&route_fallback_hook),reinterpret_cast<uint64_t>(&route_source_hook),reinterpret_cast<uint64_t>(&route_grid_hook),reinterpret_cast<uint64_t>(&route_delta_hook),reinterpret_cast<uint64_t>(&route_delta_hook),reinterpret_cast<uint64_t>(&direct_identity_hook),reinterpret_cast<uint64_t>(&identity_hook),reinterpret_cast<uint64_t>(&query_hook),reinterpret_cast<uint64_t>(&enum_hook),reinterpret_cast<uint64_t>(&selected_hook),reinterpret_cast<uint64_t>(&selected_body_hook),reinterpret_cast<uint64_t>(&producer_bridge),reinterpret_cast<uint64_t>(&travel_producer_bridge),reinterpret_cast<uint64_t>(&travel_command_bridge),reinterpret_cast<uint64_t>(&center_hook),reinterpret_cast<uint64_t>(&selector_hook)};
bool output_ok(const fs::path& p){
    if(p!=fs::path(L"D:/Projects/starfield-outpost-research/.local-work/native-oracle-live"))return false;
    for(auto cur=p;!cur.empty();){auto a=GetFileAttributesW(cur.c_str());if(a!=INVALID_FILE_ATTRIBUTES&&(a&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto parent=cur.parent_path();if(parent==cur)break;cur=parent;}return true;
}
bool integrity(){for(auto& e:edits)if(!match(e,true))return false;return true;}
void verify_native(bool installed){
    if(installed)for(unsigned i=0;i<calls;++i)if(!relay_guard(relay_page+i*16,relay_targets[i]))throw std::runtime_error("relay_integrity");
    for(auto g:guards){
        unsigned char b[32]{};SIZE_T got{};if(!ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(module+g.rva),b,32,&got)||got!=32)throw std::runtime_error("loaded_native_guard");
            if(g.rva==0x4b916e8){uint64_t p[3]{};memcpy(p,b,24);auto callback=installed?reinterpret_cast<uint64_t>(&callback_hook):module+0xad8ec0;if(p[0]!=module+0x31a630||p[1]!=callback||p[2]!=callback)throw std::runtime_error("relocated_vtable_guard");}
            else {if(installed)original_window(b,module+g.rva,32,edits,calls);if(sha_bytes(b,32)!=g.hash)throw std::runtime_error("loaded_native_guard");}}
}
bool append(HANDLE h,const void* p,size_t n){return durable_append(h,p,n,disk());}
DWORD WINAPI worker(void*){
    HANDLE raw=INVALID_HANDLE_VALUE,journal=INVALID_HANDLE_VALUE;std::string failure;Health health;
    try{
        health.open(session,session_identity);
        raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        journal=CreateFileW((session/L"records.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        if(raw==INVALID_HANDLE_VALUE||journal==INVALID_HANDLE_VALUE)throw std::runtime_error("writer_open");
        auto patch_manifest=session_identity+",\"patches\":[";
        for(unsigned i=0;i<edit_count;++i){auto& e=edits[i];if(i)patch_manifest+=",";patch_manifest+="{\"runtime_va\":"+quote(hex(reinterpret_cast<uint64_t>(e.address)))+",\"length\":"+std::to_string(e.size)+",\"installed_sha256\":"+quote(sha_bytes(e.after,e.size))+",\"original_sha256\":"+quote(sha_bytes(e.before,e.size))+"}";}
        patch_manifest+="],\"relays\":[";
        for(unsigned i=0;i<calls;++i){if(i)patch_manifest+=",";patch_manifest+="{\"runtime_va\":"+quote(hex(reinterpret_cast<uint64_t>(relay_page+i*16)))+",\"target_va\":"+quote(hex(relay_targets[i]))+",\"length\":14,\"sha256\":"+quote(sha_bytes(relay_page+i*16,14))+",\"protection\":\"PAGE_EXECUTE_READ\"}";}patch_manifest+="]}\n";
        if(!write_new(session/L"patches.json",patch_manifest))throw std::runtime_error("patch_manifest");
        health.poll(session,edits,edit_count,true);
        if(!disk()||!integrity()||!write_new(session/L"ready.json",session_identity+"}\n"))throw std::runtime_error("ready");
        uint64_t offset=0,count=0;
        for(;;){
            drain_controlled(*queue,session,edits,edit_count,[&](const Event& e){
                verify_native(true);health.poll(session,edits,edit_count);
                if(!append(raw,&e,sizeof e))throw std::runtime_error("raw_write_flush");
                auto line="{\"offset\":"+std::to_string(offset)+",\"length\":"+std::to_string(sizeof e)+",\"sha256\":"+quote(sha_bytes(&e,sizeof e))+",\"sequence\":"+std::to_string(e.sequence)+",\"invocation\":"+std::to_string(e.invocation)+",\"kind\":"+std::to_string(e.kind)+"}\n";
                if(!append(journal,line.data(),line.size()))throw std::runtime_error("journal_write_flush");
                offset+=sizeof e;++count;health.flushed_events=count;health.flushed_offset=offset;
            });
            verify_native(true);health.poll(session,edits,edit_count);
            if(gate.drained()){
                health.poll(session,edits,edit_count,true);
                auto terminal=session_identity+",\"retired_utc\":"+quote(utc())+",\"retired_tick\":"+std::to_string(GetTickCount64())+",\"events\":"+std::to_string(count)+",\"lost\":"+std::to_string(lost.load())+",\"health_timeouts\":"+std::to_string(health_timeouts.load())+",\"depth_errors\":"+std::to_string(depth_errors.load())+",\"resident_inert_until_exit\":true,\"patches_retained\":true}\n";
                if(!write_new(session/L"retired.json",terminal))throw std::runtime_error("retired_write");break;
            }
            Sleep(10);
        }
    }catch(const std::exception& e){failure=e.what();gate.stop();}
    health.close();
    if(raw!=INVALID_HANDLE_VALUE)CloseHandle(raw);if(journal!=INVALID_HANDLE_VALUE)CloseHandle(journal);
    if(!failure.empty()){try{if(disk())write_new(session/L"failure.json","{\"error\":"+quote(failure)+",\"lost\":"+std::to_string(lost.load())+",\"health_timeouts\":"+std::to_string(health_timeouts.load())+",\"active\":"+std::to_string(gate.state.load()&~stop_bit)+",\"patches_retained\":true}\n");}catch(...) {}}
    return 0;
}
bool loaded_hash(HMODULE h,const char* expected){wchar_t p[32768]{};return h&&GetModuleFileNameW(h,p,32768)&&sha_file(p)==expected;}
}
extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={
    SFSEPluginVersionData::kVersion,0x00050000,"SOR Native Position Oracle","Starfield Outpost Systems Research",0,0,{sor::game_version,0},0,0,0
};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* api){
    using namespace oracle;
    try{
        if(!api||api->runtimeVersion!=game_version||api->interfaceVersion!=1||!disk())return false;
        HMODULE self{};if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&SFSEPlugin_Load),&self))return false;
        module=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));
        if(!loaded_hash(reinterpret_cast<HMODULE>(module),expected_game_hash)||!loaded_hash(GetModuleHandleW(L"sfse_1_16_244.dll"),expected_sfse_hash))return false;
        wchar_t dll[32768]{};if(!GetModuleFileNameW(self,dll,32768))return false;
        // Self-contained exact candidate: no runtime config/text payload.
        grid_channel=true;center_channel=true;
        fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/native-oracle-live";
        if(!output_ok(root))return false;fs::create_directories(root);
        session=root/("session-"+std::to_string(GetCurrentProcessId())+"-"+std::to_string(GetTickCount64()));
        if(!fs::create_directory(session))return false;
        session_identity="{\"version\":\"0.5.0\",\"component\":\"SorNativePositionOracle\",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"module_base\":"+quote(hex(module))+",\"game_sha256\":"+quote(expected_game_hash)+",\"sfse_sha256\":"+quote(expected_sfse_hash)+",\"sfse_reported_version\":"+std::to_string(api->sfseVersion)+",\"dll_sha256\":"+quote(sha_file(dll))+",\"schema\":5,\"heartbeat_ms\":1000,\"health_deadline_ms\":15000,\"event_size\":"+std::to_string(sizeof(Event))+",\"utc\":"+quote(utc());
        FILETIME created{},exited{},kernel{},user{};LARGE_INTEGER frequency{};
        if(!GetProcessTimes(GetCurrentProcess(),&created,&exited,&kernel,&user)||!QueryPerformanceFrequency(&frequency))throw std::runtime_error("clock_process_identity");
        session_identity+=",\"process_creation_filetime\":"+std::to_string((uint64_t(created.dwHighDateTime)<<32)|created.dwLowDateTime)+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"grid_channel\":"+(grid_channel?"true":"false")+",\"center_channel\":"+(center_channel?"true":"false");
        verify_native(false);
        original_query=reinterpret_cast<Query>(module+0xad08d0);original_enum=reinterpret_cast<Enumerate>(module+0xb1e190);
        original_route=reinterpret_cast<Route>(module+0x77fc20);original_eligible=reinterpret_cast<Helper3>(module+0x77def0);
        original_search=reinterpret_cast<Six>(module+0x77f900);original_route_fallback=reinterpret_cast<Five>(module+0x77e350);
        original_route_source=reinterpret_cast<Helper3>(module+0x96eb90);original_route_grid=reinterpret_cast<Helper3>(module+0x96f5c0);
        original_route_delta=reinterpret_cast<Helper4>(module+0x96f940);original_identity=reinterpret_cast<Helper3>(module+0xad3b20);manager_slot=module+0x5fd9c30;original_selected=reinterpret_cast<Helper4>(module+0x17dfdf0);original_selected_body=reinterpret_cast<Helper3>(module+0xad3b20);original_producer=reinterpret_cast<Helper4>(module+0x78b030);
        original_travel_producer=reinterpret_cast<Helper4>(module+0x78b030);original_travel_command=reinterpret_cast<Helper2>(module+0x1a67830);
        original_callback=reinterpret_cast<Callback>(module+0xad8ec0);original_center=reinterpret_cast<Center>(module+0xf4ab80);original_selector=reinterpret_cast<Selector>(module+0x96f5c0);
        settings_addresses[0]=module+0x5ea66f0;settings_addresses[1]=module+0x5ea6770;settings_addresses[2]=module+0x4f03eec;
        queue=new Queue<4096>();
        relay_page=islands(module+0xad0c36);if(!relay_page)throw std::runtime_error("near_allocation");
        for(unsigned i=0;i<calls;++i)island(relay_page+i*16,relay_targets[i]);
        DWORD old{};if(!VirtualProtect(relay_page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),relay_page,4096))throw std::runtime_error("island_protect");
        for(unsigned i=0;i<calls;++i){
            if(!relay_guard(relay_page+i*16,relay_targets[i]))throw std::runtime_error("relay_pre_edit");
            if(!call_edit(edits[i],module+call_sites[i].rva,reinterpret_cast<uint64_t>(relay_page+i*16)))throw std::runtime_error("call_range");
            memcpy(edits[i].before,call_sites[i].bytes,5);
        }
        for(unsigned i=calls;i<edit_count;++i){auto& e=edits[i];e.address=reinterpret_cast<unsigned char*>(module+0x4b916f0+(i-calls)*8);e.size=8;auto before=module+0xad8ec0,after=reinterpret_cast<uint64_t>(&callback_hook);memcpy(e.before,&before,8);memcpy(e.after,&after,8);}
        // Mandatory fail-closed scope: SFSE synchronous pre-main Load, exactly
        // one process thread, no workers started by this plugin, no retry.
        auto waited=await_admission(session,session_identity);
        session_identity+=",\"startup_wait_ms\":"+std::to_string(waited);
        // User's continuation accepts normal overlays. Inventory is provenance,
        // not a blanket module allowlist; exact owned-site guards stay hard.
        if(!disk()||!write_new(session/L"modules-pre-edit.jsonl",module_inventory(),1048576))throw std::runtime_error("pre_edit_modules");
        verify_native(false);
        for(auto& edit:edits)if(!match(edit,false))throw std::runtime_error("pre_edit_site_conflict");
        if(!sole_thread())throw std::runtime_error("NOT_READY_NOT_SOLE_THREAD");
        if(!disk()||!write_new(session/L"admission.json",session_identity+",\"admission_utc\":"+quote(utc())+",\"owned_sites_original\":true,\"sole_thread_observed\":true,\"standard_overlays_accepted\":true,\"patches_installed_at_receipt\":false}\n"))throw std::runtime_error("admission_receipt");
        if(!install(edits,edit_count,sole_thread(),mutated))throw std::runtime_error(mutated?"install_rollback_failed":"install_refused_restored");
        worker_tick.store(GetTickCount64());worker_required.store(true);gate.state.store(0);
        HANDLE h=CreateThread(nullptr,0,worker,nullptr,0,nullptr);if(!h)throw std::runtime_error("worker_create");CloseHandle(h);
        return true;
    }catch(const std::exception& e){gate.stop();try{if(!session.empty()&&disk())write_new(session/L"not-ready.json",session_identity+",\"reason\":"+quote(e.what())+",\"may_have_patches\":"+(mutated?"true":"false")+"}\n");}catch(...){}
        // SFSE must keep callbacks/islands resident once any edit may be live.
        return mutated;
    }
}
