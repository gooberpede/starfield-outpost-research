"""Offline-only adaptation; provenance in PROVENANCE.md. No process control."""
import json
from pathlib import Path
from lifecycle_checks import survival_failures


def read_rows(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON field')
            result[key] = value
        return result
    return [json.loads(line, object_pairs_hook=unique) for line in Path(path).read_text(encoding='utf-8').splitlines()]


def validate(rows):
    errors = []
    def kind(name):
        return [x for x in rows if x['kind'] == name]
    if len(kind('config')) != 1 or len(kind('identity')) != 1:
        return dict(passed=False, errors=['Missing unique config/identity'], survival=[])
    config, identity = kind('config')[0], kind('identity')[0]['data']
    workers = set(identity['workers'])
    if len(workers) != config['workers']:
        errors.append('Worker identity mismatch')
    if any(kind(k) for k in ('error','failure','emergency_detach','cleanup_failed')):
        errors.append('Native error or emergency cleanup')
    if len(kind('complete')) != 1 or not kind('complete')[0]['success']:
        errors.append('Missing native completion')
    if len(kind('detached')) != 1 or len(kind('quiescent')) != config['stages']:
        errors.append('Incomplete retirement/detach')
    captures = kind('capture')
    if [x['hit'] for x in captures] != list(range(1,25)):
        errors.append('Incomplete ordered captures')
    sites = [int(x,16) for x in identity['sites']]
    for r in captures:
        if (r['stage'] >= config['stages'] or int(r['rip'],16) != sites[r['stage']]
                or r['tid'] not in workers or (config['filter'] and r['tid'] != identity['workers'][0])):
            errors.append('Capture identity/filter/site mismatch')
        if int(r['eflags'],16)&0x100 or not int(r['dr6'],16)&1:
            errors.append('Capture not owned hardware event')
        if (len(r['stack_bytes']) != 128 or len(r['argument_memory']) != 16
                or not 2 <= len(r['stack']) <= 8 or int(r['stack'][0]['pc'],16) != int(r['rip'],16)):
            errors.append('Missing bounded memory/stack evidence')
    originals = {x['address']: x['bytes'] for x in kind('original')}
    if len(originals) != 3:
        errors.append('Missing original-byte coverage')
    if len(kind('bytes')) != config['stages']*6 or any(x['bytes'] != originals.get(x['address']) for x in kind('bytes')):
        errors.append('Changed/missing physical bytes')
    contexts = kind('context')
    for boundary in ('initial','armed','before_retirement','retired','quiescent'):
        if not workers <= {x['tid'] for x in contexts if x['boundary'] == boundary}:
            errors.append('Missing per-worker contexts: '+boundary)
    initial = {x['tid']: x for x in contexts if x['boundary']=='initial'}
    for r in contexts:
        if int(r['eflags'],16)&0x100:
            errors.append('Unexpected TF')
        if r['boundary'] in ('retired','quiescent') and (r['dr0'],r['dr7']) != (initial[r['tid']]['dr0'],initial[r['tid']]['dr7']):
            errors.append('Debug registers not restored')
    balances = {}
    for r in rows:
        k = r['kind']
        if k in ('suspend','pending_resuspend','resume','pending_release'):
            delta = 1 if k in ('suspend','pending_resuspend') else -1
            if r['previous'] != (0 if delta == 1 else 1):
                errors.append('Unexpected suspend count')
            balances[r['tid']] = balances.get(r['tid'],0) + delta
            if balances[r['tid']] not in (0,1):
                errors.append('Unbalanced suspension history')
    if any(balances.values()):
        errors.append('Residual owned suspension')
    survival = []
    for r in kind('survival'):
        logs = [json.loads(line) for line in r['target_log'].splitlines()]
        beats = [x for x in logs if 'heartbeat' in x]
        survival.append(dict(delay=r['delay'], alive=r['alive'], exit_code=r['exit_code'],
                             heartbeat=beats[-1] if beats else None,
                             exceptions=[x for x in logs if 'exception' in x]))
    errors.extend(survival_failures(survival, config['workers']))
    if len(kind('shutdown')) != 1 or kind('shutdown')[0]['wait'] != 0 or kind('shutdown')[0]['exit_code'] != 0:
        errors.append('No clean cooperative exit')
    return dict(passed=not errors, errors=sorted(set(errors)), survival=survival,
                config=config, identity=identity, captures=len(captures),
                pending_events=sum(x['boundary']=='owned_pending_event' for x in contexts),
                pending_releases=len(kind('pending_release')), byte_checks=len(kind('bytes')))
