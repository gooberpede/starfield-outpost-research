# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute six bounded original reserve-helper controls in this process only.

Reads the pinned installed EXE and owned PE reader. Copies exactly one helper
to a private RX page, supplies synthetic recording allocation callbacks and
writes fresh ignored JSONL/final receipts. No engine allocator, game, save,
database, configuration, deployment, network or Git effects. Six calls only;
callbacks report success/failure without allocating array storage. This is a
helper control, not a complete array/allocator fixture. Normal cleanup frees
the private page; an unhandled fault preserves the flushed case prefix.
"""
import ctypes as C
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
EXE=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
EXPECTED='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def main():
    assert os.name=='nt' and C.sizeof(C.c_void_p)==8
    out=Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work') and not out.exists()
    kernel=C.WinDLL('kernel32',use_last_error=True)
    kernel.GetDiskFreeSpaceExW.argtypes=[C.c_wchar_p,C.POINTER(C.c_ulonglong),C.c_void_p,C.c_void_p]
    free={}
    for drive in ('C:/','D:/'):
        value=C.c_ulonglong()
        assert kernel.GetDiskFreeSpaceExW(drive,C.byref(value),None,None)
        free[drive]=value.value
    assert min(free.values())>=40_000_000_000 and sha(EXE)==EXPECTED
    method=ROOT/'runtime/retained-population/build.py'
    spec=importlib.util.spec_from_file_location('owned_d5z_pe',method)
    reader=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    code=reader.pe_read(EXE.read_bytes(),0x22cc0d0,0x81)
    assert len(code)==0x81 and code[-1]==0xc3
    kernel.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong]
    kernel.VirtualAlloc.restype=C.c_void_p
    kernel.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    kernel.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong]
    kernel.GetCurrentProcess.restype=C.c_void_p
    kernel.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    page=kernel.VirtualAlloc(None,4096,0x3000,0x04)
    assert page
    out.mkdir(parents=True)
    records=[]
    try:
        C.memmove(page,code,len(code))
        old=C.c_ulong()
        assert kernel.VirtualProtect(page,4096,0x20,C.byref(old))
        assert kernel.FlushInstructionCache(kernel.GetCurrentProcess(),page,len(code))
        reserve=C.WINFUNCTYPE(C.c_uint32,C.c_void_p,C.c_void_p,C.c_uint32,C.c_uint32)(page)
        invoked=[]
        success=False
        @C.WINFUNCTYPE(C.c_uint8,C.c_void_p,C.c_uint32,C.c_uint32)
        def initialize(owner,requested,width):
            invoked.append(dict(callback='initialize',requested=requested,width=width))
            return int(success)
        @C.WINFUNCTYPE(C.c_uint8,C.c_void_p,C.c_uint32,C.c_uint32,C.c_uint32,C.c_uint32,C.c_uint32)
        def grow(owner,requested,used,flag,extra,width):
            invoked.append(dict(callback='grow',requested=requested,used=used,flag=flag,extra=extra,width=width))
            return int(success)
        table=(C.c_void_p*2)(C.cast(initialize,C.c_void_p).value,C.cast(grow,C.c_void_p).value)
        cases=[(0,4,False,0,1,None),(3,4,False,3,4,None),
               (0,0,False,0xffffffff,0,'initialize'),(0,0,True,0,1,'initialize'),
               (4,4,False,0xffffffff,4,'grow'),(4,4,True,4,5,'grow')]
        with (out/'cases.jsonl').open('x',encoding='utf8',newline='\n') as stream:
            for count,capacity,success,expected,after,callback in cases:
                current=C.c_uint32(count)
                functor=(C.c_void_p*2)(C.addressof(table),C.addressof(current))
                invoked.clear()
                result=reserve(C.byref(current),C.addressof(functor),capacity,8)
                record=dict(count=count,capacity=capacity,callback_success=success,
                            returned=result,count_after=current.value,callbacks=list(invoked))
                stream.write(json.dumps(record)+'\n');stream.flush();os.fsync(stream.fileno())
                assert result==expected and current.value==after
                assert len(invoked)==int(callback is not None)
                if callback:
                    assert invoked[0]['callback']==callback and invoked[0]['requested']==count+1 and invoked[0]['width']==8
                records.append(record)
    finally:
        assert kernel.VirtualFree(page,0,0x8000)
    assert sha(EXE)==EXPECTED
    receipt=dict(schema='sor-d5z-reserve-control/1',passed=True,game_process=False,
                 executable_sha256=EXPECTED,preferred_static_va='0x1422cc0d0',code_bytes=len(code),
                 code_sha256=hashlib.sha256(code).hexdigest(),script_sha256=sha(__file__),
                 pe_reader_sha256=sha(method),free=free,cases=records,
                 substitutions='Recording true/false callbacks; no array backing allocation or engine allocator.',
                 limit='Tests reserve index/count/failure sentinel only; no full array growth, OOM, reset or retail claim.')
    (out/'control.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(cases=len(records),passed=True,receipt=str(out/'control.json'))))

if __name__=='__main__':
    main()
