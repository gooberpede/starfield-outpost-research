# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit preserved A0 actual generation operands against fixed C1 requirements.
Reads sealed baseline anchors/raw frames and exact recorder-build source pins;
writes one exclusive ignored receipt. No native execution/target/DB/network/Git
mutation. This deliberately does not infer missing inputs from matching output.
"""
import os,sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise RuntimeError('Pinned Python -E -B required')
import hashlib,json,struct,zlib
from pathlib import Path
import d5al_baseline as baseline
from d5ad_baseline import ROOT,guard,sha

def require(value,message):
    if not value:raise ValueError(message)

def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    require(out.is_relative_to(ROOT/'.local-work/d5ar') and not out.exists() and not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Fresh ignored output required')
    for path,pin in baseline.ANCHORS.items():require(sha(path)==pin,'A0 anchor changed')
    certificate=json.loads((baseline.NOTES/'receipts/checkpoint-1793680114040295400.json').read_bytes());events=(baseline.SESSION/'events.bin').read_bytes()
    require(hashlib.sha256(events[:certificate['acknowledged_bytes']]).hexdigest()==certificate['raw_prefix_sha256'],'A0 acknowledged raw prefix changed')
    frames={}
    for sequence,kind in [(2082,14),(8099,6),(8100,7)]:
        frame=events[(sequence-1)*328:sequence*328];magic,size,seq,crc=struct.unpack_from('<4I',frame);payload=frame[16:];words=struct.unpack_from('<18Q',payload)
        require(magic==0x31505253 and size==312 and seq==sequence==words[0] and kind==words[1] and zlib.crc32(payload)==crc,'Actual frame transport changed')
        require(words[8]==0 and words[7]==0,'Unqualified actual event');frames[sequence]=(words,payload)
    birth,raw_birth=frames[2082];generation,raw_generation=frames[8099];sample,raw_sample=frames[8100]
    require(birth[10]==generation[10]==sample[10] and birth[17]==932 and generation[2]==sample[2] and generation[17]==sample[17] and sample[13]==3,'Actual A0 source/generation/sample join differs')
    source=raw_birth[152:264]
    build_path=ROOT/'.local-work/d5ai-recorder/build16/build.json';build=json.loads(build_path.read_bytes())
    require(build['outputs']['SorConstructionWinner.dll']==baseline.DLL,'Different actual recorder build')
    recorder_pins={}
    for name in ['observer.h','d5ai_geometry.h','build.py']:
        path=ROOT/'.local-work/d5ai-recorder/candidate-build16/runtime/construction-winner'/name
        require(build['inputs'].get(str(path))==sha(path),'Actual recorder source pin changed');recorder_pins[str(path)]=sha(path)
    # Actual build records origin as a native argument but deliberately does not
    # persist its contents in Generating. No historical dimension/settings copy.
    observer=(ROOT/'.local-work/d5ai-recorder/candidate-build16/runtime/construction-winner/observer.h').read_text()
    require('e.a=owner;e.b=biome;e.c=geographic;e.d=out;' in observer,'Generating operand layout changed')
    fixed=ROOT/'.local-work/d5s/geometry.json';require(sha(fixed)=='9594ab2aa34856bcc3b8ecb249b46b0063ef4b5d1af80d4e557542f2d6657ccf','Fixed metadata changed')
    inputs=json.loads(fixed.read_bytes());request=inputs['results'][1]['request']
    result=dict(status='INPUT_EQUIVALENCE_NOT_ESTABLISHED',a0_birth=2082,allocation=932,generation=8099,sample=8100,actual_sample_mask=3,
        source_prefix70_hex=source.hex(),source_words={hex(o):struct.unpack_from('<I',source,o)[0] for o in range(0,112,4)},
        birth_dimension_words=[struct.unpack_from('<i',source,o)[0] for o in (0x18,0x1c)],
        source_origin_words=[struct.unpack_from('<i',source,o)[0] for o in (0x10,0x14,0x20,0x24)],
        generation_record=dict(owner=generation[13],biome_pointer=generation[14],geographic_pointer=generation[15],output_pointer=generation[16],request=list(struct.unpack_from('<2i',raw_generation,144)),source_bytes_all_zero=not any(raw_generation[152:264])),
        recovered=dict(planar_origin=[-200,-200],body=generation[13],source_birth_descriptor44=source[0x38:0x64].hex()),
        not_recovered=['Post-birth final dimensions consumed at generation','Current-at-generation stitch setting 0x145ea6770 and derived clip/cell bounds','Selected effective DNAM blocks and resource order','Per-cell packed keys from manager descriptor at each key conversion','Inactive rarity payloads for counterfactual masks','Effective Special/Everywhere eligibility and operands'],
        fixed_contract=dict(origin=request['origin'],clip_center=request['clip_center'],clip_half=request['clip_half'],cell_bounds=request['cell_bounds'],owner=request['owner_key'],resources=[r['resource'] for r in request['ordered_resources']]),
        retained_context='Generator local context and temporary dictionaries are stack/transient; holder retains resource/region/point outputs, not a historical effective-input receipt',
        interpretation='Coordinate/source representation equivalence and exact content equality do not establish full non-mask generation-input equality; no shape inversion used',
        inputs={str(path):pin for path,pin in baseline.ANCHORS.items()},recorder_sources=recorder_pins,build_receipt_sha256=sha(build_path),raw_acknowledged_prefix_sha256=certificate['raw_prefix_sha256'],fixed_metadata_sha256=sha(fixed),method_sha256=sha(__file__),floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],actual_mask=3,birth_dimensions=result['birth_dimension_words'])))
if __name__=='__main__':main()
