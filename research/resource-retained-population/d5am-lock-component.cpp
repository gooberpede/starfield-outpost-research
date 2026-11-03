// SPDX-License-Identifier: GPL-3.0-or-later
// Owned offline DLL with no SFSE entry. It observes only disposable native pages.
#include "../../runtime/construction-winner/d5am_lock_edges.h"
extern "C" {
__declspec(dllexport) void D5AM_collect(uint64_t lock,uint64_t old,uint64_t kind) noexcept {d5am::collect(lock,old,kind);}
__declspec(dllexport) void D5AM_initialize(uint64_t lock,uint64_t generation) noexcept {d5am::initialize(lock,generation);}
__declspec(dllexport) unsigned D5AM_pop(d5am::Event* out) noexcept {return d5am::pop(*out);}
__declspec(dllexport) uint64_t D5AM_metric(unsigned which) noexcept {
 using namespace d5am;
 switch(which){case 0:return drops;case 1:return failed;case 2:return active;case 3:return unregistered;case 4:return pending_held;case 5:return reentrant;default:return UINT64_MAX;}
}
__declspec(dllexport) void D5AM_hold(unsigned enable) noexcept {
 d5am::held_tid=GetCurrentThreadId();d5am::hold_pending=enable!=0;
}
__declspec(dllexport) void D5AM_stop() noexcept {
 d5am::enabled=false;while(d5am::active.load())YieldProcessor();
}
__declspec(dllexport) void D5AM_release_hold() noexcept {d5am::hold_pending=false;}
__declspec(dllexport) void D5AM_fixture_emit(uint64_t lock,uint64_t old,unsigned kind) noexcept {d5am::collect(lock,old,kind);}
}
