"""SPDX-License-Identifier: GPL-3.0-or-later
Original synthetic and opt-in real-corpus regressions. Stdlib/project only.
--corpus-run reads local primary bytes/pins, writes exclusive local test receipt;
no original writes, raw exports, external programs or live target effects.
"""
import argparse
import json
import struct
import unittest
from pathlib import Path
from unittest.mock import patch
import extractor_resources as ex
from inventory_historical_saves import identity, guard
from stream_save import decoded_save
from test_outpost_record_framing import independent


def row(kind, fid, fs, plugin='Starfield.esm', edid='MisleadingName', offset=0):
    return dict(type=kind,formid=fid,flags=0,plugin=plugin,edid=edid,offset=offset,
                fields=[(k,v.hex()) for k,v in fs])


def static_fixture():
    u=lambda n:struct.pack('<I',n)
    return [row('TES4',0,[]),
            row('CONT',0x5ef19,[('KWDA',u(0x8406)),('PRPS',struct.pack('<IfI',0x5ef18,1,0))]),
            row('IRES',0x57c7,[('NAM1',u(0x5ef18)),('NAM2',u(0x5ef53))]),
            row('COBJ',0x5ef53,[('CNAM',u(0x556e))]),row('MISC',0x556e,[]),
            row('AVIF',0x5ef18,[])]


def save_record(refs=None, token='800001', saved=0, flags=1, typ=None):
    refs=refs or ['800002','45ef19',token]
    body=b'\0'+struct.pack('<3f',1,2,3)+b'\0'
    if flags&1:body+=struct.pack('<IH',saved,0)
    tag=0x2a | (1 if typ is not None else 0)
    header=bytes([tag])+(bytes([typ]) if typ is not None else b'')
    header+=bytes.fromhex(token)+struct.pack('<I',flags)+bytes([len(refs)*4,len(body)*4])
    return header+b''.join(bytes.fromhex(t) for t in refs)+body


PLUGINS=dict(groups=dict(full=['starfield.esm','dlc.esm'],small=['small.esm'],medium=['medium.esm']))


class ExtractorTests(unittest.TestCase):
    def scan(self,b,catalog=None):
        d=dict(regions=dict(reference_u32=[0,0],region_R3=[0,len(b)]),reference_count=0,words=[0]*9+[1])
        with patch.object(ex,'directory',return_value=d):
            return ex.inventory(b,catalog or ex.definition_catalog(static_fixture()),PLUGINS)

    def test_relationships_ignore_names(self):
        rs=static_fixture();cat=ex.definition_catalog(rs)
        a=cat['starfield.esm:05ef19']['associations'][0]
        self.assertEqual(a['resource_identity'],'starfield.esm:0057c7')
        self.assertEqual(a['item_identity'],'starfield.esm:00556e')
        rs[1]['type']='COBJ'
        self.assertEqual(ex.definition_catalog(rs),{})

    def test_no_resource_unknown_not_invented(self):
        rs=static_fixture();rs[2]['fields']=[]
        x=ex.definition_catalog(rs)['starfield.esm:05ef19']
        self.assertEqual((x['status'],x['associations']),('UNKNOWN',[]))

    def test_ambiguous_resource_not_arbitrarily_selected(self):
        rs=static_fixture();rs.append(row('IRES',0x57c8,[(k,bytes.fromhex(v)) for k,v in rs[2]['fields']]))
        self.assertEqual(ex.definition_catalog(rs)['starfield.esm:05ef19']['status'],'UNKNOWN')

    def test_missing_recipe_retains_resource_and_gap(self):
        rs=static_fixture();rs.pop(3)
        a=ex.definition_catalog(rs)['starfield.esm:05ef19']['associations'][0]
        self.assertIsNone(a['item_identity']);self.assertIn('item_gap',a)

    def test_correct_reference_and_wrong_slot_lookalike(self):
        self.assertEqual(len(self.scan(save_record())['instances']),1)
        x=self.scan(save_record(['45ef19','400123','800001']))
        self.assertEqual(x['instances'],[]);self.assertEqual(len(x['unresolved_leads']),1)

    def test_static_record_and_wrong_type_not_instances(self):
        self.assertEqual(self.scan(save_record(token='400123'))['instances'],[])
        x=self.scan(save_record(typ=1))
        self.assertEqual(x['instances'],[]);self.assertEqual(x['rejected'][0]['reason'],'EXPLICIT_NON_REFR')

    def test_self_and_truncation_fail_closed(self):
        x=self.scan(save_record(['800002','45ef19','800099']))
        self.assertEqual(x['instances'],[]);self.assertIn('SELF_REFERENCE',x['rejected'][0]['reason'])
        with self.assertRaises(ValueError):self.scan(save_record()[:-1])

    def test_disabled_deleted_omitted_separate(self):
        for saved in (0x800,0x20,0):
            p=self.scan(save_record(saved=saved))['instances'][0]['prefix']
            self.assertEqual(p['disabled'],bool(saved&0x800));self.assertEqual(p['deleted'],bool(saved&0x20))
        p=self.scan(save_record(flags=0))['instances'][0]['prefix']
        self.assertIsNone(p['disabled']);self.assertIsNone(p['deleted'])

    def test_full_light_medium_file_and_save_domains(self):
        self.assertEqual(ex.saved_form(0x01012345,PLUGINS),'dlc.esm:012345')
        self.assertEqual(ex.saved_form(0xfe000123,PLUGINS),'small.esm:000123')
        self.assertEqual(ex.saved_form(0xfd001234,PLUGINS),'medium.esm:001234')
        self.assertEqual(ex.saved_form(0x01000123,PLUGINS),'dlc.esm:000123')
        self.assertEqual(ex.saved_form(0xfd000123,PLUGINS),'medium.esm:000123')
        flags={'small.esm':0x100,'medium.esm':0x400}
        self.assertEqual(ex.qualified('medium.esm',0xfd001234,['starfield.esm'],flags),'medium.esm:001234')
        self.assertEqual(ex.qualified('small.esm',0xfe000123,['starfield.esm'],flags),'small.esm:000123')
        with self.assertRaises(ValueError):ex.saved_form(0xfe001000,PLUGINS)
        with self.assertRaises(ValueError):ex.qualified('starfield.esm',0x01000001,[])

    def test_wrong_resource_actor_type_is_unknown(self):
        rs=static_fixture();rs[-1]['type']='MISC'
        self.assertEqual(ex.definition_catalog(rs)['starfield.esm:05ef19']['status'],'UNKNOWN')

    def test_plugin_header_closure_metadata_and_bad_trailer(self):
        def string(s):
            b=s.encode();return struct.pack('<H',len(b))+b
        def entry(s,metadata=False):
            return string(s)+bytes([int(metadata)])+(string('Title')+string('ID')+string('Version')+b'\1' if metadata else b'')
        plugin=b'\2'+entry('Starfield.esm')+entry('DLC.esm',True)
        plugin+=struct.pack('<H',1)+entry('small.esm')
        plugin+=struct.pack('<I',1)+entry('medium.esm')+b'\1\0'
        b=b'SFS_SAVEGAME'+struct.pack('<I',0)+b'\x99'+string('1.16.244.0')*2+struct.pack('<I',len(plugin))+plugin
        got=ex.plugin_tables(b)
        self.assertEqual(got['groups'],PLUGINS['groups']);self.assertEqual(got['end'],len(b))
        with self.assertRaises(ValueError):ex.plugin_tables(b[:-1])
        with self.assertRaises(ValueError):ex.plugin_tables(b[:-1]+b'\1')


