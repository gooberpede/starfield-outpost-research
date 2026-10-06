// SPDX-License-Identifier: GPL-3.0-or-later
// Original experiment observer. MIT interface header is the only non-system
// incorporated dependency. No sibling observer code or CommonLib linkage.
#include "format.h"
#include "initialization.h"
#include "observation_policy.h"
#include "acquisition.h"
#include <TlHelp32.h>
#include <atomic>
#include <mutex>
#include "third_party/sfse/PluginAPI.h"
#include "site_guards.generated.h" // hashes generated locally from pinned PE

namespace {
using namespace sor;
SFSETaskInterface* tasks{};
Initialization initialization;
bool session_created{};
fs::path session, plugin_path;
std::uint64_t module_base{};
std::string observer_hash, profile_hash;
std::uint32_t reported_sfse_version{};
std::atomic<bool> busy{}, stopped{};
std::atomic<std::size_t> next_checkpoint{};
LoadTelemetry load_telemetry;
std::atomic<bool> checkpoints_complete{}, had_anomalies{}, diagnostic_consumed{};
ULONGLONG session_start{};
constexpr ULONGLONG session_ms=45*60*1000;
constexpr char expected_game[]="7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28";

std::string synchronization(std::size_t cp) {
    return synchronization_fields(cp,load_telemetry.pre.load(),load_telemetry.post.load());
}

bool sites_match() {
    ProcessReader r;
    for(auto guard:site_guards) {
        std::array<unsigned char,32> bytes{};
        if(!r.bytes(module_base+guard.rva,bytes.data(),bytes.size()) || sha_bytes(bytes.data(),bytes.size())!=guard.sha256) return false;
    }
    return true;
}
void fail(const std::string& reason) {
    stopped=true;
    write_new(session/L"failure.json","{\"kind\":\"RUNTIME\",\"terminal\":\"INCOMPLETE\",\"reason\":"+quote(reason)+",\"utc\":"+quote(utc())+"}\n");
}
bool disk_guard() {
    if(stopped)return false;
    if(auto reason=disk_issue(disk_space())){fail(reason);return false;}
    return true;
}
bool evidence(const fs::path& path,const std::string& data) {
    return disk_guard()&&write_new(path,data,max_checkpoint_bytes);
}
void advance(std::size_t cp,bool anomaly) {
    if(stopped)return;
    if(cp==checkpoints.size()){diagnostic_consumed=true;return;}
    if(anomaly)had_anomalies=true;
    next_checkpoint=cp+1;
    if(cp==5) {
        checkpoints_complete=true;
        const auto terminal=had_anomalies?"CHECKPOINT_SEQUENCE_RECORDED_WITH_ANOMALIES":"CHECKPOINT_SEQUENCE_COMPLETE";
        if(!evidence(session/L"complete.json","{\"terminal\":"+quote(terminal)+",\"checkpoint_count\":6}\n"))fail("sequence_marker_failed");
    }
}
void issue(const std::string& reason,std::size_t cp,const Selection& observed={},unsigned calls=0,ULONGLONG began=0,const std::string& context="") {
    auto name=cp<checkpoints.size()?checkpoints[cp]:"TRACE";
    bool recorded=record_issue(reason,stopped,[&] {
        auto provenance=",\"observer_sha256\":"+quote(observer_hash)+",\"module_base\":"+quote(hex(module_base))+
            synchronization(cp)+",\"thread_id\":"+std::to_string(GetCurrentThreadId());
        auto data=anomaly_json(name,cp<checkpoints.size()?cp:5,reason,observed,calls,began?GetTickCount64()-began:0,provenance+context);
        return evidence(session/(std::string(name)+"-anomaly.json"),data);
    },[](const std::string& value){fail(value);});
    if(recorded)advance(cp,true);
}
void initialization_failure(const char* reason) noexcept {
    stopped=true;
    if(session_created)try {fail(reason);}catch(const std::exception&){}
}
bool live_gate(ProcessReader& r,const Acquisition& current,std::size_t cp,unsigned calls,ULONGLONG began) {
    std::string error;
    if(!consistent(r,module_base,current,error)) {
        issue(error,cp,current.selection,calls,began);return false;
    }
    return true;
}
bool query(ProcessReader& r,const Identity& selected,std::size_t cp,unsigned order,const char* name,std::uint32_t rva,
           std::string& result,const Acquisition& current,unsigned& calls,ULONGLONG began) {
    const auto& picked=current.selection;
    if(!disk_guard())return false;
    if(!sites_match()){fail("loaded_site_mismatch");return false;}
    if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,picked,calls,began);return false;}
    if(!live_gate(r,current,cp,calls,began))return false;
    Identity now{};std::string error;
    if(!identity(r,selected.pointer,now,&error)){issue(error,cp,picked,calls,began,",\"observed_identity\":"+copied_identity(now));return false;}
    if(now!=selected){issue("selected_identity_changed_before_query",cp,picked,calls,began,",\"observed_identity\":"+copied_identity(now));return false;}
    const auto role=selected.base_id==beacon_base ? "beacon":"storage";
    const auto stem=std::string(checkpoints[cp])+"-"+role+"-"+name;
    const auto stamp=utc();
    std::uint64_t global{};
    if(!r.get(module_base+0x05f0b3d8,global)){fail("key_global_read_failed");return false;}
    auto input=form(r,selected.pointer);
    if(input.find("READ_FAILED")!=std::string::npos){fail("query_input_read_failed");return false;}
    auto prefix="{\"checkpoint\":"+quote(checkpoints[cp])+",\"role\":"+quote(role)+",\"query\":"+quote(name)+
        ",\"order\":"+std::to_string(order)+",\"thread_id\":"+std::to_string(GetCurrentThreadId())+",\"utc\":"+quote(stamp)+
        ",\"input\":"+input+",\"key_global_pointer\":"+quote(hex(global))+synchronization(cp);
    if(!evidence(session/(stem+"-begin.json"),prefix+",\"terminal\":\"INVOCATION_STARTED\"}\n")){fail("query_begin_flush_failed");return false;}
    if(!disk_guard()||!live_gate(r,current,cp,calls,began))return false;
    if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,picked,calls,began);return false;}
    // Added native invocation: no exception suppression or cancellation in flight.
    using Callback=std::uint64_t(*)(std::uint64_t,std::uint64_t,std::uint64_t,std::uint64_t);
    ++calls;auto returned=reinterpret_cast<Callback>(module_base+rva)(0,0,selected.pointer,0);
    result=form(r,returned);
    if(!evidence(session/(stem+"-return.json"),prefix+",\"return_utc\":"+quote(utc())+",\"result\":"+result+",\"terminal\":\"INVOCATION_RETURNED\"}\n")){fail("query_return_flush_failed");return false;}
    if(result.find("READ_FAILED")!=std::string::npos){fail("query_result_read_failed");return false;}
    if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,picked,calls,began);return false;}
    return live_gate(r,current,cp,calls,began);
}
class Capture final:public SFSETaskInterface::ITaskDelegate {
    std::size_t cp;
public:
    explicit Capture(std::size_t value):cp(value){}
    void Destroy() override {delete this;}
    void Run() override {
        // Never dereference a reference retained from another task/checkpoint.
        if(stopped){busy=false;return;}
        if(GetTickCount64()-session_start>session_ms){fail("session_deadline");busy=false;return;}
        try {capture();} catch(const std::exception&) {fail("observer_cpp_failure");}
        busy=false;
    }
    void capture() {
        auto began=GetTickCount64();
        if(!disk_guard())return;
        if(!sites_match()){fail("loaded_site_mismatch");return;}
        if(!evidence(session/(std::string(checkpoints[cp])+"-begin.json"),"{\"checkpoint\":"+quote(checkpoints[cp])+",\"utc\":"+quote(utc())+synchronization(cp)+",\"terminal\":\"CHECKPOINT_STARTED\"}\n")){fail("checkpoint_begin_failed");return;}
        ProcessReader r;
        auto current=acquire(r,module_base,cp,true,[&]{return GetTickCount64()-began>1000;});
        const auto& picked=current.selection;
        if(!current.ok){issue(current.reason,cp,picked,0,began);return;}
        const auto& player_before=current.context.player;
        auto world=current.context.world,persistent=current.context.persistent;
        std::string error;
        std::ostringstream refs;refs<<'[';unsigned order=0,calls=0;
        for(std::size_t i=0;i<picked.selected.size();i++) {
            auto item=picked.selected[i];std::string workshop,location,worldspace;
            if(!query(r,item,cp,++order,"GetWorkshop",0x02073cf0,workshop,current,calls,began))return;
            if(!query(r,item,cp,++order,"GetCurrentLocation",0x0208b8f0,location,current,calls,began))return;
            if(!query(r,item,cp,++order,"GetWorldSpace",0x0208b9e0,worldspace,current,calls,began))return;
            if(!live_gate(r,current,cp,calls,began))return;
            Identity repeat{};if(!identity(r,item.pointer,repeat,&error)){issue(error,cp,picked,calls,began,",\"observed_identity\":"+copied_identity(repeat));return;}
            if(repeat!=item){issue("reference_changed_during_queries",cp,picked,calls,began,",\"observed_identity\":"+copied_identity(repeat));return;}
            if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,picked,calls,began);return;}
            if(i)refs<<',';
            refs<<"{\"role\":"<<quote(item.base_id==beacon_base?"beacon":"storage")<<",\"snapshot\":"<<identity_json(r,item)
                <<",\"GetWorkshop\":"<<workshop<<",\"GetCurrentLocation\":"<<location<<",\"GetWorldSpace\":"<<worldspace<<'}';
        }
        refs<<']';
        std::string data="{\"schema\":\"SOR-EXP-0002-native-v1\",\"kind\":\"RUNTIME\",\"checkpoint\":"+quote(checkpoints[cp])+
            ",\"utc\":"+quote(utc())+",\"local_timezone\":\"Australia/Sydney\",\"environment\":\"SOR-ENV-0002\",\"game_version\":\"1.16.244.0\",\"executable_sha256\":"+quote(expected_game)+
            ",\"module_base\":"+quote(hex(module_base))+",\"sfse_reported_version\":"+std::to_string(reported_sfse_version)+",\"observer_sha256\":"+quote(observer_hash)+",\"module_profile_sha256\":"+quote(profile_hash)+
            ",\"thread_id\":"+std::to_string(GetCurrentThreadId())+synchronization(cp)+",\"elapsed_session_ms\":"+std::to_string(GetTickCount64()-session_start)+
            ",\"capture_ms\":"+std::to_string(GetTickCount64()-began)+",\"game_time\":null,\"player\":"+identity_json(r,player_before)+",\"worldspace\":"+form(r,world)+
            ",\"persistent_cell_candidate\":"+form(r,persistent)+",\"scanned_entries\":"+std::to_string(picked.scanned)+",\"references\":"+refs.str()+
            ",\"snapshot_atomic\":false,\"terminal\":\"CHECKPOINT_COMPLETE\"}\n";
        if(data.find("READ_FAILED")!=std::string::npos){fail("final_snapshot_read_failed");return;}
        if(!live_gate(r,current,cp,calls,began))return;
        if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,picked,calls,began);return;}
        if(!evidence(session/(std::string(checkpoints[cp])+".json"),data)){fail("checkpoint_flush_failed");return;}
        advance(cp,false);
    }
};

