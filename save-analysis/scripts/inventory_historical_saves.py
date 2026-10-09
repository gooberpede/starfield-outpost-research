"""Bounded offline inventory; CPython stdlib, no game/tool/database effects.

Reads only authorized Saves/*.sfs, existing archive .sfs and project methods.
Writes fresh/resumable ignored JSONL receipts and JSON beneath historical-inventory.
No decoded blobs, copies, original writes, network or dependencies. File hashes
are verified again at completion. Names/paths/string evidence stay LOCAL-ONLY.
Reuses SOR-EXP-0006 directory/grammar/pool; window method is source-informed.
"""
from pathlib import Path
import argparse
import collections
import datetime as dt
import hashlib
import json
import math
import os
import re
import shutil
import struct
import sys
import time
import zlib
from validate_mature_outposts import directory, envelopes, pool, positions

ROOT = Path(__file__).resolve().parents[2]
SAVES = Path('C:/Users/User/Documents/My Games/Starfield/Saves')
MAX_PHYSICAL = 128 * 1024 * 1024
MAX_DECODED = 64 * 1024 * 1024
MAX_OUTPUT = 128 * 1024 * 1024
MAX_SECONDS = 1800


def sha(b):
    return hashlib.sha256(b).hexdigest()


def identity(p):
    s = p.stat()
    with p.open('rb') as f:
        h = hashlib.file_digest(f, 'sha256').hexdigest()
    return dict(path=str(p.resolve()), size=s.st_size, sha256=h,
                mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns,
                mtime_utc=dt.datetime.fromtimestamp(s.st_mtime, dt.timezone.utc).isoformat(),
                ctime_utc=dt.datetime.fromtimestamp(s.st_ctime, dt.timezone.utc).isoformat())


def guard(out=None):
    for d in ('C:/', 'D:/'):
        if shutil.disk_usage(d).free < 40_000_000_000:
            raise RuntimeError('free-space stop on ' + d)
    if out and sum(p.stat().st_size for p in out.rglob('*') if p.is_file()) > MAX_OUTPUT:
        raise RuntimeError('output bound stop')


def framing(b):
    if len(b) < 72 or b[:8] != b'BCPS\x01\0\0\0' or b[68:72] != b'ZIP ':
        raise ValueError('unsupported physical signature')
    table, start, total, block = (struct.unpack_from('<Q', b, p)[0] for p in (8, 24, 32, 48))
    if table != 72 or block != 262144 or not 0 < total <= 1024**3:
        raise ValueError('unsupported physical fields/bounds')
    count = math.ceil(total / block)
    end = table + 4 * count
    if not 0 <= start - end <= 15 or start % 16 or end > len(b):
        raise ValueError('unsupported table alignment')
    spans = []
    p = start
    for i in range(count):
        n = struct.unpack_from('<I', b, table + 4*i)[0]
        if n == 0 or p+n > len(b):
            raise ValueError('physical stream bounds')
        z = (p+n+15)//16*16
        if z > len(b):
            raise ValueError('physical padding bounds')
        spans.append((p, n, min(block, total-i*block)))
        p = z
    if p != len(b):
        raise ValueError('physical EOF not consumed')
    return dict(container_version=1, declared_decoded_size=total, block_size=block,
                streams=count, table_end=end, stream_start=start,
                alignment_bytes=start-end), spans


def transform(b, spans, full):
    parts = []
    for p, n, expected in spans if full else spans[:1]:
        dec = zlib.decompressobj()
        raw = dec.decompress(b[p:p+n], expected+1)
        if not dec.eof or dec.unused_data or dec.unconsumed_tail or len(raw) != expected:
            raise ValueError('stream checksum/EOF/length mismatch')
        parts.append(raw)
    raw = b''.join(parts)
    if not raw.startswith(b'SFS_SAVEGAME'):
        raise ValueError('unsupported decoded signature')
    return raw


