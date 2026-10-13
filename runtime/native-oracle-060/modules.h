// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "patch.h"
#include <algorithm>
#include <cwctype>
namespace history {
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
}
