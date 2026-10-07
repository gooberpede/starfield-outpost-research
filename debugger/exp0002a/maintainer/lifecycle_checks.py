"""Pure verdicts for disposable integration evidence, never process control."""


def restoration_failures(original, observed):
    if not original or len(original) != len(observed):
        return ['Missing breakpoint-site byte evidence']
    return [f'Site {i}: original instruction bytes not restored'
            for i, (before, after) in enumerate(zip(original, observed))
            if len(before) != 16 or before != after]


def thread_hazards(snapshot):
    """Positive hazards only; no hits does not prove the OS debug queue is empty."""
    return [row for row in snapshot['threads']
            if row['at_site'] or row['after_site'] or int(row.get('eflags', '0'), 16) & 0x100]


def survival_failures(rows, workers):
    errors = []
    if [row['delay'] for row in rows] != [0, 1, 5, 15]:
        return ['Missing delayed observation window']
    previous = None
    for row in rows:
        heartbeat = row['heartbeat']
        if not row['alive'] or row['exit_code'] is not None:
            errors.append(f"Target exited by +{row['delay']} seconds")
        if row['exceptions']:
            errors.append(f"Unhandled target exception by +{row['delay']} seconds")
        if not heartbeat or len(heartbeat.get('counters', [])) != workers:
            errors.append('Missing per-worker heartbeat evidence')
        elif previous is not None:
            if heartbeat['heartbeat'] <= previous['heartbeat']:
                errors.append('Heartbeat stalled')
            if any(a <= b for a, b in zip(heartbeat['counters'], previous['counters'])):
                errors.append('At least one worker stalled')
        previous = heartbeat
    return errors
