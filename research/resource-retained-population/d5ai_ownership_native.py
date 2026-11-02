# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute bounded original map erase/clear and nested-release instructions offline.

Reads pinned installed EXE and retained native export ranges. Writes a fresh
ignored receipt. Caller-owned fixtures contain map/holder/contour chains and
preallocated output vectors. This D5AI adaptation executes the original point-map
scan, point predicate, map erase and nested destructors. Form-resolution and
recording-free callbacks substitute their surrounding game services; Python
retains all fixture backing. No target, save, database, deployment, network or
installed writes occur. Stop on any pin, disk, output, mapping or assertion
failure; preserve output and let this disposable host exit. No cleanup needed.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B without -O/-OO')
from pathlib import Path
import ctypes as C
import faulthandler
import hashlib
import json
import re
import struct
import sys

faulthandler.enable()
if C.sizeof(C.c_void_p)!=8: raise RuntimeError('Windows x64 required')
ROOT=Path(__file__).resolve().parents[2]
EXE=Path("C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe")
PIN="7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28"
output=Path(sys.argv[1]).resolve()
assert output.is_relative_to(ROOT/".local-work") and not output.exists()

def free_space():
    result={}
    for drive in ("C:/","D:/"):
        n=C.c_ulonglong()
        assert C.windll.kernel32.GetDiskFreeSpaceExW(drive,C.byref(n),None,None)
        assert n.value>=40000000000,(drive,n.value)
        result[drive]=n.value
    return result

free_before=free_space()
data=EXE.read_bytes(); assert hashlib.sha256(data).hexdigest()==PIN
pe=struct.unpack_from("<I",data,0x3c)[0]
base=struct.unpack_from("<Q",data,pe+48)[0]; assert base==0x140000000
opt=struct.unpack_from("<H",data,pe+20)[0]
sections=[struct.unpack_from("<IIII",data,pe+24+opt+i*40+8) for i in range(struct.unpack_from("<H",data,pe+6)[0])]
k=C.WinDLL("kernel32",use_last_error=True)
k.SetErrorMode(0x8003)
k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong]; k.VirtualAlloc.restype=C.c_void_p
k.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.POINTER(C.c_ulong)]
k.GetCurrentProcess.restype=C.c_void_p
k.FlushInstructionCache.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
pages=set(); code=set(); pins=[]

def page(va):
    p=va&~4095
    if p not in pages:
        gran=p&~65535
        if not any(q&~65535==gran for q in pages): assert k.VirtualAlloc(gran,65536,0x2000,4)==gran
        assert k.VirtualAlloc(p,4096,0x1000,4)==p
        for vs,rva,size,raw in sections:
            lo,hi=max(p,base+rva),min(p+4096,base+rva+size)
            if lo<hi: C.memmove(lo,data[raw+lo-base-rva:raw+hi-base-rva],hi-lo)
        pages.add(p)
    return p

def load(path,expected,entries):
    b=(ROOT/path).read_bytes(); assert hashlib.sha256(b).hexdigest()==expected
    text=b.decode("utf-8-sig")
    for entry in entries:
        chunk=text.split("FUNCTION\t"+entry+"\t",1)[1].split("END_FUNCTION",1)[0]
        spans=re.findall(r"\[([0-9a-f]+), ([0-9a-f]+)\]",chunk.splitlines()[0]); assert spans
        for a,z in spans:
            lo,hi=int(a,16),int(z,16)
            for p in range(lo&~4095,(hi+4096)&~4095,4096): page(p); code.add(p)
        pins.append(dict(entry="0x"+entry,path=path,export_sha256=expected))

