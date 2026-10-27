# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent-custodian freeze/reveal file bridge, CPython stdlib only.

Reads a flat provisioned bundle and independently supplied expected digests.
Writes new registry/trial directories exclusively. No overwrite, backdated
client time, trial reuse, network or target effect. Registry ACL/custody must
exclude the predictor; this is not tamper-proof against its custodian/admin.
All files and the registered protocol are reauthenticated before revelation.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import time
from bridge import loads, exact, hexword
from compare import validate_prediction, validate_truth, compare

METHODS = ('bridge.py', 'compare.py', 'gate.py', 'truth.py', 'predict.py', 'conditional.py', 'saved_adapter.py',
           'AppContainer.cs', 'boundary.ps1')
POLICY_FILES = dict(eligibility='eligibility.json', transforms='transforms.json',
    comparison='compare.py', collector='collector.json', inputs='inputs.json',
    corpus='corpus.json', dependencies='dependencies.json', methods='gate.py')
ROOT = Path(__file__).resolve().parents[2]
OWNED = {'geometry.py': ROOT/'research/resource-geometry/geometry.py',
    'context.py': ROOT/'research/resource-geometry/context.py',
    'resource_spatial.py': ROOT/'save-analysis/scripts/resource_spatial.py',
    'resource_availability.py': ROOT/'save-analysis/scripts/resource_availability.py',
    'consumer.py': ROOT/'research/resource-combined-acquisition/consumer.py'}
for _name in ('durable_position_v2', 'durable_position_model', 'audit_activated_grid',
              'beacon_terrain_projection', 'planet_world_key'):
    OWNED[_name+'.py'] = ROOT/('save-analysis/scripts/'+_name+'.py')
