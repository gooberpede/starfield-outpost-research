"""SPDX-License-Identifier: GPL-3.0-or-later
Offline trial runner. Reads approved archived saves/manifests and installed ESMs;
writes exclusive ignored JSON/text under .local-work/extractor-resource/<run>.
Stdlib and project readers only; no external program, game or database effects.
Temporary disk-backed decoder scratch is removed by existing decoded_save.
All selected record regions are exhausted, with C:/D: disk guards. No raw save
or game fields are written outside ignored local work. No downloads/dependencies.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys
from extractor_resources import definition_catalog, inventory, plugin_tables, select_records
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import ROOT, identity, guard
from stream_save import decoded_save


def write(path, data):
    with path.open('x', encoding='utf8', newline='\n') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write('\n')


def run(out, data, static=None):
    guard()
    out.mkdir(parents=True, exist_ok=False)
    contract = ROOT / 'docs/experiments/extractor-resource-contract.md'
    write(out/'contract-pin.json', identity(contract))
    if static:
        before_static = identity(static)
        source = json.loads(static.read_text(encoding='utf8'))
        for s in source['sources']:
            if identity(Path(s['path'])) != s:
                raise ValueError('STATIC_SOURCE_PIN_CHANGED')
        if identity(static) != before_static:
            raise ValueError('STATIC_DERIVATION_CHANGED')
    else:
        source = dict(records=[], sources=[])
        for p in sorted(data.glob('*.esm'), key=lambda p: p.name.lower()):
            before = identity(p)
            for r, fs in esm_records(p, {b'TES4', b'CONT', b'COBJ', b'AVIF', b'IRES',
                                        b'MISC', b'LVLI', b'KYWD'}, repeated=True):
                edid = next((v.rstrip(b'\0').decode('utf8', 'backslashreplace')
                             for k, v in fs if k == b'EDID'), '')
                source['records'].append(dict(plugin=p.name, edid=edid, **r,
                    fields=[(k.decode('ascii'), v.hex()) for k, v in fs]))
            if identity(p) != before:
                raise ValueError('ESM_INPUT_CHANGED')
            source['sources'].append(before)
            print('ESM', p.name, flush=True)
        guard()
        write(out/'static-records.json', source)
    catalog = definition_catalog(source['records'])
    write(out/'all-installed-catalog.json', catalog)
    inputs = []
    manifests = []
    for folder in ('manual-S0-S7C', 'output-link-L0-L2C'):
        manifest = ROOT/'.local-work'/folder/'manifest.json'
        manifests.append(identity(manifest))
        m = json.loads(manifest.read_text(encoding='utf8'))
        for s in m['samples']:
            inputs.append(dict(label=s['label'], series=folder, sample_id=s['sample_id'],
                               source=Path(s['copy']['path']), expected=s['copy']['sha256']))
    mature = list((ROOT/'.local-work/savegames').glob('Save52_*.sfs'))
    if len(mature) != 1:
        raise ValueError('MATURE_ARCHIVE_AMBIGUOUS')
    # Independently recorded input pin from the prior mature extraction receipt.
    prior = ROOT/'.local-work/mature-save-validation'
    pins = []
    for f in prior.glob('*/inputs-before.json'):
        old = json.loads(f.read_text(encoding='utf8'))
        pins += [v['sha256'] for k,v in old.items() if Path(k)==mature[0]]
    if not pins or len(set(pins)) != 1:
        raise ValueError('MATURE_PRIOR_PIN_MISSING_OR_CONFLICTING')
    inputs.append(dict(label='Save52',series='mature',sample_id='SOR-SAMPLE-0029',
                       source=mature[0],expected=pins[0]))
    before = [identity(x['source']) for x in inputs]
    if any(p['sha256'] != x['expected'] for p,x in zip(before,inputs)):
        raise ValueError('SAVE_INPUT_HASH_MISMATCH')
    write(out/'inputs-before.json',dict(saves=before,manifests=manifests,
        static_sources=source['sources'],python=identity(Path(sys.executable)),
        python_version=sys.version,
        scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))
    summary=[]
    human=['series\tlabel\tsaved_token\tbase\tresource\tcreated_item\tdisabled\tdeleted\tcontext_beacon_leads\tlogical_offset']
    for x,pin in zip(inputs,before):
        with decoded_save(x['source'], out/'scratch') as (b,metrics):
            plugins=plugin_tables(b)
            selected=select_records(source['records'],plugins)
            cat=definition_catalog(selected)
            result=inventory(b,cat,plugins)
            # Exact repeat over same primary bytes, independent of output ordering.
            if result != inventory(b,cat,plugins):
                raise ValueError('NONDETERMINISTIC_INVENTORY')
            result.update(label=x['label'],series=x['series'],sample_id=x['sample_id'],
                          source=pin,plugins=plugins,decode=metrics)
        write(out/(x['series']+'-'+x['label']+'.json'),result)
        for obj in result['instances']:
            aa=obj['definition']['associations']
            association=aa[0] if len(aa)==1 else {}
            human.append('\t'.join(str(v) for v in [x['series'],x['label'],obj['token'],
                obj['base_identity'],association.get('resource_identity','UNKNOWN'),
                association.get('item_identity','UNKNOWN'),obj['prefix']['disabled'],
                obj['prefix']['deleted'],','.join(c['beacon_token'] for c in obj['context_leads']),
                obj['offset']]))
        summary.append(dict(label=x['label'],series=x['series'],
            count=len(result['instances']),resource_counts=result['resource_counts'],
            framed_records=result['coverage']['framed_records'],
            unknown=sum(r['definition']['status']!='ASSOCIATED' for r in result['instances']),
            rejected=len(result['rejected']),unresolved_leads=len(result['unresolved_leads'])))
        print(x['label'],summary[-1],flush=True)
    after=[identity(x['source']) for x in inputs]
    if before!=after or manifests!=[identity(Path(m['path'])) for m in manifests]:
        raise ValueError('PROTECTED_INPUT_CHANGED')
    if source['sources'] != [identity(Path(p['path'])) for p in source['sources']]:
        raise ValueError('STATIC_INPUT_CHANGED')
    write(out/'inputs-after.json',dict(saves=after,manifests=manifests,
                                      static_sources=source['sources']))
    write(out/'summary.json',summary)
    with (out/'inventory.txt').open('x',encoding='utf8',newline='\n') as f:
        for s in summary:f.write(json.dumps(s,sort_keys=True)+'\n')
        f.write('\nSave52 per-instance details: mature-Save52.json (LOCAL-ONLY).\n')
    with (out/'instances.tsv').open('x',encoding='utf8',newline='\n') as f:
        f.write('\n'.join(human)+'\n')
    guard()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run',required=True)
    ap.add_argument('--data',type=Path,required=True)
    ap.add_argument('--static',type=Path)
    args=ap.parse_args()
    if not args.run.replace('-','').isalnum():raise ValueError('RUN_NAME')
    run(ROOT/'.local-work/extractor-resource'/args.run,args.data,args.static)


if __name__=='__main__':main()
