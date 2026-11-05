# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit A0-pinned config bytes for both native stitching setting keys.

Read-only installed/config access; fresh ignored receipt only. No claim that
configuration absence proves absence of a runtime text/Papyrus setter.
"""
import os, sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Pinned Python -E -B required')
import json
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha


def main():
    out = Path(sys.argv[1]).resolve()
    before = guard()
    if not out.is_relative_to(ROOT / '.local-work/d5ar') or out.exists() or any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)):
        raise ValueError('Fresh ignored output required')
    audit = ROOT / '.local-work/d5ar/a0-file-inputs05.json'
    source = json.loads(audit.read_bytes())
    rows = []
    for name, pin in source['inputs'].items():
        path = Path(name)
        if path.suffix.lower() != '.ini' and path.name.lower() not in ('plugins.txt', 'loadorder.txt'):
            continue
        if sha(path) != pin:
            raise ValueError('A0 configuration no longer matches: ' + name)
        raw = path.read_bytes()
        # All relevant ASCII spellings in both ordinary byte and UTF-16 files.
        matches = []
        for key in ('uBlockSize', 'uBlockMergeZoneSize', 'Stitching'):
            if key.lower().encode('ascii') in raw.lower() or key.lower().encode('utf-16le') in raw.lower():
                matches.append(key)
        rows.append(dict(path=name, sha256=pin, matching_keys=matches))
    if len(rows) != 23:
        raise ValueError('Incomplete A0 configuration inventory')
    if any(r['matching_keys'] for r in rows):
        raise ValueError('Pinned config has a relevant override requiring parse')
    result = dict(status='PASS_NO_STITCH_KEYS_IN_A0_PINNED_CONFIGS', files=rows,
                  native_default={'uBlockSize:Stitching':10, 'uBlockMergeZoneSize:Stitching':2},
                  default_provenance='Prior exact-beacon-planetary-coordinates ledger; new stitching-default01 original instructions for 0x14008cc50',
                  limits=['No runtime dynamic-setting write history certified', 'No successful initialization/INI apply inferred merely from absent config key'],
                  audit_sha256=sha(audit), method_sha256=sha(__file__), floors_before=before, floors_after=guard())
    with out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
