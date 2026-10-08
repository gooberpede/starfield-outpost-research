"""Offline mature-outpost validation, stdlib only. Source-informed offbook methods.
Reads mature/S/L archive copies and prior project decoder/directory. Writes fresh
ignored JSON, no decoded blobs, source edits, target effects or dependencies.
64MiB decoded bound, one save at a time. Freeze extraction before opening JSON.
128/512-byte object windows are observation extents, not complete records.
"""
from pathlib import Path
import argparse,collections,datetime as dt,hashlib,importlib.util,json,re,shutil,struct,sys,zlib
from analyze_structural_containment import directory as historical_directory, REGION_NAMES
ROOT=Path(__file__).resolve().parents[2]
OFF=ROOT/'.local-work/mature-save-offbook'
SAVE=ROOT/'.local-work/savegames/Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs'
def sha(b): return hashlib.sha256(b).hexdigest()
def identity(p):
 s=p.stat();return dict(path=str(p.resolve()),size=s.st_size,sha256=sha(p.read_bytes()),mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,mtime_utc=dt.datetime.fromtimestamp(s.st_mtime,dt.timezone.utc).isoformat())
def write(p,v):
 with p.open('x',encoding='utf-8',newline='\n') as f: json.dump(v,f,indent=2);f.write('\n')
def positions(b,p): return [m.start() for m in re.finditer(re.escape(p),b)]
class Cursor:
 def __init__(self,b): self.b,self.p,self.trace=b,0,[]
 def take(self,n):
  if n<0 or n>len(self.b)-self.p: raise ValueError('boundary crossing')
  p=self.p;self.p+=n;return self.b[p:self.p]
 def count(self,label):
  p=self.p;h=self.take(1)[0];w={0:1,1:2,2:4}.get(h&3)
  if w is None: raise ValueError('unsupported count tag 3')
  b=bytes([h])+self.take(w-1);n=int.from_bytes(b,'little')>>2
  self.trace.append(dict(field=label,relative=p,width=w,bytes=b.hex(),value=n));return n
 def refs(self,n):
  if n>(len(self.b)-self.p)//3: raise ValueError('implausible reference count')
  return [self.take(3).hex() for _ in range(n)]
def grammar(b):
 c=Cursor(b);beacons=c.refs(c.count('beacon_count'));ng=c.count('group_count')
 if ng>(len(b)-c.p)//4: raise ValueError('implausible group count')
 groups=[]
 for i in range(ng):
  p=c.p;k=c.take(3).hex();refs=c.refs(c.count(f'group_{i}_count'));groups.append(dict(relative=p,key=k,refs=refs,end=c.p))
 if c.p!=len(b): raise ValueError('trailing bytes')
 return dict(beacons=beacons,groups=groups,trace=c.trace,consumed=c.p,duplicate_beacons=len(beacons)-len(set(beacons)),duplicate_keys=ng-len({g['key'] for g in groups}),duplicate_refs=sum(len(g['refs'])-len(set(g['refs'])) for g in groups))
