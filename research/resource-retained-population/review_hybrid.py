# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate a completed D5N capture using the owned independent binder.

Reads only task-local journal/SRO1/ACK evidence and the hybrid reducer; writes
one exclusive local report. No target, original evidence, save, installation,
network, analysis or Git changes. Synthetic domain requires --synthetic.
"""
import argparse
import json
from pathlib import Path
import hybrid
import review_capture
from build import LOCAL


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--synthetic', action='store_true')
    args=parser.parse_args()
    folder, output=args.capture.resolve(), args.output.resolve()
    assert folder.is_relative_to(LOCAL) and output.is_relative_to(LOCAL)
    review_capture.reduce=hybrid.reducer().reduce
    report=review_capture.checked(folder, args.synthetic)
    with output.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(report,stream,indent=2);stream.write('\n')
    print(report['receipts'], 'authenticated receipts;', len(report['reduction']['chains']), 'witnessed chains')


if __name__=='__main__':
    main()
