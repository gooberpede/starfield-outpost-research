# SPDX-License-Identifier: GPL-3.0-or-later
"""Export selected C2D numeric traces and inventories, never raw tree/geometry data.

Reads final ignored receipts; exclusively creates reviewable JSON/CSV in the
new experiment directory. Stdlib only; run once at repository root after tests.
No target, installed-input, historical-report, Git, network or database effects.
"""
import csv
import json
import argparse
from pathlib import Path
from predict import ROOT, pin


def main(destination):
    local = ROOT / '.local-work/resource-pattern-selection'
    for name in ('installed01.json', 'installed03.json', 'blind02.json',
                 'validation05.json', 'tests02.json', 'determinism02.json'):
        if not (local / name).is_file():
            raise ValueError(f'Close required calculation before export: {name}')
    out = destination.resolve()
    assert out.is_relative_to(ROOT)
    out.mkdir(parents=True, exist_ok=True)
    prediction = json.loads((local / 'installed01.json').read_text())
    old_prediction = json.loads((local / 'blind02.json').read_text())
    validation = json.loads((local / 'validation05.json').read_text())
    def save(name, value):
        with (out / name).open('x', encoding='utf8', newline='\n') as f:
            json.dump(value, f, indent=2)
            f.write('\n')
    save('selection-v1.json', dict(schema='sor-c2d-selected-traces/1',
        installed_sites=prediction['sites'], generation_control=old_prediction['sites'],
        predictor_sha256=pin(local / 'installed01.json'),
        validator_sha256=pin(local / 'validation05.json')))
    summaries = []
    for site in validation['sites']:
        name = site['site'].lower()
        with (out / f'{name}-cells-v1.csv').open('x', encoding='utf8', newline='') as f:
            fields = ['x', 'y', 'before', 'before_source', 'after', 'source', 'pattern',
                      'initial_form', 'initial_flags', 'resolved_flags', 'used_fallback', 'rule']
            writer = csv.DictWriter(f, fields, lineterminator='\n')
            writer.writeheader()
            for cell in site['cells']:
                row = dict(cell)
                row['x'], row['y'] = row.pop('cell')
                writer.writerow(row)
        with (out / f'{name}-sources-v1.csv').open('x', encoding='utf8', newline='') as f:
            fields = ['identity', 'pattern', 'before', 'after', 'classification', 'reason',
                      'source_flags', 'nominal_dimensions', 'mask_footprint']
            writer = csv.DictWriter(f, fields, lineterminator='\n')
            writer.writeheader()
            for source in site['source_inventories']:
                row = {k: source[k] for k in fields[:6]}
                row.update(source_flags=f'0x{source["source"]["source_flags"]:02x}',
                    nominal_dimensions='x'.join(map(str, source['source']['dimensions'])),
                    mask_footprint='|'.join(map(str, source['mask_footprint'])))
                writer.writerow(row)
        summaries.append({k: v for k, v in site.items() if k not in ('cells', 'source_inventories')})
    save('results-v1.json', dict(sites=summaries, publication='REVIEW-REQUIRED',
        scope='Finite conditional base-source enumeration; no native source census'))
    paths = set(validation['inputs']) | set(prediction['inputs']) | set(old_prediction['inputs'])
    prior = json.loads((ROOT / '.local-work/resource-source-enumeration/analysis05.json').read_text())
    paths.update(prior['inputs'])
    with (ROOT / 'docs/experiments/resource-source-enumeration/sources.csv').open(newline='') as f:
        paths.update(str(ROOT / r['path']) for r in csv.DictReader(f))
    paths.update(str(ROOT / p) for p in [
        'docs/experiments/resource-source-enumeration/sources.csv',
        '.local-work/resource-geometry-mature-context/native/012.request.tsv',
        '.local-work/recon/rg1-surface-crc-01.tsv'])
    paths.add('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    paths.update(str(p) for p in (local / 'native').glob('*.tsv'))
    paths.update(str(p) for p in (local / 'native').glob('*.request'))
    paths.update(str(p) for p in (ROOT / 'research/resource-pattern-selection').glob('*.py'))
    paths.update(str(ROOT / p) for p in ['ghidra/scripts/OutpostRecon.java',
        '.local-work/resource-pattern-selection/native/E2ReadSession.java',
        '.local-work/e2-organic/native/E2ReadSession.java', '.local-work/rg1-source-definitions.py',
        'research/resource-installed-settings/replay.py', 'research/resource-source-enumeration/analyze.py',
        'research/review_package.py'])
    paths.update(str(local / p) for p in ['installed01.json', 'installed03.json', 'validation05.json',
        'tree-inventory01.json', 'tests02.json', 'determinism02.json', 'command.json'])
    paths.update(str(ROOT / p) for p in [
        '.local-work/resource-installed-settings/c2d-replay01.json',
        '.local-work/resource-installed-settings/c2d-geometry01.json'])
    with (out / 'sources.csv').open('x', encoding='utf8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['id', 'path', 'bytes', 'sha256', 'use'])
        for ordinal, name in enumerate(sorted(paths), 1):
            path = Path(name)
            label = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
            writer.writerow([f'C2D-S{ordinal:03d}', label, path.stat().st_size, pin(path),
                'Pinned primary or owned method; raw proprietary inputs remain LOCAL-ONLY'])
    print('Exported selected traces, two source inventories, 756 cell rows and source pins')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-directory', type=Path,
                        default=ROOT / 'docs/experiments/resource-pattern-selection')
    main(parser.parse_args().output_directory)
