# SPDX-License-Identifier: GPL-3.0-or-later
"""Check actual owned-DLL outputs through the separate offline source method.

Reads a completed fresh D5AR build, its immutable synthetic snapshots and pinned
project sources. Writes one exclusive ignored receipt; no native execution,
target/save/database/configuration/network/Git mutation. This is an integration
control, not a retail sample or independent acquisition-origin certificate.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path

import d5ar_snapshot as raw
import d5ar_source_frames as method
from d5ar_source_frame_qualify import oracle
from d5ad_baseline import ROOT, guard, sha


def main():
    guard()
    raw.require(len(sys.argv) == 3, 'Usage: d5ar_producer_controls.py FRESH_RECEIPT BUILD_DIRECTORY')
    out, build_dir = (Path(argument).absolute() for argument in sys.argv[1:])
    raw.require(out.resolve().is_relative_to(ROOT / '.local-work/d5ar') and out.parent.is_dir() and
                not out.exists(), 'Fresh ignored D5AR output required')
    raw.require(build_dir.resolve().is_relative_to(ROOT / '.local-work/d5ar') and build_dir.is_dir(),
                'Existing ignored D5AR build required')
    raw.require(not any(p.is_symlink() or p.is_junction() for path in (out, build_dir)
                        for p in (path, *path.parents)), 'No reparse paths')
    sources = {str(Path(module.__file__).resolve()): sha(module.__file__)
               for module in tuple(sys.modules.values()) if getattr(module, '__file__', None) and
               Path(module.__file__).suffix == '.py' and Path(module.__file__).resolve().is_relative_to(ROOT)}
    profile = method.NATIVE_BUILD
    raw.require(profile is not None, 'Native producer profile remains unadmitted')
    receipt_path = build_dir / 'build.json'
    build = json.loads(receipt_path.read_bytes(), object_pairs_hook=raw.unique_pairs)
    inputs = {str(receipt_path): sha(receipt_path)}
    for path, expected in ((build_dir / 'source-lock.json', profile['source_lock_sha256']),
                           (build_dir / 'SorOutpostGeometrySnapshot.dll', profile['plugin_sha256'])):
        raw.require(sha(path) == expected, 'Exact producer bytes differ')
        inputs[str(path)] = expected
    raw.require(build['exit'] == 0 and build['source_preserved'] and
                build['dll_sha256'] == profile['plugin_sha256'] and
                build['source_lock_sha256'] == profile['source_lock_sha256'], 'Build identity/failure')
    checks, values = [], {}

    def check(name, condition):
        raw.require(condition, name)
        checks.append(dict(name=name, status='PASS'))

    refused = {status: 0 for status in ('SOURCE_LIFETIME_RETIRED', 'SOURCE_RECORDER_UNAVAILABLE')}
    for path in sorted(build_dir.glob('exact-dll-*/*.snapshot.json')):
        value, digest = raw.read_snapshot(path)
        inputs[str(path)] = digest
        check(path.parent.name + ' exact producer synthetic identity',
              value['build'] == profile and value['evidence_basis'] == 'SYNTHETIC')
        values.setdefault(path.parent.name, []).append(value)
        if value['status'] != 'COPIED_UNQUALIFIED':
            continue
        try:
            derived = method.derive(value)
        except (ValueError, TypeError, KeyError) as error:
            check(path.parent.name + ' incomplete source admission refuses', bool(str(error)))
            continue
        check(path.parent.name + ' never becomes retail evidence', derived['role'] == 'SYNTHETIC_ONLY')
        for source, row in zip(value['sources'], derived['sources']):
            status = source['source_diagnostics']['status']
            if status in refused:
                refused[status] += 1
                check(path.parent.name + ' ' + status + ' has no source basis',
                      row['frame'] is None and row['population'] is None)
                check(path.parent.name + ' ' + status + ' preserves represented geometry',
                      source['geometry'] is not None and source['geometry']['capture']['complete'])
    check('both lifetime refusal paths emitted by exact DLL', all(refused.values()))
    selected, unavailable = (values['exact-dll-' + str(mode)] for mode in (25, 40))
    check('one artifact per selected integration invocation', len(selected) == len(unavailable) == 1)
    left, right = selected[0], unavailable[0]
    first, second = method.derive(left), method.derive(right)
    check('actual protected lease record independently decoded',
          first['selected_reference']['status'] == 'QUALIFIED_SELECTED_REFERENCE_AT_NATIVE_RESOLUTION_TIME' and
          second['selected_reference']['status'] == 'UNAVAILABLE/INCONCLUSIVE')
    for label, derived in (('selected', first), ('unavailable selected identity', second)):
        qualified = [row for row in derived['sources'] if row['frame'] is not None]
        check(label + ' generic source group derives', bool(qualified))
        for row in qualified:
            direct = oracle(row['frame'], row['population'])
            check(label + ' independent complete byte oracle',
                  direct == method.normalized(row['frame'], row['population']) and
                  raw.digest(direct) == row['normalized_sha256'])
            check(label + ' has no later allocation lifetime claim',
                  row['source_allocation_scope'] == 'PROTECTED_SOURCE_GROUP_READ_ONLY_NO_LATER_LIFETIME_CLAIM')
    comparison = method.compare(left, right)
    check('generic comparison survives unavailable selected identity without inventing area',
          any(row['status'] == 'EQUAL_REPRESENTED_BYTES' for row in comparison['sources']) and
          comparison['physical_outpost_area'] == 'UNKNOWN' and comparison['historical_sampled_mask'] == 'UNKNOWN')
    raw.require(all(sha(path) == digest for path, digest in sources.items()), 'Executed source changed')
    raw.require(all(sha(path) == digest for path, digest in inputs.items()), 'Build artifact changed')
    result = dict(status='PASS', synthetic_only=True, native_execution=False, checks=checks,
                  profile=profile, source_sha256=sources, input_sha256=inputs, floors=guard())
    with out.open('xb') as stream:
        stream.write(raw.encoded(result) + b'\n')
    print(json.dumps(dict(status='PASS', controls=len(checks), receipt=str(out))))


if __name__ == '__main__':
    main()
