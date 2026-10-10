// SPDX-License-Identifier: GPL-3.0-or-later
#include "capture.h"
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
#include <TlHelp32.h>
#include <atomic>
#include <psapi.h>
#pragma comment(lib,"psapi.lib")

namespace {
using namespace beacon;
fs::path root,session;uint64_t module{};std::string dll_hash;uint32_t reported_sfse{};
std::string path_text(const fs::path& path){auto s=path.u8string();return std::string(reinterpret_cast<const char*>(s.data()),s.size());}
bool disk(){
    ULARGE_INTEGER c{},d{};
    bool queried=GetDiskFreeSpaceExW(L"C:\\",&c,nullptr,nullptr)&&GetDiskFreeSpaceExW(L"D:\\",&d,nullptr,nullptr);
    return space_safe(c.QuadPart,d.QuadPart,queried);
}
bool safe_output(const fs::path& p){
    if(!p.is_absolute() || p.lexically_normal()!=p || p.filename()!=L"beacon-observer-live" || p.parent_path().filename()!=L".local-work")return false;
    if(!fs::is_regular_file(p.parent_path().parent_path()/L"docs/implementation-briefs/CODEX_IMPLEMENTATION_BRIEF_SOR_live_beacon_coordinate_observer.md"))return false;
    for(auto cur=p;!cur.empty();){auto attrs=GetFileAttributesW(cur.c_str());if(attrs!=INVALID_FILE_ATTRIBUTES&&(attrs&FILE_ATTRIBUTE_REPARSE_POINT))return false;auto parent=cur.parent_path();if(parent==cur)break;cur=parent;}return true;
}
std::string context(){FILETIME created{},exited{},kernel{},user{};if(!GetProcessTimes(GetCurrentProcess(),&created,&exited,&kernel,&user))throw std::runtime_error("process_identity_unavailable");
    return "\"version\":"+quote(observer_version)+",\"game_version\":\"1.16.244.0\",\"sfse_reported_version\":"+std::to_string(reported_sfse)+",\"sfse_sha256\":"+quote(expected_sfse_hash)+",\"utc\":"+quote(utc())+",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"process_creation_filetime\":"+quote(hex((uint64_t(created.dwHighDateTime)<<32)|created.dwLowDateTime))+",\"thread_id\":"+std::to_string(GetCurrentThreadId())+",\"execution_context\":\"observer_worker_read_only_no_engine_calls\",\"module_base\":"+quote(hex(module))+",\"game_sha256\":"+quote(expected_game_hash)+",\"dll_sha256\":"+quote(dll_hash);}
bool sites(){ProcessReader r;for(auto g:guards){unsigned char b[32]{};if(!r.bytes(module+g.rva,b,sizeof b)||sha_bytes(b,sizeof b)!=g.hash)return false;}return true;}
DWORD WINAPI worker(void*){
    try{
        Writer startup(session/L"startup",disk);
        startup.event("{\"kind\":\"session\","+context()+"}");
        HANDLE snap=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());
        if(snap==INVALID_HANDLE_VALUE)throw std::runtime_error("module_snapshot");
        MODULEENTRY32W e{};e.dwSize=sizeof e;
        if(!Module32FirstW(snap,&e)){CloseHandle(snap);throw std::runtime_error("module_first");}
        do{startup.event("{\"kind\":\"module\",\"path\":"+quote(path_text(e.szExePath))+",\"base\":"+quote(hex(reinterpret_cast<uint64_t>(e.modBaseAddr)))+",\"size\":"+std::to_string(e.modBaseSize)+",\"sha256\":"+quote(sha_file(e.szExePath))+"}");}while(Module32NextW(snap,&e));
        auto error=GetLastError();CloseHandle(snap);if(error!=ERROR_NO_MORE_FILES)throw std::runtime_error("module_enumeration");startup.finish("STARTUP_RECORDED");
        if(!disk()||!write_new(session/L"ready.json","{"+context()+",\"ready\":true}\n"))throw std::runtime_error("ready_failed");
        std::set<std::string> consumed;
        while(!fs::exists(session/L"STOP")){
            if(!disk())throw std::runtime_error("disk_guard");
            for(auto& entry:fs::directory_iterator(session)){
                if(entry.path().extension()!=L".request" || !entry.is_regular_file())continue;
                auto label=entry.path().stem().string();if(!consumed.insert(label).second)continue;
                std::string value;
                if(!label_ok(label)||!read_small(entry.path(),value,128)||value!="SETTLED "+label+"\n"){
                    if(!write_new(session/("rejected-"+std::to_string(consumed.size())+".json"),"{\"reason\":\"invalid_request\","+context()+"}\n"))throw std::runtime_error("rejection_write");continue;
                }
                if(!sites())throw std::runtime_error("loaded_code_integrity");
                auto start=GetTickCount64();Writer writer(session/label,[&]{if(fs::exists(session/L"STOP"))throw std::runtime_error("operator_stop_partial");return disk();});
                writer.event("{\"kind\":\"begin\",\"label\":"+quote(label)+","+context()+"}");
                ProcessReader r;Capture capture(r,writer,module);capture.run();
                // Cost report occurs after the durable acquisition marker.
                PROCESS_MEMORY_COUNTERS pm{};pm.cb=sizeof pm;bool measured=GetProcessMemoryInfo(GetCurrentProcess(),&pm,sizeof pm)!=0;
                writer.event("{\"kind\":\"metrics\",\"elapsed_ms\":"+std::to_string(GetTickCount64()-start)+",\"bytes\":"+std::to_string(writer.bytes)+",\"process_memory_measured\":"+(measured?"true":"false")+",\"working_set_bytes\":"+std::to_string(pm.WorkingSetSize)+",\"peak_working_set_bytes\":"+std::to_string(pm.PeakWorkingSetSize)+",\"scope\":\"whole_process_not_observer_only\"}");
            }
            Sleep(250);
        }
        if(disk())write_new(session/L"retired.json","{"+context()+",\"resident_until_process_exit\":true}\n");
    }catch(const std::exception& e){
        // No write attempted below disk threshold. Last fully flushed journal
        // records remain recoverable even when terminal evidence cannot be made.
        try{if(disk())write_new(session/L"failure.json","{\"version\":"+quote(observer_version)+",\"utc\":"+quote(utc())+",\"instrumentation_health\":\"STOPPED\",\"reason\":"+quote(e.what())+"}\n");}catch(const std::exception&){}
    }return 0;
}
}
extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={
    SFSEPluginVersionData::kVersion,observer_version_int,"SOR Beacon Coordinate Observer","Starfield Outpost Systems Research",0,0,{sor::game_version,0},0,0,0
};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* sfse){
    try{
        using namespace beacon;
        if(!sfse||sfse->runtimeVersion!=game_version||sfse->interfaceVersion!=1||!disk())return false;
        reported_sfse=sfse->sfseVersion;
        wchar_t exe[32768]{},self[32768]{},sfse_path[32768]{};HMODULE dll{};
        if(!GetModuleFileNameW(nullptr,exe,32768)||sha_file(exe)!=expected_game_hash)return false;
        HMODULE sfse_module=GetModuleHandleW(L"sfse_1_16_244.dll");
        if(!sfse_module||!GetModuleFileNameW(sfse_module,sfse_path,32768)||sha_file(sfse_path)!=expected_sfse_hash)return false;
        module=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));if(!sites())return false;
        if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&SFSEPlugin_Load),&dll)||!GetModuleFileNameW(dll,self,32768))return false;
        dll_hash=sha_file(self);if(dll_hash.empty())return false;
        auto config=fs::path(self);config.replace_extension(L"config");std::string text;
        if(!read_small(config,text)||text.empty()||text.back()!='\n')return false;text.pop_back();
        root=fs::path(std::u8string(reinterpret_cast<const char8_t*>(text.data()),text.size()));
        if(!safe_output(root))return false;
        fs::create_directories(root);session=root/("session-"+std::to_string(GetCurrentProcessId())+"-"+std::to_string(GetTickCount64()));
        if(!fs::create_directory(session))return false;
        // No registered callback, task queue, hook or native ownership exists.
        // Worker exits cooperatively; DLL stays loaded until normal process exit.
        HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);if(!thread)return false;CloseHandle(thread);return true;
    }catch(const std::exception&){return false;}
}
