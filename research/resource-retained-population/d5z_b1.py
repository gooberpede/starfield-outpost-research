# SPDX-License-Identifier: GPL-3.0-or-later
"""Re-evaluate B1 reset certificates and the pre-travel prefix offline.

Reads the original raw B1 capture, frozen owned decoder and a fresh authenticated
D5Y forensic result. Writes one fresh ignored receipt and a small review
aggregate. Stdlib only; no game, save, native execution, database or Git writes.
Run d5y_forensics.py with a fresh label first. Raw pointers stay local.
"""
from collections import Counter
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SESSION = ROOT / '.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def main():
    source, out = (Path(s).resolve() for s in sys.argv[1:])
    assert source.is_relative_to(ROOT/'.local-work')
    assert out.is_relative_to(ROOT/'.local-work') and not out.exists()
    analysis = json.loads((source/'analysis.json').read_text())
    raw = SESSION/'events.bin'
    assert sha(raw) == analysis['raw_sha256'] == 'cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c'
    module_path = ROOT/'runtime/construction-winner/read_capture.py'
    spec = importlib.util.spec_from_file_location('owned_d5z_reader', module_path)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    content = raw.read_bytes()
    events = [reader.decode(content[i+16:i+328]) for i in range(0,len(content),328)]
    assert len(events) == analysis['authenticated_records'] == 19780
    resets, anchors, certificates, details = {}, {}, [], []
    for event in events:
        kind, proc = event['kind'], event['proc']
        if kind == 10 and event['a'] == 0:
            resets[proc] = event
        if kind == 12:
            begin = resets.get(proc)
            if begin and not event['status'] and event['hazards'] == 1 and begin['epoch'] == event['epoch']:
                anchors[proc] = event
        if kind == 11 and event['a'] == 0:
            anchor = anchors.pop(proc, None)
            if anchor and not event['status'] and not event['hazards'] and anchor['epoch'] == event['epoch']:
                certificates.append(dict(begin=resets[proc]['sequence'],unlock=anchor['sequence'],end=event['sequence'],epoch=event['epoch']))
            resets.pop(proc, None)
        if kind == 12 or kind in (10,11) and event['a'] == 0:
            details.append(event)
    ack_path = SESSION/'ack-8d85d0bf7dcbd78c5ca21407d2195151.json'
    assert sha(ack_path) == analysis['input_hashes'][str(ack_path)]
    ack = json.loads(ack_path.read_text())
    assert ack['request_nonce'] == '8d85d0bf7dcbd78c5ca21407d2195151'
    assert ack['capture_active'] and ack['hooks_intact'] and ack['drops'] == 0
    prefix = events[:ack['acknowledged']]
    spatial = json.loads((source/'spatial-controls.json').read_text())
    with (source/'conditional-target.csv').open(encoding='utf8',newline='') as stream:
        conditional = list(csv.DictReader(stream))
    bypasses = sum(row['bypass']=='True' for row in conditional)
    assert bypasses == spatial['conditional_singleton_bypasses']
    for row in conditional:
        selected, visited = (events[int(row[k])-1] for k in ('selection_sequence','visited_sequence'))
        assert selected['kind'] == 2 and visited['kind'] == 3 and visited['a'] == 1
        assert selected['epoch'] == visited['epoch'] == int(row['epoch'])
        assert selected['invocation'] == visited['invocation'] and selected['selection'] == visited['selection']
    frequency = analysis['qpc_frequency']
    aggregate = dict(schema='sor-d5z-b1/1',raw_sha256=sha(raw),forensics_sha256=sha(source/'analysis.json'),
        records=len(events),reset_begin=sum(e['kind']==10 and e['a']==0 for e in events),
        reset_end=sum(e['kind']==11 and e['a']==0 for e in events),unlock_records=sum(e['kind']==12 for e in events),
        matched_certificates=certificates,pretravel_records=ack['acknowledged'],pretravel_ack_sha256=sha(ack_path),pretravel_kinds=dict(Counter(reader.KINDS[e['kind']] for e in prefix)),
        prefix_last_sequence=prefix[-1]['sequence'],prefix_last_second=(prefix[-1]['ticks']-analysis['t0'])/frequency,
        conditional_target_bypasses=bypasses,conditional_csv_sha256=sha(source/'conditional-target.csv'),target_copied_records=analysis['target_positive_records'],
        first_loss_sampled_admission=analysis['terminal']['first_loss_sampled_admission'],
        reader_qualified_chains=len(json.loads((source/'cold-reader.json').read_text())['chains']),
        limit='Certificates establish empty stores at a matched reset boundary only; no continuous target history to later conditional bypass epochs.')
    out.mkdir(parents=True)
    (out/'private-reset-events.json').write_text(json.dumps(details,indent=2)+'\n',encoding='utf8',newline='\n')
    (out/'b1.json').write_text(json.dumps(aggregate,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(aggregate,indent=2))

if __name__ == '__main__':
    main()
