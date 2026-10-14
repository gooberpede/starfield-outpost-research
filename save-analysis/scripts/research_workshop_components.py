"""SPDX-License-Identifier: GPL-3.0-or-later
Read pinned saves and native-qualified type6; exclusive local receipts only.
Stdlib/project dependencies, decoder scratch cleanup, C/D40GB guards. No target,
save, database, Git or network changes. Raw component data remains LOCAL-ONLY.
"""
import argparse
import json
from pathlib import Path
from inventory_historical_saves import ROOT, guard, identity
from extractor_resources import plugin_tables
from outpost_record_framing import Reader
from stream_save import decoded_save
from workshop_components import component_sections
from workshop_global_units import global_units


def audit(b):
    if int.from_bytes(b[16:20], 'little') != 27 or b[20] != 153:
        raise ValueError('UNQUALIFIED_COMPONENT_FORMAT')
    plugin_tables(b)  # Enforce the observed pinned-build header/plugin context.
    units = global_units(b)
    unit, = [r for r in units if r['type'] == 6]
    c = Reader(b, unit['body'], unit['end'])
    def u(n): return int.from_bytes(c.take(n), 'little')
    names = []
    for _ in range(u(4)):
        row = dict(offset=c.p, id_word=u(4), index=u(2))
        row['name'] = c.take(u(4)).decode('utf8')
        names.append(row)
    # This is an explicit sample qualification: successful body closure and the
    # independent name/vtable join support this activity format in these saves.
    sections = component_sections(b, c.p, c.end, buffer_version=153, activity_custom_payloads=True)
    return dict(schema='workshop-component-audit/1', unit=unit, names=names,
                sections=sections, exact_body_closure=True,
                population_complete=False, offset_domain='DECODED_LOGICAL_STREAM')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--labels', nargs='+', required=True)
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    if not a.run.isascii() or not a.run.replace('-', '').isalnum():
        raise ValueError('RUN_NAME')
    guard(); out = ROOT / '.local-work/workshop-population-rework' / a.run
    out.mkdir(exist_ok=False)
    manifest_pin = identity(a.inputs)
    inputs = json.loads(a.inputs.read_text(encoding='utf8'))
    for item in inputs:
        if item['label'] not in a.labels: continue
        pin = item['pin']; path = Path(pin['path'])
        if identity(path) != pin: raise ValueError('INPUT_IDENTITY')
        guard()
        with decoded_save(path, out / 'scratch') as (b, metrics):
            result = audit(b)
        if identity(path) != pin: raise ValueError('INPUT_CHANGED')
        result.update(source=pin, label=item['label'], decode=metrics)
        with (out / (item['label'] + '.json')).open('x', encoding='utf8') as f:
            json.dump(result, f, indent=2); f.write('\n')
        print(item['label'], result['unit']['size'], 'EXACT_CLOSURE', flush=True)
    if identity(a.inputs) != manifest_pin: raise ValueError('MANIFEST_CHANGED')
    guard()
