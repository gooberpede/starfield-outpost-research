"""Header-only qualification of graph terminals; writes local receipt only."""
from pathlib import Path
import json,struct,collections
W=Path('.local-work/build-catalogue');g=json.loads((W/'graph02.json').read_text());wanted={int(i,16) for i in g['missing_ids']};src=Path(json.loads((W/'definitions.json').read_text())['source']['path']);p=0;total=src.stat().st_size;out=[]
with src.open('rb') as f:
 while p<total:
  f.seek(p);h=f.read(24);n,flags,i=struct.unpack_from('<III',h,4);t=h[:4].decode()
  if t!='GRUP' and i in wanted:out.append(dict(formid=f'{i:08x}',type=t,offset=p,flags=flags))
  p+=24 if t=='GRUP' else n+24
assert p==total and len(out)==len(wanted)
(W/'terminal-types.json').open('x',encoding='utf8').write(json.dumps(out,indent=2)+'\n');print(dict(collections.Counter(x['type'] for x in out)))
