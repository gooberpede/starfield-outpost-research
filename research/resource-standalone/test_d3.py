# SPDX-License-Identifier: GPL-3.0-or-later
"""D3 branch and missing-operand controls; stdlib, no target or file writes."""
import copy
import unittest
from unittest.mock import patch
from types import SimpleNamespace as NS
import struct

from test_predictor import fixture
import predictor_d3 as p
from corpus_d3 import ordinary


class D3Tests(unittest.TestCase):
    def fixture(self):
        c,q = fixture()
        c['schema'] = p.SCHEMA
        for b in c['bodies']['00000001']['biomes'].values():
            b['status'] = 'ORDINARY_AND_SPECIAL'
        return c,q

    def test_d1_schema_is_not_silently_upgraded(self):
        c,q = fixture()
        self.assertEqual(p.predict(p.seal(c),q)['reason'],'INCOMPATIBLE_CORPUS')

    def test_special_pass_uses_high_nibble_after_ordinary(self):
        for mask,weight in ((4,0.3),(20,1.0)):
            c,q = self.fixture()
            c['settings'][5] = 0.3
            for tile in c['bodies']['00000001']['tiles'].values():
                tile[3] = mask
            c['bodies']['00000001']['biomes']['biome']['resources'].append(
                dict(id='special',rarity=5,block='test',branch='special'))
            calls = []
            def record(request,constants):
                calls.append(copy.deepcopy(request['ordered_resources']))
                return dict(status='CONDITIONAL_PLANAR_SOURCE',regions=[])
            with patch.object(p.geometry,'populate_source',side_effect=record):
                result = p.predict(p.seal(c),q)
            self.assertEqual(result['status'],'CONDITIONAL_GEOMETRY')
            self.assertTrue(calls)
            self.assertTrue(all([v['resource'] for v in call]==['authored','special'] for call in calls))
            self.assertTrue(all(call[-1]['weight']==weight for call in calls))

    def test_nonuniform_mask_requires_first_construction_query(self):
        c,q = self.fixture()
        c['bodies']['00000001']['tiles']['0:99:99'][3] = 8
        result = p.predict(p.seal(c),q)
        self.assertEqual(result['status'],'PARTIAL')
        self.assertTrue(any(r['reason']=='MISSING_FIRST_CONSTRUCTION_QUERY_MASK' for r in result['failures']))

    def test_special_order_and_rarity_are_required(self):
        for tail in ((dict(id='special',rarity=4,block='test',branch='special'),),
                     (dict(id='special',rarity=5,block='test',branch='special'),dict(id='late',rarity=0,block='test'))):
            c,q = self.fixture()
            c['bodies']['00000001']['biomes']['biome']['resources'].extend(tail)
            self.assertEqual(p.predict(p.seal(c),q)['status'],'UNKNOWN')

    def test_missing_full_mask_is_not_defaulted(self):
        c,q = self.fixture()
        c['bodies']['00000001']['tiles']['0:99:99'].pop()
        self.assertEqual(p.predict(p.seal(c),q)['reason'],'TILE_DOMAIN')

    def corpus_fixture(self):
        def blob(value):
            return struct.pack('<140f',*([value]*140))
        def rsgd(entries):
            return (None,[(tag,b) for fid,value in entries for tag,b in
                ((b'RNAM',fid.to_bytes(4,'little')),(b'DNAM',blob(value)))])
        family = NS(root=NS(form_id='1'),emitted_form_ids=['1'])
        def view(biome,rid,special=None):
            return NS(orchestration=NS(biome=NS(form_id=f'{biome:x}'),
                effective_rsgd=NS(form_id=f'{rid:x}',entries=[]),special_selection=special),
                common_assignment=NS(family=family,mechanism='SYNTHETIC_FALLBACK'),family_access=None)
        records = {1:(None,[(b'SNAM',b'\0')]),2:(None,[(b'SNAM',b'\5')]),
            10:(None,[(b'RNAM',(21).to_bytes(4,'little'))]),20:rsgd([(99,2.0)]),
            21:rsgd([(1,3.0),(2,4.0)])}
        v = view(10,20,NS(form_id='2'))
        return records,NS(biome_results=[v],planet=NS(resource_creation_seed=0),final_draw_count=0),view,rsgd

    def test_current_biome_descriptor_precedes_other_components(self):
        records,prediction,view,rsgd = self.corpus_fixture()
        blocks = {}
        result,detail = ordinary(records,prediction,10,blocks)
        self.assertEqual(detail['descriptor_route'],'CURRENT_BIOME_RNAM')
        self.assertEqual(blocks[result['resources'][0]['block']],[3.0]*8)
        self.assertEqual(blocks[result['resources'][-1]['block']],[4.0]*8)

    def test_different_alternate_descriptors_are_not_fitted(self):
        records,prediction,view,rsgd = self.corpus_fixture()
        records[21] = rsgd([(99,2.0)])
        prediction.biome_results[0].orchestration.special_selection = None
        for biome,rid,value in ((11,22,3.0),(12,23,4.0)):
            records[biome]=(None,[(b'RNAM',rid.to_bytes(4,'little'))])
            records[rid]=rsgd([(1,value)])
            prediction.biome_results.append(view(biome,rid))
        with self.assertRaisesRegex(ValueError,'UNRESOLVED_ALTERNATE_COMPONENT_DESCRIPTOR_ORDER'):
            ordinary(records,prediction,10,{})

    def test_invariant_alternate_descriptor_and_first_fallback(self):
        for alternate in (False,True):
            records,prediction,view,rsgd = self.corpus_fixture()
            records[21]=rsgd([(99,2.0)])
            prediction.biome_results[0].orchestration.special_selection = None
            if alternate:
                records[11]=(None,[(b'RNAM',(22).to_bytes(4,'little'))])
                records[22]=rsgd([(1,3.0)])
                prediction.biome_results.append(view(11,22))
            blocks = {}
            result,detail = ordinary(records,prediction,10,blocks)
            self.assertEqual(detail['descriptor_route'],'INVARIANT_SAME_ROOT_ALTERNATE_COMPONENT' if alternate
                else 'FIRST_BIOME_DESCRIPTOR_AFTER_NO_ALTERNATE')
            self.assertEqual(blocks[result['resources'][0]['block']],[3.0 if alternate else 2.0]*8)


if __name__=='__main__':
    unittest.main()
