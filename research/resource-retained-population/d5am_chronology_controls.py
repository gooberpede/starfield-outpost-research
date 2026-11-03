# SPDX-License-Identifier: GPL-3.0-or-later
"""Cross-check D5AM chronology with sealed independent wire/geometry methods.

SOR-P-0002 covers conceptual reuse of owned sealed D5AK/D5AL oracles and the
existing readers. Reads only stopped recordings, seals, plans and source locks.
Writes one exclusive D5AM-local receipt. No live, save or database operations.
Uses installed Python -E -B and stdlib; refuses optimization before any output.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import csv
import json
from pathlib import Path
import struct
import subprocess

from d5am_chronology import ROOT, dump, frames, guard, module, owner_context, require, sha


def independent_context(raw, generation_sequence, birth_sequence):
    """Separate fixed-offset participant census; no production grouping helper."""
    values = [struct.unpack_from('<18Q', raw, offset + 16) for offset in range(0, len(raw), 328)]
    proc, source = values[generation_sequence - 1][9], values[birth_sequence - 1][10]
    active = {r[2] for r in values if r[1] == 3 and r[10] == source and not r[13]}
    starts = [r for r in values if r[1] == 1 and r[2] in active]
    finishes = [r for r in values if r[1] == 4 and r[10] == source and r[2] in active]
    low, high = min(r[0] for r in starts), max(r[0] for r in finishes)
    early, late = min(r[5] for r in starts), max(r[5] for r in finishes)
    groups = {}
    for row in values:
        if row[2]:
            groups.setdefault(row[2], []).append(row)
    expected, included, left_crossings, right_crossings = {}, set(), set(), set()
    for invocation, rows in groups.items():
        if not any(row[9] == proc for row in rows):
            continue
        a, b = [r for r in rows if r[1] == 1], [r for r in rows if r[1] == 9]
        valid = len(a) == len(b) == 1 and a[0][0] < b[0][0] and a[0][5] <= b[0][5]
        sequence = valid and a[0][0] <= high and b[0][0] >= low
        qpc = valid and a[0][5] <= late and b[0][5] >= early
        if not valid or sequence or qpc:
            included.update(r[0] for r in rows)
            expected[invocation] = dict(entry=a[0][0] if valid else 'UNKNOWN', returned=b[0][0] if valid else 'UNKNOWN',
                                       sequence_overlap=bool(sequence), qpc_overlap=bool(qpc), context_records=len(rows))
            if valid and a[0][0] < low <= b[0][0]:
                left_crossings.add(invocation)
            if valid and a[0][0] <= high < b[0][0]:
                right_crossings.add(invocation)
    included.update(r[0] for r in values if not r[2] and r[9] == proc and (low <= r[0] <= high or early <= r[5] <= late))
    return expected, included, left_crossings, right_crossings


def interval_adversaries():
    def event(sequence, kind, invocation, ticks):
        return dict(sequence=sequence, kind=kind, invocation=invocation, ticks=ticks, proc=1, thread=1)
    events = [event(8, 1, 1, 120), event(9, 9, 1, 180),
              event(15, 1, 2, 50), event(16, 9, 2, 90), event(3, 2, 3, 300),
              event(30, 1, 4, 300), event(31, 9, 4, 310),
              event(4, 1, 5, 20), event(5, 1, 5, 30), event(6, 9, 5, 40),
              event(40, 1, 6, 200), event(41, 9, 6, 200)]
    context, participants = owner_context(events, 1, dict(sequence=10, ticks=100), dict(sequence=20, ticks=200))
    by_id = {row['invocation']: row for row in participants}
    require(set(by_id) == {1, 2, 3, 5, 6}, 'Overlap union, tie or unknown endpoint refused')
    require(by_id[1]['qpc_overlap'] and not by_id[1]['sequence_overlap'], 'QPC-only overlap omitted')
    require(by_id[2]['sequence_overlap'] and not by_id[2]['qpc_overlap'], 'Reservation-only overlap omitted')
    require(by_id[3]['endpoints'] == by_id[5]['endpoints'] == 'UNKNOWN', 'Missing/duplicate endpoints promoted')
    require({row['sequence'] for row in context} == {e['sequence'] for e in events if e['invocation'] != 4}, 'Whole context omitted')
    return dict(check='interval-adversaries', qpc_only=True, reservation_only=True, ties_included=True,
                missing_duplicate_endpoints_included=True, disjoint_known_interval_excluded=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chronology', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(args.out.absolute().resolve().is_relative_to(ROOT / '.local-work/d5am'), 'D5AM-local output required')
    require(not any(p.is_symlink() or p.is_junction() for p in (args.out.absolute(), *args.out.absolute().parents)), 'Reparse output path')
    guard()
    summary_bytes = args.chronology.read_bytes()
    summary = json.loads(summary_bytes)
    sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
    sys.path.insert(0, str(ROOT / 'research/resource-retained-population'))
    oracle = module('d5am_sealed_independent_oracle', ROOT / '.local-work/d5al/b-live01/analyze.py')
    official = module('d5am_official_core', ROOT / 'runtime/construction-winner/read_capture.py')
    method = ROOT / 'research/resource-retained-population/d5am_chronology.py'
    controls, sources, plans = [], {}, []
    context_path = args.chronology.parent / 'review-tables/d5am-retail-owner-events.csv'
    participant_path = args.chronology.parent / 'review-tables/d5am-retail-owner-participants.csv'
    with context_path.open(newline='') as stream:
        actual_context = list(csv.DictReader(stream))
    with participant_path.open(newline='') as stream:
        actual_participants = list(csv.DictReader(stream))
    known_left = {'B2': {3823, 3825, 3827, 3829, 3835}, 'A0': {3871, 3872}, 'A1': set(), 'B0': set()}
    known_right = {'B2': {3835, 3837, 3840, 3846, 3860, 3865, 3945, 3977}, 'A0': {3871, 3872, 3875},
                   'A1': {33653, 33670, 33681, 33711, 33713, 33715, 33722, 33724, 33726, 33728},
                   'B0': {3471, 3483, 3485, 3490, 3492, 3497, 3499, 3501, 3507}}
    originals = {}
    for row in summary['sessions']:
        session = Path(row['session'])
        raw = (session / 'events.bin').read_bytes()
        original = frames(raw)
        require(original == oracle.core(raw), 'Independent core field mismatch')
        require(all(e == official.decode(raw[i * 328 + 16:(i + 1) * 328]) for i, e in enumerate(original)),
                'Official decode field mismatch')
        controls.append(dict(case=row['case'], check='all-core-fields-agree', records=len(original)))
        for generation in row['generations']:
            label = generation['label']
            expected, expected_context, left, right = independent_context(raw, generation['generation'], generation['birth'])
            actual = {int(r['invocation']): r for r in actual_participants if r['episode'] == label}
            require(set(actual) == set(expected), 'Independent participant census mismatch: ' + label)
            require({int(r['sequence']) for r in actual_context if r['episode'] == label} == expected_context,
                    'Independent whole-context event census mismatch: ' + label)
            for invocation, values in expected.items():
                for key, value in values.items():
                    require(actual[invocation][key] == str(value), 'Participant endpoint/overlap field mismatch')
            require(left == known_left[label] and right == known_right[label], 'Known boundary crossings changed')
            controls.append(dict(episode=label, check='independent-struct-participant-census',
                invocations=len(expected), context_records=len(expected_context),
                left_crossings=sorted(left), right_crossings=sorted(right)))
        for name, data in [('corrupt', bytes([raw[0] ^ 1]) + raw[1:]), ('partial', raw[:-1]), ('duplicate', raw[:328] * 2)]:
            try:
                frames(data)
            except ValueError:
                controls.append(dict(case=row['case'], check=name, refused=True))
            else:
                raise ValueError('Corrupt core accepted')
        originals[str(session / 'events.bin')] = sha(raw)
        if row['case'] == 'B2':
            invocation_path = ROOT / '.local-work/d5ab/B2-APPROVED-002-notes/arrival-request-a824807a8c6a46e2b916dd740bdddd1c-invocation.json'
            invocation = json.loads(invocation_path.read_bytes())['command']
            plan_path = Path(invocation[invocation.index('--plan') + 1])
            expected = invocation[invocation.index('--plan-sha256') + 1]
        else:
            case_path = ROOT / ('.local-work/d5ak/a-live01' if row['case'] == 'A' else '.local-work/d5al/b-live01')
            binding = json.loads((case_path / 'binding.json').read_bytes())
            plan_path, expected = Path(binding['plan']), binding['plan_sha256']
            comparison = json.loads((case_path / 'comparison01.json').read_bytes())
            for number, observation in ((1, comparison['before']), (2, comparison['after'])) if row['case'] == 'A' else ((1, comparison['after']),):
                raw_geometry = (session / f'geometry-{number}.bin').read_bytes()
                parsed = oracle.geometry(raw_geometry)
                envelope, proof = observation['envelope'], observation['proof']
                target = parsed['holders'][proof['source']['source_pointer']]
                require(target['holder'] == proof['holder_pointer'], 'Target holder mismatch')
                normalized = oracle.normalized(envelope['source'], envelope['frame'], target['resources'])
                expected_bytes = (case_path / (f'oracle-snapshot-{number}.normalized.bin' if row['case'] == 'A' else 'B0.normalized.bin')).read_bytes()
                require(normalized == expected_bytes and len(normalized) == 5090, 'Full target geometry differs')
                require(sha(normalized) == '0c05d4a4c458b533d1ec7ae3acc8b34698ac48b91ff2965224e5c37ca055da96', 'Target normalized pin mismatch')
                generation = original[proof['generation']['generate_sequence'] - 1]
                descriptor = [e for e in original if e['kind'] == 5 and e['invocation'] == generation['invocation'] and e['selection'] == generation['selection']]
                require(len(descriptor) == 1, 'Ambiguous construction frame')
                d = bytes.fromhex(descriptor[0]['descriptor'])
                require((d[:1] + d[4:]).hex() == envelope['frame']['descriptor_semantic'], 'Actual frame mismatch')
                try:
                    oracle.geometry(raw_geometry[:-1])
                except ValueError:
                    pass
                else:
                    raise ValueError('Partial geometry accepted')
                changed = bytearray(normalized)
                changed[-1] ^= 1
                require(changed != expected_bytes, 'Changed semantic byte equals baseline')
                controls.append(dict(case=row['case'], snapshot=number, check='independent-complete-geometry',
                    bytes=len(normalized), sha256=sha(normalized), partial_refused=True, semantic_change_detected=True))
        raw_plan = plan_path.read_bytes()
        require(sha(raw_plan) == expected, 'Historical plan differs from sealed invocation/binding')
        plan = json.loads(raw_plan)
        identity = row['identity']
        require(plan['dll_sha256'] == identity['dll_sha256'] and plan['game_sha256'] == identity['host_sha256'], 'Plan/producer identity mismatch')
        require(plan['sites'] == identity['sites'] or all(
            p['rva'] == i['rva'] and p['guard_sha256'] == i['guard_sha256'] for p, i in zip(plan['sites'], identity['sites'])),
            'Plan/producer sites differ')
        lock_rows = {}
        for key in ('d5ak_source_lock', 'd5aj_source_lock', 'd5al_source_lock', 'checkpoint_source_lock_path'):
            if key not in plan:
                continue
            path = Path(plan[key])
            expected_lock = plan.get(key + '_sha256', plan.get(key.replace('_path', '_sha256')))
            raw_lock = path.read_bytes()
            require(expected_lock is not None and sha(raw_lock) == expected_lock, 'Source-lock hash mismatch')
            lock = json.loads(raw_lock)
            lock_rows[str(path)] = dict(sha256=sha(raw_lock), schema=lock.get('schema'), source_count=len(lock.get('sources', {})))
            for source, expected_source in lock.get('sources', {}).items():
                source_path = Path(source)
                actual = sha(source_path.read_bytes())
                require(actual == expected_source, 'Source-lock member mismatch: ' + source)
                sources[str(source_path)] = actual
        plans.append(dict(case=row['case'], path=str(plan_path), sha256=expected,
            native_version=plan.get('native_version', 'UNKNOWN_NOT_EXPLICIT_IN_PLAN'), dll_sha256=plan['dll_sha256'],
            site_count=len(plan['sites']), locks=lock_rows))
        sources[str(plan_path)] = expected
    for entry in (method, Path(__file__)):
        for flags, environment in ((['-E', '-B', '-O'], None), (['-E', '-B', '-OO'], None),
                                   (['-E', '-B'], dict(os.environ, PYTHONOPTIMIZE='1'))):
            result = subprocess.run([sys.executable, *flags, str(entry), '--help'], capture_output=True, text=True, env=environment)
            require(result.returncode != 0 and 'optimization is forbidden' in result.stderr, 'Optimization was not refused')
            controls.append(dict(check='optimization-refusal', entry=entry.name, flags=flags, inherited_environment=environment is not None))
    controls.append(interval_adversaries())
    for path, expected in originals.items():
        require(sha(Path(path).read_bytes()) == expected, 'Original changed')
    sources[str(Path(__file__))] = sha(Path(__file__).read_bytes())
    sources[str(method)] = sha(method.read_bytes())
    sources[str(ROOT / '.local-work/d5al/b-live01/analyze.py')] = sha((ROOT / '.local-work/d5al/b-live01/analyze.py').read_bytes())
    dump(args.out, dict(state='PASS', chronology_sha256=sha(summary_bytes), controls=controls, plans=plans,
                        source_sha256=sources, originals_unchanged=True, free=guard(),
                        limit='Independent wire and retained geometry checks; no new native execution or retail scheduling measurement.'))
    print(json.dumps(dict(state='PASS', controls=len(controls), source_pins=len(sources))))


if __name__ == '__main__':
    main()
