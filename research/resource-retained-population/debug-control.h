// SPDX-License-Identifier: GPL-3.0-or-later
// D5M control evidence is independent of scientific samples and flushed before
// each continuation. Borrowed event handles never enter the owning registry.
#include <set>
static HANDLE control_file=INVALID_HANDLE_VALUE;
static uint64_t control_sequence=0,control_event_sequence=0,control_creation=0,control_lifetime=0;
static DWORD control_step=0;
static int control_site=-1;
static std::set<HANDLE> owned_handles;
static bool inject_continue=false,inject_close=false;
static std::string control_buffer;
static std::string inject_diagnostic_action;
static void adopt_owned(HANDLE h){
    try{if(!owned_handles.insert(h).second)throw std::runtime_error("duplicate ownership");}
    catch(...){CloseHandle(h);throw;}
}
static void diagnostic(const char* action,const std::string& fields=""){
    if(control_file==INVALID_HANDLE_VALUE)throw std::runtime_error("control journal unavailable");
    if(inject_diagnostic_action==action){inject_diagnostic_action.clear();throw std::runtime_error("injected diagnostic transition failure");}
    std::ostringstream s;s<<"{\"sequence\":"<<++control_sequence<<",\"action\":\""<<action
        <<"\",\"pid\":"<<pending.dwProcessId<<",\"tid\":"<<pending.dwThreadId
        <<",\"debug_event_sequence\":"<<control_event_sequence<<",\"process_creation\":"<<control_creation<<",\"thread_lifetime\":"<<control_lifetime
        <<",\"event\":"<<pending.dwDebugEventCode<<",\"step_tid\":"<<control_step<<",\"step_site\":"<<control_site
        <<",\"terminal\":"<<(terminal?"true":"false");
    if(pending.dwDebugEventCode==EXCEPTION_DEBUG_EVENT)s<<",\"exception_code\":"<<pending.u.Exception.ExceptionRecord.ExceptionCode
        <<",\"exception_address\":"<<reinterpret_cast<uint64_t>(pending.u.Exception.ExceptionRecord.ExceptionAddress)
        <<",\"first_chance\":"<<pending.u.Exception.dwFirstChance;
    s<<fields<<"}\n";control_buffer+=s.str();
    // Batch transitions while Windows holds the pending debug event. The full
    // batch must reach disk before continuation; the result is flushed too.
    // This bounds volatile diagnostic state without a scientific event quota.
    if(control_buffer.size()>1024*1024)throw std::runtime_error("control buffer integrity bound");
    std::string name=action;
    if(name=="CONTINUE_INTENT"||name=="CONTINUE_RESULT"||name=="CONTROLLER_FATAL"||name=="CONTROL_END"||name=="CONTROL_START"){
        DWORD wrote=0;
        if(!WriteFile(control_file,control_buffer.data(),DWORD(control_buffer.size()),&wrote,nullptr)||wrote!=control_buffer.size()||!FlushFileBuffers(control_file))
            throw std::runtime_error("durable control write failed");
        control_buffer.clear();
    }
}
static void start_control(){
    wchar_t path[32768]{};auto n=GetEnvironmentVariableW(L"SOR_D5M_CONTROL_PATH",path,32768);
    if(!n||n>=32768)throw std::runtime_error("explicit control journal path required");
    control_file=CreateFileW(path,GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);
    if(control_file==INVALID_HANDLE_VALUE)throw std::runtime_error("exclusive control journal create failed");
    diagnostic("CONTROL_START");
}
static bool d5m_continue(){
    if(!pending_owned)return true;
    diagnostic("CONTINUE_INTENT",",\"disposition\":"+std::to_string(pending_disposition));
    SetLastError(ERROR_SUCCESS);
    BOOL ok;
    if(inject_continue){inject_continue=false;ok=ContinueDebugEvent(pending.dwProcessId,pending.dwThreadId,0);}
    else ok=ContinueDebugEvent(pending.dwProcessId,pending.dwThreadId,pending_disposition);
    DWORD error=ok?ERROR_SUCCESS:GetLastError();
    if(ok)pending_owned=false;
    diagnostic("CONTINUE_RESULT",",\"ok\":"+std::string(ok?"true":"false")+",\"error\":"+std::to_string(error)+",\"disposition\":"+std::to_string(pending_disposition));
    SetLastError(error);return ok!=FALSE;
}
static HANDLE duplicate_event_handle(HANDLE borrowed,DWORD tid,const char* origin="thread_event"){
    HANDLE own=nullptr;SetLastError(0);
    BOOL ok=DuplicateHandle(GetCurrentProcess(),borrowed,GetCurrentProcess(),&own,0,FALSE,DUPLICATE_SAME_ACCESS);
    auto error=ok?0:GetLastError();
    if(ok)adopt_owned(own);
    diagnostic("DUPLICATE",",\"origin\":\""+std::string(origin)+"\",\"borrowed\":"+std::to_string(reinterpret_cast<uint64_t>(borrowed))+",\"owned\":"+std::to_string(reinterpret_cast<uint64_t>(own))+",\"target_tid\":"+std::to_string(tid)+",\"ok\":"+(ok?"true":"false")+",\"error\":"+std::to_string(error));
    if(!ok)throw std::runtime_error("event handle duplication failed");
    return own;
}
static void close_owned(HANDLE h){
    if(!owned_handles.count(h))throw std::runtime_error("lost handle ownership");
    // Invalid-handle fault injection leaves the real owned handle for cleanup.
    SetLastError(0);BOOL ok=CloseHandle(inject_close?nullptr:h);
    DWORD error=ok?0:GetLastError();inject_close=false;
    if(ok)owned_handles.erase(h);
    diagnostic("CLOSE_OWNED",",\"handle\":"+std::to_string(reinterpret_cast<uint64_t>(h))+",\"ok\":"+(ok?"true":"false")+",\"error\":"+std::to_string(error));
    if(!ok)throw std::runtime_error("owned close failed");
}
static void close_file_handle(HANDLE h){
    if(!h)return;
    // The debugger owns image/DLL file handles, unlike process/thread handles.
    // Failure-drain events arrive outside the ordinary event adoption path.
    if(!owned_handles.count(h))adopt_owned(h);
    close_owned(h);
    diagnostic("CLOSE_EVENT_FILE",",\"handle\":"+std::to_string(reinterpret_cast<uint64_t>(h)));
}
static void close_plain(HANDLE& owner,const char* origin){
    if(!owner)return;
    auto value=owner;SetLastError(0);BOOL ok=CloseHandle(value);auto error=ok?0:GetLastError();
    // Clear the owner before diagnostics or another close can throw.
    if(ok)owner=nullptr;
    diagnostic("CLOSE_PLAIN",",\"origin\":\""+std::string(origin)+"\",\"handle\":"+std::to_string(reinterpret_cast<uint64_t>(value))
        +",\"ok\":"+(ok?"true":"false")+",\"error\":"+std::to_string(error));
    if(!ok)throw std::runtime_error("plain owned close failed");
}
static void finish_control(unsigned plain_remaining=0){
    diagnostic("CONTROL_END",",\"owned_remaining\":"+std::to_string(owned_handles.size())+",\"plain_remaining\":"+std::to_string(plain_remaining));
    if(!owned_handles.empty()||plain_remaining)throw std::runtime_error("owned handles remain");
    auto h=control_file;
    if(!CloseHandle(h))throw std::runtime_error("control journal close failed");
    control_file=INVALID_HANDLE_VALUE;
}
static void ordinary_identity(HANDLE target){
    HANDLE a=nullptr,b=nullptr;
    if(!OpenProcessToken(GetCurrentProcess(),TOKEN_QUERY,&a))throw std::runtime_error("caller token query");
    if(!OpenProcessToken(target,TOKEN_QUERY,&b)){CloseHandle(a);throw std::runtime_error("target token query");}
    unsigned char aa[4096],bb[4096];DWORD n=0,m=0;TOKEN_ELEVATION ae{},be{};
    bool ok=GetTokenInformation(a,TokenUser,aa,sizeof aa,&n)&&GetTokenInformation(b,TokenUser,bb,sizeof bb,&m)
        &&EqualSid(reinterpret_cast<TOKEN_USER*>(aa)->User.Sid,reinterpret_cast<TOKEN_USER*>(bb)->User.Sid)
        &&GetTokenInformation(a,TokenElevation,&ae,sizeof ae,&n)&&GetTokenInformation(b,TokenElevation,&be,sizeof be,&m)
        &&!ae.TokenIsElevated&&!be.TokenIsElevated;
    wchar_t user[256]{};DWORD count=256;
    ok=ok&&GetUserNameW(user,&count);std::wstring name=user;std::transform(name.begin(),name.end(),name.begin(),towlower);
    ok=ok&&name.find(L"codexsandbox")==std::wstring::npos;
    DWORD caller_session=0,target_session=0;
    ok=ok&&ProcessIdToSessionId(GetCurrentProcessId(),&caller_session)&&ProcessIdToSessionId(GetProcessId(target),&target_session)&&caller_session==target_session;
    bool ca=CloseHandle(a)!=FALSE,cb=CloseHandle(b)!=FALSE;
    if(!ok||!ca||!cb)throw std::runtime_error("ordinary caller/target account mismatch; admission refused before attachment");
}
#pragma comment(lib,"advapi32.lib")
