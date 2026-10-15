# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only lightweight future 070 health snapshot: own session files, disk,
QUERY_LIMITED_INFORMATION process metadata only. No memory/debugger/target write.
Staleness is a warning, not a deadline or automatic STOP. Full pins use operate.
"""
import argparse
import json
from operate import session_path, process_state
from build import guard

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('session');a=ap.parse_args();p=session_path(a.session)
    identity=json.loads((p/'session.json').read_text(encoding='utf8'))
    if identity.get('version')!='0.7.0' or identity.get('schema')!=7:raise ValueError('session_version')
    values=guard();failure=[]
    for name in ('failure.json','not-ready.json'):
        if (p/name).exists():failure.append(name)
    if (p/'emergency-status.json').exists():
        data=json.loads((p/'emergency-status.json').read_text(encoding='utf8'))
        if data.get('error'):failure.append(data['error'])
    last=None;partial=False
    if (p/'health.jsonl').exists():
        # Bounded suffix read, not a bound on evidence/session growth.
        with (p/'health.jsonl').open('rb') as f:
            f.seek(0,2);n=f.tell();f.seek(max(0,n-65536));lines=f.read().split(b'\n')
        partial=bool(lines[-1])
        for line in reversed(lines[:-1]):
            try:last=json.loads(line);break
            except (ValueError,UnicodeError):continue
    if last and (last.get('integrity_failure') or last.get('failed')):failure.append('worker_integrity_failure')
    state=process_state(identity['pid'],identity['process_creation_filetime'])
    print(json.dumps(dict(status='FAILURE' if failure else 'HEALTH_SNAPSHOT',failure=failure,process_state=state,disk=values,health=last,partial_current_health_line=partial,
        policy='Compare serial progress; slow/missing heartbeat requires investigation, not an arbitrary timer STOP.')))
    return bool(failure)
if __name__=='__main__':raise SystemExit(main())
