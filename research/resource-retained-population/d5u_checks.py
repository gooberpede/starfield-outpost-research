# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify D5U retained evidence, derivatives, preserved pins and final statistics.

Reads named local/source inputs and installed/database hashes, but executes no
native or game code. Writes one fresh ignored receipt. No network, saves,
database edits or Git mutation. Missing local inputs fail without downloading.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import xml.etree.ElementTree as ET

from d5u_census import ROOT, LOCAL, DOC, write


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def main():
    output = LOCAL/sys.argv[1]
    assert not output.exists() and output.resolve().is_relative_to(LOCAL.resolve())
    initial = read(LOCAL/'initial.json')
    for category in ('installed','database'):
        assert {p:sha(p) for p in initial[category]} == initial[category]
    sources = list(csv.DictReader((ROOT/'docs/experiments/resource-retained-population/d5u-sources.csv').open(encoding='utf8')))
    for source in sources:
        path = Path(source['path'])
        if not path.is_absolute():
            path = ROOT/path
        assert sha(path)==source['sha256'],source['path']
    catalogue = list(csv.DictReader((DOC/'catalogue.csv').open(encoding='utf8')))
    queries = list(csv.DictReader((DOC/'queries.csv').open(encoding='utf8')))
    assert len(catalogue)==26 and len(queries)==6536
    assert len({(r['body'],r['source_key']) for r in catalogue})==26
    assert sum(int(r['raster_masks'])==1 for r in catalogue[:25])==19
    assert sum(int(r['raster_masks'])==2 for r in catalogue[:25])==6
    for row in catalogue:
        q = [v for v in queries if v['source_id']==row['source_id']]
        expected = {(str(x),str(y)) for x in range(-2,int(row['width'])+2) for y in range(-2,int(row['height'])+2)}
        assert len(q)==len(expected)==int(row['support_cells'])
        assert {(v['x'],v['y']) for v in q}==expected
        assert dict(Counter(v['mask'] for v in q))==json.loads(row['histogram'])
    geometry = read(DOC/'geometry.json')
    stats = dict(runs=0,cells=0,probes=0,unequal_pairs=0,equal_pairs=0)
    for summary in read(LOCAL/'native05/summary.json'):
        native = read(LOCAL/'native05'/summary['native'])
        assert native['code_sha256']==sha(Path(__file__).with_name('d5u_native.py'))
        assert native['input_sha256']==sha(LOCAL/'native05'/summary['model'])
        assert not native['errors']
        assert native['runs'][-1]['regions']==native['runs'][-2]['regions']
        assert all(v['native']==v['planar'] for v in native['spatial_checks'])
        models = read(LOCAL/'native05'/summary['model'])['results']
        for run,model in zip(native['runs'],models):
            expected = model['full']['regions']
            assert len(run['regions'])==len(expected)
            for raw,predicted in zip(run['regions'],expected):
                assert raw['points']==b''.join(struct.pack('<4f',*p) for p in predicted['points']).hex()
                assert raw['header'][:32]==struct.pack('<4f',*predicted['native_bound']).hex()
            if 'repeat' in run['outcome'] or run['outcome'].startswith('CONTROL'):
                continue
            out = next(o for o in geometry['outcomes'] if o['source_id']==summary['source_id'] and o['mask']==run['mask'])
            assert len(out['regions'])==len(run['regions'])
            for exported,raw in zip(out['regions'],run['regions']):
                assert exported['resource']==raw['resource']
                assert b''.join(struct.pack('<4f',*p) for p in exported['points_xyz_width']).hex()==raw['points']
                assert struct.pack('<4f',*exported['native_bound']).hex()==raw['header'][:32]
                assert struct.pack('<2I',*exported['metadata_words']).hex()==raw['header'][32:48]
        for pair in native['population_discriminators']:
            if pair['exact_equal']:
                stats['equal_pairs']+=1
            else:
                assert pair['witness']['native_a'] != pair['witness']['native_b']
                stats['unequal_pairs']+=1
        stats['runs']+=len(native['runs'])
        stats['cells']+=sum(len(r['calls']) for r in native['runs'])
        stats['probes']+=len(native['spatial_checks'])
        if summary['source_id']=='U26':
            assert native['runs'][0]['regions']==native['runs'][1]['regions']
            assert native['runs'][0]['weights']!=native['runs'][1]['weights']
            assert [len(r['regions']) for r in native['runs'][1:4]]==[69,77,75]
    keys = read(LOCAL/'keys04.json')
    assert keys['code_sha256']==sha(Path(__file__).with_name('d5u_keys.py'))
    assert len(keys['queries'])==6536 and len(keys['packed_keys'])==1296
    assert sorted(c['mask'] for c in keys['corners'])==[0,1,3]
    assert all(c['permutations']==24 and not c['visited_collision'] for c in keys['corners'])
    svgs = list(DOC.glob('*.svg'))
    assert len(svgs)==38
    for path in svgs:
        root = ET.parse(path).getroot()
        ids = [element.attrib['id'] for element in root.iter() if 'id' in element.attrib]
        assert len(ids)==len(set(ids))
        assert root.attrib.get('viewBox') and root.find('{http://www.w3.org/2000/svg}title') is not None
    floor = {d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    assert min(floor.values())>=40_000_000_000
    write(output,dict(source_hashes=len(sources),queries=6536,native_keys=1296,svgs=38,
                      native=stats,installed_database='PASS',free=floor,
                      limits='Retained evidence/derivative consistency; native runs and scientific admissibility require their separate primary evidence.'))
    print('PASS',stats)


if __name__=='__main__':
    main()
