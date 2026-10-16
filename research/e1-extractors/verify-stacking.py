# SPDX-License-Identifier: GPL-3.0-or-later
"""Original scoped offline receipts, definition gates and preservation checker.
Reads task inventories/exports, installed ESM/exe/database files and baseline;
writes one exclusive ignored JSON receipt. Requires repository cwd, CPython
stdlib and owned disk guard. No game/save/process/project/index/network effects.
Text-presence checks are locators, not native semantic oracles. No simulator.
"""
from pathlib import Path
import csv
import hashlib
import json
import struct
import sys
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'.local-work/e1-stacking'
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inventory_historical_saves import guard

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    guard()
    checks=[]
    def check(ok,label):
        assert ok,label
        checks.append(label)
    before=json.loads((BASE/'protected-before.json').read_text())
    after=[]
    for p in before:
        f=Path(p['path'])
        actual=dict(path=str(f),size=f.stat().st_size,sha256=sha(f))
        check(actual==p,'protected '+p['path'])
        after.append(actual)
    definitions=json.loads((BASE/'research-definitions01.json').read_text())
    check(sha(Path(definitions['source']))==definitions['sha256'],'installed ESM unchanged')
    projects=[r for r in definitions['records'] if r['type']=='RSPJ']
    recipes=[r for r in definitions['records'] if r['type']=='COBJ']
    outposts=[r for r in projects if r['edid'].startswith('Outpost_Research_')]
    check(len(projects)==82 and len(recipes)==3009,'82 projects / 3009 recipes')
    check(len(outposts)==20,'20 Outpost projects')
    check(all(dict(r['fields'])['NNAM']=='0000' for r in projects),'all 82 NNAM zero')
    ids={r['formid'] for r in outposts}
    gates={}
    for r in recipes:
        for tag,value in r['fields']:
            b=bytes.fromhex(value)
            if tag=='CTDA' and len(b)>=16 and int.from_bytes(b[8:10],'little')==0x36a:
                target=int.from_bytes(b[12:16],'little')
                if target in ids:
                    gates.setdefault(r['formid'],set()).add(target)
    check(len(gates)==307,'307 unique recipes with exact Outpost research parameter')
    check(sum(0x389f0b in v for v in gates.values())==51,'51 ResourceExtraction1 recipes')
    check(sum(0x389f0c in v for v in gates.values())==51,'51 ResourceExtraction2 recipes')
    perks=json.loads((ROOT/'.local-work/e1-production/perks01.json').read_text())['records']
    research_conditions=[]
    for r in perks:
        for tag,value in r['fields']:
            b=bytes.fromhex(value)
            if tag=='CTDA' and len(b)>=16 and int.from_bytes(b[8:10],'little')==0x36a:
                research_conditions.append(r['formid'])
    check(len(perks)==502 and not research_conditions,'502 main PERKs / no research condition 036a')
    mag=next(r for r in perks if r['formid']==0x208e92)
    rank=None
    timer_ranks=[]
    for tag,value in mag['fields']:
        if tag=='PRKE':rank=bytes.fromhex(value)[1]
        if tag=='DATA' and value=='a10302':timer_ranks.append(rank)
    check(timer_ranks==[3,4],'guide timer entries at zero-based ranks3/4')
    robot=json.loads((BASE/'robot-scripts01.json').read_text())
    needle=struct.pack('<H',22)+b'AssignAsCrewOnCreation'+bytes([5,1,1])
    for name in ['OutpostRobotMiniBotA_Garden','OutpostRobotMiniBotA_Sanitation','OutpostRobotModelA01']:
        rec=next(r for r in robot if r['edid']==name)
        raw=bytes.fromhex(dict(rec['fields'])['VMAD'])
        check(b'OutpostActorScript' in raw and needle in raw,'explicit robot Boolean '+name)
    for file,needles in {
        '07':['FUNCTION\t140408a50','CrewExtraData::vftable'],
        '08':['FUNCTION\t1404076b0','FUNCTION\t141954810','FUNCTION\t141801ee0','Health'],
        '11':['FUNCTION\t140ca3910','FUNCTION\t14040a9d0','FUNCTION\t140c07e70'],
        '12':['FUNCTION\t140ca1bd0','FUNCTION\t14200e610'],
    }.items():
        s=(ROOT/'.local-work/recon'/('e1-stacking-'+file+'.tsv')).read_text()
        for needle in needles:check(needle in s,'locator '+file+' '+needle)
    # Direct record checks: verify original installed headers and selected values,
    # independently of the cached JSON's counts and strings.
    with Path(definitions['source']).open('rb') as f:
        for r in outposts:
            f.seek(r['offset']);h=f.read(24)
            check(h[:4]==b'RSPJ' and struct.unpack_from('<I',h,12)[0]==r['formid'],
                  'actual RSPJ header '+hex(r['formid']))
    seed=json.loads((BASE/'baseline.json').read_text())
    check(sha(ROOT/'.git/index')==seed['index']['sha256'],'index unchanged')
    receipt=dict(count=len(checks),checks=checks,protected_after=after,
                 limits='Scoped integrity/definitions/locators; no runtime or exhaustive startup/template closure')
    with (BASE/'verification01.json').open('x',encoding='utf8',newline='\n') as f:
        json.dump(receipt,f,indent=2);f.write('\n')
    guard()
    print('PASS',len(checks),'checks; no runtime measurement')

if __name__=='__main__':
    main()
