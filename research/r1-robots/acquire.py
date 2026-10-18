# SPDX-License-Identifier: GPL-3.0-or-later
"""R1 bounded installed definition/script acquisition, not a production tool.

Reads ESM, ContentResources.zip and Misc.ba2; owned CR1 PEX/ESM readers, stdlib.
Writes exclusive ignored JSON only. No source save, target, database, Git or
network effects. Run from repository root; both-drive guard and pinned sources.
Provenance: CR2 definitions.py/grants.py; CR1 scripts.py, SOR-P-0002.
"""
from pathlib import Path
import argparse
import sys,json,struct,zlib,zipfile,contextlib,io
R=Path.cwd(); W=R/'.local-work/r1-robots'
sys.path[:0]=[str(R/'research/cr2-skills'),str(R/'save-analysis/scripts'),str(R/'.local-work/cr1-crew')]
from definitions import pin
from inventory_historical_saves import guard
from inspect_outpost_definitions import esm_records
from pex_probe import P

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args();assert args.run.isalnum()
 guard(); seed=json.loads((W/'baseline.json').read_text())
 paths={Path(p['path']).name:Path(p['path']) for p in seed['protected']}
 for name in ['Starfield.esm','ContentResources.zip','Starfield - Misc.ba2']:
  assert pin(paths[name])==next(p for p in seed['protected'] if p['path']==str(paths[name]))
 records=[]
 for h,fs in esm_records(paths['Starfield.esm'],{x.encode() for x in ['COBJ','PKIN','NPC_','GLOB','AVIF','KYWD','QUST','PERK','DFOB','REFR','ACHR']},repeated=True):
  ed=next((v.rstrip(b'\0').decode('utf8') for k,v in fs if k==b'EDID'),'')
  # Placed definitions only supply robot leads; retaining every placed payload
  # needlessly duplicates the proprietary ESM and consumes memory.
  if h['type'] in ('REFR','ACHR') and not any(k==b'NAME' and int.from_bytes(v,'little') in {0x4297c,0xbd67e,0x1d924e,0x1d9250,0x1f416e} for k,v in fs):continue
  records.append(dict(**h,edid=ed,fields=[(k.decode(),v.hex()) for k,v in fs]))
 (W/('definitions-'+args.run+'.json')).open('x',encoding='utf8').write(json.dumps(dict(source=pin(paths['Starfield.esm']),records=records),indent=2)+'\n')
 sources={}; selected=[]
 with zipfile.ZipFile(paths['ContentResources.zip']) as z:
  for n in z.namelist():
   if n.endswith('.psc') and (Path(n).stem in ['OutpostActorScript','OutpostBeaconScript','SQ_CrewScript','QF_PlayerSkills_002C59E4'] or 'robot' in Path(n).stem.lower()):
    b=z.read(n);sources[n]=dict(sha256=__import__('hashlib').sha256(b).hexdigest(),text=b.decode('utf-8-sig'));selected.append(n.replace('/Source','')[:-4]+'.pex')
 members={}
 with paths['Starfield - Misc.ba2'].open('rb') as f:
  _,_,kind,count,names=struct.unpack('<4sI4sIQ',f.read(24));assert kind==b'GNRL';f.seek(32)
  index=[struct.unpack('<I4sIIQIII',f.read(36)) for _ in range(count)];f.seek(names)
  names=[f.read(int.from_bytes(f.read(2),'little')).decode() for _ in range(count)]
  for name in selected:
   i=next((i for i,n in enumerate(names) if n.lower().replace('\\','/')==name.lower()),None)
   if i is None:members[name]=dict(error='MISSING_PEX');continue
   off,packed,size=index[i][4:7];f.seek(off);b=f.read(packed or size)
   if packed:b=zlib.decompress(b)
   assert len(b)==size
   with contextlib.redirect_stdout(io.StringIO()):d=P(b).parse()
   members[name]=dict(archive_offset=off,sha256=__import__('hashlib').sha256(b).hexdigest(),decoded=d)
 (W/('scripts-'+args.run+'.json')).open('x',encoding='utf8').write(json.dumps(dict(sources=sources,members=members),indent=2)+'\n')
 for name in ['Starfield.esm','ContentResources.zip','Starfield - Misc.ba2']:
  assert pin(paths[name])==next(p for p in seed['protected'] if p['path']==str(paths[name]))
 guard(); print('PASS',len(records),'records',len(members),'compiled members')
if __name__=='__main__':main()
