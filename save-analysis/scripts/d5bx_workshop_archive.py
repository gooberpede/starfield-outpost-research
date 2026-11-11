# SPDX-License-Identifier: GPL-3.0-or-later
"""Canonical Workshop supplementary ZIP encoding and exact member checks."""
import hashlib
import json
import stat
from collections import Counter
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

SCHEMA = 'sor-d5bx-workshop/2'
NAMES = ('manifest.json', 'workshop.json', 'canonical-candidates01.json')
CANONICAL = (9469, '34972f368f95b671d68bcb0087a9b50619d87cc0f8f2d426eb88d6a5d1dfccb3')
SOURCE_PINS = (
    (417320665, '229b79deedec274ffd9816e7aee7675e14e5e657c17776930e2085b3b648480c'),
    (226146013, '1b4f69b4e5bfacfcecb91721670def8f9690dde2cc615ff97d55bdaeb37d9086'),
    (956014, 'b4533026f2c933cfe0057927149758964d2d0418c99d57c73d4a7a62b317ab68'),
)
SOURCE_IDS = ('WORKSHOP-BASELINE', 'WORKSHOP-TYPED', 'WORKSHOP-ALLA', 'WORKSHOP-CANONICAL')
KEYWORDS = {'starfield.esm:054ba6', 'starfield.esm:000191', 'starfield.esm:000192'}
OWNER_KEY = 'starfield.esm:054ba6'
HABS = {'DYNAMIC:ff01b59b', 'DYNAMIC:ff05d48a'}
EPOCH = (1980, 1, 1, 0, 0, 0)


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                       separators=(',', ':')) + '\n').encode('ascii')


def fingerprint(data):
    return len(data), hashlib.sha256(data).hexdigest()


def manifest(payload, ledger):
    return dict(schema=SCHEMA, sources=dict(zip(SOURCE_IDS, (*SOURCE_PINS, CANONICAL), strict=True)),
                members=dict(zip(NAMES[1:], map(fingerprint, (payload, ledger)), strict=True)))


def quest_operand(alla):
    counts = Counter(row['keyword'] for row in alla['pairs'])
    return dict(schema=alla['schema'], keyword_counts=[dict(keyword=k, count=v) for k, v in counts.items()])


def canonical_da_groups(extras, groups):
    if any(edge['keyword_identity'] == OWNER_KEY for edge in extras.get('entries', [])):
        return ()
    return tuple(da['identities'][3] for da in extras.get('packin', []) if da['identities'][3] in groups)


def write_archive(stream, payload, ledger):
    require(fingerprint(ledger) == CANONICAL, 'CANONICAL_IDENTITY')
    with ZipFile(stream, 'w', allowZip64=False) as archive:
        for name, raw in zip(NAMES, (encoded(manifest(payload, ledger)), payload, ledger), strict=True):
            info = ZipInfo(name, EPOCH)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, raw, compress_type=ZIP_DEFLATED, compresslevel=9)


def read_archive(stream, member_pins):
    """Read exact named byte strings in memory without filesystem extraction."""
    with ZipFile(stream) as archive:
        entries = archive.infolist()
        require(tuple(info.filename for info in entries) == NAMES, 'ARCHIVE_MEMBER_SELECTION')
        require(not archive.comment, 'ARCHIVE_COMMENT')
        result = []
        for info in entries:
            require(info.orig_filename == info.filename and info.compress_type == ZIP_DEFLATED
                    and info.date_time == EPOCH and info.flag_bits == 0 and not info.extra
                    and not info.comment and info.create_system == 3
                    and info.external_attr == (stat.S_IFREG | 0o644) << 16, 'ARCHIVE_MEMBER_TYPE')
            expected = tuple(member_pins[info.filename])
            require(info.file_size == expected[0], 'ARCHIVE_MEMBER_LENGTH')
            raw = archive.read(info)
            require(fingerprint(raw) == expected, 'ARCHIVE_MEMBER_IDENTITY')
            result.append(raw)
    index, payload, ledger = result
    require(fingerprint(ledger) == CANONICAL, 'CANONICAL_IDENTITY')
    require(index == encoded(manifest(payload, ledger)), 'ARCHIVE_MANIFEST')
    parsed = json.loads(payload)
    require(parsed['schema'] == SCHEMA and encoded(parsed) == payload, 'PROJECTION_SCHEMA')
    return parsed, json.loads(ledger)
