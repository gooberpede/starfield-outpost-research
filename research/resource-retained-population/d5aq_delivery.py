# SPDX-License-Identifier: GPL-3.0-or-later
"""Preserve source identities and export D5AQ review patches without Git writes.

SOR-P-0002 adaptation of the owned N2 exporter. Reads Git and authored files;
writes fresh ignored receipts, diffs and disposable application trees. No game,
database, save, network, staging, commit or ref operation. Both disk floors and
the inherited exact-byte forward/reverse and inventory checks remain active.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from pathlib import Path
import json
import d5ao_n2_delivery as original


def main():
    original.LOCAL = original.ROOT / '.local-work/d5aq'
    original.BRIEF = 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AQ_ordinary_construction_mask_invariance.md'
    original.allowed = lambda n: n in {
        'CREDITS.md', 'docs/SOURCES.md', 'docs/RESEARCH_STATE.md',
        'docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md'
    } or n.startswith(('docs/experiments/resource-retained-population/d5aq-',
                      'research/resource-retained-population/d5aq_'))
    if sys.argv[1:] == ['baseline']:
        original.baseline()
        return
    if len(sys.argv) != 3 or sys.argv[1] != 'export':
        raise SystemExit('Usage: d5aq_delivery.py baseline | export FRESH_LABEL')
    original.export(sys.argv[2])
    receipt = original.LOCAL / sys.argv[2] / 'delivery.json'
    result = json.loads(receipt.read_bytes())
    for coverage, info in result['patches'].items():
        target = original.ROOT / '.local-work/diffs' / ('d5aq-' + sys.argv[2] + '-' + coverage + '.diff')
        with target.open('xb') as stream:
            stream.write(Path(info['path']).read_bytes())
        if original.sha(target) != info['sha256']:
            raise ValueError('Named export differs')
        info['path'] = str(target)
    result['adapter_sha256'] = original.sha(__file__)
    result['inherited_exporter_sha256'] = original.sha(original.__file__)
    original.write(receipt.with_name('d5aq-delivery.json'), result)


if __name__ == '__main__':
    main()
