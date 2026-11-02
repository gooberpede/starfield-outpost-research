# SPDX-License-Identifier: GPL-3.0-or-later
"""Original holder/collection release with owned typed ending probes.

Reads the pinned owned prior method/PE/exports; writes fresh ignored JSON.
Reuses its owned buffers and recording-free services. Original teardown bodies
are copied to private host pages with explicit direct-call relocation; entry
probes record typed begin/end then call those bodies. No game, save, database,
network, installed writes or deployment. STOP on pin/disk/mapping/oracle fault;
preserve failed output and exit disposable host. Fixture backing is never freed.
SOR-P-0002: adapts d5ai_ownership_native.py; not the production bridge.
"""
import sys
from pathlib import Path
import hashlib
import json
import ctypes as C
import struct
import re

root = Path(__file__).resolve().parents[2]
prior = root / 'research/resource-retained-population/d5ai_ownership_native.py'
source = prior.read_bytes()
if hashlib.sha256(source).hexdigest() != '57a3eab5f4feeeb2f7cbf9c3367b3d8d2bb8b81b95060dd4a474bcc6eb873590':
    raise ValueError('Prior method changed')
prefix = source.decode().split('proc,points,region,collection,slots,holder,resources=setup(2)', 1)[0]
n = {'__file__': str(prior), '__name__': 'owned_ending_fixture'}
exec(compile(prefix, str(prior), 'exec'), n)
globals().update({key: value for key, value in n.items() if not key.startswith('__')})
events = []
errors = []
probes = []

def instrument(entry, end, clone, kind, adjustment, export):
    native = bytearray(C.string_at(entry, end-entry))
    listing = (root / export).read_text().split('FUNCTION\t'+format(entry, 'x')+'\t', 1)[1].split('DECOMPILE', 1)[0]
    assert not re.search(r'^\w+\t[^\n]*\[0x[0-9a-f]+\]', listing, re.M), 'Unexpected RIP operand'
    for address, target in re.findall(r'^([0-9a-f]+)\tCALL 0x([0-9a-f]+)$', listing, re.M):
        address, target = int(address, 16), int(target, 16)
        offset = address-entry
        assert native[offset] == 0xe8
        struct.pack_into('<i', native, offset+1, target-(clone+offset+5))
    page(clone)
    C.memmove(clone, bytes(native), len(native))
    original = C.WINFUNCTYPE(None, C.c_void_p)(clone)
    @C.WINFUNCTYPE(None, C.c_void_p)
    def probe(receiver):
        identity = int(receiver)-adjustment
        events.append([kind, 'begin', identity])
        original(receiver)
        events.append([kind, 'end', identity])
    probes.extend([original, probe])
    old = C.c_ulong()
    assert k.VirtualProtect(entry & ~4095, 4096, 4, C.byref(old))
    C.memmove(entry, b'\x48\xb8'+struct.pack('<Q', C.cast(probe, C.c_void_p).value)+b'\xff\xe0', 12)
    assert k.VirtualProtect(entry & ~4095, 4096, 0x20, C.byref(old))
    assert k.VirtualProtect(clone & ~4095, 4096, 0x20, C.byref(old))

instrument(0x1407aab10, 0x1407aabc5, 0x1407b8000, 'holder-ending', 0x10,
           '.local-work/d5ah-extractor/export02/native.tsv')
instrument(0x1407ac260, 0x1407ac2e3, 0x1407b9000, 'collection-ending', 8,
           '.local-work/d5s/export08/native.tsv')
assert k.FlushInstructionCache(k.GetCurrentProcess(), None, 0)
release_holder = C.WINFUNCTYPE(None, C.c_void_p)(0x1407ab6a0)
replace_collection = C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p)(0x1407aabd0)
rows = []

def ends(kind):
    return [e[2] for e in events if e[:2] == [kind, 'begin']]

def record(name, holder, collections, expected_holder, expected_collections):
    assert ends('holder-ending') == expected_holder, (name, events)
    assert ends('collection-ending') == expected_collections, (name, events)
    assert len(events) == 2 * (len(expected_holder)+len(expected_collections))
    rows.append(dict(case=name, events=list(events), holder_refs=count(holder),
                     collection_refs=[count(c) for c in collections],
                     frees=list(frees)))

