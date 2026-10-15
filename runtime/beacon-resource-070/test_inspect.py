# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable decoder/adversarial fixtures only; exclusive scratch under supplied
fixture directory. Reads native fixture WAL, never target/save/analysis state."""
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import unittest
from inspect_resources import inspect, decode, SIZE

ROOT=Path(sys.argv.pop(1)) if len(sys.argv)>1 else None

class Inspector(unittest.TestCase):
    def test_native_fixture(self):
        r=inspect(ROOT)
        self.assertEqual(r['status'],'RETIRED_INTEGRITY_OK',r['errors'])
        self.assertEqual(len(r['evaluations']),13)
        sets=[[m['form_id'] for p in e['populations'] if p for m in p['members']] for e in r['evaluations'][:5]]
        self.assertEqual(sets[:3],[sets[0]]*3)
        self.assertNotEqual(sets[0],sets[3]);self.assertEqual(sets[0],sets[4])
        self.assertTrue(all(0x57f5 in s for s in sets))
        self.assertEqual(r['evaluations'][0]['position']['xyz'][0],1)
        self.assertEqual(r['evaluations'][4]['position']['xyz'][0],4)
        self.assertEqual(r['evaluations'][0]['indexed_domain_type'],0x49)
        self.assertEqual(r['evaluations'][0]['preview_base_form_id'],0xabc123)
        self.assertEqual(r['milestone_A'],'NOT_TESTED_NO_DISPLAYED_UI_ORACLE')
        self.assertEqual(len(r['ui_updates']),4)
        for u in r['ui_updates'][:1]:
            self.assertTrue(u['complete_row_association'],u)
            self.assertEqual([m['form_id'] for m in u['rows']],[0x57c7,0x57f5])
            self.assertEqual(u['evaluation_candidates'],[1,2,3,5,6])
            self.assertEqual(u['native_ancestry'],'UNRESOLVED_ASYNCHRONOUS')
            self.assertEqual(u['native_input_row_reconciliation'],'AGREE')
        self.assertEqual([m['form_id'] for m in r['ui_updates'][2]['rows']],[0x57c7,0x57f5,0x83ec,0x83ec])
        self.assertEqual(r['ui_updates'][2]['native_input_row_reconciliation'],'AGREE')
        self.assertEqual(r['ui_updates'][3]['rows'][0]['status'],'UNKNOWN_ID')
        self.assertEqual(r['ui_updates'][3]['native_input_row_reconciliation'],'NOT_TESTED')
        self.assertEqual(r['evaluations'][5]['refresh_result'],0)
        self.assertEqual(r['evaluations'][5]['set_change'],'UNCHANGED_POPULATIONS')
        self.assertEqual(r['ui_updates'][0]['allocation_candidates'],[8])
        self.assertEqual(r['ui_updates'][1]['allocation_candidates'],[7])
        self.assertEqual(r['ui_updates'][2]['native_row_set_change'],'UNCHANGED')
        self.assertEqual(r['ui_updates'][1]['native_row_set_change'],'CHANGED')
        self.assertEqual(r['ui_updates'][0]['searched_after'],1)
        self.assertFalse(r['evaluations'][-1]['complete_snapshot'])

    def variant(self,name):
        p=ROOT/name;p.mkdir();shutil.copyfile(ROOT/'events.bin',p/'events.bin');shutil.copyfile(ROOT/'records.jsonl',p/'records.jsonl');return p

    def test_partial_raw(self):
        p=self.variant('partial-raw');b=(p/'events.bin').read_bytes();(p/'events.bin').write_bytes(b[:-7]);self.assertEqual(inspect(p)['status'],'INCOMPLETE')
    def test_partial_journal(self):
        p=self.variant('partial-wal');b=(p/'records.jsonl').read_bytes();(p/'records.jsonl').write_bytes(b[:-3]);self.assertIn('partial_journal_tail',inspect(p)['errors'])
    def test_corrupt_raw(self):
        p=self.variant('corrupt');b=bytearray((p/'events.bin').read_bytes());b[19]^=1;(p/'events.bin').write_bytes(b);self.assertIn('raw_integrity',inspect(p)['errors'])
    def test_tail(self):
        p=self.variant('tail')
        with (p/'events.bin').open('ab') as f:f.write(b'x')
        self.assertIn('unjournaled_raw_tail',inspect(p)['errors'])
    def test_unknown(self):
        b=bytearray(SIZE);struct.pack_into('<QII',b,128,1,0x18,0);e=decode(b);self.assertFalse(e['ref']['ok'])
    def test_invalid_blob(self):
        b=bytearray(SIZE);struct.pack_into('<QII',b,128,1,385,1)
        with self.assertRaises(ValueError):decode(b)
    def test_incomplete_row_constructor(self):
        p=self.variant('unpaired-row');raw=bytearray((p/'events.bin').read_bytes())
        for off in range(0,len(raw),SIZE):
            e=decode(raw[off:off+SIZE])
            if e['kind']==106 and e['phase']==2:
                struct.pack_into('<Q',raw,off+7*8,1);break
        (p/'events.bin').write_bytes(raw)
        lines=[]
        for i,off in enumerate(range(0,len(raw),SIZE),1):lines.append(json.dumps(dict(sequence=i,offset=off,length=SIZE,sha256=hashlib.sha256(raw[off:off+SIZE]).hexdigest()))+'\n')
        (p/'records.jsonl').write_text(''.join(lines),encoding='utf8')
        r=inspect(p);self.assertEqual(r['status'],'INCOMPLETE');self.assertTrue(r['errors'])
    def test_complete_evidence_worker_failure(self):
        p=self.variant('worker-failure');terminal=json.loads((ROOT/'retired.json').read_text());terminal.update(error='native_guard_changed',integrity_failure=True)
        (p/'failure.json').write_text(json.dumps(terminal),encoding='utf8')
        r=inspect(p);self.assertEqual(r['status'],'INSTRUMENT_FAILURE_VERIFIED_EVIDENCE');self.assertEqual(r['evidence_status'],'RETIRED_INTEGRITY_OK');self.assertEqual(r['terminal']['error'],'native_guard_changed')
    def test_malformed_position(self):
        p=self.variant('malformed-position');raw=bytearray((p/'events.bin').read_bytes())
        for off in range(0,len(raw),SIZE):
            e=decode(raw[off:off+SIZE])
            if e['kind']==101 and e['phase']==1:
                struct.pack_into('<I',raw,off+128+8,12);break
        (p/'events.bin').write_bytes(raw)
        lines=[json.dumps(dict(sequence=i,offset=off,length=SIZE,sha256=hashlib.sha256(raw[off:off+SIZE]).hexdigest()))+'\n' for i,off in enumerate(range(0,len(raw),SIZE),1)]
        (p/'records.jsonl').write_text(''.join(lines),encoding='utf8')
        r=inspect(p);self.assertFalse(r['evaluations'][0]['complete_snapshot']);self.assertIsNone(r['evaluations'][0]['position'])

if __name__=='__main__':unittest.main()
