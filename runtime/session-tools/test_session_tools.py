# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable offline controls. All process/deployed/control contacts are mocked.
Archive tests write only a fresh TemporaryDirectory; no approved capture changes.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import archive
import adapter070
import common
import session

SPACE = {'C:/': 10**12, 'D:/': 10**12}


class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='sor-infrastructure-')
        self.root = Path(self.temp.name)
        self.p = self.root / 'raw'
        self.p.mkdir()
        self.s = dict(version='0.7.0', schema=7, pid=10, process_creation_filetime=20,
                      dll_sha256='dll', game_sha256='game', sfse_sha256='sfse', module_base='0x1000')
        self.m = dict(guards=[dict(site=32, length=5, original='e800000000')])
        self.put('ready.json', dict(self.s, capture_active=True, group_flush_spool=True))
        self.put('admission.json', dict(sole_thread_observed=True, owned_sites_original=True, dll_sha256='dll', startup_wait_ms=1))
        self.put('patches.json', dict(patches=[dict(rva=32, length=5, original_sha256=hashlib.sha256(bytes.fromhex('e800000000')).hexdigest())]))
        self.put('health.jsonl', dict(self.s, health_sequence=1, integrity_failure=False, failed=0))
        self.nonce = 'a' * 32
        self.request = dict(nonce=self.nonce)
        self.put('ack-' + self.nonce + '.json', dict(self.s, nonce=self.nonce, integrity_failure=False, failed=0))
        self.enter = contextlib.ExitStack()
        for mod in (session, archive):
            self.enter.enter_context(patch.object(mod, 'guard', return_value=SPACE))

    def tearDown(self):
        self.enter.close()
        self.temp.cleanup()

    def put(self, name, row):
        (self.p / name).write_text(json.dumps(row) + '\n', encoding='utf8')

    def test_valid_ready_ack_real_admission_contract(self):
        self.assertEqual(adapter070.status(self.p, self.m, self.s, self.request)['status'], 'READY_ACK')

    def test_no_request_does_not_accept_unrelated_ack(self):
        self.assertEqual(adapter070.status(self.p, self.m, self.s, None)['status'], 'WAITING_FRESH_ACK')

    def test_stale_other_nonce_waits(self):
        self.assertEqual(adapter070.status(self.p, self.m, self.s, dict(nonce='b'*32))['status'], 'WAITING_ACK')

    def test_mismatched_ack_identity_fails(self):
        self.put('ack-' + self.nonce + '.json', dict(self.s, nonce=self.nonce, pid=11))
        with self.assertRaisesRegex(ValueError, 'worker_identity'):
            adapter070.status(self.p, self.m, self.s, self.request)

    def test_mismatched_ack_nonce_fails(self):
        self.put('ack-' + self.nonce + '.json', dict(self.s, nonce='b'*32, failed=0, integrity_failure=False))
        with self.assertRaisesRegex(ValueError, 'ack_mismatch'):
            adapter070.status(self.p, self.m, self.s, self.request)

    def test_bad_hook_admission_fails(self):
        self.put('patches.json', dict(patches=[]))
        with self.assertRaises(AssertionError):
            adapter070.status(self.p, self.m, self.s, self.request)

    def test_worker_failure_distinct(self):
        self.put('failure.json', dict(error='disk'))
        self.assertEqual(adapter070.status(self.p, self.m, self.s, self.request)['status'], 'WORKER_FAILURE')

    def test_malformed_complete_health_fails(self):
        (self.p / 'health.jsonl').write_bytes(b'broken\n')
        with self.assertRaises(ValueError):
            adapter070.status(self.p, self.m, self.s, self.request)

    def test_inflight_partial_health_line_disclosed(self):
        with (self.p / 'health.jsonl').open('ab') as f:
            f.write(b'{')
        self.assertTrue(adapter070.health(self.p, self.s)['partial_current_line'])

    def test_stop_pending_distinct_from_retirement(self):
        (self.p / 'operator-stop.flag').write_bytes(b'STOP')
        self.assertEqual(adapter070.status(self.p, self.m, self.s, None)['status'], 'STOP_PENDING_RETIREMENT')

    def test_retirement_error(self):
        self.put('retired.json', dict(self.s, captured=10, last_durable_sequence=9, failed=0, integrity_failure=False))
        self.assertEqual(adapter070.status(self.p, self.m, self.s, None)['status'], 'RETIREMENT_ERROR')

    def test_retired(self):
        self.put('retired.json', dict(self.s, captured=10, last_durable_sequence=10, failed=0, integrity_failure=False))
        self.assertEqual(adapter070.status(self.p, self.m, self.s, None)['status'], 'RETIRED')

    def test_disk_floor_both_drives(self):
        for bad in ('C:/', 'D:/'):
            with self.assertRaisesRegex(ValueError, 'disk_guard'):
                common.guard(query=lambda d: common.FLOOR-1 if d == bad else 10**12)

    def test_disk_unavailable(self):
        def query(d):
            raise OSError('unavailable')
        with self.assertRaises(OSError):
            common.guard(query=query)

    def test_archive_temporary_reservation(self):
        with self.assertRaises(ValueError):
            common.guard({'D:/': 100}, query=lambda d: common.FLOOR+99)

    def test_exit_rotation_and_other_change(self):
        b = {'ExitSave_old.sfs': dict(sha256='x', size=1), 'Save3.sfs': dict(sha256='a', size=1)}
        a = {'ExitSave_new.sfs': dict(sha256='y', size=2), 'Save3.sfs': dict(sha256='b', size=1)}
        r = session.save_delta(b, a)
        self.assertEqual(len(r['exit_save_rotation']), 2)
        self.assertEqual(len(r['unexpected_changes']), 1)

    def test_metadata_change_is_not_content_change(self):
        r = session.save_delta({'a': dict(sha256='x', size=1, mtime_ns=1)}, {'a': dict(sha256='x', size=1, mtime_ns=2)})
        self.assertFalse(r['unexpected_changes'])
        self.assertEqual(len(r['metadata_only']), 1)

    def preflight(self):
        build = self.root / 'build'
        build.mkdir()
        common.fresh(build / 'build.json', {})
        loader = self.root / 'sfse_loader.exe'
        loader.write_bytes(b'fake loader')
        self.protected = self.root / 'protected.bin'
        self.protected.write_bytes(b'protected')
        pins = {str(loader): common.sha(loader), str(self.protected): common.sha(self.protected)}
        self.plan = self.root / 'plan.json'
        common.fresh(self.plan, dict(adapter='070', build=str(build), manifest_sha256=common.sha(build/'build.json'),
                                    extra_pins=pins, deployed=False, saves=str(self.p)))
        with patch.object(adapter070, 'full', return_value=self.m) as full, patch.object(adapter070, 'prelaunch_processes', return_value=[]):
            r = session.prelaunch(self.plan, common.sha(self.plan))
            full.assert_called_once()
        self.receipt = self.root / 'preflight.json'
        common.fresh(self.receipt, r)
        self.pin = common.sha(self.receipt)
        return r

    def test_preflight_receipt_reuse_and_changed_missing_inputs(self):
        self.preflight()
        with patch.object(adapter070, 'full', return_value=self.m):
            session.reuse(self.receipt, self.pin, full=True)
            self.protected.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'pinned_input_changed'):
                session.reuse(self.receipt, self.pin, full=True)
            self.protected.unlink()
            with self.assertRaises(FileNotFoundError):
                session.reuse(self.receipt, self.pin, full=True)

    def test_receipt_tampering(self):
        self.preflight()
        with self.receipt.open('ab') as f:
            f.write(b' ')
        with self.assertRaisesRegex(ValueError, 'receipt_identity'):
            session.reuse(self.receipt, self.pin)

    def test_lightweight_never_calls_full_or_hashes_corpus(self):
        self.preflight()
        self.protected.unlink()  # light phase intentionally cannot certify unseen drift
        with patch.object(adapter070, 'full', side_effect=AssertionError('full audit in live')), \
                patch.object(adapter070, 'session', return_value=(self.p, self.s)), \
                patch.object(adapter070, 'process', return_value='ACTIVE'), \
                patch.object(adapter070, 'deployed', return_value=[]), \
                patch.object(session, 'inventory', side_effect=AssertionError('corpus scan')):
            r = session.action('live', self.receipt, self.pin, self.p)
        self.assertEqual(r['status'], 'WAITING_FRESH_ACK')

    def test_request_session_binding(self):
        self.preflight()
        (self.p / ('control-' + self.nonce + '.request')).write_bytes(b'ACK\n')
        req = self.root/'request.json'
        common.fresh(req, dict(status='ACK_REQUESTED', nonce=self.nonce, session=str(self.p), identity=self.s, prelaunch_sha256='other'))
        with self.assertRaisesRegex(ValueError, 'request_receipt_mismatch'):
            session.bound_request(req, common.sha(req), self.p, self.s, self.pin)

    def test_stop_available_when_disk_guard_fails(self):
        self.preflight()
        (self.p/'operator-stop.flag').write_bytes(b'RUN\n')
        with patch.object(adapter070, 'session', return_value=(self.p, self.s)), patch.object(session, 'guard', side_effect=OSError('disk')):
            r = session.action('stop', self.receipt, self.pin, self.p)
        self.assertTrue(r['status'].startswith('STOP_REQUESTED'))
        self.assertEqual((self.p/'operator-stop.flag').read_bytes(), b'STOP')

    def test_stop_invalid_flag(self):
        (self.p/'operator-stop.flag').write_bytes(b'x')
        with self.assertRaisesRegex(ValueError, 'stop_flag_size'):
            adapter070.ops.stop_control(self.p)

    def test_postflight_incomplete_is_partial(self):
        self.preflight()
        with patch.object(adapter070, 'session', return_value=(self.p, self.s)), \
                patch.object(adapter070, 'process', return_value='EXITED'), \
                patch.object(adapter070, 'deployed'), patch.object(adapter070, 'full', return_value=self.m), \
                patch.object(adapter070, 'inspect', return_value=dict(status='VERIFIED_PREFIX')):
            r = session.action('postflight', self.receipt, self.pin, self.p)
        self.assertEqual(r['status'], 'PARTIAL_POSTFLIGHT')

    def sealed(self, partial=False):
        companion = self.root/'receipts'
        companion.mkdir()
        post = companion/'postflight.json'
        common.fresh(post, dict(action='postflight', process_state='EXITED', session=str(self.p),
                                status='PARTIAL_POSTFLIGHT' if partial else 'PASS_POSTFLIGHT'))
        roots = dict(raw=dict(path=str(self.p), kind='raw-capture'), receipts=dict(path=str(companion), kind='private-receipt'))
        s = archive.seal(roots, post, common.sha(post), 'crashed tail' if partial else None)
        seal = self.root/'seal.json'
        common.fresh(seal, s)
        return s, seal

    def zipped(self, s, path=None, omit=None, corrupt=None):
        path = path or self.root/'test.zip'
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr(archive.MANIFEST, json.dumps(s))
            for name in s['files']:
                if name == omit:
                    continue
                label, relative = name.split('/', 1)
                data = (Path(s['roots'][label]['path'])/relative).read_bytes()
                z.writestr(name, bytes(b ^ 1 for b in data) if name == corrupt else data)
        return path

    def test_round_trip_binary_and_inventory(self):
        (self.p/'bytes.bin').write_bytes(bytes(range(256))*2000)
        s, seal = self.sealed()
        z = self.zipped(s)
        self.assertEqual(archive.verify(z, s)['members'], len(s['files']))

    def test_create_actual_zip_pipeline(self):
        s, seal = self.sealed()
        z = self.root/'pipeline.zip'
        r = archive.create(seal, common.sha(seal), z)
        self.assertEqual(r['status'], 'VERIFIED_EVERY_MEMBER')
        self.assertEqual(archive.collect(s['roots']), s['files'])

    def test_changed_and_missing_sealed_source_refused(self):
        s, seal = self.sealed()
        (self.p/'ready.json').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'sealed_source_changed'):
            archive.create(seal, common.sha(seal), self.root/'changed.zip')
        (self.p/'ready.json').unlink()
        with self.assertRaisesRegex(ValueError, 'sealed_source_changed'):
            archive.create(seal, common.sha(seal), self.root/'missing.zip')

    def test_missing_member(self):
        s, _ = self.sealed()
        with self.assertRaisesRegex(ValueError, 'inventory_mismatch'):
            archive.verify(self.zipped(s, omit=next(iter(s['files']))), s)

    def test_corrupt_member(self):
        s, _ = self.sealed()
        with self.assertRaises(ValueError):
            archive.verify(self.zipped(s, corrupt=next(iter(s['files']))), s)

    def test_truncated_archive(self):
        s, _ = self.sealed()
        z = self.zipped(s)
        z.write_bytes(z.read_bytes()[:-25])
        with self.assertRaises(zipfile.BadZipFile):
            archive.verify(z, s)

    def test_duplicate_archive_member(self):
        s, _ = self.sealed()
        z = self.zipped(s)
        with zipfile.ZipFile(z, 'a') as f:
            with __import__('warnings').catch_warnings():
                __import__('warnings').simplefilter('ignore')
                f.writestr(archive.MANIFEST, '{}')
        with self.assertRaisesRegex(ValueError, 'duplicate_member'):
            archive.verify(z, s)

    def test_malicious_paths(self):
        for name in ('../a', '/a', 'C:/a', 'a\\b', 'a//b', 'a/./b', 'a/../b', 'a/NUL.txt', 'x.', 'x '):
            with self.subTest(name=name), self.assertRaises(ValueError):
                archive.validate_names([name])
        for names in (['a', 'A'], ['a', 'a/b']):
            with self.assertRaises(ValueError):
                archive.validate_names(names)

    def test_malicious_member_in_zip(self):
        s, _ = self.sealed()
        z = self.zipped(s)
        with zipfile.ZipFile(z, 'a') as f:
            f.writestr('../escape', b'x')
        with self.assertRaisesRegex(ValueError, 'unsafe_member'):
            archive.verify(z, s)

    def test_archive_hash_mismatch(self):
        s, _ = self.sealed()
        with self.assertRaisesRegex(ValueError, 'archive_hash_mismatch'):
            archive.verify(self.zipped(s), s, '0'*64)

    def test_partial_capture_explicit(self):
        s, _ = self.sealed(partial=True)
        self.assertEqual(s['status'], 'PARTIAL')
        self.assertEqual(archive.verify(self.zipped(s), s)['status'], 'VERIFIED_EVERY_MEMBER')

    def test_partial_not_silently_complete(self):
        s, _ = self.sealed(partial=True)
        post = self.root/'receipts/postflight.json'
        with self.assertRaisesRegex(ValueError, 'partial_reason_required'):
            archive.seal(s['roots'], post, common.sha(post))

    def test_output_cannot_enter_source(self):
        s, seal = self.sealed()
        with self.assertRaisesRegex(ValueError, 'output_inside'):
            archive.create(seal, common.sha(seal), self.p/'bad.zip')

    def test_exclusive_receipts(self):
        out = self.root/'new.json'
        common.fresh(out, {})
        with self.assertRaises(FileExistsError):
            common.fresh(out, {})

    def test_archive_generation_error_preserves_raw(self):
        s, seal = self.sealed()
        with patch.object(archive.zipfile.ZipFile, 'open', side_effect=OSError('simulated writer failure')):
            with self.assertRaises(OSError):
                archive.create(seal, common.sha(seal), self.root/'writer-failure.zip')
        self.assertEqual(archive.collect(s['roots']), s['files'])

    def test_archive_crc_error(self):
        s, _ = self.sealed()
        z = self.zipped(s)
        with zipfile.ZipFile(z) as f:
            item = f.infolist()[1]
            offset = item.header_offset + 30 + len(item.filename.encode()) + len(item.extra)
        data = bytearray(z.read_bytes())
        data[offset+1] ^= 0xff
        z.write_bytes(data)
        with self.assertRaises((zipfile.BadZipFile, __import__('zlib').error, ValueError)):
            archive.verify(z, s)

    def test_symlink_member(self):
        s, _ = self.sealed()
        z = self.root/'link.zip'
        with zipfile.ZipFile(z, 'w') as f:
            f.writestr(archive.MANIFEST, json.dumps(s))
            for name in s['files']:
                label, relative = name.split('/', 1)
                item = zipfile.ZipInfo(name)
                item.create_system = 3
                item.external_attr = 0o120777 << 16
                f.writestr(item, (Path(s['roots'][label]['path'])/relative).read_bytes())
        with self.assertRaisesRegex(ValueError, 'unsupported_member_type'):
            archive.verify(z, s)

    def test_new_save_is_not_exitsave_rotation(self):
        delta = session.save_delta({}, {'Save4.sfs': dict(size=1, sha256='new')})
        self.assertEqual(len(delta['unexpected_changes']), 1)

    def test_missing_ready_waits(self):
        (self.p/'ready.json').unlink()
        self.assertEqual(adapter070.status(self.p, self.m, self.s, self.request)['status'], 'WAITING_READY')

    def test_request_publish_and_bound_ack_round_trip(self):
        self.preflight()
        with patch.object(adapter070, 'session', return_value=(self.p, self.s)), \
                patch.object(adapter070, 'process', return_value='ACTIVE'), patch.object(adapter070, 'deployed', return_value=[]):
            req = session.action('request', self.receipt, self.pin, self.p)
            request_path = self.root/'fresh-request.json'
            common.fresh(request_path, req)
            self.put('ack-' + req['nonce'] + '.json', dict(self.s, nonce=req['nonce'], integrity_failure=False, failed=0))
            result = session.action('live', self.receipt, self.pin, self.p, request_path, common.sha(request_path))
        self.assertEqual(result['status'], 'READY_ACK')

    def test_postflight_protected_failure_cannot_pass(self):
        self.preflight()
        self.protected.write_bytes(b'changed')
        with patch.object(adapter070, 'session', return_value=(self.p, self.s)), \
                patch.object(adapter070, 'process', return_value='EXITED'), patch.object(adapter070, 'deployed'), \
                patch.object(adapter070, 'full', return_value=self.m), \
                patch.object(adapter070, 'inspect', return_value=dict(status='RETIRED_INTEGRITY_OK')):
            result = session.action('postflight', self.receipt, self.pin, self.p)
        self.assertEqual(result['status'], 'PARTIAL_POSTFLIGHT')
        self.assertTrue(result['protection_errors'])

    def test_postflight_active_process_refused(self):
        self.preflight()
        with patch.object(adapter070, 'session', return_value=(self.p, self.s)), patch.object(adapter070, 'process', return_value='ACTIVE'):
            with self.assertRaisesRegex(ValueError, 'not_confirmed_gone'):
                session.action('postflight', self.receipt, self.pin, self.p)

    def test_seal_unknown_exit_refused(self):
        s, _ = self.sealed()
        post = self.root/'receipts/postflight.json'
        row = common.read(post)
        row['process_state'] = 'UNKNOWN_ACCESS_ERROR'
        post.write_text(json.dumps(row), encoding='utf8')
        with self.assertRaisesRegex(ValueError, 'offline_postflight_required'):
            archive.seal(s['roots'], post, common.sha(post), 'unknown')

    def test_cli_mismatch_has_durable_failure_receipt(self):
        plan = self.root/'bad-plan.json'
        common.fresh(plan, {})
        out = self.root/'failure-receipt.json'
        import subprocess
        import sys
        result = subprocess.run([sys.executable, '-E', '-B', str(Path(session.__file__)), 'prelaunch', '--input', str(plan),
                                 '--sha256', '0'*64, '--out', str(out)], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(common.read(out)['status'], 'CHECK_ERROR')

    def test_inventory_detects_mid_hash_mutation(self):
        victim = self.p/'ready.json'
        real_sha = common.sha
        def mutating_sha(p):
            digest = real_sha(p)
            if p == victim:
                p.write_bytes(b'changed during hash')
            return digest
        with patch.object(common, 'sha', side_effect=mutating_sha):
            with self.assertRaisesRegex(ValueError, 'changed_during_inventory'):
                common.inventory(self.p)

    def test_preexisting_session_refused(self):
        self.preflight()
        row = common.read(self.receipt)
        row['existing_sessions'].append(self.p.name)
        self.receipt.write_text(json.dumps(row), encoding='utf8')
        with patch.object(adapter070, 'session', return_value=(self.p, self.s)):
            with self.assertRaisesRegex(ValueError, 'preexisting_session'):
                session.action('live', self.receipt, common.sha(self.receipt), self.p)

    def test_missing_worker_integrity_is_not_healthy(self):
        self.put('ack-' + self.nonce + '.json', dict(self.s, nonce=self.nonce))
        with self.assertRaisesRegex(ValueError, 'worker_integrity_fields'):
            adapter070.status(self.p, self.m, self.s, self.request)


if __name__ == '__main__':
    unittest.main(verbosity=2)
