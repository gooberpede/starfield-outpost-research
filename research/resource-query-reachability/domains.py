# SPDX-License-Identifier: GPL-3.0-or-later
"""D5H finite builder-stage domains, independent of the base-selector inverse.

Reads authenticated restored D5/D4E corpora and D5G roster, plus installed BA2.
Writes new CSVs and one exclusive ignored receipt; no generator or game-native calls.
Python stdlib only. Bounds describe 1409832e0/140985900/140985c50 insert attempts,
before clipping, occupied-slot rejection, completion, demand and first-miss gates.
They are deliberately not classified as actual admitted queries.
"""
import csv
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib
from roundtrip import projected

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-query-reachability'
OLD = ROOT / 'docs/experiments/resource-predictability-contrast'
LEASE = ROOT / '.local-work/resources-evidence-consolidation/d5h-input-lease03'
ARCHIVE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield - PlanetData.ba2')


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load(original, digest):
    path = LEASE / original
    assert pin(path) == digest, original
    value = json.loads(path.read_text(encoding='utf8'))
    if 'payload' in value:
        canonical = json.dumps(value['payload'], sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        assert hashlib.sha256(canonical).hexdigest() == value['sha256']
        return value['payload']
    return value


def attempted_cells(width, height, padding):
    """Transcribe native fill, signed edge offsets and four corner cases."""
    cells = {(x, y) for x in range(width) for y in range(height)}
    for i in range(1, padding + 1):
        for x in range(width):
            cells.add((x, height - 1 + i))
            cells.add((x, -padding - 1 + i))
        for y in range(height):
            cells.add((-padding - 1 + i, y))
            cells.add((width - 1 + i, y))
        for j in range(padding):
            for x in (-padding - 1 + i, width - 1 + i):
                cells.add((x, height + j))
                cells.add((x, j - padding))
    return cells


def maps(manifest, bodies):
    """Adapt D5G's bounded BA2 member read; verify each original member hash."""
    assert pin(ARCHIVE) == '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'
    result = {}
    with ARCHIVE.open('rb') as stream:
        magic, version, kind, count, offset = struct.unpack('<4sI4sIQ', stream.read(24))
        assert (magic, version, kind) == (b'BTDX', 2, b'GNRL') and count <= 10000
        stream.seek(32)
        entries = [struct.unpack('<I4sIIQIII', stream.read(36)) for _ in range(count)]
        stream.seek(offset)
        names = [stream.read(int.from_bytes(stream.read(2), 'little')).decode() for _ in range(count)]
        for body in bodies:
            member = manifest['members'][body]
            assert names.count(member['name']) == 1
            at, packed, size = entries[names.index(member['name'])][4:7]
            assert size == member['bytes'] and size <= 2000000
            assert at + (packed or size) <= ARCHIVE.stat().st_size
            stream.seek(at)
            data = stream.read(packed or size)
            if packed:
                decoder = zlib.decompressobj()
                data = decoder.decompress(data, size + 1)
                assert decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
            assert len(data) == size and hashlib.sha256(data).hexdigest() == member['sha256']
            sys.path.insert(0, str(ROOT / 'research/resource-geometry'))
            from context import read_map
            result[body] = read_map(data)
    return result


def table(path, rows):
    with path.open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    c = load('.local-work/resource-feynman-d5/build04/normalized.json',
             '97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9')
    cc = load('.local-work/resource-slot-provenance/build-controls02/normalized.json',
              '8162cded8e6cb4117352703062242c42110738090383aba541c278210b6e53da')
    manifest = load('.local-work/resource-save52/build-v1/manifest.json',
                    '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de')
    source_rows = list(csv.DictReader((OLD / 'source-matrix.csv').open(encoding='utf8')))
    prior = {(r['case'], r['source_key']): r for r in csv.DictReader((OLD / 'query-domains.csv').open(encoding='utf8'))}
    assert len(source_rows) == len(prior) == 25
    raster = maps(manifest, {r['body'][2:] for r in source_rows})
    arithmetic = json.loads((ROOT / '.local-work/resource-query-reachability/native-bytes09.json').read_text())
    assert all(v['dll'] == 'api-ms-win-crt-math-l1-1-0.dll' for v in arithmetic['scalar_math_imports'].values())
    crt = ctypes.CDLL('api-ms-win-crt-math-l1-1-0.dll')
    crt.cos.argtypes = [ctypes.c_double]
    crt.cos.restype = ctypes.c_double
    crt.atan2.argtypes = [ctypes.c_double, ctypes.c_double]
    crt.atan2.restype = ctypes.c_double
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetModuleFileNameW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint32]
    kernel.GetModuleFileNameW.restype = ctypes.c_uint32
    host_name = ctypes.create_unicode_buffer(32768)
    assert 0 < kernel.GetModuleFileNameW(crt._handle, host_name, len(host_name)) < len(host_name)
    host_path = Path(host_name.value)
    host = ctypes.CDLL(str(host_path))
    host._controlfp_s.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32]
    host._controlfp_s.restype = ctypes.c_int
    control = ctypes.c_uint32()
    assert host._controlfp_s(ctypes.byref(control), 0, 0) == 0 and control.value & 0x300 == 0
    scalar_host = dict(path=str(host_path), sha256=pin(host_path), control_word=hex(control.value),
                       qualification='Current offline CRT host and round-to-nearest; historical host unobserved')
    rows, examples, receipts = [], [], []
    for source in source_rows:
        case, key = source['case'], source['source_key']
        old = prior[case, key]
        chart, ax, ay, block = key.split(':')
        chart, ax, ay = int(chart), int(ax), int(ay)
        corpus = cc if case in ('original-V', 'Carinae') else c
        body = source['body'][2:]
        raw = corpus['source_blocks'][block]
        padding = 2
        width, height = [v - 2 * padding for v in raw]
        assert width > 0 and height > 0
        cells = attempted_cells(width, height, padding)
        closed_form = {(x, y) for x in range(-padding, width + padding)
                       for y in range(-padding, height + padding)}
        assert cells == closed_form
        face = raster[body]['faces'][chart]

        def mask(x, y):
            assert 0 <= x < 49152 and 0 <= y < 49152
            return face['mask'][(255 - y // 192) * 256 + x // 192] & 15

        sampled = {mask(ax + x, ay + y) for x, y in cells}
        transformed = [projected(chart, ax+x, ay+y) for x, y in sorted(cells)]
        transformed_masks = {raster[body]['faces'][tag]['mask'][row * 256 + column] & 15
                             for tag, column, row, _ in transformed}
        assert transformed_masks == sampled
        native_branches = {}
        for fused in (False, True):
            values = [projected(chart, ax+x, ay+y, constants=arithmetic['sine_constants'],
                                fused=fused, scalar_math=crt) for x, y in sorted(cells)]
            values_masks = {raster[body]['faces'][tag]['mask'][row*256+column] & 15
                            for tag, column, row, _ in values}
            assert values_masks == sampled
            native_branches[str(fused)] = dict(masks=sorted(values_masks),
                max_error_fine_cells=max(value[3] for value in values))
        max_error = max(item[3] for item in transformed)
        resources = [r for r in corpus['bodies'][body]['biomes'][source['biome'][2:]]['resources']
                     if r.get('branch') != 'special']
        globe = sorted({v & 15 for f in raster[body]['faces'] for v in f['mask']})
        vectors = {str(m): [(0.0 if r['rarity'] == 6 else corpus['settings'][r['rarity']])
                           if m == 8 or m < r['rarity'] else 1.0 for r in resources] for m in globe}
        assert set(map(str, sampled)) <= set(vectors)
        row = dict(case=case, source_key=key, body=source['body'], sfpt=source['sfpt'],
            biome=source['biome'], root=source['root'], effective_rsgd=source['effective_rsgd'],
            candidate_order=';'.join(r['id'] for r in resources),
            nominal=old['nominal_half_open_fine_xy'], nominal_masks=old['nominal_masks'],
            inverse_cells=old['inverse_base_selector_cells'], inverse_masks=old['inverse_base_selector_masks'],
            conservative=old['conservative_half_open_fine_xy'], conservative_masks=old['conservative_masks'],
            insertion_attempt_half_open=f'[{ax-2},{ax+width+2})x[{ay-2},{ay+height+2})',
            insertion_attempt_cells=len(cells), pre_projection_masks=';'.join(map(str, sorted(sampled))),
            modeled_roundtrip_masks=';'.join(map(str, sorted(transformed_masks))),
            modeled_max_error_fine_cells=max_error,
            native_arithmetic_branches=json.dumps(native_branches, separators=(',', ':')),
            padding_premise=padding, ordinary_vectors=json.dumps(vectors, separators=(',', ':')),
            first_miss_mask_lower='EMPTY_UNPROVED', installed_raster_mask_upper=';'.join(map(str, globe)),
            classification='PROVED INVARIANT' if len(sampled) == 1 else 'UNRESOLVED',
            qualification='Ordinary base-index pad2; coherent interior source/manager frame; current pinned scalar CRT; RN; either SIMD branch; fixed other generation inputs',
            missing_operands='Effective completed grid slots and frame; original query transform; demand and visited/map state within one source lifetime',
            native_controls=source['native_control_captures'],
            zero_intersection_preserved=source['positive_area_paths'],
            domain_status='Insertion-attempt relaxation; not an admitted first-miss domain')
        rows.append(row)
        witnesses = []
        for m in sorted(sampled):
            x, y = min((x, y) for x, y in cells if mask(ax + x, ay + y) == m)
            outside = not (0 <= x < width and 0 <= y < height)
            witnesses.append(dict(mask=m, offset=[x, y], geographic_pre_projection=[ax+x, ay+y]))
            examples.append(dict(case=case, source_key=key, geographic_pre_projection=f'{ax+x};{ay+y}',
                source_relative_query=f'{x};{y}', outside_nominal=outside, raster_mask=m,
                ordinary_vector=json.dumps(vectors[str(m)], separators=(',', ':')),
                insertion_attempt=True, actual_slot_occupancy='UNKNOWN', actual_first_miss='NOT_PROVED',
                verdict='Candidate only; excluded as an admitted counterexample'))
        receipts.append(dict(case=case, source_key=key, source_dimensions=raw,
                             attempt_cells=sorted(cells), mask_witnesses=witnesses,
                             native_arithmetic_branches=native_branches))
    table(DOC / 'source-domains.csv', rows)
    table(DOC / 'counterexamples.csv', examples)
    with output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(dict(rows=receipts, geometry_rerun=False, actual_first_miss_witnesses=0,
                       scalar_host=scalar_host,
                       classified_unresolved=sum(r['classification']=='UNRESOLVED' for r in rows)), stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(sources=len(rows), candidate_examples=len(examples),
        mixed_attempt_domains=sum(';' in r['pre_projection_masks'] for r in rows),
        classifications={k:sum(r['classification']==k for r in rows) for k in ('PROVED INVARIANT','UNRESOLVED')}, actual_first_miss_witnesses=0)))


if __name__ == '__main__':
    main()
