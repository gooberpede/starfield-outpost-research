# SPDX-License-Identifier: GPL-3.0-or-later
"""Compile and test an offline native-copy lock-edge recorder component.

Reads pinned installed PE, owned PE reader and D5AM component sources. Writes
only a fresh D5AM local component tree. Runs MSVC/MASM and the authored
DLL in this disposable Python host; never loads a retail plugin, opens analysis
projects, operates Starfield, changes saves/configuration, or uses the network.
Private native helper pages substitute only checked IAT calls and two probes.
This component does not qualify full observer coverage or deployment readiness.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
from pathlib import Path
import ctypes as C
import hashlib
import importlib.util
import json
import re
import struct
import subprocess
import threading
import time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PYTHON=Path(sys.executable)
EXE=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
EXE_SHA='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
VC=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat')

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def guard():
    k=C.WinDLL('kernel32',use_last_error=True)
    free={}
    for drive in ('C:/','D:/'):
        value=C.c_uint64()
        if not k.GetDiskFreeSpaceExW(C.c_wchar_p(drive),C.byref(value),None,None):
            raise OSError('Caller-available free-space query failed')
        if value.value<40_000_000_000:
            raise RuntimeError('Caller-available free-space floor failed')
        free[drive]=value.value
    return free

def check(condition,message):
    if not condition:
        raise RuntimeError(message)

def main():
    check(C.sizeof(C.c_void_p)==8,'Windows x64 required')
    label=sys.argv[1]
    check(re.fullmatch('[a-z0-9-]+',label) is not None,'Bounded fresh label required')
    parent=ROOT/'.local-work/d5am'
    parent.mkdir(exist_ok=True)
    out=parent/label
    out.mkdir(exist_ok=False)
    initial_free=guard()
    inputs=[Path(__file__),HERE/'d5am-lock-component.cpp',HERE/'d5am-lock-bridges.asm',
            ROOT/'runtime/construction-winner/d5am_lock_edges.h',
            ROOT/'runtime/retained-population/build.py']
    pins={str(p):sha(p) for p in inputs}
    check(sha(EXE)==EXE_SHA,'Installed PE identity mismatch')
    commands=[f'call "{VC}"',
              f'ml64 /nologo /c /Fobridges.obj "{HERE / "d5am-lock-bridges.asm"}"',
              f'cl /nologo /std:c++20 /EHsc /W4 /O2 /MD "{HERE / "d5am-lock-component.cpp"}" bridges.obj /LD /Fe:SorConstructionWinner-0.8.0-D5AM-lock-component.dll /link /Brepro /INCREMENTAL:NO /EXPORT:D5AM_pending_bridge /EXPORT:D5AM_acquired_bridge']
    cmd=out/'build.cmd'
    cmd.write_text('@echo off\n'+'\nif errorlevel 1 exit /b 1\n'.join(commands)+'\n',encoding='utf8',newline='\r\n')
    result=subprocess.run(['cmd','/d','/c',str(cmd)],cwd=out,capture_output=True)
    (out/'build.log').write_bytes(result.stdout+result.stderr)
    check(result.returncode==0,'Native compilation failed; see retained build.log')
    dll_path=out/'SorConstructionWinner-0.8.0-D5AM-lock-component.dll'
    dll=C.CDLL(str(dll_path))
    dll.D5AM_initialize.argtypes=[C.c_uint64,C.c_uint64]
    dll.D5AM_metric.argtypes=[C.c_uint];dll.D5AM_metric.restype=C.c_uint64
    dll.D5AM_fixture_emit.argtypes=[C.c_uint64,C.c_uint64,C.c_uint]
    dll.D5AM_hold.argtypes=[C.c_uint]
    class Event(C.Structure):
        _fields_=[(name,C.c_uint64) for name in 'sequence kind thread ticks lock generation old_state new_state'.split()]
    dll.D5AM_pop.argtypes=[C.POINTER(Event)]
    def events():
        rows=[];event=Event()
        while dll.D5AM_pop(C.byref(event)):
            rows.append({name:getattr(event,name) for name,_ in Event._fields_})
        return rows
    spec=importlib.util.spec_from_file_location('owned_pe',ROOT/'runtime/retained-population/build.py')
    pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
    image=EXE.read_bytes()
    k=C.WinDLL('kernel32',use_last_error=True)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    bridge={1:C.cast(dll.D5AM_pending_bridge,C.c_void_p).value,
            2:C.cast(dll.D5AM_acquired_bridge,C.c_void_p).value}
    anchor=bridge[1]&~0xffff
    page=None
    for distance in range(0x10000,0x70000000,0x10000):
        for sign in (1,-1):
            page=k.VirtualAlloc(C.c_void_p(anchor+sign*distance),4096,0x3000,4)
            if page:
                break
        if page:
            break
    check(bool(page),'Near private native page allocation failed')
    lock=(C.c_uint32*2)();address=C.addressof(lock)
    waits=[]
    @C.WINFUNCTYPE(C.c_int,C.c_void_p,C.c_void_p,C.c_size_t,C.c_uint32)
    def wait(a,b,size,timeout):
        waits.append([a,size,timeout])
        # This fixture models a foreign final release; it does not measure OS wait.
        lock[0]=0;lock[1]=(lock[1]-0x401000)&0xffffffff
        return 1
    @C.WINFUNCTYPE(None,C.c_void_p)
    def wake(a):
        pass
    imports={0x143a3f418:k.GetCurrentThreadId,0x143a402d0:wait,
             0x143a402c8:wake,0x143a402d8:wake}
    original=[];relocations=[];rows=[];worker=None
    try:
        slot=768
        for va,size,offset in ((0x1422cc3d0,216,0),(0x1402c45a0,81,256)):
            raw=bytearray(pe.pe_read(image,va-0x140000000,size))
            original.append(dict(va=hex(va),size=size,sha256=hashlib.sha256(raw).hexdigest()))
            i=0
            while i<len(raw)-5:
                if raw[i:i+2] in (b'\xff\x15',b'\xff\x25'):
                    target=va+i+6+struct.unpack_from('<i',raw,i+2)[0]
                    check(target in imports,'Unexpected original native import')
                    C.c_uint64.from_address(page+slot).value=C.cast(imports[target],C.c_void_p).value
                    struct.pack_into('<i',raw,i+2,slot-(offset+i+6))
                    relocations.append(dict(site=hex(va+i),iat=hex(target),slot=slot));slot+=8;i+=6
                else:
                    i+=1
            if va==0x1422cc3d0:
                for site,kind,expected in ((0x1422cc410,1,'f0410fc14604'),(0x1422cc48f,2,'41892e0faef0')):
                    pos=site-va
                    check(raw[pos:pos+6]==bytes.fromhex(expected),'Probe preimage mismatch')
                    displacement=bridge[kind]-(page+offset+pos+5)
                    check(-(2**31)<=displacement<2**31,'Probe bridge range')
                    raw[pos:pos+6]=b'\xe8'+struct.pack('<i',displacement)+b'\x90'
            C.memmove(page+offset,bytes(raw),size)
        old=C.c_ulong()
        check(k.VirtualProtect(page,4096,0x20,C.byref(old))!=0,'Private RX failed')
        check(k.FlushInstructionCache(k.GetCurrentProcess(),page,4096)!=0,'Private instruction flush failed')
        acquire=C.WINFUNCTYPE(None,C.c_void_p)(page)
        release=C.WINFUNCTYPE(None,C.c_void_p)(page+256)
        def reset():
            dll.D5AM_initialize(address,1);lock[:]=[0,0]
        def take():
            acquire(address)
        def give():
            release(address)
        reset();take();first=events()
        check([e['kind'] for e in first]==[1,2],'Pending/acquired positive missing')
        check(first[0]['old_state']==0 and first[0]['new_state']==0x1000,'Pending atomic operands')
        check(first[1]['old_state']==0x1000 and lock[1]==0x401000,'Successful CAS operands')
        take();check(events()==[] and lock[1]==0x801000,'Recursive path incorrectly labelled nonowner')
        give();give();check(lock[1]==0,'Original release semantics changed')
        rows.append(dict(case='positive-and-recursion',events=first))
        reset();lock[:]=[0,0x1000];take();later=events();give()
        check(later[0]['old_state']==0x1000 and later[1]['new_state']==0x402000,'Pending-writer overtaking predicate changed')
        rows.append(dict(case='preexisting-pending-writer',events=later,limit='Earlier pending writer is a controlled native state, not measured retail thread history.'))
        reset()
        def delayed():
            dll.D5AM_hold(1);take();give()
        worker=threading.Thread(target=delayed);worker.start()
        deadline=time.monotonic()+10
        while not dll.D5AM_metric(4) and time.monotonic()<deadline:
            time.sleep(0.001)
        check(bool(dll.D5AM_metric(4)),'Private held-pending fixture failed')
        take();give();dll.D5AM_release_hold();worker.join(10)
        check(not worker.is_alive(),'Private contender failed to return')
        competing=events()
        check([e['kind'] for e in competing]==[1,1,2,2],'Competing sequence differs')
        check(competing[0]['thread']==competing[3]['thread'] and competing[1]['thread']==competing[2]['thread'],'Pending/acquired thread joins fail')
        rows.append(dict(case='probe-delay-changes-winner',events=competing,limit='Deliberate offline callback hold proves perturbation possibility; no retail frequency.'))
        reset();lock[:]=[k.GetCurrentThreadId()^0x80000000,0x401000];take();give()
        check(len(waits)==1 and [e['kind'] for e in events()]==[1,2],'Contended original helper path failed')
        rows.append(dict(case='native-wait-after-controlled-release',waits=waits))
        reset();dll.D5AM_fixture_emit(address+8,0,1)
        check(events()==[] and dll.D5AM_metric(3)==1,'Unregistered lock accounting')
        rows.append(dict(case='unregistered-lock-refusal',count=dll.D5AM_metric(3)))
        for _ in range(1025):
            dll.D5AM_fixture_emit(address,0,1)
        saturated=events()
        check(len(saturated)==1024 and dll.D5AM_metric(0)==1 and dll.D5AM_metric(1)==1,'Honest saturation failure missing')
        rows.append(dict(case='saturation',kept=len(saturated),drops=dll.D5AM_metric(0),failed=dll.D5AM_metric(1)))
        dll.D5AM_stop();dll.D5AM_fixture_emit(address,0,1)
        check(events()==[] and dll.D5AM_metric(2)==0,'Inert stopped producer failed')
        rows.append(dict(case='inert-stop',active=dll.D5AM_metric(2)))
        optimization=[]
        for flag in ('-O','-OO'):
            refused=subprocess.run([str(PYTHON),'-E','-B',flag,str(Path(__file__)),label+'-must-not-exist'],capture_output=True)
            check(refused.returncode!=0 and not (parent/(label+'-must-not-exist')).exists(),'Optimization did not refuse before output')
            optimization.append(dict(flag=flag,exit=refused.returncode))
        env=dict(os.environ,PYTHONOPTIMIZE='2')
        refused=subprocess.run([str(PYTHON),'-B',str(Path(__file__)),label+'-env-must-not-exist'],env=env,capture_output=True)
        check(refused.returncode!=0 and not (parent/(label+'-env-must-not-exist')).exists(),'PYTHONOPTIMIZE did not refuse before output')
        optimization.append(dict(flag='PYTHONOPTIMIZE=2',exit=refused.returncode))
        env=dict(os.environ,PYTHONOPTIMIZE='1')
        refused=subprocess.run([str(PYTHON),'-E','-B',str(Path(__file__)),label+'-isolated-env-must-not-exist'],env=env,capture_output=True)
        check(refused.returncode!=0 and not (parent/(label+'-isolated-env-must-not-exist')).exists(),'Inherited PYTHONOPTIMIZE with -E did not refuse before output')
        optimization.append(dict(flag='-E -B with PYTHONOPTIMIZE=1',exit=refused.returncode))
        check(all(sha(p)==digest for p,digest in pins.items()),'Source changed during qualification')
        receipt=dict(schema='sor-d5am-lock-component/1',version='0.8.0-D5AM-lock-component',passed=True,
                     scope='Offline private-copy component only; no SFSE entry, retail installer, complete owner-wide registry, scheduler join or deployment readiness.',
                     inputs=pins,exe_sha256=EXE_SHA,original_code=original,relocations=relocations,
                     dll_sha256=sha(dll_path),cases=rows,optimization_refusals=optimization,
                     initial_free=initial_free,final_free=guard())
        (out/'qualification.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
        print(json.dumps(dict(passed=True,cases=len(rows),path=str(out),dll_sha256=sha(dll_path))))
    finally:
        dll.D5AM_release_hold()
        if worker is not None and worker.is_alive():
            worker.join(10)
            check(not worker.is_alive(),'Private contender still active; preserve its native page')
        check(k.VirtualFree(page,0,0x8000)!=0,'Private page cleanup failed')

if __name__=='__main__':
    main()