proc, points, region, collection, slots, holder, resources = setup(1)
put(holder, 0, '<I', 2)
events.clear(); frees.clear()
assert erase(addr(proc)+16, 0) == 1 and query(proc, (0, 0, 0)) == []
record('external-holder-survives-map-erase', holder, [collection], [], [])
assert count(holder) == 1 and count(collection) == 1
external = buf(24); put(external, 8, '<Q', addr(holder))
release_holder(addr(external))
record('external-holder-final-release-ends-holder-and-collection', holder,
       [collection], [addr(holder)], [addr(collection)])

proc, points, region, collection, slots, holder, resources = setup(2)
events.clear(); frees.clear()
assert erase(addr(proc)+16, 0) == 1 and query(proc, (0, 0, 0)) == []
record('external-collection-survives-final-holder-release', holder,
       [collection], [addr(holder)], [])
assert count(collection) == 1 and C.c_uint64.from_buffer(region, 32).value == addr(points)
retained = buf(8); empty = buf(8); put(retained, 0, '<Q', addr(collection))
replace_collection(addr(retained), addr(empty))
record('last-external-collection-release-ends-nested-storage', holder,
       [collection], [addr(holder)], [addr(collection)])
assert C.c_uint32.from_buffer(collection, 8).value == 0
assert C.c_uint64.from_buffer(collection, 16).value == 0

proc, points, region, collection, slots, holder, resources = setup(2)
p2, r2, c2 = geometry(1)
two = buf(48); C.memmove(addr(two), addr(resources), 24)
put(two, 24, '<I', 0x57d5); put(two, 32, '<Q', addr(c2)); put(two, 40, '<I', 2)
put(holder, 32, '<Q', addr(two)); put(holder, 40, '<Q', 2)
events.clear(); frees.clear()
assert erase(addr(proc)+16, 0) == 1
record('partial-constituent-survival-is-not-whole-population-survival', holder,
       [collection, c2], [addr(holder)], [addr(c2)])
assert count(collection) == 1 and count(c2) == -1

proc, points, region, collection, slots, holder, resources = setup(1)
put(collection, 8, '<I', 0); put(collection, 12, '<I', 0); put(collection, 16, '<Q', 0)
events.clear(); frees.clear()
assert erase(addr(proc)+16, 0) == 1
record('empty-collection-still-emits-ending-before-outer-free', holder,
       [collection], [addr(holder)], [addr(collection)])

proc, points, region, collection, slots, holder, resources = setup(1)
old_identity = addr(collection)
events.clear(); frees.clear(); assert erase(addr(proc)+16, 0) == 1
old_events = list(events)
put(collection, 0, '<I', 1); put(collection, 8, '<I', 1)
put(collection, 12, '<I', 1); put(collection, 16, '<Q', addr(region))
assert addr(collection) == old_identity and old_identity in ends('collection-ending')
rows.append(dict(case='same-address-reinitialized-after-native-ending-is-new-lifetime',
                 old_identity=old_identity, events=old_events, old_identity_retained=False))
def continuity(identity, kind, journal, lost=False):
    if lost:
        return False
    return not any(e[0] == kind and e[2] == identity for e in journal)
assert not continuity(old_identity, 'collection-ending', old_events)
assert not continuity(old_identity, 'collection-ending', [], lost=True)
assert not continuity(old_identity, 'collection-ending', [['collection-ending', 'begin', old_identity]])
rows.append(dict(case='lost-or-unmatched-ending-history-refuses-continuity',
                 lost_record=True, unmatched_begin=True, continuity_qualified=False,
                 label='Owned admission oracle; not native transport execution'))
assert not errors and not resolver_errors
output.write_text(json.dumps(dict(scope=__doc__, rows=rows,
    method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    prior_method_sha256=hashlib.sha256(source).hexdigest(), executable_sha256=PIN,
    free_before=free_before, free_after=free_space()), indent=2)+'\n',
    encoding='utf8', newline='\n')
print('PASS', len(rows), output)
