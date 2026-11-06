# SPDX-License-Identifier: GPL-3.0-or-later
"""Trace modeled Save52 keys through ordinary Grid retention and registration.

Read pinned installed/native and Save52 derivatives. Write one ignored
receipt. No game instructions execute. The caller supplies the D5S
focus-zero initialized context as a scenario, with saved descriptors.
"""
import os
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from collections import Counter
from itertools import product
from pathlib import Path

import d5at_survey as s


DOCS = s.ROOT / 'docs/experiments/resource-query-reachability'
EXE = s.INSTALL / 'Starfield.exe'
NATIVE = DOCS / 'native.csv'
REGISTRATION = s.ROOT / '.local-work/d5s/registration.json'
SURVEY = s.ROOT / '.local-work/d5at-survey07.json'
PINS = {
    NATIVE: '1e888112aef7a74f46d28719b15b6e7239b0f5728ad6bed38c3292c72631ea8e',
    REGISTRATION: '72505fe91be0fa2633fbc9ddab37d1ad40afca4c72aac7bcb324f05ed1b3ff0a',
    s.D5: s.PINNED[s.D5],
    EXE: s.PINNED[EXE],
}
FUNCTIONS = {
    '0x1407847b0', '0x1407862a0', '0x140982d90', '0x1409832e0',
    '0x140985900', '0x140985c50', '0x140986080', '0x140983270',
    '0x140988220', '0x140988240', '0x1409882d0', '0x1409884e0',
    '0x140988330', '0x140988670', '0x140988760', '0x140988ab0', '0x140985870',
    '0x1407af970', '0x1407b4bb0', '0x1407b2390', '0x1407b30c0',
    '0x1407b5160', '0x1407a0fa0', '0x14079f860', '0x1407a1940',
}
OFFSETS = ((-1, 1), (-1, 0), (0, 1), (1, 1))
CORNER = {6: 0x20, 5: 0x30, 10: 0x18, 9: 0x28}
# Both native insertion paths give the same two slots for these edge
# contributors: conversion of an existing edge and insertion into a corner.
EDGE_IN_CORNER = {
    ('edgeX', 0x18): (0x18, 0x28), ('edgeX', 0x20): (0x20, 0x30),
    ('edgeY', 0x18): (0x18, 0x20), ('edgeY', 0x20): (0x28, 0x30),
}
EDGE_GETTERS = {
    0x988380: '814fdc19f7ccb3fe4be3f9afb514015512f8ff2bd2cabc2daa11b4948786be96',
    0x988540: 'affde492c3af5103609912ef5d19d61a8db1c98502b78ea6fbb6e33f9b3d23f3',
}


def verify_native():
    """Check each retained export and the independent installed PE file ranges."""
    import hashlib
    import json

    rows = [row for row in s.read_csv(NATIVE) if row['va'] in FUNCTIONS]
    s.require({row['va'] for row in rows} == FUNCTIONS, 'Native function inventory incomplete')
    inputs = {}
    with EXE.open('rb') as image:
        for rva, digest in EDGE_GETTERS.items():
            image.seek(rva - 0x1000 + 0x600)  # Pinned PE .text RVA and file offset.
            s.require(hashlib.sha256(image.read(23)).hexdigest() == digest, 'Edge getter instruction mismatch')
        for row in rows:
            path = s.ROOT / row['locator']
            if path not in inputs:
                s.require(s.sha(path) == row['export_sha256'], 'Native export changed')
                inputs[path] = row['export_sha256']
            for span in json.loads(row['byte_ranges']):
                image.seek(span['file_offset'])
                data = image.read(span['bytes'])
                s.require(len(data) == span['bytes'] and hashlib.sha256(data).hexdigest() == span['sha256'],
                          'Native range mismatch')
    return inputs


def registrations(low, high):
    """Transcribe the ordered cold coordinate recursion and density dedup."""
    roots, density = {}, {}

    def visit(q):
        if q in roots:
            return
        roots[q] = len(roots)
        for dx, dy in OFFSETS:
            n = q[0] + dx, q[1] + dy
            density.setdefault(n, len(density))
            if all(low <= v <= high for v in n):
                visit(n)

    for x, y in product(range(low, high + 1), range(high, low - 1, -1)):
        visit((x, y))
    independent = {(x + dx, y + dy) for x, y in product(range(low, high + 1), repeat=2)
                   for dx, dy in OFFSETS}
    s.require(set(density) == independent and len(roots) == (high - low + 1) ** 2,
              'Registration disagrees with set oracle')
    return roots, density


