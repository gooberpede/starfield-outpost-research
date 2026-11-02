# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate D5AF source windows and retain exact local evidence locators.

Reads the owned D5AE ledger, its local exports and fresh D5AF outputs. Writes
an authored locator CSV plus a fresh ignored receipt, without copying native
instructions into Git. Stdlib only. No game, save, database, network or Git
mutation. SOR-P-0002: owned source-ledger method; Bethesda native provenance is
retained separately. Refuse missing/hash-changed inherited primary material.
"""
import csv
import io
import json
from pathlib import Path
import re
import sys

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT/'docs/experiments/resource-retained-population'


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT/'.local-work/d5af'):
        raise ValueError('Fresh task-local receipt required')
    guard()
    used, rows = {}, []
    old = DOC/'d5ae-sources.csv'
    for row in csv.DictReader(old.read_text(encoding='utf8').splitlines()):
        p = ROOT/row['path']
        if str(p) not in used:
            used[str(p)] = sha(p)
        if used[str(p)] != row['sha256']:
            raise ValueError('Inherited input drift: '+str(p))
        rows.append(dict(row, id=f'D5AF-I{len(rows)+1:03}',
                         origin='Inherited '+row['id']+'; '+row['origin']))
    for p in sorted((ROOT/'.local-work/d5af').glob('**/native.tsv')):
        text = p.read_text(encoding='utf8')
        if not text.endswith('END\n'):
            continue
        used[str(p)] = sha(p)
        for m in re.finditer(r'^FUNCTION\t([^\t]+).*?^END_FUNCTION\s*$',text,re.M|re.S):
            rows.append(dict(id=f'D5AF-N{len(rows)+1:03}',path=p.relative_to(ROOT).as_posix(),
                             sha256=used[str(p)],static_va='0x'+m[1],
                             first_line=text.count('\n',0,m.start())+1,
                             last_line=text.count('\n',0,m.end())+1,
                             origin='Bethesda native; verified disposable-project export',
                             use='Targeted lock/geometry dependency analysis',eligibility='LOCAL-ONLY'))
    direct = [ROOT/'.local-work/d5af/baseline.json',ROOT/'.local-work/d5af/inputs01.json',
              ROOT/'.local-work/d5af/inputs02.json',
              ROOT/'.local-work/d5af/incremental01.json',ROOT/'.local-work/d5af/controls01/controls.json',
              ROOT/'.local-work/d5ac/d5af-reconstruction01/summary.json',
              ROOT/'.local-work/d5ac/d5af-reconstruction01/target.json',
              ROOT/'runtime/construction-winner/observer.h',
              ROOT/'runtime/construction-winner/bridges.asm',
              ROOT/'.local-work/d5af/extra-inputs03.json',
              ROOT/'.local-work/d5af/geometry-special-inputs02.json',
              ROOT/'.local-work/d5af/geometry-summary-final02.json',
              ROOT/'.local-work/d5af/geometry-d5t-oracle.json',
              DOC/'d5t-sources.csv',DOC/'d5t/geometry.json',
              ROOT/'.local-work/d5t/native-full05.json']
    direct += sorted((ROOT/'.local-work/d5af').glob('**/result.json'))
    direct += sorted((ROOT/'.local-work/d5af').glob('**/control.json'))
    direct += sorted((ROOT/'.local-work/d5af').glob('**/population.json'))
    for p in direct:
        used[str(p)] = sha(p)
        rows.append(dict(id=f'D5AF-E{len(rows)+1:03}',path=p.relative_to(ROOT).as_posix(),
                         sha256=used[str(p)],static_va='',first_line='',last_line='',
                         origin='Owned methods/receipts; provenance within referenced artifact',
                         use='Exact byte/control identity; not proof of semantics',
                         eligibility='LOCAL-ONLY' if '.local-work' in p.parts else 'REVIEW-REQUIRED'))
    fields='id path sha256 static_va first_line last_line origin use eligibility'.split()
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n')
    writer.writeheader();writer.writerows(rows)
    target=DOC/'d5af-sources.csv'
    target.write_text(stream.getvalue(),encoding='utf8',newline='\n')
    result=dict(rows=len(rows),inputs=used,source_ledger_sha256=sha(old),
                output_sha256=sha(target),method_sha256=sha(__file__),free=guard())
    out.mkdir(parents=True)
    (out/'sources.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(rows=len(rows),unique_inputs=len(used))))


if __name__ == '__main__':
    main()
