// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "binding.h"
#include <cstring>
#include <stdexcept>

namespace d5ar::fixture {
struct BindingInput {
    std::uint64_t manager=0x20000,proc=0x30000;
    std::uint32_t owner=7;
    std::uint8_t mode=2;
    std::array<std::uint8_t,44> descriptor{};
    unsigned calls{},failure{};bool throws{};
    static bool read(void* context,std::uint64_t address,void* output,std::size_t size) {
        auto& input=*static_cast<BindingInput*>(context);++input.calls;
        if(input.throws)throw std::runtime_error("Owned reader exception");
        if(input.calls==input.failure)return false;
        const void* source=nullptr;std::size_t expected=0;
        if(address==0x140000000ULL+0x5fd9c30){source=&input.manager;expected=8;}
        else if(address==input.manager+0x130){source=&input.proc;expected=8;}
        else if(address==input.manager+0x80){source=&input.owner;expected=4;}
        else if(address==input.manager+0x20){source=&input.mode;expected=1;}
        else if(address==input.manager+(input.mode==3?0x1c0:0xc8)){source=input.descriptor.data();expected=44;}
        if(!source||expected!=size)return false;std::memcpy(output,source,size);return true;
    }
    OwnedBinding run(){return read_binding(read,this,0x140000000ULL);}
};
inline unsigned binding_controls() {
    unsigned checks=0;
    auto check=[&](bool condition,const char* label){if(!condition)throw std::runtime_error(label);++checks;};
    {BindingInput x;for(std::size_t i=0;i<44;++i)x.descriptor[i]=std::uint8_t(i);auto b=x.run();
        check(b.complete&&b.attached_proc==x.proc&&b.owner_formid==7&&b.mode==2&&b.descriptor==x.descriptor&&x.calls==5,"exact current binding fields");}
    {BindingInput x;x.mode=3;check(x.run().complete&&x.calls==5,"alternate native descriptor selection");}
    {BindingInput x;x.manager=0;auto b=x.run();check(!b.complete&&std::string(b.status)=="NO_MANAGER"&&x.calls==1,"absent current manager explicit");}
    for(unsigned failed=1;failed<=5;++failed){BindingInput x;x.failure=failed;auto b=x.run();check(!b.complete&&std::string(b.status)=="READ_FAILED","partial binding never a certificate");}
    {BindingInput x;x.throws=true;check(std::string(x.run().status)=="READ_EXCEPTION","reader exception preserved");}
    {BindingInput x;x.manager=UINT64_MAX;check(!x.run().complete&&x.calls==1,"manager address overflow refused");}
    {BindingInput x;check(!read_binding(nullptr,&x,0x140000000ULL).complete,"missing binding reader");}
    {BindingInput x;check(!read_binding(BindingInput::read,&x,UINT64_MAX).complete&&x.calls==0,"module address overflow refused");}
    return checks;
}
}
