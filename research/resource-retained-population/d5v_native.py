# SPDX-License-Identifier: GPL-3.0-or-later
"""Run pinned area-predicate controls in a disposable offline Python process.

Reads the D5V identity receipt, original PE pages and local function metadata,
plus delivered C1 geometry. Writes a new ignored JSON receipt. Only selected
native functions run. Fixture callbacks resolve one IRES and supply temporary
quad storage; the original predicate and preallocated-set insertion run intact.
No game launch, attachment, save, database, network or installed writes. Stdlib.
"""
from pathlib import Path
import ctypes as C
import faulthandler
import hashlib
import json
import re
import shutil
import struct
import sys

faulthandler.enable()
ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT/'.local-work/d5v'
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from resource_spatial import evaluate_region, f32


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    destination = LOCAL/sys.argv[1]
    assert destination.parent == LOCAL and not destination.exists()
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(free.values()) >= 40_000_000_000
    initial = json.loads((LOCAL/'initial.json').read_text(encoding='utf8'))
    exe = next(p for p in initial['installed'] if p.endswith('Starfield.exe'))
    assert sha(exe) == initial['installed'][exe]
    data = Path(exe).read_bytes()
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    base = struct.unpack_from('<Q', data, pe+48)[0]
    assert base == 0x140000000
    opts = struct.unpack_from('<H', data, pe+20)[0]
    sections = [struct.unpack_from('<IIII', data, pe+24+opts+i*40+8)
                for i in range(struct.unpack_from('<H', data, pe+6)[0])]
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.SetErrorMode(0x0001 | 0x0002 | 0x8000)
    kernel.VirtualAlloc.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.c_ulong]
    kernel.VirtualAlloc.restype = C.c_void_p
    kernel.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.POINTER(C.c_ulong)]
    kernel.GetCurrentProcess.restype = C.c_void_p
    kernel.FlushInstructionCache.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t]
    pages, code = set(), set()

    def page(va):
        start = va & ~4095
        if start not in pages:
            gran = start & ~65535
            if not any(q & ~65535 == gran for q in pages):
                assert kernel.VirtualAlloc(gran, 65536, 0x2000, 4) == gran
            assert kernel.VirtualAlloc(start, 4096, 0x1000, 4) == start
            for vs, rva, size, raw in sections:
                lo, hi = max(start, base+rva), min(start+4096, base+rva+size)
                if lo < hi:
                    C.memmove(lo, data[raw+lo-base-rva:raw+hi-base-rva], hi-lo)
            pages.add(start)
        return start

    def write(va, payload):
        for start in range(va & ~4095, (va+len(payload)+4095) & ~4095, 4096):
            page(start)
        C.memmove(va, payload, len(payload))

    functions = {}
    for entry in ('1421e0f50', '1404a7f90', '140f4ac50', '141116580',
                  '142346b30', '1434ca936', '14374dd70', '143751450'):
        meta = LOCAL/'functions'/f'{entry}.txt'
        source = meta.read_text(encoding='utf8')
        spans = re.findall(r'\[([0-9a-f]+), ([0-9a-f]+)\]', source.splitlines()[0])
        assert spans
        for low, high in spans:
            for start in range(int(low,16) & ~4095, (int(high,16)+4096) & ~4095, 4096):
                page(start)
                code.add(start)
        for address in re.findall(r'\[0x([0-9a-f]+)\]', source.split('DECOMPILE')[0]):
            page(int(address,16))
        functions[entry] = sha(meta)

    ires = C.create_string_buffer(0x120)
    C.c_uint32.from_buffer(ires, 0x28).value = 0x57cf
    C.c_uint8.from_buffer(ires, 0x2e).value = 0x9f
    quads = []
    errors = []

    @C.WINFUNCTYPE(C.c_void_p, C.c_uint32)
    def resolve(identity):
        if identity != 0x57cf:
            errors.append(['unexpected IRES', identity])
        return C.addressof(ires)

    @C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_uint32)
    def quad_allocate(context, count):
        if count != 4:
            errors.append(['unexpected quad count', count])
        quad = C.create_string_buffer(64)
        quads.append(quad)
        return C.addressof(quad)

    @C.WINFUNCTYPE(None, C.c_void_p, C.c_void_p)
    def quad_free(context, pointer):
        pass

    callbacks = [resolve, quad_allocate, quad_free]
    for va, callback in zip((0x1405de3b0, 0x140f4af20, 0x1402b7230), callbacks):
        write(va, b'\x48\xb8'+struct.pack('<Q', C.cast(callback,C.c_void_p).value)+b'\xff\xe0')
        code.add(va & ~4095)
    crt = C.CDLL('C:/Windows/System32/ucrtbase.dll')
    crt.atan2f.argtypes = [C.c_float, C.c_float]
    crt.atan2f.restype = C.c_float
    write(0x143a40600,struct.pack('<Q',C.cast(crt.atan2f,C.c_void_p).value))
    for start in code:
        old = C.c_ulong()
        assert kernel.VirtualProtect(start, 4096, 0x20, C.byref(old))
    assert kernel.FlushInstructionCache(kernel.GetCurrentProcess(), None, 0)
    callback = C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_void_p,C.c_void_p)(0x1421e0f50)
    point_callback = C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_void_p)(0x142346b30)
    rows = []
    point_rows = []
    point_controls = []
    inputs = {str((ROOT/'save-analysis/scripts/resource_spatial.py').relative_to(ROOT)):
              sha(ROOT/'save-analysis/scripts/resource_spatial.py')}

    def test(label, query, radius, upper, bound, points, translation=None):
        quads.clear()
        query_data = C.create_string_buffer(24)
        C.memmove(query_data, struct.pack('<3fI', *query, 0), 16)
        translated = query
        if translation is None:
            write(0x1461fae80, struct.pack('<I', 0))
        else:
            translation_data = (C.c_float*3)(*translation)
            write(0x1461fae80, struct.pack('<I', 1))
            write(0x1461fae88, struct.pack('<Q', C.addressof(translation_data)))
            translated = [f32(query[k]+translation[k]) for k in range(3)]
        region = C.create_string_buffer(48)
        point_data = (C.c_float*(4*len(points)))(*(v for p in points for v in p))
        C.memmove(region, struct.pack('<4f', *bound), 16)
        C.c_uint32.from_buffer(region, 24).value = len(points)
        C.c_void_p.from_buffer(region, 32).value = C.addressof(point_data)
        collection = C.create_string_buffer(24)
        C.c_uint32.from_buffer(collection, 8).value = 1
        C.c_void_p.from_buffer(collection, 16).value = C.addressof(region)
        slot = C.create_string_buffer(24)
        C.c_uint32.from_buffer(slot).value = 0x57cf
        C.c_void_p.from_buffer(slot, 8).value = C.addressof(collection)
        C.c_uint32.from_buffer(slot, 16).value = 1
        wrapper = C.create_string_buffer(64)
        C.c_void_p.from_buffer(wrapper,32).value = C.addressof(slot)
        C.c_uint64.from_buffer(wrapper,40).value = 1
        wrapper_value = C.c_void_p(C.addressof(wrapper))
        output = C.create_string_buffer(32)
        output_slot = C.create_string_buffer(16)
        C.c_uint32.from_buffer(output_slot,8).value = 0xffffffff
        C.c_void_p.from_buffer(output,8).value = C.addressof(output_slot)
        C.c_uint64.from_buffer(output,16).value = 1
        C.c_uint64.from_buffer(output,24).value = 1
        closure = C.create_string_buffer(24)
        C.c_void_p.from_buffer(closure).value = C.addressof(query_data)
        C.c_void_p.from_buffer(closure,8).value = C.addressof(output)
        C.c_float.from_buffer(closure,16).value = radius
        C.c_float.from_buffer(closure,20).value = upper
        returned = callback(C.addressof(closure),0,C.addressof(wrapper_value))
        native = C.c_uint64.from_buffer(output_slot).value == C.addressof(ires)
        expected = evaluate_region(translated,radius,upper,bound[:3],bound[3],points)
        assert not errors, errors
        assert expected['status'] == 'KNOWN', (label, expected)
        assert native == expected['accepted'], (label,native,expected)
        rows.append(dict(label=label,query=query,radius=radius,upper=upper,
                         translation=translation,native_accepted=native,
                         translated_query=translated,bound=bound,points=points,
                         expected=expected,callback_return=returned,
                         geometry_sha256=hashlib.sha256(struct.pack('<4f',*bound)+bytes(point_data)).hexdigest()))
        raw_query = (C.c_float*3)(*translated)
        point_result = bool(point_callback(C.addressof(region),C.addressof(raw_query)) & 0xff)
        point_rows.append(dict(label=label,query=translated,native_point=point_result,
                               native_area=native,geometry_sha256=rows[-1]['geometry_sha256']))
        if points and points[0][3]>0:
            first=(C.c_float*3)(*points[0][:3])
            endpoint_result=bool(point_callback(C.addressof(region),C.addressof(first)) & 0xff)
            assert endpoint_result,(label,'positive-width first-point control')
            first[2]=f32(first[2]+1000)
            z_result=bool(point_callback(C.addressof(region),C.addressof(first)) & 0xff)
            assert z_result
            point_controls.append(dict(label=label,first_point=points[0],positive_endpoint=endpoint_result,
                                       same_xy_changed_z=z_result))

    for case in ('D2-83388f','D2-84e101'):
        source = ROOT/'docs/experiments/resource-retained-population/d5u/outposts'/f'{case}.json'
        inputs[str(source.relative_to(ROOT))] = sha(source)
        model = json.loads(source.read_text(encoding='utf8'))
        ref = model['reference']
        for layer in model['layers']:
            for n, region in enumerate(layer['regions']):
                test(f'{case}/{layer["id"]}/{n}',ref['center'],150,ref['upper'],
                     region['native_bound'],region['points'])
    for label, query, radius, upper, bound, points, translation in [
        ('one-point-height-independent',[0,0,1000],0,-1000,[0,0,0,2],[[0,0,0,2]],None),
        ('same-geometry-near',[0,0,0],0,100,[0,0,0,2],[[0,0,0,2]],None),
        ('same-geometry-far',[3,0,0],0,100,[0,0,0,2],[[0,0,0,2]],None),
        ('area-versus-point',[3,0,0],150,100,[0,0,0,2],[[0,0,0,2]],None),
        ('inclusive-tangency',[2,0,0],0,100,[0,0,0,2],[[0,0,0,2]],None),
        ('empty-points',[0,0,0],150,100,[0,0,0,2],[],None),
        ('indexed-translation',[10,20,0],0,100,[0,0,0,2],[[0,0,0,2]],[-10,-20,0]),
        ('strip-interior-height-independent',[0,0,1000],0,-1000,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-far',[0,30,0],0,100,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-narrowphase-reject',[0,8,0],0,100,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-edge-3d-accept',[0,2.5,0],1,-10,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-edge-3d-reject',[0,2.5,3],1,-10,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-vertex-height-accept',[10,2.5,-100],1,0,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('strip-vertex-height-reject',[10,2.5,-100],1,-1,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],None),
        ('translated-strip',[100,200,0],0,100,[0,0,0,20],[[-10,0,0,2],[10,0,0,2]],[-100,-200,0]),
    ]:
        test(label,query,radius,upper,bound,points,translation)
    by_label = {v['label']:v for v in point_rows}
    assert by_label['same-geometry-near']['native_point']
    assert not by_label['same-geometry-far']['native_point']
    assert by_label['same-geometry-far']['native_area'] is False
    assert by_label['area-versus-point']['native_area'] and not by_label['area-versus-point']['native_point']
    assert by_label['one-point-height-independent']['native_point']
    result = dict(schema='sor-d5v-native/1',scope='Original area callback and point predicate with fixture ownership/resolution',
                  game_process=False,functions=functions,executable_sha256=initial['installed'][exe],
                  free=free,inputs=inputs,rows=rows,point_rows=point_rows,point_controls=point_controls,
                  crt_sha256=sha('C:/Windows/System32/ucrtbase.dll'),
                  passed=len(rows),code_sha256=sha(__file__))
    destination.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=len(rows),output=str(destination)),indent=2))


if __name__ == '__main__':
    main()
