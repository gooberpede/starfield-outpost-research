"""Original exact target joins of closed location24 receipt; local only."""
import json,collections
from pathlib import Path
p=Path('.local-work/workshop-population-rework');o=p/'specialist'
c=json.loads((o/'location-census24.json').read_text());leads=json.loads((p/'nonref-targets01.json').read_text());targets={r['identity'] for r in leads['rows'] if r['form_type']==117}
rows=[r for r in c['rows'] if r['identity'] in targets];assert len(rows)==19
counts=collections.Counter(x['type'] for r in rows for x in r['fields'].get('140',[]))
for r in rows:
 r['beacon_pairs']=[x for x in r['fields'].get('140',[]) if x['type']=='starfield.esm:3e8651']
 r['target_hits_by_field']={k:[x for x in v if isinstance(x,dict) and x.get('reference') in {h for q in leads['rows'] for h in q['hits']}] for k,v in r['fields'].items() if isinstance(v,list)}
result=dict(schema='closed-location-target-join/1',source=c['source'],count=len(rows),total_pairs=sum(counts.values()),pair_types=dict(counts),rows=rows,all_type75_count=c['count'],all_type75_closed=True)
with (o/'location-target25.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
print(result['count'],result['total_pairs'],dict(counts))
for r in rows:print(r['identity'],r['beacon_pairs'],len(r['fields'].get('140',[])))
