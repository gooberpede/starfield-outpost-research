# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare the fixed D5AQ native ordinary stage to the planar model and D5AS.

SOR-P-0002 lineage: D5AF geometry host, D5S private native callbacks, RG1
geometry/context, owned ESM and surface layout readers. Supply explicit EXE,
ESM, PlanetData and a separately provisioned exact D5AS comparison archive.
Run in a disposable process. Reads inputs and writes only JSON to stdout.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import shutil
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as sampler

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = 'd0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c'
OWNER = 0x5e0de
BIOME = 0x145440
RSGD = 0x258050
ROOT_RESOURCE = 0x57cf
RESOURCES = {0x57d4: 3, 0x57d0: 1, ROOT_RESOURCE: 0}
SETTINGS = (0x2d40c0, 0x226b0c, 0x226b0e, 0x226b0d, 0x2f031c, 0x2d40ce)
CONSTANTS = (
    0x144f0416c, 0x144f049f4, 0x144f04654, 0x144f048dc, 0x144f052b0,
    0x144f052f8, 0x144f03d80, 0x144f03d40, 0x144f03e00, 0x144f03ed4,
    0x144f04178, 0x144f03dc4, 0x144f03d58, 0x144f03e48, 0x144f03fd4, 0x144f03f50,
)
CODE = tuple(sorted(set(sampler.CODE) | {
    0x1402fb000, 0x1404a7000, 0x1404a8000, 0x14079a000, 0x14079b000,
    0x1407a9000, 0x1407ac000, 0x1407ae000, 0x1407af000, 0x1422cc000,
    0x142346000, 0x142bf4000, 0x143751000,
}))
WRITABLE = (0x14591f000, 0x145920000, 0x145921000)
DATA = tuple(sorted(set(sampler.DATA) | set(WRITABLE) | {
    0x143a3f000, 0x144a47000, 0x144ae8000, 0x144af7000, 0x144b01000,
    0x144b0f000, 0x144d58000, 0x144d59000, 0x144f03000, 0x145e60000,
    0x145fb5000, 0x145fd9000, 0x14883e000,
}))
ORIGIN = (-200, -200)
ANCHOR = (37536, 20928)
CELLS = range(1, 13)
require = sampler.require


