// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "acquisition.h"

void acquisition_tests(const sor::fs::path& root) {
    using namespace sor;
    constexpr std::uint64_t module=0x10000000;
    struct ObservedMemory:Memory {
        std::vector<std::uint64_t> reads;
        LoadTelemetry* notifications{};
        std::function<void(std::uint64_t)> on_read;
        bool bytes(std::uint64_t p,void* out,std::size_t n)override {
            reads.push_back(p);
            if(on_read)on_read(p);
            if(notifications){notifications->before();notifications->after();}
            return Memory::bytes(p,out,n);
        }
        void scene(std::uint64_t shift,bool pair=true) {
            data.clear();reads.clear();
            auto player=shift+0x60000,cell=shift+0x10000,world=shift+0x70000,array=shift+0x40000;
            put(module+0x05f43230,player);ref(player,7,0x14);put(player+0xb0,cell);
            put(cell+0x2e,std::uint8_t(0x49));put(cell+0x48,std::uint32_t(0));put(cell+0x110,world);
            put(world+0x2e,std::uint8_t(0x56));put(world+0xd8,std::uint64_t(0));
            put(cell+0x80,Collection{pair?2u:0u,2,array});
            if(pair) {
                ref(shift+0x20000,beacon_base,0xff000100);ref(shift+0x22000,storage_base,0xff000101);
                put(shift+0x200b0,cell);put(shift+0x220b0,cell);
                put(array,shift+0x20000);put(array+8,shift+0x22000);
            }
        }
    } m;
    LoadTelemetry telemetry;
    m.scene(0,false);
    auto a0=acquire(m,module,0,true);
    std::string reason;
    require(a0.ok&&consistent(m,module,a0,reason)&&telemetry.pre==0&&telemetry.post==0,"zero notifications permits confirmed A0 capture");
    m.reads.clear();
    require(acquire(m,module,0,false).reason=="operator_confirmation_missing"&&m.reads.empty(),"unconfirmed checkpoint performs no live reads");
    m.scene(0);
    auto a2=acquire(m,module,4,true);
    require(a2.ok&&consistent(m,module,a2,reason),"zero notifications permits A2 selected-query gate");
    const auto evidence_only=a2.selection.selected;
    m.scene(0x100000); // Destroy all A2 addresses; reused FormIDs, entirely new pointers.
    auto a2r=acquire(m,module,5,true);
    require(a2r.ok&&consistent(m,module,a2r,reason),"A2R reacquires with no load notification");
    require(a2r.context.player.pointer==0x160000&&a2r.context.cells[0]==0x110000&&a2r.context.world==0x170000,"A2R reacquires player cell and world");
    require(a2r.selection.selected[0].pointer==0x120000&&a2r.selection.selected[1].pointer==0x122000,"A2R uses fresh selected pointers");
    require(a2r.selection.selected[0].id==evidence_only[0].id&&a2r.selection.selected[0].pointer!=evidence_only[0].pointer,"stable ID comparison uses copied evidence only");
    bool stale=false;for(auto p:m.reads)if(p>=0x10000&&p<0x80000)stale=true;
    require(!stale,"A2R never dereferences old player cell world array or selected addresses");
    telemetry.before(); // Unpaired notification cannot latch a loading state.
    auto unpaired=acquire(m,module,5,true);
    require(unpaired.ok&&consistent(m,module,unpaired,reason),"unpaired optional preload does not block acquisition");
    m.notifications=&telemetry;
    auto noisy=acquire(m,module,5,true);
    require(noisy.ok&&consistent(m,module,noisy,reason)&&telemetry.pre>1&&telemetry.post>0,"notifications during reads do not gate correctness");
    require(noisy.selection.selected==a2r.selection.selected,"optional notification delivery does not change selection");
    m.notifications=nullptr;

    auto persist=[&](const char* stem,const Acquisition& current,const std::string& why) {
        std::atomic<bool> stopped{};std::string failure;
        auto data=anomaly_json("A2R",5,why,current.selection,0,7,"","SYNTHETIC");
        require(data.size()<=max_checkpoint_bytes,"inconsistent-state anomaly bounded");
        require(record_issue(why,stopped,[&]{return write_new(root/(std::string(stem)+"-anomaly.json"),data);},
            [&](const std::string& v){failure=v;})&&!stopped&&failure.empty(),"inconsistent-state anomaly persists and leaves observer available");
    };
    m.put(0x16008c,std::array<float,3>{9,2,3});
    require(!consistent(m,module,a2r,reason)&&reason=="player_context_changed","player drift blocks queries without messages");
    persist("player-context",a2r,reason);
    m.scene(0x100000);m.put(0x110048,std::uint32_t(2));
    require(!consistent(m,module,a2r,reason)&&reason=="cell_context_changed","cell flag change blocks queries without messages");
    persist("cell-context",a2r,reason);
    m.scene(0x100000);m.put(0x110080,Collection{1,2,0x140000});
    require(!consistent(m,module,a2r,reason)&&reason=="collection_changed","collection change blocks cached selection");
    persist("live-collection",a2r,reason);
    m.scene(0x100000);m.put(0x1220b0,std::uint64_t(0x180000));
    require(!consistent(m,module,a2r,reason)&&reason=="selected_identity_changed_before_query","reference stored-cell change blocks query");
    persist("reference-context",a2r,reason);
    m.scene(0x100000);m.data.erase(module+0x05f43230);
    require(!consistent(m,module,a2r,reason)&&reason=="player_pointer_read_failed"&&!scientific_anomaly(reason),"unsafe player-global read remains terminal");
    m.scene(0x100000);m.put(module+0x05f43230,std::uint64_t(0));
    require(acquire(m,module,5,true).reason=="player_context_unavailable","operator confirmation alone cannot approve absent player");
    for(std::size_t cp=0;cp<checkpoints.size();++cp) {
        auto prefix=std::string(checkpoints[cp]);
        require(!request_matches(prefix+"\n",cp),"legacy unconfirmed request rejected");
        require(request_matches(prefix+(cp==5?"\nRELOADED_SETTLED\n":"\nSETTLED\n"),cp),"exact per-checkpoint attestation accepted");
    }
    require(!request_matches("A2R\nSETTLED\n",5),"A2R requires reload-specific attestation");
    m.scene(0x100000);unsigned global_reads{};
    m.on_read=[&](std::uint64_t p) {
        if(p==module+0x05f43230&&++global_reads==2)m.put(0x16008c,std::array<float,3>{8,2,3});
    };
    auto during=acquire(m,module,5,true);
    require(!during.ok&&during.reason=="player_context_changed"&&during.selection.selected.size()==2,"player change during fresh acquisition preserves candidates and blocks query path");
    persist("during-acquisition",during,during.reason);
    require(write_new(root/L"synchronization.json","{\"checkpoint\":\"A2R\""+synchronization_fields(5,0,0)+"}\n"),"production synchronization evidence with zero telemetry");
}
