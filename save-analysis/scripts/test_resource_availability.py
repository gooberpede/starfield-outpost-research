"""SPDX-License-Identifier: GPL-3.0-or-later
Original adversarial wire tests; synthetic fixtures are not availability oracles.
"""
import struct
import unittest
from outpost_record_framing import Reader
from research_resource_availability import saved_resource_groups
from resource_availability import ResourceOperand, UIInputs, project_ui_rows, compare_sets, EXE_SHA256, region_broadphase
from resource_availability import harvester_resource_gate
from resource_availability import biome_rnam_resources
from resource_availability import generation_seed, first_mt_word, generation_first_gate


class GenerationFirstGate(unittest.TestCase):
    def test_raw_crc_against_independent_stdlib_convention(self):
        import binascii
        for key, world in ((0, 0), (0x0123456789abcdef, 0xfedcba98), (2**64-1, 2**32-1)):
            data = struct.pack('<QI', key, world)
            expected = binascii.crc32(data, 0xffffffff)^0xffffffff
            self.assertEqual(generation_seed(key, world), expected)

    def test_classic_mt_first_word(self):
        # Known classic seed/reference corroborated by owned prior model, not retail capture.
        self.assertEqual(first_mt_word(5489), 3499211612)

    def test_zero_full_chance_and_missing(self):
        self.assertFalse(generation_first_gate(1, 2, 0, 1)['first_gate_pass'])
        self.assertTrue(generation_first_gate(1, 2, 100, 1)['first_gate_pass'])
        self.assertIsNone(generation_first_gate(None, 2, 100, 1)['first_gate_pass'])
        self.assertEqual(generation_first_gate(1, 2, 100, 1)['local_availability'], 'NOT_EVALUATED')

    def test_rng_reseeds_each_cell_and_world_changes_seed(self):
        self.assertEqual(generation_first_gate(123, 1, 50, 1), generation_first_gate(123, 1, 50, 1))
        self.assertNotEqual(generation_seed(123, 1), generation_seed(123, 2))

    def test_unsigned_domains_rejected(self):
        for key, world in ((-1, 1), (True, 1), (2**64, 1), (1, 2**32)):
            with self.assertRaises(ValueError): generation_seed(key, world)


class BiomeProjection(unittest.TestCase):
    def test_order_and_duplicate_occurrences_preserved(self):
        d = {'biome':dict(kind='BIOM', rnam=('gen1', 'gen2')),
             'gen1':dict(kind='RSGD', rnam=('iron', 'water')),
             'gen2':dict(kind='RSGD', rnam=('water',)),
             'iron':dict(kind='IRES'), 'water':dict(kind='IRES')}
        r = biome_rnam_resources('biome', d)
        self.assertEqual(r['resource_occurrences'], ['iron', 'water', 'water'])
        self.assertEqual(r['resource_set'], ['iron', 'water'])
        self.assertEqual(r['local_availability'], 'NOT_EVALUATED')

    def test_missing_wrong_kind_and_empty_are_distinct(self):
        self.assertIsNone(biome_rnam_resources('b', {})['resource_set'])
        self.assertIsNone(biome_rnam_resources('b', {'b':dict(kind='CELL', rnam=())})['resource_set'])
        self.assertEqual(biome_rnam_resources('b', {'b':dict(kind='BIOM', rnam=())})['resource_set'], [])
        self.assertIsNone(biome_rnam_resources('b', {'b':dict(kind='BIOM', rnam=('g',))})['resource_set'])

    def test_wrong_resource_target_does_not_invent_list(self):
        d = {'b':dict(kind='BIOM', rnam=('g',)), 'g':dict(kind='RSGD', rnam=('x',)), 'x':dict(kind='MISC')}
        self.assertEqual(biome_rnam_resources('b', d)['missing'], ['x'])


