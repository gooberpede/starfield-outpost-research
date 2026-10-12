// SPDX-License-Identifier: GPL-3.0-or-later
#include "patch.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
#include <exception>

namespace {
using namespace oracle;
fs::path session;Edit edits[4];uint64_t module{};std::string session_identity;bool mutated{};
bool output_ok(const fs::path& p){
    if(p!=fs::path(L"D:/Projects/starfield-outpost-research/.local-work/native-oracle-live"))return false;
    for(auto cur=p;!cur.empty();){auto a=GetFileAttributesW(cur.c_str());if(a!=INVALID_FILE_ATTRIBUTES&&(a&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto parent=cur.parent_path();if(parent==cur)break;cur=parent;}return true;
}
bool integrity(){for(auto& e:edits)if(!match(e,true))return false;return true;}
bool append(HANDLE h,const void* p,size_t n){return durable_append(h,p,n,disk());}
DWORD WINAPI worker(void*){
    HANDLE raw=INVALID_HANDLE_VALUE,journal=INVALID_HANDLE_VALUE;std::string failure;
    try{
        raw=CreateFileW((session/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        journal=CreateFileW((session/L"records.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        if(raw==INVALID_HANDLE_VALUE||journal==INVALID_HANDLE_VALUE)throw std::runtime_error("writer_open");
        auto patch_manifest=session_identity+",\"patches\":[";
        for(unsigned i=0;i<4;++i){auto& e=edits[i];if(i)patch_manifest+=",";patch_manifest+="{\"runtime_va\":"+quote(hex(reinterpret_cast<uint64_t>(e.address)))+",\"length\":"+std::to_string(e.size)+",\"installed_sha256\":"+quote(sha_bytes(e.after,e.size))+",\"original_sha256\":"+quote(sha_bytes(e.before,e.size))+"}";}
        patch_manifest+="]}\n";
        if(!write_new(session/L"patches.json",patch_manifest))throw std::runtime_error("patch_manifest");
        HANDLE modules=CreateFileW((session/L"modules.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);
        if(modules==INVALID_HANDLE_VALUE)throw std::runtime_error("modules_open");
        HANDLE snapshot=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());MODULEENTRY32W entry{};entry.dwSize=sizeof entry;
        bool module_ok=snapshot!=INVALID_HANDLE_VALUE&&Module32FirstW(snapshot,&entry);
        if(module_ok){do{auto u=fs::path(entry.szExePath).u8string();auto line="{\"path\":"+quote(std::string(reinterpret_cast<const char*>(u.data()),u.size()))+",\"base\":"+quote(hex(reinterpret_cast<uint64_t>(entry.modBaseAddr)))+",\"size\":"+std::to_string(entry.modBaseSize)+",\"sha256\":"+quote(sha_file(entry.szExePath))+"}\n";if(!append(modules,line.data(),line.size())){module_ok=false;break;}}while(Module32NextW(snapshot,&entry));if(module_ok)module_ok=GetLastError()==ERROR_NO_MORE_FILES;}
        if(snapshot!=INVALID_HANDLE_VALUE)CloseHandle(snapshot);CloseHandle(modules);if(!module_ok)throw std::runtime_error("modules_snapshot");
        if(!disk()||!integrity()||!write_new(session/L"ready.json",session_identity+"}\n"))throw std::runtime_error("ready");
        uint64_t offset=0,count=0;
        for(;;){
            drain_controlled(*queue,session,edits,4,[&](const Event& e){
                if(!append(raw,&e,sizeof e))throw std::runtime_error("raw_write_flush");
                auto line="{\"offset\":"+std::to_string(offset)+",\"length\":"+std::to_string(sizeof e)+",\"sha256\":"+quote(sha_bytes(&e,sizeof e))+",\"sequence\":"+std::to_string(e.sequence)+",\"invocation\":"+std::to_string(e.invocation)+",\"kind\":"+std::to_string(e.kind)+"}\n";
                if(!append(journal,line.data(),line.size()))throw std::runtime_error("journal_write_flush");
                offset+=sizeof e;++count;
            });
            if(gate.drained()){
                auto terminal=session_identity+",\"events\":"+std::to_string(count)+",\"lost\":"+std::to_string(lost.load())+",\"depth_errors\":"+std::to_string(depth_errors.load())+",\"resident_inert_until_exit\":true,\"patches_retained\":true}\n";
                if(!write_new(session/L"retired.json",terminal))throw std::runtime_error("retired_write");break;
            }
            Sleep(10);
        }
    }catch(const std::exception& e){failure=e.what();gate.stop();}
    if(raw!=INVALID_HANDLE_VALUE)CloseHandle(raw);if(journal!=INVALID_HANDLE_VALUE)CloseHandle(journal);
    if(!failure.empty()){try{if(disk())write_new(session/L"failure.json","{\"error\":"+quote(failure)+",\"lost\":"+std::to_string(lost.load())+",\"active\":"+std::to_string(gate.state.load()&~stop_bit)+",\"patches_retained\":true}\n");}catch(...) {}}
    return 0;
}
bool loaded_hash(HMODULE h,const char* expected){wchar_t p[32768]{};return h&&GetModuleFileNameW(h,p,32768)&&sha_file(p)==expected;}
}
extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={
    SFSEPluginVersionData::kVersion,0x00010000,"SOR Native Position Oracle","Starfield Outpost Systems Research",0,0,{sor::game_version,0},0,0,0
};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* api){
    using namespace oracle;
    try{
        if(!api||api->runtimeVersion!=game_version||api->interfaceVersion!=1||!disk())return false;
        HMODULE self{};if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&SFSEPlugin_Load),&self))return false;
        module=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));
        if(!loaded_hash(reinterpret_cast<HMODULE>(module),expected_game_hash)||!loaded_hash(GetModuleHandleW(L"sfse_1_16_244.dll"),expected_sfse_hash))return false;
        wchar_t dll[32768]{};if(!GetModuleFileNameW(self,dll,32768))return false;
        auto config=fs::path(dll);config.replace_extension(L"config");std::string content;
        if(!read_small(config,content))return false;
        bool configuration=false;
        for(int g:{0,1})for(int c:{0,1})if(g||c){auto expected="D:/Projects/starfield-outpost-research/.local-work/native-oracle-live\ngrid="+std::to_string(g)+"\ncenter="+std::to_string(c)+"\n";if(content==expected){grid_channel=g!=0;center_channel=c!=0;configuration=true;}}
        if(!configuration)return false;
        fs::path root=L"D:/Projects/starfield-outpost-research/.local-work/native-oracle-live";
        if(!output_ok(root))return false;fs::create_directories(root);
        session=root/("session-"+std::to_string(GetCurrentProcessId())+"-"+std::to_string(GetTickCount64()));
        if(!fs::create_directory(session))return false;
        session_identity="{\"version\":\"0.1.0\",\"component\":\"SorNativePositionOracle\",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"module_base\":"+quote(hex(module))+",\"game_sha256\":"+quote(expected_game_hash)+",\"sfse_sha256\":"+quote(expected_sfse_hash)+",\"sfse_reported_version\":"+std::to_string(api->sfseVersion)+",\"dll_sha256\":"+quote(sha_file(dll))+",\"event_size\":"+std::to_string(sizeof(Event))+",\"utc\":"+quote(utc());
        FILETIME created{},exited{},kernel{},user{};LARGE_INTEGER frequency{};
        if(!GetProcessTimes(GetCurrentProcess(),&created,&exited,&kernel,&user)||!QueryPerformanceFrequency(&frequency))throw std::runtime_error("clock_process_identity");
        session_identity+=",\"process_creation_filetime\":"+std::to_string((uint64_t(created.dwHighDateTime)<<32)|created.dwLowDateTime)+",\"qpc_frequency\":"+std::to_string(frequency.QuadPart)+",\"grid_channel\":"+(grid_channel?"true":"false")+",\"center_channel\":"+(center_channel?"true":"false");
        for(auto g:guards){unsigned char b[32]{};SIZE_T got{};if(!ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(module+g.rva),b,32,&got)||got!=32)throw std::runtime_error("loaded_native_guard");
            if(g.rva==0x4b916e8){uint64_t p[3]{};memcpy(p,b,24);if(p[0]!=module+0x31a630||p[1]!=module+0xad8ec0||p[2]!=module+0xad8ec0)throw std::runtime_error("relocated_vtable_guard");}
            else if(sha_bytes(b,32)!=g.hash)throw std::runtime_error("loaded_native_guard");}
        original_callback=reinterpret_cast<Callback>(module+0xad8ec0);original_center=reinterpret_cast<Center>(module+0xf4ab80);original_selector=reinterpret_cast<Selector>(module+0x96f5c0);
        settings_addresses[0]=module+0x5ea66f0;settings_addresses[1]=module+0x5ea6770;settings_addresses[2]=module+0x4f03eec;
        queue=new Queue<4096>();
        auto relay_page=islands(module+0xad0c36);if(!relay_page)throw std::runtime_error("near_allocation");
        island(relay_page,reinterpret_cast<uint64_t>(&center_hook));island(relay_page+16,reinterpret_cast<uint64_t>(&selector_hook));
        DWORD old{};if(!VirtualProtect(relay_page,4096,PAGE_EXECUTE_READ,&old)||!FlushInstructionCache(GetCurrentProcess(),relay_page,4096))throw std::runtime_error("island_protect");
        if(!call_edit(edits[0],module+0xad0c36,reinterpret_cast<uint64_t>(relay_page))||!call_edit(edits[1],module+0xad0d36,reinterpret_cast<uint64_t>(relay_page+16)))throw std::runtime_error("call_range");
        const unsigned char center_before[]={0xe8,0x45,0x9f,0x47,0};const unsigned char grid_before[]={0xe8,0x85,0xe8,0xe9,0xff};
        memcpy(edits[0].before,center_before,5);memcpy(edits[1].before,grid_before,5);
        for(unsigned i=2;i<4;++i){auto& e=edits[i];e.address=reinterpret_cast<unsigned char*>(module+0x4b916f0+(i-2)*8);e.size=8;auto before=module+0xad8ec0,after=reinterpret_cast<uint64_t>(&callback_hook);memcpy(e.before,&before,8);memcpy(e.after,&after,8);}
        // Mandatory fail-closed scope: SFSE synchronous pre-main Load, exactly
        // one process thread, no workers started by this plugin, no retry.
        auto wait_start=GetTickCount64();
        while(!sole_thread()&&GetTickCount64()-wait_start<120000){if(!disk())throw std::runtime_error("startup_disk_guard");Sleep(100);}
        if(!sole_thread())throw std::runtime_error("NOT_READY_NOT_SOLE_THREAD");
        session_identity+=",\"startup_wait_ms\":"+std::to_string(GetTickCount64()-wait_start);
        if(!install(edits,4,true,mutated))throw std::runtime_error(mutated?"install_rollback_failed":"install_refused_restored");
        gate.state.store(0);
        HANDLE h=CreateThread(nullptr,0,worker,nullptr,0,nullptr);if(!h)throw std::runtime_error("worker_create");CloseHandle(h);
        return true;
    }catch(const std::exception& e){gate.stop();try{if(!session.empty()&&disk())write_new(session/L"not-ready.json",session_identity+",\"reason\":"+quote(e.what())+",\"may_have_patches\":"+(mutated?"true":"false")+"}\n");}catch(...){}
        // SFSE must keep callbacks/islands resident once any edit may be live.
        return mutated;
    }
}
