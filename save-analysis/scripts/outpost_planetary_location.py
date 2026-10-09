"""SPDX-License-Identifier: GPL-3.0-or-later
Offline, source-informed project research; no I/O or external implementation.
Beacon -> saved overlay -> two independent body associations. No name inputs.
Empirical global-unit suffix and component fields are scoped to tested saves;
angular order/units and restoration authority are explicitly unresolved.
"""
import collections
import math
import struct
from validate_mature_outposts import directory
from outpost_record_framing import iter_records
from outpost_membership import initial_prefix, token_value


def global_suffix(b, d):
    """Unique length-closed units 4..16 ending exactly at R1 end.
    Not a decoder for the earlier variable units or complete component grammar.
    """
    a, z = d['regions']['region_R1']
    found = []
    q = a
    while (q := b.find(b'\4\0\0\0', q, min(a+8192,z))) >= 0:
        p, units = q, {}
        for tag in range(4,17):
            if p+8>z:break
            t,n=struct.unpack_from('<II',b,p)
            if t!=tag or n>z-p-8:break
            units[tag]=(p+8,p+8+n)
            p+=8+n
        if len(units)==13 and p==z:found.append(units)
        q+=1
    if len(found)!=1:raise ValueError('GLOBAL_SUFFIX_AMBIGUOUS_OR_UNSUPPORTED')
    return found[0]


def body_catalog(esm):
    by_pair=collections.defaultdict(list);by_id={}
    for r in esm:
        if r['type']!='PNDT':continue
        by_id[r['formid']]=r
        raw=bytes.fromhex(r['fields'].get('GNAM',''))
        if len(raw)==12:
            system,orbital,body=struct.unpack('<III',raw)
            by_pair[(system,body)].append(r)
    return by_pair,by_id


def associations(b, a, z, parent, by_pair, by_id):
    pattern=int(parent,16).to_bytes(4,'little')
    cache, points=[],[]
    q=a
    while (q:=b.find(pattern,q,z))>=0:
        if q+20<=z:
            system,body=struct.unpack_from('<II',b,q+8)
            options=by_pair.get((system,body),[])
            if options:
                cache.append(dict(offset=q,raw_words=list(struct.unpack_from('<5I',b,q)),
                    system_id=system,body_index=body,
                    body_options=[dict(formid=r['formid'],editor_id=r['edid']) for r in options],
                    source_world_token=f'{struct.unpack_from("<I",b,q+16)[0]:06x}'))
        if q>=a+4 and q+26<=z:
            token=struct.unpack_from('<I',b,q-4)[0]
            fid=token&0x3fffff
            if token>>22==1 and fid in by_id and b[q+22:q+26]==pattern:
                pair=struct.unpack_from('<2d',b,q+6)
                if all(math.isfinite(x) for x in pair):
                    points.append(dict(offset=q,body_formid=fid,body_editor_id=by_id[fid]['edid'],
                        raw_kind=b[q+4:q+6].hex(),pair=list(pair),repeated_parent_offset=q+22,
                        frame='BODY_ASSOCIATED_PAIR; ANGULAR_ORDER_UNITS_ORIGIN_UNVALIDATED'))
        q+=1
    return cache,points


def extract(b, esm):
    d=directory(b);units=global_suffix(b,d);by_pair,by_id=body_catalog(esm)
    table_start=d['regions']['reference_u32'][0]
    class Table:
        def __len__(self):return d['reference_count']
        def __getitem__(self,i):return struct.unpack_from('<I',b,table_start+4+4*i)[0]
    table=Table();a,z=d['regions']['region_R3'];rows=[];player=[]
    for r in iter_records(b,a,z,d['words'][9]):
        if r['token']=='400014':
            case=5 if not r['flags']&0x8000 else 6 if r['flags']&0x02000008 else 4 if r['flags']&6 else 7
            try:player.append(dict(record_offset=r['offset'],prefix=initial_prefix(b,r,case)))
            except ValueError as e:player.append(dict(error=str(e)))
        if len(r['refs'])<3 or r['flags']&0x8000 or int(r['token'],16)>>22!=2:continue
        if r['explicit_type'] is not None and not 0x4a<=r['explicit_type']<=0x55:continue
        try:base=token_value(r['refs'][1],table)
        except ValueError:continue
        if base!=0x2c60e9:continue
        p=initial_prefix(b,r,5);cache,points=associations(b,*units[6],p['parent_token'],by_pair,by_id)
        choices={v['formid'] for m in cache for v in m['body_options']}
        direct={m['body_formid'] for m in points}
        concordant=len(choices)==1 and (not direct or choices==direct)
        rows.append(dict(token=r['token'],record_start=r['offset'],record_end=r['end'],string_indices=r['strings'],
            parent_token=p['parent_token'],parent_queue_offset=r['reference_start'],
            saved_disabled=p['disabled'],local_xyz=p['xyz'],cache=cache,points=points,
            proposed_body_formid=next(iter(choices)) if concordant else None,
            confidence='STRONG_SCOPED_PROPOSED' if concordant and direct else 'PROVISIONAL',
            independent_direct_agreement=bool(concordant and direct)))
    return dict(global_units=units,beacons=rows,player=player,
        domain='DECODED_LOGICAL_STREAM; TAGGED_IDENTITIES_BEFORE_LOAD_REMAP',
        complete_enumeration=False)
