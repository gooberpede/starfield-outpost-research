"""SPDX-License-Identifier: GPL-3.0-or-later
Offline detector CLI. Reads frozen identity manifests, prior archive locators,
verified archived saves and existing ESM definition summary. Hashes originals
for preservation only; never analyzes live originals or creates save copies.
Writes fresh ignored JSON results/provenance under .local-work/ordinary-beacons.
Stdlib/project readers only; <=128MiB physical, <=64MiB decoded, >=40GB C/D,
128MiB output and cooperative 1800s run bound. No live/database/network effects.
Labels select inputs only; no expected gameplay labels/counts enter detection.
"""
from pathlib import Path
import argparse
import datetime as dt
import json
import re
import struct
import sys
import time
from investigate_active_outposts import specs
from inventory_historical_saves import identity, guard, framing, transform, metadata, sha, MAX_PHYSICAL, MAX_DECODED
from ordinary_outpost_beacons import catalog_for, summarize, compact, SCHEMA

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', required=True)
    ap.add_argument('--labels', help='comma-separated existing manifest IDs; omit for full bounded corpus')
    ap.add_argument('--definitions', type=Path,
                    default=ROOT / '.local-work/membership-completion/definitions-01/definitions.json')
    ap.add_argument('--archives', type=Path,
                    default=ROOT / '.local-work/membership-completion/challenge-final/preservation.json')
    args = ap.parse_args()
    if not re.fullmatch('[a-z0-9-]+', args.run):
        raise ValueError('invalid run name')
    selected = list(specs())
    if args.labels:
        labels = set(args.labels.split(','))
        selected = [s for s in selected if s['label'] in labels]
        if labels != {s['label'] for s in selected}:
            raise ValueError('unknown requested label')
    out = ROOT / '.local-work/ordinary-beacons' / args.run
    out.mkdir(parents=True, exist_ok=False)
    guard(out)
    start = time.monotonic()
    archives = {}
    for r in json.loads(args.archives.read_text()):
        v = r['copy_before']
        archives[v['sha256']] = Path(v['path'])
    definitions = json.loads(args.definitions.read_text())
    tools = [Path(sys.executable), args.definitions, args.archives] + sorted(Path(__file__).parent.glob('*.py'))
    manifests = [ROOT / p for p in [
        '.local-work/exp0002/integrity-before.json', '.local-work/manual-S0-S7C/manifest.json',
        '.local-work/output-link-L0-L2C/manifest.json',
        '.local-work/historical-inventory/scan-04/inventory.json',
        '.local-work/third-party/the-daily-xperience-1798/scan-03/inventory.json']]
    before = {str(p.resolve()): identity(p) for p in tools + manifests}
    cache, rows = {}, []
    for s in selected:
        guard(out)
        if time.monotonic() - start > 1800:
            raise RuntimeError('SCAN_TIME_BOUND')
        h = s['copy']['sha256']
        archive = archives.get(h)
        if archive is None or not archive.is_relative_to(ROOT / '.local-work'):
            raise ValueError('missing local archive: ' + s['label'])
        for p in (Path(s['source']['path']), archive):
            key = str(p.resolve())
            if key not in before:
                v = identity(p)
                if v['sha256'] != h or v['size'] != s['copy']['size']:
                    raise ValueError('identity mismatch: ' + s['label'])
                before[key] = v
        if h not in cache:
            result = dict(schema=SCHEMA, headline='SCAN_UNSUPPORTED', ordinary_count=None,
                authoritative_player_membership='INDETERMINATE', candidates=[],
                coverage=dict(exact_r3_closure=False, complete_ordinary_enumeration=False))
            try:
                if archive.stat().st_size > MAX_PHYSICAL:
                    raise ValueError('PHYSICAL_SIZE_LIMIT')
                physical = archive.read_bytes()
                if sha(physical) != h:
                    raise RuntimeError('read identity mismatch')
                f, spans = framing(physical)
                if f['declared_decoded_size'] > MAX_DECODED:
                    raise ValueError('DECODED_SIZE_LIMIT')
                decoded = transform(physical, spans, True)
                catalog, plugins = catalog_for(decoded, definitions)
                result = summarize(decoded, catalog)
                result.update(decoded_sha256=sha(decoded), container=f,
                    header_versions=metadata(decoded)['build_strings'],
                    conditional_plugin_sequence=plugins)
                for r in result['candidates']:
                    loc = r['location']
                    first = loc['record_start'] // f['block_size']
                    last = (loc['record_end'] - 1) // f['block_size']
                    loc['compressed_streams'] = [dict(index=i, physical_start=spans[i][0],
                        compressed_bytes=spans[i][1], logical_start=i*f['block_size'])
                        for i in range(first, last+1)]
                    loc['record_start_in_first_decoded_stream'] = loc['record_start'] % f['block_size']
                    loc['physical_domain'] = 'COMPRESSED_STREAM_SPAN; NO_LINEAR_RECORD_FILE_OFFSET'
                del decoded, physical
            except (ValueError, struct.error) as e:
                result['headline'] = 'SCAN_UNSUPPORTED'
                result['ordinary_count'] = None
                result['reason_codes'] = [str(e)]
            cache[h] = result
        rows.append(dict(save_id=s['label'], sample_id=s.get('sample_id'),
                         source_sha256=h, source_bytes=s['copy']['size'], result=cache[h]))
        if args.labels:
            print(s['label'], compact(cache[h]) if cache[h]['ordinary_count'] is not None else 'SCAN_UNSUPPORTED', flush=True)
        elif len(rows) % 50 == 0:
            print('processed', len(rows), flush=True)
    after = {key: identity(Path(key)) for key in before}
    if before != after:
        raise RuntimeError('INPUT_OR_TOOL_CHANGED')
    for name, data in [('results.json', rows), ('preservation.json', dict(before=before, after=after)),
                       ('run.json', dict(argv=sys.argv, python=sys.version,
                         created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                         labels=len(rows), unique_hashes=len(cache), schema=SCHEMA,
                         seconds=time.monotonic()-start))]:
        payload = json.dumps(data, indent=2, allow_nan=False) + '\n'
        if len(payload.encode('utf-8')) > 32 * 1024 * 1024:
            raise RuntimeError('RECEIPT_SIZE_LIMIT')
        (out / name).write_text(payload, encoding='utf-8', newline='\n')
        guard(out)
    print('complete', len(rows), 'labels;', len(cache), 'hashes;', out)


if __name__ == '__main__':
    main()
