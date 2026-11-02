// SPDX-License-Identifier: GPL-3.0-or-later
// Cost oracle linked to the exact retained transport/bridge objects. Supplied
// owned objects and logical reader fields measure copying, not lock semantics.
#include "d5ai_geometry.h"
#include "d5ai_population.generated.h"
#include <cstdio>
#include <vector>
#include <algorithm>
#include <intrin.h>
extern "C" {
 void d5ai_area_capture(uint64_t,uint64_t,uint64_t,uint32_t,uint32_t) noexcept;
 void d5ai_preunlock_capture(uint64_t) noexcept;
 void d5ai_complete_capture(uint64_t,uint64_t,uint64_t) noexcept;
 uint64_t d5ai_native_acquire(uint64_t,uint64_t,uint64_t,uint64_t){return 0;}
}
using namespace winner;
namespace g=winner::geometry;
__declspec(noinline) void baseline(U,U,U,uint32_t,uint32_t){_ReadWriteBarrier();}
template<class T> void put(void* p,size_t at,const T& v){memcpy((unsigned char*)p+at,&v,sizeof v);}
U qpc(){LARGE_INTEGER n{};QueryPerformanceCounter(&n);return U(n.QuadPart);}
void summary(const char* label,std::vector<U> values){std::sort(values.begin(),values.end());printf("\"%s\":{\"n\":%zu,\"p50_ticks\":%llu,\"p95_ticks\":%llu,\"max_ticks\":%llu}",label,values.size(),values[values.size()/2],values[values.size()*95/100],values.back());}
int main(){
 SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
 alignas(16) unsigned char proc[0x80]{},manager[0x210]{},holder[64]{},map[48]{},query[24]{};
 std::vector<std::vector<unsigned char>> buffers;
 auto alloc=[&](size_t n){buffers.emplace_back(n,0);return buffers.back().data();};
 const auto* source=d5ai_population_data[1];size_t pos=0;
 auto word=[&](){uint32_t v{};memcpy(&v,source+pos,4);pos+=4;return v;};
 auto count=word();U capacity=1;while(capacity<=count)capacity*=2;
 auto resources=alloc(size_t(capacity)*24);for(U i=0;i<capacity;++i)put(resources,size_t(i)*24+16,UINT32_MAX);
 for(uint32_t i=0;i<count;++i){auto form=word(),regions=word();auto collection=alloc(24),data=alloc(size_t(regions)*48);
  put(resources,size_t(i)*24,form);put(resources,size_t(i)*24+8,U(collection));put(resources,size_t(i)*24+16,uint32_t(0));
  put(collection,0,uint32_t(1));put(collection,8,regions);put(collection,12,regions);put(collection,16,U(data));
  for(uint32_t j=0;j<regions;++j){auto region=data+size_t(j)*48;memcpy(region,source+pos,24);pos+=24;auto n=word();auto points=alloc(size_t(n)*16);memcpy(points,source+pos,size_t(n)*16);pos+=size_t(n)*16;put(region,24,n);put(region,28,n);put(region,32,U(points));}
 }
 if(pos!=d5ai_population_size[1])return 1;
 put(holder,0x20,U(resources));put(holder,0x28,capacity);put(map,0,U(0x10001));put(map,8,U(holder));put(map,16,uint32_t(0));put(map,40,UINT32_MAX);
 put(proc,0x20,U(map));put(proc,0x28,U(2));put(proc,0x44,uint32_t(1));put(manager,0x20,uint8_t(2));put(manager,0x80,uint32_t(0x5e0de));put(manager,0x130,U(proc));g::fixture_manager=U(manager);enabled=true;
 std::vector<U> empty,unarmed,armed,copies;
 for(unsigned i=0;i<10000;++i){auto begin=qpc();baseline(U(proc),U(query),0,0,0);empty.push_back(qpc()-begin);begin=qpc();d5ai_area_capture(U(proc),U(query),0,0,0);unarmed.push_back(qpc()-begin);}
 U copied_bytes{};
 for(U i=1;i<=100;++i){if(!g::arm(i))return 2;auto begin=qpc();d5ai_area_capture(U(proc),U(query),0,0,0);armed.push_back(qpc()-begin);d5ai_preunlock_capture(1);d5ai_complete_capture(2,2,0xdeadbeef);
  bool found=false;for(auto& slot:g::slots)if(slot.state==g::Queued){auto& h=slot.header;if(h.status||h.resources!=3||h.regions!=78||h.points!=180)return 3;copies.push_back(h.ticks_end-h.ticks_begin);copied_bytes=h.payload_bytes;slot.state=g::Free;found=true;break;}if(!found)return 4;
 }
 LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);printf("{\"status\":\"PASS\",\"frequency\":%llu,\"payload_bytes\":%llu,\"header_bytes\":%zu,\"slot_bytes\":%zu,\"slot_count\":%zu,",U(frequency.QuadPart),copied_bytes,sizeof(g::Header),sizeof(g::Slot),g::slot_count);
 summary("baseline_call",empty);printf(",");summary("unarmed_callback",unarmed);printf(",");summary("armed_callback",armed);printf(",");summary("copy_interval",copies);printf("}\n");return 0;
}