class Diagnostic final:public SFSETaskInterface::ITaskDelegate {
public:
    void Destroy()override{delete this;}
    void Run()override {
        try {capture();}catch(const std::exception&){fail("diagnostic_cpp_failure");}
        busy=false;
    }
    void capture() {
        constexpr auto cp=checkpoints.size();
        if(!disk_guard())return;
        if(GetTickCount64()-session_start>session_ms){fail("session_deadline");return;}
        auto began=GetTickCount64();
        ProcessReader r;
        if(!sites_match()){fail("loaded_site_mismatch");return;}
        auto current=acquire(r,module_base,5,true,[&]{return GetTickCount64()-began>1000;});
        const auto& selected=current.selection;
        if(!current.ok){issue(current.reason,cp,selected,0,began);return;}
        auto item=selected.selected[1];
        if(!live_gate(r,current,cp,0,began))return;
        auto input=form(r,item.pointer);
        if(input.find("READ_FAILED")!=std::string::npos){fail("diagnostic_input_read_failed");return;}
        auto begin="{\"kind\":\"RUNTIME\",\"query\":\"GetWorkshop\",\"checkpoint\":\"TRACE\",\"input\":"+input+",\"utc\":"+quote(utc())+synchronization(cp);
        if(!evidence(session/L"TRACE-begin.json",begin+",\"terminal\":\"INVOCATION_STARTED\"}\n")){fail("diagnostic_begin_failed");return;}
        if(!disk_guard()||!live_gate(r,current,cp,0,began))return;
        if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,selected,0,began);return;}
        using Callback=std::uint64_t(*)(std::uint64_t,std::uint64_t,std::uint64_t,std::uint64_t);
        auto result=reinterpret_cast<Callback>(module_base+0x2073cf0)(0,0,item.pointer,0);
        auto returned=form(r,result);
        if(!evidence(session/L"TRACE.json",begin+",\"return_utc\":"+quote(utc())+",\"result\":"+returned+",\"terminal\":\"INVOCATION_RETURNED\"}\n")){fail("diagnostic_return_failed");return;}
        if(returned.find("READ_FAILED")!=std::string::npos){fail("diagnostic_result_read_failed");return;}
        if(!live_gate(r,current,cp,1,began))return;
        if(GetTickCount64()-began>2000){issue("checkpoint_time_budget_after_query",cp,selected,1,began);return;}
        advance(cp,false);
    }
};

