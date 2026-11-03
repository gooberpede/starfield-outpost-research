# SPDX-License-Identifier: GPL-3.0-or-later
"""Focused offline A0 binding and frozen equality-oracle controls.

Reads immutable originals and the new baseline manifest. Writes one fresh
isolated receipt and a deliberately changed derivative only under D5AL scratch.
No live, save, original, network or dependency operations. SOR-P-0002 reuse of
owned D5AK/D5AJ codecs; fixture forecasts are not Episode B observations.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')
import argparse
import copy
import json
from pathlib import Path
import d5al_baseline as subject
from d5ae_baseline import guard


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    guard()
    subject.require(args.out.resolve().is_relative_to(subject.ROOT / '.local-work/d5al'), 'D5AL scratch only')
    args.out.mkdir(parents=True, exist_ok=False)
    path = subject.ROOT / '.local-work/d5al/baseline01/manifest.json'
    plan = dict(d5al_baseline=str(path), d5al_baseline_sha256=subject.sha(path))
    manifest = subject.authenticate(plan)
    checks = ['actual-full-original-authentication', 'complete-byte-normalization', 'all-36-holder-attribution']

    def reject(name, function):
        try:
            function()
        except (ValueError, KeyError, TypeError):
            checks.append(name)
        else:
            raise ValueError('Adverse input accepted: ' + name)

    for name, mutate in (
        ('swapped-equal-A1', lambda m: m['observation']['envelope'].update(snapshot_id='2')),
        ('aborted-A0-session', lambda m: m.update(session='historical-aborted-A0')),
        ('changed-process', lambda m: m['process'].update(creation_filetime=1)),
        ('synthetic-baseline', lambda m: m['observation']['envelope'].update(session_id='fixture')),
        ('changed-prediction', lambda m: m.update(prediction_sha256='0' * 64)),
        ('wrong-source', lambda m: m['observation']['envelope']['source'].update(key='wrong')),
        ('wrong-raw-equal-normalization', lambda m: m['observation'].update(raw_sha256=subject.sha(subject.SESSION / 'geometry-2.bin'))),
        ('missing-original-anchor', lambda m: m['pins'].pop(str(subject.SESSION / 'identity.json'))),
    ):
        changed = copy.deepcopy(manifest)
        mutate(changed)
        reject(name, lambda: subject.validate_binding(changed))
    changed = copy.deepcopy(manifest)
    data = bytearray(Path(manifest['normalized_path']).read_bytes())
    data[-1] ^= 1
    damaged = args.out / 'changed.normalized.bin'
    damaged.write_bytes(data)
    changed['normalized_path'] = str(damaged.resolve())
    reject('altered-complete-normalized-byte', lambda: subject.validate_binding(changed))
    raw = (subject.SESSION / 'geometry-1.bin').read_bytes()
    reject('partial-geometry', lambda: subject.geometry(raw[:-1]))
    reject('malformed-geometry', lambda: subject.geometry(b'\0' + raw[1:]))

    before = manifest['observation']
    after = copy.deepcopy(before)
    after['envelope']['session_id'] = 'separate-offline-fixture'
    after['envelope']['snapshot_id'] = '1'
    after['proof']['process_identity']['creation_filetime'] += 1
    lineage = dict(qualified=True, loss=0, relation='RECONSTRUCTED',
                   before=[before['envelope']['session_id'], '1'],
                   after=[after['envelope']['session_id'], '1'])

    def expect(name, value, expected):
        subject.require(value['prediction'] == expected, name + ': ' + str(value))
        checks.append(name)

    expect('fixture-confirmation-full-bytes', subject.assess(before, after, lineage), 'CONFIRMED')
    expect('not-executed', subject.assess(before, after, lineage, executed=False), 'NOT TESTED')
    expect('inputs-changed', subject.assess(before, after, lineage, inputs_equivalent=False), 'INCONCLUSIVE')
    expect('same-process', subject.assess(before, before, lineage), 'INCONCLUSIVE')
    changed = copy.deepcopy(after)
    region = changed['envelope']['population'][0]['regions'][0]
    # Toggle an initialized semantic flag byte, retaining valid complete geometry.
    header = bytearray.fromhex(region['header'])
    header[20] ^= 1
    region['header'] = header.hex()
    expect('fixture-contradiction-semantic-byte', subject.assess(before, changed, lineage), 'CONTRADICTED')
    for name, mutate in (
        ('source-mismatch', lambda o: o['envelope']['source'].update(key='wrong')),
        ('owner-mismatch', lambda o: o['envelope']['source'].update(body_formid='00000001')),
        ('frame-mismatch', lambda o: o['envelope']['frame'].update(owner_formid='00000001')),
        ('incomplete-geometry', lambda o: o['envelope']['capture'].update(complete=False)),
        ('malformed-points', lambda o: o['envelope']['population'][0]['regions'][0].update(points='')),
        ('relevant-loss', lambda o: o['envelope'].update(loss=1)),
    ):
        changed = copy.deepcopy(after)
        mutate(changed)
        expect(name, subject.assess(before, changed, lineage), 'INCONCLUSIVE')
    for name in ('own-grid-ending', 'owner-replacement', 'ABA', 'unknown-fence', 'missing-construction'):
        invalid = copy.deepcopy(lineage)
        invalid.update(qualified=False, relation='UNKNOWN')
        expect('unqualified-lineage-' + name, subject.assess(before, after, invalid), 'INCONCLUSIVE')
    absent = copy.deepcopy(after)
    absent['envelope'].update(population=[], frame=None)
    absent['envelope']['capture'].update(resource_slots=0, region_total=0, point_total=0)
    absent['envelope']['availability'].update(holder_present=False, exposed=False)
    unavailable = subject.assess(before, absent, lineage)
    expect('unavailable-prediction', unavailable, 'INCONCLUSIVE')
    subject.require(unavailable['observation'] == 'UNAVAILABLE', 'Availability outcome lost')
    receipt = dict(state='PASS', checks=checks, count=len(checks), baseline_sha256=subject.sha(path),
                   method_sha256=subject.sha(__file__), evaluator_sha256=subject.sha(subject.__file__),
                   limits='In-memory oracle negatives do not recreate native histories. Integrated native and source-Grid adverse controls are separate. No retail B result.')
    (args.out / 'qualification.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(state='PASS', checks=len(checks))))


if __name__ == '__main__':
    main()
