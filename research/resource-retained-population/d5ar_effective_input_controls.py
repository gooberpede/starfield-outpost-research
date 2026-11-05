# SPDX-License-Identifier: GPL-3.0-or-later
"""Original ordinary multiplier branch and native float-store counterexample.
Bounded disposable native child, owned buffers only. No game/save/database/
configuration/install/network/Git changes. Full setter callbacks are explicitly
not executed; this proves operand insensitivity, not identical retail histories.
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
    branch_start=0x14079bda8;branch_end=0x14079be13
    branch=original(branch_start,branch_end-branch_start);table=original(0x14079c454,24)
    write(branch_start,branch);write(branch_end,bytes.fromhex('0f28c3c3'));write(0x14079c454,table)
    store=original(0x140684b43,5)
    if store!=bytes.fromhex('c5fa114908'):raise ValueError('Original GMST store changed')
    store_at=0x13f110000;write(store_at,store+bytes.fromhex('c3'))
    set_float=C.WINFUNCTYPE(None,C.c_void_p,C.c_float)(store_at)
    wrapper=0x13f100000
    # Owned Win64 adapter preserves nonvolatileGP/XMM7/XMM8, sets the actual
    # branch's unit/zero lanes, and returns its actual XMM3 scalar as XMM0.
    prefix=bytes.fromhex('5741564883ec38f30f7f7c2420f3440f7f4424104489c749be')+struct.pack('<Q',0x140000000)
    prefix+=bytes.fromhex('0f57ffb80000803f66440f6ec048b8')+struct.pack('<Q',branch_start)+bytes.fromhex('ffd0')
    suffix=bytes.fromhex('f30f6f7c2420f3440f6f4424104883c438415e5fc3')
    write(wrapper,prefix+suffix)
    for at in [0x145e901b8,0x145e901d8,0x145e901f8,0x145e90218,0x145e90238,0x145e90258]:write(at,struct.pack('<f',0.2))
    old=C.c_ulong()
    for at in (branch_start,0x14079c454,wrapper,store_at):
        if not k.VirtualProtect(at&~0xffff,65536,0x20,C.byref(old)):raise ValueError('Owned executable protection failed')
    if not k.FlushInstructionCache(k.GetCurrentProcess(),None,0):raise ValueError('Owned instruction flush failed')
    invoke=C.WINFUNCTYPE(C.c_float,C.c_void_p,C.c_void_p,C.c_uint32)(wrapper)
    form=C.create_string_buffer(0x118);rows=[]
    def bits(value):return struct.pack('<f',value).hex()
    for rarity in (3,1,0):
        C.c_uint8.from_buffer(form,0x110).value=rarity
        for exotic in (0.01,0.05):
            # This executes the exact native write, but not its subsequent
            # virtual notification/registered-callback behavior.
            set_float(0x145e90210,exotic)
            if bits(C.c_float.from_address(0x145e90218).value)!=bits(exotic):raise ValueError('Original float store did not set alternate payload')
            for mask in (0,3):
                result=invoke(None,C.addressof(form),mask)
                expected=1.0 if rarity<=mask else exotic if rarity==3 else 0.2
                if bits(result)!=bits(expected):raise ValueError('Original ordinary mask branch mismatch')
                rows.append(dict(rarity=rarity,mask=mask,exotic_payload_bits=bits(exotic),actual_effective_weight_bits=bits(result)))
    active=[r for r in rows if r['mask']==3]
    exotic_inactive=[r for r in rows if r['rarity']==3 and r['mask']==0]
    if len({r['actual_effective_weight_bits'] for r in active})!=1 or len({r['actual_effective_weight_bits'] for r in exotic_inactive})!=2:raise ValueError('Unread-setting counterexample failed')
    result=dict(status='PASS',controls=12,rows=rows,exe_sha256=PIN,
        native_branch=dict(start=hex(branch_start),end_exclusive=hex(branch_end),sha256=hashlib.sha256(branch).hexdigest()),
        native_float_store=dict(start='0x140684b43',sha256=hashlib.sha256(store).hexdigest()),
        substitutions=['Owned native interior-branch register adapter and return continuation','Original float-store instruction copied into private returning microblock; full setter notifications NOT executed','Owned IRES and unit/zero lanes plus setting storage; no game execution'],
        conclusion='Mask3 ordinary operands are insensitive to unobserved inactive Exotic payload; mask0 counterfactual operands differ. This does not prove two entire retail histories identical.',
        original_branch_bytes_preserved=C.string_at(branch_start,len(branch))==branch,
        floors_before=before,floors_after=disk_floor())
    if not result['original_branch_bytes_preserved']:raise ValueError('Original branch bytes changed')
    with destination.open('x',encoding='utf8',newline='\\n') as stream:stream.write(json.dumps(result,indent=2)+'\\n')
'''
    derived=destination.with_suffix('.method.py')
    with derived.open('x',encoding='utf8',newline='\n') as stream:stream.write(source+tail)
    namespace={'__file__':str(derived),'__name__':'d5ar_owned_effective_input'}
    exec(compile(source+tail,str(derived),'exec'),namespace);namespace['owned_host'](destination)
    with destination.with_suffix('.qualification.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='PASS',controls=12,wrapper_sha256=sha(__file__),inherited_method_sha256=sha(inherited),derived_method_sha256=sha(derived),result_sha256=sha(destination)),indent=2)+'\n')


def main():
    destination=Path(sys.argv[-1]).resolve();guard()
    if not destination.is_relative_to(ROOT/'.local-work/d5ar') or destination.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (destination,*destination.parents)):raise ValueError('No reparse output')
    if sys.argv[1:2]==['--owned-host']:return owned(destination)
    try:
        result=subprocess.run([sys.executable,'-E','-B',str(Path(__file__).resolve()),'--owned-host',str(destination)],capture_output=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(status='OWNED_HOST_TIMEOUT',seconds=20))+'\n')
        raise RuntimeError('Owned effective-input timeout') from failure
    if result.returncode:
        with destination.with_suffix('.failure.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(dict(exit=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace')),indent=2)+'\n')
        raise RuntimeError('Owned effective-input failed; receipt retained')
    print(json.dumps(dict(status='PASS',controls=12,path=str(destination))))


if __name__=='__main__':main()
