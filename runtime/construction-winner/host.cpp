// SPDX-License-Identifier: GPL-3.0-or-later
// Only loads the explicitly supplied disposable qualification DLL.
#include <Windows.h>
#include "../exp0002/third_party/sfse/PluginAPI.h"
int wmain(int count,wchar_t** args){
 SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOGPFAULTERRORBOX);
 if(count!=4)return 80;auto dll=LoadLibraryW(args[1]);if(!dll)return 81;
 auto load=(bool(*)(const SFSEInterface*))GetProcAddress(dll,"SFSEPlugin_Load");
 if(!load||load(nullptr))return 83;SFSEInterface api{};api.interfaceVersion=1;api.runtimeVersion=(1u<<24)|(16u<<16)|(244u<<4);
 if(load(&api))return 84;api.runtimeVersion=0;if(load(&api))return 85;
 auto run=(int(*)(const wchar_t*,const wchar_t*))GetProcAddress(dll,"D5X_Qualify");
 return run?run(args[2],args[3]):82;
}
