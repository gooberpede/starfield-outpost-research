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
 for(unsigned p=0;p<producers;++p)workers.emplace_back([&,p]{
  for(unsigned i=0;i<per_producer;++i){emit(payload(U(p)*per_producer+i));if(i%97==0)SwitchToThread();}++completed;
 });
 std::set<U> seen;U sequence=0;
 while(completed<producers||dequeue<enqueue){if(pop(e)){validate(e);require(e.sequence==++sequence);require(seen.insert(e.a).second);}else SwitchToThread();}
 for(auto& worker:workers)worker.join();
 require(seen.size()+drops==U(producers)*per_producer);require(full_losses+contention_losses==drops);
 U concurrent_admitted=sequence,concurrent_losses=drops.load(),concurrent_retry=retries.load(),concurrent_high=high_water.load();
 // Qualified paced representative queue workload: four simultaneous producers
 // offer 12,000 records while the consumer is stalled for three seconds.
 fresh();QueryPerformanceCounter(&start);workers.clear();
 for(unsigned p=0;p<4;++p)workers.emplace_back([&,p]{for(unsigned i=0;i<3000;++i){emit(payload(U(p)*3000+i));if(i%6==0)Sleep(1);}});
 Sleep(3000);seen.clear();sequence=0;
 for(auto& worker:workers)worker.join();while(pop(e)){validate(e);require(e.sequence==++sequence);require(seen.insert(e.a).second);}
 require(sequence+drops==12000);require(capacity<12000||drops==0);
 U burst_losses=drops.load(),burst_high=high_water.load();
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
 printf("{\"passed\":true,\"capacity\":%llu,\"event_bytes\":%zu,\"cell_bytes\":%zu,\"queue_bytes\":%zu,\"concurrent_admitted\":%llu,\"concurrent_losses\":%llu,\"concurrent_retries\":%llu,\"concurrent_high_water\":%llu,\"burst_offered\":12000,\"burst_losses\":%llu,\"burst_high_water\":%llu,\"peak_working_set_bytes\":%zu,\"peak_pagefile_bytes\":%zu,\"measured_burst_and_closeout_ticks\":%llu,\"qpc_frequency\":%llu}\n",
 capacity,sizeof(Event),sizeof(Cell),sizeof(queue),concurrent_admitted,concurrent_losses,concurrent_retry,concurrent_high,burst_losses,burst_high,memory.PeakWorkingSetSize,memory.PeakPagefileUsage,U(end.QuadPart-start.QuadPart),U(frequency.QuadPart));
 return 0;
 }catch(const std::exception& ex){fprintf(stderr,"%s\n",ex.what());return 1;}}
