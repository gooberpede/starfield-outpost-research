# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute pinned native lock helpers in private pages with controlled imports.

Reads installed PE and owned PE reader; writes fresh ignored D5AF receipt.
SOR-P-0002: D5AE private-page fixture method. No target process, saves, database,
network or Git mutation. Import callbacks model release/wake; not OS fairness.
"""
from pathlib import Path
import ctypes as C
import hashlib
import importlib.util
import json
import struct
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/resource-retained-population'))
from d5ad_baseline import guard,sha

def main():
    if not __debug__ or sys.flags.optimize or C.sizeof(C.c_void_p) != 8:
        raise RuntimeError('Use Windows x64 Python -E -B')
    guard()
    out=(ROOT/'.local-work/d5af'/sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT/'.local-work/d5af'):
        raise ValueError('Fresh task-local output required')
    out.mkdir()
    exe=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    if sha(exe)!='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':raise ValueError('PE identity')
    spec=importlib.util.spec_from_file_location('owned_pe',ROOT/'runtime/retained-population/build.py')
    pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
    data=exe.read_bytes();k=C.WinDLL('kernel32',use_last_error=True)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    tid=k.GetCurrentThreadId();lock=(C.c_uint32*2)(); waits=[];wakes=[];errors=[]
    mode=''
    @C.WINFUNCTYPE(C.c_int,C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32)
    def wait(address,comparison,size,timeout):
        waits.append(dict(state=lock[1],comparison=C.c_uint32.from_address(comparison).value,size=size,timeout=timeout))
        if address!=C.addressof(lock)+4 or size!=4 or timeout!=0xffffffff:errors.append('Wait operands')
        if mode not in ('writer-wait','reader-wait'):errors.append('Unexpected wait')
        # Controlled other-owner final release; no real OS wake/fairness claim.
        lock[0]=0;lock[1]=(lock[1]-0x401000)&0xffffffff
        return 1
    @C.WINFUNCTYPE(None,C.c_void_p)
    def single(address):wakes.append(('single',address-C.addressof(lock)))
    @C.WINFUNCTYPE(None,C.c_void_p)
    def allwake(address):wakes.append(('all',address-C.addressof(lock)))
    imports={0x143a3f418:k.GetCurrentThreadId,0x143a402d0:wait,0x143a402c8:single,0x143a402d8:allwake}
    page=k.VirtualAlloc(None,4096,0x3000,4)
    if not page:raise OSError('Allocation')
    ranges=[(0x1422cc350,126,0),(0x1422cc3d0,216,256),(0x1402c45a0,81,512)]
    original=[];relocations=[];slot=768
    try:
        for va,size,offset in ranges:
            b=bytearray(pe.pe_read(data,va-0x140000000,size));original.append(dict(va=hex(va),size=size,sha256=hashlib.sha256(b).hexdigest()))
            i=0
            while i<len(b)-5:
                if b[i:i+2] in (b'\xff\x15',b'\xff\x25'):
                    target=va+i+6+struct.unpack_from('<i',b,i+2)[0]
                    if target not in imports:raise ValueError(('Unexpected import',hex(target)))
                    C.c_uint64.from_address(page+slot).value=C.cast(imports[target],C.c_void_p).value
                    struct.pack_into('<i',b,i+2,slot-(offset+i+6));relocations.append(dict(site=hex(va+i),iat=hex(target),slot=slot));slot+=8;i+=6
                else:i+=1
            C.memmove(page+offset,bytes(b),size)
        old=C.c_ulong()
        if not k.VirtualProtect(page,4096,0x20,C.byref(old)):raise OSError('RX')
        if not k.FlushInstructionCache(k.GetCurrentProcess(),page,4096):raise OSError('Flush')
        call=lambda off:C.WINFUNCTYPE(None,C.c_void_p)(page+off)(C.addressof(lock))
        rows=[]
        def check(name,expected_owner,expected_state,expected_wakes=None):
            row=dict(case=name,owner=lock[0],state=hex(lock[1]),waits=list(waits),wakes=list(wakes))
            if lock[0]!=expected_owner or lock[1]!=expected_state or errors:raise AssertionError(row)
            if expected_wakes is not None and wakes!=expected_wakes:raise AssertionError(row)
            rows.append(row);waits.clear();wakes.clear()
        lock[:]=[0,0];call(256);check('exclusive-empty',tid,0x401000)
        call(256);check('exclusive-recursion',tid,0x801000)
        call(512);check('release-recursion',tid,0x401000,[])
        call(512);check('release-final-empty',0,0,[])
        lock[:]=[0,0x1000];call(256);check('later-writer-barges-registered-pending',tid,0x402000,[])
        call(512);check('final-release-wakes-one-pending',0,0x1000,[('single',4)])
        lock[:]=[0,0x1000];call(0);check('reader-admitted-despite-pending-writer',0,0x1001,[])
        lock[:]=[tid,0x401000];call(0);check('owner-shared-recursion',tid,0x401001,[])
        call(512);check('final-release-wakes-all-readers',0,1,[('all',4)])
        lock[:]=[tid^0x80000000,0x401000];mode='writer-wait';call(256)
        if len(waits)!=1:raise AssertionError('Writer wait not exercised')
        check('contended-writer-after-controlled-release',tid,0x401000,[])
        lock[:]=[tid^0x80000000,0x401000];mode='reader-wait';call(0)
        if len(waits)!=1:raise AssertionError('Reader wait not exercised')
        check('contended-reader-after-controlled-release',0,1,[])
        receipt=dict(passed=True,cases=rows,original_code=original,relocations=relocations,script_sha256=sha(__file__),executable_sha256=sha(exe),free=guard(),scope='Original lock helper bytes; import callbacks model release/wake. No actual OS wait, worker schedule, retail frequency or full provider execution.')
        (out/'control.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
        print(json.dumps(dict(cases=len(rows),passed=True,path=str(out))))
    finally:
        if not k.VirtualFree(page,0,0x8000):raise OSError('Page cleanup')

if __name__=='__main__':main()
