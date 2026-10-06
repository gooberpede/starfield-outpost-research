// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>
#include <functional>

namespace sor {
constexpr std::uint32_t beacon_base = 0x002c60e9, storage_base = 0x0023aed9;
constexpr std::uint32_t game_version = (1u << 24) | (16u << 16) | (244u << 4);
constexpr std::size_t max_references = 4096, max_checkpoint_bytes = 32768;
constexpr std::size_t max_anomaly_candidates=16;
inline constexpr std::array<const char*, 6> checkpoints{"A0", "A0C", "A1", "A1C", "A2", "A2R"};

// Newly authored byte-view contract, not a copied C++ engine class. Offsets are
// independently checked native operands; see STATIC-CONTRACT.md and local PE guards.
struct Identity {
    std::uint64_t pointer{}, base{}, cell{}, extra{};
    std::uint32_t id{}, base_id{}, candidate{};
    std::uint8_t type{};
    std::array<float, 3> position{}, rotation_raw{};
    bool operator==(const Identity&) const = default;
};
struct Collection {
    std::uint32_t count{}, capacity{};
    std::uint64_t data{};
    bool operator==(const Collection&) const = default;
};
static_assert(sizeof(Collection) == 16);

struct Reader {
    virtual bool bytes(std::uint64_t address, void* into, std::size_t size) = 0;
    template<class T> bool get(std::uint64_t address, T& into) { return bytes(address, &into, sizeof(into)); }
    virtual ~Reader() = default;
};

inline bool identity(Reader& read, std::uint64_t p, Identity& out, std::string* error=nullptr) {
    if(error)*error="identity_read_or_structure_failed";
    if (!p || p > 0x00007fffffffff00ULL || (p & 7)) return false;
    Identity a{}; a.pointer = p;
    if (!read.get(p+0x24,a.candidate) || !read.get(p+0x28,a.id) || !read.get(p+0x2e,a.type)
        || !read.get(p+0x80,a.rotation_raw) || !read.get(p+0x8c,a.position)
        || !read.get(p+0x98,a.base) || !read.get(p+0xb0,a.cell) || !read.get(p+0xc8,a.extra)) return false;
    if (!a.base || !read.get(a.base+0x28,a.base_id) || !a.id || (a.type != 0x4a && a.type != 0x4b)) return false;
    out=a;
    for (auto v:a.position) if (!std::isfinite(v)) {if(error)*error="nonfinite_transform";return false;}
    for (auto v:a.rotation_raw) if (!std::isfinite(v)) {if(error)*error="nonfinite_transform";return false;}
    out=a; return true;
}

struct Selection {
    bool ok{};
    std::string reason;
    std::vector<Identity> selected;
    std::uint32_t scanned{};
    std::uint32_t beacons{}, stores{};
    bool counts_complete{}, candidates_truncated{};
    Identity rechecked{};
    bool has_recheck{};
};

inline Selection select(Reader& read, const std::vector<std::uint64_t>& cells, std::size_t checkpoint,
                        std::function<bool()> time_expired=[] {return false;}) {
    Selection out;
    if(checkpoint>=checkpoints.size() || cells.empty() || cells.size()>2) {out.reason="invalid_selection_scope"; return out;}
    std::vector<std::uint64_t> seen;
    for (auto cell:cells) {
        std::uint8_t type{}; Collection before{}, after{};
        if (!cell || !read.get(cell+0x2e,type) || type!=0x49 || !read.get(cell+0x80,before)) {out.reason="cell_read_failed"; return out;}
        if(before.count && !before.data){out.reason="collection_structure_failed";return out;}
        if(before.count>max_references){out.reason="collection_scope_bound";return out;}
        for(std::uint32_t i=0;i<before.count;i++) {
            if(time_expired()){out.reason="selection_time_budget";return out;}
            std::uint64_t p{}, base{}; std::uint32_t id{};
            if(!read.get(before.data+std::uint64_t(i)*8,p)) {out.reason="entry_read_failed";return out;}
            ++out.scanned;
            if(!p) continue;
            if(!read.get(p+0x98,base) || !base || !read.get(base+0x28,id)) {out.reason="candidate_read_failed";return out;}
            if(id!=beacon_base && id!=storage_base) continue;
            bool duplicate=false; for(auto existing:seen) if(existing==p) duplicate=true;
            if(duplicate) continue;
            seen.push_back(p);
            out.beacons+=id==beacon_base;out.stores+=id==storage_base;
            if(out.selected.size()==max_anomaly_candidates){out.candidates_truncated=true;out.reason="ambiguous_selection";return out;}
            Identity item{}, repeat{};
            if(!identity(read,p,item,&out.reason)) {
                if(out.reason=="nonfinite_transform")out.selected.push_back(item);
                return out;
            }
            out.selected.push_back(item);
            if(item.base!=base||item.base_id!=id){out.reason="unstable_identity";return out;}
            if(!identity(read,p,repeat,&out.reason)) {
                if(out.reason=="nonfinite_transform"){out.rechecked=repeat;out.has_recheck=true;}
                return out;
            }
            if(item!=repeat){out.rechecked=repeat;out.has_recheck=true;out.reason="unstable_identity";return out;}
        }
        if(!read.get(cell+0x80,after)) {out.reason="collection_read_failed";return out;}
        if(before!=after) {out.reason="collection_changed";return out;}
    }
    out.counts_complete=true;
    auto need_beacon=checkpoint>=2 ? 1u:0u, need_store=checkpoint>=4 ? 1u:0u;
    if(out.beacons>1 || out.stores>1){out.reason="ambiguous_selection";return out;}
    if(out.beacons!=need_beacon || out.stores!=need_store) {out.reason="selected_counts_disagree";return out;}
    if(out.selected.size()==2 && out.selected[0].base_id==storage_base) std::swap(out.selected[0],out.selected[1]);
    out.ok=true; out.reason="selected"; return out;
}
inline bool request_matches(const std::string& bytes,std::size_t index) {
    return index<checkpoints.size() && bytes==std::string(checkpoints[index])+
        (index==5?"\nRELOADED_SETTLED\n":"\nSETTLED\n");
}
inline std::uint64_t runtime_address(std::uint64_t base,std::uint32_t rva,std::uint32_t image_size) {
    if(!base || (base&0xffff) || rva>=image_size || base+image_size>0x800000000000ULL) return 0;
    return base+rva;
}
}
