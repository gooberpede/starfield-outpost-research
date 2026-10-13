# SPDX-License-Identifier: GPL-3.0-or-later
"""Read immutable schema4 raw/journal/health; write exclusive derivative only.
No target process, game call, original mutation or prediction adjustment.
Native component replay and saved correspondence are separate result dimensions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from inspect_events import decode,raw,hierarchy,SIZE,ROOT,PREDICTION_HASH
from durable_position_v2 import offset

def u64(e,n,at=0):
 b=raw(e,n,at+8)
 return struct.unpack_from('<Q',b,at)[0] if b is not None else None

def pair(items,begin,end,abnormal):
 items=sorted(items,key=lambda e:e['sequence'])
 ok=(len(items)==2 and items[0]['kind']==begin and items[1]['kind']==end
     and all(items[0][k]==items[1][k] for k in ('invocation','parent','thread','reference','context'))
     and items[0]['qpc']<=items[1]['qpc'])
 return ok,items[0],items[-1]

def reconcile(events,module_base=None):
 groups={}
 if len({e['sequence'] for e in events})!=len(events):raise ValueError('duplicate_sequence')
 for e in events:groups.setdefault(e['invocation'],[]).append(e)
 routes={i:sorted(v,key=lambda e:e['sequence']) for i,v in groups.items() if any(e['kind'] in (22,23,24) for e in v)}
 result=[]
 selection_groups={i:sorted(v,key=lambda e:e['sequence']) for i,v in groups.items() if any(e['kind'] in (40,41,42,43,44,48,49) for e in v)}
 selections=[]
 for sid,items in selection_groups.items():
  k=items[0]['kind'];k=items[0]['status'] if k==44 else k if k%2==0 else k-1
  good,a,b=pair(items,k,k+1,44)
  selections.append(dict(invocation=sid,kind=k,paired_normal=good,reference=a['reference'],thread=a['thread']))
 for i,items in routes.items():
  ok,start,end=pair(items,22,23,24)
  row=dict(invocation=i,thread=start['thread'],parent=start['parent'],paired_normal=ok,path='UNRESOLVED',grid=[],defects=[],selected_reference=u64(start,'input_hierarchy',24),selected_metadata=raw(start,'candidate'),saved_join='UNASSESSED_REQUIRES_BODY_ANGLES_PARENT_AND_LOAD_IDENTITY',full_model_equivalence='NOT TESTED')
  children=[]
  for cid,cs in groups.items():
   cs=sorted(cs,key=lambda e:e['sequence'])
   if cs[0]['parent']!=i or cs[0]['kind'] not in (*range(25,40),45,46):continue
   k=cs[0]['kind'] if cs[0]['kind']%2 else cs[0]['kind']-1
   if k==39:k=cs[0]['status']
   good,a,b=pair(cs,k,k+1,39)
   good=good and a['thread']==start['thread'] and start['sequence']<a['sequence']<b['sequence']<end['sequence']
   if not good:row['defects'].append('unpaired_or_unbound_child:'+str(cid))
   if module_base is not None:
    expected={25:[0x7800a6],27:[0x7801b3],29:[0x780264],31:[0x77fe91],33:[0x77fec0],35:[0x77fd45,0x780132],37:[0x7800d6],45:[0x77fce9]}.get(k,[])
    if u64(a,'block',8) not in [module_base+r+5 for r in expected] or u64(a,'block',8)!=u64(b,'block',8):
     good=False;row['defects'].append('callsite:'+str(cid))
   children.append((k,good,a,b))
  eligible=[v for v in children if v[0]==25];search=[v for v in children if v[0]==27];fallback=[v for v in children if v[0]==29]
  val=lambda x:u64(x[3],'result')
  # Source CFG has a separate direct supplied-reference configuration bypass.
  if len(eligible)==1 and eligible[0][1] and val(eligible[0]) is not None:
   if val(eligible[0])&255:
    if not search and not fallback:row['path']='SUPPLIED_REFERENCE'
   elif len(search)==1 and search[0][1]:
    if val(search[0]):
     if not fallback:row['path']='SEARCH_SHORTCUT'
    elif len(fallback)==1 and fallback[0][1] and search[0][3]['sequence']<fallback[0][2]['sequence']:
     row['path']='FALLBACK_REFERENCE' if val(fallback[0]) else 'FALLBACK_NO_REFERENCE'
  direct=[v for v in children if v[0]==45]
  if not eligible and not search and not fallback:
   row['path']='DIRECT_OR_UNOBSERVED_PRECONDITION'
   if len(direct)==1 and direct[0][1] and val(direct[0]) is not None and val(direct[0])&255:row['path']='DIRECT_SUPPLIED_REFERENCE'
  selection=selection_groups.get(start['parent'])
  row['selected_reference_bound']=False
  if selection:
   sk=selection[0]['kind'];sg,sa,sb=pair(selection,sk,sk+1,44)
   binding=sg and not(sa['status']&8 or sb['status']&8) and sa['thread']==start['thread'] and sa['sequence']<start['sequence']<end['sequence']<sb['sequence'] and sa['reference']!=0 and sa['blobs']['ref']['ok']
   if sk==48:binding=binding and u64(sa,'input_hierarchy',24)==u64(start,'input_hierarchy',16) and sa['blobs']['source']['address']==start['blobs']['source']['address'] and raw(sa,'source',16) is not None and raw(start,'source',16) is not None and raw(sa,'source',16)[:16]==raw(start,'source',16)[:16]
   if sk==40:binding=binding and sa['reference']==u64(start,'input_hierarchy',24)
   row['selected_reference_bound']=bool(binding and sk in (40,48));row['selected_reference_invocation']=start['parent'];row['upstream_selected_reference']=sa['reference']
  source=[v for v in children if v[0]==31]
  for k,good,a,b in children:
   if k!=33:continue
   source_before=[s for s in source if s[1] and s[3]['sequence']<a['sequence'] and u64(s[2],'input_hierarchy',8)==u64(a,'input_hierarchy',8)]
   inp=raw(a,'candidate',44);out=raw(b,'candidate',44);xy=raw(a,'floor_xy',8);land=raw(a,'landscape',0x60)
   chosen=u64(a,'context_raw',0x18);ref=a['blobs']['ref'];base=raw(a,'base',0x30)
   source_fresh=len(source_before)==1 and not(source_before[0][3]['status']&8) and raw(source_before[0][3],'candidate',44)==inp
   binding=bool(not(a['status']&8 or b['status']&8) and chosen and ref['ok'] and ref['address']==chosen and b['blobs']['ref']['address']==chosen and raw(a,'ref')==raw(b,'ref') and u64(b,'context_raw',0x18)==chosen)
   if row['path']=='SEARCH_SHORTCUT':binding=binding and chosen==val(search[0])
   if row['path'] in ('SUPPLIED_REFERENCE','DIRECT_SUPPLIED_REFERENCE'):binding=binding and chosen==u64(start,'input_hierarchy',32)
   if row['path']=='FALLBACK_REFERENCE':binding=binding and chosen==val(fallback[0])
   grid=dict(invocation=a['invocation'],paired_normal=good,source_fresh=source_fresh,chosen_reference=chosen,reference_bound=binding,path=row['path'],ordinary_base=base is not None and struct.unpack_from('<I',base,0x28)[0]==0x2c60e9,
     input_hex=None if inp is None else inp.hex(),output_hex=None if out is None else out.hex(),native_floor=None if xy is None else list(struct.unpack('<2i',xy)),classification='UNQUALIFIED',grid_equal=None,full_model_equivalence='NOT TESTED')
   if good and source_fresh and binding and all(v is not None for v in (inp,out,xy,land)) and row['path'] in ('SUPPLIED_REFERENCE','DIRECT_SUPPLIED_REFERENCE','SEARCH_SHORTCUT','FALLBACK_REFERENCE'):
    block=raw(a,'block',16);merge=raw(a,'merge',4)
    if block is not None and struct.unpack_from('<I',block,4)[0]==1 and merge is not None and struct.unpack_from('<I',land,0x50)[0]==256 and struct.unpack_from('<I',block)[0]+struct.unpack_from('<I',merge)[0]==12:
     try:
      expected=list(offset(*hierarchy(inp),*struct.unpack('<2i',xy)))
      grid.update(classification='IDENTITY_BOUND_GENERIC_COMPONENT_REPLAY',derived_grid=expected,native_grid=hierarchy(out),grid_equal=expected==hierarchy(out),body=struct.unpack_from('<I',land,0x54)[0],system=struct.unpack_from('<I',land,0x58)[0],body_index=struct.unpack_from('<I',land,0x5c)[0])
     except (ValueError,OverflowError):grid['reason']='unsupported_input_hierarchy'
   row['grid'].append(grid)
  # Exact route integrity remains independent of optional scientific fields.
  if not ok:row['defects'].append('outer_unpaired_or_unwound')
  row['reachability']='GRID' if row['grid'] else 'FALLBACK' if fallback else 'SEARCH' if search else 'ELIGIBILITY' if eligible else 'OUTER_ONLY'
  row['scientific_complete']=ok and not row['defects'] and bool(row['grid']) and all(g['classification']=='IDENTITY_BOUND_GENERIC_COMPONENT_REPLAY' for g in row['grid'])
  result.append(row)
 orphans=[i for i,cs in groups.items() if cs[0]['kind'] in (*range(25,40),45,46) and cs[0]['parent'] not in routes]
 diagnostics=[i for i,cs in groups.items() if any(e['kind'] in (7,8,9,10,11,12) for e in cs)]
 incomplete_diagnostics=[i for i in diagnostics if not pair(groups[i],7 if any(e['kind'] in (7,8,9) for e in groups[i]) else 10,8 if any(e['kind'] in (7,8,9) for e in groups[i]) else 11,9)[0]]
 return dict(incomplete_diagnostics=incomplete_diagnostics,routes=result,unpaired_or_orphan_children=orphans,selections=selections,incomplete_roots=[i for i,cs in routes.items() if not pair(cs,22,23,24)[0]],selection_invocations=list(selection_groups),q_invocations=[i for i,cs in groups.items() if cs[0]['kind']==7],e_invocations=[i for i,cs in groups.items() if cs[0]['kind']==10],native_equivalence='NOT TESTED')

def records(session):
 data=(session/'events.bin').read_bytes();journal=(session/'records.jsonl').read_bytes();events=[];at=0;tail=False
 for line in journal.splitlines(keepends=True):
  if not line.endswith(b'\n'):tail=True;break
  r=json.loads(line)
  if r['offset']!=at or r['length']!=SIZE:raise ValueError('journal_extent')
  chunk=data[at:at+SIZE]
  if len(chunk)!=SIZE or hashlib.sha256(chunk).hexdigest()!=r['sha256']:raise ValueError('record_integrity')
  e=decode(chunk)
  if any(e[k]!=r[k] for k in ('sequence','invocation','kind')):raise ValueError('record_identity')
  events.append(e);at+=SIZE
 seq=sorted(e['sequence'] for e in events)
 if seq!=list(range(1,len(seq)+1)):raise ValueError('sequence_integrity')
 return events,dict(journal_incomplete_tail=tail,raw_unjournaled_bytes=len(data)-at,complete_records=len(events))

def inspect(session):
 session=Path(session);ready=json.loads((session/'ready.json').read_text())
 if ready.get('component')!='SorNativePositionOracle':raise ValueError('ready_component')
 if (ready.get('version'),ready.get('schema'),ready.get('event_size'))!=('0.4.0',4,SIZE):raise ValueError('ready_identity')
 frozen=(ROOT/'docs/experiments/engine-oracle/predictions.json').read_bytes()
 if hashlib.sha256(frozen).hexdigest()!=PREDICTION_HASH:raise ValueError('frozen_input_changed')
 events,integrity=records(session);r=reconcile(events,int(ready['module_base'],16));r['integrity']=integrity
 retired=json.loads((session/'retired.json').read_text()) if (session/'retired.json').exists() else None
 r['retirement_complete']=bool(retired and retired.get('events')==len(events) and all(retired.get(k)==0 for k in ('lost','depth_errors','health_timeouts')) and all(retired.get(k)==ready.get(k) for k in ('component','version','schema','pid','process_creation_filetime','dll_sha256','module_base','qpc_frequency')) and retired.get('patches_retained') and retired.get('resident_inert_until_exit') and not integrity['journal_incomplete_tail'] and not integrity['raw_unjournaled_bytes'])
 from operate import valid_health_counts,valid_health_transition
 health=[];health_tail=False
 for line in (session/'health.jsonl').read_bytes().splitlines(keepends=True):
  if not line.endswith(b'\n'):health_tail=True;break
  h=json.loads(line)
  if not valid_health_counts(h) or h['health_sequence']!=len(health)+1 or not valid_health_transition(health[-1] if health else None,h,ready.get('qpc_frequency')):raise ValueError('health_integrity')
  if any(h.get(k)!=ready.get(k) for k in ('component','version','schema','pid','process_creation_filetime','dll_sha256','module_base','qpc_frequency')):raise ValueError('health_identity')
  health.append(h)
 expected_entered=[sum(e['kind']==7 for e in events),sum(e['kind']==10 for e in events),sum(e['kind'] in (22,40,42,48) for e in events)]
 r['worker_complete']=bool(health and not health_tail and health[-1]['flushed_events']==len(events) and health[-1]['queue_depth']==0 and health[-1]['active']==[0,0,0] and health[-1]['entered']==expected_entered and health[-1]['stopping'])
 r['capture_complete']=r['worker_complete'] and r['retirement_complete'] and not (session/'failure.json').exists() and not r['unpaired_or_orphan_children'] and not r['incomplete_roots'] and not r['incomplete_diagnostics'] and all(s['paired_normal'] for s in r['selections'])
 if not r['capture_complete']:
  for row in r['routes']:row['scientific_complete']=False
 r['frozen_prediction_sha256']=PREDICTION_HASH;r['frozen_prediction_comparison']='NOT TESTED: generic reference coordinates do not equal compensated workshop center by contract'
 r['target_survival']='OPERATOR_POSTFLIGHT_REQUIRED';return r

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('session',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 result=inspect(a.session)
 with a.output.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
