# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay D5S/D5AQ source-key, corner and Grid retirement fixture controls.

SOR-P-0002 adaptation of D5S native key/corner/retirement and D5H placement
closure methods. Reads explicitly supplied EXE/ESM and owned readers.
Private buffers, callback substitutions and stdout are the only effects.
"""
import argparse
from collections import Counter, defaultdict
import ctypes as C
from itertools import permutations
import json
from pathlib import Path
import shutil
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as sampler

ROOT = Path(__file__).resolve().parents[2]
ANCHOR = (37536, 20928)
TARGET = (*ANCHOR, 0x29d20e)
CODE = (
    0x1402c4000, 0x140781000, 0x140785000, 0x140970000, 0x140982000, 0x140986000,
    0x140987000, 0x140988000, 0x1422c7000, 0x1422cc000, 0x14365c000,
)
DATA = (
    0x143a40000, 0x144b3e000, 0x144b67000, 0x144d58000, 0x144d59000,
    0x144da9000, 0x145fd9000,
)
require = sampler.require
PLACEMENT = {'DFOB', 'PCMT', 'PCBN', 'PCCN', 'CNDF'}
PLACEMENT_SLOTS = (
    (0x144b41d80, 0x350, 0x1407c6080),
    (0x144b41200, 0x350, 0x1407c1260), (0x144b41200, 0x358, 0x1407c2cb0),
    (0x144b41200, 0x370, 0x1407c0950),
    (0x144b417d8, 0x350, 0x1407c3a00), (0x144b417d8, 0x358, 0x1407c3fb0),
    (0x144b417d8, 0x370, 0x1407c4800),
)


def placement_tree(records):
    root = 0x5b62b
    kind, fields = records[0x5b63c]
    require(kind == 'DFOB' and [raw for key, raw in fields if key == b'DATA'] == [struct.pack('<I', root)]
            and records[root][0] == 'PCMT', 'Wrong LoadingCells default or tree')
    children = defaultdict(list)
    for fid, (kind, fields) in records.items():
        if kind in ('PCBN', 'PCCN'):
            for key, raw in fields:
                if key == b'PRTN':
                    parent, = struct.unpack('<I', raw)
                    children[parent].append(fid)
    visited, pending = set(), [root]
    while pending:
        fid = pending.pop()
        if fid in visited:
            continue
        visited.add(fid)
        pending.extend(children[fid])
    kinds = Counter(records[fid][0] for fid in visited)
    require(kinds == {'PCMT': 1, 'PCBN': 108, 'PCCN': 525}, 'Wrong LoadingCells tree closure')
    pending = list(visited)
    conditions = Counter()
    while pending:
        fid = pending.pop()
        for key, raw in records[fid][1]:
            if key != b'CTDA':
                continue
            require(len(raw) == 32, 'Unexpected main-file placement condition layout')
            index, = struct.unpack_from('<H', raw, 8)
            conditions[index] += 1
            if index == 837:
                reference, = struct.unpack_from('<I', raw, 12)
                require(records[reference][0] == 'CNDF', 'Wrong nested placement condition form')
                if reference not in visited:
                    visited.add(reference)
                    pending.append(reference)
    require(len(visited) - sum(kinds.values()) == 38, 'Wrong nested condition-form closure')
    require(conditions == {74: 17, 77: 16, 562: 5, 801: 3, 837: 53, 858: 40,
                           859: 18, 861: 50, 865: 13, 916: 6, 942: 1}, 'Wrong placement condition census')
    return {'forms': dict(kinds) | {'CNDF': 38}, 'condition_uses': dict(conditions)}


def placement_dispatch_slots(pe):
    sections = sampler.pe_sections(pe)
    for table, slot, expected in PLACEMENT_SLOTS:
        address = table + slot
        offsets = [offset + address - start for name, start, virtual, size, offset, _ in sections
                   if name == b'.rdata' and start <= address and address + 8 <= start + min(size, virtual)]
        require(len(offsets) == 1 and struct.unpack_from('<Q', pe, offsets[0])[0] == expected,
                f'Wrong main-file placement dispatch pointer at {address:#x}')
    return len(PLACEMENT_SLOTS)


def inventory(esm):
    for path in ('save-analysis/scripts', 'research/resource-pattern-selection',
                 'research/resource-owner-root'):
        sys.path.insert(0, str(ROOT / path))
    from inspect_outpost_definitions import esm_records
    from installed import decode_tree, planet_tree
    from source_layout import install_fnam

    sampler.read_pinned(esm, sampler.ESM, 'Starfield main ESM')
    wanted = {b'PNDT', b'SFTR', b'SFPT', b'SFBK'} | {kind.encode('ascii') for kind in PLACEMENT}
    records = {}
    for header, fields in esm_records(esm, wanted, repeated=True):
        if header['type'] in PLACEMENT | {'SFPT', 'SFBK'} or header['formid'] in (0x5e0de, 0x168814):
            fid = header['formid']
            require(fid not in records, f'Duplicate main-file record {fid:#x}')
            records[fid] = (header['type'], fields)
    sampler.read_pinned(esm, sampler.ESM, 'Starfield main ESM after source walk')
    require(records[0x5e0de][0] == 'PNDT', 'Wrong source owner type')
    tree = planet_tree(records[0x5e0de][1])
    require(tree == 0x168814 and records[tree][0] == 'SFTR', 'Wrong source tree')
    chart = decode_tree(records[tree][1])[0]

    def field(fid, kind, tag):
        actual, fields = records[fid]
        values = [raw for key, raw in fields if key == tag]
        require(actual == kind and len(values) == 1, f'Wrong {kind}/{tag!r} for {fid:#x}')
        return values[0]

    sources = {}
    for tx in range(194, 197):
        for ty in range(108, 110):
            pattern, flags = chart[tx * 256 + ty]
            require(flags == 8, 'Wrong source tree flags')
            entries = install_fnam(list(zip(struct.unpack('<256I', field(pattern, 'SFPT', b'FNAM')),
                                            field(pattern, 'SFPT', b'GNAM'))))
            for slot, (block, flags) in enumerate(entries):
                if not flags & 8:
                    continue
                sx, sy = divmod(slot, 16)
                x, y = tx * 192 + sx * 12, ty * 192 + sy * 12
                width, height = (v - 4 for v in struct.unpack('<II', field(block, 'SFBK', b'DNAM')))
                nx, ny = x - ANCHOR[0], y - ANCHOR[1]
                if -100 < nx + width + 2 and nx - 2 < 100 and -100 < ny + height + 2 and ny - 2 < 100:
                    sources[x, y, block] = (width, height, tx, ty, sx, sy, flags >> 5)
    require(len(sources) == 324 and len({k[:2] for k in sources}) == 324
            and sources.get(TARGET, ())[:2] == (10, 10),
            f'Wrong admitted source inventory: {len(sources)} sources, target {sources.get(TARGET)}')
    return sources, placement_tree(records)


def keys_and_corners(sources):
    hashpoint = sampler.callsite(0x140982090, 6, C.c_uint32)
    table = (C.c_uint32 * 256).from_address(0x144d58d70)

    def low_word(tx, ty, sx, sy, orientation):
        args = [C.c_uint32(v) for v in (ty, sx, sy, 0, 0, orientation)]
        seed = hashpoint(*(C.byref(word) for word in args))
        for value in struct.pack('<IB', tx, 0):
            seed = (seed >> 8) ^ table[(seed ^ value) & 255]
        return (seed << 2) & 0xffffffff

    target_words = []
    for oriented in (False, True):
        lows = {source: low_word(tx, ty, sx, sy, orient if oriented else 0)
                for source, (_, _, tx, ty, sx, sy, orient) in sources.items()}
        require(list(lows.values()).count(lows[TARGET]) == 1, 'A prior source aliases the target token low word')
        target_words.append(lows[TARGET])
    require(target_words == [1718132308, 1003558160], 'Target key differs from original native control')
    setter = C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p,
                           C.c_void_p, C.c_uint8)(0x140988670)
    slots = {10: 0x18, 6: 0x20, 9: 0x28, 5: 0x30}
    result = []
    for query, target_slot in (((-2, 11), 0x30), ((11, -2), 0x18), ((10, 11), 0x28), ((-2, -2), 0x20)):
        x, y = (a + b for a, b in zip(query, ANCHOR))
        contributors = {}
        for source, (width, height, *_) in sources.items():
            dx, dy = x - source[0], y - source[1]
            if -2 <= dx < width + 2 and -2 <= dy < height + 2:
                require(not 0 <= dx < width and not 0 <= dy < height, 'Unexpected non-corner contributor')
                flag = (4 if dx < 0 else 8) | (2 if dy < 0 else 1)
                contributors[source] = flag
        require(len(contributors) == 4 and set(contributors.values()) == set(slots)
                and slots[contributors[TARGET]] == target_slot, 'Wrong fixed corner contributors')
        identities = {source: i + 0x1000 for i, source in enumerate(contributors)}
        count = 0
        for order in permutations(contributors):
            cell, coord, weight = C.create_string_buffer(0x80), C.c_uint64(), C.c_uint64()
            for source in order:
                setter(cell, identities[source], C.byref(coord), C.byref(weight), contributors[source])
            require(all(struct.unpack_from('<Q', cell, slots[flag])[0] == identities[source]
                        for source, flag in contributors.items()), 'Native corner slot mismatch')
            count += 1
        result.append(dict(query=query, target_slot=hex(target_slot), permutations=count))
    return target_words, result


def retire_controls():
    events = []
    errors = []

    @C.WINFUNCTYPE(None, C.c_void_p)
    def lock(pointer):
        events.append('lock')

    @C.WINFUNCTYPE(None, C.c_void_p)
    def unlock(pointer):
        events.append('unlock')

    @C.WINFUNCTYPE(None, C.c_void_p, C.c_void_p, C.c_void_p)
    def free_cell(pointer, size, owner):
        if pointer:
            errors.append('Unexpected nonempty native cell free')

    @C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)
    def retire(pointer, owner, unused):
        events.append(pointer)
        return pointer

    manager = C.create_string_buffer(0x210)
    landscape = C.create_string_buffer(0x40)
    parent = C.create_string_buffer(0x78)
    master = C.create_string_buffer(0x40)
    wrapper = C.create_string_buffer(16)
    grid = C.create_string_buffer(0x70)
    source = C.create_string_buffer(0x1a0)
    addresses = (C.c_uint64 * 1)(C.addressof(source))
    cells, aux = ((C.c_uint64 * 40000)() for _ in range(2))
    C.c_void_p.from_address(0x145fd9c30).value = C.addressof(manager)
    sampler.put(landscape, 0x20, '<Q', C.addressof(parent))
    sampler.put(parent, 0, '<Q', 0x144b3e0b8)
    sampler.put(parent, 0x18, '<Q', C.addressof(master))
    struct.pack_into('<II', master, 0x28, 100, 100)
    sampler.put(wrapper, 8, '<Q', C.addressof(parent))
    sampler.put(grid, 0, '<Q', 0x144b67f48)
    sampler.put(grid, 8, '<I', 2)
    struct.pack_into('<IIQQQQ', grid, 0x10, 1, 1, C.addressof(addresses),
                     C.addressof(cells), C.addressof(aux), C.addressof(wrapper))
    struct.pack_into('<IIII', grid, 0x48, 200, 200, 2, 2)
    struct.pack_into('<IIII', source, 0x18, 10, 10, 2, 2)
    for address, callback in ((0x1422cc3d0, lock), (0x1402c45a0, unlock), (0x1422c7560, free_cell),
                              (0x14365cdb0, free_cell), (0x140982b70, retire)):
        jump = b'\x48\xb8' + struct.pack('<Q', C.cast(callback, C.c_void_p).value) + b'\xff\xe0'
        C.memmove(address, jump, len(jump))

    def run():
        origin = sampler.callsite(0x1409870d0, 2)
        predicate = sampler.callsite(0x140987080, 2, C.c_uint64)
        update = sampler.callsite(0x140785610, 1, None)
        shift = sampler.callsite(0x140986da0, 3, None)
        rebase = (C.c_int32 * 2)(0, 0)

        def origin_now():
            result = (C.c_int32 * 2)()
            origin(grid, result)
            return tuple(result)

        def reset(y, source_y):
            events.clear()
            struct.pack_into('<ii', parent, 0x70, -50, y)
            sampler.put(source, 0x14, '<i', source_y)
            sampler.put(grid, 0x10, '<I', 1)
            addresses[0] = C.addressof(source)

        def step(dx):
            sampler.put(manager, 0x1a0, '<i', dx)
            update(landscape)
            shift(grid, (C.c_int32 * 2)(dx, 0), rebase)
            require(not errors, str(errors))
            return struct.unpack_from('<I', grid, 0x10)[0]

        for dx, remaining in ((2, 1), (256, 0)):
            reset(-50, 0)
            require(origin_now() == (-100, -100) and not (predicate(grid, source) & 255), 'Wrong initial Grid state')
            require(step(dx) == remaining and origin_now() == (dx - 100, -100)
                    and (predicate(grid, source) & 255) == 1 - remaining
                    and events.count(C.addressof(source)) == 1 - remaining, 'Native shift or retirement mismatch')
        reset(-62, -25)
        for ordinal in range(1, 39):
            require(step(3) == int(ordinal < 38) and origin_now() == (ordinal * 3 - 100, -112),
                    f'Wrong native retirement state at shift {ordinal}')
        require(events.count(C.addressof(source)) == 1, 'Wrong terminal retirement count')
        return {'small_shift_retained': True, 'large_shift_retired': True, 'three_cell_retirement_step': 38}

    keepalive = (master, wrapper, cells, aux, lock, unlock, free_cell, retire)
    return run, keepalive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--esm', type=Path, required=True)
    args = parser.parse_args()
    try:
        kernel, _ = sampler.host_preflight()
        exe, esm = sampler.regular(args.exe), sampler.regular(args.esm)
        drives = {exe.anchor, esm.anchor, Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives), 'Insufficient disk floor')
        pe = sampler.read_pinned(exe, sampler.EXE, 'Starfield EXE', keep=True)
        pages = sampler.pe_pages(pe, CODE, DATA)
        slots = placement_dispatch_slots(pe)
        sources, placement = inventory(esm)
        sampler.cpu_check(kernel)
        sampler.allocate_pages(kernel, pages)
        retire, keepalive = retire_controls()
        for page in pages:
            sampler.protect(kernel, page, 0x20 if page in CODE else 2)
        sampler.flush(kernel)
        words, corners = keys_and_corners(sources)
        retirement = retire()
    except (ValueError, KeyError, OSError, struct.error) as error:
        parser.exit(1, f'D5BJ source controls refused: {error}\n')
    print(json.dumps(dict(scope='Native key and corner controls and private Grid retirement predicate',
                          admitted_sources=len(sources), target_low_words=words, corners=corners,
                          placement_static=placement | {'matching_dispatch_slots': slots},
                          retirement=retirement), sort_keys=True))


if __name__ == '__main__':
    main()
