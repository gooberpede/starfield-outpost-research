# SPDX-License-Identifier: GPL-3.0-or-later
"""Recheck archived extractor controls and one installed definition chain.

Reads six authenticated historical JSON receipts and exact installed ESM bytes;
writes a fresh ignored result. No save decoding, native invocation, target,
analysis-project mutation, cleanup, network or Git changes. SOR-P-0002 adapts
E1 verify.py's header/decompression checks and reuses owned subrecords().
Historical derivative rechecks are not fresh save or runtime observations.
"""
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib
from d5ad_baseline import guard, sha
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import subrecords

def require(condition,message):
    if not condition:raise ValueError(message)

def record(stream,offset,kind,fid):
    stream.seek(offset); h=stream.read(24)
    n,flags,actual=struct.unpack_from('<III',h,4)
    require(h[:4]==kind and actual==fid,'Wrong exact definition record')
    raw=stream.read(n)
    require(len(raw)==n,'Partial definition copy')
    if flags&0x40000:
        size=struct.unpack_from('<I',raw)[0]
        d=zlib.decompressobj(); raw=d.decompress(raw[4:],size+1)
        require(len(raw)==size and d.eof and not d.unused_data and not d.unconsumed_tail,'Compressed closure')
    return list(subrecords(raw))

def one(fields,tag):
    v=[v for k,v in fields if k==tag]
    require(len(v)==1,'Nonunique field '+repr(tag));return v[0]

def main():
    if sys.flags.optimize or not __debug__:raise RuntimeError('Use Python -E -B')
    guard()
    out=ROOT/'.local-work/d5ah-extractor'/sys.argv[1]
    require(not out.exists() and out.resolve().is_relative_to(ROOT/'.local-work/d5ah-extractor'),'Fresh output')
    lease=ROOT/'.local-work/resources-evidence-consolidation/d5ah-extractor-lease01'
    receipt=json.loads((ROOT/'.local-work/d5ah-extractor/restore01.json').read_bytes())['receipt']
    require(sha(lease/'LEASE.json')==receipt['lease_sha256'],'Lease changed')
    rows=json.loads((lease/'LEASE.json').read_bytes())['rows']
    pins={}
    for r in rows:
        p=lease/r['path'];require(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Archived receipt changed');pins[str(p)]=r['sha256']
    inputs=lease/'.local-work/extractor-resource/run05'
    load=lambda name:json.loads((inputs/name).read_bytes())
    controls={}
    for name,count in [('S3',1),('S3C',1),('S7',0),('S7C',0)]:
        d=load('manual-S0-S7C-'+name+'.json');require(d['coverage']['exact_r3_closure'],'Historical walk not closed')
        require(len(d['instances'])==count,'Action/control count disagrees')
        if count:require(d['instances'][0]['definition']['associations'][0]['resource_identity']=='starfield.esm:0057c7','Iron control mismatch')
        controls[name]=count
    d=load('mature-Save52.json');require(len(d['instances'])==63,'Mature count')
    resources=collections.Counter(a['resource_identity'] for r in d['instances'] for a in r['definition']['associations'])
    require(len(resources)==29,'Mature resource count')
    target=[r for r in d['instances'] if r['saved_reference']=='DYNAMIC:ff041387'];require(len(target)==1,'Target not unique');target=target[0]
    require(target['base_identity']=='starfield.esm:20a076','Target base mismatch')
    require(target['offset']==5034479 and target['end']==5034935,'Target decoded range mismatch')
    esm=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    esm_sha='1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    require(sha(esm)==esm_sha,'ESM identity')
    with esm.open('rb') as f:
        base=record(f,5673796,b'CONT',0x20a076)
        resource=record(f,1301612783,b'IRES',0x0057d4)
        recipe=record(f,1300253505,b'COBJ',0x05ef52)
        category_default=record(f,1294790259,b'DFOB',410270)
    require(0x008406 in struct.unpack('<'+'I'*(len(one(base,b'KWDA'))//4),one(base,b'KWDA')),'Extractor category missing')
    prps=one(base,b'PRPS');require(len(prps)%12==0,'PRPS width')
    props=[struct.unpack_from('<IfI',prps,i) for i in range(0,len(prps),12)]
    require(one(category_default,b'EDID').rstrip(b'\0')==b'OutpostCategoryHarvesters_DO','Category default name')
    require(int.from_bytes(one(category_default,b'DATA'),'little')==0x008406,'Category default target')
    require(not {0x31986f,0x271128,0x0083ff}&{r[0] for r in props},'Target has placement bypass or atmospheric selector')
    require(props[3][0]==0x05ef20 and props[3][1]==1.0,'Resource property mismatch')
    require(int.from_bytes(one(resource,b'NAM1'),'little')==0x05ef20,'IRES AV mismatch')
    require(int.from_bytes(one(resource,b'NAM2'),'little')==0x05ef52,'IRES recipe mismatch')
    require(int.from_bytes(one(recipe,b'CNAM'),'little')==0x00557a,'Recipe product mismatch')
    require(sha(esm)==esm_sha,'ESM changed during reads')
    for p,digest in pins.items():require(sha(p)==digest,'Receipt changed during reads')
    result=dict(status='PASS',historical_receipt_controls=controls,mature_instances=63,mature_resource_identities=29,
        candidate_saved_reference=target['saved_reference'],candidate_base=target['base_identity'],decoded_range=[5034479,5034935],
        chain=dict(base='Starfield.esm:20a076',actor_value='Starfield.esm:05ef20',resource='Starfield.esm:0057d4',recipe='Starfield.esm:05ef52',item='Starfield.esm:00557a'),
        installed_record_offsets=[5673796,1301612783,1300253505,1294790259],category_default='OutpostCategoryHarvesters_DO -> KYWD 0x008406',ordinary_definition_no_bypass=True,inputs=pins,esm_sha256=esm_sha,method_sha256=sha(__file__),free_after=guard(),
        limits=['Historical JSON recheck, not fresh save decode','No runtime or native execution','Queued beacon adjacency does not establish Workshop ownership','No geometry observation or production measurement'])
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps({k:result[k] for k in ['status','historical_receipt_controls','mature_instances','mature_resource_identities','chain']}))
if __name__=='__main__':main()
