"""SPDX-License-Identifier: GPL-3.0-or-later
EXP0021 proposed natural-execution capture format and offline decoder, v0.1.0.
Pure stdlib; no target access or writes. Raw records remain local. Native
instruction basis and ownership: docs/experiments/engine-oracle/oracle-contract.md.
"""
import math
import re
import struct

RVA=0xad0d3b
VERSION='0.1.0'


def log_format():
    # x64dbg expression numbers and memory lengths are hexadecimal.
    return ('SOR_POSITION tid={u:tid()} rip={p:cip} rbx={p:rbx} rsi={p:rsi} rbp={p:rbp} '
            'center={mem;C@rbp-49} result={mem;2C@rbp-9} floor={mem;8@rbp+6F} '
            'context={mem;30@rsi} base={mem;2C@[rsi+18]} translation={mem;C@[rsi+20]} '
            'position={mem;C@rbx+8C} body={mem;4@[[rsi+10]]+54} '
            'resolution={mem;4@[[rsi+10]]+50}')


def decode_pair(raw,block=12,resolution=256):
    if len(raw)!=44 or block!=12 or resolution!=256:
        raise ValueError('UNSUPPORTED_PAIR_LAYOUT_OR_RESOLUTION')
    tag=raw[0]
    vals=[struct.unpack_from('<i',raw,p)[0] for p in (4,8,20,24,36,40)]
    cx,cy,sx,sy,fx,fy=vals
    if tag not in range(4) or not all(0<=v<limit for v,limit in zip(vals,(256,256,16,16,12,12))):
        raise ValueError('INVALID_NATIVE_HIERARCHY')
    return dict(tag=tag,x=cx*192+sx*12+fx,y=cy*192+sy*12+fy,
                hierarchy=vals,opaque_pattern_hex=raw[12:20].hex(),opaque_block_hex=raw[28:36].hex())


def decode_line(line,evidence_kind):
    if evidence_kind not in ('SYNTHETIC','RUNTIME'):
        raise ValueError('EXPLICIT_EVIDENCE_KIND_REQUIRED')
    if not line.startswith('SOR_POSITION '):raise ValueError('WRONG_RECORD')
    fields=dict(re.findall(r'(\w+)=([^\s]+)',line))
    sizes={'center':12,'result':44,'floor':8,'context':48,'base':44,
           'translation':12,'position':12,'body':4,'resolution':4}
    raw={};failures=[]
    for key,size in sizes.items():
        value=fields.get(key,'')
        if not re.fullmatch('[0-9a-fA-F]{'+str(size*2)+'}',value):failures.append(key)
        else:raw[key]=bytes.fromhex(value)
    if failures:
        return dict(status='PARTIAL',unreadable=failures,evidence_kind=evidence_kind,raw_fields=fields)
    resolution=int.from_bytes(raw['resolution'],'little')
    result=decode_pair(raw['result'],resolution=resolution)
    base=decode_pair(raw['base'],resolution=resolution)
    vectors={k:list(struct.unpack('<3f',raw[k])) for k in ('center','translation','position')}
    if any(not math.isfinite(v) for vals in vectors.values() for v in vals):
        return dict(status='PARTIAL',reason='NONFINITE',evidence_kind=evidence_kind,raw_fields=fields)
    return dict(status='DECODED_SEMANTICS_UNASSESSED',evidence_kind=evidence_kind,
                thread_id=int(fields['tid']),rip=fields['rip'],body=raw['body'][::-1].hex().upper(),
                center_hex=raw['center'].hex(),cell=[result[k] for k in ('tag','x','y')],
                native_floor=list(struct.unpack('<2i',raw['floor'])),base=base,result=result,
                vectors=vectors,raw_fields=fields)
