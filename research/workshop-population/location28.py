"""Original target-family joins; reads closed receipts, exclusive local output."""
import json,collections,hashlib
from pathlib import Path
p=Path('.local-work/workshop-population-rework');o=p/'specialist';read=lambda path:json.loads(path.read_text())
c=read(o/'location-census24.json');da=read(p/'nonowner-da01.json');rel=read(p/'nonowner-relations01.json');lead=read(p/'nonref-targets01.json')
groups={r['identity'] for r in da['nonnull_groups'] if r['identity'].startswith('DYNAMIC:')};members={r['identity'] for r in da['rows'] if r['da']['identities'][3] in groups};canonical={r['target'] for r in rel['rows']};beacons={x['reference'] for r in read(o/'location-target25.json')['rows'] for x in r['beacon_pairs']}
assert list(map(len,[groups,members,canonical,beacons]))==[31,115,16,19]
targets=dict(groups=groups,members=members,canonical=canonical,beacons=beacons);matches={k:[] for k in targets}
for r in c['rows']:
 for field,values in r['fields'].items():
  for j,v in enumerate(values if isinstance(values,list) else [values]):
   ident=v.get('reference') if isinstance(v,dict) else v
   for k,ids in targets.items():
    if isinstance(ident,str) and ident in ids:matches[k].append(dict(location=r['identity'],offset=r['offset'],field=field,index=j,identity=ident,type=v.get('type') if isinstance(v,dict) else None))
result=dict(schema='all-location-target-family-join/1',source=c['source'],counts={k:len(v) for k,v in targets.items()},match_counts={k:len(v) for k,v in matches.items()},matched_identities={k:sorted({r['identity'] for r in v}) for k,v in matches.items()},matches=matches,interpretation='Recorded location context, not per-object player construction or WorkshopItem owner proof. Exact clone ancestry separately supports both Hab historical beacon contexts.')
with (o/'location-joins28.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
print(result['match_counts'],{k:len(v) for k,v in result['matched_identities'].items()})
