// SPDX-License-Identifier: GPL-3.0-or-later
#include "win_support.h"
#include <iostream>
#include <map>
#include "third_party/sfse/PluginAPI.h"
#include "trace_state.h"
#include "format.h"
using namespace sor;
unsigned checks{};
void require(bool passed,const char* name){++checks;if(!passed)throw std::runtime_error(name);}
#include "initialization_tests.h"
struct Memory:Reader {
    std::map<std::uint64_t,unsigned char> data;
    template<class T>void put(std::uint64_t address,const T& value){auto p=reinterpret_cast<const unsigned char*>(&value);for(std::size_t i=0;i<sizeof value;i++)data[address+i]=p[i];}
    bool bytes(std::uint64_t p,void* out,std::size_t n)override {
        auto d=static_cast<unsigned char*>(out);for(std::size_t i=0;i<n;i++){auto found=data.find(p+i);if(found==data.end())return false;d[i]=found->second;}return true;
    }
    void ref(std::uint64_t p,std::uint32_t base_id,std::uint32_t id) {
        auto base=p+0x1000;put(p+0x24,std::uint32_t(0));put(p+0x28,id);put(p+0x2e,std::uint8_t(0x4a));
        put(p+0x80,std::array<float,3>{0,0,0});put(p+0x8c,std::array<float,3>{1,2,3});put(p+0x98,base);
        put(p+0xb0,std::uint64_t(0x10000));put(p+0xc8,std::uint64_t(0x90000));put(base+0x28,base_id);
    }
};
#include "observation_tests.h"
#include "acquisition_tests.h"
int main(int argc,char** argv) {
    try {
        require(argc==3,"arguments: fixture root and DLL");fs::path root=fs::absolute(argv[1]);fs::create_directories(root);
        initialization_tests(root);
        observation_tests(root);
        acquisition_tests(root);
        Memory m;m.put(0x1002e,std::uint8_t(0x49));m.put(0x10080,Collection{0,0,0});
        require(select(m,{0x10000},0).ok,"empty A0");require(!select(m,{0x10000},2).ok,"beacon missing");
        m.ref(0x20000,beacon_base,0xff000100);m.put(0x40000,std::uint64_t(0x20000));m.put(0x10080,Collection{1,1,0x40000});
        require(select(m,{0x10000},2).ok,"beacon only");require(!select(m,{0x10000},0).ok,"unexpected baseline beacon");
        m.ref(0x22000,storage_base,0xff000101);m.put(0x40008,std::uint64_t(0x22000));m.put(0x10080,Collection{2,2,0x40000});
        m.put(0x23024,std::uint32_t(0));m.put(0x2302e,std::uint8_t(0x1b));
        m.put(0x10024,std::uint32_t(0));m.put(0x10028,std::uint32_t(1));
        Identity fixture{};require(identity(m,0x22000,fixture),"fixture identity");
        require(write_new(root/L"native-identity.json","{\"kind\":\"SYNTHETIC\",\"snapshot\":"+identity_json(m,fixture)+",\"null_query\":"+form(m,0)+",\"failed_query\":"+form(m,0x777777)+"}\n"),"production serializer fixture");
        require(select(m,{0x10000},4).ok,"A2 selected pair");require(select(m,{0x10000},5).ok,"reload reacquisition");
        m.put(0x5002e,std::uint8_t(0x49));m.put(0x50080,Collection{2,2,0x40000});
        require(select(m,{0x10000,0x50000},4).selected.size()==2,"same references in two cells deduplicated");
        struct Changing:Memory {unsigned reads{};bool bytes(std::uint64_t p,void* out,std::size_t n)override {
            if(p==0x10080&&++reads==2)put(0x10080,Collection{1,2,0x40000});return Memory::bytes(p,out,n);
        }} changing;changing.data=m.data;
        require(!select(changing,{0x10000},4).ok,"collection change rejected");
        m.ref(0x24000,storage_base,0xff000102);m.put(0x40010,std::uint64_t(0x24000));m.put(0x10080,Collection{3,3,0x40000});
        require(!select(m,{0x10000},4).ok,"ambiguous storage rejected");m.put(0x10080,Collection{4097,4097,0x40000});
        require(!select(m,{0x10000},4).ok,"scan bound");
        m.put(0x10080,Collection{2,2,0x40000});m.put(0x2208c,std::array<float,3>{NAN,0,0});require(!select(m,{0x10000},4).ok,"NaN rejected");
        require(!select(m,{0x60000},0).ok,"unreadable cell");require(!select(m,{},0).ok,"empty scope");
        for(std::size_t i=0;i<checkpoints.size();i++){require(request_matches(std::string(checkpoints[i])+(i==5?"\nRELOADED_SETTLED\n":"\nSETTLED\n"),i),"exact request");require(!request_matches(std::string(checkpoints[i])+"\r\n",i),"invalid request");}
        require(runtime_address(0x7ff600000000,0x2073cf0,0x89c2000)==0x7ff602073cf0,"ASLR");
        require(!runtime_address(0x7ff600000001,0x2073cf0,0x89c2000),"bad base");
        TraceState trace;trace.armed=100;
        require(!trace.expired(5099)&&trace.expired(5100),"zero-hit independent deadline");
        require(!trace.tail(1000)&&!trace.returned(1008),"reject missing entry");
        require(trace.entry(1000,2000),"selected entry");
        require(!trace.entry(1000,2000),"reject recursion");
        require(!trace.tail(992)&&trace.tail(1000),"tail stack correlation");
        require(!trace.returned(1000)&&trace.returned(1008),"return stack correlation");
        trace.hits=100;require(trace.expired(101),"hit bound");
        require(sha_bytes("abc",3)=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","SHA-256 vector");
        require(!allowed_root(L"C:\\Windows\\exp0002-live"),"outside output root");
        auto test=root/L"record.json";
        require(write_new(test,"{\"kind\":\"SYNTHETIC\",\"terminal\":\"CHECKPOINT_COMPLETE\"}\n"),"write and flush");
        require(!write_new(test,"overwrite"),"overwrite rejected");require(!write_new(root/L"oversize.json",std::string(32769,'x')),"bounded output");
        std::string content;require(read_small(test,content),"flushed record readback");require(content.find("CHECKPOINT_COMPLETE")!=std::string::npos,"terminal preserved");
        auto dll=LoadLibraryW(fs::absolute(argv[2]).c_str());require(dll!=nullptr,"load observer in fixture process");
        auto load=reinterpret_cast<bool(*)(const SFSEInterface*)>(GetProcAddress(dll,"SFSEPlugin_Load"));require(load!=nullptr,"SFSE export");
        SFSEInterface fake{};require(!load(&fake),"wrong version rejected");fake.runtimeVersion=game_version;fake.interfaceVersion=1;
        require(!load(&fake),"non-game executable hash rejected before interface use");FreeLibrary(dll);
        std::cout<<"{\"kind\":\"SYNTHETIC\",\"checks\":"<<checks<<",\"terminal\":\"TESTS_COMPLETE\"}\n";return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
