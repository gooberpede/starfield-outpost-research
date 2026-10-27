# SPDX-License-Identifier: GPL-3.0-or-later
"""Synthetic pre/post/audit regressions; temporary files stay in ignored scratch.

No original save, backup, game process, configuration or Git writes.
"""
import copy
import hashlib
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from save_policy import classify, partition, compare, admission, snapshot, policy_hash
from admission import admit
from protection import audit_rows, sync_equal


def name(kind='Save', slot=52, timestamp='20261023053108'):
    return f'{kind}{slot}_BA75E3CDM43616F205472616E_580746_{timestamp}_319_15_4.sfs'


def row(value):
    b = value.encode()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


class SaveProtection(unittest.TestCase):
    def setUp(self):
        self.manual = name()
        self.exit = name('Exitsave', 0)
        self.auto = name('Autosave', 1)
        self.quick = name('Quicksave', 0)
        self.old = {self.manual: row('research'), self.exit: row('exit'),
                    self.auto: row('auto'), self.quick: row('quick')}
        self.policy = dict(designated={self.manual: dict(self.old[self.manual], evidence='Synthetic research designation')}, classified={})

    def both(self, current, expected):
        # These are the same gate functions called by the operational preflight
        # and postflight; historic backup bytes remain independent of live churn.
        pre = admission(current, self.old, self.old, self.policy)
        post = compare(self.old, current, self.policy)
        self.assertEqual(pre['ok'], expected)
        self.assertEqual(post['ok'], expected)
        if expected:
            self.assertEqual(admit(current, self.old, self.old, self.policy), pre)
        else:
            with self.assertRaises(AssertionError):
                admit(current, self.old, self.old, self.policy)

    def test_native_grammar_kinds_flags_and_bounds(self):
        for kind, slot, expected in [('Save', 52, 'PROTECTED'), ('Quicksave', 0, 'PROTECTED'),
                                      ('Autosave', 1, 'TRANSIENT'), ('Exitsave', 0, 'TRANSIENT')]:
            for flags in ('M', 'S', 'SM', '_'):
                n = name(kind, slot).replace('CDM', 'CD'+flags)
                self.assertEqual(classify(n, self.policy)['protection'], expected)

    def test_exit_creation_removal_replacement_rotation(self):
        for change in ('create', 'remove', 'replace', 'rotate'):
            with self.subTest(change=change):
                current = copy.deepcopy(self.old)
                newer = name('Exitsave', 0, '20261023063108')
                if change in ('remove', 'rotate'):
                    del current[self.exit]
                if change in ('create', 'rotate'):
                    current[newer] = row('new exit')
                if change == 'replace':
                    current[self.exit] = row('replacement')
                self.both(current, True)

    def test_autosave_churn(self):
        for change in ('create', 'remove', 'replace', 'rotate'):
            with self.subTest(change=change):
                current = copy.deepcopy(self.old)
                newer = name('Autosave', 2, '20261023063108')
                if change in ('remove', 'rotate'):
                    del current[self.auto]
                if change in ('create', 'rotate'):
                    current[newer] = row('new auto')
                if change == 'replace':
                    current[self.auto] = row('replacement')
                self.both(current, True)

    def test_designated_save52_changed_removed_with_transient_churn(self):
        for remove in (False, True):
            current = copy.deepcopy(self.old)
            if remove:
                del current[self.manual]
            else:
                current[self.manual] = row('corruption')
            del current[self.exit]
            current[name('Autosave', 2)] = row('new auto')
            self.both(current, False)

    def test_new_changed_removed_manual_save(self):
        n = name('Save', 53)
        for before, after in ((self.old, dict(self.old, **{n: row('new')})),
                              (dict(self.old, **{n: row('old')}), dict(self.old, **{n: row('new')})),
                              (dict(self.old, **{n: row('old')}), self.old)):
            self.assertFalse(admission(after, before, before, self.policy)['ok'])
            self.assertFalse(compare(before, after, self.policy)['ok'])

    def test_quicksaves_remain_protected(self):
        current = dict(self.old)
        current[self.quick] = row('changed quick')
        self.both(current, False)
        del current[self.quick]
        self.both(current, False)

    def test_missing_corrupt_backup_including_archived_transient(self):
        for n in (self.manual, self.exit):
            for remove in (True, False):
                backup = dict(self.old)
                if remove:
                    del backup[n]
                else:
                    backup[n] = row('corrupt backup')
                self.assertFalse(admission(self.old, backup, self.old, self.policy)['ok'])

    def test_ambiguous_names_kinds_fail_closed(self):
        for n in ('funclist.sfs', 'containsAutosave.sfs', 'Autosave1_manual.sfs',
                  name('Exitsave', 1), name('Exitsave', 0, '20261323053108'),
                  self.exit.replace('_580746_', '_0000000_'),
                  self.exit.replace('M43616F', 'M00616F'),
                  name('Exitsave', 0)+'.bak', 'archive/'+self.exit):
            with self.subTest(name=n):
                self.assertEqual(classify(n, self.policy)['protection'], 'UNCLASSIFIED')
                self.both(dict(self.old, **{n: row('unknown')}), False)
        with self.assertRaises(AssertionError):
            partition({self.exit: row('a'), self.exit.upper(): row('b')}, self.policy)

    def test_designated_transients_override_kind_prospectively(self):
        for n in (self.exit, self.auto):
            self.policy['designated'][n] = dict(self.old[n], evidence='Explicit later research designation')
            self.assertEqual(classify(n, self.policy)['protection'], 'PROTECTED')
            current = dict(self.old)
            del current[n]
            self.both(current, False)
            current[n] = row('changed designated transient')
            self.both(current, False)
        late = name('Autosave', 2)
        self.policy['designated'][late] = dict(row('late'), evidence='Later exact prospective baseline')
        self.assertFalse(admission(dict(self.old, **{late: row('late')}), self.old, self.old, self.policy)['ok'])
        qualified = dict(self.old, **{late: row('late')})
        self.assertTrue(admission(qualified, qualified, qualified, self.policy)['ok'])
        self.assertFalse(admission(dict(self.old, **{late: row('wrong')}), self.old, self.old, self.policy)['ok'])

    def test_explicit_classification_and_policy_identity(self):
        p = copy.deepcopy(self.policy)
        p['classified']['unknown.sfs'] = dict(kind='QUICK', evidence='Synthetic maintainer classification')
        self.assertEqual(classify('unknown.sfs', p)['protection'], 'PROTECTED')
        self.assertNotEqual(policy_hash(p), policy_hash(self.policy))

    def test_broad_audit_skips_only_active_transients(self):
        # This is a disposable file-policy control, not a real archive audit.
        archived = patch('protection.archived_expectations', return_value={})
        archived.start()
        self.addCleanup(archived.stop)
        root = Path(__file__).resolve().parents[2]/'.local-work/resource-carinae-transient-saves'
        with tempfile.TemporaryDirectory(prefix='policy-', dir=root) as temporary:
            base = Path(temporary)
            live, archive = base/'live', base/'archive'
            live.mkdir(); archive.mkdir()
            rows = []
            for folder in (live, archive):
                for n in (self.manual, self.exit):
                    (folder/n).write_text('old', encoding='utf8')
                    rows.append(dict(path=str(folder/n), sha256=row('old')['sha256'], match=True))
            (live/self.exit).unlink()
            (live/name('Autosave', 2)).write_text('new', encoding='utf8')
            self.assertFalse(audit_rows(rows, live, self.policy)['changes'])
            (archive/self.exit).write_text('corrupt', encoding='utf8')
            self.assertTrue(audit_rows(rows, live, self.policy)['changes'])
            (archive/self.exit).write_text('old', encoding='utf8')
            (live/self.manual).write_text('corrupt', encoding='utf8')
            self.assertTrue(audit_rows(rows, live, self.policy)['changes'])
            (live/self.manual).write_text('old', encoding='utf8')
            (live/'ambiguous.sfs').write_text('unknown', encoding='utf8')
            self.assertTrue(audit_rows(rows, live, self.policy)['changes'])
            (live/'ambiguous.sfs').unlink()
            (live/name('Save', 53)).write_text('new', encoding='utf8')
            self.assertTrue(audit_rows(rows, live, self.policy)['changes'])

    def test_transient_read_race_is_diagnostic_protected_read_race_fails(self):
        root = Path(__file__).resolve().parents[2]/'.local-work/resource-carinae-transient-saves'
        with tempfile.TemporaryDirectory(prefix='race-', dir=root) as temporary:
            folder = Path(temporary)
            p = folder/self.exit
            p.write_text('transient', encoding='utf8')
            with patch.object(Path, 'open', side_effect=PermissionError('synthetic transient read race')):
                self.assertEqual(snapshot(folder, self.policy)[self.exit]['diagnostic'], 'PermissionError')
            p.unlink()
            (folder/self.manual).write_text('protected', encoding='utf8')
            with patch.object(Path, 'open', side_effect=PermissionError('synthetic protected read failure')):
                with self.assertRaises(PermissionError):
                    snapshot(folder, self.policy)

    def test_root_reparse_rejected(self):
        # A mocked root reparse flag exercises the strict root guard without
        # creating symlinks or changing any real filesystem permissions.
        with patch.object(Path, 'is_dir', return_value=True), patch.object(Path, 'lstat', return_value=SimpleNamespace(st_file_attributes=0x400)):
            with self.assertRaises(AssertionError):
                snapshot(Path('synthetic'), self.policy)

    def test_steam_metadata_is_diagnostic_remote_saves_stay_strict(self):
        before = dict(remote_path='root', remote=self.old, other={}, remotecache_sha256='fixed')
        after = dict(before, remote={n: r for n, r in self.old.items() if n != self.exit})
        self.assertTrue(sync_equal(before, after, self.policy))
        self.assertTrue(sync_equal(before, dict(after, remotecache_sha256='changed'), self.policy))
        self.assertFalse(sync_equal(before, dict(after, remote={}), self.policy))


if __name__ == '__main__':
    unittest.main()