def metadata(b):
    # Observed header fields, not filename conventions or executable identity.
    p = 25
    fields = {}
    def string(label):
        nonlocal p
        if p+2 > min(len(b), 8192):
            raise ValueError('header field bounds')
        n = int.from_bytes(b[p:p+2], 'little')
        if p+2+n > min(len(b), 8192):
            raise ValueError('header string bounds')
        fields[label] = dict(offset=p, text=b[p+2:p+2+n].decode('utf-8', 'backslashreplace'))
        p += 2+n
    string('character_name')
    fields['level_candidate'] = dict(offset=p, value=struct.unpack_from('<I', b, p)[0])
    p += 4
    string('save_display_location')
    string('playtime_text')
    string('race_text')
    fields['header_word_16'] = dict(offset=16, value=struct.unpack_from('<I', b, 16)[0], meaning='UNKNOWN')
    # Only two adjacent uint16-length-prefixed strings before the directory;
    # later plugin version text is unrelated and must not become game versions.
    versions = []
    for m in re.finditer(rb'\d+\.\d+\.\d+\.\d+', b[p:min(len(b), p+96)]):
        q = p+m.start()
        if int.from_bytes(b[q-2:q], 'little') == len(m.group()):
            versions.append(dict(offset=q, text=m.group().decode(), role='HEADER_VERSION_ROLE_UNKNOWN'))
    fields['build_strings'] = versions[:2]
    return fields


def candidate_windows(b, a, z, base, marker):
    rows = []
    for rel in positions(b[a:z], bytes.fromhex(base)):
        q = a+rel
        if q+6 > z:
            continue
        token = b[q+3:q+6]
        matches = []
        for p in range(max(a, q-32), q):
            if b[p] == marker and b[p+1:p+4] == token and token in b[p+4:min(p+48, z)]:
                matches.append(p)
        for p in matches:
            rows.append(dict(offset=p, base_offset=q, base_relative=q-p,
                             token=token.hex(), prefix_matches=len(matches)))
    return rows


