# SPDX-License-Identifier: GPL-3.0-or-later
"""Export bounded C2C numeric interpretation and pins; raw inputs stay local.

Reads the closed analysis05 and unchanged C1H control replay. Creates new versioned
Markdown-free JSON/CSV documents exclusively. Stdlib only; no target effects.
Requires repository root and the analysis/controls described in verification.md.
"""
import csv
import json
from pathlib import Path
from analyze import ROOT, pin

OUT=ROOT/'docs/experiments/resource-source-enumeration'
LOCAL=ROOT/'.local-work/resource-source-enumeration'


def write_json(name,value):
    with (OUT/name).open('x',encoding='utf8',newline='\n') as stream:
        json.dump(value,stream,indent=2);stream.write('\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    path=LOCAL/'analysis05.json'
    result=json.loads(path.read_text())
    for site in result['sites']:
        before={s['id'] for s in site['before']}
        after=site.get('after',site['before'])
        after_ids={s['id'] for s in after}
        for phase,rows in (('before',site['before']),('after',after),('candidates',site['candidate_after'])):
            name=f'{site["site"].lower()}-{phase}-v1.csv'
            with (OUT/name).open('x',encoding='utf8',newline='') as stream:
                writer=csv.DictWriter(stream,fieldnames=['source','pattern','block','geographic_x','geographic_y',
                    'local_x','local_y','origin_x','origin_y','nominal_x','nominal_y','padding',
                    'source_flags','in_before','in_after','classification','reason'],lineterminator='\n')
                writer.writeheader()
                for s in rows:
                    writer.writerow(dict(source=s['id'],pattern=f'0x{s["pattern"]:08x}',block=f'0x{s["block"]:08x}',
                        geographic_x=s['geographic_origin'][0],geographic_y=s['geographic_origin'][1],
                        local_x=s['local_cell_origin'][0],local_y=s['local_cell_origin'][1],
                        origin_x=s['origin'][0],origin_y=s['origin'][1],nominal_x=s['dimensions'][0],nominal_y=s['dimensions'][1],
                        padding=s['padding'],source_flags=f'0x{s["source_flags"]:02x}',
                        in_before=s['id'] in before,in_after=s['id'] in after_ids,
                        classification='CANDIDATE' if phase=='candidates' else 'DERIVED',
                        reason=('Compatible-pattern envelope; actual selected membership unestablished' if phase=='candidates'
                          else 'Frozen ordinary initialization pattern and owner-cell halo' if phase=='before'
                          else 'Retained coarse-pattern witness and unchanged owner-cell halo; not a source census' if site['site']=='Carinae'
                          else 'No independent pattern witness; retain conditional frozen inventory')))
        if 'replay' in site:
            replay={k:v for k,v in site['replay'].items() if k not in ('request','generated_regions')}
            site['replay']=replay
        site.pop('candidate_after')
        site['after']=after
        site['excluded_before_sources']=[dict(source=s['id'],reason='Different source identity under witnessed coarse pattern; historical frozen input retained')
            for s in site['before'] if s['id'] not in after_ids]
    write_json('results-v1.json',dict(result,inputs={k:v for k,v in result['inputs'].items() if not k.endswith('.py')}))
    controls_path=ROOT/'.local-work/resource-installed-settings/c2c-replay01.json'
    controls=json.loads(controls_path.read_text())
    # Retain the complete bounded numerical control summary; it has no raw memory.
    write_json('controls-v1.json',dict(schema='sor-c2c-controls/1',receipt_sha256=pin(controls_path),
        sites=[dict(site=s['site'],baseline_count=s['baseline_count'],installed_count=s['installed_count'],
                    accepted=s.get('accepted'),chance_comparison=s.get('chance_comparison'),
                    visited=s.get('visited'),actual_retained_query_positive_paths=s.get('actual_retained_query_positive_paths')) for s in controls['sites']]))
    paths=set(result['inputs'])|{str(path),str(controls_path),str(Path(__file__)),
        str(ROOT/'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_C2C_source_enumeration_carinae_reconciliation.md'),
        str(ROOT/'docs/experiments/resource-geometry-mature-context/operands-v2.json'),
        str(ROOT/'.local-work/resource-installed-settings/settings01.json'),
        str(ROOT/'.local-work/resource-carinae-source-context/phase-b-finalization02/audit-attempt02.json')}
    paths|={str(ROOT/f'.local-work/resource-geometry/native/{n:03d}.request.tsv') for n in (1,3,5,6,7,11,13,19,20,22)}
    paths|={str(ROOT/'.local-work/recon'/n) for n in ('exact-beacon-05.tsv','resource-milestone-b-producers-01.tsv','resource-availability-ui-15.tsv','resource-availability-ui-16.tsv')}
    with (OUT/'sources.csv').open('x',encoding='utf8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n');writer.writerow(['id','path','bytes','sha256','use'])
        for i,p in enumerate(sorted(paths),1):
            p=Path(p)
            writer.writerow([f'C2C-S{i:03d}',p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p),p.stat().st_size,pin(p),
                'Owned method or protected primary input; raw proprietary artifacts remain LOCAL-ONLY'])


if __name__=='__main__':
    main()