# Close static sibling imports of the unchanged custodian-side save modules.
# This binds their source bytes without importing or executing their utilities.
_queue = list(OWNED.values())
_visited = set()
while _queue:
    _source = _queue.pop()
    if _source in _visited:
        continue
    _visited.add(_source)
    for _node in ast.walk(ast.parse(_source.read_text(encoding='utf8'))):
        _names = ([n.name.split('.')[0] for n in _node.names] if isinstance(_node, ast.Import)
            else [_node.module.split('.')[0]] if isinstance(_node, ast.ImportFrom) and _node.module and not _node.level else [])
        for _name in _names:
            _path = _source.with_name(_name+'.py')
            if _path.is_file() and _path not in _visited:
                if _path.name in OWNED and OWNED[_path.name] != _path:
                    raise ValueError('AMBIGUOUS_OWNED_DEPENDENCY')
                OWNED[_path.name] = _path
                _queue.append(_path)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf8') + b'\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def clean(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.is_symlink() or part.is_junction():
            raise ValueError('REPARSE_PATH')
    return path


def write(path, data):
    with clean(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def files(bundle):
    bundle = clean(bundle)
    out = {}
    for p in bundle.iterdir():
        clean(p)
        if not p.is_file() or re.fullmatch(r'[a-zA-Z0-9_-]+\.(json|py|cs|ps1|md|dll|exe|pyd|txt)', p.name) is None:
            raise ValueError('NONFLAT_OR_UNSAFE_BUNDLE')
        out[p.name] = digest(p.read_bytes())
    if not {'prediction.json', 'protocol.json'} <= out.keys():
        raise ValueError('MISSING_FREEZE_INPUT')
    return out


def verify_methods(inventory):
    for name in METHODS:
        if inventory.get(name) != digest(Path(__file__).with_name(name).read_bytes()):
            raise ValueError('TOOL_VERSION_CHANGED_OR_UNREGISTERED')
    for name, source in OWNED.items():
        if inventory.get(name) != digest(source.read_bytes()):
            raise ValueError('TRANSITIVE_METHOD_CHANGED_OR_UNREGISTERED')


def verify_dependencies(bundle, inventory, prediction):
    dep = loads((bundle/'dependencies.json').read_bytes())
    exact(dep, 'schema kind worker worker_sha256 modules runtime_root runtime_manifest_sha256')
    if dep['schema'] != 'sor-blind-dependencies/1' or dep['kind'] not in ('SYNTHETIC', 'APP_CONTAINER'):
        raise ValueError('DEPENDENCY_SCHEMA')
    if dep['worker'] != 'worker.py' or inventory.get('worker.py') != dep['worker_sha256']:
        raise ValueError('UNBOUND_WORKER')
    if dep['modules'] != {n: inventory[n] for n in OWNED}:
        raise ValueError('UNBOUND_TRANSITIVE_MODULES')
    if inventory.get('runtime-manifest.json') != dep['runtime_manifest_sha256']:
        raise ValueError('UNBOUND_RUNTIME_MANIFEST')
    if dep['kind'] == 'SYNTHETIC':
        if prediction.get('body') != 'SYNTHETIC':
            raise ValueError('SYNTHETIC_NOT_PROSPECTIVE')
    elif (inventory['worker.py'] != inventory['predict.py'] or prediction.get('schema') != 'sor-blind-prediction/1'):
        raise ValueError('UNQUALIFIED_PREDICTION_RUNNER')
    runtime = clean(dep['runtime_root'])
    if not runtime.is_relative_to(ROOT/'.local-work/blinded-outpost-validation'):
        raise ValueError('RUNTIME_OUTSIDE_PROVISIONED_AREA')
    manifest = loads((bundle/'runtime-manifest.json').read_bytes())
    if type(manifest) is not dict or not manifest:
        raise ValueError('EMPTY_RUNTIME')
    actual = {}
    for p in runtime.rglob('*'):
        clean(p)
        if p.is_file():
            actual[p.relative_to(runtime).as_posix()] = digest(p.read_bytes())
    if actual != manifest:
        raise ValueError('RUNTIME_BYTES_CHANGED')


def freeze(registry, bundle, trial, participants, expected_inventory):
    hexword(trial, 32)
    hexword(expected_inventory, 64)
    if participants != ['location_custodian', 'prediction_runner', 'revelation_custodian', 'independent_gate', 'comparator']:
        raise ValueError('PARTICIPANT_ROLES')
    registry, bundle = clean(registry), clean(bundle)
    inventory = files(bundle)
    verify_methods(inventory)
    if digest(canonical(inventory)) != expected_inventory:
        raise ValueError('INDEPENDENT_INVENTORY_MISMATCH')
    prediction = loads((bundle/'prediction.json').read_bytes())
    validate_prediction(prediction)
    verify_dependencies(bundle, inventory, prediction)
    if prediction['trial'] != trial:
        raise ValueError('TRIAL_MISMATCH')
    protocol = loads((bundle/'protocol.json').read_bytes())
    exact(protocol, 'schema eligibility transforms comparison collector inputs corpus dependencies methods')
    if protocol['schema'] != 'sor-blind-protocol/1':
        raise ValueError('PROTOCOL_VERSION')
    # Every protocol category binds an exact file/hash, not mutable prose paths.
    for category in set(protocol) - {'schema'}:
        if type(protocol[category]) is not dict or not protocol[category]:
            raise ValueError('PROTOCOL_BINDING')
        if POLICY_FILES[category] not in protocol[category]:
            raise ValueError('MISSING_REQUIRED_PROTOCOL_CATEGORY')
        for name, expected in protocol[category].items():
            if name not in inventory or inventory[name] != expected or name in ('prediction.json', 'protocol.json'):
                raise ValueError('UNBOUND_PROTOCOL_DEPENDENCY')
    trialdir = registry/trial
    trialdir.mkdir()  # Atomic refusal of repeat/refreeze, including old failures.
    (trialdir/'bundle').mkdir()
    for name, expected in inventory.items():
        data = (bundle/name).read_bytes()
        if digest(data) != expected:
            raise ValueError('FREEZE_RACE')
        write(trialdir/'bundle'/name, data)
    if files(bundle) != inventory:
        raise ValueError('FREEZE_RACE')
    record = dict(schema='sor-blind-freeze/1', trial=trial, time_ns=time.time_ns(),
        participants=participants, files=inventory, inventory_sha256=expected_inventory)
    write(trialdir/'freeze.json', canonical(record))
    return digest(canonical(record))


def reveal(registry, bundle, trial, freeze_hash, truth_path, truth_hash):
    hexword(trial, 32)
    hexword(freeze_hash, 64)
    hexword(truth_hash, 64)
    trialdir, bundle = clean(Path(registry)/trial), clean(bundle)
    raw = (trialdir/'freeze.json').read_bytes()
    if digest(raw) != freeze_hash:
        raise ValueError('INDEPENDENT_FREEZE_MISMATCH')
    frozen = loads(raw)
    verify_methods(frozen['files'])
    if frozen['trial'] != trial or files(bundle) != frozen['files'] or files(trialdir/'bundle') != frozen['files']:
        raise ValueError('FROZEN_BYTES_CHANGED')
    # The truth hash must come from the independent revelation custodian.
    # A self-supplied hash proves byte equality only, not native authenticity.
    truthraw = clean(truth_path).read_bytes()
    if digest(truthraw) != truth_hash:
        raise ValueError('INDEPENDENT_TRUTH_MISMATCH')
    truth = validate_truth(loads(truthraw))
    prediction = validate_prediction(loads((bundle/'prediction.json').read_bytes()))
    verify_dependencies(bundle, frozen['files'], prediction)
    result = compare(prediction, truth)
    record = dict(schema='sor-blind-revelation/1', trial=trial, time_ns=time.time_ns(),
        freeze_sha256=freeze_hash, truth_sha256=truth_hash, comparison=result)
    if record['time_ns'] < frozen['time_ns']:
        raise ValueError('CLOCK_ROLLBACK')
    # Reserve reveal first. A crash leaves an incomplete trial, never a retry
    # which silently replaces a known prediction or outcome.
    (trialdir/'revelation').mkdir()
    write(trialdir/'revelation/truth.json', truthraw)
    write(trialdir/'revelation/result.json', canonical(record))
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('inventory', 'freeze', 'reveal'))
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--registry', type=Path)
    parser.add_argument('--trial')
    parser.add_argument('--inventory-hash')
    parser.add_argument('--freeze-hash')
    parser.add_argument('--truth', type=Path)
    parser.add_argument('--truth-hash')
    args = parser.parse_args()
    if args.operation == 'inventory':
        result = dict(files=files(args.bundle), inventory_sha256=digest(canonical(files(args.bundle))))
    elif args.operation == 'freeze':
        result = freeze(args.registry, args.bundle, args.trial,
            ['location_custodian', 'prediction_runner', 'revelation_custodian', 'independent_gate', 'comparator'], args.inventory_hash)
    else:
        result = reveal(args.registry, args.bundle, args.trial, args.freeze_hash, args.truth, args.truth_hash)
    print(json.dumps(result, sort_keys=True, allow_nan=False))