def envelopes(b,d):
 a,z=d['regions']['region_R2'];rows=[]
 for q in positions(b[a:z],bytes.fromhex('79000000')):
  p=a+q
  if p+8>z: continue
  n=struct.unpack_from('<I',b,p+4)[0];end=p+8+n;framed=end+8<=z and b[end:end+8]==bytes.fromhex('7a00000028000000')
  r=dict(offset=p,payload_offset=p+8,length=n,end=end,qualifies=framed)
  if framed:
   r.update(header=b[p:p+8].hex(),successor=b[end:end+8].hex(),chunk=p//262144,chunk_relative=p%262144,payload_sha256=sha(b[p+8:end]))
   try: r['parsed']=grammar(b[p+8:end])
   except ValueError as e: r['error']=str(e)
  rows.append(r)
 return rows

def pool(b,d):
 field=d['regions']['region_R1'][0]+4;start=struct.unpack_from('<I',b,field)[0]
 if not d['regions']['late_region'][0]<=start<len(b)-2: raise ValueError('pool pointer')
 n=int.from_bytes(b[start:start+2],'little');p=start+2;entries=[]
 for i in range(n):
  if p+2>len(b): raise ValueError('pool length')
  length=int.from_bytes(b[p:p+2],'little');end=p+2+length
  if end>len(b): raise ValueError('pool bounds')
  entries.append(dict(index=i,offset=p,text_offset=p+2,length=length,bytes_hex=b[p+2:end].hex(),text=b[p+2:end].decode('utf-8',errors='backslashreplace')));p=end
 return dict(pointer_field=field,start=start,end=p,count=n),entries

def windows(b,a,z,t):
 token=bytes.fromhex(t);rows=[]
 for marker in (0x2a,0x3a):
  for q in positions(b[a:z],bytes([marker])+token):
   p=a+q;repeat=positions(b[p+4:min(p+48,z)],token)
   if repeat: rows.append(dict(offset=p,marker=f'{marker:02x}',repeats=[x+4 for x in repeat]))
 return rows

def directory(b):
 # Independently bounded by file length and exact table closure; auxiliary words
 # are recorded, not used as unexplained small-corpus semantic cardinality caps.
 found=[]
 for p in range(160,min(8192,len(b)-40)):
  v=struct.unpack_from('<10I',b,p);a,z=v[:2]
  if 1000<a<z<len(b) and 0<v[2]<v[3]<v[4]<v[5]<a:
   n=struct.unpack_from('<I',b,a)[0]
   if n<=(len(b)-a-4)//4 and a+4+4*n==z: found.append((p,v,n))
 if len(found)!=1: raise ValueError('directory closure ambiguous/missing')
 p,v,n=found[0];bounds=[0,v[2],v[3],v[4],v[5],v[0],v[1],len(b)]
 return dict(offset=p,words=list(v),reference_count=n,regions={name:[bounds[i],bounds[i+1]] for i,name in enumerate(REGION_NAMES)})

def extract(b,ch):
 d=directory(b);es=envelopes(b,d);valid=[e for e in es if e['qualifies']]
 if len(valid)!=1 or 'parsed' not in valid[0]: raise ValueError('ambiguous/invalid mature envelope')
 parsed=valid[0]['parsed'];active=set(parsed['beacons']);ps,entries=pool(b,d);a,z=d['regions']['region_R3'];beacons=[]
 for q in positions(b[a:z],bytes.fromhex('6c60e9')):
  q+=a;t=b[q+3:q+6].hex()
  for w in windows(b,a,z,t):
   p=w['offset']
   if w['marker']!='3a' or not 0<q-p<=32: continue
   names=[]
   # Index-bearing subunit terminates at observed 1100190004 motif.
   # Zero, one or two known animation indices may follow the name.
   # Earlier fixed-three-index assumption fails in 15/19 mature windows.
   animations={'OBJ_Outpost_Beacon_Deploy','OBJ_Outpost_Beacon_On_LP'}
   for tail in positions(b[p:p+512],bytes.fromhex('1100190004')):
    for width in (2,4,6):
     rel=tail-width
     if rel<0: continue
     ids=struct.unpack_from('<'+'H'*(width//2),b,p+rel)
     if all(i<len(entries) for i in ids) and entries[ids[0]]['text'] not in animations and all(entries[i]['text'] in animations for i in ids[1:]):
      names.append(dict(relative=rel,index_offset=p+rel,indices=list(ids),name_entry=entries[ids[0]],animation_entries=[entries[i] for i in ids[1:]],index_bytes=b[p+rel:p+tail].hex(),terminator_offset=p+tail))
   beacons.append(dict(**w,token=t,base_offset=q,base_relative=q-p,active=t in active,names=names))
 bt={v['token']:v for v in beacons}
 if len(bt)!=len(beacons) or not active<=bt.keys() or any(len(v['names'])!=1 for v in beacons): raise ValueError('ambiguous beacon/name')
 names={t:v['names'][0]['name_entry']['text'] for t,v in bt.items()}
 def owners(p):
  rows=[]
  for t in bt:
   pattern=bytes.fromhex('454ba6'+t)
   for rel in positions(b[p:min(p+128,z)],pattern): rows.append(dict(beacon=t,name=names[t],relative=rel,offset=p+rel,bytes=pattern.hex(),active=t in active))
  return rows
 tokens=active|{g['key'] for g in parsed['groups']}|{t for g in parsed['groups'] for t in g['refs']}
 tw={t:[dict(**w,associations=owners(w['offset'])) for w in windows(b,a,z,t)] for t in sorted(tokens-{'000000'})}
 pads=[]
 for base,typ in [('6a6c3f','regular'),('619523','interstellar')]:
  for q in positions(b[a:z],bytes.fromhex(base)):
   q+=a;t=b[q+3:q+6].hex()
   for w in windows(b,a,z,t):
    p=w['offset']
    if w['marker']!='2a' or not 0<q-p<=32: continue
    links=[dict(relative=r,offset=p+r,keyword='655cc8',token=b[p+r+3:p+r+6].hex()) for r in positions(b[p:min(p+128,z)],bytes.fromhex('655cc8'))]
    pads.append(dict(**w,token=t,type=typ,base_bytes=base,base_offset=q,base_relative=q-p,associations=owners(p),keyword_refs=links))
 pd={p['token']:p for p in pads}
 if len(pd)!=len(pads): raise ValueError('duplicate pad windows')
 arrows={};unknown=[]
 for p in pads:
  ns=[r['token'] for r in p['keyword_refs'] if r['token']!=p['token'] and 0x80<=int(r['token'][:2],16)<0xc0]
  if len(ns)>1 or any(t not in pd for t in ns): unknown.append(dict(token=p['token'],refs=ns))
  elif ns: arrows[p['token']]=ns[0]
 pairs=[]
 for s,t in arrows.items():
  if arrows.get(t)!=s: unknown.append(dict(nonreciprocal=[s,t]))
  elif s<t: pairs.append([s,t])
 return dict(decoded_size=len(b),decoded_sha256=sha(b),chunks=ch,directory=d,envelopes=es,pool=ps,beacons=beacons,token_windows=tw,pads=pads,pairs=pairs,unresolved=unknown)

def compare(x,j):
 net=j['networks'][0]['network'];ops=net['outposts'];byid={o['id']:o for o in ops};active=[b['names'][0]['name_entry']['text'] for b in x['beacons'] if b['active']]
 def owner(p):
  v=p['associations']
  if len(v)!=1 or not v[0]['active']: raise ValueError('ambiguous/inactive pad owner')
  return v[0]['name']
 pd={p['token']:p for p in x['pads'] if len(p['associations'])==1 and p['associations'][0]['active']};rows=[]
 for name in sorted(set(active)|{o['name'] for o in ops}):
  js=[o for o in ops if o['name']==name];actual=collections.Counter(p['type'] for p in pd.values() if owner(p)==name);expected=collections.Counter(p['type'] for o in js for p in o['cargoPads'])
  rows.append(dict(name=name,save_member=name in active,json_members=len(js),save=dict(actual),json=dict(expected),equal=actual==expected))
 obs=collections.Counter(tuple(sorted([owner(pd[s]),owner(pd[t])])) for s,t in x['pairs']);exp=collections.Counter(tuple(sorted([byid[e['endpointA']['outpostId']]['name'],byid[e['endpointB']['outpostId']]['name']])) for e in net['cargoLinks'])
 jp={p['id']:(o['name'],p['type']) for o in ops for p in o['cargoPads']};je=[]
 for e in net['cargoLinks']:
  aa,bb=e['endpointA'],e['endpointB'];je.append((jp[aa['cargoPadId']],jp[bb['cargoPadId']],aa['cargoPadId'],bb['cargoPadId']))
 ep=[]
 for s,t in x['pairs']:
  a=(owner(pd[s]),pd[s]['type']);b=(owner(pd[t]),pd[t]['type']);matches=[]
  for u,v,ui,vi in je:
   if (a,b)==(u,v): matches.append([ui,vi])
   if (a,b)==(v,u): matches.append([vi,ui])
  ep.append(dict(save_tokens=[s,t],signature=[a,b],json_pad_pairs=matches,ambiguity='unique_by_signature_only' if len(matches)==1 else 'permutation' if matches else 'mismatch'))
 return dict(names_equal=collections.Counter(active)==collections.Counter(o['name'] for o in ops),per_outpost=rows,topology_equal=obs==exp,multigraph=[dict(names=list(e),save_count=obs[e],json_count=exp[e]) for e in sorted(set(obs)|set(exp))],endpoint_matches=ep,json_links=len(je),json_pad_types=dict(collections.Counter(v[1] for v in jp.values())))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args()
 if not re.fullmatch('[A-Za-z0-9_-]+',args.run): raise ValueError('run name')
 for drive in ('C:/','D:/'):
  if shutil.disk_usage(drive).free<40_000_000_000: raise ValueError('free-space stop')
 out=ROOT/'.local-work/mature-save-validation'/args.run;out.mkdir(parents=True,exist_ok=False)
 js=list((ROOT/'.local-work/scratch').glob('*.json'))
 if len(js)!=1: raise ValueError('comparison JSON ambiguous')
 scripts=list(OFF.glob('*.py'))+list(Path(__file__).parent.glob('*.py'))
 manifests=[ROOT/'.local-work'/f/'manifest.json' for f in ('manual-S0-S7C','output-link-L0-L2C')]
 prior_analyses=[p.parent/'analysis-01/analysis.json' for p in manifests]
 before={str(p):identity(p) for p in [SAVE,js[0]]+scripts+manifests+prior_analyses};write(out/'inputs-before.json',before)
 spec=importlib.util.spec_from_file_location('preserved_local_decode',OFF/'local_decode.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 physical=SAVE.read_bytes();raw,ch=mod.decode(physical);x=extract(raw,ch)
 x['framing']=dict(size=len(physical),table_end=72+len(ch)*4,stream_start=struct.unpack_from('<Q',physical,24)[0],alignment_hex=physical[72+len(ch)*4:ch[0]['file_offset']].hex(),embedded_build_offsets=positions(raw,b'1.16.244.0'))
 write(out/'save-extraction.json',x);frozen=identity(out/'save-extraction.json');write(out/'extraction-frozen.json',frozen);del raw,physical
 cmp=compare(json.loads((out/'save-extraction.json').read_text()),json.loads(js[0].read_text(encoding='utf-8')));write(out/'comparison.json',cmp)
 corpus=[];negatives=[]
 for folder,labels in [('manual-S0-S7C',[f'S{i}{c}' for i in range(8) for c in ('','C')]),('output-link-L0-L2C',['L0','L0C','L1','L1C','L2','L2C'])]:
  m=json.loads((ROOT/'.local-work'/folder/'manifest.json').read_text())
  prior_analysis=json.loads((ROOT/'.local-work'/folder/'analysis-01/analysis.json').read_text())
  for label in labels:
   s=next(s for s in m['samples'] if s['label']==label);p=Path(s['copy']['path']);prior=identity(p)
   if prior['sha256']!=s['copy']['sha256']: raise ValueError('corpus hash')
   raw,ch=mod.decode(p.read_bytes())
   old=next(r for r in prior_analysis['samples'] if r['label']==label)
   if sha(raw)!=old['decoded_sha256']: raise ValueError('prior decoded hash mismatch')
   d=directory(raw);es=envelopes(raw,d);corpus.append(dict(label=label,sample_id=s['sample_id'],source=prior,decoded_sha256=sha(raw),envelopes=es))
   for e in es:
    if not e['qualifies']: continue
    for shift in range(-8,9):
     if shift==0: continue
     start=e['payload_offset']+shift
     try: grammar(raw[start:start+e['length']]);accepted=True
     except ValueError: accepted=False
     negatives.append(dict(label=label,shift=shift,accepted=accepted))
   if identity(p)!=prior: raise ValueError('corpus changed')
   del raw
 if identity(out/'save-extraction.json')!=frozen: raise ValueError('frozen extraction changed')
 after={p:identity(Path(p)) for p in before}
 if before!=after: raise ValueError('source/script changed')
 write(out/'corpus.json',corpus);write(out/'negative-controls.json',negatives);write(out/'inputs-after.json',after)
 write(out/'run.json',dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),python=sys.version,python_executable=identity(Path(sys.executable)),zlib=zlib.ZLIB_RUNTIME_VERSION,frozen=frozen,corpus_preserved=len(corpus),max_decoded_size=64*1024*1024,decoded_files_written=0,space={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}))
 print('Frozen',frozen['sha256'],'beacons',sum(b['active'] for b in x['beacons']),'marker windows',len(x['pads']),'pairs',len(x['pairs']),'topology',cmp['topology_equal'])
 print('Corpus',len(corpus),'negative accepts',sum(n['accepted'] for n in negatives),'of',len(negatives))
if __name__=='__main__': main()
