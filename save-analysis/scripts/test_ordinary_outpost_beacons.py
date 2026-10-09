"""SPDX-License-Identifier: GPL-3.0-or-later
Synthetic detector tests: actual R3 framing/prefix decoding, synthetic directory
injection only. No files/corpus/live effects. No gameplay-label inputs.
"""
import struct
import unittest
from unittest.mock import patch
from test_outpost_membership import fixture
from ordinary_outpost_beacons import summarize, catalog_for


def count(n):
    width, tag = (1, 0) if n < 64 else (2, 1)
    return ((n << 2) | tag).to_bytes(width, 'little')


def sample(case=5, flags=1, saved=0x400408, base='6c60e9', table=(), lead=False,
           explicit=None, corrupt_self=False, truncate=False):
    body, r = fixture(case=case, flags=flags, saved=saved)
    if case == 5:
        r['refs'][1] = base
    if corrupt_self:
        r['refs'][-1] = '800099'
    if truncate:
        body = body[:-1]
    rec = bytes([0x2a | (explicit is not None)])
    if explicit is not None:
        rec += bytes([explicit])
    rec += bytes.fromhex(r['token']) + struct.pack('<I', flags)
    rec += count(len(r['refs'])) + count(len(body))
    rec += b''.join(bytes.fromhex(t) for t in r['refs']) + body
    tab = struct.pack('<I', len(table)) + b''.join(struct.pack('<I', x) for x in table)
    tail = bytes.fromhex('800001000001') if lead else b''
    b = rec + tab + tail
    d = dict(regions=dict(region_R3=(0, len(rec)), reference_u32=(len(rec), len(rec)+len(tab)),
                         region_R1=(len(rec)+len(tab), len(b))), reference_count=len(table),
             words=[0]*9+[1])
    return b, d


CAT = dict(direct_bases={0x2c60e9: 'OutpostBeaconActivator'}, templates={})


class DetectorTests(unittest.TestCase):
    def detect(self, catalog=CAT, **kwargs):
        b, d = sample(**kwargs)
        with patch('outpost_membership.directory', return_value=d):
            return summarize(b, catalog)

    def test_positive_and_disabled(self):
        for saved, state in [(0x400408, 'EXPLICITLY_CLEAR'), (0x400c08, 'EXPLICITLY_SET')]:
            r = self.detect(saved=saved)
            self.assertEqual(r['ordinary_count'], 1)
            self.assertEqual(r['candidates'][0]['disabled_state'], state)
            self.assertEqual(r['authoritative_player_membership'], 'INDETERMINATE')
            self.assertEqual(r['candidates'][0]['saved_flags_logical_offset'],
                             r['candidates'][0]['location']['body_start']+14)

    def test_omitted_flags_still_positive(self):
        r = self.detect(flags=0)
        self.assertEqual(r['ordinary_count'], 1)
        self.assertEqual(r['counts']['ordinary']['OMITTED'], 1)
        self.assertIsNone(r['candidates'][0]['saved_form_flags'])

    def test_array_base_representation(self):
        r = self.detect(base='000001', table=[0x2c60e9])
        self.assertEqual(r['ordinary_count'], 1)
        self.assertEqual(r['candidates'][0]['raw_base_token'], '000001')

    def test_alternate_case_template_is_unresolved(self):
        catalog = dict(direct_bases=CAT['direct_bases'], templates={0x302b256: 0x3038aca})
        r = self.detect(catalog, case=6, flags=0x92018200, table=[0x302b256], lead=True)
        self.assertEqual(r['ordinary_count'], 0)
        self.assertEqual(r['counts']['unresolved beacon-like']['OMITTED'], 1)
        self.assertEqual(r['candidates'][0]['initial_case'], 6)

    def test_faction_inline_separate(self):
        catalog = dict(direct_bases={**CAT['direct_bases'], 0x3038aca: 'OutpostBeaconActivatorUC'}, templates={})
        r = self.detect(catalog, base='000001', table=[0x3038aca])
        self.assertEqual(r['ordinary_count'], 0)
        self.assertEqual(r['counts']['exceptional/faction']['EXPLICITLY_CLEAR'], 1)

    def test_decoy_and_failed_self_are_inspectable(self):
        for kwargs in [dict(explicit=0x3e), dict(corrupt_self=True), dict(truncate=True)]:
            r = self.detect(**kwargs)
            self.assertEqual(r['ordinary_count'], 0)
            self.assertEqual(r['headline'], 'NO_RECOGNIZED_ORDINARY_BEACONS')
            self.assertEqual(r['counts']['unresolved beacon-like']['UNRESOLVED'], 1)

    def test_no_match_is_scanner_negative(self):
        r = self.detect(base='400123')
        self.assertEqual(r['ordinary_count'], 0)
        self.assertEqual(r['candidates'], [])
        self.assertFalse(r['coverage']['complete_ordinary_enumeration'])
        self.assertEqual(r['headline'], 'NO_RECOGNIZED_ORDINARY_BEACONS')

    def test_real_parser_error_propagates(self):
        b, d = sample()
        d['words'][9] = 2
        with patch('outpost_membership.directory', return_value=d), self.assertRaises(ValueError):
            summarize(b, CAT)

    def test_unknown_mapping_does_not_invent_identity(self):
        r = self.detect(base='000001', table=[0xdeadbeef])
        self.assertEqual(r['ordinary_count'], 0)
        catalog, plugins = catalog_for(b'SFS_SAVEGAME', {})
        self.assertEqual(catalog, CAT)
        self.assertEqual(plugins, [])


if __name__ == '__main__':
    unittest.main()