def definitions(esm):
    for path in ('save-analysis/scripts', 'research/resource-pattern-selection',
                 'research/resource-owner-root'):
        sys.path.insert(0, str(ROOT / path))
    from inspect_outpost_definitions import esm_records
    from installed import decode_tree, planet_tree
    from source_layout import install_fnam

    sampler.read_pinned(esm, sampler.ESM, 'Starfield main ESM')
    records = {}
    tags = {b'PNDT', b'SFTR', b'SFPT', b'SFBK', b'BIOM', b'RSGD', b'IRES', b'GMST'}
    needed = {OWNER, 0x168814, 0x23ddf3, 0x29d20e, BIOME, RSGD, 0x57cb, 0x57d1, *RESOURCES, *SETTINGS}
    for header, fields in esm_records(esm, tags, repeated=True):
        fid = header['formid']
        if fid in needed:
            require(fid not in records, f'Duplicate main-file FormID {fid:#x}')
            records[fid] = (header['type'], fields)
    require(set(records) == needed, 'Incomplete selected main-file records')
    sampler.read_pinned(esm, sampler.ESM, 'Starfield main ESM after record walk')

    def fields(fid, kind, tag):
        require(records[fid][0] == kind, f'Unexpected record type for {fid:#x}')
        return [raw for key, raw in records[fid][1] if key == tag]

    def one(fid, kind, tag):
        values = fields(fid, kind, tag)
        require(len(values) == 1, f'Expected one {tag!r} for {fid:#x}')
        return values[0]

    system_fields = [raw for raw in fields(OWNER, 'PNDT', b'GNAM') if len(raw) == 12]
    require(len(system_fields) == 1, 'Expected one PNDT system/body field')
    system, parent, body = struct.unpack('<III', system_fields[0])
    require((system, parent, body) == (86469, 0, 5), 'Feynman V system/body mismatch')
    tree = planet_tree(records[OWNER][1])
    require(tree == 0x168814 and records[tree][0] == 'SFTR', 'Wrong PNDT tree')
    pattern, flags = decode_tree(records[tree][1])[0][195 * 256 + 109]
    require((pattern, flags) == (0x23ddf3, 8), 'Wrong tree tile or flags')
    entries = zip(struct.unpack('<256I', one(pattern, 'SFPT', b'FNAM')), one(pattern, 'SFPT', b'GNAM'))
    block, flags = install_fnam(list(entries))[8 * 16]
    require((block, flags) == (0x29d20e, 136)
            and struct.unpack('<II', one(block, 'SFBK', b'DNAM')) == (14, 14),
            'Wrong installed pattern source or extent')
    selected = [struct.unpack_from('<IfII', raw) for raw in fields(OWNER, 'PNDT', b'PPBD')
                if struct.unpack_from('<I', raw)[0] == BIOME]
    require(selected == [(BIOME, 25., 0x63c977c1, 0)]
            and struct.unpack('<I', one(BIOME, 'BIOM', b'RNAM'))[0] == RSGD,
            'Wrong main-file biome or RSGD path')
    entries = [(tag, raw) for tag, raw in records[RSGD][1] if tag in (b'RNAM', b'DNAM')]
    require(records[RSGD][0] == 'RSGD' and [tag for tag, _ in entries] == [b'RNAM', b'DNAM'] * 2,
            'Unexpected RSGD entry layout')
    rsgd_resources = [struct.unpack('<I', entries[i][1])[0] for i in (0, 2)]
    require(rsgd_resources == [0x57cb, ROOT_RESOURCE]
            and all(struct.unpack('<I', one(fid, 'IRES', b'SNAM'))[0] == 0 for fid in rsgd_resources),
            'Special or Everywhere RSGD entry or wrong common resources')
    for parent, child in ((ROOT_RESOURCE, 0x57d0), (0x57d0, 0x57d1), (0x57d1, 0x57d4)):
        children = {struct.unpack('<I', raw)[0] for raw in fields(parent, 'IRES', b'CNAM')}
        require(child in children, 'Wrong fixed family membership')
    require(all(struct.unpack('<I', one(fid, 'IRES', b'SNAM'))[0] == rarity
                for fid, rarity in RESOURCES.items()), 'Wrong fixed family rarities')
    descriptor = entries[3][1]
    require(len(descriptor) == 560, 'Unexpected Copper DNAM size')
    blocks = {fid: list(struct.unpack_from('<8f', descriptor, (rarity + 7) * 40)) + [0, 0]
              for fid, rarity in RESOURCES.items()}
    settings = [struct.unpack('<f', one(fid, 'GMST', b'DATA'))[0] for fid in SETTINGS]
    return system, body, blocks, settings


def plan(esm, pages):
    sys.path.insert(0, str(ROOT / 'research/resource-geometry'))
    import context
    import geometry

    system, body, blocks, settings = definitions(esm)
    constants = {va: struct.unpack_from('<f', pages[va & ~4095], va & 4095)[0] for va in CONSTANTS}
    keys = {(x, y): context.packed_seed_key(0, ANCHOR, ORIGIN, (x, y), system, body)
            for x in CELLS for y in CELLS}
    requests = {}
    for mask in (0, 3):
        ordered = [{'resource': f'{fid:08x}', 'block': blocks[fid],
                    'weight': settings[rarity] if mask < rarity else 1.0}
                   for fid, rarity in RESOURCES.items()]
        request = dict(source='0:37536:20928:0029d20e', provenance='D5BJ fixed main-file operands',
                       origin=ORIGIN, owner_key=OWNER, clip_center=[300, 300, 0],
                       clip_half=[700, 700, 0], context_qualified=True, order_qualified=True,
                       cell_bounds=[1, 13, 1, 13], ordered_resources=ordered,
                       packed_keys={f'{x},{y}': key for (x, y), key in keys.items()})
        oracle = geometry.populate_source(request, constants)
        require(oracle['status'] == 'CONDITIONAL_PLANAR_SOURCE',
                f"Planar model declined fixed inputs: {oracle.get('reason')}")
        requests[mask] = (ordered, oracle['regions'])
    return keys, requests


