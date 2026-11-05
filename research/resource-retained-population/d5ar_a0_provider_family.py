# SPDX-License-Identifier: GPL-3.0-or-later
"""Recover A0 provider family from exact recorder/native stack relationships.
Reads owned build16 COFF object, pinned A0 DLL, original exports and CRC events.
No target/native/DB execution. Writes one exclusive local receipt. Pointer
appearance is never used to distinguish stack/heap: the Layer equation is exact.
"""
import os,sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise RuntimeError('Pinned Python -E -B required')
import hashlib,json,struct,zlib
from pathlib import Path
from d5ad_baseline import ROOT,guard,sha
import d5al_baseline as baseline

def need(value,message):
 if not value:raise ValueError(message)

def main():
 out=Path(sys.argv[1]).resolve();before=guard()
 need(out.is_relative_to(ROOT/'.local-work/d5ar') and not out.exists() and not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Fresh ignored output')
 folder=ROOT/'.local-work/d5ai-recorder/build16';obj=folder/'plugin.obj';dll=folder/'package-runtime/SorConstructionWinner.dll';build_path=folder/'build.json';build=json.loads(build_path.read_bytes())
 need(sha(dll)==baseline.DLL==build['outputs']['SorConstructionWinner.dll'] and sha(obj)==build['outputs']['plugin.obj'],'Different actual recorder build/object')
 b=obj.read_bytes();machine,nsec,_,symbols,nsymbols,optional,_=struct.unpack_from('<HHIIIHH',b);need(machine==0x8664 and optional==0,'Ordinary AMD64 COFF required');strings=symbols+nsymbols*18;names={};chosen=None;i=0
 while i<nsymbols:
  at=symbols+i*18;name=b[at:at+8]
  if name[:4]==bytes(4):
   where=strings+struct.unpack_from('<I',name,4)[0];name=b[where:b.index(bytes(1),where)]
  else:name=name.rstrip(bytes(1))
  value,section,_,_,aux=struct.unpack_from('<IhHBB',b,at+8);names[i]=name
  if name==b'?provider_hook@winner@@YA_K_K000@Z':chosen=(value,section)
  i+=1+aux
 need(chosen is not None and chosen[0]==0,'Unique provider COMDAT absent');section_at=20+(chosen[1]-1)*40;length,offset,reloc=struct.unpack_from('<III',b,section_at+16);nreloc=struct.unpack_from('<H',b,section_at+32)[0];code=b[offset:offset+length];mask=set();calls=[]
 for i in range(nreloc):
  pos,index,kind=struct.unpack_from('<IIH',b,reloc+i*10);need(kind in (4,11) and pos+4<=length,'Unexpected provider relocation')
  mask.update(range(pos,pos+4))
  if names.get(index)==b'?provider_original@winner@@3P6A_K_K000@ZEA':calls.append(pos)
 need(calls==[0x49,0x523] and code[0x521:0x523]==bytes.fromhex('ff15'),'Enabled original-call shape changed')
 need(code[:len(bytes.fromhex('40555356574154415541564157488dac2498fbffff4881ec68050000'))]==bytes.fromhex('40555356574154415541564157488dac2498fbffff4881ec68050000'),'Provider fixed stack prologue changed')
 rsp_edits=[i for i in range(length) if code[i:i+3] in (bytes.fromhex('4881ec'),bytes.fromhex('4881c4'),bytes.fromhex('4883ec'),bytes.fromhex('4883c4'))]
 need(rsp_edits==[0x15,0x6bf],'Unexpected fixed stack adjustment pattern')
 image=dll.read_bytes();pe=struct.unpack_from('<I',image,60)[0];opt=pe+24;sections=[struct.unpack_from('<IIII',image,opt+struct.unpack_from('<H',image,pe+20)[0]+n*40+8) for n in range(struct.unpack_from('<H',image,pe+6)[0])]
 def raw(rva,n):
  for _,start,size,file in sections:
   if start<=rva and rva+n<=start+size:return image[file+rva-start:file+rva-start+n]
  raise ValueError('Missing file-backed DLL range')
 needle=code[:len(bytes.fromhex('40555356574154415541564157488dac2498fbffff4881ec68050000'))];offsets=[];position=0
 while True:
  position=image.find(needle,position)
  if position<0:break
  if position+length<=len(image) and all(image[position+j]==byte for j,byte in enumerate(code) if j not in mask):offsets.append(position)
  position+=1
 need(len(offsets)==1,'Provider object-to-DLL match is not unique');file=offsets[0];rva=next(start+file-off for _,start,size,off in sections if off<=file<off+size)
 directory,size=struct.unpack_from('<II',image,opt+112+3*8);parents=[(a,z,u) for a,z,u in struct.iter_unpack('<III',raw(directory,size)) if a==rva]
 need(len(parents)==1 and parents[0][1]-rva==length,'Actual DLL provider runtime-function range differs');unwind=raw(parents[0][2],24)
 need(unwind==bytes.fromhex('192d0a001c01ad000df00be009d007c00570046003300250'),'Actual provider unwind allocation/pushes changed')
 export=ROOT/'.local-work/d5q/export01/native.tsv';text=export.read_text(encoding='utf8')
 need('1407b5258\tLEA R8,[RSP + 0x88]' in text and '1407b526a\tCALL 0x14079f860' in text and '14079f87b\tLEA RBP,[RAX + -0x2c8]' in text,'Original Layer/provider fixed stack relation changed')
 patch=ROOT/'.local-work/d5ai-recorder/candidate-build16/runtime/construction-winner/patch.h';need(build['inputs'].get(str(patch))==sha(patch),'Actual trampoline source changed')
 need('p[0]=0xff;p[1]=0x25' in patch.read_text(encoding='utf8'),'Original preserving trampoline jump changed')
 certificate=json.loads((baseline.NOTES/'receipts/checkpoint-1793680114040295400.json').read_bytes());events=(baseline.SESSION/'events.bin').read_bytes();need(hashlib.sha256(events[:certificate['acknowledged_bytes']]).hexdigest()==certificate['raw_prefix_sha256'],'A0 acknowledged prefix changed')
 rows=[]
 for sequence,kind in [(8094,1),(8095,2)]:
  frame=events[(sequence-1)*328:sequence*328];magic,size,seq,crc=struct.unpack_from('<4I',frame);payload=frame[16:];words=struct.unpack_from('<18Q',payload)
  need(magic==0x31505253 and size==312 and seq==sequence==words[0] and words[1]==kind and zlib.crc32(payload)==crc and words[8]==words[7]==0,'Actual provider record invalid');rows.append(words)
 entry,selected=rows;need(entry[2]==selected[2]==3875 and entry[4]==selected[4] and entry[12]==selected[12],'Different provider invocation/argument')
 expected=8+(8*8+0x568)+8+0x2c8+0x88;observed=entry[12]-selected[11]
 need(expected==0x908 and observed!=expected,'Layer not excluded')
 result=dict(status='PASS_SCOPED_DENSITY_ORIGIN',invocation=3875,entry=8094,selected=8095,observed_r8_minus_native_rbp=observed,required_layer_delta=expected,
  wrapper_stack_delta=0x5a8,wrapper_provider_call_offset=0x521,provider_rva=hex(rva),provider_size=length,provider_unwind=unwind.hex(),object_relocations_masked=len(mask)//4,
  conclusion='Exact Layer stack equation is false; within the two original ordinary provider callers this actual A0 invocation entered through Density, not Layer. No pointer-appearance inference.',
  limits=['Scoped original ordinary caller graph; no arbitrary foreign callers or corrupted ABI','Density origin alone does not certify absence/presence of an ambient retained manager reader'],
  inputs={str(p.relative_to(ROOT)):sha(p) for p in (obj,dll,build_path,export,patch)},method_sha256=sha(__file__),floors_before=before,floors_after=guard())
 with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(status=result['status'],required_layer_delta=hex(expected),actual_delta=observed)))
if __name__=='__main__':main()
