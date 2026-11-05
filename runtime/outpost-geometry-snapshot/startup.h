// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Startup-only admission. No owner/population is borrowed and no engine lock
// is acquired. A healthy wait has no elapsed-time cutoff; STOP remains active.
namespace d5ar {
enum class StartupResult {Ready,OwnerPresent,OwnerReadFailed,DiskFailed,Stopped,StopQueryFailed};
struct StartupServices {
 int(*owner)(void*);bool(*sole)(void*);bool(*disk)(void*);int(*stop)(void*);void(*pause)(void*);
};
inline StartupResult await_startup(void* context,const StartupServices& services){
 for(;;){
  auto owner=services.owner(context);if(owner<0)return StartupResult::OwnerReadFailed;if(owner)return StartupResult::OwnerPresent;
  if(!services.disk(context))return StartupResult::DiskFailed;
  auto stop=services.stop(context);if(stop<0)return StartupResult::StopQueryFailed;if(stop)return StartupResult::Stopped;
  if(services.sole(context))return StartupResult::Ready;
  services.pause(context);
 }
}
}
