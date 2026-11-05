// SPDX-License-Identifier: GPL-3.0-or-later
// Native ABI/exception probes run only in this disposable fixture executable.
#include "hooks.h"
#include "capture.h"
#include "startup_stack.h"
#include <iostream>
#include <stdexcept>
extern "C" {
uint64_t observed[12]{},captured_arguments[6]{};
uint8_t observed_simd[96]{};
uint64_t d5ar_callback_original{},d5ar_area_callback_original{},d5ar_area_dispatch{},d5ar_selection_release_original{},d5ar_source_free_original{};
uint64_t probe_bridge(unsigned);void original_sink();
void d5ar_callback_bridge_deallocate();void d5ar_callback_bridge_flags();
void d5ar_area_callback_bridge_deallocate();void d5ar_area_callback_bridge_flags();
void d5ar_area_entry_bridge_deallocate();void d5ar_area_entry_bridge_flags();
void d5ar_selection_release_bridge_deallocate();void d5ar_selection_release_bridge_flags();
void d5ar_source_free_bridge_deallocate();void d5ar_source_free_bridge_flags();
}
static bool throw_from_capture{};
extern "C" void fixture_capture_c(){if(throw_from_capture)RaiseException(0xe0424441,0,0,nullptr);}
static void require(bool value,const char* description){if(!value)throw std::runtime_error(description);}
static bool exception_probe(unsigned area){
 __try{probe_bridge(area);}
 __except(GetExceptionCode()==0xe0424441?EXCEPTION_EXECUTE_HANDLER:EXCEPTION_CONTINUE_SEARCH){return true;}
 return false;
}
int main(){
 try{
  d5ar_callback_original=reinterpret_cast<uint64_t>(&original_sink);d5ar_area_callback_original=d5ar_callback_original;d5ar_area_dispatch=d5ar_callback_original;d5ar_selection_release_original=d5ar_callback_original;d5ar_source_free_original=d5ar_callback_original;
  unsigned passed=0;
  for(unsigned area=0;area<5;++area){
   require(probe_bridge(area)==1,"Bridge result");
   const uint64_t expected[]{0x5555,0x1111,0x2222,0x3333,0x4444,0x6666,0x7777,0x8888,0x9999};
   for(unsigned i=0;i<9;++i)require(observed[i]==expected[i],"Volatile/nonvolatile register corruption");
   require((observed[9]&0x8d5)==0x44,"Arithmetic flags corruption");
   require(observed[10]==0xa5&&(observed[11]&15)==8,"Stack argument/alignment corruption");
   const uint8_t expected_simd[]{0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff,0x10};
   for(unsigned i=0;i<96;++i)require(observed_simd[i]==expected_simd[i%16],"SIMD corruption");
   if(area<3)require(captured_arguments[2]==(area==2?0xaaaa:area?0x9999:0x8888)&&captured_arguments[3],"Native caller operands");
   else if(area==3)require(captured_arguments[0]==0x1111&&captured_arguments[1]&&captured_arguments[2]==observed[11]+0x90&&captured_arguments[3]==observed[11],"Lease CALL native return/stack operands");
   if(area==4)require(captured_arguments[0]==0x1111&&captured_arguments[1]==0x2222&&captured_arguments[2]&&captured_arguments[3]==observed[11],"Source ending CALL operands");
   if(area==1)require(captured_arguments[0]==0x3333&&captured_arguments[1]==0x1111,"Area holder slot/context operands");
   else if(area<3)require(captured_arguments[0]==0x1111&&captured_arguments[1]==0x2222,"Point holder-map operands");
   if(area==2)require(captured_arguments[4]==0x44332211&&captured_arguments[5]==0x44332211,"Area scalar input operands");
   ++passed;
  }
  throw_from_capture=true;require(exception_probe(0),"Point bridge SEH unwind");++passed;
  require(exception_probe(1),"Area bridge SEH unwind");++passed;throw_from_capture=false;
  throw_from_capture=true;require(exception_probe(2),"Area entry SEH unwind");++passed;throw_from_capture=false;
  throw_from_capture=true;require(exception_probe(3),"Lease CALL bridge SEH unwind");++passed;throw_from_capture=false;
  throw_from_capture=true;require(exception_probe(4),"Source ending bridge SEH unwind");++passed;throw_from_capture=false;
  unsigned epilogue_checks=0;
  const uint64_t boundaries[][2]={
{reinterpret_cast<uint64_t>(&d5ar_callback_bridge_deallocate),reinterpret_cast<uint64_t>(&d5ar_callback_bridge_flags)},
{reinterpret_cast<uint64_t>(&d5ar_area_callback_bridge_deallocate),reinterpret_cast<uint64_t>(&d5ar_area_callback_bridge_flags)},
{reinterpret_cast<uint64_t>(&d5ar_area_entry_bridge_deallocate),reinterpret_cast<uint64_t>(&d5ar_area_entry_bridge_flags)},
{reinterpret_cast<uint64_t>(&d5ar_selection_release_bridge_deallocate),reinterpret_cast<uint64_t>(&d5ar_selection_release_bridge_flags)},
{reinterpret_cast<uint64_t>(&d5ar_source_free_bridge_deallocate),reinterpret_cast<uint64_t>(&d5ar_source_free_bridge_flags)},
  };
  for(const auto& boundary:boundaries)for(unsigned step=0;step<3;++step){
   alignas(16) std::array<uint64_t,128> stack{};auto start=reinterpret_cast<uint64_t>(stack.data()),resume=reinterpret_cast<uint64_t>(&original_sink);
   stack[28]=0x246;stack[29]=resume;CONTEXT context{};context.ContextFlags=CONTEXT_FULL;
   context.Rip=step?boundary[1]+(step==2?1:0):boundary[0];context.Rsp=start+(step==0?0:step==1?224:232);
   DWORD64 image{};auto entry=RtlLookupFunctionEntry(context.Rip,&image,nullptr);
   require(entry&&d5ar::unwind_step(context,image,entry),"Bridge epilogue unwind entry");
   require(context.Rip==resume&&context.Rsp==start+240,"Bridge ADD/POPFQ/JMP unwind corruption");++epilogue_checks;
  }
  std::cout<<"{\"schema\":\"sor-d5ar-bridge-abi/1\",\"passed\":"<<passed<<",\"epilogue_unwind_checks\":"<<epilogue_checks<<",\"scope\":\"Same DLL context bridges: four installed roles and one offline point prototype\"}\n";
  return 0;
 }catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
}
