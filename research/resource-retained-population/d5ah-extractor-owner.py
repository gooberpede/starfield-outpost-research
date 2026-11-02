# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify one actual Save52 extractor's explicit saved WorkshopItem owner.

Reads policy-pinned protected research Save52 bytes only, plus owned parsers and
saved owner labels. Decodes into memory without writing a decoded save; writes
one fresh ignored receipt. No game, native call, save write, analysis-project,
cleanup, network or Git mutation. SOR-P-0002 reuses D5Z independent_slice,
stream_save.header, record framing and qualified Workshop membership parsers.
C:/D: caller-available free-space guards and source pre/post identity remain.
"""
import collections
import csv
import json
from pathlib import Path
import struct
import sys
from d5ad_baseline import guard,sha
from d5z_save import independent_slice
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from stream_save import header
from validate_mature_outposts import directory
from outpost_record_framing import iter_records
from outpost_membership import token_value
from extractor_resources import plugin_tables,saved_form
from workshop_inventory import reference_prefix,linked_prefix

def require(condition,message):
    if not condition:raise ValueError(message)

def main():
    if sys.flags.optimize or not __debug__:raise RuntimeError('Use Python -E -B')
    free=guard()
    out=ROOT/'.local-work/d5ah-extractor-owner'/sys.argv[1]
    require(not out.exists() and out.resolve().is_relative_to(ROOT/'.local-work/d5ah-extractor-owner'),'Fresh output')
    policy=ROOT/'research/resource-carinae-source-context/save_policy.json'
    named=json.loads(policy.read_bytes())['designated']
    name=next(n for n in named if n.startswith('Save52_'))
    source=ROOT/'.local-work/savegames'/name
    require(source.stat().st_size==named[name]['bytes'] and sha(source)==named[name]['sha256'],'Protected Save52 identity')
    with source.open('rb') as f:info=header(f,deadline=float('inf'))
    b=independent_slice(source,0,info['declared_decoded_size'])
    require(len(b)==info['declared_decoded_size'],'Complete logical output')
    decoded=__import__('hashlib').sha256(b).hexdigest()
    require(decoded=='e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93','Historical decoded input mismatch')
    d=directory(b);plugins=plugin_tables(b)
    require(plugins['builds']==['1.16.244.0']*2 and plugins['version']==153,'Qualified save version')
    a,_=d['regions']['reference_u32']
    class Table:
        def __len__(self):return d['reference_count']
        def __getitem__(self,i):
            if not 0<=i<len(self):raise IndexError(i)
            return struct.unpack_from('<I',b,a+4+4*i)[0]
    table=Table()
    resolve=lambda token:saved_form(token_value(token,table),plugins)
    chosen={};count=0;seen=collections.Counter()
    for r in iter_records(b,*d['regions']['region_R3'],d['words'][9]):
        count+=1
        if r['token'] not in ('841387','84e101'):continue
        seen[r['token']]+=1
        require(r['explicit_type'] is None or 0x4a<=r['explicit_type']<=0x55,'Reference representation')
        case=5 if not r['flags']&0x8000 else 6 if r['flags']&0x02000008 else 4 if r['flags']&6 else 7
        require(case==5,'Inline base case')
        p=reference_prefix(b,r,case);x=linked_prefix(b,r,p)
        for e in x['entries']:
            e['keyword_identity']=resolve(e['keyword_token']);e['target_identity']=resolve(e['target_token'])
        chosen[r['token']]=dict(saved_reference=resolve(r['token']),base=resolve(p['base_token']),record_offset=r['offset'],record_end=r['end'],ordinal=r['ordinal'],prefix=p,extras=x)
    require(count==205557 and seen=={'841387':1,'84e101':1},'Complete framing or selected identity uniqueness')
    target=chosen['841387'];owner=chosen['84e101']
    require(target['base']=='starfield.esm:20a076' and owner['base']=='starfield.esm:2c60e9','Exact target and owner bases')
    require(target['record_offset']==5034479 and target['record_end']==5034935 and owner['record_offset']==5712362,'Selected record boundaries')
    x=target['extras'];edges=[e for e in x['entries'] if e['keyword_identity']=='starfield.esm:054ba6']
    require(x['following_extras']=='CLOSED' and x['extra_count']==7 and not x['alternate_groups'],'Closed extras and no alternate owner representation')
    require(len(edges)==1 and edges[0]['target_mode']==0 and edges[0]['target_identity']==owner['saved_reference'],'Unique direct owner edge')
    require(edges[0]['flag_offset']==5034589,'Owner mode byte location')
    require(b[5034589]==0,'Independent direct mode-byte check')
    require(not target['prefix']['disabled'] and not target['prefix']['deleted'] and not owner['prefix']['disabled'] and not owner['prefix']['deleted'],'Saved state flags')
    labels=ROOT/'docs/experiments/workshop-membership/owners.csv'
    matches=[r for r in csv.DictReader(labels.open(encoding='utf8')) if r['owner_identity']==owner['saved_reference']]
    require(len(matches)==1,'Unique prior saved owner label')
    require(sha(source)==named[name]['sha256'],'Source changed during analysis')
    methods=[Path(__file__),ROOT/'research/resource-retained-population/d5z_save.py',ROOT/'research/resource-retained-population/d5ad_baseline.py']+[ROOT/'save-analysis/scripts'/n for n in ('stream_save.py','validate_mature_outposts.py','outpost_record_framing.py','outpost_membership.py','extractor_resources.py','workshop_inventory.py')]
    result=dict(status='PASS',source=str(source),source_sha256=named[name]['sha256'],source_bytes=source.stat().st_size,decoded_sha256=decoded,complete_framed_records=count,
        selected=chosen,explicit_owner_edge=edges[0],independent_mode_byte=0,saved_owner_label=matches[0],saved_owner_label_sha256=sha(labels),policy_sha256=sha(policy),methods={str(p.relative_to(ROOT)):sha(p) for p in methods},free_before=free,free_after=guard(),
        limits=['Authoritative explicit saved relationship; current loaded GetWorkshop remains unmeasured','No complete physical population claim','No geometry or production observation','Decoded Save52 existed in memory only'])
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf8',newline='\n') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',extractor=target['saved_reference'],owner=owner['saved_reference'],edge=edges[0],records=count)))
if __name__=='__main__':main()
