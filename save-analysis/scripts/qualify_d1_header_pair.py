"""SPDX-License-Identifier: GPL-3.0-or-later
D1 diagnostic for two primary saves rejected by the reader's build-pair allowlist.
Reads immutable run01 receipt and original Save38/39, existing catalogs; writes
new ignored header-qualification receipts. No byte substitution, save writes,
shared-reader relaxation, target/database/network/Git effects or dependencies.
Adapted from project-owned extractor_resources.plugin_tables; exact boundaries
and version 153 required, only header pair 1.16.244.0 / 1.16.242.0 admitted here.
This qualifies observed framing, not historical installed-definition equivalence.
"""
import json
from pathlib import Path
import struct
from inventory_historical_saves import identity, guard
from stream_save import decoded_save
from outpost_record_framing import Reader, iter_records
from outpost_membership import token_value
from extractor_resources import inventory, select_records, definition_catalog, saved_form
from workshop_inventory import reference_prefix, linked_prefix
from validate_mature_outposts import directory
from test_outpost_record_framing import independent

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'.local-work/disappearing-deposits/header-qualification01'


def write(name, value):
    with (OUT/name).open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')


def tables(b):
    if b[:12] != b'SFS_SAVEGAME': raise ValueError('SIGNATURE')
    c = Reader(b, 16+int.from_bytes(b[12:16], 'little'), len(b))
    version = c.take(1)[0]
    def string(cursor):
        return cursor.take(int.from_bytes(cursor.take(2), 'little')).decode('utf8')
    builds = [string(c), string(c)]
    if version != 153 or builds != ['1.16.244.0','1.16.242.0']:
        raise ValueError('D1_QUALIFICATION_SCOPE')
    size = int.from_bytes(c.take(4), 'little')
    p = Reader(b, c.p, c.p+size)
    groups = {}
    for label, width in [('full',1),('small',2),('medium',4)]:
        n = int.from_bytes(p.take(width), 'little')
        if n > (p.end-p.p)//3: raise ValueError('COUNT_BOUNDS')
        names=[]
        for _ in range(n):
            name=string(p).lower()
            if not name.endswith(('.esm','.esp','.esl')): raise ValueError('PLUGIN_NAME')
            flag=p.take(1)[0]
            if flag==1:
                for _ in range(3): string(p)
                p.take(1)
            elif flag!=0: raise ValueError('METADATA_FLAG')
            names.append(name)
        groups[label]=names
    trailer=p.take(p.end-p.p)
    allnames=sum(groups.values(),[])
    if trailer!=b'\1\0' or len(set(allnames))!=len(allnames) or groups['full'][0]!='starfield.esm':
        raise ValueError('TABLE_CLOSURE_OR_IDENTITY')
    return dict(groups=groups,start=c.p,end=p.end,version=version,builds=builds,
        trailer=trailer.hex(),qualification='D1_PAIR_FRAMING_ONLY')


def main():
    guard(); OUT.mkdir(parents=True,exist_ok=False)
    sp=ROOT/'.local-work/extractor-resource/run01/static-records.json'
    static=json.loads(sp.read_text())
    inputs=[sp]+[Path(s['path']) for s in static['sources']]
    for label in ('HIST-0250','HIST-0251'):
        inputs.append(ROOT/'.local-work/disappearing-deposits/run01'/(label+'.json'))
    before={str(p):identity(p) for p in inputs}
    for s in static['sources']:
        if before[str(Path(s['path']))]['sha256']!=s['sha256']: raise ValueError('DEFINITION_HASH')
    write('before.json',before)
    for label in ('HIST-0250','HIST-0251'):
        row=json.loads((ROOT/'.local-work/disappearing-deposits/run01'/(label+'.json')).read_text())
        p=Path(row['source']['path']); pin=identity(p)
        if pin!=row['source']: raise ValueError('SOURCE_IDENTITY')
        with decoded_save(p,OUT/'scratch') as (b,metrics):
            plugins=tables(b); d=directory(b)
            cat=definition_catalog(select_records(static['records'],plugins))
            result=inventory(b,cat,plugins)
            records=list(iter_records(b,*d['regions']['region_R3'],d['words'][9]))
            walk=independent(b,*d['regions']['region_R3'],d['words'][9])
            if [(r['offset'],r['end'],r['token'],r['flags']) for r in records]!=[r[:4] for r in walk]:
                raise ValueError('INDEPENDENT_WALK')
            start=d['regions']['reference_u32'][0]
            class Table:
                def __len__(self): return d['reference_count']
                def __getitem__(self,i): return struct.unpack_from('<I',b,start+4+4*i)[0]
            table=Table()
            def resolve(t): return saved_form(token_value(t,table),plugins)
            owners={resolve(s['token']) for s in row['sites']}
            bytoken={r['token']:r for r in records}
            for obj in result['instances']:
                r=bytoken[obj['token']]
                try:
                    prefix=reference_prefix(b,r,5)
                    links=linked_prefix(b,r,prefix)
                    edges=[dict(e,keyword_identity=resolve(e['keyword_token']),target_identity=resolve(e['target_token']))
                        for e in links['entries'] if resolve(e['keyword_token'])=='starfield.esm:054ba6']
                    targets={e['target_identity'] for e in edges}
                    obj['direct_owner_evidence']=edges
                    obj['direct_owner']=next(iter(targets)) if len(targets)==1 and next(iter(targets)) in owners and all(e['target_mode']==0 for e in edges) else None
                    obj['owner_reason']='D1_DECODED_DIRECT4C' if obj['direct_owner'] else 'UNRESOLVED'
                except ValueError as e:
                    obj.update(direct_owner=None,owner_error=str(e))
            row.update(extractors=result,plugins=plugins,independent_record_walk=True,
                diagnostic='Original strict-reader rejection preserved in run01; D1 scoped framing qualification',
                extractor_or_ownership_error=None)
        if identity(p)!=pin: raise ValueError('SAVE_CHANGED')
        write(label+'.json',row)
        print(label,len(result['instances']),'extractors',sum(bool(o['direct_owner']) for o in result['instances']),'direct owners',flush=True)
    after={str(p):identity(p) for p in inputs}
    write('preservation.json',dict(equal=before==after,after=after))
    if before!=after: raise ValueError('INPUT_CHANGED')
    guard()


if __name__=='__main__': main()
