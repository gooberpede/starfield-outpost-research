# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned PE phase parent/chained ranges and FH4 cleanup ownership.

SOR-P-0002 adaptation of owned d5ab_p1_exception_parents.py metadata decoder;
format facts were previously consulted, no Microsoft implementation copied.
Reads PE only, emits exclusive ignored interval/ownership receipt. Does not
execute instructions or alter original/copy databases. No unknown EH/trap/leaf
ownership is guessed: uncovered metadata is explicit and must refuse startup.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import json
from pathlib import Path
import struct
from d5ar_native_inventory import ROOT,EXE,PIN,disk_floor


def main():
    out=Path(sys.argv[1]).resolve();before=disk_floor()
    if not out.is_relative_to(ROOT/'.local-work/d5ar') or out.exists():raise ValueError('Fresh ignored output required')
    if any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)):raise ValueError('No reparse output')
    data=EXE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('Installed PE changed')
    pe=struct.unpack_from('<I',data,0x3c)[0];optional=pe+24
    count=struct.unpack_from('<H',data,pe+6)[0];opt_size=struct.unpack_from('<H',data,pe+20)[0]
    sections=[struct.unpack_from('<IIII',data,optional+opt_size+40*n+8) for n in range(count)]
    def raw(rva,size):
        for _,start,length,file in sections:
            if start<=rva and rva+size<=start+length:return data[file+rva-start:file+rva-start+size]
        raise ValueError('Not wholly file-backed '+hex(rva))
    def word(rva):return struct.unpack('<I',raw(rva,4))[0]
    def compressed(rva):
        first=raw(rva,1)[0];prefix=0
        while prefix<4 and first&(1<<prefix):prefix+=1
        if prefix==4:return word(rva+1),rva+5
        size=prefix+1;return int.from_bytes(raw(rva,size),'little')>>size,rva+size
    directory,size=struct.unpack_from('<II',data,optional+112+3*8)
    records=list(struct.iter_unpack('<III',raw(directory,size)))
    def root(record,seen=()):
        begin,end,unwind=record
        if unwind in seen:raise ValueError('Cyclic unwind chain')
        header=raw(unwind,4)
        if header[0]>>3&4:
            at=(unwind+4+2*header[2]+3)&~3
            return root(struct.unpack('<III',raw(at,12)),(*seen,unwind))
        return begin
    rooted={}
    for record in records:rooted.setdefault(root(record),[]).append(record)
    parents=[0x1881660,0x787830,0x788bc0,0x788e70,0x789ce0,0x79d910]
    rows=[];ranges=set();open_metadata=[]
    for parent in parents:
        if parent not in rooted:raise ValueError('Missing exact parent runtime entry')
        owned=set();infos=[];pending=[parent];visited=set()
        while pending:
            target=pending.pop()
            if target in visited:continue
            visited.add(target)
            if target not in rooted:
                containing=[record for record in records if record[0]<=target<record[1]]
                if containing:
                    for record in containing:
                        ranges.add((record[0],record[1]));owned.add((record[0],record[1]));pending.append(root(record))
                else:
                    open_metadata.append(dict(parent_rva=hex(parent),action_rva=hex(target),reason='NO_RUNTIME_FUNCTION_ENTRY_REQUIRES_STARTUP_REFUSAL'))
                continue
            for begin,end,unwind in rooted[target]:
                ranges.add((begin,end));owned.add((begin,end));header=raw(unwind,4);flags=header[0]>>3
                if flags&4 or not flags&3:continue
                at=(unwind+4+2*header[2]+3)&~3;handler=word(at)
                if handler!=0x3663130:
                    open_metadata.append(dict(parent_rva=hex(parent),target_rva=hex(target),reason='OTHER_EH_HANDLER',handler_rva=hex(handler)))
                    continue
                info=word(at+4);cursor=info;bits=raw(cursor,1)[0];cursor+=1
                if bits&4:_,cursor=compressed(cursor)
                actions=[]
                if bits&8:
                    unwind_map=word(cursor);cursor+=4;states,at_state=compressed(unwind_map)
                    if states>10000:raise ValueError('FH4 state bound')
                    for state in range(states):
                        encoded,at_state=compressed(at_state);kind=encoded&3
                        if kind:
                            action=word(at_state);at_state+=4
                            if action:actions.append(action);pending.append(action)
                        if kind in (1,2):_,at_state=compressed(at_state)
                if bits&16:
                    open_metadata.append(dict(parent_rva=hex(parent),target_rva=hex(target),reason='TRY_BLOCK_MAP_NOT_DECODED',funcinfo_rva=hex(info)))
                infos.append(dict(target_rva=hex(target),funcinfo_rva=hex(info),bits=bits,actions_rva=[hex(a) for a in actions]))
                if len(visited)>256:raise ValueError('Bounded phase cleanup family exceeded')
        rows.append(dict(parent_rva=hex(parent),ranges=[[hex(a),hex(z)] for a,z in sorted(owned)],fh4=infos))
    value=dict(status='PASS',exe_sha256=PIN,method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inherited_metadata_method_sha256=hashlib.sha256((ROOT/'research/resource-retained-population/d5ab_p1_exception_parents.py').read_bytes()).hexdigest(),
        address_domain='module RVA; half-open original .pdata ranges',parents=rows,all_ranges=[[hex(a),hex(z)] for a,z in sorted(ranges)],
        open_metadata=open_metadata,scope='Original phase roots, chained functions and recursively named FH4 unwind actions; undeclared EH/leaf paths require startup refusal',
        floors_before=before,floors_after=disk_floor())
    with out.open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',ranges=len(ranges),open_metadata=open_metadata)))


if __name__=='__main__':main()
