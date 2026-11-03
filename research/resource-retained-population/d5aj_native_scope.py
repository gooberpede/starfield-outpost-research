# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate D5AJ native scope inputs and derive Episode A Grid relationships.

Reads the pinned installed executable, retained native exports and stopped local
Episode A session. Writes a fresh ignored JSON receipt only. Uses the project's
owned schema-4 decoder unchanged under SOR-P-0002. No native instructions execute,
database opens, process attaches, save writes, network or Git mutations occur.
The assertions authenticate cited windows; manual instruction analysis supplies
their semantic interpretation. This is not a general disassembler or a live tool.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use Python -E -B without optimization')

import argparse
import csv
import ctypes
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import read_capture
import d5ai_read_geometry

EXE = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
EXE_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
DLL_SHA = '9df5a04ef770887b402dca7c61ee3af52f6046711fcd4e997b66922055bbe67c'
SESSION = ROOT / '.local-work/d5x/live/session-2f305e35afac69b4faca3025a30c7e6f0c04aeaefd579c387d464ef3c4981571'


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5aj') or out.exists():
        raise ValueError('Fresh D5AJ ignored output required')
    free = {}
    for drive in ('C:/', 'D:/'):
        available = ctypes.c_ulonglong()
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(drive), ctypes.byref(available), None, None):
            raise OSError('Caller-available disk query failed')
        if available.value < 40_000_000_000:
            raise RuntimeError('Required disk floor')
        free[drive] = available.value
    if sha(EXE) != EXE_SHA:
        raise ValueError('Pinned executable mismatch')
    sources = {}
    registers = ('d5ai-ownership-sources.csv', 'd5ai-owner-context-sources.csv',
                 'd5ab-p1-sources.csv')
    for name in registers:
        path = ROOT / 'docs/experiments/resource-retained-population' / name
        for row in csv.DictReader(path.read_text(encoding='utf8').splitlines()):
            source = ROOT / row['path']
            if source in sources:
                continue
            actual = sha(source)
            if actual != row['sha256']:
                raise ValueError(str(source))
            sources[source] = dict(path=row['path'], sha256=actual)
    native = (ROOT / '.local-work/d5v/export01/native.tsv').read_text(encoding='utf8')
    constructor = (ROOT / '.local-work/d5v/export02/native.tsv').read_text(encoding='utf8')
    erase = (ROOT / '.local-work/d5ah-extractor/export02/native.tsv').read_text(encoding='utf8')
    finder_path = ROOT / '.local-work/d5s/export32/native.tsv'
    finder_sha = 'a7797c96e98d190ec6808f2e242a97c02f77a187a2eaacaa7df5d2667d6febbc'
    if sha(finder_path) != finder_sha:
        raise ValueError('D5S-E32 pointer-map finder export mismatch')
    sources[finder_path] = dict(path='.local-work/d5s/export32/native.tsv', sha256=finder_sha)
    finder = finder_path.read_text(encoding='utf8')
    fresh_exports = []
    for label, expected in (
            ('export05', '9c61b7e5c8d4dfe2fadd4dbc4a1f70f2aa350254891c7420e13f3cf66ac30762'),
            ('export06', '4b3736bca8cc04d8950cf79c119b40a99e90fd64125b5f8e44b732ada9181718'),
            ('export07', '52a5d7eb8bf9450ff8644e4c92f1525b9e7f59785100905efc3ad53b72d146d0'),
            ('export08', '52a5d7eb8bf9450ff8644e4c92f1525b9e7f59785100905efc3ad53b72d146d0')):
        directory = ROOT / '.local-work/d5aj/native-scope' / label
        receipt = json.loads((directory / 'result.json').read_bytes())
        export = directory / 'native.tsv'
        if (sha(export) != expected or receipt['native_sha256'] != expected or
                not receipt['copy_core_preserved'] or receipt['exit'] or
                '-readOnly' not in receipt['command'] or '-noanalysis' not in receipt['command'] or
                'D:\\tools\\sor-d5ai-ownership-export01' not in receipt['command']):
            raise ValueError('Disposable export identity/preservation mismatch')
        for path, pin in receipt['copy_core_before'].items():
            if not Path(path).is_relative_to(Path('D:/tools/sor-d5ai-ownership-export01')) or sha(Path(path)) != pin:
                raise ValueError('Disposable core changed: ' + path)
        sources[export] = dict(path=str(export.relative_to(ROOT)), sha256=expected)
        fresh_exports.append(dict(label=label, receipt_sha256=sha(directory / 'result.json'),
                                  method_sha256=receipt['method_sha256'], java_sha256=receipt['java_sha256'],
                                  copy_core_preserved=True))
    # These exact operands are the primary locations manually interpreted in the
    # invalidation matrix. Presence checks do not prove a complete writer census.
    windows = [
        (native, '1409829c6\tMOV R14,RCX'),
        (native, '1409829db\tMOV RBX,qword ptr [RCX + 0x18]'),
        (native, '1409829fc\tMOV RAX,qword ptr [0x145fd9c30]'),
        (native, '140982a03\tMOV RSI,qword ptr [RAX + 0x130]'),
        (native, '140982a36\tCALL 0x140975030'),
        (native, '140982af8\tCALL 0x14365cdb0'),
        (native, '140982b7f\tMOV RSI,RCX'),
        (native, '140982b89\tMOV RDI,qword ptr [RAX + 0x130]'),
        (native, '140982c32\tCALL 0x14365cdb0'),
        (constructor, '140982db2\tMOV R12,RCX'),
        (constructor, '140982db5\tLEA RBX,[RCX + 0x5c]'),
        (constructor, '140982e07\tADD R12,0x10'),
        (constructor, '140982e21\tMOV R14,qword ptr [RAX]'),
        (constructor, '140982e39\tJZ 0x140983182'),
        (constructor, '140983006\tMOV R14,RAX'),
        (constructor, '14098317e\tMOV qword ptr [RAX + RCX*0x8],R14'),
        (erase, '140975115\tMOV qword ptr [R14],RAX'),
        (erase, '14097511c\tMOV qword ptr [R13 + 0x8],RCX'),
        (erase, '140975120\tMOV qword ptr [R14 + 0x8],RAX'),
        (finder, '140349ae4\tCMP qword ptr [RDX + RCX*0x8],RBX'),
    ]
    for body, line in windows:
        if line not in body:
            raise ValueError('Missing cited instruction: ' + line)
    transport = read_capture.inspect(SESSION, DLL_SHA)
    if not transport['complete_session'] or transport['damage']:
        raise ValueError('Stopped transport does not authenticate')
    sidecar = d5ai_read_geometry.read_session(SESSION)
    if sidecar['errors'] or len(sidecar['snapshots']) != 1:
        raise ValueError('Expected single valid Episode A snapshot')
    snapshot = sidecar['snapshots'][0]
    header = snapshot['header']
    raw = (SESSION / 'events.bin').read_bytes()
    events = [read_capture.decode(raw[i + 16:i + 328]) for i in range(0, len(raw), 328)]
    holders = []
    for holder in snapshot['holders']:
        births = [e for e in events if e['kind'] == 14 and
                  e['source'] == holder['source_pointer'] and e['ticks'] < header['ticks_begin']]
        birth = max(births, key=lambda e: (e['ticks'], e['sequence']))
        pubs = [e for e in events if e['kind'] == 15 and
                e['source'] == birth['source'] and birth['ticks'] < e['ticks'] < header['ticks_begin']]
        if len(pubs) != 1 or pubs[0]['holder'] != birth['holder']:
            raise ValueError('Birth/publication Grid join is not unique')
        holders.append(dict(source=birth['source'], key=read_capture.source_key(birth),
                            allocation=birth['selection'], grid=birth['holder'],
                            birth_sequence=birth['sequence'], publication_sequence=pubs[0]['sequence'],
                            birth_ticks=birth['ticks']))
    start = min(h['birth_ticks'] for h in holders)
    fences = [e for e in events if e['kind'] in (10, 11) and
              start <= e['ticks'] <= header['completion_ticks']]
    opened, pairs = {}, []
    for event in sorted(fences, key=lambda e: (e['ticks'], e['sequence'])):
        key = (event['a'], event['proc'], event['thread'])
        if event['kind'] == 10:
            if key in opened:
                raise ValueError('Ambiguous nested identical fence')
            opened[key] = event
        else:
            begin = opened.pop(key)
            if event['ticks'] <= begin['ticks']:
                raise ValueError('Unordered fence')
            pairs.append(dict(reason=event['a'], receiver=event['proc'],
                              receiver_domain='GRID' if event['a'] == 3 else 'REQUIRES_TYPED_ANALYSIS',
                              begin_sequence=begin['sequence'], end_sequence=event['sequence'],
                              begin_ticks=begin['ticks'], end_ticks=event['ticks'], thread=event['thread'],
                              begin_epoch=begin['epoch'], end_epoch=event['epoch'],
                              matches_occupied_source_grid=[h['allocation'] for h in holders
                                                            if h['grid'] == event['proc']]))
    if opened or len(pairs) != 9 or any(p['reason'] != 3 or p['matches_occupied_source_grid'] for p in pairs):
        raise ValueError('Episode A nine-other-Grid premise does not hold')
    result = dict(schema='sor-d5aj-native-scope/1', executable_sha256=EXE_SHA,
                  method_sha256=sha(Path(__file__)), inputs=list(sources.values()),
                  fresh_disposable_exports=fresh_exports,
                  producer_sources={p: sha(ROOT / p) for p in (
                      'runtime/construction-winner/observer.h', 'runtime/construction-winner/bridges.asm')},
                  instruction_windows=[line for _, line in windows],
                  raw_sha256=hashlib.sha256(raw).hexdigest(), snapshot_sha256=snapshot['sha256'],
                  snapshot_proc=header['proc'], holders=holders, fence_pairs=pairs, free=free,
                  scope='Typed Grid receiver and ordinary source-owning-vector graph; no inferred different ProcGen, no live execution')
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print('PASS:', len(sources), 'authenticated exports;', len(holders), 'holders;', len(pairs), 'other-Grid pairs')


if __name__ == '__main__':
    main()
