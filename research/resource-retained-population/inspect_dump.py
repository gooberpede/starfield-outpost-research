# SPDX-License-Identifier: GPL-3.0-or-later
"""Inspect one existing D5L minidump without executing or changing its contents.

Reads the explicitly supplied dump and READY using installed SDK structure layouts;
writes a new local metadata receipt. No symbol downloads, debugger, live target,
save or Git operations. Only identity-qualified metadata is interpreted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def inspect(path, ready):
    b = path.read_bytes()
    def u(fmt, at):
        assert 0 <= at <= len(b)-struct.calcsize(fmt)
        return struct.unpack_from(fmt, b, at)
    assert b[:4] == b'MDMP'
    _, version, count, directory, checksum, timestamp, flags = u('<6IQ', 0)
    streams = {}
    for i in range(count):
        kind, size, rva = u('<3I', directory+12*i)
        if kind == 0 and size == 0:
            continue
        assert rva+size <= len(b) and kind not in streams
        streams[kind] = (size, rva)
    _, misc = streams[15]
    size, valid, pid, born, user, kernel = u('<6I', misc)
    session = ready['session']
    assert valid & 3 == 3
    assert pid == session['pid']
    assert born == session['creation_filetime_100ns']//10_000_000-11644473600
    modules = []
    _, at = streams[4]
    for i in range(u('<I', at)[0]):
        m = at+4+108*i
        base, length, check, stamp, name = u('<Q4I', m)
        n = u('<I', name)[0]
        label = b[name+4:name+4+n].decode('utf-16-le')
        modules.append(dict(base=base, size=length, timestamp=stamp, path=label))
    module = next(m for m in modules if Path(m['path']).name.lower() == 'starfield.exe')
    assert module['base'] == session['module_base']
    _, at = streams[6]
    tid, unused, code, exception_flags, nested, address = u('<4I2Q', at)
    context_size, context_at = u('<2I', at+160)
    context = b[context_at:context_at+context_size]
    assert len(context) == context_size and context_size >= 0x100
    rip = struct.unpack_from('<Q', context, 0xf8)[0]
    eflags = struct.unpack_from('<I', context, 0x44)[0]
    ranges = []
    if 5 in streams:
        _, at = streams[5]
        for i in range(u('<I', at)[0]):
            va, n, loc = u('<Q2I', at+4+16*i)
            ranges.append((va, n, loc))
    if 9 in streams:
        _, at = streams[9]
        n, loc = u('<2Q', at)
        for i in range(n):
            va, length = u('<2Q', at+16+16*i)
            ranges.append((va, length, loc)); loc += length
    def memory(va, n):
        for start, length, loc in ranges:
            if start <= va and va+n <= start+length:
                return b[loc+va-start:loc+va-start+n].hex()
        return None
    _, at = streams[3]
    threads = []
    for i in range(u('<I', at)[0]):
        t = at+4+48*i
        thread_id, suspend_count, priority_class, priority = u('<4I', t)
        threads.append(dict(tid=thread_id, suspend_count=suspend_count))
    return dict(schema='sor-d5m-dump/1', path=str(path), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
        stream_types=sorted(streams), pid=pid, creation_unix_seconds=born,
        creation_precision='one second; matches exact READY FILETIME truncated to seconds',
        dump_timestamp_unix_seconds=timestamp, module=module, thread=tid,
        exception_code=hex(code), exception_address=hex(address), exception_rva=hex(address-module['base']),
        rip=hex(rip), eflags=hex(eflags), tf=bool(eflags & 0x100),
        site_bytes=memory(address,16), rip_bytes=memory(rip,16), threads=threads,
        limits='No debugger continuation trail or first/second-chance flag in this exception stream; absent memory is UNKNOWN.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('dump','ready','output'): p.add_argument('--'+name,type=Path,required=True)
    a = p.parse_args()
    result = inspect(a.dump, json.loads(a.ready.read_text()))
    with a.output.open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2); f.write('\n')
    print({k:v for k,v in result.items() if k not in ('threads','module')})


if __name__ == '__main__': main()
