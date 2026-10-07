// SPDX-License-Identifier: GPL-3.0-or-later
// Adapted maintainer core: see ../maintainer/PROVENANCE.md.
// One-request adapter; this file is included by adapter.cpp.
// Writes only owned DR0/DR6/DR7 and event-thread RF; never code/data/RIP/TF.
// Quiesces all tracked threads at retirement, consumes owned pending events,
// detaches while explicitly suspended, then balances only its own suspensions.
#define NOMINMAX
#include <windows.h>
#include <tlhelp32.h>
#include <bcrypt.h>
#include "identity.h"
#include <filesystem>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <regex>
#include <stdexcept>

namespace fs = std::filesystem;
static HANDLE output = INVALID_HANDLE_VALUE;
static unsigned long output_bytes = 0;
static std::string quote(const std::string& s) {
    std::ostringstream o; o << '"';
    for (unsigned char c : s) {
        if (c == '"' || c == '\\') o << '\\' << c;
        else if (c < 32) o << "\\u" << std::hex << std::setw(4) << std::setfill('0') << unsigned(c);
        else o << c;
    }
    return o.str() + '"';
}
static std::string hex(ULONG64 n) { std::ostringstream o; o << "0x" << std::hex << n; return quote(o.str()); }
static void log(const char* kind, const std::string& fields = "") {
    FILETIME utc; GetSystemTimeAsFileTime(&utc);
    ULARGE_INTEGER stamp{}; stamp.LowPart=utc.dwLowDateTime; stamp.HighPart=utc.dwHighDateTime;
    std::string row = "{\"kind\":" + quote(kind) + ",\"version\":\"" SOR_VERSION "\",\"source_id\":\"" SOR_SOURCE_ID "\",\"utc_filetime\":" + std::to_string(stamp.QuadPart) + ",\"tick_ms\":" + std::to_string(GetTickCount64()) + fields + "}\n";
    if (output_bytes + row.size() > 2000000) throw std::runtime_error("output limit");
    DWORD used=0;
    if (!WriteFile(output,row.data(),DWORD(row.size()),&used,nullptr) || used!=row.size() || !FlushFileBuffers(output))
        throw std::runtime_error("durable evidence write");
    output_bytes += used;
}
static void require(BOOL ok, const char* op) {
    if (!ok) { log("error", ",\"operation\":" + quote(op) + ",\"winerror\":" + std::to_string(GetLastError())); throw std::runtime_error(op); }
}
static void touch(const fs::path& path) { std::ofstream f(path); if (!f) throw std::runtime_error("signal file"); }
static HANDLE process;
static DWORD pid;
struct Thread {
    HANDLE handle = nullptr;
    CONTEXT original{};
    bool armed = false;
    bool suspended = false;
    ULONG64 created = 0;
};
static std::map<DWORD, Thread> threads;
static ULONG64 site = 0;
static bool attached = false, held = false, quiescing = false;
static bool population_frozen = false, fixture_retirement_fault = false;
static bool target_exited = false, control_s1 = false;
static DWORD target_exit_code = 0, selected_tid = 0;
struct TargetExited {};
static unsigned new_unarmed_threads = 0;
static DEBUG_EVENT event{};
static CONTEXT context(DWORD tid) {
    CONTEXT c{}; c.ContextFlags = CONTEXT_CONTROL | CONTEXT_INTEGER | CONTEXT_DEBUG_REGISTERS;
    require(GetThreadContext(threads.at(tid).handle, &c), "GetThreadContext"); return c;
}
static void snapshot(DWORD tid, const char* boundary) {
    auto c = context(tid);
    log("context", ",\"boundary\":" + quote(boundary) + ",\"tid\":" + std::to_string(tid) +
        ",\"rip\":" + hex(c.Rip) + ",\"eflags\":" + hex(c.EFlags) + ",\"dr0\":" + hex(c.Dr0) +
        ",\"dr6\":" + hex(c.Dr6) + ",\"dr7\":" + hex(c.Dr7));
}
static void add_thread(DWORD tid) {
    if (threads.count(tid)) throw std::runtime_error("duplicate thread");
    Thread t;
    t.handle = OpenThread(THREAD_GET_CONTEXT | THREAD_SET_CONTEXT | THREAD_SUSPEND_RESUME | THREAD_QUERY_INFORMATION, FALSE, tid);
    require(t.handle != nullptr, "OpenThread");
    require(GetProcessIdOfThread(t.handle) == pid, "thread PID");
    FILETIME creation{}, exit{}, kernel{}, user{};
    require(GetThreadTimes(t.handle,&creation,&exit,&kernel,&user),"thread creation time");
    t.created=(ULONG64(creation.dwHighDateTime)<<32)|creation.dwLowDateTime;
    threads.emplace(tid, t);
    auto c = context(tid);
    if ((c.Dr7 & ~0x400ULL) || (c.Dr6 & 0xe00fULL) || (c.EFlags & 0x100)) throw std::runtime_error("preexisting debug state");
    threads.at(tid).original = c;
    snapshot(tid, "initial");
}
static void arm(DWORD tid) {
    if(population_frozen) throw std::runtime_error("refuse ownership expansion after ARMED");
    auto c = context(tid);
    if (c.EFlags & 0x100) throw std::runtime_error("unexpected TF");
    c.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    c.Dr0 = site; c.Dr6 &= ~1ULL; c.Dr7 = (c.Dr7 & ~0xf0003ULL) | 1;
    // Mark before write so partial failure still requires restoration.
    threads.at(tid).armed = true;
    require(SetThreadContext(threads.at(tid).handle, &c), "arm DR0");
    auto check = context(tid);
    require(check.Dr0 == site && (check.Dr7 & 0xf0003) == 1, "verify DR0");
    snapshot(tid, "armed");
}
static void disarm(DWORD tid) {
    auto& t = threads.at(tid);
    auto c = context(tid);
    c.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    c.Dr0 = t.original.Dr0;
    c.Dr6 = t.original.Dr6;
    c.Dr7 = t.original.Dr7;
    require(SetThreadContext(t.handle, &c), "restore debug registers");
    auto check = context(tid);
    require(check.Dr0 == t.original.Dr0 && check.Dr7 == t.original.Dr7 && !(check.EFlags & 0x100), "verify retirement");
    t.armed = false;
    snapshot(tid, "retired");
}
static void continue_event(DWORD disposition) {
    log("continue", ",\"pid\":" + std::to_string(event.dwProcessId) + ",\"tid\":" + std::to_string(event.dwThreadId) + ",\"disposition\":" + hex(disposition));
    require(ContinueDebugEvent(event.dwProcessId, event.dwThreadId, disposition), "ContinueDebugEvent");
    held = false;
}
static bool wait_event(DWORD ms) {
    if (!WaitForDebugEvent(&event, ms)) {
        if (GetLastError() == ERROR_SEM_TIMEOUT) return false;
        require(FALSE, "WaitForDebugEvent");
    }
    held = true;
    log("event", ",\"code\":" + std::to_string(event.dwDebugEventCode) + ",\"tid\":" + std::to_string(event.dwThreadId) +
        (event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT ? ",\"exception\":" + hex(event.u.Exception.ExceptionRecord.ExceptionCode) +
        ",\"address\":" + hex((ULONG64)event.u.Exception.ExceptionRecord.ExceptionAddress) + ",\"first_chance\":" + std::to_string(event.u.Exception.dwFirstChance) : ""));
    return true;
}
static void module_check();
static bool administration(bool install) {
    switch(event.dwDebugEventCode) {
    case CREATE_PROCESS_DEBUG_EVENT:
        add_thread(event.dwThreadId);
        (void)install; // Research ownership is assigned only at the selected boundary.
        // Windows owns event process/thread handles; never close/recycle them early.
        if (event.u.CreateProcessInfo.hFile) CloseHandle(event.u.CreateProcessInfo.hFile);
        break;
    case CREATE_THREAD_DEBUG_EVENT:
        add_thread(event.dwThreadId);
        if(population_frozen) {
            ++new_unarmed_threads;
            log("new_thread_unarmed",",\"tid\":"+std::to_string(event.dwThreadId)+
                ",\"created_filetime\":"+std::to_string(threads.at(event.dwThreadId).created)+",\"dr0_installed\":false");
        }
        if (quiescing) {
            DWORD previous = SuspendThread(threads.at(event.dwThreadId).handle);
            require(previous != DWORD(-1), "suspend new thread");
            threads.at(event.dwThreadId).suspended = true;
            log("suspend",",\"tid\":"+std::to_string(event.dwThreadId)+",\"previous\":"+std::to_string(previous)+",\"reason\":\"new_during_retirement\"");
        }
        break;
    case EXIT_THREAD_DEBUG_EVENT:
        if (threads.count(event.dwThreadId)) { CloseHandle(threads.at(event.dwThreadId).handle); threads.erase(event.dwThreadId); }
        break;
    case LOAD_DLL_DEBUG_EVENT:
        if (event.u.LoadDll.hFile) CloseHandle(event.u.LoadDll.hFile);
        module_check();
        break;
    case EXCEPTION_DEBUG_EVENT: return false;
    case EXIT_PROCESS_DEBUG_EVENT:
        target_exited = true;
        target_exit_code = event.u.ExitProcess.dwExitCode;
        log("target_exit", ",\"exit_code\":"+std::to_string(target_exit_code));
        continue_event(DBG_CONTINUE);
        attached = false;
        for(auto& [tid,t]:threads) CloseHandle(t.handle);
        threads.clear();
        log("target_exit_continued");
        throw TargetExited{};
    default: break;
    }
    continue_event(DBG_CONTINUE); return true;
}
static void resume_owned() {
    for (auto& [tid, t] : threads) if (t.suspended) {
        DWORD previous = ResumeThread(t.handle);
        log("resume", ",\"tid\":" + std::to_string(tid) + ",\"previous\":" + std::to_string(previous));
        require(previous >= 1 && previous != DWORD(-1), "ResumeThread"); t.suspended = false;
    }
}
// Called at an owned hardware event. Every competing exception is still owned by
// this debugger: the watched address has not changed and no instruction is patched.
static void retire(bool final, unsigned& pending_count, DWORD disposition = DBG_CONTINUE) {
    const ULONG64 cleanup_deadline = GetTickCount64() + 15000;
    quiescing = true;
    std::set<DWORD> pending;
    for (auto& [tid, t] : threads) {
        if (GetTickCount64() >= cleanup_deadline) throw std::runtime_error("cleanup deadline");
        DWORD previous = SuspendThread(t.handle);
        log("suspend", ",\"tid\":" + std::to_string(tid) + ",\"previous\":" + std::to_string(previous));
        require(previous != DWORD(-1), "SuspendThread"); t.suspended = true;
        auto c = context(tid);
        snapshot(tid, "before_retirement");
        if (t.armed && (!held || tid != event.dwThreadId) && c.Rip == site && (c.Dr6 & 1)) pending.insert(tid);
        if(t.armed) disarm(tid);
        else snapshot(tid,"unarmed_untouched");
    }
    if (held) continue_event(disposition);
    unsigned count = 0;
    // Frozen threads cannot execute another watched instruction. Service pending
    // owned events while frozen; two idle waits are an empirical qualification
    // boundary, not a documented promise about the complete Windows event queue.
    unsigned idle = 0;
    DWORD released_pending = 0;
    ULONG64 release_deadline = 0;
    while (idle < 2) {
        if (GetTickCount64() >= cleanup_deadline) throw std::runtime_error("cleanup deadline");
        if (!wait_event(100)) {
            if (!pending.empty()) {
                // Windows may postpone a pending exception on an explicitly
                // suspended thread. Release ONLY a thread whose DR6/RIP proved
                // an owned stop before retirement; re-suspend at its event.
                if (!released_pending) {
                    released_pending = *pending.begin();
                    auto& t = threads.at(released_pending);
                    DWORD previous = ResumeThread(t.handle);
                    log("pending_release", ",\"tid\":" + std::to_string(released_pending) + ",\"previous\":" + std::to_string(previous));
                    require(previous == 1, "release pending thread"); t.suspended = false;
                    release_deadline = GetTickCount64() + 2000;
                } else if (GetTickCount64() >= release_deadline) throw std::runtime_error("pending delivery deadline");
                continue;
            }
            ++idle; continue;
        }
        idle = 0;
        if (++count > 1024) throw std::runtime_error("retirement event bound");
        if (administration(false)) continue;
        auto c = context(event.dwThreadId);
        if (event.u.Exception.ExceptionRecord.ExceptionCode != EXCEPTION_SINGLE_STEP ||
            !event.u.Exception.dwFirstChance || (ULONG64)event.u.Exception.ExceptionRecord.ExceptionAddress != site || c.Rip != site || (c.EFlags & 0x100))
            throw std::runtime_error("unowned exception during retirement");
        if (!pending.erase(event.dwThreadId)) throw std::runtime_error("pending event lacks prior thread ownership");
        if (event.dwThreadId == released_pending) {
            auto& t = threads.at(released_pending);
            DWORD previous = SuspendThread(t.handle);
            require(previous == 0, "re-suspend pending thread"); t.suspended = true;
            log("pending_resuspend", ",\"tid\":" + std::to_string(released_pending) + ",\"previous\":" + std::to_string(previous));
            released_pending = 0;
        }
        ++pending_count;
        snapshot(event.dwThreadId, "owned_pending_event");
        disarm(event.dwThreadId);
        continue_event(DBG_CONTINUE);
    }
    if (!pending.empty()) throw std::runtime_error("undelivered pending event at retirement");
    for (const auto& [tid, t] : threads) snapshot(tid, "quiescent");
    log("quiescent", ",\"pending_events\":" + std::to_string(pending_count) + ",\"idle_waits\":2");
    if (final) {
        if(fixture_retirement_fault) throw std::runtime_error("DISPOSABLE_ONLY injected retirement failure before detach");
        require(DebugActiveProcessStop(pid), "DebugActiveProcessStop");
        attached = false;
        log("detached");
        resume_owned();
    }
}
