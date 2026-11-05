# SPDX-License-Identifier: GPL-3.0-or-later
"""Check A0 file overrides of Feynman's complete PNDT resource dependencies.

Owned bounded ESM reader, read-only pinned files; exclusive ignored receipt.
Includes every IRES conservatively, PNDT PPBD biomes and their/override RSGDs.
Does not infer effective runtime component initialization from a file result.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import json, struct
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records


def main():
    out = Path(sys.argv[1]).resolve(); before = guard()
    if not out.is_relative_to(ROOT / '.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('Fresh ignored output required')
    audit_path = ROOT / '.local-work/d5ar/a0-file-inputs05.json'
    audit = json.loads(audit_path.read_bytes())
    files = {n:h for n,h in audit['inputs'].items() if Path(n).suffix.lower() in ('.esm','.esp','.esl')}
    if len(files) != 39:
        raise ValueError('Incomplete original file inventory')
    main_path = next(Path(n) for n in files if Path(n).name.lower()=='starfield.esm')
    if any(sha(Path(n))!=pin for n,pin in files.items()):
        raise ValueError('A0 file pins changed')
    records = {h['formid']:(h,fs) for h,fs in esm_records(main_path, {b'PNDT',b'BIOM',b'RSGD',b'IRES'}, repeated=True)}
    body = 0x5e0de
    biomes=set(); rsgds=set()
    for tag, raw in records[body][1]:
        if tag==b'PPBD':
            biome, chance, opaque, override = struct.unpack_from('<IfII',raw)
            biomes.add(biome)
            if override:rsgds.add(override)
    for biome in biomes:
        rsgds.update(int.from_bytes(raw,'little') for tag,raw in records[biome][1] if tag==b'RNAM')
    ires={fid for fid,(h,fs) in records.items() if h['type']=='IRES'}
    targets={body}|biomes|rsgds|ires
    overrides=[]; walked=[]
    for name,pin in files.items():
        path=Path(name); masters=[]; count=0
        for h,fs in esm_records(path,{b'TES4',b'PNDT',b'BIOM',b'RSGD',b'IRES'}, repeated=True):
            count+=1
            if h['type']=='TES4':
                masters=[raw.rstrip(b'\0').decode('utf8') for tag,raw in fs if tag==b'MAST'];continue
            index=h['formid']>>24
            master=masters[index] if index<len(masters) else path.name if index==len(masters) else 'UNRESOLVED'
            if path!=main_path and master.lower()=='starfield.esm' and h['formid']&0xffffff in targets:
                overrides.append(dict(file=name,header=h))
        if sha(path)!=pin:raise ValueError('File changed during scan')
        walked.append(dict(path=name,sha256=pin,examined_records=count))
    if overrides:raise ValueError('Effective dependency overrides require reconciliation: '+repr(overrides))
    result=dict(status='PASS_NO_A0_FILE_OVERRIDE_IN_FEYNMAN_RESOURCE_DEPENDENCY_SET',
                body=hex(body),biomes=[hex(x) for x in sorted(biomes)],rsgds=[hex(x) for x in sorted(rsgds)],
                conservative_all_ires=len(ires),target_records=len(targets),overrides=overrides,files=walked,
                scope='All PPBD biomes, PNDT override and BIOM RSGDs; every main IRES conservatively includes child and shared-occupancy candidates.',
                limits=['Does not prove runtime component seed/initialization/order or absence of native/script mutation', 'Does not turn an on-disk roster into a complete runtime module inventory'],
                audit_sha256=sha(audit_path),reader_sha256=sha(ROOT/'save-analysis/scripts/inspect_outpost_definitions.py'),method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','target_records','conservative_all_ires')}))


if __name__=='__main__':main()
