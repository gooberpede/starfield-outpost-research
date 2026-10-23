// SPDX-License-Identifier: GPL-3.0-or-later
#define NOMINMAX
#include <windows.h>
#include "operands.h"
#include <thread>
#include <string>
extern "C" void fixture_run(void*);
template<class T>void put(unsigned char* p,size_t at,T v){memcpy(p+at,&v,sizeof v);}
struct Packet {
    void* source;void* origin;void* descriptor;uint64_t owner;
    void* biom;void* output;void* ires;void* dnam;
    uint64_t mask;uint32_t setting;uint32_t padding;Packet* nested;
    Packet* next_resource=nullptr;uint64_t* order_list=nullptr;uint64_t order_index=0;
};
static bool crash_during=false;
extern "C" void fixture_nested(Packet* p){
    if(crash_during)RaiseException(0xe0c1f002,0,0,nullptr);
    if(p->nested)fixture_run(p->nested);
}
extern "C" void fixture_setup(Packet* p,unsigned char* s){
    put<uint8_t>(s,0x30,uint8_t(p->mask));
    put<uint32_t>(s,0x40,p->order_list?2:1);put<uint32_t>(s,0x44,p->order_list?2:1);
    put<uint64_t>(s,0x50,reinterpret_cast<uint64_t>(p->order_list?p->order_list:reinterpret_cast<uint64_t*>(&p->ires)));
    put<uint32_t>(s,0x58,0x57d4);
    put<uint64_t>(s,0x68,reinterpret_cast<uint64_t>(p->dnam));
    put<uint64_t>(s,0x80,reinterpret_cast<uint64_t>(p->biom));
    memset(s+0xe0,0,0x68);
    put<uint64_t>(s,0x180,reinterpret_cast<uint64_t>(p->origin));
    put<uint64_t>(s,0x188,reinterpret_cast<uint64_t>(p->output));
    put<uint32_t>(s,0x190,1);
    put<uint64_t>(s,0x198,reinterpret_cast<uint64_t>(p->descriptor));
    put<uint64_t>(s,0x1a0,reinterpret_cast<uint64_t>(p->source));
}
extern "C" void fixture_cell_setup(unsigned char* s,unsigned char* res,int* xy){
    // Known test constants, not a synthetic implementation of native CRC/MT.
    put<uint64_t>(s,0xa0,0x1234567800000000ULL|uint32_t(xy[0]));
    float draw=retail::field<float>(res,0x114);
    if(xy[0]==11&&draw<1)draw=10.240686416625977f;
    put<float>(s,0xa8,draw);
}
int main(int argc,char** argv){
    if(argc!=3)return 2;
    HANDLE gate=OpenEventA(SYNCHRONIZE,FALSE,argv[2]);if(!gate)return 4;
    auto name=std::string(argv[2])+"-ready";
    HANDLE ready=OpenEventA(EVENT_MODIFY_STATE,FALSE,name.c_str());
    if(!ready||!SetEvent(ready))return 7;CloseHandle(ready);
    if(WaitForSingleObject(gate,INFINITE)!=WAIT_OBJECT_0)return 5;CloseHandle(gate);
    auto base=reinterpret_cast<uint64_t>(GetModuleHandleW(nullptr));
    auto globals=static_cast<unsigned char*>(VirtualAlloc(reinterpret_cast<void*>(base+0x5e90000),0x10000,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE));
    auto mgrslot=static_cast<unsigned char*>(VirtualAlloc(reinterpret_cast<void*>(base+0x5fd0000),0x10000,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE));
    auto rng=static_cast<unsigned char*>(VirtualAlloc(reinterpret_cast<void*>(base+0x5920000),0x10000,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE));
    if(!globals||!mgrslot||!rng)return 3;
    unsigned char source[0x70]{},desc[0x18]{},alternate[0x18]{},biom[0x30]{},manager[0x200]{},ires[0x118]{},dnam[560]{};
    int origin[]={-3800,-200};unsigned char output[0x30]{};
    put<int32_t>(source,0x10,-38);put<int32_t>(source,0x14,-2);
    put<int32_t>(source,0x18,10);put<int32_t>(source,0x1c,10);
    put<int32_t>(source,0x20,2);put<int32_t>(source,0x24,2);
    put<uint32_t>(biom,0x28,1332288);
    put<uint32_t>(manager,0x80,385246);
    put<uint64_t>(mgrslot,0x9c30,reinterpret_cast<uint64_t>(manager));
    put<uint32_t>(rng,0xb00,1);put<uint32_t>(rng,0xb04,0x12345678);
    put<uint32_t>(ires,0x28,0x57d4);put<uint8_t>(ires,0x2e,0x9f);
    auto files=static_cast<unsigned char*>(VirtualAlloc(reinterpret_cast<void*>(base+0x5e80000),0x10000,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
    if(!files)return 3;
    unsigned char file[0x370]{},entry[16]{};
    uint64_t filep=reinterpret_cast<uint64_t>(file),entryp=reinterpret_cast<uint64_t>(entry);
    put<uint64_t>(file,0,base+0x4b29b80);memcpy(file+0x38,"Starfield.esm",14);
    put<uint64_t>(entry,0,reinterpret_cast<uint64_t>(&filep));put<int32_t>(entry,8,1);
    put<uint32_t>(files,0x81e8,1);put<uint64_t>(files,0x81f0,reinterpret_cast<uint64_t>(&entryp));
    put<uint8_t>(ires,0x110,3);put<float>(ires,0x114,0.49152764678001404f);
    put<float>(dnam,40*(3+7)+28,15.0f);put<float>(dnam,40*7+28,60.0f);
    for(unsigned j=0;j<6;++j)put<float>(globals,0x1b8+0x20*j,j==3?.01f:.3f);
    Packet p{source,origin,desc,385246,biom,output,ires,dnam,8,0x3c23d70a,0,nullptr},inner=p;
    std::string mode=argv[1];
    crash_during=mode=="crash-during";
    if(mode=="active")p.mask=3;
    if(mode=="rarity-above-mask")p.mask=0;
    if(mode=="inactive-out-of-switch")put<uint8_t>(ires,0x110,6);
    if(mode=="installed-setting"){
        p.setting=0x3d4ccccd;put<float>(globals,0x218,.05f);
    }
    if(mode=="alternate"){p.descriptor=alternate;put<uint64_t>(alternate,0x10,0xaabbccdd);}
    if(mode=="copper"){put<uint8_t>(ires,0x110,0);put<uint32_t>(ires,0x28,0x57cf);p.setting=0x3e99999a;}
    if(mode=="rejected")put<float>(ires,0x114,90);
    if(mode=="wrong-owner")p.owner=7;
    if(mode=="wrong-source")p.source=reinterpret_cast<void*>(8);
    if(mode=="partial-descriptor")p.descriptor=reinterpret_cast<void*>(8);
    if(mode=="wrong-workshop")put<uint64_t>(source,0x60,0x85f5fc4c6f86a5c3ULL);
    if(mode=="missing-namespace")put<uint16_t>(ires,0x30,0xffff);
    std::vector<Packet> deep(65,p);
    if(mode=="stack-budget"){
        for(size_t i=0;i+1<deep.size();++i)deep[i].nested=&deep[i+1];
        p.nested=&deep[0];
    }
    if(mode=="partial-dnam"){
        // Readable complete block for target, but external full descriptor read crosses NOACCESS.
        auto mem=static_cast<unsigned char*>(VirtualAlloc(nullptr,8192,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));
        p.dnam=mem+4096-440;memcpy(p.dnam,dnam,440);DWORD old{};VirtualProtect(mem+4096,4096,PAGE_NOACCESS,&old);
    }
    if(mode=="nested"){p.nested=&inner;inner.mask=3;}
    unsigned char cu[0x118]{};memcpy(cu,ires,sizeof cu);
    put<uint32_t>(cu,0x28,0x57cf);put<uint8_t>(cu,0x110,0);
    Packet cu_packet=p;cu_packet.ires=cu;cu_packet.setting=0x3e99999a;
    uint64_t order[]={reinterpret_cast<uint64_t>(ires),reinterpret_cast<uint64_t>(cu)};
    if(mode=="paired"||mode=="completion"){
        p.setting=0x3d4ccccd;put<float>(globals,0x218,.05f);
        p.next_resource=&cu_packet;p.order_list=order;
        cu_packet.order_list=order;cu_packet.order_index=1;
    }
    if(mode=="crash-before")RaiseException(0xe0c1f000,0,0,nullptr);
    if(mode=="no-hit")return 0;
    if(mode=="threads"){for(int i=0;i<3;++i){std::thread t([&]{fixture_run(&p);});t.join();}}
    else fixture_run(&p);
    if(mode=="crash-after")RaiseException(0xe0c1f001,0,0,nullptr);
    return 0;
}
