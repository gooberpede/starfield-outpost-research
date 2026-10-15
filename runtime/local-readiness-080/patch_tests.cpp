// SPDX-License-Identifier: GPL-3.0-or-later
// Original controlled synthetic pages only; never opens or patches Starfield.
#define SOR_FIXTURE
#include "patch.h"
#include <cassert>
using namespace history;
int main(){
    auto* page=static_cast<unsigned char*>(VirtualAlloc(nullptr,4096,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));assert(page);
    Edit e[3];for(unsigned i=0;i<3;++i){e[i].address=page+i*8;e[i].size=8;memset(e[i].after,0x40+i,8);}
    bool dirty=false;
    assert(!install(e,3,false,dirty)&&!dirty);
    page[16]=1;assert(!install(e,3,true,dirty)&&!dirty);assert(page[0]==0&&page[8]==0);page[16]=0;
    fixture_write_failure=page+8;assert(!install(e,3,true,dirty)&&!dirty);for(auto& edit:e)assert(match(edit,false));
    fixture_write_failure=nullptr;assert(install(e,3,true,dirty)&&dirty);for(auto& edit:e)assert(match(edit,true));
    for(auto& edit:e)assert(write(edit,false));for(auto& edit:e)assert(match(edit,false));
    Edit call;assert(call_edit(call,0x100000,0x100123));assert(!call_edit(call,0x100000,0x100000000ULL));
    VirtualFree(page,0,MEM_RELEASE);puts("PASS quiescent admission, all-preimage guard, partial install rollback, restore and rel32 range");
}
