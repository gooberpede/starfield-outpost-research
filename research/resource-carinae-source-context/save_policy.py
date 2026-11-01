# SPDX-License-Identifier: GPL-3.0-or-later
"""Prospective save classes from the pinned native filename grammar/designations.

Reads names, optional explicit classifications and immutable inventory rows.
No header save-kind claim, target operation, restoration or source write.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import datetime
import hashlib
import json
from pathlib import Path
import re

POLICY_PATH = Path(__file__).with_name('save_policy.json')
NAME = re.compile(
    r'(?P<kind>Save|Autosave|Exitsave|Quicksave)(?P<slot>0|[1-9][0-9]*)_'
    r'(?P<profile>[0-9A-F]{8})(?P<flags>SM|S|M|_)(?P<character>(?:[0-9A-F]{2})+)_'
    r'(?P<elapsed>[0-9]{6,})_(?P<utc>[0-9]{14})_'
    r'(?P<level>0|[1-9][0-9]*)_(?P<counter>0|[1-9][0-9]*)_4\.sfs', re.IGNORECASE)
KINDS = {'save': 'MANUAL', 'autosave': 'AUTO', 'exitsave': 'EXIT', 'quicksave': 'QUICK'}


def load_policy():
    return json.loads(POLICY_PATH.read_text(encoding='utf8'))


def policy_hash(policy):
    return hashlib.sha256(json.dumps(policy, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def classify(name, policy):
    """Explicit research designation wins; unsupported names stay unclassified."""
    if Path(name).name != name:
        return dict(kind='UNKNOWN', protection='UNCLASSIFIED', basis='NESTED_OR_NONBASENAME')
    folded = name.casefold()
    designated = {n.casefold(): v for n, v in policy['designated'].items()}
    if folded in designated:
        assert designated[folded]['evidence'].strip(), 'Research designation requires provenance'
        return dict(kind='DESIGNATED', protection='PROTECTED', basis='EXPLICIT_RESEARCH_DESIGNATION')
    kinds = {n.casefold(): v for n, v in policy['classified'].items()}
    if folded in kinds:
        entry = kinds[folded]
        assert entry['evidence'].strip() and entry['kind'] in ('MANUAL', 'AUTO', 'EXIT', 'QUICK')
        kind = entry['kind']
        basis = 'EXPLICIT_MAINTAINER_CLASSIFICATION'
    else:
        match = NAME.fullmatch(name)
        if not match:
            return dict(kind='UNKNOWN', protection='UNCLASSIFIED', basis='UNSUPPORTED_NAME')
        try:
            kind = KINDS[match['kind'].lower()]
            assert 0 not in bytes.fromhex(match['character'])
            elapsed = match['elapsed']
            assert f'{int(elapsed[:-4]):02d}' == elapsed[:-4]
            assert int(elapsed[:-4]) <= 0xffffffff
            assert int(elapsed[-4:-2]) < 24 and int(elapsed[-2:]) < 60
            assert int(match['slot']) <= 0xffffffff and int(match['counter']) <= 0xffffffff
            assert int(match['level']) <= 0xffff
            if kind in ('QUICK', 'EXIT'):
                assert match['slot'] == '0'
            datetime.datetime.strptime(match['utc'], '%Y%m%d%H%M%S')
        except (AssertionError, ValueError):
            return dict(kind='UNKNOWN', protection='UNCLASSIFIED', basis='INVALID_NATIVE_FIELDS')
        basis = 'NATIVE_FULL_FILENAME_GRAMMAR_1.16.244.0'
    return dict(kind=kind, protection='TRANSIENT' if kind in ('AUTO', 'EXIT') else 'PROTECTED', basis=basis)


def partition(rows, policy):
    groups = dict(protected={}, transient={}, unclassified={}, classifications={})
    seen = set()
    for name, row in rows.items():
        assert name.casefold() not in seen, 'Ambiguous case-colliding inventory names'
        seen.add(name.casefold())
        result = classify(name, policy)
        groups['classifications'][name] = result
        group = dict(PROTECTED='protected', TRANSIENT='transient', UNCLASSIFIED='unclassified')[result['protection']]
        groups[group][name] = row
    return groups


def changes(before, after):
    return dict(new=sorted(set(after)-set(before)), missing=sorted(set(before)-set(after)),
                changed=sorted(n for n in before.keys() & after.keys() if before[n] != after[n]))


def compare(before, after, policy):
    """Identical policy at pre/post; transient diagnostics never hide failures."""
    a, b = partition(before, policy), partition(after, policy)
    protected = changes(a['protected'], b['protected'])
    unknown = sorted(set(a['unclassified']) | set(b['unclassified']))
    return dict(ok=not unknown and not any(protected.values()), protected_changes=protected,
                unclassified=unknown, transient_changes=changes(a['transient'], b['transient']))


def admission(live, backup, historical, policy):
    """Keep every historical backup record strict; gate live protected rows only."""
    expected = partition(historical, policy)
    baseline = dict(expected['protected'])
    for name, entry in policy['designated'].items():
        declared = dict(bytes=entry['bytes'], sha256=entry['sha256'])
        if name in baseline:
            assert baseline[name] == declared, 'Designation and historical protected pin disagree'
        baseline[name] = declared
    result = compare(baseline, live, policy)
    result['backup_changes'] = changes(historical, backup)
    result['designated_without_backup'] = [name for name, entry in policy['designated'].items()
        if backup.get(name) != dict(bytes=entry['bytes'], sha256=entry['sha256'])]
    result['historical_unclassified'] = sorted(expected['unclassified'])
    result['ok'] &= (not any(result['backup_changes'].values()) and
                     not result['historical_unclassified'] and not result['designated_without_backup'])
    # Diagnostic comparison uses the full immutable old inventory, including transients.
    result['transient_changes'] = compare(historical, live, policy)['transient_changes']
    return result


def snapshot(folder, policy):
    """Hash protected content strictly; tolerate a transient vanishing mid-read."""
    folder = Path(folder)
    assert folder.is_dir(), 'Save namespace missing'
    for ancestor in (folder, *folder.parents):
        assert not ancestor.lstat().st_file_attributes & 0x400, 'Reparse save namespace/ancestor'
    rows = {}
    for p in sorted(folder.rglob('*')):
        name = p.relative_to(folder).as_posix()
        transient = classify(name, policy)['protection'] == 'TRANSIENT'
        try:
            assert not p.lstat().st_file_attributes & 0x400, 'Reparse save path'
            if p.is_file():
                with p.open('rb') as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                rows[name] = dict(bytes=p.stat().st_size, sha256=digest)
        except OSError as error:
            if not transient:
                raise
            rows[name] = dict(diagnostic=type(error).__name__)
    return rows


def sizes(folder, policy):
    """Lightweight launch admission inventory; transient races are diagnostic only."""
    folder = Path(folder)
    assert folder.is_dir(), 'Save namespace missing'
    for ancestor in (folder, *folder.parents):
        assert not ancestor.lstat().st_file_attributes & 0x400, 'Reparse save namespace/ancestor'
    rows = {}
    for p in sorted(folder.rglob('*')):
        name = p.relative_to(folder).as_posix()
        try:
            stat = p.lstat()
            assert not stat.st_file_attributes & 0x400, 'Reparse save path'
            if p.is_file():
                rows[name] = dict(bytes=stat.st_size)
        except OSError:
            if classify(name, policy)['protection'] != 'TRANSIENT':
                raise
    return rows
