# SPDX-License-Identifier: GPL-3.0-or-later
"""Read installed PE strings and pointer references into exclusive local evidence.

This original read-only method uses installed CPython/Windows facilities. It
reads the pinned executable and writes one ignored JSON receipt. It does not
execute native game instructions, open an analysis project, load a plugin, or
write protected inputs. Source-informed console leads are credited in the D5AR
native investigation; no SFSE implementation or structure declaration is reused.
"""
import os
import sys
if sys.flags.optimize or not __debug__ or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Optimization forbidden; invoke pinned Python -E -B')

import ctypes
import hashlib
import json
import mmap
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
PIN = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def disk_floor():
    result = {}
    api = ctypes.WinDLL('kernel32', use_last_error=True).GetDiskFreeSpaceExW
    api.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_void_p, ctypes.c_void_p]
    for drive in ('C:/', 'D:/'):
        value = ctypes.c_ulonglong()
        if not api(drive, ctypes.byref(value), None, None):
            raise OSError(ctypes.get_last_error(), 'Caller-available free-space query failed')
        if value.value < 40_000_000_000:
            raise RuntimeError(f'Disk floor failed: {drive} {value.value}')
        result[drive] = value.value
    return result


def main():
    destination = Path(sys.argv[1]).resolve()
    if not destination.is_relative_to(ROOT / '.local-work') or destination.exists():
        raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination, *destination.parents)):
        raise ValueError('Reparse output refused')
    before = disk_floor()
    with EXE.open('rb') as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        actual = hashlib.sha256(data).hexdigest()
        if actual != PIN:
            raise ValueError('Installed PE identity mismatch')
        pe = struct.unpack_from('<I', data, 0x3c)[0]
        count = struct.unpack_from('<H', data, pe + 6)[0]
        optional = struct.unpack_from('<H', data, pe + 20)[0]
        base = struct.unpack_from('<Q', data, pe + 48)[0]
        if base != 0x140000000:
            raise ValueError('Unexpected image base')
        sections = []
        for index in range(count):
            at = pe + 24 + optional + 40 * index
            virtual_size, rva, raw_size, raw = struct.unpack_from('<IIII', data, at + 8)
            sections.append((rva, virtual_size, raw, raw_size))

        def va(offset):
            for rva, _, raw, size in sections:
                if raw <= offset < raw + size:
                    return base + rva + offset - raw
            return None

        rows = []
        for name in ('BetaComment', 'GameComment', 'ToggleGodMode', 'GetSFSEVersion'):
            start = 0
            while True:
                at = data.find(name.encode('ascii') + b'\0', start)
                if at < 0:
                    break
                start = at + 1
                address = va(at)
                refs = []
                if address is not None:
                    needle = struct.pack('<Q', address)
                    search = 0
                    while True:
                        pointer = data.find(needle, search)
                        if pointer < 0:
                            break
                        search = pointer + 1
                        refs.append(dict(file_offset=pointer, static_va=va(pointer)))
                rip_leads = []
                if address is not None:
                    for rva, _, raw, size in sections:
                        for prefix in (b'\x48\x8d', b'\x4c\x8d'):
                            search = raw
                            while True:
                                instruction = data.find(prefix, search, raw + size)
                                if instruction < 0:
                                    break
                                search = instruction + 1
                                if instruction + 7 > raw + size or data[instruction + 2] & 0xc7 != 5:
                                    continue
                                target = base + rva + instruction - raw + 7 + struct.unpack_from('<i', data, instruction + 3)[0]
                                if target == address:
                                    rip_leads.append(dict(file_offset=instruction, static_va=va(instruction)))
                rows.append(dict(name=name, file_offset=at, static_va=address, references=refs,
                                 rip_relative_lea_candidates=rip_leads))
    receipt = dict(schema='sor-d5ar/native-inventory/1', method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   interpreter_sha256=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
                   exe_sha256=actual, image_base=base, strings=rows, free_before=before, free_after=disk_floor(),
                   scope='STATIC string and full-pointer discovery; not table-layout or dispatch qualification')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf8', newline='\n') as output:
        json.dump(receipt, output, indent=2)
        output.write('\n')
    print(destination)


if __name__ == '__main__':
    main()
