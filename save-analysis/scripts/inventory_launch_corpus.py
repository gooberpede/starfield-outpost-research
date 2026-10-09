"""SOR-EXP-0008: bounded local intake and launch-era outpost compatibility.

Reads only the operator-specified archive, installed 7z, and project parsers.
Writes a fresh ignored corpus/receipts; never writes decoded blobs or live saves.
Uses 7z as a separate installed tool, not incorporated implementation. No network.
Project-owned framing/fingerprint methods reused unchanged with hashed provenance.
"""
from pathlib import Path, PureWindowsPath
import collections
import json
import os
import stat
import struct
import subprocess
import sys
import time
import zlib
import inventory_historical_saves as inv

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = Path('C:/Users/User/Downloads/Over 110 saves-1798-1-1694378623.7z')
SEVEN = Path('C:/Program Files/7-Zip/7z.exe')
OUT = ROOT / '.local-work/third-party/the-daily-xperience-1798'
MAX_FILES = 256
MAX_EXPANDED = 4 * 1024**3
MAX_SECONDS = 1800


def members(text):
    if '\n----------\n' not in text:
        raise ValueError('missing member separator')
    result = []
    seen = set()
    for block in text.split('\n----------\n', 1)[1].split('\n\n'):
        if not block.strip():
            continue
        row = dict(line.split(' = ', 1) for line in block.splitlines() if ' = ' in line)
        path = PureWindowsPath(row['Path'])
        if (path.is_absolute() or path.root or path.drive or any(v in ('', '.', '..') for v in row['Path'].replace('\\', '/').split('/'))
                or ':' in row['Path'] or any(v.rstrip(' .') != v for v in path.parts)
                or any(v.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(1, 10)), *('LPT'+str(i) for i in range(1, 10))} for v in path.parts)):
            raise ValueError('unsafe member path')
        if str(path).casefold() in seen:
            raise ValueError('duplicate member path')
        seen.add(str(path).casefold())
        if any('link' in k.lower() or 'reparse' in k.lower() for k in row):
            raise ValueError('link/reparse metadata')
        if row.get('Attributes') not in ('A', 'D') or row.get('Encrypted') != '-':
            raise ValueError('unsupported attributes/encryption')
        row['directory'] = row['Attributes'] == 'D'
        row['size'] = int(row['Size'])
        if not row['directory'] and (path.suffix.lower() != '.sfs' or not 0 < row['size'] <= inv.MAX_PHYSICAL):
            raise ValueError('unexpected content/file size')
        result.append(row)
    if not result or len(result) > MAX_FILES or sum(v['size'] for v in result) > MAX_EXPANDED:
        raise ValueError('member total bound')
    return result


def classification(f):
    if f is None:
        return 'INCONCLUSIVE'
    if any(len(v['names']) == 1 and v['names'][0]['name'] for v in f['beacon_windows']):
        return 'OUTPOST_EVIDENCE_PRESENT'
    if (not f['errors'] and f['beacon_collection_count'] == 0
            and f['beacon_count'] == f['marker_count'] == f['animation_string_count'] == 0
            and (f['keyed_groups'], f['endpoints']) in ((0, 0), (1, 1))):
        # Detection label only. Older-version semantic negative controls absent.
        return 'NO_ACTIVE_OUTPOST_INDICATORS_DETECTED'
    return 'INCONCLUSIVE'


def audit(raw, f):
    """Independent direct count/length walk; no calls to grammar/Cursor."""
    rows = []
    for e in f['envelopes']:
        p, end = e['payload_offset'], e['end']
        if int.from_bytes(raw[p-4:p], 'little') != end-p:
            raise ValueError('independent declared length')
        def count():
            nonlocal p
            if p >= end:
                raise ValueError('audit truncated count')
            width = {0: 1, 1: 2, 2: 4}.get(raw[p] & 3)
            if width is None or p+width > end:
                raise ValueError('audit count width')
            n = int.from_bytes(raw[p:p+width], 'little') >> 2
            p += width
            return n
        n = count()
        p += 3*n
        if p > end:
            raise ValueError('audit beacon bounds')
        groups = count()
        endpoints = 0
        for _ in range(groups):
            p += 3
            k = count()
            endpoints += k
            p += 3*k
            if p > end:
                raise ValueError('audit reference bounds')
        if p != end or raw[end:end+8] != bytes.fromhex('7a00000028000000'):
            raise ValueError('audit consumption/successor')
        rows.append(dict(payload_offset=e['payload_offset'], length=end-e['payload_offset'],
                         consumed=p-e['payload_offset'], beacons=n, groups=groups, endpoints=endpoints))
    return rows


def write(name, value):
    inv.write(OUT / name, value)