def tile_sources(corpus, body, chart, tx, ty):
    s.require(0 <= tx < 256 and 0 <= ty < 256, 'Unqualified chart boundary')
    sfpt, flags, biome, _ = corpus['bodies'][body]['tiles'][f'{chart}:{tx}:{ty}']
    s.require(flags == 8, 'Unsupported SFPT orientation')
    for index, (block, flags) in enumerate(corpus['patterns'][sfpt]):
        if flags & 8:
            sx, sy = divmod(index, 16)
            ax, ay = tx * 192 + sx * 12, ty * 192 + sy * 12
            w, h = (v - 4 for v in corpus['source_blocks'][block])
            yield dict(key=f'{body}/{chart}:{ax}:{ay}:{block}', anchor=(ax, ay),
                       size=(w, h), sfpt=sfpt, biome=biome, fnam_index=index, flags=flags)


def slot(dx, dy, width, height):
    """Return homogeneous cell kind and native source-pointer slot."""
    xflag = 4 if dx < 0 else 8 if dx >= width else 0
    yflag = 2 if dy < 0 else 1 if dy >= height else 0
    if xflag and yflag:
        return 'corner', CORNER[xflag | yflag]
    if xflag:
        return 'edgeX', 0x20 if xflag == 4 else 0x18
    if yflag:
        return 'edgeY', 0x18 if yflag == 2 else 0x20
    return 'fill', 0x18


def retention(contributors):
    kinds = {kind for kind, _, _ in contributors}
    converts = 'corner' in kinds and len(kinds) > 1
    if len(kinds) != 1 and (not converts or 'fill' in kinds or {'edgeX', 'edgeY'} <= kinds):
        return None
    slots = {}
    for kind, offset, key in contributors:
        offsets = EDGE_IN_CORNER[kind, offset] if converts and kind != 'corner' else (offset,)
        for target in offsets:
            slots.setdefault(target, set()).add(key)
    if any(len(keys) != 1 for keys in slots.values()):
        return None
    return [next(iter(slots[offset])) for offset in sorted(slots)]


