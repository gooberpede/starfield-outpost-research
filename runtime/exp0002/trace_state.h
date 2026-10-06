// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include <cstdint>
namespace sor {
// Independent wall-clock checks also run when no debug event arrives.
struct TraceState {
    std::uint64_t armed{}, stack{}, return_site{};
    unsigned hits{}, phase{};
    bool expired(std::uint64_t now) const {return now-armed>=5000 || hits>=100;}
    bool entry(std::uint64_t rsp,std::uint64_t ret) {
        ++hits;if(phase || !rsp || !ret)return false;
        stack=rsp;return_site=ret;phase=1;return true;
    }
    bool tail(std::uint64_t rsp) {if(phase!=1||rsp!=stack)return false;phase=2;return true;}
    bool returned(std::uint64_t rsp) {if(phase!=2||rsp!=stack+8)return false;phase=3;return true;}
};
}
