# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate A0 full-source birth and fixed-native source-planar operands.

Reads original sealed A0 via owned D5AL baseline oracle and pinned D5AQ native
receipts; independently checks Birth sequence 2082 fixed frame/CRC and original full 0x70-byte
payload. Writes exclusive ignored receipt only. No native execution, target/save/
DB/configuration/Git/network mutation. Source-local basis is a proposed bounded
contract distinct from historical consumed-descriptor qualification and current
indexed outpost query frame; no sampled mask inference.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import csv
import hashlib
import json
import math
from pathlib import Path
import struct
import zlib
import d5al_baseline as baseline
from d5ad_baseline import ROOT,guard,sha


def require(condition,message):
    if not condition:raise ValueError(message)


def main():
    out=Path(sys.argv[1]).resolve();before=guard()
    require(out.is_relative_to(ROOT/'.local-work/d5ar') and not out.exists(),'Fresh ignored output required')
    require(not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'No reparse output')
    observation,normalized,census=baseline.baseline_observation()
    certificate=json.loads((baseline.NOTES/'receipts/checkpoint-1793680114040295400.json').read_bytes())
    events=baseline.SESSION/'events.bin';raw=events.read_bytes()
    require(hashlib.sha256(raw[:certificate['acknowledged_bytes']]).hexdigest()==certificate['raw_prefix_sha256'],'A0 acknowledged event prefix changed')
    at=(2082-1)*328;frame=raw[at:at+328]
    require(len(frame)==328,'Truncated exact A0 birth frame')
    magic,size,sequence,crc=struct.unpack_from('<4I',frame);payload=frame[16:]
    words=struct.unpack_from('<18Q',payload)
    require(magic==0x31505253 and size==312 and sequence==2082 and words[0]==2082 and words[1]==14 and zlib.crc32(payload)==crc,'A0 birth transport integrity')
    source=observation['proof']['source']
    require(words[17]==932 and words[10]==source['source_pointer'] and source['allocation']==932 and source['birth_sequence']==2082,'A0 full-source allocation join differs')
    source_bytes=payload[152:264];descriptor=source_bytes[0x38:0x64]
    semantic=descriptor[:1]+descriptor[4:]
    origin_words=[struct.unpack_from('<i',source_bytes,offset)[0] for offset in (0x10,0x14,0x20,0x24)]
    require(origin_words==[0,0,2,2],'A0 birth origin inputs differ')
    planar=[100*(origin_words[0]-origin_words[2]),100*(origin_words[1]-origin_words[3])]
    actual_frame=observation['envelope']['frame']
    require(actual_frame['basis']=='consumed-descriptor-v1' and semantic.hex()==actual_frame['descriptor_semantic'],'A0 source descriptor versus actual consumed generation descriptor differs')
    require(planar==[-200,-200],'A0 native planar origin differs')
    metadata_path=ROOT/'.local-work/d5s/geometry.json'
    metadata_pin='9594ab2aa34856bcc3b8ecb249b46b0063ef4b5d1af80d4e557542f2d6657ccf'
    require(sha(metadata_path)==metadata_pin,'Original fixed request metadata changed')
    metadata=json.loads(metadata_path.read_bytes())
    request=metadata['results'][1]['request']
    require(request['origin']==planar,'Fixed native fixture source origin differs from A0 birth')
    pins={str(path):digest for path,digest in baseline.ANCHORS.items()}
    pins[str(events)+'#acknowledged-prefix']=certificate['raw_prefix_sha256'];pins[str(metadata_path)]=sha(metadata_path)
    rows=list(csv.DictReader((ROOT/'docs/experiments/resource-retained-population/d5aq-sources.csv').open(encoding='utf8')))
    outputs=[]
    def content(population):
        return [(r['resource'],[(g['header'][:42],g['count'],g['points']) for g in r['regions']]) for r in sorted(population,key=lambda r:int(r['resource'],16))]
    actual=content(observation['envelope']['population'])
    for label in ('geometry01','geometry02'):
        path=ROOT/'.local-work/d5aq'/label/'control.json'
        expected=next(row['sha256'] for row in rows if Path(row['path']).as_posix()==path.relative_to(ROOT).as_posix())
        require(sha(path)==expected,'Pinned fixed native output changed');pins[str(path)]=expected
        value=json.loads(path.read_bytes());require(not value['errors'],'Fixed original native control failure')
        require(value['model_input_sha256']==metadata_pin,'Pinned fixed control does not authenticate request metadata')
        copied=path.parent/'geometry.json';execution=path.parent/'execution.json'
        require(sha(copied)==metadata_pin,'Fixed child copied different request metadata')
        execution_value=json.loads(execution.read_bytes())
        require(execution_value['exit']==0 and execution_value['inputs'].get(str(metadata_path))==metadata_pin,'Fixed child execution request provenance differs')
        pins[str(copied)]=metadata_pin;pins[str(execution)]=sha(execution)
        runs=[]
        for run in value['runs']:
            require(all(row['exact_points_bounds'] for row in run['planar_model_comparison']),'Independent fixed native geometry mismatch')
            regions=points=0
            for resource in run['population']:
                for region in resource['regions']:
                    header=bytes.fromhex(region['header']);point_bytes=bytes.fromhex(region['points'])
                    require(struct.unpack_from('<I',header,8)[0]==0,'Fixed native header Z is not positive zero')
                    require(len(point_bytes)==region['count']*16,'Fixed point byte completeness')
                    require(all(struct.unpack_from('<I',point_bytes,n+8)[0]==0 for n in range(0,len(point_bytes),16)),'Fixed native point Z is not positive zero')
                    require(all(math.isfinite(v) for v in struct.unpack('<'+'f'*(len(point_bytes)//4),point_bytes)),'Nonfinite fixed native point word')
                    regions+=1;points+=region['count']
            runs.append(dict(label=run['label'],regions=regions,points=points,all_header_point_z_positive_zero=True,
                represented_content_equal_to_actual_a0=content(run['population'])==actual))
        outputs.append(dict(control=label,runs=runs))
    for resource in observation['envelope']['population']:
        for region in resource['regions']:
            point_bytes=bytes.fromhex(region['points'])
            require(struct.unpack_from('<I',bytes.fromhex(region['header']),8)[0]==0 and all(struct.unpack_from('<I',point_bytes,n+8)[0]==0 for n in range(0,len(point_bytes),16)),'Actual A0 is not native planarZ0')
    require(outputs[0]['runs']==outputs[1]['runs'],'Distinct owned hosts disagree')
    result=dict(status='PASS',contract='sor-d5ar-source-planar-basis-proposal/1',review_required=True,
        a0_birth_sequence=2082,a0_allocation=932,source_origin_words_i32=origin_words,source_origin_input_hex=b''.join(source_bytes[o:o+4] for o in (0x10,0x14,0x20,0x24)).hex(),
        source_descriptor_raw44_hex=descriptor.hex(),source_descriptor_semantic41_hex=semantic.hex(),native_planar_origin_i32=planar,
        actual_consumed_generation_descriptor_matches_source=True,source=observation['envelope']['source'],a0_normalized_sha256=hashlib.sha256(normalized).hexdigest(),
        authenticated_resident_holders=len(census),fixed_outputs=outputs,inputs=pins,method_sha256=sha(__file__),
        historical_sampled_mask_inferred=False,current_indexed_outpost_frame_qualified=False,
        floors_before=before,floors_after=guard())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',a0_birth=2082,origin=planar,semantic_descriptor_match=True,review_required=True)))


if __name__=='__main__':main()
