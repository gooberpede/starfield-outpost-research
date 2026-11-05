// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Owned service controls; no clock, OS wait, process or engine state is altered.
// The production admission function runs unchanged with explicit owned inputs.
#include "startup.h"
#include <limits>
#include <stdexcept>

namespace d5ar::fixture {
struct StartupState {
    unsigned phase{},sole_after{},pauses{},owner_calls{},disk_calls{},stop_calls{},sole_calls{};
    unsigned owner_after=std::numeric_limits<unsigned>::max();
    unsigned owner_failure_after=std::numeric_limits<unsigned>::max();
    unsigned disk_failure_after=std::numeric_limits<unsigned>::max();
    unsigned stop_after=std::numeric_limits<unsigned>::max();
    unsigned stop_failure_after=std::numeric_limits<unsigned>::max();
    static int owner(void* opaque) {
        auto& state=*static_cast<StartupState*>(opaque);++state.owner_calls;
        return state.phase>=state.owner_failure_after?-1:state.phase>=state.owner_after?1:0;
    }
    static bool sole(void* opaque) {
        auto& state=*static_cast<StartupState*>(opaque);++state.sole_calls;return state.phase>=state.sole_after;
    }
    static bool disk(void* opaque) {
        auto& state=*static_cast<StartupState*>(opaque);++state.disk_calls;return state.phase<state.disk_failure_after;
    }
    static int stop(void* opaque) {
        auto& state=*static_cast<StartupState*>(opaque);++state.stop_calls;
        return state.phase>=state.stop_failure_after?-1:state.phase>=state.stop_after?1:0;
    }
    static void pause(void* opaque) {
        auto& state=*static_cast<StartupState*>(opaque);++state.phase;++state.pauses;
    }
    StartupResult run() {
        return await_startup(this,StartupServices{owner,sole,disk,stop,pause});
    }
};
inline unsigned startup_controls() {
    unsigned checks=0;
    auto check=[&](bool condition,const char* label) {
        if(!condition)throw std::runtime_error(label);++checks;
    };
    {StartupState s;check(s.run()==StartupResult::Ready&&s.pauses==0,"immediate sole-thread admission");}
    {StartupState s;s.sole_after=4;check(s.run()==StartupResult::Ready&&s.pauses==4&&s.owner_calls==5,"delayed actual sole-thread admission");}
    {StartupState s;s.sole_after=10000;check(s.run()==StartupResult::Ready&&s.pauses==10000,"healthy wait has no event-count cutoff");}
    {StartupState s;s.sole_after=9;s.stop_after=3;check(s.run()==StartupResult::Stopped&&s.pauses==3,"operator STOP during healthy wait");}
    {StartupState s;s.owner_after=0;check(s.run()==StartupResult::OwnerPresent&&s.disk_calls==0&&s.sole_calls==0,"existing owner refuses before admission");}
    {StartupState s;s.sole_after=9;s.owner_after=2;check(s.run()==StartupResult::OwnerPresent&&s.pauses==2,"owner appeared during admission wait");}
    {StartupState s;s.sole_after=9;s.owner_failure_after=2;check(s.run()==StartupResult::OwnerReadFailed&&s.pauses==2,"owner read failure refuses");}
    {StartupState s;s.sole_after=9;s.disk_failure_after=2;check(s.run()==StartupResult::DiskFailed&&s.pauses==2,"disk/query failure refuses");}
    {StartupState s;s.sole_after=9;s.stop_failure_after=2;check(s.run()==StartupResult::StopQueryFailed&&s.pauses==2,"STOP query failure refuses");}
    {StartupState s;s.stop_after=0;check(s.run()==StartupResult::Stopped&&s.sole_calls==0,"STOP precedes even otherwise-ready admission");}
    {StartupState s;s.disk_failure_after=0;s.stop_after=0;check(s.run()==StartupResult::DiskFailed&&s.stop_calls==0,"failed disk gate is never reported ready");}
    return checks;
}
}
