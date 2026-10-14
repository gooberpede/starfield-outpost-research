"""SPDX-License-Identifier: GPL-3.0-or-later
Original pinned-native global envelope reader, no target/file effects.
141824020/1418236c0/141864e70. This frames envelopes, not their semantics.
Pointer units0/2 retain out-of-line targets; no invented length/queue grammar.
"""
from outpost_record_framing import Reader
from validate_mature_outposts import directory


def global_units(b):
    d=directory(b);result=[]
    #1009 follows the native unknown-mask default (zero) in this pinned build;
    # preserve that fact, rather than pretending it has a length envelope.
    zero={0,2,4,6,15,104,107,112,1001,1009}
    strings={1,3,101,102,1000}
    buffer={5,*range(7,15),16,100,103,105,106,*range(108,112),*range(113,125),*range(1002,1008)}
    for region,count in zip(('region_R1','region_R2','region_R4'),d['words'][6:9]):
        c=Reader(b,*d['regions'][region])
        for ordinal in range(count):
            at=c.p;typ=int.from_bytes(c.take(4),'little');row=dict(region=region,ordinal=ordinal,type=typ,offset=at)
            if typ==1009:row['native_mask_status']='UNKNOWN_TYPE_DEFAULT_ZERO'
            if typ in (0,2):
                target=int.from_bytes(c.take(4),'little')
                if not 0<=target<len(b):raise ValueError('GLOBAL_POINTER_BOUNDS')
                row['out_of_line_pointer']=target
            elif typ in (4,6,15,1001):
                size=int.from_bytes(c.take(4),'little');row.update(body=c.p,size=size);c.take(size)
            else:
                if typ not in zero|strings|buffer:raise ValueError(('GLOBAL_TYPE',typ,at))
                if typ in strings:
                    n=c.count();row['strings']=[int.from_bytes(c.take(2),'little') for _ in range(n)]
                if typ in strings|buffer:
                    size=int.from_bytes(c.take(4),'little');row.update(body=c.p,size=size);c.take(size)
            row['end']=c.p;result.append(row)
        if c.p!=c.end:raise ValueError(('GLOBAL_REGION_CLOSURE',region,c.p,c.end))
    return result
