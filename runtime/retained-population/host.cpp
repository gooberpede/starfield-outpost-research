// SPDX-License-Identifier: GPL-3.0-or-later
// Disposable process only. The DLL refuses this entry from Starfield.
#include <Windows.h>
#include "../exp0002/third_party/sfse/PluginAPI.h"
int wmain(int n,wchar_t** v){if(n!=4)return 80;auto h=LoadLibraryW(v[1]);if(!h)return 81;
 auto load=(bool(*)(const SFSEInterface*))GetProcAddress(h,"SFSEPlugin_Load");
 SFSEInterface api{};api.interfaceVersion=1;api.runtimeVersion=(1u<<24)|(16u<<16)|(244u<<4);
 if(!load||load(nullptr)||load(&api))return 83;
 api.runtimeVersion=0;if(load(&api))return 84;
 auto run=(int(*)(const wchar_t*,const char*))GetProcAddress(h,"D5P_Qualify");if(!run)return 82;
 char scenario[100]{};size_t got{};wcstombs_s(&got,scenario,v[3],99);return run(v[2],scenario);
}
