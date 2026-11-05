# SPDX-License-Identifier: GPL-3.0-or-later
"""Original manager zero writers and landscape-to-Grid origin controls.

SOR-P-0002 derivative of owned D5AR's pinned PE/unwind loader. Executes only
original C3A0/C290 zero setup, isolated constructor/threshold original write
blocks, landscape shift caller and Grid shift/filter on
owned objects in a disposable child. Population tail is a recording RET; source
retirement records only. No game, saves, DB, installs, Git or network effects.
Nonzero helper rebase is an explicitly supplied adverse primitive input, not
claimed ordinary gameplay. Writes exclusive ignored method/receipts; both-drive
floors and optimization rejection apply before native execution.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import subprocess
from d5ad_baseline import ROOT,guard,sha


def run_owned(destination):
    inherited=Path(__file__).with_name('d5ar_source_lifetime_controls.py')
    prior=ROOT/'.local-work/d5ar/source-lifetime06.json'
    if sha(inherited)!=json.loads(prior.read_bytes())['source_sha256']:
        raise ValueError('Owned authenticated PE loader changed')
    source=inherited.read_text(encoding='utf8')
    anchor="    k=C.WinDLL('kernel32',use_last_error=True)"
    if source.count(anchor)!=1:raise ValueError('Owned loader anchor changed')
    source=source.split(anchor,1)[0]
    tail='''    import faulthandler
    faulthandler.enable()
    k=C.WinDLL('kernel32',use_last_error=True)
    synchronization=C.WinDLL('kernelbase',use_last_error=True)
    k.SetErrorMode(0x0001|0x0002|0x8000)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    blocks=set()
    def reserve(address):
        block=address&~0xffff
        if block not in blocks:
            if k.VirtualAlloc(block,65536,0x3000,4)!=block:raise ValueError('Owned reservation failed')
            blocks.add(block)
    def write(address,content):
        for block in range(address&~0xffff,(address+len(content)+0xffff)&~0xffff,65536):reserve(block)
        C.memmove(address,content,len(content))
    entries=[0x14078c3a0,0x14078c290,0x1407856b0,0x140986da0,0x140988100,
        0x140987080,0x1409870d0,0x140982d00,0x1422cc3d0,0x1402c45a0]
    pins=[]
    for address in entries:
        content=function(address);write(address,content)
        pins.append(dict(static_va=hex(address),bytes=len(content),sha256=hashlib.sha256(content).hexdigest()))
    write(0x144da97a0,original(0x144da97a0,20))
    # Unrelated mutable reset-AABB template is supplied as owned zero bytes;
    # the tested origin triple is loaded from a different file-backed constant.
    write(0x145fc00a0,bytes(24))
    zero=original(0x144da97a8,12)
    if zero!=bytes(12):raise ValueError('Original zero-rebase constant differs')
    constructor_stores=original(0x140787ab4,14)
    threshold_stores=original(0x14078c894,28)
    # Owned ABI wrappers preserve the blocks' nonvolatile destination registers.
    # These execute only the original write blocks, not entire ctor/threshold paths.
    write(0x13f000000,b'\\x41\\x57\\x41\\x56\\x49\\x89\\xcf\\x45\\x31\\xf6'+constructor_stores+b'\\x41\\x5e\\x41\\x5f\\xc3')
    # Threshold block has RIP-relative constants: retain original displacements
    # by placing its bytes at the original static block, with an owned wrapper.
    write(0x14078c894,threshold_stores+b'\\x5f\\xc3')
    write(0x13f000100,b'\\x57\\x48\\x89\\xcf\\x48\\xb8'+struct.pack('<Q',0x14078c894)+b'\\xff\\xe0')
    pins.extend([dict(static_va=hex(address),bytes=len(content),sha256=hashlib.sha256(content).hexdigest(),scope='isolated original write block')
        for address,content in [(0x140787ab4,constructor_stores),(0x14078c894,threshold_stores)]])
    events=[]
    @C.WINFUNCTYPE(None,C.c_void_p)
    def population(pointer):events.append('population-tail-recorded')
    @C.WINFUNCTYPE(None,C.c_void_p)
    def retired(pointer):events.append('retirement-recorded')
    callbacks=[population,retired]
    for address,callback in [(0x140785190,population),(0x140982b70,retired)]:
        write(address,b'\\x48\\xb8'+struct.pack('<Q',C.cast(callback,C.c_void_p).value)+b'\\xff\\xe0')
    for address,target in [(0x143a3f418,k.GetCurrentThreadId),(0x143a402c8,synchronization.WakeByAddressSingle),(0x143a402d8,synchronization.WakeByAddressAll)]:
        reserve(address);C.c_void_p.from_address(address).value=C.cast(target,C.c_void_p).value
    reserve(0x145fd9c30)
    previous=C.c_ulong()
    for block in blocks:
        if block in (0x143a30000,0x143a40000,0x145fd0000):continue
        if not k.VirtualProtect(block,65536,0x20,C.byref(previous)):raise ValueError('Owned executable protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise ValueError('Owned instruction flush failed')
    manager=C.create_string_buffer(0x220);landscape=C.create_string_buffer(0x40)
    grid=C.create_string_buffer(0x70);source=C.create_string_buffer(0x1a0)
    source_array=(C.c_uint64*1)(C.addressof(source));cells=(C.c_uint64*40000)();aux=(C.c_uint64*40000)()
    def put(buffer,at,fmt,value):C.memmove(C.addressof(buffer)+at,struct.pack(fmt,value),struct.calcsize(fmt))
    def origin_words():return [C.c_int32.from_buffer(source,at).value for at in (0x10,0x14,0x20,0x24)]
    C.c_void_p.from_address(0x145fd9c30).value=C.addressof(manager)
    put(landscape,0x10,'<Q',C.addressof(grid))
    put(grid,0,'<Q',0x144b67f48)
    # Grid filter invokes the known predicate through its ordinary vtable slot.
    # A separate owned table supplies that exact original function pointer.
    table=(C.c_uint64*16)();table[8]=0x140987080;put(grid,0,'<Q',C.addressof(table))
    for at,value in [(0x10,1),(0x14,1),(0x48,200),(0x4c,200),(0x50,2),(0x54,2)]:put(grid,at,'<I',value)
    put(grid,0x64,'<i',-100);put(grid,0x68,'<i',-100)
    for at,value in [(0x18,C.addressof(source_array)),(0x20,C.addressof(cells)),(0x28,C.addressof(aux))]:put(grid,at,'<Q',value)
    for at,value in [(0x10,0),(0x14,0),(0x18,10),(0x1c,10),(0x20,2),(0x24,2)]:put(source,at,'<i',value)
    setup=C.WINFUNCTYPE(None,C.c_void_p)(0x14078c3a0)
    finish=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p)(0x14078c290)
    constructor_block=C.WINFUNCTYPE(None,C.c_void_p)(0x13f000000)
    threshold_block=C.WINFUNCTYPE(None,C.c_void_p)(0x13f000100)
    caller=C.WINFUNCTYPE(None,C.c_void_p)(0x1407856b0)
    shift=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_void_p)(0x140986da0)
    rows=[]
    for name,writer in [('constructor-write-block',lambda:constructor_block(C.addressof(manager))),
            ('threshold-write-block',lambda:threshold_block(C.addressof(manager))),
            ('C3A0',lambda:setup(C.addressof(manager))),('C290',lambda:finish(C.addressof(manager),0))]:
        print('SETUP',name,flush=True)
        C.memset(C.addressof(manager)+0x1ec,0x7f,12)
        writer()
        if C.string_at(C.addressof(manager)+0x1ec,12)!=bytes(12):raise ValueError('Original zero writer differs')
        put(manager,0x1a0,'<Q',0)
        before_words=origin_words();print('CALLER',name,flush=True);caller(C.addressof(landscape))
        if origin_words()!=before_words or C.c_uint32.from_buffer(grid,0x10).value!=1:raise ValueError('Zero ordinary caller changed source origin')
        rows.append(dict(case=name+'-zero-setup-original-caller',origin_before=before_words,origin_after=origin_words(),manager_rebase_hex=C.string_at(C.addressof(manager)+0x1ec,12).hex()))
    delta=(C.c_int32*2)(0,0);rebase=(C.c_int32*2)(3,-2)
    before_words=origin_words();print('NONZERO',flush=True);shift(C.addressof(grid),C.addressof(delta),C.addressof(rebase))
    if origin_words()!=[-3,2,2,2]:raise ValueError('Original nonzero rebase counterexample differs')
    rows.append(dict(case='owned-nonzero-primitive-outside-zero-caller',origin_before=before_words,origin_after=origin_words()))
    inverse=(C.c_int32*2)(-3,2);shift(C.addressof(grid),C.addressof(delta),C.addressof(inverse))
    if origin_words()!=before_words:raise ValueError('Original inverse rebase differs')
    rows.append(dict(case='owned-primitive-restoration-not-epoch-proof',origin_before=[-3,2,2,2],origin_after=origin_words()))
    if events.count('population-tail-recorded')!=4 or 'retirement-recorded' in events:raise ValueError('Unexpected owned native branch')
    result=dict(status='PASS',controls=6,rows=rows,functions=pins,exe_sha256=PIN,
        zero_constant_hex=zero.hex(),events=events,floors_before=before,floors_after=disk_floor(),
        substitutions=['Population tail records/returns','Retirement records only','Unrelated mutable reset-AABB template supplied as owned zero24'],
        scope='Two full original setup functions and two wrapped isolated original write blocks, then original caller/Grid operations; population tail substituted; no whole alias theorem')
    with destination.open('x',encoding='utf8',newline='\\n') as stream:stream.write(json.dumps(result,indent=2)+'\\n')
'''
    derived=destination.with_suffix('.method.py')
    with derived.open('x',encoding='utf8',newline='\n') as stream:stream.write(source+tail)
    namespace={'__file__':str(derived),'__name__':'d5ar_owned_origin_fixture'}
    exec(compile(source+tail,str(derived),'exec'),namespace);namespace['owned_host'](destination)
    receipt=dict(status='PASS',controls=6,wrapper_sha256=sha(__file__),inherited_method_sha256=sha(inherited),
        inherited_receipt_sha256=sha(prior),derived_method_sha256=sha(derived),result_sha256=sha(destination),floors=guard())
    with destination.with_suffix('.qualification.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(receipt,indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve()
    if not destination.is_relative_to(ROOT/'.local-work/d5ar') or destination.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):raise ValueError('No reparse output')
    guard()
    if sys.argv[1:2]==['--owned-host']:return run_owned(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],
            capture_output=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='OWNED_HOST_TIMEOUT',seconds=20))+'\n')
        raise RuntimeError('Owned native fixture timeout') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned native fixture failed; receipt retained')
    print(json.dumps(dict(status='PASS',controls=6,path=str(destination))))


if __name__=='__main__':main()
