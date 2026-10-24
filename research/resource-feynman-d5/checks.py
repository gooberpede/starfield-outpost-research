# SPDX-License-Identifier: GPL-3.0-or-later
"""Run D5 synthetic tests and verify finite accounting/byte invariants offline.

Reads frozen receipts, source files and local corpora. Writes one exclusive
ignored check directory. No target, protected inputs, network or Git writes.
Uses stdlib subprocesses for project-owned tests; no new dependencies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-feynman-d5'


def pin(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(LOCAL)
    args.output.mkdir(exist_ok=False)
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
               'research/resource-feynman-d5', '-p', 'test_*.py', '-v']
    run = subprocess.run(command, cwd=ROOT, capture_output=True)
    (args.output / 'tests-stdout.txt').write_bytes(run.stdout)
    (args.output / 'tests-stderr.txt').write_bytes(run.stderr)
    assert run.returncode == 0
    old = json.loads((ROOT / '.local-work/resource-slot-provenance/build02/normalized.json').read_text())['payload']
    new = json.loads((LOCAL / 'build04/normalized.json').read_text())['payload']
    delta = {k: len(canonical(new[k])) - len(canonical(old[k])) for k in new}
    assert sum(delta.values()) == len(canonical(new)) - len(canonical(old)) == 364
    assert {k for k in new if new[k] != old[k]} == {'bodies'}
    changed = [(body, biome) for body in new['bodies'] for biome in new['bodies'][body]['biomes']
               if new['bodies'][body]['biomes'][biome] != old['bodies'][body]['biomes'][biome]]
    assert changed == [('0005e0dc', '000fd00a')]
    assert all(pin(LOCAL / f'build02/{v}.json') == pin(LOCAL / f'build04/{v}.json') for v in ('normalized', 'expanded'))
    controls = ROOT / '.local-work/resource-slot-provenance/build-controls02'
    for name in ('geometry.py', 'context.py', 'resource_spatial.py', 'resource_availability.py', 'predictor.py'):
        assert pin(LOCAL / 'build04/code' / name) == pin(controls / 'code' / name)
    summary = json.loads((LOCAL / 'validation01/summary.json').read_text())
    assert summary['all_exact'] and summary['native_controls'] == 10
    assert summary['cases'] == 19 and summary['predicted'] == 17 and summary['associations'] == 46
    comparisons = json.loads((LOCAL / 'validation01/native-comparison.json').read_text())
    assert len(comparisons) == 20 and all(r['exact_matches'] == 1 and r['callback_equal'] for r in comparisons)
    capture = json.loads((LOCAL / 'screenshots01/manifest.json').read_text())
    assert all(pin(LOCAL / 'screenshots01' / r['filename']) == r['sha256'] for r in capture['images'])
    assert pin(capture['source']) == pin(LOCAL / 'screenshots01/original.zip') == capture['archive_sha256']
    result = dict(commands=[command], tests_exit=run.returncode, synthetic_tests=15,
        canonical_before=len(canonical(old)), canonical_after=len(canonical(new)),
        canonical_delta=364, field_deltas=delta, changed_biomes=changed,
        fresh_build_equal=True, geometry_and_inference_bytes_unchanged=True,
        native_controls=10, source_identity_qualified_controls=3,
        source_identity_other_seven='NOT TESTED: original callback receipts lack source_context',
        screenshot_originals_equal=True, summary=summary,
        failures_preserved=[dict(attempt='First corpus import', error='Missing predictor_d4e import path', correction='Use pinned inherited module directory'),
            dict(attempt='Final code audit', error='Descriptor refactor omitted inherited nonzero Everywhere guard', correction='Restore effective-RSGD own-rarity-6 chance rejection; add test; build04 is byte-identical to frozen build02'),
            dict(attempt='checks01', error='Expected a new generation block, but all referenced blocks already existed', correction='Measure and verify the actual changed-field set: bodies only'),
            dict(attempt='build01', error='Missing inherited candidate_order.py path', correction='Use explicit pinned source path in build02/build03'),
            dict(attempt='First inputs import', error='Missing geometry module search path', correction='Use owned dependency directories'),
            dict(attempt='Additional all-source identity probe', error='KeyError: source_context on legacy callback receipt',
                 correction='Retain seven resource/shape/bound controls; do not invent missing source provenance')])
    (args.output / 'checks.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(tests=15, delta=364, all_ten_geometry_exact=True)))


if __name__ == '__main__':
    main()
