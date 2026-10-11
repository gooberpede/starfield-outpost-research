"""SPDX-License-Identifier: GPL-3.0-or-later
Offline inspector. Reads journal/raw sections; writes only explicit --output.
Validates hashes, extents and pairing without granting frame/identity semantics.
Incomplete final journal lines are recoverable; corrupt completed raw is fatal.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

def inspect(root):
    root=Path(root);data=(root/'records.jsonl').read_bytes();truncated=bool(data and not data.endswith(b'\n'))
    lines=data.splitlines();lines=lines[:-1] if truncated else lines
    rows=[json.loads(line) for line in lines];raw={};sections=0
    for row in rows:
        if row.get('kind')!='raw':continue
        name=row['file']
        if Path(name).name!=name:raise ValueError('unsafe raw path')
        b=(root/name).read_bytes();sections+=1
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('raw integrity')
        raw[row['root']]=b
    boundaries=[r for r in rows if r['kind']=='boundary'];entered={};paired=set();grid=[];centers=[];axes={}
    def identity(label):
        ref=raw.get(label+'.reference');base=raw.get(label+'.reference.base');extra=raw.get(label+'.reference.extra.workshop')
        result={'status':'PARTIAL','workshop_identifier_hex':None}
        if ref and len(ref)>=0xd0:
            result.update(formid=struct.unpack_from('<I',ref,0x28)[0],cell_pointer=hex(struct.unpack_from('<Q',ref,0xb0)[0]),reference_xyz_hex=ref[0x8c:0x98].hex())
        if base and len(base)>=0x30:result['base_formid']=struct.unpack_from('<I',base,0x28)[0]
        if extra and len(extra)>=0xa0 and extra[0x12]==0xbc:
            result.update(workshop_identifier_hex=extra[0x98:0xa0].hex(),compensation_hex=extra[0x60:0x6c].hex(),status='CAPTURED_SEMANTICS_REVIEW_REQUIRED')
        return result
    for row in boundaries:
        key=(row['thread'],row['invocation']);site=row['site']
        if site.endswith('_entry'):
            if key in entered or not key[1]:raise ValueError('duplicate invocation')
            entered[key]=row
        if row['pairing']=='paired':
            if key not in entered or key in paired:raise ValueError('invalid exit pair')
            paired.add(key)
            if site=='center_exit':
                label=row['label'];b=raw.get(label+'.native_center')
                entry_id=identity(entered[key]['label']);exit_id=identity(label)
                centers.append({'invocation':key[1],'thread':key[0],'parent':row['parent'],'center_hex':b.hex() if b else None,'entry_identity':entry_id,'exit_identity':exit_id,'identity_fields_equal':entry_id==exit_id,'frame_status':'UNASSESSED'})
        if site in ('grid_x','grid_y'):
            label=row['label'];axis=site[-1];value=raw.get(label+'.translated_axis');scale=raw.get(label+'.scale')
            axes.setdefault(key,{})[axis]={'native_translated_hex':value.hex() if value else None,'scale_hex':scale.hex() if scale else None,'pairing':row['pairing']}
        if site=='grid_result':
            label=row['label'];c=raw.get(label+'.center_local',raw.get(label+'.translated'));f=raw.get(label+'.floor');h=raw.get(label+'.hierarchy')
            land=raw.get(label+'.landscape');translation=raw.get(label+'.translation');source=raw.get(label+'.source')
            grid.append({'invocation':key[1],'thread':key[0],'pairing':row['pairing'],'center_hex':c.hex() if c else None,'center_is_pretranslation':True,'axes':axes.get(key,{}),'floor':list(struct.unpack('<2i',f)) if f else None,'hierarchy_hex':h.hex() if h else None,'body':struct.unpack_from('<I',land,0x54)[0] if land else None,'resolution':struct.unpack_from('<I',land,0x50)[0] if land else None,'translation_hex':translation.hex() if translation else None,'source_hierarchy_hex':source.hex() if source else None,'identity':identity(label),'frame_status':'UNASSESSED'})
    return {'rows':rows,'boundaries':boundaries,'centers':centers,'grid_results':grid,'raw_sections':sections,'unpaired':len(entered.keys()-paired),'journal_truncated_final_line':truncated,'scientific_equivalence':'UNASSESSED','live_game_qualification':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    result=inspect(a.root)
    with a.output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
