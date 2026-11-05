# SPDX-License-Identifier: GPL-3.0-or-later
"""Original singleton publication block with owned adverse interleavings.

Reads the pinned PE via the owned D5AR loader and executes original preferred
VA range 0x141881f3d–0x141881f5c, including the
predicate/CALL/final-store bytes at original addresses in a disposable child.
Constructor is an explicit callback stand-in; source retirement is not executed
here (separate original D5AR controls cover its old/current-map dependency).
Models destructor-only versus whole-initializer phase admission around the actual
original publication block. No game/save/database/install/Git/network effects.
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
    start=0x141881f3d;block=original(start,0x20)
    if block[:3]!=bytes.fromhex('48833d') or block[8:10]!=bytes.fromhex('7516') or block[20]!=0xe8 or block[25:28]!=bytes.fromhex('488905'):
        raise ValueError('Original publication block boundaries differ')
    write(start,block+bytes.fromhex('4883c420c3'))
    write(0x145fd9c30,bytes(8));write(0x146218488,bytes(0x210))
    alternate=C.create_string_buffer(0x210);global_pointer=C.c_uint64.from_address(0x145fd9c30)
    phase={'hazards':0,'epoch':0,'ctor_active':False,'destructor_epoch':1};history=[]
    @C.WINFUNCTYPE(C.c_uint64,C.c_uint64,C.c_uint64)
    def constructor(receiver,argument):
        print('OWNED_CTOR',hex(receiver),flush=True)
        if receiver!=0x146218488:raise RuntimeError('Original constructor receiver differs')
        phase['ctor_active']=True;global_pointer.value=receiver
        history.append(dict(stage='constructor-early-publication',binding=global_pointer.value,phase_hazards=phase['hazards'],ctor_active=True))
        global_pointer.value=C.addressof(alternate)
        history.append(dict(stage='intervening-current-manager',binding=global_pointer.value,phase_hazards=phase['hazards']))
        phase['ctor_active']=False
        history.append(dict(stage='constructor-body-ended-before-native-final-store',binding=global_pointer.value,phase_hazards=phase['hazards'],ctor_active=False))
        return receiver
    write(0x140787830,b'\\x48\\xb8'+struct.pack('<Q',C.cast(constructor,C.c_void_p).value)+b'\\xff\\xe0')
    # Owned wrapper enters the original interior block with its required RSP
    # alignment and a private continuation in place of the enclosing body.
    wrapper=0x13f100000
    prefix=bytes.fromhex('41574531ff4883ec28')
    continuation=wrapper+len(prefix)+10+1+4+10+2
    code=prefix+b'\\x48\\xb8'+struct.pack('<Q',continuation)+bytes.fromhex('504883ec2048b8')+struct.pack('<Q',start)+b'\\xff\\xe0'+bytes.fromhex('4883c428415fc3')
    write(wrapper,code)
    old=C.c_ulong()
    for address in (start,0x140787830,wrapper):
        if not k.VirtualProtect(address&~0xffff,65536,0x20,C.byref(old)):raise ValueError('Owned executable protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise ValueError('Owned instruction flush failed')
    invoke=C.WINFUNCTYPE(None)(wrapper);rows=[]
    for fenced in (False,True):
        history.clear();global_pointer.value=0
        if fenced:phase['hazards']+=1;phase['epoch']+=1
        epoch_before=phase['epoch'];invoke();after=global_pointer.value
        expected=history[0]['binding']
        if expected!=after or phase['destructor_epoch']!=1:raise ValueError('Original final publication failed to restore binding')
        if not history[1]['binding']!=expected:raise ValueError('Adverse binding did not intervene')
        rejected_during=all(item['phase_hazards']>0 for item in history)
        if fenced and not rejected_during:raise ValueError('Whole phase failed before native final store')
        if fenced:phase['hazards']-=1;phase['epoch']+=1
        rows.append(dict(case='whole-phase' if fenced else 'destructor-only',before_after_equal=expected==after,
            destructor_epoch_unchanged=True,phase_rejects_all_constructor_and_pre_final_store_stages=rejected_during,
            phase_epoch_changed_across_final_publication=phase['epoch']!=epoch_before,history=list(history)))
    history.clear();global_pointer.value=0x146218488;invoke()
    if history or global_pointer.value!=0x146218488:raise ValueError('Original initialized predicate did not bypass constructor')
    rows.append(dict(case='already-initialized-native-branch',constructor_calls=0,binding_preserved=True))
    result=dict(status='PASS',controls=3,rows=rows,exe_sha256=PIN,original_static_start=hex(start),
        original_bytes_sha256=hashlib.sha256(block).hexdigest(),original_bytes_preserved=C.string_at(start,len(block))==block,
        substitutions=['Constructor callback schedules owned early/intervening/return values','Interior block terminal continuation is private RET','Phase admission is owned model, not production DLL'],
        scope='Original publication instruction-order counterexample plus owned phase admission; no actual native source retirement in this fixture',floors_before=before,floors_after=disk_floor())
    if not result['original_bytes_preserved']:raise ValueError('Original publication bytes changed')
    with destination.open('x',encoding='utf8',newline='\\n') as stream:stream.write(json.dumps(result,indent=2)+'\\n')
'''
    derived=destination.with_suffix('.method.py')
    with derived.open('x',encoding='utf8',newline='\n') as stream:stream.write(source+tail)
    namespace={'__file__':str(derived),'__name__':'d5ar_owned_publication'}
    exec(compile(source+tail,str(derived),'exec'),namespace);namespace['owned_host'](destination)
    with destination.with_suffix('.qualification.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='PASS',controls=3,wrapper_sha256=sha(__file__),inherited_method_sha256=sha(inherited),derived_method_sha256=sha(derived),result_sha256=sha(destination)),indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve();guard()
    if not destination.is_relative_to(ROOT/'.local-work/d5ar') or destination.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):raise ValueError('No reparse output')
    if sys.argv[1:2]==['--owned-host']:return owned(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],capture_output=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='OWNED_HOST_TIMEOUT',seconds=20))+'\n')
        raise RuntimeError('Owned publication timeout') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned publication failed; receipt retained')
    print(json.dumps(dict(status='PASS',controls=3,path=str(destination))))


if __name__=='__main__':main()
