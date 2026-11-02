# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute bounded original owner-installation predicates on owned objects.

Reads pinned PE bytes and retained native metadata; writes a fresh ignored JSON
receipt. Original branch/store bytes execute at preferred addresses. Owned reset
callbacks model the independently traced clear consequence; native nonzero
setter services are skipped after the actual owner store, through its original
epilogue. Entry/exit adapters isolate these explicitly bounded predicates.
No game, save, analysis database, network, deployment or installed writes occur.
Stop on pin, disk, mapping, callback or oracle failure; disposable host exits.
SOR-P-0002: private-page mapping adapted from d5ai_ownership_native.py.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B without -O/-OO')
from pathlib import Path
import ctypes as C
import faulthandler
import hashlib
import json
import struct

faulthandler.enable()
ROOT=Path(__file__).resolve().parents[2]
out=(ROOT/sys.argv[1]).resolve()
if not out.is_relative_to(ROOT/'.local-work/d5ai-ownership') or out.exists():
    raise ValueError('Fresh ignored output required')
free={}
for drive in ('C:/','D:/'):
    n=C.c_ulonglong()
    if not C.windll.kernel32.GetDiskFreeSpaceExW(C.c_wchar_p(drive),C.byref(n),None,None):raise OSError(drive)
    if n.value<40_000_000_000:raise RuntimeError('Disk floor')
    free[drive]=n.value
exe=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
data=exe.read_bytes(); sha=lambda b:hashlib.sha256(b).hexdigest()
if sha(data)!='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':raise ValueError('PE mismatch')
export=ROOT/'.local-work/d5v/export01/native.tsv'
if sha(export.read_bytes())!='10b853e420d4aa5e97935bb5591bc16a23d15cfa1db2a692fee0ca00754f66e3':raise ValueError('Export mismatch')
pe=struct.unpack_from('<I',data,0x3c)[0]; opt=struct.unpack_from('<H',data,pe+20)[0]
sections=[struct.unpack_from('<IIII',data,pe+24+opt+i*40+8) for i in range(struct.unpack_from('<H',data,pe+6)[0])]
def original(va,size):
    for vs,rva,n,raw in sections:
        r=va-0x140000000
        if rva<=r and r+size<=rva+n:return data[raw+r-rva:raw+r-rva+size]
    raise ValueError(hex(va))
k=C.WinDLL('kernel32',use_last_error=True);k.SetErrorMode(0x8003)
k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
k.GetCurrentProcess.restype=C.c_void_p;k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
pages=set();regions=set()
def write(va,b):
    for page in range(va&~4095,(va+len(b)+4095)&~4095,4096):
        if page not in pages:
            region=page&~65535
            if region not in regions:
                if k.VirtualAlloc(region,65536,0x2000,4)!=region:raise OSError('Reserve')
                regions.add(region)
            if k.VirtualAlloc(page,4096,0x1000,4)!=page:raise OSError('Commit')
            pages.add(page)
    C.memmove(va,b,len(b))

# Preserve the original relative branches/calls at their preferred addresses.
install=(0x140789d53,0x14078a0d9)
setter=(0x14078a120,0x14078a5a6)
write(install[0],original(install[0],install[1]-install[0]))
write(setter[0],original(setter[0],setter[1]-setter[0]))
reset_log=[]
@C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_uint64,C.c_uint64,C.c_uint64)
def reset_true(manager,b,c,d):
    before=C.c_uint32.from_address(manager+0x80).value
    reset_log.append(dict(kind='true-reset',owner_before=before))
    C.c_uint32.from_address(manager+0x80).value=0
    return 0
@C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_uint64,C.c_uint64,C.c_uint64)
def reset_false(manager,b,c,d):
    reset_log.append(dict(kind='false-reset',owner_before=C.c_uint32.from_address(manager+0x80).value))
    return 0
for va,callback in ((0x140788e70,reset_true),(0x140789850,reset_false)):
    write(va,b'\x48\xb8'+struct.pack('<Q',C.cast(callback,C.c_void_p).value)+b'\xff\xe0')