class HarvesterGate(unittest.TestCase):
    def gate(self, produced=(1,), first=(1,), second=(2,), special=(3,), anywhere=False, atmosphere=False, skip=False):
        return harvester_resource_gate(produced, first, second, special,
            place_anywhere_present=anywhere, atmosphere_present=atmosphere, skip_vein_present=skip)

    def test_place_anywhere_presence_bypasses_resource_overlap(self):
        self.assertTrue(self.gate(produced=(), first=(), second=(), special=(), anywhere=True)['passes'])

    def test_source_selection_and_skip_precedence(self):
        self.assertTrue(self.gate()['passes'])
        self.assertFalse(self.gate(atmosphere=True)['passes'])
        self.assertTrue(self.gate(produced=(3,), atmosphere=True, skip=True)['passes'])

    def test_empty_is_false_and_unknown_is_unobserved(self):
        self.assertFalse(self.gate(produced=())['passes'])
        self.assertIsNone(self.gate(first=None)['passes'])
        self.assertIsNone(self.gate(anywhere=None)['passes'])

    def test_null_pointer_cannot_be_resource(self):
        with self.assertRaisesRegex(ValueError, 'NONNULL_POINTER_TUPLE_REQUIRED'):
            self.gate(produced=(0,))


class RegionBroadphase(unittest.TestCase):
    def test_tangent_one_point_and_outside(self):
        self.assertTrue(region_broadphase((0, 0), (3, 4), 2, 3, 1)['callback_candidate'])
        self.assertFalse(region_broadphase((0, 0), (3, 4), 2, 2, 1)['callback_candidate'])

    def test_zero_and_multi_point_are_distinct(self):
        self.assertFalse(region_broadphase((0, 0), (0, 0), 1, 1, 0)['callback_candidate'])
        self.assertIsNone(region_broadphase((0, 0), (0, 0), 1, 1, 2)['callback_candidate'])

    def test_same_frame_translation(self):
        self.assertEqual(region_broadphase((0, 0), (3, 4), 2, 3, 1),
                         region_broadphase((-100, 100), (-97, 104), 2, 3, 1))

    def test_f32_input_rounding_boundary(self):
        self.assertTrue(region_broadphase((0, 0), (1+2**-25, 0), 1, 0, 1)['callback_candidate'])
        self.assertFalse(region_broadphase((0, 0), (1+2**-22, 0), 1, 0, 1)['callback_candidate'])

    def test_unqualified_numeric_domains_fail(self):
        for v in (float('nan'), float('inf'), 2**-140, True, 1e40):
            with self.assertRaises(ValueError): region_broadphase((v, 0), (0, 0), 1, 1, 1)
        with self.assertRaisesRegex(ValueError, 'RADIUS_DOMAIN'):
            region_broadphase((0, 0), (0, 0), -1, 1, 1)


class UIProjection(unittest.TestCase):
    def inputs(self, first=(), second=(), special=(), selected=None, observed=True):
        return UIInputs(EXE_SHA256, 'synthetic-session', 'synthetic; no retail observation',
                        first, second, special, observed, selected, True)

    def test_missing_is_not_empty(self):
        self.assertEqual(project_ui_rows(self.inputs(first=None))['ui_form_set'], None)
        self.assertEqual(project_ui_rows(self.inputs())['ui_form_set'], [])
        self.assertEqual(project_ui_rows(self.inputs(observed=False))['status'], 'UNKNOWN')

    def test_pointer_union_not_form_union(self):
        a, b, c = ResourceOperand(10, 1), ResourceOperand(20, 1), ResourceOperand(30, 2)
        v = project_ui_rows(self.inputs((a, b), (a, c)))
        self.assertEqual([x['pointer'] for x in v['ui_rows']], [10, 20, 30])
        self.assertEqual(v['ui_form_set'], [1, 2])

    def test_special_form_filter_appends_duplicate(self):
        a, b = ResourceOperand(10, 1), ResourceOperand(20, 2)
        v = project_ui_rows(self.inputs((a,), (), (a, b, a), 1))
        self.assertEqual([x['pointer'] for x in v['ui_rows']], [10, 10, 10])

    def test_null_common_skipped_null_special_invalid(self):
        null = ResourceOperand(0, None)
        self.assertEqual(project_ui_rows(self.inputs((null,), (null,)))['ui_rows'], [])
        with self.assertRaisesRegex(ValueError, 'NULL_SPECIAL_DEREFERENCE'):
            project_ui_rows(self.inputs(special=(null,), selected=1))

    def test_inconsistent_lifetime_rejected(self):
        with self.assertRaisesRegex(ValueError, 'INCONSISTENT_POINTER_SNAPSHOT'):
            project_ui_rows(self.inputs((ResourceOperand(1, 1),), (ResourceOperand(1, 2),)))

    def test_invalid_domains(self):
        for args in [(True, 1), (-1, 1), (1, True), (0, 1), (1, 2**32)]:
            with self.assertRaises(ValueError): ResourceOperand(*args)

    def test_set_channels(self):
        self.assertEqual(compare_sets(None, set())['status'], 'NOT_TESTED')
        self.assertTrue(compare_sets(set(), set())['exact'])
        self.assertEqual(compare_sets({1, 2}, {2, 3}),
                         dict(status='COMPARED', exact=False, false_positives=[3], false_negatives=[1]))

    def test_allocation_status_is_required(self):
        from dataclasses import replace
        self.assertEqual(project_ui_rows(replace(self.inputs(), allocations_complete=None))['status'], 'UNKNOWN')
        self.assertEqual(project_ui_rows(replace(self.inputs(), allocations_complete=False))['status'], 'INCOMPLETE_NATIVE_ALLOCATION')

    def test_unobserved_selector_cannot_have_value(self):
        with self.assertRaisesRegex(ValueError, 'UNOBSERVED_SELECTOR_HAS_VALUE'):
            project_ui_rows(self.inputs(selected=1, observed=False))


