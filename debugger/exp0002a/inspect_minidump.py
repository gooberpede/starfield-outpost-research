# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline bounded AMD64 minidump extraction, standard library only.
Reads explicit dump and pinned PE; creates a new JSON derivative, never writes
inputs or uses process/debug-control APIs. Structure offsets are independently
encoded from installed Windows SDK minidumpapiset.h / winnt.h format declarations;
no SDK implementation or header is incorporated. Not a general dump validator.
Every extracted context/memory item records its dump file offset. UNAVAILABLE
means missing/not-valid in the dump; PE bytes are separately labelled fallback.
"""
import argparse,hashlib,json,struct
from pathlib import Path
from datetime import datetime,timezone
def sha(b):return hashlib.sha256(b).hexdigest()
def inspect(dump,image):
 b=dump.read_bytes();pe=image.read_bytes()
 def unpack(fmt,offset):
  assert 0<=offset<=len(b)-struct.calcsize(fmt)
  return struct.unpack_from(fmt,b,offset)
 assert b[:4]==b'MDMP'
 count,directory=unpack('<II',8);assert count<=128
 streams={}
 for i in range(count):
  kind,size,offset=unpack('<III',directory+12*i);assert offset+size<=len(b);streams[kind]=(offset,size)
 assert unpack('<H',streams[7][0])[0]==9, 'AMD64 dump required'
 def context(offset,size):
  assert size>=256
  flags=unpack('<I',offset+48)[0]
  assert flags&0x100000, 'AMD64 context required'
  definitions={'eflags':(68,'<I',1),'dr0':(72,'<Q',16),'dr1':(80,'<Q',16),'dr2':(88,'<Q',16),'dr3':(96,'<Q',16),'dr6':(104,'<Q',16),'dr7':(112,'<Q',16),'rax':(120,'<Q',2),'rcx':(128,'<Q',2),'rdx':(136,'<Q',2),'rsp':(152,'<Q',1),'rbp':(160,'<Q',2),'r8':(184,'<Q',2),'r9':(192,'<Q',2),'rip':(248,'<Q',1)}
  return {'file_offset':offset,'size':size,'context_flags':hex(flags),'registers':{n:{'value':hex(unpack(fmt,offset+at)[0]) if flags&required else 'UNAVAILABLE','stored_raw':hex(unpack(fmt,offset+at)[0]),'file_offset':offset+at,'context_group_present':bool(flags&required)} for n,(at,fmt,required) in definitions.items()}}
 e,esize=streams[6];assert esize>=168
 tid=unpack('<I',e)[0];code,flags,record,address,nparams=unpack('<IIQQI',e+8);assert nparams<=15
 size,offset=unpack('<II',e+160);ctx=context(offset,size)
 def value(name):return int(ctx['registers'][name]['value'],0)
 modules=[]
 mo,ms=streams[4];n=unpack('<I',mo)[0];assert 4+108*n<=ms
 for i in range(n):
  at=mo+4+108*i;base,sz,checksum,stamp,name=unpack('<QIIII',at)
  length=unpack('<I',name)[0];assert length<32768
  path=b[name+4:name+4+length].decode('utf-16-le')
  modules.append({'path':path,'base':hex(base),'size':sz,'checksum':hex(checksum),'timestamp':stamp,'file_offset':at})
 game=next(x for x in modules if Path(x['path']).name.lower()=='starfield.exe');base=int(game['base'],0)
 threads=[];to,ts=streams[3];n=unpack('<I',to)[0];assert n<=4096 and 4+48*n<=ts
 for i in range(n):
  at=to+4+48*i;t,suspend=unpack('<II',at);cs,co=unpack('<II',at+40)
  threads.append({'tid':t,'suspend_count_stored':suspend,'record_offset':at,'context':context(co,cs) if t==tid else {'file_offset':co,'size':cs}})
 ranges=[]
 if 5 in streams:
  at,sz=streams[5];n=unpack('<I',at)[0];assert 4+16*n<=sz
  for i in range(n):
   va,length,fo=unpack('<QII',at+4+16*i);ranges.append((va,length,fo))
 if 9 in streams:
  at,sz=streams[9];n,fo=unpack('<QQ',at);assert 16+16*n<=sz
  for i in range(n):
   va,length=unpack('<QQ',at+16+16*i);ranges.append((va,length,fo));fo+=length
 def memory(va,length):
  for start,size,fo in ranges:
   if start<=va and va+length<=start+size:
    offset=fo+va-start;assert offset+length<=len(b)
    return {'va':hex(va),'file_offset':offset,'size':length,'hex':b[offset:offset+length].hex(),'sha256':sha(b[offset:offset+length])}
  return 'UNAVAILABLE'
 header=struct.unpack_from('<I',pe,0x3c)[0];optional=header+24
 imagebase=struct.unpack_from('<Q',pe,optional+24)[0]
 section_count=struct.unpack_from('<H',pe,header+6)[0];section_start=optional+struct.unpack_from('<H',pe,header+20)[0]
 rva=value('rip')-base;fileoffset=None
 for i in range(section_count):
  vs,rs,rawsize,raw=struct.unpack_from('<IIII',pe,section_start+40*i+8)
  if rs<=rva and rva+32<=rs+min(vs,rawsize):fileoffset=raw+rva-rs
 assert fileoffset is not None
 exception={'file_offset':e,'tid':tid,'code':hex(code),'flags':hex(flags),'record':hex(record),'address':hex(address),'parameter_count':nparams,'parameters':[hex(unpack('<Q',e+40+i*8)[0]) for i in range(nparams)],'context':ctx}
 flags_value=value('eflags')
 misc='UNAVAILABLE'
 if 15 in streams:
  at,sz=streams[15];mf=unpack('<I',at+4)[0];misc={'file_offset':at,'flags':hex(mf),'process_id':unpack('<I',at+8)[0] if mf&1 else 'UNAVAILABLE'}
 return {'dump':str(dump),'dump_sha256':sha(b),'header_timestamp_utc':datetime.fromtimestamp(unpack('<I',20)[0],timezone.utc).isoformat(),'header_flags':hex(unpack('<Q',24)[0]),'streams':{str(k):{'file_offset':v[0],'size':v[1]} for k,v in streams.items()},'misc':misc,'exception':exception,'faulting_thread_record':next(x for x in threads if x['tid']==tid),'module':game,'faulting_rva':hex(rva),'request_entry':{'runtime':hex(base+0x183c590),'rip_equals':value('rip')==base+0x183c590,'rip_delta':rva-0x183c590,'dr0_equals':value('dr0')==base+0x183c590,'dr6_b0':bool(value('dr6')&1),'tf':bool(flags_value&0x100),'rf':bool(flags_value&0x10000)},'dump_code_window':memory(value('rip'),32),'dump_stack_96':memory(value('rsp'),96),'dump_manager_50':memory(value('rcx')+0x50,4),'dump_manager_8c':memory(value('rcx')+0x8c,1),'pinned_pe':{'path':str(image),'sha256':sha(pe),'image_base':hex(imagebase),'static_address':hex(imagebase+rva),'file_offset':fileoffset,'code_hex':pe[fileoffset:fileoffset+32].hex(),'code_sha256':sha(pe[fileoffset:fileoffset+32])}}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--dump',type=Path,required=True);p.add_argument('--image',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 assert a.output.resolve().is_relative_to(Path(__file__).resolve().parents[2]/'.local-work/exp0002a-dump-comparison')
 result=inspect(a.dump,a.image)
 with a.output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
 print(json.dumps({k:result[k] for k in ['exception','faulting_rva','request_entry','dump_code_window','dump_manager_50','dump_manager_8c']},indent=2))
