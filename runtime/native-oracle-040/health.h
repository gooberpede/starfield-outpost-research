// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "patch.h"
#include <set>
#include <cctype>
#include <algorithm>
#include <cwctype>
namespace oracle {
constexpr uint64_t heartbeat_ms=1000,health_deadline_ms=15000;
inline bool nonce_name(const std::string& name){return name.size()==48&&name.substr(0,8)=="control-"&&name.substr(40)==".request"&&std::all_of(name.begin()+8,name.begin()+40,[](unsigned char c){return std::isxdigit(c)!=0;});}
inline std::string module_inventory(){
    HANDLE h=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());
    if(h==INVALID_HANDLE_VALUE)throw std::runtime_error("modules_snapshot");
    MODULEENTRY32W e{};e.dwSize=sizeof e;std::string lines;bool ok=Module32FirstW(h,&e)!=0;
    try{if(ok){do{
        auto name=fs::path(e.szExePath);auto u=name.u8string();auto file=name.filename().wstring();std::transform(file.begin(),file.end(),file.begin(),::towlower);
        auto module_hash=sha_file(name);
        auto role=file==L"gameoverlayrenderer64.dll"||file==L"nvspcap64.dll"||file==L"nvppex.dll"?"accepted_standard_overlay":"recorded_no_blanket_allowlist";
        lines+="{\"path\":"+quote(std::string(reinterpret_cast<const char*>(u.data()),u.size()))+",\"base\":"+quote(hex(reinterpret_cast<uint64_t>(e.modBaseAddr)))+",\"size\":"+std::to_string(e.modBaseSize)+",\"sha256\":"+quote(module_hash)+",\"hash_status\":"+quote(module_hash.size()==64?"READ_OK":"UNREADABLE_ASSESS_SPECIFIC_RISK")+",\"role\":"+quote(role)+"}\n";
    }while(Module32NextW(h,&e));ok=GetLastError()==ERROR_NO_MORE_FILES;}}catch(...){CloseHandle(h);throw;}
    CloseHandle(h);if(!ok)throw std::runtime_error("modules_enumeration");return lines;
}
// Lightweight ongoing module-set observation. New/unfamiliar modules are logged,
// not blocked by name; every owned native edit remains independently guarded.
inline std::string module_set(){
    HANDLE h=CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,GetCurrentProcessId());if(h==INVALID_HANDLE_VALUE)throw std::runtime_error("modules_snapshot");
    MODULEENTRY32W e{};e.dwSize=sizeof e;std::string value;bool ok=Module32FirstW(h,&e)!=0;
    try{if(ok){do{auto u=fs::path(e.szExePath).u8string();value+=hex(reinterpret_cast<uint64_t>(e.modBaseAddr))+":"+std::to_string(e.modBaseSize)+":"+std::string(reinterpret_cast<const char*>(u.data()),u.size())+"\n";}while(Module32NextW(h,&e));ok=GetLastError()==ERROR_NO_MORE_FILES;}}catch(...){CloseHandle(h);throw;}
    CloseHandle(h);if(!ok)throw std::runtime_error("modules_enumeration");return value;
}
struct Health {
    HANDLE log=INVALID_HANDLE_VALUE;uint64_t tick{},serial{},module_serial{},flushed_events{},flushed_offset{};std::set<std::string> acknowledged;std::string modules,identity;
    void open(const fs::path& session,const std::string& id){identity=id;log=CreateFileW((session/L"health.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_FLAG_WRITE_THROUGH,nullptr);if(log==INVALID_HANDLE_VALUE)throw std::runtime_error("health_open");}
    void append_health(const std::string& nonce){
        LARGE_INTEGER q{};QueryPerformanceCounter(&q);auto line=identity+",\"health_sequence\":"+std::to_string(++serial)+",\"health_utc\":"+quote(utc())+",\"qpc\":"+std::to_string(q.QuadPart)+",\"nonce\":"+quote(nonce)+",\"flushed_events\":"+std::to_string(flushed_events)+",\"flushed_offset\":"+std::to_string(flushed_offset)+",\"queue_depth\":"+std::to_string(queue?queue->put.load()-queue->take:0)+",\"lost\":"+std::to_string(lost.load())+",\"health_timeouts\":"+std::to_string(health_timeouts.load())+",\"depth_errors\":"+std::to_string(depth_errors.load())+",\"stopping\":"+((gate.state.load()&stop_bit)?"true":"false")+",\"active\":["+std::to_string(active_stages[0].load())+","+std::to_string(active_stages[1].load())+","+std::to_string(active_stages[2].load())+"],\"entered\":["+std::to_string(entered_stages[0].load())+","+std::to_string(entered_stages[1].load())+","+std::to_string(entered_stages[2].load())+"]}\n";
        if(!durable_append(log,line.data(),line.size(),disk()))throw std::runtime_error("health_write_flush");worker_tick.store(GetTickCount64());
    }
    void poll(const fs::path& session,Edit* edits,size_t n,bool force=false){
        worker_control(session,edits,n);auto now=GetTickCount64();if(!force&&now-tick<heartbeat_ms)return;
        auto current=module_set();if(current!=modules){auto inventory=module_inventory();worker_control(session,edits,n);if(!write_new(session/("modules-"+std::to_string(++module_serial)+".jsonl"),inventory,1048576))throw std::runtime_error("modules_write");modules=current;}
        append_health("");
        for(auto& p:fs::directory_iterator(session)){auto name=p.path().filename().string();if(nonce_name(name)&&!acknowledged.count(name)){
            if(acknowledged.size()>=1024)throw std::runtime_error("control_file_excess");std::string value;if(!read_small(p.path(),value)||value!="ACK\n")throw std::runtime_error("control_payload");append_health(name.substr(8,32));acknowledged.insert(name);
        }}tick=now;
    }
    void close(){if(log!=INVALID_HANDLE_VALUE){CloseHandle(log);log=INVALID_HANDLE_VALUE;}}
};
}
