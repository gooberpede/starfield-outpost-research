# SPDX-License-Identifier: GPL-3.0-or-later
"""Focused offline metadata/save gates using disposable synthetic files only.

Reads project code; build-source controls use synthetic manifests.
Writes temporary test files in task-owned scratch, removed on completion.
No real GO receipt, debugger, game, save, backup or archive operation occurs.
"""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from build import ROOT, pin
from collect_native import admission_checks
from prepare_native import SOURCE
from preservation_native import PREFLIGHT_SCHEMA, verify_build_files, postflight_comparison
from protection import metadata_diagnostic, sync_snapshot, sync_equal
from save_policy import snapshot, policy_hash
import protection
import save_policy
import preservation_native


class Preservation(unittest.TestCase):
    def setUp(self):
        scratch = ROOT/'.local-work/d5l-cloud-amendment'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='control-', dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.name = 'research.sfs'
        self.policy = dict(designated={self.name: dict(evidence='Synthetic designation')}, classified={})
        for folder in ('live', 'remote/Saves', 'backups'):
            p = self.root/folder
            p.mkdir(parents=True)
            (p/self.name).write_bytes(b'original')
        self.cache = self.root/'remotecache.vdf'
        self.cache.write_bytes(b'old metadata')
        self.files = {}
        for name in ('card.md', 'build.json', 'code.py', 'archive.bin', 'definition.esm', 'config.ini', 'Starfield.exe'):
            p = self.root/name
            p.write_bytes(b'synthetic')
            self.files[name] = p
        descriptor = lambda p: dict(path=str(p), sha256=pin(p))
        guard = lambda p: dict(bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns)
        live = snapshot(self.root/'live', self.policy)
        sync = dict(remote_path=str(self.root/'remote'), remote=snapshot(self.root/'remote/Saves', self.policy),
                    other={}, remotecache_sha256=pin(self.cache), matches_historical=False,
                    scientific_inputs_match=True)
        self.pre = dict(schema=PREFLIGHT_SCHEMA, status='OFFLINE_CHECKED_NOT_AUTHORIZED', source=SOURCE,
            save_policy=self.policy, save_policy_sha256=policy_hash(self.policy), live_path=str(self.root/'live'),
            protected_live=live, sync=sync, save52=self.name, code_pins={str(self.files['code.py']):pin(self.files['code.py'])},
            archive_guard={str(self.files['archive.bin']):guard(self.files['archive.bin'])},
            backups={self.name:[dict(path=str(self.root/'backups'/self.name), kind='LOOSE_BACKUP',
                sha256=pin(self.root/'backups'/self.name), metadata=guard(self.root/'backups'/self.name))]},
            installed={str(self.files['Starfield.exe']):dict(guard(self.files['Starfield.exe']), sha256=pin(self.files['Starfield.exe']))},
            file_guards={str(self.files[n]):guard(self.files[n]) for n in ('definition.esm', 'config.ini')},
            definitions={str(self.files['definition.esm']):pin(self.files['definition.esm'])},
            config={str(self.files['config.ini']):pin(self.files['config.ini'])},
            restore_rehearsal_sha256=pin(self.root/'backups'/self.name), operational_sources={},
            qualification=dict(path='synthetic',sha256='synthetic'), created_filetime_100ns=1,
            run_card=descriptor(self.files['card.md']), build_manifest=descriptor(self.files['build.json']))
        self.prepath = self.root/'preflight.json'
        self.refresh()
        self.gate = dict(status='GO', phase='B', source=SOURCE, synthetic=True,
            approval_reference='IN-MEMORY SYNTHETIC CONTROL; NO AUTHORITY', cloud_confirmed=True,
            allowed_interventions=['software_int3_14','all_stop_and_peer_suspend','owned_rip_tf_rearm','termination_teardown'],
            run_card=self.pre['run_card'], build_manifest=self.pre['build_manifest'],
            preflight=descriptor(self.prepath), creation_filetime_100ns=2, used=False)
        self.loader = patch.object(save_policy, 'load_policy', return_value=self.policy)
        self.loader.start()
        self.addCleanup(self.loader.stop)

    def refresh(self):
        self.prepath.write_text(json.dumps(self.pre), encoding='utf8')
        if hasattr(self, 'gate'):
            self.gate['preflight']['sha256'] = pin(self.prepath)

    def test_changed_metadata_admits_without_exception(self):
        self.cache.write_bytes(b'new synchronization state')
        self.assertNotEqual(pin(self.cache), self.pre['sync']['remotecache_sha256'])
        self.assertNotIn('cloud_metadata_decision', self.gate)
        admission_checks(self.gate)

    def test_missing_metadata_admits(self):
        self.cache.unlink()
        admission_checks(self.gate)

    def test_cloud_confirmation_still_required(self):
        self.gate['cloud_confirmed'] = False
        with self.assertRaises(AssertionError):
            admission_checks(self.gate)

    def test_old_receipt_rejected(self):
        self.pre['schema'] = 'sor-d5l-preflight/1'
        self.refresh()
        with self.assertRaises(AssertionError):
            admission_checks(self.gate)

    def test_light_admission_protected_names_sizes_and_other_inputs(self):
        admission_checks(self.gate)
        paths = [self.root/'live'/self.name, self.root/'remote/Saves'/self.name,
                 self.root/'backups'/self.name, *[self.files[n] for n in
                 ('archive.bin', 'definition.esm', 'config.ini', 'Starfield.exe', 'code.py')]]
        for p in paths:
            original = p.read_bytes()
            st = p.stat()
            for action in ('change', 'missing', 'substitute'):
                with self.subTest(path=p.name, action=action):
                    p.unlink()
                    if action == 'change':
                        p.write_bytes(b'changed length')
                    elif action == 'substitute':
                        p.with_suffix('.substitute').write_bytes(original)
                    with self.assertRaises((AssertionError, OSError)):
                        admission_checks(self.gate)
                    p.with_suffix('.substitute').unlink(missing_ok=True)
                    p.write_bytes(original)
                    import os
                    os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))

    def test_remote_non_save_change_rejected(self):
        (self.root/'remote/unexpected.bin').write_bytes(b'new')
        with self.assertRaises(AssertionError):
            admission_checks(self.gate)

    def test_metadata_postflight_drift_missing_and_read_failure_are_diagnostic(self):
        for value in ('different hash', None):
            after = copy.deepcopy(self.pre)
            after['sync']['remotecache_sha256'] = value
            self.assertTrue(postflight_comparison(self.pre, after)['ok'])
        self.cache.unlink()
        self.assertIsNone(metadata_diagnostic(self.cache)['sha256'])
        with patch.object(protection, 'pin', side_effect=PermissionError('synthetic')):
            self.assertEqual(metadata_diagnostic(self.cache)['status'], 'PermissionError')

    def test_full_postflight_same_length_substitution_and_missing_saves(self):
        for folder, field in (('live', 'protected_live'), ('remote/Saves', 'remote')):
            p = self.root/folder/self.name
            for data in (b'altered!', None):
                with self.subTest(folder=folder, data=data):
                    p.unlink(missing_ok=True)
                    if data is not None:
                        p.write_bytes(data)
                    after = copy.deepcopy(self.pre)
                    current = snapshot(p.parent, self.policy)
                    if field == 'remote':
                        after['sync']['remote'] = current
                    else:
                        after[field] = current
                    self.assertFalse(postflight_comparison(self.pre, after)['ok'])
            p.write_bytes(b'original')

    def test_postflight_other_scientific_input_and_identity_changes_rejected(self):
        for field in ('backups', 'installed', 'definitions', 'config', 'archive_guard',
                      'code_pins', 'operational_sources', 'build_manifest', 'source', 'qualification'):
            with self.subTest(field=field):
                after = copy.deepcopy(self.pre)
                after[field] = 'substituted'
                self.assertFalse(postflight_comparison(self.pre, after)['ok'])
        for field in ('remote_path', 'other'):
            after = copy.deepcopy(self.pre)
            after['sync'][field] = 'substituted'
            self.assertFalse(postflight_comparison(self.pre, after)['ok'])

    def test_snapshot_preflight_scientific_gate_ignores_only_metadata(self):
        prior = self.root/'.local-work/resource-carinae/sync-paths-preflight02.json'
        prior.parent.mkdir(parents=True)
        prior.write_text(json.dumps(dict(remote_path=str(self.root/'remote'),
            remote={'Saves/'+n:r for n,r in self.pre['sync']['remote'].items()},
            remotecache_sha256=pin(self.cache))), encoding='utf8')
        self.cache.write_bytes(b'new metadata')
        with patch.object(protection, 'ROOT', self.root):
            result = sync_snapshot(self.policy)
            self.assertTrue(result['scientific_inputs_match'])
            self.assertFalse(result['matches_historical'])
            (self.root/'remote/Saves'/self.name).write_bytes(b'altered!')
            self.assertFalse(sync_snapshot(self.policy)['scientific_inputs_match'])

    def test_build_amendment_has_no_native_or_arbitrary_python_exception(self):
        p = self.files['code.py']
        manifest = dict(files={str(p):pin(p)}, source_snapshots={})
        self.assertEqual(verify_build_files(manifest), {})
        p.write_bytes(b'changed')
        with self.assertRaises(AssertionError):
            verify_build_files(manifest)

    def test_operational_build_exception_requires_exact_original_snapshot(self):
        p = self.files['code.py']
        saved = self.root/'saved-code.py'
        saved.write_bytes(p.read_bytes())
        original = pin(p)
        manifest = dict(files={str(p):original}, source_snapshots={str(p):dict(path=str(saved), sha256=original)})
        p.write_bytes(b'amended operations')
        with patch.object(preservation_native, 'OPERATIONAL', {str(p)}):
            self.assertEqual(verify_build_files(manifest)[str(p)]['current_sha256'], pin(p))
            saved.write_bytes(b'corrupt old source')
            with self.assertRaises(AssertionError):
                verify_build_files(manifest)
        manifest['files'] = {str(p.with_suffix('.cpp')):'old'}
        p.with_suffix('.cpp').write_bytes(b'changed native')
        with self.assertRaises(AssertionError):
            verify_build_files(manifest)


if __name__ == '__main__':
    unittest.main()
