# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline supplemental qualification. Reads exact own DLL/receipts and protected
pins, executes own DLL refusal API in disposable Python only, original tests and
frozen regression. Writes exclusive local receipt/logs. Never game/SFSE execution,
process attachment, deployment, database/save mutation, download or network.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from procedure import ROOT,guard,sha,write

def main(build,out):
 guard();out=Path(out);out.mkdir(parents=True,exist_ok=False);build=Path(build)
 m=json.loads((build/'build.json').read_text());dll=build/'SorNativePositionOracle.dll'
 if sha(dll)!=m['files']['Data/SFSE/Plugins/SorNativePositionOracle.dll']['sha256']:raise ValueError('dll_pin')
 old=ROOT/'.local-work/q030-module-inventory-fix/release-lock-05.json';pins=json.loads(old.read_text())['pins']
 def protect():
  for p,h in pins.items():
   if sha(ROOT/Path(p))!=h:raise ValueError('protected:'+p)
 protect()
 # Own instrument loaded only in this disposable interpreter. Runtime checks
 # reject nullptr, wrong runtime/interface and correct API with wrong host image.
 api=(ctypes.c_uint32*64)();api[0]=0x00020015
 lib=ctypes.WinDLL(str(dll.resolve()));load=lib.SFSEPlugin_Load;load.argtypes=[ctypes.c_void_p];load.restype=ctypes.c_bool
 refusals=[]
 for label,ptr,runtime,interface in [('null',None,0,0),('wrong_version',ctypes.addressof(api),0,1),('wrong_interface',ctypes.addressof(api),(1<<24)|(16<<16)|(244<<4),2),('wrong_host_image',ctypes.addressof(api),(1<<24)|(16<<16)|(244<<4),1)]:
  api[1]=runtime;api[2]=interface
  if load(ptr):raise ValueError('startup_refusal:'+label)
  refusals.append(label)
 results=[]
 commands=[('procedure-tests',[sys.executable,'-B','-m','unittest','discover','-s',str(ROOT/'research/existing-reference-grid'),'-p','test_*.py']),
 ('save-regressions',[sys.executable,'-B','-m','unittest','discover','-s',str(ROOT/'save-analysis/scripts'),'-p','test_*.py'])]
 for label,cmd in commands:
  guard();r=subprocess.run(cmd,cwd=ROOT,capture_output=True);path=out/(label+'.txt');path.write_bytes(r.stdout+r.stderr)
  results.append(dict(label=label,exit=r.returncode,path=str(path),sha256=sha(path)))
  if r.returncode:raise RuntimeError(label)
 # Frozen replay is retained separately using verify_position_v2.py.
 protect();receipt=dict(build=str(build),build_sha256=sha(build/'build.json'),dll_sha256=sha(dll),startup_refusals=refusals,regressions=results,protected_pins=len(pins),disk=guard(),native_equivalence='NOT TESTED')
 write(out/'receipt.json',receipt);print(json.dumps(receipt))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.build,a.out)
