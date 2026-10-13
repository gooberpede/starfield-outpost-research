# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline tests: independent synthetic decisions, including adversaries."""
import copy
import struct
import unittest
from branch_inspect import path,mismatch

def event(k,seq,v=1):
    def blob(b):return dict(ok=True,length=len(b),hex=b.hex(),address=0x1234)
    argv=[0x1234]*4
    if k in (13,16):argv[2]=4
    if k==15:argv[1]=1
    blobs=dict(result=blob(struct.pack('<Q',v)),ref=blob(bytes(0x2e)+b'\x56\0'),candidate=blob(bytes(44)),source=blob(bytes(44)),translation=blob(struct.pack('<2i',-17,23)),center=blob(bytes(24) if k==18 else b'\x01'),extra=blob(bytes(0x34)),input_hierarchy=blob(struct.pack('<4Q',*argv)),context_raw=blob(struct.pack('<5Q',0x1234,0x5678,0x1234,0x5678,0x1234)),floor_xy=blob(struct.pack('<Q',0x1234)))
    if k==14:blobs['ref']['address']=v
    return dict(kind=k,sequence=seq,qpc=seq,invocation=1,parent=0,thread=2,reference=3,context=4,
                blobs=blobs)

def chain(stages,values=None):
    events=[event(k,i,(values or {}).get(k,1)) for i,k in enumerate([7]+stages+[8],1)]
    if 17 in stages and 19 not in stages:
        for e in (events[0],events[-1]):e['blobs']['center']['hex']='00'
        events[-1]['blobs']['result']['hex']='00'*8
    return events

class BranchTests(unittest.TestCase):
    def test_null_and_type(self):
        for stages,values,reason in [([13,14],{13:0,14:0},'FALLBACK_NULL'),([13,15],{15:0},'OVERLAY_NULL'),([13,15],{},'LANDSCAPE_NULL_STATIC_PATH')]:
            self.assertEqual(path(chain(stages,values),True)['reason'],reason)
        c=chain([13,14],{13:0});c[2]['blobs']['ref']['hex']='00'*0x30
        self.assertEqual(path(c,True)['reason'],'FALLBACK_TYPE_NOT_56')
    def test_equal_and_E(self):
        self.assertEqual(path(chain([13,15,16,17]),True)['reason'],'OVERLAY_BIT0_CLEAR_STATIC_PATH')
        self.assertEqual(path(chain([13,15,16,17,20,18,19]),True)['final_delta'],[-17,23])
        self.assertEqual(path(chain([13,15,16,17,20]),True)['reason'],'E_ENTERED')
    def test_ordered_mismatch_all_fields(self):
        # Expected offsets authored separately from the implementation's list.
        for o in (0,4,8,16,12,20,24,32,28,36,40):
            a=bytes(44);b=bytearray(a);b[o]=1
            self.assertEqual(mismatch(a,bytes(b)),hex(o))
        b=bytearray(44);b[12]=b[16]=1
        self.assertEqual(mismatch(bytes(44),bytes(b)),'0x10')
        b=bytearray(44);b[1]=1 # padding not compared by Q
        self.assertIsNone(mismatch(bytes(44),bytes(b)))
    def test_no_false_absence(self):
        base=chain([13,15,16,17,20,18,19])
        cases=[]
        for i in (1,3,4,6,7):cases.append(base[:i]+base[i+1:])
        c=copy.deepcopy(base);c[4]['blobs']['source']['ok']=False;cases.append(c)
        c=copy.deepcopy(base);c[3]['thread']=9;cases.append(c)
        c=copy.deepcopy(base);c[3]['sequence']=0;cases.append(c)
        c=copy.deepcopy(base);c[4]['blobs']['candidate']['hex']='01'+'00'*43;cases.append(c)
        for c in cases:self.assertEqual(path(c,True)['classification'],'UNQUALIFIED')
        self.assertEqual(path(base,False)['classification'],'UNQUALIFIED')
    def test_control_contradictions_and_samples(self):
        c=chain([13,14],{13:0,14:0});c[-1]['blobs']['result']['hex']='00'*8
        self.assertEqual(path(c,True)['reason'],'Q_return_latch_contradiction')
        c=chain([13,15,16,17]);c[-1]['blobs']['center']['hex']='01'
        c[-1]['blobs']['result']['hex']='01'+'00'*7
        self.assertEqual(path(c,True)['reason'],'missing_final_geometry_nonzero_latch')
        c=chain([13,15,16,17]);c[4]['blobs']['extra']['hex']='00'*32+'01'+'00'*19
        r=path(c,True);self.assertEqual(r['classification'],'SCOPED_PATH_RECONSTRUCTION');self.assertTrue(r['sample_path_disagreement'])
    def test_unwind_and_wrong_returns(self):
        c=chain([13,21]);c[-1]['kind']=9
        self.assertEqual(path(c,True)['classification'],'UNQUALIFIED')
        c=chain([13,15]);c[1]['blobs']['result']['ok']=False
        self.assertEqual(path(c,True)['reason'],'helper_return_missing')
if __name__=='__main__':unittest.main()
