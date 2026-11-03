// SPDX-License-Identifier: GPL-3.0-or-later
// Owned native composition controls. The CALL target really is the same private
// original helper that receives causal site3, matching the retail alias.
namespace {
std::string d5am_guard_original;
void d5am_guard_prepare(){
 using namespace winner;
 auto* call=d5am_private+1668;check(!enabled.load());
 for(auto& p:causal::edits)check(match(p,false));
 // Wrong independently supplied original target hash must fail before installation.
 check(!geometry::configure_acquire(call,sor::sha_bytes(call,32),std::string(64,'0'),false));
 d5am_guard_original=sor::sha_bytes(d5am_private,32);
 // Execute the exact shared CALL before either family is installed.
 alignas(8) uint32_t initial_lock[2]{};
 ((Four)(d5am_private+1664))(U(initial_lock),0,0,0);check(initial_lock[1]==1);
 ((void(*)(U,U))(d5am_private+1152))(U(initial_lock)+4,0xffffffff);check(initial_lock[1]==0);
 DWORD protection{},ignored{};check(VirtualProtect(d5am_private,1,PAGE_EXECUTE_READWRITE,&protection));
 unsigned char original=d5am_private[0];d5am_private[0]^=1;
 check(!geometry::configure_acquire(call,sor::sha_bytes(call,32),d5am_guard_original,false));
 d5am_private[0]=original;check(FlushInstructionCache(GetCurrentProcess(),d5am_private,1));
 check(VirtualProtect(d5am_private,1,protection,&ignored));
 check(geometry::configure_acquire(call,sor::sha_bytes(call,32),d5am_guard_original,false));
 check(geometry::guarded_target==U(d5am_private));
 check(sor::sha_bytes(d5am_private,32)==d5am_guard_original);
}
void d5am_guard_run(const std::wstring& scenario,U proc,HANDLE worker){
 using namespace winner;
 check(geometry::guards()&&causal::guards());
 check(!guardrepair::target(U(d5am_private),std::string(64,'0')));
 // Execute the installed geometry CALL wrapper, original helper, and its causal
 // bridge. Snapshot is deliberately unarmed; this control tests hook composition.
 auto* words=(uint32_t*)(proc+0x40);check(!words[0]&&!words[1]);
 ((Four)(d5am_private+1664))(proc+0x40,0,0,0);check(words[1]==1);
 ((void(*)(U,U))(d5am_private+1152))(proc+0x44,0xffffffff);check(!words[1]);
 if(scenario==L"d5am-guard-alias"){
  check(sor::write_new(session/L"guard-composition.json","{\"alias\":true,\"original_check\":true,\"installed_check\":true,\"native_call\":true}\n"));return;
 }
 unsigned char* damaged=nullptr;
 if(scenario==L"d5am-guard-overlap"||scenario==L"d5am-guard-patch")damaged=d5am_private+22;
 else if(scenario==L"d5am-guard-outside")damaged=d5am_private;
 else if(scenario==L"d5am-guard-preimage")damaged=causal::edits[3].before;
 else if(scenario==L"d5am-guard-relay")damaged=causal::page;
 check(damaged!=nullptr);DWORD old{},unused{};
 check(VirtualProtect(damaged,1,PAGE_EXECUTE_READWRITE,&old));unsigned char before=*damaged;if(scenario==L"d5am-guard-patch")*damaged=causal::edits[3].before[0];else *damaged^=1;
 check(FlushInstructionCache(GetCurrentProcess(),damaged,1));
 check(!geometry::guards());
 if(scenario==L"d5am-guard-preimage")check(causal::guards());
 // Let the real worker enforce its ordinary protective terminal guard path.
 check(WaitForSingleObject(worker,60000)==WAIT_OBJECT_0);
 *damaged=before;check(FlushInstructionCache(GetCurrentProcess(),damaged,1));
 check(VirtualProtect(damaged,1,old,&unused));check(geometry::guards());
 check(sor::write_new(session/L"guard-composition.json","{\"alias\":true,\"corruption_refused\":true,\"worker_terminal\":true}\n"));
}
}
