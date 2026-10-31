// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable offline host. Uses the production queue, never a game process.
#include "observer.h"
#include <psapi.h>
#include <algorithm>
#include <cstdio>
#include <stdexcept>
#include <thread>
#include <vector>
#include <set>
#include <barrier>
#include <array>
using namespace winner;
void require(bool value){if(!value)throw std::runtime_error("queue oracle failure");}
void fresh(U origin=0){
 initialize_queue(origin);enabled=true;broken=false;counter_overflow=false;
 drops=0;full_losses=0;contention_losses=0;reentrant_losses=0;recorder_busy=false;retries=0;active=0;high_water=0;
 first_loss=0;last_loss=0;loss_generation=0;loss_bounds_uncertain=false;epoch=1;
}
Event payload(U value){Event e{};e.kind=Ready;e.a=value;e.source=~value;return e;}
void validate(const Event& e){require(e.source==~e.a);}
int main(){try{
 LARGE_INTEGER start{},end{},frequency{};QueryPerformanceCounter(&start);QueryPerformanceFrequency(&frequency);
 // Sequential wrap is checked against independently enumerated offered IDs.
 fresh();for(U n=0;n<capacity*4;++n){require(emit(payload(n)));Event e{};require(pop(e));validate(e);require(e.a==n&&e.sequence==n+1);}
 require(!drops);
 // A reserved head is never consumed, even after a later producer publishes.
 fresh();HANDLE reserved=CreateEventW(nullptr,TRUE,FALSE,nullptr),publish=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 require(reserved&&publish);
 std::thread delayed([&]{fixture_reserved=reserved;fixture_publish=publish;require(emit(payload(0)));fixture_reserved=nullptr;});
 require(WaitForSingleObject(reserved,60000)==WAIT_OBJECT_0);require(emit(payload(1)));
 Event e{};require(!pop(e));SetEvent(publish);delayed.join();require(pop(e)&&e.a==0);require(pop(e)&&e.a==1);require(!pop(e));
 CloseHandle(reserved);CloseHandle(publish);
 // Capacity overload and retry exhaustion are distinct, exact counter oracles.
 fresh();for(U n=0;n<capacity;++n)require(emit(payload(n)));
 require(!emit(payload(capacity)));require(drops==1&&full_losses==1&&contention_losses==0&&loss_generation==1);
 for(U n=0;n<capacity;++n){require(pop(e));require(e.a==n);}
 fixture_retry_failures=1;require(!emit(payload(0)));require(drops==2&&contention_losses==1&&retries==32);
 fixture_bounds_failure=true;fixture_retry_failures=1;require(!emit(payload(0))&&loss_bounds_uncertain);fixture_bounds_failure=false;
 require(emit(payload(999)));require(pop(e)&&e.a==999);
 // Concurrent reservation, publication and wrap. The oracle checks every
 // durable ID independently of queue admission order, including honest losses.
 fresh();constexpr unsigned producers=8,per_producer=12000;
 std::atomic<unsigned> completed{};std::vector<std::thread> workers;
 std::array<std::vector<U>,producers> admitted;
 for(unsigned p=0;p<producers;++p)workers.emplace_back([&,p]{
  for(unsigned i=0;i<per_producer;++i){U id=U(p)*per_producer+i;if(emit(payload(id)))admitted[p].push_back(id);if(i%97==0)SwitchToThread();}++completed;
 });
 std::set<U> seen;U sequence=0;std::array<std::vector<U>,producers> observed;
 while(completed<producers||dequeue<enqueue){if(pop(e)){validate(e);require(e.sequence==++sequence);require(e.a<U(producers)*per_producer);require(seen.insert(e.a).second);observed[e.a/per_producer].push_back(e.a);}else SwitchToThread();}
 for(auto& worker:workers)worker.join();
 require(admitted==observed);
 require(seen.size()+drops==U(producers)*per_producer);require(full_losses+contention_losses==drops);
 U concurrent_admitted=sequence,concurrent_losses=drops.load(),concurrent_retry=retries.load(),concurrent_high=high_water.load();
 U concurrent_full=full_losses.load(),concurrent_contention=contention_losses.load();
 // Hot concurrent microbursts isolate bounded-retry contention from capacity.
 // Eight producers offer 48 records each per round, with a consumer running
 // concurrently. A round barrier bounds outstanding traffic to 384 records;
 // it is engineering backpressure, not a proposed scientific capture cutoff.
 fresh();workers.clear();completed=0;seen.clear();sequence=0;
 for(auto& ids:admitted)ids.clear();for(auto& ids:observed)ids.clear();
 constexpr unsigned rounds=200,per_round=48;
 std::barrier round_start(producers+1),round_end(producers+1);
 std::atomic<unsigned> round_finished{};
 LARGE_INTEGER lossless_begin{},lossless_end{};QueryPerformanceCounter(&lossless_begin);
 for(unsigned p=0;p<producers;++p)workers.emplace_back([&,p]{
  for(unsigned round=0;round<rounds;++round){round_start.arrive_and_wait();
   for(unsigned i=0;i<per_round;++i){U id=U(round)*producers*per_round+U(p)*per_round+i;if(emit(payload(id)))admitted[p].push_back(id);}
   ++round_finished;
   round_end.arrive_and_wait();}
 });
 for(unsigned round=0;round<rounds;++round){round_start.arrive_and_wait();
  while(round_finished<U(round+1)*producers||dequeue<enqueue){if(pop(e)){validate(e);require(e.sequence==++sequence);require(e.a<U(rounds)*producers*per_round);require(seen.insert(e.a).second);observed[(e.a/per_round)%producers].push_back(e.a);}else SwitchToThread();}
  round_end.arrive_and_wait();}
 for(auto& worker:workers)worker.join();QueryPerformanceCounter(&lossless_end);
 require(admitted==observed);
 require(seen.size()+drops==U(rounds)*producers*per_round&&enqueue==dequeue);
 require(full_losses==0&&contention_losses==drops);
 U hot_losses=drops.load(),hot_retries=retries.load(),hot_high=high_water.load();
 // Qualified paced traffic uses four concurrent producers, four offers per
 // producer followed by a one-millisecond yield. Every offered ID must survive.
 fresh();workers.clear();completed=0;seen.clear();sequence=0;
 for(auto& ids:admitted)ids.clear();for(auto& ids:observed)ids.clear();
 QueryPerformanceCounter(&lossless_begin);
 for(unsigned p=0;p<4;++p)workers.emplace_back([&,p]{
  for(unsigned i=0;i<4000;++i){U id=U(p)*4000+i;if(emit(payload(id)))admitted[p].push_back(id);if(i%4==3)Sleep(1);}++completed;
 });
 while(completed<4||dequeue<enqueue){if(pop(e)){validate(e);require(e.sequence==++sequence);require(e.a<16000);require(seen.insert(e.a).second);observed[e.a/4000].push_back(e.a);}else SwitchToThread();}
 for(auto& worker:workers)worker.join();QueryPerformanceCounter(&lossless_end);
 require(admitted==observed);
 if(drops)fprintf(stderr,"paced workload losses=%llu full=%llu contention=%llu retries=%llu\n",drops.load(),full_losses.load(),contention_losses.load(),retries.load());
 require(!drops&&seen.size()==16000&&enqueue==dequeue);
 for(U id=0;id<16000;++id)require(seen.contains(id));
 U lossless_ticks=U(lossless_end.QuadPart-lossless_begin.QuadPart),lossless_high=high_water.load(),lossless_retries=retries.load();
 // Held burst: drain only after the three-second pause and all producer joins.
 // The driver can select 32,000 offers instead of this 12,000-offer default.
 fresh();QueryPerformanceCounter(&start);workers.clear();
 for(auto& ids:admitted)ids.clear();for(auto& ids:observed)ids.clear();
 constexpr unsigned burst_per_producer=3000;
 for(unsigned p=0;p<4;++p)workers.emplace_back([&,p]{for(unsigned i=0;i<burst_per_producer;++i){U id=U(p)*burst_per_producer+i;if(emit(payload(id)))admitted[p].push_back(id);if(i%6==0)Sleep(1);}});
 Sleep(3000);seen.clear();sequence=0;
 for(auto& worker:workers)worker.join();while(pop(e)){validate(e);require(e.sequence==++sequence);require(e.a<4*burst_per_producer);require(seen.insert(e.a).second);observed[e.a/burst_per_producer].push_back(e.a);}
 require(admitted==observed);require(full_losses+contention_losses==drops);
 require(sequence+drops==12000);require(capacity<12000||drops==0);
 U burst_losses=drops.load(),burst_high=high_water.load();
 U burst_full=full_losses.load(),burst_contention=contention_losses.load();
 fresh();recorder_busy=true;require(!emit(payload(0))&&reentrant_losses==1&&contention_losses==0);recorder_busy=false;
 // STOP cannot mistake a reserved producer for a quiescent queue.
 fresh();reserved=CreateEventW(nullptr,TRUE,FALSE,nullptr);publish=CreateEventW(nullptr,TRUE,FALSE,nullptr);
 std::thread stopping([&]{fixture_reserved=reserved;fixture_publish=publish;require(emit(payload(44)));});
 require(WaitForSingleObject(reserved,60000)==WAIT_OBJECT_0);enabled=false;require(active>0);SetEvent(publish);stopping.join();
 require(active==0&&pop(e)&&e.a==44);require(!emit(payload(45)));CloseHandle(reserved);CloseHandle(publish);
 // The visited callback consumes a supplied token without reading source=1.
 fresh();Scope scope{};scope.e.frame=9;scope.e.proc=8;scope.e.source=1;scope.e.epoch=epoch;
 current=&scope;visited_capture(9,8,1,1234);current=nullptr;
 require(pop(e)&&e.source==1&&e.b==1234&&!e.status);
 fresh(U(INT64_MAX)-capacity+1);require(!emit(payload(0))&&broken&&counter_overflow&&!enabled);
 QueryPerformanceCounter(&end);PROCESS_MEMORY_COUNTERS memory{};memory.cb=sizeof memory;
 require(K32GetProcessMemoryInfo(GetCurrentProcess(),&memory,sizeof memory));
 printf("{\"passed\":true,\"capacity\":%llu,\"event_bytes\":%zu,\"cell_bytes\":%zu,\"queue_bytes\":%zu,\"concurrent_admitted\":%llu,\"concurrent_losses\":%llu,\"concurrent_full_losses\":%llu,\"concurrent_contention_losses\":%llu,\"concurrent_retries\":%llu,\"concurrent_high_water\":%llu,\"hot_offered\":76800,\"hot_losses\":%llu,\"hot_retries\":%llu,\"hot_high_water\":%llu,\"lossless_offered\":16000,\"lossless_losses\":0,\"lossless_ticks\":%llu,\"lossless_high_water\":%llu,\"lossless_retries\":%llu,\"burst_offered\":12000,\"burst_losses\":%llu,\"burst_full_losses\":%llu,\"burst_contention_losses\":%llu,\"burst_high_water\":%llu,\"peak_working_set_bytes\":%zu,\"peak_pagefile_bytes\":%zu,\"measured_burst_and_closeout_ticks\":%llu,\"qpc_frequency\":%llu}\n",
 capacity,sizeof(Event),sizeof(Cell),sizeof(queue),concurrent_admitted,concurrent_losses,concurrent_full,concurrent_contention,concurrent_retry,concurrent_high,hot_losses,hot_retries,hot_high,lossless_ticks,lossless_high,lossless_retries,burst_losses,burst_full,burst_contention,burst_high,memory.PeakWorkingSetSize,memory.PeakPagefileUsage,U(end.QuadPart-start.QuadPart),U(frequency.QuadPart));
 return 0;
 }catch(const std::exception& ex){fprintf(stderr,"%s\n",ex.what());return 1;}}
