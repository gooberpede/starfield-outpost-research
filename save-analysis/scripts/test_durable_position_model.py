"""SPDX-License-Identifier: GPL-3.0-or-later
EXP0021 independent expectations, input-boundary and pathological arithmetic tests.
Stdlib only; no process/target access. Prior cases are regressions, not oracle proof.
"""
import copy
import json
from pathlib import Path
import struct
import unittest

from durable_position_model import center, reconstruct, vector

ROOT=Path(__file__).resolve().parents[2]


class PositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=json.loads((ROOT/'docs/experiments/engine-oracle/inputs.json').read_text())

    def test_controlled_invariance_and_distinction(self):
        groups={}
        for i in self.inputs:
            if i['source']['sample'] in ('Save25','Save26'):
                r=reconstruct(i)
                groups.setdefault(i['identity']['workshop_id'],[]).append((r['center_hex'],r['cell'],r['residual']))
        self.assertEqual(len(groups),2)
        self.assertTrue(all(len(g)==2 and g[0]==g[1] for g in groups.values()))
        self.assertEqual({tuple(g[0][1]) for g in groups.values()},{(1,10465,21122),(1,10467,21144)})

    def test_negative_saved_site_frame(self):
        i=next(i for i in self.inputs if i['identity']['saved_reference']=='84ede9')
        r=reconstruct(i)
        self.assertEqual(r['trace']['floor'],[-1,0])
        self.assertEqual(r['cell'],[0,13151,45120])
        self.assertEqual(r['residual'][:2],[46.5641975402832,58.03339767456055])

    def test_no_action(self):
        values=[reconstruct(i) for i in self.inputs if i['source']['sample'] in ('S1','S1C')]
        self.assertEqual(len(values),2)
        self.assertEqual([(r['center_hex'],r['cell'],r['residual']) for r in values][0],
                         [(r['center_hex'],r['cell'],r['residual']) for r in values][1])

    def test_signed_zero_vector_bypass(self):
        p=vector('000000800000008000000080')
        result,branch=center(p,(0.,-0.,0.))
        self.assertEqual(struct.pack('<3f',*result).hex(),'000000800000008000000080')
        self.assertEqual(branch,'zero-vector-copy')
        result,branch=center(p,(1.,0.,0.))
        self.assertEqual(struct.pack('<3f',*result).hex(),'0000803f0000000000000000')

    def test_seam_and_negative_boundary(self):
        i=copy.deepcopy(self.inputs[0])
        i['frame']=0x2b;i['site_cell']=[0,0,0]
        i['position_hex']=struct.pack('<3f',-0.25,-100.25,0.).hex()
        i['compensation_hex']='00'*12
        r=reconstruct(i)
        self.assertEqual(r['trace']['floor'],[-1,-2])
        self.assertEqual(r['cell'],[2,49151,49150])
        self.assertEqual(r['residual'],[99.75,99.75,0.])

    def test_reject_missing_and_expected_outputs(self):
        for field in self.inputs[0]:
            i=copy.deepcopy(self.inputs[0]);del i[field]
            with self.assertRaises(ValueError):reconstruct(i)
        i=copy.deepcopy(self.inputs[0]);i['expected_cell']=[1,1,1]
        with self.assertRaises(ValueError):reconstruct(i)

    def test_reject_unsupported_domains(self):
        for key,value in [('frame',0x3b),('frame',True),('frame',0),('exe_sha256','0'*64),
                          ('position_hex','0000807f'+'00'*8),('position_hex','01000000'+'00'*8),
                          ('position_hex',struct.pack('<3f',2**24,0.,0.).hex())]:
            i=copy.deepcopy(self.inputs[0]);i[key]=value
            with self.assertRaises(ValueError):reconstruct(i)

    def test_reject_unqualified_identity_and_missing_site(self):
        for section,field,value in [('descriptor','body','00000000'),('descriptor','world_token','000000'),
                                   ('descriptor','system_id',0),('source','decoded_sha256','unknown')]:
            i=copy.deepcopy(self.inputs[0]);i[section][field]=value
            with self.assertRaises(ValueError):reconstruct(i)
        i=copy.deepcopy(self.inputs[0]);i['frame']=0x2b;i['site_cell']=None
        with self.assertRaises(ValueError):reconstruct(i)


if __name__=='__main__':unittest.main()
