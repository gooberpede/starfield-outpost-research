# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute the bounded D5T ordinary population in a disposable Python process.

Reads authenticated D5S fixture support, D5T read-only function exports and the
pinned installed executable. Writes a new ignored JSON receipt. Original native
cell, RNG, walk, competition, bounds and deep copy execute in this process only.
Fixture callbacks supply packed keys, preallocated resource collections and
successful allocation. Temporary frees are suppressed inside this process.
No game, attachment, installed write, save, network or database mutation occurs.
Prerequisite: .local-work/d5t prepared and D5S_OUTPUT points to that directory.
Stop on identity, disk-floor, native-process or callback failure; retain failures.
"""
from pathlib import Path
import faulthandler
import os
import sys
import csv
import hashlib

faulthandler.enable()
ROOT = Path(__file__).resolve().parents[2]
local = Path(os.environ['D5S_OUTPUT'])
assert local.resolve().is_relative_to((ROOT / '.local-work').resolve())
sources = {r['path'].replace('\\', '/'): r['sha256'] for r in csv.DictReader(
    (ROOT / 'docs/experiments/resource-retained-population/d5s-sources.csv').open(encoding='utf8'))}
for name in ('start.py', 'native_probe.py', 'geometry.json'):
    expected = sources[f'.local-work/d5s/{name}']
    assert hashlib.sha256((local / name).read_bytes()).hexdigest() == expected, name
destination_path = local / sys.argv[1]
assert destination_path.parent == local and destination_path.suffix == '.json' and not destination_path.exists()
sys.path.insert(0, str(local))
probe = (local / 'native_probe.py').read_text().split('receipt=json.loads')[0]
probe = probe.replace("'1407aedd0']", "'1407aedd0','14079a330','1404a7f90',"
                      "'142bf4850','1407af1a0','14079b020','1434ca936',"
                      "'14374dd70','143751450']")
exec(compile(probe, 'owned-D5S-native-setup', 'exec'))

@C.WINFUNCTYPE(C.c_long, C.c_void_p)
def fault_info(ep):
    record, ctx = (C.c_void_p * 2).from_address(ep)
    print('FAULT', hex(C.c_uint32.from_address(record).value),
          'RIP', hex(C.c_uint64.from_address(ctx + 0xf8).value), flush=True)
    return 0

k.AddVectoredExceptionHandler.argtypes = [C.c_ulong, C.c_void_p]
k.AddVectoredExceptionHandler.restype = C.c_void_p
k.AddVectoredExceptionHandler(1, C.cast(fault_info, C.c_void_p))
crt.atan2f.argtypes = [C.c_float, C.c_float]
crt.atan2f.restype = C.c_float
write(0x143a40600, struct.pack('<Q', C.cast(crt.atan2f, C.c_void_p).value))
page(0x144d59000)
receipt = json.loads((OUT / 'geometry.json').read_text())
req = receipt['results'][1]['request']
manager = C.create_string_buffer(0x100)
C.c_uint32.from_buffer(manager, 0x80).value = req['owner_key']
write(0x145fd9c30, struct.pack('<Q', C.addressof(manager)))
write(0x145e60398, struct.pack('<I', 2))
write(0x145e603c0, b'\0')
write(0x145921e84, struct.pack('<I', 0xffffffff))
resources = req['ordered_resources']
ids = [int(r['resource'], 16) for r in resources]
collections = [C.create_string_buffer(24) for _ in ids]
slots = C.create_string_buffer(24 * len(ids))
output = C.create_string_buffer(48)
C.c_void_p.from_buffer(output, 24).value = C.addressof(slots)
C.c_uint64.from_buffer(output, 32).value = len(ids)
for i, (identity, collection) in enumerate(zip(ids, collections)):
    C.c_uint32.from_buffer(collection).value = 1
    C.c_uint32.from_buffer(slots, i * 24).value = identity
    C.c_void_p.from_buffer(slots, i * 24 + 8).value = C.addressof(collection)
    C.c_uint32.from_buffer(slots, i * 24 + 16).value = len(ids)
current = [1, 1]
key_calls = []
errors = []

@C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)
def convert(manager_pointer, out, xy):
    got = list((C.c_int32 * 2).from_address(xy))
    if got != [req['origin'][i] + current[i] for i in range(2)]:
        errors.append(['key operands', got, current[:]])
    packed = req['packed_keys'][f'{current[0]},{current[1]}']
    C.c_uint64.from_address(out).value = packed
    key_calls.append(current[:])
    return out

@C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p)
def get_collection(owner, key, out):
    identity = C.c_uint32.from_address(key).value
    if owner != C.addressof(output) or identity not in ids:
        errors.append(['collection', identity])
        return 0
    collection = collections[ids.index(identity)]
    C.c_uint32.from_buffer(collection).value += 1
    C.c_void_p.from_address(out).value = C.addressof(collection)
    return 1

@C.WINFUNCTYPE(None, C.c_void_p)
def no_free(pointer):
    pass

callbacks_extra = [convert, get_collection, no_free]

def stub(va, callback):
    p = page(va)
    old = C.c_ulong()
    assert k.VirtualProtect(p, 4096, 4, C.byref(old))
    write(va, b'\x48\xb8' + struct.pack('<Q', C.cast(callback, C.c_void_p).value) + b'\xff\xe0')
    assert k.VirtualProtect(p, 4096, 0x20, C.byref(old))

stub(0x14078d7b0, convert)
stub(0x1407a97c0, get_collection)
write(0x143a40470, struct.pack('<Q', C.cast(no_free, C.c_void_p).value))
origin = (C.c_int32 * 2)(*req['origin'])
clip = (C.c_float * 8)(*req['clip_center'], 0, *req['clip_half'], 0)
cell = (C.c_int32 * 4)()
native_cell = C.WINFUNCTYPE(C.c_uint64, *([C.c_void_p] * 5), C.c_float, C.c_void_p)(0x14079a330)
ires = C.create_string_buffer(0x118)
dnam = C.create_string_buffer(0x238)
runs = []
for label, mask, weights in [('O0', 0, [r['weight'] for r in receipt['results'][0]['request']['ordered_resources']]),
                              ('O3', 3, [1., 1., 1.]), ('O3-repeat', 3, [1., 1., 1.])]:
    free()
    for collection in collections:
        C.memset(C.addressof(collection) + 8, 0, 16)
    calls = []
    for resource, weight, collection in zip(resources, weights, collections):
        identity = int(resource['resource'], 16)
        C.c_uint32.from_buffer(ires, 0x28).value = identity
        rarity = {0x57d4: 3, 0x57d0: 1, 0x57cf: 0}[identity]
        C.c_uint8.from_buffer(ires, 0x110).value = rarity
        C.memmove(C.addressof(dnam) + 40 * (rarity + 7), struct.pack('<10f', *resource['block']), 40)
        for x in range(1, 13):
            for y in range(1, 13):
                current[:] = [x, y]
                cell[0], cell[1] = x, y
                before = C.c_uint32.from_buffer(collection, 8).value
                print('CELL', label, resource['resource'], x, y, flush=True)
                returned = native_cell(C.addressof(ires), C.addressof(cell), C.addressof(origin),
                                       C.addressof(clip), C.addressof(dnam), weight, C.addressof(output))
                assert not errors, errors
                after = C.c_uint32.from_buffer(collection, 8).value
                calls.append(dict(resource=resource['resource'], cell=current[:], appended=after-before,
                                  returned_low_byte=returned & 255))
    regions = []
    for identity, collection in zip(ids, collections):
        count = C.c_uint32.from_buffer(collection, 8).value
        data_pointer = C.c_void_p.from_buffer(collection, 16).value
        for i in range(count):
            at = data_pointer + i * 48
            num = C.c_uint32.from_address(at + 24).value
            ptr = C.c_void_p.from_address(at + 32).value
            assert num and ptr
            regions.append(dict(resource=f'{identity:08x}', header=C.string_at(at, 24).hex(),
                                count=num, points=C.string_at(ptr, num * 16).hex()))
    runs.append(dict(outcome=label, mask=mask, weights=weights, calls=calls, regions=regions))
assert runs[1]['regions'] == runs[2]['regions']
sys.path.insert(0, str(ROOT / 'research/resource-geometry'))
import geometry
import math
comparisons = []
consumer = C.WINFUNCTYPE(C.c_uint8, C.c_void_p, C.c_void_p)(0x14079b020)
spatial_checks = []
for run, model in zip(runs[:2], receipt['results']):
    expected = model['full']['regions']
    assert len(expected) == len(run['regions'])
    for actual, predicted in zip(run['regions'], expected):
        assert actual['resource'] == predicted['resource']
        assert actual['points'] == b''.join(struct.pack('<4f', *p) for p in predicted['points']).hex()
        assert actual['header'][:32] == struct.pack('<4f', *predicted['native_bound']).hex()
        pts = [list(struct.unpack('<4f', bytes.fromhex(actual['points'])[i:i+16]))
               for i in range(0, actual['count'] * 16, 16)]
        header = C.create_string_buffer(48)
        point_buffer = C.create_string_buffer(bytes.fromhex(actual['points']))
        C.memmove(C.addressof(header), bytes.fromhex(actual['header']), 24)
        C.c_uint32.from_buffer(header, 24).value = len(pts)
        C.c_void_p.from_buffer(header, 32).value = C.addressof(point_buffer)
        probes = [(p[:2], 'endpoint') for p in pts]
        probes.append(([1000000., 1000000.], 'far'))
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0]-a[0], b[1]-a[1]
            length = math.hypot(dx, dy)
            if length == 0:
                continue
            w = max(a[3], b[3])
            for fraction in (0., .5, .9999, 1.0001, 1.5):
                probes.append(([(a[0]+b[0])/2-dy/length*w*fraction,
                                (a[1]+b[1])/2+dx/length*w*fraction], 'segment'))
        for xy, kind in probes:
            xy = [geometry.number(v) for v in xy]
            hit = C.c_uint8()
            positions = (C.c_float * 27)(*([*xy, 0] * 9))
            payload = (C.c_uint64 * 2)(C.addressof(hit), C.addressof(positions))
            returned = consumer(C.addressof(payload), C.addressof(header))
            assert returned == int(not hit.value)
            semantic = geometry.region_membership(pts, xy) != 'OUTSIDE'
            spatial_checks.append(dict(outcome=run['outcome'], resource=actual['resource'],
                                       kind=kind, xy=xy, native=bool(hit.value), planar=semantic))
    comparisons.append(dict(outcome=run['outcome'], regions=len(expected), exact_points_and_bounds=True))
assert all(r['native'] == r['planar'] for r in spatial_checks)
result = dict(schema='sor-d5t-native/1', functions=pins, runs=runs, key_calls=len(key_calls),
              model_comparisons=comparisons, spatial_checks=spatial_checks,
              errors=errors, crt_sha256=sha('C:/Windows/System32/ucrtbase.dll'),
              code_sha256=sha(__file__), probe_sha256=sha(local/'native_probe.py'), free=free())
with destination_path.open('x', encoding='utf8') as destination:
    json.dump(result, destination, indent=2)
print('PASS', [[sum(r['resource'] == f'{identity:08x}' for r in run['regions'])
                for identity in ids] for run in runs])
