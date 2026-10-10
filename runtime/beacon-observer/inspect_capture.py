# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline hash-verified capture inventory; no process/game/save access.

Reads one snapshot journal and its raw sections, writes new JSON only under the
chosen output path. Reports packed origins and float bits; never labels a site
anchor or a speculative fractional projection an exact beacon coordinate.
Stdlib only. Truncated final JSON line is recoverable; earlier malformed lines
and any referenced raw mismatch are integrity errors.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

def inspect(path):
    content=(path/'records.jsonl').read_bytes()
    lines=content.splitlines(keepends=True)
    rows=[];truncated=False
    for i,line in enumerate(lines):
        if not line.endswith(b'\n') and i==len(lines)-1:
            truncated=True;break
        rows.append(json.loads(line))
    raw={}
    for row in rows:
        if row.get('kind')!='raw':continue
        name=row['file']
        if Path(name).name!=name or not name.startswith('raw-') or not name.endswith('.bin'):
            raise ValueError('Unsafe section path')
        data=(path/name).read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise ValueError('Raw integrity mismatch: '+name)
        raw.setdefault(row['root'],[]).append((row,data))
    def one(root):
        values=raw.get(root,[])
        return values[0][1] if len(values)==1 else None
    result={'journal_truncated_final_line':truncated,'rows':len(rows),
            'raw_sections':sum(map(len,raw.values())),
            'references':[r for r in rows if r.get('kind')=='reference'],
            'status':[r for r in rows if r.get('kind')=='status'],
            'interpretation':'RAW_RUNTIME_CANDIDATES_NOT_EXACT_PLANETARY_COORDINATES'}
    terrain=one('terrain')
    if terrain:
        origins={}
        for offset in (0xc8,0x1c0):
            origins[hex(offset)]={'tag':terrain[offset],
                'coarse_xy':struct.unpack_from('<2i',terrain,offset+4),
                'sub_xy':struct.unpack_from('<2i',terrain,offset+0x14),
                'fine_xy':struct.unpack_from('<2i',terrain,offset+0x24),
                'bytes':terrain[offset:offset+0x2c].hex()}
        result['terrain']={'mode':terrain[0x20],
            'selected_origin_offset':hex(0x1c0 if terrain[0x20]==3 else 0xc8),
            'body_candidate_formid':f'{struct.unpack_from("<I",terrain,0x80)[0]:08X}',
            'origins':origins}
    grid=one('terrain.grid');block=one('stitch.block');merge=one('stitch.merge')
    output_brackets={}
    for phase in ('before','after'):
        blob=one('terrain.workshop_output.'+phase)
        if blob and len(blob)>=0x100:
            output_brackets[phase]={'center_float32_hex':blob[0x90:0x9c].hex(),
                'radius_float32_hex':blob[0x9c:0xa0].hex(),
                'flags_e8_e9_ea':list(blob[0xe8:0xeb]),
                'status':'NATIVE_STORED_RESULT_FRESHNESS_AND_WORKSHOP_ID_UNASSESSED'}
    if output_brackets:
        result['native_workshop_output']=output_brackets
        result['native_workshop_output']['equal_bracket_values']=(len(output_brackets)==2 and
            output_brackets['before']==output_brackets['after'])
    if grid and block and merge:
        r=struct.unpack_from('<I',grid,0x50)[0]
        b=struct.unpack('<I',block)[0]+struct.unpack('<I',merge)[0]
        result['grid']={'resolution':r,'block_plus_merge':b,'candidate_axis_steps':16*b*r}
    for ref in result['references']:
        data=one(ref['root'])
        if data:
            ref['xyz_float32_hex']=data[0x8c:0x98].hex()
            ref['rotation_float32_hex']=data[0x80:0x8c].hex()
    marker=path/'complete.json'
    result['marker']=json.loads(marker.read_text()) if marker.exists() else None
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('snapshot',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();data=inspect(a.snapshot)
    with a.output.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(data,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'output':str(a.output),'raw_sections':data['raw_sections'],'rows':data['rows']}))
if __name__=='__main__':main()
