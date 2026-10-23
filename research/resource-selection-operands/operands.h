// SPDX-License-Identifier: GPL-3.0-or-later
// Owned C1G extension of C1E debug-event engine, not game implementation.
#pragma once
#include "../resource-oracle-retail/decode.h"
#include <vector>
namespace operands {
constexpr uint32_t sites[]={0x79b520,0x79be20,0x79a59e,0x79ff1d};
struct Invocation {
    uint64_t token=0,parent=0,entry=0,source=0,descriptor=0,biom=0,output=0;
    uint64_t resource=0,selection=0,order=0,cells=0;
    bool entry_ok=false,call_ok=false;
};
struct State { uint64_t next=0; std::vector<Invocation> stack; };
}
