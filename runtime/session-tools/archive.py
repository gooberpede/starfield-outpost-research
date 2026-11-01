# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline sealing and ZIP/Deflate archival, streaming every member to SHA256.
Reads quiescent evidence and hash-bound postflight/seals; writes new receipts and
archives only. Never deletes, extracts over originals, repairs, or uploads data.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import time
import zipfile
from common import fresh, guard, inventory, now, read, regular, sha

MANIFEST = 'SOR-MANIFEST.json'


def safe_name(name):
    parts = name.split('/')
    if (not name or any(c in name for c in '\\:<>"|?*') or name.startswith('/')
            or any(p in ('', '.', '..') or p.endswith((' ', '.')) for p in parts)
            or any(ord(c) < 32 for c in name)
            or any(re.fullmatch(r'(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(\..*)?', p) for p in parts)):
        raise ValueError('unsafe_member_path: ' + name)
    return PurePosixPath(name)


def validate_names(names):
    seen = set()
    for n in names:
        safe_name(n)
        key = n.casefold()
        if key in seen:
            raise ValueError('duplicate_member_path')
        seen.add(key)
    for n in seen:
        if any(str(p) in seen for p in PurePosixPath(n).parents if str(p) != '.'):
            raise ValueError('file_directory_collision')


def collect(roots):
    files = {}
    for label, row in roots.items():
        safe_name(label)
        if '/' in label or row['kind'] not in ('raw-capture', 'derivative', 'private-receipt', 'publishable-report'):
            raise ValueError('root_classification')
        for name, value in inventory(row['path']).items():
            files[label + '/' + name] = value
    validate_names([MANIFEST, *files])
    return files


def outside(path, roots):
    p = regular(path).resolve()
    if any(p.is_relative_to(Path(r['path']).resolve()) for r in roots.values()):
        raise ValueError('output_inside_sealed_source')


def seal(roots, postflight, pin, partial_reason=None):
    guard()
    post = read(postflight, pin)
    if (post.get('action') != 'postflight' or post.get('process_state') not in ('GONE', 'EXITED', 'ORIGINAL_GONE_PID_REUSED')
            or post.get('status') not in ('PASS_POSTFLIGHT', 'PARTIAL_POSTFLIGHT')):
        raise ValueError('offline_postflight_required')
    raw = [Path(r['path']).resolve() for r in roots.values() if r['kind'] == 'raw-capture']
    if Path(post['session']).resolve() not in raw:
        raise ValueError('postflight_raw_root_mismatch')
    if post['status'] != 'PASS_POSTFLIGHT' and not partial_reason:
        raise ValueError('partial_reason_required')
    if not any(Path(postflight).resolve().is_relative_to(Path(r['path']).resolve()) for r in roots.values()):
        raise ValueError('postflight_companion_missing')
    files = collect(roots)
    return dict(schema='sor-seal/1', status='PARTIAL' if partial_reason else 'COMPLETE',
                utc=now(), roots=roots, files=files, postflight_sha256=pin,
                partial_reason=partial_reason, publication='LOCAL-ONLY; classifications do not clear publication',
                immutability='Content seal, not filesystem write protection. Sources must remain quiescent; every archival adoption rechecks all bytes.')


def verify(archive, seal_value, archive_pin=None):
    if archive_pin and sha(archive) != archive_pin:
        raise ValueError('archive_hash_mismatch')
    expected = seal_value['files']
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        validate_names(names)
        if set(names) != set(expected) | {MANIFEST}:
            raise ValueError('archive_inventory_mismatch')
        if json.loads(z.read(MANIFEST)) != seal_value:
            raise ValueError('embedded_manifest_mismatch')
        for item in z.infolist():
            if item.is_dir() or stat.S_ISLNK(item.external_attr >> 16) or item.flag_bits & 1:
                raise ValueError('unsupported_member_type')
            if item.filename == MANIFEST:
                continue
            row = expected[item.filename]
            if item.file_size != row['size']:
                raise ValueError('member_size_mismatch')
            digest, size = hashlib.sha256(), 0
            with z.open(item) as src:
                while block := src.read(1024 * 1024):
                    guard()
                    digest.update(block)
                    size += len(block)
            if size != row['size'] or digest.hexdigest() != row['sha256']:
                raise ValueError('member_hash_mismatch')
    return dict(status='VERIFIED_EVERY_MEMBER', members=len(expected), archive_sha256=sha(archive))


