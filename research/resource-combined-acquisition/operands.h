// SPDX-License-Identifier: GPL-3.0-or-later
// Owned D4 extension of C1E debug-event engine, not game implementation.
#pragma once
#include "../resource-tungsten-acquisition/decode.h"
#include <vector>
namespace operands {
constexpr uint32_t sites[]={0x79b520,0x79be20,0x79fb1b,0x79ff1d};
struct Invocation {
    uint64_t token=0,parent=0,entry=0,source=0,descriptor=0,biom=0,output=0;
    uint64_t resource=0,selection=0,order=0,cells=0;
    bool entry_ok=false,call_ok=false; uint64_t provider_rsp=0; bool upstream=false; uint32_t stages=0; bool selection_valid=true;
};
struct Upstream { uint64_t rsp=0,source=0,biom=0,query=0,biom_capture=0,query_capture=0,provider_token=0; bool complete=false,query_seen=false; };
struct State { Upstream pending{}; uint64_t next=0; std::vector<Invocation> stack; };
}
