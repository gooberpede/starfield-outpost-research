// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable Windows tests of the production validator and a labelled variant.
// Reads/writes only owned pages and a new output file. No game or SFSE operation.
#define NOMINMAX
#include <Windows.h>
#include <cstdint>
static uintptr_t trigger_address{}, replacement_grid{}, old_storage{}, new_storage{};
static bool inject_reallocation{};
static BOOL observed_read(HANDLE process,LPCVOID address,LPVOID target,SIZE_T size,SIZE_T* got){
 BOOL result=ReadProcessMemory(process,address,target,size,got);
 // Deterministic interleaving after the member pointer has been copied. This
 // models append/reallocation followed by reuse of still-readable old storage.
 if(inject_reallocation&&uintptr_t(address)==trigger_address&&result){
  inject_reallocation=false;
  auto* header=reinterpret_cast<unsigned char*>(replacement_grid);
  uint32_t count=2,capacity=2;
  memcpy(header+0x10,&count,4);memcpy(header+0x14,&capacity,4);
  memcpy(header+0x18,&new_storage,8);
  memset(reinterpret_cast<void*>(old_storage),0,8);
 }
 return result;
}
#define ReadProcessMemory observed_read
#include SOR_OBSERVER_HEADER
#undef ReadProcessMemory
#include <algorithm>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace retained;
void require(bool condition){if(!condition)throw std::runtime_error("R3 native oracle");}
template<class T>void put(U address,T value){memcpy(reinterpret_cast<void*>(address),&value,sizeof value);}
int wmain(int argc,wchar_t** argv){
 try{
  require(argc==2);std::ofstream out(argv[1]);require(bool(out));
  auto* image=static_cast<unsigned char*>(VirtualAlloc(nullptr,0x6000000,MEM_RESERVE,PAGE_NOACCESS));require(image!=nullptr);base=U(image);
  require(VirtualAlloc(image+0x5fd9000,4096,MEM_COMMIT,PAGE_READWRITE)!=nullptr);
  alignas(8) unsigned char manager[0x300]{},proc[64]{},source[0x70]{},index[64]{},grid[64]{},frame[0x400]{};
  U query=123;std::vector<U> members(1024,0),replacement(2,0);
  auto reset=[&](uint32_t n,uint32_t cap){
   hazards=0;broken=false;epoch=1;inject_reallocation=false;std::fill(members.begin(),members.end(),0);
   put(base+0x5fd9c30,U(manager));put(U(manager)+0x130,U(proc));put(U(manager)+0x120,U(index));
   put(U(proc),base+0x4b3f3a8);put(U(index)+0x10,U(grid));put(U(grid),base+0x4b67f48);
   put(U(grid)+0x10,n);put(U(grid)+0x14,cap);put(U(grid)+0x18,U(members.data()));
   put(U(frame)+0x38,U(source));put(U(frame)+0x3d8,U(&query));put(U(frame)+0x100,U(grid));
  };
  unsigned cases=0;
  auto sample=[&](const char* label,Reason expected){Event e{};source_context(e,U(frame),U(proc));require(e.reason==expected);
   out<<"{\"case\":\""<<label<<"\",\"reason\":"<<e.reason<<",\"count\":"<<e.grid_count
      <<",\"capacity\":"<<e.grid_capacity<<",\"members\":"<<e.members<<",\"retained_grid\":"<<e.retained_grid
      <<",\"read_returned\":"<<e.read_returned<<",\"read_requested\":"<<e.read_requested<<"}\n";++cases;
  };
  for(uint32_t n:{0u,1u,255u,256u,257u,324u,512u,1024u}){
   uint32_t cap=n==324?512:n;
   for(auto position:{0u,n/2,n?n-1:0}){
    reset(n,cap);if(n)members[position]=U(source);
    sample("boundary-hit",!SOR_R3_UNCAPPED&&n>256?GridCoverageLimit:n?ContextOK:NotMember);
   }
   reset(n,cap);sample("complete-array-absence",!SOR_R3_UNCAPPED&&n>256?GridCoverageLimit:NotMember);
  }
  reset(2,1);sample("count-over-capacity",GridExtent);
  reset(1,1);put(U(grid)+0x18,U(0));sample("null-storage",MemberRead);
  reset(1,1);put(U(grid)+0x18,UINT64_MAX-3);sample("pointer-overflow-domain",MemberRead);
  auto* pages=static_cast<unsigned char*>(VirtualAlloc(nullptr,8192,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE));require(pages!=nullptr);
  DWORD old{};require(VirtualProtect(pages+4096,4096,PAGE_NOACCESS,&old)!=0);
  reset(2,2);put(U(grid)+0x18,U(pages+4088));put(U(pages+4088),U(source));sample("read-failure-after-hit",MemberRead);
  reset(1,1);members[0]=U(source);put(U(frame)+0x100,U(1));sample("invocation-grid-mismatch",GridChanged);
  reset(1,1);members[0]=U(source);hazards=1;sample("lifetime-hazard",ContextLifetime);
  reset(1,1);members[0]=U(source);broken=true;sample("broken-lifetime",ContextLifetime);
  // Claimed array extent overlaps a distinct logical allocation within the same
  // readable page. Virtual memory readability cannot recover allocator ownership.
  reset(2,2);put(U(grid)+0x18,U(pages));put(U(pages),U(0));put(U(pages+8),U(source));
  MEMORY_BASIC_INFORMATION info{};require(VirtualQuery(pages,&info,sizeof info)==sizeof info&&info.RegionSize>=16);
  sample("logical-one-slot-allocation-with-adjacent-alias",ContextOK);
  // The source remains present in the new native-shaped array. Reading the old
  // reused array yields a false complete-negative reason in the unchanged code.
  reset(1,1);members[0]=U(source);replacement[0]=U(source);replacement[1]=0;
  trigger_address=U(grid)+0x18;replacement_grid=U(grid);old_storage=U(members.data());new_storage=U(replacement.data());inject_reallocation=true;
  sample("reallocation-false-negative",NotMember);require(!inject_reallocation&&replacement[0]==U(source));
  for(uint32_t n:{1u,256u,324u,512u,1024u}){
   reset(n,n==324?512:n);members[n-1]=U(source);std::vector<double> samples;LARGE_INTEGER frequency{};QueryPerformanceFrequency(&frequency);
   for(unsigned i=0;i<1000;++i){LARGE_INTEGER start{},end{};QueryPerformanceCounter(&start);Event e{};source_context(e,U(frame),U(proc));QueryPerformanceCounter(&end);
    require(e.reason==(!SOR_R3_UNCAPPED&&n>256?GridCoverageLimit:ContextOK));samples.push_back(double(end.QuadPart-start.QuadPart)*1e6/double(frequency.QuadPart));}
   std::sort(samples.begin(),samples.end());double mean=0;for(double value:samples)mean+=value;mean/=samples.size();
   out<<"{\"timing_count\":"<<n<<",\"samples\":1000,\"mean_us\":"<<mean<<",\"p95_us\":"<<samples[949]
      <<",\"p99_us\":"<<samples[989]<<",\"max_observed_us\":"<<samples.back()<<"}\n";
  }
  out.flush();require(bool(out));std::cout<<"cases="<<cases<<" uncapped="<<SOR_R3_UNCAPPED<<"\n";return 0;
 }catch(...){return 91;}
}
