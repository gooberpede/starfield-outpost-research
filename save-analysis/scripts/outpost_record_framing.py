"""SPDX-License-Identifier: GPL-3.0-or-later
Original save-record framing, source-informed by installed retail instructions
at static 14185e180/141809400 and project count grammar. No external code.
Reads bytes only. No writes or target effects. R3 must close exactly with the
directory-declared count. Reference/string tables are relocations, not proof
that a referenced base belongs to this record. Body semantics remain separate.
"""
import struct
from stream_save import ResourceLimit


def beacon_prefix(b,r):
    """Diagnostic case-5 REFR prefix only; never an ownership/classification rule.

    Preconditions are token tag 10, no 0x8000 change flag and second queued
    reference equal to the content-derived beacon token. Actual form type and
    load remapping remain a separate proof obligation. Reads no files/writes.
    """
    if (int(r['token'],16)&0xc00000)!=0x800000 or r['flags']&0x8000:return None
    if len(r['refs'])<3 or r['refs'][1]!='6c60e9' or r['refs'][2]!=r['token']:return None
    c=Reader(b,r['body'],r['end']);shape=c.take(1)[0]
    xyz=struct.unpack('<3f',c.take(12))
    for i in range(3):
        if shape&(1<<i):c.take(4)
    if not shape&0x18:c.take(1)
    result=dict(transform_shape=shape,xyz=xyz,initial_data_end=c.p,
                promoted=bool(r['flags']&0x02000000))
    if r['flags']&1:
        result.update(saved_flags_offset=c.p,saved_form_flags=int.from_bytes(c.take(4),'little'),
            saved_aux_flags=int.from_bytes(c.take(2),'little'))
        result['disabled']=bool(result['saved_form_flags']&0x800)
        result['deleted']=bool(result['saved_form_flags']&0x20)
    return result


class Reader:
    def __init__(self,b,start,end):
        if not 0<=start<=end<=len(b):raise ValueError('reader bounds')
        self.b,self.p,self.end=b,start,end
    def take(self,n):
        if not 0<=n<=self.end-self.p:raise ValueError('record boundary crossing')
        p=self.p;self.p+=n;return self.b[p:self.p]
    def count(self):
        first=self.take(1)[0];width={0:1,1:2,2:4}.get(first&3)
        if width is None:raise ValueError('unsupported count tag 3')
        return int.from_bytes(bytes([first])+self.take(width-1),'little')>>2


def iter_records(b,start,end,expected,queue_budget=16*1024*1024):
    """Iterate records without retaining the region or copying body payloads.
    Full closure is checked only when the iterator is exhausted.
    """
    c=Reader(b,start,end)
    if not 0<=expected<=(end-start)//4:raise ValueError('record count bounds')
    for ordinal in range(expected):
        p=c.p;tag=c.take(1)[0]
        if tag&0xc0:raise ValueError('unexplained header bits')
        explicit_type=c.take(1)[0] if tag&1 else None
        token=c.take(3).hex()
        flags=int.from_bytes(c.take(4),'little') if tag&2 else 0x80008000
        nr=c.count() if tag&8 else 0;ns=c.count() if tag&16 else 0;size=c.count() if tag&32 else 0
        header_end=c.p
        if nr>(end-c.p)//3:raise ValueError('reference table bounds')
        if nr*3+ns*2+size>end-c.p:raise ValueError('combined record bounds')
        if nr*64+ns*36>queue_budget:raise ResourceLimit('RECORD_QUEUE_WORKING_MEMORY_BUDGET')
        refs=[c.take(3).hex() for _ in range(nr)]
        if ns>(end-c.p)//2:raise ValueError('string table bounds')
        strings=[int.from_bytes(c.take(2),'little') for _ in range(ns)]
        body=c.p
        if size>c.end-c.p:raise ValueError('record boundary crossing')
        c.p+=size
        yield dict(ordinal=ordinal,offset=p,end=c.p,tag=tag,explicit_type=explicit_type,
            token=token,flags=flags,reference_start=header_end,refs=refs,
            string_start=header_end+nr*3,strings=strings,body=body,size=size)
    if c.p!=end:raise ValueError('record count/region closure mismatch')


def records(b,start,end,expected):
    """Compatibility list API; capacity consumers should use iter_records."""
    return list(iter_records(b,start,end,expected))
