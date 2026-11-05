# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute original reflected array clear/reserve on owned buffers only.

SOR-P-0002 adaptation of the authenticated owned PE loader. Reads pinned PE and
existing method receipt; writes fresh ignored method/results. No game, save, DB,
install, configuration, network or Git mutation. The twenty-second child bound
is an owned fixture failure guard, not a healthy retail capture limit.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B')
import json
from pathlib import Path
import subprocess
from d5ad_baseline import ROOT, guard, sha


def host(destination):
    inherited = Path(__file__).with_name('d5ar_source_lifetime_controls.py')
    prior = ROOT / '.local-work/d5ar/source-lifetime06.json'
    if sha(inherited) != json.loads(prior.read_bytes())['source_sha256']:
        raise ValueError('Authenticated owned PE loader changed')
    prefix = inherited.read_text(encoding='utf8').split("    k=C.WinDLL('kernel32',use_last_error=True)", 1)[0]
    tail = '''    import faulthandler
    faulthandler.enable()
    k=C.WinDLL('kernel32',use_last_error=True)
    k.SetErrorMode(0x0001|0x0002|0x8000)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong]
    k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    blocks=[]
    for address in (0x1408e0000,0x1422c0000,0x1402c0000,0x1402b0000):
        if k.VirtualAlloc(address,65536,0x3000,4)!=address:
            raise OSError(C.get_last_error(),'Owned reservation failed')
        blocks.append(address)
    pins=[]
    for address in (0x1408e2df0,0x1422cc2c0,0x1402c5be0):
        content=function(address)
        if address//65536!=(address+len(content)-1)//65536:
            raise ValueError('Owned code exceeds explicit mapped block')
        C.memmove(address,content,len(content))
        pins.append(dict(static_va=hex(address),bytes=len(content),sha256=hashlib.sha256(content).hexdigest()))
    table=original(0x144af7088,24)
    if struct.unpack('<QQQ',table)!=(0x1402c5b80,0x1402c5bd0,0x1402c5be0):
        raise ValueError('Original allocator vtable changed')
    if k.VirtualAlloc(0x144af0000,65536,0x3000,4)!=0x144af0000:
        raise OSError(C.get_last_error(),'Owned vtable reservation failed')
    C.memmove(0x144af7088,table,len(table))
    old=C.c_ulong()
    if not k.VirtualProtect(0x144af0000,65536,2,C.byref(old)):
        raise OSError(C.get_last_error(),'Owned vtable read protection failed')
    frees=[]
    @C.WINFUNCTYPE(None,C.c_void_p,C.c_uint32)
    def free(pointer,size):
        frees.append((int(pointer or 0),size))
    stub=bytes.fromhex('48b8')+struct.pack('<Q',C.cast(free,C.c_void_p).value)+bytes.fromhex('ffe0')
    C.memmove(0x1402ba340,stub,len(stub))
    for address in blocks:
        old=C.c_ulong()
        if not k.VirtualProtect(address,65536,0x20,C.byref(old)):
            raise OSError(C.get_last_error(),'Owned RX protection failed')
        if not k.FlushInstructionCache(k.GetCurrentProcess(),address,65536):
            raise OSError(C.get_last_error(),'Owned instruction flush failed')
    invoke=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_uint32)(0x1408e2df0)
    rows=[]
    for count,capacity,nonnull in ((3,4,True),(0,4,True),(0,0,False)):
        points=C.create_string_buffer(bytes(range(32)))
        array=C.create_string_buffer(16)
        C.c_uint32.from_buffer(array,0).value=count
        C.c_uint32.from_buffer(array,4).value=capacity
        pointer=C.addressof(points) if nonnull else 0
        C.c_uint64.from_buffer(array,8).value=pointer
        pair=(C.c_uint64*2)(0x145975240,C.addressof(array))
        points_before=bytes(points)
        frees.clear()
        invoke(0,C.addressof(pair),0)
        after=(C.c_uint32.from_buffer(array,0).value,C.c_uint32.from_buffer(array,4).value,C.c_uint64.from_buffer(array,8).value)
        if after!=(0,0,0) or frees!=([(pointer,capacity*8)] if capacity else []) or bytes(points)!=points_before:
            raise ValueError('Original zero-count array transition differs')
        rows.append(dict(before_count=count,before_capacity=capacity,before_data_nonnull=nonnull,
                         after_count=after[0],after_capacity=after[1],after_data_null=not after[2],
                         release_sizes=[size for pointer,size in frees],owned_backing_unchanged=True,passed=True))
    result=dict(status='PASS_ORIGINAL_ZERO_LIST_ARRAY_CONTRACT',rows=rows,functions=pins,
                exe_sha256=PIN,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                floors_before=before,floors_after=disk_floor(),
                substitutions=['Only heap free 0x1402ba340 records pointer/size; owned Python backing remains live'],
                allocator_vtable_sha256=hashlib.sha256(table).hexdigest(),
                scope='Original reflected array callback, reserve and array release execute with requested count zero; owned TypeInfo pair/buffers. No wire field binding, parent application, live component or historical input certificate.')
    with destination.open('x',encoding='utf8',newline='\\n') as stream:
        stream.write(json.dumps(result,indent=2)+'\\n')
'''
    derived = prefix + tail
    method = destination.with_suffix('.method.py')
    if method.exists():
        raise ValueError('Fresh owned method required')
    with method.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(derived)
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'owned_zero_list_method'}
    exec(compile(derived, str(method), 'exec'), namespace)
    namespace['owned_host'](destination)


def main():
    destination = Path(sys.argv[-1]).resolve()
    if not destination.is_relative_to(ROOT / '.local-work/d5ar') or destination.exists():
        raise ValueError('Fresh ignored receipt required')
    if any(p.is_symlink() or p.is_junction() for p in (destination, *destination.parents)):
        raise ValueError('No reparse outputs')
    guard()
    if sys.argv[1:2] == ['--owned-host']:
        return host(destination)
    try:
        result = subprocess.run([sys.executable, '-E', '-B', str(Path(__file__).resolve()), '--owned-host', str(destination)],
                                capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired as failure:
        value = dict(status='OWNED_FIXTURE_TIMEOUT', stdout=(failure.stdout or b'').decode(errors='replace'),
                     stderr=(failure.stderr or b'').decode(errors='replace'))
    else:
        value = dict(exit=result.returncode, stdout=result.stdout.decode(errors='replace'), stderr=result.stderr.decode(errors='replace'))
        if not result.returncode and destination.is_file():
            print(json.dumps(dict(status='PASS_ORIGINAL_ZERO_LIST_ARRAY_CONTRACT', controls=3)))
            return
    with destination.with_suffix('.failure.json').open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')
    raise RuntimeError('Owned original array host failed; receipt retained')


if __name__ == '__main__':
    main()
