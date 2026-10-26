# SPDX-License-Identifier: GPL-3.0-or-later
"""Opt-in committed archive substitution for historical preservation rows.

Before the separate GO publishes an ACTIVE selection, return no substitutions.
After activation, authenticate the journal, baseline, archive/index and loose
holds once. Preserve each original expected digest; never substitute saved files.
Historical verification retains original protected-save/input reads.
No restoration, deletion or target effects.
"""
import json
import os
import sys
from pathlib import Path

from cutover import ROOT, OUT, OWNER, e, verify_active_selection, trusted_configuration

SELECTION = ROOT / 'docs/experiments/resources-evidence-consolidation/active-baseline.json'


def archived_expectations():
    if not SELECTION.exists():
        return {}
    config = trusted_configuration()
    result, tx = verify_active_selection(SELECTION, config, include_members=True)
    return {os.path.normcase(os.path.normpath(str(tx.root / row['path']))): row['sha256']
            for row in result['_archive_rows']}


def verify_historical():
    """Verify the actual D5G roster with only committed substitutions enabled."""
    sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
    import protection
    protected = protection.audit(include_archive_pins=True)
    archived = protected.pop('_archive_pins')
    if protected['changes']:
        raise e.Error('Existing protected-input/save policy failed')
    manifest = OUT / 'historical-pins.json'
    if e.pin(manifest) != 'a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b':
        raise e.Error('Historical pin roster changed')
    pins = json.loads(manifest.read_text())['pins']
    loose, substituted = 0, 0
    for name, expected in pins.items():
        key = os.path.normcase(os.path.normpath(name))
        if key in archived:
            actual = archived[key]
            substituted += 1
        else:
            actual = e.pin(Path(name))
            loose += 1
        if actual != expected:
            raise e.Error('Historical expected digest mismatch: ' + name)
    return dict(state='ACTIVE' if archived else 'ORIGINAL-LOOSE', before_pins=len(pins),
                loose_payload_hashes=loose, archived_pin_matches=substituted,
                protected_policy_rows=protected['count'], protected_changes=0)


if __name__ == '__main__':
    print(json.dumps(verify_historical(), indent=2))
