# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline EXP0002 input checks. Standard library only; never opens a process.

Reads explicit files and the existing recon baseline. Saves are only hashed and
byte-compared. Writes CREATE_NEW reports beneath the repository's ignored
.local-work/exp0002 directory. No save copying, parsing, launch or deployment.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
from datetime import datetime, timezone
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / '.local-work' / 'exp0002'
GAME_HASH = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
TARGETS = {'callback': 0x2073cf0, 'tail': 0x517d60, 'key_global': 0x5f0b3d8}


def metadata(path):
    path = Path(path).resolve(strict=True)
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('Input changed during hashing')
    return dict(path=str(path), filename=path.name, size=after.st_size,
                sha256=h.hexdigest(), mtime_ns=after.st_mtime_ns,
                last_write_utc=datetime.fromtimestamp(after.st_mtime, timezone.utc).isoformat())


def equal_bytes(a, b):
    with Path(a).open('rb') as left, Path(b).open('rb') as right:
        while True:
            x, y = left.read(1024 * 1024), right.read(1024 * 1024)
            if x != y:
                return False
            if not x:
                return True


def write_report(name, data):
    if not re.fullmatch(r'[a-z0-9-]+\.json', name):
        raise ValueError('Simple JSON basename required')
    base = OUTPUT.resolve()
    if not base.is_relative_to(ROOT.resolve()) or base != OUTPUT.absolute():
        raise ValueError('Output root redirected outside expected repository location')
    base.mkdir(parents=True, exist_ok=True)
    target = base / name
    if target.is_symlink():
        raise ValueError('Output symlink rejected')
    payload = (json.dumps(data, indent=2, allow_nan=False) + '\n').encode()
    if len(payload) > 2 * 1024 * 1024:
        raise ValueError('Report exceeds 2 MiB')
    with target.open('xb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    return target


def pe_layout(data):
    if data[:2] != b'MZ':
        raise ValueError('Not PE')
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    if data[pe:pe+4] != b'PE\0\0':
        raise ValueError('Invalid PE signature')
    machine, count = struct.unpack_from('<HH', data, pe + 4)
    optional_size = struct.unpack_from('<H', data, pe + 20)[0]
    opt = pe + 24
    if machine != 0x8664 or struct.unpack_from('<H', data, opt)[0] != 0x20b:
        raise ValueError('Expected x64 PE32+')
    image_base = struct.unpack_from('<Q', data, opt + 24)[0]
    image_size = struct.unpack_from('<I', data, opt + 56)[0]
    sections = []
    for i in range(count):
        pos = opt + optional_size + i * 40
        virtual_size, rva, raw_size, raw = struct.unpack_from('<IIII', data, pos + 8)
        sections.append((rva, virtual_size, raw, raw_size))
    return image_base, image_size, sections


def file_offset(sections, rva, length):
    for start, virtual_size, raw, raw_size in sections:
        delta = rva - start
        if 0 <= delta and delta + length <= min(virtual_size, raw_size):
            return raw + delta
    raise ValueError('RVA has no file-backed range')


def runtime_site(base, size, rva):
    if type(base) is not int or base <= 0 or base % 0x10000 or not 0 <= rva < size:
        raise ValueError('Invalid module base or RVA')
    if base + size > 0x800000000000:
        raise ValueError('Outside canonical user address range')
    return base + rva


def inspect_pe(path):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != GAME_HASH:
        raise ValueError('Wrong game build; target inspection stopped')
    base, size, sections = pe_layout(data)
    rows = []
    for name, rva in TARGETS.items():
        length = 8 if name == 'key_global' else 24
        if name == 'key_global':
            rows.append(dict(name=name, static_va=hex(base+rva), rva=hex(rva),
                             length=length, status='RUNTIME_VALUE_REQUIRED'))
            continue
        offset = file_offset(sections, rva, length)
        rows.append(dict(name=name, static_va=hex(base+rva), rva=hex(rva),
                         file_offset=hex(offset), length=length,
                         hex=data[offset:offset+length].hex()))
    callback = bytes.fromhex(rows[0]['hex'])
    if callback[:10].hex() != '498b88c80000004533c0' or callback[10:13] != b'\x48\x8b\x15' or callback[17] != 0xe9:
        raise ValueError('Callback instruction prefix mismatch')
    global_rva = TARGETS['callback'] + 17 + struct.unpack_from('<i', callback, 13)[0]
    tail_rva = TARGETS['callback'] + 22 + struct.unpack_from('<i', callback, 18)[0]
    if global_rva != TARGETS['key_global'] or tail_rva != TARGETS['tail']:
        raise ValueError('Callback relative targets disagree')
    return dict(preferred_base=hex(base), image_size=size, targets=rows,
                global_rva=hex(global_rva), tail_rva=hex(tail_rva))


def integrity(args):
    initial = [metadata(args.original), metadata(args.backup)]
    same = equal_bytes(args.original, args.backup)
    final = [metadata(args.original), metadata(args.backup)]
    baseline = json.loads((ROOT / '.local-work/recon/baseline.json').read_text())
    observed = []
    for item in baseline:
        if Path(item['path']).name in ('Starfield.exe', 'CreationKit.exe', 'sfse_loader.exe', 'sfse_1_16_244.dll', 'ContentResources.zip'):
            actual = metadata(item['path'])
            actual['matches_env0001'] = actual['sha256'] == item['sha256'].lower() and actual['size'] == item['size']
            observed.append(actual)
    ok = same and initial == final and all(x['matches_env0001'] for x in observed)
    report = dict(schema_version=1, utc=datetime.now(timezone.utc).isoformat(),
                  classification='LOCAL-ONLY', sample_id='SOR-SAMPLE-0001',
                  environment_id='SOR-ENV-0002', original=initial[0], backup=initial[1],
                  byte_equal=same, unchanged_during_check=initial == final,
                  baseline=observed, checks_passed=ok, terminal='OFFLINE_CHECK_COMPLETE')
    write_report(args.output, report)
    if not ok:
        raise ValueError('Integrity mismatch: stop affected experiment path')


COORDINATES = re.compile(r'latitude|longitude|planet.?coord|surface.?coord|planet.?map|landing.?site|planetary.?location|biome.?map|worldspace|cell.?coord|planet.?body.?transform', re.I)


def coordinates(args):
    report = dict(classification='LOCAL-ONLY', inputs=[], binary_matches=[], script_matches=[])
    expression = re.compile(r'latitude|longitude|planet.?coord|surface.?coord|planet.?map|landing.?site|planetary.?location', re.I) if args.focused else COORDINATES
    report['pattern'] = expression.pattern
    for path in args.binary:
        item = metadata(path)
        data = Path(path).read_bytes()
        if hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('Binary changed during inspection')
        base, size, sections = pe_layout(data)
        matches = []
        for encoding, pattern in [('ascii', rb'[\x20-\x7e]{6,}'), ('utf-16le', rb'(?:[\x20-\x7e]\x00){6,}')]:
            count = 0
            for found in re.finditer(pattern, data):
                value = found.group().decode(encoding)
                if len(value) > 1024 or not expression.search(value):
                    continue
                if count == 80:
                    matches.append(dict(encoding=encoding, truncated=True))
                    break
                offset = found.start()
                rvas = [rva + offset - raw for rva, vs, raw, rs in sections if raw <= offset < raw + rs]
                matches.append(dict(encoding=encoding, file_offset=hex(offset),
                                    static_va=hex(base+rvas[0]) if rvas else None, text=value))
                count += 1
        report['inputs'].append(item)
        report['binary_matches'].append(dict(filename=Path(path).name, matches=matches))
    report['inputs'].append(metadata(args.archive))
    with zipfile.ZipFile(args.archive) as archive:
        for leaf in ('ObjectReference.psc', 'Cell.psc', 'WorldSpace.psc', 'Location.psc', 'Planet.psc', 'Game.psc'):
            names = [name for name in archive.namelist() if name.lower() == ('scripts/source/' + leaf).lower()]
            if not names:
                report['script_matches'].append(dict(entry=leaf, status='NOT_FOUND_AT_EXACT_PATH'))
            for name in names:
                raw = archive.read(name)
                hits = [dict(line=i, text=line) for i, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1)
                        if COORDINATES.search(line) or re.search(r'Get(Position|Angle|CurrentLocation|ParentCell|WorldSpace|Planet)|Is3DLoaded', line)]
                report['script_matches'].append(dict(entry=name, sha256=hashlib.sha256(raw).hexdigest(), matches=hits[:100], truncated=len(hits)>100))
    report['terminal'] = 'BOUNDED_STATIC_SCAN_COMPLETE'
    write_report(args.output, report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('integrity')
    p.add_argument('--original', required=True)
    p.add_argument('--backup', required=True)
    p.add_argument('--output', required=True)
    p.set_defaults(run=integrity)
    p = sub.add_parser('pe')
    p.add_argument('--executable', required=True)
    p.add_argument('--output', required=True)
    p.set_defaults(run=lambda a: write_report(a.output, inspect_pe(a.executable)))
    p = sub.add_parser('coordinates')
    p.add_argument('--binary', nargs='+', required=True)
    p.add_argument('--archive', required=True)
    p.add_argument('--focused', action='store_true')
    p.add_argument('--output', required=True)
    p.set_defaults(run=coordinates)
    args = parser.parse_args()
    args.run(args)


if __name__ == '__main__':
    main()