def trace(corpus, case, source, roots, density):
    body, chart = case['body'], case['request']['chart']
    ax, ay = source['anchor']
    key = source['source_id']
    s.require(source['body'] == body and source['chart'] == chart, 'Site/source identity mismatch')
    try:
        installed = [row for row in tile_sources(corpus, body, chart, ax // 192, ay // 192)
                     if row['anchor'] == (ax, ay)]
    except (KeyError, ValueError) as error:
        return dict(source=key, status='UNQUALIFIED_ANCHOR', reason=str(error))
    if not installed:
        return dict(source=key, status='NO_MAIN_FILE_ANCHOR')
    s.require(len(installed) == 1, 'Multiple installed entries at anchor')
    installed = installed[0]
    if installed['key'] != key:
        return dict(source=key, status='DIFFERENT_MAIN_FILE_BLOCK', selected=installed)
    width, height = installed['size']
    s.require((width, height) == (source['width'], source['height']), 'Installed source extent differs')
    max_w = max(v[0] - 4 for v in corpus['source_blocks'].values())
    max_h = max(v[1] - 4 for v in corpus['source_blocks'].values())
    # Cover every anchor whose padded support can reach any target cell.
    tx = range((ax - 2 - max_w - 1) // 192, (ax + width + 3) // 192 + 1)
    ty = range((ay - 2 - max_h - 1) // 192, (ay + height + 3) // 192 + 1)
    try:
        neighbors = [row for x, y in product(tx, ty) for row in tile_sources(corpus, body, chart, x, y)]
    except (KeyError, ValueError) as error:
        return dict(source=key, status='UNQUALIFIED_NEIGHBOR_TILE', selected=installed, reason=str(error))
    s.require(len({r['anchor'] for r in neighbors}) == len(neighbors), 'Duplicate installed anchor')
    desc = case['request']['descriptor']
    counts = {'grid': Counter(), 'density': Counter(), 'layer': Counter()}
    rows = []
    masks = {(row['x'], row['y']): row['mask'] for row in source['rows']}
    for x, y in product(range(-2, width + 2), range(-2, height + 2)):
        native = (ax + x - desc[0], ay + y - desc[1])
        mask = masks.get((x, y))
        qx, qy = ax + x, ay + y
        contenders = []
        for neighbor in neighbors:
            bx, by = neighbor['anchor']
            w, h = neighbor['size']
            dx, dy = qx - bx, qy - by
            if -2 <= dx < w + 2 and -2 <= dy < h + 2:
                contenders.append((*slot(dx, dy, w, h), neighbor['key']))
        emitted = retention(contenders)
        in_grid = all(-100 <= v < 100 for v in native)
        if not in_grid:
            disposition = 'CLIPPED'
        elif emitted is None:
            disposition = 'UNQUALIFIED_SLOT'
        elif key not in emitted:
            disposition = 'NOT_RETAINED'
        else:
            disposition = 'RETAINED'
            counts['grid'][mask] += 1
            if native in density:
                counts['density'][mask] += 1
            if native in roots:
                counts['layer'][mask] += 1
        rows.append(dict(relative=(x, y), native=native, mask=mask, contenders=contenders,
                         emitted=emitted, grid=disposition, density=density.get(native), layer=roots.get(native)))
    return dict(source=key, status='FIXED_INPUT_TRACE', selected=installed,
                tiles=[f'{chart}:{x}:{y}' for x, y in product(tx, ty)],
                histograms=counts, rows=rows)


def run(output):
    before = s.guard()
    s.require(s.sha(sys.executable) == s.PINNED[Path(sys.executable)], 'Interpreter identity')
    for path, digest in PINS.items():
        s.require(s.sha(path) == digest, f'Input changed: {path}')
    expected = s.load(s.ROOT / '.local-work/d5at-source-lock.json')['sha256']
    s.require(s.sha(SURVEY) == expected[SURVEY.relative_to(s.ROOT).as_posix()], 'Survey pin differs')
    native = verify_native()
    roots, density = registrations(-16, 23)
    known = s.load(REGISTRATION)
    s.require(list(density) == list(map(tuple, known['density_order'])) and
              list(roots) == list(map(tuple, known['producer_root_order'])),
              'D5S exact registration regression')
    s.require(retention([('corner', 0x18, 'A'), ('corner', 0x18, 'B')]) is None and
              retention([('edgeX', 0x20, 'A'), ('corner', 0x18, 'B')]) == ['B', 'A', 'A'] and
              retention([('edgeY', 0x20, 'A'), ('corner', 0x28, 'B')]) is None,
              'Unsupported slot transition control')
    survey = s.load(SURVEY)
    corpus = s.load(s.D5)['payload']
    cases = {r['case']: r for r in survey['outposts'] if r.get('request')}
    first = {'D2-81bf2a': 0, 'D2-844cc6': 1}
    results = []
    for join in sorted(survey['joins'], key=lambda row: first.get(row['outpost'], 2)):
        if join['qualification'] == 'PLAUSIBLE_SOURCE_CANDIDATE' and join['outpost'] in cases:
            case = cases[join['outpost']]
            result = trace(corpus, case, survey['sources'][join['source_id']], roots, density)
            results.append(dict(outpost=case['case'], descriptor=case['request']['descriptor'], **result))
    after = s.guard()
    s.write(output, dict(scenario='D5AT-GRID-PREWARM-0', results=results,
                         roots=len(roots), density=len(density), before=before, after=after,
                         inputs={str(path): digest for path, digest in (PINS | native | {SURVEY: s.sha(SURVEY)}).items()}))
    print(Counter(r['status'] for r in results))


if __name__ == '__main__':
    output = Path(sys.argv[1]).absolute()
    s.require(output.is_relative_to(s.ROOT / '.local-work') and output == output.resolve()
              and not output.exists(), 'Fresh ignored output required')
    run(output)
