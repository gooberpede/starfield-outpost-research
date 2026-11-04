# SPDX-License-Identifier: GPL-3.0-or-later
"""Queryable offline causal windows, adapted from the owned D5AM reader.

SOR-P-0002 covers source-informed reuse of d5am_read_causal.registration_windows.
Original readers and raw evidence are unchanged. This module accepts decoded
rows; callers must authenticate them with the unchanged authoritative reader.
It writes nothing, imports no external dependency and never touches the target.
The export retains every call and lifecycle boundary needed to reproduce every
legacy conditional witness lazily. It does not infer atomic order from QPC.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict

SCHEMA = 'sor-d5ap-causal-index/1'
ALGORITHM = 'owner-context-index-and-lifecycle-bisection/1'
FATAL = {'MISSING_OR_DUPLICATE_REGISTRATION', 'UNKNOWN_INITIAL_HOLDERS'}
LIMIT = ('No winner/miss or upstream eligibility claim without qualified core/task/source joins; '
         'added probes can alter this order.')


class HistoryIndex:
    """Index one owner generation in O(E log E) time and O(E + W) memory.

    Pair queries take O(log L + K), with L lifecycle boundaries and K returned
    boundary witnesses. Iterating all W squared requested pairs is intentionally
    lazy and needs constant additional space. Reader/recursive records remain
    available through exact sequence, thread and context indexes; they are not
    silently promoted to nonowner writer calls.
    """

    def __init__(self, rows, issues=(), qualified=False):
        self.rows = tuple(rows)
        self.issues = tuple(sorted(set(issues)))
        self.qualified = qualified
        self.by_sequence = {}
        self.by_thread = defaultdict(list)
        self.by_context = defaultdict(list)
        self.calls = []
        self.owner = None
        for row in self.rows:
            key = (row['lock'], row['generation'])
            if self.owner is None:
                self.owner = key
            elif self.owner != key:
                raise ValueError('A HistoryIndex must contain one owner generation')
            seq = row['sequence']
            if seq in self.by_sequence:
                raise ValueError('Duplicate causal sequence')
            self.by_sequence[seq] = row
            self.by_thread[row['thread']].append(row)
            context = tuple(row[k] for k in ('thread', 'invocation', 'selection', 'source'))
            self.by_context[context].append(row)
        for key, parts in self.by_context.items():
            approach = pending = None
            for row in parts:
                if row['kind'] == 9:
                    approach, pending = row, None
                elif row['kind'] == 2:
                    pending = row
                elif row['kind'] == 3 and pending is not None:
                    used = tuple(r for r in (approach, pending, row) if r is not None)
                    self.calls.append(dict(key=key, approach=approach, pending=pending,
                                           acquired=row, first=min(r['ticks'] for r in used),
                                           last=max(r['ticks'] for r in used),
                                           uncertain=any(r['status'] or r['hazards'] for r in used)))
                    approach = pending = None
        self.call_by_acquisition = {c['acquired']['sequence']: c for c in self.calls}
        self.invalidators = sorted((r['ticks'], r['sequence']) for r in self.rows if r['kind'] in (12, 13, 14))
        self.invalidator_ticks = [p[0] for p in self.invalidators]
        self.tick_index = sorted((r['ticks'], r['sequence']) for r in self.rows)
        self.ticks = [p[0] for p in self.tick_index]
        self.thread_positions = {}
        for thread, parts in self.by_thread.items():
            for pos, row in enumerate(parts):
                self.thread_positions[row['sequence']] = (thread, pos)

    def interval(self, first, last):
        """Return all callback witnesses in an inclusive QPC interval, not HB."""
        if first > last:
            raise ValueError('Reversed interval')
        a, b = bisect_left(self.ticks, first), bisect_right(self.ticks, last)
        return [self.by_sequence[s] for _, s in self.tick_index[a:b]]

    def lifecycle(self, first, last):
        a = bisect_left(self.invalidator_ticks, first)
        b = bisect_right(self.invalidator_ticks, last)
        return [seq for _, seq in self.invalidators[a:b]]

    def legacy_pair(self, earlier_sequence, later_sequence):
        """Reproduce one original conditional witness exactly, or return None.

        The acquisition stamp order only selects the original query orientation.
        The returned interpretation supplies conditional native interval bounds;
        this function never asserts that stamp order itself is atomic order.
        """
        earlier = self.call_by_acquisition[earlier_sequence]
        later = self.call_by_acquisition[later_sequence]
        b, a = earlier['acquired'], later['acquired']
        if FATAL.intersection(self.issues) or a['thread'] == b['thread'] or not b['ticks'] < a['ticks']:
            return None
        rule = 'OVERLAPPING_INTERVALS_UNKNOWN'
        boundaries = []
        if (earlier['uncertain'] or later['uncertain'] or
                self.lifecycle(min(earlier['first'], later['first']), max(earlier['last'], later['last']))):
            rule = 'RELEVANT_LIFECYCLE_OR_CONTEXT_UNCERTAINTY'
        elif later['approach'] is not None and b['ticks'] < later['approach']['ticks']:
            rule = 'EARLIER_ACQUISITION_BEFORE_OTHER_HELPER_ENTRY'
            boundaries = [b['sequence'], later['approach']['sequence']]
        elif earlier['approach'] is not None and later['pending']['ticks'] < earlier['approach']['ticks']:
            rule = 'PRIOR_PENDING_WRITER_OVERTAKEN'
            boundaries = [later['pending']['sequence'], earlier['approach']['sequence'], b['sequence']]
        return dict(earlier_acquisition=b['sequence'], later_acquisition=a['sequence'],
                    interpretation=rule, disjoint_callback_boundaries=boundaries,
                    basis='CONDITIONAL_NATIVE_INTERVALS', limit=LIMIT)

    def iter_legacy(self):
        """Expand all original witnesses in original order without storing pairs."""
        for earlier in self.calls:
            for later in self.calls:
                value = self.legacy_pair(earlier['acquired']['sequence'], later['acquired']['sequence'])
                if value is not None:
                    yield value

    def pair(self, left_sequence, right_sequence):
        """Qualify a writer pair, retaining equal-stamp and coverage uncertainty.

        DEFINITELY_PRECEDES describes only the named native operation endpoints,
        never the entire calls or arbitrary cross-thread atomic transition order.
        Same-thread program order is independently available via event_pair.
        """
        left = self.call_by_acquisition[left_sequence]
        right = self.call_by_acquisition[right_sequence]
        first, last = min(left['first'], right['first']), max(left['last'], right['last'])
        invalidators = self.lifecycle(first, last)
        result = dict(left=left_sequence, right=right_sequence, lifecycle_witnesses=invalidators,
                      coverage_issues=list(self.issues), witnesses=[], native_edges=[])
        if not self.qualified or self.issues or invalidators or left['uncertain'] or right['uncertain']:
            result['relationship'] = 'OUTSIDE_QUALIFIED_COVERAGE'
            return result
        if left_sequence == right_sequence:
            result['relationship'] = 'NOT_COMPARABLE'
            return result
        if left['acquired']['thread'] == right['acquired']['thread']:
            order = self.event_pair(left_sequence, right_sequence)
            result.update(relationship=order['relationship'], witnesses=order['witnesses'],
                          native_edges=order.get('native_edges', []))
            return result
        witness = self.legacy_pair(left_sequence, right_sequence) or self.legacy_pair(right_sequence, left_sequence)
        result['witnesses'] = [] if witness is None else [witness]
        result['relationship'] = 'OVERLAPS_OR_INDETERMINATE'
        if witness is not None:
            early = self.call_by_acquisition[witness['earlier_acquisition']]
            late = self.call_by_acquisition[witness['later_acquisition']]
            if witness['interpretation'] == 'EARLIER_ACQUISITION_BEFORE_OTHER_HELPER_ENTRY':
                result['relationship'] = 'DEFINITELY_PRECEDES'
                result['native_edges'] = [dict(before=early['acquired']['sequence'],
                    after=late['approach']['sequence'], semantics='OWNERSHIP_ACQUIRED_BEFORE_OTHER_HELPER_ENTRY')]
            elif witness['interpretation'] == 'PRIOR_PENDING_WRITER_OVERTAKEN':
                result['relationship'] = 'DEFINITELY_PRECEDES'
                result['native_edges'] = [dict(before=late['pending']['sequence'],
                    after=early['approach']['sequence'], semantics='OTHER_PENDING_REGISTRATION_BEFORE_EARLIER_ACQUIRER_ENTRY')]
        return result

    def event_pair(self, left_sequence, right_sequence):
        """Program order is positive evidence; cross-thread QPC alone is not."""
        left, right = self.by_sequence[left_sequence], self.by_sequence[right_sequence]
        lo, hi = sorted((left['ticks'], right['ticks']))
        out = dict(left=left_sequence, right=right_sequence, witnesses=[left_sequence, right_sequence])
        if (not self.qualified or self.issues or left['status'] or left['hazards'] or
                right['status'] or right['hazards'] or self.lifecycle(lo, hi)):
            out['relationship'] = 'OUTSIDE_QUALIFIED_COVERAGE'
        elif left_sequence == right_sequence or left['thread'] != right['thread']:
            out['relationship'] = 'NOT_COMPARABLE'
        else:
            _, a = self.thread_positions[left_sequence]
            _, b = self.thread_positions[right_sequence]
            out['relationship'] = 'DEFINITELY_PRECEDES' if a < b else 'DEFINITELY_FOLLOWS'
            out['native_edges'] = [dict(before=left_sequence if a < b else right_sequence,
                after=right_sequence if a < b else left_sequence, semantics='SAME_THREAD_PROGRAM_ORDER')]
        return out

    def export(self):
        """Serialize a complete compact index; no empty array denotes omission."""
        return dict(schema=SCHEMA, algorithm=ALGORITHM, owner=self.owner,
                    qualified=self.qualified, issues=list(self.issues), event_count=len(self.rows),
                    kind_counts=dict(Counter(r['kind'] for r in self.rows)),
                    event_sequences=[r['sequence'] for r in self.rows],
                    calls=[dict(context=list(c['key']),
                        approach=c['approach'], pending=c['pending'], acquired=c['acquired']) for c in self.calls],
                    lifecycle=[self.by_sequence[s] for _, s in self.invalidators],
                    disposition='COMPLETE_QUERYABLE_CONDITIONAL_WINDOWS',
                    semantics='Use HistoryIndex.legacy_pair/iter_legacy or pair; QPC orientation is not atomic order.',
                    source='runtime/construction-winner/d5am_read_causal.py:registration_windows; SOR-P-0002')


def registration_windows(rows, issues):
    """Reader enrichment adapter; original validation/history checks still run."""
    return HistoryIndex(rows, issues).export()
