# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only independent joins/checks over P1 receipt, E2 PNDT cache and source CSV.
Writes only exclusive ignored JSON. Stdlib; no source-script/tool/game execution.
Source-informed comparison under SOR-P-0002; exporter itself is not ported.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import subrecords


def pin(p):
    with p.open('rb') as f:return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.file_digest(f,'sha256').hexdigest())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--run',required=True);args=ap.parse_args()
    assert args.run.isalnum()
    inp=Path(args.input);j=json.loads(inp.read_text());old=json.loads(Path(j['cache']['path']).read_text());rs=old['records']
    by={r['formid']:r for r in rs};candidate={r['formid']:r for r in j['candidates']}
    def field(r,k):return next((bytes.fromhex(v) for t,v in r['fields'] if t==k),b'')
    rows=[];stats=collections.Counter()
    with Path(j['sources'][1]['path']).open(encoding='utf-8-sig',newline='') as f:src=list(csv.DictReader(f))
    mainrows=[r for r in src if r['SourceFile']=='Starfield.esm']
    source=Path(j['source']['path']);assert pin(source)==j['source']
    with source.open('rb') as f:
        for r in mainrows:
            p=by[int(r['PlanetFormID'],16)];f.seek(p['offset']);h=f.read(24)
            n,flags,fid=struct.unpack_from('<III',h,4)
            assert h[:4]==b'PNDT' and fid==p['formid'] and flags==p['flags']
            b=f.read(n)
            if flags&0x40000:
                size=struct.unpack_from('<I',b)[0];d=zlib.decompressobj();b=d.decompress(b[4:],size+1)
                assert len(b)==size and d.eof and not d.unused_data and not d.unconsumed_tail
            assert [[k.decode(),v.hex()] for k,v in subrecords(b)]==p['fields']
    for r in mainrows:
        fid=int(r['PlanetFormID'],16)
        if fid not in by:stats['csv_unjoined']+=1;continue
        p=by[fid];assert p['type']=='PNDT' and p['edid']==r['PlanetEditorID']
        kws={i[0] for i in struct.iter_unpack('<I',field(p,'KWDA'))}
        if 0xb04f3 in kws:
            assert not r['SolarArrayPower'] and not r['WindTurbinePower'];stats['nonlandable_blank']+=1;continue
        for fl,col in [('002031dc','SolarArrayPower'),('002031da','WindTurbinePower')]:
            possible={x['rating'] for x in j['environment'] if x['list_formid']==fl and int(x['keyword'].split(':')[0],16) in kws}
            if col=='WindTurbinePower' and 0x295eaa in kws:
                assert r[col]=='0';stats['wind_no_atmosphere_zero']+=1;continue
            if len(possible)==1:
                v=next(iter(possible));assert float(r[col])==v
                stats[col+'_agree']+=1
            else:rows.append(dict(formid=r['PlanetFormID'],column=col,values=sorted(possible),source_value=r[col],body_type=r['BodyType']))
    expected={'00030238':2,'002031e2':4,'002031e1':6,'002031e0':8,'0003023a':4,'002031df':8,'002031de':12,'002031dd':16,
        '0003023c':3,'002031e4':6,'002031e3':10,'001c5149':6,'001c5148':14,'001c5147':25,'00007f7b':30,'001c514b':100,'002b063a':20}
    assert all(candidate[k]['properties']['0000032e']==v for k,v in expected.items())
    assert len(j['fuel'])==1 and j['fuel'][0]['seconds']==36 and j['fuel'][0]['inputs'][0]['resource']['formid']=='000057f5'
    assert j['fuel'][0]['inputs'][0]['quantity']==1 and j['fuel'][0]['output']==0
    assert all(r['body_type']=='Orbital' and r['source_value']=='' and r['values']==[] for r in rows)
    assert pin(source)==j['source']
    counts=collections.Counter(r['type'] for r in j['candidates'])
    result=dict(tool=pin(Path(__file__)),input=pin(inp),python=sys.version,source_csv=pin(Path(j['sources'][1]['path'])),
        csv_total=len(src),main_csv_rows=len(mainrows),physical_pndt_checked=len(mainrows),stats=stats,unresolved=rows,generator_assertions=len(expected),candidate_types=counts,
        limits=['CSV-vs-definition agreement does not prove runtime output or FLST evaluator precedence','Main ESM source rows only; other source files excluded'])
    out=ROOT/'.local-work/p1-power'/f'{args.run}.json'
    with out.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(main_csv_rows=len(mainrows),stats=stats,orbital_blank_fields=len(rows),generator_assertions=len(expected),candidate_types=counts)))


if __name__=='__main__':main()
