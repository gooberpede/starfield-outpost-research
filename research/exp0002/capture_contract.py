# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline capture contract and bounded writer, NOT a game observer.

Only caller-supplied records are accepted. No process access, pointer reads, SDK,
save parsing or query invocation. The future observer must supply qualified
records. Synthetic tests cannot qualify a game ABI or runtime selection method.
"""
from datetime import datetime
import json
import math
import re

from prepare import GAME_HASH, write_report

CHECKPOINTS = ('A0', 'A0C', 'A1', 'A1C', 'A2', 'A2R')
IDENTITY = ('base_form_id', 'reference_form_id', 'pointer', 'handle',
            'location', 'cell', 'worldspace', 'loaded_3d')
DOMAINS = ('reference_xyz', 'rotation', 'cell_local_xyz', 'worldspace_xyz',
           'body_relative_xyz', 'surface_map', 'latitude_longitude')


def field(value=None, status='UNAVAILABLE', source='UNKNOWN'):
    return dict(status=status, value=value, source=source)


def check_field(item):
    if not isinstance(item, dict) or set(item) != {'status', 'value', 'source'}:
        raise ValueError('Field must carry status, value and source')
    if item['status'] not in ('OBSERVED', 'NULL_RESULT', 'UNAVAILABLE', 'NOT_APPLICABLE'):
        raise ValueError('Unknown field status')
    if not isinstance(item['source'], str) or not item['source']:
        raise ValueError('Source required')
    if item['status'] == 'OBSERVED':
        if item['value'] is None or item['source'] == 'UNKNOWN':
            raise ValueError('Observed field needs value and source')
    elif item['value'] is not None:
        raise ValueError('Non-observed field must not contain a value')
    if item['status'] == 'NULL_RESULT' and item['source'] == 'UNKNOWN':
        raise ValueError('Null result needs an actual query source')


def reference(role):
    return dict(role=role, identity={key: field() for key in IDENTITY},
                coordinates={key: dict(**field(), units='UNKNOWN', frame='UNKNOWN') for key in DOMAINS},
                workshop=dict(status='UNAVAILABLE', invocation_utc=None, invocation_order=None,
                              result={key: field() for key in ('reference_form_id', 'pointer', 'handle')}))


def template(checkpoint):
    if checkpoint not in CHECKPOINTS:
        raise ValueError('Unknown checkpoint')
    roles = [] if checkpoint in ('A0', 'A0C') else ['beacon']
    if checkpoint in ('A2', 'A2R'):
        roles.append('storage')
    return dict(schema_version=1, experiment='SOR-EXP-0002', checkpoint=checkpoint,
                kind='PLANNED', utc=None, local_time=None, environment='SOR-ENV-0002',
                executable_sha256=GAME_HASH, module_base=field(), instrumentation_sha256=None,
                module_profile_sha256=None, elapsed_real_seconds=field(), game_time=field(),
                player_state=field(), references=[reference(role) for role in roles],
                terminal='NOT_CAPTURED')


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('Timestamp required')
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError('Timestamp must include offset')


def validate(record):
    expected = template(record.get('checkpoint'))
    if set(record) != set(expected) or record['schema_version'] != 1 or record['experiment'] != 'SOR-EXP-0002':
        raise ValueError('Unexpected contract shape')
    if record['executable_sha256'] != GAME_HASH or record['environment'] != 'SOR-ENV-0002':
        raise ValueError('Wrong baseline')
    if record['kind'] not in ('PLANNED', 'SYNTHETIC', 'RUNTIME'):
        raise ValueError('Invalid evidence kind')
    if record['terminal'] not in ('NOT_CAPTURED', 'RECORD_COMPLETE', 'INCOMPLETE'):
        raise ValueError('Invalid completion state')
    if record['kind'] == 'PLANNED' and record['terminal'] != 'NOT_CAPTURED':
        raise ValueError('Plan is not a capture')
    if record['kind'] != 'PLANNED':
        timestamp(record['utc'])
        timestamp(record['local_time'])
    if record['kind'] == 'RUNTIME':
        for key in ('instrumentation_sha256', 'module_profile_sha256'):
            if not isinstance(record[key], str) or not re.fullmatch('[0-9a-f]{64}', record[key]):
                raise ValueError('Runtime instrumentation/profile identity required')
        if record['module_base']['status'] != 'OBSERVED':
            raise ValueError('Runtime ASLR base required')
    for key in ('module_base', 'elapsed_real_seconds', 'game_time', 'player_state'):
        check_field(record[key])
    roles = [r['role'] for r in expected['references']]
    if [r.get('role') for r in record['references']] != roles:
        raise ValueError('Selected roles missing, duplicated, reordered or excessive')
    for ref in record['references']:
        if set(ref) != {'role', 'identity', 'coordinates', 'workshop'} or set(ref['identity']) != set(IDENTITY):
            raise ValueError('Reference identity shape invalid')
        for key, value in ref['identity'].items():
            check_field(value)
            if value['status'] == 'OBSERVED':
                actual = value['value']
                if key in ('base_form_id', 'reference_form_id', 'handle') and not (isinstance(actual, str) and re.fullmatch('0x[0-9a-fA-F]{8}', actual)):
                    raise ValueError('Identity domain requires 32-bit hex')
                if key == 'pointer' and not (isinstance(actual, str) and re.fullmatch('0x[0-9a-fA-F]{16}', actual)):
                    raise ValueError('Pointer requires 64-bit hex')
                if key == 'loaded_3d' and type(actual) is not bool:
                    raise ValueError('Loaded state must be boolean')
        if set(ref['coordinates']) != set(DOMAINS):
            raise ValueError('Coordinate domains must remain distinct')
        for domain, value in ref['coordinates'].items():
            if set(value) != {'status', 'value', 'source', 'units', 'frame'}:
                raise ValueError('Coordinate provenance missing')
            check_field({k: value[k] for k in ('status', 'value', 'source')})
            if value['status'] == 'OBSERVED':
                vector = value['value']
                size = 2 if domain in ('surface_map', 'latitude_longitude') else 3
                if not isinstance(vector, list) or len(vector) != size or any(type(v) not in (int, float) or not math.isfinite(v) for v in vector):
                    raise ValueError('Invalid coordinate vector')
        query = ref['workshop']
        if set(query) != {'status', 'invocation_utc', 'invocation_order', 'result'} or query['status'] not in ('UNAVAILABLE', 'NULL_RESULT', 'OBSERVED', 'FAILED'):
            raise ValueError('Invalid workshop query')
        if query['status'] != 'UNAVAILABLE':
            timestamp(query['invocation_utc'])
            if type(query['invocation_order']) is not int or query['invocation_order'] < 1:
                raise ValueError('Query order required')
        if set(query['result']) != {'reference_form_id', 'pointer', 'handle'}:
            raise ValueError('Query result domains missing')
        for value in query['result'].values():
            check_field(value)
        if query['status'] in ('UNAVAILABLE', 'FAILED', 'NULL_RESULT') and any(v['status'] == 'OBSERVED' for v in query['result'].values()):
            raise ValueError('Query status contradicts result')
    json.dumps(record, allow_nan=False)


def persist(name, record):
    validate(record)
    # Completion marker is part of one fsynced CREATE_NEW JSON document. A
    # truncated document is never accepted as complete by the JSON reader.
    if len((json.dumps(record, indent=2, allow_nan=False) + '\n').encode()) > 32768:
        raise ValueError('Checkpoint limit 32 KiB')
    if name != ('checkpoint-' + record['checkpoint'].lower() + '.json'):
        raise ValueError('One fixed filename per checkpoint/session directory')
    return write_report(name, record)


def manifest():
    parents = dict(A0='SOR-SAMPLE-0001', A0C='SOR-SAMPLE-EXP0002-A0',
                   A1='SOR-SAMPLE-EXP0002-A0C', A1C='SOR-SAMPLE-EXP0002-A1',
                   A2='SOR-SAMPLE-EXP0002-A1C', A2R='SOR-SAMPLE-EXP0002-A2')
    return dict(schema_version=1, experiment='SOR-EXP-0002', status='PLANNED',
                samples=[dict(sample_id='SOR-SAMPLE-EXP0002-'+cp, logical_checkpoint=cp,
                              parent_sample=parents[cp], actual_filename=None,
                              creation_timestamp=None, size=None, sha256=None,
                              game_build='1.16.244.0 (planned; runtime unverified)',
                              plugin_module_profile=None, player_body_location_state='USER-REPORTED Kreet; verify live',
                              observer_checkpoint_ids=[], operator_actions_since_parent=[],
                              incidental_save_artifacts=[], publication_classification='LOCAL-ONLY',
                              artifact_kind='RUNTIME_CHECKPOINT_ONLY' if cp == 'A2R' else 'PLANNED_MENU_SAVE')
                         for cp in CHECKPOINTS])


if __name__ == '__main__':
    # Templates only: this entry point cannot create runtime evidence.
    write_report('checkpoint-templates.json', [template(cp) for cp in CHECKPOINTS])
    write_report('sample-manifest-template.json', manifest())
