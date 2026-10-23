# SPDX-License-Identifier: GPL-3.0-or-later
"""Read upstream PNDT-linked SFTR tables, without native witness inputs.

Reads the pinned installed main ESM using the owned bounded ESM reader; no
external dependencies or target effects. Full decoded tables remain local.
Only the unmodified main-file FormID namespace and FNAM/GNAM route are covered.
"""
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records

ESM = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')


def planet_tree(fields):
    """FNAM outside BDST is the typed SFTR link, not BDST orbital data."""
    links = []
    in_body = False
    for tag, value in fields:
        if tag == b'BDST':
            in_body = True
        elif tag == b'BDED':
            in_body = False
        elif tag == b'FNAM' and not in_body:
            if len(value) != 4:
                raise ValueError('PNDT tree reference must be uint32')
            links.append(struct.unpack('<I', value)[0])
    if len(links) != 1 or not links[0]:
        raise ValueError('one nonzero PNDT tree link required')
    return links[0]


def decode_tree(fields):
    """Native 0x14096fde0 FNAM/GNAM path stores table words in native order.

    Do not apply BIOM raster transposition to these precomputed arrays. Reject
    packed ENAM or malformed faces rather than silently treating them as empty.
    """
    count = struct.unpack('<I', next(v for t, v in fields if t == b'CNAM'))[0]
    dimension = struct.unpack('<I', next(v for t, v in fields if t == b'DNAM'))[0]
    arrays = [(t, v) for t, v in fields if t in (b'FNAM', b'GNAM', b'ENAM')]
    if count != 2 or dimension != 256 or [t for t, v in arrays] != [b'FNAM', b'GNAM'] * 2:
        raise ValueError('qualified two-face 256-square FNAM/GNAM tree required')
    tables = []
    for face in range(count):
        ids, flags = arrays[face * 2][1], arrays[face * 2 + 1][1]
        if len(ids) != 4 * 65536 or len(flags) != 65536:
            raise ValueError('surface-tree face length mismatch')
        tables.append(list(zip(struct.unpack('<65536I', ids), flags)))
    return tables


def load_trees(owners):
    """Resolve records by PNDT FormID and its link, never by expected SFPT."""
    planets = {r['formid']: (r, fs) for r, fs in esm_records(ESM, {b'PNDT'}, repeated=True)
               if r['formid'] in owners}
    if set(planets) != set(owners):
        raise ValueError('missing selected PNDT')
    links = {owner: planet_tree(fs) for owner, (r, fs) in planets.items()}
    trees = {r['formid']: (r, fs) for r, fs in esm_records(ESM, {b'SFTR'}, repeated=True)
             if r['formid'] in links.values()}
    if set(trees) != set(links.values()):
        raise ValueError('missing linked SFTR')
    return {owner: dict(owner=owner, pndt=planets[owner][0], tree=trees[link][0],
        tables=decode_tree(trees[link][1]),
        components=[v.rstrip(b'\0').decode() for t, v in trees[link][1] if t == b'BFCB'])
        for owner, link in links.items()}
