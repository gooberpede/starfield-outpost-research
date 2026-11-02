# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only source/caller audit; writes one fresh ignored JSON receipt.

Reads authored ending CSV and retained native/audit/export receipts. No target,
analysis database, save, installed-file or network changes. Stop on any source,
receiver, metadata disposition or count mismatch; preserve prior receipts.
"""
import sys
from pathlib import Path
import csv
import hashlib
import json

root = Path(__file__).resolve().parents[2]
out = (root / sys.argv[1]).resolve()
if not out.is_relative_to(root / '.local-work/d5ai-ownership') or out.exists():
    raise ValueError('Fresh ignored output required')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sources = root / 'docs/experiments/resource-retained-population/d5ai-population-ending-sources.csv'
with sources.open(encoding='utf8', newline='') as f:
    rows = list(csv.DictReader(f))
for row in rows:
    p = root / row['path']
    assert sha(p) == row['sha256']
    lines = p.read_text().splitlines()
    lo, hi = int(row['first_line']), int(row['last_line'])
    assert lines[lo-1].startswith('FUNCTION\t'+row['static_va'][2:]+'\t')
    assert hi <= len(lines)
audit_path = root / '.local-work/d5ai-ownership/audit03.json'
audit = json.loads(audit_path.read_bytes())
refs = next(v for v in audit.values() if isinstance(v, list) and any(
    isinstance(x, dict) and 'target' in x for x in v))
native = root / '.local-work/d5ai-ownership/ending01/native.tsv'
export = json.loads((native.parent / 'result.json').read_bytes())
assert export['copy_core_preserved'] and export['native_sha256'] == sha(native)
text = native.read_text()
checks = []
for target, count, adjustment in [('0x1407aab10', 10, 0x10), ('0x1407ac260', 11, 8)]:
    these = [x for x in refs if x.get('target') == target]
    calls = [x for x in these if x['disposition'] == 'code-reference']
    assert len(calls) == count
    assert all(x['disposition'] == 'exception-directory' for x in these if x not in calls)
    for call in calls:
        line = call['source'][2:]+'\tCALL '+target
        assert line in text
        before = text[:text.index(line)].splitlines()[-7:]
        assert any('LEA RCX,[' in l and ('+ 0x%x]' % adjustment) in l for l in before)
        checks.append(dict(site=call['source'], target=target,
                           receiver_adjustment=adjustment, prior_instructions=before))
result = dict(scope=__doc__, source_windows=len(rows), checks=checks,
              method_sha256=sha(Path(__file__)), source_csv_sha256=sha(sources),
              native_sha256=sha(native), inherited_audit_sha256=sha(audit_path),
              limitation='Existing typed direct caller graph, not a global heap or arbitrary computed-call census')
out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8', newline='\n')
print('PASS', len(rows), 'windows', len(checks), 'typed calls', out)