load(".local-work/d5ah-extractor/export02/native.tsv","647a07d95df2f3301e0596dda4fecad148f3063ea35178f1610094fa79fc3911",["1407aa8a0","1407aab10"])
load(".local-work/d5ah-extractor/export03/native.tsv","e05a852f559876a0faa23116ccce7def61122de645a882a001ef229b1667af47",["1407ab6a0"])
load(".local-work/d5ah-extractor/export02/native.tsv","647a07d95df2f3301e0596dda4fecad148f3063ea35178f1610094fa79fc3911",["140975030"])
load(".local-work/d5s/export08/native.tsv","fd0cbc75eaf2575de30acb5068087da0dcfbb0b8fdc5b9fcf60c7287fe42b081",["1407ac260"])
frees=[]
@C.WINFUNCTYPE(None,C.c_void_p,C.c_size_t,C.c_void_p)
def sized_free(p,size,arg): frees.append([int(p or 0),int(size)])
@C.WINFUNCTYPE(None,C.c_void_p)
def heap_free(p): frees.append([int(p or 0),None])
# Additional original point-reader, predicate and uncontended lock helper.
load('.local-work/d5v/export04/native.tsv','c2e4216835dbd41e6dc16a3a1b3c911b773ab63a70299e4045b864698b31510e',['14079df70'])
load('.local-work/d5v/export05/native.tsv','449f6e9f8678d93870bd7825f590af31632b8a128971ba9ed8611b76c4d43658',['1407affb0'])
# Predicate/lock ranges are authenticated by their complete retained export bytes.
extra = [('.local-work/d5v/export06/native.tsv', '142346b30', 'a5293312d9c74c581e8a14884447ce852bb8c0ca3cf0bcc801807405ad795152'),
         ('.local-work/d5af/prelock-export01/native.tsv', '1422cc350', 'bad793664b90b987bd5dc4d91fb70936a2d9590029b17dc2eb7e7d1e2c807b47')]
for path, entry, expected in extra:
    raw=(ROOT/path).read_bytes()
    load(path,expected,[entry])
    text=raw.decode('utf8'); chunk=text.split('FUNCTION\t'+entry+'\t',1)[1].split('DECOMPILE',1)[0]
    for address in re.findall(r'\[0x([0-9a-f]+)\]',chunk): page(int(address,16))
ires=C.create_string_buffer(0x120); C.c_uint8.from_buffer(ires,0x2e).value=0x9f
ires2=C.create_string_buffer(0x120); C.c_uint8.from_buffer(ires2,0x2e).value=0x9f
resolver_errors=[]
@C.WINFUNCTYPE(C.c_void_p,C.c_uint32)
def resolve(identity):
    if identity==0x57d4: return C.addressof(ires)
    if identity==0x57d5: return C.addressof(ires2)
    resolver_errors.append(identity)
    return 0
page(0x1405de3b0); C.memmove(0x1405de3b0,b'\x48\xb8'+struct.pack('<Q',C.cast(resolve,C.c_void_p).value)+b'\xff\xe0',12); code.add(0x1405de000)
callbacks=[sized_free,heap_free,resolve]
page(0x143a3f418)
C.c_uint64.from_address(0x143a3f418).value=C.cast(k.GetCurrentThreadId,C.c_void_p).value
for va,callback in ((0x1402ba340,sized_free),(0x14365cdb0,sized_free),(0x1402b7910,heap_free)):
    page(va); C.memmove(va,b"\x48\xb8"+struct.pack("<Q",C.cast(callback,C.c_void_p).value)+b"\xff\xe0",12); code.add(va&~4095)
for p in code:
    old=C.c_ulong(); assert k.VirtualProtect(p,4096,0x20,C.byref(old))
assert k.FlushInstructionCache(k.GetCurrentProcess(),None,0)
clear=C.WINFUNCTYPE(None,C.c_void_p)(0x1407aa8a0)
erase=C.WINFUNCTYPE(C.c_uint64,C.c_void_p,C.c_uint64)(0x140975030)
buffers=[]
def buf(size):
    x=C.create_string_buffer(size); buffers.append(x); return x

def put(x,at,fmt,value): struct.pack_into(fmt,x,at,value)
def addr(x): return C.addressof(x)
def count(x): return C.c_int32.from_buffer(x).value

def geometry(owners):
    points=buf(16); region=buf(48); collection=buf(24)
    put(region,24,"<I",1); put(region,28,"<I",1); put(region,32,"<Q",addr(points))
    put(collection,0,"<I",owners); put(collection,8,"<I",1); put(collection,12,"<I",1); put(collection,16,"<Q",addr(region))
    return points,region,collection

def owner(collection):
    resource_slots=buf(24); holder=buf(64); map_slots=buf(24); mapping=buf(48)
    put(resource_slots,0,"<I",0x57d4); put(resource_slots,8,"<Q",addr(collection)); put(resource_slots,16,"<I",1)
    put(holder,0,"<I",1); put(holder,32,"<Q",addr(resource_slots)); put(holder,40,"<Q",1)
    put(map_slots,0,"<Q",0x12345000); put(map_slots,8,"<Q",addr(holder)); put(map_slots,16,"<I",1)
    put(mapping,16,"<Q",addr(map_slots)); put(mapping,24,"<Q",1)
    return mapping,map_slots,holder,resource_slots


