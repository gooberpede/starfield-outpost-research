# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline chronology; stdlib plus owned cross-session decoder (provenance README).
Reads sealed sessions, writes exclusive derivative directory only. No native API.
"""
import argparse
import collections
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import statistics

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('cross', ROOT/'research/cross-session-center/verify.py')
cross = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cross)


def stats(values):
    if not values:
        return None
    x = sorted(values)
    return dict(n=len(x), minimum=x[0], median=statistics.median(x),
                p90=x[int((len(x)-1)*.90)], p99=x[int((len(x)-1)*.99)], maximum=x[-1])


def intervals(events, frequency):
    # Native thread sampling time, never journal order or fitted wall clock.
    ticks = sorted(e['qpc'] for e in events)
    return [(b-a)/frequency for a, b in zip(ticks, ticks[1:])]


def run(out):
    disk = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(disk.values()) >= 40_000_000_000
    out.mkdir(parents=True, exist_ok=False)
    groups = collections.defaultdict(list)
    pins = []
    timeline = []
    sources = []
    for version in (5, 6):
        root = cross.SESSIONS[version]
        meta = json.loads((root/'ready.json').read_bytes())
        frequency = meta['qpc_frequency']
        assert frequency == 10_000_000
        first = None
        pending = {}
        for e in cross.records(version):
            first = e['qpc'] if first is None else min(first, e['qpc'])
            if version == 5:
                if e['kind'] != 2:
                    continue
                site, phase = 'AD0C36', 'return'
            else:
                if e['kind'] != 8:
                    continue
                site, phase = f"{e['site']:X}", {1:'before', 2:'return', 3:'unwind'}[e['phase']]
            try:
                wid, form = cross.identity(e)
                identity = cross.WIDS[wid]
            except ValueError:
                identity = 'INCOHERENT'
            row = dict(version=version, site=site, phase=phase, identity=identity,
                       sequence=e['sequence'], invocation=e['invocation'], parent=e['parent'],
                       qpc=e['qpc'], thread=e['thread'], status=e['status'],
                       raw_offset=e['offset'], record_sha256=e['record_sha256'])
            if phase == 'before':
                pending[e['invocation']] = row
            elif version == 6:
                before = pending.pop(e['invocation'])
                assert (before['thread'], before['site']) == (row['thread'], row['site'])
                row['bracket_seconds'] = (row['qpc']-before['qpc'])/frequency
            groups[(version, site, phase, identity, e['thread'])].append(row)
            timeline.append(row)
        assert not pending
        for r in timeline:
            if r['version'] == version:
                r['seconds_since_first_any_event'] = (r['qpc']-first)/frequency
        for p in [root/'events.bin', root/'records.jsonl', root/'ready.json', root/'retired.json']:
            pins.append(dict(path=str(p), sha256=cross.sha(p)))
        # UTC fields in060 health are copied session-start fields, not fresh clocks.
        # Preserve operator/ACK chronology without claiming UTC-QPC calibration.
        candidates = list(root.glob('*.operator.json')) + list(root.glob('ack-*.json'))
        if version == 6:
            candidates += list((ROOT/'.local-work/position-write-history/run-20261013T085008190141Z').glob('*checkpoint-request.json'))
        for p in sorted(candidates):
            x = json.loads(p.read_bytes())
            sources.append(dict(version=version, path=str(p.relative_to(ROOT)),
                sha256=cross.sha(p), utc=x.get('ack_utc', x.get('utc')),
                label=x.get('phase', x.get('label', x.get('nonce'))),
                note=x.get('operator_report', x.get('note')),
                captured_sequence=x.get('captured')))
    summaries = []
    for key, events in sorted(groups.items()):
        v, site, phase, identity, thread = key
        times = [e['qpc'] for e in events]
        duration = (max(times)-min(times))/10_000_000
        gaps = intervals(events, 10_000_000)
        summaries.append(dict(version=v, site=site, phase=phase, identity=identity,
            thread=thread, count=len(events), span_seconds=duration,
            rate_over_span=(len(events)-1)/duration if duration else None,
            interval_seconds=stats(gaps), gaps_over_one_second=sum(g>1 for g in gaps),
            brackets=stats([e['bracket_seconds'] for e in events if 'bracket_seconds' in e])))
    bins = collections.Counter((r['version'], r['site'], r['phase'],
        r['identity'], int(r['seconds_since_first_any_event']//5)) for r in timeline)
    with (out/'bins.csv').open('w', newline='', encoding='utf8') as f:
        w=csv.writer(f, lineterminator='\n');w.writerow(['schema','call_rva','phase','identity','five_second_bin','count'])
        w.writerows((*k, n) for k,n in sorted(bins.items()))
    with (out/'events.csv').open('w', newline='', encoding='utf8') as f:
        names=list(timeline[0])+['bracket_seconds','seconds_since_first_any_event']
        names=list(dict.fromkeys(names))
        w=csv.DictWriter(f, fieldnames=names, lineterminator='\n');w.writeheader();w.writerows(timeline)
    pooled = []
    pooled_groups = collections.defaultdict(list)
    for r in timeline:
        if r['phase'] == 'return':
            pooled_groups[(r['version'], r['site'], r['identity'])].append(r)
    for (v, site, identity), events in sorted(pooled_groups.items()):
        gaps = intervals(events, 10_000_000)
        pooled.append(dict(version=v,site=site,identity=identity,count=len(events),
            threads=len({e['thread'] for e in events}),parents=dict(collections.Counter(e['parent'] for e in events)),
            start_seconds=min(e['seconds_since_first_any_event'] for e in events),
            end_seconds=max(e['seconds_since_first_any_event'] for e in events),
            interval_seconds=stats(gaps),gaps_over_one_second=sum(g>1 for g in gaps)))
    # ACK sequences bound emission prefixes, not exact gameplay action instants.
    phase_counts=[]
    previous=0
    for mark in sorted((x for x in sources if x['version']==6 and x['captured_sequence'] is not None), key=lambda x:x['captured_sequence']):
        seq=mark['captured_sequence']
        counts=collections.Counter((r['site'],r['identity']) for r in timeline if r['version']==6 and r['phase']=='return' and previous<r['sequence']<=seq)
        phase_counts.append(dict(previous_sequence=previous,captured_sequence=seq,ack_utc=mark['utc'],
            counts=[dict(site=k[0],identity=k[1],count=n) for k,n in sorted(counts.items())]))
        previous=seq
    counts=collections.Counter((r['site'],r['identity']) for r in timeline if r['version']==6 and r['phase']=='return' and r['sequence']>previous)
    phase_counts.append(dict(previous_sequence=previous,captured_sequence=562326,ack_utc='retirement tail',
        counts=[dict(site=k[0],identity=k[1],count=n) for k,n in sorted(counts.items())]))
    result=dict(disk=disk, groups=summaries, pooled=pooled, phase_counts=phase_counts, action_marks=sources, pins=pins,
        decoder_sha256=cross.sha(ROOT/'research/cross-session-center/verify.py'),
        script_sha256=cross.sha(Path(__file__)),
        timebase='QPC/10000000; relative to first any event separately per session. No060 UTC calibration.',
        limits=['No idle camera state or input inactivity trace captured',
                'Brackets include observer before/after work and scheduling, not pure native duration',
                'Per-identity sampling excludes incoherent identity rows; retained separately'])
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(pooled=pooled,phase_counts=phase_counts),indent=2))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output', type=Path, required=True)
    run(p.parse_args().output)
