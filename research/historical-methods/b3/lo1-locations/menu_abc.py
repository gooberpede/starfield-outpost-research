# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite nonexecuting WorkshopTargetMenu ABC inspection, stdlib only.
Reads only the ignored C1 menu asset; writes exclusive local method/string/byte
receipts. Does not execute ActionScript or alter original assets. This is a
bounded evidence aid, not a general SWF decompiler. Unknown opcodes stop a method.
"""
from pathlib import Path
import argparse
import json
import struct
import zlib

ROOT = Path.cwd()
BASE = ROOT / '.local-work/lo1-locations'
ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
cli = ap.parse_args()
assert cli.run.isalnum()
class Cursor:
    def __init__(self, b):
        self.b, self.p = b, 0
    def take(self, n):
        assert 0 <= n <= len(self.b) - self.p
        p = self.p
        self.p += n
        return self.b[p:self.p]
    def byte(self):
        return self.take(1)[0]
    def u(self):
        n = 0
        for shift in range(0, 35, 7):
            b = self.byte()
            n |= (b & 127) << shift
            if not b & 128:
                return n
        raise ValueError('unterminated variable integer')
    def s24(self):
        return int.from_bytes(self.take(3), 'little', signed=True)

b = (BASE / 'LocationsPage.swf').read_bytes()
assert b[:3] == b'CWS'
b = b[:8] + zlib.decompress(b[8:])
assert len(b) == int.from_bytes(b[4:8], 'little')
c = Cursor(b)
c.p = 8
bits = b[8] >> 3
c.take((5 + 4 * bits + 7) // 8 + 4)
abcs = []
while c.p < len(b):
    h = int.from_bytes(c.take(2), 'little')
    tag, n = h >> 6, h & 63
    if n == 63:
        n = int.from_bytes(c.take(4), 'little')
    payload = c.take(n)
    if tag == 82:
        abcs.append(payload[5 + payload[4:].index(0):])
assert len(abcs) == 1
c = Cursor(abcs[0])
version = c.take(4).hex()
ints = [0] + [c.u() for _ in range(c.u() - 1)]
uints = [0] + [c.u() for _ in range(c.u() - 1)]
doubles = [0] + [struct.unpack('<d', c.take(8))[0] for _ in range(c.u() - 1)]
ss = [''] + [c.take(c.u()).decode('utf8') for _ in range(c.u() - 1)]
ns = [''] + [str(c.byte()) + ':' + ss[c.u()] for _ in range(c.u() - 1)]
sets = [[]] + [[c.u() for _ in range(c.u())] for _ in range(c.u() - 1)]
names = ['*']
for _ in range(c.u() - 1):
    kind = c.byte()
    if kind in (7, 13):
        space, name = c.u(), c.u()
        names.append(ns[space] + '::' + ss[name])
    elif kind in (15, 16):
        names.append(ss[c.u()])
    elif kind in (17, 18):
        names.append('<runtime>')
    elif kind in (9, 14):
        name, space = c.u(), c.u()
        names.append(ss[name])
    elif kind in (27, 28):
        c.u()
        names.append('<indexed>')
    elif kind == 29:
        name = c.u()
        args = [c.u() for _ in range(c.u())]
        names.append(names[name] + '<' + ','.join(names[x] for x in args) + '>')
    else:
        raise ValueError(('multiname', kind))
methods = []
for _ in range(c.u()):
    n, result = c.u(), c.u()
    params = [c.u() for _ in range(n)]
    name, flags = ss[c.u()], c.byte()
    if flags & 8:
        for _ in range(c.u()):
            c.u(); c.byte()
    if flags & 128:
        for _ in range(n):
            c.u()
    methods.append(dict(name=name, result=names[result], params=[names[x] for x in params]))
for _ in range(c.u()):
    c.u()
    n = c.u()
    for _ in range(2 * n):
        c.u()
bindings = {}
trait_constants = []
def traits(owner):
    for _ in range(c.u()):
        name, attr = c.u(), c.byte()
        kind = attr & 15
        if kind in (0, 6):
            slot, typ, value = c.u(), c.u(), c.u()
            value_kind = c.byte() if value else 0
            if owner == '22:::OutpostEntry' and names[name].endswith('::PRECISION'):
                assert value_kind == 3
                trait_constants.append(dict(owner=owner, name=names[name],
                                            slot=slot, type=names[typ],
                                            value_kind=value_kind,
                                            int_pool_index=value, value=ints[value]))
        elif kind in (1, 2, 3):
            c.u()
            bindings[c.u()] = owner + '/' + names[name]
        elif kind in (4, 5):
            c.u(); c.u()
        else:
            raise ValueError(('trait', kind))
        if attr & 64:
            for _ in range(c.u()):
                c.u()
nclasses = c.u()
classes = []
for _ in range(nclasses):
    name = names[c.u()]
    classes.append(name)
    c.u()
    if c.byte() & 8:
        c.u()
    for _ in range(c.u()):
        c.u()
    bindings[c.u()] = name + '/<init>'
    traits(name)
for name in classes:
    bindings[c.u()] = name + '/<class-init>'
    traits(name)
for _ in range(c.u()):
    c.u(); traits('<script>')
# Operand shape and labels for the inspected AVM2 operations. Any unfamiliar
# opcode remains a positive stop, not guessed instruction alignment.
one = {0x04,0x05,0x06,0x08,0x25,0x2c,0x2d,0x2e,0x2f,0x31,0x40,0x41,0x42,
       0x49,0x53,0x55,0x56,0x58,0x59,0x5a,0x5d,0x5e,0x5f,0x60,0x61,0x62,
       0x63,0x66,0x68,0x6a,0x6c,0x6d,0x6e,0x6f,0x80,0x86,0x92,0x94,0xb2,
       0xc2,0xc3,0xf0,0xf1}
two = {0x32,0x43,0x44,0x45,0x46,0x4a,0x4c,0x4e,0x4f}
mnops = {0x04,0x05,0x45,0x46,0x4a,0x4c,0x4e,0x4f,0x59,0x5d,0x5e,0x5f,
         0x60,0x61,0x66,0x68,0x6a,0x80,0x86,0xb2}
zero = {0x01,0x02,0x03,0x07,0x09,0x1c,0x1d,0x1e,0x1f,0x20,0x21,0x23,0x26,
        0x27,0x28,0x29,0x2a,0x2b,0x30,0x47,0x48,0x50,0x51,0x52,0x57,0x64,
        0x69,0x6b,0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x77,0x78,0x81,0x82,
        0x83,0x84,0x85,0x87,0x89,0x90,0x91,0x93,0x95,0x96,0x97,0xa0,0xa1,
        0xa2,0xa3,0xa4,0xa5,0xa6,0xa7,0xa8,0xa9,0xaa,0xab,0xac,0xad,0xae,
        0xaf,0xb0,0xb1,0xb3,0xb4,0xc0,0xc1,0xc4,0xc5,0xc6,0xc7,
        0xd0,0xd1,0xd2,0xd3,0xd4,0xd5,0xd6,0xd7}
labels = {0x2c:'pushstring',0x46:'callproperty',0x4f:'callpropvoid',0x61:'setproperty',
          0x66:'getproperty',0x60:'getlex',0x5d:'findpropstrict',0x68:'initproperty',
          0x47:'returnvoid',0x48:'returnvalue',0x29:'pop',0x2a:'dup',0x24:'pushbyte',
          0x25:'pushshort',0x26:'pushtrue',0x27:'pushfalse',0x56:'newarray'}
bodies = []
for _ in range(c.u()):
    method = c.u()
    header = [c.u() for _ in range(4)]
    start = c.p
    code = c.take(c.u())
    exceptions = [[c.u() for _ in range(5)] for _ in range(c.u())]
    traits('<body>')
    binding = bindings.get(method, methods[method]['name'])
    # Limit interpretation to this menu's entry/list/resource update methods.
    d = Cursor(code)
    lines = []
    while d.p < len(code):
        pos, op = d.p, d.byte()
        args = []
        if 0x0c <= op <= 0x1a:
            args = [d.s24()]
        elif op == 0x1b:
            args = [d.s24()]
            n = d.u()
            args += [d.s24() for _ in range(n+1)]
        elif op == 0x24:
            args = [int.from_bytes(d.take(1), 'little', signed=True)]
        elif op == 0x65:
            args = [d.byte()]
        elif op == 0xef:
            args = [d.byte(),d.u(),d.byte(),d.u()]
        elif op in one:
            args = [d.u()]
        elif op in two:
            args = [d.u(),d.u()]
        elif op not in zero:
            lines.append([pos, 'UNKNOWN_STOP', hex(op)])
            break
        if op in mnops:
            args[0] = names[args[0]]
        if op in (0x2c, 0xf1):
            args[0] = ss[args[0]]
        lines.append([pos, labels.get(op, hex(op)), *args])
    bodies.append(dict(method=method, binding=binding, code_bytes=len(code), exceptions=exceptions,
                       decoded_bytes=d.p, instructions=lines))
assert c.p == len(c.b)
with (BASE / (cli.run + '.json')).open('x', encoding='utf8', newline='\n') as f:
    json.dump(dict(version=version, strings=ss, methods=bodies,
                   trait_constants=trait_constants), f, indent=2)
    f.write('\n')
print('PASS ABC framing;',len(bodies),'selected bodies;',
      sum(any(x[1]=='UNKNOWN_STOP' for x in r['instructions']) for r in bodies),'opcode gaps')
