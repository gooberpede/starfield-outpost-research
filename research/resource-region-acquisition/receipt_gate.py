# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline classification-envelope prototype, sor-rg2c1a-envelope/1.

Stdlib only. CLI reads one JSON {before, after}; prints a derived classification
to stdout. --self-test uses synthetic in-memory fixtures, no filesystem writes.
No game/process/network/save/config/analysis-project effects. Does not validate
raw media, authenticate identity, compare native geometry or authorize a run.
See docs/experiments/resource-region-acquisition/receipts.md for the raw contract.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import unittest

SCHEMA = 'sor-rg2c1a-envelope/1'
CASES = {'C1-IL': '0057d4', 'C1-CU': '0057cf', 'C1-FE': '0057c7'}
ENUMS = {'list': {'PRESENT', 'NOT_LISTED', 'UNREADABLE'},
         'ground': {'PRESENT', 'NOT_DETECTED', 'UNREADABLE', 'NOT_TESTED'},
         'preview': {'ACCEPTABLE', 'BLOCKED', 'UNREADABLE', 'NOT_TESTED'}}


def qualified(row):
    """Refuse incomplete envelopes. True means admissible categorical accounting."""
    try:
        return (row['schema'] == SCHEMA
                and CASES.get(row['case']) == row['ires']
                and row['case'] in CASES
                and row['identity'] == 'EXACT_SAVED_JOIN_AND_VISUAL'
                and row['complete'] is True and row['loss'] == 0
                and type(row['loss']) is int
                and row['control_positive'] is True
                and row['labels_readable'] is True
                and row['roi_complete'] is True
                and row['native_epoch'] is None
                and all(re.fullmatch('[0-9a-f]{64}', row[k])
                        for k in ('root_save_sha256', 'config_sha256', 'video_sha256'))
                and all(row[k] in choices for k, choices in ENUMS.items()))
    except (KeyError, TypeError):
        return False


def sample(row):
    if not qualified(row):
        return 'UNKNOWN'
    if row['ground'] in {'UNREADABLE', 'NOT_TESTED'}:
        return 'INSUFFICIENT_GROUND_EVIDENCE'
    if row['ground'] == 'NOT_DETECTED':
        return 'NO_OVERLAY_DETECTED_IN_RECORDED_ROI'
    if row['preview'] == 'BLOCKED':
        return 'VISIBLE_RESOURCE_PREVIEW_BLOCKED'
    if row['preview'] == 'ACCEPTABLE':
        return 'VISIBLE_RESOURCE_PREVIEW_ACCEPTABLE'
    return 'VISIBLE_RESOURCE_PREVIEW_UNKNOWN'


def compare(before, after):
    """Only a registered controlled pair earns a stability/change classification."""
    if not all(qualified(r) for r in (before, after)):
        return 'INSUFFICIENT_EVIDENCE'
    for key in ('case', 'ires', 'root_save_sha256', 'config_sha256', 'station_id'):
        if not before.get(key) or before.get(key) != after.get(key):
            return 'INSUFFICIENT_EVIDENCE'
    if (before.get('phase') != 'PRE' or after.get('phase') != 'POST_RELOAD'
            or before.get('sample_id') == after.get('sample_id')
            or not before.get('sample_id') or not after.get('sample_id')
            or after.get('stationary_control_stable') is not True
            or after.get('transition_complete') is not True
            or not all(r.get('registered') is True for r in (before, after))
            or any(r[k] in {'UNREADABLE', 'NOT_TESTED'}
                   for r in (before, after) for k in ENUMS)):
        return 'INSUFFICIENT_EVIDENCE'
    same = all(before[k] == after[k] for k in ENUMS)
    return 'STABLE_SAMPLED_UI_PAIR' if same else 'OBSERVED_UI_CHANGE_ACROSS_RELOAD'


def fixture():
    """Synthetic placeholders; repeated hex words do not identify real evidence."""
    return dict(schema=SCHEMA, case='C1-IL', ires='0057d4',
                identity='EXACT_SAVED_JOIN_AND_VISUAL', complete=True, loss=0,
                control_positive=True, labels_readable=True, roi_complete=True,
                native_epoch=None, root_save_sha256='1'*64, config_sha256='2'*64,
                video_sha256='3'*64, list='PRESENT', ground='PRESENT',
                preview='BLOCKED', phase='PRE', sample_id='synthetic-pre',
                station_id='synthetic-station', registered=True)


class AccountingTests(unittest.TestCase):
    def test_blocked_is_not_absence(self):
        self.assertEqual(sample(fixture()), 'VISIBLE_RESOURCE_PREVIEW_BLOCKED')

    def test_no_overlay_is_scoped(self):
        r = fixture(); r['ground'] = 'NOT_DETECTED'
        self.assertEqual(sample(r), 'NO_OVERLAY_DETECTED_IN_RECORDED_ROI')

    def test_missing_ground_is_unknown(self):
        r = fixture(); r['ground'] = 'NOT_TESTED'
        self.assertEqual(sample(r), 'INSUFFICIENT_GROUND_EVIDENCE')

    def test_loss_and_missing_context(self):
        for key, value in [('loss', 1), ('loss', None), ('complete', False),
                           ('identity', 'SITE_ONLY'), ('control_positive', False),
                           ('roi_complete', False), ('labels_readable', False),
                           ('video_sha256', ''), ('native_epoch', 42),
                           ('ires', '0057cf'), ('case', 'wrong')]:
            with self.subTest(key=key, value=value):
                r = fixture(); r[key] = value
                self.assertEqual(sample(r), 'UNKNOWN')
        r = fixture(); del r['case']
        self.assertEqual(sample(r), 'UNKNOWN')

    def pair(self):
        a = fixture(); b = copy.deepcopy(a)
        b.update(phase='POST_RELOAD', sample_id='synthetic-post',
                 stationary_control_stable=True, transition_complete=True)
        return a, b

    def test_stable_pair(self):
        self.assertEqual(compare(*self.pair()), 'STABLE_SAMPLED_UI_PAIR')

    def test_changed_pair(self):
        a, b = self.pair(); b['ground'] = 'NOT_DETECTED'
        self.assertEqual(compare(a, b), 'OBSERVED_UI_CHANGE_ACROSS_RELOAD')

    def test_unknown_pairs(self):
        for key, value in [('registered', False), ('transition_complete', False),
                           ('stationary_control_stable', False),
                           ('root_save_sha256', '4'*64), ('config_sha256', '4'*64),
                           ('station_id', 'elsewhere'), ('ground', 'NOT_TESTED'),
                           ('list', 'UNREADABLE'), ('sample_id', 'synthetic-pre')]:
            with self.subTest(key=key):
                a, b = self.pair(); b[key] = value
                self.assertEqual(compare(a, b), 'INSUFFICIENT_EVIDENCE')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=['receipt_gate'], exit=True)
    elif args.input:
        data = json.loads(args.input.read_text(encoding='utf8'))
        print(json.dumps(dict(before=sample(data['before']), after=sample(data['after']),
                              comparison=compare(data['before'], data['after']))))
    else:
        parser.error('Supply --input or --self-test')
