# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AP source patch export using the unchanged owned N2 exporter.

SOR-P-0002 adaptation: configure original d5ao_n2_delivery.export for D5AP
paths and its initial tracked-source baseline. Reads Git and authored text;
writes exclusive local diffs, manifests and disposable review trees. Never
stages, commits, changes refs, contacts a remote or writes protected evidence.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import d5ao_n2_delivery as original


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: d5ap_delivery.py FRESH_LABEL')
    original.guard()
    original.LOCAL = original.ROOT / '.local-work/d5ap'
    original.BRIEF = 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AP_GC10_competitor_causal_analysis.md'
    original.allowed = lambda n: n in {
        'CREDITS.md', 'docs/SOURCES.md', 'docs/RESEARCH_STATE.md',
        'docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md'
    } or n.startswith(('docs/experiments/resource-retained-population/d5ap-',
                      'research/resource-retained-population/d5ap_'))
    baseline = original.LOCAL / 'source-baseline02.json'
    if not baseline.exists():
        value = json.loads((original.LOCAL / 'baseline.json').read_bytes())
        value['supplied_brief'] = dict(path=original.BRIEF,
            sha256=original.sha(original.ROOT / original.BRIEF))
        value['adapter_origin_sha256'] = original.sha(original.__file__)
        value['scope'] = 'Initial tracked baseline plus supplied brief pinned at export preparation.'
        original.write(baseline, value)
    # Original exporter verifies complete/task inventories and exact patch bytes.
    original.export(sys.argv[1])
    receipt = original.LOCAL / sys.argv[1] / 'delivery.json'
    result = json.loads(receipt.read_bytes())
    for coverage, info in result['patches'].items():
        source_patch = Path(info['path'])
        target = original.ROOT / '.local-work/diffs' / ('d5ap-' + sys.argv[1] + '-' + coverage + '.diff')
        with target.open('xb') as stream:
            stream.write(source_patch.read_bytes())
        if original.sha(target) != info['sha256']:
            raise ValueError('D5AP named export differs')
        info['path'] = str(target)
    result['adapter_sha256'] = original.sha(__file__)
    result['original_export_receipt_sha256'] = original.sha(receipt)
    original.write(receipt.with_name('d5ap-delivery.json'), result)


if __name__ == '__main__':
    main()
