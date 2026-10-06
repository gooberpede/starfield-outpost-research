// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "core.h"
#include <atomic>

namespace sor {
// Optional counters only. No acquisition function accepts or consults them.
struct LoadTelemetry {
    std::atomic<unsigned> pre{},post{};
    void before(){++pre;}
    void after(){++post;}
};
inline std::string synchronization_fields(std::size_t cp,unsigned pre,unsigned post) {
    return ",\"synchronization\":\"operator_settled_fresh_state_v1\",\"operator_settled\":true,\"reloaded_and_settled\":"+
        std::string(cp==5?"true":"false")+",\"load_notifications\":{\"pre\":"+std::to_string(pre)+
        ",\"post\":"+std::to_string(post)+",\"role\":\"telemetry_only\"}";
}
struct LiveContext {
    Identity player{};
    std::uint64_t world{},persistent{};
    std::uint32_t flags{};
    std::vector<std::uint64_t> cells;
    std::vector<Collection> collections;
};
inline bool read_context(Reader& r,std::uint64_t module,LiveContext& out,std::string& error) {
    out={};std::uint64_t player{};std::uint8_t type{};
    if(!r.get(module+0x05f43230,player)){error="player_pointer_read_failed";return false;}
    if(!player){error="player_context_unavailable";return false;}
    if(!identity(r,player,out.player,&error))return false;
    if(out.player.id!=0x14){error="player_identity_mismatch";return false;}
    if(!out.player.cell){error="player_context_unavailable";return false;}
    if(!r.get(out.player.cell+0x2e,type)||type!=0x49){error="cell_read_failed";return false;}
    if(!r.get(out.player.cell+0x48,out.flags)||!r.get(out.player.cell+0x110,out.world)){error="exterior_context_read_failed";return false;}
    if((out.flags&1)||!out.world){error="exterior_context_unavailable";return false;}
    if(!r.get(out.world+0x2e,type)||type!=0x56||!r.get(out.world+0xd8,out.persistent)){error="world_structure_failed";return false;}
    out.cells.push_back(out.player.cell);
    if(out.persistent&&out.persistent!=out.player.cell)out.cells.push_back(out.persistent);
    for(auto cell:out.cells) {
        Collection view{};
        if(!r.get(cell+0x2e,type)||type!=0x49||!r.get(cell+0x80,view)){error="collection_read_failed";return false;}
        out.collections.push_back(view);
    }
    return true;
}
inline bool context_matches(Reader& r,std::uint64_t module,const LiveContext& expected,std::string& error) {
    // Re-read the global first: do not start by dereferencing a cached player.
    LiveContext now;
    if(!read_context(r,module,now,error))return false;
    if(now.player!=expected.player){error="player_context_changed";return false;}
    if(now.world!=expected.world||now.persistent!=expected.persistent||now.flags!=expected.flags||now.cells!=expected.cells){error="cell_context_changed";return false;}
    if(now.collections!=expected.collections){error="collection_changed";return false;}
    return true;
}
struct Acquisition {
    bool ok{};
    std::string reason;
    LiveContext context;
    Selection selection;
};
inline Acquisition acquire(Reader& r,std::uint64_t module,std::size_t cp,bool operator_confirmed,
                           std::function<bool()> expired=[] {return false;}) {
    // All state belongs to this invocation. In particular A2R takes no A2 input.
    Acquisition out;
    if(!operator_confirmed){out.reason="operator_confirmation_missing";return out;}
    if(cp>=checkpoints.size()){out.reason="invalid_selection_scope";return out;}
    if(!read_context(r,module,out.context,out.reason))return out;
    out.selection=select(r,out.context.cells,cp,expired);
    if(!out.selection.ok){out.reason=out.selection.reason;return out;}
    if(expired()){out.reason="selection_time_budget";return out;}
    if(!context_matches(r,module,out.context,out.reason))return out;
    out.ok=true;return out;
}
inline bool consistent(Reader& r,std::uint64_t module,const Acquisition& current,std::string& error) {
    if(!current.ok){error="invalid_acquisition";return false;}
    if(!context_matches(r,module,current.context,error))return false;
    for(const auto& item:current.selection.selected) {
        Identity now;
        if(!identity(r,item.pointer,now,&error))return false;
        if(now!=item){error="selected_identity_changed_before_query";return false;}
    }
    return context_matches(r,module,current.context,error);
}
}
