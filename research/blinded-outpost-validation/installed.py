# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only installed identity inventory; writes one exclusive local receipt.

Reuses owned bounded ESM framing. Reads/hashes EXE, ESM and PlanetData without
loading executable code. Finds candidate PNDT EDIDs independently of resources.
No game, save, asset extraction, configuration, network or analysis DB effects.
"""
from pathlib import Path
import sys
from audit import ROOT, LOCAL, pin, write
from bridge import EXE, ESM, PLANET


def main():
    output = Path(sys.argv[1]).resolve()
    if not output.is_relative_to(LOCAL) or output.exists():
        raise ValueError('FRESH_LOCAL_OUTPUT')
    base = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    inputs = {}
    for relative, expected in (('Starfield.exe', EXE), ('Data/Starfield.esm', ESM), ('Data/Starfield - PlanetData.ba2', PLANET)):
        actual = pin(base/relative)
        if actual != expected:
            raise ValueError('UNKNOWN_INSTALLED_INPUT')
        inputs[relative] = actual
    sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
    from inspect_outpost_definitions import esm_records
    candidates = []
    for header, fields in esm_records(base/'Data/Starfield.esm', {b'PNDT'}, repeated=True):
        edid = next((v.rstrip(b'\0').decode('utf8') for tag, v in fields if tag == b'EDID'), '')
        if any(name.lower() in edid.lower() for name in ('Kreet', 'Vectera', 'Jemison')):
            candidates.append(dict(formid=format(header['formid'], '08x'), edid=edid))
    write(output, dict(installed=inputs, candidates=candidates,
        capability='IDENTITY_ONLY; complete generation corpus and effective Workshop transform unqualified',
        decoder_sha256=pin(ROOT/'save-analysis/scripts/inspect_outpost_definitions.py')))
    print(candidates)


if __name__ == '__main__':
    main()
