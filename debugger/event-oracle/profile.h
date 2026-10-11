// SPDX-License-Identifier: GPL-3.0-or-later
// Original single-debugger-thread QPC accounting. No target access or I/O until save.
#pragma once
#define NOMINMAX
#include <Windows.h>
#include <array>
#include <vector>
#include <string>
#include <fstream>
namespace latency {
enum Part {other,memory,writer,control,suspension,guard,count};
inline long long now(){LARGE_INTEGER q{};if(!QueryPerformanceCounter(&q))throw std::runtime_error("profile_qpc");return q.QuadPart;}
struct Sample {DWORD code{},exception{};std::string site;std::array<long long,count> ticks{};long long wait{},replay_delivery{},continuation{};};
struct Profiler {
    bool active{};Part part=other;long long last{},wait_start{},continued_at{};Sample current;std::vector<Sample> samples;
    void accrue(){auto t=now();if(active)current.ticks[part]+=t-last;last=t;}
    void start(const DEBUG_EVENT& e){current={};current.code=e.dwDebugEventCode;current.exception=e.dwDebugEventCode==EXCEPTION_DEBUG_EVENT?e.u.Exception.ExceptionRecord.ExceptionCode:0;auto t=now();current.wait=t-wait_start;if(current.exception==EXCEPTION_SINGLE_STEP&&continued_at)current.replay_delivery=t-continued_at;active=true;part=other;last=t;}
    void end(){if(active){accrue();active=false;samples.push_back(current);}}
    void save(const std::wstring& path){
        LARGE_INTEGER f{};if(!QueryPerformanceFrequency(&f))throw std::runtime_error("profile_frequency");
        std::ofstream out(path,std::ios::binary);out<<"{\"qpc_frequency\":"<<f.QuadPart<<",\"samples\":[";
        bool first=true;for(auto& s:samples){if(!first)out<<',';first=false;out<<"{\"code\":"<<s.code<<",\"exception\":"<<s.exception<<",\"site\":\""<<s.site<<"\",\"ticks\":[";for(int i=0;i<count;++i){if(i)out<<',';out<<s.ticks[i];}out<<"],\"wait\":"<<s.wait<<",\"replay_delivery\":"<<s.replay_delivery<<",\"continuation\":"<<s.continuation<<'}';}
        out<<"],\"parts\":[\"other\",\"memory\",\"writer\",\"control\",\"suspension\",\"guard\"]}\n";if(!out)throw std::runtime_error("profile_write");
    }
};
inline Profiler profiler;
struct Phase {Part previous;Phase(Part p):previous(profiler.part){profiler.accrue();profiler.part=p;}~Phase(){profiler.accrue();profiler.part=previous;}};
inline BOOL continued(DWORD pid,DWORD tid,DWORD disposition){profiler.end();auto start=now();BOOL ok=ContinueDebugEvent(pid,tid,disposition);auto end=now();profiler.continued_at=end;if(!profiler.samples.empty())profiler.samples.back().continuation+=end-start;return ok;}
}
