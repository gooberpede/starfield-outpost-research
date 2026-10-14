"""SPDX-License-Identifier: GPL-3.0-or-later
Read-only, BCPS1 save-menu support; stdlib and existing project readers only.
Reads exact save paths / optional identity mappings; hashes before and after.
Decodes only the first stream in memory. Writes exclusive JSON only when asked.
No scratch, game, database, configuration, network or save writes. See report.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zlib

from inventory_historical_saves import metadata
from stream_save import BLOCK, CorruptSave, header

VERSION = '1.0.0'


def fixed_zone(text):
    m = re.fullmatch(r'([+-])(\d{2}):(\d{2})', text)
    if not m or int(m[2]) > 23 or int(m[3]) > 59:
        raise ValueError('UTC offset must be +/-HH:MM, less than 24 hours')
    minutes = (int(m[2]) * 60 + int(m[3])) * (1 if m[1] == '+' else -1)
    return dt.timezone(dt.timedelta(minutes=minutes))


def display_time(ns, zone):
    # Integer arithmetic preserves second boundaries; no rounding from floats.
    utc = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(seconds=ns // 10**9)
    local = utc.astimezone(zone)
    return (f'{local.month}/{local.day}/{local.year % 100:02d}, '
            f'{local.hour % 12 or 12}:{local.minute:02d}:{local.second:02d} '
            f'{"AM" if local.hour < 12 else "PM"}')


def identity(path):
    s = path.stat()
    with path.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return dict(path=str(path.resolve()), filename=path.name, size=s.st_size,
                sha256=digest, mtime_ns=s.st_mtime_ns)


def first_stream(path):
    with path.open('rb') as f:
        info = header(f)
        f.seek(72)
        n = int.from_bytes(f.read(4), 'little')
        if n > BLOCK + 1024:
            raise CorruptSave('FIRST_COMPRESSED_STREAM_BOUND')
        f.seek(info['stream_start'])
        compressed = f.read(n)
    expected = min(BLOCK, info['declared_decoded_size'])
    dec = zlib.decompressobj()
    b = dec.decompress(compressed, expected + 1)
    if (not dec.eof or dec.unused_data or dec.unconsumed_tail or len(b) != expected
            or not b.startswith(b'SFS_SAVEGAME')):
        raise CorruptSave('FIRST_STREAM_INTEGRITY')
    return b, info


def parse_metadata(b):
    if len(b) < 25 or not b.startswith(b'SFS_SAVEGAME'):
        raise CorruptSave('DECODED_HEADER')
    if struct.unpack_from('<I', b, 16)[0] != 27:
        raise CorruptSave('UNSUPPORTED_HEADER_WORD_16')
    raw = metadata(b)
    # Existing metadata reader preserves undecodable bytes as diagnostic text.
    # For operator-facing labels, validate original UTF-8 and reject controls.
    for key in ('character_name', 'save_display_location', 'playtime_text', 'race_text'):
        p = raw[key]['offset']
        n = int.from_bytes(b[p:p+2], 'little')
        text = b[p+2:p+2+n].decode('utf-8')
        if any(ord(c) < 32 or ord(c) == 127 for c in text):
            raise CorruptSave('CONTROL_CHARACTER_IN_HEADER')
        raw[key].update(text=text, byte_length=n, encoding='UTF-8')
    p = raw['race_text']['offset'] + 2 + raw['race_text']['byte_length'] + 10
    if p + 8 > min(len(b), 8192):
        raise CorruptSave('TIMESTAMP_BOUNDS')
    ticks = struct.unpack_from('<Q', b, p)[0]
    try:
        timestamp = dt.datetime(1601, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(microseconds=ticks // 10)
        iso = timestamp.isoformat()
    except OverflowError:
        iso = None
    raw['header_filetime_candidate'] = dict(offset=p, value=ticks, utc_candidate=iso,
        meaning='NOT_MENU_TIME', domain='decompressed-stream offset', unit='100ns since 1601 UTC (candidate)')
    return raw


def field(value, source, confidence):
    return dict(value=value, source=source, confidence=confidence if value is not None else 'UNKNOWN')


def inspect(spec, zone, zone_name):
    path = Path(spec['path']).resolve()
    row = dict(research_id=spec.get('label'), source_path=(spec.get('source') or {}).get('path', str(path)),
               read_path=str(path), status='ERROR', warnings=[], fields={})
    before = None
    try:
        before = identity(path)
        row['input'] = before
        if path.suffix.lower() != '.sfs':
            raise ValueError('input must be .sfs')
        if spec.get('sha256') and before['sha256'] != spec['sha256']:
            raise ValueError('INPUT_HASH_MISMATCH')
        b, container = first_stream(path)
        raw = parse_metadata(b)
        row.update(raw_metadata=raw, container=container,
                   first_stream_sha256=hashlib.sha256(b).hexdigest())
        fields = row['fields']
        for name, key, member in [('character', 'character_name', 'text'),
                                  ('location', 'save_display_location', 'text'),
                                  ('level', 'level_candidate', 'value')]:
            value = raw[key][member]
            if value == '' or (name == 'level' and value == 0):
                value = None
            fields[name] = field(value, f'decompressed header +{raw[key]["offset"]}', 'HEADER_OBSERVED')
        play = raw['playtime_text']['text']
        match = re.match(r'^(\d+)d\.(\d+)h\.(\d+)m\.', play)
        short = None
        if match:
            days, hours, minutes = map(int, match.groups())
            if hours < 24 and minutes < 60:
                short = ' '.join([f'{days}d'] * bool(days) + [f'{hours}h', f'{minutes}m'])
        fields['playtime'] = field(short, 'English header text prefix; no elapsed-time calculation', 'HEADER_DERIVED')
        kind = re.match(r'^(Save\d+|Autosave\d+|Exitsave\d+|Quicksave\d+)_', path.name, re.I)
        kind = (('AUTO SAVE' if kind[1].lower().startswith('auto') else
                 'EXIT SAVE' if kind[1].lower().startswith('exit') else
                 'QUICK SAVE' if kind[1].lower().startswith('quick') else 'SAVE') if kind else None)
        fields['save_kind'] = field(kind, 'filename prefix; NOT a decoded header field', 'FILENAME_INFERRED')
        source = spec.get('source')
        stamp = None
        if source:
            if source.get('sha256') != before['sha256']:
                raise ValueError('SOURCE_TIMESTAMP_NOT_HASH_BOUND')
            if isinstance(source.get('mtime_ns'), int):
                stamp = source['mtime_ns']
            stamp_source = 'hash-bound original source identity in mapping'
        else:
            stamp = before['mtime_ns']
            stamp_source = 'input file last-write time'
            row['warnings'].append('File-mtime model: use original player-visible file; copied/restored/retimed files may differ. Prefer hash-bound original source metadata.')
        local_zone = fixed_zone(spec['utc_offset']) if 'utc_offset' in spec else zone
        row['timezone'] = spec.get('utc_offset', zone_name)
        row['timestamp_ns_used'] = stamp
        fields['timestamp'] = field(display_time(stamp, local_zone) if stamp is not None else None,
                                    stamp_source, 'MENU_MTIME_MODEL')
        control = spec.get('control')
        if control:
            if not control.get('evidence') or not control.get('sha256'):
                raise ValueError('CONTROL_REQUIRES_EVIDENCE_HASH')
            if identity(Path(control['evidence']))['sha256'] != control['sha256']:
                raise ValueError('CONTROL_EVIDENCE_HASH_MISMATCH')
            row['control'] = control
            for key, value in control.get('fields', {}).items():
                if key not in fields or fields[key]['value'] != value:
                    raise ValueError('CONTROL_MISMATCH: ' + key)
                fields[key]['confidence'] = 'CONTROL_MATCHED'
        essential = all(fields[k]['value'] is not None for k in ('character', 'timestamp'))
        row['status'] = 'OK' if essential else 'INCOMPLETE'
    except (OSError, ValueError, KeyError, TypeError, struct.error, zlib.error, OverflowError) as e:
        row['error'] = str(e)
        row['status'] = 'ERROR'
    if before is not None:
        try:
            row['preserved'] = identity(path) == before
        except OSError:
            row['preserved'] = False
        if not row['preserved']:
            row.update(status='ERROR', error='INPUT_CHANGED_DURING_READ')
    return row


def instructions(rows):
    groups = {}
    for row in rows:
        if row['status'] == 'OK':
            f = row['fields']
            groups.setdefault((f['character']['value'], f['timestamp']['value']), []).append(row)
    for group in groups.values():
        if len({r['input']['sha256'] for r in group}) > 1:
            for r in group:
                r['warnings'].append('COLLISION: character/timestamp shared by different save bytes; compare location/level/playtime and neighboring timestamps. Filename/hash are offline clues, not displayed menu IDs. Do not choose by ordinal.')
                r['collision'] = [dict(path=x['read_path'], sha256=x['input']['sha256']) for x in group if x is not r]
        elif len(group) > 1:
            for r in group:
                r['warnings'].append('Duplicate input content; not a distinct-save collision.')
    for row in rows:
        if row['status'] != 'OK':
            row['instruction'] = f'No load instruction: {row.get("research_id") or row["read_path"]} — {row.get("error", "essential field UNKNOWN")}'
            continue
        f = row['fields']
        parts = [f'{f["character"]["value"]}' + (f' {row["research_id"]}' if row.get('research_id') else '')]
        if f['location']['value'] is not None:
            parts.append(f['location']['value'])
        if f['level']['value'] is not None:
            parts.append(f'Level {f["level"]["value"]}')
        parts.append(f['timestamp']['value'])
        prefix = 'Ambiguous load candidate: ' if row.get('collision') else 'Load '
        row['instruction'] = prefix + ' — '.join(parts)
        if f['timestamp']['confidence'] != 'CONTROL_MATCHED':
            row['instruction'] += ' [file-mtime model; not screenshot-verified]'


def load_mapping(path):
    """Accept a list, {samples:[...]}, or a label->path/record mapping.
    Existing project source/source_before + copy identities retain original mtime.
    Paths resolve relative to caller cwd, as in existing repository manifests.
    """
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data, dict):
        data = data['samples'] if 'samples' in data else [dict(label=k, **(v if isinstance(v, dict) else {'path': v})) for k, v in data.items()]
    result = []
    for entry in data:
        entry = dict(entry)
        source = entry.get('source_before', entry.get('source'))
        read = entry.get('copy', source)
        if 'path' not in entry:
            entry.update(path=read['path'], sha256=read['sha256'])
        if source:
            entry['source'] = source
        result.append(entry)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('paths', nargs='*', help='exact original save paths')
    ap.add_argument('--mapping', help='JSON research label mapping / existing samples manifest')
    ap.add_argument('--utc-offset', required=True,
                    help='explicit current menu offset, e.g. +11:00; applied to ALL save dates')
    ap.add_argument('--json', help='new JSON file, exclusive creation; private output remains local')
    args = ap.parse_args(argv)
    try:
        if args.json and Path(args.json).suffix.lower() != '.json':
            raise ValueError('output must have .json extension; save/artifact paths are not outputs')
        zone = fixed_zone(args.utc_offset)
        specs = load_mapping(args.mapping) if args.mapping else []
        specs += [dict(path=p) for p in args.paths]
        if not specs:
            ap.error('supply paths or --mapping')
        rows = [inspect(s, zone, args.utc_offset) for s in specs]
        instructions(rows)
        result = dict(version=VERSION, publication='LOCAL-ONLY', locale='M/D/YY, h:mm:ss AM/PM',
                      timezone=args.utc_offset, rows=rows,
                      tool=dict(python=sys.version, executable=identity(Path(sys.executable)),
                                scripts=[identity(Path(__file__)), identity(Path(__file__).with_name('stream_save.py')),
                                         identity(Path(__file__).with_name('inventory_historical_saves.py'))]))
        if args.json:
            with Path(args.json).open('x', encoding='utf-8', newline='\n') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
                f.write('\n')
        for row in rows:
            print(row['instruction'])
            for warning in row['warnings']:
                print('  Warning: ' + warning)
        return 1 if any(r['status'] != 'OK' or r.get('collision') for r in rows) else 0
    except (OSError, ValueError, KeyError, TypeError) as e:
        print('save-menu error: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
