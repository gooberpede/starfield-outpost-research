// SPDX-License-Identifier: GPL-3.0-or-later
// Combined D5B derivative of owned D4 producer and repaired D4B teardown.
// Exact lineage, observation limits and synthetic-only witness: sources.csv/native.md.
#include <windows.h>
#include "operands.h"
#include "../resource-tungsten-acquisition/ancestry.h"
#include "../resource-tungsten-acquisition/context.h"
#include "../resource-tungsten-acquisition/sourcefiles.h"

#include <bcrypt.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <map>
#include <string>
#include <stdexcept>
#include <algorithm>
#pragma comment(lib,"bcrypt.lib")
static HANDLE process=nullptr;
static HANDLE fixture_gate=nullptr;
static HANDLE fixture_ready=nullptr;
static bool disposal_allowed=false;
// Terminal intent is monotonic and precedes every disposal API call. A failed
// API does not reopen sampling or transfer ownership of a pending debug event.
static bool terminal=false, termination_requested=false, attached=false;
static ULONGLONG terminal_since=0;
static DEBUG_EVENT pending{};
static bool pending_owned=false;
static DWORD pending_disposition=DBG_CONTINUE;
static void commit_stop(){
    if(terminal)return;
    terminal=true;
    terminal_since=GetTickCount64();
    std::cout<<"{\"kind\":\"STOP_COMMITTED\"}"<<std::endl;
}
static bool continue_pending(){
    if(!pending_owned)return true;
    if(!ContinueDebugEvent(pending.dwProcessId,pending.dwThreadId,pending_disposition))return false;
    pending_owned=false;return true;
}
static bool terminate_once(HANDLE target,DWORD code){
    commit_stop();
    if(termination_requested)return true;
    if(!TerminateProcess(target,code))return false;
    termination_requested=true;return true;
}
static void drain_failure(HANDLE target,DWORD pid){
    commit_stop();
    bool killed=terminate_once(target,0xc1cf);
    bool continued=continue_pending(),exited=false;
    auto until=GetTickCount64()+10000;
    // Engineering recovery bound only: drain an already disposed synthetic or
    // approved target; this is not a scientific capture or operator deadline.
    while(attached&&continued&&GetTickCount64()<until){
        DEBUG_EVENT ev{};
        if(!WaitForDebugEvent(&ev,100))continue;
        pending=ev;pending_owned=true;
        pending_disposition=ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT?DBG_EXCEPTION_NOT_HANDLED:DBG_CONTINUE;
        if(ev.dwProcessId!=pid)break;
        if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT&&ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);
        if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT&&ev.u.CreateProcessInfo.hFile)CloseHandle(ev.u.CreateProcessInfo.hFile);
        exited=ev.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT;
        continued=continue_pending();
        if(exited){attached=false;break;}
    }
    std::cout<<"{\"kind\":\"FAILURE_CLEANUP\",\"termination_requested\":"<<(killed?"true":"false")
        <<",\"continued\":"<<(continued?"true":"false")<<",\"exit_observed\":"<<(exited?"true":"false")<<"}"<<std::endl;
}
static uint64_t reads=0, bytes=0;
static std::string fault;
static void require(bool ok,const char* why);
static void require(bool ok,const char* why) {
    if (!ok) throw std::runtime_error(std::string(why)+" win32="+std::to_string(GetLastError()));
}
static void disk_guard(){
    for(auto drive:{L"C:\\",L"D:\\"}){ULARGE_INTEGER available{};
        require(GetDiskFreeSpaceExW(drive,&available,nullptr,nullptr)&&available.QuadPart>=40000000000ULL,"disk guard");}
}
static std::string input_line(){
    std::string line;char ch{};DWORD got{};
    while(ReadFile(GetStdHandle(STD_INPUT_HANDLE),&ch,1,&got,nullptr)&&got){
        if(ch=='\n')return line;if(ch!='\r')line.push_back(ch);require(line.size()<=128,"control line budget");}
    return "STOP";
}
static std::string hex(const void* data,size_t size) {
    std::ostringstream s; s<<std::hex<<std::setfill('0');
    auto p=static_cast<const unsigned char*>(data);
    for(size_t i=0;i<size;++i) s<<std::setw(2)<<unsigned(p[i]);
    return s.str();
}
static std::string sha(const std::vector<char>& b) {
    BCRYPT_ALG_HANDLE a; BCRYPT_HASH_HANDLE h; unsigned char digest[32];
    require(BCryptOpenAlgorithmProvider(&a,BCRYPT_SHA256_ALGORITHM,nullptr,0)==0,"sha provider");
    require(BCryptCreateHash(a,&h,nullptr,0,nullptr,0,0)==0,"sha create");
    require(BCryptHashData(h,reinterpret_cast<PUCHAR>(const_cast<char*>(b.data())),ULONG(b.size()),0)==0,"sha data");
    require(BCryptFinishHash(h,digest,32,0)==0,"sha finish");
    BCryptDestroyHash(h); BCryptCloseAlgorithmProvider(a,0); return hex(digest,32);
}
static std::vector<char> file(const std::wstring& path) {
    std::ifstream f(path,std::ios::binary); require(bool(f),"open image");
    std::vector<char> b((std::istreambuf_iterator<char>(f)),{});
    require(!b.empty() && b.size()<256*1024*1024,"image size"); return b;
}
static bool read(uint64_t address,void* dest,size_t n) {
    ++reads; if(n>65536 || bytes+n>1048576 || !retail::range(address,n)) return false;
    bytes+=n; SIZE_T got=0;
    return ReadProcessMemory(process,reinterpret_cast<void*>(address),dest,n,&got) && got==n;
}
#ifdef RETAIL_FIXTURE
// Resolve exports from bytes of the pinned PE, never load/run the target locally.
static uint32_t exported(const std::vector<char>& b,const char* name) {
    auto span=[&](size_t at,size_t n)->const char* {
        require(at<=b.size() && n<=b.size()-at,"PE bounds"); return b.data()+at;
    };
    auto dos=reinterpret_cast<const IMAGE_DOS_HEADER*>(span(0,sizeof(IMAGE_DOS_HEADER)));
    require(dos->e_magic==IMAGE_DOS_SIGNATURE,"DOS");
    auto nt=reinterpret_cast<const IMAGE_NT_HEADERS64*>(span(dos->e_lfanew,sizeof(IMAGE_NT_HEADERS64)));
    require(nt->Signature==IMAGE_NT_SIGNATURE && nt->FileHeader.Machine==IMAGE_FILE_MACHINE_AMD64,"PE x64");
    auto sections=reinterpret_cast<const IMAGE_SECTION_HEADER*>(span(dos->e_lfanew+sizeof(IMAGE_NT_HEADERS64),nt->FileHeader.NumberOfSections*sizeof(IMAGE_SECTION_HEADER)));
    auto rva=[&](uint32_t r,size_t n)->const char* {
        for(unsigned i=0;i<nt->FileHeader.NumberOfSections;++i) {
            auto s=sections[i];
            if(r>=s.VirtualAddress && uint64_t(r)-s.VirtualAddress+n<=s.SizeOfRawData)
                return span(uint64_t(s.PointerToRawData)+r-s.VirtualAddress,n);
        } throw std::runtime_error("unmapped PE RVA");
    };
    auto exp=reinterpret_cast<const IMAGE_EXPORT_DIRECTORY*>(rva(nt->OptionalHeader.DataDirectory[0].VirtualAddress,sizeof(IMAGE_EXPORT_DIRECTORY)));
    require(exp->NumberOfNames<=128 && exp->NumberOfFunctions<=128,"export budget");
    auto names=reinterpret_cast<const DWORD*>(rva(exp->AddressOfNames,exp->NumberOfNames*4));
    auto ord=reinterpret_cast<const WORD*>(rva(exp->AddressOfNameOrdinals,exp->NumberOfNames*2));
    auto funcs=reinterpret_cast<const DWORD*>(rva(exp->AddressOfFunctions,exp->NumberOfFunctions*4));
    for(unsigned i=0;i<exp->NumberOfNames;++i) {
        auto p=rva(names[i],strlen(name)+1);
        if(!memcmp(p,name,strlen(name)+1)) {
            require(ord[i]<exp->NumberOfFunctions,"export ordinal"); return funcs[ord[i]];
        }
    } throw std::runtime_error("missing synthetic export");
}
#endif
struct Thread { HANDLE handle; uint64_t lifetime,sequence=0; uint64_t reference=0, operation=0, root=0, call_rsp=0; retail::Join gate{}; operands::State ancestry{}; ancestry::State consumer{}; unsigned stage=0; bool generation_watch=false; uint64_t provider_rsp=0,provider_token=0,next_provider=0; };
int wmain(int argc,wchar_t** argv) {
    PROCESS_INFORMATION pi{};
    try {
        disk_guard();
#ifdef RETAIL_FIXTURE
        require(argc==4 && std::wstring(argv[1])==L"--synthetic-fixture","fixture-only required");
        std::string expected;
        for(auto q=argv[2];*q;++q){require(*q>=32&&*q<=126,"hash ASCII");expected.push_back(static_cast<char>(*q));}
        wchar_t own[32768];require(GetModuleFileNameW(nullptr,own,32768)>0,"self path");
        std::wstring target=own;target=target.substr(0,target.find_last_of(L"\\/")+1)+L"sor-d5b-fixture.exe";
        auto image=file(target);require(sha(image)==expected,"fixture hash");
        const char* labels[]={"generation_entry","resource_call","selection_stage","provider_return"};
        const char* names[]={"fixture_entry","fixture_resource_call","fixture_biom","fixture_provider"};
        uint32_t rvas[4];for(int i=0;i<4;++i)rvas[i]=exported(image,names[i]);
        uint32_t provider_return=exported(image,"fixture_terminal");
        uint32_t provider_entry=exported(image,"fixture_provider");
        std::wstring gate_name=L"Local\\sor-d5b-"+std::to_wstring(GetCurrentProcessId())+L"-"+std::to_wstring(GetTickCount64());
        fixture_gate=CreateEventW(nullptr,TRUE,FALSE,gate_name.c_str());require(fixture_gate!=nullptr,"fixture gate");
        fixture_ready=CreateEventW(nullptr,TRUE,FALSE,(gate_name+L"-ready").c_str());require(fixture_ready!=nullptr,"fixture ready event");
        std::wstring command=L"\""+target+L"\" "+argv[3]+L" "+gate_name;
#else
        require(argc==3 && std::wstring(argv[1])==L"--retail-pilot", "retail-pilot PID required");
        std::string expected="7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28";
        std::wstring target=L"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Starfield\\Starfield.exe";
        auto image=file(target);require(sha(image)==expected,"pinned retail hash");
        const char* labels[]={"generation_entry","resource_call","selection_stage","provider_return"};
        uint32_t rvas[4]={0x79b520,0x79be20,0x79fb1b,0x79f860};
        std::wstring command=L"\""+target+L"\"";
        uint32_t provider_return=0x79ff1d;
        uint32_t provider_entry=0x79f860;
#endif
#ifdef RETAIL_FIXTURE
        uint32_t extra[]={exported(image,"fixture_biom"),exported(image,"fixture_query"),exported(image,"fixture_component"),exported(image,"fixture_mask_call"),exported(image,"fixture_mask_return"),exported(image,"fixture_candidate"),exported(image,"fixture_resolved")};
#else
        uint32_t extra[]={0x79fb1b,0x79feaf,0x79b6a5,0x79b8e8,0x79b8ed,0x79c642,0x79c674};
#endif
#ifdef RETAIL_FIXTURE
        uint32_t consumer_sites[]={exported(image,"con_fixture_updater_entry"),exported(image,"con_fixture_accept"),exported(image,"con_fixture_reject"),exported(image,"con_fixture_transfer")};
        uint32_t updater_return=exported(image,"con_fixture_update_return"),callback_return=exported(image,"con_fixture_callback_return");
#else
        uint32_t consumer_sites[]={0x21e07d0,0x21e1772,0x21e174e,0x21e0bf4};
        uint32_t updater_return=0x21b6936,callback_return=0x21e0a4b;
#endif
        unsigned char consumer_guards[4][16]{};
        unsigned char extra_guards[7][16]{},return_guard[16]{};
        STARTUPINFOW si{}; si.cb=sizeof(si);
        auto target_dir=target.substr(0,target.find_last_of(L"\\/"));
#ifdef RETAIL_FIXTURE
        require(CreateProcessW(target.c_str(),command.data(),nullptr,nullptr,FALSE,CREATE_NO_WINDOW,nullptr,target_dir.c_str(),&si,&pi),"create gated fixture");
        disposal_allowed=true;
        // Fixture-only startup bound: no operator input. Attach only after main
        // has completed loader/CRT initialization and reached its blocking gate.
        require(WaitForSingleObject(fixture_ready,10000)==WAIT_OBJECT_0,"fixture main readiness");
#else
        wchar_t* end=nullptr;auto requested=wcstoul(argv[2],&end,10);
        require(end&&!*end&&requested>0,"PID domain");pi.dwProcessId=requested;
        pi.hProcess=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION|PROCESS_VM_READ|PROCESS_TERMINATE,FALSE,pi.dwProcessId);
        require(pi.hProcess!=nullptr,"retail process rights");
        wchar_t actual_before[32768];DWORD actual_size=32768;
        require(QueryFullProcessImageNameW(pi.hProcess,0,actual_before,&actual_size),"pre-attach image path");
        require(!_wcsicmp(actual_before,target.c_str())&&sha(file(actual_before))==expected,"pre-attach pinned identity");
        disposal_allowed=true;
#endif
        require(DebugActiveProcess(pi.dwProcessId),"attach guarded process");
        attached=true;
        require(DebugSetProcessKillOnExit(TRUE),"kill-on-debugger-exit");
        std::map<DWORD,Thread> threads; uint64_t base=0,lifetimes=0,events=0,samples=0;
        bool startup=false;bool& stopping=terminal;bool consumer_mode=false;unsigned char guards[4][16]{};
        auto phase_change=[&](bool next,DWORD current,CONTEXT& c){
            require(next!=consumer_mode,"phase must change");consumer_mode=next;unsigned invalidated=0;
            for(auto& [id,other]:threads){
                invalidated+=unsigned(other.ancestry.stack.size()+other.consumer.stack.size());
                other.ancestry.pending={};other.ancestry.stack.clear();other.consumer.stack.clear();other.provider_token=0;other.generation_watch=false;other.stage=0;
                CONTEXT arm{};arm.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                if(id!=current)require(GetThreadContext(other.handle,&arm),"phase context");
                auto& value=id==current?c:arm;
                value.Dr0=base+(next?consumer_sites[0]:rvas[0]);value.Dr1=base+(next?consumer_sites[1]:consumer_sites[0]);
                value.Dr2=base+(next?consumer_sites[2]:extra[0]);value.Dr3=base+(next?consumer_sites[3]:provider_entry);
                value.Dr6=0;value.Dr7=(value.Dr7&~0xffff00ffULL)|0x55;
                if(id!=current){require(SetThreadContext(other.handle,&arm),"phase arm");CONTEXT v{};v.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                    require(GetThreadContext(other.handle,&v)&&v.Dr0==arm.Dr0&&v.Dr1==arm.Dr1&&v.Dr2==arm.Dr2&&v.Dr3==arm.Dr3&&(v.Dr7&0xffff00ff)==0x55,"phase readback");}
            }
            std::cout<<"{\"kind\":\"PHASE\",\"consumer_mode\":"<<(next?"true":"false")<<",\"invalidated_constructions\":"<<invalidated<<",\"link_coverage\":\"LOSS_NO_NATIVE_LIFETIME_JOIN\"}"<<std::endl;
        };
        for(;;) {
            disk_guard();
            DEBUG_EVENT ev{}; if(!WaitForDebugEvent(&ev,1000)) {
                require(GetLastError()==ERROR_SEM_TIMEOUT,"wait event");
                require(!stopping||GetTickCount64()-terminal_since<=10000,"terminal drain timeout");
                DWORD available=0;
                if(PeekNamedPipe(GetStdHandle(STD_INPUT_HANDLE),nullptr,0,nullptr,&available,nullptr)&&available){
                    std::string control=input_line();
                    require(control=="STOP","idle control");require(terminate_once(pi.hProcess,0xc1d0),"operator idle STOP");
                }
                continue;
            } ++events;
            pending=ev;pending_owned=true;pending_disposition=DBG_CONTINUE;
            require(ev.dwProcessId==pi.dwProcessId,"debug PID");
            DWORD disposition=DBG_CONTINUE;
            if(stopping&&ev.dwDebugEventCode!=EXIT_PROCESS_DEBUG_EVENT){
                // Windows can deliver queued thread/exception events after
                // TerminateProcess. Drain them without context reads or arming.
                if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT&&ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);
                if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT&&ev.u.CreateProcessInfo.hFile)CloseHandle(ev.u.CreateProcessInfo.hFile);
                if(ev.dwDebugEventCode==EXIT_THREAD_DEBUG_EVENT)threads.erase(ev.dwThreadId);
                if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT){
                    auto& x=ev.u.Exception;
                    auto address=reinterpret_cast<uint64_t>(x.ExceptionRecord.ExceptionAddress);
                    bool owned=x.ExceptionRecord.ExceptionCode==EXCEPTION_SINGLE_STEP&&threads.count(ev.dwThreadId)&&
                        ([&]{for(auto rv:rvas)if(address==base+rv)return true;for(auto rv:extra)if(address==base+rv)return true;for(auto rv:consumer_sites)if(address==base+rv)return true;return address==base+provider_return;})();
                    disposition=owned?DBG_CONTINUE:DBG_EXCEPTION_NOT_HANDLED;
                }
                std::cout<<"{\"kind\":\"TERMINAL_EVENT\",\"event\":"<<ev.dwDebugEventCode<<",\"tid\":"<<ev.dwThreadId<<"}"<<std::endl;
                pending_disposition=disposition;
                require(continue_pending(),"continue terminal event");continue;
            }
            if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT || ev.dwDebugEventCode==CREATE_THREAD_DEBUG_EVENT) {
                HANDLE thread;
                if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT) {
                    process=ev.u.CreateProcessInfo.hProcess; base=reinterpret_cast<uint64_t>(ev.u.CreateProcessInfo.lpBaseOfImage);
                    wchar_t actual[32768]; DWORD length=32768;
                    require(QueryFullProcessImageNameW(process,0,actual,&length),"process image path");
                    require(!_wcsicmp(actual,target.c_str()),"actual image identity");
                    require(sha(file(actual))==expected,"created image hash");
                    thread=ev.u.CreateProcessInfo.hThread;
                    if(ev.u.CreateProcessInfo.hFile) CloseHandle(ev.u.CreateProcessInfo.hFile);
                    // Pin instruction bytes to the same on-disk export RVA via a mapped image resource.
                    HMODULE mapped=LoadLibraryExW(target.c_str(),nullptr,LOAD_LIBRARY_AS_IMAGE_RESOURCE);
                    require(mapped!=nullptr,"image resource mapping");
                    auto local=reinterpret_cast<uint64_t>(mapped)&~uint64_t(3);
                    for(int i=0;i<4;++i) {
                        require(read(base+rvas[i],guards[i],16),"site read");
                        require(!memcmp(guards[i],reinterpret_cast<void*>(local+rvas[i]),16),"site instruction guard");
                    }
                    for(unsigned i=0;i<7;++i){
                        require(read(base+extra[i],extra_guards[i],16),"extra site read");
                        require(!memcmp(extra_guards[i],reinterpret_cast<void*>(local+extra[i]),16),"extra instruction guard");
                    }
                    require(read(base+provider_return,return_guard,16),"provider return read");
                    require(!memcmp(return_guard,reinterpret_cast<void*>(local+provider_return),16),"provider return guard");
                    for(unsigned i=0;i<4;++i){require(read(base+consumer_sites[i],consumer_guards[i],16),"consumer guard read");require(!memcmp(consumer_guards[i],reinterpret_cast<void*>(local+consumer_sites[i]),16),"consumer guard");}
                    FreeLibrary(mapped);
                    std::cout<<"{\"kind\":\"SESSION\",\"pid\":"<<pi.dwProcessId<<",\"module_base\":"<<base<<",\"exe_sha256\":\""<<expected<<"\",\"sites\":[";
                    for(int i=0;i<4;++i) { if(i) std::cout<<','; std::cout<<"{\"rva\":"<<rvas[i]<<",\"bytes\":\""<<hex(guards[i],16)<<"\"}"; }
                    std::cout<<"],\"provider_return_rva\":"<<provider_return<<",\"provider_return_guard\":\""<<hex(return_guard,16)<<"\",\"selection_sites\":[";
                    for(unsigned i=0;i<7;++i){if(i)std::cout<<',';std::cout<<"{\"rva\":"<<extra[i]<<",\"bytes\":\""<<hex(extra_guards[i],16)<<"\"}";}
                    std::cout<<"],\"consumer_sites\":[";
                    for(unsigned i=0;i<4;++i){if(i)std::cout<<',';std::cout<<"{\"rva\":"<<consumer_sites[i]<<",\"bytes\":\""<<hex(consumer_guards[i],16)<<"\"}";}
                    std::cout<<"]}"<<std::endl;
                } else thread=ev.u.CreateThread.hThread;
                CONTEXT c{}; c.ContextFlags=CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;
                require(GetThreadContext(thread,&c),"initial context");
                require(!(c.Dr7&0xffff00ff) && !(c.EFlags&0x100),"unowned debug state");
                std::cout<<"{\"kind\":\"THREAD_BEGIN\",\"tid\":"<<ev.dwThreadId<<",\"lifetime\":"<<++lifetimes<<",\"original_dr7\":"<<c.Dr7<<"}"<<std::endl;
                require(threads.size()<4096,"thread-state capacity");
                threads.emplace(ev.dwThreadId,Thread{thread,lifetimes});
                c.Dr0=base+(consumer_mode?consumer_sites[0]:rvas[0]); c.Dr1=base+(consumer_mode?consumer_sites[1]:consumer_sites[0]); c.Dr2=base+(consumer_mode?consumer_sites[2]:rvas[2]); c.Dr3=base+(consumer_mode?consumer_sites[3]:rvas[3]); c.Dr7=(c.Dr7&~0xffff00ffULL)|0x55;
                c.Dr6=0; require(SetThreadContext(thread,&c),"install hardware sites");
            } else if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT) {
                if(ev.u.LoadDll.hFile) CloseHandle(ev.u.LoadDll.hFile);
            } else if(ev.dwDebugEventCode==EXIT_THREAD_DEBUG_EVENT) {
                require(threads.count(ev.dwThreadId)!=0,"thread exit lifetime");
                std::cout<<"{\"kind\":\"THREAD_END\",\"tid\":"<<ev.dwThreadId<<",\"lifetime\":"<<threads.at(ev.dwThreadId).lifetime<<",\"unwitnessed_terminals\":"<<threads.at(ev.dwThreadId).ancestry.stack.size()<<"}"<<std::endl;
                threads.erase(ev.dwThreadId);
            } else if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT) {
                auto x=ev.u.Exception; auto code=x.ExceptionRecord.ExceptionCode;
                disposition=DBG_EXCEPTION_NOT_HANDLED;
                pending_disposition=disposition;
                if(code==EXCEPTION_BREAKPOINT && !startup && x.dwFirstChance) {
                    startup=true; disposition=DBG_CONTINUE;pending_disposition=DBG_CONTINUE;
                    // Attachment initialization can restore initial thread state
                    // after CREATE events. Reconcile slots at the all-stop startup
                    // breakpoint before releasing the cooperative test gate.
                    for(auto& [tid,t]:threads){CONTEXT arm{};arm.ContextFlags=CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;
                        require(GetThreadContext(t.handle,&arm),"startup thread context");
                        auto prior=arm.Dr7;
                        require(!(arm.EFlags&0x100),"startup unowned TF");
                        require(!(arm.Dr7&0xffff00ff)||((arm.Dr7&0xffff00ff)==0x55&&arm.Dr0==base+rvas[0]&&arm.Dr1==base+consumer_sites[0]&&arm.Dr2==base+rvas[2]&&arm.Dr3==base+rvas[3]),"startup unowned slots");
                        arm.Dr0=base+(consumer_mode?consumer_sites[0]:rvas[0]);arm.Dr1=base+(consumer_mode?consumer_sites[1]:consumer_sites[0]);arm.Dr2=base+(consumer_mode?consumer_sites[2]:rvas[2]);arm.Dr3=base+(consumer_mode?consumer_sites[3]:rvas[3]);arm.Dr6=0;arm.Dr7=(arm.Dr7&~0xffff00ffULL)|0x55;
                        require(SetThreadContext(t.handle,&arm),"startup arm");
                        CONTEXT verify{};verify.ContextFlags=CONTEXT_DEBUG_REGISTERS;
                        require(GetThreadContext(t.handle,&verify)&&(verify.Dr7&0xffff00ff)==0x55&&verify.Dr0==arm.Dr0&&verify.Dr1==arm.Dr1&&verify.Dr2==arm.Dr2&&verify.Dr3==arm.Dr3,"startup arm readback");
                        std::cout<<"{\"kind\":\"STARTUP_ARMED\",\"tid\":"<<tid<<",\"prior_dr7\":"<<prior<<",\"readback_dr7\":"<<verify.Dr7<<"}"<<std::endl;
                    }
                    if(fixture_gate)require(SetEvent(fixture_gate),"release fixture after attachment");
                }
                else if(code==EXCEPTION_SINGLE_STEP && !stopping) {
                    require(threads.count(ev.dwThreadId)!=0,"trap thread"); auto& t=threads.at(ev.dwThreadId);
                    CONTEXT c{}; c.ContextFlags=CONTEXT_ALL; require(GetThreadContext(t.handle,&c),"trap context");
#ifdef RETAIL_FIXTURE
                    require(std::wstring(argv[3])!=L"injected-context-failure","injected unavailable context");
#endif
                    bool observed_return=t.generation_watch;
                    uint32_t active[4]={rvas[0],t.generation_watch?rvas[1]:consumer_sites[0],extra[t.stage],observed_return?provider_return:provider_entry};
                    if(consumer_mode)std::copy(consumer_sites,consumer_sites+4,active);
                    int slot=retail::owned_slot(base,c.Rip,c.Dr6,active);
                    require(slot>=0 && (c.Dr6&15)==(1ULL<<slot) && !(c.Dr6&0x6000) &&
                        c.Dr0==base+active[0] && c.Dr1==base+active[1] && c.Dr2==base+active[2] && c.Dr3==base+active[3] && (c.Dr7&0xffff00ff)==0x55,"unowned trap");
#ifdef RETAIL_FIXTURE
                    if(std::wstring(argv[3])==L"guard-mismatch")(slot==2?extra_guards[t.stage]:slot==3&&observed_return?return_guard:guards[slot])[0]^=1;
#endif
                    bool entering_consumer=!consumer_mode&&slot==1&&!t.generation_watch;
                    if(entering_consumer){phase_change(true,ev.dwThreadId,c);slot=0;std::copy(consumer_sites,consumer_sites+4,active);}
                    pending_disposition=DBG_CONTINUE;
                    auto began=GetTickCount64();
                    reads=bytes=0; unsigned char check[16];
                    require(read(c.Rip,check,16) && !memcmp(check,consumer_mode?consumer_guards[slot]:slot==2?extra_guards[t.stage]:slot==3&&observed_return?return_guard:guards[slot],16),"hit instruction guard");
                    FILETIME utc{};GetSystemTimeAsFileTime(&utc);
                    std::ostringstream row;
                    row<<"{\"kind\":\"SAMPLE\",\"pid\":"<<ev.dwProcessId<<",\"tid\":"<<ev.dwThreadId
                       <<",\"thread_lifetime\":"<<t.lifetime<<",\"thread_sequence\":"<<++t.sequence
                       <<",\"debug_event\":"<<events<<",\"capture\":"<<++samples
                       <<",\"site\":\""<<(consumer_mode?(slot==0?"updater_entry":slot==1?"region_accept":slot==2?"region_reject":"spatial_transfer_payload"):(slot==3&&!observed_return?"provider_entry":labels[slot]))<<"\",\"site_rva\":"<<active[slot]
                       <<",\"utc_filetime_100ns\":"<<((uint64_t(utc.dwHighDateTime)<<32)|utc.dwLowDateTime)
                       <<",\"rip\":"<<c.Rip<<",\"raw_context\":\""<<hex(&c,sizeof(c))
                       <<"\",\"schema\":\"sor-d5b-operands/1\",\"freshness\":\"UNKNOWN\"";
                    auto reader=[](uint64_t at,void* dest,size_t n){return read(at,dest,n);};
                    if(consumer_mode){
                    #include "consumer.inc"
                    }else{
                    #ifdef RETAIL_FIXTURE
                    auto synthetic_output=slot==3&&observed_return&&!t.ancestry.stack.empty()?t.ancestry.stack.back().output:0;
                    #endif
                    #include "../resource-selection-context/sample.inc"
                    #ifdef RETAIL_FIXTURE
                    if(synthetic_output){
                        auto witness=copy("synthetic_population_witness",synthetic_output,0x70);
                        if(witness.size()==0x70&&retail::field<uint64_t>(witness.data(),0x30)==0x4453424c49464531ULL){
                            auto region=retail::field<uint64_t>(witness.data(),0x58);
                            row<<",\"synthetic_population_geometry\":"<<ancestry::geometry(reader,region).json();
                        }
                    }
                    #endif
                    }
                    if(!consumer_mode){c.Dr1=base+(t.generation_watch?rvas[1]:consumer_sites[0]);c.Dr2=base+extra[t.stage];c.Dr3=base+(t.generation_watch?provider_return:provider_entry);}
                    row<<",\"active_updaters\":"<<[&]{size_t n=0;for(auto& [id,thread]:threads)n+=thread.consumer.stack.size();return n;}();
                    row<<",\"read_calls\":"<<reads<<",\"read_bytes\":"<<bytes
                       <<",\"copy_ms\":"<<(GetTickCount64()-began)<<"}";
                    require(row.str().size()<=1024*1024,"frame byte budget");
                    std::cout<<row.str()<<std::endl;
                    std::string ack=input_line();auto numbered="ACK "+std::to_string(samples);
                    bool accepted=ack==numbered || ack==numbered+" STOP" || ack==numbered+" CONSUMER" || ack==numbered+" PRODUCER";
                    std::cout<<"{\"kind\":\"ACK_ACCEPTED\",\"capture\":"<<samples<<",\"accepted\":"<<(accepted?"true":"false")<<"}"<<std::endl;
                    if(!accepted || ack==numbered+" STOP") {
                        require(terminate_once(process,0xc1c0),"fixture STOP");
                    } else {
                        if(ack==numbered+" CONSUMER")phase_change(true,ev.dwThreadId,c);
                        if(ack==numbered+" PRODUCER")phase_change(false,ev.dwThreadId,c);
                        // Execution breakpoints fault before execution. RF resumes this instruction once;
                        // DR slots remain armed, with no byte patch, TF dance, or manual thread suspension.
                        c.ContextFlags=CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;
                        c.Dr6&=~15ULL; c.EFlags|=0x10000;
                        require(SetThreadContext(t.handle,&c),"resume RF");
                        CONTEXT after{}; after.ContextFlags=CONTEXT_ALL;
                        require(GetThreadContext(t.handle,&after),"verify resume state");
                        require(!memcmp(&c.Rax,&after.Rax,17*sizeof(DWORD64)) &&
                            !memcmp(&c.FltSave,&after.FltSave,sizeof(c.FltSave)) && c.MxCsr==after.MxCsr &&
                            (after.EFlags&~0x10002UL)==(c.EFlags&~0x10002UL) &&
                            after.Dr0==c.Dr0 && after.Dr1==c.Dr1 && after.Dr2==c.Dr2 && after.Dr3==c.Dr3 && (after.Dr7&~0x400ULL)==(c.Dr7&~0x400ULL),"unintended CPU state change");
                        std::cout<<"{\"kind\":\"RESUME_VERIFIED\",\"capture\":"<<samples
                            <<",\"flags_requested\":"<<c.EFlags<<",\"flags_readback\":"<<after.EFlags
                            <<",\"dr7_requested\":"<<c.Dr7<<",\"dr7_readback\":"<<after.Dr7<<"}"<<std::endl;
                    }
                    disposition=DBG_CONTINUE;
                } else {
                    auto invalidated=threads.count(ev.dwThreadId)?threads.at(ev.dwThreadId).ancestry.stack.size():0;
                    if(threads.count(ev.dwThreadId)){auto& bad=threads.at(ev.dwThreadId);bad.consumer.stack.clear();bad.ancestry.stack.clear();bad.ancestry.pending={};bad.provider_rsp=bad.provider_token=0;}
                    std::cout<<"{\"kind\":\"EXCEPTION\",\"code\":"<<code<<",\"tid\":"<<ev.dwThreadId<<",\"thread_lifetime\":"<<(threads.count(ev.dwThreadId)?threads.at(ev.dwThreadId).lifetime:0)<<",\"invalidated_invocations\":"<<invalidated<<",\"first_chance\":"<<x.dwFirstChance<<"}"<<std::endl;
                }
            } else if(ev.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT) {
                std::cout<<"{\"kind\":\"EXIT\",\"code\":"<<ev.u.ExitProcess.dwExitCode<<",\"open_invocations\":"<<[&]{size_t n=0;for(auto& [id,t]:threads)n+=t.ancestry.stack.size();return n;}()<<",\"captures\":"<<samples<<",\"stopped\":"<<(stopping?"true":"false")<<"}"<<std::endl;
                commit_stop();pending_disposition=DBG_CONTINUE;require(continue_pending(),"continue exit");attached=false;break;
            }
            pending_disposition=disposition;require(continue_pending(),"continue event");
        }
        CloseHandle(pi.hThread); CloseHandle(pi.hProcess); return 0;
    } catch(const std::exception& e) {
        std::cerr<<e.what()<<std::endl;
        std::cout<<"{\"kind\":\"LOSS\",\"reason\":\"controller-fatal\",\"detail_hex\":\""<<hex(e.what(),strlen(e.what()))<<"\"}"<<std::endl;
        if(pi.hProcess) { if(disposal_allowed)drain_failure(pi.hProcess,pi.dwProcessId); CloseHandle(pi.hProcess); CloseHandle(pi.hThread); }
        return 2;
    }
}
