# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic contract tests with disposable receipt files only; no game input."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from admission import admit, useful_transfer
from qualify import independent, preserve


class Contract(unittest.TestCase):
    def test_joint_transfer_requires_all_resources_and_complete_frame(self):
        row = dict(ancestry='BOUND_TRANSFER', required_reads_complete=True,
                   refresh_payload=dict(status='COMPLETE', members=[dict(pointer=i) for i in (1, 2, 3)]))
        accepted = {1: 0x57c7, 2: 0x57c9, 3: 0x5df1}
        self.assertTrue(useful_transfer(row, accepted))
        self.assertFalse(useful_transfer(row, {1: 0x57c7}))
        self.assertFalse(useful_transfer(dict(row, ancestry='UNKNOWN'), accepted))
        self.assertFalse(useful_transfer(dict(row, required_reads_complete=False), accepted))
        self.assertFalse(useful_transfer(row, {}))

    def test_frame_projection_preserves_width_and_rounds_binary32(self):
        import struct
        from investigate import translated_consumer
        raw = bytearray(48)
        struct.pack_into('<4f', raw, 0, -813.3619384765625, -729.5208740234375, 0, 25)
        row = dict(geometry=dict(raw_region=raw.hex(), ordered_xyzw=raw[:16].hex()))
        before = copy.deepcopy(row)
        result = translated_consumer([row], [900, 800])[0]
        self.assertEqual(row, before)
        self.assertEqual(struct.unpack('<4f', bytes.fromhex(result['geometry']['ordered_xyzw'])),
                         (86.6380615234375, 70.4791259765625, 0, 25))

    def test_missing_corpus_requires_exact_authority(self):
        old = {'Save52': dict(bytes=3, sha256='52'), 'Exitsave0': dict(bytes=4, sha256='exit')}
        live = {'Save52': old['Save52']}
        with self.assertRaises(AssertionError):
            admit(live, old, old)
        decision = dict(status='ACCEPT_CURRENT_CORPUS_PRESERVE_BACKUP',
            human_instruction='Synthetic approval fixture', card_sha256='card',
            missing={'Exitsave0': old['Exitsave0']}, added={}, restore_authorized=False)
        self.assertEqual(admit(live, old, old, decision, 'card'), (['Exitsave0'], []))
        current = dict(live, NewExit=dict(bytes=4, sha256='new'))
        with self.assertRaises(AssertionError):
            admit(current, old, old, decision, 'card')
        accepted = dict(decision, added={'NewExit': current['NewExit']})
        self.assertEqual(admit(current, old, old, accepted, 'card'), (['Exitsave0'], ['NewExit']))
        for field, value in (('card_sha256', 'other'), ('human_instruction', ''),
                             ('missing', {}), ('restore_authorized', True)):
            bad = dict(decision, **{field: value})
            with self.assertRaises(AssertionError):
                admit(live, old, old, bad, 'card')
        with self.assertRaises(AssertionError):
            admit({'Save52': dict(bytes=3, sha256='changed')}, old, old, decision, 'card')

    def test_receipt_loss_truncation_and_ack(self):
        root = Path(__file__).resolve().parents[2] / '.local-work/resource-carinae-source-context'
        with tempfile.TemporaryDirectory(prefix='contract-', dir=root) as temporary:
            folder = Path(temporary)
            row = dict(kind='SAMPLE', capture=1, required_reads_complete=True,
                       source_context=dict(status='INCOMPLETE'))
            preserve(folder, dict(kind='SESSION'), row)
            path = folder / 'capture-00001.bin'
            self.assertFalse(independent(path)[-1]['complete'])
            raw = path.read_bytes()
            path.write_bytes(raw[:-1])
            with self.assertRaises(AssertionError):
                independent(path)
            path.write_bytes(raw)
            ack = path.with_suffix('.ack.json')
            value = json.loads(ack.read_text())
            ack.write_text(json.dumps(dict(value, sha256='wrong')))
            with self.assertRaises(AssertionError):
                independent(path)
            ack.write_text(json.dumps(value))
            with self.assertRaises(FileExistsError):
                preserve(folder, dict(kind='SESSION'), row)


if __name__ == '__main__':
    unittest.main()
