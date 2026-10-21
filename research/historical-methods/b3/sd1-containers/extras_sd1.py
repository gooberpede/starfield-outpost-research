# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded P1 saved-instance inspection; project-owned readers, stdlib only.

Reads explicit existing source receipts, hash-pinned original saves, installed
definition cache and selected power catalogue. Writes exclusive local JSON under
.local-work/p1-power/saved and temporary decoded scratch removed by decoded_save.
No game/tool invocation, original modification, database, network or Git effects.
Preserves unsupported extras as gaps, never absence. Offsets: decoded logical
stream unless explicitly marked definition original-file offset. Run from repo
with CPython -B; --run alphanumeric --sample HIST-0036 or mature-Save52.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix


def pin(path):
    with path.open('rb') as f:
        return dict(path=str(path), bytes=path.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def extra_view(data, record, prefix, resolve):
    """Scoped adaptation of owned workshop_inventory.linked_prefix grammar.

    Returns all recognized extras even without 4C. BF values retain section and
    bit identity, not an invented effective-value sum. Unknown type stops parsing.
    """
    c = Reader(data, prefix['form_prefix_end'], record['end'])
    ri = prefix['next_reference_index']
    def refs(n):
        nonlocal ri
        if not 0 <= n <= len(record['refs']) - ri:
            raise ValueError('EXTRA_QUEUE_BOUNDS')
        tokens = record['refs'][ri:ri+n]
        ri += n
        return [resolve(t) for t in tokens]
    if record['flags'] & 0x80:
        refs(1)
        if not record['flags'] & 0xa6031f40:
            refs(1)
    if record['flags'] & 0x10:
        c.take(4)
    if not record['flags'] & 0xa6031f40:
        return dict(status='NO_EXTRA_DISPATCH')
    count = c.count()
    rows = []
    for _ in range(count):
        start = c.p
        tag = c.take(1)[0]
        row = dict(type=f'{tag:02x}', offset=start)
        if tag in (0x86,0xd2):
            row['references']=refs(1)
        elif tag==0x1a:
            row['references']=refs(2)
        elif tag == 0x33:
            mask=c.take(1)[0];row['flags']=mask
            if mask&1:row['word']=int.from_bytes(c.take(2),'little')
            if mask&2:
                n=c.count();bits=c.take((n*3+7)//8);row['modifications']=[]
                for i in range(n):
                    r=dict(form=refs(1)[0],flags=(int.from_bytes(bits,'little')>>(i*3))&7)
                    if r['flags']&1:r['byte_a']=c.take(1)[0]
                    if r['flags']&2:r['byte_b']=c.take(1)[0]
                    row['modifications'].append(r)
            if mask&~3:raise ValueError('UNQUALIFIED_33_FLAGS')
        elif tag == 0x22:
            row['count']=c.count()
        elif tag == 0x96:
            row['flags']=c.take(1)[0]
            if row['flags']:raise ValueError('UNQUALIFIED_96_FLAGS')
            row['string_queue_note']='Native fallback name uses separate string queue; not consumed by this reference-only reader'
        elif tag == 0x36:
            row['references']=refs(1);row['byte']=c.take(1)[0]
        elif tag == 0x37:
            row['references']=refs(c.count())
        elif tag == 0x9c:
            row['flags'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0xbc:
            n=int.from_bytes(c.take(4),'little'); row['resource_count']=n
            for _ in range(n):
                refs(1); m=int.from_bytes(c.take(4),'little'); refs(m*2); c.take(m*17)
            row['objects']=refs(c.count()); c.take(25)
        elif tag == 0xe2:
            n=c.count(); row['members']=refs(n)
        elif tag == 0xbf:
            row['sections'] = []
            for bits in (1, 3):
                n = c.count()
                mask = c.take((bits*n+7)//8)
                avs = refs(n)
                values = []
                for i in range(n*bits):
                    if mask[i//8] & (1 << (i%8)):
                        values.append(dict(av=avs[i//bits], bit=i%bits,
                                           offset=c.p, value=struct.unpack('<f', c.take(4))[0]))
                row['sections'].append(dict(bits=bits, avs=avs, values=values))
        elif tag == 0x4c:
            row['entries'] = []
            for _ in range(c.count()):
                key = refs(1)[0]
                off = c.p
                flag = c.take(1)[0]
                row['entries'].append(dict(keyword=key, target=refs(1)[0], mode=flag, offset=off))
        elif tag in (0x45, 0x83):
            row['references'] = refs(1)
        elif tag == 0x84:
            n = c.count(); row['references'] = refs(n); c.take(n)
        elif tag == 0x80:
            row['entries'] = []
            for _ in range(c.count()):
                row['entries'].append(dict(base=refs(1)[0], group=int.from_bytes(c.take(4), 'little')))
        elif tag in (0x54, 0x57, 0x2a, 0x2c):
            row['u32'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0x1f:
            row['references'] = refs(2); row['byte'] = c.take(1)[0]
        elif tag == 0x61:
            c.take(32)
        elif tag == 0xda:
            row['references'] = refs(4); row['flag'] = c.take(1)[0]
            row['references'] += refs(1); row['word'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0xcb:
            n = c.count(); row['references'] = refs(n)
            row['words_offset'] = c.p
            row['words'] = list(struct.unpack('<'+'I'*n, c.take(n*4)))
        elif tag == 0xca:
            row['string_queue_count'] = c.count()
        elif tag == 0x30:
            row['references'] = refs(1)
            row['node_count'] = c.count()
            if row['node_count']:
                row['unparsed_bytes'] = record['end'] - c.p
                rows.append(row)
                return dict(status='UNSUPPORTED_POLYMORPHIC_NODES', count=count, extras=rows,
                            next_reference_index=ri)
        elif tag == 0x0c:
            row['references'] = refs(c.count()); c.take(c.count())
        else:
            row['unparsed_bytes'] = record['end'] - start
            row['opaque_hex'] = bytes(data[start:record['end']]).hex()
            rows.append(row)
            return dict(status='UNSUPPORTED_EXTRA', count=count, extras=rows, next_reference_index=ri)
        row['end'] = c.p
        rows.append(row)
    return dict(status='COUNT_CLOSED', count=count, extras=rows,
                body_end=c.p, record_end=record['end'], next_reference_index=ri,
                queue_count=len(record['refs']))

