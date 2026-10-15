// SPDX-License-Identifier: GPL-3.0-or-later
// Original finite fixture protocol. All storage allocated before admission.
#pragma once
#include <windows.h>
#include <atomic>
#include <cstdint>
#include <cstring>
#include <intrin.h>

namespace capture {
constexpr unsigned max_points=8192, max_uses=64;
enum Status : uint32_t { complete=1, incomplete=2, not_evaluated=3 };
enum Reason : uint32_t { none=0, capacity=1, read_failed=2, coherence=3,
    stopped=4, no_verdict=5, ancestry=6, changing_use=7, interrupted=8, use_capacity=9,
    mutation=10, lifecycle=11 };
#pragma pack(push,1)
struct Point { float x,y,z,w; };
struct Use {
    uint32_t ordinal, kind;
    float indexed[3], translation[3], resolved[3], radius, upper;
    uint32_t index; uint64_t domain;
};
struct Header {
    uint32_t magic=0x31514f53, version=1, status=incomplete, reason=none;
    uint64_t token=0,parent=0,thread=0,query=0,source=0,region=0;
    uint32_t case_id=0,count=0,bytes=0,uses=0,verdict=2,terminal=0;
    float center[3]{}; float radius=10;
    uint32_t mxcsr=0x1f80;
};
#pragma pack(pop)
struct Record { Header h; Point points[max_points]; Use uses[max_uses]; };
struct Source {
    std::atomic_flag lease=ATOMIC_FLAG_INIT;
    const Point* points{}; uint64_t count{};
    bool certified=true;
    uint64_t version=0;
    void (*during_copy)(Source&)=nullptr; // failure injection only; null in normal capture
};
inline std::atomic<uint64_t> next_token{1};
inline std::atomic<bool> stopping{false}, overflow{false};
// SEH helper is deliberately POD-only. Never dereference source on the worker.
inline bool read(void* dst,const void* src,size_t bytes) {
    __try { if(bytes) std::memcpy(dst,src,bytes); return true; }
    __except(EXCEPTION_EXECUTE_HANDLER) { return false; }
}
struct Group {
    Record& r; Source& source; bool held=false, begun=false, closed=false, terminal_seen=false;
    Group(Record& out,Source& in):r(out),source(in) {}
    void fail(Reason why) { r.h.status=incomplete; r.h.reason=why; }
    void begin(unsigned case_id,uint64_t parent=0) {
        r.h=Header{}; r.h.case_id=case_id; r.h.token=next_token++;
        r.h.mxcsr=_mm_getcsr();
        r.h.parent=parent; r.h.thread=GetCurrentThreadId();
        r.h.query=r.h.token; r.h.source=case_id+100; r.h.region=case_id+200;
        if(stopping) { r.h.status=not_evaluated; r.h.reason=stopped; return; }
        begun=true;
        if(!source.certified) { fail(coherence); return; }
        if(source.lease.test_and_set(std::memory_order_acquire)) { fail(coherence); return; }
        held=true;
        if(source.count>UINT32_MAX || source.count>max_points) {
            overflow=true; fail(capacity); return;
        }
        r.h.count=static_cast<uint32_t>(source.count); r.h.bytes=r.h.count*sizeof(Point);
        auto version=source.version;
        auto half=r.h.bytes/32*16;
        if(!read(r.points,source.points,half)) { r.h.bytes=0; fail(read_failed); return; }
        if(source.during_copy) source.during_copy(source);
        if(!read(reinterpret_cast<char*>(r.points)+half,
                 reinterpret_cast<const char*>(source.points)+half,r.h.bytes-half)) {
            r.h.bytes=0; fail(read_failed); return;
        }
        if(version!=source.version) fail(mutation);
    }
    void use(const Use& use) {
        if(r.h.reason) return;
        if(closed || terminal_seen) { fail(lifecycle); return; }
        if(!begun || r.h.reason) return;
        if(r.h.uses==max_uses) { overflow=true; fail(use_capacity); return; }
        if(use.ordinal!=r.h.uses) { fail(ancestry); return; }
        r.uses[r.h.uses++]=use;
    }
    void finish(uint64_t token,unsigned terminal) {
        if(r.h.reason) return;
        if(closed || terminal_seen) { fail(lifecycle); return; }
        if(!begun || r.h.reason) return;
        terminal_seen=true;
        if(stopping) { fail(stopped); return; }
        if(token!=r.h.token || (terminal!=1 && terminal!=2)) { fail(ancestry); return; }
        r.h.terminal=terminal; r.h.verdict=terminal==1 ? 1 : 0;
        if(!r.h.uses) { fail(ancestry); return; }
        // A single-query evaluator requires equality at every supplied actual-use site.
        for(unsigned i=1;i<r.h.uses;++i)
            if(std::memcmp(r.uses[0].resolved,r.uses[i].resolved,5*sizeof(float))) {
                fail(changing_use); return;
            }
        r.h.status=complete;
    }
    void close() {
        if(closed) return;
        if(begun && !r.h.reason && r.h.status!=complete) fail(no_verdict);
        if(held) { source.lease.clear(std::memory_order_release); held=false; }
        closed=true;
    }
    ~Group() { close(); }
};
} // namespace capture
