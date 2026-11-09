# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay the pinned Feynman V resource-slot initializer with reader definitions.

SOR-P-0002 lineage: D4E slots, D5AD initializer and D5AR atmosphere reflection.
Constructs private native-shaped forms, supplies the storage and allocator seams,
and executes original selection and slot writes in a disposable process.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import shutil
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
from d5ar_atmosphere_reflection_audit import examine_child

ROOT = Path(__file__).resolve().parents[2]
BODY = 0x5e0de
CODE = (
    0x1402fb000, 0x1402fc000, 0x1403c9000, 0x1405de000, 0x140777000,
    0x140778000, 0x140779000, 0x14077a000, 0x14077b000, 0x14077c000,
    0x1409dd000, 0x1422cc000, 0x142410000, 0x14365d000,
)
DATA = (
    0x143a40000, 0x144a4b000, 0x144af7000, 0x144afa000, 0x144f03000,
    0x144f04000, 0x144f05000, 0x14591f000, 0x145e60000, 0x1461e1000,
)
EXPECTED = {
    0xfc61c: (0x57cb, 0x57ce, 0, 0, 0, 0, 0x83ec),
    0x145440: (0x57cf, 0x57d0, 0, 0x57d4, 0, 0, 0),
    0x1a540d: (0x57c1, 0x57c4, 0, 0, 0, 0, 0),
}
require = host.require
address = C.addressof


