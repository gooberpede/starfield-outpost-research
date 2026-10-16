# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline E2 definition inventory, using the maintainer-owned strict ESM reader.
Reads installed main ESM and supplied/sibling text; writes exclusive ignored JSON.
Stdlib only, CPython, repository cwd; no game/save/database/configuration effects.
Raw record fields remain local. No native invocation or external tool execution.
Usage: python -B research/e2-organic/catalog.py --run NAME
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import guard


def pin(p):
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    out = ROOT / '.local-work/e2-organic' / (args.run + '.json')
    assert not out.exists()
    guard()
    source = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    before = pin(source)
    assert before['sha256'] == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    records = []
    for h, fs in esm_records(source, {t.encode() for t in
            ['IRES', 'CONT', 'COBJ', 'KYWD', 'GLOB', 'AVIF', 'MISC', 'FLOR', 'OMOD', 'PNDT', 'NPC_', 'DFOB', 'PERK', 'RSPJ', 'PKIN', 'FLST']}, repeated=True):
        records.append(dict(**h, edid=next((v.rstrip(b'\0').decode() for k, v in fs if k == b'EDID'), ''),
                            fields=[(k.decode(), v.hex()) for k, v in fs]))
    network = Path('D:/Projects/starfield-outpost-network')
    texts = [Path('D:/tools/xEdit.4.1.5p/Edit Scripts/Starfield - Export Planet Biome Organic Resources.pas'),
             ROOT / '.local-work/screengrabs/1716740_63.jpg',
             network / 'reference-source/biome-organic-resources.csv',
             network / 'scripts/biome-reference-data.mjs',
             network / 'public/reference-data/organic-farming-profiles.json']
    textpins = [pin(p) for p in texts]
    with texts[2].open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    signatures = collections.Counter()
    for r in rows:
        signature = (r['SpeciesType'], r['ResourceResolutionStatus'], r['Domesticable'],
                     tuple((r['ResourceInput'+str(i)+'EditorID'], r['ResourceInput'+str(i)+'Qty']) for i in (1, 2)))
        signatures[str(signature)] += 1
    assert pin(source) == before
    assert [pin(p) for p in texts] == textpins
    result = dict(source=before, script=pin(Path(__file__)), dependencies=[pin(ROOT/'save-analysis/scripts'/n) for n in
                  ['inspect_outpost_definitions.py', 'inventory_historical_saves.py']], python=sys.version,
                  text_sources=textpins, records=records, source_rows=len(rows), source_signatures=signatures,
                  limits=['Main ESM only, no load-order override merger', 'CSV signatures are source-reported until definition cross-check'])
    out.parent.mkdir(exist_ok=True, parents=True)
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(records=len(records), source_rows=len(rows), signatures=signatures)))


if __name__ == '__main__':
    main()
