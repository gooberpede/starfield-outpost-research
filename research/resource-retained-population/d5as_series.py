# SPDX-License-Identifier: GPL-3.0-or-later
"""Inventory and freeze the D5AS series offline using Windows CPython -E -B.

Reads the dedicated series directory, owned D5AR decoder and D5AS geometry
references, and pinned local preparation/review artifacts. Writes fresh ignored
ledgers, a lossless archive or a freeze receipt. No target, process, deployment,
original save or source evidence changes. See the D5AS analysis protocol.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
from fractions import Fraction
import hashlib
import json
from math import comb
import os
from pathlib import Path
import re
import sys
from uuid import UUID, uuid4
import zipfile

import d5ar_snapshot as raw
import d5as_geometry as geometry
from d5as_prepare import (
    BEFORE, BEFORE_SHA, CAPTURE, CONFIG, DLL, DLL_SHA, HOSTS, LOCAL, PACKAGE, PREFIX, ROOT,
    SOURCE_LOCK_SHA,
    digest, disk_floor, plain, require, safe_output, sha,
)

N = 30
FROZEN = LOCAL / 'frozen-corpus.json'
PACKAGE_SHA = 'a646848f13c475f6ef4bc3a046f70b4d84506c962a2da52daf02f3c91fa44c18'
MASK0 = 'MATCH_MASK0_REFERENCE'
MASK3 = 'MATCH_MASK3_REFERENCE'
OTHER = 'OTHER_QUALIFIED_GEOMETRY'
INVALID = 'INVALID_OR_INCONCLUSIVE'
BUILD = dict(game_exe_sha256=HOSTS['Starfield.exe'], sfse_sha256=HOSTS['sfse_1_16_244.dll'],
             plugin_sha256=DLL_SHA, source_lock_sha256=SOURCE_LOCK_SHA)
UUID_PATTERN = r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}'
CAPTURE_NAME = re.compile(
    rf'(?P<stamp>[0-9]{{8}}T[0-9]{{6}}\.[0-9]{{6}}Z)_(?P<session>{UUID_PATTERN})_'
    rf'(?P<capture>{UUID_PATTERN})(?P<suffix>\.snapshot\.json|\.partial)')
STARTUP_NAME = re.compile(rf'startup-{UUID_PATTERN}(?P<suffix>\.startup\.json|\.partial)')
STAGES = {'WAITING_STARTUP_ADMISSION', 'STARTUP_HOOKS_INSTALLED', 'COMMAND_READY'}
DEVIATION_CODES = {'WRONG_SAVE', 'WRONG_ROUTE_OR_SITE', 'UNAPPROVED_GAMEPLAY_OR_TRIGGER',
                   'NON_FRESH_PROCESS', 'OPERATOR_STOP_DURING_ATTEMPT', 'WRONG_PACKAGE_OR_PROFILE'}
STARTUP_KEYS = set(BUILD) | {
    'source_history_startup_premise', 'source_address_reuse', 'stack_admission_observed',
    'stack_admission_complete', 'stack_admission_code', 'stack_frames', 'evidence_basis',
    'schema', 'status', 'session_id', 'pid', 'creation_filetime', 'thread',
    'config_sha256', 'utc', 'wait_ms',
}
UTC = '%Y-%m-%dT%H:%M:%S.%fZ'


def load_json(data):
    def nonfinite(word):
        raise ValueError(f'Nonfinite JSON token {word}')

    return json.loads(data, object_pairs_hook=raw.unique_pairs, parse_constant=nonfinite)


def read_file(path):
    before = path.lstat()
    require(path.is_file() and not before.st_file_attributes & 0x400,
            f'Expected plain file {path.name}')
    data = path.read_bytes()
    after = path.lstat()
    require((before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_ino, after.st_size, after.st_mtime_ns) and len(data) == before.st_size,
            f'File changed during read {path.name}')
    return data


def identity(value):
    pid, birth = value['pid'], value['creation_filetime']
    require(type(pid) is int and 0 < pid < 2**32 and type(birth) is int and 0 < birth < 2**64,
            'Invalid process identity')
    return dict(pid=pid, creation_filetime=birth)


def check_utc(utc):
    require(isinstance(utc, str) and len(utc) == 27, 'Invalid exact UTC')
    parsed = datetime.strptime(utc, UTC)
    require(parsed.strftime(UTC) == utc, 'Invalid exact UTC')


def startup(data, config_sha, synthetic):
    value = load_json(data)
    require(isinstance(value, dict) and set(value) == STARTUP_KEYS
            and value['schema'] == 'sor-d5ar-startup/1', 'Invalid startup schema')
    require(data.endswith(b'\n'), 'Startup receipt lacks final LF')
    require(value['evidence_basis'] == ('SYNTHETIC' if synthetic else 'UNQUALIFIED_NATIVE') and
            value['source_history_startup_premise'] ==
            'FRESH_PROCESS_OFFICIAL_SFSE_PRELOAD_BEFORE_ORDINARY_SOURCE_HISTORY' and
            value['source_address_reuse'] == 'PERMANENT_REFUSAL', 'Startup provenance mismatch')
    require(all(value[k] == v for k, v in BUILD.items()) and value['config_sha256'] == config_sha,
            'Startup producer or series sidecar mismatch')
    check_utc(value['utc'])
    identity(value)
    require(str(UUID(value['session_id'])) == value['session_id'], 'Invalid startup session')
    status = value['status']
    require(isinstance(status, str) and bool(status), 'Invalid startup status')
    if status in STAGES - {'WAITING_STARTUP_ADMISSION'}:
        require(value['stack_admission_observed'] is True and
                value['stack_admission_complete'] is True and
                type(value['stack_admission_code']) is int and value['stack_admission_code'] == 0 and
                type(value['stack_frames']) is int and value['stack_frames'] > 0,
                'Startup stack admission incomplete')
    return value


def snapshot(data, name):
    value = load_json(data)
    require(isinstance(value, dict), 'Snapshot is not an object')
    raw.validate(value)
    check_utc(value['utc'])
    stamp = value['utc'].replace('-', '').replace(':', '')
    require((stamp, value['session_id'], value['capture_id']) ==
            (name['stamp'], name['session'], name['capture']), 'Filename and snapshot identity differ')
    require(data == raw.encoded(value) + b'\n', 'Snapshot exact publication encoding differs')
    return value


def inventory(folder, config_sha, references, deviations=(), *, synthetic=False):
    """Return the attempt ledger without ranking or classifying geometry outcomes."""
    plain(folder)
    require(synthetic or folder == CAPTURE, 'Use the configured series capture directory')
    files, starts, incomplete_starts, attempts = [], defaultdict(list), defaultdict(list), {}
    partial_processes = defaultdict(set)
    for path in sorted(folder.iterdir(), key=lambda p: p.name):
        item = dict(name=path.name)
        files.append(item)
        capture = CAPTURE_NAME.fullmatch(path.name)
        start = STARTUP_NAME.fullmatch(path.name)
        if capture:
            stamp, session, capture_id, suffix = capture.groups()
            row = attempts.setdefault((session, capture_id), dict(
                session_id=session, capture_id=capture_id, files=[], reasons=[],
                filename_stamps=[], process=None, utc=None, geometry=None))
            row['files'].append(path.name)
            row['filename_stamps'].append(stamp)
        try:
            data = read_file(path)
            item.update(sha256=digest(data), bytes=len(data))
            if capture:
                if suffix == '.partial':
                    row['reasons'].append('UNPUBLISHED_CAPTURE_PARTIAL')
                    value = snapshot(data, capture)
                    item.update(process=identity(value['process']), utc=value['utc'],
                                copy_status=value['capture_diagnostics']['copy_status'])
                    partial_processes[session].add(tuple(item['process'].values()))
                else:
                    require(row['utc'] is None, 'Multiple final snapshots for capture identity')
                    value = snapshot(data, capture)
                    row.update(process=identity(value['process']), utc=value['utc'],
                               build=value['build'], copy_status=value['capture_diagnostics']['copy_status'],
                               represented_entries=len(value['sources']), snapshot=path.name)
                    if (capture_id == geometry.PILOT_CAPTURE_ID or
                            item['sha256'] == geometry.PILOT_SNAPSHOT_SHA256):
                        row['reasons'].append('PILOT04_EXCLUDED')
                    elif value['status'] == 'REFUSED':
                        row['reasons'].append('NATIVE_REFUSED: ' + row['copy_status'])
                    else:
                        admission = geometry.admit(value, references, synthetic=synthetic)
                        row['geometry'] = admission
                        if not admission['eligible']:
                            row['reasons'].append('GEOMETRY: ' + admission['reason'])
            elif start and start['suffix'] == '.startup.json':
                value = startup(data, config_sha, synthetic)
                item.update(session_id=value['session_id'], process=identity(value),
                            startup_status=value['status'], utc=value['utc'])
                starts[value['session_id']].append(item)
            elif start:
                item['diagnostic'] = 'UNPUBLISHED_STARTUP_PARTIAL_UNATTRIBUTED'
                value = startup(data, config_sha, synthetic)
                item.update(session_id=value['session_id'], process=identity(value),
                            startup_status=value['status'], utc=value['utc'],
                            diagnostic='UNPUBLISHED_STARTUP_PARTIAL')
                incomplete_starts[value['session_id']].append(item)
            elif path.name in ('STOP', 'STARTUP_STOP'):
                item['diagnostic'] = 'STOP_MARKER_WITHOUT_ATTEMPT_ID'
            else:
                item['diagnostic'] = 'UNRECOGNIZED_FILE_NO_ATTEMPT_ID'
        except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError, RecursionError) as exc:
            item['diagnostic'] = str(exc)
            if capture:
                row['reasons'].append('SNAPSHOT_OR_FILE: ' + str(exc))

    session_counts = Counter(row['session_id'] for row in attempts.values())
    capture_counts = Counter(row['capture_id'] for row in attempts.values())
    for deviation in deviations:
        key = deviation['session_id'], deviation['capture_id']
        require(key in attempts and deviation['code'] in DEVIATION_CODES and
                isinstance(deviation['evidence'], str) and deviation['evidence'].strip(),
                'A documented procedure deviation requires an observed identity and evidence')
        attempts[key]['reasons'].append('DOCUMENTED_DEVIATION: ' + deviation['code'])
    process_sessions = defaultdict(set)
    for session, records in starts.items():
        for record in records:
            process_sessions[tuple(record['process'].values())].add(session)
    for session, records in incomplete_starts.items():
        for record in records:
            process_sessions[tuple(record['process'].values())].add(session)
    for session, processes in partial_processes.items():
        for process in processes:
            process_sessions[process].add(session)
    for row in attempts.values():
        if row['process']:
            process_sessions[tuple(row['process'].values())].add(row['session_id'])
    for row in attempts.values():
        session, capture_id = row['session_id'], row['capture_id']
        records = starts.get(session, [])
        partial_records = incomplete_starts.get(session, [])
        row['startup_files'] = [record['name'] for record in records + partial_records]
        if partial_records:
            row['reasons'].append('UNPUBLISHED_STARTUP_STAGE')
        if session_counts[session] != 1:
            row['reasons'].append('MULTIPLE_CAPTURE_IDS_IN_SESSION')
        if capture_counts[capture_id] != 1 or len(row['files']) != 1:
            row['reasons'].append('COLLIDING_CAPTURE_ARTIFACTS')
        if Counter(record['startup_status'] for record in records) != Counter(STAGES):
            row['reasons'].append('MISSING_DUPLICATE_OR_REFUSED_STARTUP_STAGE')
        if row['process'] is not None:
            if any(record['process'] != row['process'] for record in records):
                row['reasons'].append('STARTUP_PROCESS_MISMATCH')
            if len(process_sessions[tuple(row['process'].values())]) != 1:
                row['reasons'].append('MULTIPLE_SESSIONS_FOR_PROCESS')
        else:
            candidates = ({tuple(record['process'].values()) for record in records + partial_records} |
                          partial_processes[session])
            row['diagnostic_process_candidates'] = [
                dict(pid=pid, creation_filetime=birth) for pid, birth in sorted(candidates)]
            row['reasons'].append('NO_AUTHENTICATED_SNAPSHOT_PROCESS')
        row['eligible'] = not row['reasons']
        if not row['eligible']:
            row['classification'] = INVALID
    qualified = sorted((r for r in attempts.values() if r['eligible']),
                       key=lambda r: (r['process']['creation_filetime'], r['utc'],
                                      r['session_id'], r['capture_id']))
    invalid = [row for row in attempts.values() if not row['eligible']]
    startup_sessions = set(starts) | set(incomplete_starts)
    launch_only = [dict(session_id=s, startup_files=[r['name'] for r in records],
                        process_candidates=[r['process'] for r in records],
                        status='LAUNCH_EVIDENCE_CAPTURE_UNVERIFIED')
                   for s in sorted(startup_sessions - set(session_counts))
                   for records in [starts[s] + incomplete_starts[s]]]
    return dict(schema='sor-d5as-attempt-ledger/1', synthetic=synthetic, capture_directory=str(folder),
                config_sha256=config_sha, files=files, attempts=list(attempts.values()),
                observed_attempts=len(attempts), qualified_samples=len(qualified),
                invalid_or_inconclusive=len(invalid),
                causes=dict(Counter(reason for row in invalid for reason in row['reasons'])),
                launch_only=launch_only, launch_only_sessions=len(launch_only),
                no_artifact_attempt_count=None,
                additional_eligible_required=max(N - len(qualified), 0),
                status='PROVISIONAL_NEEDS_REPLACEMENTS' if len(qualified) < N else
                       'CANDIDATE_AWAITS_PROTECTED_CLOSEOUT_AND_INDEPENDENT_REVIEW',
                earliest_eligible_candidates=[r['snapshot'] for r in qualified[:N]]
                if len(qualified) >= N else [],
                later_eligible_attempts=[r['snapshot'] for r in qualified[N:]])


def checked_package():
    value = load_json(read_file(LOCAL / 'package.json'))
    require(value['schema'] == 'sor-d5as-package/1' and value['capture_directory'] == str(CAPTURE)
            and sha(PACKAGE) == value['archive_sha256'] == PACKAGE_SHA, 'Series package changed')
    with zipfile.ZipFile(PACKAGE) as archive:
        require(archive.namelist() == sorted(value['members']) and archive.testzip() is None,
                'Series package members changed')
        for name, expected in value['members'].items():
            require(digest(archive.read(name)) == expected, 'Series member changed')
        require(digest(archive.read(PREFIX + DLL)) == DLL_SHA and
                archive.read(PREFIX + CONFIG) == (str(CAPTURE) + '\n').encode(),
                'Series DLL or sidecar mismatch')
    require(value['artifacts']['source-lock.json'] == SOURCE_LOCK_SHA, 'Series source lock differs')
    return value


def discover(references, deviations=()):
    package = checked_package()
    ledger = inventory(CAPTURE, package['members'][PREFIX + CONFIG], references, deviations)
    ledger['documented_deviations'] = deviations
    ledger['package_sha256'] = package['archive_sha256']
    ledger['method_pins'] = {str(p.relative_to(ROOT)): sha(p) for p in
                             map(Path, (__file__, raw.__file__, geometry.__file__,
                                        Path(__file__).with_name('d5as_prepare.py')))}
    ledger['reference_pins'] = references['inputs']
    return ledger


def archive_corpus(ledger, path):
    require(not ledger['synthetic'] and len(ledger['earliest_eligible_candidates']) == N,
            'Archive requires at least 30 qualified real candidates')
    partial = path.with_name(f'{path.name}.{uuid4()}.partial')
    write_archive(ledger, CAPTURE, partial)
    disk_floor()
    partial.rename(path)


def write_archive(ledger, folder, path):
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for file in ledger['files']:
            data = read_file(folder / file['name'])
            require(digest(data) == file.get('sha256'), 'Capture changed before archive')
            archive.writestr(file['name'], data)
    verify_archive(ledger, path)


def verify_archive(ledger, path):
    with zipfile.ZipFile(path) as archive:
        require(archive.namelist() == [file['name'] for file in ledger['files']],
                'Archive inventory differs from ledger')
        for file in ledger['files']:
            with archive.open(file['name']) as stream:
                observed = hashlib.file_digest(stream, 'sha256').hexdigest()
            require(observed == file.get('sha256'), 'Archive payload differs from ledger')


def publish_json(path, result):
    """Flush a unique sibling before Windows rename without replacement."""
    require(os.name == 'nt', 'Exclusive rename requires Windows')
    partial = path.with_name(f'{path.name}.{uuid4()}.partial')
    with partial.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    partial.rename(path)


def exact_null(k):
    mass = [Fraction(comb(N, x) * 6**(N - x), 7**N) for x in range(N + 1)]
    return dict(lower_inclusive=float(sum(mass[:k + 1])), upper_inclusive=float(sum(mass[k:])),
                probability_order_two_sided=float(sum(p for p in mass if p <= mass[k])),
                all_mask3_equivalent=float(mass[0]), null_p='1/7', assumes_iid=True)


def interval(k):
    """95% equal-tailed exact marginal binomial interval by tail inversion."""
    def bound(target, tail, increasing):
        low, high = 0.0, 1.0
        for _ in range(60):
            p = (low + high) / 2
            value = sum(comb(N, x) * p**x * (1-p)**(N-x) for x in tail)
            if (value < target) == increasing:
                low = p
            else:
                high = p
        return (low + high) / 2

    return [0.0 if k == 0 else bound(.025, range(k, N + 1), True),
            1.0 if k == N else bound(.025, range(k + 1), False)]


def statistics(classes):
    require(len(classes) == N and set(classes) <= {MASK0, MASK3, OTHER},
            'Statistics require a full classified roster')
    counts = Counter(classes)
    return dict(n=N, classes={key: dict(count=counts[key], fraction=counts[key]/N,
                                         iid_marginal_ci95=interval(counts[key]))
                              for key in (MASK0, MASK3, OTHER)},
                binary_proxy_test=('INCONCLUSIVE_OTHER_GEOMETRY' if counts[OTHER] else
                                   'CONDITIONAL_IID_COMPARISON'),
                null=None if counts[OTHER] else exact_null(counts[MASK0]))


def review_closeout(ledger, before, after, authorization_record, review, pins):
    require(before['schema'] == after['schema'] == 'sor-d5as-protection/1' and
            before['phase'] == 'before' and after['phase'] == 'after' and
            before['equal'] is True and after['equal'] is True and
            after['previous_sha256'] == pins['before'], 'Protected closeout is missing or inconsistent')
    from d5al_content import compare_protection
    compare_protection(before['protection'], after['protection'])
    require(before['remote_protected_sizes'] == after['remote_protected_sizes']
            and after['protection']['sync']['scientific_inputs_match'] is True,
            'Protected remote closeout differs')
    require(authorization_record['schema'] == 'sor-d5as-series-authorization/1' and
            authorization_record['decision'] == 'AUTHORIZED_BY_MAINTAINER' and
            authorization_record['package_sha256'] == PACKAGE_SHA and
            authorization_record['method_pins'] == ledger['method_pins'] and
            authorization_record['reference_pins'] == ledger['reference_pins'] and
            authorization_record['before_sha256'] == pins['before'] and
            authorization_record['maintainer_record'].strip(),
            'Exact series-level authorization record required')
    require(review['schema'] == 'sor-d5as-independent-freeze-review/1' and
            review['decision'] == 'ACCEPT' and review['reviewer'].strip() and
            review['review_record'].strip() and
            review['pins'] == pins, 'Independent review and reviewed evidence pins required')


def classify_roster(ledger, folder, references, *, synthetic=False):
    roster = []
    by_name = {r['snapshot']: r for r in ledger['attempts'] if r['eligible']}
    files = {f['name']: f for f in ledger['files']}
    for name in ledger['earliest_eligible_candidates']:
        row = by_name[name]
        data = read_file(folder / name)
        expected = files[name]['sha256']
        require(digest(data) == expected, 'Selected capture changed')
        result = geometry.classify(snapshot(data, CAPTURE_NAME.fullmatch(name)), references,
                                   synthetic=synthetic)
        require(result['eligible'] and result['body_sha256'] == row['geometry']['body_sha256'],
                'Geometry qualification changed at freeze')
        roster.append(dict(snapshot=name, sha256=expected, process=row['process'],
                           session_id=row['session_id'], capture_id=row['capture_id'], geometry=result))
    return roster


def freeze(ledger, ledger_path, archive, review_path, authorization, before_path, after_path,
           references, deviations=()):
    require(not ledger['synthetic'] and len(ledger['earliest_eligible_candidates']) == N,
            'Incomplete or synthetic corpus cannot freeze')
    require(before_path.absolute() == BEFORE, 'Use the integrated D5AS protected baseline')
    inputs = {key: read_file(path) for key, path in dict(
        ledger=ledger_path, before=before_path, after=after_path, authorization=authorization,
        review=review_path).items()}
    require(load_json(inputs['ledger']) == ledger, 'Reviewed ledger changed at freeze')
    pins = {key: digest(data) for key, data in inputs.items() if key != 'review'}
    require(pins['before'] == BEFORE_SHA, 'Integrated D5AS protected baseline changed')
    pins['archive'] = sha(archive)
    review_closeout(ledger, *(load_json(inputs[key]) for key in
                             ('before', 'after', 'authorization', 'review')), pins)
    verify_archive(ledger, archive)
    require(sha(archive) == pins['archive'], 'Archive changed during validation')
    roster = classify_roster(ledger, CAPTURE, references)
    require(discover(references, deviations) == ledger, 'Corpus or method changed at freeze')
    return dict(schema='sor-d5as-frozen-corpus/1', roster=roster, reviewed_pins=pins,
                independent_review_sha256=digest(inputs['review']), method_pins=ledger['method_pins'],
                reference_pins=ledger['reference_pins'],
                package_sha256=ledger['package_sha256'],
                later_eligible_attempts=ledger['later_eligible_attempts'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('inventory', 'archive', 'freeze'))
    parser.add_argument('output', type=Path)
    for key in ('ledger', 'archive', 'review', 'authorization', 'before', 'after', 'deviations'):
        parser.add_argument('--' + key, type=Path)
    args = parser.parse_args()
    disk_floor()
    output = safe_output(args.output)
    references = geometry.reference_bundle()
    deviations = []
    if args.deviations is not None:
        observed = load_json(read_file(args.deviations))
        require(observed['schema'] == 'sor-d5as-documented-deviations/1' and
                isinstance(observed['deviations'], list), 'Invalid aggregate deviation record')
        deviations = observed['deviations']
    result = discover(references, deviations)
    if args.action != 'inventory':
        require(args.ledger is not None and load_json(read_file(args.ledger)) == result,
                'Current corpus differs from reviewed ledger')
    if args.action == 'archive':
        archive_corpus(result, output)
        disk_floor()
        print(sha(output))
        return
    if args.action == 'freeze':
        require(output == FROZEN, 'Use the single canonical frozen-corpus.json')
        require(all((args.archive, args.review, args.authorization, args.before, args.after)),
                'Supply archive, review, series authorization and both protected checkpoints')
        result = freeze(result, args.ledger, args.archive, args.review, args.authorization,
                        args.before, args.after, references, deviations)
        result['statistics'] = statistics([row['geometry']['class_name'] for row in result['roster']])
    disk_floor()
    publish_json(output, result)
    print(output)


if __name__ == '__main__':
    main()
