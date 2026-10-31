# SPDX-License-Identifier: GPL-3.0-or-later
"""Read only Save52's native-justified global-type-3 prefix from an existing copy.

Uses the owned stream decoder, directory and unit-3 framing readers. Their
source-informed research provenance remains in the D5Z source ledger. Stdlib
only; no third-party parser. Reads one pinned controlled save copy and policy,
writes a fresh ignored receipt, uses a temporary decoded mmap that is removed
by the owned decoder. Does not load/resave a game or write protected originals.
Independent selected-block zlib decompression cross-checks the extracted bytes.
Native 0x141830550 reads the header structure u32 at logical 0x10; for
structure version >=25 its next byte at 0x14 becomes file+0x110, copied into
global reader+0x28 at 0x1418240c7. This is distinct from a build string.
"""
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from stream_save import decoded_save
from validate_mature_outposts import directory
from outpost_planetary_location import global_suffix
from planet_world_key import find_unit3_context, unit3_world_descriptors

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def guard(scratch=None,reserve=0):
    for drive in ('C:/','D:/'):
        value=ctypes.c_ulonglong()
        assert ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive),ctypes.byref(value),None,None)
        assert value.value-reserve >= 40_000_000_000

def independent_slice(path,offset,length):
    # Independent physical-table iteration and one-shot zlib decode; no mmap or
    # envelope parser. This checks bytes at the selected logical offset only.
    with path.open('rb') as stream:
        header=stream.read(72)
        table,start,total,block=(struct.unpack_from('<Q',header,p)[0] for p in (8,24,32,48))
        assert table==72 and block==262144 and 0<=offset<offset+length<=total
        pieces=[]
        physical=start
        for index in range((offset+length-1)//block+1):
            stream.seek(table+4*index)
            n=int.from_bytes(stream.read(4),'little')
            if index>=offset//block:
                stream.seek(physical)
                decoded=zlib.decompress(stream.read(n))
                lo=max(offset-index*block,0)
                hi=min(offset+length-index*block,len(decoded))
                pieces.append(decoded[lo:hi])
            physical=(physical+n+15)//16*16
        return b''.join(pieces)

def main():
    out=Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work') and not out.exists()
    policy=ROOT/'research/resource-carinae-source-context/save_policy.json'
    pins=json.loads(policy.read_text())['designated']
    name=next(n for n in pins if n.startswith('Save52_'))
    source=ROOT/'.local-work/savegames'/name
    assert source.stat().st_size==pins[name]['bytes'] and sha(source)==pins[name]['sha256']
    guard()
    out.mkdir(parents=True)
    with decoded_save(source,out/'scratch',seconds=float('inf'),guard=guard) as (buffer,metrics):
        d=directory(buffer)
        suffix=global_suffix(buffer,d)
        context=find_unit3_context(buffer,d['regions']['region_R1'][0],suffix[4][0]-8)
        descriptors, descriptor_end = unit3_world_descriptors(buffer,context)
        offset=context['start']
        prefix=bytes(buffer[offset:offset+12])
        assert prefix==independent_slice(source,offset,12)
        assert bytes(buffer[offset:descriptor_end])==independent_slice(source,offset,descriptor_end-offset)
        assert bytes(buffer[:25])==independent_slice(source,0,25)
        structure_version=struct.unpack_from('<I',buffer,16)[0]
        assert structure_version>=25
        buffer_version=buffer[20]
        receipt=dict(schema='sor-d5z-save-prefix/1',source=str(source),source_sha256=sha(source),source_bytes=source.stat().st_size,
            policy_sha256=sha(policy),metrics=metrics,directory=d,context=context,
            prefix_hex=prefix.hex(),key_u64=struct.unpack_from('<Q',prefix)[0],comparison_u32=struct.unpack_from('<I',prefix,8)[0],
            prefix_logical_offset=offset,prefix_length=12,independent_selected_block_match=True,
            independent_descriptor_span_match=True,script_sha256=sha(__file__),
            header_structure_version=dict(logical_offset=16,value=structure_version),
            native_buffer_version=dict(logical_offset=20,value=buffer_version,at_least_0x3e=buffer_version>=0x3e),
            world_descriptors=descriptors,world_descriptor_end=descriptor_end,
            remaining_unit3_bytes=context['start']+context['length']-descriptor_end,
            scope='Global type 3 prefix and grounded world-descriptor array; later overlay/component payload not decoded; no visited-serialization absence proof',
            methods={str(ROOT/'save-analysis/scripts'/n):sha(ROOT/'save-analysis/scripts'/n) for n in
                ('stream_save.py','validate_mature_outposts.py','outpost_planetary_location.py','planet_world_key.py')})
    assert sha(source)==pins[name]['sha256']
    assert not any((out/'scratch').iterdir())
    (out/'save-prefix.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({k:receipt[k] for k in ('source_sha256','prefix_logical_offset','world_descriptor_end','remaining_unit3_bytes','independent_descriptor_span_match','header_structure_version','native_buffer_version')},indent=2))

if __name__=='__main__':
    main()
