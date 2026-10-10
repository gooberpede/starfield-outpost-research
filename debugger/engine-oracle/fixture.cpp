// SPDX-License-Identifier: GPL-3.0-or-later
// Original disposable layout fixture. No game code, API, saves or native math.
// Literal sentinel outputs qualify acquisition/formatting, never the algorithm.
#include <windows.h>
#include <array>
#include <cstring>
#include <thread>
#include <filesystem>
extern "C" void OracleCheckpoint(void*,void*,void*);

void call_site() {
    std::array<unsigned char,256> frame{}, ref{};
    std::array<unsigned char,128> landscape{};
    std::array<unsigned char,44> base{}, result{};
    std::array<void*,6> context{};
    void* land=landscape.data();
    auto set=[](void* p,int v){std::memcpy(p,&v,4);};
    // Cell (1,10467,21144): hierarchy 54/110,8/2,3/0.
    result[0]=1;set(result.data()+4,54);set(result.data()+8,110);
    set(result.data()+20,8);set(result.data()+24,2);set(result.data()+36,3);
    base=result;set(base.data()+36,0);set(base.data()+24,0);
    float center[3]={356.820404052734375f,2459.05859375f,-31.89084243774414f};
    float translation[3]={0,0,0};int floor[2]={3,24};
    auto anchor=frame.data()+128;
    std::memcpy(anchor-0x49,center,12);std::memcpy(anchor-9,result.data(),44);
    std::memcpy(anchor+0x6f,floor,8);std::memcpy(ref.data()+0x8c,center,12);
    set(landscape.data()+0x50,256);set(landscape.data()+0x54,0x3f59f);
    context[2]=&land;context[3]=base.data();context[4]=translation;
    OracleCheckpoint(ref.data(),context.data(),anchor);
}
int wmain(int argc,wchar_t** argv){
    if(argc!=2)return 2;
    auto start=GetTickCount64();
    while(!std::filesystem::exists(argv[1])) {
        if(GetTickCount64()-start>60000)return 3;
        Sleep(20);
    }
    call_site();std::thread worker(call_site);worker.join();
    auto release=std::filesystem::path(argv[1]);release+=L".release";
    while(!std::filesystem::exists(release)) {
        if(GetTickCount64()-start>60000)return 4;
        Sleep(20);
    }
    return 0;
}
