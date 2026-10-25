# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded, offline consumer selector; no IO or target effects."""
import math
import struct

TARGETS = (0x57d4, 0x57d0, 0x57cf)
BODY = 0x5e0de


def complete(row):
    return (row.get('required_reads_complete') is True and
            all(row[k].get('status') == 'COMPLETE' for k in
                ('geometry', 'selected', 'source_context', 'refresh_payload') if k in row) and
            all(row.get(k, True) is True for k in
                ('closure_read', 'descriptor_read', 'qb_retained_read')))


class Tracker:
    """Same evaluation only; never infer a generation epoch from proximity.

    Input SAMPLE bytes must be independently persisted and checked before feed.
    Useful requests still require a positive ACK_ACCEPTED and terminal sealing.
    """
    def __init__(self):
        self.active = {}
        self.gaps = 0
        self.last_match = None

    def feed(self, row):
        kind = row.get('kind')
        if kind in ('EXCEPTION', 'LOSS'):
            self.active.clear()
            self.gaps += 1
            return False
        if kind == 'THREAD_END':
            self.active = {k: v for k, v in self.active.items() if k[1] != row['tid']}
            return False
        if kind != 'SAMPLE':
            return False
        key = (row['pid'], row['tid'], row['thread_lifetime'], row.get('updater_token'))
        if row['site'] == 'updater_entry':
            # Prune overwritten frames, retaining genuinely nested evaluations.
            self.active = {k: v for k, v in self.active.items()
                           if k[:3] != key[:3] or v['bp'] > row['updater_bp']}
            query=bytes.fromhex(row.get('query_raw',''))
            scalars=struct.unpack('<ff',struct.pack('<II',row.get('radius_bits',0),row.get('upper_bits',0)))
            valid_query=len(query)==24 and all(map(math.isfinite,struct.unpack('<fff',query[:12])+scalars)) and scalars[0]>=0
            if row.get('frame_verified') and row.get('query_read') and complete(row) and valid_query:
                self.active[key] = dict(bp=row['updater_bp'], accepted={}, entry=row)
            assert len(self.active) <= 4096
            return False
        inv = self.active.get(key)
        if inv is None:
            return False
        if row.get('updater_bp') != inv['bp'] or not complete(row):
            return False
        if row.get('decision') == 'ACCEPT' and row.get('ancestry') == 'BOUND_CALLBACK':
            context = row['source_context']
            raw = bytes.fromhex(row['selected']['raw_resource'])
            if (len(raw) == 48 and int.from_bytes(raw[40:44], 'little') in TARGETS and
                    raw[46] == 0x9f and row['file_provenance'].get('main_file_identity') is True and
                    context.get('owner_key_u32') == BODY):
                header = bytes.fromhex(row['geometry']['raw_region'])
                points = bytes.fromhex(row['geometry']['ordered_xyzw'])
                n, cap = struct.unpack_from('<II', header, 24)
                values = struct.unpack('<' + 'f' * (len(points)//4), points)
                bounds=struct.unpack_from('<ffff',header)
                entry=inv['entry'];closure=bytes.fromhex(row['raw_closure'])
                query_ok=(row['raw_descriptor']==entry['query_raw'] and
                          closure[16:20]==struct.pack('<I',entry['radius_bits']) and
                          closure[20:24]==struct.pack('<I',entry['upper_bits']))
                if (n and n <= cap <= 4096 and len(points) == n*16 and all(map(math.isfinite, values+bounds)) and
                        bounds[3]>=0 and all(v>=0 for v in values[3::4]) and query_ok):
                    inv['accepted'][row['resource_pointer']] = row
        if 'refresh_payload' not in row:
            return False
        self.active.pop(key, None)
        if row.get('ancestry') != 'BOUND_TRANSFER':
            return False
        for member in row['refresh_payload'].get('members') or []:
            accepted = inv['accepted'].get(member['pointer'])
            if (accepted and member['raw'] == accepted['selected']['raw_resource'] and
                    row['temporary_set'] == accepted['temporary_set'] and
                    row['binding_reference'] == accepted['binding_reference'] and
                    row['raw_binding_extra'] == accepted['raw_binding_extra']):
                self.last_match = accepted
                return True
        return False
