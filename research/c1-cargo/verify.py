# SPDX-License-Identifier: GPL-3.0-or-later
"""C1 pins, selected real-data controls, native/ABC anchors and regressions.
Reads local baseline/final receipts and protected sources/database, owned tools,
HEAD/index read-only. Writes exclusive ignored JSON; --tables writes authored
source/function metadata only. CPython -B stdlib/project; both-drive40GB guards.
No native/game execution, target mutation, original writes or network.
"""
import argparse
import csv
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin
from inventory_historical_saves import guard

ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
ap.add_argument('--tables', action='store_true')
args = ap.parse_args()
assert args.run.isalnum()
guard()
base = ROOT / '.local-work/c1-cargo'
out = base / (args.run + '.json')
assert not out.exists()
baseline = json.loads((base / 'baseline.json').read_text())
checks, sources = [], []
def check(ok, label):
    assert ok, label
    checks.append(label)
def protected():
    for p in baseline['protected'] + [baseline['index'],baseline['brief'],baseline['screenshot']]:
        check(pin(p['path']) == p, 'protected ' + p['path'])
    check(subprocess.check_output(['git','rev-parse','HEAD']).decode().strip() == baseline['head'], 'HEAD unchanged')
protected()
for p in baseline['starting_untracked'].values():
    check(pin(p['path']) == p, 'supplied/starting untracked preserved ' + p['path'])
db = Path('D:/ReverseEngineering/Starfield/GhidraProject')
check({str(p) for p in db.rglob('*') if p.is_file()} ==
      {p['path'] for p in baseline['protected'] if 'GhidraProject' in p['path']},
      'database file inventory unchanged')
for p in baseline['protected'] + [baseline['brief'], baseline['screenshot']]:
    sources.append(p)
save = json.loads((base / 'save06.json').read_text())
src = json.loads((base / 'sources03.json').read_text())
abc = json.loads((base / 'menuabc03.json').read_text())
for p in [save['source'],save['prior'],save['cache'],save['tool'],src['esm'],
          src['cache'],src['assemblies'],src['zip'],src['archive'],src['swf'],src['tool']]:
    check(pin(p['path']) == p, 'receipt pin ' + p['path'])
    sources.append(p)
for s in src['scripts']:
    check(pin(s['local']['path']) == s['local'], 'installed source ZIP comparison receipt ' + s['member'])
    sources.append(s['local'])
check(len(src['definitions']) == 80, '80 physical ESM rereads retained')
check(len(save['rows']) == 29 and save['records'] == 205557, '29 selected /205557 framed Save52 records')
check(len(save['edges']) == 246, '246 fresh local edges')
def links(t):
    return {e['keyword']: e['target'] for x in save['rows'][t]['extra']['extras']
            if x['type'] == '4c' for e in x['entries']}
def dyn(t):
    return f'DYNAMIC:{0xff000000 | (int(t, 16) & 0x3fffff):08x}'
for a,b,owner in [('82c3c4','83444c','825f95'),('83444c','82c3c4','830a80')]:
    check(save['rows'][a]['base'] == 'starfield.esm:2a6c3f', 'ordinary pad base ' + a)
    check(links(a)['starfield.esm:255cc8'] == dyn(b) and
          links(a)['starfield.esm:255cc7'] == dyn('82dc37') and
          links(a)['starfield.esm:054ba6'] == dyn(owner), 'peer/ship/owner ' + a)
for marker,t,key,kind in [('82c3c4','82c3ef','2a6c45','219171'),
                          ('82c3c4','82c3f0','2a6c46','219173'),
                          ('83444c','834474','2a6c45','219171'),
                          ('83444c','834475','2a6c46','219173')]:
    row = save['rows'][t]
    check(links(marker)['starfield.esm:'+key] == dyn(t) and
          links(t)['starfield.esm:'+key] == dyn(marker), 'reciprocal child role ' + t)
    check(row['base'] == 'starfield.esm:'+kind, 'actual compartment base ' + t)
    check(row['inventory']['status'] == 'DECODED_EMPTY_STACK_EXTRA_SUBSET' and
          row['inventory']['item_count'] == 0 and
          row['inventory']['end'] - row['inventory']['start'] == 1, 'explicit zero inventory ' + t)
ship = save['rows']['82dc37']
check(ship['extra']['status'] == 'COUNT_CLOSED' and ship['extra']['extension'] == 'C1 bounded Extra33',
      'specific ship Extra33 gap resolved, no whole-record closure claim')
check(ship['inventory']['item_count'] == 0 and ship['inventory']['start'] == 2344497,
      'ship explicitly zero inventory at independent cursor')
check(len(links('82dc37')) == 9 and links('82dc37')['starfield.esm:255ccb'] == dyn('834474'),
      'nine ship role links and independently matching opposite outbox')
for t in ('82c3eb','82c3ee','834470','834473'):
    check(save['rows'][t]['base'] == 'starfield.esm:2508aa' and
          links(t)['starfield.esm:2a6c3e'] in (dyn('82c3c4'),dyn('83444c')),
          'terminal base/marker role ' + t)
