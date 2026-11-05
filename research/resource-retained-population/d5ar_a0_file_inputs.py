# SPDX-License-Identifier: GPL-3.0-or-later
"""Read all 39 A0-pinned definition files for relevant GMST/ordinary overrides.
Uses owned bounded ESM reader (SOR-P-0002). Authenticates A0 archive and original
preflight/postflight pins, reads files/config only, writes fresh ignored receipt.
Does not promote on-disk file inventory into runtime load/VM/GMST ordering.
"""
import os,sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise RuntimeError('Pinned Python -E -B required')
import hashlib,json,struct,zipfile
from pathlib import Path
from d5ad_baseline import ROOT,guard,sha
import d5al_baseline as baseline
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records

def need(condition,message):
    if not condition:raise ValueError(message)

def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    need(out.is_relative_to(ROOT/'.local-work/d5ar') and not out.exists() and not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Fresh ignored output required')
    archive=baseline.ARCHIVE/'episode-a.zip';need(sha(archive)==baseline.ANCHORS[archive],'A0 archive changed')
    with zipfile.ZipFile(archive) as zipped:
        pre=json.loads(zipped.read('notes/preflight01/receipt.json'))['protection'];post=json.loads(zipped.read('notes/postflight01/receipt.json'))
    need(post['status']=='PASS_POSTFLIGHT' and not post['protection_errors'] and any(row['equal'] and {'definitions','config'}<=set(row['fields']) for row in post['protection_comparisons']),'A0 definitions/config postflight comparison not qualified')
    rows=[];pins={};target={0x57d4,0x57d0,0x57cf,0x145440,0x258050,0x5e0de,0x29d20e,0x23ddf3,0x168814};walked={}
    for name,pin in pre['definitions'].items():
        path=Path(name);need(sha(path)==pin,'A0 definition file changed: '+name);pins[name]=pin;masters=[];counts={}
        for header,fields in esm_records(path,{b'TES4',b'GMST',b'IRES',b'RSGD',b'BIOM',b'PNDT',b'SFPT',b'SFTR',b'SFBK'},repeated=True):
            counts[header['type']]=counts.get(header['type'],0)+1
            if header['type']=='TES4':masters=[v.rstrip(b'\0').decode('utf8') for k,v in fields if k==b'MAST'];continue
            edid=next((v.rstrip(b'\0').decode('utf8') for k,v in fields if k==b'EDID'),'')
            fid=header['formid'];index=fid>>24;master=masters[index] if index<len(masters) else path.name if index==len(masters) else 'UNRESOLVED'
            named=header['type']=='GMST' and ('InactiveResourceChanceMult' in edid or edid in ('uResourceCellGridSize','uResourceCellGridStitch','iResourceCellGridSize','iResourceCellGridStitch'))
            if named or master.lower()=='starfield.esm' and fid&0xffffff in target:
                rows.append(dict(file=name,master=master,header=header,editor_id=edid,record_sha256=hashlib.sha256(b''.join(k+struct.pack('<I',len(v))+v for k,v in fields)).hexdigest(),gmst_data=[v.hex() for k,v in fields if k==b'DATA'] if header['type']=='GMST' else None,subrecord_signatures=[k.decode('ascii') for k,v in fields]))
        need(sha(path)==pin,'Definition changed during audit');walked[name]=dict(masters=masters,records=counts)
    configs={}
    for name,pin in pre['config'].items():
        path=Path(name);need(sha(path)==pin,'A0 configuration file changed');pins[name]=pin
        if path.name.lower() in ('plugins.txt','starfieldcustom.ini','loadorder.txt'):
            configs[name]=path.read_text(encoding='utf-8-sig')
    result=dict(status='PASS_FILE_INPUT_AUDIT',definition_files=len(walked),config_files=len(pre['config']),records=rows,walked=walked,selected_config_text=configs,
        limits=['No runtime loaded-plugin/override state certified','No GMST initialization-completion or dynamic-write history certified','Selected known C1 FormIDs, not universal effective-input merger'],
        inputs=pins,archive_sha256=sha(archive),reader_sha256=sha(ROOT/'save-analysis/scripts/inspect_outpost_definitions.py'),method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],definition_files=len(walked),selected_records=len(rows))))
if __name__=='__main__':main()
