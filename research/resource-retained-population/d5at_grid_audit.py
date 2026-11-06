# SPDX-License-Identifier: GPL-3.0-or-later
"""Check Grid receipt geometry and request/mask joins, then write summary CSV."""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from collections import Counter
import csv
from itertools import product
import json
from pathlib import Path
import struct

import d5at_grid as grid
import d5at_survey as s
from inspect_outpost_definitions import esm_records


def verify_installed(data, corpus):
    """Compare the selected normalized patterns to serialized ESM fields."""
    patterns = set()
    for row in data['results']:
        body, geographic = row['source'].split('/')
        chart, x, y, _ = geographic.split(':')
        tiles = {f'{chart}:{int(x)//192}:{int(y)//192}', *row.get('tiles', ())}
        patterns.update(corpus['bodies'][body]['tiles'][tile][0] for tile in tiles)
    blocks = {key for pattern in patterns for key, flags in corpus['patterns'][pattern] if flags & 8}
    esm = s.INSTALL / 'Data/Starfield.esm'
    s.require(s.sha(esm) == s.PINNED[esm], 'Installed ESM identity')
    found = set()
    for header, fields in esm_records(esm, {b'SFPT', b'SFBK'}):
        key = f"{header['formid']:08x}"
        if header['type'] == 'SFPT' and key in patterns:
            ids = struct.unpack('<256I', fields[b'FNAM'])
            flags = fields[b'GNAM']
            transposed = [[f'{ids[y*16+x]:08x}', flags[y*16+x]] for x, y in product(range(16), repeat=2)]
            s.require(len(flags) == 256 and transposed == corpus['patterns'][key], 'Serialized SFPT differs')
            found.add(key)
        elif header['type'] == 'SFBK' and key in blocks:
            size = list(struct.unpack('<2I', fields[b'DNAM']))
            s.require(size == corpus['source_blocks'][key], 'Serialized SFBK differs')
            found.add(key)
    s.require(found == patterns | blocks and s.sha(esm) == s.PINNED[esm], 'Installed record closure differs')
    return len(patterns), len(blocks)


