# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared offline file/receipt primitives. Stdlib only; never alters inputs."""
import ctypes
import datetime
import hashlib
import json
import os
from pathlib import Path

FLOOR = 40_000_000_000


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(path, pin=None):
    data = Path(path).read_bytes()
    if pin is not None and hashlib.sha256(data).hexdigest() != pin:
        raise ValueError('receipt_identity')
    return json.loads(data)


def fresh(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def now():
    return datetime.datetime.now(datetime.UTC).isoformat()


def available(drive):
    # Explicit caller-available bytes, not total volume free space.
    value = ctypes.c_ulonglong()
    api = ctypes.WinDLL('kernel32', use_last_error=True).GetDiskFreeSpaceExW
    api.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulonglong),
                    ctypes.c_void_p, ctypes.c_void_p]
    api.restype = ctypes.c_int
    if not api(drive, ctypes.byref(value), None, None):
        raise ctypes.WinError(ctypes.get_last_error())
    return value.value


def guard(required=None, query=available):
    values = {d: query(d) for d in ('C:/', 'D:/')}
    for d, n in values.items():
        if n < FLOOR + (required or {}).get(d, 0):
            raise ValueError('caller_available_disk_guard: ' + d)
    return values


def regular(path):
    path = Path(path).absolute()
    for p in (path, *path.parents):
        if p.is_symlink() or p.is_junction():
            raise ValueError('reparse_path: ' + str(p))
    return path


def inventory(root):
    root = regular(root)
    if not root.is_dir():
        raise ValueError('missing_inventory_root')
    result = {}
    for p in sorted(root.rglob('*')):
        regular(p)
        if p.is_file():
            before = p.stat()
            digest = sha(p)
            after = p.stat()
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                raise ValueError('input_changed_during_inventory: ' + str(p))
            result[p.relative_to(root).as_posix()] = dict(size=after.st_size, sha256=digest)
        elif not p.is_dir():
            raise ValueError('nonregular_input')
    return result


def tool_pins():
    return {str(p.resolve()): sha(p) for p in sorted(Path(__file__).parent.glob('*.py'))
            if not p.name.startswith('test_')}


def verify_pins(pins):
    for p, expected in pins.items():
        if sha(p) != expected:
            raise ValueError('pinned_input_changed: ' + p)
