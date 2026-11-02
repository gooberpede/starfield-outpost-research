# SPDX-License-Identifier: GPL-3.0-or-later
"""Restore selected historical extractor receipts into a fresh authenticated lease.

Reads the committed resource archive baseline and owned evidence-access Store;
writes only a fresh local lease and receipt. No saved-game decoding, live target,
cleanup, protected-original mutation or network operation. SOR-P-0002 reuses
research/evidence-access/access.py and its exact-input verification contract.
"""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'research/evidence-access'))
import access

def main():
    if sys.flags.optimize or not __debug__:
        raise RuntimeError('Use Python -E -B')
    baseline = ROOT/'docs/experiments/resources-evidence-consolidation/active-baseline.json'
    b = json.loads(baseline.read_bytes())
    head = __import__('subprocess').check_output(['git','show','HEAD:docs/experiments/resources-evidence-consolidation/active-baseline.json'],cwd=ROOT)
    if json.loads(head) != b:
        raise RuntimeError('Archive baseline differs from HEAD')
    st = access.Store(b['index']['path'], b['index']['sha256'], b['archive_sha256'], b['manifest_sha256'], b['owner'])
    members = ['.local-work/extractor-resource/run05/'+n for n in ('summary.json','mature-Save52.json','manual-S0-S7C-S3.json','manual-S0-S7C-S3C.json','manual-S0-S7C-S7.json','manual-S0-S7C-S7C.json')]
    dest=ROOT/'.local-work/resources-evidence-consolidation/d5ah-extractor-lease01'
    receipt=st.restore(dest,selected=members)
    out=ROOT/'.local-work/d5ah-extractor/restore01.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf8',newline='\n') as f:
        f.write(json.dumps(dict(receipt=receipt,baseline_sha256=access.e.pin(baseline),method_sha256=access.e.pin(__file__),access_sha256=access.e.pin(ROOT/'research/evidence-access/access.py')),indent=2)+'\n')
    print(json.dumps(receipt))
if __name__=='__main__':main()
