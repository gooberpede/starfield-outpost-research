# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect exact original and repaired observer-owned native code offline.

Reads old/new DLLs and compiler objects and runs installed MSVC dumpbin only.
Writes fresh local disassemblies, selected symbol/instruction-location rows and
hash receipts; raw instructions stay local. No build, deployment, game, save,
database, Git or network writes. Object disassembly offsets are not DLL RVAs.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import json
from pathlib import Path
import re
import subprocess
import struct
from d5am_lock_qualify import ROOT,guard,sha

TOOL=Path('C:/Program Files/Microsoft Visual Studio/18/Community/VC/Tools/MSVC/14.51.36231/bin/Hostx64/x64/dumpbin.exe')

def require(value,message):
    if not value:raise RuntimeError(message)

def linked_code(obj,dll):
    """Match owned COFF code to the DLL while masking declared relocations.

    Returns only byte-verified mappings. Ambiguous matches remain explicit;
    COFF section offsets are never silently treated as image RVAs.
    """
    raw=obj.read_bytes();image=dll.read_bytes()
    sections=struct.unpack_from('<H',raw,2)[0];symbols,count=struct.unpack_from('<2I',raw,8)
    optional=struct.unpack_from('<H',raw,16)[0];table=20+optional
    strings=symbols+count*18
    def name_at(record):
        name=record[:8]
        if name[:4]==b'\0'*4:
            start=strings+struct.unpack_from('<I',name,4)[0];end=raw.index(b'\0',start)
            return raw[start:end].decode('utf8')
        return name.rstrip(b'\0').decode('ascii')
    wanted={};index=0
    while index<count:
        record=raw[symbols+index*18:symbols+(index+1)*18];name=name_at(record)
        section=struct.unpack_from('<h',record,12)[0]
        function=bool(struct.unpack_from('<H',record,14)[0]&0x20)
        if section>0 and function and (any(group in name for group in ('@scheduler@winner@@','@causal@winner@@','@counter@winner@@')) or name.startswith('?worker_body@winner')):
            wanted[name]=section
        index+=1+record[17]
    nt=struct.unpack_from('<I',image,0x3c)[0];pe_sections=struct.unpack_from('<H',image,nt+6)[0]
    pe_table=nt+24+struct.unpack_from('<H',image,nt+20)[0];domains=[]
    for index in range(pe_sections):
        off=pe_table+index*40;name=image[off:off+8].rstrip(b'\0')
        if name==b'.text':
            rva,size,pointer=struct.unpack_from('<3I',image,off+12);domains.append((rva,pointer,size))
    mapping={};assembly=obj.name in ('d5am-scheduler.obj','d5am-causality.obj')
    text_sections={i+1 for i in range(sections) if assembly and raw[table+i*40:table+i*40+8].rstrip(b'\0').startswith(b'.text')}
    for number in sorted(set(wanted.values())|text_sections):
        off=table+(number-1)*40;length,pointer,relocs=struct.unpack_from('<3I',raw,off+16)
        nrel=struct.unpack_from('<H',raw,off+32)[0];code=raw[pointer:pointer+length]
        if not code:continue
        spans=[]
        for i in range(nrel):
            location,unused,kind=struct.unpack_from('<IIH',raw,relocs+i*10)
            width=8 if kind==1 else 2 if kind==10 else 4 if kind in (2,3,4,5,6,7,8,9,11) else None
            require(width is not None,'Unsupported COFF code relocation')
            spans.append((location,location+width))
        segments=[];cursor=0
        for begin,end in sorted(spans):
            require(cursor<=begin<=end<=length,'Overlapping/out-of-range COFF relocation')
            if begin>cursor:segments.append((cursor,code[cursor:begin]))
            cursor=end
        if cursor<length:segments.append((cursor,code[cursor:]))
        if not segments:continue
        anchor_offset,anchor=max(segments,key=lambda row:len(row[1]));matches=[]
        if len(anchor)>=8:
            for image_rva,image_offset,image_length in domains:
                found=image.find(anchor,image_offset,image_offset+image_length)
                while found!=-1:
                    candidate=found-anchor_offset
                    if image_offset<=candidate and candidate+length<=image_offset+image_length and all(image[candidate+p:candidate+p+len(part)]==part for p,part in segments):
                        matches.append(dict(rva=hex(image_rva+candidate-image_offset),file_offset=hex(candidate)))
                    found=image.find(anchor,found+1,image_offset+image_length)
        keys=[name for name,section in wanted.items() if section==number]
        if number in text_sections:keys.append('.text')
        for name in keys:mapping[name]=dict(section=number,bytes=length,relocations=nrel,matches=matches,
            status='UNIQUE_BYTE_VERIFIED' if len(matches)==1 else 'AMBIGUOUS_OR_UNMAPPED')
    return mapping

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('build',type=Path);parser.add_argument('out',type=Path)
    args=parser.parse_args();build=args.build.resolve();out=args.out.resolve()
    require(build.is_relative_to(ROOT/'.local-work/d5ao') and out.is_relative_to(ROOT/'.local-work/d5ao'),'D5AN local paths required')
    free=guard();out.mkdir(exist_ok=False)
    pins={str(TOOL):sha(TOOL),str(Path(__file__)):sha(__file__)};rows=[];products={};code_maps={}
    for label,folder in [('original',ROOT/'.local-work/d5am/guard-final02'),('candidate',build)]:
        receipt=json.loads((folder/'build.json').read_bytes())
        require(receipt['compilation']==0 and sha(folder/'SorConstructionWinner.dll')==receipt['dll_sha256'],'Binary receipt mismatch')
        pins[str(folder/'build.json')]=sha(folder/'build.json')
        code_maps[label]={name:linked_code(folder/name,folder/'SorConstructionWinner.dll') for name in ('d5am-scheduler.obj','d5am-causality.obj','transport.obj','fixture.obj','plugin.obj')}
        for name in ('d5am-scheduler.obj','d5am-causality.obj','transport.obj','fixture.obj','plugin.obj','SorConstructionWinner.dll'):
            source=folder/name;pins[str(source)]=sha(source)
            mode='/disasm';command=[str(TOOL),'/nologo',mode,str(source)]
            run=subprocess.run(command,capture_output=True);require(run.returncode==0,'Disassembler failed: '+name)
            raw=out/(label+'-'+name+'.disasm.txt');raw.write_bytes(run.stdout+run.stderr)
            products[raw.name]=sha(raw)
            symbol='UNKNOWN';lines=run.stdout.decode('utf8',errors='replace').splitlines()
            for number,line in enumerate(lines,1):
                if line and not line[0].isspace() and line.endswith(':'):symbol=line[:-1]
                selected=any(marker in line for marker in ('D5AM_sched_counter_faults','D5AM_causal_counter_faults',
                    'D5AN_counter_next','D5AN_counter_leave','?failed@causal@winner','?failed@scheduler@winner',
                    '?counter_overflow@causal@winner','?broken@winner'))
                if selected:
                    match=re.match(r'\s*([0-9A-F]+):',line)
                    rows.append(dict(build=label,object=name,symbol=symbol,
                        location='0x'+match.group(1) if match else None,
                        domain='disassembler preferred VA' if name.endswith('.dll') else 'COFF section-relative instruction offset within named symbol block',
                        line=number,text=line.strip(),raw=raw.name))
        for mode,suffix in [('/exports','exports'),('/headers','headers')]:
            run=subprocess.run([str(TOOL),'/nologo',mode,str(folder/'SorConstructionWinner.dll')],capture_output=True)
            require(run.returncode==0,'DLL metadata read failed');p=out/(label+'-'+suffix+'.txt');p.write_bytes(run.stdout+run.stderr);products[p.name]=sha(p)
    require(any(r['build']=='original' and 'D5AM_sched_counter_faults' in r['text'] for r in rows),'No original sticky producer reference found')
    require(any(r['build']=='candidate' and 'D5AN_counter_next' in r['text'] for r in rows),'No repaired common helper call found')
    for row in rows:
        if row['location'] is None or row['object'].endswith('.dll'):continue
        key='.text' if row['object'] in ('d5am-scheduler.obj','d5am-causality.obj') else row['symbol'].split(' (',1)[0]
        mapping=code_maps[row['build']][row['object']].get(key)
        if mapping and mapping['status']=='UNIQUE_BYTE_VERIFIED':
            row['linked_rva']=hex(int(mapping['matches'][0]['rva'],16)+int(row['location'],16))
            row['linked_domain']='Corresponding owned DLL RVA; non-relocation code bytes matched uniquely'
    require(all(sha(p)==h for p,h in pins.items()),'Inspected input drift')
    value=dict(schema='sor-d5an-native-census/1',status='PASS_INSPECTION',inputs=pins,products=products,locations=rows,code_maps=code_maps,
        initial_free=free,final_free=guard(),limits='Selected native instruction references do not prove exhaustive semantic attribution alone. Combine with full disassemblies, source call graph, exact export/map domains and independent review. No game instructions are published.')
    with (out/'census.json').open('x',encoding='utf8',newline='\n') as stream:json.dump(value,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(status=value['status'],locations=len(rows),products=len(products))))

if __name__=='__main__':main()
