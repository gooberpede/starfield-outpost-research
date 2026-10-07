// SPDX-License-Identifier: GPL-3.0-or-later
// Original debugger qualification target. No game/save access. Reads only its
// operator trigger path, waits at most 60 seconds, then exits normally.
#include <windows.h>
#include <cstdio>
extern "C" __declspec(dllexport) __declspec(noinline)
void sor_marker(unsigned long long a, unsigned long long b,
                unsigned long long c, unsigned long long d) {
    volatile auto value = a + b + c + d;
    (void)value;
}
DWORD WINAPI worker(void*) { sor_marker(5,6,7,8); return 0; }
int wmain(int argc, wchar_t** argv) {
    if (argc != 2 && argc != 3) return 2;
    const auto start = GetTickCount64();
    while (GetTickCount64()-start < 60000) {
        if (GetFileAttributesW(argv[1]) != INVALID_FILE_ATTRIBUTES) {
            for (int i=0; i<(argc==3 ? 100 : 1); ++i) sor_marker(1,2,3,4);
            auto t = CreateThread(nullptr,0,worker,nullptr,0,nullptr);
            if (t) { WaitForSingleObject(t,2000); CloseHandle(t); }
            Sleep(3000);
            return 0;
        }
        Sleep(20);
    }
    return 0;
}
