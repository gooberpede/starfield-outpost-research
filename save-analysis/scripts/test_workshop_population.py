"""SPDX-License-Identifier: GPL-3.0-or-later
Adversarial research regression: no target/file effects, stdlib/project only.
"""
import copy
import unittest
from unittest.mock import patch
from workshop_population import additional_single, typed_records, initial_case
from workshop_global_units import global_units
from workshop_components import component_sections
from workshop_population_extras import partial_extras


class PopulationTests(unittest.TestCase):
    def row(self):
        return dict(saved_reference='DYNAMIC:ff000001', owner_identity='DYNAMIC:ff000002',
            token='800001', offset=4, end=80, prefix=dict(disabled=False, deleted=False),
            linked_prefix=dict(following_extras='CLOSED', types=[0x4c], extra_flags=None,
                entries=[dict(keyword_identity='starfield.esm:054ba6')]))

    def test_omitted_flags_does_not_mean_zero(self):
        r=self.row(); before=copy.deepcopy(r)
        self.assertIsNone(additional_single(r, {r['saved_reference']:1})['extra_flags'])
        self.assertEqual(r,before)

    def test_uncertainty_and_group_inputs_rejected(self):
        for key,value in [('following_extras','NOT_DECODED'),('types',[]),
                          ('packin',[{}]),('alternate_groups',[{}])]:
            with self.subTest(key=key):
                r=self.row();r['linked_prefix'][key]=value
                with self.assertRaises(ValueError):additional_single(r,{r['saved_reference']:1})

    def test_foundation_and_replacement_not_promoted(self):
        for key in ('starfield.esm:000191','starfield.esm:000192'):
            r=self.row();r['linked_prefix']['entries'].append(dict(keyword_identity=key))
            with self.assertRaises(ValueError):additional_single(r,{r['saved_reference']:1})

    def test_duplicate_identity_not_deduplicated(self):
        r=self.row()
        with self.assertRaises(ValueError):additional_single(r,{r['saved_reference']:2})

    def test_static_and_actor_alternatives(self):
        self.assertEqual(initial_case(dict(form_type=0x4b,token='400123',flags=0)),0)
        self.assertEqual(initial_case(dict(form_type=0x4a,token='800123',flags=0x8000)),7)
        self.assertEqual(initial_case(dict(form_type=0x4a,token='800123',flags=0)),5)
        self.assertIsNone(initial_case(dict(form_type=0x49,token='800123',flags=0)))

    def test_ordered_runs_and_version_independence(self):
        # Three runs, repeated type0 separated bytype1; optional override153 is
        # deliberately unrelated to actual types4a/4b.
        b=bytearray(160);b[16:20]=(27).to_bytes(4,'little');b[20]=153;b[80:87]=bytes([12,0,4,1,4,0,4])
        records=[dict(explicit_type=v, token='800001',flags=0) for v in (None,151,153)]
        d=dict(offset=0,words=[0]*9+[3],regions={'late_region':(80,160),'region_R3':(60,70)})
        b[44:48]=(80).to_bytes(4,'little')
        with patch('workshop_population.directory',return_value=d),patch('workshop_population.iter_records',return_value=iter(records)):
            rows=list(typed_records(b))
        self.assertEqual([r['form_type'] for r in rows],[0x4a,0x4b,0x4a])
        self.assertEqual([r['buffer_version'] for r in rows],[153,151,153])

    def test_invalid_registry_index(self):
        b=bytearray(160);b[16:20]=(27).to_bytes(4,'little');b[44:48]=(80).to_bytes(4,'little');b[80:83]=bytes([4,59,4])
        d=dict(offset=0,words=[0]*9+[1],regions={'late_region':(80,160),'region_R3':(60,70)})
        with patch('workshop_population.directory',return_value=d):
            with self.assertRaisesRegex(ValueError,'TYPE_INDEX'):list(typed_records(b))

    def test_global_strings_precede_length(self):
        #type101: VS2 strings, two u16 indices, u32bodylength, body.
        a=(101).to_bytes(4,'little')+bytes([8])+bytes([1,0,2,0])+(3).to_bytes(4,'little')+b'abc'
        b=a+(1009).to_bytes(4,'little');d=dict(words=[0]*6+[1,0,1],regions={'region_R1':(0,len(a)),'region_R2':(len(a),len(a)),'region_R4':(len(a),len(b))})
        with patch('workshop_global_units.directory',return_value=d):rows=global_units(b)
        self.assertEqual(rows[0]['strings'],[1,2]);self.assertEqual(rows[0]['size'],3)
        self.assertEqual(rows[1]['native_mask_status'],'UNKNOWN_TYPE_DEFAULT_ZERO')

    def test_global_pointer_is_not_length(self):
        b=bytearray(40);b[:4]=(2).to_bytes(4,'little');b[4:8]=(32).to_bytes(4,'little')
        d=dict(words=[0]*6+[1,0,0],regions={'region_R1':(0,8),'region_R2':(8,8),'region_R4':(8,8)})
        with patch('workshop_global_units.directory',return_value=d):rows=global_units(b)
        self.assertEqual(rows[0]['end'],8);self.assertEqual(rows[0]['out_of_line_pointer'],32)

    def test_global_payload_overflow_rejected(self):
        b=(100).to_bytes(4,'little')+(20).to_bytes(4,'little')
        d=dict(words=[0]*6+[1,0,0],regions={'region_R1':(0,8),'region_R2':(8,8),'region_R4':(8,8)})
        with patch('workshop_global_units.directory',return_value=d):
            with self.assertRaisesRegex(ValueError,'boundary'):global_units(b)

    def component(self, b):
        return component_sections(b,0,len(b),buffer_version=153,activity_custom_payloads=True)

    def test_component_requires_context(self):
        for version,custom in [(152,True),(153,False),(153,None)]:
            with self.assertRaisesRegex(ValueError,'UNQUALIFIED'):
                component_sections(bytes(172),0,172,buffer_version=version,activity_custom_payloads=custom)

    def test_component_exact_closure_and_truncation(self):
        self.assertEqual(len(self.component(bytes(172))),43)
        with self.assertRaisesRegex(ValueError,'boundary'):self.component(bytes(171))
        with self.assertRaisesRegex(ValueError,'TYPE6_CLOSURE'):self.component(bytes(173))

    def test_calculated_packin_u16_count_u32_ids(self):
        entry=bytes.fromhex('040000000100020078563412efcdab00')
        b=bytes(39*4)+(1).to_bytes(4,'little')+entry+bytes(3*4)
        section=self.component(b)[39]
        self.assertEqual(section['rows'][0]['ids'],[0x12345678,0x00abcdef])

    def test_color_count_is_clamped_without_skipping_surplus(self):
        # Native consumes only3triples even when savedcount4, then nexttable.
        entry=bytes(6)+bytes([1])+(4).to_bytes(4,'little')+bytes(36)
        b=bytes(36*4)+(1).to_bytes(4,'little')+entry+bytes(6*4)
        row=self.component(b)[36]['rows'][0]
        self.assertEqual(row['saved_count'],4);self.assertEqual(len(row['colors']),72)

    def test_unknown_nonempty_leaf_is_not_silently_skipped(self):
        b=bytes(24*4)+(1).to_bytes(4,'little')+bytes(6)+bytes(18*4)
        with self.assertRaisesRegex(ValueError,'PAYLOAD_UNQUALIFIED'):self.component(b)

    def test_da_only_closed_list_is_retained(self):
        b=b'\x04\xda\0'+bytes(4)
        r=dict(end=len(b),flags=0x40,form_type=0x4a,refs=['400001','400001','000000','800002','400003'],strings=[])
        x=partial_extras(b,r,dict(form_prefix_end=0,next_reference_index=0))
        self.assertEqual(x['following_extras'],'CLOSED');self.assertEqual(x['entries'],[])
        self.assertEqual(x['packin'][0]['tokens'][3],'800002')

    def test_partial_da_survives_unknown_later_extra(self):
        b=b'\x08\xda\0'+bytes(4)+b'\xf1'
        r=dict(end=len(b),flags=0x40,form_type=0x4a,refs=['400001','400001','000000','800002','400003'],strings=[])
        x=partial_extras(b,r,dict(form_prefix_end=0,next_reference_index=0))
        self.assertEqual(x['following_extras'],'NOT_DECODED');self.assertEqual(x['following_gap'],'EXTRA_F1_UNSUPPORTED')
        self.assertEqual(x['decoded_extra_count'],1);self.assertEqual(len(x['packin']),1)

    def test_fd_zero_body_and_actual_actor_dispatch(self):
        b=b'\x04\xfd';r=dict(end=2,flags=0x400,form_type=0x4a,refs=[],strings=[])
        prefix=dict(form_prefix_end=0,next_reference_index=0)
        self.assertEqual(partial_extras(b,r,prefix)['end'],2)
        r['form_type']=0x4b
        with self.assertRaisesRegex(ValueError,'NO_EXTRA_DISPATCH'):partial_extras(b,r,prefix)


if __name__=='__main__':unittest.main()
