# SPDX-License-Identifier: GPL-3.0-or-later
"""D5G bounded installed-lineage and source-domain audit (stdlib, owned readers).

Reads pinned ESM, frozen D5/D4E corpora/outputs and framed historical controls.
Writes exclusive local JSON and new authored CSV tables. No geometry generation,
target, save, analysis-project, network or Git writes. Run after audit.py before.
Source enumeration adapts D5 inputs.py; record decoding imports owned C2D/D1 code.
"""
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import zlib

from audit import ROOT, OUT, pin, write
sys.path[:0] = [str(ROOT / 'research' / p) for p in
    ('resource-standalone', 'resource-slot-provenance', 'resource-geometry',
     'resource-spatial', 'resource-pattern-selection', 'resource-owner-root')]
import builder
import predictor_d4e as predictor
import verify
from installed import planet_tree, decode_tree
from source_layout import install_fnam

DOC = ROOT / 'docs/experiments/resource-predictability-contrast'
LOCAL = ROOT / '.local-work'
D5 = LOCAL / 'resource-feynman-d5'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def table(name, rows):
    with (DOC / name).open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def joined(values):
    return ';'.join(map(str, sorted(set(values))))


def sources(c, q):
    body = c['bodies'][q['body']]
    halo = q['radius'] + 400 + 2 * c['maximum_width']
    lo = [math.floor(q['descriptor'][k] + (q['query'][k] - halo) / 100) for k in (0, 1)]
    hi = [math.floor(q['descriptor'][k] + (q['query'][k] + halo) / 100) for k in (0, 1)]
    found = {}
    for x in range(lo[0], hi[0] + 1):
        for y in range(lo[1], hi[1] + 1):
            s = predictor.resolve(c, body, q['chart'], x, y)
            found[s[:3]] = s
    return sorted(found.values())


