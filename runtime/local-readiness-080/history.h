// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "../exp0002/win_support.h"
#include <atomic>
#include <intrin.h>
#include <immintrin.h>
#include <TlHelp32.h>

namespace history {
using namespace sor;
constexpr uint64_t disk_floor=40'000'000'000ULL;
inline std::atomic<bool> fixture_disk_query_failure{false}; // never set by plugin
inline bool disk(size_t reserve=0){ULARGE_INTEGER c{},d{};return !fixture_disk_query_failure&&reserve<=UINT64_MAX-disk_floor&&GetDiskFreeSpaceExW(L"C:\\",&c,nullptr,nullptr)&&GetDiskFreeSpaceExW(L"D:\\",&d,nullptr,nullptr)&&c.QuadPart>=disk_floor&&d.QuadPart>=disk_floor+reserve;}
struct Environment {
    DWORD error=GetLastError();alignas(16) unsigned char fp[512];
    Environment(){_fxsave64(fp);}~Environment(){_fxrstor64(fp);SetLastError(error);}
};
struct Blob {uint64_t address{};uint32_t length{},ok{};unsigned char bytes[0x180]{};};
#ifdef SOR_FIXTURE
inline std::atomic<uint64_t> fixture_reads{};
#define SOR_COUNT_READ ++fixture_reads;
#else
#define SOR_COUNT_READ
#endif
inline bool copy(Blob& b,uint64_t p,size_t n){SOR_COUNT_READ b.address=p;b.length=static_cast<uint32_t>(n);SIZE_T got{};b.ok=0;memset(b.bytes,0,sizeof b.bytes);if(p>=0x10000&&p<=0x7fffffffffffULL&&n&&n<=sizeof b.bytes&&n-1<=0x7fffffffffffULL-p)b.ok=ReadProcessMemory(GetCurrentProcess(),reinterpret_cast<void*>(p),b.bytes,n,&got)&&got==n;return b.ok!=0;}
template<class T>T field(const Blob& b,size_t off){T v{};if(b.ok&&off+sizeof v<=b.length)memcpy(&v,b.bytes+off,sizeof v);return v;}
inline uint64_t pointer(uint64_t p){Blob b;copy(b,p,8);return field<uint64_t>(b,0);}
// Flat fixed-width records; every scalar is little endian. Blobs own snapshots.
struct Event {
    uint64_t sequence{},invocation{},parent{},thread{},qpc{},site{},kind{},phase{},reference{},command{},result{},status{};
    uint64_t args[4]{};
    Blob ref,base,extra,cell,world,operand,aux,output;
};
static_assert(sizeof(Blob)==400);static_assert(sizeof(Event)==3328);
enum Kind:uint64_t{replace=1,convert=2,apply=3,producer=4,enqueue=5,submission=6,application=7,center=8,allocation=9,restoration=10};
enum Phase:uint64_t{before=1,after=2,unwind=3};
inline void snapshot(Event& e){
    copy(e.ref,e.reference,0xd8);
    if(!e.ref.ok)return;
    copy(e.base,field<uint64_t>(e.ref,0x98),0x30);copy(e.cell,field<uint64_t>(e.ref,0xb0),0x118);
    if(e.cell.ok&&!(field<uint32_t>(e.cell,0x48)&1))copy(e.world,field<uint64_t>(e.cell,0x110),0x180);
    auto list=field<uint64_t>(e.ref,0xc8),node=pointer(list+8);uint64_t seen[64]{};
    for(unsigned i=0;node&&i<64;++i){bool cycle=false;for(unsigned j=0;j<i;++j)cycle|=seen[j]==node;if(cycle){e.status|=1;break;}seen[i]=node;Blob h;if(!copy(h,node,0x18)){e.status|=2;break;}if(h.bytes[0x12]==0xbc){copy(e.extra,node,0xa0);break;}node=field<uint64_t>(h,8);if(i==63&&node)e.status|=4;}
    Blob again;copy(again,e.reference,0xd8);if(!again.ok||memcmp(again.bytes,e.ref.bytes,0xd8))e.status|=8;
}
// Fixed preallocated queue. Callback threads only lock-free SLIST/copy; no file I/O,
// allocations, waits, hashing or disk queries. Queue overflow is sticky
// instrumentation failure, not a sampled suffix. Only the worker drains/writes.
struct Spool {
    static constexpr size_t capacity=4096;
    struct alignas(16) Node { SLIST_ENTRY link;Event event; };
    SLIST_HEADER free_list,pending;HANDLE raw=INVALID_HANDLE_VALUE,journal=INVALID_HANDLE_VALUE;
    std::atomic<uint64_t> attempted{},captured{},durable{},failed{},active{},next_invocation{},queued{},losses{};
    std::atomic<bool> stopping{false},broken{false};uint64_t offset{};fs::path root;
    Node nodes[capacity]{};uint64_t fail_sequence{};
    Spool(){InitializeSListHead(&free_list);InitializeSListHead(&pending);for(auto& n:nodes)InterlockedPushEntrySList(&free_list,&n.link);}
    bool open(const fs::path& p){root=p;raw=CreateFileW((p/L"events.bin").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);journal=CreateFileW((p/L"records.jsonl").c_str(),GENERIC_WRITE,FILE_SHARE_READ,nullptr,CREATE_NEW,FILE_ATTRIBUTE_NORMAL,nullptr);return raw!=INVALID_HANDLE_VALUE&&journal!=INVALID_HANDLE_VALUE;}
    static bool append(HANDLE f,const void* p,size_t n){DWORD got{};return n<=MAXDWORD&&WriteFile(f,p,static_cast<DWORD>(n),&got,nullptr)&&got==n&&FlushFileBuffers(f);}
    static bool cached(HANDLE f,const void* p,size_t n){DWORD got{};return n<=MAXDWORD&&WriteFile(f,p,static_cast<DWORD>(n),&got,nullptr)&&got==n;}
    void fault(){++failed;++losses;broken=true;stopping=true;}
    bool emit(Event& e){
        ++attempted;if(broken){fault();return false;}
        auto* entry=InterlockedPopEntrySList(&free_list);
        if(!entry){fault();return false;}
        auto* n=reinterpret_cast<Node*>(entry);n->event=e;
        ++queued;InterlockedPushEntrySList(&pending,&n->link);return true;
    }
    bool enter(){++active;if(stopping||broken){--active;return false;}return true;}
    bool flush(){
        // Detach one bounded batch. Reverse publication stack to FIFO for
        // that batch. Persistent sequence is writer order, NOT call admission.
        auto* batch=InterlockedFlushSList(&pending);SLIST_ENTRY* fifo=nullptr;
        while(batch){auto* next=batch->Next;batch->Next=fifo;fifo=batch;batch=next;}
        while(fifo){auto* n=reinterpret_cast<Node*>(fifo);fifo=fifo->Next;
            Event e=n->event;e.sequence=captured.load()+1;
            auto hash=sha_bytes(&e,sizeof e);auto line="{\"sequence\":"+std::to_string(e.sequence)+",\"offset\":"+std::to_string(offset)+",\"length\":"+std::to_string(sizeof e)+",\"sha256\":"+quote(hash)+"}\n";
            if(e.sequence==fail_sequence||hash.size()!=64||!disk(sizeof e+line.size())||!cached(raw,&e,sizeof e)||!cached(journal,line.data(),line.size())){fault();return false;}
            offset+=sizeof e;captured=e.sequence;--queued;InterlockedPushEntrySList(&free_list,&n->link);
        }
        if(!disk()||!FlushFileBuffers(raw)||!FlushFileBuffers(journal)){fault();return false;}
        durable=captured.load();return true;
    }
    void stop(){stopping=true;}
    std::string counts(){return "\"attempted\":"+std::to_string(attempted.load())+",\"captured\":"+std::to_string(captured.load())+",\"last_durable_sequence\":"+std::to_string(durable.load())+",\"failed\":"+std::to_string(failed.load())+",\"active\":"+std::to_string(active.load())+",\"queued\":"+std::to_string(queued.load())+",\"losses\":"+std::to_string(losses.load())+",\"offset\":"+std::to_string(offset)+",\"integrity_failure\":"+(broken?"true":"false");}
    void close(){if(raw!=INVALID_HANDLE_VALUE){CloseHandle(raw);raw=INVALID_HANDLE_VALUE;}if(journal!=INVALID_HANDLE_VALUE){CloseHandle(journal);journal=INVALID_HANDLE_VALUE;}}
};
inline Spool spool;
struct Scope;inline thread_local Scope* current{};
struct Scope {
    Scope* outer{};bool entered{};Event event;
    Scope(uint64_t site,Kind k,uint64_t a,uint64_t b,uint64_t c,uint64_t d){
        Environment env;entered=spool.enter();if(!entered)return;outer=current;current=this;
        event.invocation=++spool.next_invocation;event.parent=outer?outer->event.invocation:0;event.site=site;event.kind=k;event.args[0]=a;event.args[1]=b;event.args[2]=c;event.args[3]=d;
        event.reference=k==enqueue?b:a;if(k==allocation)event.reference=outer?outer->event.reference:0;if(k==submission){event.command=b;copy(event.aux,b,0x30);event.reference=field<uint64_t>(event.aux,0x20);}if(k==application){event.command=c>=0x10?c-0x10:0;copy(event.aux,event.command,0x30);}
        capture(before,0);
    }
    __declspec(noinline) void capture(Phase p,uint64_t r){
        if(!entered)return;event.phase=p;event.result=r;event.thread=GetCurrentThreadId();LARGE_INTEGER q{};QueryPerformanceCounter(&q);event.qpc=q.QuadPart;
        event.ref={};event.base={};event.extra={};event.cell={};event.world={};event.operand={};event.output={};event.status=0;snapshot(event);
        auto k=event.kind;auto* a=event.args;
        if(k==replace||k==restoration||k==convert||k==apply)copy(event.operand,a[1],k==apply?16:12);
        if(k==producer)copy(event.operand,a[2],12);if(k==enqueue)copy(event.operand,a[3],12);
        if(k==submission||k==application){copy(event.aux,event.command,0x30);copy(event.operand,event.command+0x10,12);}
        if(k==allocation&&p==after){event.command=r;copy(event.output,r,0x30);}
        if(k==center)copy(event.output,a[1],12);
        spool.emit(event);
    }
    void finish(bool abnormal,uint64_t r){Environment env;if(entered){capture(abnormal?unwind:after,r);current=outer;--spool.active;entered=false;}}
};
using Four=uint64_t(*)(uint64_t,uint64_t,uint64_t,uint64_t);
// The audited targets use integer/pointer arguments only, at most four. The
// wrapper forwards R8/R9 even for superficially two-argument writers.
template<unsigned Site,Kind K> uint64_t invoke(Four original,uint64_t a,uint64_t b,uint64_t c,uint64_t d){Scope s(Site,K,a,b,c,d);uint64_t r{};__try{r=original(a,b,c,d);}__finally{s.finish(AbnormalTermination()!=0,r);}return r;}
}
