# SPDX-License-Identifier: GPL-3.0-or-later
"""R1 integrity and real-record verification; repository cwd, installed CPython.

Reads baseline, source saves, actual ESM bytes and retained raw records; stdlib
and owned readers only. Writes exclusive ignored --run receipt. Checks framing,
definition correspondence, template masks and pins, not runtime operation.
No source/target/database/Git/network writes. Both-drive guards fail closed.
"""
from pathlib import Path
import sys,json,hashlib,struct,zlib,subprocess,argparse
R=Path.cwd();W=R/'.local-work/r1-robots'
sys.path[:0]=[str(R/'research/r1-robots'),str(R/'research/cr1-crew'),str(R/'save-analysis/scripts')]
from links import explicit_actor_links,actor_prefix
from current import explicit_actor_links as old_links
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard
def pin(p):
 with p.open('rb') as f:return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);a=ap.parse_args();assert a.run.isalnum();guard();checks=[]
 def check(n,b):
  assert b,n
  checks.append(n)
 seed=json.loads((W/'baseline.json').read_text())
 for p in seed['protected']+[seed['index'],seed['brief']]:check('preserved '+p['path'],pin(Path(p['path']))==p)
 check('HEAD preserved',subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==seed['head'])
 defs=json.loads((W/'definitions-final.json').read_text());by={r['formid']:r for r in defs['records']}
 recipes=[r for r in defs['records'] if r['type']=='COBJ' and dict(r['fields']).get('FNAM')=='5f9f1d00']
 check('all eight category recipes',len(recipes)==8)
 ids={r['formid'] for r in recipes}|{int.from_bytes(bytes.fromhex(dict(r['fields'])['CNAM']),'little') for r in recipes}|{0x4297e,0x4297f,0x21b8c3,0x21b8c8,0x20d24f,0x172f8f,0x172f8e,0x1d9f5e,0x2c59e4,0x9b33e}
 rereads=[]
 with Path(defs['source']['path']).open('rb') as f:
  for fid in sorted(ids):
   r=by[fid];f.seek(r['offset']);h=f.read(24);n,flags,actual=struct.unpack_from('<III',h,4);check('ESM identity '+hex(fid),actual==fid and h[:4].decode()==r['type']);b=f.read(n)
   if flags&0x40000:
    expected=int.from_bytes(b[:4],'little');b=zlib.decompress(b[4:]);check('ESM decoded bounds '+hex(fid),len(b)==expected)
   check('ESM exact fields '+hex(fid),[(k.decode(),v.hex()) for k,v in subrecords(b)]==[tuple(x) for x in r['fields']]);rereads.append(dict(formid=f'{fid:08x}',offset=r['offset']))
   if r in recipes:check('shared count global '+hex(fid),dict(r['fields'])['JNAM']=='5e9f1d00')
 for fid in [0x4297d,0x1d8ee5,0x337eab]:
  check('no ordinary process grant '+hex(fid),not any(k=='PRKR' for k,v in by[fid]['fields']) and not int.from_bytes(bytes.fromhex(dict(by[fid]['fields'])['ACBS'])[14:16],'little')&8)
 for fid in [0x4297c,0x4297d,0xbd67e,0x1f416e,0x1d9250,0x1d924e,0x337eab,0x1d8ee5]:
  source=fid;seen=set()
  while int.from_bytes(bytes.fromhex(dict(by[source]['fields'])['ACBS'])[14:16],'little')&0x200:
   check('script template cycle guard '+hex(source),source not in seen);seen.add(source)
   source=struct.unpack('<15I',bytes.fromhex(dict(by[source]['fields'])['TPTA']))[9]
  vm=bytes.fromhex(dict(by[source]['fields'])['VMAD'])
  check('selected script binding '+hex(fid),b'OutpostActorScript' in vm and b'AssignAsCrewOnCreation' in vm and b'CrewSlotCost' in vm and b'CrewReassignDisabled' in vm)
 vmad=bytes.fromhex(dict(by[0x2c59e4]['fields'])['VMAD']);name=b'OutpostManagementBonus';needle=struct.pack('<H',len(name))+name+b'\x03\x01';at=vmad.find(needle)
 check('installed quest bonus overrides default with3',at>=0 and struct.unpack_from('<i',vmad,at+len(needle))[0]==3)
 check('robot global initial3',struct.unpack('<f',bytes.fromhex(dict(by[0x1d9f5e]['fields'])['FLTV']))[0]==3)
 scripts=json.loads((W/'scripts-final.json').read_text())['members']
 actor=next(v for n,v in scripts.items() if n.lower().endswith('/outpostactorscript.pex'))
 objects=actor['decoded']['objects'];variables={v[0]:v[3] for v in objects[0]['variables']}
 check('compiled robot slot modifier default minus1',variables['::CrewSlotCostValue_var']==[3,-1])
 funcs={name:body for o in objects for _,fs in o['states'] for name,body in fs}
 check('compiled placement calls SetValue/ModValue',all(any(op['op']==23 and op['args'][0][1].lower()==x for op in funcs['OnWorkshopObjectPlaced']['ops']) for x in ['setvalue','modvalue']))
 helper=funcs['CheckAssignAsCrew'];check('compiled assign and remove paths',all(any(op['op']==23 and op['args'][0][1].lower()==x for op in helper['ops']) for x in ['assigncrew','unassigncrew']))
 quest=next(v for n,v in scripts.items() if n.lower().endswith('/qf_playerskills_002c59e4.pex'))
 f702=next(body for o in quest['decoded']['objects'] for _,fs in o['states'] for name,body in fs if name=='Fragment_Stage_0702_Item_00')
 check('compiled stage702 modifies robot global',any(op['op']==23 and op['args'][0][1].lower()=='mod' and 'Outpost_BuildLimit_Robots' in str(op['args']) for op in f702['ops']))
 successful=0;missing=[];positive=[]
 for path in sorted(W.glob('HIST-*.json')):
  d=json.loads(path.read_text())
  if d.get('missing'):missing.append(path.stem);continue
  check('original rehash '+path.stem,pin(Path(d['source']['path']))==d['source']);successful+=1
  for row in d['robots']:
   rec=row['record'];data=bytearray(rec['end']);data[rec['body']:rec['end']]=bytes.fromhex(row['body_hex']);resolve=dict(zip(rec['refs'],row['queue'])).__getitem__
   l=explicit_actor_links(data,rec,resolve);edges={e['keyword']:e for e in l['entries']};owner=edges['starfield.esm:054ba6']['target'];check('reciprocal keyed robot '+row['identity'],edges['starfield.esm:26beac']['target']==owner)
   dest=next(r for r in d['owners'] if r['identity']==owner);e2=next(e for e in dest['extras']['extras'] if e['type']=='e2');check('independent beacon member '+row['identity'],row['identity'] in e2['members'])
   for e in l['entries']:
    check('independent mode byte '+row['identity']+e['keyword'],data[e['mode_offset']]==e['mode'])
    i=e['keyword_queue_index'];check('independent pair '+row['identity']+e['keyword'],row['queue'][i:i+2]==[e['keyword'],e['target']])
   try:old_links(data,rec,resolve)
   except ValueError as e:check('preserved CR3 9C gap '+row['identity'],'9C' in str(e))
   else:raise AssertionError('expected old 9C boundary')
   try:explicit_actor_links(data,dict(rec,buffer_version=152),resolve)
   except ValueError:checks.append('wrong-version rejected '+row['identity'])
   else:raise AssertionError('wrong version accepted')
   try:explicit_actor_links(data,dict(rec,refs=rec['refs'][:2]),resolve)
   except ValueError:checks.append('short queue rejected '+row['identity'])
   else:raise AssertionError('short queue accepted')
   positive.append(dict(sample=path.stem,actor=row['identity'],owner=owner,link_offset=l['trace'][-1]['start']))
 check('eight independent actor identities',len({x['actor'] for x in positive})==8)
 check('137 readable mature originals',successful==137)
 check('one unavailable original retained',missing==['HIST-0167'])
 for p in seed['protected']+[seed['index'],seed['brief']]:check('postcheck '+p['path'],pin(Path(p['path']))==p)
 out=dict(checks=checks,passed=len(checks),successful_saves=successful,missing=missing,physical_esm_rereads=rereads,positive_joins=positive,limits='Integrity/framing/static correspondence, not historical runtime operation or all save representations')
 (W/('verification-'+a.run+'.json')).open('x',encoding='utf8').write(json.dumps(out,indent=2)+'\n');guard();print('PASS',len(checks),'checks',successful,'source saves',len(positive),'robot joins')
if __name__=='__main__':main()
