# SPDX-License-Identifier: GPL-3.0-or-later
"""Execute bounded original map erase/clear and nested-release instructions offline.

Reads pinned installed EXE and retained native export ranges. Writes a fresh
ignored receipt. Caller-owned fixtures contain map/holder/contour chains, two independent
holders sharing one collection, or two source slots requiring chain relocation. The only substituted functions record
frees; Python retains all fixture backing. No target, save, database, deployment,
network or installed writes. Stop on any pin, disk, output, mapping or assertion
failure; preserve output and let this disposable host exit. No cleanup needed.
"""
from pathlib import Path
import ctypes as C
import faulthandler
import hashlib
import json
import re
import struct
import sys

faulthandler.enable()
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
callbacks=[sized_free,heap_free]
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

rows=[]
points,region,collection=geometry(1); mapping,slots,holder,resources=owner(collection)
clear(addr(mapping))
assert count(holder)==-1 and count(collection)==-1
expected={addr(x) for x in (points,region,collection,holder,resources)}
assert {p for p,n in frees}==expected and len(frees)==5
assert C.c_uint64.from_buffer(slots,8).value==0 and C.c_uint32.from_buffer(slots,16).value==0xffffffff
rows.append(dict(name="last-map-owner-frees-full-nested-chain",frees=len(frees),pass_native=True))
frees.clear(); points,region,collection=geometry(2); first=owner(collection); second=owner(collection)
clear(addr(first[0]))
assert count(collection)==1 and count(first[2])==-1
assert {p for p,n in frees}=={addr(first[2]),addr(first[3])}
assert C.c_uint32.from_buffer(collection,8).value==1 and C.c_uint64.from_buffer(region,32).value==addr(points)
rows.append(dict(name="independent-holder-keeps-collection-after-first-clear",collection_references=count(collection),frees=len(frees),pass_native=True))
frees.clear(); clear(addr(second[0]))
assert count(collection)==-1 and count(second[2])==-1
assert {p for p,n in frees}=={addr(points),addr(region),addr(collection),addr(second[2]),addr(second[3])}
rows.append(dict(name="last-independent-holder-releases-nested-chain",frees=len(frees),pass_native=True))
frees.clear(); empty=buf(48); clear(addr(empty)); assert not frees
rows.append(dict(name="empty-map-no-free",frees=0,pass_native=True))
frees.clear(); points,region,collection=geometry(1); mapping,slots,holder,resources=owner(collection)
assert erase(addr(mapping),0)==1
assert {p for p,n in frees}=={addr(x) for x in (points,region,collection,holder,resources)}
assert C.c_uint64.from_buffer(mapping,32).value==1 and C.c_uint32.from_buffer(slots,16).value==0xffffffff
rows.append(dict(name="terminal-chain-erase-releases-holder",frees=len(frees),pass_native=True))
frees.clear(); ga=geometry(1); gb=geometry(1); oa=owner(ga[2]); ob=owner(gb[2]); slots=buf(48); mapping=buf(48)
C.memmove(addr(slots),addr(oa[1]),24); C.memmove(addr(slots)+24,addr(ob[1]),24)
put(slots,0,"<Q",0x11110000); put(slots,24,"<Q",0x22220000)
put(slots,16,"<I",1); put(slots,40,"<I",2); put(slots,44,"<I",0)
put(mapping,16,"<Q",addr(slots)); put(mapping,24,"<Q",2)
assert erase(addr(mapping),0)==0
assert C.c_uint64.from_buffer(slots,0).value==0x22220000 and C.c_uint64.from_buffer(slots,8).value==addr(ob[2])
assert count(ob[2])==1 and count(gb[2])==1 and C.c_uint64.from_buffer(slots,32).value==0
assert {p for p,n in frees}=={addr(x) for x in (*ga,oa[2],oa[3])}
rows.append(dict(name="chain-erase-moves-survivor-without-extra-release",frees=len(frees),pass_native=True))
frees.clear(); clear(addr(mapping))
assert {p for p,n in frees}=={addr(x) for x in (*gb,ob[2],ob[3])}
rows.append(dict(name="moved-survivor-later-clear-releases-once",frees=len(frees),pass_native=True))
output.parent.mkdir(parents=True,exist_ok=True)
with output.open("x",encoding="utf-8",newline="\n") as f:
    json.dump(dict(scope="Actual native map-clear/holder/collection/point release instructions; recorder frees; owned allocation fixtures; no retail",exe_sha256=PIN,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),functions=pins,free_before=free_before,free_after=free_space(),rows=rows),f,indent=2)
print("PASS",len(rows),output)
