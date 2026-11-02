# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute two original rank/serial bound searches in a disposable process.

Reads the pinned installed PE, owned PE reader and D5AE export06. Copies two
101-byte leaf helpers into private executable pages, supplies bounded synthetic
tree nodes, and compares indices against independent Python tuple ordering.
Writes fresh ignored results; frees private pages on normal exit. No game,
save, original/copy Ghidra, configuration, network or Git effects. Native ABI
fault risk is confined to this process. Stop on identity, guard or oracle fault.
SOR-P-0002: D5AD readiness private-page fixture method and D5AE native research.
"""
import ctypes as C
import importlib.util
import json
from pathlib import Path
import re
import struct
import sys

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize or C.sizeof(C.c_void_p) != 8:
        raise RuntimeError('Use Windows x64 Python -E -B')
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ae'):
        raise ValueError('Fresh task-local output required')
    free = guard()
    native = ROOT / '.local-work/d5ae/export06/native.tsv'
    if sha(native) != 'f8815fdb3e646848902eb377e95e2c323ba8f6d21b73cc9a8210d3d9a913eca1':
        raise ValueError('Native locator changed')
    exe = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    if sha(exe) != '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':
        raise ValueError('Wrong executable')
    method = ROOT / 'runtime/retained-population/build.py'
    spec = importlib.util.spec_from_file_location('ae_rank_pe', method)
    pe = importlib.util.module_from_spec(spec); spec.loader.exec_module(pe)
    data = exe.read_bytes()
    k = C.WinDLL('kernel32', use_last_error=True)
    k.VirtualAlloc.argtypes = [C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong]
    k.VirtualAlloc.restype = C.c_void_p
    k.VirtualProtect.argtypes = [C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.VirtualFree.argtypes = [C.c_void_p,C.c_size_t,C.c_ulong]
    k.GetCurrentProcess.restype = C.c_void_p
    k.FlushInstructionCache.argtypes = [C.c_void_p,C.c_void_p,C.c_size_t]
    rows = []
    out.mkdir(parents=True)
    with (out/'cases.jsonl').open('x',encoding='utf8',newline='\n') as log:
        for va, start in ((0x1406dd4f0,0x18),(0x1406db950,8)):
            code = pe.pe_read(data, va-0x140000000, 101)
            if code[-1] != 0xc3:
                raise ValueError('Helper extent')
            page = k.VirtualAlloc(None,4096,0x3000,4)
            if not page:
                raise OSError('Private allocation failed')
            try:
                C.memmove(page,code,len(code)); old=C.c_ulong()
                if not k.VirtualProtect(page,4096,0x20,C.byref(old)):
                    raise OSError('RX protection failed')
                if not k.FlushInstructionCache(k.GetCurrentProcess(),page,len(code)):
                    raise OSError('Instruction cache flush failed')
                search=C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_void_p,C.c_void_p)(page)
                for keys in ([],[(0,0)],[(0,2),(0,9),(1,0),(0xffffffff,0xffffffffffffffff)]):
                    for query in ((0,0),(0,2),(0,8),(0,9),(1,0),(1,3),(0xffffffff,0xffffffffffffffff)):
                        node=C.create_string_buffer(256)
                        struct.pack_into('<I',node,4,len(keys))
                        for i,(rank,serial) in enumerate(keys):
                            struct.pack_into('<I4xQ',node,start+i*16,rank,serial)
                        operand=C.create_string_buffer(struct.pack('<I4xQ',*query))
                        before=node.raw
                        result=search(None,C.addressof(node),C.addressof(operand))
                        expected=sum(key < query for key in keys)
                        row=dict(static_va=hex(va),keys=keys,query=query,result=result,expected=expected)
                        log.write(json.dumps(row)+'\n');log.flush()
                        if result != expected or node.raw != before:
                            raise AssertionError(row)
                        rows.append(row)
            finally:
                if not k.VirtualFree(page,0,0x8000):
                    raise OSError('Private page cleanup failed')
    result=dict(cases=len(rows),passed=True,free=free,script_sha256=sha(__file__),
                executable_sha256=sha(exe),pe_reader_sha256=sha(method),
                native_sha256=sha(native),scope='Rank/serial bound helpers only; no full ready tree or worker scheduler')
    (out/'control.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
