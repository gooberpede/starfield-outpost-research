# SPDX-License-Identifier: GPL-3.0-or-later
"""Check D5T receipts/derivatives, optionally replay the disposable native method.

Reads local evidence, installed/database pins, source records and authored maps.
Writes only a new ignored JSON receipt and optional new ignored replay directory.
Replay copies owned fixture support and existing function exports, then executes
the tracked native harness in a separate Python process. No game, attachment,
save, installed write, Ghidra mutation, network, dependency install or Git write.
Requires retained local evidence; missing input fails without downloading it.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT/'.local-work/d5t'
DOC = ROOT/'docs/experiments/resource-retained-population/d5t'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def free():
    values = {drive:shutil.disk_usage(drive).free for drive in ('C:/','D:/')}
    assert min(values.values()) >= 40_000_000_000, values
    return values


def check():
    initial = read(LOCAL/'initial.json')
    for category in ('installed','database'):
        assert {p:sha(p) for p in initial[category]} == initial[category], category
    native = read(LOCAL/'native-full05.json')
    assert native['code_sha256'] == sha(Path(__file__).with_name('d5t_native.py'))
    assert not native['errors'] and native['key_calls'] == 1296
    assert all(len(r['calls']) == 432 for r in native['runs'])
    assert native['runs'][1]['regions'] == native['runs'][2]['regions']
    assert len(native['spatial_checks']) == 1630
    assert all(r['native'] == r['planar'] for r in native['spatial_checks'])
    assert [r['regions'] for r in native['model_comparisons']] == [74,78]
    fresh = read(LOCAL/'winner-candidates05.json')
    old = read(LOCAL/'winner-candidates03.json')
    assert fresh['global_fifo_raster_census'] == old['global_fifo_raster_census']
    queries = read(LOCAL/'native-queries05.json')['rows']
    assert len(queries)==196
    assert all(r['converted_face_cell']==[37536+r['original_int2'][0],20928+r['original_int2'][1]] for r in queries)
    rows = list(csv.DictReader((DOC/'candidates.csv').open(encoding='utf8')))
    assert len(rows)==196 and sum(r['feasibility'].startswith('PROVEN') for r in rows)==2
    assert sum(r['mask']=='0' for r in rows)==28 and sum(r['mask']=='3' for r in rows)==168
    geometry = read(DOC/'geometry.json')
    assert geometry['native_receipt_sha256'] == sha(LOCAL/'native-full05.json')
    for outcome, run in zip(geometry['outcomes'],native['runs']):
        assert len(outcome['regions']) == len(run['regions'])
        for region, raw in zip(outcome['regions'],run['regions']):
            assert region['resource'] == raw['resource']
            assert b''.join(struct.pack('<4f',*p) for p in region['points_xyz_width']).hex()==raw['points']
            assert struct.pack('<4f',*region['native_bound']).hex()==raw['header'][:32]
    svg = {}
    for name in ('O0.svg','O3.svg','comparison.svg'):
        tree = ET.parse(DOC/name)
        root = tree.getroot()
        assert root.attrib['height']=='1005'
        ids = [element.attrib['id'] for element in root.iter() if 'id' in element.attrib]
        assert len(ids)==len(set(ids))
        assert len(ids)==(152 if name=='comparison.svg' else 74 if name=='O0.svg' else 78)
        svg[name] = sha(DOC/name)
    return dict(scope='Evidence/shape consistency, not independent scientific proof',
                native_counts=[74,78],candidate_count=196,spatial_probes=1630,
                svg=svg,free=free(),installed_and_database='PASS')


def replay(output):
    assert not output.exists()
    output.mkdir()
    for name in ('start.py','native_probe.py','geometry.json','initial.json'):
        shutil.copyfile(LOCAL/name, output/name)
    shutil.copytree(LOCAL/'functions',output/'functions')
    environment = dict(os.environ,D5S_OUTPUT=str(output))
    native = ROOT/'research/resource-retained-population/d5t_native.py'
    command = [sys.executable,'-B',str(native),'native-replay.json']
    free()
    result = subprocess.run(command,cwd=ROOT,env=environment,capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    (output/'stdout.log').write_bytes(result.stdout)
    (output/'stderr.log').write_bytes(result.stderr)
    assert result.returncode==0,(result.returncode,result.stderr[-2000:])
    assert not result.stderr and b'FAULT' not in result.stdout
    observed = read(output/'native-replay.json')
    original = read(LOCAL/'native-full05.json')
    for key in ('runs','key_calls','model_comparisons','spatial_checks','functions','errors'):
        assert observed[key]==original[key], key
    return dict(path=str(output),exit=result.returncode,numerical_comparison='PASS',
                receipt_sha256=sha(output/'native-replay.json'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--replay',type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    assert output.is_relative_to((ROOT/'.local-work').resolve()) and not output.exists()
    result = check()
    if args.replay:
        target = args.replay.resolve()
        assert target.is_relative_to((ROOT/'.local-work').resolve()) and not target.exists()
        result['replay'] = replay(target)
    result['postflight'] = check()
    output.parent.mkdir(exist_ok=True,parents=True)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print('PASS',output)


if __name__=='__main__':
    main()