# The same-owner/null-world branch compares against the native default component.
write(0x144a4b780,b'\0'*8)
exit_address=0x14078f100
for site in (0x140789e15,0x140789ff0,0x14078a024,0x14078a0d9):
    write(site,b'\xe9'+struct.pack('<i',exit_address-(site+5)))
# Execute the actual setter owner store and zero-input branch, skipping unrelated
# resource-definition/UI services only on its nonzero-input path.
write(0x14078a16e,b'\xe9'+struct.pack('<i',0x14078a588-(0x14078a16e+5)))
adapter=0x14078f000
prologue=(b'\x53\x55\x56\x57\x41\x54\x41\x55\x41\x56\x41\x57'
          +b'\x48\x83\xec\x68'+b'\x49\x89\xcf'+b'\x89\xd3'+b'\x4c\x89\xc6'
          +b'\x4d\x89\xcd'+b'\x48\xb8'+struct.pack('<Q',install[0])+b'\xff\xe0')
write(adapter,prologue)
epilogue=(b'\x41\x8b\x87\x80\x00\x00\x00'+b'\x41\x89\x45\x00'
          +b'\x48\x83\xc4\x68'+b'\x41\x5f\x41\x5e\x41\x5d\x41\x5c\x5f\x5e\x5d\x5b\xc3')
write(exit_address,epilogue)
for p in pages:
    old=C.c_ulong()
    protection=4 if p==0x144a4b000 else 0x20
    if not k.VirtualProtect(p,4096,protection,C.byref(old)):raise OSError('Protect')
if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise OSError('Flush')
run=C.WINFUNCTYPE(None,C.c_void_p,C.c_uint32,C.c_void_p,C.c_void_p)(adapter)
set_owner=C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_uint32)(setter[0])
rows=[]
def test(name,old,incoming,component,expected,kinds):
    manager=C.create_string_buffer(0x220);world=C.create_string_buffer(8);request=C.create_string_buffer(8);result=C.c_uint32()
    struct.pack_into('<Q',manager,0x78,C.addressof(world));struct.pack_into('<I',manager,0x80,old)
    struct.pack_into('<Q',request,0,component)
    reset_log.clear()
    run(C.addressof(manager),incoming,C.addressof(request),C.byref(result))
    if result.value!=expected or [v['kind'] for v in reset_log]!=kinds:
        raise AssertionError((name,result.value,reset_log))
    rows.append(dict(case=name,old_owner=old,incoming_owner=incoming,incoming_component=component,owner_after=result.value,resets=list(reset_log)))
test('changed-nonzero-owner-resets-before-store',0x5e0de,0x1234,0,0x1234,['true-reset'])
test('initial-zero-owner-installs-without-reset',0,0x5e0de,0,0x5e0de,[])
test('same-owner-component-reinstall-false-resets',0x5e0de,0x5e0de,0,0x5e0de,['false-reset'])
test('same-owner-changed-component-resets-before-recursion',0x5e0de,0x5e0de,1,0,['true-reset'])
test('incoming-zero-owner-resets',0x5e0de,0,0,0,['true-reset'])
test('owner-ABA-first-leg-invalidates',0x5e0de,0x1234,0,0x1234,['true-reset'])
test('owner-ABA-return-leg-invalidates',0x1234,0x5e0de,0,0x5e0de,['true-reset'])
manager=C.create_string_buffer(0x220);struct.pack_into('<I',manager,0x80,0x5e0de)
set_owner(C.addressof(manager),0)
if C.c_uint32.from_buffer(manager,0x80).value!=0:raise AssertionError('Native setter zero path')
rows.append(dict(case='actual-setter-zero-input-clears-owner',owner_after=0))
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(dict(scope='Original owner-installation branch/store slices on owned objects. Reset callbacks model independently traced clear; nonzero setter services and post-reset continuation skipped. No whole manager initialization or retail execution.',
                 method_sha256=sha(Path(__file__).read_bytes()),executable_sha256=sha(data),
                 native_ranges=[dict(start=hex(a),end_exclusive=hex(z),sha256=sha(original(a,z-a))) for a,z in (install,setter)],
                 owned_exit_sites=[hex(x) for x in (0x140789e15,0x140789ff0,0x14078a024,0x14078a0d9,0x14078a16e)],
                 free=free,rows=rows),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS',len(rows),out)
