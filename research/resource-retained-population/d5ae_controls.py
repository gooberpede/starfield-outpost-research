# SPDX-License-Identifier: GPL-3.0-or-later
"""Check bounded source-arbitration predicates against explicit contrary cases.

Reads owned D5AC raw-frame decoder and authenticated B2 capture, plus exact
local native listings. Writes a fresh ignored receipt below .local-work/d5ae.
Stdlib only; no native execution, game, save, database, network or Git writes.
The state machine is a source-informed model, not an engine scheduler. Native
queue, entry-state and reserve controls are separate processes and receipts.
SOR-P-0002 lineage: D5AC reconstruction and D5Z/D5V arbitration research.
Stop on input mismatch, failed oracle or caller-available C:/D: disk floor.
Outputs and failures remain local; there is no cleanup of original inputs.
"""
import json
from pathlib import Path
import sys

from d5ad_baseline import guard, sha
from d5ac_reconstruct import SESSION, decode_frames

ROOT = Path(__file__).resolve().parents[2]


class SourceModel:
    """Qualified successful holder/map allocation; exclusive phases are atomic."""

    def __init__(self):
        self.visited = set()
        self.holders = {}
        self.admitted = set()
        self.log = []

    def visit(self, request, owner=1, token=10, ready=True, aggregate=False):
        outcome = ('dependency-pending' if not ready else 'aggregate-reuse'
                   if aggregate else 'visited' if (owner, token) in self.visited
                   else 'unvisited')
        if outcome == 'unvisited':
            self.admitted.add(request)
        self.log.append((request, outcome))
        return outcome

    def exclusive(self, request, owner=1, pointer=100, token=10,
                  metadata=True, raster=True, append=True):
        if request not in self.admitted:
            raise ValueError('No qualified visit admission')
        self.admitted.remove(request)
        key = owner, pointer
        if key in self.holders:
            outcome = 'map-hit'
        else:
            # Insertion precedes generator prerequisites; no visited recheck.
            self.holders[key] = request
            outcome = 'construct' if metadata and raster else 'empty-attempt'
            if append:
                self.visited.add((owner, token))
        self.log.append((request, outcome))
        return outcome

    def clear_grid(self, owner=1, pointer=100):
        self.holders.pop((owner, pointer), None)

    def reset(self, owner=1):
        self.holders = {k: v for k, v in self.holders.items() if k[0] != owner}
        self.visited = {k for k in self.visited if k[0] != owner}


