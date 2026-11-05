# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute unchanged native outer/resource rehash and exclusive admission.
Owned buffers and explicit heap stand-ins only in disposable child. Reads pinned
PE, writes exclusive local receipts. No game/save/DB/install/network/Git mutation.
Source storage reuse counterexample is separately labeled owned model.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import subprocess
from d5ad_baseline import ROOT,guard,sha


def owned(destination):
    inherited=Path(__file__).with_name('d5ar_source_lifetime_controls.py')
    previous=ROOT/'.local-work/d5ar/source-lifetime06.json'
    if sha(inherited)!=json.loads(previous.read_bytes())['source_sha256']:raise ValueError('Owned PE loader changed')
    source=inherited.read_text(encoding='utf8').split("    k=C.WinDLL('kernel32',use_last_error=True)",1)[0]
    tail='''    import faulthandler
    faulthandler.enable()
    k=C.WinDLL('kernel32',use_last_error=True);k.SetErrorMode(0x0001|0x0002|0x8000)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.GetCurrentProcess.restype=C.c_void_p;k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    @C.WINFUNCTYPE(C.c_long,C.c_void_p)
    def fault_info(pointer):
        record,context=(C.c_void_p*2).from_address(pointer)
        print('OWNED_FAULT_RIP',hex(C.c_uint64.from_address(context+0xf8).value),flush=True)
        return 0
    k.AddVectoredExceptionHandler.argtypes=[C.c_ulong,C.c_void_p];k.AddVectoredExceptionHandler.restype=C.c_void_p
    fault_registration=k.AddVectoredExceptionHandler(1,C.cast(fault_info,C.c_void_p))
    if not fault_registration:raise ValueError('Owned fault diagnostic registration failed')
    blocks=set()
    def write(address,content):
        for block in range(address&~0xffff,(address+len(content)+0xffff)&~0xffff,65536):
            if block not in blocks:
                if k.VirtualAlloc(block,65536,0x3000,4)!=block:raise ValueError('Owned reservation failed')
                blocks.add(block)
        C.memmove(address,content,len(content))
    before_floor=before
    synchronization=C.WinDLL('kernelbase',use_last_error=True)
    synchronization.WaitOnAddress.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32];synchronization.WaitOnAddress.restype=C.c_int
    synchronization.WakeByAddressAll.argtypes=[C.c_void_p]
    keep=[];allocations=[];frees=[];wait_entered=threading.Event()
    def buffer(size):
        result=C.create_string_buffer(size);keep.append(result);return C.addressof(result)
    def q(at,off=0):return C.c_uint64.from_address(at+off)
    def d(at,off=0):return C.c_uint32.from_address(at+off)
    @C.WINFUNCTYPE(C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32,C.c_uint8)
    def allocate(heap,size,alignment,flag):
        at=buffer(size);allocations.append(dict(address=at,size=size,alignment=alignment,flag=flag));return at
    @C.WINFUNCTYPE(None,C.c_void_p)
    def free(pointer):frees.append(int(pointer or 0))
    @C.WINFUNCTYPE(C.c_int,C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32)
    def wait(address,comparison,size,timeout):
        wait_entered.set();return synchronization.WaitOnAddress(address,comparison,size,timeout)
    entries=[0x1407abaf0,0x1407abc90,0x1407ab510,0x1407ab730,0x1422cc3d0,0x1402c45a0,0x140975030,0x1407aa5f0]
    pins=[]
    for at in entries:
        content=function(at);write(at,content);pins.append(dict(address=hex(at),bytes=len(content),sha256=hashlib.sha256(content).hexdigest()))
    # Pointer-key hash is an actual leaf in this original executable. Preserve
    # its entire file-backed code block rather than inventing function extent.
    hash_block=original(0x140340000,65536);write(0x140340000,hash_block)
    constants=original(0x144d50000,65536);write(0x144d50000,constants)
    write(0x145e60398,struct.pack('<I',2));write(0x145e603c0,bytes(64))
    for at,target in [(0x1422c7ad0,allocate),(0x1402b7910,free)]:write(at,bytes.fromhex('48b8')+struct.pack('<Q',C.cast(target,C.c_void_p).value)+bytes.fromhex('ffe0'))
    imports={0x143a3f418:k.GetCurrentThreadId,0x143a402d0:wait,0x143a402c8:synchronization.WakeByAddressSingle,0x143a402d8:synchronization.WakeByAddressAll}
    for at,target in imports.items():write(at,struct.pack('<Q',C.cast(target,C.c_void_p).value))
    publication=original(0x14079fe14,9)
    if publication!=bytes.fromhex('488904ca48895cca08'):raise ValueError('Original native slot publication stores changed')
    publication_entry=0x13f100000
    publication_shim=bytes.fromhex('534c89cb4c89c04989cb488d0c524c89da')+publication+bytes.fromhex('5bc3')
    write(publication_entry,publication_shim)
    old=C.c_ulong()
    for at in entries+[0x140340000,0x1422c7ad0,0x1402b7910,publication_entry]:
        if not k.VirtualProtect(at&~0xffff,65536,0x20,C.byref(old)):raise ValueError('Owned executable protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise ValueError('Owned instruction flush failed')
    outer=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_uint64)(0x1407abaf0)
    resource=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_uint64)(0x1407abc90)
    hash_key=C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_void_p)(0x14034a220)
    exclusive=C.WINFUNCTYPE(None,C.c_void_p)(0x1422cc3d0);unlock=C.WINFUNCTYPE(None,C.c_void_p)(0x1402c45a0)
    table=list(struct.unpack('<256I',original(0x144d58d70,1024)))
    def hash_resource(key):
        value=0
        for byte in struct.pack('<I',key):value=table[(value^byte)&255]^(value>>8)
        return value
    def hash_pointer(key):
        value=C.c_uint64(key);return hash_key(None,C.byref(value))
    def colliding(hashfn,values):
        found={}
        for value in values:
            home=hashfn(value)&7
            if home in found:return found[home],value,home
            found[home]=value
        raise ValueError('Owned finite collision fixture unavailable')
    sources=[buffer(0x70) for _ in range(32)]
    first,second,outer_home=colliding(hash_pointer,sources)
    resource_first,resource_second,resource_home=colliding(hash_resource,range(1,33))
    def map_fixture(keys,home,values):
        at=buffer(0x40);slots=buffer(4*24)
        for i in range(4):q(slots+i*24,16).value=0xffffffffffffffff
        first=home&3;second=(first+1)&3
        for index,key,value in [(first,keys[0],values[0]),(second,keys[1],values[1])]:
            q(slots+index*24).value=key;q(slots+index*24,8).value=value;d(slots+index*24,20).value=first
        d(slots+first*24,16).value=second;d(slots+second*24,16).value=4
        q(at,16).value=slots;q(at,24).value=4;q(at,32).value=2;q(at,40).value=second
        return at,slots
    def entries_of(at,resource_keys=False):
        data=q(at,16).value;count=q(at,24).value;result={};locations={}
        for i in range(count):
            slot=data+i*24
            if d(slot,16).value!=0xffffffff:
                key=d(slot).value if resource_keys else q(slot).value
                if key in result:raise ValueError('Duplicate native rehash key')
                result[key]=q(slot,8).value;locations[key]=slot
        if len(result)!=count-q(at,32).value:raise ValueError('Native occupancy accounting differs')
        return result,locations
    rows=[];holders=[buffer(64),buffer(64)];collections=[buffer(24),buffer(24)];payloads=[]
    for holder,collection in zip(holders,collections):
        slots=buffer(24);region=buffer(48);points=buffer(16)
        q(holder,32).value=slots;q(holder,40).value=1
        d(slots).value=7;q(slots,8).value=collection;d(slots,16).value=1
        d(collection,8).value=1;d(collection,12).value=1;q(collection,16).value=region
        d(region,16).value=7;d(region,24).value=1;d(region,28).value=1;q(region,32).value=points
        C.memmove(points,struct.pack('<4f',1,2,0,4),16)
        payloads.extend([(holder,64),(collection,24),(slots,24),(region,48),(points,16)])
    for at in holders+collections:d(at).value=3
    payload_before=[C.string_at(at,size) for at,size in payloads]
    for label,fn,keys,home,values,is_resource in [('outer',outer,[first,second],outer_home,holders,False),('resource',resource,[resource_first,resource_second],resource_home,collections,True)]:
        at,oldslots=map_fixture(keys,home,values);before,locations=entries_of(at,is_resource);old_values=[C.string_at(v,24) for v in values]
        fn(at,None,8);after,newlocations=entries_of(at,is_resource)
        if before!=after or q(at,24).value!=8 or q(at,16).value==oldslots or not all(newlocations[k]!=locations[k] for k in keys):raise ValueError('Original rehash did not preserve moved key/pointer entries')
        if [C.string_at(v,24) for v in values]!=old_values or any(q(oldslots+i*24,8).value for i in range(4)):raise ValueError('Native rehash changed pointee/retained old ownership')
        if oldslots not in frees:raise ValueError('Original rehash omitted old slot release')
        if not all(d(newlocations[key],20).value==home for key in keys) or sum(newlocations[key]==q(at,16).value+home*24 for key in keys)!=1:raise ValueError('Actual native collision path was not exercised')
        if [C.string_at(pointer,size) for pointer,size in payloads]!=payload_before:raise ValueError('Original rehash altered nested retained geometry')
        rows.append(dict(case=label+'-actual-growth-collision-rehash',old_capacity=4,new_capacity=8,logical_entries_preserved=True,physical_slots_relocated=True,pointee_bytes_unchanged=True,old_slot_release_observed=True,actual_native_collision=True,nested_geometry_bytes_unchanged=True,keys=keys))
    # Exact original writer admission plus rehash; Python only provides the
    # enclosing call sequence and owns the pre-existing read count.
    at,oldslots=map_fixture([first,second],outer_home,[holders[0],holders[1]])
    lock=buffer(8);d(lock,4).value=1;wait_entered.clear();writer_done=threading.Event();errors=[]
    def writer():
        try:
            exclusive(lock)
            try:outer(at,None,8)
            finally:unlock(lock)
        except BaseException as error:errors.append(repr(error))
        finally:writer_done.set()
    before=C.string_at(at,0x40);thread=threading.Thread(target=writer);thread.start()
    if not wait_entered.wait(5) or writer_done.is_set() or C.string_at(at,0x40)!=before:raise ValueError('Foreign rehash mutated map behind held reader')
    d(lock,4).value-=1;synchronization.WakeByAddressAll(lock+4);thread.join(5)
    if thread.is_alive() or errors or q(at,24).value!=8 or d(lock).value or d(lock,4).value:raise ValueError('Original writer did not complete/release after reader exit')
    if entries_of(at)[0]!={first:holders[0],second:holders[1]}:raise ValueError('Foreign rehash lost logical entries')
    rows.append(dict(case='held-reader-blocks-original-exclusive-foreign-rehash',wait_observed=True,map_unchanged_before_reader_release=True,writer_completes_after_release=True))
    # Execute the original erase/reserve/native publication stores around same
    # source-key reuse. The source-byte overwrite remains explicitly owned.
    old_holder=entries_of(at)[0][first];old_count=d(old_holder).value
    old_index=(entries_of(at)[1][first]-q(at,16).value)//24
    erase=C.WINFUNCTYPE(None,C.c_void_p,C.c_uint64)(0x140975030)
    reserve=C.WINFUNCTYPE(C.c_uint8,C.c_void_p,C.c_void_p,C.c_void_p)(0x1407aa5f0)
    publish=C.WINFUNCTYPE(None,C.c_void_p,C.c_uint64,C.c_uint64,C.c_void_p)(publication_entry)
    exclusive(lock)
    try:
        erase(at,old_index)
        if first in entries_of(at)[0] or d(old_holder).value!=old_count-1:raise ValueError('Native erase failed before reused-key publication')
        C.memset(first,0x5a,0x70);newholder=buffer(64);d(newholder).value=2
        index=C.c_uint64(q(at,24).value);key=C.c_uint64(first)
        inserted=reserve(at,C.byref(index),C.byref(key))
        if not inserted or index.value>=q(at,24).value:raise ValueError('Native reservation did not create new reused-key slot')
        publish(q(at,16).value,index.value,first,newholder)
    finally:unlock(lock)
    if entries_of(at)[0].get(first)!=newholder or newholder==old_holder or d(old_holder).value!=old_count-1:raise ValueError('Native reused-key publication lost distinct holder lifetime')
    rows.append(dict(case='actual-native-erase-reserve-publication-same-source-key',key_unchanged=True,old_holder_retained=True,new_holder_distinct=True,original_publication_stores_sha256=hashlib.sha256(publication).hexdigest(),source_byte_reinitialization='Owned overwrite; native allocation/free not claimed'))
    # Rehash preserves pointer identity; it cannot establish allocation birth.
    # Reuse is an explicit owned counterexample, not disguised native rehash.
    birth_before=C.string_at(first,0x70);C.memset(first,0xa5,0x70)
    if entries_of(at)[0][first]!=newholder or C.string_at(first,0x70)==birth_before:raise ValueError('Source ABA counterexample failed')
    rows.append(dict(case='owned-source-address-reuse-remains-distinct-from-rehash',same_key_and_holder=True,allocation_birth_qualified=False,substitution='Owned source storage overwritten after reader ended; no original allocation/free claimed'))
    unchanged=all(C.string_at(int(pin['address'],16),pin['bytes'])==function(int(pin['address'],16)) for pin in pins)
    result=dict(status='PASS',controls=5,rows=rows,exe_sha256=PIN,functions=pins,original_bytes_preserved=unchanged,
        hash_block_sha256=hashlib.sha256(hash_block).hexdigest(),hash_constants_sha256=hashlib.sha256(constants).hexdigest(),allocations=allocations,frees=frees,
        substitutions=['Heap allocator returns owned retained buffers; heap free logs and retains backing','Heap initialized flag set2 in owned memory','Enclosing writer calls original exclusive/rehash/unlock; held reader represented by owned native reader count1'],
        scope='Actual original outer/resource growth and collision relocation, actual native exclusive wait ordering; source ABA overwrite separately owned model, not allocation certificate',floors_before=before_floor,floors_after=disk_floor())
    if not unchanged:raise ValueError('Original native bytes changed')
    with destination.open('x',encoding='utf8',newline='\\n') as stream:stream.write(json.dumps(result,indent=2)+'\\n')
'''
    derived=destination.with_suffix('.method.py')
    with derived.open('x',encoding='utf8',newline='\n') as stream:stream.write(source+tail)
    namespace={'__file__':str(derived),'__name__':'d5ar_owned_rehash'}
    exec(compile(source+tail,str(derived),'exec'),namespace);namespace['owned_host'](destination)
    with destination.with_suffix('.qualification.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='PASS',controls=5,wrapper_sha256=sha(__file__),inherited_method_sha256=sha(inherited),derived_method_sha256=sha(derived),result_sha256=sha(destination)),indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve();guard()
    if not destination.is_relative_to(ROOT/'.local-work/d5ar') or destination.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):raise ValueError('No reparse output')
    if sys.argv[1:2]==['--owned-host']:return owned(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],capture_output=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='OWNED_HOST_TIMEOUT',seconds=20,stdout=(failure.stdout or b'').decode(errors='replace'),stderr=(failure.stderr or b'').decode(errors='replace')))+'\n')
        raise RuntimeError('Owned rehash timeout') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned rehash failed; receipt retained')
    print(json.dumps(dict(status='PASS',controls=5,path=str(destination))))


if __name__=='__main__':main()
