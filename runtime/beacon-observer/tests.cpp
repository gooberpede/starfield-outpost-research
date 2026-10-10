// SPDX-License-Identifier: GPL-3.0-or-later
#include "capture.h"
#include <iostream>
#include <map>
#include <thread>
#include "../exp0002/third_party/sfse/PluginAPI.h"
#include "identity.generated.h"
using namespace beacon;
void require(bool v,const char* text){if(!v)throw std::runtime_error(text);}
struct Fake:Reader{
    std::map<uint64_t,std::vector<unsigned char>> regions;
    bool bytes(uint64_t p,void* b,size_t n)override{
        for(auto& [a,data]:regions)if(p>=a && p-a<=data.size() && n<=data.size()-(p-a)){memcpy(b,data.data()+p-a,n);return true;}return false;
    }
    template<class T>void put(uint64_t p,size_t o,T v){auto& data=regions[p];if(data.size()<o+sizeof v)data.resize(o+sizeof v);memcpy(data.data()+o,&v,sizeof v);}
};
int main(int argc,char** argv){try{
    require(argc==3,"fixture output and DLL arguments");fs::path root=argv[1];require(fs::create_directory(root),"new test directory");
    HMODULE dll=LoadLibraryA(argv[2]);require(dll!=nullptr,"disposable DLL load");
    auto version=reinterpret_cast<SFSEPluginVersionData*>(GetProcAddress(dll,"SFSEPlugin_Version"));
    require(version&&version->pluginVersion==observer_version_int,"version export");
    auto load=reinterpret_cast<bool(*)(const SFSEInterface*)>(GetProcAddress(dll,"SFSEPlugin_Load"));
    require(load&&!load(nullptr),"null SFSE rejected without worker");require(FreeLibrary(dll)!=0,"test DLL unload");
    require(!range(0,1)&&!range(UINT64_MAX,8)&&!range(user_end,2)&&range(user_end,1),"pointer ranges");
    require(associated(0x400007,7,0x400000)&&!associated(0x400007,8,0x400000)&&!associated(0x600007,7,0x400000)&&!associated(0x400007,7,0x1400000),"handle generation and slot mismatch");
    require(!label_ok("../escape")&&label_ok("baseline-003")&&!label_ok("a\nb"),"request parser");
    require(floor_bytes==40000000000ULL,"decimal disk floor");
    require(space_safe(floor_bytes,floor_bytes)&&!space_safe(floor_bytes-1,floor_bytes)&&!space_safe(floor_bytes,floor_bytes-1)&&!space_safe(floor_bytes,floor_bytes,false),"threshold both volumes exact boundary");
    require(number(std::numeric_limits<float>::infinity())=="\"+Infinity\"","nonfinite JSON");
    Fake fake;uint64_t list=0x10000,node=0x11000;
    fake.regions[list].resize(0x20);fake.put(list,8,node);
    fake.regions[node].resize(0x40);fake.put(node,8,node);fake.put<uint8_t>(node,0x12,0x81);
    {Writer w(root/"cyclic",[]{return true;});Capture c(fake,w,0);c.extras("test",list);require(c.partial,"cycle classified");w.finish("CAPTURE_PARTIAL");}
    // A failed terrain component must still reach census and the durable marker.
    {Writer w(root/"missing",[]{return true;});Capture c(fake,w,0x140000000);c.run();require(c.partial,"partial failure");}
    bool reject=false;try{Writer w(root/"below-floor",[]{return false;});}catch(const std::exception&){reject=true;}require(reject&&!fs::exists(root/"below-floor"),"preflight low disk");
    int writes=0;
    try{Writer w(root/"interrupted",[&]{return ++writes<4;});w.event("{\"durable\":true}");std::vector<unsigned char> b(200000,1);w.raw("long",0x10000,b.data(),b.size(),"test");require(false,"injected write must stop");}catch(const std::exception&){}
    require(fs::exists(root/"interrupted/records.jsonl")&&!fs::exists(root/"interrupted/complete.json"),"flush recovery no false complete");
    // Disposable OS process, real ReadProcessMemory and guard-page behavior.
    ProcessReader process;auto p=VirtualAlloc(nullptr,8192,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE);require(p!=nullptr,"fixture allocation");
    memset(p,0x5a,4096);DWORD previous{};require(VirtualProtect(static_cast<char*>(p)+4096,4096,PAGE_NOACCESS,&previous)!=0,"fixture guard");
    std::vector<unsigned char> data(4096);require(process.bytes(reinterpret_cast<uint64_t>(p),data.data(),data.size())&&data[0]==0x5a,"OS readable region");
    require(!process.bytes(reinterpret_cast<uint64_t>(p)+4096,data.data(),data.size()),"OS inaccessible region");
    auto main_thread=GetCurrentThreadId();DWORD worker_thread{};std::thread t([&]{worker_thread=GetCurrentThreadId();require(process.bytes(reinterpret_cast<uint64_t>(p),data.data(),data.size()),"worker read");});t.join();require(main_thread!=worker_thread,"different actual thread");
    VirtualFree(p,0,MEM_RELEASE);require(!process.bytes(reinterpret_cast<uint64_t>(p),data.data(),data.size()),"stale allocation read");
    // Reacquisition reads the new root rather than retaining a previous address.
    fake.regions[0x20000].resize(8);fake.put<uint64_t>(0x20000,0,0x30000);
    {Writer w(root/"reacquire",[]{return true;});Capture c(fake,w,0);require(c.pointer("global",0x20000,"test")==0x30000,"initial root");fake.put<uint64_t>(0x20000,0,0x40000);require(c.pointer("global",0x20000,"test")==0x40000,"fresh root");w.finish("TEST_COMPLETE");}
    // Full stock-capacity census with two independent beacons. Missing terrain
    // and absent cells/extras must not suppress either useful reference.
    const uint64_t module=0x140000000,mgr=module+0x62d1380,pool=module+0x62d1400;
    fake.regions[mgr].resize(0x70);fake.put(mgr,0,module+0x4cb2e98);fake.put(mgr,0x50,pool);
    fake.put<uint32_t>(mgr,0x64,0x200000);fake.put<uint32_t>(mgr,0x68,0x1fffff);
    fake.regions[module+0x5e60380].resize(8);fake.put(module+0x5e60380,0,mgr);
    fake.regions[pool].resize(0x200000*16);
    for(uint32_t i:{7u,23u}){
        uint64_t ref=0x50000+uint64_t(i)*0x1000,base=0x90000;
        fake.regions[ref].resize(0xd0);fake.put<uint8_t>(ref,0x2e,0x4a);fake.put<uint32_t>(ref,0x24,0x400000|i);
        fake.put<uint32_t>(ref,0x28,0xff000000|i);fake.put(ref,0x98,base);fake.put<float>(ref,0x8c,float(i)+0.125f);
        fake.regions[base].resize(0x30);fake.put<uint32_t>(base,0x28,0x2c60e9);
        fake.put(pool,i*16,ref);fake.put<uint64_t>(pool,i*16+8,0x400000);
    }
    {Writer w(root/"full-pool",[]{return true;});Capture c(fake,w,module);c.run();require(c.partial,"missing optional terrain remains partial");require(w.bytes>32*1024*1024,"no inherited tiny evidence cap");}
    // Corrupt claimed map length is rejected before allocation or writing.
    {Writer w(root/"overflow-map",[]{return true;});Capture c(fake,w,module);c.table("map",0x10000,UINT64_MAX,24);require(c.partial,"table overflow");w.finish("CAPTURE_PARTIAL");}
    {Writer w(root/"wrong-player",[]{return true;});Capture c(fake,w,module);c.reference("player",0x57000);require(c.partial,"wrong player identity rejected");w.finish("CAPTURE_PARTIAL");}
    // A formerly valid slot is not allowed to attest a later different slot.
    fake.put<uint64_t>(pool,7*16,0xdead0000);
    {Writer w(root/"stale-slot",[]{return true;});Capture c(fake,w,module);c.reference("beacon-7",0x57000,7,0x400000);require(c.partial,"stale slot rejected");w.finish("CAPTURE_PARTIAL");}
    std::cout<<"PASS pointer bounds; handle index/generation; labels; nonfinite JSON; cyclic graph; independent missing collectors; low disk; interrupted multi-chunk output; real OS reads and guard page; worker thread; stale memory; root reacquisition\n";
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