class GeometryHost:
    def __init__(self, kernel, crt, pages):
        self.buffers = {}
        self.collections = {fid: C.create_string_buffer(24) for fid in RESOURCES}
        self.output = C.create_string_buffer(48)
        self.slots = C.create_string_buffer(24 * len(RESOURCES))
        self.manager, self.index, self.master = sampler.numeric_fixture()
        self.fail_append = False
        self.fail_allocation = False
        self.errors = []
        sampler.put(self.manager, 0x80, '<I', OWNER)
        sampler.put(self.output, 24, '<Q', C.addressof(self.slots))
        sampler.put(self.output, 32, '<Q', len(self.collections))
        for i, (fid, collection) in enumerate(self.collections.items()):
            struct.pack_into('<I4xQI', self.slots, 24 * i, fid, C.addressof(collection), 1)
        sampler.allocate_pages(kernel, pages)
        sampler.bind_imports(crt, sampler.IMPORTS | {'atan2f': (0x1434ca936, 0x143a40600)})
        sampler.set_numeric_globals()
        C.c_void_p.from_address(0x143a404f0).value = C.cast(crt.log2f, C.c_void_p).value
        C.c_void_p.from_address(0x145fd9c30).value = C.addressof(self.manager)
        C.c_uint32.from_address(0x145e60398).value = 2
        C.c_uint8.from_address(0x145e603c0).value = 0
        C.c_uint32.from_address(0x145921e84).value = 0xffffffff
        self.callbacks = (
            C.WINFUNCTYPE(C.c_uint32, C.c_void_p, C.c_void_p, C.c_uint32, C.c_uint32)(self.append),
            C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_uint32, C.c_uint32, C.c_uint32)(self.reserve),
            C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p)(self.collection),
            C.WINFUNCTYPE(None, C.c_void_p)(self.keep_until_exit),
        )
        for address, callback in zip((0x1422cc0d0, 0x1422cc2c0, 0x1407a97c0), self.callbacks):
            jump = b'\x48\xb8' + struct.pack('<Q', C.cast(callback, C.c_void_p).value) + b'\xff\xe0'
            C.memmove(address, jump, len(jump))
        C.c_void_p.from_address(0x143a40470).value = C.cast(self.callbacks[3], C.c_void_p).value
        for page in pages:
            protection = 0x20 if page in CODE else 4 if page in WRITABLE else 2
            sampler.protect(kernel, page, protection)
        sampler.flush(kernel)
        self.invoke = C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p,
                                    C.c_void_p, C.c_void_p, C.c_float, C.c_void_p)(0x14079a330)

    def ensure(self, vector, capacity, stride):
        length, current = (C.c_uint32 * 2).from_address(vector)
        if not 0 <= length <= current <= 1024 or not 0 < capacity <= 1024 or stride not in (16, 48):
            self.errors.append('Unsupported native allocation operands')
            return False
        if capacity <= current:
            return True
        if self.fail_allocation:
            return False
        new = C.create_string_buffer(max(capacity, 4) * stride)
        self.buffers[C.addressof(new)] = new
        pointer = C.c_void_p.from_address(vector + 8)
        if length and not self.has_span(pointer.value, length * stride):
            self.errors.append('Unowned native allocation')
            return False
        if length:
            C.memmove(new, pointer.value, length * stride)
        pointer.value = C.addressof(new)
        C.c_uint32.from_address(vector + 4).value = max(capacity, 4)
        return True

    def has_span(self, address, size):
        buffer = self.buffers.get(address)
        return buffer is not None and C.sizeof(buffer) >= size

    def append(self, vector, allocator, capacity, stride):
        count = C.c_uint32.from_address(vector)
        if self.fail_append or not self.ensure(vector, count.value + 1, stride):
            return 0xffffffff
        count.value += 1
        return count.value - 1

    def reserve(self, vector, allocator, capacity, needed, stride):
        return int(self.ensure(vector, needed, stride))

    def collection(self, owner, key, destination):
        target = self.collections.get(C.c_uint32.from_address(key).value)
        if target is None:
            self.errors.append('Unknown native resource collection')
            C.c_void_p.from_address(destination).value = None
            return 0
        C.c_uint32.from_buffer(target).value += 1
        C.c_void_p.from_address(destination).value = C.addressof(target)
        return 1

    def keep_until_exit(self, pointer):
        """The private buffers remain owned by Python until process exit."""

    def verify_keys(self, keys):
        convert = sampler.callsite(0x14078d7b0, 3)
        for (x, y), expected in keys.items():
            query = (C.c_int32 * 2)(x + ORIGIN[0], y + ORIGIN[1])
            result = C.c_uint64()
            convert(self.manager, C.byref(result), query)
            require(result.value == expected, f'Native generation key mismatch at ({x}, {y})')

    def populate(self, resources):
        for collection in self.collections.values():
            C.memset(collection, 0, 24)
            sampler.put(collection, 0, '<I', 1)
        origin = (C.c_int32 * 2)(*ORIGIN)
        clip = (C.c_float * 8)(300, 300, 0, 0, 700, 700, 0, 0)
        for item in resources:
            fid = int(item['resource'], 16)
            rarity = RESOURCES[fid]
            ires = C.create_string_buffer(0x118)
            sampler.put(ires, 0x28, '<I', fid)
            sampler.put(ires, 0x110, '<B', rarity)
            dnam = C.create_string_buffer(0x238)
            struct.pack_into('<10f', dnam, (rarity + 7) * 40, *item['block'])
            for x in CELLS:
                for y in CELLS:
                    cell = (C.c_int32 * 4)(x, y)
                    self.invoke(ires, cell, origin, clip, dnam, item['weight'], self.output)
                    require(not self.errors, str(self.errors))
        result = {}
        for fid, collection in self.collections.items():
            count, address = struct.unpack_from('<I4xQ', collection, 8)
            require(0 < count <= 144 and self.has_span(address, count * 48),
                    f'Invalid native collection for {fid:#x}')
            regions = []
            for i in range(count):
                region = address + i * 48
                size = C.c_uint32.from_address(region + 24).value
                points = C.c_void_p.from_address(region + 32).value
                require(0 < size <= 64 and self.has_span(points, size * 16), 'Invalid native region')
                regions.append((C.string_at(region, 24), C.string_at(points, size * 16)))
            result[fid] = regions
        return result

    def copy_and_failure_controls(self):
        append = sampler.callsite(0x1407ac2f0, 2, C.c_uint32)
        point = (C.c_float * 4)(1., 2., 0., 3.)
        source, collection = C.create_string_buffer(48), C.create_string_buffer(16)
        struct.pack_into('<4fIB3xIIQ', source, 0, *point, 0x57d4, 3, 1, 1, C.addressof(point))
        require(append(collection, source) == 0, 'Native positive region append failed')
        destination, = struct.unpack_from('<Q', collection, 8)
        require(self.has_span(destination, 48), 'Native destination region is unowned')
        copied = C.c_void_p.from_address(destination + 32).value
        original_point = bytes(point)
        require(copied != C.addressof(point) and self.has_span(copied, 16)
                and C.string_at(copied, 16) == original_point
                and C.string_at(destination, 24) == source.raw[:24]
                and C.c_uint32.from_address(destination + 24).value == 1,
                'Native region append failed to deep-copy the point and header')
        point[0] = 9.
        require(C.string_at(copied, 16) == original_point, 'Native copy aliases the source point')
        self.fail_append = True
        negative = C.create_string_buffer(16)
        require(append(negative, source) == 0xffffffff and negative.raw == bytes(16),
                'Native failed append did not preserve an empty collection')
        self.fail_append = False
        self.fail_allocation = True
        negative = C.create_string_buffer(16)
        require(append(negative, source) == 0xffffffff and negative.raw == bytes(16),
                'Native failed allocation did not preserve an empty collection')
        self.fail_allocation = False


