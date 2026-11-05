# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute original source retirement against owned current/old map contexts.

Reads pinned installed PE; maps original retirement, lookup and lock instructions
only inside a disposable child. Source-definition release is RET and source free
records only. Actual Windows wait/wake functions serve the native lock. Writes
exclusive ignored receipts/logs; no game, saves, database, installs or Git writes.
The twenty-second child failure bound is a fixture fault guard, not a healthy
retail capture limit. This proves a scoped native dependency, not a source lease.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import threading
from d5ar_native_inventory import ROOT, EXE, PIN, disk_floor


def owned_host(destination):
    before=disk_floor()
    data=EXE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=PIN:
        raise ValueError('Installed executable changed')
    pe=struct.unpack_from('<I',data,0x3c)[0]
    optional=struct.unpack_from('<H',data,pe+20)[0]
    sections=[struct.unpack_from('<IIII',data,pe+24+optional+40*n+8)
              for n in range(struct.unpack_from('<H',data,pe+6)[0])]
    base=0x140000000
    def original(address,size):
        rva=address-base
        for _,start,length,raw in sections:
            if start<=rva and rva+size<=start+length:
                return data[raw+rva-start:raw+rva-start+size]
        raise ValueError('File-backed bytes absent')
    exception_rva,exception_size=struct.unpack_from('<II',data,pe+24+112+3*8)
    directory=original(base+exception_rva,exception_size)
    runtime_functions=list(struct.iter_unpack('<III',directory))
    def root_entry(record,seen=()):
        a,z,unwind=record
        if unwind in seen:
            raise ValueError('Cyclic unwind chain')
        header=original(base+unwind,4)
        if header[0]>>3&4:
            chain=(unwind+4+2*header[2]+3)&~3
            return root_entry(struct.unpack('<III',original(base+chain,12)),(*seen,unwind))
        return a
    def function(address):
        matches=[(a,z) for a,z,u in runtime_functions if root_entry((a,z,u))==address-base]
        # The existing authenticated D5AF leaf-helper record spans 81 bytes;
        # as a leaf it has no runtime-function entry in this PE.
        if not matches and address==0x1402c45a0:
            return original(address,81)
        if not matches or min(a for a,_ in matches)!=address-base:
            raise ValueError('Unique function start required')
        return original(address,max(z for _,z in matches)-(address-base))
    k=C.WinDLL('kernel32',use_last_error=True)
    synchronization=C.WinDLL('kernelbase',use_last_error=True)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong]
    k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    synchronization.WaitOnAddress.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32]
    synchronization.WaitOnAddress.restype=C.c_int
    synchronization.WakeByAddressAll.argtypes=[C.c_void_p]
    blocks=[0x140980000,0x140970000,0x1407a0000,0x1402b0000,0x140340000,
            0x1402c0000,0x1422c0000,0x1428c0000,0x143650000,
            0x143a30000,0x143a40000,0x145fd0000]
    for block in blocks:
        if k.VirtualAlloc(block,0x10000,0x3000,4)!=block:
            raise OSError(C.get_last_error(),'Owned original-address reservation failed')
    entries=[0x140982b70,0x1403499f0,0x1422cc3d0,0x1402c45a0,
             0x140975030,0x1407ab6a0,0x1407aab10,0x1407ac260]
    pins=[]
    for address in entries:
        content=function(address)
        C.memmove(address,content,len(content))
        pins.append(dict(static_va=hex(address),bytes=len(content),sha256=hashlib.sha256(content).hexdigest()))
    lookup_bytes=function(0x1403499f0)
    sites=[n for n in range(len(lookup_bytes)-6) if lookup_bytes[n:n+3]==b'\x48\x8d\x35']
    if len(sites)!=1:
        raise ValueError('Unique native lookup hash-table operand required')
    at=sites[0]
    hash_table=0x1403499f0+at+7+struct.unpack_from('<i',lookup_bytes,at+3)[0]
    hash_block=hash_table&~0xffff
    if hash_block in blocks or k.VirtualAlloc(hash_block,0x10000,0x3000,4)!=hash_block:
        raise ValueError('Owned hash-table reservation failed')
    blocks.append(hash_block)
    constants=original(hash_block,0x10000)
    C.memmove(hash_block,constants,len(constants))
    C.memmove(0x1428caea0,b'\xc3',1)
    frees=[]
    @C.WINFUNCTYPE(None,C.c_void_p,C.c_size_t)
    def source_free(pointer,size):
        frees.append(dict(pointer=int(pointer or 0),size=int(size)))
    jump=b'\x48\xb8'+struct.pack('<Q',C.cast(source_free,C.c_void_p).value)+b'\xff\xe0'
    C.memmove(0x14365cdb0,jump,len(jump))
    C.memmove(0x1402ba340,jump,len(jump))
    @C.WINFUNCTYPE(None,C.c_void_p)
    def heap_free(pointer):
        frees.append(dict(pointer=int(pointer or 0),size=None))
    heap_jump=b'\x48\xb8'+struct.pack('<Q',C.cast(heap_free,C.c_void_p).value)+b'\xff\xe0'
    C.memmove(0x1402b7910,heap_jump,len(heap_jump))
    wait_entered=threading.Event()
    @C.WINFUNCTYPE(C.c_int,C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32)
    def wait(address,comparison,size,timeout):
        wait_entered.set()
        return synchronization.WaitOnAddress(address,comparison,size,timeout)
    imports={0x143a3f418:k.GetCurrentThreadId,0x143a402d0:wait,
             0x143a402c8:synchronization.WakeByAddressSingle,0x143a402d8:synchronization.WakeByAddressAll}
    for address,target in imports.items():
        C.c_void_p.from_address(address).value=C.cast(target,C.c_void_p).value
    previous=C.c_ulong()
    for block in blocks:
        if block in (0x143a30000,0x143a40000,0x145fd0000):
            continue
        if not k.VirtualProtect(block,0x10000,0x20,C.byref(previous)) or not k.FlushInstructionCache(k.GetCurrentProcess(),block,0x10000):
            raise OSError(C.get_last_error(),'Owned native protection/flush failed')
    retirement=C.WINFUNCTYPE(C.c_void_p,C.c_void_p)(0x140982b70)
    keep=[]
    def buffer(size):
        value=C.create_string_buffer(size);keep.append(value);return value
    def address(value):
        return C.addressof(value)
    def u32(value,offset):
        return C.c_uint32.from_buffer(value,offset)
    def u64(value,offset):
        return C.c_uint64.from_buffer(value,offset)
    manager=buffer(0x200)
    C.c_void_p.from_address(0x145fd9c30).value=address(manager)
    current=buffer(0x160);old=buffer(0x160);source=buffer(0x1a0)
    u64(manager,0x130).value=address(current)
    u32(current,0x44).value=1
    errors=[]
    def run_retirement():
        try:
            retirement(address(source))
        except BaseException as error:
            errors.append(repr(error))
    thread=threading.Thread(target=run_retirement)
    thread.start()
    if not wait_entered.wait(5):
        raise ValueError('Original retirement did not wait behind current reader')
    if frees or not thread.is_alive():
        raise ValueError('Source released before current reader ended')
    # The only release belongs to this owned fixture, not the game.
    u32(current,0x44).value-=1
    synchronization.WakeByAddressAll(address(current)+0x44)
    thread.join(5)
    if thread.is_alive() or errors or frees!=[dict(pointer=address(source),size=0x1a0)] or u32(current,0x44).value!=0:
        raise ValueError('Current-reader retirement continuation differs: '+repr(dict(errors=errors,frees=frees,
            alive=thread.is_alive(),word=u32(current,0x44).value)))
    rows=[dict(case='current-map-reader-blocks-source-retirement',passed=True,wait_observed=True,
               free_before_release=False,free_after_release=True,actual_free=frees[0])]
    frees.clear();wait_entered.clear()
    old_source=buffer(0x1a0);u32(old,0x44).value=1
    retirement(address(old_source))
    if frees!=[dict(pointer=address(old_source),size=0x1a0)] or u32(old,0x44).value!=1 or wait_entered.is_set():
        raise ValueError('Old-map reader counterexample differs')
    rows.append(dict(case='old-map-reader-does-not-block-current-map-retirement',passed=True,
                     old_reader_word=1,actual_free=frees[0],consequence='Current owner binding is indispensable for a source lease'))
    def population(holder_owners,collection_owners):
        proc=buffer(0x160);slot=buffer(24);holder=buffer(64);resource=buffer(24)
        collection=buffer(24);region=buffer(48);points=buffer(16);source=buffer(0x1a0)
        u64(proc,0x20).value=address(slot);u64(proc,0x28).value=1
        u64(slot,0).value=address(source);u64(slot,8).value=address(holder);u32(slot,16).value=1
        u32(holder,0).value=holder_owners;u64(holder,0x20).value=address(resource);u64(holder,0x28).value=1
        u32(resource,0).value=7;u64(resource,8).value=address(collection);u32(resource,16).value=1
        u32(collection,0).value=collection_owners;u32(collection,8).value=1;u32(collection,12).value=1;u64(collection,16).value=address(region)
        u32(region,16).value=7;u32(region,24).value=1;u32(region,28).value=1;u64(region,32).value=address(points)
        return proc,slot,holder,resource,collection,region,points,source
    current,slot,holder,resource,collection,region,points,source=population(2,2)
    u64(manager,0x130).value=address(current);u32(current,0x44).value=1
    frees.clear();wait_entered.clear();errors.clear();thread=threading.Thread(target=run_retirement);thread.start()
    if not wait_entered.wait(5) or frees:
        raise ValueError('Populated map retirement failed to wait')
    u32(current,0x44).value-=1;synchronization.WakeByAddressAll(address(current)+0x44);thread.join(5)
    if thread.is_alive() or errors or u64(slot,8).value or u32(slot,16).value!=0xffffffff or u32(holder,0).value!=1 or frees!=[dict(pointer=address(source),size=0x1a0)]:
        raise ValueError('Populated map erase/retained-holder result differs: '+repr(dict(errors=errors,frees=frees,holder=u32(holder,0).value)))
    rows.append(dict(case='populated-current-map-retirement-erases-after-reader-release',passed=True,
                     occupied_slot_erased=True,holder_references_after=1,collection_references_after=u32(collection,0).value))
    for owners in (2,1):
        current,slot,holder,resource,collection,region,points,source=population(1,owners)
        u64(manager,0x130).value=address(current);frees.clear();wait_entered.clear()
        retirement(address(source))
        if u64(slot,8).value or u32(slot,16).value!=0xffffffff or u32(holder,0).value!=0xffffffff:
            raise ValueError('Final holder retirement did not clear map')
        if owners==2:
            expected=[dict(pointer=address(resource),size=None),dict(pointer=address(holder),size=64),dict(pointer=address(source),size=416)]
            if frees!=expected or u32(collection,0).value!=1 or u32(collection,8).value!=1 or u64(region,32).value!=address(points):
                raise ValueError('Externally retained collection lifetime differs: '+repr(frees))
        else:
            expected=[dict(pointer=address(points),size=16),dict(pointer=address(region),size=48),
                      dict(pointer=address(collection),size=24),dict(pointer=address(resource),size=None),
                      dict(pointer=address(holder),size=64),dict(pointer=address(source),size=416)]
            if frees!=expected or u32(collection,0).value!=0xffffffff or u32(collection,8).value or u64(collection,16).value or u64(region,32).value:
                raise ValueError('Final nested storage ending differs: '+repr(frees))
        rows.append(dict(case='source-retirement-nested-collection-'+('retained' if owners==2 else 'final-release'),
                         passed=True,collection_references_before=owners,
                         collection_references_after=u32(collection,0).value,original_release_sequence=frees.copy()))
    result=dict(status='PASS',rows=rows,functions=pins,exe_sha256=PIN,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                floors_before=before,floors_after=disk_floor(),
                hash_table=dict(static_va=hex(hash_table),block_sha256=hashlib.sha256(constants).hexdigest()),
                substitutions=['Source definition/path-reference release replaced with RET',
                               'Heap/sized releases record pointer/size; Python backing retained'],
                scope='Original retirement and native exclusive/unlock/lookup with actual OS wait; no retail or completed current-owner certificate')
    with destination.open('x',encoding='utf8',newline='\n') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve()
    if not destination.is_relative_to(ROOT / '.local-work/d5ar') or destination.exists():
        raise ValueError('Fresh ignored D5AR receipt required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):
        raise ValueError('No reparse outputs')
    disk_floor()
    if sys.argv[1:2]==['--owned-host']:
        return owned_host(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],
                              capture_output=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:
            stream.write(json.dumps(dict(status='OWNED_FIXTURE_TIMEOUT',
                stdout=(failure.stdout or b'').decode(errors='replace'),
                stderr=(failure.stderr or b'').decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned retirement host exceeded fixture failure bound; receipt retained') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:
            stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),
                stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned retirement host failed; retained failure receipt')
    if not destination.is_file():
        raise RuntimeError('Missing owned retirement receipt')
    print(json.dumps(dict(status='PASS',controls=5,path=str(destination))))


if __name__=='__main__':
    main()
