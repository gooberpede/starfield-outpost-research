# SPDX-License-Identifier: GPL-3.0-or-later
"""Phase-aware 070 file/control harness. No launch/deploy/debug/save/Git writes.
Reads pinned plans, protected files and session evidence; writes exclusive private
receipts and, only for request/stop, existing observer control protocol files.
Live actions require separate experiment authority. See README.md.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import uuid
from common import fresh, guard, inventory, now, read, sha, tool_pins, verify_pins
import adapter070 as adapter


def saves(root):
    rows = inventory(root)
    for name, row in rows.items():
        row['mtime_ns'] = (Path(root) / name).stat().st_mtime_ns
    return rows


def prelaunch(plan_path, pin):
    plan = read(plan_path, pin)
    if plan['adapter'] != '070' or not any(Path(p).name.lower() == 'sfse_loader.exe' for p in plan['extra_pins']):
        raise ValueError('adapter_or_missing_loader_tool_pins')
    initial_disk = guard()
    if adapter.prelaunch_processes():
        raise ValueError('prelaunch_processes_present')
    m = adapter.full(plan['build'], plan['manifest_sha256'])
    verify_pins(plan['extra_pins'])
    plugins = adapter.deployed(m) if plan['deployed'] else None
    # Reuse the prior process-name inventory; no process opening or memory reads.
    save_inventory = saves(plan['saves'])
    if adapter.prelaunch_processes():
        raise ValueError('prelaunch_processes_present')
    return dict(status='PASS_PRELAUNCH', utc=now(), adapter='070', disk=guard(), initial_disk=initial_disk,
                plan=str(Path(plan_path).resolve()), plan_sha256=pin, plan_data=plan,
                manifest=m, tools=tool_pins(), save_inventory=save_inventory,
                plugin_inventory=plugins, build=str(Path(plan['build']).resolve()),
                existing_sessions=sorted(p.name for p in adapter.ops.LIVE.glob('session-*')),
                scope='FULL_CONTENT_AUDIT; source inventory is manifest protected/sources plus extra_pins and save_inventory')


def reuse(path, pin, full=False):
    r = read(path, pin)
    if r['status'] != 'PASS_PRELAUNCH' or r['adapter'] != '070':
        raise ValueError('prelaunch_receipt_required')
    verify_pins(r['tools'])
    plan = r['plan_data']
    if sha(Path(r['build']) / 'build.json') != plan['manifest_sha256']:
        raise ValueError('build_manifest_changed')
    if full:
        adapter.full(r['build'], plan['manifest_sha256'])
        verify_pins(plan['extra_pins'])
    return r


def save_delta(before, after):
    rotations, violations, metadata = [], [], []
    for name in sorted(before.keys() | after.keys()):
        b, a = before.get(name), after.get(name)
        if b == a:
            continue
        if b and a and (b['sha256'], b['size']) == (a['sha256'], a['size']):
            metadata.append(dict(path=name, before=b, after=a))
            continue
        # Only exact ExitSave prefix is exempt, never arbitrary added/changed saves.
        target = rotations if Path(name).name.lower().startswith('exitsave') else violations
        target.append(dict(path=name, before=before.get(name), after=after.get(name)))
    return dict(exit_save_rotation=rotations, unexpected_changes=violations, metadata_only=metadata,
                note='Content comparison; timestamps do not establish identity. No original is restored or overwritten.')


def bound_request(path, pin, p, s, receipt_pin):
    q = read(path, pin)
    if (q['status'] != 'ACK_REQUESTED' or q['session'] != str(p) or q['identity'] != s
            or q['prelaunch_sha256'] != receipt_pin or not re.fullmatch('[0-9a-f]{32}', q['nonce'])):
        raise ValueError('request_receipt_mismatch')
    if (p / ('control-' + q['nonce'] + '.request')).read_bytes() != b'ACK\n':
        raise ValueError('request_file_changed')
    return q


def action(kind, receipt, pin, session, request=None, request_pin=None):
    # STOP deliberately bypasses disk/full/deployed audits so it remains usable
    # on integrity incidents; the hash-bound own-session identity is still required.
    r = reuse(receipt, pin)
    p, s = adapter.session(session, r['manifest'])
    if p.name in r['existing_sessions']:
        raise ValueError('preexisting_session_not_this_run')
    result = dict(action=kind, utc=now(), prelaunch_sha256=pin, session=str(p), identity=s)
    if kind == 'stop':
        result['status'] = adapter.ops.stop_control(p)
        return result
    result['disk'] = guard()
    state = adapter.process(s)
    result['process_state'] = state
    if kind == 'postflight':
        if state not in ('GONE', 'EXITED', 'ORIGINAL_GONE_PID_REUSED'):
            raise ValueError('original_process_not_confirmed_gone')
        protection_errors = []
        try:
            reuse(receipt, pin, full=True)
        except Exception as exc:
            protection_errors.append(repr(exc))
        try:
            adapter.deployed(r['manifest'], False)
            for path in r['plan_data'].get('removal_paths', []):
                if Path(path).exists():
                    raise ValueError('effective_observer_remnant: ' + path)
        except Exception as exc:
            protection_errors.append(repr(exc))
        changes = save_delta(r['save_inventory'], saves(r['plan_data']['saves']))
        try:
            report = adapter.inspect(p)
        except Exception as exc:
            report = dict(status='DECODER_ERROR_PRESERVE_RAW', error=repr(exc))
        result.update(save_changes=changes, inspection=report, protection_errors=protection_errors,
                      status='PASS_POSTFLIGHT' if not protection_errors and not changes['unexpected_changes'] and report['status'] == 'RETIRED_INTEGRITY_OK'
                      else 'PARTIAL_POSTFLIGHT')
        return result
    if state != 'ACTIVE':
        raise ValueError('live_process_not_active: ' + state)
    result['plugin_inventory'] = adapter.deployed(r['manifest'])
    if kind == 'request':
        nonce = uuid.uuid4().hex
        # Nonce must never already have an ACK; receipt binds session and audit.
        if (p / ('ack-' + nonce + '.json')).exists():
            raise ValueError('ack_already_exists')
        with (p / ('control-' + nonce + '.request')).open('xb') as f:
            f.write(b'ACK\n')
            f.flush()
            __import__('os').fsync(f.fileno())
        result.update(status='ACK_REQUESTED', nonce=nonce)
    else:
        q = bound_request(request, request_pin, p, s, pin) if request else None
        result.update(adapter.status(p, r['manifest'], s, q))
    return result


def main():
    if sys.flags.optimize:
        raise RuntimeError('optimized_Python_would_disable_observer_assertions')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action', choices=['prelaunch', 'reuse-full', 'request', 'live', 'stop', 'postflight'])
    ap.add_argument('--input', type=Path, required=True, help='plan for prelaunch, otherwise prelaunch receipt')
    ap.add_argument('--sha256', required=True)
    ap.add_argument('--session', type=Path)
    ap.add_argument('--request', type=Path)
    ap.add_argument('--request-sha256')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        ap.error('receipt exists; choose a fresh output')
    try:
        if a.action == 'prelaunch':
            result = prelaunch(a.input, a.sha256)
        elif a.action == 'reuse-full':
            r = reuse(a.input, a.sha256, full=True)
            guard()
            delta = save_delta(r['save_inventory'], saves(r['plan_data']['saves']))
            if delta['unexpected_changes']:
                raise ValueError('protected_save_inventory_changed')
            result = dict(status='PASS_FULL_REUSE', prelaunch_sha256=a.sha256, save_changes=delta)
        else:
            if not a.session or bool(a.request) != bool(a.request_sha256):
                ap.error('session and paired request/hash required')
            result = action(a.action, a.input, a.sha256, a.session, a.request, a.request_sha256)
    except Exception as exc:
        result = dict(status='CHECK_ERROR', action=a.action, utc=now(), error=type(exc).__name__ + ': ' + str(exc))
        fresh(a.out, result)
        print(json.dumps(result))
        return 1
    fresh(a.out, result)
    print(json.dumps({k: result[k] for k in ('status', 'nonce', 'process_state') if k in result}))
    return int(result['status'] in ('WORKER_FAILURE', 'RETIREMENT_ERROR', 'PARTIAL_POSTFLIGHT'))


if __name__ == '__main__':
    sys.exit(main())
