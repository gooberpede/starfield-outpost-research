# SPDX-License-Identifier: GPL-3.0-or-later
"""Reconcile the bounded C19 callback derivative with Python 3.10+ stdlib.

Reads only an explicitly supplied candidate. Synthetic and mutation controls
run in memory. No game files, WAL, local repository paths, network or writes.
"""

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path


SCHEMA = 'sor-d5be-c19-callbacks/1'
RECORDS = 611926
EXE = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ESM = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
WATER_SELECTOR = '000083ec'
DEFINITIONS = {
    '000057c1': ('Lead', 'ResInorgCommonLead'),
    '000057c7': ('Iron', 'ResInorgCommonIron'),
    '000057c9': ('Alkanes', 'ResInorgUncommonAlkanes_G'),
    '000057f5': ('Helium-3', 'ResInorgCommonHelium3_G'),
}
LABELS = (None, None, None, ('Iron', 'Helium-3'), ('Iron', 'Alkanes', 'Helium-3'), ('Iron', 'Helium-3'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value, low, high):
    return type(value) is int and low <= value <= high


def fold(spatial, atmosphere, appends):
    # Dict insertion order retains the first occurrence of each native pointer token.
    common = {}
    for token, form in spatial + atmosphere:
        if token:
            common.setdefault(token, form)
    return list(common.items()) + appends


def selected_from_biome(biome, selector):
    return [item for item in biome if item[0] and item[1] == selector[1]] if selector[0] else []


def synthetic_control():
    # One alias recurs across sources, two aliases share a FormID, and the
    # selected append is allowed to repeat a common operand and itself.
    first = [(1, 'iron'), (0, None), (2, 'iron')]
    second = [(1, 'iron'), (3, 'helium')]
    biome = [(2, 'iron'), (4, 'lead'), (2, 'iron')]
    actual_appends = [(2, 'iron'), (2, 'iron')]
    require(selected_from_biome(biome, (5, 'iron')) == actual_appends, 'synthetic selected append')
    require(fold(first, second, actual_appends) == [(1, 'iron'), (2, 'iron'), (3, 'helium'), *actual_appends],
            'synthetic pointer/order/deduplication fold')


class Verifier:
    def __init__(self):
        self.sequences = set()
        self.calls = set()
        self.form_by_token = {}

    def record(self, sequence, low=1, high=RECORDS):
        require(number(sequence, low, high) and sequence not in self.sequences,
                'record sequence reuse or ordering error')
        self.sequences.add(sequence)

    def call(self, invocation):
        require(number(invocation, 1, RECORDS) and invocation not in self.calls,
                'duplicate or malformed invocation')
        self.calls.add(invocation)

    def identity(self, token, form, *, selector=False):
        require(number(token, 0, RECORDS), 'malformed pointer alias')
        if token == 0:
            require(form is None, 'null pointer alias has a FormID')
        else:
            require((form == WATER_SELECTOR if selector else form in DEFINITIONS)
                    and self.form_by_token.setdefault(token, form) == form,
                    'unknown FormID or inconsistent pointer identity')
        return token, form

    def population(self, source, low, high):
        self.record(source['header'], low, high)
        last = source['header']
        inputs = []
        for sequence, token, form in source['members']:
            self.record(sequence, last + 1, high)
            last = sequence
            inputs.append(self.identity(token, form))
        return inputs

    def callback(self, event):
        self.call(event['invocation'])
        entry, end = event['entry'], event['exit']
        self.record(entry)
        self.record(end, entry + 1)
        biome = self.population(event['biome'], 1, entry - 1)
        selector = self.identity(*event['selector'], selector=True)
        require(selector[0] > 0, 'missing recorded Water selector')
        last = entry
        common = []
        for name in ('spatial', 'atmosphere'):
            source = event[name]
            self.call(source['call'])
            self.record(source['entry'], last + 1, end - 1)
            self.record(source['exit'], source['entry'] + 1, end - 1)
            common.append(self.population(source, last + 1, source['entry'] - 1))
            last = source['exit']
        appends = []
        for invocation, before, after, token, form in event['append']:
            self.call(invocation)
            self.record(before, last + 1, end - 1)
            self.record(after, before + 1, end - 1)
            last = after
            appends.append(self.identity(token, form))
        require(appends == selected_from_biome(biome, selector), 'selected append differs from selector/biome evidence')
        require(len(event['rows']) in (2, 3), 'unexpected final row count')
        observed = []
        census = []
        for expected, (ordinal, invocation, before, after, census_seq, token, form) in enumerate(event['rows']):
            require(number(ordinal, expected, expected), 'wrong final row ordinal/order')
            self.call(invocation)
            self.record(before, last + 1, end - 1)
            self.record(after, before + 1, end - 1)
            last = after
            census.append(census_seq)
            observed.append(self.identity(token, form))
        for sequence in census:
            self.record(sequence, last + 1, end - 1)
            last = sequence
        predicted = fold(*common, appends)
        forms = tuple(form for _, form in observed)
        require(forms == tuple(form for _, form in predicted), f'callback {event["invocation"]} native row mismatch')
        signature = [[form for _, form in source] for source in (*common, biome)]
        return forms, predicted == observed, signature


def verify(package):
    require((package['schema'], package['capture'], package['exe_sha256'], package['definition_esm_sha256'])
            == (SCHEMA, 'SOR-EV-0043', EXE, ESM), 'wrong capture or data domain')
    require((package['records'], package['initialization_evaluations'], package['preview_evaluations'])
            == (RECORDS, 1, 35573), 'wrong source census')
    require(package['definitions'] == {
        form: dict(label=label, editor_id=editor, definition=f'Starfield.esm:{form[-6:]}')
        for form, (label, editor) in DEFINITIONS.items()
    }, 'resource definition mapping')
    callbacks, runs = package['callbacks'], package['runs']
    require(len(callbacks) == 346, 'expected all 346 callbacks')
    require(len(runs) == 6, 'expected six preview runs')
    verifier = Verifier()
    last_entry = 0
    previous_rows, change, counts, run_counts = {}, Counter(), Counter(), Counter()
    pointer_matches = append_count = 0
    for event in callbacks:
        require(number(event['entry'], last_entry + 1, RECORDS), 'callback chronology or duplication')
        last_entry = event['entry']
        forms, pointers_match, signature = verifier.callback(event)
        pointer_matches += pointers_match
        append_count += len(event['append'])
        require(number(event['run'], 1, len(runs)) and number(event['model'], 1, len(callbacks)), 'run/model identifier')
        run = runs[event['run'] - 1]
        require(run['first_invocation'] < event['invocation'] < run['last_invocation']
                and run['populations'] == signature, 'callback does not agree with reported run context')
        labels = tuple(DEFINITIONS[form][0] for form in forms)
        if run['operator_labels'] is not None:
            require(labels == tuple(run['operator_labels']), 'operator label/run disagreement')
        model, values = event['model'], frozenset(forms)
        previous = previous_rows.get(model)
        change['initial' if previous is None else 'unchanged' if previous == values else 'changed'] += 1
        previous_rows[model] = values
        run_counts[event['run']] += 1
        counts[len(forms)] += 1
    for i, (run, labels) in enumerate(zip(runs, LABELS, strict=True), 1):
        require(run['run'] == i and run['phase'] == (None if labels is None else 'ABC'[i - 4])
                and (None if run['operator_labels'] is None else tuple(run['operator_labels'])) == labels,
                'preview phase labels or order')
    require([r['evaluations'] for r in runs] == [10602, 86, 253, 18397, 3964, 2271]
            and list(run_counts.items()) == [(1, 315), (2, 2), (3, 14), (4, 3), (5, 10), (6, 2)],
            'preview run or callback run census')
    require(counts == {2: 7, 3: 339} and change == {'initial': 1, 'changed': 5, 'unchanged': 340}
            and append_count == 0, 'native output distribution, redelivery or append census')
    return dict(comparisons=346, rows=dict(counts), set_change=dict(change),
                append_count=append_count, pointer_alias_matches=pointer_matches, preview_run_callbacks=dict(run_counts))


def negative_controls(package):
    def change_row(copy):
        rows = copy['callbacks'][0]['rows']
        rows[0][-2:] = rows[-1][-2:]

    def wrong_order(copy):
        copy['callbacks'][0]['spatial']['members'].reverse()
        # The first update has two spatial members in this exact capture.

    def swapped_operands(copy):
        first, second = copy['callbacks'][0]['spatial']['members']
        first[1:], second[1:] = second[1:], first[1:]

    controls = {
        'changed-row': change_row,
        'wrong-order': wrong_order,
        'swapped-operands': swapped_operands,
        'missing-callback': lambda copy: copy['callbacks'].pop(),
        'duplicate-callback': lambda copy: copy['callbacks'].__setitem__(1, copy['callbacks'][0]),
        'wrong-domain': lambda copy: copy.__setitem__('schema', 'synthetic/1'),
    }
    rejected = {}
    for name, mutate in controls.items():
        copy = deepcopy(package)
        mutate(copy)
        try:
            verify(copy)
        except ValueError as error:
            rejected[name] = str(error)
        else:
            raise ValueError(f'negative control accepted: {name}')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', nargs='?', type=Path)
    parser.add_argument('--sha256', help='exact candidate hash from the evidence manifest')
    parser.add_argument('--negative-controls', action='store_true')
    parser.add_argument('--self-test', action='store_true', help='synthetic fold check without evidence')
    args = parser.parse_args()
    try:
        if args.self_test and args.candidate is None and args.sha256 is None and not args.negative_controls:
            synthetic_control()
            print('PASS synthetic fold only')
            return
        require(not args.self_test and args.candidate is not None and args.sha256 is not None,
                'provide a candidate and its manifest SHA-256, or --self-test alone')
        raw = args.candidate.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == args.sha256, 'candidate SHA-256 mismatch')
        package = json.loads(raw)
        canonical = (json.dumps(package, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')
        require(raw == canonical, 'candidate JSON byte encoding')
        results = verify(package)
        if args.negative_controls:
            results['rejected'] = negative_controls(package)
        print(json.dumps(results, sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        parser.exit(1, f'C19 verify: {error}\n')


if __name__ == '__main__':
    main()
