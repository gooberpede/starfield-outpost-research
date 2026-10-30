# SPDX-License-Identifier: GPL-3.0-or-later
"""Recalculate D5U finite supports and predeclared installed discriminators.

Reads pinned D5R static leases, installed PlanetData and D5H arithmetic inputs.
Writes authored CSV/JSON derivatives and ignored receipts, never raw assets.
Reuses owned D5H domains/roundtrip under SOR-P-0002 at the starting HEAD.
No target, save, database, network, package installation or Git mutation.
The census proves raster support, not first-constructor admissibility.
"""
from collections import Counter
import csv
import ctypes
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/d5u'
DOC = ROOT / 'docs/experiments/resource-retained-population/d5u'
sys.path.insert(0, str(ROOT / 'research/resource-query-reachability'))
import domains
from roundtrip import projected


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf8', newline='\n')


def table(path, rows):
    with path.open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def inputs():
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    domains.LEASE = ROOT / '.local-work/resources-evidence-consolidation/d5r-input-lease01'
    assert domains.pin(domains.LEASE/'LEASE.json') == '2faa4f392ac9ac8f37de7410836039cc07c07752cea054f8cac5c6fe39a2207a'
    c = domains.load('.local-work/resource-feynman-d5/build04/normalized.json',
                     '97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9')
    cc = domains.load('.local-work/resource-slot-provenance/build-controls02/normalized.json',
                      '8162cded8e6cb4117352703062242c42110738090383aba541c278210b6e53da')
    manifest = domains.load('.local-work/resource-save52/build-v1/manifest.json',
                            '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de')
    raster = domains.maps(manifest, set(c['bodies']) | set(cc['bodies']))
    return c, cc, raster


def resources(corpus, body, biome):
    return [r for r in corpus['bodies'][body]['biomes'][biome]['resources'] if r.get('branch') != 'special']


def weights(corpus, rs, mask):
    return [((0.0 if r['rarity'] == 6 else corpus['settings'][r['rarity']])
             if mask == 8 or mask < r['rarity'] else 1.0) for r in rs]


