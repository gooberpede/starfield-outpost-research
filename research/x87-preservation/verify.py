# SPDX-License-Identifier: GPL-3.0-or-later
"""Decode owned synthetic records; write exact field comparisons beside input.

Stdlib only; no execution, target access or input modification. FXSAVE64 pointer
words and legacy offset/selector words are intentionally different views.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

SIZE = 5212
FIELDS = {'control': (0, 2), 'status_top_conditions': (2, 2),
          'abridged_tag': (4, 1), 'opcode': (6, 2),
          'fip64': (8, 8), 'fdp64': (16, 8), 'mxcsr': (24, 4)}
FIELDS.update({f'st{i}_80bits': (32+16*i, 10) for i in range(8)})
BOUNDARIES = {'before': 704, 'entry_hardware': 3072,
              'context_legacy': 3584, 'after': 2240,
              'before_repeat': 4096, 'before_legacy': 4608}


def decode(data):
    if len(data)<8:
        raise ValueError('empty/header')
    version=struct.unpack_from('<I',data,4)[0]
    if version not in (1,2):
        raise ValueError('version')
    size=SIZE if version==1 else 5724
    if len(data) % size:
        raise ValueError('incomplete frame')
    rows = []
    for offset in range(0, len(data), size):
        magic, row_version, seq, condition, mode, identity = struct.unpack_from('<6I', data, offset)
        if (magic, row_version, seq) != (0x37385853, version, len(rows)+1):
            raise ValueError('header/sequence')
        if condition not in (0, 1, 2) or mode not in (0, 1, 2):
            raise ValueError('condition/mode')
        if struct.unpack_from('<I',data,offset+size-4)[0] != 0x454e4421:
            raise ValueError('trailer')
        state = data[offset+24:offset+size-4]
        values = {b: {f: state[base+o:base+o+n].hex() for f,(o,n) in FIELDS.items()}
                  for b,base in BOUNDARIES.items() if condition or b not in ('entry_hardware','context_legacy')}
        # Qualify adjacent FXSAVE64 measurement and explicit restore precondition.
        assert values['before'] == values['before_repeat'], (seq,'measurement changed state')
        assert values['before']['control'] == '7f07'
        assert values['before']['opcode'] == '2103'
        assert values['before']['status_top_conditions'] in ('0020','0165')
        assert values['before']['abridged_tag'] == 'b0'
        for f in ('fip64','fdp64'):
            assert int.from_bytes(bytes.fromhex(values['before'][f]),'little') > 0xffffffff, (seq,f)
        # Distinct logical ST0=2.5, ST1=-pi, an empty hole ST2, ST3=1.
        assert values['before']['st0_80bits']=='00000000000000a00040'
        assert values['before']['st1_80bits']=='34c26821a2da0fc900c0'
        assert values['before']['st3_80bits']=='0000000000000080ff3f'
        for f in ('fip64','fdp64'):
            assert values['before_legacy'][f][:8] == values['before'][f][:8]
        mismatches = {b:[f for f in FIELDS if values[b][f] != values['before'][f]]
                      for b in ('entry_hardware','context_legacy','after') if b in values}
        # GP/flags/SIMD checks also cover the nested child omitted by old compare().
        a, b = state[:1536], state[1536:3072]
        assert all(a[i*8:i*8+8]==b[i*8:i*8+8] for i in range(16) if i!=1), (seq,'GPR')
        before_rbx = struct.unpack_from('<Q',a,8)[0]
        assert struct.unpack_from('<Q',b,8)[0] == (0x22334455 if mode else before_rbx+0x30)
        expected = 0 if mode==2 else (0xad7&0x8d5) if mode else 4
        assert struct.unpack_from('<Q',b,128)[0]&0x8d5 == expected
        assert a[160:672] == b[160:672], (seq,'YMM')
        assert a[864:1120] == b[864:1120], (seq,'XMM')
        if version==2 and condition:
            expected=bytearray(state[3584:4096])
            expected[8:24]=state[3080:3096]
            assert state[5120:5632]==expected, (seq,'restore image provenance')
        rows.append(dict(sequence=seq, frame_file_offset=offset, condition=condition,
                         mode=mode, thread_id=identity&0xffffff, child=identity>>24,
                         fields=values, mismatches=mismatches))
    return rows


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path',type=Path)
    ap.add_argument('--expect',choices=['loss','preserved'],required=True)
    args=ap.parse_args()
    data=args.path.read_bytes()
    rows=decode(data)
    size=SIZE if struct.unpack_from('<I',data,4)[0]==1 else 5724
    counts=Counter((r['condition'],b,f) for r in rows for b,fs in r['mismatches'].items() for f in fs)
    for row in rows:
        mismatch=row['mismatches']
        assert mismatch['after'] == (['fip64','fdp64'] if row['condition'] and args.expect=='loss' else []),row['sequence']
        if row['condition']:
            assert mismatch['entry_hardware']==[],row['sequence']
            assert mismatch['context_legacy']==['fip64','fdp64'],row['sequence']
    negatives={}
    for name,bad in [('tail',data[:-1]),('header',b'BAD!'+data[4:]),
                     ('sequence',data+data[:size]),('empty',b'')]:
        try: decode(bad)
        except (ValueError,AssertionError): negatives[name]='REJECTED'
        else: raise AssertionError(name)
    result=dict(measurement_checks='PASS', required_preservation='FAIL' if args.expect=='loss' else 'PASS',
                records=len(rows),condition_counts=dict(Counter(r['condition'] for r in rows)),
                modes=dict(Counter(r['mode'] for r in rows)),
                threads=sorted(set(r['thread_id'] for r in rows)),children=sum(r['child'] for r in rows),
                mismatches=[dict(condition=c,boundary=b,field=f,count=n) for (c,b,f),n in sorted(counts.items())],
                negative_controls=negatives,sha256=hashlib.sha256(data).hexdigest(),rows=rows)
    output=args.path.with_name('comparison.json')
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))


if __name__=='__main__': main()
