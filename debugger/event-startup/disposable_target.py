# SPDX-License-Identifier: GPL-3.0-or-later
"""Original disposable Python target; optional empty process DACL denies new opens.

No game access. Uses OS ctypes only. Restores its own saved DACL on RELEASE/EOF
and exits normally; parent retains its original process handle throughout.
"""
import ctypes as C
from ctypes import wintypes as W
import json
import os
import sys

kernel = C.WinDLL('kernel32', use_last_error=True)
advapi = C.WinDLL('advapi32', use_last_error=True)
kernel.GetCurrentProcess.restype = W.HANDLE
advapi.GetKernelObjectSecurity.argtypes = [W.HANDLE, W.DWORD, C.c_void_p, W.DWORD, C.POINTER(W.DWORD)]
advapi.GetKernelObjectSecurity.restype = W.BOOL
advapi.SetKernelObjectSecurity.argtypes = [W.HANDLE, W.DWORD, C.c_void_p]
advapi.SetKernelObjectSecurity.restype = W.BOOL
advapi.InitializeSecurityDescriptor.argtypes = [C.c_void_p, W.DWORD]
advapi.InitializeAcl.argtypes = [C.c_void_p, W.DWORD, W.DWORD]
advapi.SetSecurityDescriptorDacl.argtypes = [C.c_void_p, W.BOOL, C.c_void_p, W.BOOL]
handle = kernel.GetCurrentProcess()
saved = None
if sys.argv[1:] == ['deny-open']:
    size = W.DWORD()
    advapi.GetKernelObjectSecurity(handle, 4, None, 0, C.byref(size))
    saved = C.create_string_buffer(size.value)
    if not advapi.GetKernelObjectSecurity(handle, 4, saved, size, C.byref(size)):
        raise C.WinError(C.get_last_error())
    sd, acl = C.create_string_buffer(64), C.create_string_buffer(8)
    if not (advapi.InitializeSecurityDescriptor(sd, 1) and advapi.InitializeAcl(acl, 8, 2)
            and advapi.SetSecurityDescriptorDacl(sd, True, acl, False)
            and advapi.SetKernelObjectSecurity(handle, 4, sd)):
        raise C.WinError(C.get_last_error())
try:
    print(json.dumps({'pid': os.getpid(), 'empty_DACL': saved is not None}), flush=True)
    sys.stdin.readline()
finally:
    if saved is not None and not advapi.SetKernelObjectSecurity(handle, 4, saved):
        raise C.WinError(C.get_last_error())
print('NORMAL_EXIT_DACL_RESTORED', flush=True)
