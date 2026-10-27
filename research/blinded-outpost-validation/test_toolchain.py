# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable original synthetic tests; no game/raw-save/history inputs.

Reads task source and unchanged owned arithmetic, writes only fresh temporary
trees under the task's ignored workspace. Tests protocol behavior independently
of prediction accuracy. unittest/stdlib only. No live acquisition or network.
"""
import copy
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import importlib.util

import bridge
import compare
import gate
from predict import predict

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT/'.local-work/blinded-outpost-validation'
HERE = Path(__file__).parent


def location(body='Kreet'):
    return dict(schema='sor-blind-location/1', trial='1'*32, body=body,
        body_formid=bridge.BODIES[body], workshop='2'*16, beacon_token='000001',
        position_le=struct.pack('<3f', -0.0, 1.0000001192092896, -1.0).hex(),
        compensation_le='00'*12, frame=0x2b, chart=0, descriptor=[19200, 19200],
        effective='UNKNOWN', receipt='3'*64)


def region(x=0.0):
    return dict(resource='00000001', points_le=struct.pack('<4f', x, 0, 0, 1).hex(),
                bound_le=struct.pack('<4f', x, 0, 0, 1).hex())


def comparable():
    return dict(schema='sor-blind-comparable/1', trial='1'*32, body='SYNTHETIC',
        body_formid='00000001', workshop='2'*16, session='4'*32, epoch='5'*32,
        scope_complete=True, sources=[dict(source='0:19200:19200:00000001',
            alternatives=[dict(mask=0, regions=[region()], presence=['00000001']),
                          dict(mask=3, regions=[region(1.0)], presence=['00000001'])])])


def truth(p=None, winner=0):
    p = p or comparable()
    t = {k: p[k] for k in ('trial', 'body', 'body_formid', 'workshop', 'session', 'epoch')}
    return dict(t, schema='sor-blind-truth/1', oracle='SYNTHETIC_WORKSHOP_TRANSFER', complete=True,
        sources=[dict(source=s['source'], regions=copy.deepcopy(s['alternatives'][winner]['regions']),
                      presence=list(s['alternatives'][winner]['presence'])) for s in p['sources']])


def bundle(path, prediction):
    path.mkdir()
    for name in gate.METHODS:
        (path/name).write_bytes((HERE/name).read_bytes())
    for name, source in gate.OWNED.items():
        (path/name).write_bytes(source.read_bytes())
    for name in gate.POLICY_FILES.values():
        if not (path/name).exists():
            (path/name).write_bytes(gate.canonical(dict(kind='SYNTHETIC', trial=prediction['trial'])))
    (path/'prediction.json').write_bytes(gate.canonical(prediction))
    # Explicit synthetic runtime/worker markers exercise binding and tamper
    # checks; they are never represented as an executed prediction runtime.
    runtime = path.parent/(path.name+'-synthetic-runtime'); runtime.mkdir()
    (runtime/'synthetic.txt').write_bytes(b'SYNTHETIC NONEXECUTABLE RUNTIME\n')
    (path/'worker.py').write_bytes(b"raise RuntimeError('Synthetic comparator fixture; no prediction worker invoked')\n")
    (path/'runtime-manifest.json').write_bytes(gate.canonical({'synthetic.txt': gate.digest((runtime/'synthetic.txt').read_bytes())}))
    (path/'dependencies.json').write_bytes(gate.canonical(dict(schema='sor-blind-dependencies/1', kind='SYNTHETIC',
        worker='worker.py', worker_sha256=gate.digest((path/'worker.py').read_bytes()),
        modules={n: gate.digest((path/n).read_bytes()) for n in gate.OWNED}, runtime_root=str(runtime),
        runtime_manifest_sha256=gate.digest((path/'runtime-manifest.json').read_bytes()))))
    protocol = dict(schema='sor-blind-protocol/1', **{k: {v: gate.digest((path/v).read_bytes())} for k, v in gate.POLICY_FILES.items()})
    (path/'protocol.json').write_bytes(gate.canonical(protocol))
    return gate.digest(gate.canonical(gate.files(path)))


class LocationTests(unittest.TestCase):
    def test_all_bodies_unknown_and_deterministic(self):
        for body in bridge.BODIES:
            first = gate.canonical(predict(location(body)))
            self.assertEqual(first, gate.canonical(predict(location(body))))
            result = json.loads(first)
            self.assertFalse(result['scope_complete'])
            self.assertEqual(result['classification'], 'UNSUPPORTED')
            compare.validate_prediction(result)

    def test_binary32_preserved(self):
        row = location()
        self.assertEqual(bridge.validate(row)['position_le'], '000000800100803f000080bf')

    def test_allowlist_injection(self):
        for field in ('resource_formids', 'extractors', 'source_regions', 'winner', 'log', '../truth.json'):
            row = location(); row[field] = ['000057c4']
            with self.assertRaises(ValueError): bridge.validate(row)
        for field in ('body', 'body_formid', 'workshop', 'beacon_token', 'position_le', 'receipt'):
            row = location(); row[field] += ' Copper 000057c4'
            with self.assertRaises(ValueError): bridge.validate(row)

    def test_ambiguity_absence_and_frames(self):
        row = {k: v for k, v in location().items() if k not in ('schema', 'trial', 'effective', 'receipt')}
        table = dict(schema='sor-blind-location-table/1', exe=bridge.EXE, esm=bridge.ESM, planet=bridge.PLANET, receipt='3'*64, rows=[row])
        self.assertEqual(bridge.extract(table, '1'*32, '2'*16), location())
        for rows in ([], [row, row]):
            bad = dict(table, rows=rows)
            with self.assertRaises(ValueError): bridge.extract(bad, '1'*32, '2'*16)
        for field, value in (('frame', 99), ('frame', 11.0), ('frame', 43.0), ('chart', 2), ('chart', True), ('descriptor', None),
                             ('effective', 'QUALIFIED'), ('body_formid', '00000001'),
                             ('position_le', '0000c07f'+'00'*8)):
            bad = location(); bad[field] = value
            with self.assertRaises(ValueError): bridge.validate(bad)
        table['exe'] = '0'*64
        with self.assertRaises(ValueError): bridge.extract(table, '1'*32, '2'*16)

    def test_duplicate_fields(self):
        with self.assertRaises(ValueError): bridge.loads('{"frame":11,"frame":43}')
        with self.assertRaises(ValueError): bridge.loads('{"x":NaN}')


class ComparatorTests(unittest.TestCase):
    def test_different_winner_is_valid(self):
        p = comparable(); before = gate.canonical(p)
        result = compare.compare(p, truth(p, 1))
        self.assertEqual(result['protocol'], 'COMPARABLE')
        self.assertEqual(result['sources'][0]['included_masks'], [3])
        self.assertEqual(before, gate.canonical(p))

    def test_mismatch_is_result(self):
        t = truth(); t['sources'][0]['regions'][0] = region(17.0)
        result = compare.compare(comparable(), t)
        self.assertEqual(result['protocol'], 'COMPARABLE')
        self.assertEqual(result['sources'][0]['result'], 'DISCREPANCY')
        self.assertFalse(result['accuracy_is_acceptance_criterion'])

    def test_signed_zero_width_bound_order_and_one_bit(self):
        p = comparable()
        for replacement in (region(-0.0), region(1.0000001192092896)):
            t = truth(); t['sources'][0]['regions'] = [replacement]
            result = compare.compare(p, t)
            self.assertEqual(result['sources'][0]['included_masks'], [])
        for field in ('points_le', 'bound_le'):
            t = truth(); r = t['sources'][0]['regions'][0]
            r[field] = r[field][:-8] + struct.pack('<f', 2.0).hex()
            self.assertEqual(compare.compare(p, t)['sources'][0]['included_masks'], [])
        p['sources'][0]['alternatives'][0]['regions'].append(region(2.0))
        t = truth(p); t['sources'][0]['regions'].reverse()
        self.assertFalse(compare.compare(p, t)['sources'][0]['alternatives'][0]['geometry_exact'])

    def test_identity_epoch_and_unqualified_oracles(self):
        for field in ('trial', 'body_formid', 'workshop', 'session', 'epoch'):
            t = truth(); t[field] = ('a' * len(t[field]))
            self.assertEqual(compare.compare(comparable(), t)['protocol'], 'ACQUISITION_FAILURE')
        for oracle in ('EXTRACTOR_SCREENSHOT', 'SAVED_EQUIPMENT', 'X_TECH'):
            t = truth(); t['oracle'] = oracle
            with self.assertRaises(ValueError): compare.compare(comparable(), t)
        t = truth(); t['oracle'] = 'ORDINARY_WORKSHOP_TRANSFER'
        with self.assertRaisesRegex(ValueError, 'UNQUALIFIED_NATIVE_CENSUS'): compare.compare(comparable(), t)

    def test_incomplete_is_not_negative_or_geometry_mismatch(self):
        t = truth(); t['complete'] = False
        result = compare.compare(comparable(), t)
        self.assertEqual(result['protocol'], 'INCOMPLETE_ACQUISITION')
        self.assertIsNone(result['sources'][0]['geometry_exact'])
        self.assertEqual(result['sources'][0]['absence'], 'UNKNOWN')
        self.assertTrue(result['sources'][0]['alternatives'][0]['all_observed_included'])
        t['sources'][0]['presence'] = []; t['sources'][0]['regions'] = []
        result = compare.compare(comparable(), t)
        self.assertEqual(result['scientific'], 'UNKNOWN_NO_POSITIVES')
        self.assertIsNone(result['sources'][0]['alternatives'][0]['all_observed_included'])

    def test_inconsistent_accepted_truth_refused(self):
        for complete in (True, False):
            t = truth(); t['complete'] = complete; t['sources'][0]['presence'] = []
            with self.assertRaisesRegex(ValueError, 'INCONSISTENT_ACCEPTED_REGION'):
                compare.compare(comparable(), t)
        t = truth(); t['sources'][0]['regions'][0]['points_le'] = ''
        with self.assertRaisesRegex(ValueError, 'INCONSISTENT_ACCEPTED_REGION'):
            compare.compare(comparable(), t)

    def test_partial_geometry_match_does_not_hide_admission_disagreement(self):
        t = truth(); t['complete'] = False
        p = comparable(); p['sources'][0]['alternatives'][0]['presence'] = []
        result = compare.compare(p, t)
        row = result['sources'][0]
        self.assertEqual(result['protocol'], 'INCOMPLETE_ACQUISITION')
        self.assertTrue(row['alternatives'][0]['all_observed_included'])
        self.assertFalse(row['alternatives'][0]['admission_all_observed_included'])
        self.assertEqual(row['alternatives'][0]['observed_presence_unpredicted'], ['00000001'])
        self.assertEqual(row['presence']['00000001']['modeled'], 'SOME_ALTERNATIVES')
        p['sources'][0]['alternatives'][1]['presence'] = []
        row = compare.compare(p, t)['sources'][0]
        self.assertEqual(row['presence']['00000001']['modeled'], 'NONE_WITHIN_QUALIFIED_SCOPE')
        p['scope_complete'] = False
        self.assertEqual(compare.compare(p,t)['sources'][0]['presence']['00000001']['modeled'], 'UNKNOWN')
        p['sources'][0]['alternatives'][0]['presence'] = ['00000002']
        self.assertEqual(compare.compare(p,t)['sources'][0]['presence']['00000002']['observed'], 'UNKNOWN')

    def test_per_resource_conditional_and_unmodeled(self):
        p = comparable(); p['sources'][0]['alternatives'][0]['presence'] = []
        t = truth(p, 1); t['sources'][0]['presence'].append('00000002')
        row = compare.compare(p, t)['sources'][0]
        self.assertEqual(row['presence']['00000001']['modeled'], 'SOME_ALTERNATIVES')
        self.assertEqual(row['presence']['00000002']['modeled'], 'NONE_WITHIN_QUALIFIED_SCOPE')
        p['scope_complete'] = False
        self.assertEqual(compare.compare(p, t)['sources'][0]['presence']['00000002']['modeled'], 'UNKNOWN')
        t['sources'][0]['source'] = '0:19200:19212:00000001'
        self.assertEqual({r['result'] for r in compare.compare(p, t)['sources']}, {'GROUND_TRUTH_MISSING', 'UNMODELED'})


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gate-', dir=LOCAL)
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.registry = self.root/'registry'; self.registry.mkdir()
        self.bundle = self.root/'bundle'
        self.prediction = comparable()
        self.inventory = bundle(self.bundle, self.prediction)
        self.truthpath = self.root/'truth.json'; self.truthpath.write_bytes(gate.canonical(truth()))
        self.roles = ['location_custodian', 'prediction_runner', 'revelation_custodian', 'independent_gate', 'comparator']

    def freeze(self):
        return gate.freeze(self.registry, self.bundle, '1'*32, self.roles, self.inventory)

    def reveal(self, frozen):
        return gate.reveal(self.registry, self.bundle, '1'*32, frozen, self.truthpath, gate.digest(self.truthpath.read_bytes()))

    def test_normal_mismatch_and_alternate_freeze(self):
        frozen = self.freeze()
        t = truth(winner=1); self.truthpath.write_bytes(gate.canonical(t))
        result = self.reveal(frozen)
        self.assertEqual(result['comparison']['sources'][0]['included_masks'], [3])
        self.assertGreaterEqual(result['time_ns'], json.loads((self.registry/('1'*32)/'freeze.json').read_bytes())['time_ns'])
        with self.assertRaises(FileExistsError): self.reveal(frozen)

    def test_premature_reveal_refreeze_and_wrong_hash(self):
        with self.assertRaises(FileNotFoundError): self.reveal('0'*64)
        frozen = self.freeze()
        with self.assertRaises(FileExistsError): self.freeze()
        with self.assertRaises(ValueError): self.reveal('0'*64)
        with self.assertRaises(ValueError): gate.reveal(self.registry, self.bundle, '1'*32, frozen, self.truthpath, '0'*64)

    def test_prediction_code_protocol_and_sidecar_tamper(self):
        frozen = self.freeze()
        for name in ('prediction.json', 'protocol.json', 'compare.py', 'corpus.json', 'worker.py', 'geometry.py', 'dependencies.json'):
            path = self.bundle/name; old = path.read_bytes(); path.write_bytes(old + b' ')
            with self.assertRaises(ValueError): self.reveal(frozen)
            path.write_bytes(old)
        (self.bundle/'hidden.json').write_bytes(b'{}')
        with self.assertRaises(ValueError): self.reveal(frozen)
        self.assertEqual((self.registry/('1'*32)/'bundle/prediction.json').read_bytes(), gate.canonical(self.prediction))

    def test_runtime_and_transitive_bindings(self):
        frozen = self.freeze()
        runtime = self.root/'bundle-synthetic-runtime/synthetic.txt'
        runtime.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'RUNTIME_BYTES_CHANGED'): self.reveal(frozen)

    def test_unregistered_worker_module_and_manifest_rejected(self):
        for name in ('worker.py', 'geometry.py', 'runtime-manifest.json'):
            p = self.bundle/name; old = p.read_bytes(); p.unlink()
            inventory = gate.digest(gate.canonical(gate.files(self.bundle)))
            with self.assertRaises((ValueError, FileNotFoundError, KeyError)):
                gate.freeze(self.registry, self.bundle, '1'*32, self.roles, inventory)
            p.write_bytes(old)

    def test_path_traversal_and_missing_bound_category(self):
        with self.assertRaises(ValueError): gate.freeze(self.registry, self.bundle, '../truth', self.roles, self.inventory)
        (self.bundle/'nested').mkdir()
        with self.assertRaises(ValueError): gate.files(self.bundle)

    def test_missing_required_protocol_category(self):
        protocol = json.loads((self.bundle/'protocol.json').read_bytes())
        protocol['comparison'] = {'eligibility.json': gate.digest((self.bundle/'eligibility.json').read_bytes())}
        (self.bundle/'protocol.json').write_bytes(gate.canonical(protocol))
        inventory = gate.digest(gate.canonical(gate.files(self.bundle)))
        with self.assertRaisesRegex(ValueError, 'MISSING_REQUIRED_PROTOCOL_CATEGORY'):
            gate.freeze(self.registry, self.bundle, '1'*32, self.roles, inventory)

    def test_snapshot_tamper_and_backdated_record(self):
        frozen = self.freeze()
        raw = self.registry/('1'*32)/'freeze.json'
        old = raw.read_bytes(); data = json.loads(old); data['time_ns'] = 0
        raw.write_bytes(gate.canonical(data))
        with self.assertRaises(ValueError): self.reveal(frozen)
        raw.write_bytes(old)
        (self.registry/('1'*32)/'bundle/bridge.py').write_bytes(b'# changed\n')
        with self.assertRaises(ValueError): self.reveal(frozen)


class GeometryTests(unittest.TestCase):
    def test_unchanged_generator_alternatives(self):
        sys.path[:0] = [str(ROOT/'research/resource-geometry'), str(ROOT/'save-analysis/scripts')]
        from conditional import generate
        constants = (0x144f0416c,0x144f049f4,0x144f04654,0x144f048dc,0x144f052b0,
            0x144f052f8,0x144f03d80,0x144f03d40,0x144f03e00,0x144f03ed4,
            0x144f04178,0x144f03dc4,0x144f03d58,0x144f03e48,0x144f03fd4,0x144f03f50)
        corpus = dict(bodies={'00000001': dict(system=1, index=1)}, settings=[0.25]*6,
            generation_blocks={'test': [1, 1, 2, 2, 0, 0, 0, 100]}, constants={hex(k): 1.0 for k in constants})
        request = dict(body='00000001', chart=0, descriptor=[19200,19200], query=[0,0,0], radius=150, upper=100)
        source = dict(nominal=[2,2], source_origin_native=[-200,-200], source_key='0:19200:19200:00000001',
            selected=dict(resources=[dict(id='00000001', rarity=0, block='test')]))
        result = generate(corpus, request, source, [0,8])
        self.assertEqual([a['mask'] for a in result['alternatives']], [0,8])
        self.assertNotEqual(result['alternatives'][0]['weights_le'], result['alternatives'][1]['weights_le'])
        self.assertNotEqual(result['alternatives'][0]['paths'], result['alternatives'][1]['paths'])
        self.assertEqual(gate.canonical(result), gate.canonical(generate(corpus, request, source, [8,0])))
        invariant = generate(corpus, request, source, [0,3])
        self.assertEqual(invariant['classification'], 'INVARIANT')
        source['selected']['resources'][0]['rarity'] = 6
        with self.assertRaisesRegex(ValueError, 'UNSUPPORTED_NONZERO_RARITY6_WATER'):
            generate(corpus, request, source, [0,3])


def positive_rows():
    common = dict(kind='SAMPLE', pid=1, tid=2, thread_lifetime=3, updater_token=4,
                  updater_bp=4096, required_reads_complete=True)
    query = struct.pack('<6f', 0,0,0,0,0,0).hex()
    entry = dict(common, capture=1, site='updater_entry', frame_verified=True, query_read=True,
        query_raw=query, radius_bits=0x3f800000, upper_bits=0x3f800000)
    raw_region = bytearray(48); struct.pack_into('<4f', raw_region, 0, 0,0,0,1)
    struct.pack_into('<II', raw_region, 24, 1,1)
    resource = bytearray(48); struct.pack_into('<I', resource, 40, 1); resource[46] = 0x9f
    extra = bytearray(0xa0); extra[0x98:0xa0] = bytes.fromhex('2'*16)
    manager = bytearray(0x200); struct.pack_into('<2i', manager, 0xc8+4, 100,100)
    source = bytearray(0x70); struct.pack_into('<I', source, 0, 1)
    closure = bytearray(24); struct.pack_into('<2f', closure,16,1,1)
    shared = dict(raw_binding_extra=extra.hex(), temporary_set=5, binding_reference=6)
    accepted = dict(common, **shared, capture=2, site='region_accept', decision='ACCEPT', ancestry='BOUND_CALLBACK',
        source_context=dict(status='COMPLETE', owner_key_u32=1, raw_manager=manager.hex(), raw_source=source.hex()),
        selected=dict(status='COMPLETE', raw_resource=resource.hex()),
        geometry=dict(status='COMPLETE', raw_region=raw_region.hex(), ordered_xyzw=region()['points_le']),
        file_provenance=dict(main_file_identity=True), raw_descriptor=query,
        raw_closure=closure.hex(), resource_pointer=7)
    transfer = dict(common, **shared, capture=3, site='spatial_transfer_payload', ancestry='BOUND_TRANSFER',
        refresh_payload=dict(status='COMPLETE', members=[dict(pointer=7,raw=resource.hex())]))
    return [dict(kind='SESSION'), entry, dict(kind='ACK_ACCEPTED',capture=1,accepted=True),
        accepted, dict(kind='ACK_ACCEPTED',capture=2,accepted=True), transfer,
        dict(kind='ACK_ACCEPTED',capture=3,accepted=True)]


class TruthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('synthetic_consumer', ROOT/'research/resource-combined-acquisition/consumer.py')
        cls.module = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.module)

    def reduce(self, rows):
        from truth import reduce_positive
        raw = b''.join(gate.canonical(row) for row in rows)
        return reduce_positive(raw, gate.digest(raw), self.module, '00000001', ['00000001'],
                               '2'*16, '0:19200:19200:00000001', [0,19200,19200])

    def test_positive_only_and_missing_entry_ack(self):
        result = self.reduce(positive_rows())
        self.assertEqual(len(result['regions']), 1)
        self.assertFalse(result['complete'])
        rows = [r for r in positive_rows() if not (r.get('kind') == 'ACK_ACCEPTED' and r.get('capture') == 1)]
        self.assertEqual(self.reduce(rows)['regions'], [])

    def test_ack_before_sample_or_duplicate(self):
        rows = positive_rows(); ack = rows.pop(2); rows.insert(1, ack)
        with self.assertRaisesRegex(ValueError, 'ACK_BEFORE'): self.reduce(rows)
        rows = positive_rows(); rows.append(rows[-1])
        with self.assertRaisesRegex(ValueError, 'ACK_BEFORE'): self.reduce(rows)

    def test_all_intervening_invalidations(self):
        for kind in ('PHASE', 'LOSS', 'EXCEPTION', 'THREAD_END'):
            rows = positive_rows(); rows.insert(5, dict(kind=kind,tid=2))
            self.assertEqual(self.reduce(rows)['regions'], [], kind)
        rows = positive_rows(); entry = dict(rows[1], capture=4); rows.insert(5,entry)
        self.assertEqual(self.reduce(rows)['regions'], [])

    def test_incomplete_context_and_unrecognized_body(self):
        for field in ('required_reads_complete',):
            rows = positive_rows(); rows[3][field] = False
            self.assertEqual(self.reduce(rows)['regions'], [])
        rows = positive_rows(); rows[3]['source_context']['owner_key_u32'] = 99
        self.assertEqual(self.reduce(rows)['regions'], [])

    def test_independent_journal_hash(self):
        from truth import reduce_positive
        with self.assertRaisesRegex(ValueError, 'INDEPENDENT_JOURNAL'):
            reduce_positive(b'{}\n', '0'*64, self.module, '00000001', ['00000001'], '2'*16,
                            '0:19200:19200:00000001', [0,19200,19200])


if __name__ == '__main__':
    LOCAL.mkdir(exist_ok=True)
    unittest.main(verbosity=2)
