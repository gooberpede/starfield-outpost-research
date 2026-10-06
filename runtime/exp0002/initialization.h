// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
#include "win_support.h"
#include <atomic>

namespace sor {
struct Initialization {
    std::atomic<bool> listener_registered{};

    // A registered callback keeps this DLL resident even if thread creation
    // fails. Load success is not READY; the worker alone publishes that marker.
    template<class Register, class Start, class Failure>
    bool start(Register register_listener, Start start_worker, Failure failure) {
        try {
            if(!register_listener()){failure("listener_registration_failed");return false;}
            listener_registered=true;
            if(!start_worker())failure("worker_start_failed");
        }catch(const std::exception&){failure("initialization_cpp_failure");}
        return listener_registered;
    }

    // Called on entry to the successfully created worker, before request polling.
    template<class Publish, class Failure>
    bool worker_ready(Publish publish, Failure failure) {
        if(!listener_registered){failure("worker_without_listener");return false;}
        if(!publish()){failure("ready_publication_failed");return false;}
        return true;
    }
};

// No READY filename is exposed for partial/failed writes or failed flushes.
// Keep a failed pending artifact as evidence; never replace an existing marker.
template<class Write>
bool publish_ready(const fs::path& session,const std::string& data,Write write) {
    auto pending=session/L"ready.pending";
    if(!write(pending,data))return false;
    return MoveFileExW(pending.c_str(),(session/L"ready.json").c_str(),MOVEFILE_WRITE_THROUGH)!=0;
}
}
