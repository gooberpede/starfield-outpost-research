# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline qualification on exclusive ignored output. Reads existing identities,
seals and bounded evidence prefixes; writes disposable copies/ZIPs and receipts.
No process contact, build, deployment, original modification or network.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile
import archive
import adapter070
from common import fresh, guard, inventory, read, sha

ROOT = Path(__file__).resolve().parents[2]


def historical_inventory():
    result = {}
    bases = [('050-build', '.local-work/native-oracle-050'),
             ('shared-020-to-050-live', '.local-work/native-oracle-live'),
             ('050-receipts', '.local-work/ship-relocation-050'),
             ('060', '.local-work/position-write-history'),
             ('070', '.local-work/continuous-beacon-preview')]
    for label, relative in bases:
        rows = []
        for p in (ROOT/relative).rglob('*'):
            if not p.is_file() or not (p.name in ('events.bin', 'records.jsonl') or p.suffix.lower() in ('.zip', '.7z', '.zst', '.gz')):
                continue
            row = dict(path=str(p), size=p.stat().st_size)
            if p.suffix.lower() == '.zip':
                with zipfile.ZipFile(p) as z:
                    names = z.namelist()
                row.update(category='ZIP metadata inspected; contents not round-trip verified', members=len(names),
                           evidence_members=[n for n in names if Path(n).name in ('events.bin', 'records.jsonl')])
            else:
                row['category'] = 'uncompressed raw/fixture evidence' if p.suffix == '.bin' or p.name == 'records.jsonl' else 'other compressed extension; contents not verified'
            rows.append(row)
        result[label] = rows
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--metadata-only', action='store_true')
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    guard()
    if a.metadata_only:
        fresh(a.out/'historical-inventory.json', historical_inventory())
        return
    build = ROOT/'.local-work/continuous-beacon-preview/builds/qualification-06'
    pin = '20d82ecea1949265778ba2ee1af578baa9a9d2836bb82a23f48a131df7381b2a'
    m = read(build/'build.json', pin)
    protected = dict(m['protected'])
    protected.update(m['sources'])
    protected.update(m['external_runtime'])
    protected.update({m['game_path']: m['game_hash'], m['sfse_path']: m['sfse_hash']})
    protected[str(build/'build.json')] = pin
    protected[str(build/'SorNativePositionOracle.dll')] = m['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256']
    protected[str(build/'SorNativePositionOracle-0.7.0.zip')] = m['zip_sha256']
    existing = ROOT/'.local-work/continuous-beacon-preview/live/session-24552-88395531'
    historical_seal = ROOT/'.local-work/continuous-beacon-preview/run-20261014T233433728771Z/seal.json'
    protected[str(historical_seal)] = sha(historical_seal)
    for name, row in read(historical_seal)['files'].items():
        protected[str(existing/name)] = row['sha256']
    def audit():
        start = time.perf_counter()
        mismatches = [p for p, h in protected.items() if not Path(p).is_file() or sha(p) != h]
        return dict(seconds=time.perf_counter()-start, files=len(protected),
                    bytes=sum(Path(p).stat().st_size for p in protected if Path(p).is_file()), mismatches=mismatches)
    before = audit()
    fresh(a.out/'protected-before.json', dict(pins=protected, result=before))
    if before['mismatches']:
        raise ValueError('protected_before_mismatch; see receipt')
    # Exact reviewed existing full checker, without main/process/deployed actions.
    start = time.perf_counter()
    adapter070.full(build, pin)
    full_seconds = time.perf_counter()-start
    tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
                            str(Path(__file__).parent), '-p', 'test_session_tools.py', '-v'], capture_output=True)
    (a.out/'tests.txt').write_bytes(tests.stdout+tests.stderr)
    if tests.returncode:
        raise ValueError('offline_tests_failed')
    # Metadata-only historical audit; no historical archive creation/conversion.
    fresh(a.out/'historical-inventory.json', historical_inventory())
    # Evidence-shaped disposable prefixes, not production archival of a session.
    raw = a.out/'disposable/raw'
    receipts = a.out/'disposable/receipts'
    raw.mkdir(parents=True)
    receipts.mkdir(parents=True)
    sample_sources = {}
    for name, limit in [('events.bin', 16*1024*1024), ('records.jsonl', 4*1024*1024), ('health.jsonl', 1024*1024)]:
        with (existing/name).open('rb') as f:
            data = f.read(limit)
        (raw/name).write_bytes(data)
        sample_sources[name] = dict(source=str(existing/name), source_sha256=protected[str(existing/name)],
                                    prefix_bytes=len(data), copied_sha256=sha(raw/name),
                                    classification='DISPOSABLE DERIVATIVE PREFIX; not a complete or scientifically decoded session')
    fresh(receipts/'sample-provenance.json', sample_sources)
    post = receipts/'postflight.json'
    fresh(post, dict(action='postflight', process_state='EXITED', session=str(raw.resolve()),
                     status='PARTIAL_POSTFLIGHT', provenance='SYNTHETIC OFFLINE FIXTURE; no process queried'))
    roots = dict(raw=dict(path=str(raw.resolve()), kind='raw-capture'),
                 receipts=dict(path=str(receipts.resolve()), kind='private-receipt'))
    root_path = a.out/'roots.json'
    fresh(root_path, roots)
    def cli(*args):
        p = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('archive.py')), *map(str, args)], capture_output=True)
        if p.returncode:
            raise RuntimeError(p.stdout.decode(errors='replace')+p.stderr.decode(errors='replace'))
    seal = a.out/'sample-seal.json'
    cli('seal', '--input', root_path, '--sha256', sha(root_path), '--postflight', post,
        '--postflight-sha256', sha(post), '--partial-reason', 'Disposable sliced historical evidence; incomplete framing intentionally preserved.', '--out', seal)
    zipped = a.out/'disposable-evidence.zip'
    receipt = a.out/'archive-receipt.json'
    cli('create', '--input', seal, '--sha256', sha(seal), '--archive', zipped, '--out', receipt)
    cli('verify', '--input', seal, '--sha256', sha(seal), '--archive', zipped, '--archive-sha256', sha(zipped), '--out', a.out/'verify-receipt.json')
    # Durable negative receipts on disposable data. No expected failure is waived.
    bad = a.out/'truncated.zip'
    with zipped.open('rb') as src, bad.open('xb') as dst:
        dst.write(src.read(zipped.stat().st_size-25))
    negatives = {}
    for label, call in [('truncated', lambda: archive.verify(bad, read(seal))),
                        ('duplicate', lambda: archive.validate_names(['a', 'A'])),
                        ('malicious', lambda: archive.validate_names(['../escape'])),
                        ('archive_hash', lambda: archive.verify(zipped, read(seal), '0'*64))]:
        try:
            call()
        except Exception as exc:
            negatives[label] = dict(status='EXPECTED_REFUSAL', error=repr(exc))
        else:
            raise AssertionError(label+' unexpectedly accepted')
    fresh(a.out/'negative-receipts.json', negatives)
    after = audit()
    fresh(a.out/'protected-after.json', after)
    if after['mismatches']:
        raise ValueError('protected_after_mismatch')
    fresh(a.out/'summary.json', dict(status='PASS_OFFLINE_QUALIFICATION', protected_before=before,
                                    protected_after=after, existing_full_checker_seconds=full_seconds,
                                    archive=read(receipt), live='NOT TESTED; process/deployment functions mocked',
                                    source_manifest_sha256=pin, existing_captures_archived=0,
                                    existing_captures_modified=0, existing_captures_deleted=0))
    print(json.dumps(read(a.out/'summary.json'), indent=2))


if __name__ == '__main__':
    main()