def definitions(esm):
    sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
    from inspect_outpost_definitions import esm_records

    host.read_pinned(esm, host.ESM, 'Starfield main ESM')
    wanted = {b'PNDT', b'ATMO', b'BIOM', b'RSGD', b'IRES'}
    records = {}
    for header, fields in esm_records(esm, wanted, repeated=True):
        fid, kind = header['formid'], header['type']
        if kind in ('PNDT', 'ATMO') and fid not in (BODY, 0xc19b):
            continue
        require(fid not in records, 'Duplicate main-file form in component inventory')
        records[fid] = (kind, fields)
    host.read_pinned(esm, host.ESM, 'Starfield main ESM after component extraction')

    def fields(fid, kind, tag):
        actual, values = records[fid]
        require(actual == kind, f'Unexpected record type for {fid:#x}')
        return [raw for key, raw in values if key == tag]

    def one(fid, kind, tag):
        values = fields(fid, kind, tag)
        require(len(values) == 1, f'Wrong {tag!r} count for {fid:#x}')
        return values[0]

    seed, = struct.unpack('<I', one(BODY, 'PNDT', b'RSCS'))
    components = [struct.unpack_from('<IfII', raw) for raw in fields(BODY, 'PNDT', b'PPBD')]
    require([row[0] for row in components] == sorted(EXPECTED), 'Wrong component inventory')
    atmosphere = [struct.unpack_from('<I', raw)[0] for raw in fields(BODY, 'PNDT', b'INAM') if len(raw) == 16]
    require(atmosphere == [0xc19b], 'Wrong typed atmosphere link')
    parent, = struct.unpack('<I', one(0xc19b, 'ATMO', b'RFDP'))
    atmosphere_count = examine_child(one(0xc19b, 'ATMO', b'RDIF'), parent)['requested_list_count']
    require(atmosphere_count == 0, 'Nonempty atmosphere requires a new fixture')
    biomes = {fid: [v[0] for v in struct.iter_unpack('<I', b''.join(fields(fid, 'BIOM', b'RNAM')))]
              for fid, _, _, _ in components}
    descriptors = {}
    for fid in {fid for links in biomes.values() for fid in links} | {r[3] for r in components if r[3]}:
        kind, values = records[fid]
        entries = [(tag, raw) for tag, raw in values if tag in (b'RNAM', b'DNAM')]
        require(kind == 'RSGD' and len(entries) % 2 == 0
                and [t for t, _ in entries] == [b'RNAM', b'DNAM'] * (len(entries) // 2),
                'Unexpected RSGD descriptor framing')
        descriptors[fid] = [(struct.unpack('<I', entries[i][1])[0], entries[i + 1][1])
                            for i in range(0, len(entries), 2)]
        require(all(len(raw) == 560 for _, raw in descriptors[fid]), 'Wrong DNAM length')
    resources = {}
    pending = [rid for items in descriptors.values() for rid, _ in items]
    while pending:
        rid = pending.pop()
        if rid in resources:
            continue
        rarity, = struct.unpack('<I', one(rid, 'IRES', b'SNAM'))
        require(rarity <= 6, 'Unsupported IRES rarity')
        children = [struct.unpack('<I', raw)[0] for raw in fields(rid, 'IRES', b'CNAM')]
        resources[rid] = rarity, children
        pending.extend(children)
    return seed, components, biomes, descriptors, resources


class Components:
    def __init__(self, kernel, crt, pages, definitions):
        self.seed, self.rows, biomes, descriptors, resources = definitions
        self.keep = []
        self.callbacks = []
        self.buffers = {}
        self.errors = []
        self.storage = self.buffer(0x400)
        self.atmosphere = self.buffer(0x108)
        self.allocator = self.buffer(0xa0)
        self.tls = self.buffer(0x1d8)
        self.tls[0xbc] = b'\1'
        self.planet = self.form(BODY, 0xba, 0x80)
        self.forms = {}
        for fid, (rarity, _) in resources.items():
            self.forms[fid] = self.form(fid, 0x9f, 0x118)
            host.put(self.forms[fid], 0x110, '<B', rarity)
        for fid, (_, children) in resources.items():
            pointers = self.pointer_array(self.forms[c] for c in children)
            struct.pack_into('<I4xQ', self.forms[fid], 0xc0, len(children), address(pointers))
        for fid, items in descriptors.items():
            form = self.form(fid, 0xab, 0x48)
            self.forms[fid] = form
            entries = self.buffer(0x238 * len(items))
            for i, (rid, dnam) in enumerate(items):
                struct.pack_into('<Q560s', entries, i * 0x238, address(self.forms[rid]), dnam)
            struct.pack_into('<I4xQ', form, 0x38, len(items), address(entries))
        for fid, links in biomes.items():
            self.forms[fid] = form = self.form(fid, 0xa0, 0x318)
            pointers = self.pointer_array(self.forms[link] for link in links)
            struct.pack_into('<I4xQ', form, 0x308, len(links), address(pointers))
        self.payloads = {fid: self.buffer(0x70) for fid, _, _, _ in self.rows}
        host.allocate_pages(kernel, pages)
        C.c_void_p.from_address(0x143a404f0).value = C.cast(crt.log2f, C.c_void_p).value
        # Redirect the game's static TLS load to fixture memory. All arithmetic
        # and subsequent selection/slot instructions are original.
        C.memmove(0x1407778a0, b'\x48\xbb' + struct.pack('<Q', address(self.tls)) + b'\x90\x90', 12)
        ptr, word = C.c_void_p, C.c_uint32
        self.stub(0x14077bce0, None, (ptr, word, ptr), self.collect)
        self.stub(0x1409dd080, ptr, (ptr, word), self.atmosphere_lookup)
        self.stub(0x1405de3b0, ptr, (word,), self.resolve)
        self.stub(0x1424105d0, ptr, (ptr, ptr, ptr), self.late_lookup)
        self.stub(0x1422cc0d0, word, (ptr, ptr, word, word), self.append)
        reserve = self.callback(None, (ptr, word, word), self.reserve)
        C.c_void_p.from_address(0x144afa3a0).value = C.cast(reserve, ptr).value
        C.c_uint32.from_address(0x145e60398).value = 2
        C.c_uint8.from_address(0x145e603c0).value = 0
        C.c_uint64.from_address(0x145e60898).value = 0
        for page in pages:
            host.protect(kernel, page, 0x20 if page in CODE else 2)
        host.flush(kernel)
        self.initialize = host.callsite(0x140779760, 2, None)

    def buffer(self, size):
        result = C.create_string_buffer(size)
        self.keep.append(result)
        return result

    def form(self, fid, kind, size):
        result = self.buffer(size)
        host.put(result, 0x28, '<I', fid)
        host.put(result, 0x2e, '<B', kind)
        return result

    def pointer_array(self, buffers):
        result = (C.c_uint64 * len(items := list(buffers)))(*(address(x) for x in items))
        self.keep.append(result)
        return result

    def callback(self, result, args, operation):
        def checked(*values):
            try:
                return operation(*values)
            except (ValueError, KeyError, struct.error) as error:
                self.errors.append(str(error))
                return None if result in (None, C.c_void_p) else 0xffffffff
        function = C.WINFUNCTYPE(result, *args)(checked)
        self.callbacks.append(function)
        return function

    def stub(self, entry, result, args, operation):
        function = self.callback(result, args, operation)
        jump = b'\x48\xb8' + struct.pack('<Q', C.cast(function, C.c_void_p).value) + b'\xff\xe0'
        C.memmove(entry, jump, len(jump))

    def install_vector(self, vector, stride, items=None):
        require(stride in (4, 8), 'Unsupported vector element width')
        storage = self.buffer(32 * stride)
        self.buffers[address(storage)] = stride
        count = 0
        if items is not None:
            for count, value in enumerate(items, 1):
                host.put(storage, (count - 1) * stride, '<Q', value)
        C.memmove(vector, struct.pack('<IIQQ', count, 32, address(self.allocator), address(storage)), 24)

    def reserve(self, adapter, capacity, stride):
        require(0 < capacity <= 32, 'Unexpected native reserve request')
        self.install_vector(C.c_void_p.from_address(adapter + 8).value, stride)

    def append(self, vector, adapter, capacity, stride):
        count, actual = (C.c_uint32 * 2).from_address(vector)
        if not actual:
            self.install_vector(vector, stride)
        pointer = C.c_void_p.from_address(vector + 0x10).value
        require(count < 32 and self.buffers[pointer] == stride, 'Out-of-bounds vector append')
        C.c_uint32.from_address(vector).value = count + 1
        return count

    def collect(self, storage, fid, capture):
        require(fid == BODY and C.c_void_p.from_address(storage).value == address(self.storage),
                'Wrong component storage collector input')
        self.install_vector(C.c_void_p.from_address(capture).value, 8,
                            (address(self.payloads[fid]) for fid in sorted(self.payloads)))

    def atmosphere_lookup(self, storage, fid):
        require(fid == BODY and C.c_void_p.from_address(storage).value == address(self.storage),
                'Wrong atmosphere lookup input')
        return address(self.atmosphere)

    def resolve(self, fid):
        return address(self.forms[fid]) if fid else None

    def late_lookup(self, storage, result, key):
        require(storage == address(self.storage) + 0x268, 'Wrong late BiomeData storage')
        C.memmove(result, struct.pack('<4Q', 0, 0, 0, 0xfe0), 32)
        return result

    def run(self, seed):
        struct.pack_into('<II', self.planet, 0x50, seed, BODY)
        for fid, chance, fallback, override in self.rows:
            payload = self.payloads[fid]
            C.memset(payload, 0, C.sizeof(payload))
            struct.pack_into('<IfII', payload, 0x40, fid, chance, fallback, override)
            struct.pack_into('<7I', payload, 0x50, *([0xffffffff] * 7))
        self.initialize(C.byref(C.c_void_p(address(self.planet))), C.byref(C.c_void_p(address(self.storage))))
        require(not self.errors, f'Native component seams refused: {self.errors}')
        return {fid: struct.unpack_from('<7I', payload, 0x50) for fid, payload in self.payloads.items()}

    def controls(self):
        actual = self.run(self.seed)
        require(actual == EXPECTED, f'Original seeded initializer differs: {actual}')
        shifted = self.run(self.seed + 1)
        fallback = self.run(0)
        require(shifted[0x145440] == (0x57cb, 0x57ce, 0, 0, 0, 0, 0)
                and fallback[0x145440] != actual[0x145440], 'Native seed perturbation did not discriminate')
        return {'seed': self.seed, 'components': actual, 'seed_plus_one': shifted, 'zero_seed': fallback,
                'zero_seed_matches_owned_model': fallback[0x145440] == (0x57cf, 0x57d0, 0, 0, 0, 0, 0)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('--exe', '--esm'):
        parser.add_argument(flag, required=True, type=Path)
    args = parser.parse_args()
    try:
        kernel, crt = host.host_preflight()
        exe, esm = host.regular(args.exe), host.regular(args.esm)
        drives = {exe.anchor, esm.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), 'Insufficient disk floor')
        pages = host.pe_pages(host.read_pinned(exe, host.EXE, 'Starfield EXE', keep=True), CODE, DATA)
        reader = definitions(esm)
        host.cpu_check(kernel)
        result = Components(kernel, crt, pages, reader).controls()
    except (OSError, ValueError, KeyError, struct.error) as error:
        parser.exit(1, f'D5BJ components refused: {error}\n')
    print(json.dumps(dict(scope='Native seeded slot initialization with reader-derived forms and private storage',
                          **result), sort_keys=True))


if __name__ == '__main__':
    main()
