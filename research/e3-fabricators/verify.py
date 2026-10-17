# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded E3 cross-evidence/integrity audit. CPython stdlib only.
Reads authored CSVs, prior/new local evidence, pinned installed inputs, saved
receipts, HEAD/index and Ghidra database files. Writes exclusive ignored JSON.
No game/native execution, database/save mutation, network or Git writes.
Requires completed catalogue/details runs and stopped read-only export session.
Checks prove table/byte consistency; native semantics require instruction review.
"""
import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/e3-fabricators'
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inventory_historical_saves import guard


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--catalog', default='catalog05.json')
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    out = BASE/(args.run+'.json')
    assert not out.exists()
    checks = []

    def check(ok, label):
        assert ok, label
        checks.append(label)

    cat = json.loads((BASE/args.catalog).read_text())
    check(sha(Path(cat['source']['path'])) == cat['source']['sha256'], 'ESM pin')
    check(sha(Path(cat['cache']['path'])) == cat['cache']['sha256'], 'prior E2 cache pin')
    check(sha(Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')) ==
          '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28', 'executable pin')
    doc = ROOT/'docs/experiments/fabricators'
    rows = list(csv.DictReader((doc/'facilities.csv').open(encoding='utf8', newline='')))
    recipes = list(csv.DictReader((doc/'recipes.csv').open(encoding='utf8', newline='')))
    check(len(rows) == len(cat['facilities']) == 45, '45 manufactured builder bases')
    check(len(recipes) == len(cat['resources']) == 43, '43 recipe-bearing resources including exceptions')
    check(sum(r['ordinary'] == 'True' for r in rows) == 30, '30 construction-reachable producer bases')
    check(len({r['ires'] for r in recipes}) == 43, 'IRES identities distinct')
    for row, f in zip(rows, cat['facilities']):
        check(row['formid'] == f['formid'] and row['edid'] == f['edid'] and
              int(row['esm_offset']) == f['offset'] and
              row['ordinary'] == str(f['ordinary']) and
              row['resource_avs'] == ';'.join(f['resource_avs']) and
              row['preset'] == ';'.join(f['preset']), 'facility identity/properties '+f['formid'])
        if f['ordinary']:
            a = f['assembly']
            check(row['tier'] == str(a['packin']['tier']) and row['packin'] == a['packin']['formid'] and
                  row['cell'] == f"{a['packin']['cell']:08x}" and row['producer_refr'] == a['reference'],
                  'facility construction join '+f['formid'])
    for row, r in zip(recipes, cat['resources']):
        expected = dict(ires=r['formid'], ires_edid=r['edid'], ires_offset=str(r['offset']),
                        av=r['av']['formid'], recipe=r['recipe']['formid'], recipe_offset=str(r['recipe']['offset']),
                        product=r['product']['formid'], product_edid=r['product']['edid'],
                        count=str(r['recipe_count']), interval_global=r['interval_global']['formid'],
                        seconds=str(r['seconds']), conditions=';'.join(r['conditions']),
                        inputs=';'.join(x['formid']+':'+x['edid']+'*'+str(x['quantity']) for x in r['inputs']))
        check(all(row[k] == v for k, v in expected.items()), 'exact recipe fields '+r['formid'])
        tiers = sorted({str(f['assembly']['packin']['tier']) for f in cat['facilities']
                        if f['ordinary'] and r['av']['formid'] in f['resource_avs']})
        check(row['ordinary_tiers'].split(';') == tiers if tiers else row['ordinary_tiers'] == '',
              'recipe catalogue membership '+r['formid'])
    for tier, count in [('1', 11), ('2', 10), ('3', 9)]:
        subset = [r for r in recipes if tier in r['ordinary_tiers'].split(';')]
        check(len(subset) == count, 'ordinary tier '+tier+' catalogue '+str(count))
        check(all(r['count'] == '1' for r in subset), 'recipe NNAM one tier '+tier)
    check(cat['physical_records_checked'] == 308, '308 independently reread physical definitions')
    detail = json.loads((BASE/'detail05.json').read_text())
    check(sha(Path(detail['source']['path'])) == detail['source']['sha256'], 'representative original save preserved')
    check(sha(Path(detail['tool']['path'])) == detail['tool']['sha256'], 'final detailed save reader pinned')
    check(len(detail['selected_rows']) == 17 and all(r['selected_value'] == 1 and
          r['evidence_kind'] == 'SAVED_BASE_AND_PRODUCER_CORROBORATED; DEFINITION_DERIVED_AV; NO_BF_OVERRIDE'
          for r in detail['selected_rows']), '17 saved preset/row joins; definition-derived AV explicitly labelled')
    summary = json.loads((BASE/'saved01/summary.json').read_text())
    check(summary['candidate_count'] == len(summary['rows']) == 184, 'mature inventory candidate coverage')
    present = 0
    for receipt in (BASE/'saved01').glob('HIST-*.json'):
        saved = json.loads(receipt.read_text())
        source = saved.get('source', {})
        if source and Path(source['path']).exists():
            check(sha(Path(source['path'])) == source['sha256'], 'audited original preserved '+receipt.stem)
            present += 1
    central = list(csv.DictReader((ROOT/'docs/experiments/native-availability-map/functions.csv').open(encoding='utf8', newline='')))
    check(len({r['key'] for r in central}) == len(central), 'unique central native keys')
    additions = json.loads((BASE/'register-additions.json').read_text())
    for r in additions:
        check(r in central, 'register exact '+r['key'])
        check(int(r['static_va'], 16)-0x140000000 == int(r['rva'], 16), 'address domain '+r['key'])
        check('FUNCTION\t'+r['static_va'][2:]+'\t' in (ROOT/r['source']).read_text(), 'export entry '+r['key'])
    before = json.loads((BASE/'db-before.json').read_text())
    after = {p: sha(Path(p)) for p in before}
    check(before == after, 'all recorded Ghidra database/project bytes preserved')
    seed = json.loads((BASE/'baseline.json').read_text())
    check(sha(ROOT/'.git/index') == seed['index']['sha256'], 'index bytes preserved')
    check(subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip() == seed['head'], 'HEAD preserved')
    check((ROOT/'docs/implementation-briefs/CODEX_BRIEF_SOR_E3_fabricators_manufactured_production.md').read_bytes() ==
          (BASE/'baseline-tree/docs/implementation-briefs/CODEX_BRIEF_SOR_E3_fabricators_manufactured_production.md').read_bytes(), 'supplied brief preserved')
    prose = []
    for p in [*doc.glob('*.md'), * (ROOT/'research/e3-fabricators').glob('*.py')]:
        raw = p.read_bytes()
        s = raw.decode('utf8')
        check(not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw, 'UTF8 LF '+p.name)
        check(not any(ord(c) in range(0x80, 0xa0) or c == '\ufffd' for c in s), 'no corrupt/control prose '+p.name)
        check(not re.search(r'\b(?:RVA|VA|CALL|stride|version)(?:0x|[0-9])', s), 'no fused address/version labels '+p.name)
        check(all(line.rstrip() == line for line in s.splitlines()), 'new-file whitespace '+p.name)
        if p.suffix == '.py':
            ast.parse(s)
        prose.append(str(p.relative_to(ROOT)))
    result = dict(status='PASS', checks=checks, prose_scope=prose,
                  database_files=len(before), saved_existing_files_rehashed=present, tool_sha256=sha(Path(__file__)),
                  limits=['No runtime measurements', 'No universal save population or output guarantee',
                          'Instruction interpretation separately independently reviewed'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    guard()
    print('PASS', len(checks), 'checks;', len(before), 'database/project files')


if __name__ == '__main__':
    main()