def corpus(out):
    guard()
    before=json.loads((out/'inputs-before.json').read_text())
    summary=json.loads((out/'summary.json').read_text())
    assert len(summary)==25, '17 manual + seven link (incidental exit) + mature'
    receipts=[]
    for s in summary:
        r=json.loads((out/(s['series']+'-'+s['label']+'.json')).read_text())
        p=Path(r['source']['path']);pin=identity(p)
        assert pin==r['source']
        with decoded_save(p,out/'scratch') as (b,metrics):
            d=ex.directory(b)
            # Independent arithmetic walker confirms every saved record boundary.
            other=independent(b,*d['regions']['region_R3'],d['words'][9])
            assert len(other)==r['coverage']['framed_records']
            for obj in r['instances']:
                bound=other[obj['ordinal']]
                assert (obj['offset'],obj['end'],obj['token'])==bound[:3]
            if s['series']=='manual-S0-S7C':
                expected=int(s['label'] in [f'S{i}{c}' for i in range(3,7) for c in ('','C')])
                assert s['count']==expected,(s,expected)
                # Earlier independent action candidate anchors, not classifier output.
                signature=bytes.fromhex('3a822da96b03009a')
                found=0;pos=0
                while (pos:=b.find(signature,pos))>=0:
                    found+=1;pos+=len(signature)
                assert found==expected
                if expected:
                    assert r['instances'][0]['token']=='822da9'
                    assert r['instances'][0]['base_identity']=='starfield.esm:05ef19'
                if s['label'] in ('S7','S7C','exit'):
                    # Independent retained-object signatures from EXP0003.
                    for retained in ('3a822c5d03070192','3a822d486b03009a','3a822dba0f030092'):
                        assert b.find(bytes.fromhex(retained))>=0
            elif s['series']=='output-link-L0-L2C':
                assert s['count']==1
            assert s['unknown']==0 and s['rejected']==0
            for obj in r['instances']:
                assert obj['definition']['associations'][0]['item_identity'] is not None
        assert identity(p)==pin
        receipts.append(dict(series=s['series'],label=s['label'],PASS=True,source=pin,
                             independently_walked=len(other),count=s['count']))
    from research_extractor_resources import write
    write(out/'corpus-tests.json',receipts)
    print('CORPUS PASS',len(receipts),'labels;',sum(r['independently_walked'] for r in receipts),'records')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--corpus-run',type=Path);args=ap.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ExtractorTests)
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():raise SystemExit(1)
    if args.corpus_run:corpus(args.corpus_run)
