# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently bind a native event journal to every durable SRO1/ACK before reduction.

Reads task-local evidence and owned decoders; writes one fresh task-local report.
No target, original evidence, save, analysis, network or Git effects. Synthetic
domain requires an explicit flag and cannot become retail evidence.
"""
import argparse
import json
from pathlib import Path
from build import LOCAL,pin
from native_reduce import reduce
from prepare_native import EXE
from qualify import decoder


def checked(folder,synthetic):
    rows=[json.loads(s) for s in (folder/'events.jsonl').read_text().splitlines()]
    session=next(r for r in rows if r['kind']=='SESSION');assert session['synthetic'] is synthetic
    events=[r for r in rows if r['kind'] in ('SAMPLE','ARM_BARRIER')];files=sorted(folder.glob('capture-*.bin'))
    assert len(files)==len(events)
    for path,event in zip(files,events):
        payload=decoder.independent(path);assert len(payload)==3
        header=dict(payload[0]);header.pop('admission_sha256',None)
        assert header==session and payload[1]==dict(kind='SAMPLE',event=event)
        assert payload[2]==dict(kind='END',complete=event.get('read_complete',True))
        ack=json.loads(path.with_suffix('.ack.json').read_text())
        assert ack==dict(bytes=path.stat().st_size,sha256=pin(path),records=3,synthetic=synthetic,status='DURABLE_READBACK')
    return dict(receipts=len(files),journal_sha256=pin(folder/'events.jsonl'),
        reduction=reduce(rows,session['image_sha256'] if synthetic else EXE,synthetic))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--synthetic',action='store_true');a=p.parse_args()
    folder,output=a.capture.resolve(),a.output.resolve();assert folder.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    report=checked(folder,a.synthetic)
    with output.open('x',encoding='utf8') as s:json.dump(report,s,indent=2);s.write('\n')
    print(report['receipts'],'receipts and ACKs independently bound',len(report['reduction']['chains']),'bounded chains')
