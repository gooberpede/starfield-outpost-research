# SPDX-License-Identifier: GPL-3.0-or-later
"""Windows process identity/read/detach verification, no write/control APIs.

Uses installed OS functions via CPython ctypes, no third-party bindings.
Reads only the requested PID and explicit byte ranges (maximum 4096 bytes).
"""
import ctypes as C
from ctypes import wintypes as W

K = C.WinDLL('kernel32', use_last_error=True)
K.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.OpenProcess.restype = W.HANDLE
K.CloseHandle.argtypes = [W.HANDLE]
K.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
K.QueryFullProcessImageNameW.restype = W.BOOL
K.CheckRemoteDebuggerPresent.argtypes = [W.HANDLE, C.POINTER(W.BOOL)]
K.CheckRemoteDebuggerPresent.restype = W.BOOL
K.ReadProcessMemory.argtypes = [W.HANDLE, C.c_void_p, C.c_void_p, C.c_size_t, C.POINTER(C.c_size_t)]
K.ReadProcessMemory.restype = W.BOOL
K.GetExitCodeProcess.argtypes = [W.HANDLE, C.POINTER(W.DWORD)]
K.GetExitCodeProcess.restype = W.BOOL


class ProcessRead:
    def __init__(self, pid):
        self.handle = K.OpenProcess(0x410, False, pid)  # QUERY_INFORMATION | VM_READ
        if not self.handle:
            raise C.WinError(C.get_last_error())

    def close(self):
        K.CloseHandle(self.handle)

    def path(self):
        path = C.create_unicode_buffer(32768)
        length = W.DWORD(len(path))
        if not K.QueryFullProcessImageNameW(self.handle, 0, path, C.byref(length)):
            raise C.WinError(C.get_last_error())
        return path.value

    def debugged(self):
        value = W.BOOL()
        if not K.CheckRemoteDebuggerPresent(self.handle, C.byref(value)):
            raise C.WinError(C.get_last_error())
        return bool(value.value)

    def alive(self):
        value = W.DWORD()
        if not K.GetExitCodeProcess(self.handle, C.byref(value)):
            raise C.WinError(C.get_last_error())
        return value.value == 259

    def read(self, address, size):
        if not 0 < address < 0x800000000000 or not 0 < size <= 4096:
            raise ValueError('Invalid bounded read')
        buffer = C.create_string_buffer(size)
        count = C.c_size_t()
        if not K.ReadProcessMemory(self.handle, address, buffer, size, C.byref(count)) or count.value != size:
            raise C.WinError(C.get_last_error())
        return buffer.raw
