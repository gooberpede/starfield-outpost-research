# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute the fixed three-resource ordinary stage in an owned native host.

SOR-P-0002 lineage: D5S native_probe.py/native_cell.py and RG1 geometry.py.
Reads authenticated D5S methods, function metadata, numerical inputs and pinned
installed PE. Maps explicit native pages in this disposable Python process.
Uses supplied coordinate keys, resource collections and successful allocators;
no generator/scheduler/game process, save, database or configuration operations.
Writes fresh ignored D5AF receipts only. Requires installed Windows CPython.
Stop on disk-floor, identity, callback, ABI or independent-oracle failure.
Preserve failed outputs; process exit releases only its own mapped buffers.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / '.local-work/d5s'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def native(out):
    sys.path.insert(0, str(out))
    probe = (out / 'native_probe.py').read_text().split('receipt=json.loads')[0]
    additions = ['14079a330', '1404a7f90', '142bf4850', '1407af1a0', '14079b020']
    additions += json.loads((out / 'extra-entries.json').read_bytes())
    probe = probe.replace("'1407aedd0']", "'1407aedd0'," +
                          ','.join(repr(v) for v in additions) + ']')
    ns = {'__file__': __file__, '__name__': 'd5af_native_fixture'}
    exec(compile(probe, 'owned-D5S-native-probe-prefix', 'exec'), ns)
    C, struct, k = ns['C'], ns['struct'], ns['k']
    page, write, code, buffers = (ns[v] for v in ('page', 'write', 'code', 'buffers'))
    page(0x144d59000)
    # The verified native thunk jumps through this atan2f import slot.
    import_slot = 0x143a40600
    if ns['data'][ns['offset'](0x1434ca936):ns['offset'](0x1434ca936)+6] != bytes.fromhex('ff25c45c5700'):
        raise ValueError('atan2f thunk bytes differ')
    atan2f = ns['crt'].atan2f
    atan2f.argtypes = [C.c_float, C.c_float]
    atan2f.restype = C.c_float
    write(import_slot, struct.pack('<Q', C.cast(atan2f, C.c_void_p).value))
    fault = []

    @C.WINFUNCTYPE(C.c_long, C.c_void_p)
    def fault_info(ep):
        record, context_ptr = (C.c_void_p * 2).from_address(ep)
        row = dict(code=hex(C.c_uint32.from_address(record).value),
                   rip=hex(C.c_uint64.from_address(context_ptr+0xf8).value))
        print('FAULT', json.dumps(row), flush=True)
        return 0

    k.AddVectoredExceptionHandler.argtypes = [C.c_ulong, C.c_void_p]
    k.AddVectoredExceptionHandler.restype = C.c_void_p
    k.AddVectoredExceptionHandler(1, C.cast(fault_info, C.c_void_p))
    receipt = json.loads((out / 'geometry.json').read_bytes())
    req = receipt['results'][1]['request']
    sys.path[:0] = [str(ROOT / 'research' / p) for p in
                    ('resource-slot-provenance', 'resource-geometry', 'resource-spatial')]
    import predictor_d4e
    corpus = ROOT / '.local-work/resources-evidence-consolidation/d5r-input-lease01/.local-work/resource-feynman-d5/build04/normalized.json'
    if sha(corpus) != receipt['summary']['corpus']:
        raise ValueError('Effective definition corpus drift')
    context = predictor_d4e.validate(json.loads(corpus.read_bytes()))
    rarities = {r['id']: r['rarity'] for r in
                context['bodies']['0005e0de']['biomes']['00145440']['resources']}
    current = [1, 1]
    manager = C.create_string_buffer(0x100)
    C.c_uint32.from_buffer(manager, 0x80).value = req['owner_key']
    write(0x145fd9c30, struct.pack('<Q', C.addressof(manager)))
    write(0x145e60398, struct.pack('<I', 2))
    write(0x145e603c0, b'\0')
    write(0x145921e84, struct.pack('<I', 0xffffffff))
    output = C.create_string_buffer(48)
    slots = C.create_string_buffer(24 * 3)
    collections = {}
    for i, resource in enumerate(req['ordered_resources']):
        key = int(resource['resource'], 16)
        collection = C.create_string_buffer(24)
        collections[key] = collection
        C.c_uint32.from_buffer(collection).value = 1
        C.c_uint32.from_buffer(slots, 24*i).value = key
        C.c_void_p.from_buffer(slots, 24*i+8).value = C.addressof(collection)
        C.c_uint32.from_buffer(slots, 24*i+16).value = 1
    C.c_void_p.from_buffer(output, 24).value = C.addressof(slots)
    C.c_uint64.from_buffer(output, 32).value = 3
    errors, key_calls = [], []

    @C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)
    def convert(m, dest, xy):
        got = list((C.c_int32*2).from_address(xy))
        if got != [req['origin'][i]+current[i] for i in range(2)]:
            errors.append(['conversion-operand', got])
        packed = req['packed_keys'][f'{current[0]},{current[1]}']
        C.c_uint64.from_address(dest).value = packed
        key_calls.append([current[:], packed])
        return dest

    @C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p)
    def get_collection(owner, key_pointer, dest):
        key = C.c_uint32.from_address(key_pointer).value
        if key not in collections:
            errors.append(['unknown-resource', key])
            C.c_void_p.from_address(dest).value = 0
            return 0
        collection = collections[key]
        C.c_uint32.from_buffer(collection).value += 1
        C.c_void_p.from_address(dest).value = C.addressof(collection)
        return 1

    @C.WINFUNCTYPE(None, C.c_void_p)
    def no_free(pointer):
        pass

    callbacks = [convert, get_collection, no_free, fault_info]

    def stub(va, callback):
        address = page(va)
        old = C.c_ulong()
        assert k.VirtualProtect(address, 4096, 4, C.byref(old))
        write(va, b'\x48\xb8' + struct.pack('<Q', C.cast(callback, C.c_void_p).value)+b'\xff\xe0')
        assert k.VirtualProtect(address, 4096, 0x20, C.byref(old))
        code.add(address)

    stub(0x14078d7b0, convert)
    stub(0x1407a97c0, get_collection)
    write(0x143a40470, struct.pack('<Q', C.cast(no_free, C.c_void_p).value))
    origin = (C.c_int32*2)(*req['origin'])
    clip = (C.c_float*8)(*req['clip_center'], 0, *req['clip_half'], 0)
    cell = (C.c_int32*4)()
    invoke = C.WINFUNCTYPE(C.c_uint64, C.c_void_p, C.c_void_p, C.c_void_p,
                          C.c_void_p, C.c_void_p, C.c_float, C.c_void_p)(0x14079a330)
    runs = []
    body = context['bodies']['0005e0de']
    for label, model_index, original_query in [('mask0', 0, [4, -1]),
                                             ('mask3', 1, [4, 1]),
                                             ('mask3-independent-repeat', 1, [5, 0])]:
        face = [37536+original_query[0], 20928+original_query[1]]
        raster_byte = predictor_d4e.tile_at(body, 0, *face)[3]
        expected_mask = 0 if model_index == 0 else 3
        assert raster_byte & 15 == expected_mask
        for collection in collections.values():
            C.memset(C.addressof(collection)+8, 0, 16)
        model = receipt['results'][model_index]
        for resource in model['request']['ordered_resources']:
            key = int(resource['resource'], 16)
            ires = C.create_string_buffer(0x118)
            C.c_uint32.from_buffer(ires, 0x28).value = key
            rarity = rarities[resource['resource']]
            C.c_uint8.from_buffer(ires, 0x110).value = rarity
            dnam = C.create_string_buffer(0x238)
            C.memmove(C.addressof(dnam)+(rarity+7)*40, struct.pack('<10f', *resource['block']), 40)
            for x in range(1, 13):
                for y in range(1, 13):
                    current[:] = [x, y]
                    cell[0], cell[1] = x, y
                    invoke(C.addressof(ires), C.addressof(cell), C.addressof(origin),
                           C.addressof(clip), C.addressof(dnam), resource['weight'], C.addressof(output))
                    if errors:
                        raise AssertionError(errors)
        population = []
        for key, collection in collections.items():
            count = C.c_uint32.from_buffer(collection, 8).value
            address = C.c_void_p.from_buffer(collection, 16).value
            regions = []
            for i in range(count):
                at = address+i*48
                n = C.c_uint32.from_address(at+24).value
                points = C.c_void_p.from_address(at+32).value
                assert n and points
                regions.append(dict(header=C.string_at(at, 24).hex(), count=n,
                                    points=C.string_at(points, n*16).hex()))
            population.append(dict(resource=f'{key:08x}', regions=regions))
        oracle = []
        for item in population:
            expected = [r for r in model['full']['regions'] if r['resource'] == item['resource']]
            expected_words = [dict(points=b''.join(struct.pack('<4f', *point) for point in r['points']).hex(),
                                   bound=struct.pack('<4f', *r['native_bound']).hex()) for r in expected]
            actual_words = [dict(points=r['points'], bound=r['header'][:32]) for r in item['regions']]
            oracle.append(dict(resource=item['resource'], native_count=len(actual_words),
                               model_count=len(expected_words), exact_points_bounds=actual_words == expected_words))
        # The planar oracle is separate owned arithmetic, not native output replay.
        # This asserts only the tested finite operands, not arbitrary boundary math.
        assert all(row['exact_points_bounds'] for row in oracle), oracle
        runs.append(dict(label=label, original_query=original_query,
                         body_face_query=face, supplied_query_conversion=True,
                         raster_byte=raster_byte, low_mask=expected_mask,
                         population=population, planar_model_comparison=oracle))
        (out / 'progress.json').write_text(json.dumps(runs, indent=2)+'\n', encoding='utf8', newline='\n')
    assert runs[1]['population'] == runs[2]['population']
    assert runs[0]['population'] != runs[1]['population']
    result = dict(scope='Three fixed ordinary resource stages, 144 native cells each; supplied keys/collections/allocators, no full generator or retail',
                  runs=runs, native_pins=ns['pins'], errors=errors,
                  model_input_sha256=sha(out / 'geometry.json'), method_sha256=sha(__file__),
                  rarity_by_resource=rarities, corpus_sha256=sha(corpus),
                  crt_sha256=sha('C:/Windows/System32/ucrtbase.dll'),
                  bound_import=dict(static_slot=hex(import_slot), name='atan2f'),
                  key_calls=key_calls, free=ns['free']())
    (out / 'control.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(counts=[[len(r['regions']) for r in run['population']] for run in runs], repeated_equal=True)))


def main():
    if not __debug__ or sys.flags.optimize or os.name != 'nt' or sys.maxsize <= 2**32:
        raise RuntimeError('Use unoptimized installed x64 Windows CPython with -E -B')
    if sys.argv[1] == '--native':
        out = Path(sys.argv[2]).resolve()
        if not out.is_dir() or not out.is_relative_to(ROOT / '.local-work/d5af'):
            raise ValueError('Existing D5AF child-process directory required')
        return native(out)
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5af'):
        raise ValueError('Fresh D5AF directory required')
    for drive in ('C:/', 'D:/'):
        if shutil.disk_usage(drive).free < 40_000_000_000:
            raise RuntimeError('Disk floor')
    out.mkdir(parents=True)
    ledger = ROOT / 'docs/experiments/resource-retained-population/d5s-sources.csv'
    with ledger.open(encoding='utf8') as stream:
        rows = list(csv.DictReader(stream))
    for name in ('start.py', 'native_probe.py', 'initial.json', 'geometry.json'):
        source = OLD / name
        expected = next(row['sha256'] for row in rows
                        if Path(row['path']).resolve() == source.resolve())
        if sha(source) != expected:
            raise ValueError('D5S source drift: ' + name)
    for name in ('start.py', 'native_probe.py', 'initial.json', 'geometry.json'):
        shutil.copyfile(OLD / name, out / name)
    shutil.copytree(OLD / 'functions', out / 'functions')
    extra = Path(sys.argv[2])
    # Extra native metadata must be exported from the verified disposable copy.
    for path in extra.glob('*.txt'):
        shutil.copyfile(path, out / 'functions' / path.name)
    (out / 'extra-entries.json').write_text(json.dumps([p.stem for p in extra.glob('*.txt')])+'\n', encoding='utf8', newline='\n')
    inputs = {str(p): sha(p) for p in [OLD / n for n in ('start.py', 'native_probe.py', 'initial.json', 'geometry.json')]}
    env = dict(os.environ, D5S_OUTPUT=str(out))
    command = [sys.executable, '-E', '-B', str(Path(__file__).resolve()), '--native', str(out)]
    result = subprocess.run(command, env=env, cwd=ROOT, capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    (out / 'stdout.log').write_bytes(result.stdout)
    (out / 'stderr.log').write_bytes(result.stderr)
    receipt = dict(exit=result.returncode, command=command, inputs=inputs,
                   method_sha256=sha(__file__), extra_metadata={str(p): sha(p) for p in extra.glob('*.txt')})
    (out / 'execution.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8', newline='\n')
    if result.returncode or b'Exception ignored' in result.stderr:
        raise RuntimeError('Native control failed; retain logs')
    print(result.stdout.decode('utf8'))


if __name__ == '__main__':
    main()
