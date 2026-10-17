# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded E3 definitions; adapts owned E2 derive.py/assemblies.py readers.
Reads E2 inventory02 and pinned installed ESM; independently checks every selected
record at its physical offset and walks all group headers for target PKIN cells.
Writes exclusive ignored JSON and, with --tables, authored CSV summaries. Stdlib
and project reader only; no game, save, analysis-project or Git mutations.
Prerequisite: repository cwd, CPython, existing E2 inventory; no downloads.
"""
import argparse
import csv
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard
import hashlib


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
    guard()
    out = ROOT / '.local-work/e3-fabricators' / (args.run + '.json')
    assert not out.exists()
    cache = ROOT / '.local-work/e2-organic/inventory02.json'
    j = json.loads(cache.read_text())
    rs = j['records']; by = {r['formid']: r for r in rs}
    selected = {}

    def field(r, k):
        a = [bytes.fromhex(v) for t, v in r['fields'] if t == k]
        assert len(a) <= 1
        return a[0] if a else b''

    def number(r, k): return int.from_bytes(field(r, k), 'little')

    def ident(r):
        selected[r['formid']] = r
        return dict(formid=f"{r['formid']:08x}", edid=r['edid'], offset=r['offset'], type=r['type'])

    def props(r): return {i: v for i, v, tail in struct.iter_unpack('<IfI', field(r, 'PRPS'))}

    def kws(r): return [i[0] for i in struct.iter_unpack('<I', field(r, 'KWDA'))]

    def inputs(r):
        return [dict(**ident(by[i]), quantity=q, tail=t) for i, q, t in struct.iter_unpack('<III', field(r, 'FVPA'))]

    bases = [r for r in rs if r['type'] == 'CONT' and {0x2731a0, 0x23ceb6}.issubset(kws(r))]
    ires_avs = {number(r,'NAM1') for r in rs if r['type']=='IRES'}
    avs = {i for r in bases for i in props(r) if i in ires_avs}
    resources = []
    unresolved_resources = []
    for r in rs:
        if r['type'] != 'IRES' or number(r, 'NAM1') not in avs: continue
        if number(r, 'NAM2') == 0:
            unresolved_resources.append(dict(**ident(r),av=ident(by[number(r,'NAM1')]),reason='NULL_NAM2'))
            continue
        av, recipe, glob = [by[number(r, k)] for k in ['NAM1', 'NAM2', 'NAM3']]
        product = by[number(recipe, 'CNAM')]
        assert (av['type'], recipe['type'], glob['type'], product['type']) == ('AVIF','COBJ','GLOB','MISC')
        hours = struct.unpack('<f', field(glob, 'FLTV'))[0]
        resources.append(dict(**ident(r), av=ident(av), recipe=ident(recipe), product=ident(product),
                              av_nam1=number(av,'NAM1'),av_flags=number(av,'AVFL'),
                              interval_global=ident(glob), hours=hours,
                              seconds=struct.unpack('<f', struct.pack('<f', hours * 3600))[0],
                              recipe_count=number(recipe,'NNAM'), inputs=inputs(recipe),
                              conditions=[v for k,v in recipe['fields'] if k=='CTDA']))
    family_lists = {1: 0x29c458, 2: 0x29c459, 3: 0x249ba5}
    packins = {}
    for tier, fid in family_lists.items():
        fl = by[fid]; ident(fl)
        for k,v in fl['fields']:
            if k == 'LNAM':
                pk = by[int.from_bytes(bytes.fromhex(v), 'little')]
                assert pk['type'] == 'PKIN'
                packins[pk['formid']] = dict(**ident(pk), tier=tier, cell=number(pk,'CNAM'))
    cells = {p['cell']: p for p in packins.values()}
    source = Path(j['source']['path']); assert pin(source) == j['source']
    children = []
    with source.open('rb') as f:
        end = source.stat().st_size; stack = [(end,None)]; pos = 0
        while pos < end:
            while pos == stack[-1][0] and len(stack)>1: stack.pop()
            f.seek(pos); h=f.read(24); assert len(h)==24
            tag=h[:4]; n,flags,fid=struct.unpack_from('<III',h,4)
            stop=pos+(n if tag==b'GRUP' else n+24)
            assert pos+24<=stop<=stack[-1][0]
            cell=stack[-1][1]
            if tag==b'GRUP':
                if struct.unpack_from('<I',h,12)[0]==6: cell=flags
                stack.append((stop,cell));pos+=24;continue
            if tag==b'REFR' and cell in cells:
                data=f.read(n)
                if flags&0x40000:
                    size=struct.unpack_from('<I',data)[0]; data=zlib.decompress(data[4:]);assert len(data)==size
                names=[int.from_bytes(v,'little') for k,v in subrecords(data) if k==b'NAME']
                assert len(names)==1
                if names[0] in {r['formid'] for r in bases}:
                    children.append(dict(packin=cells[cell], reference=f'{fid:08x}', offset=pos, base=names[0]))
            pos=stop
        assert pos==end
    assert len(children)==len(packins)
    ordinary={c['base']: c for c in children}
    facilities=[]
    for r in bases:
        ps=props(r); assoc=ordinary.get(r['formid'])
        facilities.append(dict(**ident(r), ordinary=bool(assoc), assembly=assoc,
                               keywords=[ident(by[i]) for i in kws(r)],
                               properties={f'{i:08x}':v for i,v in ps.items()},
                               resource_avs=[f'{i:08x}' for i in ps if i in avs],
                               preset=[f'{i:08x}' for i,v in ps.items() if i in avs and v>0]))
    ordinary_avs = set()
    for tier, expected in [(1,11),(2,10),(3,9)]:
        family=[f for f in facilities if f['ordinary'] and f['assembly']['packin']['tier']==tier]
        assert len(family)==expected
        union={a for f in family for a in f['resource_avs']}
        assert len(union)==expected and all(set(f['resource_avs'])==union and len(f['preset'])==1 for f in family)
        ordinary_avs.update(union)
    ordinary_resources=[r for r in resources if r['av']['formid'] in ordinary_avs]
    assert len(ordinary_resources)==30 and len({r['product']['formid'] for r in ordinary_resources})==30
    assert all(r['av_nam1']==9 and not r['av_flags']&2 for r in ordinary_resources)
    assert all(r['recipe_count']==1 and r['inputs'] and all(x['tail']==0 and x['quantity']>0 for x in r['inputs']) for r in ordinary_resources)
    construction=[]
    for r in rs:
        if r['type']=='COBJ' and number(r,'CNAM') in family_lists.values():
            construction.append(dict(**ident(r), created=ident(by[number(r,'CNAM')]), inputs=inputs(r),
                                     conditions=[v for k,v in r['fields'] if k=='CTDA']))
    with source.open('rb') as f:
        for r in selected.values():
            f.seek(r['offset']);h=f.read(24);n,flags,fid=struct.unpack_from('<III',h,4)
            assert h[:4].decode()==r['type'] and fid==r['formid'] and flags==r['flags']
            data=f.read(n)
            if flags&0x40000:
                size=struct.unpack_from('<I',data)[0];d=zlib.decompressobj();data=d.decompress(data[4:],size+1)
                assert len(data)==size and d.eof and not d.unused_data and not d.unconsumed_tail
            assert [[k.decode(),v.hex()] for k,v in subrecords(data)]==r['fields']
    assert pin(source)==j['source']
    result=dict(source=j['source'],cache=pin(cache),tool=pin(Path(__file__)),facilities=facilities,
                resources=resources,unresolved_resources=unresolved_resources,construction=construction,physical_records_checked=len(selected),
                limits=['Main ESM only; no override merger','Definitions and ordinary construction reachability, not loaded menu membership'])
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf8',newline='\n') as f: json.dump(result,f,indent=2);f.write('\n')
    if args.tables:
        dest=ROOT/'docs/experiments/fabricators'
        tables={
            'facilities.csv': [dict(formid=r['formid'],edid=r['edid'],esm_offset=r['offset'],ordinary=r['ordinary'],
                tier=r['assembly']['packin']['tier'] if r['ordinary'] else '',
                packin=r['assembly']['packin']['formid'] if r['ordinary'] else '',
                cell=f"{r['assembly']['packin']['cell']:08x}" if r['ordinary'] else '',
                producer_refr=r['assembly']['reference'] if r['ordinary'] else '',
                resource_avs=';'.join(r['resource_avs']),preset=';'.join(r['preset'])) for r in facilities],
            'recipes.csv': [dict(ires=r['formid'],ires_edid=r['edid'],ires_offset=r['offset'],av=r['av']['formid'],
                ordinary_tiers=';'.join(str(t) for t in (1,2,3) if any(f['ordinary'] and f['assembly']['packin']['tier']==t
                    and r['av']['formid'] in f['resource_avs'] for f in facilities)),
                recipe=r['recipe']['formid'],recipe_offset=r['recipe']['offset'],product=r['product']['formid'],
                product_edid=r['product']['edid'],count=r['recipe_count'],interval_global=r['interval_global']['formid'],
                seconds=r['seconds'],conditions=';'.join(r['conditions']),
                inputs=';'.join(f"{x['formid']}:{x['edid']}*{x['quantity']}" for x in r['inputs'])) for r in resources]}
        for name,rows in tables.items():
            with (dest/name).open('w',encoding='utf8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    guard()
    print(json.dumps(dict(bases=len(facilities),ordinary=len(ordinary),recipes=len(resources),physical=len(selected))))


if __name__=='__main__': main()
