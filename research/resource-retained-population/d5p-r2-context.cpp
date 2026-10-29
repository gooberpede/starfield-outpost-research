// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable native qualifier. Includes unchanged production validator source.
// Reads only its own allocated pages; writes Event bytes to a fresh local file.
// No SFSE, external process access, interception or game operation.
#include "../../runtime/retained-population/observer.h"
#include <fstream>
#include <filesystem>
#include <stdexcept>
#include <vector>
using namespace retained;
void require(bool value){if(!value)throw std::runtime_error("native oracle failed");}
template<class T> void put(U p,T value){memcpy((void*)p,&value,sizeof value);}
int wmain(int argc,wchar_t** argv){
 try {
  require(argc==2);std::ofstream out(argv[1],std::ios::binary);require(bool(out));
  auto* image=(unsigned char*)VirtualAlloc(nullptr,0x6000000,MEM_RESERVE,PAGE_NOACCESS);require(image!=nullptr);base=U(image);
  require(VirtualAlloc(image+0x5fd9000,4096,MEM_COMMIT,PAGE_READWRITE)!=nullptr);
  alignas(8) unsigned char manager[0x300]{},proc[64]{},source[0x70]{},index[64]{},grid[64]{},frame[0x400]{};
  U member=U(source),query=0x1122334455667788ULL;
  auto restore=[&](){hazards=0;broken=false;epoch=1;put(base+0x5fd9c30,U(manager));
   put(U(manager)+0x130,U(proc));put(U(manager)+0x120,U(index));manager[0x20]=2;put(U(manager)+0x80,uint32_t(0x5e0de));
   put(U(proc),base+0x4b3f3a8);put(U(index)+0x10,U(grid));put(U(grid),base+0x4b67f48);
   put(U(grid)+0x10,uint32_t(1));put(U(grid)+0x14,uint32_t(1));put(U(grid)+0x18,U(&member));member=U(source);
   put(U(frame)+0x38,U(source));put(U(frame)+0x3d8,U(&query));put(U(frame)+0x100,U(grid));};
  U sequence=0;
  auto sample=[&](Reason reason,U w,U p){Event e{};source_context(e,w,p);require(e.reason==reason);
   e.kind=Visited;e.sequence=++sequence;e.invocation=sequence;e.thread=GetCurrentThreadId();
   // Standalone harness outputs are source-path evidence, not plugin receipts.
   out.write((const char*)&e,sizeof e);require(bool(out));};
  restore();sample(ContextOK,U(frame),U(proc));
  DWORD old{};require(VirtualProtect(image+0x5fd9000,4096,PAGE_NOACCESS,&old)!=0);sample(SingletonRead,U(frame),U(proc));
  require(VirtualProtect(image+0x5fd9000,4096,PAGE_READWRITE,&old)!=0);
  restore();sample(SourcePointerRead,0,U(proc));
  auto* pages=(unsigned char*)VirtualAlloc(nullptr,12288,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);require(pages!=nullptr);
  require(VirtualProtect(pages+4096,4096,PAGE_NOACCESS,&old)!=0);
  U w=U(pages+4096)-0x3d8;put(w+0x38,U(source));sample(QueryPointerRead,w,U(proc));
  restore();put(base+0x5fd9c30,U(1));sample(ManagerProcRead,U(frame),U(proc));
  restore();put(U(manager)+0x130,U(2));sample(ManagerProcMismatch,U(frame),U(proc));
  restore();U alternate=U(pages+8192)-0x100;put(alternate+0x130,U(proc));put(base+0x5fd9c30,alternate);sample(ModeRead,U(frame),U(proc));
  restore();put(U(frame)+0x38,U(1));sample(SourceBytesRead,U(frame),U(proc));
  restore();put(U(frame)+0x3d8,U(1));sample(QueryWordsRead,U(frame),U(proc));
  restore();put(U(manager)+0x130,U(1));sample(ProcTypeRead,U(frame),1);
  restore();put(U(proc),U(3));sample(ProcTypeMismatch,U(frame),U(proc));
  restore();put(U(manager)+0x120,U(1));sample(GridPointerRead,U(frame),U(proc));
  restore();put(U(index)+0x10,U(1));sample(GridTypeRead,U(frame),U(proc));
  restore();put(U(grid),U(4));sample(GridTypeMismatch,U(frame),U(proc));
  for(auto reason:{GridCountRead,GridCapacityRead,GridDataRead}){
   restore();U g=U(pages+4096)-(reason==GridCountRead?0x10:reason==GridCapacityRead?0x14:0x18);
   put(g,base+0x4b67f48);if(reason!=GridCountRead)put(g+0x10,uint32_t(1));
   if(reason==GridDataRead)put(g+0x14,uint32_t(1));put(U(index)+0x10,g);sample(reason,U(frame),U(proc));
  }
  restore();put(U(grid)+0x10,uint32_t(2));sample(GridExtent,U(frame),U(proc));
  restore();put(U(grid)+0x10,uint32_t(257));put(U(grid)+0x14,uint32_t(257));sample(GridCoverageLimit,U(frame),U(proc));
  restore();put(U(grid)+0x18,U(1));sample(MemberRead,U(frame),U(proc));
  restore();member=1;sample(NotMember,U(frame),U(proc));
  restore();put(U(frame)+0x100,U(1));sample(GridChanged,U(frame),U(proc));
  restore();hazards=1;sample(ContextLifetime,U(frame),U(proc));
  restore();broken=true;sample(ContextLifetime,U(frame),U(proc));
  restore();put(U(source),uint32_t(0xabcdef));manager[0x20]=3;sample(ContextOK,U(frame),U(proc));
  // Composite ordering prevents deterministic page isolation for reasons
  // 9,10,13,25 with this small ordinary layout. Exercise the exact read primitive
  // for every read reason separately; do not call it composite coverage.
  for(auto reason:{SingletonRead,SourcePointerRead,QueryPointerRead,ManagerProcRead,ModeRead,SourceBytesRead,QueryWordsRead,OwnerRead,DescriptorRead,ProcTypeRead,IndexRead,GridPointerRead,GridTypeRead,GridCountRead,GridCapacityRead,GridDataRead,MemberRead,RetainedGridRead}){
   Event e{};U value{};require(!context_read(e,1,&value,8,reason));require(e.reason==reason&&e.read_requested==8&&e.read_returned==0);
  }
  Event partial{};unsigned char bytes[16]{};
  require(!context_read(partial,U(pages+4090),bytes,16,SourceBytesRead));require(partial.read_returned<16);
  std::ofstream stats(std::filesystem::path(argv[1]).concat(L".json"));
  stats<<"{\"image_base\":"<<base<<",\"composite_records\":"<<sequence<<",\"read_primitive_reasons\":18,\"cross_page_returned\":"<<partial.read_returned<<",\"cross_page_requested\":16}\n";
  return 0;
 }catch(...){return 91;}
}
