# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute original resolved-reference lease callback/release on owned buffers.
Reads pinned PE; disposable native child only, no game/save/DB/install/network/Git
mutation. Callback/Release bytes stay unchanged; reference count starts at 2 so actual
last-release/free paths are outside fixture scope. Owns a same-address/same-ID
recycle counterexample to prohibit inferred post-release allocation continuity.
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
    callback=0x1402b7070;release=0x140384600
    callback_bytes=original(callback,0x3e);release_bytes=function(release)
    write(callback,callback_bytes);write(release,release_bytes)
    old=C.c_ulong()
    for address in (callback,release):
        if not k.VirtualProtect(address&~0xffff,65536,0x20,C.byref(old)):raise ValueError('Owned executable protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise ValueError('Owned instruction flush failed')
    invoke=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_uint32)(callback)
    release_ref=C.WINFUNCTYPE(C.c_uint64,C.c_void_p)(release)
    source=C.create_string_buffer(0x40);other=C.create_string_buffer(0x40)
    output=C.c_uint64();output_pointer=C.c_uint64(C.addressof(output));functor=(C.c_uint64*2)(0,C.addressof(output_pointer))
    address=C.addressof(source);other_address=C.addressof(other);delta=0x80000200001;rows=[]
    def put(at,offset,value,kind=C.c_uint64):kind.from_address(at+offset).value=value
    def count(at):return C.c_uint64.from_address(at+8).value
    def reset(initial=2,handle=0x12345):
        C.memset(address,0,0x40);C.memset(other_address,0,0x40);output.value=0
        put(address,8,initial);put(address,0x24,handle,C.c_uint32);put(address,0x28,0x12345678,C.c_uint32);put(address,0x2e,0x40,C.c_uint8)
    reset();invoke(C.addressof(functor),address,0x12345)
    if output.value!=address or count(address)!=2+delta:raise ValueError('Original callback did not acquire exact resolved lease')
    identity=(C.c_uint32.from_address(address+0x28).value,C.c_uint8.from_address(address+0x2e).value)
    released=release_ref(address)
    if count(address)!=2 or identity!=(0x12345678,0x40):raise ValueError('Original native release failed to balance acquired lease')
    rows.append(dict(case='actual-acquire-read-release',count_before=2,count_during_lease=2+delta,count_after=count(address),identity=list(identity)))
    for label,initial,requested in [('stale-handle',2,0x12346),('zero-low-refcount',0,0x12345)]:
        reset(initial);invoke(C.addressof(functor),address,requested)
        if output.value or count(address)!=initial:raise ValueError('Original invalid resolution acquired lease')
        rows.append(dict(case=label,output_null=True,count_unchanged=True))
    reset();output.value=address;invoke(C.addressof(functor),address,0x12345)
    if count(address)!=2:raise ValueError('Same-slot callback acquired twice')
    rows.append(dict(case='same-slot-idempotence',count_unchanged=True))
    reset();put(other_address,8,2+delta);output.value=other_address
    invoke(C.addressof(functor),address,0x12345)
    if output.value!=address or count(address)!=2+delta or count(other_address)!=2:raise ValueError('Original replacement did not release previous slot')
    release_ref(address)
    rows.append(dict(case='replacement-balances-old-slot',old_count_after=count(other_address),new_count_after=count(address)))
    reset();invoke(C.addressof(functor),address,0x12345);release_ref(address)
    # Owned storage recycling deliberately demonstrates no later allocation
    # continuity claim can follow merely from an equal pointer/FormID pair.
    C.memset(address,0,0x40);put(address,0x28,identity[0],C.c_uint32);put(address,0x2e,identity[1],C.c_uint8)
    if (C.c_uint32.from_address(address+0x28).value,C.c_uint8.from_address(address+0x2e).value)!=identity:raise ValueError('Owned recycle counterexample failed')
    rows.append(dict(case='post-release-equal-pointer-and-identity-counterexample',later_allocation_continuity_qualified=False))
    result=dict(status='PASS',controls=6,rows=rows,exe_sha256=PIN,original_native=[dict(address=hex(a),size=len(b),sha256=hashlib.sha256(b).hexdigest()) for a,b in [(callback,callback_bytes),(release,release_bytes)]],
        original_bytes_preserved=C.string_at(callback,len(callback_bytes))==callback_bytes and C.string_at(release,len(release_bytes))==release_bytes,
        substitutions=['Owned input reference/output/functor buffers only; no native callback/release instruction substituted','No final-zero/free branch selected; initial owned low-reference-count is2'],
        scope='Original resolved-lease acquisition/release and exact selection-time identity; no full resolver enumeration or later area allocation lease',floors_before=before,floors_after=disk_floor())
    if not result['original_bytes_preserved']:raise ValueError('Original callback/release bytes changed')
    with destination.open('x',encoding='utf8',newline='\\n') as stream:stream.write(json.dumps(result,indent=2)+'\\n')
'''
    derived=destination.with_suffix('.method.py')
    with derived.open('x',encoding='utf8',newline='\n') as stream:stream.write(source+tail)
    namespace={'__file__':str(derived),'__name__':'d5ar_owned_selected_lease'}
    exec(compile(source+tail,str(derived),'exec'),namespace);namespace['owned_host'](destination)
    with destination.with_suffix('.qualification.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='PASS',controls=6,wrapper_sha256=sha(__file__),inherited_method_sha256=sha(inherited),derived_method_sha256=sha(derived),result_sha256=sha(destination)),indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve();guard()
    if not destination.is_relative_to(ROOT/'.local-work/d5ar') or destination.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):raise ValueError('No reparse output')
    if sys.argv[1:2]==['--owned-host']:return owned(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],capture_output=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='OWNED_HOST_TIMEOUT',seconds=20))+'\n')
        raise RuntimeError('Owned selected-lease timeout') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned selected-lease failed; receipt retained')
    print(json.dumps(dict(status='PASS',controls=6,path=str(destination))))


if __name__=='__main__':main()
