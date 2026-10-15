# SPDX-License-Identifier: GPL-3.0-or-later
"""Future approved operator observation marker. Reads session identity, hashes
optional local screenshot; writes one exclusive private marker in validated 070
session. Never captures screen, contacts target, alters evidence/save/config/Git.
Stdlib and owned session-path validator only."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import time
import uuid
from operate import session_path, fresh

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('session');ap.add_argument('--phase',required=True);ap.add_argument('--labels',nargs='*');ap.add_argument('--screenshot',type=Path);a=ap.parse_args()
    p=session_path(a.session);s=json.loads((p/'session.json').read_text())
    if s.get('version')!='0.7.0' or s.get('schema')!=7:raise ValueError('wrong_session')
    value=dict(session_identity=s,phase=a.phase,reported_labels=a.labels,
        receipt_utc=datetime.datetime.now(datetime.UTC).isoformat(),receipt_monotonic_ns=time.perf_counter_ns(),
        timing='OPERATOR_REPORT_RECEIPT_NOT_EXACT_RENDER_TIME',native_pairing='PHASE_INTERVAL_CANDIDATES_NOT_NEAREST_EVENT')
    if a.screenshot:
        with a.screenshot.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
        value['screenshot']=dict(path=str(a.screenshot.resolve()),sha256=h)
    out=p/('operator-'+uuid.uuid4().hex+'.json');fresh(out,value);print(out)
if __name__=='__main__':main()
