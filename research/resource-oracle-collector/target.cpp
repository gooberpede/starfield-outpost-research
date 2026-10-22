// SPDX-License-Identifier: GPL-3.0-or-later
#include "fixture.h"
#include <cstring>
static volatile LONG64 sequence = 0, sink = 0;
static const char* mode;
static void evaluate(Evaluation& e);
extern "C" __declspec(dllexport) __declspec(noinline) void sample_decision(Evaluation* e);
extern "C" __declspec(dllexport) __declspec(noinline) void sample_refresh(Evaluation* e) {
    InterlockedAdd64(&sink, e->result + 1);
    Evaluation nested=*e;
    nested.depth=3; nested.selector=1; nested.produced=101;
    evaluate(nested); nested.sequence=InterlockedIncrement64(&sequence);
    sample_decision(&nested); // actually executes while the refresh marker's frame is live
}
extern "C" __declspec(dllexport) __declspec(noinline) void sample_retained(Evaluation* e) {
    InterlockedAdd64(&sink, e->result + 1);
}
extern "C" __declspec(dllexport) __declspec(noinline) void sample_decision(Evaluation* e) {
    InterlockedAdd64(&sink, e->result + 1);
}
static void stamp(Evaluation& e) { e.sequence = InterlockedIncrement64(&sequence); }
static void evaluate(Evaluation& e) {
    e.result = 0;
    auto p = reinterpret_cast<Resource**>(e.populations[e.selector].begin);
    auto end = reinterpret_cast<Resource**>(e.populations[e.selector].end);
    for (; p != end; ++p) if ((*p)->id == e.produced) e.result = 1;
}
static void nested(Evaluation e, uint64_t depth) {
    e.depth = depth;
    if (depth) nested(e, depth - 1);
    e.selector = depth % 3; e.produced = depth==0 ? 101 : depth==1 ? 303 : 202;
    evaluate(e); stamp(e); sample_decision(&e);
    if (!strcmp(mode,"threads")) Sleep(1); // expose cross-worker scheduling between samples
}
static DWORD WINAPI worker(void* arg) {
    Resource a{101,0x9f}, b{202,0x9f}, c{303,0x9f};
    Resource* spatial[]{&a,&b,&a}; // intentional duplicate pointer
    Resource* atmosphere[]{&c};
    Resource* biome[]{&b,&c};
    Evaluation e{}; e.magic=MAGIC; e.visit=reinterpret_cast<uint64_t>(arg);
    Resource** arrays[]{spatial,atmosphere,biome}; size_t counts[]{3,1,2};
    for (size_t i=0;i<3;++i) {
        e.populations[i] = {reinterpret_cast<uint64_t>(arrays[i]),
            reinterpret_cast<uint64_t>(arrays[i]+counts[i]),
            reinterpret_cast<uint64_t>(arrays[i]+counts[i])};
    }
    e.selector=0; e.produced=101;
    if (!strcmp(mode,"zero")) e.populations[0].end=e.populations[0].begin;
    evaluate(e); e.branch=1; stamp(e); sample_refresh(&e);
    if (!strcmp(mode,"threads")) Sleep(1);
    e.branch=2; stamp(e); sample_retained(&e);
    if (!strcmp(mode,"threads")) Sleep(1);
    nested(e,2);
    // Corruption follows valid observations; never execute a filter on bad storage.
    if (!strcmp(mode,"bad-pointer")) e.populations[0]={8,16,16};
    if (!strcmp(mode,"bad-count")) e.populations[0].capacity=e.populations[0].begin;
    if (!strcmp(mode,"overflow")) e.populations[0]={0xfffffffffffffff8ULL,0,8};
    if (!strcmp(mode,"budget")) e.populations[0]={8,8+4097*8,8+4097*8};
    void* pages=nullptr;
    if (!strcmp(mode,"truncated") || !strcmp(mode,"truncated-resource")) {
        pages=VirtualAlloc(nullptr,8192,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);
        if (!pages) return 9;
        DWORD old; VirtualProtect(static_cast<char*>(pages)+4096,4096,PAGE_NOACCESS,&old);
        auto start=reinterpret_cast<uint64_t>(pages)+4096-8;
        *reinterpret_cast<Resource**>(start)=&a;
        if (!strcmp(mode,"truncated-resource")) {
            // Valid pointer array, but the pointed-to Resource crosses into PAGE_NOACCESS.
            spatial[0]=reinterpret_cast<Resource*>(static_cast<char*>(pages)+4096-4);
            e.populations[0].end=e.populations[0].begin+8;
        } else e.populations[0]={start,start+16,start+16};
    }
    if (strcmp(mode,"good") && strcmp(mode,"zero") && strcmp(mode,"threads") &&
        strcmp(mode,"crash-after") && strcmp(mode,"crash-before")) {
        e.branch=2; stamp(e); sample_retained(&e);
    }
    if (pages) VirtualFree(pages,0,MEM_RELEASE);
    return 0;
}
int main(int argc,char** argv) {
    mode=argc==2?argv[1]:"good";
    if (!strcmp(mode,"crash-before")) RaiseException(0xe043c1c0,EXCEPTION_NONCONTINUABLE,0,nullptr);
    if (!strcmp(mode,"threads")) {
        HANDLE threads[3];
        for (uint64_t i=0;i<3;++i) threads[i]=CreateThread(nullptr,0,worker,reinterpret_cast<void*>(i+1),0,nullptr);
        for (auto t:threads) if (!t) return 8;
        WaitForMultipleObjects(3,threads,TRUE,INFINITE);
        for (auto t:threads) CloseHandle(t);
    } else { worker(reinterpret_cast<void*>(1)); worker(reinterpret_cast<void*>(2)); }
    if (!strcmp(mode,"crash-after")) RaiseException(0xe043c1c1,EXCEPTION_NONCONTINUABLE,0,nullptr);
    return 0;
}