def main():
    import argparse
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--reuse-extracted', action='store_true')
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    if not __import__('re').fullmatch('[A-Za-z0-9_-]+', args.run):
        raise ValueError('simple run name required')
    corpus_root = OUT
    OUT = corpus_root / args.run
    inv.guard()
    before = inv.identity(ARCHIVE)
    OUT.mkdir(parents=True, exist_ok=False)
    tools = [Path(sys.executable), SEVEN, *sorted(Path(__file__).parent.glob('*.py'))]
    provenance = dict(archive=before, tools=[inv.identity(p) for p in tools], python=sys.version,
                      zlib=zlib.ZLIB_RUNTIME_VERSION, brief=inv.identity(ROOT/'docs/implementation-briefs/CODEX_RESEARCH_BRIEF_launch_era_third_party_save_corpus.md'),
                      limits=dict(files=MAX_FILES, extracted=MAX_EXPANDED, physical=inv.MAX_PHYSICAL,
                                  decoded=inv.MAX_DECODED, seconds=MAX_SECONDS, seven_timeout=300,
                                  receipt_bytes=inv.MAX_OUTPUT, free_bytes_each_drive=40_000_000_000))
    write('provenance.json', provenance)
    listing = subprocess.run([str(SEVEN), 'l', '-slt', str(ARCHIVE)], capture_output=True, text=True, check=True, timeout=60).stdout
    (OUT/'archive-listing.txt').write_text(listing, encoding='utf-8', newline='\n')
    manifest = members(listing)
    write('archive-members.json', manifest)
    inv.guard()
    dest = corpus_root/'extracted'
    # Prevalidated <=4GiB expansion leaves the 40GB guard intact on D:.
    import shutil
    if shutil.disk_usage('D:/').free - sum(v['size'] for v in manifest) < 40_000_000_000:
        raise RuntimeError('projected space guard')
    started = time.monotonic()
    if args.reuse_extracted:
        if not dest.is_dir():
            raise RuntimeError('missing preserved extraction')
        write('extraction.json', dict(reused=True, integrity='pending complete member size/CRC/hash validation'))
    else:
        if dest.exists():
            raise RuntimeError('refuse overwrite existing extraction')
        proc = subprocess.Popen([str(SEVEN), 'x', '-y', '-o'+str(dest), str(ARCHIVE)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            while proc.poll() is None:
                inv.guard()
                if time.monotonic()-started > 300:
                    raise RuntimeError('extraction timeout; partial evidence retained')
                time.sleep(0.5)
        except BaseException:
            proc.kill(); proc.communicate()
            raise
        stdout, stderr = proc.communicate()
        write('extraction.json', dict(returncode=proc.returncode, stdout=stdout, stderr=stderr))
        if proc.returncode:
            raise RuntimeError('7z extraction failure')
    if any(p.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT for p in dest.rglob('*')):
        raise RuntimeError('extracted reparse point')
    expected = {v['Path'].replace('\\', '/'): v for v in manifest if not v['directory']}
    actual = {p.relative_to(dest).as_posix(): p for p in dest.rglob('*') if p.is_file()}
    if expected.keys() != actual.keys():
        raise RuntimeError('extracted member set differs')
    rows = []
    with (OUT/'progress.jsonl').open('x', encoding='utf-8', newline='\n') as receipt:
        for i, member in enumerate(sorted(expected)):
            inv.guard(OUT)  # Extraction bytes excluded from receipt-only 128MiB guard.
            if time.monotonic()-started > MAX_SECONDS:
                raise RuntimeError('inventory runtime stop')
            p = actual[member]
            if p.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise RuntimeError('extracted reparse point')
            b = p.read_bytes()
            m = expected[member]
            if len(b) != m['size'] or f'{zlib.crc32(b):08X}' != m['CRC']:
                raise RuntimeError('member size/CRC mismatch')
            row = inv.inspect(p, f'TDX1798-{i+1:04d}')
            row['member'] = m
            f = row.get('fingerprint')
            row['classification'] = classification(f)
            if f:
                _, spans = inv.framing(b)
                raw = inv.transform(b, spans, True)
                row['independent_audit'] = audit(raw, f)
                # Only local receipts retain load-order strings/character fields.
                d = f['directory']['regions']['early_metadata'] if 'early_metadata' in f['directory']['regions'] else [0, f['directory']['words'][2]]
                import re
                row['plugin_string_leads'] = [x.decode('utf-8', 'backslashreplace') for x in re.findall(rb'[A-Za-z0-9_ .-]{1,100}\.(?:esm|esp|esl)', raw[d[0]:d[1]], re.I)]
                del raw
            rows.append(row)
            receipt.write(json.dumps(row)+'\n'); receipt.flush(); os.fsync(receipt.fileno())
            if (i+1) % 10 == 0:
                print(i+1, '/', len(expected), row['status'], flush=True)
    for row in rows:
        if inv.identity(Path(row['source']['path'])) != row['source']:
            raise RuntimeError('extracted source changed')
    if inv.identity(ARCHIVE) != before:
        raise RuntimeError('original archive changed')
    if [inv.identity(p) for p in tools] != provenance['tools']:
        raise RuntimeError('tooling changed')
    write('inventory.json', rows)
    write('completion.json', dict(count=len(rows), expanded=sum(v['size'] for v in manifest),
          originals_preserved=True, crc_verified=len(rows), seconds=time.monotonic()-started,
          status=dict(collections.Counter(r['status'] for r in rows)),
          classification=dict(collections.Counter(r['classification'] for r in rows)),
          free_bytes={d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}))
    print('COMPLETE', len(rows), flush=True)


if __name__ == '__main__':
    main()
