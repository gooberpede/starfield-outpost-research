# SPDX-License-Identifier: GPL-3.0-or-later
"""Narrow D4 acquisition to a requested geographic source and complete lineage.

Pure row selector. No target access. Matching numeric source context is not a
Workshop pointer or historical epoch join. Descriptor decoding is limited to
the qualified interior chart and 12-fine-cell pattern-slot route.
"""
import importlib.util
from pathlib import Path
import struct

spec = importlib.util.spec_from_file_location('d4_readiness',
    Path(__file__).resolve().parents[1] / 'resource-selection-context/readiness.py')
inherited = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inherited)


def raw(row, name, size):
    field = row.get(name, {})
    if field.get('status') != 'COMPLETE':
        return None
    value = bytes.fromhex(field['raw'])
    return value if len(value) == size else None


class Tracker(inherited.Tracker):
    def __init__(self, body, target):
        super().__init__(body)
        self.target = target
        self.frames = {}

    def observe(self, row):
        if row['kind'] in ('THREAD_END', 'EXCEPTION'):
            self.frames = {k: v for k, v in self.frames.items() if k[0] != row['tid']}
        if row['kind'] == 'SAMPLE' and 'manager_frame_descriptor' in row:
            key = (row['tid'], row['thread_lifetime'], row['capture'])
            self.frames[key] = raw(row, 'manager_frame_descriptor', 0x2c)
            if len(self.frames) > 4096:
                raise RuntimeError('pending descriptor capacity; stop, do not evict evidence')
        if row.get('site') == 'generation_entry':
            key = (row['tid'], row['thread_lifetime'], row['upstream_query_capture'])
            frame = self.frames.pop(key, None)
            source = raw(row, 'source', 0x70)
            match = False
            if frame is not None and source is not None:
                ox = struct.unpack_from('<i', frame, 4)[0] * 192 + struct.unpack_from('<i', frame, 0x14)[0] * 12 + struct.unpack_from('<i', frame, 0x24)[0]
                oy = struct.unpack_from('<i', frame, 8)[0] * 192 + struct.unpack_from('<i', frame, 0x18)[0] * 12 + struct.unpack_from('<i', frame, 0x28)[0]
                sx, sy = struct.unpack_from('<2i', source, 0x10)
                fid = struct.unpack_from('<I', source)[0]
                actual = f'{frame[0]}:{ox+sx}:{oy+sy}:{fid:08x}'
                match = (frame[0] == self.target['chart'] and [ox, oy] == self.target['descriptor']
                         and actual in self.target['source_keys'])
            row = dict(row, entry_bound=bool(row.get('entry_bound') and match))
        return super().observe(row)
