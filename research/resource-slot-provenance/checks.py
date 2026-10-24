# SPDX-License-Identifier: GPL-3.0-or-later
"""Retain offline tests, local field costs and per-use evidence/method hashes.

Reads task outputs, installed ESM and owned methods. Writes an exclusive ignored
check directory plus authored sources.csv metadata. No target, original evidence,
save, analysis database, network, Git index or ref writes. Stdlib only.
"""
import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'research' / p) for p in
               ('resource-standalone', 'resource-owner-root')]
import builder
from audit import pin, write
from qualification import qualify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assert args.label.isalnum()
    local = ROOT / '.local-work/resource-slot-provenance'
    out = local / args.label
    out.mkdir(exist_ok=False)
    for name in ('resource-slot-provenance', 'resource-owner-root', 'resource-standalone'):
        run = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
            str(ROOT / 'research' / name), '-p', 'test_*.py', '-v'], cwd=ROOT, capture_output=True)
        (out / f'{name}-tests.txt').write_bytes(run.stdout + run.stderr)
        assert run.returncode == 0, run.stderr.decode()
    comparison = json.loads((local / 'comparison03/comparison.json').read_text())
    assert len(comparison['slots']) == 48 and all(r['equal'] and r['identity_equal'] and
        r['root_equal'] and r['second_key_equal'] for r in comparison['slots'])
    assert all(r['equal'] for r in comparison['transitions'])
    assert comparison['calls_equal'] and comparison['final_selected_equal']
    costs = []
    for build in ('build02', 'build-controls02'):
        prep = json.loads((local / build / 'preparation.json').read_text())
        before = json.loads(Path(prep['base']).read_text())['payload']
        after = json.loads((local / build / 'normalized.json').read_text())['payload']
        size = lambda value: len(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())
        fields = {key: size(after[key]) - size(before[key]) for key in before if after[key] != before[key]}
        assert sum(fields.values()) == prep['incremental_payload_bytes']
        costs.append(dict(build=build, incremental_bytes=prep['incremental_payload_bytes'], field_deltas=fields))
    write(out / 'field-costs.json', costs)
    records = {h['formid']: (h, fs) for h, fs in builder.esm_records(builder.ESM,
        {b'PNDT', b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
    prediction = json.loads((local / 'freeze01/prediction-v1.json').read_text())
    qualification = {body: qualify(records, builder.selections(records, int(body, 16)))
                     for body in prediction}
    write(out / 'projection-qualification.json', qualification)
    dependencies = []
    for body, value in prediction.items():
        for row in value['components']:
            ids = [int(body, 16), row['biome'], row['rsgd']]
            ids += [int.from_bytes(raw, 'little') for tag, raw in records[row['biome']][1] if tag == b'RNAM']
            ids += [fid for fid in row['slots'] if fid]
            dependencies.append(dict(body=body, biome=row['biome'], fields=[dict(formid=f'0x{fid:08x}',
                header=records[fid][0], subrecord_pins=[dict(tag=tag.decode(), bytes=len(raw),
                    sha256=builder.hashlib.sha256(raw).hexdigest()) for tag, raw in records[fid][1]
                    if tag in (b'RNAM', b'SNAM', b'PPBD', b'RSCS', b'CNAM', b'DNAM')]) for fid in dict.fromkeys(ids)]))
    write(out / 'installed-lineage.json', dependencies)
    write(out / 'failures.json', [
        dict(attempt='d4e-slotrefs01', result='PARTIAL EXPORT', reason='Non-entry address 0x140771fa0; no END; containing-function export in producers02'),
        dict(attempt='comparison01', result='COMPARATOR FAIL', reason='Integer versus JSON string map keys; retained; canonical key comparison passes in comparison02/03'),
        dict(attempt='validation01', result='COMPARATOR FAIL', reason="KeyError alternative: wrong inherited CSV columns; method and completed frozen predictions retained; corrected comparator reuse in validation02"),
        dict(attempt='build01 / validation02', result='PRESERVED COVERAGE REGRESSION', reason='Small unequal-rarity tie rejected conservatively; source-backed stable insertion refinement in build02')])
    sources = {}
    def add(path, use):
        path = Path(path)
        assert path.exists(), path
        sources[path] = use
    seal = json.loads((local / 'freeze01/freeze-v1.json').read_text())
    for path in seal['inputs']:
        add(path, 'Pinned installed or owned input; no D4D answer supplied to builder')
    for path in seal['methods']:
        add(path, 'Owned independent component/map preparation method; SOR-P-0002')
    for relative, use in (
        ('research/resource-standalone/predictor_d3.py', 'Owned D3 predictor adapted into predictor_d4e.py; SOR-P-0002'),
        ('research/resource-standalone/corpus_d3.py', 'Owned descriptor resolver reused conservatively; SOR-P-0002'),
        ('research/resource-standalone/isolate.py', 'Owned inference read boundary; SOR-P-0002'),
        ('research/resource-standalone/verify.py', 'Owned native decoder/control request methods; SOR-P-0002'),
        ('research/resource-owner-root/package.py', 'Owned exact patch exporter adapted; SOR-P-0002'),
        ('research/resource-owner-root/audit.py', 'Owned preservation audit adapted; SOR-P-0002'),
        ('research/resource-tungsten-repair/regressions.py', 'Owned historic regression driver adapted; SOR-P-0002'),
        ('research/resource-tungsten-acquisition/qualify.py', 'Owned independent SRO1 decoder reused; SOR-P-0002'),
        ('research/resource-owner-acquisition/compare.py', 'Owned guarded chain decoder reused; SOR-P-0002'),
        ('research/workshop-population/export.ps1', 'Owned read-only Ghidra launcher; SOR-P-0002'),
        ('research/workshop-population/ReadSpecialist.java', 'Owned read-only native export method; SOR-P-0002'),
        ('runtime/session-tools/export_review.py', 'Owned exact byte patch serialization/application; SOR-P-0002'),
        ('research/editorial/screen.py', 'Owned changed-text editorial screen; SOR-P-0002'),
        ('.local-work/recon/resource-availability-ui-28.tsv', 'Existing complete native sixth-slot writer'),
        ('.local-work/recon/resource-availability-ui-29.tsv', 'Existing native small-list insertion-sort instructions'),
        ('docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D4E_component_slot_provenance_owner_root_prediction.md', 'Unchanged governing brief')):
        add(ROOT / relative, use)
    for path in (ROOT / 'research/resource-slot-provenance').glob('*.py'):
        add(path, 'D4E authored research method; adaptations identified above')
    for path in (ROOT / '.local-work/workshop-population-rework/specialist').glob('d4e-*'):
        add(path, 'STATIC export/log; slotrefs01 is preserved partial failure')
    for path in local.rglob('*'):
        if path.is_file():
            add(path, 'Local prediction, comparison, check, failure or preservation receipt')
    for path, digest in comparison['receipt_pins'].items():
        assert pin(path) == digest
        add(path, 'Original D4D answer opened after independent freeze')
    for row in json.loads((local / 'validation03/native-comparison.json').read_text()):
        folder, attempt = {'0005e0de': ('resource-region-ancestry', '01'),
            '0005e4da': ('resource-carinae', '02'),
            '0005de4c': ('resource-tungsten-acquisition', '01')}[row['body']]
        path = ROOT / f'.local-work/{folder}/retail-attempt{attempt}/capture-{row["capture"]:05d}.bin'
        assert pin(path) == row['receipt_sha256']
        add(path, 'Original native geometry control; post-prediction comparison only')
    target = ROOT / 'docs/experiments/resource-slot-provenance/sources.csv'
    with target.open('w', encoding='utf8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['id', 'path', 'bytes', 'sha256', 'use', 'eligibility'])
        for index, (path, use) in enumerate(sorted(sources.items()), 1):
            display = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
            writer.writerow([f'D4E-S{index:03d}', display, path.stat().st_size, pin(path), use,
                'REVIEW-REQUIRED authored method/metadata' if path.is_relative_to(ROOT) and '.local-work' not in path.parts
                else 'LOCAL-ONLY payload; metadata REVIEW-REQUIRED'])
    print(json.dumps(dict(sources=len(sources), field_costs=costs, tests='PASS')))


if __name__ == '__main__':
    main()
