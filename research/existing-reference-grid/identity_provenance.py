"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline fallback identity probe. Reads installed ESMs, protected saves,
archived input-pin receipts and project reader modules. Uses CPython stdlib only.
Writes exclusively to a NEW ignored .local-work directory; never alters inputs.
ESM/save identities checked before/after; both-drive40GB guard before work.
Scope: complete ESM header census/exact7145 record definitions; qualified saved
R3/reference-array/queued tokens and untyped numeric matches; exact static record
definition follow-through. No live process, analysis database or network access.
Native/source provenance: SOR-S-0128 installed content, existing project readers
at save-analysis/scripts. Run from repository root with --out .local-work/NEW.
"""
import sys, json, hashlib, struct, shutil, zlib, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import identity
from stream_save import decoded_save
from validate_mature_outposts import directory
from outpost_record_framing import iter_records
from outpost_membership import token_value, initial_prefix
from extractor_resources import plugin_tables
def queued_static_ids(saved):
    """Use resolved saved FormIDs; inline and array tokens are equally eligible."""
    return {int(row['saved_record_formid'], 16) for save in saved
            for row in save['queue_leads']
            if int(row['saved_record_formid'], 16) >> 24 == 0}


def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--out',type=Path,required=True,help='New output directory under repository .local-work')
 args=ap.parse_args()
 OUT=args.out.resolve()
 if not OUT.is_relative_to(ROOT/'.local-work'):raise ValueError('OUTPUT_MUST_BE_IGNORED_LOCAL_WORK')
 for drive in ('C:/','D:/'): assert shutil.disk_usage(drive).free>=40000000000
 OUT.mkdir(parents=True,exist_ok=False)
 with (OUT/'probe-source.json').open('x',encoding='utf8') as f:
  json.dump(dict(script=identity(Path(__file__)),python=identity(Path(sys.executable)),python_version=sys.version,readers={n:identity(ROOT/'save-analysis/scripts'/n) for n in ('inspect_outpost_definitions.py','inventory_historical_saves.py','stream_save.py','validate_mature_outposts.py','outpost_record_framing.py','outpost_membership.py','extractor_resources.py')}),f,indent=2);f.write('\n')
 data=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data')
 esm=[]
 for p in sorted(data.glob('*.esm')):
  before=identity(p);hits=[];nrec=0;total=p.stat().st_size
  with p.open('rb') as f:
   pos=0;stack=[total]
   while pos<total:
    while pos==stack[-1] and len(stack)>1:stack.pop()
    f.seek(pos);h=f.read(24);tag=h[:4];n,flags,fid=struct.unpack_from('<III',h,4)
    end=pos+(n if tag==b'GRUP' else 24+n)
    assert pos+24<=end<=stack[-1]
    if tag==b'GRUP':stack.append(end);pos+=24;continue
    nrec+=1
    if fid==0x7145:
     assert n<=16*1024*1024
     b=f.read(n)
     if flags&0x40000:
      size=struct.unpack_from('<I',b)[0];assert size<=16*1024*1024
      decoder=zlib.decompressobj();b=decoder.decompress(b[4:],size+1)
      assert len(b)==size and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
     hits.append(dict(offset=pos,type=tag.decode(),fid=fid,flags=flags,fields=[(t.decode(),v.hex()) for t,v in subrecords(b) if t in (b'EDID',b'MODL',b'KWDA',b'XMRK',b'VMAD')]))
    pos=end
  assert identity(p)==before
  esm.append(dict(source=before,records=nrec,hits=hits))
  print(p.name,nrec,len(hits),flush=True)
 with (OUT/'esm-7145.json').open('x',encoding='utf8',newline='\n') as f:json.dump(esm,f,indent=2);f.write('\n')
 old=json.loads((ROOT/'.local-work/workshop-origin/final-03/before.json').read_text())
 pins=[v for k,v in old.items() if Path(k).name.startswith(('Save25_','Save26_'))]
 pins+=json.loads((ROOT/'.local-work/native-oracle-020/operations/continuation-live-postflight-supplement-01.json').read_text())['new_checkpoint_pins']
 saved=[]
 for pin in pins:
  p=Path(pin['path']);before=identity(p);assert before['sha256']==pin['sha256']
  with decoded_save(p,OUT/'scratch') as (b,metrics):
   d=directory(b);a,_=d['regions']['reference_u32'];table=[struct.unpack_from('<I',b,a+4+4*i)[0] for i in range(d['reference_count'])]
   pt=plugin_tables(b);rows=[];exact=[];count=0;queue_leads=[];record_map={}
   for r in iter_records(b,*d['regions']['region_R3'],d['words'][9]):
    count+=1
    record_map.setdefault(r['token'],[]).append(r)
    fid=token_value(r['token'],table)
    relevant=[]
    for qi,t in enumerate(r['refs']):
     try:qfid=token_value(t,table)
     except ValueError:continue
     if qfid in (0x7145,0xff02380f,0xff02380a,0xff023809):relevant.append(dict(index=qi,token=t,saved_formid=f'{qfid:08X}'))
    if relevant:
     context=dict(ordinal=r['ordinal'],token=r['token'],saved_record_formid=f'{fid:08X}',offset=r['offset'],hits=relevant,
                  flags=r['flags'],end=r['end'],references=r['refs'],
                  interpretation_scope='CONDITIONAL_PREFIX_NOT_NATIVE_TYPE_PROOF' if int(r['token'],16)>>22==2 else 'STATIC_DIAGNOSTIC_NOT_BASE_GRAMMAR')
     case=5 if not r['flags']&0x8000 else 6 if r['flags']&0x02000008 else 4 if r['flags']&6 else 7
     context['conditional_case']=case
     try:
      prefix=initial_prefix(b,r,case);context['conditional_prefix']=prefix
      for key in ('base_token','parent_token','initial_reference_token'):
       if prefix.get(key):context[key+'_resolved']=f'{token_value(prefix[key],table):08X}'
     except ValueError as e:context['conditional_prefix_error']=str(e)
     queue_leads.append(context)
    if fid in (0xff02380f,0xff02380a,0xff023809):exact.append(dict(ordinal=r['ordinal'],token=r['token'],fid=f'{fid:08X}',offset=r['offset'],refs=r['refs']))
    if len(r['refs'])<3 or r['flags']&0x8000 or int(r['token'],16)>>22!=2:continue
    try:base=token_value(r['refs'][1],table)
    except ValueError:continue
    if base!=0x7145:continue
    row=dict(token=r['token'],fid=f'{fid:08X}',offset=r['offset'],end=r['end'],ordinal=r['ordinal'],explicit_type=r['explicit_type'],flags=r['flags'],refs=r['refs'])
    try:row['prefix']=initial_prefix(b,r,5)
    except ValueError as e:row['prefix_error']=str(e)
    rows.append(row)
   numeric=[]
   for value in (0x7145,0xff02380f,0xff02380a,0xff023809):
    pattern=struct.pack('<I',value);start=0;positions=[]
    while (start:=b.find(pattern,start))>=0:positions.append(start);start+=1
    numeric.append(dict(value=f'{value:08X}',array_indices=[i+1 for i,n in enumerate(table) if n==value],logical_byte_occurrences=positions))
   for lead in queue_leads:
    initial=lead.get('conditional_prefix',{}).get('initial_reference_token')
    if initial:
     lead['initial_record_matches']=[{k:r[k] for k in ('ordinal','offset','end','flags','refs')} for r in record_map.get(initial,[])]
   saved.append(dict(source=before,plugins=pt,decode=metrics,framed_records=count,landing_marker_candidates=rows,exact_runtime_number_matches=exact,queue_leads=queue_leads,numeric_only=numeric))
  assert identity(p)==before
  print(p.name,'marker rows',len(rows),'number matches',len(exact),flush=True)
 with (OUT/'saved-markers.json').open('x',encoding='utf8',newline='\n') as f:json.dump(saved,f,indent=2);f.write('\n')

 # The shared static reference leads are not assumed to be inline base objects.
 # Resolve every static saved record which queues7145, retaining ESM group labels.
 # A static record may use either an inline token or a form-array token. Select
 # by the already resolved saved ID and qualified Starfield namespace, not tag1.
 wanted=queued_static_ids(saved)
 base_wanted={int(r['base_token_resolved'],16) for save in saved for r in save['queue_leads'] if r.get('base_token_resolved') and int(r['base_token_resolved'],16)>>24==0}
 p=data/'Starfield.esm';before=identity(p);hits=[];total=p.stat().st_size
 with p.open('rb') as f:
  pos=0;stack=[(total,None)]
  while pos<total:
   while pos==stack[-1][0] and len(stack)>1:stack.pop()
   f.seek(pos);h=f.read(24);tag=h[:4];n,flags,fid=struct.unpack_from('<III',h,4);end=pos+(n if tag==b'GRUP' else 24+n)
   assert pos+24<=end<=stack[-1][0]
   if tag==b'GRUP':stack.append((end,dict(offset=pos,label=h[8:12].hex(),type=struct.unpack_from('<i',h,12)[0])));pos+=24;continue
   if fid in wanted|base_wanted:
    b=f.read(n)
    if flags&0x40000:
     size=struct.unpack_from('<I',b)[0];assert size<=16*1024*1024
     decoder=zlib.decompressobj();b=decoder.decompress(b[4:],size+1)
     assert len(b)==size and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
    hits.append(dict(fid=f'{fid:08X}',offset=pos,type=tag.decode(),parents=[x[1] for x in stack[1:]],fields=[(t.decode(),v.hex()) for t,v in subrecords(b) if t in (b'EDID',b'NAME',b'DATA')]))
   pos=end
 assert identity(p)==before
 if {int(h['fid'],16) for h in hits} != wanted|base_wanted:raise ValueError('STATIC_REFERENCE_DEFINITION_COVERAGE')
 with (OUT/'saved-marker-static-records.json').open('x',encoding='utf8',newline='\n') as f:json.dump(dict(source=before,wanted=sorted(wanted),conditional_base_wanted=sorted(base_wanted),hits=hits),f,indent=2);f.write('\n')
 print('static owner/base definitions resolved',len(hits),'of',len(wanted|base_wanted),flush=True)


if __name__ == '__main__':
 main()
