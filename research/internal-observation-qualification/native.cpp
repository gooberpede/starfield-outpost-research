// SPDX-License-Identifier: GPL-3.0-or-later
// Original, disposable process only. No handles to other processes or game APIs.
#include <windows.h>
#include <intrin.h>
#include <atomic>
#include <array>
#include <thread>
#include <vector>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <chrono>

extern "C" void probe(void*, void*, unsigned long long);
extern "C" void accept_site(), reject_site(), accept_resume(), reject_resume(), disturb();
void capture_terminal(unsigned,unsigned,const void*);
void geometry_tests();
struct alignas(64) Snapshot { unsigned char bytes[3072]; };
static std::atomic<unsigned> hits{}, nested{}, invalid{}, live{}, maxlive{};
static std::atomic<bool> admitting{true};
static thread_local unsigned depth{};
static thread_local bool inject_nested{}, inject_interrupt{};
static thread_local unsigned callbacks{};
static std::atomic<unsigned> failures{}, x87_pointer_losses{};
static void check(bool value, const char* label) {
    if (!value) { std::fprintf(stderr,"FAIL %s\n",label); ++failures; }
}
static void interrupt_capture() {
    __try { RaiseException(0xe0420001,0,0,nullptr); }
    __except(GetExceptionCode()==0xe0420001 ? EXCEPTION_EXECUTE_HANDLER : EXCEPTION_CONTINUE_SEARCH) {
        ++invalid;
    }
}
static LONG CALLBACK handler(EXCEPTION_POINTERS* e) {
    if (e->ExceptionRecord->ExceptionCode != EXCEPTION_BREAKPOINT) return EXCEPTION_CONTINUE_SEARCH;
    auto site = e->ExceptionRecord->ExceptionAddress;
    if (site != reinterpret_cast<void*>(accept_site) && site != reinterpret_cast<void*>(reject_site))
        return EXCEPTION_CONTINUE_SEARCH;
    auto saved_error = GetLastError();
    auto active = ++live;
    unsigned old = maxlive;
    while (old < active && !maxlive.compare_exchange_weak(old,active)) {}
    ++depth; ++hits;
    if (admitting) {
        ++callbacks;
        if (inject_nested && depth == 1) {
            Snapshot child{}; unsigned long long closure[2]{0,0x22334455};
            probe(&child,closure,0); ++nested;
        }
        if (inject_interrupt) interrupt_capture();
        capture_terminal(site==reinterpret_cast<void*>(accept_site) ? 1 : 2,depth,
                         reinterpret_cast<void*>(e->ContextRecord->Rsi));
    }
    e->ContextRecord->Rip = reinterpret_cast<DWORD64>(
        site == reinterpret_cast<void*>(accept_site) ? accept_resume : reject_resume);
    --depth; --live;
    SetLastError(saved_error);
    // Deliberately destroy volatile GPR/SIMD, AVX upper halves, x87 and MXCSR.
    // This is an adversarial fixture, not a reusable ABI-compliant helper.
    disturb();
    return EXCEPTION_CONTINUE_EXECUTION;
}
static unsigned char originals[2];
static void patch(bool install) {
    void* sites[]{reinterpret_cast<void*>(accept_site),reinterpret_cast<void*>(reject_site)};
    for (unsigned i=0;i<2;++i) {
        DWORD protection{};
        check(VirtualProtect(sites[i],1,PAGE_EXECUTE_READWRITE,&protection)!=0,"own fixture protection");
        auto p=static_cast<unsigned char*>(sites[i]);
        if (install) { originals[i]=*p; *p=0xcc; } else *p=originals[i];
        check(FlushInstructionCache(GetCurrentProcess(),p,1)!=0,"own cache flush");
        DWORD ignored{};
        check(VirtualProtect(p,1,protection,&ignored)!=0,"own protection restore");
    }
}
static void compare(Snapshot& s, unsigned mode) {
    auto a=s.bytes; auto b=a+1536;
    // GPRs and RSP except RBX, whose displaced original effect is checked separately.
    for(unsigned i=0;i<16;++i) if(i!=1) check(!std::memcmp(a+8*i,b+8*i,8),"GPR/RSP");
    unsigned long long before{},after{};
    std::memcpy(&before,a+8,8); std::memcpy(&after,b+8,8);
    check(after==(mode ? 0x22334455ull : before+0x30),"displaced result");
    unsigned long long flags{}; std::memcpy(&flags,b+128,8);
    // Reject ADD must produce PF=1, other arithmetic flags clear for chosen RBX.
    check((flags&0x8d5)==(mode==2 ? 0 : mode ? (0xad7&0x8d5) : 4),"displaced flags");
    check(!std::memcmp(a+160,b+160,512),"all YMM lanes");
    // Reserved bytes are ignored. Observable x87 pointers are separately tested
    // and excluded only from the explicitly scoped SSE/AVX qualification.
    // Native mapped path is SSE/AVX. Preserve the extra x87 diagnostic failure:
    // Windows exception continuation loses high x87 instruction-pointer bits.
    if (std::memcmp(a+712,b+712,16)) ++x87_pointer_losses;
    check(!std::memcmp(a+704,b+704,8),"x87 control/status/tag");
    check(!std::memcmp(a+728,b+728,8),"MXCSR");
    check(!std::memcmp(a+736,b+736,128),"x87 stack");
    check(!std::memcmp(a+864,b+864,256),"all XMM lanes");
}
static void run(unsigned mode) {
    Snapshot state{}; unsigned long long closure[2]{0,0x22334455};
    auto mxcsr=_mm_getcsr();
    _mm_setcsr(mode==2 ? 0xffc0 : mode==1 ? 0x3f80 : 0x1f80);
    SetLastError(0x13579);
    probe(&state,closure,mode);
    check(GetLastError()==0x13579,"LastError"); compare(state,mode);
    _mm_setcsr(mxcsr);
}
int main() {
    int cpu[4]{}; __cpuid(cpu,1);
    check((cpu[2]&(1<<27)) && (cpu[2]&(1<<28)) && ((_xgetbv(0)&6)==6),"AVX OS support");
    for(unsigned mode=0;mode<3;++mode) run(mode);
    auto h=AddVectoredExceptionHandler(1,handler); check(h!=nullptr,"VEH");
    patch(true);
    for(unsigned mode=0;mode<3;++mode) run(mode);
    inject_nested=true; run(1); inject_nested=false;
    inject_interrupt=true; run(0); inject_interrupt=false;
    if(failures) { admitting=false; patch(false); RemoveVectoredExceptionHandler(h); return 2; }
    auto start=std::chrono::steady_clock::now();
    std::array<std::thread,4> workers;
    for(auto& t:workers) t=std::thread([] { for(unsigned i=0;i<250;++i) run(i%3); });
    for(auto& t:workers) t.join();
    auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now()-start).count();
    geometry_tests();
    // Cooperative STOP disables evidence admission, but handlers/continuations remain.
    std::atomic<bool> exit_workers{false}; auto initial=hits.load();
    for(auto& t:workers) t=std::thread([&] {
        while(!exit_workers) run(1);
        auto calls=callbacks; run(1); check(callbacks==calls,"STOP worker admission");
    });
    while(hits<initial+100) std::this_thread::yield();
    admitting=false; exit_workers=true;
    for(auto& t:workers) t.join();
    auto calls=callbacks; run(1); check(callbacks==calls,"STOP admission");
    check(live==0,"joined quiescence");
    // Never patch/unregister while workers can execute the sites.
    patch(false); check(RemoveVectoredExceptionHandler(h)!=0,"retirement");
    for(unsigned mode=0;mode<3;++mode) run(mode);
    std::printf("{\"mapped_sse_avx_state\":\"%s\",\"x87_full_environment\":\"%s\",\"x87_pointer_losses\":%u,\"hits\":%u,\"nested\":%u,\"invalid_interruptions\":%u,\"max_concurrent\":%u,\"threaded_1000_ns\":%lld}\n",
                failures ? "FAIL":"PASS",x87_pointer_losses ? "FAIL":"PASS",x87_pointer_losses.load(),
                hits.load(),nested.load(),invalid.load(),maxlive.load(),ns);
    return failures ? 2 : 0;
}
