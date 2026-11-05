# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute original clip arithmetic and cell-loop bounds on owned operands.

SOR-P-0002 adaptation of the owned D5AR pinned-PE loader. A disposable child
executes only the original clip block and cell iterator; the actual per-cell
generator is replaced by a coordinate logger. Inputs are declared synthetic
dimensions, stitch and origin, not historical runtime observations. Writes fresh
ignored source/logs/receipts; no game, save, DB, install, network or Git mutation.
Stop on source/input drift, native failure or either caller-available drive floor.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import subprocess

from d5ad_baseline import ROOT, guard, sha


def main():
    guard()
    out = Path(sys.argv[1]).absolute()
    if not out.resolve().is_relative_to(ROOT / '.local-work/d5ar') or out.exists():
        raise ValueError('Fresh ignored output directory required')
    if any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('No reparse output')
    inherited = Path(__file__).with_name('d5ar_source_lifetime_controls.py')
    prior = ROOT / '.local-work/d5ar/source-lifetime06.json'
    if sha(inherited) != json.loads(prior.read_bytes())['source_sha256']:
        raise ValueError('Authenticated owned loader changed')
    pins = {str(p): sha(p) for p in (Path(__file__).resolve(), inherited.resolve(), prior,
            inherited.with_name('d5ar_native_inventory.py').resolve(),
            inherited.with_name('d5ad_baseline.py').resolve())}
    source = inherited.read_text(encoding='utf8')
    anchor = "    k=C.WinDLL('kernel32',use_last_error=True)"
    if source.count(anchor) != 1:
        raise ValueError('Owned loader anchor changed')
    tail = r'''
    import faulthandler
    faulthandler.enable()
    k=C.WinDLL('kernel32',use_last_error=True)
    k.SetErrorMode(0x0001|0x0002|0x8000)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
    k.GetCurrentProcess.restype=C.c_void_p
    k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
    blocks=set()
    def write(at,value):
        for page in range(at&~0xffff,(at+len(value)+0xffff)&~0xffff,65536):
            if page not in blocks:
                if k.VirtualAlloc(page,65536,0x3000,4)!=page:raise ValueError('Owned address unavailable')
                blocks.add(page)
        C.memmove(at,value,len(value))
    def jump(at):return b'\xff\x25\0\0\0\0'+struct.pack('<Q',at)
    block=original(0x14079b79a,0x14079b8af-0x14079b79a)
    loop=function(0x14079c470)
    scale=original(0x144f04cb8,4)
    if scale!=struct.pack('<f',100.):raise ValueError('Native scale changed')
    write(0x144f04cb8,scale);write(0x145ea6770,struct.pack('<i',2))
    write(0x14079b79a,block+jump(0x13f000200))
    write(0x14079c470,loop)
    # Original stack offsets are retained. Only XMM6/XMM7 are nonvolatile
    # outputs of this isolated block; the owned wrapper preserves both.
    setup=(b'\x48\x81\xec\x58\x03\0\0'
        b'\xf3\x0f\x7f\xb4\x24\x10\x03\0\0\xf3\x0f\x7f\xbc\x24\x20\x03\0\0'
        b'\x48\x89\x8c\x24\xe0\x02\0\0\x48\x89\x94\x24\xe8\x02\0\0'
        b'\x4c\x89\x84\x24\x40\x03\0\0\x48\xc7\x84\x24\x08\x03\0\0\0\0\0\0'
        b'\x0f\x57\xff')+jump(0x14079b79a)
    tailcode=b'\x48\x8b\x84\x24\x40\x03\0\0'
    for n,offset in enumerate((0x1b0,0x1b4,0x1b8,0x1c0,0x1c4,0x1c8,0xb0,0xb4,0x190)):
        tailcode+=b'\x8b\x94\x24'+struct.pack('<I',offset)+b'\x89\x90'+struct.pack('<I',n*4)
    tailcode+=(b'\xf3\x0f\x6f\xb4\x24\x10\x03\0\0\xf3\x0f\x6f\xbc\x24\x20\x03\0\0'
               b'\x48\x81\xc4\x58\x03\0\0\xc3')
    write(0x13f000000,setup);write(0x13f000200,tailcode)
    coordinates=[]
    @C.WINFUNCTYPE(None,C.c_uint64,C.c_void_p,C.c_void_p,C.c_void_p)
    def record(unused,position,origin,clip):coordinates.append(struct.unpack('<2i',C.string_at(position,8)))
    write(0x14079a330,jump(C.cast(record,C.c_void_p).value))
    # Data pages remain writable; only privately reserved instruction pages
    # become executable. No original module/process is mapped or modified.
    for page in (0x13f000000,0x140790000):
        old=C.c_ulong()
        if not k.VirtualProtect(page,65536,0x20,C.byref(old)):raise OSError('Owned code protection')
        if not k.FlushInstructionCache(k.GetCurrentProcess(),page,65536):raise OSError('Owned instruction flush')
    execute=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_void_p)(0x13f000000)
    iterate=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_void_p,C.c_float)(0x14079c470)
    rows=[]
    for label,dims,stitch,anchor in (
        ('conditional A0/C1',(10,10),2,(-200,-200)),
        ('distinct asymmetric context',(8,14),3,(-123,234)),
        ('minimum healthy dimensions',(1,1),2,(0,0))):
        source=C.create_string_buffer(0x70);struct.pack_into('<2i',source,0x18,*dims)
        origin=C.create_string_buffer(struct.pack('<2i',*anchor));result=C.create_string_buffer(36)
        C.memmove(0x145ea6770,struct.pack('<i',stitch),4)
        execute(C.addressof(source),C.addressof(origin),C.addressof(result))
        center=struct.unpack_from('<3f',result);half=struct.unpack_from('<3f',result,12)
        bounds=struct.unpack_from('<2i',result,24);padding=struct.unpack_from('<i',result,32)[0]
        expected_center=(float(anchor[0]+(dims[0]//2)*100),float(anchor[1]+(dims[1]//2)*100),0.)
        expected_half=(float((dims[0]//2+stitch)*100),float((dims[1]//2+stitch)*100),0.)
        if center!=expected_center or half!=expected_half or bounds!=tuple(v+2*stitch for v in dims) or padding!=stitch//2:
            raise ValueError('Original clip differs from independent integer oracle')
        context=C.create_string_buffer(40);native_dims=C.create_string_buffer(struct.pack('<2i',*bounds))
        struct.pack_into('<i',context,0x10,padding);struct.pack_into('<Q',context,0x20,C.addressof(native_dims))
        coordinates.clear();iterate(C.addressof(context),None,None,1.)
        expected=[(x,y) for x in range(padding,bounds[0]-padding) for y in range(padding,bounds[1]-padding)]
        if coordinates!=expected:raise ValueError('Original cell loop differs from full ordered oracle')
        rows.append(dict(label=label,dimensions=dims,stitch=stitch,origin=anchor,clip_center=center,clip_half=half,
            cell_bounds=[padding,bounds[0]-padding,padding,bounds[1]-padding],cells=len(coordinates),
            ordered_cell_bytes_sha256=hashlib.sha256(b''.join(struct.pack('<2i',*v) for v in coordinates)).hexdigest()))
    result=dict(status='PASS',synthetic_operands=True,historical_runtime_observation=False,checks=rows,
        native_blocks=[dict(start=hex(a),bytes=len(v),sha256=hashlib.sha256(v).hexdigest())
            for a,v in ((0x14079b79a,block),(0x14079c470,loop),(0x144f04cb8,scale))],
        substitution='Actual per-cell generator replaced by owned coordinate logger',floors=disk_floor())
    with destination.open('xb') as stream:stream.write(json.dumps(result,sort_keys=True,separators=(',',':')).encode()+b'\n')

if __name__=='__main__':owned_host(Path(sys.argv[1]))
'''
    out.mkdir()
    method = out / 'owned.py'
    # The raw tail spells generated byte literals explicitly; one level belongs
    # to the emitted Python source, not to interpreted native instruction data.
    prefix = source.split(anchor, 1)[0]
    import_anchor = 'from d5ar_native_inventory import '
    if prefix.count(import_anchor) != 1:
        raise ValueError('Owned loader import anchor changed')
    prefix = prefix.replace(import_anchor, 'sys.path.insert(0, ' + repr(str(inherited.parent.resolve())) + ')\n' + import_anchor)
    generated = prefix + tail.replace('\\\\', '\\')
    with method.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(generated)
    result = subprocess.run([sys.executable, '-E', '-B', str(method), str(out / 'native.json')],
                            capture_output=True, timeout=30)
    (out / 'stdout.log').write_bytes(result.stdout)
    (out / 'stderr.log').write_bytes(result.stderr)
    if result.returncode:
        raise ValueError('Owned native clip control failed; preserve logs')
    value = json.loads((out / 'native.json').read_bytes())
    if any(sha(p) != digest for p, digest in pins.items()):
        raise ValueError('Executed source changed')
    value.update(source_sha256=pins, generated_method_sha256=sha(method), floors_after=guard())
    with (out / 'qualification.json').open('xb') as stream:
        stream.write(json.dumps(value, sort_keys=True, separators=(',', ':')).encode() + b'\n')
    print(json.dumps(dict(status='PASS', cases=len(value['checks']), receipt=str(out / 'qualification.json'))))


if __name__ == '__main__':
    main()
