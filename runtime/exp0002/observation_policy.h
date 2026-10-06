// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "win_support.h"
#include <atomic>

namespace sor {
// Fail closed for unclassified reasons; anomalies abort only the current task.
inline bool scientific_anomaly(const std::string& reason) {
    for(const char* value:{"selected_counts_disagree","ambiguous_selection","collection_changed",
        "unstable_identity","nonfinite_transform","player_or_load_changed","loading_before_task",
        "selection_time_budget","checkpoint_time_budget_after_query","selected_identity_changed_before_query",
        "reference_changed_during_queries","final_snapshot_load_changed","player_context_unavailable",
        "exterior_context_unavailable","collection_scope_bound","player_context_changed","cell_context_changed"})if(reason==value)return true;
    return false;
}
template<class Report>
bool selected_or_report(const Selection& selection,Report report) {
    if(selection.ok)return true;
    report(selection.reason);return false;
}

// Shared production/test dispatch: only durable anomalies may advance to the
// next explicit checkpoint. Never call the query path after any failed selection.
template<class Persist, class Failure>
bool record_issue(const std::string& reason,std::atomic<bool>& stopped,Persist persist,Failure failure) {
    if(stopped)return false;
    if(!scientific_anomaly(reason)){stopped=true;failure(reason);return false;}
    if(!persist()){stopped=true;failure("anomaly_persistence_failed");return false;}
    return !stopped;
}

constexpr std::uint64_t minimum_free_bytes=40000000000ULL; // 40 decimal GB, each drive
struct DiskSpace {bool known{};std::uint64_t c{},d{};};
inline const char* disk_issue(const DiskSpace& space) {
    if(!space.known)return "disk_space_read_failed";
    if(space.c<minimum_free_bytes)return "disk_space_low_C";
    if(space.d<minimum_free_bytes)return "disk_space_low_D";
    return nullptr;
}
inline DiskSpace disk_space() {
    ULARGE_INTEGER c{},d{};
    bool a=GetDiskFreeSpaceExW(L"C:\\",&c,nullptr,nullptr)!=0;
    bool b=GetDiskFreeSpaceExW(L"D:\\",&d,nullptr,nullptr)!=0;
    return {a&&b,c.QuadPart,d.QuadPart};
}

inline std::string observed_vector(const std::array<float,3>& values) {
    std::ostringstream s;s<<'[';
    for(std::size_t i=0;i<3;i++){if(i)s<<',';if(std::isfinite(values[i]))s<<std::setprecision(9)<<values[i];
        else s<<quote(std::isnan(values[i])?"NaN":values[i]>0?"+Infinity":"-Infinity");}
    return s.str()+']';
}
inline std::string copied_identity(const Identity& a) {
    return "{\"pointer\":"+quote(hex(a.pointer))+",\"form_id\":"+quote(hex(a.id,8))+",\"base_pointer\":"+quote(hex(a.base))+
        ",\"base_form_id\":"+quote(hex(a.base_id,8))+",\"stored_cell\":"+quote(hex(a.cell))+",\"extra\":"+quote(hex(a.extra))+
        ",\"native_handle_candidate\":"+quote(hex(a.candidate,8))+",\"type\":"+std::to_string(a.type)+
        ",\"position\":"+observed_vector(a.position)+",\"rotation_raw\":"+observed_vector(a.rotation_raw)+'}';
}
// Serialize copies only: no new reference dereference while recording anomaly.
inline std::string anomaly_json(const char* checkpoint,std::size_t expected_stage,const std::string& reason,
                               const Selection& observed,unsigned calls,std::uint64_t elapsed,
                               const std::string& provenance,const char* kind="RUNTIME") {
    std::ostringstream s;
    s<<"{\"schema\":\"SOR-EXP-0002-anomaly-v1\",\"kind\":"<<quote(kind)<<",\"checkpoint\":"<<quote(checkpoint)
     <<",\"reason\":"<<quote(reason)<<",\"utc\":"<<quote(utc())<<",\"expected_counts\":{\"beacon\":"<<(expected_stage>=2?1:0)
     <<",\"storage\":"<<(expected_stage>=4?1:0)<<"},\"observed_counts\":{\"beacon\":"<<observed.beacons<<",\"storage\":"<<observed.stores
     <<"},\"counts_complete\":"<<(observed.counts_complete?"true":"false")<<",\"candidates_truncated\":"<<(observed.candidates_truncated?"true":"false")
     <<",\"scanned_entries\":"<<observed.scanned<<",\"queries_invoked\":"<<calls<<",\"elapsed_ms\":"<<elapsed
     <<",\"snapshot_atomic\":false,\"candidates\":[";
    for(std::size_t i=0;i<observed.selected.size()&&i<max_anomaly_candidates;i++) {
        if(i)s<<',';const auto& a=observed.selected[i];
        s<<"{\"pointer\":"<<quote(hex(a.pointer))<<",\"form_id\":"<<quote(hex(a.id,8))<<",\"base_pointer\":"<<quote(hex(a.base))
         <<",\"base_form_id\":"<<quote(hex(a.base_id,8))<<",\"stored_cell\":"<<quote(hex(a.cell))<<",\"extra\":"<<quote(hex(a.extra))
         <<",\"native_handle_candidate\":"<<quote(hex(a.candidate,8))<<",\"type\":"<<unsigned(a.type)
         <<",\"position\":"<<observed_vector(a.position)<<",\"rotation_raw\":"<<observed_vector(a.rotation_raw)<<'}';
    }
    s<<"],\"rechecked_identity\":";
    if(observed.has_recheck) {
        const auto& a=observed.rechecked;
        s<<"{\"pointer\":"<<quote(hex(a.pointer))<<",\"form_id\":"<<quote(hex(a.id,8))<<",\"base_form_id\":"<<quote(hex(a.base_id,8))
         <<",\"stored_cell\":"<<quote(hex(a.cell))<<",\"position\":"<<observed_vector(a.position)<<",\"rotation_raw\":"<<observed_vector(a.rotation_raw)<<'}';
    }else s<<"null";
    s<<provenance<<",\"terminal\":\"ANOMALY_RECORDED\",\"instrument_available\":true}\n";return s.str();
}
}
