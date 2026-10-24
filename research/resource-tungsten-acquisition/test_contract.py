# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline receipt replay and frozen comparator tests; reads only, no target."""
import copy
import json
from pathlib import Path
import struct
import unittest
from admission import Tracker
from compare import discriminate, FROZEN, CORPUS

ROOT = Path(__file__).resolve().parents[2]


class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads((ROOT/'.local-work/resource-tungsten-acquisition/qualification05/good/events.json').read_text(encoding='utf8'))
        cls.samples = [r for r in cls.rows if r['kind'] == 'SAMPLE']
        cls.frozen = json.loads(FROZEN.read_text(encoding='utf8'))
        cls.corpus = json.loads(CORPUS.read_text(encoding='utf8'))

    def test_replayed_identity_mutations(self):
        # Every case starts with genuine native-copy bytes; change one join edge.
        for field in ('pid','tid','thread_lifetime','updater_token','updater_bp','temporary_set','binding_reference','raw_binding_extra'):
            with self.subTest(field=field):
                rows = copy.deepcopy(self.samples)
                value = rows[-1][field]
                rows[-1][field] = value+1 if isinstance(value, int) else '00'*len(bytes.fromhex(value))
                t = Tracker()
                self.assertFalse(any(t.feed(r) for r in rows))

    def test_loss_invalidates_pending_chain(self):
        for kind in ('EXCEPTION','LOSS','THREAD_END'):
            t = Tracker()
            for r in self.samples[:-1]:
                self.assertFalse(t.feed(r))
            t.feed(dict(kind=kind, tid=self.samples[0]['tid']))
            self.assertFalse(t.feed(self.samples[-1]))

    def test_query_frame_is_descriptor_identity(self):
        rows = copy.deepcopy(self.samples)
        rows[1]['qb_retained_bits'] = struct.pack('<fff',100,200,0).hex()
        t = Tracker()
        self.assertTrue(any(t.feed(r) for r in rows))
        # Absolute Qb may differ after indexed conversion. Descriptor mismatch fails.
        rows[1]['raw_descriptor'] = 'ff'*24
        t = Tracker()
        self.assertFalse(any(t.feed(r) for r in rows))

    def modeled(self):
        row = copy.deepcopy(self.samples[1])
        g = self.frozen['regions'][0]
        chart, ax, ay, fid = g['source'].split(':')
        frame = self.frozen['request']['descriptor']
        m = bytearray.fromhex(row['source_context']['raw_manager'])
        m[0x20] = 2
        m[0xc8] = int(chart)
        struct.pack_into('<2i',m,0xcc,*(v//192 for v in frame))
        struct.pack_into('<2i',m,0xdc,*((v%192)//12 for v in frame))
        struct.pack_into('<2i',m,0xec,*(v%12 for v in frame))
        s = bytearray.fromhex(row['source_context']['raw_source'])
        struct.pack_into('<2i',s,0x10,int(ax)-frame[0],int(ay)-frame[1])
        row['source_context']['raw_manager'] = m.hex()
        row['source_context']['raw_source'] = s.hex()
        resource = bytearray.fromhex(row['selected']['raw_resource'])
        struct.pack_into('<I',resource,40,int(g['resource'],16))
        row['selected']['raw_resource'] = resource.hex()
        row['geometry']['raw_region'] = g['native_bound_le'] + row['geometry']['raw_region'][32:]
        row['geometry']['ordered_xyzw'] = g['ordered_xyzw_le']
        return row

    def test_comparator_exact_and_different(self):
        row = self.modeled()
        result = discriminate(row,self.frozen,self.corpus)
        self.assertEqual(result['geometry'],'MATCH')
        row['geometry']['ordered_xyzw'] = 'ff'+row['geometry']['ordered_xyzw'][2:]
        self.assertEqual(discriminate(row,self.frozen,self.corpus)['geometry'],'DIFFER')

    def test_comparator_missing_family_and_unsupported_frame(self):
        row = self.modeled()
        raw = bytearray.fromhex(row['selected']['raw_resource'])
        struct.pack_into('<I',raw,40,0x57c4)
        row['selected']['raw_resource'] = raw.hex()
        result = discriminate(row,self.frozen,self.corpus)
        self.assertFalse(result['consumed_resource_represented'])
        self.assertEqual(result['geometry'],'UNSUPPORTED')
        self.assertEqual(result['earliest_mismatch'],'CONSUMED_RESOURCE_VS_MODELED_FAMILY')
        m = bytearray.fromhex(row['source_context']['raw_manager'])
        m[0xc8] = 7
        row['source_context']['raw_manager'] = m.hex()
        self.assertEqual(discriminate(row,self.frozen,self.corpus)['source_representation'],'UNSUPPORTED')


if __name__ == '__main__':
    unittest.main()
