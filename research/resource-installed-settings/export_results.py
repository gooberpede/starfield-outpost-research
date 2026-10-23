# SPDX-License-Identifier: GPL-3.0-or-later
"""Export selected authored numeric C1H results, never raw source payloads.

Reads closed local replay/settings and their source pins, plus original methods.
Exclusively writes three versioned JSON/CSV files in the new experiment folder.
Stdlib only; no save, game, config, analysis or Git mutation. Review required.
"""
import csv
import json
from pathlib import Path
from settings import ROOT, pin

def main():
    local=ROOT/'.local-work/resource-installed-settings'
    out=ROOT/'docs/experiments/resource-installed-settings'
    out.mkdir(exist_ok=True)
    settings=json.loads((local/'settings01.json').read_text())
    replay=json.loads((local/'replay02.json').read_text())
    pins=dict(settings['pins'])|replay['inputs']
    paths=[local/'settings01.json',local/'replay02.json',local/'geometry02.json',
           local/'protected-before.json',local/'baseline.json',local/'tests02.json',
           ROOT/'.local-work/resource-geometry/native/019.request.tsv',
           ROOT/'.local-work/resource-region-ancestry/analysis-attempt01.json',
           ROOT/'.local-work/resource-geometry-mature-context/selection-empty-local.json',
           ROOT/'.local-work/resource-geometry-mature-context/selection-inherited-water.json',
           ROOT/'.local-work/outpost-biomes/feynman v.biom',ROOT/'.local-work/outpost-biomes/carinae iii-a.biom',
           ROOT/'.local-work/recon/resource-availability-cont-01.tsv']
    paths.extend((ROOT/'.local-work/resource-selection-operands/native').glob('settings*.tsv'))
    paths.extend((ROOT/'research/resource-installed-settings').glob('*.py'))
    paths.extend((ROOT/'research/editorial').glob('*'))
    for site in replay['sites']:
        if site['site']=='Feynman':
            c1e=ROOT/'.local-work/resource-region-ancestry/retail-attempt01'
            paths.extend(c1e/f'capture-{r["capture"]:05d}.bin' for r in site['accepted'])
            c1g=ROOT/'.local-work/resource-selection-operands/retail-attempt01'
            paths.extend(c1g/f'capture-{n:05d}.bin' for r in site['chance_comparison'] for n in (r['capture'],r['call_capture']))
    pins.update({str(p):pin(p) for p in paths if p.is_file()})
    assert all(pin(p)==h for p,h in pins.items())
    for name,value in (('predictions-installed-v1.json',replay),('settings-provenance-v1.json',settings)):
        with (out/name).open('x',encoding='utf8',newline='\n') as f:
            json.dump(value,f,indent=2);f.write('\n')
    with (out/'sources.csv').open('x',encoding='utf8',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['source_id','path','bytes','sha256','role'])
        for i,(path,h) in enumerate(sorted(pins.items()),1):
            p=Path(path)
            locator=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)
            w.writerow([f'C1H-S{i:03d}',locator,p.stat().st_size,h,
                        'Original owned method; REVIEW-REQUIRED' if locator.startswith('research/') else 'Primary or derived input; raw bytes LOCAL-ONLY; see sources.md'])
    print('exported selected results and',len(pins),'pins')

if __name__=='__main__':main()
