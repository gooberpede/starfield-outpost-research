// SPDX-License-Identifier: GPL-3.0-or-later
#include <windows.h>
#include <filesystem>
#include <fstream>
#include <array>
#include <thread>
#include <atomic>
#include <cstring>
#include <stdexcept>
#include <iostream>
extern "C" void CenterEntry(void*,float*),CenterExit(),GridEntry(void*,void*),GridX(),GridY(),GridResult(),GridExit();
extern "C" int CheckState(void*,float*);
struct Ref {
    std::array<unsigned char,0xd0> raw{};float compensation[3]{};int mode{},depth{};
    std::array<unsigned char,0x30> base{};std::array<unsigned char,0x20> list{};
    std::array<unsigned char,0xa0> extra{};std::array<unsigned char,0x118> cell{};std::array<unsigned char,0x390> world{};
    Ref(){
        auto ptr=[](auto& array,size_t offset,void* p){std::memcpy(array.data()+offset,&p,8);};
        unsigned id=0x2c60e9;std::memcpy(base.data()+0x28,&id,4);base[0x2e]=0x1e;raw[0x2e]=0x4a;
        ptr(raw,0x98,base.data());ptr(raw,0xc8,list.data());ptr(list,8,extra.data());extra[0x12]=0xbc;
        ptr(raw,0xb0,cell.data());cell[0x2e]=0x49;ptr(cell,0x110,world.data());
        unsigned long long workshop=0x9b7b4cee66a0fc0eULL;std::memcpy(extra.data()+0x98,&workshop,8);
    }
};
std::atomic<unsigned> entered{},completed{},exceptions{},bad{};std::atomic<bool> overlap{};
extern "C" void CenterBody(Ref* r,float* out){
    ++entered;
    if(r->mode==3)throw std::runtime_error("fixture_unwind");
    std::memcpy(out,r->raw.data()+0x8c,12);
    if(r->depth){Ref child=*r;child.depth--;float nested[3];CenterEntry(&child,nested);}
    if(r->mode==4){++exceptions;RaiseException(0xe0424242,0,0,nullptr);}
    if(r->mode==5)while(!overlap.load())Sleep(1);
    if(r->mode!=1)for(int i=0;i<3;++i)out[i]+=r->compensation[i];
    ++completed;
}
extern "C" void GridBody(void*,Ref* r,float* translated,unsigned char* result){
    CenterEntry(r,translated);
    result[0]=1;int values[]={54,110,8,2,3,0};int offsets[]={4,8,20,24,36,40};
    for(int i=0;i<6;++i)std::memcpy(result+offsets[i],&values[i],4);
    int floor[]={3,24};std::memcpy(result+0x78,floor,8); // (RBP+6f)-(RBP-9)
}
LONG WINAPI handler(EXCEPTION_POINTERS* e){return e->ExceptionRecord->ExceptionCode==0xe0424242?EXCEPTION_CONTINUE_EXECUTION:EXCEPTION_CONTINUE_SEARCH;}
void one(int mode,int depth){Ref r;r.mode=mode;r.depth=depth;float input[]={321.25f,-42.5f,17.0f};
    std::memcpy(r.raw.data()+0x8c,input,12);if(mode!=1){r.compensation[0]=2.0f;r.compensation[1]=-3.0f;r.compensation[2]=4.0f;}
    std::memcpy(r.extra.data()+0x60,r.compensation,12);
    float output[3]{};
    try {if(!CheckState(&r,output))++bad;if(mode!=3){for(int i=0;i<3;++i)if(output[i]!=input[i]+r.compensation[i])++bad;}}
    catch(const std::runtime_error&){++exceptions;}
}
int wmain(int argc,wchar_t** argv){
    SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
    if(argc!=3)return 2;std::filesystem::path root=argv[1];std::string mode=std::filesystem::path(argv[2]).string();
    auto base=(uintptr_t)GetModuleHandleW(nullptr);
    std::ofstream plan(root/L"fixture.plan");
    for(auto [name,p,len]:std::initializer_list<std::tuple<const char*,uintptr_t,int>>{
        {"center_entry",(uintptr_t)CenterEntry,5},{"center_exit",(uintptr_t)CenterExit,5},
        {"grid_entry",(uintptr_t)GridEntry,5},{"grid_x",(uintptr_t)GridX,4},{"grid_y",(uintptr_t)GridY,4},{"grid_result",(uintptr_t)GridResult,4},{"grid_exit",(uintptr_t)GridExit,8}}){
        plan<<name<<" "<<std::hex<<(p-base)<<" ";for(int i=0;i<len;++i){char b[3];sprintf_s(b,"%02x",((unsigned char*)p)[i]);plan<<b;}plan<<"\n";
    }plan.close();
    AddVectoredExceptionHandler(1,handler);
    while(!std::filesystem::exists(root/L"GO"))Sleep(10);
    if(mode=="retire-active"){
        std::thread active([]{one(5,0);});while(!entered.load())Sleep(1);std::ofstream(root/L"ACTIVE")<<"active\n";
        while(!std::filesystem::exists(root/L"CONTINUE"))Sleep(10);overlap=true;active.join();
    }else if(mode!="zero"){
        one(1,0);one(2,0);one(2,2);one(3,0);one(4,0);
        auto previous=entered.load();std::thread first([]{one(5,0);});while(entered.load()==previous)Sleep(1);
        std::thread second([]{overlap=true;one(2,0);});first.join();second.join();
        std::array<std::thread,8> workers;for(auto& t:workers)t=std::thread([]{for(int i=0;i<4;++i)one((i%2)+1,0);});for(auto& t:workers)t.join();
        Ref r;float xyz[]={356.820404052734375f,2459.05859375f,-31.89084243774414f};std::memcpy(r.raw.data()+0x8c,xyz,12);
        std::array<unsigned char,0x58> landscape{};int resolution=256,body=0x3f59f;std::memcpy(landscape.data()+0x50,&resolution,4);std::memcpy(landscape.data()+0x54,&body,4);
        void* land=landscape.data();std::array<unsigned char,44> hierarchy{};float translation[3]{};int bounds[4]{};bool value{};
        void* context[]={&value,hierarchy.data(),&land,hierarchy.data(),translation,bounds};GridEntry(context,&r);
    }
    std::ofstream(root/L"counts.json")<<"{\"entered\":"<<entered<<",\"completed\":"<<completed<<",\"exceptions\":"<<exceptions<<",\"bad\":"<<bad<<"}\n";
    while(!std::filesystem::exists(root/L"RELEASE"))Sleep(10);
    return bad?3:0;
}
