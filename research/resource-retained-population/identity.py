# SPDX-License-Identifier: GPL-3.0-or-later
"""Read Windows process/token identity before consuming a live admission.

Uses installed Win32 APIs through ctypes. Query handles only; no attachment,
privilege changes, process mutation or writes. Synthetic dictionaries can test
the predicate independently; they never authorize a target operation.
"""
import ctypes as c
from ctypes import wintypes as w


def compatible(caller, target):
    return (caller['sid'] == target['sid'] and caller['session'] == target['session']
            and not caller['elevated'] and not target['elevated']
            and 'codexsandbox' not in caller['account'].lower())


def snapshot(pid):
    k = c.WinDLL('kernel32', use_last_error=True)
    a = c.WinDLL('advapi32', use_last_error=True)
    k.OpenProcess.argtypes = (w.DWORD,w.BOOL,w.DWORD); k.OpenProcess.restype = w.HANDLE
    k.CloseHandle.argtypes = (w.HANDLE,); k.CloseHandle.restype = w.BOOL
    k.LocalFree.argtypes = (w.HLOCAL,); k.LocalFree.restype = w.HLOCAL
    a.OpenProcessToken.argtypes = (w.HANDLE,w.DWORD,c.POINTER(w.HANDLE))
    a.GetTokenInformation.argtypes = (w.HANDLE,c.c_int,c.c_void_p,w.DWORD,c.POINTER(w.DWORD))
    a.ConvertSidToStringSidW.argtypes = (c.c_void_p,c.POINTER(w.LPWSTR))
    a.LookupAccountSidW.argtypes = (w.LPCWSTR,c.c_void_p,w.LPWSTR,c.POINTER(w.DWORD),w.LPWSTR,c.POINTER(w.DWORD),c.POINTER(w.DWORD))
    k.ProcessIdToSessionId.argtypes = (w.DWORD,c.POINTER(w.DWORD))
    def check(ok):
        if not ok: raise c.WinError(c.get_last_error())
    process = k.OpenProcess(0x1000,False,pid)
    check(process); token = w.HANDLE()
    try:
        check(a.OpenProcessToken(process,8,c.byref(token)))
        user = c.create_string_buffer(4096); size = w.DWORD()
        check(a.GetTokenInformation(token,1,user,len(user),c.byref(size)))
        sid = c.cast(user,c.POINTER(c.c_void_p))[0]
        string = w.LPWSTR()
        check(a.ConvertSidToStringSidW(sid,c.byref(string)))
        try: sid_text = string.value
        finally: check(k.LocalFree(c.cast(string,w.HLOCAL)) is None)
        name = c.create_unicode_buffer(256); domain = c.create_unicode_buffer(256)
        ns = w.DWORD(256); ds = w.DWORD(256); use = w.DWORD()
        check(a.LookupAccountSidW(None,sid,name,c.byref(ns),domain,c.byref(ds),c.byref(use)))
        elevation = w.DWORD(); session = w.DWORD()
        check(a.GetTokenInformation(token,20,c.byref(elevation),4,c.byref(size)))
        check(k.ProcessIdToSessionId(pid,c.byref(session)))
        return dict(pid=pid,sid=sid_text,account=domain.value+'\\'+name.value,
                    elevated=bool(elevation.value),session=session.value)
    finally:
        if token: check(k.CloseHandle(token))
        check(k.CloseHandle(process))


def require_ordinary(pid):
    import os
    caller, target = snapshot(os.getpid()), snapshot(pid)
    if not compatible(caller,target):
        raise RuntimeError(f'Ordinary-user caller/target mismatch before admission consumption: {caller!r}; {target!r}')
    return dict(caller=caller,target=target)
