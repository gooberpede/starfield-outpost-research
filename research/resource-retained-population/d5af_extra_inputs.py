# SPDX-License-Identifier: GPL-3.0-or-later
"""Recompute fixed Feynman component selection from pinned installed definitions.

Uses existing owned builder and maintainer-owned sibling selection model under
SOR-P-0002. Reads installed ESM and owned methods; writes one fresh ignored JSON.
No target, save, native execution, database or Git mutation. Model output is
conditional main-file initialization, never B2 effective runtime state.
"""
from pathlib import Path
import dataclasses
import hashlib
import json
import sys

root = Path(__file__).resolve().parents[2]
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B')
target = (root / '.local-work/d5af' / sys.argv[1]).resolve()
if target.exists() or not target.is_relative_to(root / '.local-work/d5af'):
    raise ValueError('Fresh task-local receipt required')
sys.path.insert(0, str(root / 'research/resource-standalone'))
import builder

assert min(builder.shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
assert builder.pin(builder.ESM) == builder.DEFINITION
assert all(builder.pin(builder.OWNED / name) == value for name, value in builder.OWNED_PINS.items())
records = {h['formid']: (h, fs) for h, fs in builder.esm_records(
    builder.ESM, {b'PNDT', b'BIOM', b'RSGD', b'IRES'}, repeated=True)}
predicted = builder.selections(records, 0x5e0de)
selected = next(v for v in predicted.biome_results
                if int(str(v.orchestration.biome.form_id), 16) == 0x145440)
result = dataclasses.asdict(selected)
effective = selected.orchestration.effective_rsgd
special = selected.orchestration.special_selection
everywhere = [str(e.resource_form_id) for e in effective.entries
              if e.resource_rarity.value == 'Everywhere']
sys.path.insert(0, str(root / 'research/resource-slot-provenance'))
import components
component = next(row for row in components.components(records, predicted)
                 if row['biome'] == 0x145440)
assert component['slots'][4:] == [0, 0]
inputs = dict(esm_sha256=builder.DEFINITION,
              owned_sibling=str(builder.OWNED), owned_pins=builder.OWNED_PINS,
              builder_sha256=builder.pin(root / 'research/resource-standalone/builder.py'))
out = dict(scope='Fixed main-file/default initialization selection; not B2 runtime operands',
           inputs=inputs, selected_biome='00145440', body='0005e0de',
           special_is_none=special is None, everywhere=everywhere,
           selected=result, component=component,
           components_method_sha256=builder.pin(root / 'research/resource-slot-provenance/components.py'),
           method_sha256=builder.pin(Path(__file__)))
if special is not None or everywhere:
    raise AssertionError('Fixed-source extra pass unexpectedly present')
with target.open('x', encoding='utf8', newline='\n') as stream:
    stream.write(json.dumps(out, indent=2, default=str)+'\n')
print(json.dumps(dict(special_none=special is None, everywhere=everywhere,
                     effective_rsgd=str(effective.form_id))))
