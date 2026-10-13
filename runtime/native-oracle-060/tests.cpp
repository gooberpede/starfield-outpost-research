// SPDX-License-Identifier: GPL-3.0-or-later
// Original disposable process only; no retail code executes. Output directories
// are new ignored paths. Uses own Win32 memory, files and fixture instructions.
#include "modules.h"
#include <thread>
#include <iostream>
#include <stdexcept>
#include <chrono>
using namespace history;
extern "C" uint64_t fixture_call(uint64_t,uint64_t,uint64_t,uint64_t);
extern "C" unsigned char fixture_call_site[];
extern "C" uint32_t abi_probe(Four,uint64_t,uint64_t);
void check(bool ok,const char* msg){if(!ok)throw std::runtime_error(msg);std::cout<<"PASS "<<msg<<"\n";}
template<class T>void put(unsigned char* p,size_t off,T v){memcpy(p+off,&v,sizeof v);}
struct Reference {
    alignas(16) unsigned char bytes[0xd8]{},base[0x30]{},list[0x18]{},extra[0xa0]{},cell[0x118]{},world[0x180]{};
    Reference(uint64_t id=0){put(bytes,0x98,reinterpret_cast<uint64_t>(base));put(bytes,0xc8,reinterpret_cast<uint64_t>(list));put(bytes,0xb0,reinterpret_cast<uint64_t>(cell));put(cell,0x110,reinterpret_cast<uint64_t>(world));put(list,8,reinterpret_cast<uint64_t>(extra));extra[0x12]=0xbc;put(extra,0x98,id);put(base,0x28,uint32_t(0x2c60e9));}
    uint64_t ptr(){return reinterpret_cast<uint64_t>(bytes);}void xyz(float x,float y,float z){float v[]{x,y,z};memcpy(bytes+0x8c,v,12);}
};
extern "C" uint64_t fixture_writer(uint64_t a,uint64_t b,uint64_t c,uint64_t d){
    auto* p=reinterpret_cast<unsigned char*>(a);memcpy(p+0x8c,reinterpret_cast<void*>(b),12);if(c==0x1122334455667788ULL&&d==0x8877665544332211ULL)return 0xabcdef9876543210ULL;return 17;
}
uint64_t writer_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return invoke<0x5a14da,restoration>(fixture_writer,a,b,c,d);}
uint64_t add_writer(uint64_t a,uint64_t b,uint64_t,uint64_t){auto* p=reinterpret_cast<float*>(a+0x8c);auto* v=reinterpret_cast<float*>(b);for(unsigned i=0;i<3;++i)p[i]+=v[i];return 23;}
uint64_t add_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return invoke<0xb7351a,apply>(add_writer,a,b,c,d);}
uint64_t convert_writer(uint64_t a,uint64_t b,uint64_t c,uint64_t d){auto* p=reinterpret_cast<unsigned char*>(a);if(((p[0xd3]>>1)&1)!=(c&0xff)){float v[4]{};memcpy(v,reinterpret_cast<void*>(b),12);put(reinterpret_cast<unsigned char*>(v),12,uint32_t(((c&0xff)^1)+1));add_hook(a,reinterpret_cast<uint64_t>(v),c,d);p[0xd3]=(p[0xd3]&0xfd)|static_cast<unsigned char>(c*2);}return 29;}
uint64_t convert_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return invoke<0x4b967b0,convert>(convert_writer,a,b,c,d);}
uint64_t center_writer(uint64_t a,uint64_t b,uint64_t,uint64_t){auto* out=reinterpret_cast<float*>(b);auto* xyz=reinterpret_cast<float*>(a+0x8c);Blob ref;copy(ref,a,0xd8);auto extra=pointer(field<uint64_t>(ref,0xc8)+8);for(unsigned i=0;i<3;++i){float v{};memcpy(&v,reinterpret_cast<void*>(extra+0x60+i*4),4);out[i]=xyz[i]+v;}return b;}
uint64_t center_hook(uint64_t a,uint64_t b,uint64_t c,uint64_t d){return invoke<0xad0c36,center>(center_writer,a,b,c,d);}
uint64_t fault(uint64_t,uint64_t,uint64_t,uint64_t){RaiseException(0xe0123456,0,0,nullptr);return 0;}
void invoke_fault(){__try{invoke<123,replace>(fault,0,0,0,0);}__except(GetExceptionCode()==0xe0123456?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){}}
void open_case(const fs::path& root,const char* name){spool.close();spool.attempted=0;spool.captured=0;spool.durable=0;spool.failed=0;spool.active=0;spool.next_invocation=0;spool.offset=0;spool.fail_sequence=0;spool.stopping=false;spool.broken=false;auto p=root/name;fs::create_directory(p);check(spool.open(p),name);}
void finish_case(){spool.stop();spool.flush();check(spool.active==0,"no active invocations");check(write_new(spool.root/L"terminal.json","{"+spool.counts()+"}\n"),"terminal receipt");spool.close();}
int main(int argc,char** argv){
    try{
        if(argc<2)return 2;fs::path root=argv[1];if(argc==3&&std::string(argv[2])=="crash"){fs::create_directories(root);open_case(root,"crash");Reference r;float v[]{1,2,3};writer_hook(r.ptr(),reinterpret_cast<uint64_t>(v),0,0);spool.flush();TerminateProcess(GetCurrentProcess(),73);}
        fs::create_directory(root);check(disk(),"both 40GB guards");
        open_case(root,"normal");Reference r(0);r.xyz(1,2,3);float v[]{4,-5,6};
        Edit edit;check(call_edit(edit,reinterpret_cast<uint64_t>(fixture_call_site),reinterpret_cast<uint64_t>(&writer_hook)),"fixture rel32 range");memcpy(edit.before,fixture_call_site,5);bool dirty{};check(install(&edit,1,true,dirty),"complete CALL replacement");
        check(fixture_call(r.ptr(),reinterpret_cast<uint64_t>(v),0x1122334455667788ULL,0x8877665544332211ULL)==0xabcdef9876543210ULL,"all integer arguments and return");
        check(!memcmp(r.bytes+0x8c,v,12),"replacement all XYZ bytes");check(abi_probe(writer_hook,r.ptr(),reinterpret_cast<uint64_t>(v))==0,"nonvolatile GPR and XMM preservation");
        auto csr=_mm_getcsr();auto mode=(csr&~0x6000)|0x4000;_mm_setcsr(mode);SetLastError(12345);writer_hook(r.ptr(),reinterpret_cast<uint64_t>(v),0,0);check(_mm_getcsr()==mode&&GetLastError()==12345,"FP control and LastError");_mm_setcsr(csr);
        check(write(edit,false)&&!memcmp(fixture_call_site,edit.before,5),"original CALL restored byte exact");edit.before[0]^=1;dirty=false;check(!install(&edit,1,true,dirty)&&!dirty,"guard mismatch no mutation");
        auto admission_case=root/L"admission-stop";fs::create_directory(admission_case);check(write_new(admission_case/L"operator-stop.flag","STOP"),"preallocated startup STOP fixture");bool refused=false;try{await_admission(admission_case,"{\"fixture\":true");}catch(const std::exception& e){refused=std::string(e.what())=="operator_STOP_before_admission";}check(refused,"startup STOP before hook transaction");
        // Scientific ID convention is raw-byte hex, not uint64 numeric spelling.
        put(r.extra,0x98,uint64_t(0x4517173ee47d51f1));convert_hook(r.ptr(),reinterpret_cast<uint64_t>(v),1,0);float expected[]{8,-10,12};check(!memcmp(r.bytes+0x8c,expected,12)&&r.bytes[0xd3]==2,"nested conversion XYZ and d3");
        float compensation[]{1.25f,-2.5f,0.75f};memcpy(r.extra+0x60,compensation,12);float center_expected[]{9.25f,-12.5f,12.75f};
        float output[3]{};center_hook(r.ptr(),reinterpret_cast<uint64_t>(output),0,0);check(!memcmp(output,center_expected,12),"nonzero signed center compensation XYZ");
        convert_hook(r.ptr(),reinterpret_cast<uint64_t>(v),1,0);check(!memcmp(r.bytes+0x8c,expected,12),"same-flag conversion leaves sample unchanged");
        // A changed nonzero durable identity at the same pointer must split an
        // association, never append old writes to the new identity.
        put(r.extra,0x98,uint64_t(0x9b7b4cee66a0fc0e));writer_hook(r.ptr(),reinterpret_cast<uint64_t>(v),0,0);
        invoke_fault();check(spool.active==0&&current==nullptr,"unwind preserved and scope paired");
        {Scope a(1,producer,r.ptr(),0,reinterpret_cast<uint64_t>(v),0);{Scope b(2,enqueue,0,r.ptr(),0,reinterpret_cast<uint64_t>(v));unsigned char command[0x30]{};Scope alloc(3,allocation,0,0,0,0);alloc.finish(false,reinterpret_cast<uint64_t>(command));put(command,0x20,r.ptr());put(command,0x28,uint64_t(111));memcpy(command+0x10,v,12);
            std::thread application_thread([&]{Scope app(4,application,r.ptr(),111,reinterpret_cast<uint64_t>(command+0x10),0);app.finish(false,0);});application_thread.join();b.finish(false,0);a.finish(false,0);
        }}
        finish_case();
        open_case(root,"high-rate");auto started=GetTickCount64();std::vector<std::thread> threads;
        for(unsigned t=0;t<8;++t)threads.emplace_back([]{Reference ref;float xyz[]{1,2,3};for(unsigned i=0;i<1000;++i)writer_hook(ref.ptr(),reinterpret_cast<uint64_t>(xyz),0,0);});
        for(auto& t:threads)t.join();check(spool.attempted==16000&&spool.captured==16000&&spool.failed==0,"16000 concurrent records zero silent loss");std::cout<<"MEASURE high_rate_ms "<<GetTickCount64()-started<<"\n";finish_case();
        open_case(root,"stop-pending");{Scope s(1,replace,r.ptr(),reinterpret_cast<uint64_t>(v),0,0);spool.stop();{Scope denied(2,replace,0,0,0,0);check(!denied.entered,"STOP refuses new invocation");}check(spool.active==1,"STOP retains pending lease");s.finish(false,0);}check(spool.captured==2,"pending after record flushed after STOP");finish_case();
        open_case(root,"invalid");{Scope s(1,replace,1,2,3,4);s.finish(false,0);}check(!spool.broken&&spool.captured==2,"invalid optional memory continues capture");finish_case();
        open_case(root,"writer-failure");CloseHandle(spool.raw);spool.raw=INVALID_HANDLE_VALUE;{Scope s(1,replace,0,0,0,0);s.finish(false,0);}check(spool.broken&&spool.failed==2&&spool.durable==0,"genuine write failure counted and stops admission");finish_case();
        open_case(root,"journal-failure");CloseHandle(spool.journal);spool.journal=INVALID_HANDLE_VALUE;{Scope s(1,replace,0,0,0,0);s.finish(false,0);}check(spool.broken&&spool.durable==0&&fs::file_size(spool.root/L"events.bin")==sizeof(Event),"raw flush before journal failure recoverable tail");finish_case();
        wchar_t self[32768]{};GetModuleFileNameW(nullptr,self,32768);auto command=L"\""+std::wstring(self)+L"\" \""+(root/L"crash-child").wstring()+L"\" crash";STARTUPINFOW si{};si.cb=sizeof si;PROCESS_INFORMATION pi{};check(CreateProcessW(nullptr,command.data(),nullptr,nullptr,false,CREATE_NO_WINDOW,nullptr,nullptr,&si,&pi)!=0,"crash child started");WaitForSingleObject(pi.hProcess,INFINITE);DWORD exit{};GetExitCodeProcess(pi.hProcess,&exit);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);check(exit==73,"crash after flush original fixture only");
        check(!module_inventory().empty(),"actual disposable module inventory");std::cout<<"ALL PASS\n";return 0;
    }catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
