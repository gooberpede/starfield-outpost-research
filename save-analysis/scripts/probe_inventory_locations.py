"""Narrow location follow-up to a completed historical inventory.

Reads selected hash-verified authorized originals and local inventory; writes
exclusive local location.json only. Stdlib/project methods; no decoded blobs,
game/database effects or network. Index-end+5 floats are hypotheses, never
planetary coordinates. Names and header locations are separate evidence.
"""
import argparse
import json
import math
from pathlib import Path
import re
import struct
import sys
from inventory_historical_saves import (ROOT, SAVES, MAX_PHYSICAL, MAX_DECODED,
                                        identity, sha, guard, framing, transform, fingerprint, pool, write, positions)


def probe(raw, f, entries):
    rows = []
    animations = {'OBJ_Outpost_Beacon_Deploy', 'OBJ_Outpost_Beacon_On_LP'}
    for v in f['beacon_windows']:
        probes = []
        names = list(v['names'])
        if not names:
            # Exploratory fallback only: valid name index immediately before one
            # or two known animation indices. Ambiguities are retained, never
            # fed back into the frozen inventory's classification.
            a, z = f['directory']['regions']['region_R3']
            start = v['offset']
            for e in entries:
                if e['text'] not in animations:
                    continue
                for rel in positions(raw[start:min(start+512, z)], struct.pack('<H', e['index'])):
                    if rel < 2:
                        continue
                    q = start+rel-2
                    idx = struct.unpack_from('<H', raw, q)[0]
                    if idx >= len(entries) or not entries[idx]['text'] or entries[idx]['text'] in animations:
                        continue
                    ids = [idx, e['index']]
                    if q+6 <= z:
                        following = struct.unpack_from('<H', raw, q+4)[0]
                        if following < len(entries) and entries[following]['text'] in animations:
                            ids.append(following)
                    names.append(dict(name=entries[idx]['text'], indices=ids, index_offset=q,
                                      string_offset=entries[idx]['text_offset'],
                                      method='animation_predecessor_PROVISIONAL'))
        for n in names:
            p = n['index_offset']+2*len(n['indices'])+5
            a, z = f['directory']['regions']['region_R3']
            if not a <= p <= z-12 or p+12 > v['offset']+512:
                raise ValueError('location probe outside observation window')
            xyz = struct.unpack_from('<3f', raw, p)
            probes.append(dict(offset=p, values=[x if math.isfinite(x) else None for x in xyz],
                               bytes_sha256=sha(raw[p:p+12]), finite=all(math.isfinite(x) for x in xyz),
                               method='name_index_subunit_end_plus_5', meaning='PROVISIONAL_LOCAL_XYZ_CANDIDATE'))
        rows.append(dict(token=v['token'], window_offset=v['offset'], names=names, probes=probes))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--ids', required=True)
    ap.add_argument('--output', default='location.json')
    args = ap.parse_args()
    if not re.fullmatch('[A-Za-z0-9_-]+', args.run):
        raise ValueError('run name')
    if not re.fullmatch(r'[A-Za-z0-9_-]+\.json', args.output):
        raise ValueError('simple output filename')
    ids = args.ids.split(',')
    if not 1 <= len(ids) <= 5 or any(not re.fullmatch('HIST-[0-9]{4}', s) for s in ids):
        raise ValueError('one to five inventory IDs')
    out = ROOT/'.local-work/historical-inventory'/args.run
    guard(out)
    manifest = out/'inventory.json'
    before = identity(manifest)
    rows = json.loads(manifest.read_text())
    results = []
    for sid in ids:
        r = next(r for r in rows if r['inventory_id'] == sid)
        p = Path(r['source']['path'])
        if p.resolve().parent != SAVES.resolve() or identity(p) != r['source']:
            raise ValueError('source identity/root')
        if r['source']['size'] > MAX_PHYSICAL or r['framing']['declared_decoded_size'] > MAX_DECODED:
            raise ValueError('resource bound')
        physical = p.read_bytes()
        _, spans = framing(physical)
        raw = transform(physical, spans, True)
        if sha(raw) != r['decoded_sha256']:
            raise ValueError('decoded hash')
        f = fingerprint(raw)
        _, entries = pool(raw, f['directory'])
        results.append(dict(inventory_id=sid, source_sha256=r['source']['sha256'],
                            decoded_sha256=sha(raw), header_location=r['metadata']['save_display_location'],
                            beacons=probe(raw, f, entries), literal_probes=f['literal_probes']))
        if identity(p) != r['source']:
            raise ValueError('source changed')
        del raw, physical
    if identity(manifest) != before:
        raise ValueError('manifest changed')
    write(out/args.output, dict(inventory=before, script=identity(Path(__file__)),
          python=identity(Path(sys.executable)), results=results))
    print('Location probes', sum(len(b['probes']) for r in results for b in r['beacons']), 'across', len(ids), 'saves')


if __name__ == '__main__':
    main()
