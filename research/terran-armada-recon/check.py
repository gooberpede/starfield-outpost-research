# SPDX-License-Identifier: GPL-3.0-or-later
"""Check D5J joins, compiled-script closure/branches and immutable input pins.

Reads the two local investigation receipts and selected extracted PEX members.
Rehashes their installed inputs and method sources. Writes one exclusive ignored
receipt plus compact authored candidate/source tables. No game/VM/save effects.
Controls check parsing and identity, not runtime Workshop functionality.
"""
import csv
import argparse
import hashlib
import json
from pathlib import Path
import struct
from scan import OUT, ROOT, DATA, P, pin

DOC = ROOT / 'docs/experiments/terran-armada-outpost-recon'
SITES = [('FC', 'Give and Take', '02028236', '0202b254', '02038ac8', '0202b007', '0202b011', '0001b6ca', '0005dee9', 'Alpha Ternion III'),
         ('RI', 'Favors for Favors', '02028237', '0202b255', '02038ac9', '0202b032', '0202b061', '0001b060', '0005e13c', 'Nemeria IV-a'),
         ('UC', 'Quid Pro Quo', '02028235', '0202b256', '02038aca', '0202b062', '0202b096', '0001b51a', '0005df86', 'Strix I')]


def table(path, rows):
    with path.open('x', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main(out=OUT, doc=DOC):
    out, doc = Path(out).resolve(), Path(doc).resolve()
    assert out.is_relative_to(ROOT / '.local-work')
    assert doc.is_relative_to(ROOT / '.local-work') or doc == DOC
    a = json.loads((out / 'installed.json').read_text())
    b = json.loads((out / 'joins.json').read_text())
    for path, digest in a['inputs'].items():
        assert pin(path) == digest
    for row in b['headers']:
        assert pin(DATA / row['file']) == row['sha256']
    assert len(b['headers']) == 39 and len(b['dlc_overrides']) == 32
    assert {v['type'] for v in b['dlc_overrides']} == {'GBFM'}
    assert not b['loose_scripts']
    normal = next(r for r in b['records'] if r['formid'] == 0x2c60e9)
    nfields = dict(normal['fields'])
    strings = a['scripts']['strings/sfbgs050_en.strings']['strings']
    candidates, checks = [], []
    for faction, title, quest, ref, base, world, loc, bodyloc, pndt, bodyname in SITES:
        q, r, d = [a['records'][k] for k in (quest, ref, base)]
        bodyrec = next(v for v in b['records'] if v['formid'] == int(bodyloc, 16))
        planetrec = next(v for v in b['records'] if v['formid'] == int(pndt, 16))
        bodyfields = dict(bodyrec['fields'])
        body_system = int.from_bytes(bytes.fromhex(bodyfields['XNAM']), 'little')
        body_index = int.from_bytes(bytes.fromhex(bodyfields['YNAM']), 'little')
        in_body, triples = False, []
        for tag, h in planetrec['fields']:
            if tag == 'BDST':
                in_body = True
            elif tag == 'BDED':
                in_body = False
            elif tag == 'GNAM' and in_body:
                triples.append(struct.unpack('<III', bytes.fromhex(h)))
        assert len(triples) == 1 and (triples[0][0], triples[0][2]) == (body_system, body_index)
        qf, rf, df = [dict(v['fields']) for v in (q, r, d)]
        assert strings[str(int.from_bytes(bytes.fromhex(qf['FULL']), 'little'))] == title
        assert rf['NAME'] == int(base, 16).to_bytes(4, 'little').hex()
        assert any(x[1] == '0x' + world and x[2] == 1 for x in b['ancestry']['0x' + ref])
        assert df['KWDA'] == nfields['KWDA']
        assert 'XOWN' not in rf and 'XESP' not in rf
        xyz = struct.unpack('<6f', bytes.fromhex(rf['DATA']))
        props = list(struct.iter_unpack('<IfI', bytes.fromhex(df['PRPS'])))
        assert (0x63fc5, 150.0, 0) in props and (0x319872, 500.0, 0) in props
        assert (0x319872, 500.0, 0) not in list(struct.iter_unpack('<IfI', bytes.fromhex(nfields['PRPS'])))
        location = bytes.fromhex(dict(a['records'][loc]['fields'])['LCSR'])
        assert len(location) % 20 == 0
        assert struct.unpack_from('<III', location) == (0x3e8651, int(ref, 16), int(world, 16))
        assert sum(1 for v in a['catalog'] if v['type'] == 'REFR' and v['formid'] == int(ref, 16)) == 1
        candidates.append(dict(candidate=faction, quest=title, quest_file_formid='0x' + quest,
            beacon_template='0x' + ref, beacon_base='0x' + base, world='0x' + world,
            location='0x' + loc, body_location='0x' + bodyloc, planet='0x' + pndt,
            body=bodyname, authored_xyz='; '.join(repr(v) for v in xyz[:3]),
            authored_rotation='; '.join(repr(v) for v in xyz[3:]),
            placement='Hybrid static route: authored template plus native queued request; instance state unresolved',
            exact_planetary_center='UNKNOWN', ordinary_admission='Shared beacon binding and native accessor eligibility; execution unverified',
            oracle='Conditional native geometry; Workshop accept and transfer not observed',
            missing='Instantiated placement and frame; current Workshop state; source history',
            decision='PROMISING_NEEDS_EXACT_OPERAND'))
        checks.append(faction + ': title, base, ancestry, radius, budget and reference-type joins pass')
    rejected, branches = 0, 0
    for name, v in a['scripts'].items():
        if 'decoded' not in v:
            continue
        raw = (out / Path(name).name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == v['sha256']
        assert json.loads(json.dumps(P(raw).parse())) == v['decoded']
        for bad in (raw[:-1], raw[:16], b'bad!' + raw[4:]):
            try:
                P(bad).parse()
            except (AssertionError, IndexError, ValueError, struct.error, UnicodeDecodeError):
                rejected += 1
            else:
                raise AssertionError('Malformed member accepted')
        for obj in v['decoded']['objects']:
            for state, fs in obj['states']:
                for fn, f in fs:
                    for i, op in enumerate(f['ops']):
                        if op['op'] in (20, 21, 22):
                            delta = op['args'][-1]
                            assert delta[0] == 3 and 0 <= i + delta[1] <= len(f['ops'])
                            branches += 1
    sources = []
    for path in [out / 'installed.json', out / 'joins.json', out / 'preservation-before.json']:
        sources.append(dict(key=path.stem, locator=str(path), sha256=pin(path), scope='Local primary receipt; excluded from patches'))
    for path, digest in a['inputs'].items():
        sources.append(dict(key=Path(path).name, locator=path, sha256=digest, scope='Bethesda installed input; LOCAL-ONLY'))
    for name, v in a['scripts'].items():
        sources.append(dict(key=Path(name).name, locator='SFBGS050 - Main.ba2::' + name, sha256=v['sha256'], scope='Selected compiled member or localized strings; LOCAL-ONLY'))
    for path in [ROOT / 'save-analysis/scripts/inspect_outpost_definitions.py', ROOT / 'research/c2-transport/pex.py', ROOT / 'research/review_package.py']:
        sources.append(dict(key=path.name, locator=str(path), sha256=pin(path), scope='Owned method at starting HEAD; SOR-P-0002'))
    for name in ('Starfield.esm', 'SFBGS00D.esm', 'BlueprintShips-SFBGS050.esm'):
        row = next(v for v in b['headers'] if v['file'].lower() == name.lower())
        sources.append(dict(key=name, locator=str(DATA / name), sha256=row['sha256'], scope='Installed definition context; LOCAL-ONLY'))
    for path, row in b['config'].items():
        sources.append(dict(key=Path(path).name, locator=path, sha256=row['sha256'], scope='Current installed or Git identity; no runtime slot inference'))
    doc.mkdir(parents=True, exist_ok=True)
    table(doc / 'candidates.csv', candidates)
    table(doc / 'sources.csv', sources)
    with (out / 'checks.json').open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(identity_checks=checks, malformed_inputs_rejected=rejected,
                       bounded_branch_targets=branches, runtime_functionality='NOT TESTED'), f, indent=2)
        f.write('\n')
    print('PASS', checks, 'malformed rejections', rejected, 'branches', branches)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--doc', type=Path, default=DOC)
    args = ap.parse_args()
    main(args.out, args.doc)
