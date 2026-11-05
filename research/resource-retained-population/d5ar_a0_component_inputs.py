# SPDX-License-Identifier: GPL-3.0-or-later
"""Reconstruct conditional Feynman component inputs from pinned definitions.

Uses maintainer-owned SOR-P-0002 selection/owner-map methods. Reads main ESM and
the complete A0 dependency audit; writes one ignored receipt. No runtime answer
or geometry is used as an inverse oracle. Empty-atmosphere and normal initialized
component route remain explicit prerequisites rather than historical findings.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import hashlib, json, struct
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha
sys.path[:0] = [str(ROOT/'research'/name) for name in ('resource-standalone','resource-owner-root','resource-slot-provenance','resource-feynman-d5')]
import builder
from components import components
from qualification import qualify
from owner_map import reconstruct
from candidate_order import candidates
from selection import descriptor, special, qualify_everywhere


def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):
        raise ValueError('Fresh ignored output required')
    audit=ROOT/'.local-work/d5ar/a0-definition-closure02.json';closure=json.loads(audit.read_bytes())
    if closure['status']!='PASS_NO_A0_FILE_OVERRIDE_IN_FEYNMAN_RESOURCE_DEPENDENCY_SET' or closure['overrides']:
        raise ValueError('File dependency closure failed')
    if sha(builder.ESM)!=builder.DEFINITION or any(sha(builder.OWNED/name)!=pin for name,pin in builder.OWNED_PINS.items()):
        raise ValueError('Owned model or main definition pin changed')
    records={h['formid']:(h,fs) for h,fs in builder.esm_records(builder.ESM,{b'PNDT',b'BIOM',b'RSGD',b'IRES'},repeated=True)}
    body=0x5e0de;biome=0x145440
    prediction=builder.selections(records,body)
    qualification=qualify(records,prediction)
    rows=components(records,prediction);mapping=reconstruct(rows)
    selected=next(row for row in rows if row['biome']==biome)
    rarity={fid:builder.last(fs,b'SNAM')[0] for fid,(h,fs) in records.items() if h['type']=='IRES'}
    ordered=candidates(selected['root'],mapping['maps'],rarity)
    raw,detail=descriptor(records,rows,biome);qualify_everywhere(records,selected['rsgd'])
    blocks=[dict(resource=hex(fid),rarity=rarity[fid],raw32=raw[40*(rarity[fid]+7):40*(rarity[fid]+7)+32].hex()) for fid in ordered['ordered']]
    seed=int.from_bytes(builder.last(records[body][1],b'RSCS'),'little')
    inputs=[Path(builder.__file__),ROOT/'research/resource-slot-provenance/components.py',ROOT/'research/resource-slot-provenance/qualification.py',ROOT/'research/resource-slot-provenance/candidate_order.py',ROOT/'research/resource-owner-root/owner_map.py',ROOT/'research/resource-feynman-d5/selection.py',*list(builder.OWNED.glob('*.py'))]
    result=dict(status='PASS_CONDITIONAL_MAIN_FILE_COMPONENT_RECONSTRUCTION',body=hex(body),biome=hex(biome),pndt_raw_seed=seed,
                pndt_seed_nonzero_excludes_native_zero_seed_fallback=seed!=0,components=rows,qualification=qualification,
                selected=selected,owner_map=mapping,ordered=ordered,descriptor=detail,blocks=blocks,
                selected_special=special(records,selected),
                premises=['Normal native initialized-component creation/copy route and stable input definitions', 'Empty initial atmospheric occupancy as explicitly supplied by the inherited model; not certified by this receipt', 'Successful allocations and native component ordering; no intervening dynamic mutation'],
                not_certified=['Actual A0 loaded component values/initialization event merely from model agreement', 'Complete non-mask input equivalence or per-cell descriptor/setting intervals'],
                main_definition_sha256=sha(builder.ESM),dependency_audit_sha256=sha(audit),methods={str(p):sha(p) for p in inputs},method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','pndt_raw_seed','selected','ordered')}))


if __name__=='__main__':main()
