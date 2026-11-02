# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute the original area-map traversal/release interval on owned objects.

Reads pinned PE bytes and retained native metadata; writes a fresh ignored JSON
receipt. Original traversal bytes execute at their preferred addresses. An owned
callback supplies success/failure schedules. A relocated original release block
preserves its branch offsets, with one explicitly rebound RIP-relative import.
Owned entry/exit adapters record pre-release EDX and post-release iterator/state.
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
entry=0x1421e09f2;end=0x1421e0aa5;release=0x1421e0a79
raw=original(entry,end-entry)
write(entry,raw)
calls=[];errors=[];slot_base=0;fail_at=None
@C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_void_p,C.c_void_p)
def callback(context,unused,slot):
    index=(slot-slot_base-8)//24
    if slot!=slot_base+index*24+8:errors.append('Callback slot')
    calls.append(index)
    return 0 if index==fail_at else 1
write(0x1421e0f50,b'\x48\xb8'+struct.pack('<Q',C.cast(callback,C.c_void_p).value)+b'\xff\xe0')
# The relocated release bytes have unchanged intra-block branches. Only their
# RIP-relative WakeByAddressSingle import displacement changes by relocation.
release_original=original(release,end-release)
relocated=0x1421e0b04
release_bytes=bytearray(release_original)
iat_at=0x1421e0a9f-release
if release_bytes[iat_at:iat_at+2]!=b'\xff\x15':raise ValueError('Import opcode')
old_target=0x1421e0a9f+6+struct.unpack_from('<i',release_bytes,iat_at+2)[0]
if old_target!=0x143a402c8:raise ValueError('Import target')
struct.pack_into('<i',release_bytes,iat_at+2,old_target-(relocated+iat_at+6))
write(release,b'\xe9'+struct.pack('<i',0x1421e0b00-(release+5)))
write(0x1421e0b00,b'\x41\x89\x55\x00'+release_bytes)
epilogue=(b'\x49\x89\x7d\x08'+b'\x4d\x89\x65\x10'+b'\x41\x89\x55\x18'
          +b'\x8b\x43\x04'+b'\x41\x89\x45\x1c'+b'\x48\x81\xc4\x10\x01\x00\x00'
          +b'\x41\x5f\x41\x5d\x41\x5c\x5f\x5e\x5d\x5b\xc3')
write(relocated+len(release_bytes),epilogue)
wakes=C.c_uint64()
wake=0x1421e0d00
write(wake,b'\x48\xb8'+struct.pack('<Q',C.addressof(wakes))+b'\x48\xff\x00\xba\xef\xbe\xad\xde\xc3')
write(0x143a402c8,struct.pack('<Q',wake))
adapter=0x1421e0c00
prologue=(b'\x53\x55\x56\x57\x41\x54\x41\x55\x41\x57'
          +b'\x48\x81\xec\x10\x01\x00\x00'+b'\x49\x89\xcf'+b'\x48\x8d\x59\x40'
          +b'\x49\x89\xd5'+b'\x31\xf6'+b'\x48\x8d\xac\x24\x88\x00\x00\x00'
          +b'\x48\xb8'+struct.pack('<Q',entry)+b'\xff\xe0')
write(adapter,prologue)
for p in pages:
    old=C.c_ulong()
    if not k.VirtualProtect(p,4096,0x20,C.byref(old)):raise OSError('RX')
if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise OSError('Flush')
run=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p)(adapter)
rows=[]
def test(name,occupied,fail,readers,pending=False):
    global slot_base,fail_at
    capacity=len(occupied);slots=C.create_string_buffer(max(24,24*capacity));proc=C.create_string_buffer(96);result=C.create_string_buffer(40)
    slot_base=C.addressof(slots);fail_at=fail;calls.clear();wakes.value=0
    for i,is_used in enumerate(occupied):struct.pack_into('<I',slots,i*24+16,capacity if is_used else 0xffffffff)
    struct.pack_into('<Q',proc,32,slot_base);struct.pack_into('<Q',proc,40,capacity)
    before=readers+(0x1000 if pending else 0)
    struct.pack_into('<I',proc,68,before)
    run(C.addressof(proc),C.addressof(result))
    pre=struct.unpack_from('<I',result,0)[0];index,cap=struct.unpack_from('<QQ',result,8);post,state=struct.unpack_from('<II',result,24)
    expected_calls=[]
    for i,used in enumerate(occupied):
        if used:
            expected_calls.append(i)
            if i==fail:break
    expected_success=fail is None or fail not in expected_calls
    if calls!=expected_calls or errors or cap!=capacity or state!=before-1:raise AssertionError((name,calls,expected_calls,pre,index,cap,state,errors))
    # A failure may have advanced through trailing vacant slots to capacity.
    observed=(pre==1 and index==cap)
    if observed!=expected_success:raise AssertionError((name,observed,expected_success))
    rows.append(dict(case=name,calls=list(calls),pre_release_callback_result=pre,index=index,capacity=cap,
                     post_release_edx=hex(post),lock_before=hex(before),lock_after=hex(state),wakes=wakes.value,
                     iterator_only_claim=index==cap,qualified_full_traversal=observed,expected=expected_success))
test('full-reader-one',[True,True],None,1)
test('full-concurrent-readers',[True,True],None,3)
test('early-callback-false',[True,True,True],0,2)
test('last-occupied-callback-false',[True,True],1,2)
test('false-followed-only-vacant',[True,False,False],0,2)
test('empty-capacity',[],None,1)
test('all-slots-vacant',[False,False,False],None,4)
test('interleaved-vacant-success',[False,True,False,True,False],None,2)
test('wake-clobbers-volatile-edx',[True,True],None,1,True)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(dict(scope='Actual original area traversal/release interval; owned callback schedules, supplied prior reader counts, entry/exit adapters and deliberately EDX-clobbering wake. No multithread schedule, whole updater or retail execution.',
                 method_sha256=sha(Path(__file__).read_bytes()),executable_sha256=sha(data),source_export_sha256=sha(export.read_bytes()),
                 traversal=dict(start=hex(entry),end_exclusive=hex(release),sha256=sha(original(entry,release-entry))),
                 release=dict(original_start=hex(release),end_exclusive=hex(end),sha256=sha(release_original),relocated_start=hex(relocated),rebound_import=hex(old_target)),
                 free=free,rows=rows),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS',len(rows),out)