def create(seal_path, pin, destination):
    start = time.perf_counter()
    s = read(seal_path, pin)
    if s['schema'] != 'sor-seal/1' or s['status'] not in ('COMPLETE', 'PARTIAL'):
        raise ValueError('seal_required')
    outside(destination, s['roots'])
    if Path(destination).exists():
        raise ValueError('archive_exists')
    # Deflate worst-case overhead is small; reserve conservative 1% + metadata
    # and 16 MiB. Stream verification needs no full-size extraction temporary.
    total = sum(r['size'] for r in s['files'].values())
    reserve = total + total // 100 + len(s['files']) * 4096 + len(json.dumps(s).encode()) + 16 * 1024 * 1024
    drive = Path(destination).resolve().drive.replace('\\', '/') + '/'
    if drive not in ('C:/', 'D:/'):
        raise ValueError('archive_destination_must_be_C_or_D')
    disk = guard({drive: reserve})
    if collect(s['roots']) != s['files']:
        raise ValueError('sealed_source_changed')
    checked = time.perf_counter()
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        z.writestr(MANIFEST, json.dumps(s, indent=2).encode('utf8') + b'\n')
        for name in s['files']:
            guard()  # both drives; no sampling or evidence-volume quota
            label, relative = name.split('/', 1)
            source = regular(Path(s['roots'][label]['path']) / relative)
            with source.open('rb') as src, z.open(name, 'w', force_zip64=True) as dst:
                while block := src.read(1024 * 1024):
                    guard()
                    dst.write(block)
    compressed = time.perf_counter()
    result = verify(destination, s)
    # Detect addition/removal/content drift during creation, not just ZIP errors.
    if collect(s['roots']) != s['files']:
        raise ValueError('source_changed_during_archive')
    guard()
    end = time.perf_counter()
    result.update(capture_status=s['status'], seal_sha256=pin, utc=now(),
                  original_bytes=total, archive_bytes=Path(destination).stat().st_size,
                  seconds=dict(source_check=checked-start, compression=compressed-checked,
                               verification_and_source_recheck=end-compressed, total=end-start),
                  disk=disk, reserved_bytes=reserve, raw_originals='PRESERVED',
                  retention='Keep raw and archive; retirement requires separate maintainer authorization.')
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=['seal', 'create', 'verify'])
    ap.add_argument('--input', type=Path, required=True, help='roots JSON for seal; seal JSON otherwise')
    ap.add_argument('--sha256', required=True)
    ap.add_argument('--postflight', type=Path)
    ap.add_argument('--postflight-sha256')
    ap.add_argument('--partial-reason')
    ap.add_argument('--archive', type=Path)
    ap.add_argument('--archive-sha256')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        ap.error('receipt exists')
    try:
        value = read(a.input, a.sha256)
        roots = value if a.action == 'seal' else value['roots']
        outside(a.out, roots)
        if a.action == 'seal':
            if not a.postflight or not a.postflight_sha256:
                raise ValueError('postflight_pin_required')
            result = seal(value, a.postflight, a.postflight_sha256, a.partial_reason)
        elif a.action == 'create':
            if not a.archive:
                raise ValueError('archive_path_required')
            result = create(a.input, a.sha256, a.archive)
        else:
            guard()
            if not a.archive or not a.archive_sha256:
                raise ValueError('archive_pin_required')
            result = verify(a.archive, value, a.archive_sha256)
    except Exception as exc:
        # Never overwrite originals even to record a failure.
        try:
            if 'roots' in locals():
                outside(a.out, roots)
            fresh(a.out, dict(status='ARCHIVE_ERROR', utc=now(), error=repr(exc)))
        finally:
            print(repr(exc))
        return 1
    fresh(a.out, result)
    print(json.dumps(result if a.action != 'seal' else dict(status=result['status'], files=len(result['files']))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