DWORD run_worker() {
    if(!disk_guard())return 0;
    if(!initialization.worker_ready([] {
        std::string ready="{\"schema\":\"SOR-EXP-0002-ready-v1\",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"utc\":"+quote(utc())+",\"observer_sha256\":"+quote(observer_hash)+",\"module_base\":"+quote(hex(module_base))+",\"terminal\":\"READY\"}\n";
        return publish_ready(session,ready,[](const fs::path& p,const std::string& s){return evidence(p,s);});
    },initialization_failure))return 0;
    while(!stopped && GetTickCount64()-session_start<session_ms) {
        if(!disk_guard())break;
        auto cp=next_checkpoint.load();
        if(cp>=checkpoints.size()) {
            std::error_code error;
            if(!busy && !diagnostic_consumed && fs::exists(session/L"request-TRACE.txt",error)) {
                std::string request,permit;
                if(had_anomalies || !read_small(session/L"request-TRACE.txt",request,64)||request!="TRACE\nSETTLED\n" ||
                    !read_small(session/L"permit-TRACE.txt",permit,64)||permit!="SOR-EXP-0002 separate diagnostic approval\n") {fail("diagnostic_permission_marker_missing");break;}
                auto task=new(std::nothrow) Diagnostic;if(!task){fail("diagnostic_allocation_failed");break;}busy=true;tasks->AddTask(task);
            }
            if(error){fail("diagnostic_request_error");break;}
            Sleep(250);continue;
        }
        if(!busy) {
            auto request=session/(std::string("request-")+checkpoints[cp]+".txt");
            std::error_code error;
            if(fs::exists(request,error)) {
                std::string bytes;
                if(!read_small(request,bytes,64)||!request_matches(bytes,cp)){fail("invalid_checkpoint_request");break;}
                auto task=new(std::nothrow) Capture(cp);if(!task){fail("task_allocation_failed");break;}
                busy=true;tasks->AddTask(task);
            }
            if(error){fail("request_path_error");break;}
        }
        Sleep(250); // control-file polling only; no world/reference polling
    }
    if(!stopped && !checkpoints_complete)fail("session_deadline");stopped=true;return 0;
}
DWORD WINAPI worker(void*) {
    try {return run_worker();}catch(const std::exception&){initialization_failure("worker_cpp_failure");return 0;}
}
void message(SFSEMessagingInterface::Message* m) {
    if(!m)return;
    if(m->type==SFSEMessagingInterface::kMessage_PreLoadGame){load_telemetry.before();}
    if(m->type==SFSEMessagingInterface::kMessage_PostLoadGame){load_telemetry.after();}
}
}

