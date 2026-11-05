# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge whether possible atmospheric membership changes component inputs.

Owned SOR-P-0002 builder adaptation only; literal FormID candidate inventory
across every byte alignment is diagnostic, not a complete native wire proof.
Reads pinned operands/methods; writes fresh ignored method and receipt. No game,
external exporter heuristic/code, production data importer or save mutation.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import dataclasses, inspect, itertools, json
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha
sys.path[:0]=[str(ROOT/'research'/name) for name in ('resource-standalone','resource-owner-root','resource-slot-provenance')]
import builder
from components import components
from owner_map import reconstruct
from candidate_order import candidates


def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):
        raise ValueError('Fresh ignored output required')
    audit=ROOT/'.local-work/d5ar/atmosphere-definition01.json';raw=json.loads(audit.read_bytes())
    if raw['status']!='PASS_SERIALIZED_ATMO_INPUT_AUDIT_NOT_EFFECTIVE_LIST':raise ValueError('ATMO operands not qualified')
    if sha(builder.ESM)!=builder.DEFINITION or any(sha(builder.OWNED/name)!=pin for name,pin in builder.OWNED_PINS.items()):raise ValueError('Owned method/input pins changed')
    records={h['formid']:(h,fs) for h,fs in builder.esm_records(builder.ESM,{b'PNDT',b'BIOM',b'RSGD',b'IRES'},repeated=True)}
    ires={fid for fid,(h,fs) in records.items() if h['type']=='IRES'};hits=[]
    for row in raw['records']:
        for field in row['fields']:
            if field['tag'] not in ('REFL','RDIF'):continue
            data=bytes.fromhex(field['raw_hex'])
            for offset in range(len(data)-3):
                fid=int.from_bytes(data[offset:offset+4],'little')
                if fid in ires:hits.append(dict(atmo=hex(row['header']['formid']),field=field['tag'],offset=offset,ires=hex(fid)))
    possible=sorted({int(row['ires'],16) for row in hits})
    if len(possible)>4:raise ValueError('Finite sensitivity domain requires further design')
    adapted=inspect.getsource(builder.selections)
    old='def selections(records, body):';call='atmospheric_records=[]'
    if adapted.count(old)!=1 or adapted.count(call)!=1:raise ValueError('Owned builder adaptation anchors changed')
    adapted=adapted.replace(old,'def selections(records, body, atmospheric):').replace(call,'atmospheric_records=atmospheric')
    method=out.with_suffix('.method.py')
    if method.exists():raise ValueError('Fresh owned derivative required')
    method.write_text('# SPDX-License-Identifier: GPL-3.0-or-later\n# SOR-P-0002: exact owned builder selections, atmospheric input parameter only.\n'+adapted,encoding='utf8',newline='\n')
    namespace=dict(builder.__dict__);exec(compile(adapted,str(method),'exec'),namespace)
    sys.path.insert(0,str(builder.OWNED.parent))
    from starfield_resource_reproducer.domain import AtmosphericResourceRecord, FormId
    rows=[];baseline=None
    rarities={fid:builder.last(fs,b'SNAM')[0] for fid,(h,fs) in records.items() if h['type']=='IRES'}
    for count in range(len(possible)+1):
        for subset in itertools.combinations(possible,count):
            for order in itertools.permutations(subset):
                atmospheric=[]
                for ordinal,fid in enumerate(order):
                    fields={f.name:'OWNED_ADVERSE_INPUT_NOT_OBSERVED' for f in dataclasses.fields(AtmosphericResourceRecord)}
                    fields.update(source_file='Starfield.esm',planet_form_id=FormId('0005e0de'),star_system_id=0,parent_planet_id=0,planet_id=0,
                                  atmosphere_form_id=FormId('0000c19b'),atmospheric_resource_count=len(order),atmospheric_resource_index=ordinal,
                                  resource_form_id=FormId(f'{fid:08x}'),resource_source_file='Starfield.esm',defined_by_atmosphere_form_id=FormId('0020cdd4'),atmosphere_inheritance_depth=2)
                    atmospheric.append(AtmosphericResourceRecord(**fields))
                prediction=namespace['selections'](records,0x5e0de,atmospheric)
                projected=components(records,prediction);mapping=reconstruct(projected)
                selected=next(v for v in projected if v['biome']==0x145440)
                ordered=candidates(selected['root'],mapping['maps'],rarities)
                effective=dict(components=projected,mapping=mapping['maps'],selected=selected,ordered=ordered)
                if baseline is None:baseline=effective
                rows.append(dict(atmospheric_order=[hex(fid) for fid in order],effective=effective,all_component_inputs_equal_to_empty=effective==baseline))
    result=dict(status='PASS_BOUNDED_ATMOSPHERIC_SENSITIVITY',literal_ires_candidates=[hex(fid) for fid in possible],literal_hits=hits,cases=rows,
                all_cases_equal=all(row['all_component_inputs_equal_to_empty'] for row in rows),
                scope='Exhaustive subsets/orders of literal IRES candidates appearing at any byte alignment in these exact serialized ATMO operands.',
                native_wire_candidate_domain_proven=False,
                limits=['Candidate inventory is not yet a native serialization/reference/default/parent-closure theorem','Equal component outputs cannot qualify actual atmospheric state','No geometry equality used and no external xEdit heuristic transferred'],
                inputs={str(audit.relative_to(ROOT)):sha(audit),str(Path(builder.__file__).relative_to(ROOT)):sha(builder.__file__),str(method.relative_to(ROOT)):sha(method)},method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],candidates=result['literal_ires_candidates'],cases=len(rows),all_cases_equal=result['all_cases_equal'])))


if __name__=='__main__':main()