def contributors(corpus, body, chart, source):
    """Build an independent coordinate index over the complete contributing tiles."""
    ax, ay = source['anchor']
    width, height = source['width'], source['height']
    xmax = max(w for w, _ in corpus['source_blocks'].values())
    ymax = max(h for _, h in corpus['source_blocks'].values())
    txs = range((ax - xmax + 1) // 192, (ax + width + 3) // 192 + 1)
    tys = range((ay - ymax + 1) // 192, (ay + height + 3) // 192 + 1)
    tiles = [f'{chart}:{tx}:{ty}' for tx, ty in product(txs, tys)]
    cells = {(x, y): [] for x, y in product(range(-2, width + 2), range(-2, height + 2))}
    for tile in tiles:
        _, tx, ty = map(int, tile.split(':'))
        sfpt, orientation, *_ = corpus['bodies'][body]['tiles'][tile]
        s.require(orientation == 8, 'Auditor found unqualified orientation')
        for index, (block, flags) in enumerate(corpus['patterns'][sfpt]):
            if not flags & 8:
                continue
            bx, by = 192 * tx + 12 * (index // 16), 192 * ty + 12 * (index % 16)
            raw_w, raw_h = corpus['source_blocks'][block]
            for x, y in product(range(max(ax - 2, bx - 2), min(ax + width + 2, bx + raw_w - 2)),
                                range(max(ay - 2, by - 2), min(ay + height + 2, by + raw_h - 2))):
                x_side = -1 if x < bx else int(x >= bx + raw_w - 4)
                y_side = -1 if y < by else int(y >= by + raw_h - 4)
                cells[x - ax, y - ay].append((x_side, y_side, f'{body}/{chart}:{bx}:{by}:{block}'))
    return tiles, cells


def emission(contributors):
    corner = any(x and y for x, y, _ in contributors)
    slots = {}
    for x, y, key in contributors:
        if corner:
            # A single nonzero axis spans the two quadrants on that side.
            choices = product((x,) if x else (-1, 1), (y,) if y else (-1, 1))
            indexes = [int(u < 0) + 2 * int(v > 0) for u, v in choices]
        else:
            indexes = [int(x < 0 or y > 0)]
        for index in indexes:
            s.require(index not in slots, 'Auditor found competing slot')
            slots[index] = key
    return [slots[index] for index in sorted(slots)]


def check(data, survey, corpus):
    expected = {(r['outpost'], r['source_id']) for r in survey['joins']
                if r['qualification'] == 'PLAUSIBLE_SOURCE_CANDIDATE'}
    seen = set()
    requests = {(x, y) for x, y in product(range(-16, 24), repeat=2)}
    density = {(x - 1, y + 1) for x, y in requests} | {(x - 1, y) for x, y in requests}
    density |= {(x, y + 1) for x, y in requests} | {(x + 1, y + 1) for x, y in requests}
    summary = []
    descriptors = {r['case']: r['request']['descriptor'] for r in survey['outposts'] if r.get('request')}
    for row in data['results']:
        key = row['outpost'], row['source']
        s.require(key not in seen and key in expected, 'Duplicate or unrecognized trace join')
        seen.add(key)
        source = survey['sources'][row['source']]
        s.require(row['descriptor'] == descriptors[key[0]], 'Saved descriptor substitution')
        ax, ay = source['anchor']
        chart, body = source['chart'], source['body']
        sfpt = corpus['bodies'][body]['tiles'][f'{chart}:{ax//192}:{ay//192}'][0]
        # Invert the tile entry lookup from each candidate anchor.
        s.require(ax % 12 == ay % 12 == 0, 'Unaligned anchor')
        block, flags = corpus['patterns'][sfpt][(ax % 192 // 12) * 16 + ay % 192 // 12]
        status = ('NO_MAIN_FILE_ANCHOR' if not flags & 8 else 'DIFFERENT_MAIN_FILE_BLOCK'
                  if block != source['block'] else 'FIXED_INPUT_TRACE')
        s.require(status == row['status'], 'Main-file slot status disagrees')
        if status == 'FIXED_INPUT_TRACE':
            tiles, cells = contributors(corpus, body, chart, source)
            s.require(tiles == row['tiles'], 'Contributing tile closure differs')
        expected_masks = {(r['x'], r['y']): r['mask'] for r in source['rows']}
        masks = {}
        counters = {name: Counter() for name in ('grid', 'density', 'layer')}
        for cell in row.get('rows', ()):
            xy = tuple(cell['relative'])
            native = tuple(cell['native'])
            s.require(xy not in masks and cell['mask'] == expected_masks[xy], 'Mask identity mismatch')
            masks[xy] = cell['mask']
            desc_x, desc_y = row['descriptor']
            s.require(native == (ax + xy[0] - desc_x, ay + xy[1] - desc_y), 'Descriptor join differs')
            s.require((cell['density'] is not None) == (native in density) and
                      (cell['layer'] is not None) == (native in requests), 'Preparation membership differs')
            s.require(cell['grid'] == 'RETAINED' and row['source'] in cell['emitted'],
                      'Current fixed-input trace has an unresolved Grid cell')
            s.require(all(-100 <= v < 100 for v in native) and emission(cells[xy]) == cell['emitted'],
                      'Emitted slot identity or order differs')
            counters['grid'][cell['mask']] += 1
            if native in density:
                counters['density'][cell['mask']] += 1
            if native in requests:
                counters['layer'][cell['mask']] += 1
        if status == 'FIXED_INPUT_TRACE':
            s.require(masks == expected_masks, 'Fixed-input trace lost samples')
            s.require(json.loads(json.dumps(counters)) == row['histograms'], 'Trace histogram differs')
        else:
            s.require(not masks, 'Rejected block emitted requests')
        item = dict(outpost=row['outpost'], source_id=row['source'], status=status,
                    main_file_block=block if flags & 8 else 'NONE',
                    descriptor=json.dumps(row['descriptor'], separators=(',', ':')))
        for name, counts in counters.items():
            item[f'{name}_count'] = sum(counts.values()) if masks else 'UNKNOWN'
            item[f'{name}_masks'] = json.dumps(dict(sorted(counts.items())), separators=(',', ':')) if masks else 'UNKNOWN'
        summary.append(item)
    s.require(seen == expected, 'Trace dropped candidate sources')
    return summary


if __name__ == '__main__':
    receipt, output = (Path(arg).absolute() for arg in sys.argv[1:])
    s.require(output.is_relative_to(s.ROOT) and output == output.resolve() and not output.exists(),
              'Fresh repository output required')
    s.guard()
    s.require(s.sha(sys.executable) == s.PINNED[Path(sys.executable)], 'Interpreter identity')
    data, survey, corpus = s.load(receipt), s.load(grid.SURVEY), s.load(s.D5)['payload']
    for path, digest in data['inputs'].items():
        s.require(s.sha(path) == digest, 'Trace input drift')
    summary = check(data, survey, corpus)
    patterns, blocks = verify_installed(data, corpus)
    target = next(row for row in data['results'] if row['outpost'] == 'D2-81bf2a'
                  and row['source'].endswith('0006ce56'))
    first = target['rows'][0]
    for item, field, corrupted, reason in (
        (first, 'mask', first['mask'] ^ 1, 'Mask identity mismatch'),
        (first, 'emitted', first['emitted'] + ['forged'], 'Emitted slot identity or order differs'),
        (target, 'descriptor', [0, 0], 'Saved descriptor substitution'),
    ):
        original = item[field]
        item[field] = corrupted
        try:
            check(data, survey, corpus)
        except ValueError as error:
            s.require(str(error) == reason, 'Wrong corruption refusal')
        else:
            raise ValueError('Corrupted trace accepted')
        finally:
            item[field] = original
    s.guard()
    with output.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(summary)
    print(f'Checked {len(summary)} candidate joins, {patterns} SFPT tables, {blocks} SFBK dimensions and three corruptions')
