# SPDX-License-Identifier: GPL-3.0-or-later
"""D5AR adapter of owned D5AO N2 exact-byte review exporter (SOR-P-0002).

Reads Git and authored files; writes fresh ignored preservation receipts, diffs
and disposable replay trees. No staging, refs, game, saves or database writes.
The inherited exporter enforces both caller-available drive floors.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import d5ao_n2_delivery as original
import json
from pathlib import Path

original.LOCAL = original.ROOT / '.local-work/d5ar'
original.BRIEF = 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AR_generic_outpost_geometry_snapshot_plugin.md'
original.allowed = lambda n: n in {'CREDITS.md', 'docs/SOURCES.md', 'docs/RESEARCH_STATE.md', 'docs/PERMISSIONS.md', 'THIRD_PARTY_NOTICES.md'} or n.startswith((
    'docs/experiments/resource-retained-population/d5ar-',
    'docs/experiments/resource-retained-population/run-card-d5ar-',
    'research/resource-retained-population/d5ar_',
    'runtime/outpost-geometry-snapshot/'))

if __name__ == '__main__':
    if sys.argv[1:] == ['baseline']:
        original.baseline()
    elif len(sys.argv) == 3 and sys.argv[1] == 'export':
        original.export(sys.argv[2])
        receipt = original.LOCAL / sys.argv[2] / 'delivery.json'
        value = json.loads(receipt.read_bytes())
        for coverage, row in value['patches'].items():
            destination = original.ROOT / '.local-work/diffs' / ('d5ar-' + sys.argv[2] + '-' + coverage + '.diff')
            with destination.open('xb') as stream:
                stream.write(Path(row['path']).read_bytes())
            if original.sha(destination) != row['sha256']:
                raise ValueError('Named patch differs')
            row['path'] = str(destination)
        # Read-only Ghidra adapters retain task-named exports beside the existing
        # copied D5AM project. Inventory these new local outputs as well; do not
        # imply that all task evidence lives inside the D5AR output directory.
        extra = sorted(path for directory in (original.ROOT / '.local-work/d5am').glob('d5ar-*')
                       if directory.is_dir() for path in directory.rglob('*') if path.is_file())
        extra_hashes = original.hashes(extra)
        value['additional_local_exclusions'] = [dict(path=path.relative_to(original.ROOT).as_posix(),
            bytes=path.stat().st_size, sha256=extra_hashes[path]) for path in extra]
        if original.hashes(extra) != extra_hashes:
            raise ValueError('Task export changed during local exclusion inventory')
        if any(original.sha(original.ROOT / name) != row['sha256']
               for name, row in value['files'].items() if row['sha256'] is not None):
            raise ValueError('Authored source changed during final adapter inventory')
        value['adapter_sha256'] = original.sha(__file__)
        value['inherited_exporter_sha256'] = original.sha(original.__file__)
        original.guard()
        original.write(receipt.with_name('d5ar-delivery.json'), value)
    else:
        raise SystemExit('Usage: d5ar_delivery.py baseline | export FRESH_LABEL')
