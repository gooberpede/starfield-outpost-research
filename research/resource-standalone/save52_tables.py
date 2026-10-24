# SPDX-License-Identifier: GPL-3.0-or-later
"""Write limited D2 authored aggregate tables from closed local evidence.

Reads ignored inventories/comparisons; writes new research CSV/Markdown and
source-hash ledger under docs/experiments/resource-save52. No raw bodies,
coordinates, geometry, native pointers or personal source basenames exported.
Stdlib/project only. These tables remain REVIEW-REQUIRED, not publication-cleared.
"""
import collections
import csv
import json
from pathlib import Path

import save52 as s


def table(path,rows):
    with path.open('x',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def run():
    dest=s.ROOT/'docs/experiments/resource-save52'
    inv=json.loads((s.OUT/'inventory-v2.json').read_text())
    summary=json.loads((s.OUT/'first-pass-v1/summary.json').read_text())
    comparisons=json.loads((s.OUT/'comparison-v3/pairs.json').read_text())
    manual=json.loads((s.OUT/'diagnostics-v3.json').read_text())['membership']
    rows=[]
    for r in inv['cases']:
        p=next((v for v in summary if v['case']==r['case']),{})
        counts=collections.Counter(v['outcome'] for v in comparisons if v['case']==r['case'])
        rows.append(dict(case=r['case'],name=r['name'][0],body='0x'+r['body'],
            saved_state='SAVED_ACTIVE_QUALIFIED' if r['eligibility']=='ACTIVE' else r['eligibility'],
            control=r['control'],manual_name_body_match=next(v['body_equal'] for v in manual if v['case']==r['case']),
            frame=f'0x{r["frame"]:02x}',prediction=p.get('status','EXCLUDED_DISABLED'),
            supported_positive_resources=sum(v['status']=='PRESENT' for v in p.get('resources',{}).values()),
            corroborated=counts['POSITIVE_CORRESPONDENCE'],candidate=counts['POTENTIAL_FALSE_NEGATIVE'],
            indeterminate=counts['UNSUPPORTED_INDETERMINATE'],alternative=counts['ALTERNATIVE_ADMISSION'],
            coverage_reasons='; '.join(sorted({v['reason'] for v in p.get('failures',[])}))))
    table(dest/'cases.csv',rows)
    table(dest/'comparison.csv',[{k:r[k] for k in ('case','control','resource','label','outcome','extractors')} for r in comparisons])
    lines=['# Save52 population and prediction inventory','',
        '2026-10-24, Australia/Sydney. Limited authored aggregate, REVIEW-REQUIRED.',
        'Names are navigation labels opened outside inference; they did not select resources.',
        'Body values are installed main-file FormIDs; case suffixes are saved tokens.',
        'Saved-active qualification combines clear flags, saved collection membership,',
        'Workshop/body joins and later manual name/body corroboration. Authoritative',
        'player membership and current runtime state remain unverified. See the [report](report.md).','',
        '| Case | Original navigation name | Body FormID | Saved state | Role | Prediction |',
        '|---|---|---|---|---|---|']
    for r in rows:
        lines.append(f'| `{r["case"]}` | {r["name"].replace("|", "/")} | `{r["body"]}` | {r["saved_state"]} | '+
                     ('Known control' if r['control'] else 'Held out' if r['saved_state']=='SAVED_ACTIVE_QUALIFIED' else 'Excluded')+
                     f' | {r["prediction"]} |')
    (dest/'population.md').write_bytes(('\n'.join(lines)+'\n').encode())
    paths=[s.OUT/p for p in ('inventory-v1.json','inventory-v2.json','requests-v1.json','build-v1/manifest.json',
        'build-v1/normalized.json','first-pass-v1/input-freeze.json','first-pass-v1/prediction-freeze.json',
        'first-pass-v1/summary.json','comparison-v1/answer-access.json','comparison-v2/summary.json',
        'comparison-v3/answer-access.json','comparison-v3/summary.json','comparison-v3/instances.json',
        'comparison-v3/pairs.json','comparison-v3/extras.json','diagnostics-v3.json')]
    paths += [s.builder.ESM,s.builder.EXE,s.builder.ARCHIVE,
        s.ROOT/'.local-work/resource-standalone/build03/normalized.json']
    paths += [s.ROOT/('save-analysis/scripts/'+n) for n in ('stream_save.py','outpost_planetary_location.py',
        'outpost_membership.py','ordinary_outpost_beacons.py','workshop_inventory.py','extractor_resources.py',
        'research_workshop_origin.py','planet_world_key.py','saved_world_components.py','audit_beacon_projection.py',
        'research_durable_center.py','durable_position_model.py','inspect_outpost_definitions.py')]
    paths += list(s.builder.OWNED.glob('*.py'))
    ledger=[]
    for i,p in enumerate(paths,1):
        ledger.append(dict(id=f'D2-S{i:03}',path=p.relative_to(s.ROOT).as_posix() if p.is_relative_to(s.ROOT) else str(p),
            bytes=p.stat().st_size,sha256=s.builder.pin(p),
            use='Owned method under SOR-P-0002 or primary local evidence; payloads remain LOCAL-ONLY'))
    table(dest/'sources.csv',ledger)
    print(json.dumps(dict(cases=len(rows),comparison_rows=len(comparisons),sources=len(ledger))))


if __name__=='__main__':
    run()