extern "C" __declspec(dllexport) SFSEPluginVersionData SFSEPlugin_Version={
    SFSEPluginVersionData::kVersion,1,"SOR EXP0002 Observer","Starfield Outpost Systems Research",0,0,{sor::game_version,0},0,0,0
};
extern "C" __declspec(dllexport) bool SFSEPlugin_Load(const SFSEInterface* sfse) {
    if(!sfse || sfse->runtimeVersion!=sor::game_version || sfse->interfaceVersion!=1)return false;
    try {
        using namespace sor;
        wchar_t exe[32768]{},self[32768]{};HMODULE dll{};
        if(!GetModuleFileNameW(nullptr,exe,32768)||sha_file(exe)!=expected_game)return false;
        auto sfse_module=GetModuleHandleW(L"sfse_1_16_244.dll");wchar_t sfse_path[32768]{};
        if(!sfse_module || !GetModuleFileNameW(sfse_module,sfse_path,32768) || sha_file(sfse_path)!="28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b")return false;
        reported_sfse_version=sfse->sfseVersion;
        module_base=reinterpret_cast<std::uint64_t>(GetModuleHandleW(nullptr));
        if(!sites_match())return false;
        if(!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,reinterpret_cast<LPCWSTR>(&SFSEPlugin_Load),&dll)
            || !GetModuleFileNameW(dll,self,32768))return false;
        plugin_path=self;observer_hash=sha_file(plugin_path);
        auto config=plugin_path;config.replace_extension(L"config");std::string bytes;
        if(!read_small(config,bytes)||bytes.empty()||bytes.back()!='\n')return false;
        bytes.pop_back();fs::path root(std::u8string(reinterpret_cast<const char8_t*>(bytes.data()),bytes.size()));
        if(!allowed_root(root))return false;
        tasks=static_cast<SFSETaskInterface*>(sfse->QueryInterface(kInterface_Task));
        auto messaging=static_cast<SFSEMessagingInterface*>(sfse->QueryInterface(kInterface_Messaging));
        if(!tasks || tasks->interfaceVersion!=1 || !tasks->AddTask || !messaging || messaging->interfaceVersion!=1 || !messaging->RegisterListener)return false;
        auto handle=sfse->GetPluginHandle();
        fs::create_directories(root);session=root/("session-"+std::to_string(GetCurrentProcessId())+"-"+std::to_string(GetTickCount64()));
        if(!fs::create_directory(session))return false;
        session_created=true;
        if(!disk_guard())return false;
        session_start=GetTickCount64();
        // Snapshot is explicitly startup-time, not a resolved ESM load order.
        std::ostringstream profile;profile<<"{\"scope\":\"native_modules_at_observer_load\",\"modules\":[";
        HANDLE snapshot=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());
        if(snapshot==INVALID_HANDLE_VALUE){initialization_failure("module_snapshot_failed");return false;}
        struct SnapshotGuard {HANDLE handle;~SnapshotGuard(){CloseHandle(handle);}} snapshot_guard{snapshot};
        MODULEENTRY32W entry{};entry.dwSize=sizeof entry;bool first=true;unsigned count=0;
        if(!Module32FirstW(snapshot,&entry)){initialization_failure("module_enumeration_failed");return false;}
        do {
            if(!first)profile<<',';first=false;
            auto path=fs::path(entry.szExePath);
            profile<<"{\"name\":"<<quote(path.filename().string())<<",\"base\":"<<quote(hex(reinterpret_cast<std::uint64_t>(entry.modBaseAddr)))<<",\"size\":"<<entry.modBaseSize<<'}';
            ++count;
        }while(count<256 && Module32NextW(snapshot,&entry));
        if(count<256&&GetLastError()!=ERROR_NO_MORE_FILES){initialization_failure("module_enumeration_failed");return false;}
        profile<<"],\"count\":"<<count<<",\"possibly_truncated\":"<<(count==256?"true":"false")<<"}\n";
        profile_hash=sha_bytes(profile.str().data(),profile.str().size());
        if(profile_hash.empty()){initialization_failure("module_profile_hash_failed");return false;}
        if(!evidence(session/L"modules.json",profile.str())){initialization_failure("module_profile_write_failed");return false;}
        return initialization.start([&]{return messaging->RegisterListener(handle,"SFSE",message);},[]{
            auto thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);
            if(!thread)return false;CloseHandle(thread);return true;
        },initialization_failure);
    }catch(const std::exception&){initialization_failure("initialization_cpp_failure");return initialization.listener_registered;}
}
