// SPDX-License-Identifier: GPL-3.0-or-later
// D5O coverage reads happen only inside a pending, all-stop debug event.
// A retained duplicate and verified creation time bind each admitted lifetime.
static void check_coverage(DWORD tid,const ProbeThread& peer,uint64_t address,int site,
                           const std::wstring& mode,bool& injected){
    require(pending_owned&&owned_handles.count(peer.handle),"coverage ownership/all-stop");
    auto fields=",\"peer_tid\":"+std::to_string(tid)+",\"peer_lifetime\":"+std::to_string(peer.lifetime)
        +",\"peer_birth\":"+std::to_string(peer.birth)+",\"owned_handle\":"+std::to_string(reinterpret_cast<uint64_t>(peer.handle))
        +",\"owned\":true,\"suspended\":"+(peer.suspended?"true":"false")+",\"site\":"+std::to_string(site)
        +",\"expected_dr0\":"+std::to_string(address)+",\"expected_dr7_mask\":4294910207,\"expected_dr7_value\":1";
    auto wait=WaitForSingleObject(peer.handle,0);auto wait_error=wait==WAIT_FAILED?GetLastError():0;
    diagnostic("COVERAGE_STATE",fields+",\"wait\":"+std::to_string(wait)+",\"error\":"+std::to_string(wait_error));
    require(wait==WAIT_TIMEOUT||wait==WAIT_OBJECT_0,"coverage thread state");
    if(wait==WAIT_OBJECT_0){diagnostic("COVERAGE_EXITED",fields);return;}
    require(tid==pending.dwThreadId||peer.suspended,"coverage peer fence");
    FILETIME born{},dead{},kernel{},user{};
    require(GetThreadTimes(peer.handle,&born,&dead,&kernel,&user),"coverage birth query");
    require(((uint64_t(born.dwHighDateTime)<<32)|born.dwLowDateTime)==peer.birth,"coverage birth identity");
    CONTEXT value{};value.ContextFlags=CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;
    HANDLE api_handle=peer.handle;
#ifndef D5L_RETAIL_TARGET
    if(site==7&&tid!=pending.dwThreadId&&!injected&&mode==L"coverage-api-failure"){api_handle=nullptr;injected=true;}
    if(site==7&&tid!=pending.dwThreadId&&!injected&&(mode==L"coverage-dr0-loss"||mode==L"coverage-dr7-loss"||mode==L"coverage-dr7-type-loss"||mode==L"coverage-gd-sanitized")){
        CONTEXT fault{};fault.ContextFlags=CONTEXT_DEBUG_REGISTERS;
        require(GetThreadContext(peer.handle,&fault),"fixture coverage fault read");
        if(mode==L"coverage-dr0-loss")fault.Dr0++;
        else if(mode==L"coverage-dr7-type-loss")fault.Dr7|=0x10000;
        else if(mode==L"coverage-gd-sanitized")fault.Dr7|=0x2000;
        else fault.Dr7&=~1ULL;
        BOOL set_ok=SetThreadContext(peer.handle,&fault);auto set_error=set_ok?0:GetLastError();
        diagnostic("COVERAGE_FAULT_INJECTED",fields+",\"attempted_dr0\":"+std::to_string(fault.Dr0)
            +",\"attempted_dr7\":"+std::to_string(fault.Dr7)+",\"ok\":"+(set_ok?"true":"false")+",\"error\":"+std::to_string(set_error));
        require(set_ok!=FALSE,"fixture actual coverage loss");injected=true;
    }
#endif
    const auto requested=value.ContextFlags;
    BOOL ok=GetThreadContext(api_handle,&value);
    const DWORD error=ok?0:GetLastError();
    // No API may intervene between the failed call and GetLastError.
    bool returned_fault=false;
#ifndef D5L_RETAIL_TARGET
    // Windows sanitizes GD on this host. This separate fault tests the consumer
    // of a successful API return, without claiming the target actually held GD.
    if(ok&&site==7&&tid!=pending.dwThreadId&&!injected&&mode==L"coverage-gd-return-fault"){
        value.Dr7|=0x2000;injected=true;returned_fault=true;
    }
#endif
    std::ostringstream detail;detail<<fields<<",\"api_handle\":"<<reinterpret_cast<uint64_t>(api_handle)
        <<",\"api_ok\":"<<(ok?"true":"false")<<",\"error_meaningful\":"<<(ok?"false":"true")
        <<",\"error\":"<<error<<",\"requested_flags\":"<<requested
        <<",\"synthetic_return_fault\":"<<(returned_fault?"true":"false");
    if(!ok){diagnostic("COVERAGE_READ",detail.str()+",\"failure\":\"api\"");
        throw std::runtime_error("coverage context API failure error="+std::to_string(error));}
    detail<<",\"context_flags\":"<<value.ContextFlags<<",\"dr0\":"<<value.Dr0<<",\"dr1\":"<<value.Dr1
        <<",\"dr2\":"<<value.Dr2<<",\"dr3\":"<<value.Dr3<<",\"dr6\":"<<value.Dr6<<",\"dr7\":"<<value.Dr7
        <<",\"eflags\":"<<value.EFlags<<",\"rip\":"<<value.Rip;
    const char* failure=(value.ContextFlags&requested)!=requested?"flags":value.Dr0!=address?"dr0":
        (value.Dr1||value.Dr2||value.Dr3)?"foreign_address":(value.Dr7&0x2000)?"gd":
        (value.Dr7&0xffff00ffULL)!=1?"dr7":"none";
    diagnostic("COVERAGE_READ",detail.str()+",\"failure\":\""+failure+"\"");
    require(std::string(failure)=="none","continuous hardware coverage mismatch");
}