def main():
    c, cc, raster = inputs()
    old = list(csv.DictReader((ROOT/'docs/experiments/resource-query-reachability/source-domains.csv').open()))
    assert len(old) == 25 and len({(r['body'], r['source_key']) for r in old}) == 25
    # Selection is based only on masks and effective rarity, before geometry.
    # Scan all installed tiles already represented in the authenticated corpus.
    search, same = [], []
    for corpus in (c, cc):
        for body, b in corpus['bodies'].items():
            for key, tile in sorted(b['tiles'].items()):
                chart, tx, ty = map(int, key.split(':'))
                face = raster[body]['faces'][chart]
                for slot, (block, flags) in enumerate(corpus['patterns'][tile[0]]):
                    if not flags & 8:
                        continue
                    sx, sy = divmod(slot, 16)
                    ax, ay = tx*192+sx*12, ty*192+sy*12
                    w, h = [v-4 for v in corpus['source_blocks'][block]]
                    cells = {(x//192, y//192) for x in (ax-2, ax+w+1) for y in (ay-2, ay+h+1)}
                    masks = sorted({face['mask'][(255-y)*256+x] & 15 for x, y in cells})
                    rs = resources(corpus, body, tile[2])
                    classes = {tuple(weights(corpus, rs, m)) for m in masks}
                    row = dict(body=body, source_key=f'{chart}:{ax}:{ay}:{block}', biome=tile[2],
                               sfpt=tile[0], masks=masks, dimensions=[w, h], weight_classes=len(classes))
                    if len(masks) >= 3:
                        search.append(row)
                    if len(masks) > len(classes):
                        same.append(row)
    search = list({(r['body'],r['source_key']):r for r in search}.values())
    same = list({(r['body'],r['source_key']):r for r in same}.values())
    write(LOCAL/'discriminator-search.json', dict(three_mask=search, same_weight=same,
          selection='First same-body Copper-family three-class corner; first equal-weight mask collision in sorted installed corpus. No geometry consulted.'))
    selected = next(r for r in search if r['body']=='0005e0de' and r['source_key']=='0:37440:20928:0029d211')
    reference = next(r for r in old if r['body']=='0x'+selected['body'] and r['biome']=='0x'+selected['biome'])
    extras = [dict(case='corner-V', source_key=selected['source_key'], body='0x'+selected['body'],
                   biome='0x'+selected['biome'], sfpt='0x'+selected['sfpt'], root=reference['root'],
                   effective_rsgd=reference['effective_rsgd'], classification='NEW DISCRIMINATOR')]
    if same:
        s = same[0]
        extras.append(dict(case='equal-weight', source_key=s['source_key'], body='0x'+s['body'],
                           biome='0x'+s['biome'], sfpt='0x'+s['sfpt'], classification='NEW DISCRIMINATOR'))
    constants = json.loads((ROOT/'.local-work/resource-query-reachability/native-bytes09.json').read_text(encoding='utf8'))['sine_constants']
    host = Path('C:/Windows/System32/ucrtbase.dll')
    assert domains.pin(host) == '3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9'
    crt = ctypes.CDLL(str(host))
    for name in ('cos', 'atan2'):
        fn = getattr(crt, name)
        fn.argtypes = [ctypes.c_double] * (2 if name=='atan2' else 1)
        fn.restype = ctypes.c_double
    control = ctypes.c_uint32()
    crt._controlfp_s.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32]
    assert crt._controlfp_s(ctypes.byref(control), 0, 0) == 0 and control.value & 0x300 == 0
    catalogue, points, source_data = [], [], []
    for ordinal, source in enumerate(old+extras, 1):
        corpus = cc if source['case'] in ('original-V', 'Carinae') else c
        chart, ax, ay, block = source['source_key'].split(':')
        chart, ax, ay = int(chart), int(ax), int(ay)
        body, biome = source['body'][2:], source['biome'][2:]
        w, h = [v-4 for v in corpus['source_blocks'][block]]
        support = domains.attempted_cells(w, h, 2)
        assert support == {(x,y) for x in range(-2,w+2) for y in range(-2,h+2)}
        rs = resources(corpus, body, biome)
        rows = []
        for x, y in sorted(support):
            branches = [projected(chart, ax+x, ay+y, constants=constants, fused=fused, scalar_math=crt)
                        for fused in (False, True)]
            masks = [raster[body]['faces'][tag]['mask'][row*256+col] & 15 for tag,col,row,error in branches]
            assert masks[0] == masks[1]
            rows.append(dict(source_id=f'U{ordinal:02}', x=x, y=y, face_x=ax+x, face_y=ay+y,
                             chart=chart, mask=masks[0], status='UNQUALIFIED CANDIDATE',
                             raster_column=branches[0][1], raster_row=branches[0][2]))
        hist = Counter(r['mask'] for r in rows)
        vectors = {str(m):weights(corpus, rs, m) for m in sorted(hist)}
        if ordinal <= 25:
            assert set(hist) == set(map(int, source['pre_projection_masks'].split(';')))
        row = dict(source_id=f'U{ordinal:02}', case=source['case'], body=source['body'], chart=chart,
                   source_key=source['source_key'], sfpt=source['sfpt'], biome=source['biome'],
                   root=source.get('root','UNKNOWN'), effective_rsgd=source.get('effective_rsgd','UNKNOWN'),
                   width=w, height=h, padding=2, support_cells=len(rows),
                   histogram=json.dumps(dict(sorted(hist.items())),separators=(',',':')),
                   raster_masks=len(hist), reachable_masks='PENDING QUALIFICATION',
                   weight_classes=len({tuple(v) for v in vectors.values()}),
                   geometry_outcomes='PENDING QUALIFICATION', historical=source['classification'],
                   ordinary_order=';'.join(r['id'] for r in rs), vectors=json.dumps(vectors,separators=(',',':')),
                   outpost_centre='UNKNOWN', beacon='UNKNOWN')
        catalogue.append(row)
        points.extend(rows)
        source_data.append(dict(catalogue=row, coordinates=rows, resources=rs, weights=vectors,
                                corpus='controls' if corpus is cc else 'D5'))
    DOC.mkdir(exist_ok=True)
    table(DOC/'catalogue.csv', catalogue)
    table(DOC/'queries.csv', points)
    write(LOCAL/'census.json',dict(sources=source_data, arithmetic_branches=2, host_sha256=domains.pin(host),
                                 code_sha256=domains.pin(Path(__file__)), cells=len(points)))
    print(json.dumps(dict(sources=len(catalogue), cells=len(points), three_mask_candidates=len(search),
                         same_weight_candidates=len(same), extras=extras),indent=2))


if __name__ == '__main__':
    main()
