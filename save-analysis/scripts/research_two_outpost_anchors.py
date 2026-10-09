"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0014 original offline probe using this project's EXP0012/13 readers.
Reads explicit Save25, frozen controls, catalog and installed ESM/executable.
Exclusively creates ignored archive/run directories; hashes before decoding;
never writes originals. Stdlib only. 40GB guard, mapped bounded decoder, no
target execution/database/network/Git effects. Names are post-extract labels.
"""
import argparse
import json
from pathlib import Path
import shutil
import struct
import sys

from inventory_historical_saves import ROOT, identity, guard, metadata
from stream_save import decoded_save
from outpost_planetary_location import extract, associations, body_catalog
from outpost_record_framing import iter_records
from outpost_membership import initial_prefix
from validate_mature_outposts import directory, pool
from research_surface_anchors import audit_pair, write, fixed_points
from ordinary_outpost_beacons import summarize


def inspect(b, catalog):
    result = extract(b, catalog)
    result['scoped_detector'] = summarize(b, dict(direct_bases={0x2c60e9: 'OutpostBeaconActivator'}, templates={}))
    d = directory(b)
    _, strings = pool(b, d)
    wanted = {r['token']: r for r in result['beacons']}
    parents = {r['parent_token'] for r in wanted.values()}
    linked = []
    count = 0
    for r in iter_records(b, *d['regions']['region_R3'], d['words'][9]):
        count += 1
        if r['token'] in parents:
            linked.append(r)
        if r['token'] not in wanted:
            continue
        row = wanted[r['token']]
        p = initial_prefix(b, r, 5)
        q = r['body'] + 13
        # Decode only floats whose presence is established by shape bits.
        rotation = []
        for i in range(3):
            if p['shape'] & (1 << i):
                rotation.append(dict(axis=i, offset=q, raw_hex=bytes(b[q:q+4]).hex(),
                                     value=struct.unpack_from('<f', b, q)[0]))
                q += 4
        row.update(record=r, prefix=p, rotation_present_fields=rotation,
                   xyz_offset=r['body']+1, xyz_hex=bytes(b[r['body']+1:r['body']+13]).hex(),
                   name_for_comparison=[strings[i] for i in r['strings']])
        for pt in row['points']:
            q = pt['offset'] + 6
            raw = bytes(b[q:q+16])
            pt.update(pair_offset=q, pair_hex=raw.hex(), **audit_pair(raw))
    result.update(framed_count=count, parent_records=linked, directory=d)
    # Fixed-location control bypasses the ordinary-beacon predicate explicitly.
    if not wanted:
        by_pair, by_id = body_catalog(catalog)
        controls = []
        for r in iter_records(b, *d['regions']['region_R3'], d['words'][9]):
            if r['token'] == '400014' and r['refs']:
                _, points = associations(b, *result['global_units'][6], r['refs'][0], by_pair, by_id)
                for pt in points:
                    raw = bytes(b[pt['offset']+6:pt['offset']+22])
                    pt.update(pair_offset=pt['offset']+6, pair_hex=raw.hex(), **audit_pair(raw))
                controls.append(dict(record_offset=r['offset'], parent=r['refs'][0], points=points))
        result['player_location_control'] = controls
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--run', required=True)
    ap.add_argument('--catalog', type=Path, required=True)
    ap.add_argument('--frozen', type=Path, required=True)
    a = ap.parse_args()
    if not a.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    out = ROOT/'.local-work/two-outpost-anchor'/a.run
    out.mkdir(parents=True, exist_ok=False)
    guard(out)
    cat = json.loads(a.catalog.read_text())
    frozen = json.loads(a.frozen.read_text())
    paths = [a.source, a.catalog, a.frozen, Path(cat['source']['path']),
             Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')]
    comparison_path = ROOT/'.local-work/save-capacity-location/body-final-03/comparison.json'
    comparison = json.loads(comparison_path.read_text())
    network_path = Path(comparison['source']['path'])
    paths.extend([comparison_path, network_path])
    before = {str(p): identity(p) for p in paths}
    if before[str(Path(cat['source']['path']))]['sha256'] != cat['source']['sha256']:
        raise ValueError('ESM_HASH')
    archive = ROOT/'.local-work/savegames/two-outpost-anchor'/a.run
    archive.mkdir(parents=True, exist_ok=False)
    copy = archive/a.source.name
    with a.source.open('rb') as src, copy.open('xb') as dst:
        shutil.copyfileobj(src, dst, 1024*1024)
    copied = identity(copy)
    if copied['sha256'] != before[str(a.source)]['sha256'] or copied['size'] != before[str(a.source)]['size']:
        raise ValueError('COPY_MISMATCH')
    write(out/'manifest.json', dict(source=before[str(a.source)], copy=copied))
    cases = [('Save25', copy, None)]
    unavailable_sources = []
    for s in frozen:
        if s['label'] in ('Save3', 'S1', 'S1C', 'L2C', 'HIST-0245', 'HIST-0267'):
            for role in ('source', 'copy'):
                p = Path(s['source'][role]['path'])
                if role == 'source' and not p.exists():
                    unavailable_sources.append(dict(label=s['label'], expected=s['source'][role]))
                    continue
                v = identity(p)
                if v['sha256'] != s['source'][role]['sha256']:
                    raise ValueError('CONTROL_HASH')
                before[str(p)] = v
            cases.append((s['label'], Path(s['source']['copy']['path']), s['metrics']['decoded_sha256']))
    before[str(copy)] = copied
    write(out/'unavailable-control-originals.json', unavailable_sources)
    results = []
    for label, path, expected in cases:
        with decoded_save(path, out/'scratch') as (b, m):
            if expected and m['decoded_sha256'] != expected:
                raise ValueError('CONTROL_DECODED_HASH')
            r = inspect(b, cat['records'])
            results.append(dict(label=label, metrics=m, metadata=metadata(b), extraction=r))
        guard(out)
        print(label, [(r['token'], r['parent_token'], r['local_xyz']) for r in r['beacons']], flush=True)
    write(out/'results.json', results)
    fixed = fixed_points(Path(cat['source']['path']))
    write(out/'fixed.json', fixed)
    # Validation only, after all save-derived extraction is closed on disk.
    net = json.loads(network_path.read_text())
    network = next(n['network'] for n in net['networks'] if n['id'] == net['activeNetworkId'])
    mature = next(s for s in results if s['label'] == 'HIST-0267')
    validations = []
    for r in mature['extraction']['beacons']:
        name = r['name_for_comparison'][0]['text'] if r['name_for_comparison'] else None
        matches = [p for p in network['outposts'] if p['name'] == name]
        if len(matches) == 1:
            oracle = matches[0]
            body = next(v for v in cat['records'] if v['type'] == 'PNDT' and v['formid'] == r['proposed_body_formid'])
            system = int.from_bytes(bytes.fromhex(body['fields']['GNAM'])[:4], 'little')
            validations.append(dict(token=r['token'], body_match=int(oracle['bodyId'],16)==body['formid'],
                                    system_match=int(oracle['systemId'])==system))
    write(out/'network-validation.json', validations)
    after = {p: identity(Path(p)) for p in before}
    if before != after:
        raise ValueError('INPUT_CHANGED')
    write(out/'preservation.json', dict(before=before, after=after))
    write(out/'tools.json', dict(python=sys.version, argv=sys.argv,
                                scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))


if __name__ == '__main__':
    main()
