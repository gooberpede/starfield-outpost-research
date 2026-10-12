# SPDX-License-Identifier: GPL-3.0-or-later
"""Read existing immutable receipts and exact new build; write exclusive local lock.
No deployment, process handle, save/config writes or network. Requires 40GB/drive.
"""
import argparse
from pathlib import Path
from procedure import ROOT,read,write,sha,pins,archive_check

def prepare(build,out):
 build=Path(build).resolve(strict=True);b=read(build/'build.json')
 if b['version']!='0.4.0' or b['runtime_essential']!=['Data/SFSE/Plugins/SorNativePositionOracle.dll']:raise ValueError('build_contract')
 oldpath=ROOT/'.local-work/q030-module-inventory-fix/release-lock-05.json'
 if sha(oldpath)!='d25345876fa33719e9aaccc3bd021e6efa131c375e357687ec8c369956cacd73':raise ValueError('historical_lock_identity')
 old=read(oldpath);protected={str((ROOT/Path(k)).resolve()):v for k,v in old['pins'].items()}
 def pin(p,s=None):
  p=Path(p).resolve(strict=True);h=sha(p)
  if s and h!=s:raise ValueError('pin:'+str(p))
  protected[str(p)]=h
 for n,s in b['sources'].items():pin(ROOT/n,s)
 for n,s in b['protected'].items():pin(n,s)
 for n,s in b['external_runtime_prerequisites'].items():pin(n,s)
 pin(build/'build.json');pin(build/'SorNativePositionOracle-0.4.0.zip',b['zip_sha256']);pin(build/'SorNativePositionOracle.dll',b['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256']);pin(oldpath)
 for p in Path(__file__).parent.glob('*.py'):pin(p)
 for name in ['qualification.txt','inspection-tests.txt','branch-qualification.txt','branch-decoder-qualification.txt','branch-inspection-tests.txt','route-qualification.txt','route-decoder-tests.txt']:pin(build/name)
 lock=dict(external_runtime_prerequisites=b['external_runtime_prerequisites'],module_inventory_source='040_WORKER_COOPERATIVE_INVENTORY',version='0.4.0',schema=4,pins=protected,zip=str(build/'SorNativePositionOracle-0.4.0.zip'),package={n:v['sha256'] for n,v in b['files'].items()},runtime_essential=b['runtime_essential'],game_dir=old['game_dir'],save_dir=old['save_dir'],live_root=old['live_root'],installed_loader=old['installed_loader'],
  calls=[dict(rva=rva,target_rva=target,sha256=next(g['sha256'] for g in b['guards'] if g['rva']==rva)) for rva,target in b['call_pairs']],
  dll_sha256=b['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256'],game_sha256=b['game_hash'],sfse_sha256=b['sfse_hash'],build_sha256=sha(build/'build.json'))
 # CALL originals have five-byte hash rather than the wider guard hash.
 import sys
 sys.path.insert(0,str(ROOT/'research/exp0002'))
 from prepare import pe_layout,file_offset
 import hashlib,struct
 data=(Path(lock['game_dir'])/'Starfield.exe').read_bytes()
 if hashlib.sha256(data).hexdigest()!=b['game_hash']:raise ValueError('game_identity')
 _,_,sections=pe_layout(data)
 for c in lock['calls']:
  raw=data[file_offset(sections,c['rva'],5):][:5]
  if raw[0]!=0xe8 or c['rva']+5+struct.unpack_from('<i',raw,1)[0]!=c['target_rva']:raise ValueError('call_target')
  c['sha256']=hashlib.sha256(raw).hexdigest()
 pins(lock);archive_check(lock);write(out,lock);print(str(out));print(sha(out));print('pins',len(protected))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();prepare(a.build,a.out)
