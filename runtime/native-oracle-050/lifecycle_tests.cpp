// SPDX-License-Identifier: GPL-3.0-or-later
// Runs the production worker in a disposable process. Copies only pinned guard
// windows into private allocations; never executes any game instruction.
#include "plugin.cpp"
#include <iostream>
#include <vector>
std::vector<unsigned char> read_all(const fs::path& path){std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("fixture read");return {std::istreambuf_iterator<char>(f),std::istreambuf_iterator<char>()};}
unsigned checks{};
void require(bool b,const char* label){if(!b)throw std::runtime_error(label);++checks;std::cout<<"PASS "<<label<<'\n';}
int main(int argc,char** argv){using namespace oracle;try{
    if(argc!=4)throw std::runtime_error("arguments: exclusive-root game-path scenario");
    session=fs::path(argv[1]);require(fs::create_directory(session),"exclusive lifecycle output");
    auto scenario=std::string(argv[3]);auto bytes=read_all(argv[2]);
    require(sha_file(argv[2])==expected_game_hash,"pinned guard input");
    // A sparse private image supplies data to the exact production verifier.
    auto dos=reinterpret_cast<const IMAGE_DOS_HEADER*>(bytes.data());
    auto nt=reinterpret_cast<const IMAGE_NT_HEADERS64*>(bytes.data()+dos->e_lfanew);
    auto image=static_cast<unsigned char*>(VirtualAlloc(nullptr,nt->OptionalHeader.SizeOfImage,MEM_RESERVE,PAGE_READWRITE));
    require(image!=nullptr,"private guard image reservation");module=reinterpret_cast<uint64_t>(image);
    SYSTEM_INFO si{};GetSystemInfo(&si);auto sections=IMAGE_FIRST_SECTION(nt);
    for(auto g:guards){auto page=g.rva&~(si.dwPageSize-1);require(VirtualAlloc(image+page,si.dwPageSize*2,MEM_COMMIT,PAGE_READWRITE)!=nullptr,"guard pages committed");
        bool found=false;for(unsigned i=0;i<nt->FileHeader.NumberOfSections;++i){auto& sec=sections[i];if(g.rva>=sec.VirtualAddress&&g.rva+32<=sec.VirtualAddress+sec.SizeOfRawData){memcpy(image+g.rva,bytes.data()+sec.PointerToRawData+g.rva-sec.VirtualAddress,32);found=true;break;}}
        require(found,"guard file extent");
    }
    uint64_t table[]{module+0x31a630,module+0xad8ec0,module+0xad8ec0};memcpy(image+0x4b916e8,table,sizeof table);
    relay_page=islands(module+0xad0c36);require(relay_page!=nullptr,"lifecycle relay allocation");
    for(unsigned i=0;i<calls;++i){island(relay_page+i*16,relay_targets[i]);require(call_edit(edits[i],module+call_sites[i].rva,reinterpret_cast<uint64_t>(relay_page+i*16)),"lifecycle rel32 range");memcpy(edits[i].before,call_sites[i].bytes,5);}
    DWORD old{};require(VirtualProtect(relay_page,4096,PAGE_EXECUTE_READ,&old)!=0&&FlushInstructionCache(GetCurrentProcess(),relay_page,4096),"lifecycle RX relays");
    for(unsigned i=calls;i<edit_count;++i){auto& e=edits[i];e.address=image+0x4b916f0+(i-calls)*8;e.size=8;auto before=module+0xad8ec0,after=reinterpret_cast<uint64_t>(&callback_hook);memcpy(e.before,&before,8);memcpy(e.after,&after,8);}
    verify_native(false);require(install(edits,edit_count,true,mutated),"production 21-edit transaction on disposable bytes");verify_native(true);
    queue=new Queue<4096>();gate.state=0;worker_tick=GetTickCount64();worker_required=true;
    LARGE_INTEGER freq{};QueryPerformanceFrequency(&freq);
    session_identity="{\"component\":\"SorNativePositionOracle\",\"version\":\"0.5.0\",\"schema\":5,\"synthetic\":true,\"event_size\":"+std::to_string(sizeof(Event))+",\"pid\":"+std::to_string(GetCurrentProcessId())+",\"process_creation_filetime\":1,\"module_base\":"+quote(hex(module))+",\"dll_sha256\":\"DISPOSABLE\",\"qpc_frequency\":"+std::to_string(freq.QuadPart);
    if(scenario=="writer-failure")require(write_new(session/L"events.bin","occupied"),"preexisting raw file forces CREATE_NEW refusal");
    if(scenario=="normal"){Event e;Scope scope{};scope.id=1;stamp(e,scope,begin);e.sequence=1;require(queue->push(e),"synthetic early-return entry enqueued");stamp(e,scope,end);e.sequence=2;require(queue->push(e),"synthetic early-return exit enqueued");entered_stages[2]=1;}
    HANDLE thread=CreateThread(nullptr,0,worker,nullptr,0,nullptr);require(thread!=nullptr,"actual production worker start");
    if(scenario!="writer-failure"){
        while(!fs::exists(session/L"ready.json")&&!fs::exists(session/L"failure.json"))Sleep(10);
        require(fs::exists(session/L"ready.json"),"production READY written");
        require(write_new(session/L"control-0123456789abcdef0123456789abcdef.request","ACK\n"),"durable no-hit challenge submitted");
        for(;;){auto h=read_all(session/L"health.jsonl");std::string text(h.begin(),h.end());if(text.find("0123456789abcdef0123456789abcdef")!=std::string::npos)break;if(fs::exists(session/L"failure.json"))throw std::runtime_error("worker failed before ACK");Sleep(10);}
        require(worker_tick.load()>0,"worker health independent of native hits");
        if(scenario=="guard-failure")edits[0].after[1]^=1;
        else require(write_new(session/L"STOP","STOP\n"),"orderly STOP submitted");
    }
    require(WaitForSingleObject(thread,30000)==WAIT_OBJECT_0,"production worker exits and joins");CloseHandle(thread);
    if(scenario=="normal"||scenario=="no-hit"){
        require(fs::exists(session/L"retired.json")&&!fs::exists(session/L"failure.json"),"orderly retirement precedes normal process return");
        require(gate.drained(),"admission fully drained");require(fs::file_size(session/L"events.bin")== (scenario=="normal"?2*sizeof(Event):0),"raw flushed exact extent");
        if(scenario=="normal"){auto raw=read_all(session/L"events.bin");auto j=read_all(session/L"records.jsonl");require(std::string(j.begin(),j.end()).find(sha_bytes(raw.data(),sizeof(Event)))!=std::string::npos,"production journal matches raw hash");}
        for(auto& e:edits)require(match(e,true),"STOP retains inert resident patches");
    }else require(fs::exists(session/L"failure.json")&&!fs::exists(session/L"retired.json")&&gate.drained(),"real writer or integrity failure reported without successful retirement");
    if(scenario=="guard-failure")edits[0].after[1]^=1;
    for(auto& e:edits)require(write(e,false)&&match(e,false),"disposable-only restoration");
    require(VirtualFree(image,0,MEM_RELEASE)&&VirtualFree(relay_page,0,MEM_RELEASE),"private fixture allocations released after worker join");
    std::cout<<"PASS lifecycle "<<scenario<<" checks="<<checks<<'\n';return 0;
}catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
