# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay activation arithmetic for two Save52 sites in a disposable host.

Reuses the pinned owned D5AQ private native setup (SOR-P-0002), stopping
before its case-specific driver. Replays coordinate helpers for saved sites and
ordinary raster sampling for two sources. Reads existing receipts and capture
JSON. The only writes are fresh ignored fixture artifacts and derived tables.
"""
import csv
import json
import math
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

import d5aq_startup as host
from d5at_audit import distribution
import d5at_grid as grid
import d5at_survey as s
from planet_world_key import qualified_grid


CASES = {
    'D2-81bf2a': '0005e0e3/0:29568:10944:0006ce56',
    'D2-844cc6': '0005e0ee/1:38112:960:0029d211',
}
HOST_SHA = '997a7bcd8a8f8833a72bfd9128b3fc4eb341cc94fcc24be24ca3ee6ae85a0e99'
GRID_RECEIPT = s.ROOT / '.local-work/d5at-grid03.json'
CAPTURE_LEDGER_SHA = 'f248c86e940accf2643f3f9d4a1778e0d9f84bc03a9d93ec8131e6cebd34eefa'
EXTRAS_SHA = '1ae573810de97eacb6cd3064b04702ae4f93526ddcc4096d7a53857127ffd88a'
WORLD_COMPONENTS_SHA = '177483381d46f4f2b7a1b1d54dc22de75bfb455a81abab74163612a53ec96ef6'
DISABLED = {'81b58f': ('833538', '817cf6'), '8483f2': ('85d721', '8172a4')}


def setup(output):
    source = Path(host.__file__)
    s.require(s.sha(source) == HOST_SHA, 'D5AQ native fixture source identity')
    code = source.read_text(encoding='utf-8')
    prefix, marker, _ = code.partition('    raster=C.create_string_buffer(0x30);')
    s.require(marker and code.count(marker) == 1, 'D5AQ fixture boundary changed')
    namespace = dict(__file__=str(source), __name__='d5at_private_native_host')
    exec(compile(prefix + '    return locals()\n', str(source), 'exec'), namespace)
    sys.argv = [str(source), '--out', str(output)]
    return namespace['main']()


def run(output):
    before = s.guard()
    for path in (Path(sys.executable), s.D5):
        s.require(s.sha(path) == s.PINNED[path], 'Interpreter or normalized corpus identity')
    prior = s.load(s.ROOT / '.local-work/d5at-rework-final-source-lock.json')['sha256']
    for path in (grid.SURVEY, GRID_RECEIPT):
        s.require(s.sha(path) == prior[path.relative_to(s.ROOT).as_posix()], 'Prior receipt identity')
    survey = s.load(grid.SURVEY)
    grid_rows = defaultdict(list)
    for row in s.load(GRID_RECEIPT)['results']:
        if 'rows' in row:
            grid_rows[row['outpost']].append(row)
    cases = {row['case']: row for row in survey['outposts'] if row.get('site_projection')}
    corpus = s.load(s.D5)['payload']
    manifest = s.LEASE / 'resource-save52/build-v1/manifest.json'
    s.require(s.sha(manifest) == s.PINNED[manifest], 'Map manifest identity')
    rasters = s.domains.maps(s.load(manifest), {cases[case]['body'] for case in CASES})
    ctx = setup(output)
    C, put = ctx['C'], ctx['put']
    manager, master = ctx['manager'], ctx['master']
    results, comparisons, census = [], [], []
    for case, row in cases.items():
        chart = row['request']['chart']
        anchor = row['request']['descriptor']
        packed = qualified_grid(int(row['descriptor_key'], 16))
        body = corpus['bodies'][row['body']]
        s.require((packed['tag'], packed['x'], packed['y'], packed['system_id'], packed['body_index']) ==
                  (chart, *anchor, body['system'], body['index']), 'Saved descriptor and body do not agree')
        fields = descriptor(chart, anchor)
        put(master, 0x58, '<I', packed['system_id'])
        put(master, 0x5c, '<I', packed['body_index'])
        install(put, manager, 0xc8, fields)
        site = row['site_projection'][0]
        saved_angles = (site['longitude_rad'], site['latitude_rad'])
        ctx['branch'](0x14374e650)
        angular = convert_angles(ctx, saved_angles)
        ctx['branch'](0x14374dda0)
        s.require(angular == convert_angles(ctx, saved_angles), 'Saved angular paths disagree')
        s.require(angular['quantized'] == descriptor(chart, (site['i'], site['j'])),
                  'Saved angular quantization differs')
        focus = [math.floor(C.c_float(C.c_float(value).value * C.c_float(0.01).value).value)
                 for value in row['request']['query'][:2]]
        same_descriptor = angular['snap'] == fields
        aligned = same_descriptor and angular['center'] == focus
        comparisons.append(dict(case=case, explicit_key=row['descriptor_key'], saved_descriptor=fields,
                                saved_angular_input=angular, focus=focus, aligned=aligned,
                                saved_parent_formid=dynamic_formid(row['parent'])))
        if same_descriptor:
            for source in grid_rows[case]:
                masks = {tuple(r['native']): r['mask'] for r in source['rows'] if r['grid'] == 'RETAINED'}
                for trigger, center in (('manager', angular['center']), ('focus', focus)):
                    if trigger == 'focus' and aligned:
                        continue
                    prepared = prepare(center, masks)
                    census.append(dict(case=case, source=source['source'],
                                       trigger='both' if aligned else trigger, **prepared))
        if case not in CASES:
            continue
        s.require(aligned, 'Priority case descriptor, manager center and focus do not align')
        source_id = CASES[case]
        raster, faces = C.create_string_buffer(0x30), C.create_string_buffer(0x60)
        put(raster, 0x18, '<Q', C.addressof(faces))
        arrays = [C.create_string_buffer(bytes(face['mask'])) for face in rasters[row['body']]['faces']]
        for n, array in enumerate(arrays):
            put(faces, n * 0x30, '<I', 256)
            put(faces, n * 0x30 + 4, '<I', 256)
            put(faces, n * 0x30 + 0x20, '<Q', C.addressof(array))
        expected = {tuple(sample['native']): sample['mask'] for source in census if source['source'] == source_id
                    for sample in source['samples']}
        s.require(len(expected) == 196, 'Priority source support changed')
        for label, address in (('fma', 0x14374e650), ('nonfused', 0x14374dda0)):
            ctx['branch'](address)
            fixed_angles = angles_at(ctx, (0, 0))
            fixed = convert_angles(ctx, fixed_angles)
            s.require(fixed['snap'] == fields and fixed['center'] == [0, 0], 'Anchor-zero preimage failed')
            sampled = {q: ctx['sample'](C.addressof(raster), C.addressof(angles_at(ctx, q))) for q in expected}
            s.require(sampled == expected, 'Native mask differs from fixed Grid receipt')
            requests = prepare(focus, sampled)
            results.append(dict(case=case, source_id=source_id, branch=label, explicit_key=row['descriptor_key'],
                                saved_descriptor=fields, anchor_preimage=fixed, saved_angular_input=angular,
                                expected_owner_pndt=row['body'], actual_world_discriminator=None,
                                actual_generation=None, actual_completed_keys=None,
                                samples=requests['samples'], bounds=requests['bounds'], counts=requests['counts']))
    s.require(len(comparisons) == 17 and len({row['source'] for row in census}) == 77,
              'Saved-site or installed-source coverage changed')
    s.write(output / 'activation.json', dict(rows=results, sites=comparisons, census=census,
                                             host_sha256=HOST_SHA, before=before, after=s.guard(),
                                             grid_sha256=s.sha(GRID_RECEIPT), capture_scope=capture_scope(),
                                             disabled_scope=disabled_scope()))
    with (output / 'activation-requests.csv').open('x', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(('outpost', 'source', 'trigger', 'x', 'y', 'mask', 'coordinate_word',
                         'layer_candidate', 'density_candidate'))
        for row in census:
            for sample in row['samples']:
                writer.writerow((row['case'], row['source'], row['trigger'], *sample['native'], sample['mask'],
                                 sample['coordinate_word'], sample['layer_candidate'], sample['density_candidate']))
    write_distributions(output, census)
    print([(r['case'], r['branch'], r['saved_angular_input'], r['counts']) for r in results])


def dynamic_formid(token):
    word = int(token, 16)
    s.require(word >> 22 == 2, 'Expected saved dynamic parent FormRef')
    return f'{0xff000000 | (word & 0x3fffff):08x}'


def capture_scope():
    root = s.ROOT / '.local-work/d5as'
    ledger = root / 'attempts-02.json'
    s.require(s.sha(ledger) == CAPTURE_LEDGER_SHA, 'D5AS capture ledger identity')
    files = {row['name']: row for row in s.load(ledger)['files'] if row['name'].endswith('.snapshot.json')}
    actual = {path.name: path for path in (root / 'capture').glob('*.snapshot.json')}
    s.require(actual.keys() == files.keys() and len(actual) == 31, 'D5AS published snapshot roster')
    owners = Counter()
    for name, path in actual.items():
        pin = files[name]
        s.require(path.stat().st_size == pin['bytes'] and s.sha(path) == pin['sha256'], 'Snapshot identity')
        capture = s.load(path)
        context = capture['owner_context']
        before = context['before']
        if before['complete'] and before == context['after']:
            body = int.from_bytes(bytes.fromhex(before['owner_formid_word']), 'little')
            owners[f'{body:08x}'] += 1
        else:
            owners['UNBOUND'] += 1
    s.require(owners == {'0005e0de': 31}, 'D5AS owner scope changed')
    return dict(ledger_sha256=CAPTURE_LEDGER_SHA, snapshot_owners=owners)


def disabled_scope():
    """Check the closed historical extra lists and typed saved world component."""
    extras = s.ROOT / '.local-work/workshop-population-rework/specialist/historical-targetcensus05.jsonl'
    worlds = s.ROOT / '.local-work/static-exhaustion/saved-context-04/saved-world-components.csv'
    s.require(s.sha(extras) == EXTRAS_SHA and s.sha(worlds) == WORLD_COMPONENTS_SHA, 'Disabled evidence identity')
    identities = {f'DYNAMIC:{dynamic_formid(token)}': token for token in DISABLED}
    scoped = {}
    with extras.open(encoding='utf-8') as stream:
        for line in stream:
            sample = json.loads(line)
            if sample['inventory_id'] not in ('HIST-0210', 'HIST-0267'):
                continue
            s.require(sample['status'] == 'QUALIFIED_TYPED_R3_CLOSED', 'Historical typed framing')
            for record in sample['target_rows']:
                if record['identity'] not in identities:
                    continue
                extra = record['extras']
                s.require(extra['following_extras'] == 'CLOSED' and len(extra['types']) == extra['extra_count']
                          and 0x81 not in extra['types'], 'ExtraLocation route requires review')
                scoped[sample['inventory_id'], identities[record['identity']]] = extra['types']
    s.require(len(scoped) == 4, 'Expected both disabled targets in both typed samples')
    with worlds.open(encoding='utf-8', newline='') as stream:
        components = {row['world']: row for row in csv.DictReader(stream) if row['sample'] == 'HIST-0267'}
    results = []
    for token, (parent, secondary) in DISABLED.items():
        row = components[parent]
        s.require(row['linked'] == '000000' and row['secondary'] == secondary and row['flags'] == '1',
                  'Unexpected saved world component')
        results.append(dict(token=token, world=row, save52_extra_types=scoped['HIST-0267', token],
                            quicksave_extra_types=scoped['HIST-0210', token]))
    return results


def write_distributions(output, census):
    with (output / 'activation-distributions.csv').open('x', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(('family_rank', 'family', 'outpost', 'source', 'trigger', 'window_low', 'window_high',
                         'retained_grid_pairs', 'requests', 'mask_counts', 'mask_shares', 'classes',
                         'largest_share', 'effective_classes', 'qualification', 'actual_completion'))
        for family in ('density', 'layer'):
            rows = []
            for row in census:
                samples = [sample for sample in row['samples'] if sample[f'{family}_candidate']]
                stats = distribution(samples)
                rows.append((row, stats, len(samples)))
            rows.sort(key=lambda item: (not item[2], len(item[1]['counts']) != 2,
                                        len(item[1]['counts']) < 2, item[1]['largest_share'] or 0,
                                        -item[1]['effective_classes'], item[0]['case'], item[0]['source'],
                                        item[0]['trigger']))
            for rank, (row, stats, count) in enumerate(rows, 1):
                counts = {f'0x{mask:x}': n for mask, n in stats['counts'].items()}
                shares = {mask: n / count for mask, n in counts.items()}
                writer.writerow((rank if count else 'UNRANKED', family, row['case'], row['source'], row['trigger'],
                                 json.dumps(row['bounds']['low']), json.dumps(row['bounds']['high']),
                                 len(row['samples']), count, json.dumps(counts), json.dumps(shares), len(counts),
                                 stats['largest_share'], stats['effective_classes'] if count else 'UNKNOWN',
                                 'CONDITIONAL_SAVED_ANGLE_PREWARM', 'UNKNOWN'))


def prepare(center, masks):
    # Native signed IDIV first subtracts the full chunk for negative values.
    chunks = [value // 8 if value >= 0 else -((-value + 8) // 8) for value in center]
    low = [(chunk - 2) * 8 for chunk in chunks]
    high = [(chunk + 3) * 8 - 1 for chunk in chunks]
    roots = set(product(*(range(lo, hi + 1) for lo, hi in zip(low, high))))
    density = {(x + dx, y + dy) for x, y in roots for dx, dy in grid.OFFSETS}
    # Independent closed-form union of the four translated root rectangles.
    oracle = {(x, y) for x, y in product(range(low[0] - 1, high[0] + 2), range(low[1], high[1] + 2))
              if y != low[1] or x < high[0]}
    s.require(density == oracle and len(roots) == 1600 and len(density) == 1720,
              'Cold rectangular key oracle disagrees')
    samples = []
    for q, mask in sorted(masks.items()):
        x, y = q
        # Native 12-byte key is [world FormID, database kind, packed signed Int2].
        coordinate_word = (x & 0xffff) | ((y & 0xffff) << 16)
        samples.append(dict(native=q, mask=mask, coordinate_word=f'0x{coordinate_word:08x}',
                            layer_candidate=q in roots, density_candidate=q in density))
    s.require(len({r['coordinate_word'] for r in samples}) == len(samples), 'Coordinate-word collision')
    return dict(bounds=dict(low=low, high=high), samples=samples,
                counts=dict(support=Counter(masks.values()),
                            layer=Counter(masks[q] for q in roots & masks.keys()),
                            density=Counter(masks[q] for q in density & masks.keys())))


def descriptor(chart, anchor):
    x, y = anchor
    return [chart, x // 192, y // 192, x % 192 // 12, y % 192 // 12, x % 12, y % 12]


def install(put, buffer, base, fields):
    for offset, value in zip((0, 4, 8, 20, 24, 36, 40), fields):
        put(buffer, base + offset, '<i', value)


def angles_at(ctx, query):
    C = ctx['C']
    manager = C.addressof(ctx['manager'])
    square = C.create_string_buffer(24)
    angles = (C.c_double * 2)()
    ctx['convert'](manager, C.addressof(square), manager + 0xc8, C.addressof((C.c_int32 * 2)(*query)))
    ctx['project'](C.addressof(angles), C.addressof(square))
    return angles


def convert_angles(ctx, angles):
    C = ctx['C']
    pair = (C.c_double * 2)(*angles)
    quantized, snapped = C.create_string_buffer(48), C.create_string_buffer(48)
    center = (C.c_int32 * 2)()
    ctx['quantize'](C.addressof(quantized), C.addressof(pair), 256)
    ctx['snap'](C.addressof(ctx['master']), C.addressof(snapped), C.addressof(pair))
    ctx['center'](C.addressof(ctx['manager']), C.addressof(center), C.addressof(pair))

    def words(buffer):
        return [buffer.raw[0], *(C.c_int32.from_buffer(buffer, offset).value for offset in (4, 8, 20, 24, 36, 40))]

    return dict(angles=list(pair), quantized=words(quantized), snap=words(snapped), center=list(center))


if __name__ == '__main__':
    output = Path(sys.argv[1]).absolute()
    s.require(output.is_relative_to(s.ROOT / '.local-work/d5aq') and output == output.resolve()
              and not output.exists(), 'Fresh local D5AQ fixture output required')
    run(output)
