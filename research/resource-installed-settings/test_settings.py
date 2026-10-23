# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic parser/mask tests and local pinned-evidence replay regressions.

Reads existing C1H settings and frozen evidence when available; writes nothing.
No screenshots are input to parameter resolution or geometry generation.
"""
import argparse
import json
import struct
import unittest
from settings import CLASSES, IDS, ROOT, bits, parse_setting, resolve
from replay import run

class Settings(unittest.TestCase):
    def setUp(self):
        self.values={i:struct.unpack('<f',struct.pack('<f',v))[0] for i,v in enumerate((.3,.2,.1,.05,0,.3))}

    def test_record_identity_and_binary32(self):
        for i in range(6):
            h=dict(type='GMST',formid=IDS[i],offset=100+i)
            f=[(b'EDID',('fInactiveResourceChanceMult'+CLASSES[i]).encode()+b'\0'),(b'DATA',struct.pack('<f',self.values[i]))]
            self.assertEqual(parse_setting(h,f,i)['installed_bits'],bits(self.values[i]))
            with self.assertRaises(ValueError):parse_setting(dict(h,formid=IDS[(i+1)%6]),f,i)
            with self.assertRaises(ValueError):parse_setting(h,[(b'EDID',b'wrong\0'),f[1]],i)
            with self.assertRaises(ValueError):parse_setting(h,[f[0],(b'DATA',b'\0')],i)

    def test_mask_eight_inactive(self):
        for i in range(6):self.assertEqual(resolve(i,8,self.values),self.values[i])

    def test_active_mask_four(self):
        for i in range(5):self.assertEqual(resolve(i,4,self.values),1)
        self.assertEqual(resolve(5,4,self.values),self.values[5])

    def test_rarity_exceeds_mask(self):
        for i in range(1,6):self.assertEqual(resolve(i,0,self.values),self.values[i])
        self.assertEqual(resolve(0,0,self.values),1)

    def test_everywhere_is_separate(self):
        self.assertEqual(resolve(6,8,self.values),0)
        self.assertEqual(resolve(6,8,self.values,'everywhere'),1)
        with self.assertRaises(ValueError):resolve(5,8,self.values,'everywhere')

    def test_unknowns_rejected(self):
        for rarity,mask in ((-1,8),(7,8),(3,None),(3,16),(True,8)):
            with self.assertRaises(ValueError):resolve(rarity,mask,self.values)
        with self.assertRaises(ValueError):resolve(3,8,{3:.05})
        for value in (float('nan'),float('inf'),'unknown',True):
            with self.assertRaises(ValueError):resolve(3,8,dict(self.values, **{}) | {3:value})

    def test_nonfinite_definition_rejected(self):
        h=dict(type='GMST',formid=IDS[3],offset=100)
        f=[(b'EDID',b'fInactiveResourceChanceMultExotic\0'),(b'DATA',struct.pack('<f',float('nan')))]
        with self.assertRaises(ValueError):parse_setting(h,f,3)

    def test_binary32_gate_not_double(self):
        self.assertEqual(bits(.05),'0x3d4ccccd')
        self.assertEqual(bits(.01),'0x3c23d70a')
        self.assertNotEqual(bits(.01),bits(.05))

class LocalRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=ROOT/'.local-work/resource-installed-settings/settings01.json'
        if not p.exists():raise unittest.SkipTest('local proprietary input audit unavailable')
        cls.result,cls.full=run(argparse.Namespace(settings=p))
        cls.feynman,cls.carinae=cls.result['sites']

    def test_preserved_baseline(self):
        self.assertEqual((self.feynman['baseline_count'],self.carinae['baseline_count']),(156,895))

    def test_four_exact_native_paths(self):
        self.assertEqual(len(self.feynman['accepted']),4)
        self.assertTrue(all(len(x['installed_matches'])==1 for x in self.feynman['accepted']))
        self.assertEqual([x['baseline_matches'] for x in self.feynman['accepted']],[0,1,1,1])

    def test_three_native_chance_decisions(self):
        self.assertEqual(len(self.feynman['chance_comparison']),3)
        self.assertTrue(all(x['equal'] for x in self.feynman['chance_comparison']))
        self.assertEqual([x['observed']['edge'] for x in self.feynman['chance_comparison']],['ADMIT','REJECT','ADMIT'])

    def test_copper_retained_without_extra_il(self):
        req=next(x for x in self.full if x['request']['source']=='0:25116:32448:00257f38')
        self.assertTrue(any(r['resource']=='000057cf' and r['cell']==[11,1] for r in req['regions']))
        self.assertFalse(any(r['resource']=='000057d4' and r['cell']==[11,1] for r in req['regions']))

    def test_exact_population_change(self):
        self.assertEqual(self.feynman['installed_count'],156)
        self.assertEqual(len(self.feynman['added']),2)
        self.assertEqual(len(self.feynman['removed']),2)
        self.assertEqual(self.feynman['unchanged_geometry'],154)
        self.assertEqual({r['resource'] for r in self.feynman['removed']},{'0x000057d0'})
        self.assertEqual({r['resource'] for r in self.feynman['added']},{'0x000057d4'})
        self.assertEqual({tuple(r['cell']) for r in self.feynman['added']},{(2,6),(10,1)})

    def test_unfitted_carinae(self):
        self.assertEqual(self.carinae['baseline'],self.carinae['installed'])
        self.assertEqual(self.carinae['added']+self.carinae['removed'],[])
        self.assertTrue(all(w['baseline']==w['installed'] for w in self.carinae['witnesses']))
        self.assertEqual(self.carinae['installed']['000057c7']['bounded'],{'DISJOINT_OR_ZERO_AREA':259})

    def test_swapped_defaults_fail_baseline(self):
        # The resolver must preserve distinct Common/Exotic binary32 defaults.
        data=json.loads((ROOT/'.local-work/resource-installed-settings/settings01.json').read_text())
        defaults={r['rarity']:r['default_value'] for r in data['settings']}
        self.assertNotEqual(bits(resolve(0,8,defaults)),bits(resolve(3,8,defaults)))
        self.assertEqual(bits(resolve(3,8,defaults)),'0x3c23d70a')

if __name__=='__main__':unittest.main()
