# Original global QUST ALLA census, stdlib/project reader only.
# Reads all 38 installed ESMs from parent pinned context, writes new local numeric JSON.
import sys,json,struct,collections
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from extractor_resources import qualified
ctx=json.loads(Path('.local-work/workshop-population-rework/definition-80.json').read_text())
data=Path(r'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data')
paths={p.name.lower():p for p in data.glob('*.esm') if p.name in ctx['header_census']}; assert len(paths)==38
headers={};stats={}
for n,p in paths.items():
 stats[n]=(p.stat().st_size,p.stat().st_mtime_ns)
 r,fs=next(esm_records(p,{b'TES4'},repeated=True));headers[n]=dict(flags=r['flags'],masters=[v.rstrip(b'\0').decode().lower() for k,v in fs if k==b'MAST'])
flags={n:h['flags'] for n,h in headers.items()}; rows=[];counts={};totalaliases=0;questcount=0;keys=collections.Counter()
for n,p in paths.items():
 nq=na=nl=0
 for r,fs in esm_records(p,{b'QUST'},repeated=True):
  nq+=1;questcount+=1;alias=None;aliasname=None;edid=None
  for k,b in fs:
   if k==b'EDID':edid=b.rstrip(b'\0').decode('utf8')
   if k in (b'ALST',b'ALLS'):
    assert len(b)==4;alias=int.from_bytes(b,'little');aliasname=None;na+=1;totalaliases+=1
   if k==b'ALID':aliasname=b.rstrip(b'\0').decode('utf8')
   if k==b'ALLA':
    assert alias is not None and len(b)%8==0
    for i in range(0,len(b),8):
     kw,target=struct.unpack_from('<II',b,i);qkw=qualified(n,kw,headers[n]['masters'],flags);keys[qkw]+=1;nl+=1
     rows.append(dict(quest=qualified(n,r['formid'],headers[n]['masters'],flags),plugin=p.name,record_offset=r['offset'],formid=r['formid'],quest_name=edid,alias_id=alias,alias_name=aliasname,keyword=qkw,keyword_raw=kw,target_alias_id=target))
 counts[n]=dict(quest_variants=nq,aliases=na,ALLA_pairs=nl)
 assert (p.stat().st_size,p.stat().st_mtime_ns)==stats[n]
 print(p.name,nq,na,nl,flush=True)
out=dict(schema='global-installed-quest-alla/1',source_context='.local-work/workshop-population-rework/definition-80.json',coverage='All QUST record variants in all38 installedESMs; ordered aliasblocks, everyALLApair. No override selection required for absentkey conclusion.',quest_variants=questcount,alias_definitions=totalaliases,ALLA_pairs=len(rows),keyword_counts=[dict(keyword=k,count=v) for k,v in sorted(keys.items(),key=lambda kv:str(kv[0]))],workshop_links=[r for r in rows if r['keyword']=='starfield.esm:054ba6'],links=rows,census=counts,file_stat_before_after=stats)
Path('.local-work/workshop-population-rework/specialist/alla-global01.json').write_text(json.dumps(out,indent=2))
print('TOTAL',questcount,totalaliases,len(rows),'WORKSHOP',len(out['workshop_links']))
