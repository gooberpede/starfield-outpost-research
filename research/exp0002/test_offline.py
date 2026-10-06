# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic tests; temporary files only, no game or save access."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import prepare
import capture_contract as contract


class OfflineTests(unittest.TestCase):
    def test_aslr_domains(self):
        for base in (0x140000000, 0x7ff600000000):
            self.assertEqual(prepare.runtime_site(base, 0x89c2000, 0x2073cf0), base+0x2073cf0)
        for base, rva in ((0, 0), (0x140000001, 0), (0x140000000, 0x89c2000), (0x800000000000, 1)):
            with self.assertRaises(ValueError):
                prepare.runtime_site(base, 0x89c2000, rva)

    def test_pe_file_domain(self):
        sections = [(0x1000, 0x200, 0x400, 0x100)]
        self.assertEqual(prepare.file_offset(sections, 0x1080, 0x20), 0x480)
        for rva in (0x1100, 0xfff):
            with self.assertRaises(ValueError):
                prepare.file_offset(sections, rva, 8)

    def test_wrong_build(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'wrong.exe'
            path.write_bytes(b'not the approved executable')
            with self.assertRaisesRegex(ValueError, 'Wrong game build'):
                prepare.inspect_pe(path)

    def test_byte_comparison_and_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            a, b = Path(folder)/'a', Path(folder)/'b'
            a.write_bytes(b'one')
            b.write_bytes(b'one')
            self.assertTrue(prepare.equal_bytes(a, b))
            before = prepare.metadata(a)
            b.write_bytes(b'two')
            self.assertFalse(prepare.equal_bytes(a, b))
            self.assertEqual(before, prepare.metadata(a))

    def test_schema_and_role_filter(self):
        for cp in contract.CHECKPOINTS:
            contract.validate(contract.template(cp))
        record = contract.template('A2')
        record['references'].append(copy.deepcopy(record['references'][1]))
        with self.assertRaises(ValueError):
            contract.validate(record)
        record = contract.template('A2')
        record['references'][1]['role'] = 'extractor'
        with self.assertRaises(ValueError):
            contract.validate(record)

    def test_unknown_is_not_null_or_observed(self):
        for item in (contract.field(None, 'OBSERVED', 'GetWorkshop'), contract.field(5), contract.field(None, 'NULL_RESULT')):
            with self.assertRaises(ValueError):
                contract.check_field(item)

    def test_bad_coordinate_and_runtime_identity(self):
        record = contract.template('A2')
        coord = record['references'][0]['coordinates']['reference_xyz']
        coord.update(status='OBSERVED', value=[0, float('nan'), 1], source='synthetic')
        with self.assertRaises(ValueError):
            contract.validate(record)
        record = contract.template('A2')
        record.update(kind='RUNTIME', utc='2026-10-06T00:00:00+00:00', local_time='2026-10-06T11:00:00+11:00')
        with self.assertRaises(ValueError):
            contract.validate(record)

    def test_writer_guards_and_flush(self):
        with tempfile.TemporaryDirectory(dir=prepare.ROOT/'.local-work') as folder:
            with patch.object(prepare, 'OUTPUT', Path(folder)), patch.object(prepare.os, 'fsync', wraps=prepare.os.fsync) as sync:
                record = contract.template('A2')
                record.update(kind='SYNTHETIC', utc='2026-10-06T00:00:00+00:00', local_time='2026-10-06T11:00:00+11:00', terminal='RECORD_COMPLETE')
                path = contract.persist('checkpoint-a2.json', record)
                self.assertTrue(sync.called)
                contract.validate(json.loads(path.read_text()))
                with self.assertRaises(FileExistsError):
                    contract.persist('checkpoint-a2.json', record)
                with self.assertRaises(ValueError):
                    prepare.write_report('../escape.json', {})
                with self.assertRaises(ValueError):
                    contract.persist('arbitrary.json', record)
                with self.assertRaises(ValueError):
                    prepare.write_report('large.json', 'x'*(2*1024*1024))
                oversized = copy.deepcopy(record)
                oversized['player_state'] = contract.field('x'*32768, 'OBSERVED', 'synthetic')
                with self.assertRaisesRegex(ValueError, '32 KiB'):
                    contract.persist('checkpoint-a2.json', oversized)
                with self.assertRaises(json.JSONDecodeError):
                    json.loads(path.read_text()[:-3])
        with tempfile.TemporaryDirectory() as folder, patch.object(prepare, 'OUTPUT', Path(folder)):
            with self.assertRaises(ValueError):
                prepare.write_report('outside.json', {})

    def test_planned_samples_not_created(self):
        manifest = contract.manifest()
        self.assertEqual(len(manifest['samples']), 6)
        self.assertTrue(all(s['sha256'] is None and s['actual_filename'] is None for s in manifest['samples']))
        self.assertEqual(manifest['samples'][-1]['artifact_kind'], 'RUNTIME_CHECKPOINT_ONLY')


if __name__ == '__main__':
    unittest.main(verbosity=2)