def main():
    expected = load(D5 / 'audit-after.json')['pins']
    expected.update(load(LOCAL / 'resource-construction-demand/audit-after.json')['pins'])
    for folder in ('resource-feynman-d5', 'resource-construction-mask-selection',
                   'resource-slot-provenance', 'resource-pattern-selection'):
        for row in csv.DictReader((ROOT / f'docs/experiments/{folder}/sources.csv').open(encoding='utf8')):
            path = row['path']
            expected[str((ROOT / path).resolve()) if not Path(path).is_absolute() else path] = row['sha256']
    expected = {str(Path(p) if Path(p).is_absolute() else ROOT / p).replace('\\', '/').lower(): h
                for p, h in expected.items()}
    checked = {}
    def checked_load(path):
        actual = pin(path)
        key = str(Path(path).resolve())
        assert actual == expected[key.replace('\\', '/').lower()], ('Missing or altered expected pin', key)
        checked[key] = actual
        return load(path)
    assert pin(builder.ESM) == builder.DEFINITION
    c = predictor.validate(checked_load(D5 / 'build04/normalized.json'))
    cc = predictor.validate(checked_load(LOCAL / 'resource-slot-provenance/build-controls02/normalized.json'))
    freeze = load(D5 / 'validation01/prediction-freeze.json')
    assert all(pin(p) == h for p, h in freeze['outputs'].items())
    assert all(pin(p) == h for p, h in freeze['corpora'].items())
    assert (D5 / 'build04/normalized.json').read_bytes() == (D5 / 'build02/normalized.json').read_bytes()
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'PNDT', b'SFTR', b'SFPT', b'SFBK', b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
    def rh(fid):
        return hashlib.sha256(b''.join(t + struct.pack('<I', len(v)) + v
            for t, v in records[fid][1])).hexdigest()
    import context
    assert pin(builder.ARCHIVE) == builder.ARCHIVE_HASH
    members = checked_load(LOCAL / 'resource-save52/build-v1/manifest.json')['members']
    maps = {}
    with builder.ARCHIVE.open('rb') as stream:
        magic, version, kind, count, offset = struct.unpack('<4sI4sIQ', stream.read(24))
        assert (magic, version, kind) == (b'BTDX', 2, b'GNRL') and count <= 10000
        stream.seek(32)
        entries = [struct.unpack('<I4sIIQIII', stream.read(36)) for _ in range(count)]
        stream.seek(offset)
        names = [stream.read(int.from_bytes(stream.read(2), 'little')).decode() for _ in range(count)]
        for bid in ('0005e0de', '0005e4da', '0005de4c', '0005e0e3', '0005e0e7', '0005e0ee'):
            member = members[bid]
            assert names.count(member['name']) == 1
            off, packed, unpacked = entries[names.index(member['name'])][4:7]
            assert unpacked == member['bytes'] and unpacked <= 2_000_000
            assert off + (packed or unpacked) <= builder.ARCHIVE.stat().st_size
            stream.seek(off)
            raw = stream.read(packed or unpacked)
            if packed:
                decoder = zlib.decompressobj()
                raw = decoder.decompress(raw, unpacked + 1)
                assert decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
            assert len(raw) == unpacked and hashlib.sha256(raw).hexdigest() == member['sha256']
            maps[bid] = context.read_map(raw)
    prep = checked_load(D5 / 'build04/preparation.json')
    selections = {(r['body'], r['biome']): r for r in prep['lineage']}
    for row in checked_load(LOCAL / 'resource-slot-provenance/build-controls02/preparation.json')['lineage']:
        selections.setdefault((row['body'], row['biome']), row)
    installed_checks = []
    for corpus in (c, cc):
        for bid in maps:
            if bid not in corpus['bodies']:
                continue
            tree = decode_tree(records[planet_tree(records[int(bid, 16)][1])][1])
            for key, tile in corpus['bodies'][bid]['tiles'].items():
                chart, x, y = map(int, key.split(':'))
                assert tree[chart][x * 256 + y] == (int(tile[0], 16), tile[1])
                if bid in maps:
                    assert context.map_lookup(maps[bid], chart, x * 192, y * 192) == int(tile[2], 16)
                    assert context.mask_lookup(maps[bid], chart, x * 192, y * 192) & 15 == tile[3] & 15
                fs = records[int(tile[0], 16)][1]
                installed = install_fnam(list(zip(struct.unpack('<256I', builder.last(fs, b'FNAM')), builder.last(fs, b'GNAM'))))
                assert corpus['patterns'][tile[0]] == [[f'{fid:08x}', flags] for fid, flags in installed]
                installed_checks.append([bid, key, tile])
    write(OUT / 'installed-projection-checks.json', installed_checks)
    requests = [('original-V', cc, verify.request('0005e0de')),
                ('Carinae', cc, verify.request('0005e4da')),
                ('Archimedes', c, load(D5 / 'validation01/cohort/D2-81a75b-request-normalized-stdout.json')['request'])]
    mixed = checked_load(D5 / 'inputs-v2.json')
    inventory = {row['case']: row for row in checked_load(LOCAL / 'resource-save52/inventory-v2.json')['cases']}
    components = checked_load(LOCAL / 'resource-slot-provenance/freeze01/prediction-v1.json')
    for case in mixed['cases']:
        if case['case'] == 'D2-832210':
            continue
        requests.append((case['case'], c, case['request']))
    # Freeze installed choices and domain hypotheses before opening native geometry.
    frozen = []
    for case, corpus, q in requests:
        for s in sources(corpus, q):
            key = f'{q["chart"]}:{s[0]}:{s[1]}:{s[2]}'
            if case.startswith('D2-') and not any(v['source_key'] == key and
                len(v['neighborhood_low_masks']) > 1 for item in mixed['cases']
                if item['case'] == case for v in item['sources']):
                continue
            frozen.append(dict(case=case, request=q, source=list(s), source_key=key))
    assert len([v for v in frozen if v['case'].startswith('D2-')]) == 13
    write(OUT / 'selection-freeze.json', dict(rows=frozen,
        hypothesis='Nominal and conservative masks differ from unproved provider reachability.',
        native_geometry_read=False, personal_blindness=False,
        script_sha256=pin(Path(__file__)), head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        checked_inputs=checked))
    DOC.mkdir(parents=True, exist_ok=True)
    lineage = []
    tree_ids = collections.Counter(h['type'] for h, fs in records.values())
    contexts = []
    for bid in (0x5e0de, 0x5e4da, 0x5de4c):
        tree = planet_tree(records[bid][1])
        pfs = records[bid][1]
        system, parent, index = struct.unpack('<III', next(v for t,v in pfs if t == b'GNAM' and len(v) == 12))
        contexts.append(dict(pndt=f'0x{bid:08x}', sftr=f'0x{tree:08x}',
            pndt_fields_sha256=rh(bid), sftr_fields_sha256=rh(tree),
            resource_creation_seed=int.from_bytes(builder.last(pfs,b'RSCS'),'little'),
            system_id=system, body_index=index,
            tree_components=';'.join(v.rstrip(b'\0').decode() for t,v in records[tree][1] if t == b'BFCB') or 'NONE_IN_INSTALLED_RECORD',
            component_effect='UNKNOWN beyond mapped linked-table route'))
    table('planet-context.csv', contexts)
    bodyid = int('0005e0de', 16)
    treeid = planet_tree(records[bodyid][1])
    trees = decode_tree(records[treeid][1])
    population = collections.Counter((pid, flag) for face in trees for pid, flag in face)
    for (pid, flag), count in sorted(population.items()):
        fs = records[pid][1]
        ids = struct.unpack('<256I', builder.last(fs, b'FNAM'))
        flags = builder.last(fs, b'GNAM')
        assert len(flags) == 256 and not any(t == b'EFRM' for t, v in fs)
        entries = install_fnam(list(zip(ids, flags)))
        for block, occurrences in sorted(collections.Counter(fid for fid, f in entries).items()):
            lineage.append(dict(scope='Feynman-V whole linked tree; both sites', kind='SFPT_SFBK_POPULATION',
                pndt=f'0x{bodyid:08x}', sftr=f'0x{treeid:08x}', sfpt=f'0x{pid:08x}',
                tree_flags=f'0x{flag:02x}', tree_cells=count, sfbk=f'0x{block:08x}',
                pattern_slots=occurrences, biome='', rsgd='', selector='Full two-face table; FNAM transpose; defaults retained',
                fields_sha256=rh(pid), linked_fields_sha256=rh(block) if block in records else 'NULL_OR_UNRESOLVED'))
    for tag, value in records[bodyid][1]:
        if tag != b'PPBD':
            continue
        biom, chance, unknown, override = struct.unpack_from('<IfII', value)
        local = [int.from_bytes(v, 'little') for t, v in records[biom][1] if t == b'RNAM']
        for rsgd in sorted(set(local + ([override] if override else []))):
            lineage.append(dict(scope='Feynman-V installed components; both sites', kind='BIOM_RSGD_POPULATION',
                pndt=f'0x{bodyid:08x}', sftr=f'0x{treeid:08x}', sfpt='', tree_flags='', tree_cells='',
                sfbk='', pattern_slots='', biome=f'0x{biom:08x}', rsgd=f'0x{rsgd:08x}',
                selector=f'PPBD chance {chance}; shuffle operand {unknown}; effective override 0x{override:08x}; BIOM RNAM {joined(hex(v) for v in local)}',
                fields_sha256=rh(biom), linked_fields_sha256=rh(rsgd)))
    domainrows, sourcerows = [], []
    measurements = []
    for item in frozen:
        case, q = item['case'], item['request']
        corpus = cc if case in ('original-V', 'Carinae') else c
        body = corpus['bodies'][q['body']]
        ax, ay, fid, dx, dy, biome = item['source']
        chart = q['chart']
        def masks(x0, x1, y0, y1):
            return {predictor.tile_at(body, chart, x, y)[3] & 15 for x in range(x0, x1) for y in range(y0, y1)}
        nominal = masks(ax, ax + dx, ay, ay + dy)
        conservative = masks(ax - 4, ax + dx + 5, ay - 4, ay + dy + 5)
        inverse = []
        for x in range(ax // 192 * 192, (ax // 192 + 1) * 192):
            for y in range(ay // 192 * 192, (ay // 192 + 1) * 192):
                try:
                    if predictor.resolve(corpus, body, chart, x, y)[:3] == (ax, ay, fid):
                        inverse.append((x, y))
                except ValueError:
                    pass
        inverse_masks = {predictor.tile_at(body, chart, x, y)[3] & 15 for x, y in inverse}
        globe = {v & 15 for face in maps[q['body']]['faces'] for v in face['mask']} if q['body'] in maps else set(range(16))
        ordinary = [r for r in body['biomes'][biome]['resources'] if r.get('branch') != 'special']
        classes = collections.defaultdict(list)
        for mask in sorted(globe):
            vector = tuple((0.0 if r['rarity'] == 6 else corpus['settings'][r['rarity']])
                if mask == 8 or mask < r['rarity'] else 1.0 for r in ordinary)
            classes[vector].append(mask)
        selection = selections.get((q['body'], biome))
        tile = predictor.tile_at(body, chart, ax, ay)
        nominal_biomes = {predictor.tile_at(body, chart, x, y)[2] for x in range(ax, ax + dx) for y in range(ay, ay + dy)}
        domainrows.append(dict(case=case, source_key=item['source_key'],
            nominal_half_open_fine_xy=f'[{ax},{ax+dx})x[{ay},{ay+dy})', nominal_masks=joined(nominal),
            conservative_half_open_fine_xy=f'[{ax-4},{ax+dx+5})x[{ay-4},{ay+dy+5})', conservative_masks=joined(conservative),
            nominal_biomes=joined('0x'+v for v in nominal_biomes),
            inverse_base_selector_cells=len(inverse), inverse_base_selector_masks=joined(inverse_masks),
            static_reachable_mask_lower='EMPTY_UNPROVED', static_reachable_mask_upper=joined(globe),
            upper_scope='Installed body raster' if q['body'] in maps else 'Low-nibble codomain; map not extracted',
            ordinary_weight_classes=json.dumps([dict(masks=v, weights=k) for k,v in classes.items()],separators=(',',':')),
            witnessed_first_miss_queries='NONE', witnessed_first_miss_masks='UNKNOWN',
            all_reachable_invariant='NOT_PROVED',
            missing_condition='Provider index origin/dimensions and per-cell virtual enumeration; effective descriptor; exact geographic round trip; first-miss state',
            basis='INSTALLED nominal; DERIVED conditional inverse; UNKNOWN native reachability'))
        selected = body['biomes'][biome]
        saved_case = {'original-V':'D2-83388f','Carinae':'D2-82be17','Archimedes':'D2-81a75b'}.get(case, case)
        identity = inventory[saved_case]
        component = next(v for v in components[q['body']]['components'] if v['biome'] == int(biome,16))
        sourcerows.append(dict(case=case, body='0x'+q['body'], source_key=item['source_key'],
            saved_beacon_token=identity['token'], workshop_bytes=identity['workshop_id'], saved_frame=hex(identity['frame']),
            descriptor_fine_xy=joined(q['descriptor']) if q['descriptor'][0] == q['descriptor'][1] else ';'.join(map(str,q['descriptor'])),
            source_origin_native_xy=';'.join(str(100*(v-o-2)) for v,o in zip((ax,ay),q['descriptor'])),
            sfpt='0x'+tile[0], sfbk='0x'+fid, biome='0x'+biome,
            root='0x'+selection['descriptor']['root'] if selection else 'See control preparation',
            effective_rsgd='0x'+selection['descriptor']['rsgd'] if selection else 'See control preparation',
            descriptor_route=selection['descriptor']['descriptor_route'] if selection else 'See control preparation',
            initialized_slots_0_through_5=';'.join(f'0x{v:08x}' for v in component['slots']),
            ordered_resources=';'.join('0x'+r['id']+(' Special' if r.get('branch') == 'special' else '') for r in selected['resources']),
            native_control_captures='', frozen_generated_paths='NOT_REPLAYED_MIXED', positive_area_paths='NOT_REPLAYED_MIXED', callback_accepted_paths='NOT_REPLAYED_MIXED',
            actual_pointer='UNKNOWN; geographic key is not a pointer',
            derivation='INSTALLED selectors + DERIVED conditional initialized population; ' +
                ('SAVE-positive conditional frame' if case.startswith('D2-') else 'RUNTIME-witnessed control frame'),
            history='UNKNOWN first query and epoch', nominal_masks=joined(nominal), conservative_masks=joined(conservative)))
        if q['body'] == '0005e0de':
            lineage.append(dict(scope=case, kind='SELECTED_SOURCE', pndt='0x0005e0de', sftr=f'0x{treeid:08x}',
                sfpt='0x'+tile[0], tree_flags=hex(tile[1]), tree_cells='', sfbk='0x'+fid, pattern_slots='',
                biome='0x'+biome, rsgd=('0x'+selection['descriptor']['rsgd']) if selection else 'CONTROL_CORPUS',
                selector=item['source_key'], fields_sha256=rh(int(tile[0],16)), linked_fields_sha256=rh(int(fid,16))))
        measurements.append(dict(**item, inverse_cells=inverse, nominal_masks=sorted(nominal), conservative_masks=sorted(conservative)))
    write(OUT / 'domain-measurements.json', measurements)
    # Existing outputs and comparisons are read only after the selection freeze.
    controlrows = []
    configs = [('original-V','0005e0de','resource-region-ancestry','01',(299,325,696,716)),
               ('Carinae','0005e4da','resource-carinae','02',(1270,1280,1301)),
               ('Archimedes','0005de4c','resource-tungsten-acquisition','01',(829,2881,2941))]
    for case, body, folder, attempt, ids in configs:
        output = D5 / ('validation01/cohort/D2-81a75b-request-normalized-stdout.json' if case == 'Archimedes'
            else f'validation01/controls/{body}-request-normalized-stdout.json')
        result = load(output)
        for row in sourcerows:
            if row['case'] != case:
                continue
            paths = [r for r in result['regions'] if r['source'] == row['source_key']]
            row['frozen_generated_paths'] = len(paths)
            row['positive_area_paths'] = sum(r['area'].get('intersection') == 'POSITIVE_AREA' for r in paths)
            row['callback_accepted_paths'] = sum(r['callback'].get('accepted') is True for r in paths)
        for n in ids:
            path = LOCAL / f'{folder}/retail-attempt{attempt}/capture-{n:05d}.bin'
            native = verify.native(path)
            assert pin(path) == expected[str(path.resolve()).replace('\\','/').lower()]
            resource = f'{struct.unpack_from("<I", bytes.fromhex(native["selected"]["raw_resource"]), 0x28)[0]:08x}'
            matches = [r for r in result['regions'] if r['resource'] == resource and
                r['ordered_xyzw_le'] == native['geometry']['ordered_xyzw'] and
                r['native_bound_le'] == native['geometry']['raw_region'][:32]]
            assert len(matches) == 1
            match = matches[0]
            assert match['callback']['accepted'] == (native['decision'] == 'ACCEPT')
            if case == 'Archimedes':
                raw = bytes.fromhex(native['source_context']['raw_source'])
                x, y = struct.unpack_from('<2i', raw, 0x10)
                ox, oy = result['request']['descriptor']
                assert match['source'] == f'0:{ox+x}:{oy+y}:{struct.unpack_from("<I",raw)[0]:08x}'
            row = next(r for r in sourcerows if r['case'] == case and r['source_key'] == match['source'])
            row['native_control_captures'] += (';' if row['native_control_captures'] else '') + str(n)
            pointer = native.get('source_key', native.get('source_pointer'))
            qualified_pointer = f'PID {native["pid"]}:{hex(pointer)}' if pointer is not None else 'UNKNOWN'
            row['actual_pointer'] = qualified_pointer + '; geometry-associated; not an epoch witness'
            controlrows.append(dict(case=case, capture=n, resource='0x'+resource, source_key=match['source'],
                pid=native['pid'], runtime_source_pointer=hex(pointer) if pointer is not None else 'UNKNOWN',
                native_sha256=pin(path), frozen_output_sha256=pin(output), exact_frozen_match=True,
                native_source_context='PRESENT' if 'source_context' in native else 'ABSENT_LEGACY',
                first_miss_query='NOT_WITNESSED_BY_THIS_CONTROL', callback=native['decision']))
    table('source-matrix.csv', sourcerows)
    table('query-domains.csv', domainrows)
    table('feynman-lineage.csv', lineage)
    table('native-controls.csv', controlrows)
    alternatives = checked_load(LOCAL / 'resource-construction-mask-selection/conditional-results.json')
    eqrows = []
    for key in sorted({(r['case'],r['source']) for r in alternatives}):
        pair = [r for r in alternatives if (r['case'],r['source']) == key]
        assert len(pair) == 2
        def shapes(r):
            return [(v['resource'],v['points'],v['cell']) for v in r['regions']]
        def presence(r):
            return sorted(v['resource'] for v in r['summaries'] if v['positive_area_paths'])
        eqrows.append(dict(case=key[0], source_key=key[1], masks=joined(v['mask'] for v in pair),
            ordered_paths_equal=shapes(pair[0]) == shapes(pair[1]),
            path_counts=';'.join(str(len(v['regions'])) for v in pair),
            positive_area_counts=';'.join(str(sum(s['positive_area_paths'] for s in v['summaries'])) for v in pair),
            catalogue_presence_equal=presence(pair[0]) == presence(pair[1]),
            comparison='Frozen D5A ordinary paths; no new generator run; catalogue equality is not geometry equality'))
    table('alternative-equivalence.csv', eqrows)
    assert all(all(0 <= int(v) <= 15 for v in row['nominal_masks'].split(';')) for row in domainrows)
    assert all(len(row['nominal_masks'].split(';')) == 1 for row in domainrows)
    for case in mixed['cases']:
        for source in case['sources']:
            if len(source['neighborhood_low_masks']) <= 1:
                continue
            row = next(r for r in domainrows if r['case'] == case['case'] and r['source_key'] == source['source_key'])
            assert row['conservative_masks'] == joined(source['neighborhood_low_masks'])
    write(OUT / 'input-pins.json', checked)
    provenance = []
    docs = ['resource-standalone/report.md', 'resource-save52/report.md', 'resource-save52-d3/report.md',
            'resource-slot-provenance/report.md', 'resource-feynman-d5/report.md',
            'resource-construction-mask-selection/report.md', 'resource-combined-acquisition/phase-b.md',
            'resource-population-lifecycle/report.md', 'resource-construction-demand/report.md',
            'resource-source-decisions/report.md', 'resource-pattern-selection/native.md',
            'resource-owner-root/source-layout.md']
    paths = [ROOT / 'docs/experiments' / p for p in docs]
    paths += [Path(p) for p in checked]
    paths += [ROOT / 'research' / p for p in ('resource-predictability-contrast/analyze.py',
              'resource-predictability-contrast/audit.py', 'resource-standalone/builder.py',
              'resource-pattern-selection/installed.py', 'resource-owner-root/source_layout.py',
              'resource-slot-provenance/predictor_d4e.py', 'resource-feynman-d5/inputs.py',
              'resource-construction-mask-selection/analyze.py')]
    paths += [ROOT / '.local-work/recon' / p for p in ('resource-region-dependencies-01.tsv',
              'resource-milestone-b-producers-01.tsv', 'resource-availability-cont-01.tsv')]
    paths += [ROOT / '.local-work/workshop-population-rework/specialist' / p
              for p in ('d5-mask01.tsv', 'd5-raster02.tsv')]
    paths += [Path(__file__).parent / 'audit.py']
    for i, path in enumerate(sorted(set(paths)), 1):
        if path.suffix == '.tsv':
            assert pin(path) == expected[str(path.resolve()).replace('\\','/').lower()]
        provenance.append(dict(id=f'D5G-S{i:03}', path=path.relative_to(ROOT).as_posix(), sha256=pin(path),
            use='Owned method or prior first-party research' if '.local-work' not in path.parts else 'Primary/frozen local evidence; payload LOCAL-ONLY'))
    for label, path, digest in [('installed-exe',builder.EXE,builder.EXE_HASH),
            ('installed-main',builder.ESM,builder.DEFINITION),('installed-PlanetData',builder.ARCHIVE,builder.ARCHIVE_HASH)]:
        assert pin(path) == digest
        provenance.append(dict(id=label, path=label, sha256=digest, use='Bethesda installed input; full local path withheld; payload LOCAL-ONLY'))
    table('sources.csv', provenance)
    write(OUT / 'analysis-summary.json', dict(source_rows=len(sourcerows), controls=len(controlrows),
        mixed_sources=13, record_population=tree_ids, linked_tree=f'0x{treeid:08x}',
        linked_sfpt=len({pid for pid, flag in population}), linked_tree_cells=sum(population.values()),
        domain_rows=len(domainrows), all_native_geometry_integrity_matches=True,
        all_reachable_invariance_proofs=0, geometry_rerun=False))
    print(json.dumps(load(OUT / 'analysis-summary.json')))


if __name__ == '__main__':
    main()
