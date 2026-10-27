# SPDX-License-Identifier: GPL-3.0-or-later
"""D5I source-specific arithmetic and competing-slot replay, version 1.

Reads an explicitly restored, hash-pinned corpus/manifest and installed BA2,
plus D5H arithmetic constants and source roster. Writes one exclusive local JSON.
Uses owned D5H replay methods (SOR-P-0002); host CRT math only, no game calls.
No original evidence, definitions, analysis DB, classification or Git writes.
The result is numerical/occupancy evidence; native first-miss proof is separate.
"""
import csv
import ctypes
import itertools
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/resource-query-reachability'))
import domains
from roundtrip import projected


def contributors(corpus, body_id, chart, query):
    """Enumerate whole contributing tiles, not selector samples at the query.

    Concrete replay deliberately accepts fill and Y-edge cells only. Any X-edge
    or corner contributor aborts rather than silently applying Y-edge semantics.
    Max dimensions cover all SFBKs in this authenticated corpus, as in D5H.
    """
    body = corpus['bodies'][body_id]
    max_x = max(w - 4 for w, h in corpus['source_blocks'].values())
    max_y = max(h - 4 for w, h in corpus['source_blocks'].values())
    qx, qy = query
    bounds = [qx - max_x - 1, qx + 2, qy - max_y - 1, qy + 2]
    rows, tiles, seen = [], [], set()
    for tx in range(bounds[0] // 192, bounds[1] // 192 + 1):
        for ty in range(bounds[2] // 192, bounds[3] // 192 + 1):
            tile_key = f'{chart}:{tx}:{ty}'
            tile = body['tiles'][tile_key]
            assert tile[1] == 8
            tiles.append(dict(key=tile_key, sfpt=tile[0], flags=tile[1], entries=256))
            for index, (block, flags) in enumerate(corpus['patterns'][tile[0]]):
                if not flags & 8:
                    continue
                sx, sy = divmod(index, 16)
                ax, ay = tx * 192 + sx * 12, ty * 192 + sy * 12
                width, height = (v - 4 for v in corpus['source_blocks'][block])
                dx, dy = qx - ax, qy - ay
                if not (-2 <= dx < width + 2 and -2 <= dy < height + 2):
                    continue
                assert (ax, ay) not in seen, 'Duplicate anchor needs first-descriptor analysis'
                seen.add((ax, ay))
                assert 0 <= dx < width, 'X-edge/corner requires different setter proof'
                kind = 'fill' if 0 <= dy < height else 'edgeY'
                slot = '0x18' if kind == 'fill' or dy < 0 else '0x20'
                assert 0 <= dx + 2 < width + 4 and 0 <= dy + 2 < height + 4
                rows.append(dict(source=f'{chart}:{ax}:{ay}:{block}', sfpt=tile[0],
                    entry=index, flags=flags, anchor=[ax, ay], dimensions=[width, height],
                    relative_query=[dx, dy], raw_query=[dx + 2, dy + 2],
                    kind=kind, edge_flag=0 if kind == 'fill' else 2 if dy < 0 else 1,
                    slot=slot))
    assert rows and len(rows) <= 6
    # D5H's concrete setters permit this simple replay only for like cell kinds.
    assert len({r['kind'] for r in rows}) == 1
    outcomes = []
    for order in itertools.permutations(rows):
        slots = {}
        for r in order:
            slots.setdefault(r['slot'], r['source'])
        outcomes.append(dict(order=[r['source'] for r in order], slots=slots,
            emitted=[slots[k] for k in sorted(slots)]))
    return dict(query=list(query), bounds_inclusive=bounds, max_nominal=[max_x, max_y],
        tiles=tiles, contributors=rows, outcomes=outcomes)


def main():
    lease, lease_sha, output = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    assert lease.is_relative_to(ROOT / '.local-work/resources-evidence-consolidation')
    assert output.is_relative_to(ROOT / '.local-work/resource-query-variability') and not output.exists()
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40000000000
    assert domains.pin(lease / 'LEASE.json') == lease_sha
    domains.LEASE = lease
    corpus = domains.load('.local-work/resource-feynman-d5/build04/normalized.json',
        '97aa50e0eb6bc7a2d5157bffbb311942fd84e7c01e6bd2ef3ea28a4e9bd9e0f9')
    manifest = domains.load('.local-work/resource-save52/build-v1/manifest.json',
        '9d2ff9012a573595227c8feda5345de35286b807103665486239ddbe8cbfa9de')
    source_path = ROOT / 'docs/experiments/resource-query-reachability/source-domains.csv'
    roster = [r for r in csv.DictReader(source_path.open()) if r['classification'] == 'UNRESOLVED']
    assert len(roster) == 5
    roster.sort(key=lambda r: ({'D2-844cc6': 0, 'D2-84e101': 1, 'D2-81bf2a': 2}[r['case']], r['source_key']))
    rasters = domains.maps(manifest, {r['body'][2:] for r in roster})
    constants_path = ROOT / '.local-work/resource-query-reachability/native-bytes09.json'
    constants = json.loads(constants_path.read_text())['sine_constants']
    host = Path('C:/Windows/System32/ucrtbase.dll')
    assert domains.pin(host) == '3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9'
    crt = ctypes.CDLL(str(host))
    for name in ('cos', 'atan2'):
        fn = getattr(crt, name)
        fn.argtypes = [ctypes.c_double] * (2 if name == 'atan2' else 1)
        fn.restype = ctypes.c_double
    crt._controlfp_s.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32]
    crt._controlfp_s.restype = ctypes.c_int
    control = ctypes.c_uint32()
    assert crt._controlfp_s(ctypes.byref(control), 0, 0) == 0 and control.value & 0x300 == 0
    result = []
    for source in roster:
        chart, ax, ay, block = source['source_key'].split(':')
        chart, ax, ay = int(chart), int(ax), int(ay)
        resources = [r for r in corpus['bodies'][source['body'][2:]]['biomes'][source['biome'][2:]]['resources']
            if r.get('branch') != 'special']
        assert [r['id'] for r in resources] == source['candidate_order'].split(';')
        alternatives = []
        for label, root in [('lower', (5, -2)), ('interior', (5, 0))]:
            queries = []
            for dx, dy in [(-1, 1), (-1, 0), (0, 1), (1, 1)]:
                q = (ax + root[0] + dx, ay + root[1] + dy)
                branches = []
                for fused in (False, True):
                    tag, x, y, error = projected(chart, *q, constants=constants, fused=fused, scalar_math=crt)
                    mask = rasters[source['body'][2:]]['faces'][tag]['mask'][y * 256 + x] & 15
                    vector = [(0.0 if r['rarity'] == 6 else corpus['settings'][r['rarity']])
                        if mask == 8 or mask < r['rarity'] else 1.0 for r in resources]
                    assert vector == json.loads(source['ordinary_vectors'])[str(mask)]
                    branches.append(dict(fused=fused, chart=tag, column=x, row=y, mask=mask,
                        vector=vector, error_fine_cells=error))
                queries.append(dict(query=list(q), branches=branches,
                    occupancy=contributors(corpus, source['body'][2:], chart, q)))
            first = queries[0]
            alternatives.append(dict(label=label, root_offset=list(root),
                root_geographic=[ax + root[0], ay + root[1]], queries=queries,
                source_emitted_first_all_orders=all(o['emitted'][0] == source['source_key']
                    for o in first['occupancy']['outcomes'])))
        result.append(dict(source=source, alternatives=alternatives))
    with output.open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(schema='sor-d5i-cases/1', helper_sha256=domains.pin(Path(__file__)),
            source_roster_sha256=domains.pin(source_path), lease_sha256=lease_sha,
            constants_sha256=domains.pin(constants_path), host_sha256=domains.pin(host),
            control_word=hex(control.value), rows=result,
            qualification='Numerical and retained-slot replay only; native admission and completion require separate proof'), f, indent=2)
        f.write('\n')
    for row in result:
        print(row['source']['source_key'], [(a['label'], a['queries'][0]['branches'][0]['mask'],
            a['source_emitted_first_all_orders']) for a in row['alternatives']])


if __name__ == '__main__':
    main()