for s,t in [('82c3f0','82c389'),('834475','839669')]:
    check([b for a,b in save['edges'] if a == dyn(s)] == [dyn(t)] and
          save['rows'][t]['base'] == 'starfield.esm:29b453', 'only immediate Warehouse destination ' + s)
check(dyn('829bce') in save['downstream']['82c3f0'] and
      dyn('84c843') in save['downstream']['834475'], 'indirect fabricator counterexamples retained')
inv = save['rows']['839669']['inventory']
check(inv['rows'][0]['item'] == 'starfield.esm:246b69' and
      inv['rows'][0]['stacks'][0]['count'] == 21, 'downstream Warehouse Magnet21 coexists with empty bay/ship')
check(len(abc['methods']) == 100 and all(r['decoded_bytes'] == r['code_bytes'] and
      all(x[1] != 'UNKNOWN_STOP' for x in r['instructions']) for r in abc['methods']),
      '100 selected ABC bodies fully framed with no unknown opcode stops')
check(len(abc['trait_constants']) == 1 and abc['trait_constants'][0]['value'] == 1,
      'OutpostEntry distance precision argument1 from actual ABC trait/int pool')
methods = {r['method']: r for r in abc['methods']}
for m, tokens in {970:['SourceRef','aResourcesNeeded','aOutgoingResources'],
                  971:['HideResources','WorkshopTargetMenu_TargetHovered'],
                  969:['fCargoShipWeight','fCargoShipMaxWeight','22:::round'],
                  579:['22:::MAX_RESOURCES','22:::SetResourceData'],
                  976:['WorkshopTargetMenu_TargetPicked','uHandle']}.items():
    text = json.dumps(methods[m])
    check(all(t in text for t in tokens), 'ABC binding anchors method ' + str(m))
exports = sorted((ROOT / '.local-work/recon').glob('c1-cargo-*.tsv')) + sorted((base / 'native').glob('*.request.tsv'))
function_rows = []
for p in exports:
    t = p.read_text(encoding='utf8')
    check('SHA256\t'+baseline['protected'][0]['sha256'] in t and 'BASE\t140000000' in t,
          'native build/domain ' + p.name)
    lines = t.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('FUNCTION\t'):
            _,addr,name,body = line.split('\t',3)
            function_rows.append([addr,'0x'+format(int(addr,16)-0x140000000,'x'),name,
                                  str(p.relative_to(ROOT)).replace('\\','/'),i+1,body,
                                  'STATIC / OBSERVED-INTERNAL; contract in native.md; no invocation'])
    sources.append(pin(p))
native = '\n'.join(p.read_text() for p in exports)
for token in ['"SourceRef"','"aResourcesNeeded"','"aOutgoingResources"',
              'FUN_140f80af0','FUN_140f7fd50','FUN_141724330','FUN_140404a10',
              'FUNCTION\t140404cf0','FUNCTION\t140562ef0','FUNCTION\t140f7ea10']:
    check(token in native, 'native decisive anchor ' + token)
check('FUN_140f80af0' not in native.split('void FUN_140f80af0',1)[1].split('FUNCTION\t',1)[0][100:],
      'no recursive self-call in exported direct-successor decompilation')
regressions = []
for name in ['test_workshop_inventory.py','test_outpost_record_framing.py',
             'test_stream_save.py','test_extractor_resources.py']:
    r = subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','save-analysis/scripts',
                        '-p',name], capture_output=True, text=True)
    check(r.returncode == 0, 'existing reader regression ' + name)
    regressions.append(dict(name=name,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
for p in [base/'baseline.json',base/'save06.json',base/'sources03.json',base/'menuabc03.json',
          Path(__file__),ROOT/'research/c1-cargo/menu_abc.py',
          ROOT/'ghidra/scripts/OutpostRecon.java',ROOT/'ghidra/scripts/Invoke-OutpostRecon.ps1',
          base/'native/E2ReadSession.java',base/'native/session.log',
          Path('C:/Users/User/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.12.8-hotspot/bin/java.exe'),
          Path(sys.executable),Path('D:/tools/ghidra_12.1.2_PUBLIC/Ghidra/application.properties')]:
    sources.append(pin(p))
for p in sorted((base/'native').glob('*.request')):
    sources.append(pin(p))
protected()
guard()
if args.tables:
    dest = ROOT/'docs/experiments/cargo-links/configuration-ui'
    with (dest/'sources.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow(['path','bytes','sha256','classification'])
        unique = {p['path']:p for p in sources}
        for p in unique.values():
            w.writerow([p['path'],p['bytes'],p['sha256'],'Metadata REVIEW-REQUIRED; payload LOCAL-ONLY'])
    with (dest/'functions.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow(['static_va','rva','original_name','local_evidence','function_line','body','scope'])
        w.writerows(function_rows)
with out.open('x',encoding='utf8',newline='\n') as f:
    json.dump(dict(checks=checks,regressions=regressions,sources=sources,
                   native_exports=len(exports),functions=len(function_rows),
                   limits=['No historical UI execution proof','No live transport/refresh observation',
                           'ABC framing and anchor checks are not an independent semantic oracle',
                           'Exact Extra33 subset only; not full ship tail'],python=sys.version),f,indent=2)
    f.write('\n')
print('PASS',len(checks),'checks;',len(exports),'native exports; four regression suites')