def fingerprint(b):
    d = directory(b)
    es = envelopes(b, d)
    qualified = [e for e in es if e['qualifies']]
    valid = [e for e in qualified if 'parsed' in e]
    ps, entries = pool(b, d)
    a, z = d['regions']['region_R3']
    beacons = candidate_windows(b, a, z, '6c60e9', 0x3a)
    animations = {'OBJ_Outpost_Beacon_Deploy', 'OBJ_Outpost_Beacon_On_LP'}
    for v in beacons:
        p = v['offset']
        ns = []
        for tail in positions(b[p:min(p+512, z)], bytes.fromhex('1100190004')):
            for width in (2, 4, 6):
                if tail < width:
                    continue
                ids = struct.unpack_from('<'+'H'*(width//2), b, p+tail-width)
                if (all(i < len(entries) for i in ids) and entries[ids[0]]['text'] not in animations
                        and all(entries[i]['text'] in animations for i in ids[1:])):
                    ns.append(dict(name=entries[ids[0]]['text'], indices=list(ids),
                                   index_offset=p+tail-width, string_offset=entries[ids[0]]['text_offset']))
        for n in ns:
            n['method'] = 'mature_terminator'
        if not ns:
            # Existing structural-containment method: the exact name/animation
            # index triple. No complete object framing or terminator is implied.
            for idx in range(len(entries)-2):
                if (entries[idx]['text'] not in animations and entries[idx+1]['text'] == 'OBJ_Outpost_Beacon_Deploy'
                        and entries[idx+2]['text'] == 'OBJ_Outpost_Beacon_On_LP'):
                    for rel in positions(b[p:min(p+512, z)], struct.pack('<3H', idx, idx+1, idx+2)):
                        ns.append(dict(name=entries[idx]['text'], indices=[idx, idx+1, idx+2],
                                       index_offset=p+rel, string_offset=entries[idx]['text_offset'],
                                       method='controlled_index_triple'))
        v['names'] = ns
        # Reproduce the exact controlled beacon tuple only. Arbitrary fixed
        # offsets in variable object windows are not coordinate measurements.
        v['controlled_xyz_pattern_offsets'] = [p+r for r in positions(b[p:min(p+512, z)],
                                                    bytes.fromhex('5d62f54290a08a436ed09241'))]
    members = set(valid[0]['parsed']['beacons']) if len(valid) == len(qualified) == 1 else set()
    bt = {v['token'] for v in beacons}
    pads = []
    for base, typ in [('6a6c3f', 'regular'), ('619523', 'interstellar')]:
        for v in candidate_windows(b, a, z, base, 0x2a):
            p = v['offset']
            v['type'] = typ
            v['associations'] = [t for t in sorted(bt) if bytes.fromhex('454ba6'+t) in b[p:min(p+128, z)]]
            v['keyword_refs'] = [b[p+r+3:p+r+6].hex()
                                 for r in positions(b[p:min(p+128, z)], bytes.fromhex('655cc8')) if p+r+6 <= z]
            pads.append(v)
    pd = {v['token']: v for v in pads}
    arrows, unresolved, self_refs = {}, [], 0
    for v in pads:
        self_refs += v['keyword_refs'].count(v['token'])
        ns = [t for t in v['keyword_refs'] if t != v['token'] and 0x80 <= int(t[:2], 16) < 0xc0]
        if len(ns) > 1 or any(t not in pd for t in ns):
            unresolved.append(dict(token=v['token'], refs=ns))
        elif ns:
            arrows[v['token']] = ns[0]
    pairs = sorted([s, t] for s, t in arrows.items() if s < t and arrows.get(t) == s)
    unresolved += [dict(nonreciprocal=[s, t]) for s, t in arrows.items() if arrows.get(t) != s]
    # Literal probes are negative-search evidence only, not coordinate exclusion.
    literals = {s: positions(b, s.encode())[:32] for s in ('latitude', 'longitude', 'KreetPlanetWorld')}
    errors = []
    if len(qualified) != 1 or len(valid) != 1:
        errors.append('relationship envelope missing/ambiguous/grammar unsupported')
    if len(bt) != len(beacons) or any(v['prefix_matches'] != 1 for v in beacons):
        errors.append('beacon token/window ambiguity')
    if any(len(v['names']) != 1 for v in beacons):
        errors.append('beacon name/index ambiguity')
    if len(pd) != len(pads):
        errors.append('pad token ambiguity')
    if not members <= bt:
        errors.append('unresolved collection beacon references')
    parsed = valid[0]['parsed'] if len(valid) == 1 else None
    return dict(directory=d, region_sizes={k: z-a for k, (a, z) in d['regions'].items()},
                envelopes=qualified, relationship_payload=qualified[0]['length'] if len(qualified) == 1 else None,
                beacon_collection_count=len(parsed['beacons']) if parsed else None,
                keyed_groups=len(parsed['groups']) if parsed else None,
                endpoints=sum(len(g['refs']) for g in parsed['groups']) if parsed else None,
                shared_strings=dict(**ps, size=ps['end']-ps['start']),
                beacon_windows=beacons, beacon_count=len(beacons), nonmember_beacons=len(bt-members),
                marker_count=len(pads), marker_types=dict(collections.Counter(v['type'] for v in pads)),
                associated_marker_types=dict(collections.Counter(v['type'] for v in pads if len(v['associations']) == 1 and v['associations'][0] in members)),
                pads=pads, reciprocal_pairs=pairs, unresolved=unresolved, self_reference_occurrences=self_refs,
                animation_string_count=sum(e['text'] in animations for e in entries),
                literal_probes=literals, errors=errors)


def classify(f, builds):
    if f is None:
        return 'INDETERMINATE'
    named = any(len(v['names']) == 1 and v['names'][0]['name'] for v in f['beacon_windows'])
    if named:
        # Presence of saved outpost state; active/runtime membership not established.
        return 'OUTPOSTS_CONFIRMED_PRESENT'
    if f['beacon_count'] or f['marker_count'] or (f['beacon_collection_count'] or 0):
        return 'POSSIBLE_RESIDUAL_OR_INACTIVE_STATE'
    # Either no keyed relationships at all, or the observed no-outpost control
    # cardinalities. Unexplained nonempty historical groups remain indeterminate.
    if (not f['errors'] and f['animation_string_count'] == 0
            and f['beacon_collection_count'] == 0 and (f['keyed_groups'], f['endpoints']) in ((0, 0), (1, 1))
            and set(builds) == {'1.16.244.0'}):
        return 'NO_ACTIVE_OUTPOSTS_SUPPORTED'
    return 'INDETERMINATE'


def inspect(p, sid):
    before = identity(p)
    row = dict(inventory_id=sid, source=before, status='UNDETERMINED', depth='HASH_ONLY',
               classification='INDETERMINATE', errors=[])
    started = time.monotonic()
    if before['size'] > MAX_PHYSICAL:
        row['errors'].append('physical size bound')
        return row
    physical = p.read_bytes()
    if sha(physical) != before['sha256']:
        raise RuntimeError('input changed during read')
    try:
        frame, spans = framing(physical)
        row['framing'] = frame
        full = frame['declared_decoded_size'] <= MAX_DECODED
        raw = transform(physical, spans, full)
        row['depth'] = 'FULL_BOUNDED_FINGERPRINT' if full else 'FIRST_STREAM_HEADER'
        row['metadata'] = metadata(raw)
        if full:
            row['decoded_sha256'] = sha(raw)
            try:
                f = fingerprint(raw)
                row['fingerprint'] = f
                row['status'] = 'PARTIAL' if f['errors'] else 'SUPPORTED'
                row['classification'] = classify(f, [v['text'] for v in row['metadata']['build_strings']])
            except (ValueError, struct.error, IndexError) as e:
                row['status'] = 'PARTIAL'
                row['errors'].append(type(e).__name__+': '+str(e))
        else:
            row['status'] = 'PARTIAL'
            row['errors'].append('declared decoded size exceeds 64MiB; first stream only')
    except (ValueError, zlib.error, struct.error, IndexError) as e:
        row['status'] = 'UNSUPPORTED'
        row['errors'].append(type(e).__name__+': '+str(e))
        # Decoder failure is never a corruption or absence verdict.
    if identity(p) != before:
        raise RuntimeError('source preservation failure')
    row['seconds'] = time.monotonic()-started
    return row


def write(p, v):
    guard(p.parent)
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, indent=2, allow_nan=False)
        f.write('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--resume', action='store_true')
    args = ap.parse_args()
    if not re.fullmatch('[A-Za-z0-9_-]+', args.run):
        raise ValueError('simple run name required')
    guard()
    out = ROOT/'.local-work/historical-inventory'/args.run
    out.mkdir(parents=True, exist_ok=args.resume)
    files = sorted(SAVES.glob('*.sfs'), key=lambda p: p.name)
    methods = list(Path(__file__).parent.glob('*.py'))
    provenance = dict(sources=[identity(p) for p in methods], python=identity(Path(sys.executable)),
                      python_version=sys.version, zlib=zlib.ZLIB_RUNTIME_VERSION,
                      files=[str(p.resolve()) for p in files], limits=dict(physical=MAX_PHYSICAL, decoded=MAX_DECODED,
                      output=MAX_OUTPUT, seconds=MAX_SECONDS),
                      brief=identity(ROOT/'docs/implementation-briefs/CODEX_RESEARCH_BRIEF_historical_save_inventory_triage.md'))
    if args.resume:
        if json.loads((out/'provenance.json').read_text()) != provenance:
            raise RuntimeError('resume inputs/tooling changed')
    else:
        write(out/'provenance.json', provenance)
    receipt = out/'progress.jsonl'
    rows = [json.loads(line) for line in receipt.read_text().splitlines()] if receipt.exists() else []
    if any(r['source'] != identity(files[i]) for i, r in enumerate(rows)):
        raise RuntimeError('resume source changed')
    start = time.monotonic()
    with receipt.open('a', encoding='utf-8', newline='\n') as f:
        for i in range(len(rows), len(files)):
            guard(out)
            if time.monotonic()-start > MAX_SECONDS:
                raise RuntimeError('runtime stop; resume with same tools/inputs')
            r = inspect(files[i], f'HIST-{i+1:04d}')
            rows.append(r)
            f.write(json.dumps(r, allow_nan=False)+'\n')
            f.flush()
            os.fsync(f.fileno())
            if (i+1) % 10 == 0:
                print(i+1, '/', len(files), r['status'], flush=True)
    if [str(p.resolve()) for p in sorted(SAVES.glob('*.sfs'), key=lambda p: p.name)] != provenance['files']:
        raise RuntimeError('directory changed')
    for r in rows:
        if identity(Path(r['source']['path'])) != r['source']:
            raise RuntimeError('final source preservation failure')
    if [identity(p) for p in methods] != provenance['sources']:
        raise RuntimeError('tooling changed')
    archives = collections.defaultdict(list)
    for p in sorted((ROOT/'.local-work/savegames').rglob('*.sfs')):
        archives[identity(p)['sha256']].append(str(p.resolve()))
    hashes = collections.defaultdict(list)
    for r in rows:
        hashes[r['source']['sha256']].append(r['inventory_id'])
    for r in rows:
        h = r['source']['sha256']
        r['duplicate_content_ids'] = hashes[h]
        r['existing_archives'] = archives[h]
    write(out/'inventory.json', rows)
    write(out/'completion.json', dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
          count=len(rows), seconds=time.monotonic()-start, originals_preserved=True,
          status=dict(collections.Counter(r['status'] for r in rows)),
          classification=dict(collections.Counter(r['classification'] for r in rows)),
          outputs={p.name: identity(p) for p in out.iterdir() if p.is_file()},
          free_bytes={d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}))
    print('COMPLETE', len(rows), dict(collections.Counter(r['status'] for r in rows)), flush=True)


if __name__ == '__main__':
    main()
