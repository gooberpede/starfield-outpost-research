"""SPDX-License-Identifier: GPL-3.0-or-later
Synthetic arithmetic/prefix tests only. No files, game or semantic validation.
"""
import math
import struct
import unittest
from research_durable_center import compensated, initial_transform, model_candidates, resource_rows
from outpost_record_framing import Reader
from beacon_terrain_projection import f32, grid_centre, split_local


class DurableCenterTests(unittest.TestCase):
    def test_resource_queue_and_body_are_independent(self):
        b=struct.pack('<I',2)+bytes(34)
        q=iter(['resource','object-a','world-a','object-b','world-b'])
        rows=resource_rows(Reader(b,0,len(b)),lambda n:[next(q) for _ in range(n)],1)
        self.assertEqual(rows[0]['rows'][1]['references'],['object-b','world-b'])
        self.assertEqual(rows[0]['rows'][1]['offset'],21)

    def test_resource_count_boundary(self):
        b=struct.pack('<I',2)+bytes(17)
        with self.assertRaises(ValueError): resource_rows(Reader(b,0,len(b)),lambda n:['r']*n,1)

    def test_relocation_and_changed_beacon(self):
        a=[356.8204040527344,2459.05859375,-31.89084243774414]
        b=[337.85345458984375,2406.418701171875,-35.21407699584961]
        d=[f32(x-y) for x,y in zip(a,b)]
        self.assertEqual(compensated(b,d),a)
        self.assertNotEqual(a,b)

    def test_rounding_is_not_universal_exact_recovery(self):
        self.assertNotEqual(compensated([1e10,0,0],[-1e10+1,0,0]),[1,0,0])

    def test_invalid_vectors(self):
        for v in ([math.nan,0,0],[math.inf,0,0],[1,2]):
            with self.assertRaises(ValueError): compensated(v,[0,0,0])

    def test_negative_cell_floor(self):
        self.assertEqual(split_local(-1),(-1,99))
        self.assertEqual(split_local(-100),(-1,0))
        self.assertEqual(split_local(100),(1,0))

    def test_ambiguous_phase_survives_invariance(self):
        pair=grid_centre(1,10467,21144,native=True)
        a=model_candidates(pair,[356.8204040527344,2459.05859375,-31.89084243774414])
        self.assertEqual(a['candidate_origin'],[10464,21120])
        self.assertGreater(abs(a['phase_difference'][0]),2e-5)
        self.assertGreater(abs(a['phase_difference'][1]),3e-5)

    def test_present_rotation_and_truncation(self):
        b=bytes([4])+struct.pack('<4f',10,20,30,.2)+bytes([0x0b])
        r=dict(flags=0,body=0,end=len(b),token='800003',refs=['800001','600002','800003'])
        a=initial_transform(b,r)
        self.assertEqual(a['prefix']['xyz'],[10,20,30])
        self.assertEqual(a['initial_frame_flag'],0x0b)
        self.assertEqual([x['axis'] for x in a['rotations']],[2])
        with self.assertRaises(ValueError): initial_transform(b,dict(r,end=len(b)-2))


if __name__=='__main__': unittest.main()
