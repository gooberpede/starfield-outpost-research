// SPDX-License-Identifier: GPL-3.0-or-later
// Original external controller. Only creates its allowlisted sibling fixture.
#include "fixture.h"
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
static uint64_t reads=0, bytes=0;
static std::string fault;
static void require(bool ok,const char* why);
static std::string ascii(const wchar_t* p) {
    std::string result;
    for(;*p;++p) { require(*p>=32 && *p<=126,"ASCII argument"); result.push_back(static_cast<char>(*p)); }
    return result;
}
static void require(bool ok,const char* why) {
    if (!ok) throw std::runtime_error(std::string(why)+" win32="+std::to_string(GetLastError()));
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
    require(!b.empty() && b.size()<16*1024*1024,"image size"); return b;
}
static bool read(uint64_t address,void* dest,size_t n) {
    ++reads; if(n>65536 || bytes+n>262144 || address>UINT64_MAX-n) return false;
    bytes+=n; SIZE_T got=0;
    return ReadProcessMemory(process,reinterpret_cast<void*>(address),dest,n,&got) && got==n;
}
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
static std::string population(const Population& p,bool interrupt) {
    std::ostringstream s;
    s<<"{\"begin\":"<<p.begin<<",\"end\":"<<p.end<<",\"capacity\":"<<p.capacity;
    auto bad=[&](const char* why) { s<<",\"status\":\"INCOMPLETE\",\"reason\":\""<<why<<"\",\"members\":null}"; return s.str(); };
    if(p.begin>p.end || p.end>p.capacity || p.begin%8 || p.end%8 || p.capacity%8 ||
       (!p.begin && p.end)) return bad("range");
    uint64_t count=(p.end-p.begin)/8;
    if(count>4096 || (p.capacity-p.begin)/8>4096) return bad("budget");
    if(interrupt) return bad("injected-interrupted-copy");
    std::vector<uint64_t> pointers(count);
    if(count && !read(p.begin,pointers.data(),size_t(count)*8)) return bad("pointer-read");
    std::vector<Resource> members(count);
    for(size_t i=0;i<count;++i) {
        if(!read(pointers[i],&members[i],sizeof(Resource))) return bad("resource-read");
        if(members[i].type!=0x9f) return bad("resource-type");
    }
    s<<",\"status\":\"COMPLETE\",\"raw_pointer_bytes\":\""<<hex(pointers.data(),pointers.size()*8)<<"\",\"members\":[";
    for(size_t i=0;i<count;++i) {
        if(i) s<<',';
        s<<"{\"pointer\":"<<pointers[i]<<",\"id\":"<<members[i].id<<",\"type\":"<<members[i].type
         <<",\"raw\":\""<<hex(&members[i],sizeof(Resource))<<"\"}";
    }
    s<<"]}"; return s.str();
}
struct Thread { HANDLE handle; uint64_t lifetime,sequence=0; };
int wmain(int argc,wchar_t** argv) {
    PROCESS_INFORMATION pi{};
    try {
        require(argc==6 && std::wstring(argv[1])==L"--synthetic-only","synthetic-only required");
        std::string expected=ascii(argv[2]);
        std::wstring mode=argv[3]; fault=ascii(argv[4]);
        unsigned limit=std::stoul(argv[5]); require(limit>0 && limit<=256,"synthetic event bound");
        const std::vector<std::wstring> modes={L"good",L"zero",L"threads",L"bad-pointer",L"bad-count",L"overflow",L"budget",L"truncated",L"truncated-resource",L"crash-before",L"crash-after"};
        require(std::find(modes.begin(),modes.end(),mode)!=modes.end(),"fixture mode");
        wchar_t own[32768]; require(GetModuleFileNameW(nullptr,own,32768)>0,"self path");
        std::wstring target=own; target=target.substr(0,target.find_last_of(L"\\/")+1)+L"sor-c1c-target.exe";
        auto image=file(target); require(sha(image)==expected,"target hash allowlist");
        const char* labels[]={"sample_refresh","sample_retained","sample_decision"};
        uint32_t rvas[3]; for(int i=0;i<3;++i) rvas[i]=exported(image,labels[i]);
        std::wstring command=L"\""+target+L"\" "+mode;
        STARTUPINFOW si{}; si.cb=sizeof(si);
        require(CreateProcessW(target.c_str(),command.data(),nullptr,nullptr,FALSE,DEBUG_ONLY_THIS_PROCESS|CREATE_NO_WINDOW,nullptr,nullptr,&si,&pi),"create synthetic process");
        require(DebugSetProcessKillOnExit(TRUE),"kill-on-debugger-exit");
        std::map<DWORD,Thread> threads; uint64_t base=0,lifetimes=0,events=0,samples=0;
        bool startup=false,stopping=false; unsigned char guards[3][16]{};
        for(;;) {
            DEBUG_EVENT ev{}; require(WaitForDebugEvent(&ev,INFINITE),"wait event"); ++events;
            require(ev.dwProcessId==pi.dwProcessId,"debug PID");
            DWORD disposition=DBG_CONTINUE;
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
                    for(int i=0;i<3;++i) {
                        require(read(base+rvas[i],guards[i],16),"site read");
                        require(!memcmp(guards[i],reinterpret_cast<void*>(local+rvas[i]),16),"site instruction guard");
                    }
                    FreeLibrary(mapped);
                    std::cout<<"{\"kind\":\"SESSION\",\"pid\":"<<pi.dwProcessId<<",\"module_base\":"<<base<<",\"exe_sha256\":\""<<expected<<"\",\"sites\":[";
                    for(int i=0;i<3;++i) { if(i) std::cout<<','; std::cout<<"{\"rva\":"<<rvas[i]<<",\"bytes\":\""<<hex(guards[i],16)<<"\"}"; }
                    std::cout<<"]}"<<std::endl;
                } else thread=ev.u.CreateThread.hThread;
                CONTEXT c{}; c.ContextFlags=CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;
                require(GetThreadContext(thread,&c),"initial context");
                require(!(c.Dr7&0xffff00ff) && !(c.EFlags&0x100),"unowned debug state");
                std::cout<<"{\"kind\":\"THREAD_BEGIN\",\"tid\":"<<ev.dwThreadId<<",\"lifetime\":"<<++lifetimes<<",\"original_dr7\":"<<c.Dr7<<"}"<<std::endl;
                threads.emplace(ev.dwThreadId,Thread{thread,lifetimes});
                c.Dr0=base+rvas[0]; c.Dr1=base+rvas[1]; c.Dr2=base+rvas[2]; c.Dr7=(c.Dr7&~0xffff00ffULL)|0x15;
                c.Dr6=0; require(SetThreadContext(thread,&c),"install hardware sites");
            } else if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT) {
                if(ev.u.LoadDll.hFile) CloseHandle(ev.u.LoadDll.hFile);
            } else if(ev.dwDebugEventCode==EXIT_THREAD_DEBUG_EVENT) {
                require(threads.count(ev.dwThreadId)!=0,"thread exit lifetime");
                std::cout<<"{\"kind\":\"THREAD_END\",\"tid\":"<<ev.dwThreadId<<",\"lifetime\":"<<threads.at(ev.dwThreadId).lifetime<<"}"<<std::endl;
                threads.erase(ev.dwThreadId);
            } else if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT) {
                auto x=ev.u.Exception; auto code=x.ExceptionRecord.ExceptionCode;
                disposition=DBG_EXCEPTION_NOT_HANDLED;
                if(code==EXCEPTION_BREAKPOINT && !startup && x.dwFirstChance) { startup=true; disposition=DBG_CONTINUE; }
                else if(code==EXCEPTION_SINGLE_STEP && !stopping) {
                    require(threads.count(ev.dwThreadId)!=0,"trap thread"); auto& t=threads.at(ev.dwThreadId);
                    CONTEXT c{}; c.ContextFlags=CONTEXT_ALL; require(GetThreadContext(t.handle,&c),"trap context");
                    int slot=-1; for(int i=0;i<3;++i) if(c.Rip==base+rvas[i] && (c.Dr6&(1ULL<<i))) slot=i;
                    require(slot>=0 && (c.Dr6&15)==(1ULL<<slot) && !(c.Dr6&0x6000) &&
                        c.Dr0==base+rvas[0] && c.Dr1==base+rvas[1] && c.Dr2==base+rvas[2] && (c.Dr7&0xffff00ff)==0x15,"unowned trap");
                    auto began=GetTickCount64();
                    reads=bytes=0; unsigned char check[16];
                    require(read(c.Rip,check,16) && !memcmp(check,guards[slot],16),"hit instruction guard");
                    Evaluation e{}; bool valid=read(c.Rcx,&e,sizeof(e)) && e.magic==MAGIC;
                    require(valid,"evaluation ABI/magic");
                    uint64_t return_va=0; require(read(c.Rsp,&return_va,8),"caller return address");
                    std::ostringstream row;
                    row<<"{\"kind\":\"SAMPLE\",\"pid\":"<<ev.dwProcessId<<",\"tid\":"<<ev.dwThreadId
                       <<",\"thread_lifetime\":"<<t.lifetime<<",\"thread_sequence\":"<<++t.sequence
                       <<",\"debug_event\":"<<events<<",\"capture\":"<<++samples<<",\"native_sequence\":"<<e.sequence
                       <<",\"visit\":"<<e.visit<<",\"depth\":"<<e.depth<<",\"site\":\""<<labels[slot]<<"\",\"site_rva\":"<<rvas[slot]
                       <<",\"rip\":"<<c.Rip<<",\"rcx\":"<<c.Rcx<<",\"rsp\":"<<c.Rsp<<",\"return_va\":"<<return_va<<",\"dr6\":"<<c.Dr6<<",\"dr7\":"<<c.Dr7
                       <<",\"eflags\":"<<c.EFlags<<",\"raw_evaluation\":\""<<hex(&e,sizeof(e))<<"\",\"raw_context\":\""<<hex(&c,sizeof(c))
                       <<"\",\"selector\":"<<e.selector<<",\"produced\":"<<e.produced<<",\"result\":"<<e.result<<",\"branch\":"<<e.branch
                       <<",\"freshness\":\""<<(slot==0?"THIS_REFRESH_REPLACED":slot==1?"RETAINED_UNCHANGED_ID":"UNKNOWN")<<"\",\"populations\":{\"spatial\":"
                       <<population(e.populations[0],fault=="interrupt" && samples==1)<<",\"atmosphere\":"<<population(e.populations[1],false)<<",\"biome\":"<<population(e.populations[2],false)
                       <<"},\"read_calls\":"<<reads<<",\"read_bytes\":"<<bytes<<",\"copy_ms\":"<<(GetTickCount64()-began)<<"}";
                    require(GetTickCount64()-began<=2000 && row.str().size()<=1024*1024,"synthetic stopped-copy time/output budget");
                    std::cout<<row.str()<<std::endl;
                    std::string ack; std::getline(std::cin,ack);
                    if(ack!="ACK "+std::to_string(samples) || samples>=limit) {
                        require(TerminateProcess(process,0xc1c0),"synthetic STOP"); stopping=true;
                    } else {
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
                            after.Dr0==c.Dr0 && after.Dr1==c.Dr1 && after.Dr2==c.Dr2 && (after.Dr7&~0x400ULL)==(c.Dr7&~0x400ULL),"unintended CPU state change");
                        std::cout<<"{\"kind\":\"RESUME_VERIFIED\",\"capture\":"<<samples
                            <<",\"flags_requested\":"<<c.EFlags<<",\"flags_readback\":"<<after.EFlags
                            <<",\"dr7_requested\":"<<c.Dr7<<",\"dr7_readback\":"<<after.Dr7<<"}"<<std::endl;
                    }
                    disposition=DBG_CONTINUE;
                } else {
                    std::cout<<"{\"kind\":\"EXCEPTION\",\"code\":"<<code<<",\"first_chance\":"<<x.dwFirstChance<<"}"<<std::endl;
                }
            } else if(ev.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT) {
                std::cout<<"{\"kind\":\"EXIT\",\"code\":"<<ev.u.ExitProcess.dwExitCode<<",\"captures\":"<<samples<<",\"stopped\":"<<(stopping?"true":"false")<<"}"<<std::endl;
                require(ContinueDebugEvent(ev.dwProcessId,ev.dwThreadId,DBG_CONTINUE),"continue exit"); break;
            }
            require(ContinueDebugEvent(ev.dwProcessId,ev.dwThreadId,disposition),"continue event");
        }
        CloseHandle(pi.hThread); CloseHandle(pi.hProcess); return 0;
    } catch(const std::exception& e) {
        std::cerr<<e.what()<<std::endl;
        if(pi.hProcess) { TerminateProcess(pi.hProcess,0xc1cf); CloseHandle(pi.hProcess); CloseHandle(pi.hThread); }
        return 2;
    }
}