# Preallocated output prevents the point reader from invoking a game allocator.
query_native=C.WINFUNCTYPE(None,C.c_void_p,C.c_void_p,C.c_void_p)(0x14079df70)
rows=[]
def query(proc,xyz):
    q=buf(12); struct.pack_into('<3f',q,0,*xyz)
    values=buf(32); vector=buf(24)
    for offset,value in ((0,addr(values)),(8,addr(values)),(16,addr(values)+32)):
        put(vector,offset,'<Q',value)
    query_native(addr(proc),addr(q),addr(vector))
    end=C.c_uint64.from_buffer(vector,8).value
    return [C.c_uint64.from_buffer(values,i).value for i in range(0,end-addr(values),8)]

def setup(owners):
    points,region,collection=geometry(owners)
    struct.pack_into('<4f',points,0,0,0,0,2)
    struct.pack_into('<4f',region,0,0,0,0,3)
    mapping,slots,holder,resources=owner(collection)
    proc=buf(96); C.memmove(addr(proc)+16,addr(mapping),48)
    return proc,points,region,collection,slots,holder,resources

proc,points,region,collection,slots,holder,resources=setup(2)
assert query(proc,(0,0,0))==[C.addressof(ires)] and count(collection)==2
rows.append(dict(case='resident-holder-point-admission',admitted=1,references_after=count(collection)))
assert query(proc,(100,100,0))==[] and count(collection)==2
rows.append(dict(case='resident-holder-geometric-nonadmission',admitted=0,references_after=count(collection)))
assert erase(addr(proc)+16,0)==1
assert count(collection)==1 and count(holder)==-1
assert query(proc,(0,0,0))==[]
assert C.c_uint32.from_buffer(collection,8).value==1
assert C.c_uint64.from_buffer(region,32).value==addr(points)
rows.append(dict(case='map-erased-external-collection-alive-not-exposed',admitted=0,references_after=count(collection)))
proc,points,region,collection,slots,holder,resources=setup(1)
assert query(proc,(0,0,0))==[C.addressof(ires)]
assert erase(addr(proc)+16,0)==1 and count(collection)==-1
assert query(proc,(0,0,0))==[]
rows.append(dict(case='final-owner-erased-point-scan-empty',admitted=0,references_after=count(collection)))
proc=buf(96)
assert query(proc,(0,0,0))==[]
rows.append(dict(case='empty-procgen-completed-query',admitted=0))
proc,points,region,collection,slots,holder,resources=setup(2)
two=buf(48); C.memmove(addr(two),addr(resources),24)
C.memmove(addr(two)+24,addr(resources),24)
put(two,24,'<I',0x57d5); put(two,40,'<I',2)
put(holder,32,'<Q',addr(two)); put(holder,40,'<Q',2)
first=query(proc,(0,0,0))
old=C.string_at(addr(two),48)
C.memmove(addr(two),old[24:]+old[:24],48)
second=query(proc,(0,0,0))
assert first==[addr(ires),addr(ires2)] and second==[addr(ires2),addr(ires)]
assert sorted(first)==sorted(second) and count(collection)==2
rows.append(dict(case='resource-slot-order-changes-vector-order-not-membership',admitted=2,reversed=True))
put(proc,64,'<I',k.GetCurrentThreadId()); put(proc,68,'<I',0x401000)
assert sorted(query(proc,(0,0,0)))==sorted(first)
assert C.c_uint32.from_buffer(proc,68).value==0x401000
rows.append(dict(case='same-thread-exclusive-allows-query-reader',state_after='0x00401000',complete_snapshot_must_refuse=True))
assert not resolver_errors
output.parent.mkdir(parents=True,exist_ok=True)
with output.open('x',encoding='utf8',newline='\n') as f:
    json.dump(dict(scope='Original point map/collection scan, point predicate and map erase; uncontended original shared lock. Resolver/free callbacks use owned fixture objects; no retail or full provider.',
                   executable_sha256=PIN,method_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   inherited_method='research/resource-retained-population/d5ah_lifecycle_native.py',
                   inherited_sha256=hashlib.sha256((ROOT/'research/resource-retained-population/d5ah_lifecycle_native.py').read_bytes()).hexdigest(),
                   functions=pins,free_before=free_before,free_after=free_space(),rows=rows),f,indent=2)
print('PASS',len(rows),output)

