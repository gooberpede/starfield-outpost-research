"""SPDX-License-Identifier: GPL-3.0-or-later
Read hash-qualified existing extractor trial archives; write a NEW ignored run.
No game/save/database/network changes. Stdlib/project only, decoder scratch
removed, both C:/D: 40-billion-byte guard retained. Bulk outputs LOCAL-ONLY.
"""
import argparse
import csv
import json
from pathlib import Path
from inventory_historical_saves import ROOT, identity, guard
from stream_save import decoded_save
from workshop_inventory import audit, ownership_ledger, constructed_inventory
from test_outpost_record_framing import independent
from validate_mature_outposts import directory


def write(p, data):
    with p.open('x', encoding='utf8', newline='\n') as f:
        json.dump(data, f, sort_keys=True, indent=2)
        f.write('\n')


def csv_rows(p, rows, columns):
    with p.open('x',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore',lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({k:json.dumps(row.get(k),sort_keys=True) if isinstance(row.get(k),(dict,list))
                else row.get(k) for k in columns})


def run(out, labels, context_path=None, extra_inputs=None):
    guard()
    out.mkdir(parents=True, exist_ok=False)
    context = json.loads(context_path.read_text(encoding='utf8')) if context_path else None
    context_pin = identity(context_path) if context_path else None
    if context:
        if context['schema']!='workshop-definition-context/1': raise ValueError('CONTEXT_SCHEMA')
        for pin in context['sources']:
            if identity(Path(pin['path']))!=pin: raise ValueError('CONTEXT_PIN_CHANGED')
    prior = ROOT/'.local-work/extractor-resource/run05'
    inputs = []
    for p in sorted(prior.glob('*.json')):
        x = json.loads(p.read_text(encoding='utf8'))
        if not isinstance(x, dict) or 'instances' not in x: continue
        if labels and x['label'] not in labels: continue
        inputs.append(dict(label=x['label'], series=x['series'], pin=x['source']))
    inputs += extra_inputs or []
    if not inputs: raise ValueError('NO_INPUTS')
    for x in inputs:
        if not all(isinstance(x[k],str) and x[k].isascii() and x[k].replace('-','').isalnum()
                   for k in ('label','series')): raise ValueError('INPUT_LABEL_OR_SERIES')
    if len({(x['series'],x['label']) for x in inputs})!=len(inputs): raise ValueError('DUPLICATE_INPUT_LABEL')
    before = [identity(Path(x['pin']['path'])) for x in inputs]
    if before != [x['pin'] for x in inputs]: raise ValueError('INPUT_PIN_MISMATCH')
    write(out/'before.json', before)
    summaries = []
    for x in inputs:
        guard()
        with decoded_save(Path(x['pin']['path']), out/'scratch') as (b, metrics):
            raw=audit(b)
            d=directory(b)
            arithmetic=independent(b,*d['regions']['region_R3'],d['words'][9])
            if [(r['offset'],r['end'],r['token'],r['change_flags']) for r in raw['records']]!=[
                r[:4] for r in arithmetic]: raise ValueError('INDEPENDENT_RECORD_WALK_MISMATCH')
            result = constructed_inventory(ownership_ledger(raw, context),context)
            # Repeat detection against primary bytes, not a previous JSON summary.
            if result != constructed_inventory(ownership_ledger(audit(b), context),context): raise ValueError('NONDETERMINISTIC')
        result.update(source=x['pin'], label=x['label'], series=x['series'], decode=metrics)
        write(out/(x['series']+'-'+x['label']+'.json'), result)
        stem=x['series']+'-'+x['label']
        csv_rows(out/(stem+'-roots.csv'),result['constructed_instances'],[
            'instance_identity','instance_token','owner_identity','base_identity','construction_definition',
            'root_kind','editor_name','record_offset','record_end','record_type','raw_position',
            'saved_form_flags','saved_aux_flags','saved_disabled','saved_deleted_bit',
            'association_status','reason','member_identities','member_offsets'])
        csv_rows(out/(stem+'-roles.csv'),result['member_roles'],[
            'reference_identity','token','offset','owner_identity','role','reason','root_identity','group_identity'])
        csv_rows(out/(stem+'-unresolved.csv'),result['unresolved_population'],[
            'saved_reference','token','offset','end','explicit_type','base_identity','reason','queued_workshop_keyword'])
        summaries.append(dict(label=x['label'], series=x['series'], coverage=result['coverage']))
        print(summaries[-1], flush=True)
    after = [identity(Path(x['pin']['path'])) for x in inputs]
    write(out/'after.json', after)
    if before != after: raise ValueError('PROTECTED_INPUT_CHANGED')
    if context and any(identity(Path(pin['path']))!=pin for pin in context['sources']):
        raise ValueError('CONTEXT_SOURCE_CHANGED_DURING_RUN')
    if context_pin and identity(context_path)!=context_pin: raise ValueError('CONTEXT_CHANGED_DURING_RUN')
    write(out/'summary.json', summaries)
    write(out/'reproduction.json', dict(context=context_pin, inputs=inputs,
        scripts=[identity(Path(__file__).parent/name) for name in [
            'research_workshop_inventory.py','workshop_inventory.py','workshop_definition_context.py',
            'outpost_record_framing.py','outpost_membership.py','stream_save.py',
            'extractor_resources.py','validate_mature_outposts.py']],
        deterministic=True, independent_record_walk=True,scientific_completeness=False))
    guard()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--labels', nargs='*')
    ap.add_argument('--context', type=Path)
    ap.add_argument('--save', type=Path)
    ap.add_argument('--sha256')
    ap.add_argument('--manifest',type=Path,help='Qualified label/series/pin input list; excludes default corpus')
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
    if bool(args.save)!=bool(args.sha256): raise ValueError('SAVE_REQUIRES_SHA256')
    if args.manifest:
        if args.save or args.sha256 or args.labels: raise ValueError('MANIFEST_EXCLUSIVE')
        run(ROOT/'.local-work/workshop-inventory'/args.run,['__MANIFEST_ONLY__'],args.context,
            json.loads(args.manifest.read_text(encoding='utf8')))
    elif args.save:
        # Explicit qualified save mode never adds the default corpus.
        pin=identity(args.save)
        if pin['sha256']!=args.sha256: raise ValueError('QUALIFIED_SAVE_HASH_MISMATCH')
        extra=[dict(label='input',series='explicit',pin=pin)]
        run(ROOT/'.local-work/workshop-inventory'/args.run, ['__EXPLICIT_ONLY__'], args.context,extra)
    else:
        run(ROOT/'.local-work/workshop-inventory'/args.run, args.labels,args.context)