def canonical(population, model):
    body = [struct.pack('<I', len(population))]
    for fid, regions in sorted(population.items()):
        expected = [(struct.pack('<4f', *row['native_bound']),
                     b''.join(struct.pack('<4f', *point) for point in row['points']))
                    for row in model if int(row['resource'], 16) == fid]
        require([(header[:16], points) for header, points in regions] == expected,
                f'Native region bounds or points differ from planar model for {fid:#x}')
        body.append(struct.pack('>I', fid) + struct.pack('<I', len(regions)))
        for header, points in regions:
            body.append(header[:21] + struct.pack('<I', len(points) // 16) + points)
    return b''.join(body)


def spatial_control(low, high):
    consumer = sampler.callsite(0x14079b020, 2, C.c_uint8)
    first = high[0x57d4][0]
    require(len(first[1]) == 16, 'Historical one-point discriminator differs')
    xy = struct.unpack_from('<2f', first[1])

    def hits(region, point):
        header, raw = region
        points = C.create_string_buffer(raw)
        fixture = C.create_string_buffer(48)
        C.memmove(fixture, header, 24)
        sampler.put(fixture, 24, '<I', len(raw) // 16)
        sampler.put(fixture, 32, '<Q', C.addressof(points))
        hit = C.c_uint8()
        positions = (C.c_float * 27)(*((*point, 0) * 9))
        payload = (C.c_uint64 * 2)(C.addressof(hit), C.addressof(positions))
        require(consumer(payload, fixture) == int(not hit.value), 'Native competition return mismatch')
        return bool(hit.value)

    require(hits(first, xy) and not any(hits(region, xy) for region in low[0x57d4])
            and not hits(first, (1e6, 1e6)), 'Native first-resource spatial discriminator mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('--exe', '--esm', '--planet-data', '--d5as'):
        parser.add_argument(flag, type=Path, required=True)
    args = parser.parse_args()
    try:
        kernel, crt = sampler.host_preflight()
        exe, esm, atlas, d5as = (sampler.regular(p) for p in (args.exe, args.esm, args.planet_data, args.d5as))
        drives = {p.anchor for p in (exe, esm, atlas, d5as)} | {Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), 'Insufficient disk floor')
        sys.path.insert(0, str(ROOT / 'research/evidence-access/d5be'))
        import d5as_verify
        manifest, bodies = d5as_verify.read_package(sampler.read_pinned(d5as, PACKAGE, 'D5AS candidate', keep=True))
        d5as_verify.verify(manifest, bodies)
        pages = sampler.pe_pages(sampler.read_pinned(exe, sampler.EXE, 'Starfield EXE', keep=True), CODE, DATA)
        with atlas.open('rb') as stream:
            sampler.authenticate(stream, sampler.BA2, 'PlanetData archive')
            masks = sampler.faces(sampler.raster_member(stream))
        expected, shifted = sampler.independent_oracle(masks)
        keys, requests = plan(esm, pages)
        sampler.cpu_check(kernel)
        host = GeometryHost(kernel, crt, pages)
        host.verify_keys(keys)
        host.copy_and_failure_controls()
        native = sampler.run_numeric(kernel, masks, expected, shifted)
        sampled = {branch: {tuple(row['query']): row['mask'] for row in result['rows']}
                   for branch, result in native.items()}
        results, previous = [], {}
        for query in ((4, -1), (4, 1), (5, 0)):
            mask = sampled['nonfused'][query]
            require(sampled['fma'][query] == mask, 'Native arithmetic paths disagree on geometry mask')
            resources, model = requests[mask]
            population = host.populate(resources)
            body = canonical(population, model)
            require(body == bodies[f'references/mask{mask}.bin'], 'Native body differs from D5AS reference bytes')
            if mask in previous:
                require(population == previous[mask], 'Repeated mask changed the full native population')
            previous[mask] = population
            counts = {f'{fid:08x}': [len(regions), sum(len(points) // 16 for _, points in regions)]
                      for fid, regions in population.items()}
            results.append(dict(query=query, mask=mask, canonical_sha256=sampler.digest(body), counts=counts))
        require(previous[0] != previous[3], 'Different masks unexpectedly match')
        spatial_control(previous[0], previous[3])
    except (ValueError, OSError, struct.error, zlib.error) as error:
        parser.exit(1, f'D5BJ geometry refused: {error}\n')
    print(json.dumps(dict(scope='Fixed ordinary stage with supplied historical family and frame',
                          candidate=PACKAGE, repeats_equal=True, classes_differ=True,
                          packed_keys=144, failed_append_refused=True,
                          failed_allocation_refused=True, deep_copy=True,
                          native_sampler_branches=list(sampled),
                          first_resource_spatial_control=True, runs=results), sort_keys=True))


if __name__ == '__main__':
    main()
