// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "observation_policy.h"

void observation_tests(const sor::fs::path& root) {
    using namespace sor;
    Memory m;m.put(0x1002e,std::uint8_t(0x49));m.put(0x10080,Collection{0,0,0});
    std::atomic<bool> stopped{};unsigned queries{},recorded{};std::string failure;
    auto capture=[&](std::size_t cp,const char* filename) {
        auto picked=select(m,{0x10000},cp);
        if(selected_or_report(picked,[&](const std::string& reason){
            if(record_issue(reason,stopped,[&]{return write_new(root/filename,anomaly_json(checkpoints[cp],cp,reason,picked,0,12,"","SYNTHETIC"));},
                [&](const std::string& value){failure=value;}))++recorded;
        })&&!stopped)++queries; // fake query stands in for the guarded native path
        return picked;
    };
    auto missing=capture(2,"missing-anomaly.json");
    require(missing.reason=="selected_counts_disagree"&&missing.counts_complete,"missing candidate counts recorded");
    require(recorded==1&&!stopped&&queries==0&&failure.empty(),"scientific mismatch persists without terminating or querying");
    m.ref(0x20000,beacon_base,0xff000100);m.put(0x40000,std::uint64_t(0x20000));m.put(0x10080,Collection{1,1,0x40000});
    require(capture(3,"unused.json").ok&&queries==1&&!stopped,"fresh subsequent checkpoint remains usable");
    m.ref(0x22000,storage_base,0xff000101);m.ref(0x24000,storage_base,0xff000102);
    m.put(0x40008,std::uint64_t(0x22000));m.put(0x40010,std::uint64_t(0x24000));m.put(0x10080,Collection{3,3,0x40000});
    auto ambiguous=capture(4,"ambiguous-anomaly.json");
    require(ambiguous.reason=="ambiguous_selection"&&ambiguous.beacons==1&&ambiguous.stores==2&&ambiguous.selected.size()==3,"retain all bounded ambiguous candidates");
    require(recorded==2&&!stopped&&queries==1,"ambiguity never guesses or queries a target");
    m.put(0x10080,Collection{2,2,0x40000});
    require(capture(5,"unused2.json").ok&&queries==2&&!stopped,"instrument survives ambiguity for fresh selection");
    m.data.erase(0x40000);
    capture(5,"unsafe-anomaly.json");
    require(stopped&&failure=="entry_read_failed"&&queries==2,"structural read failure is terminal and invokes no query");
    require(!fs::exists(root/L"unsafe-anomaly.json"),"unsafe reads are not labelled scientific anomaly");

    for(const char* reason:{"collection_changed","unstable_identity","player_or_load_changed","loading_before_task",
        "selection_time_budget","checkpoint_time_budget_after_query","nonfinite_transform","collection_scope_bound"}) {
        std::atomic<bool> alive{};bool persisted=false;
        require(record_issue(reason,alive,[&]{persisted=true;return true;},[](const std::string&){} )&&persisted&&!alive,"reviewed condition aborts task only");
    }
    for(const char* reason:{"loaded_site_mismatch","wrong_build","invalid_checkpoint_request","diagnostic_permission_marker_missing",
        "identity_read_or_structure_failed","collection_read_failed","collection_structure_failed","disk_space_low_C","disk_space_low_D","disk_space_read_failed"}) {
        std::atomic<bool> stop{};bool persisted=false;std::string why;
        require(!record_issue(reason,stop,[&]{persisted=true;return true;},[&](const std::string& v){why=v;})&&stop&&!persisted&&why==reason,"integrity/safety failures stay terminal");
    }
    std::atomic<bool> failed{};std::string why;
    require(!record_issue("ambiguous_selection",failed,[]{return false;},[&](const std::string& v){why=v;})&&failed&&why=="anomaly_persistence_failed","failed anomaly persistence is terminal");
    bool retried=false;
    require(!record_issue("collection_changed",failed,[&]{retried=true;return true;},[](const std::string&){} )&&!retried,"no observation after terminal failure");

    require(!disk_issue({true,minimum_free_bytes,minimum_free_bytes}),"40 GB inclusive boundary");
    require(std::string(disk_issue({true,minimum_free_bytes-1,minimum_free_bytes}))=="disk_space_low_C","C below threshold");
    require(std::string(disk_issue({true,minimum_free_bytes,minimum_free_bytes-1}))=="disk_space_low_D","D below threshold");
    require(std::string(disk_issue({false,minimum_free_bytes,minimum_free_bytes}))=="disk_space_read_failed","unknown free space fails closed");

    // Successful reads that disagree are distinct from unreadable repeated views.
    struct Mutating:Memory {unsigned reads{};bool unreadable{};bool bytes(std::uint64_t p,void* out,std::size_t n)override {
        if(p==0x20024&&++reads==2){if(unreadable)return false;put(0x2008c,std::array<float,3>{5,6,7});}
        return Memory::bytes(p,out,n);
    }} changing;
    changing.put(0x1002e,std::uint8_t(0x49));changing.put(0x10080,Collection{1,1,0x40000});changing.put(0x40000,std::uint64_t(0x20000));changing.ref(0x20000,beacon_base,0xff000100);
    auto unstable=select(changing,{0x10000},2);
    require(unstable.reason=="unstable_identity"&&unstable.has_recheck&&!unstable.counts_complete,"successful differing views retained as anomaly");
    require(write_new(root/L"unstable-anomaly.json",anomaly_json("A1",2,unstable.reason,unstable,0,2,"","SYNTHETIC")),"persist both unstable views");
    changing.reads=0;changing.unreadable=true;
    require(select(changing,{0x10000},2).reason=="identity_read_or_structure_failed","failed repeated view is structural failure");
    require(select(changing,{0x10000},2,[]{return true;}).reason=="selection_time_budget","time budget abandons scan without further access");
    struct HeaderChanging:Memory {unsigned reads{};bool unreadable{};bool bytes(std::uint64_t p,void* out,std::size_t n)override {
        if(p==0x10080&&++reads==2){if(unreadable)return false;put(0x10080,Collection{0,1,0x40000});}
        return Memory::bytes(p,out,n);
    }} headers;headers.data=changing.data;
    auto changed=select(headers,{0x10000},2);
    require(changed.reason=="collection_changed"&&scientific_anomaly(changed.reason)&&changed.selected.size()==1&&!changed.counts_complete,"successful changed collection is a bounded anomaly");
    require(write_new(root/L"collection-anomaly.json",anomaly_json("A1",2,changed.reason,changed,0,3,"","SYNTHETIC")),"persist safely obtained collection candidates");
    headers.reads=0;headers.unreadable=true;headers.put(0x10080,Collection{1,1,0x40000});
    require(select(headers,{0x10000},2).reason=="collection_read_failed","unreadable repeated collection is terminal");
    headers.reads=0;headers.put(0x10080,Collection{4097,4097,0x40000});
    auto scope=select(headers,{0x10000},2);
    require(scope.reason=="collection_scope_bound"&&scientific_anomaly(scope.reason)&&scope.scanned==0,"over-scope collection aborts without accessing array");
    headers.reads=0;headers.put(0x10080,Collection{1,1,0});
    require(select(headers,{0x10000},2).reason=="collection_structure_failed","nonempty null array remains unsafe");

    Memory many;many.put(0x1002e,std::uint8_t(0x49));many.put(0x10080,Collection{17,17,0x40000});
    for(unsigned i=0;i<17;i++){auto p=0x100000ULL+i*0x2000;many.ref(p,storage_base,0xff000100+i);many.put(0x40000ULL+i*8,p);}
    auto capped=select(many,{0x10000},4);
    require(capped.reason=="ambiguous_selection"&&capped.selected.size()==16&&capped.stores==17&&capped.candidates_truncated&&!capped.counts_complete,"candidate evidence cap with qualified lower-bound count");
    auto json=anomaly_json("A2",4,capped.reason,capped,0,9,"","SYNTHETIC");
    require(json.size()<max_checkpoint_bytes&&write_new(root/L"capped-anomaly.json",json),"bounded anomaly serialization");
    capped.selected[0].position[0]=NAN;
    require(write_new(root/L"nonfinite-anomaly.json",anomaly_json("A2",4,"nonfinite_transform",capped,0,9,"","SYNTHETIC")),"retain nonfinite observation as explicit JSON string");
}
