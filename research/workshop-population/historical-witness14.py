"""Original scientific target/fingerprint join across complete scan11/12/13.
Reads receipts only, exclusive output. FFID matches are never promoted alone.
All older form types remain null; their prefix interpretations are conditional.
"""
import json,collections,sys
from pathlib import Path
sys.path.insert(0,'save-analysis/scripts')
from inventory_historical_saves import identity
base=Path('.local-work/workshop-population-rework');out=base/'specialist'
paths=[out/f'historical-targetcensus{n}.jsonl' for n in ('11','12','13')]+[base/'nonowner-da01.json',base/'typed-full03/mature-Save52.json',base/'nonowner-relations01.json',out/'historical-resource15.json',out/'historical-directory08.json',Path(__file__)]
pins=[identity(p) for p in paths];xs=[]
for p,status in zip(paths[:3],('QUALIFIED_TYPED_R3_CLOSED','FRAMING_ONLY_NULL_TYPE','FRAMING_ONLY_NULL_TYPE')):
 xs.extend(dict(x,receipt=str(p)) for x in map(json.loads,p.read_text().splitlines()) if x['status']==status)
assert len(xs)==261 and len({x['source']['path'] for x in xs})==261
da=json.loads(paths[3].read_text());typed=json.loads(paths[4].read_text());relations=json.loads(paths[5].read_text());resources=json.loads(paths[6].read_text());directory=json.loads(paths[7].read_text())
groups={r['identity'] for r in da['nonnull_groups'] if str(r['identity']).startswith('DYNAMIC:')};missing={r['identity'] for r in da['nonnull_groups'] if r['identity'] in groups and not r['r3_record']}
members={r['identity']:r for r in da['rows'] if groups&set((r.get('da') or {}).get('identities',[]))};canonical={r['target'] for r in relations['rows']};current={r['identity']:r for r in typed['references']};results=[]
for x in xs:
 rows={r['identity']:r for r in x['target_rows']};member_matches=[];member_candidates=[];canonical_matches=[];group_records=[]
 for ident,o in members.items():
  r=rows.get(ident)
  if not r:continue
  same_base=r.get('base_identity')==o['base'];same_parent=r.get('parent_identity')==o['parent'];same_da=any(p.get('identities')==o['da']['identities'] for p in r.get('packin_identities',[]));oldxyz=(current.get(ident,{}).get('prefix') or {}).get('xyz');xyz=(r.get('prefix') or {}).get('xyz')
  score=dict(identity=ident,base_match=same_base,parent_match=same_parent,DA_tuple_match=same_da,xyz_match=xyz==oldxyz if xyz is not None and oldxyz is not None else None,offset=r['offset'],semantic_gap=r.get('semantic_gap'),extra_gap=(r.get('extras') or {}).get('following_gap'),current_group=o['da']['identities'][3],historical_prefix=r.get('prefix'),historical_packin=r.get('packin_identities'),historical_links=r.get('links'))
  if same_base and same_parent and same_da:member_matches.append(score)
  elif same_base or same_parent or same_da:member_candidates.append(score)
 for ident in canonical:
  r=rows.get(ident);o=current.get(ident)
  if not r or not o:continue
  p=r.get('prefix') or {};op=o.get('prefix') or {};baseid=o.get('base_identity');parent=o.get('parent_identity')
  if r.get('base_identity')==baseid and r.get('parent_identity')==parent and p.get('xyz') is not None and p.get('xyz')==op.get('xyz'):
   canonical_matches.append(dict(identity=ident,offset=r['offset'],base=baseid,parent=parent,xyz=p['xyz'],links=r.get('links'),gap=r.get('semantic_gap') or (r.get('extras') or {}).get('following_gap')))
 for ident in groups&rows.keys():
  r=rows[ident];group_records.append(dict(identity=ident,offset=r['offset'],form_type=r['form_type'],base=r.get('base_identity'),parent=r.get('parent_identity'),prefix=r.get('prefix'),links=r.get('links'),semantic_gap=r.get('semantic_gap'),extra_gap=(r.get('extras') or {}).get('following_gap'),missing_in_Save52=ident in missing))
 results.append(dict(inventory_id=x['inventory_id'],source=x['source'],frozen_source=x.get('frozen_source'),frozen_identity_match=x.get('frozen_identity_match'),metadata=x['metadata'],buffer_version=x['buffer_version'],status=x['status'],record_count=x['record_count'],target_rows=len(rows),full_member_fingerprint_matches=member_matches,partial_member_fingerprint_candidates=member_candidates,canonical_base_parent_xyz_matches=canonical_matches,group_records=group_records))
after=[]
for r in directory:
 p=Path(r['path']);s=p.stat();after.append(dict(path=str(p.resolve()),size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,in_scan04=r['in_scan04']))
assert after==directory
assert [identity(p) for p in paths]==pins
summary=dict(unique_available_sources=len(xs),modern_typed=sum(x['status']=='QUALIFIED_TYPED_R3_CLOSED' for x in xs),older_framing_only=sum(x['status']=='FRAMING_ONLY_NULL_TYPE' for x in xs),member_fingerprint_sources=[dict(id=x['inventory_id'],matches=len(x['full_member_fingerprint_matches'])) for x in results if x['full_member_fingerprint_matches']],canonical_fingerprint_sources=[dict(id=x['inventory_id'],matches=len(x['canonical_base_parent_xyz_matches'])) for x in results if x['canonical_base_parent_xyz_matches']],target_groups=len(groups),missing_groups=len(missing),target_members=len(members),canonical_targets=len(canonical))
with (out/'historical-witness14.json').open('x',encoding='utf8') as f:json.dump(dict(schema='historical-fingerprint-witness/1',inputs=pins,summary=summary,results=results,resource_continuity=resources,limits='Only complete field conjunctions corroborate a cohort; equality of FFID or character name alone is insufficient. Older frames do not inherit current form types. Full fingerprint continuity and resource identity do not supply an absent physical object or missing authoritative owner.'),f,indent=2);f.write('\n')
print(summary)
