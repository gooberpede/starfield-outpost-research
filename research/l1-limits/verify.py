# SPDX-License-Identifier: GPL-3.0-or-later
"""L1 offline evidence verification; run from repo cwd with CPython -B.

Reads baseline/protected sources, fresh definition/PEX/native/save receipts and
retained R1/Workshop methods. Physically rereads selected ESM records and saved
root records. Writes exclusive ignored receipt/metadata CSV; never writes saves,
database, target, Git or network. Stdlib/owned readers only, 40GB C:/D: guards.
These checks prove correspondence/integrity, not actual game execution.
"""
from pathlib import Path
import sys,json,struct,zlib,hashlib,subprocess,argparse,csv,collections
R=Path.cwd();W=R/'.local-work/l1-limits';D=R/'docs/experiments/limits'
sys.path[:0]=[str(R/'research/cr2-skills'),str(R/'save-analysis/scripts')]
from definitions import pin
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords
from stream_save import decoded_save
from validate_mature_outposts import directory
from workshop_population import typed_records,initial_prefix
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);a=ap.parse_args();assert a.run.isalnum();out=W/('verification-'+a.run+'.json');assert not out.exists();guard();checks=[]
 def check(name,value):
  if not value:(W/('failure-'+a.run+'.json')).open('x',encoding='utf8').write(json.dumps(dict(failed=name,prior_checks=checks),indent=2)+'\n')
  assert value,name
  checks.append(name)
 seed=json.loads((W/'baseline.json').read_text());rows=json.loads((W/'definitions01.json').read_text())['records'];by={r['formid']:r for r in rows};conds=json.loads((W/'conditions01.json').read_text())['records'];by.update({r['formid']:r for r in conds})
 old=json.loads((R/'.local-work/r1-robots/definitions-final.json').read_text())['records'];by[7]=next(r for r in old if r['formid']==7)
 for p in seed['protected']+[seed['brief'],seed['index']]:check('protected '+p['path'],pin(Path(p['path']))==p)
 check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==seed['head'])
 recipes=[r for r in rows if r['type']=='COBJ'];limited=[r for r in recipes if 'JNAM' in dict(r['fields'])];named=[r for r in recipes if 'outpost' in r['edid'].lower()]
 check('complete COBJ cardinality',len(recipes)==3009);check('bounded name candidates',len(named)==576);check('all JNAM in named candidates',len(limited)==51 and all(r in named for r in limited));check('no-JNAM count',len(named)-len(limited)==525)
 globals_expected={0xf7c96:(6,7),0x22f4c9:(1,4),0x1d9f5e:(3,8),0x3f4aee:(6,23),0x7875a:(1,4),0x190d57:(3,2),0x1f818b:(1,1),0x1b4bb2:(3,1),0x2ce192:(1,1)}
 for fid,(value,count) in globals_expected.items():
  check('global '+hex(fid),struct.unpack('<f',bytes.fromhex(dict(by[fid]['fields'])['FLTV']))[0]==value)
  check('recipe group '+hex(fid),sum(int.from_bytes(bytes.fromhex(dict(r['fields'])['JNAM']),'little')==fid for r in limited)==count)
 selected={r['formid'] for r in named}|set(globals_expected)|{7,0x2c59e4,0x23826f,0x27cbc2,0x2a84f6,0x2a84f7,0x3b6c2,0x2dfd42,0x2dfd43,0x2dfd44,0x2dfd45,0x2dfd46,0x2dfd47,0x2e88ec}
 matrix=list(csv.DictReader((R/'docs/experiments/planetary-surface-anchor/matrix.csv').open()));selected|={int(x['body_formid'],16) for x in matrix}|{0x295ec8,0x295ec2,0x295ebe,0x279292,0x279293,0x295eba}
 esm=next(Path(p['path']) for p in seed['protected'] if Path(p['path']).name=='Starfield.esm')
 with esm.open('rb') as f:
  for fid in sorted(selected):
   r=by[fid];f.seek(r['offset']);h=f.read(24);n,flags,actual=struct.unpack_from('<III',h,4);check('ESM header '+hex(fid),actual==fid and h[:4].decode()==r['type']);b=f.read(n)
   if flags&0x40000:
    sz=int.from_bytes(b[:4],'little');b=zlib.decompress(b[4:]);check('ESM decompression '+hex(fid),len(b)==sz)
   check('ESM physical fields '+hex(fid),[(k.decode(),v.hex()) for k,v in subrecords(b)]==[tuple(x) for x in r['fields']])
 prps=bytes.fromhex(dict(by[7]['fields'])['PRPS']);check('player baseline eight',len(prps)%12==0 and struct.unpack_from('<IfI',prps,0x90)==(0x2a84f7,8.0,0))
 vm=bytes.fromhex(dict(by[0x2c59e4]['fields'])['VMAD'])
 for prop,typ,expected in [('OutpostManagementCargoLinksBonus',3,3),('OutpostManagementBonus',3,3),('OutpostMaxDeployed',1,0x2a84f7),('Outpost_BuildLimit_CargoLinks',1,0x190d57)]:
  needle=struct.pack('<H',len(prop))+prop.encode()+bytes([typ,1]);at=vm.lower().find(needle.lower());check('VMAD property '+prop,at>=0);value=int.from_bytes(vm[at+len(needle)+(4 if typ==1 else 0):at+len(needle)+(8 if typ==1 else 4)],'little');check('VMAD value '+prop,value==expected)
 scripts=json.loads((W/'scripts01.json').read_text());quest=next(v for k,v in scripts['members'].items() if 'PlayerSkills' in k);funcs={n:b for o in quest['decoded']['objects'] for _,ff in o['states'] for n,b in ff}
 for rank,val in enumerate([12,16,20,24],1):
  ops=funcs[f'Fragment_Stage_090{rank}_Item_00']['ops'];check('compiled deployment rank '+str(rank),any(op['op']==23 and op['args'][0][1]=='SetValue' and op['args'][-1][-1]==[4,val] for op in ops))
 check('compiled cargo stage',any(op['op']==23 and op['args'][0][1]=='Mod' and 'CargoLinks' in str(op['args']) for op in funcs['Fragment_Stage_0701_Item_00']['ops']))
 for n,v in scripts['members'].items():check('PEX object closure '+n,all(o['end']==o['declared_end'] for o in v['decoded']['objects']))
 native_checks={2:['140f3b297\tCMP qword ptr [RAX + 0x178],R15','1421dcbfc\tMOV byte ptr [R13 + 0x61f],AL'],3:['1415f6be8\tMOV RDX,qword ptr [0x145913418]'],5:['FUN_140e466f0(DAT_145f0ace8 + 0x38','return \'\\x03\''],11:['1421b3eae\tVMOVSS XMM3,dword ptr [0x144f0528c]','1421b7904\tVMOVSS XMM3,dword ptr [0x144f044e8]'],16:['selected=3\tcancelled=false','0x135a','0x1345','0x11fb'],18:['*(uint *)(lVar5 + 0x1c0)','*(longlong **)(lVar5 + 0x1c8)']}
 for n,needles in native_checks.items():
  s=(W/f'native/{n:03}.request.tsv').read_text();check('native identity '+str(n),'SHA256\t'+seed['protected'][2]['sha256'] in s and 'BASE\t140000000' in s)
  for needle in needles:check('native evidence '+needle,needle in s)
 # Retained root corpus independently joined to freshly framed actual Save52.
 groups=json.loads((W/'root-groups01.json').read_text());wanted={x['instance_identity']:x for g in groups for x in g['roots']};src=json.loads((W/'save-HIST-0267.json').read_text())['source'];p=Path(src['path']);check('Save52 prehash',pin(p)==src);seen={}
 with decoded_save(p,W/'verify-scratch') as (data,decoded):
  dr=directory(data);forms=struct.unpack_from('<'+'I'*dr['reference_count'],data,dr['regions']['reference_u32'][0]+4);plugins=plugin_tables(data)
  def resolve(t):return saved_form(token_value(t,forms),plugins)
  for r in typed_records(data):
   ident=resolve(r['token'])
   if ident not in wanted:continue
   old=wanted[ident];check('root record bounds '+ident,r['offset']==int(old['record_offset']) and r['end']==int(old['record_end']));pfx=initial_prefix(data,r);check('root actual base '+ident,resolve(pfx['base_token'])==old['base_identity']);seen[ident]=dict(offset=r['offset'],end=r['end'],body_sha256=hashlib.sha256(data[r['body']:r['end']]).hexdigest())
 check('all selected limited roots reread',set(seen)==set(wanted));check('Save52 posthash',pin(p)==src)
 for p in sorted(W.glob('save-*.json')):
  j=json.loads(p.read_text());check('saved source '+j['label'],pin(Path(j['source']['path']))==j['source'] and j['source_unchanged'])
 check('real turret contrasts',len(json.loads((W/'save-HIST-0255.json').read_text())['turrets'])==2)
 receipt=dict(run=a.run,checks=checks,total=len(checks),physical_esm_records=len(selected),save52_roots=seen,limits='Integrity/framing and correspondence checks; no game execution, loaded AV or semantic runtime oracle',failed_attempts='review.md',guard_bytes=40000000000)
 out.open('x',encoding='utf8').write(json.dumps(receipt,indent=2)+'\n');guard();print('PASS',len(checks),'checks',len(selected),'physical ESM records',len(seen),'limited construction roots')
if __name__=='__main__':main()
