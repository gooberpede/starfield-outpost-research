"""SPDX-License-Identifier: GPL-3.0-or-later
Original owned parser extended for negative investigation. Reads decoded bytes
only, stdlib/project; no file or target effects. Retains decoded earlier extras
when later unsupported input prevents closure, even without4C. Unknown bytes
are NEVER skipped or scanned. Actual FormType selects actor dispatchmask.
Copied from preserved workshop_inventory.linked_prefix with this explicit
change; older schema and raw evidence remain untouched.
"""
from outpost_record_framing import Reader

def partial_extras(b, r, prefix):
    """Consume supported modern counted extras without byte searching.
    1419aeff0 BF masks; 140562ef0 keyed entries. Unknown trailing types retain
    decoded edges with NOT_DECODED status. CLOSED does not prove load defaults.
    """
    c = Reader(b, prefix['form_prefix_end'], r['end'])
    ri = prefix['next_reference_index']
    si=len(prefix.get('component',{}).get('strings',[]))
    def strings(n):
        nonlocal si
        if not 0<=n<=len(r['strings'])-si: raise ValueError('EXTRA_STRING_QUEUE_BOUNDS')
        si+=n
    def refs(n):
        nonlocal ri
        if not 0 <= n <= len(r['refs']) - ri: raise ValueError('EXTRA_QUEUE_BOUNDS')
        result = r['refs'][ri:ri+n]
        ri += n
        return result
    if r['flags'] & 0x80:
        refs(1)  # 140b29990 -> 1405631e0, no body bytes
        if not r['flags'] & (0xa6071b40 if r["form_type"] == 0x4b else 0xa6031f40): refs(1)
    if r['flags'] & 0x10: c.take(4)
    if not r['flags'] & (0xa6071b40 if r["form_type"] == 0x4b else 0xa6031f40): raise ValueError('NO_EXTRA_DISPATCH')
    types, alternate_groups, packin, entries = [], [], [], []
    extra_flags = None
    total = c.count()
    first_link = None
    def result(closed, gap=None):
        return dict(entries=entries, start=first_link, end=c.p, types=types,
            alternate_groups=alternate_groups, packin=packin,extra_flags=extra_flags,
            following_extras='CLOSED' if closed else 'NOT_DECODED',
            extra_count=total, decoded_extra_count=len(types)-(1 if gap else 0),
            following_gap=gap, next_reference_index=ri)
    for _ in range(total):
        start = c.p
        typ = c.take(1)[0]
        if typ in types: raise ValueError('DUPLICATE_EXTRA_TYPE_%02X' % typ)
        types.append(typ)
        if typ == 0xfd: pass  # 14051ea30/140521620: zero-payload constructor14053fde0
        elif typ == 0x9c: extra_flags=int.from_bytes(c.take(4),'little')
        elif typ in (0x45, 0x83): refs(1)
        elif typ in (0x54,0x57): c.take(4)
        elif typ == 0x2a: c.take(4)
        elif typ == 0x1f: refs(2); c.take(1)
        elif typ == 0x0c:
            refs(c.count()); c.take(c.count())
        elif typ == 0x61: c.take(32)
        elif typ == 0x81:
            refs(1); c.take(4); refs(1); c.take(16)
        elif typ == 0xca:
            strings(c.count())  # qualified modern >=4 string-queue branch
        elif typ == 0xde:
            n=c.count()
            if n>len(r['refs'])-ri: raise ValueError('DE_GROUP_QUEUE_BOUNDS')
            for _ in range(n):
                refs(1); rows=c.count()
                if rows>(c.end-c.p)//8: raise ValueError('DE_ROW_BOUNDS')
                c.take(rows*8)
        elif typ == 0x30:
            refs(1)
            if c.count():
                gap='EXTRA_30_NONEMPTY_POLYMORPHIC_NODES'
                return result(False,gap)
        elif typ == 0x96:
            flags=c.take(1)[0]
            for bit in (1,2,4):
                if flags&bit: refs(1)
            value=(c.count() if flags&0x80 else int.from_bytes(c.take(4),'little')) if flags&8 else 0xfffffffe
            if flags&0x10: c.take(2)
            if flags&6 and value==0xfffffffe:
                gap='EXTRA_96_RESOLUTION_DEPENDENT_STRING'
                return result(False,gap)
            if not flags&6 and value==0xfffffffe: strings(1)
            if flags&0x20:
                n=c.count(); strings(n); c.take(n*4)
            if flags&0x40:
                n=c.count(); strings(n); refs(n)
        elif typ == 0xbc:
            n=int.from_bytes(c.take(4),'little')
            if n>(c.end-c.p)//4: raise ValueError('WORKSHOP_RESOURCE_GROUP_BOUNDS')
            for _ in range(n):
                refs(1); rows=int.from_bytes(c.take(4),'little')
                if rows>(c.end-c.p)//17: raise ValueError('WORKSHOP_RESOURCE_ROW_BOUNDS')
                refs(rows*2); c.take(rows*17)
            refs(c.count()); c.take(1); strings(1); c.take(24)
        elif typ == 0xcb:
            n=c.count(); refs(n); c.take(n*4)
        elif typ == 0xda:
            tokens=refs(4); flag_offset=c.p; flag=c.take(1)[0]
            tokens+=refs(1); word_offset=c.p; word=int.from_bytes(c.take(4),'little')
            packin.append(dict(tokens=tokens,flag68=flag,flag_offset=flag_offset,
                word64=word,word_offset=word_offset,start=start))
        elif typ == 0x84:
            n = c.count(); refs(n); c.take(n)
        elif typ == 0xbf:
            for bits in (1, 3):
                n = c.count()
                mask = c.take((bits*n + 7)//8)
                refs(n)
                c.take(4*sum(bool(mask[i//8] & (1 << (i%8))) for i in range(bits*n)))
        elif typ == 0x4c:
            if first_link is None: first_link=start
            n = c.count()
            if n > len(r['refs'][ri:])//2: raise ValueError('LINKED_QUEUE_BOUNDS')
            for i in range(n):
                keyword_index = ri
                key = refs(1)[0]
                flag_offset = c.p
                flag = c.take(1)[0]
                target = refs(1)[0]
                entries.append(dict(keyword_token=key, target_token=target,
                    keyword_queue_index=keyword_index, target_mode=flag,
                    flag_offset=flag_offset, entry_index=i))
        elif typ == 0x80:
            n=c.count()
            if n>len(r['refs'])-ri or n>(c.end-c.p)//4: raise ValueError('GROUP80_BOUNDS')
            for i in range(n):
                base=refs(1)[0]; offset=c.p
                group=int.from_bytes(c.take(4),'little')
                alternate_groups.append(dict(base_token=base, group_index=group,offset=offset))
        else:
            gap='EXTRA_%02X_UNSUPPORTED' % typ
            return result(False,gap)
    return result(True)
