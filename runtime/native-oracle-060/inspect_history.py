# SPDX-License-Identifier: GPL-3.0-or-later
"""Read only fixed schema6 raw records and journal; return owned decoded JSON.
No save parsing, native calls, mutable model or repairs. Optional output is new.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

SIZE=3328
HEAD=struct.Struct('<16Q')
NAMES=('sequence','invocation','parent','thread','qpc','site','kind','phase','reference','command','result','status','arg0','arg1','arg2','arg3')
BLOBS=('ref','base','extra','cell','world','operand','aux','output')
KINDS={1:'replacement',2:'conversion',3:'application_xyz',4:'immediate_producer',5:'queued_producer',6:'submission',7:'deferred_application',8:'center',9:'command_allocation',10:'initial_restoration_setter_not_allocation_birth'}
def triple(b):
    return dict(hex=b.hex(),values=list(struct.unpack('<3f',b))) if len(b)==12 else None
def decode(data):
    if len(data)!=SIZE:raise ValueError('record_size')
    e=dict(zip(NAMES,HEAD.unpack_from(data)))
    for i,name in enumerate(BLOBS):
        offset=128+400*i;address,length,ok=struct.unpack_from('<QII',data,offset)
        if length>384 or ok not in (0,1):raise ValueError('blob_bounds_or_status')
        e[name]=dict(address=address,length=length,ok=bool(ok),hex=data[offset+16:offset+16+length].hex() if ok else None)
    return e
def raw(e,name):
    b=e[name];return bytes.fromhex(b['hex']) if b['ok'] else b''
def identify(e):
    b=raw(e,'base');w=raw(e,'extra');r=raw(e,'ref')
    coherent=e['status']==0
    return dict(pointer=e['reference'],form_id=struct.unpack_from('<I',r,0x28)[0] if coherent and len(r)>=0x2c else None,
        base_id=struct.unpack_from('<I',b,0x28)[0] if coherent and len(b)>=0x2c else None,
        workshop_id=w[0x98:0xa0].hex() if coherent and len(w)>=0xa0 and w[0x98:0xa0]!=bytes(8) else None,
        d3=r[0xd3] if len(r)>0xd3 else None,xyz=triple(r[0x8c:0x98]) if len(r)>=0x98 else None,
        compensation=triple(w[0x60:0x6c]) if len(w)>=0x6c else None,
        own_cell=e['cell']['address'] if e['cell']['ok'] else None,own_world=e['world']['address'] if e['world']['ok'] else None,
        sampling_status=e['status'],identity_quality='COHERENT_SAMPLED_CANDIDATE' if coherent else 'QUARANTINED_INCOHERENT_OR_PARTIAL_SAMPLE')
def file_sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def records(root,stats):
    stats.update(offset=0,records=0,errors=[])
    with (root/'events.bin').open('rb') as raw_file,(root/'records.jsonl').open('rb') as journal:
        for line in journal:
            if not line.endswith(b'\n'):stats['errors'].append('partial_journal_tail');break
            try:
                j=json.loads(line);seq=stats['records']+1
                if j['offset']!=stats['offset'] or j['length']!=SIZE or j['sequence']!=seq:raise ValueError('journal_order_or_bounds')
                b=raw_file.read(SIZE)
                if len(b)!=SIZE or hashlib.sha256(b).hexdigest()!=j['sha256']:raise ValueError('record_hash_or_length')
                e=decode(b)
                if e['sequence']!=seq:raise ValueError('raw_sequence')
                stats['records']+=1;stats['offset']+=SIZE;yield e
            except (ValueError,KeyError,TypeError) as exc:stats['errors'].append(str(exc));break
def inspect(root,workshops=None,summary=False):
    root=Path(root);selected=None;stats={}
    if workshops:
        selected=set()
        for e in records(root,stats):
            if identify(e)['workshop_id'] in workshops:selected.add(e['reference'])
    committed=[];stream_pending={};stream_pairs=0
    for e in records(root,stats):
        if summary:
            key=e['invocation']
            if e['phase']==1:
                if key in stream_pending:stats['errors'].append('duplicate_begin')
                stream_pending[key]=(e['thread'],e['site'],e['kind'],e['parent'])
            elif e['phase'] in (2,3):
                before=stream_pending.pop(key,None)
                if before!=(e['thread'],e['site'],e['kind'],e['parent']):stats['errors'].append('unpaired_or_mismatched_end')
                else:stream_pairs+=1
            else:stats['errors'].append('invalid_phase')
        elif selected is None or e['reference'] in selected:
            e['identity']=identify(e);e['kind_name']=KINDS.get(e['kind'],'UNKNOWN');committed.append(e)
    errors=stats['errors'];offset=stats['offset'];size=(root/'events.bin').stat().st_size;tail_size=size-offset;recoverable=[]
    # An unjournaled full raw record is retained, never counted as committed.
    if tail_size:
        errors.append('raw_uncommitted_tail')
        with (root/'events.bin').open('rb') as f:
            f.seek(offset);preview=f.read(SIZE)
            if len(preview)==SIZE:
                try:recoverable.append(decode(preview))
                except ValueError:pass
    pending={};pairs=[]
    for e in committed:
        key=e['invocation']
        if e['phase']==1:
            if key in pending:errors.append('duplicate_begin')
            pending[key]=e
        elif e['phase'] in (2,3):
            b=pending.pop(key,None)
            if b is None or (b['thread'],b['site'],b['kind'],b['parent'])!=(e['thread'],e['site'],e['kind'],e['parent']):errors.append('unpaired_or_mismatched_end')
            else:pairs.append((b,e))
        else:errors.append('invalid_phase')
    no_write=[]
    for b,e in pairs:
        ident=b['identity'];end=e['identity'];requested=b['arg2']&255
        if b['kind']==2 and e['phase']==2 and requested in (0,1) and ident['d3'] is not None and ((ident['d3']>>1)&1)==requested and ident['xyz']==end['xyz'] and not b['status'] and not e['status']:
            no_write.append(dict(invocation=b['invocation'],first_sequence=b['sequence'],last_sequence=e['sequence'],scope='SAMPLED_UNCHANGED_GATE_COMPATIBLE_CANDIDATE',basis='before_after_samples_only',actual_gate_branch='UNPROVEN_CONCURRENT_STATE_CHANGE_POSSIBLE',excludes_concurrent_writers=False,lifetime_complete=False))
    # Identity-late binding is a conservative candidate join. Never certify a
    # native lifetime from a pointer. Nonzero-ID changes split segments, while
    # unobserved deletion/reuse with the same ID remains explicitly uncertain.
    segments=[];by_pointer={};quarantined=[]
    for e in committed:
        ptr=e['reference']
        if not ptr:continue
        if e['status']:
            quarantined.append(dict(sequence=e['sequence'],pointer=ptr,status=e['status'],association='QUARANTINED'));continue
        identity=e['identity'];wid=identity['workshop_id'];form=identity['form_id'];base=identity['base_id']
        current=by_pointer.get(ptr)
        changed=current and any(old is not None and new not in (None,0) and old!=new for old,new in ((current['workshop_id'],wid),(current['form_id'],form),(current['base_id'],base)))
        if current is None or changed:
            current=dict(pointer=ptr,workshop_id=wid,form_id=form if form else None,base_id=base if base else None,sequences=[],identity_late_bound=False,lifetime='UNPROVEN',history='PARTIAL_OBSERVED_HISTORY',gaps=['unhooked_direct_writers','allocation_and_destruction_not_observed','save_token_remapping_not_observed','pre_capture_interval_unknown'])
            segments.append(current);by_pointer[ptr]=current
        if wid and current['workshop_id'] is None:current['workshop_id']=wid;current['identity_late_bound']=True
        for name,value in (('form_id',form),('base_id',base)):
            if value and current[name] is None:current[name]=value
        current['sequences'].append(e['sequence'])
    # Command allocation is a measured generation boundary for this allocation
    # site. Require application after allocation and before observed next reuse;
    # do not join solely by equal ref/vector or invent a cross-thread TLS parent.
    allocations={};links=[]
    for e in committed:
        if e['kind']==9 and e['phase']==2 and e['command']:
            allocations[e['command']]=e
        if e['kind']==7 and e['phase']==1:
            a=allocations.get(e['command']);aux=raw(e,'aux')
            valid=a is not None and not a['status'] and not e['status'] and len(aux)>=0x30 and struct.unpack_from('<Q',aux,0x20)[0]==e['reference'] and a['reference']==e['reference']
            links.append(dict(application_invocation=e['invocation'],command=e['command'],allocation_invocation=a['invocation'] if valid else None,producer_invocation=a['parent'] if valid else None,relationship='OBSERVED_COMMAND_ADDRESS_GENERATION_CANDIDATE' if valid else 'UNJOINED',lifetime='UNPROVEN_OTHER_ALLOCATORS_OR_REUSE',cross_thread=bool(valid and a['thread']!=e['thread'])))
    terminal=None;metadata_corrupt=False
    for name in ('retired.json','failure.json','terminal.json'):
        if (root/name).is_file():
            try:
                candidate=json.loads((root/name).read_text())
                if not isinstance(candidate,dict):raise ValueError('not_object')
                terminal=candidate;break
            except (OSError,UnicodeError,ValueError) as exc:errors.append('terminal_metadata_corrupt: '+name+': '+str(exc));metadata_corrupt=True
    emergency=root/'emergency-status.json'
    if emergency.is_file():
        try:
            page=json.loads(emergency.read_text())
            if not isinstance(page,dict):raise ValueError('not_object')
            if page.get('error'):errors.append('emergency_status_failure: '+str(page['error']))
        except (OSError,UnicodeError,ValueError) as exc:errors.append('emergency_metadata_corrupt: '+str(exc));metadata_corrupt=True
    if terminal and (terminal.get('failed',0) or terminal.get('integrity_failure') or terminal.get('error') or (root/'failure.json').is_file()):errors.append('reported_instrumentation_failure: '+str(terminal.get('error','')))
    if terminal and terminal.get('last_durable_sequence')!=stats['records']:errors.append('terminal_accounting_mismatch')
    return dict(schema=6,mode='STREAMING_PREFIX' if summary else ('SELECTED_WORKSHOP_TWO_PASS' if workshops else 'FULL_DECODE'),committed_records=stats['records'],selected_records=len(committed),raw_size=size,journal_sha256=file_sha(root/'records.jsonl'),raw_sha256=file_sha(root/'events.bin'),integrity='PASS_COMMITTED_PREFIX' if not errors else 'FAIL_OR_PARTIAL',transport_retirement='UNCONFIRMED_CORRUPT_METADATA' if metadata_corrupt else ('TERMINAL_RECORDED' if terminal else 'UNCONFIRMED_MISSING_TERMINAL'),errors=errors,unfinished_invocations=sorted(stream_pending if summary else pending),recoverable_uncommitted_records=recoverable,uncommitted_tail_bytes=tail_size,uncommitted_tail_record_count=tail_size//SIZE,partial_tail_bytes=tail_size%SIZE,terminal_present=terminal is not None and not metadata_corrupt,events=committed,paired_invocations=stream_pairs if summary else len(pairs),segments=segments,quarantined_identity_events=quarantined,command_links=links,history_completeness='PARTIAL_OBSERVED_HISTORY' if stats['records'] else 'UNUSABLE_OR_MISSING_EVIDENCE',scientific_equivalence='NOT_TESTED_REQUIRES_SAVED_IDENTITY_FRAME_AND_HISTORY',scoped_no_write='NOT_ESTABLISHED',unchanged_conversion_candidates=no_write,complete_lifetimes=0)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('session',type=Path);ap.add_argument('--output',type=Path);ap.add_argument('--summary',action='store_true');ap.add_argument('--workshop',action='append');a=ap.parse_args();result=inspect(a.session,a.workshop,a.summary)
    if a.output:
        with a.output.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2,allow_nan=True);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('events','segments','recoverable_uncommitted_records')},indent=2))
if __name__=='__main__':main()
