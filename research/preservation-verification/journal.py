# SPDX-License-Identifier: GPL-3.0-or-later
"""Read NTFS identities and USN records through Windows APIs; never change a volume.

Windows only, stdlib ctypes. Unsupported versions, gaps and errors fail closed.
This records filesystem-mediated activity; it is not a storage-corruption oracle.
"""
import ctypes as c
from ctypes import wintypes as w
import struct


class JournalError(RuntimeError):
    pass


K = c.WinDLL('kernel32', use_last_error=True)
K.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, c.c_void_p, w.DWORD, w.DWORD, w.HANDLE]
K.CreateFileW.restype = w.HANDLE
K.DeviceIoControl.argtypes = [w.HANDLE, w.DWORD, c.c_void_p, w.DWORD, c.c_void_p, w.DWORD, c.POINTER(w.DWORD), c.c_void_p]
K.DeviceIoControl.restype = w.BOOL
K.GetFileInformationByHandle.argtypes = [w.HANDLE, c.c_void_p]
K.GetFileInformationByHandle.restype = w.BOOL
K.CloseHandle.argtypes = [w.HANDLE]
INVALID = c.c_void_p(-1).value


def open_handle(path, volume=False):
    h = K.CreateFileW(str(path), 0, 7, None, 3,
                      0 if volume else 0x02200000, None)
    if h == INVALID:
        raise JournalError(str(c.WinError(c.get_last_error())))
    return h


def identity(path):
    """Return volume serial and NTFS file reference; reject reparse identities."""
    h = open_handle(path)
    try:
        data = c.create_string_buffer(52)
        if not K.GetFileInformationByHandle(h, data):
            raise JournalError(str(c.WinError(c.get_last_error())))
        attrs, = struct.unpack_from('<I', data.raw)
        if attrs & 0x400:
            raise JournalError('Reparse point')
        volume, = struct.unpack_from('<I', data.raw, 28)
        high, low = struct.unpack_from('<II', data.raw, 44)
        return volume, (high << 32) | low
    finally:
        K.CloseHandle(h)


def ioctl(h, code, payload=b''):
    out = c.create_string_buffer(1024 * 1024)
    count = w.DWORD()
    inp = c.create_string_buffer(payload) if payload else None
    if not K.DeviceIoControl(h, code, inp, len(payload), out, len(out), c.byref(count), None):
        raise JournalError(str(c.WinError(c.get_last_error())))
    return out.raw[:count.value]


def query(volume):
    h = open_handle(volume + '\\')
    try:
        raw = ioctl(h, 0x000900f4)
        if len(raw) < 56:
            raise JournalError('Truncated journal metadata')
        jid, first, nxt, lowest, maximum, size, delta = struct.unpack_from('<QqqqqQQ', raw)
        return dict(id=jid, first=first, next=nxt, lowest=lowest)
    finally:
        K.CloseHandle(h)


def validate_cursor(old, now):
    if old['id'] != now['id'] or old['next'] < max(now['first'], now['lowest']) or old['next'] > now['next']:
        raise JournalError('Journal identity/continuity gap')


def decode(raw):
    if len(raw) < 8:
        raise JournalError('Truncated journal page')
    nxt, = struct.unpack_from('<q', raw)
    rows = []
    offset = 8
    while offset < len(raw):
        if len(raw) - offset < 60:
            raise JournalError('Truncated USN record')
        length, major, minor = struct.unpack_from('<IHH', raw, offset)
        if major != 2 or length < 60 or length % 8 or offset + length > len(raw):
            raise JournalError('Unsupported/corrupt USN record')
        frn, parent, usn = struct.unpack_from('<QQq', raw, offset + 8)
        reason, = struct.unpack_from('<I', raw, offset + 40)
        rows.append((frn, parent, usn, reason))
        offset += length
    return nxt, rows


def read_since(volume, old):
    now = query(volume)
    validate_cursor(old, now)
    cursor = old['next']
    rows = []
    nbytes = 0
    h = open_handle(volume + '\\')
    try:
        while cursor < now['next']:
            raw = ioctl(h, 0x000903ab, struct.pack('<qIIQQQ', cursor, 0xffffffff, 0, 0, 0, old['id']))
            nbytes += len(raw)
            nxt, page = decode(raw)
            if nxt <= cursor:
                raise JournalError('Interrupted/non-progressing journal scan')
            rows.extend(row for row in page if row[2] < now['next'])
            cursor = nxt
        validate_cursor(old, query(volume))
        return rows, nbytes, now
    finally:
        K.CloseHandle(h)
