// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable test of the actual production pre-edit wait, no target operations.
#include "health.h"
#include <thread>
#include <iostream>
int main(int argc,char** argv){using namespace oracle;try{
    if(argc!=2)throw std::runtime_error("exclusive output required");fs::path session=argv[1];if(!fs::create_directory(session))throw std::runtime_error("exclusive path");
    unsigned char untouched[]{0xe8,1,2,3,4};std::atomic<bool> ready{},done{};
    std::thread stopper([&]{ready=true;while(!fs::exists(session/L"waiting-sole-thread.json"))SwitchToThread();if(!write_new(session/L"STOP","STOP\n"))std::abort();while(!done)SwitchToThread();});
    while(!ready)SwitchToThread();bool refused=false;
    try{await_admission(session,"{\"component\":\"SorNativePositionOracle\",\"version\":\"0.5.0\",\"synthetic\":true");}catch(const std::runtime_error& e){refused=std::string(e.what())=="operator_STOP_before_admission";}
    done=true;stopper.join();unsigned char expected[]{0xe8,1,2,3,4};
    if(!refused||memcmp(untouched,expected,5)||fs::exists(session/L"ready.json"))throw std::runtime_error("pre-edit STOP contract");
    std::cout<<"PASS production unsafe-admission wait exits on STOP before any edit or READY\n";return 0;
}catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
