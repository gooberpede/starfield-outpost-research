# SPDX-License-Identifier: GPL-3.0-or-later
"""Owned emulation of the statically traced D5AH lifetime contracts.
Reads no game state. Writes a fresh ignored JSON receipt. It is not native proof.
"""
from pathlib import Path
import ctypes, hashlib, json, sys
from dataclasses import dataclass, field

def disk():
    result={}
    for drive in ("C:", "D:"):
        n=ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive+"/",ctypes.byref(n),None,None): raise OSError(drive)
        if n.value < 40000000000: raise RuntimeError((drive,n.value))
        result[drive]=n.value
    return result

@dataclass
class Contract:
    mapping: dict=field(default_factory=dict)
    visited: set=field(default_factory=set)
    references: dict=field(default_factory=dict)
    source_birth: dict=field(default_factory=dict)
    next_collection: int=0
    attempts: int=0
    def demand(self,pointer,token,birth,passed_visit=False,complete=True):
        if not passed_visit and token in self.visited: return "visited-bypass"
        if pointer in self.mapping: return "map-hit"
        self.attempts+=1; self.next_collection+=1
        c=self.next_collection; self.mapping[pointer]=(birth,c,complete)
        self.references[c]=1; self.source_birth[pointer]=birth
        self.visited.add(token)
        return "generate"
    def lease(self,pointer):
        c=self.mapping[pointer][1]; self.references[c]+=1; return c
    def release(self,c):
        self.references[c]-=1
        if not self.references[c]: del self.references[c]
    def retire(self,pointer):
        value=self.mapping.pop(pointer,None)
        if value: self.release(value[1])
        self.source_birth.pop(pointer,None)
    def reset(self):
        for p in tuple(self.mapping): self.retire(p)
        self.visited.clear()

rows=[]
def check(name,action,expected):
    got=action(); assert got==expected,(name,got,expected)
    rows.append(dict(name=name,observed=got,expected=expected,pass_contract=True))

def repeated():
    c=Contract(); a=c.demand(100,7,1); b=c.demand(100,7,1)
    return [a,b,c.attempts,len(c.mapping)]
check("same-source-retention",repeated,["generate","visited-bypass",1,1])
def contender():
    c=Contract(); a=c.demand(100,7,1); b=c.demand(100,7,1,passed_visit=True)
    return [a,b,c.attempts]
check("two-unvisited-readers-protected-map-decision",contender,["generate","map-hit",1])
def visit_without_holder():
    c=Contract(); c.demand(100,7,1); c.retire(100)
    return [c.demand(200,7,2),len(c.mapping),len(c.references),c.attempts]
check("equal-token-new-source-after-retirement",visit_without_holder,["visited-bypass",0,0,1])
def pointer_reuse(equal):
    c=Contract(); c.demand(100,7,1); c.retire(100)
    r=c.demand(100,7 if equal else 8,2)
    return [r,c.attempts,100 in c.mapping]
check("same-address-equal-token-new-birth",lambda:pointer_reuse(True),["visited-bypass",1,False])
check("same-address-different-token-new-birth",lambda:pointer_reuse(False),["generate",2,True])
def mixed(reset):
    c=Contract(); c.demand(100,7,1); lease=c.lease(100)
    c.reset() if reset else c.retire(100)
    out=[len(c.mapping),lease in c.references,7 in c.visited]
    c.release(lease); out.append(len(c.references)); return out
check("consumer-collection-lease-outlives-map-retirement",lambda:mixed(False),[0,True,True,0])
check("consumer-collection-lease-outlives-reset",lambda:mixed(True),[0,True,False,0])
def renewed():
    c=Contract(); c.demand(100,7,1); old=c.lease(100); c.reset(); r=c.demand(100,7,2)
    return [r,c.attempts,c.mapping[100][1]!=old,old in c.references]
check("reset-reconstruction-is-new-collection",renewed,["generate",2,True,True])
def partial():
    c=Contract(); c.demand(100,7,1,complete=False)
    return [c.mapping[100][2],c.demand(100,7,1),c.demand(100,7,1,passed_visit=True),c.attempts]
check("partial-output-still-visited-and-hit",partial,[False,"visited-bypass","map-hit",1])
def nonew():
    c=Contract(); c.demand(100,7,1); before=c.attempts; c.reset()
    return [c.attempts==before,len(c.mapping),len(c.visited)]
check("reset-without-subsequent-demand",nonew,[True,0,0])
# Independent set-valued event oracle: reference survival is owners minus releases.
for remove in ("retire","reset"):
    c=Contract(); c.demand(100,7,1); old=c.lease(100); c.lease(100)
    getattr(c,remove)(100) if remove=="retire" else c.reset()
    owner_set={"map","consumer-A","consumer-B"}-{ "map" }
    assert c.references[old]==len(owner_set)==2
    c.release(old); owner_set.remove("consumer-A"); assert c.references[old]==len(owner_set)==1
    c.release(old); owner_set.remove("consumer-B"); assert old not in c.references and not owner_set
    rows.append(dict(name="independent-owner-set-"+remove,pass_contract=True))
output=Path(sys.argv[1]).resolve()
root=Path(__file__).resolve().parents[2]
if not output.is_relative_to(root/".local-work") or output.exists(): raise ValueError("Fresh ignored output required")
output.parent.mkdir(parents=True,exist_ok=True)
with output.open("x",encoding="utf-8",newline="\n") as f:
    json.dump(dict(classification="EMULATED CONTRACT ONLY; no retail/native execution",code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),free=disk(),rows=rows),f,indent=2)
print("PASS",len(rows),output)
