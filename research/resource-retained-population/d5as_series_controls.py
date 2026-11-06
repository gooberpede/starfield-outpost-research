# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AS offline controls using owned synthetic copies and disposable files.

Reads authenticated retained evidence through the D5AS geometry helper. Writes
only an exclusive local receipt and temporary fixture files removed on exit.
Requires pinned Windows CPython -E -B. No game, deployment or save operations.
"""
from copy import deepcopy
from datetime import datetime, timedelta
from fractions import Fraction
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from uuid import UUID
import zipfile

import d5ar_snapshot as raw
import d5as_geometry as geometry
from d5as_geometry_controls import fixture, reseal
import d5as_prepare as prep
import d5as_series as series
from d5al_content import content_guard


def add_snapshot(folder, value, suffix='.snapshot.json', payload=None):
    stamp = value['utc'].replace('-', '').replace(':', '')
    name = f"{stamp}_{value['session_id']}_{value['capture_id']}{suffix}"
    with (folder / name).open('xb') as output:
        output.write(raw.encoded(value) + b'\n' if payload is None else payload)
    return name


def add_startup(folder, value, seed, config, phases=None, *, partial=False):
    phases = sorted(series.STAGES) if phases is None else phases
    for i, phase in enumerate(phases):
        complete = phase != 'WAITING_STARTUP_ADMISSION'
        stamp = datetime.strptime(value['utc'], series.UTC) - timedelta(milliseconds=50 * (i + 1))
        start = dict(series.BUILD, schema='sor-d5ar-startup/1', session_id=value['session_id'],
                     **value['process'], thread=4321, wait_ms=i * 10,
                     utc=stamp.strftime(series.UTC), status=phase, config_sha256=config,
                     evidence_basis='SYNTHETIC', stack_admission_observed=complete,
                     stack_admission_complete=complete, stack_admission_code=0 if complete else 5,
                     stack_frames=9 if complete else 0, source_address_reuse='PERMANENT_REFUSAL',
                     source_history_startup_premise=
                     'FRESH_PROCESS_OFFICIAL_SFSE_PRELOAD_BEFORE_ORDINARY_SOURCE_HISTORY')
        suffix = '.partial' if partial else '.startup.json'
        with (folder / f'startup-{UUID(int=seed * 8 + i, version=4)}{suffix}').open('xb') as output:
            output.write(raw.encoded(start) + b'\n')


def main():
    output = prep.safe_output(Path(sys.argv[1]))
    free_before = prep.disk_floor()
    references, pilot = geometry.reference_bundle(), geometry.pilot_snapshot()
    prep.require(not any(prep.CAPTURE.iterdir()), 'Synthetic flight requires untouched series directory')
    checks = []

    def check(name, ok):
        prep.require(ok, 'Failed control: ' + name)
        checks.append(name)

    def refused(name, operation):
        try:
            operation()
        except (AssertionError, ValueError, FileExistsError):
            checks.append(name)
        else:
            raise RuntimeError('Expected refusal: ' + name)

    with TemporaryDirectory(dir=prep.LOCAL, prefix='synthetic-series-') as scratch:
        folder = Path(scratch) / 'capture'
        folder.mkdir()
        config = prep.digest(prep.config_bytes(folder))
        check('disposable automatic directory and sidecar round trip', len(config) == 64)
        variants = ('mask3', 'mask0', 'other')
        names, fixtures = {}, {}
        for n in reversed(range(1, 30)):
            value = fixture(pilot, references, variants[n % 3], n)
            names[n] = add_snapshot(folder, value)
            add_startup(folder, value, n, config)
            fixtures[n] = value
        for n in range(31, 41):
            fixtures[n] = fixture(pilot, references, 'mask3', n)
        partial = fixtures[31]
        partial_name = add_snapshot(folder, partial, '.partial')
        add_startup(folder, partial, 31, config)
        add_startup(folder, fixtures[32], 32, config)
        add_snapshot(folder, fixtures[33], payload=b'{')
        add_startup(folder, fixtures[33], 33, config)
        wrong_config = fixtures[34]
        add_snapshot(folder, wrong_config)
        add_startup(folder, wrong_config, 34, 'f' * 64)
        for n in (35, 36):
            fixtures[n]['process'] = deepcopy(fixtures[35]['process'])
            add_snapshot(folder, reseal(fixtures[n]))
            add_startup(folder, fixtures[n], n, config)
        colliding = fixtures[37]
        add_snapshot(folder, colliding)
        add_snapshot(folder, colliding, '.partial')
        add_startup(folder, colliding, 37, config)
        add_startup(folder, fixtures[38], 38, config, phases=['COMMAND_READY'], partial=True)
        missing = fixtures[39]
        add_snapshot(folder, missing)
        add_startup(folder, missing, 39, config, phases=['COMMAND_READY'])
        # Existing startup plus a second invocation identity in the same process.
        duplicate = fixtures[40]
        duplicate['session_id'] = missing['session_id']
        duplicate['process'] = missing['process']
        duplicate['sources'][0]['geometry']['session_id'] = missing['session_id']
        add_snapshot(folder, reseal(duplicate))
        raw_before = {p.name: prep.sha(p) for p in folder.iterdir()}
        try:
            add_snapshot(folder, fixtures[1])
        except FileExistsError:
            checks.append('exclusive create preserves an existing final')
        else:
            raise RuntimeError('Overwrite unexpectedly succeeded')
        first = series.inventory(folder, config, references, synthetic=True)
        check('planned provisional missing one', first['status'] == 'PROVISIONAL_NEEDS_REPLACEMENTS' and
              first['qualified_samples'] == 29 and first['additional_eligible_required'] == 1)
        check('exact invalid count and reasons', first['observed_attempts'] == 37 and
              first['invalid_or_inconclusive'] == 8 and
              first['causes']['MULTIPLE_SESSIONS_FOR_PROCESS'] == 2 and
              first['causes']['MULTIPLE_CAPTURE_IDS_IN_SESSION'] == 2 and
              first['causes']['UNPUBLISHED_CAPTURE_PARTIAL'] == 2 and
              first['causes']['COLLIDING_CAPTURE_ARTIFACTS'] == 1)
        check('launch-only sessions are not counted as attempts',
              first['launch_only_sessions'] == 2 and first['no_artifact_attempt_count'] is None)
        check('partial has recoverable diagnostic identity',
              next(f for f in first['files'] if f['name'] == partial_name)['process'] == partial['process'])
        check('provisional output withholds roster and final analysis',
              first['earliest_eligible_candidates'] == [] and 'null' not in first)
        check('inventory preserves original bytes',
              raw_before == {p.name: prep.sha(p) for p in folder.iterdir()})
        for n in (42, 41):
            value = fixture(pilot, references, 'other' if n == 41 else 'mask3', n)
            names[n] = add_snapshot(folder, value)
            add_startup(folder, value, n, config)
        final = series.inventory(folder, config, references, synthetic=True)
        check('synthetic replacement reaches 31 eligible with 30 candidates',
              final['qualified_samples'] == 31 and final['additional_eligible_required'] == 0 and
              final['earliest_eligible_candidates'] == [names[n] for n in range(1, 30)] + [names[41]]
              and final['later_eligible_attempts'] == [names[42]])
        check('all unsuccessful artifacts survive replacement',
              all(prep.sha(folder / name) == sha for name, sha in raw_before.items()))
        check('flight exceeds 30 distinct attempts and files', final['observed_attempts'] == 39 and
              len(final['files']) > 100)
        deviation = dict(session_id=fixtures[1]['session_id'], capture_id=fixtures[1]['capture_id'],
                         code='WRONG_SAVE', evidence='Synthetic documented deviation')
        revised = series.inventory(folder, config, references, [deviation], synthetic=True)
        check('documented wrong save excludes independently of geometry',
              revised['qualified_samples'] == 30 and
              revised['earliest_eligible_candidates'][-1] == names[42] and
              revised['causes']['DOCUMENTED_DEVIATION: WRONG_SAVE'] == 1)
        archive = Path(scratch) / 'synthetic-corpus.zip'
        series.write_archive(final, folder, archive)
        with zipfile.ZipFile(archive) as candidate:
            check('lossless archive covers qualified, invalid and status files',
                  set(candidate.namelist()) == {row['name'] for row in final['files']})
        broken_archive = Path(scratch) / 'changed.zip'
        with zipfile.ZipFile(archive) as candidate, zipfile.ZipFile(broken_archive, 'x') as broken:
            for index, name in enumerate(candidate.namelist()):
                broken.writestr(name, candidate.read(name) + (b'changed' if index == 0 else b''))
        refused('archive rejects changed payload with valid ZIP CRC',
                lambda: series.verify_archive(final, broken_archive))
        roster = series.classify_roster(final, folder, references, synthetic=True)
        check('synthetic frozen roster retains full novelty and both references',
              len(roster) == 30 and roster[-1]['geometry']['class_name'] == series.OTHER and
              all(row['geometry']['canonical_body_hex'] for row in roster) and
              {row['geometry']['class_name'] for row in roster} == {series.MASK0, series.MASK3, series.OTHER})
        refused('production freeze refuses synthetic candidate before reading receipts',
                lambda: series.freeze(final, None, None, None, None, None, None, references))
        protected_fields = dict(save_policy_sha256='fixture', protected_live={}, backups={},
                                definitions={}, config={}, archive_guard={}, file_guards={},
                                archive_content_sha256={}, installed={}, restore_rehearsal_sha256='fixture',
                                sync={'scientific_inputs_match': True})
        pins = {key: prep.digest(key.encode()) for key in
                ('ledger', 'archive', 'before', 'after', 'authorization')}
        before = dict(schema='sor-d5as-protection/1', phase='before', equal=True,
                      protection=protected_fields, remote_protected_sizes={})
        after = dict(before, phase='after', previous_sha256=pins['before'])
        final.update(method_pins={'synthetic': 'fixture'}, reference_pins={'synthetic-reference': 'fixture'})
        authorization = dict(schema='sor-d5as-series-authorization/1',
                             decision='AUTHORIZED_BY_MAINTAINER', package_sha256=series.PACKAGE_SHA,
                             method_pins=final['method_pins'], reference_pins=final['reference_pins'],
                             before_sha256=pins['before'], maintainer_record='SYNTHETIC TEST ONLY')
        review = dict(schema='sor-d5as-independent-freeze-review/1', decision='ACCEPT',
                      reviewer='Synthetic tester', review_record='SYNTHETIC TEST ONLY', pins=pins)
        series.review_closeout(final, before, after, authorization, review, pins)
        checks.append('synthetic closeout gate binds independent review, protection and source pins')
        refused('closeout refuses missing maintainer authorization',
                lambda: series.review_closeout(final, before, after,
                                               dict(authorization, decision='PENDING'), review, pins))
        refused('closeout refuses different reference pins',
                lambda: series.review_closeout(final, before, after,
                                               dict(authorization, reference_pins={}), review, pins))
        refused('closeout refuses altered reviewed ledger identity',
                lambda: series.review_closeout(final, before, after, authorization, review,
                                               dict(pins, ledger='changed')))
        changed_after = deepcopy(after)
        changed_after['protection']['restore_rehearsal_sha256'] = 'changed'
        refused('closeout refuses altered restoration content',
                lambda: series.review_closeout(final, before, changed_after, authorization, review, pins))
        exclusive = Path(scratch) / 'exclusive.json'
        series.publish_json(exclusive, {'original': True})
        expected = prep.sha(exclusive)
        refused('atomic publication collision refuses overwrite',
                lambda: series.publish_json(exclusive, {'original': False}))
        check('atomic publication collision preserves original digest', prep.sha(exclusive) == expected)
        try:
            series.archive_corpus(final, folder / 'invalid.zip')
        except ValueError:
            checks.append('synthetic candidate cannot produce production archive')
        else:
            raise RuntimeError('Synthetic archive unexpectedly succeeded')
        protected = Path(scratch) / 'synthetic-protected'
        protected.write_bytes(b'content-one')
        old = protected.stat()
        import os
        os.utime(protected, ns=(old.st_atime_ns, old.st_mtime_ns - 10_000_000))
        original = dict(bytes=old.st_size, mtime_ns=old.st_mtime_ns)
        expected = prep.digest(b'content-one')
        check('timestamp-only difference accepts identical content',
              content_guard(protected, original, expected)['timestamp_changed'])
        protected.write_bytes(b'content-two')
        os.utime(protected, ns=(old.st_atime_ns, old.st_mtime_ns))
        try:
            content_guard(protected, original, expected)
        except (AssertionError, ValueError):
            checks.append('same-size same-timestamp content change is refused')
        else:
            raise RuntimeError('Changed protected content unexpectedly accepted')

    outcome = series.statistics([series.MASK3] * 30)
    check('all-mask3 exact null tail', outcome['null']['lower_inclusive'] == float(Fraction(6, 7)**30)
          and outcome['null']['upper_inclusive'] == 1.0)
    check('probability-ordered two-sided tail', abs(outcome['null']['probability_order_two_sided'] -
          0.01666058842780394) < 1e-14)
    check('exact interval endpoints', abs(series.interval(0)[1] - (1 - .025**(1/30))) < 1e-12 and
          abs(series.interval(30)[0] - .025**(1/30)) < 1e-12)
    check('novelty suppresses binary null test',
          series.statistics([series.MASK3] * 29 + [series.OTHER])['null'] is None)
    check('series capture directory untouched', not any(prep.CAPTURE.iterdir()))
    prep.write_json(output, dict(schema='sor-d5as-series-controls/1', pass_count=len(checks),
                                checks=checks, synthetic_files=len(final['files']),
                                synthetic_observed_attempts=final['observed_attempts'],
                                source_pins={str(p.relative_to(prep.ROOT)): prep.sha(p) for p in
                                             map(Path, (__file__, series.__file__, prep.__file__,
                                                        geometry.__file__, raw.__file__))},
                                free_before=free_before, free_after=prep.disk_floor()))
    print(len(checks))


if __name__ == '__main__':
    main()
