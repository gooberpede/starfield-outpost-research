// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable synthetic-memory tests; no target process or game input.
#include "context.h"
#include <cassert>
#include <map>
int main(){
    std::map<uint64_t,std::vector<unsigned char>> memory;
    const uint64_t base=0x140000000,manager=0x10000,source=0x20000,slot=0x30008,wrapper=0x40000,procgen=0x50000;
    auto put=[&](uint64_t address,size_t size){memory[address].resize(size);};
    put(base+0x5fd9c30,8);put(manager,0x200);put(source,0x70);put(slot-8,24);
    auto word=[&](uint64_t address,size_t offset,uint64_t v){memcpy(memory[address].data()+offset,&v,8);};
    word(base+0x5fd9c30,0,manager);word(manager,0x130,procgen);
    word(slot-8,0,source);word(slot-8,8,wrapper);
    bool partial=false,change=false;unsigned reads=0;
    auto reader=[&](uint64_t address,void* destination,size_t size){
        ++reads;auto it=memory.find(address);
        if(partial||it==memory.end()||it->second.size()!=size)return false;
        memcpy(destination,it->second.data(),size);
        if(change&&reads>4&&address==source)static_cast<unsigned char*>(destination)[0]^=1;
        return true;
    };
    auto capture=[&]{reads=0;return context_capture::capture(reader,base,procgen,slot,source,wrapper);};
    auto historical_epoch_a=capture(),historical_epoch_b=capture();
    // Distinct unobservable synthetic histories have identical consumer bytes.
    // The receipt must not invent a join to either history.
    assert(historical_epoch_a==historical_epoch_b);
    assert(historical_epoch_a.find("\"status\":\"COMPLETE\"")!=std::string::npos);
    assert(historical_epoch_a.find("\"generation_epoch\":null")!=std::string::npos);
    assert(historical_epoch_a.find("\"historical_inputs\":null")!=std::string::npos);
    change=true;assert(capture().find("\"status\":\"INCOMPLETE\"")!=std::string::npos);
    change=false;partial=true;assert(capture().find("\"raw_source\":null")!=std::string::npos);
    partial=false;word(slot-8,8,wrapper+8);
    assert(capture().find("\"status\":\"INCOMPLETE\"")!=std::string::npos);
    word(slot-8,8,wrapper);word(manager,0x130,procgen+8);
    assert(capture().find("\"status\":\"INCOMPLETE\"")!=std::string::npos);
    return 0;
}
