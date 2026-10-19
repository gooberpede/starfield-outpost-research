# SPDX-License-Identifier: GPL-3.0-or-later
"""DA1 offline correspondence checker. Repository cwd, CPython 3.14 -B/stdlib.

Reads physical pinned ESM/BA2, protected saved originals, local source/native
receipts and owned readers. Writes one exclusive ignored receipt; temporary save
scratch is context-cleaned. No source, target, database, Git or network writes.
Both-drive 40GB guards apply. These are byte/branch/identity checks, not gameplay.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import struct
import subprocess
import sys
import zlib

R = Path.cwd()
W = R / '.local-work/da1-defense'
D = R / 'docs/experiments/outpost-defense'
sys.path[:0] = [str(W), str(R / 'save-analysis/scripts')]
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords
from stream_save import decoded_save
from validate_mature_outposts import directory
from workshop_population import typed_records, initial_prefix
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from links_da1 import actor_prefix, explicit_actor_links


def pin(p):
    p = Path(p)
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    assert a.run.isalnum()
    out = W / ('verification-' + a.run + '.json')
    assert not out.exists()
    guard()
    checks = []

    def check(label, ok):
        if not ok:
            (W / ('failure-' + a.run + '.json')).open('x', encoding='utf8').write(
                json.dumps(dict(failed=label, prior_checks=checks), indent=2) + '\n')
        assert ok, label
        checks.append(label)

    seed = json.loads((W / 'baseline.json').read_text(encoding='utf8'))
    for p in seed['protected'] + [seed['brief'], seed['index'], seed['screenshot']]:
        check('protected ' + Path(p['path']).name, pin(p['path']) == p)
    check('HEAD unchanged', subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == seed['head'])
    rs = json.loads((W / 'definitions01.json').read_text(encoding='utf8'))['records']
    by = {r['formid']: r for r in rs}
    esm = next(Path(p['path']) for p in seed['protected'] if Path(p['path']).name == 'Starfield.esm')
    defs = list(csv.DictReader((D / 'definitions.csv').open(encoding='utf8')))
    with esm.open('rb') as f:
        for row in defs:
            fid = int(row['formid'], 16)
            r = by[fid]
            f.seek(int(row['offset']))
            h = f.read(24)
            n, flags, actual = struct.unpack_from('<III', h, 4)
            check('physical header ' + row['formid'], actual == fid and h[:4].decode() == row['type'])
            b = f.read(n)
            if flags & 0x40000:
                sz = int.from_bytes(b[:4], 'little')
                b = zlib.decompress(b[4:])
                check('physical decompression ' + row['formid'], len(b) == sz)
            check('physical fields ' + row['formid'], [(k.decode(), v.hex()) for k, v in subrecords(b)] == [tuple(x) for x in r['fields']])
    scripts = json.loads((W / 'scripts04.json').read_text(encoding='utf8'))
    check('38 fully decoded members', len(scripts['members']) == 38 and all('decoded' in m for m in scripts['members'].values()))
    for name, m in scripts['members'].items():
        check('PEX closure ' + name, all(o['end'] == o['declared_end'] for o in m['decoded']['objects']))

    def obj(name):
        return scripts['members']['Scripts/' + name + '.pex']['decoded']['objects'][0]

    def funcs(name):
        return {fn: b for _, fs in obj(name)['states'] for fn, b in fs}

    defaults = {v[0]: v[3] for v in obj('SQ_ParentScript')['variables']}
    for name, expected in [('minDaysSinceLastAttack', 7), ('minDaysSinceLastAttackRoll', .04), ('attackChanceBase', .1), ('attackChanceCreature', .08), ('attackChanceResourceMult', .01), ('attackChanceCargoLinkMult', .05)]:
        check('compiled constant ' + name, abs(defaults[name][1] - expected) < 1e-7)
    bf = funcs('OutpostBeaconScript')
    check('one shot timer has no rearm', [o['args'][0][1] for o in bf['OnTimer']['ops'] if o['op'] == 23] == ['CheckForAttack'])
    check('timer seconds range', {v[0]: v[3] for v in obj('OutpostBeaconScript')['variables']}['fAttackTimerMinSeconds'][1] == 12 and {v[0]: v[3] for v in obj('OutpostBeaconScript')['variables']}['fAttackTimerMaxSeconds'][1] == 48)
    cf = funcs('SQ_ParentScript')['CheckForAttack']['ops']
    check('actual scheduler start/last instruction locators', cf[0]['offset'] == 43725 and cf[-1]['offset'] == 45106)
    check('same planet operands precede RNG', sum('GetCurrentPlanet' in str(o['args']) for o in cf[:15]) == 2)
    human = funcs('SQ_OutpostAttackHumansScript')
    unload = next(b['ops'] for n, b in human.items() if n.lower().endswith('onunload'))
    check('explicit unloaded destruction calls', all(any(v in str(o['args']) for o in unload) for v in ['IsAttackStarted', 'GetCountDead', 'GetDestructibleOutpostObjects', 'Is3DLoaded', 'SetDestroyed']))
    vm = json.loads((W / 'vmad01.json').read_text(encoding='utf8'))
    parent = next(s for s in vm['SQ_Parent']['scripts'] if s['name'].lower() == 'sq_parentscript')
    props = {p['name']: p for p in parent['properties']}
    special = props['OutpostAttackSpecialCases']['value']
    check('one installed special case', len(special) == 1)
    sc = {p['name'].lower(): p['value'] for p in special[0]}
    check('special50 condition/event identities', sc['specialcaseattackchance'] == .5 and sc['specialcasecondition']['form'] == '002baa4b' and sc['storyeventkeyword']['form'] == '00349c9e')
    star = next(s for s in vm['SQ_OutpostAttackSpecial_Starborn01']['scripts'] if s['name'].lower() == 'sq_outpostattackhumansscript')
    check('Starborn does not stamp ordinary cooldown', next(p['value'] for p in star['properties'] if p['name'] == 'CountsAsAttack') == 0)
    mb = next(s for s in vm['MB_Parent']['scripts'] if s['name'].lower() == 'missionparentscript')
    check('111 resource inputs', len(next(p['value'] for p in mb['properties'] if p['name'] == 'resourceAVs')) == 111)
    menu = json.loads((R / '.local-work/l2-budget/menu01.json').read_text(encoding='utf8'))
    ui = next(m for m in menu['methods'] if m['method'] == 1429)
    check('UI method closure and Integrity consumer', ui['code_bytes'] == ui['decoded_bytes'] == 1341 and [874, 'getproperty', 'fIntegrity'] in ui['instructions'] and [894, 'callpropvoid', 'gotoAndStop', 1] in ui['instructions'])
    for row in csv.DictReader((D / 'functions.csv').open(encoding='utf8')):
        p = R / row['export']
        check('native hash ' + row['va'], pin(p)['sha256'] == row['sha256'])
        s = p.read_text(encoding='utf8')
        check('native identity/entry ' + row['va'], 'SHA256\t' + seed['protected'][2]['sha256'] in s and 'BASE\t140000000' in s and 'FUNCTION\t' + row['va'] + '\t' in s)
    saved = json.loads((W / 'saved2-HIST-0255.json').read_text(encoding='utf8'))
    rows = {r['identity']: r for r in saved['rows']}
    targets = {'DYNAMIC:ff01d232': -12, 'DYNAMIC:ff0202dc': -144, 'DYNAMIC:ff0202e6': -40.5, 'DYNAMIC:ff062023': -380, 'DYNAMIC:ff072592': -3.6667633056640625}
    wanted = set(targets) | {'DYNAMIC:ff0202f7', 'DYNAMIC:ff038e6c', 'DYNAMIC:ff038e6d', 'DYNAMIC:ff087168'}
    src = Path(saved['source']['path'])
    check('selected original prehash', pin(src) == saved['source'])
    seen = set()
    with decoded_save(src, W / 'verify-scratch') as (data, _):
        dr = directory(data)
        forms = struct.unpack_from('<' + 'I' * dr['reference_count'], data, dr['regions']['reference_u32'][0] + 4)
        plugins = plugin_tables(data)

        def resolve(t):
            return saved_form(token_value(t, forms), plugins)

        for rec in typed_records(data):
            ident = resolve(rec['token'])
            if ident not in wanted:
                continue
            row = rows[ident]
            check('saved bounds ' + ident, rec['offset'] == row['record']['offset'] and rec['end'] == row['record']['end'])
            p = actor_prefix(data, rec) if rec['form_type'] == 0x4b else initial_prefix(data, rec)
            check('saved base ' + ident, resolve(p['base_token']) == row['base'])
            if ident in targets:
                vals = [v for e in row['extras']['extras'] for sec in e.get('sections', []) for v in sec['values'] if v['av'] == 'starfield.esm:0002d4']
                check('saved damage metadata ' + ident, len(vals) == 1 and vals[0]['bit'] == 2 and vals[0]['value'] == targets[ident] and row['extras']['status'] == 'COUNT_CLOSED')
                v = vals[0]
                check('literal independent float ' + ident, struct.unpack_from('<f', data, v['offset'])[0] == targets[ident])
            if ident in ['DYNAMIC:ff038e6c', 'DYNAMIC:ff038e6d']:
                links = explicit_actor_links(data, rec, resolve)
                check('actual turret owner ' + ident, any(e['keyword'] == 'starfield.esm:054ba6' and e['target'] == 'DYNAMIC:ff087168' and e['mode'] == 0 for e in links['entries']))
                check('counted E6 width ' + ident, any(t['type'] == 'e6' and t['end'] - t['start'] == 10 for t in links['trace']))
            seen.add(ident)
    check('all nine selected records reread', seen == wanted)
    check('selected original posthash', pin(src) == saved['source'])
    healthy = rows['DYNAMIC:ff0202f7']
    check('same-base healthy closed control', healthy['base'] == rows['DYNAMIC:ff0202dc']['base'] and healthy['extras']['status'] == 'COUNT_CLOSED' and not any(v['av'] == 'starfield.esm:0002d4' for e in healthy['extras']['extras'] for sec in e.get('sections', []) for v in sec['values']))
    owner = rows['DYNAMIC:ff087168']
    check('real beacon plus CB cross-check', owner['base'] == 'starfield.esm:2c60e9' and all(any(t in e.get('references', []) for e in owner['extras']['extras'] if e['type'] == 'cb') for t in ['DYNAMIC:ff038e6c', 'DYNAMIC:ff038e6d']))
    for p in W.glob('saved-*.json'):
        j = json.loads(p.read_text(encoding='utf8'))
        check('corpus preservation ' + j['label'], pin(j['source']['path']) == j['source'] and j['source_unchanged'])
    guard()
    out.open('x', encoding='utf8').write(json.dumps(dict(run=a.run, total=len(checks), checks=checks, physical_definitions=len(defs), saved_rereads=len(seen), limits='Correspondence/integrity and instruction operands, not a runtime or historical-cause oracle'), indent=2) + '\n')
    print('PASS', len(checks), 'checks;', len(defs), 'physical definitions;', len(seen), 'saved records')


if __name__ == '__main__':
    main()
