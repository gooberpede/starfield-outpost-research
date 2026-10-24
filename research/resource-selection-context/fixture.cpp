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
    void* query=nullptr; unsigned char* selection=nullptr; void* effective=nullptr; uint64_t flags=0;
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
    put<uint64_t>(s,0x80,reinterpret_cast<uint64_t>(p->effective));
    memset(s+0xe0,0,0x68);
    put<uint64_t>(s,0x180,reinterpret_cast<uint64_t>(p->origin));
    put<uint64_t>(s,0x188,reinterpret_cast<uint64_t>(p->output));
    put<uint32_t>(s,0x190,1);
    put<uint64_t>(s,0x198,reinterpret_cast<uint64_t>(p->descriptor));
    put<uint64_t>(s,0x1a0,reinterpret_cast<uint64_t>(p->source));
    if(p->selection){
        put<uint64_t>(p->selection,0x78,reinterpret_cast<uint64_t>(p));
        put<uint64_t>(p->selection,0,reinterpret_cast<uint64_t>(p->biom));
        put<uint64_t>(p->selection,8,reinterpret_cast<uint64_t>(s+0x80));
        put<uint64_t>(p->selection,0x10,reinterpret_cast<uint64_t>(s+0x68));
        put<uint32_t>(p->selection,0x18,0x57eb);
        put<uint64_t>(p->selection,0x20,reinterpret_cast<uint64_t>(p->ires));
    }
}
extern "C" uint64_t fixture_sample_mask(Packet*,const int*);
extern "C" void fixture_cell_setup(unsigned char* s,unsigned char* res,int* xy){
    // Known test constants, not a synthetic implementation of native CRC/MT.
    put<uint64_t>(s,0xa0,0x1234567800000000ULL|uint32_t(xy[0]));
    float draw=retail::field<float>(res,0x114);
    if(xy[0]==11&&draw<1)draw=10.240686416625977f;
    put<float>(s,0xa8,draw);
}
// Deliberately small original fixture selector; it is not retail code.
static uint64_t peek(uint64_t at,size_t n){
    uint64_t v=0;SIZE_T got=0;
    return n<=8&&ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(at),&v,n,&got)&&got==n?v:0;
}
static uint64_t find_descriptor(uint64_t record,uint64_t root,bool first=false){
    auto n=peek(record+0x38,4),entries=peek(record+0x40,8);
    if(n>2)return 0;
    for(uint64_t i=0;i<n;++i)if(first||peek(entries+i*0x238,8)==root)return entries+i*0x238+8;
    return 0;
}
static uint64_t find_biom(uint64_t biom,uint64_t root,bool first=false){
    auto n=peek(biom+0x308,4),refs=peek(biom+0x310,8);
    if(n>2)return 0;
    for(uint64_t i=0;i<n;++i){auto d=find_descriptor(peek(refs+i*8,8),root,first);if(d)return d;}
    return 0;
}
extern "C" uint64_t fixture_select_start(Packet* p,unsigned char* f){
    if(!(p->flags&1))return 1;
    auto root=reinterpret_cast<uint64_t>(p->ires);
    auto d=find_descriptor(reinterpret_cast<uint64_t>(p->effective),root);
    if(!d)d=find_biom(reinterpret_cast<uint64_t>(p->biom),root);
    put<uint64_t>(f,0x68,d);return d?0:1;
}
extern "C" uint64_t fixture_resolve(unsigned char* context,uint64_t biom){
    auto p=reinterpret_cast<Packet*>(peek(reinterpret_cast<uint64_t>(context)+0x78,8));
    if(!p||!(p->flags&1))return 0;
    auto d=find_descriptor(reinterpret_cast<uint64_t>(p->effective),reinterpret_cast<uint64_t>(p->ires));
    if(!d)d=find_biom(biom,reinterpret_cast<uint64_t>(p->ires));
    if(d)put<uint64_t>(reinterpret_cast<unsigned char*>(peek(reinterpret_cast<uint64_t>(context)+0x10,8)),0,d);
    return d;
}
extern "C" void fixture_select_finish(Packet* p,unsigned char* f){
    if(!(p->flags&1))return;
    auto d=peek(reinterpret_cast<uint64_t>(f)+0x68,8);
    if(!d)d=find_biom(reinterpret_cast<uint64_t>(p->biom),0,true);
    put<uint64_t>(f,0x68,d);p->dnam=reinterpret_cast<void*>(d);
}
extern "C" uint64_t fixture_sample_mask(Packet* p,const int* xy){
    // A target-owned spatial table: construction and later cells differ.
    if(!(p->flags&2))return p->mask;
    auto result=xy&&xy[0]==101&&xy[1]==-201?1ULL:4ULL;
    put<uint64_t>(static_cast<unsigned char*>(p->output),result==1?0:8,result);
    return result;
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
    unsigned char source[0x70]{},desc[0x30]{},alternate[0x30]{},biom[0x318]{},manager[0x200]{},ires[0x118]{},dnam[560]{};
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
    int query[]={101,-201};
    unsigned char selection[0x90]{},node[0x200]{},rsgd[0x48]{},entries[0x470]{},altbiom[0x318]{};
    unsigned char secondbiom[0x318]{};
    uint64_t refs[]={reinterpret_cast<uint64_t>(rsgd)};
    put<uint64_t>(selection,0x40,reinterpret_cast<uint64_t>(node));
    put<uint64_t>(selection,0x48,0);
    put<uint64_t>(selection,0x60,reinterpret_cast<uint64_t>(altbiom));
    put<uint16_t>(node,0x12,0x80);
    put<uint32_t>(node,0xe0,0x8ae7b);put<uint32_t>(node,0xf0,0x57eb);
    put<uint32_t>(rsgd,0x28,0x83ea);put<uint32_t>(rsgd,0x38,2);
    put<uint64_t>(rsgd,0x40,reinterpret_cast<uint64_t>(entries));
    put<uint64_t>(entries,0,reinterpret_cast<uint64_t>(ires));memcpy(entries+8,dnam,560);
    put<uint64_t>(entries,0x238,reinterpret_cast<uint64_t>(ires));
    put<uint32_t>(altbiom,0x28,0x8ae7b);put<uint32_t>(altbiom,0x308,1);
    put<uint64_t>(altbiom,0x310,reinterpret_cast<uint64_t>(refs));
    put<uint32_t>(biom,0x308,1);put<uint64_t>(biom,0x310,reinterpret_cast<uint64_t>(refs));
    memcpy(secondbiom,altbiom,sizeof altbiom);put<uint32_t>(secondbiom,0x28,0x95092);
    put<uint16_t>(node,0x16,0x100);
    put<uint32_t>(node,0x160,0x95092);put<uint32_t>(node,0x170,0x57eb);
    put<uint64_t>(selection,0x68,reinterpret_cast<uint64_t>(secondbiom));
    put<uint64_t>(selection,0x70,2);
    p.query=query;p.selection=selection;p.effective=rsgd;inner=p;
    unsigned char arsgd[0x48]{},brsgd[0x48]{},aentries[0x238]{},bentries[0x238]{};
    memcpy(arsgd,rsgd,sizeof rsgd);memcpy(brsgd,rsgd,sizeof rsgd);
    put<uint32_t>(arsgd,0x28,0x83ea);put<uint32_t>(brsgd,0x28,0x83dd);
    put<uint32_t>(arsgd,0x38,1);put<uint32_t>(brsgd,0x38,1);
    put<uint64_t>(arsgd,0x40,reinterpret_cast<uint64_t>(aentries));
    put<uint64_t>(brsgd,0x40,reinterpret_cast<uint64_t>(bentries));
    memcpy(aentries+8,dnam,560);memcpy(bentries+8,dnam,560);
    put<uint32_t>(entries,8,101);put<uint32_t>(aentries,8,202);put<uint32_t>(bentries,8,303);
    uint64_t arefs[]={reinterpret_cast<uint64_t>(arsgd)},brefs[]={reinterpret_cast<uint64_t>(brsgd)};
    put<uint64_t>(altbiom,0x310,reinterpret_cast<uint64_t>(arefs));
    put<uint64_t>(secondbiom,0x310,reinterpret_cast<uint64_t>(brefs));
    std::string mode=argv[1];
    if(mode=="inactive"||mode=="candidate-reversed"||mode=="first-success"||mode=="current-precedence"||mode=="rnam-precedence"||mode=="fallback"){
        p.flags=1;put<uint32_t>(rsgd,0x38,1);
        put<uint64_t>(entries,0,0x1234);put<uint64_t>(aentries,0,0x1234);
        put<uint64_t>(bentries,0,reinterpret_cast<uint64_t>(ires));
        if(mode=="first-success")put<uint64_t>(aentries,0,reinterpret_cast<uint64_t>(ires));
        if(mode=="current-precedence")put<uint64_t>(entries,0,reinterpret_cast<uint64_t>(ires));
        if(mode=="rnam-precedence"){
            put<uint64_t>(aentries,0,reinterpret_cast<uint64_t>(ires));
            put<uint64_t>(biom,0x310,reinterpret_cast<uint64_t>(arefs));
        }
        if(mode=="fallback")put<uint64_t>(bentries,0,0x1234);
    }
    if(mode=="nonuniform-mask")p.flags=2;

    if(mode=="candidate-reversed"){
        put<uint32_t>(node,0xe0,0x95092);put<uint32_t>(node,0x160,0x8ae7b);
        put<uint64_t>(selection,0x60,reinterpret_cast<uint64_t>(secondbiom));
        put<uint64_t>(selection,0x68,reinterpret_cast<uint64_t>(altbiom));
    }
    if(mode=="same-biom")put<uint32_t>(node,0xe0,1332288);
    if(mode=="wrong-family")put<uint32_t>(node,0xf0,0x57c7);
    if(mode=="bad-count")put<uint32_t>(rsgd,0x38,0xffffffff);
    if(mode=="bad-rnam")put<uint64_t>(altbiom,0x310,8);
    if(mode=="wrong-query")p.query=reinterpret_cast<void*>(8);
    if(mode=="bad-node")put<uint64_t>(selection,0x40,8);
    if(mode=="bad-index")put<uint64_t>(selection,0x48,0xfe0);


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
    unsigned char inner_selection[0x90]{};memcpy(inner_selection,selection,sizeof selection);
    if(mode=="nested"){p.nested=&inner;inner.mask=3;inner.selection=inner_selection;}
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
    if(mode=="threads"){
        std::vector<std::thread> workers;
        for(int i=0;i<3;++i)workers.emplace_back([&]{
            unsigned char thread_selection[0x90];memcpy(thread_selection,selection,sizeof selection);
            Packet own=p;own.selection=thread_selection;fixture_run(&own);
        });
        for(auto& worker:workers)worker.join();
    }
    else if(mode=="cache-only"||mode=="cache-then-generation"){
        p.flags|=4;fixture_run(&p);p.flags&=~4ULL;
        if(mode=="cache-then-generation")fixture_run(&p);
    }else fixture_run(&p);
    if(mode=="crash-after")RaiseException(0xe0c1f001,0,0,nullptr);
    return 0;
}
