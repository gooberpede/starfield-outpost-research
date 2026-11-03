// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable host adapter only; never include in the retail plugin translation.
// Executes the production registry/callback/TLS methods around an existing
// native geometry action, replacing only the synthetic scheduler's policy calls.
// This proves cross-channel joins, not actual retail task registration/dispatch.
#include <type_traits>
namespace winner::scheduler_fixture {
inline thread_local void* action_context{};
inline thread_local void(*action_call)(void*){};
alignas(16) inline U vtables[3][4]{};
alignas(16) inline unsigned char server[256]{};
inline U registration_noop(U,U,U,U){return 0;}
inline U action_body(U,U,U,U){if(action_call)action_call(action_context);return 5;}
inline bool setup_identity(){
 using namespace winner::scheduler;
 if(configured)return false;
 for(unsigned i=0;i<3;++i){D5AM_sched_vtables[i]=U(vtables[i]);vtable_hash[i]=sor::sha_bytes(vtables[i],32);}
 callback_target=U(&action_body);D5AM_sched_callback_target=callback_target;
 unsigned char code[32]{};if(!read(callback_target,code,32))return false;
 callback_hash=sor::sha_bytes(code,32);return callback_hash.size()==64;
}
inline std::string metadata(){return ",\"scheduler_fixture_scope\":\"owned typed producer adapter; generic scheduler sites not installed\"";}
template<class Function> inline bool invoke(Function&& action,int32_t x=10,int32_t y=11){
 using namespace winner::scheduler;
 if(!D5AM_sched_vtables[0]||!begun||!winner::enabled.load())return false;
 alignas(16) unsigned char node[0x100]{};
 U vtable=D5AM_sched_vtables[0];memcpy(node,&vtable,8);
 uint32_t key[]{0x31544153,0x44414d35,0},discriminator[]{0x111,0x222,0x333};
 int32_t request[]{x,y};memcpy(node+8,key,12);memcpy(node+0xb0,request,8);memcpy(node+0xb8,discriminator,12);
 node[0xa0]=2;node[0xa8]=2;
 Four old_registration=registration_original[0],old_density=density_original;
 void* old_context=action_context;auto old_call=action_call;
 struct Restore {Four registration,density;void* context;void(*call)(void*);
  ~Restore(){registration_original[0]=registration;density_original=density;action_context=context;action_call=call;}
 } restore{old_registration,old_density,old_context,old_call};
 registration_original[0]=&registration_noop;density_original=&action_body;
 action_context=&action;
 action_call=[](void* value){(*static_cast<std::remove_reference_t<Function>*>(value))();};
 U address=U(node);registration<0>(U(server),0,address,0);
 callback<0>(address+0xb0,0,0,0);
 auto consumed=cookie(address);winner::scheduler::Event retirement{};
 bool retired=snapshot(address,Retire,0,consumed,retirement);if(retired)emit(retirement);
 return retired&&retirement.allocation&&!retirement.status;
}
}
