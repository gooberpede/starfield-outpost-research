# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise archive refusals and optional mutations of the exact Workshop projection."""
from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import sys
import unittest
import warnings
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bx_workshop_archive import EPOCH, NAMES, encoded, fingerprint, quest_operand, read_archive, write_archive
from research_workshop_roots import supplement
from verify_d5bx_workshop import ASSETS, check_alla_keywords, check_canonical, replay_baseline

CANDIDATE = Path(sys.argv.pop(1)) if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else None


def synthetic_zip(names, *, mode=0o100644):
    buffer = BytesIO()
    with warnings.catch_warnings(), ZipFile(buffer, 'w') as archive:
        warnings.simplefilter('ignore', UserWarning)
        for name in names:
            info = ZipInfo(name, EPOCH)
            info.create_system = 3
            info.external_attr = mode << 16
            archive.writestr(info, b'x', compress_type=ZIP_DEFLATED)
    buffer.seek(0)
    return buffer


class ArchiveRefusals(unittest.TestCase):
    pins = dict.fromkeys(NAMES, fingerprint(b'x'))

    def test_names_and_order(self):
        for names in (NAMES[1:], (NAMES[0], NAMES[0], *NAMES[1:]), (*NAMES[:2], '../' + NAMES[2]),
                      (*NAMES, 'extra'), NAMES[::-1], (*NAMES[:2], 'C:ledger.json')):
            with self.subTest(names=names), self.assertRaisesRegex(ValueError, '^ARCHIVE_MEMBER_SELECTION$'):
                read_archive(synthetic_zip(names), self.pins)

    def test_symlink(self):
        with self.assertRaisesRegex(ValueError, '^ARCHIVE_MEMBER_TYPE$'):
            read_archive(synthetic_zip(NAMES, mode=0o120777), self.pins)

    def test_equal_length_member_swap(self):
        pins = self.pins | {NAMES[1]: fingerprint(b'y')}
        with self.assertRaisesRegex(ValueError, '^ARCHIVE_MEMBER_IDENTITY$'):
            read_archive(synthetic_zip(NAMES), pins)

    def test_false_ledger(self):
        with self.assertRaisesRegex(ValueError, '^CANONICAL_IDENTITY$'):
            read_archive(synthetic_zip(NAMES), self.pins)


@unittest.skipIf(CANDIDATE is None, 'supply the exact Workshop ZIP to exercise the source rows')
class SourceRefusals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        members = json.loads(ASSETS.read_bytes())['workshop']['members']
        with CANDIDATE.open('rb') as stream:
            cls.projected, cls.ledger = read_archive(stream, members)

    def test_original_group_member_omission(self):
        base = deepcopy(self.projected['baseline'])
        root = next(row for row in base['constructed_instances'] if row['root_kind'] == 'PACKIN_ROOT')
        root['member_identities'].pop()
        with self.assertRaisesRegex(ValueError, '^BASELINE_REPLAY_constructed_instances$'):
            replay_baseline(base)

    def test_omitted_9c_record_keyword_mutation(self):
        base = deepcopy(self.projected['baseline'])
        role = next(row for row in base['member_roles'] if row['reason'] == 'EXTRA_FLAGS_OMITTED_DEFAULT_UNKNOWN')
        row = next(row for row in base['instances'] if row['saved_reference'] == role['reference_identity'])
        edge = next(edge for edge in row['linked_prefix']['entries'] if edge['keyword_identity'] == 'starfield.esm:054ba6')
        edge['keyword_identity'] = 'starfield.esm:000192'
        with self.assertRaisesRegex(ValueError, '^RELATION_INPUT_PRESENT$'):
            supplement(base, self.projected['typed'], quest_operand(self.projected['alla']))

    def test_quest_alias_counterexample(self):
        alla = deepcopy(self.projected['alla'])
        alla['pairs'][0]['keyword'] = 'starfield.esm:000191'
        with self.assertRaisesRegex(ValueError, '^ALIAS_KEY_REQUIRES_RESEARCH$'):
            supplement(self.projected['baseline'], self.projected['typed'], quest_operand(alla))

    def test_hab_wall_omission(self):
        base = deepcopy(self.projected['baseline'])
        base['unresolved_population'] = [row for row in base['unresolved_population']
                                        if row['saved_reference'] != 'DYNAMIC:ff01b597']
        roots = supplement(base, self.projected['typed'], quest_operand(self.projected['alla']))['combined_roots']
        with self.assertRaisesRegex(ValueError, '^HAB_DA_MEMBERS$'):
            check_canonical(base, self.projected['typed'], self.ledger, {row['instance_identity'] for row in roots})

    def test_canonical_da_omission(self):
        typed = deepcopy(self.projected['typed'])
        typed['canonical_da'].pop()
        base = self.projected['baseline']
        roots = supplement(base, typed, quest_operand(self.projected['alla']))['combined_roots']
        with self.assertRaisesRegex(ValueError, '^CANONICAL_DA_COUNT_JOIN$'):
            check_canonical(base, typed, self.ledger, {row['instance_identity'] for row in roots})

    def test_raw_keyword_mutation(self):
        pairs = deepcopy(self.projected['alla']['pairs'])
        pairs[0]['keyword_raw'] = 0x2000192
        with self.assertRaisesRegex(ValueError, '^ALLA_FORBIDDEN_KEY$'):
            check_alla_keywords(pairs)

    def test_promoted_unsupported_extra(self):
        base = deepcopy(self.projected['baseline'])
        row = next(row for row in base['unresolved_population'] if row['saved_reference'] == 'DYNAMIC:ff03fb72')
        row['linked_prefix']['following_extras'] = 'CLOSED'
        roots = supplement(base, self.projected['typed'], quest_operand(self.projected['alla']))['combined_roots']
        with self.assertRaisesRegex(ValueError, '^BASELINE_UNSUPPORTED_EXTRAS$'):
            check_canonical(base, self.projected['typed'], self.ledger, {row['instance_identity'] for row in roots})

    def test_stale_schema_with_recomputed_hashes(self):
        with ZipFile(CANDIDATE) as archive:
            ledger = archive.read(NAMES[2])
        buffer = BytesIO()
        write_archive(buffer, encoded(self.projected | {'schema': 'sor-d5bx-workshop/0'}), ledger)
        with ZipFile(buffer) as archive:
            pins = {name: fingerprint(archive.read(name)) for name in NAMES}
        with self.assertRaisesRegex(ValueError, '^PROJECTION_SCHEMA$'):
            read_archive(buffer, pins)


if __name__ == '__main__':
    unittest.main()
