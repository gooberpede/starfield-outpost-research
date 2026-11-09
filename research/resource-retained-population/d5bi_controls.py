# SPDX-License-Identifier: GPL-3.0-or-later
"""Mutate disposable in-memory projections and verify precise refusals."""
import argparse
from pathlib import Path

import d5bi_verify as v


def reject(label, expected, operation):
    try:
        operation()
    except ValueError as error:
        v.require(str(error) == expected, f'{label}: wrong rejection: {error}')
        print(f'{label}: {error}')
    else:
        raise ValueError(f'{label}: adverse control was accepted')


def change(rows, seq, **fields):
    copy = rows.copy()
    copy[seq-1] = dict(v.at(rows, seq), **fields)
    return copy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    members = v.read_zip(args.candidate, v.decode(v.MANIFEST.read_bytes()))
    session, snapshot, channels = v.parse(members)
    core, causal, scheduler, lifetime = (channels[k] for k in ('core','causal','scheduler','lifetime'))
    winner, stages, _ = v.competition(core, causal, scheduler)
    chain = v.construction(core, winner)
    journal = v.lifetime_journal(lifetime, session)
    v.interpret(session, snapshot, channels)

    reject('swapped process', 'Wrong N2 process or baseline',
           lambda: v.check_session(dict(session, process=dict(session['process'], pid=11689))))
    reject('swapped journal domain', 'Wrong journal domain, process or field layout',
           lambda: v.rows(members['causal.jsonl'], 'scheduler', session))
    core_bytes = members['core.jsonl']
    reject('truncated record', 'Truncated projected journal',
           lambda: v.rows(core_bytes[:-3], 'core', session))
    lines = core_bytes.splitlines(keepends=True)
    reject('malformed record', 'Malformed projected record',
           lambda: v.rows(lines[0] + b'[]\n' + b''.join(lines[2:]), 'core', session))
    reject('reordered records', 'Projected sequence gap or reorder',
           lambda: v.rows(b''.join([lines[0], lines[2], lines[1], *lines[3:]]), 'core', session))
    reject('missing scheduler tail', 'Incomplete projected journal census',
           lambda: v.rows(b''.join(members['scheduler.jsonl'].splitlines(keepends=True)[:-1]), 'scheduler', session))
    reject('missing target competitor publication', 'Unqualified task history',
           lambda: v.competition(core, causal, change(scheduler, 4162, kind=2)))
    reject('wrong typed provider request', 'Unqualified task history',
           lambda: v.competition(core, causal, change(scheduler, 41257, request=[-2, 10])))
    reject('false visited bypass', 'False target bypass',
           lambda: v.competition(change(core, 3991, a=0), causal, scheduler))
    reject('wrong source birth', 'Substituted source birth',
           lambda: v.snapshot_evidence(snapshot, core, journal, dict(winner, source_birth=898), chain))
    reject('wrong store token', 'Wrong append destination, source token or loss',
           lambda: v.construction(core, dict(winner, core=winner['core'][:-2] +
               [dict(winner['core'][-2], b=0), winner['core'][-1]])))
    reject('omitted contrary-history record', 'Projected sequence gap or reorder',
           lambda: v.rows(b''.join(lines[:898] + lines[899:]), 'core', session))
    reject('relevant rather than disjoint Grid clear', 'Relevant, unknown or boundary-tied lifecycle fence',
           lambda: v.snapshot_evidence(snapshot, change(core, 32351, proc=v.at(core,2082)['holder']),
                                       journal, winner, chain))
    returned = v.at(core, 3970)['ticks']
    during_copy = change(lifetime, 2991, ticks=returned+1)
    during_copy = change(during_copy, 2992, ticks=returned+2)
    reject('target mutation after generation return',
           'Copied content overlaps ending or mutation after frame-qualified construction',
           lambda: v.snapshot_evidence(snapshot, core, v.lifetime_journal(during_copy, session), winner, chain))
    reject('winner pending copy changed', 'Target reader, zero-pending or acquire operand mismatch',
           lambda: v.owner_history(core, change(causal, 2949, old_state=0x1000, new_state=0x2000), scheduler, winner))
    reject('writer CAS corrupted', 'Contradictory owner atomic operands',
           lambda: v.owner_history(core, change(causal, 2950, new_state=0x401001), scheduler, winner))
    reject('reader drain altered', 'Contradictory owner atomic operands',
           lambda: v.owner_history(core, change(causal, 2941, new_state=0), scheduler, winner))
    reject('writer release before store', 'Same-thread protected constructor enclosure mismatch',
           lambda: v.owner_history(core, change(causal, 2957, ticks=v.at(core,3972)['ticks']-1), scheduler, winner))
    late = change(causal, 2950, ticks=v.at(core,3959)['ticks']+1)
    late = change(late, 2951, ticks=v.at(core,3959)['ticks']+2)
    reject('acquire after protected miss', 'Same-thread protected constructor enclosure mismatch',
           lambda: v.owner_history(core, late, scheduler, winner))
    reject('bypass before its own selection', 'Target bypass lacks ordered shared visit evidence',
           lambda: v.competition(change(core, 3991, ticks=v.at(core,3990)['ticks']-1), causal, scheduler))
    layer_provider = next(r for r in scheduler if r['allocation'] == 1237 and r['kind'] == 9)
    reject('layer provider before readiness', 'Typed task stages contradict recorded progress order',
           lambda: v.competition(core, causal, change(scheduler, layer_provider['sequence'],
                                                      ticks=v.at(core,3959)['ticks']-1)))
    reject('contrary exclusive target history', 'Contrary target exclusive or pending history',
           lambda: v.competition(core, change(causal, 2947, kind=9), scheduler))
    reject('cross-domain lock join', 'Wrong or uncertain owner generation',
           lambda: v.owner_history(core, change(causal, 2949, lock=winner['source']), scheduler, winner))
    reject('intervening peer stamp', 'Intervening peer stamp',
           lambda: v.continuations(dict(channels, lifetime=change(lifetime, 1,
               thread=56840, ticks=v.at(causal, 2946)['ticks']+1)), winner, stages))
    models = v.continuations(channels, winner, stages)
    modified = stages.copy()
    modified[10] = dict(stages[10], route=1, extra=0)
    v.require(len({tuple(ts) for ts in models['pause_models'].values()}) == 2 and
              set(models['unknown']) == set(v.UNKNOWN) and v.continuations(channels, winner, modified) == models,
              'Unsupported causal upgrade from copied queue diagnostics')
    operands = [v.at(causal, i) for i in [*range(2927,2933),2935,2937,2940,2942,2949,2950]]
    v.require(not v.exhaustive_operands(operands, 0x401000), 'Missing reader release was completed')
    print('PASS: named projection refusals, missing-release oracle and equivalent-continuation boundary')


if __name__ == '__main__':
    main()