class SavedResourceGroups(unittest.TestCase):
    def parse(self, body, tokens, count):
        c = Reader(body, 0, len(body))
        cursor = 0
        def refs(n):
            nonlocal cursor
            if n > len(tokens)-cursor: raise ValueError('REFERENCE_QUEUE_BOUNDS')
            result = tokens[cursor:cursor+n]; cursor += n
            return result
        rows = saved_resource_groups(c, refs, count)
        return rows, c.p, cursor

    def test_empty_is_registry_only(self):
        self.assertEqual(self.parse(b'', [], 0), ([], 0, 0))

    def test_two_groups_preserve_rows_and_offsets(self):
        payload = bytes(range(17))
        body = struct.pack('<I', 2)+payload+payload+struct.pack('<I', 0)
        rows, end, consumed = self.parse(body, ['key1', 'a', 'b', 'c', 'd', 'key2'], 2)
        self.assertEqual((end, consumed), (42, 6))
        self.assertEqual([g['resource'] for g in rows], ['key1', 'key2'])
        self.assertEqual([r['offset'] for r in rows[0]['rows']], [4, 21])
        self.assertEqual(rows[0]['rows'][1]['references'], ['c', 'd'])
        self.assertEqual(rows[0]['rows'][0]['payload_hex'], payload.hex())
        self.assertEqual(rows[1]['rows'], [])

    def test_outer_count_bounds(self):
        with self.assertRaisesRegex(ValueError, 'RESOURCE_GROUP_BOUNDS'):
            self.parse(b'\0'*3, ['x'], 1)

    def test_inner_count_bounds(self):
        with self.assertRaisesRegex(ValueError, 'RESOURCE_ROW_BOUNDS'):
            self.parse(struct.pack('<I', 2)+b'\0'*17, ['x', 'a', 'b'], 1)

    def test_missing_key(self):
        with self.assertRaisesRegex(ValueError, 'REFERENCE_QUEUE_BOUNDS'):
            self.parse(b'\0'*4, [], 1)

    def test_missing_row_reference(self):
        with self.assertRaisesRegex(ValueError, 'REFERENCE_QUEUE_BOUNDS'):
            self.parse(struct.pack('<I', 1)+b'\0'*17, ['x', 'a'], 1)

    def test_boundary_does_not_consume_following_extra(self):
        body = struct.pack('<I', 1)+b'\0'*17+b'\x9c'+b'\xff'*4
        _, end, _ = self.parse(body, ['x', 'a', 'b'], 1)
        self.assertEqual(end, 21)
        self.assertEqual(body[end], 0x9c)


if __name__ == '__main__': unittest.main()