def controls():
    rows = []

    def save(name, model, expected):
        actual = [v for _, v in model.log]
        if actual != expected:
            raise AssertionError((name, actual, expected))
        rows.append(dict(case=name, actual=actual, expected=expected,
                         holders=sorted((list(k), v) for k, v in model.holders.items()),
                         visited=sorted(model.visited), basis='Synthetic predicate control'))

    for winner, loser in [('B', 'A'), ('A', 'B')]:
        m = SourceModel()
        m.visit('A'); m.visit('B')
        m.exclusive(winner); m.exclusive(loser)
        if m.holders[(1, 100)] != winner:
            raise AssertionError('Winner oracle')
        save('both-pass-map-order-' + winner, m,
             ['unvisited', 'unvisited', 'construct', 'map-hit'])
    m = SourceModel()
    m.visit('A', ready=False); m.visit('B'); m.exclusive('B')
    m.visit('A'); save('A-dependency-blocked', m,
                      ['dependency-pending', 'unvisited', 'construct', 'visited'])
    m = SourceModel()
    m.visit('A', ready=False); m.visit('B', ready=False)
    save('startup-definitions-not-admitted', m, ['dependency-pending'] * 2)
    for name, kw in [('metadata-missing', dict(metadata=False)),
                     ('raster-acquisition-refused', dict(raster=False))]:
        m = SourceModel(); m.visit('A'); m.visit('B')
        m.exclusive('A', **kw); m.exclusive('B')
        save(name, m, ['unvisited', 'unvisited', 'empty-attempt', 'map-hit'])
    m = SourceModel(); m.visit('A'); m.visit('B')
    m.exclusive('A'); m.exclusive('B')
    save('raster-load-delay-inside-exclusive-does-not-overtake', m,
         ['unvisited', 'unvisited', 'construct', 'map-hit'])
    m = SourceModel(); m.holders[(1, 100)] = 'prior'
    m.visit('A'); m.exclusive('A')
    save('populated-map-without-visited', m, ['unvisited', 'map-hit'])
    m = SourceModel(); m.visit('A'); m.exclusive('A', append=False)
    m.visit('B'); m.exclusive('B')
    save('reserve-fails-holder-reused', m, ['unvisited', 'construct', 'unvisited', 'map-hit'])
    m = SourceModel(); m.visit('A'); m.exclusive('A', metadata=False)
    m.visit('B'); save('returned-empty-generator-still-visits', m,
                      ['unvisited', 'empty-attempt', 'visited'])
    for broad in (False, True):
        m = SourceModel(); m.visit('A'); m.exclusive('A')
        if broad:
            m.reset()
        else:
            m.clear_grid()
        result = m.visit('B')
        if result == 'unvisited':
            m.exclusive('B')
        save('broad-reset' if broad else 'grid-clear-retains-token', m,
             ['unvisited', 'construct', 'unvisited', 'construct'] if broad
             else ['unvisited', 'construct', 'visited'])
    m = SourceModel(); m.visit('A'); m.exclusive('A')
    m.visit('B', owner=2); m.exclusive('B', owner=2)
    save('different-owner-independent-stores', m, ['unvisited', 'construct'] * 2)
    m = SourceModel(); m.visit('A'); m.exclusive('A'); m.clear_grid()
    m.visit('B'); save('new-pointer-same-token-is-not-fresh-eligibility', m,
                      ['unvisited', 'construct', 'visited'])
    m = SourceModel(); m.visit('A'); m.exclusive('A'); m.clear_grid()
    m.visit('B', token=11); m.exclusive('B', token=11)
    save('reallocated-address-distinct-token', m, ['unvisited', 'construct'] * 2)
    m = SourceModel(); m.visit('A', aggregate=True)
    save('aggregate-skips-provider', m, ['aggregate-reuse'])
    # A protected lookup cannot hit an unrelated pointer's insertion.
    m = SourceModel(); m.visit('A'); m.exclusive('A')
    m.visit('B', token=11); m.exclusive('B', pointer=101, token=11)
    save('different-source-pointer-key', m, ['unvisited', 'construct'] * 2)
    return rows


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B without optimization')
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ae'):
        raise ValueError('Fresh task-local output required')
    free = guard()
    native = ROOT / '.local-work/d5w/functions/14079f860.txt'
    if sha(native) != '672846097b588ed3b4d02a68deddb0f480aaa6853dbc357993933d85b4d1c06a':
        raise ValueError('Provider pin mismatch')
    text = native.read_text(encoding='utf8')
    sites = {'14079fc45': 'CALL 0x1422cc350', '14079fcb3': 'CALL 0x1422cc3d0',
             '14079fccb': 'CALL 0x1403499f0', '14079fdf9': 'CALL 0x1407aa5f0',
             '14079ff18': 'CALL 0x14079b520', '14079ff3e': 'CALL 0x1422cc0d0',
             '14079ff60': 'MOV qword ptr [RAX + RCX*0x8],RDI',
             '14079ffa5': 'CALL 0x1402c45a0'}
    for address, instruction in sites.items():
        if address + '\t' + instruction not in text:
            raise ValueError('Instruction mismatch: ' + address)
    raw = SESSION / 'events.bin'
    events = decode_frames(raw.read_bytes())
    chosen = [events[s - 1] for s in (8004, 8005, 8006, 8018, 8019, 8020,
                                      8091, 8092, 8093, 8094, 8104, 8105, 8106, 8339)]
    a, b, miss, sample, reserve, store, hit = [events[s - 1] for s in (8006, 8020, 8091, 8094, 8105, 8106, 8339)]
    if not (a['ticks'] < b['ticks'] < miss['ticks'] < sample['ticks']
            < reserve['ticks'] < store['ticks'] < hit['ticks']):
        raise AssertionError('B2 QPC ordering')
    if not (a['invocation'] == hit['invocation'] == 3837
            and b['invocation'] == miss['invocation'] == 3844
            and a['request'] == [4, -1] and b['request'] == [5, 0]
            and miss['a'] == miss['b'] == 64 and hit['a'] == 18):
        raise AssertionError('B2 rivalry operands')
    if len({(e['proc'], e['source'], e['epoch']) for e in (a,b,miss,hit)}) != 1:
        raise AssertionError('B2 alias mismatch')
    if not (a['a'] == b['a'] == 0 and a['b'] == b['b'] == store['b']
            and miss['c'] == hit['c'] == a['source']
            and miss['d'] == hit['d'] == 207 and sample['a'] == 3
            and reserve['a'] == 21 and store['a'] == reserve['d'] + 21 * 8):
        raise AssertionError('B2 map/sample/token operands')
    cases = controls()
    # Independent scheduler predicate oracles: count and rank are not aliases.
    node_cases = []
    for dependencies, committed, status, expected in (
            (2, True, 2, 'pending'), (1, True, 2, 'ready-tree'),
            (1, False, 2, 'uncommitted'), (1, True, 4, 'state-4'),
            (1, True, 5, 'complete')):
        remaining = dependencies - 1
        actual = ('pending' if remaining else 'uncommitted' if not committed
                  else 'ready-tree' if status == 2 else 'state-4'
                  if status == 4 else 'complete')
        if actual != expected:
            raise AssertionError('Dependency oracle')
        node_cases.append(dict(dependencies_before=dependencies, committed=committed,
                               returned_status=status, after=actual))
    node_cases.append(dict(case='rank-is-not-dependency-count',
                           rank=0, dependencies=2, result='Not ready merely because rank is zero'))
    out.mkdir(parents=True)
    result = dict(schema='sor-d5ae-controls/1', script_sha256=sha(__file__),
                  free=free, raw_sha256=sha(raw), provider_sha256=sha(native),
                  exact_sites=sites, b2=chosen, cases=cases, node_cases=node_cases,
                  scope='B2 authentication and synthetic source predicates; no full native scheduler execution')
    (out / 'controls.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(cases=len(cases), b2_boundaries=len(chosen), passed=True)))


if __name__ == '__main__':
    main()
