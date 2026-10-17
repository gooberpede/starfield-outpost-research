# SPDX-License-Identifier: GPL-3.0-or-later
"""P1 offline definition catalogue, adapted from owned E2/E3 strict readers.
Reads pinned main ESM, existing E2 cache and supplied maintainer source files.
Writes exclusive ignored JSON and authored CSV tables with --tables. Stdlib only;
CPython and repository cwd required. No target, save, database, network or Git
mutation; no xEdit/script execution. Raw fields stay local. Not an override merge.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records, subrecords
from inventory_historical_saves import guard


def pin(p):
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--tables', action='store_true')
    args = ap.parse_args()
    assert args.run.isalnum()
    out = ROOT / '.local-work/p1-power' / (args.run + '.json')
    assert not out.exists()
    guard()
    cache = ROOT / '.local-work/e2-organic/inventory02.json'
    old = json.loads(cache.read_text())
    source = Path(old['source']['path'])
    before = pin(source)
    assert before == old['source']
    records = old['records']
    for h, fs in esm_records(source, {x.encode() for x in ['ACTI','FURN','STAT','MSTT','LIGH','DOOR']}, repeated=True):
        records.append(dict(**h, edid=next((v.rstrip(b'\0').decode() for k,v in fs if k == b'EDID'), ''),
                            fields=[(k.decode(),v.hex()) for k,v in fs]))
    by = {r['formid']:r for r in records}
    selected = {}

    def field(r,k):
        vs = [bytes.fromhex(v) for t,v in r['fields'] if t == k]
        assert len(vs) <= 1
        return vs[0] if vs else b''

    def num(r,k): return int.from_bytes(field(r,k),'little')
    def props(r): return {i:v for i,v,t in struct.iter_unpack('<IfI',field(r,'PRPS'))}
    def kws(r): return [i[0] for i in struct.iter_unpack('<I',field(r,'KWDA'))]
    def ident(r):
        selected[r['formid']] = r
        return dict(formid=f"{r['formid']:08x}", edid=r['edid'], type=r['type'], offset=r['offset'])
    def named(i): return f"{i:08x}:{by[i]['edid']}" if i in by else f'{i:08x}'

    lists = [r for r in records if r['type']=='FLST' and r['edid'].startswith('OutpostPower_')]
    env = []
    for r in lists:
        ident(r)
        choices = [int.from_bytes(bytes.fromhex(v),'little') for k,v in r['fields'] if k=='LNAM']
        idx = None
        for k,v in r['fields']:
            b=bytes.fromhex(v)
            if k=='INAM': idx=int.from_bytes(b,'little')
            if k=='CTDA':
                assert idx is not None and idx<len(choices) and len(b)==32
                kw=int.from_bytes(b[12:16],'little')
                target=by[choices[idx]]; ident(target)
                env.append(dict(list_formid=f"{r['formid']:08x}",list_edid=r['edid'],esm_offset=r['offset'],
                    index=idx,target=f"{target['formid']:08x}",target_edid=target['edid'],
                    rating=props(target).get(0x32e,''),keyword=named(kw),wire_function=f'{int.from_bytes(b[8:10],"little"):04x}',
                    condition_flags=b[0],comparison=struct.unpack_from('<f',b,4)[0]))
    candidates=[]
    types={'ACTI','CONT','FURN','STAT','MSTT','LIGH','DOOR'}
    for r in records:
        if r['type'] not in types: continue
        p=props(r); kw=kws(r)
        reasons=[]
        if 0x32e in p: reasons.append('generation-property')
        if 0x330 in p: reasons.append('demand-property')
        if 0x5fbbb in p: reasons.append('can-be-powered-property')
        if 0x1690a4 in kw: reasons.append('switch-activator-keyword')
        if 'outpost' in r['edid'].lower() and any(x in r['edid'].lower() for x in ['power','light','lamp','switch','solar','wind','reactor']):
            reasons.append('name-candidate-only')
        if not reasons: continue
        candidates.append(dict(**ident(r),reasons=reasons,properties={f'{i:08x}':v for i,v in p.items()},
            keywords=[named(i) for i in kw]))
    bases={int(r['formid'],16) for r in candidates}
    pk_cells={num(r,'CNAM'):r for r in records if r['type']=='PKIN'}
    assemblies=[]
    # Full group walk retains CELL ownership; this does not interpret saved identity.
    import zlib
    with source.open('rb') as f:
        end=source.stat().st_size;stack=[(end,None)];pos=0
        while pos<end:
            while pos==stack[-1][0] and len(stack)>1:stack.pop()
            f.seek(pos);h=f.read(24);assert len(h)==24
            tag=h[:4];n,flags,fid=struct.unpack_from('<III',h,4)
            stop=pos+(n if tag==b'GRUP' else n+24)
            assert pos+24<=stop<=stack[-1][0]
            cell=stack[-1][1]
            if tag==b'GRUP':
                if struct.unpack_from('<I',h,12)[0]==6:cell=flags
                stack.append((stop,cell));pos+=24;continue
            if tag==b'REFR' and cell in pk_cells:
                b=f.read(n)
                if flags&0x40000:
                    size=struct.unpack_from('<I',b)[0];b=zlib.decompress(b[4:]);assert len(b)==size
                names=[int.from_bytes(v,'little') for k,v in subrecords(b) if k==b'NAME']
                if len(names)==1 and names[0] in bases:
                    pk=pk_cells[cell];ident(pk)
                    assemblies.append(dict(packin=f"{pk['formid']:08x}",cell=f'{cell:08x}',reference=f'{fid:08x}',offset=pos,base=f'{names[0]:08x}'))
            pos=stop
        assert pos==end
    targets=bases|{r['formid'] for r in lists}|{int(a['packin'],16) for a in assemblies}
    construction=[]
    for r in records:
        if r['type']=='COBJ' and num(r,'CNAM') in targets:
            construction.append(dict(**ident(r),target=named(num(r,'CNAM')),
                inputs=[dict(resource=named(i),quantity=q,tail=t) for i,q,t in struct.iter_unpack('<III',field(r,'FVPA'))],
                conditions=[v for k,v in r['fields'] if k=='CTDA']))
    fuel=[]
    for r in records:
        if r['type']=='IRES' and num(r,'NAM1')==0x2b063b:
            av,co,glob=[by[num(r,k)] for k in ['NAM1','NAM2','NAM3']]
            hours=struct.unpack('<f',field(glob,'FLTV'))[0]
            fuel.append(dict(**ident(r),av=ident(av),recipe=ident(co),interval=ident(glob),hours=hours,
                seconds=struct.unpack('<f',struct.pack('<f',hours*3600))[0],output=num(co,'CNAM'),count=num(co,'NNAM'),
                inputs=[dict(resource=ident(by[i]),quantity=q,tail=t) for i,q,t in struct.iter_unpack('<III',field(co,'FVPA'))]))
    with source.open('rb') as f:
        for r in selected.values():
            f.seek(r['offset']);h=f.read(24);n,flags,fid=struct.unpack_from('<III',h,4)
            assert h[:4].decode()==r['type'] and fid==r['formid'] and flags==r['flags']
            b=f.read(n)
            if flags&0x40000:
                size=struct.unpack_from('<I',b)[0];d=zlib.decompressobj();b=d.decompress(b[4:],size+1)
                assert len(b)==size and d.eof and not d.unused_data and not d.unconsumed_tail
            assert [[k.decode(),v.hex()] for k,v in subrecords(b)]==[list(x) for x in r['fields']]
    paths=[Path('D:/tools/xEdit.4.1.5p/Edit Scripts/Starfield - Export Planet Directory.pas'),
           Path('D:/Projects/starfield-outpost-network/reference-source/planet-directory.csv'),
           Path('D:/Projects/starfield-outpost-network/src/domain/powerEfficiency.ts')]
    assert pin(source)==before
    result=dict(source=before,cache=pin(cache),tool=pin(Path(__file__)),dependencies=[pin(ROOT/'save-analysis/scripts'/n) for n in
        ['inspect_outpost_definitions.py','inventory_historical_saves.py']],python=sys.version,
        sources=[pin(p) for p in paths],candidates=candidates,environment=env,assemblies=assemblies,construction=construction,fuel=fuel,
        physical_records_checked=len(selected),coverage='Main ESM selected types; no override merge; candidate table is not relay eligibility proof')
    out.parent.mkdir(exist_ok=True,parents=True)
    with out.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    if args.tables:
        dest=ROOT/'docs/experiments/power';dest.mkdir(exist_ok=True,parents=True)
        rows=[dict(formid=r['formid'],edid=r['edid'],type=r['type'],esm_offset=r['offset'],reasons=';'.join(r['reasons']),
            generation=r['properties'].get('0000032e',''),demand=r['properties'].get('00000330',''),
            properties=';'.join(f'{k}={v}' for k,v in r['properties'].items()),keywords=';'.join(r['keywords'])) for r in candidates]
        build=[dict(formid=r['formid'],edid=r['edid'],esm_offset=r['offset'],target=r['target'],
            inputs=';'.join(f"{v['resource']}*{v['quantity']}" for v in r['inputs']),conditions=';'.join(r['conditions'])) for r in construction]
        for name,table in [('catalogue.csv',rows),('environment.csv',env),('construction.csv',build)]:
            with (dest/name).open('w',encoding='utf8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(table[0]),lineterminator='\n');w.writeheader();w.writerows(table)
    guard()
    print(json.dumps(dict(candidates=len(candidates),environment_conditions=len(env),assemblies=len(assemblies),construction=len(construction),physical=len(selected),fuel=fuel)))


if __name__=='__main__':main()
