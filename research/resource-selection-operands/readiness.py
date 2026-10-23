# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure receipt selector: never operates a process. Owned C1G minimum acquisition
policy, independently tested; source candidacy is not historical P3 ancestry.
"""
import struct


def raw(row, key):
    group = row.get(key, {})
    if group.get('status') != 'COMPLETE':
        return None
    return bytes.fromhex(group['raw'])


class Tracker:
    def __init__(self):
        self.active = {}

    def observe(self, row):
        kind = row.get('kind')
        if kind in ('THREAD_END', 'EXCEPTION'):
            self.active = {k:v for k,v in self.active.items() if k[0] != row['tid']}
            return False
        if kind != 'SAMPLE' or 'invocation_token' not in row:
            return False
        key = row['tid'], row['thread_lifetime'], row['invocation_token']
        site = row['site']
        if site == 'generation_entry':
            origin = raw(row, 'origin')
            candidate = (row['required_reads_complete'] and row['entry_bound'] and
                         row['owner_key_u32'] == 385246 and origin is not None and
                         struct.unpack('<ii', origin) == (-3800, -200))
            self.active[key] = dict(candidate=candidate, current=None, cells=set(), valid=True)
            assert len(self.active) <= 4096, 'local invocation copy budget'
        state = self.active.get(key)
        if state is None:
            return False
        if not row['required_reads_complete']:
            state['valid'] = False
        if site == 'resource_call':
            resource = raw(row, 'ires')
            proof = row.get('file_provenance', {})
            qualified = (resource is not None and proof.get('status') == 'COMPLETE' and
                         proof.get('main_file_identity') is True)
            state['current'] = struct.unpack_from('<I', resource, 0x28)[0] if qualified else None
        if site == 'chance_branch' and row.get('resource_call_join') and state['current'] is not None:
            xy = raw(row, 'cell_xy_i32')
            if xy is not None:
                state['cells'].add((state['current'], *struct.unpack('<ii', xy)))
        if site == 'provider_return':
            del self.active[key]
            return (state['candidate'] and state['valid'] and row['frame_matches'] and
                    {(0x57d4, 10, 1), (0x57d4, 11, 1), (0x57cf, 11, 1)} <= state['cells'])
        return False
