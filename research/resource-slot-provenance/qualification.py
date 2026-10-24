# SPDX-License-Identifier: GPL-3.0-or-later
"""Fail closed where owned selection cannot qualify the native slot projection.

Pure caller-data checks; no I/O. The frozen projection's Special selection is
usable only below native shared occupancy eight with a selected descriptor.
The native first-per-BIOM Everywhere set must equal the model's prepass set.
These checks bound the existing main-file/empty-atmosphere model, not every
possible loaded component or alternate creation route.
"""
from components import first_everywhere


def qualify(records, prediction):
    actual = {first_everywhere(records, int(str(v.orchestration.biome.form_id), 16))[0]
              for v in prediction.biome_results} - {0}
    modeled = {int(str(r.form_id), 16) for r in prediction.everywhere_resources}
    if actual != modeled:
        raise ValueError('UNQUALIFIED_EVERYWHERE_SHARED_OCCUPANCY')
    specials = []
    for selected in prediction.biome_results:
        state = selected.orchestration
        if not state.special_selection:
            continue
        events = [dict(e.fields) for e in state.events if e.kind.value == 'RESOURCE_OCCURRENCE_RECORDED'
                  and dict(e.fields).get('provenance').value == 'SPECIAL']
        if len(events) != 1 or events[0]['occupied_count_before'] >= 8 or not events[0]['accepted']:
            raise ValueError('UNQUALIFIED_SPECIAL_NATIVE_CAPACITY_GUARD')
        special = int(str(state.special_selection.form_id), 16)
        rsgd = int(str(state.effective_rsgd.form_id), 16)
        active, found = None, False
        for tag, raw in records[rsgd][1]:
            if tag == b'RNAM':
                active = int.from_bytes(raw, 'little')
            elif tag == b'DNAM' and active == special:
                found = True
        if not found:
            raise ValueError('UNQUALIFIED_SPECIAL_SELECTED_DESCRIPTOR')
        specials.append(dict(biome=int(str(state.biome.form_id), 16), resource=special,
                             occupied_before=events[0]['occupied_count_before']))
    return dict(everywhere_set=sorted(actual), specials=specials)
