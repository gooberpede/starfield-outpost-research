# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure bounded generation selector. Never binds a Workshop or historical epoch."""
class Tracker:
    """Select a complete body-owned invocation, independently of its resource set.

    This is candidate-source acquisition. Saved Workshop membership and accepted
    region ancestry remain UNKNOWN, even when numeric body and BIOM values match.
    """
    def __init__(self, body):
        self.body = int(body, 16)
        self.active = {}

    def observe(self, row):
        if row['kind'] in ('THREAD_END', 'EXCEPTION'):
            self.active = {k: v for k, v in self.active.items() if k[0] != row['tid']}
        if row['kind'] != 'SAMPLE' or 'invocation_token' not in row:
            return False
        key = (row['tid'], row['thread_lifetime'], row['invocation_token'])
        if row['site'] == 'generation_entry':
            ok = (row['required_reads_complete'] and row.get('upstream_join') is True
                  and row['owner_key_u32'] == self.body and row['entry_bound'])
            self.active[key] = dict(ok=ok, calls=0)
            if len(self.active) > 4096:
                raise RuntimeError('active invocation capacity')
        item = self.active.get(key)
        if item is None:
            return False
        item['ok'] &= bool(row['required_reads_complete'] and row.get('frame_matches'))
        if row['site'] == 'resource_call':
            item['ok'] &= bool(row.get('selection_chain_complete')
                               and row.get('file_provenance', {}).get('main_file_identity'))
            item['calls'] += 1
        if row['site'] == 'provider_return':
            self.active.pop(key)
            return item['ok'] and item['calls'] > 0
        return False
