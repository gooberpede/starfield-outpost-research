# SPDX-License-Identifier: GPL-3.0-or-later
"""Owned owner-certificate model; no native execution or target interaction.

Reads only this method, writes a fresh ignored receipt. This tests the stated
invalidation rule and an adverse schedule permitted by static instruction
order; it does not establish that the schedule happens in retail execution.
"""
import sys
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = (root / sys.argv[1]).resolve()
if not out.is_relative_to(root / '.local-work/d5ai-ownership') or out.exists():
    raise ValueError('Fresh ignored output required')

def qualifies(events, protected=(0, 1, 5, 6), observed=(0, 1, 2, 3, 4, 5, 6)):
    active = set()
    anchor = None
    for event, value in events:
        if event == 'begin':
            if value not in observed:
                continue
            active.add(value)
            if value in protected:
                anchor = None
        elif event == 'end':
            if value not in observed:
                continue
            active.remove(value)
        elif event == 'generation':
            anchor = value if not active else None
        elif event == 'loss':
            anchor = None
    return anchor

rows = []
def check(name, events, expected, protected=(0, 1, 5, 6), observed=(0, 1, 2, 3, 4, 5, 6)):
    actual = qualifies(events, protected, observed)
    assert actual == expected, (name, actual, expected)
    rows.append(dict(case=name, events=events, owner_certificate=actual))

# Actual true-reset order: the nested ProcGen clear ends before manager+80 zero.
# An intervening generation is an adverse allowed schedule, not an observation.
gap = [('begin', 6), ('begin', 0), ('end', 0), ('generation', 'A'), ('end', 6)]
check('old-inner-clear-only-rule-admits-late-owner-zero-gap', gap, 'A', (0, 1), (0, 1, 2, 3, 4))
check('whole-true-reset-rejects-anchor-inside-gap', gap, None)
for reason in (0, 1, 5, 6):
    check('reason-%d-invalidates-prior-generation' % reason,
          [('generation', 'A'), ('begin', reason), ('end', reason)], None)
for reason in (2, 3, 4):
    check('reason-%d-retains-owner-only-certificate' % reason,
          [('generation', 'A'), ('begin', reason), ('end', reason)], 'A')
check('installer-owner-ABA-cannot-be-repaired-by-equal-body',
      [('generation', 'A'), ('begin', 5), ('end', 5), ('begin', 5), ('end', 5)], None)
check('fresh-empty-process-without-generation-is-inconclusive', [], None)
check('lost-history-invalidates', [('generation', 'A'), ('loss', None)], None)
check('generation-inside-source-retirement-is-not-an-anchor',
      [('begin', 4), ('generation', 'A'), ('end', 4)], None)
out.write_text(json.dumps(dict(scope=__doc__, method_sha256=hashlib.sha256(
    Path(__file__).read_bytes()).hexdigest(), rows=rows), indent=2) + '\n',
    encoding='utf8', newline='\n')
print('PASS', len(rows), out)
