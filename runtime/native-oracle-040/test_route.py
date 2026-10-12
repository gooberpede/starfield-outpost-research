# SPDX-License-Identifier: GPL-3.0-or-later
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import route_inspect as r
FIXTURE=Path(sys.argv.pop(1)) if len(sys.argv)>1 and not sys.argv[1].startswith('-') else None

def events():
 b=FIXTURE.read_bytes()
 return [r.decode(b[i:i+r.SIZE]) for i in range(0,len(b),r.SIZE)]
def first_chain():
 es=events();root=es[0]['invocation']
 return [e for e in es if e['invocation']==root or e['parent']==root]
class RouteTests(unittest.TestCase):
 def test_native_primary_fixture(self):
  rows=r.reconcile(events())['routes']
  self.assertEqual([x['path'] for x in rows[:4]],['SUPPLIED_REFERENCE','SEARCH_SHORTCUT','FALLBACK_REFERENCE','FALLBACK_NO_REFERENCE'])
  self.assertTrue(all(x['scientific_complete'] and x['grid'][0]['grid_equal'] for x in rows[:3]))
  self.assertEqual(rows[3]['reachability'],'FALLBACK');self.assertFalse(rows[3]['scientific_complete'])
  self.assertGreater(len({x['thread'] for x in rows}),1)
 def test_direct_reference_config_branch(self):
  rows=r.reconcile(events())['routes'];direct=next(x for x in rows if x['path']=='DIRECT_SUPPLIED_REFERENCE')
  self.assertTrue(direct['grid'][0]['grid_equal']);self.assertTrue(direct['scientific_complete'])
 def test_sentinel_and_explicit_selected_ancestry(self):
  rows=r.reconcile(events())['routes'];bound=[x for x in rows if x['selected_reference_bound']]
  self.assertEqual(len(bound),2);self.assertTrue(all(x['upstream_selected_reference'] for x in bound))
 def test_selected_request_mismatch(self):
  es=events();selection=next(e for e in es if e['kind']==48);selection['blobs']['source']['address']+=8
  row=next(x for x in r.reconcile(es)['routes'] if x.get('selected_reference_invocation')==selection['invocation'])
  self.assertFalse(row['selected_reference_bound'])
 def test_missing_outer_start(self):
  report=r.reconcile([e for e in first_chain() if e['kind']!=22]);self.assertTrue(report['incomplete_roots'])
 def test_missing_selection_end(self):
  es=[e for e in events() if e['kind']!=49]
  self.assertFalse(next(s for s in r.reconcile(es)['selections'] if s['kind']==48)['paired_normal'])
 def test_missing_grid_start(self):
  es=[e for e in first_chain() if e['kind']!=33]
  x=r.reconcile(es)['routes'][0]
  self.assertFalse(x['scientific_complete']);self.assertTrue(x['defects'])
 def test_missing_grid_end(self):
  es=[e for e in first_chain() if e['kind']!=34]
  self.assertFalse(r.reconcile(es)['routes'][0]['scientific_complete'])
 def test_out_of_order(self):
  es=first_chain();a=next(e for e in es if e['kind']==33);b=next(e for e in es if e['kind']==34)
  a['sequence'],b['sequence']=b['sequence'],a['sequence']
  self.assertFalse(r.reconcile(es)['routes'][0]['scientific_complete'])
 def test_unpaired_orphan(self):
  es=first_chain();child=next(e for e in es if e['kind']==33);child['parent']=12345678
  self.assertTrue(r.reconcile(es)['unpaired_or_orphan_children'])
 def test_thread_mismatch(self):
  es=first_chain();next(e for e in es if e['kind']==34)['thread']+=1
  self.assertFalse(r.reconcile(es)['routes'][0]['scientific_complete'])
 def test_wrong_reference(self):
  es=first_chain();next(e for e in es if e['kind']==34)['blobs']['ref']['address']+=8
  self.assertFalse(r.reconcile(es)['routes'][0]['grid'][0]['reference_bound'])
 def test_unreadable(self):
  es=first_chain();next(e for e in es if e['kind']==33)['blobs']['candidate']['ok']=False
  self.assertEqual(r.reconcile(es)['routes'][0]['grid'][0]['classification'],'UNQUALIFIED')
 def test_stale_source(self):
  es=first_chain();a=next(e for e in es if e['kind']==32);a['blobs']['candidate']['hex']='00'*44
  self.assertFalse(r.reconcile(es)['routes'][0]['grid'][0]['source_fresh'])
 def test_disagreement_is_result(self):
  es=first_chain();a=next(e for e in es if e['kind']==34);b=bytearray.fromhex(a['blobs']['candidate']['hex']);b[0x24]^=1;a['blobs']['candidate']['hex']=b.hex()
  g=r.reconcile(es)['routes'][0]['grid'][0];self.assertFalse(g['grid_equal']);self.assertEqual(g['classification'],'IDENTITY_BOUND_GENERIC_COMPONENT_REPLAY')
 def test_fallback_not_shortcut(self):
  rows=r.reconcile(events())['routes'];self.assertEqual(rows[2]['grid'][0]['path'],'FALLBACK_REFERENCE')
 def test_wrong_callsite(self):
  self.assertFalse(r.reconcile(first_chain(),0x140000000)['routes'][0]['scientific_complete'])
 def test_duplicate_sequence(self):
  es=first_chain();es[1]['sequence']=es[0]['sequence']
  with self.assertRaisesRegex(ValueError,'duplicate_sequence'):r.reconcile(es)
 def test_q_e_independent(self):
  es=first_chain();e=copy.deepcopy(es[0]);e.update(invocation=99999,parent=0,sequence=99999,kind=7);es.append(e)
  self.assertEqual(r.reconcile(es)['q_invocations'],[99999]);self.assertEqual(r.reconcile(es)['routes'][0]['path'],'SUPPLIED_REFERENCE')
 def test_unreadable_native_block_never_substitutes_zero(self):
  rows=r.reconcile(events())['routes'];bad=[g for row in rows for g in row['grid'] if any(e['invocation']==g['invocation'] and e['kind']==33 and e['blobs']['block']['address']==1 for e in events())]
  self.assertTrue(bad);self.assertTrue(all(g['classification']=='UNQUALIFIED' for g in bad))
 def test_unwind_with_cyclic_optional_metadata(self):
  es=events();children=[e for e in es if e['kind']==39];selections=[e for e in es if e['kind']==44]
  self.assertTrue(children and selections);self.assertTrue(all(e['status']==33 for e in children));self.assertTrue(all(e['status']==48 for e in selections))
  report=r.reconcile(es,0x140000000);self.assertTrue(report['incomplete_roots'])
 def test_unknown_unwind_discriminator_is_diagnostic(self):
  es=[e for e in first_chain() if e['kind']!=33];e=next(e for e in es if e['kind']==34);e['kind']=39;e['status']=999
  self.assertFalse(r.reconcile(es,0x140000000)['routes'][0]['scientific_complete'])
 def test_raw_durability_tail_and_corruption(self):
  data=FIXTURE.read_bytes()[:r.SIZE];e=r.decode(data)
  # One local derivative; never alter native primary bytes.
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'events.bin').write_bytes(data+b'partial')
   row=dict(offset=0,length=r.SIZE,sha256=hashlib.sha256(data).hexdigest(),**{k:e[k] for k in ('sequence','invocation','kind')})
   (p/'records.jsonl').write_bytes((json.dumps(row)+'\n').encode()+b'{"partial":')
   es,receipt=r.records(p);self.assertEqual(len(es),1);self.assertTrue(receipt['journal_incomplete_tail']);self.assertEqual(receipt['raw_unjournaled_bytes'],7)
   corrupted=bytearray(data);corrupted[-1]^=1;(p/'events.bin').write_bytes(corrupted)
   with self.assertRaisesRegex(ValueError,'record_integrity'):r.records(p)
if __name__=='__main__':unittest.main(verbosity=2)
