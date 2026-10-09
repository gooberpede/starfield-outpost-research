"""SPDX-License-Identifier: GPL-3.0-or-later
BCPS1 observation-only decoder. Stdlib; reads source, uses exclusive temporary
scratch, deletes scratch on success/failure. No aggregate semantic size cap.
Operational scratch/time budgets are explicit ResourceLimit errors. Mapped
output supports existing struct/find readers without a full Python byte copy.
"""
from contextlib import contextmanager
from pathlib import Path
import hashlib
import mmap
import shutil
import struct
import tempfile
import time
import zlib

BLOCK = 262144
IO_BLOCK = 65536
FREE = 40_000_000_000


class ResourceLimit(RuntimeError):
    pass


class CorruptSave(ValueError):
    pass


def disk_guard(scratch, reserve=0):
    for drive in {Path('C:/'), Path('D:/'), Path(scratch).resolve().anchor}:
        if shutil.disk_usage(drive).free - reserve < FREE:
            raise ResourceLimit('FREE_SPACE_BUDGET: ' + str(drive))


def header(f, deadline=None):
    """Validate physical feasibility before allocating; table is iterated."""
    if deadline is None:
        deadline = time.monotonic() + 1800
    f.seek(0, 2)
    physical = f.tell()
    f.seek(0)
    h = f.read(72)
    if len(h) != 72 or h[:8] != b'BCPS\1\0\0\0' or h[68:72] != b'ZIP ':
        raise CorruptSave('UNSUPPORTED_SIGNATURE')
    table, start, total, block = (struct.unpack_from('<Q', h, p)[0] for p in (8, 24, 32, 48))
    if table != 72 or block != BLOCK or total == 0:
        raise CorruptSave('UNSUPPORTED_HEADER_FIELDS')
    count = (total + block - 1) // block
    end = table + 4 * count
    if end > physical or not 0 <= start - end <= 15 or start % 16:
        raise CorruptSave('IMPOSSIBLE_TABLE_OR_ALIGNMENT')
    # Each stream needs at least one byte and must end on a 16-byte boundary.
    if count > (physical - start) // 16:
        raise CorruptSave('IMPOSSIBLE_STREAM_COUNT')
    p = start
    for i in range(count):
        if i % 1024 == 0 and time.monotonic() > deadline:
            raise ResourceLimit('HEADER_TIME_BUDGET')
        f.seek(table + 4 * i)
        n = int.from_bytes(f.read(4), 'little')
        if n == 0 or n > physical - p:
            raise CorruptSave('COMPRESSED_BOUNDS')
        p = (p + n + 15) // 16 * 16
        if p > physical:
            raise CorruptSave('PADDING_BOUNDS')
    if p != physical:
        raise CorruptSave('PHYSICAL_EOF')
    return dict(declared_decoded_size=total, block_size=block, streams=count,
                physical_bytes=physical, table_end=end, stream_start=start)


def physical_streams(path, first, last):
    """Selected physical spans, without accumulating the full size table."""
    with Path(path).open('rb') as f:
        info = header(f)
        if not 0 <= first <= last < info['streams']:
            raise CorruptSave('SELECTED_STREAM_BOUNDS')
        p = info['stream_start']
        for i in range(last+1):
            f.seek(72+4*i)
            n = int.from_bytes(f.read(4), 'little')
            if i >= first:
                yield dict(index=i, physical_start=p, compressed_bytes=n, logical_start=i*BLOCK)
            p = (p+n+15)//16*16


@contextmanager
def decoded_save(path, scratch, *, scratch_budget=None, seconds=1800, guard=disk_guard):
    """One chunk at a time; <=64KiB input and <=256KiB+1 decoded allocation.
    Scratch budget is optional; free-space reservation is always checked.
    Mapping is virtual address space, not a resident-memory guarantee for clients.
    Yield (read-only mmap, metrics); consumers must release views before exit.
    """
    began = time.monotonic()
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    with Path(path).open('rb') as f:
        info = header(f, began + seconds)
        total = info['declared_decoded_size']
        if scratch_budget is not None and total > scratch_budget:
            raise ResourceLimit('SCRATCH_BUDGET: requested=' + str(total))
        guard(scratch, total + IO_BLOCK)
        digest = hashlib.sha256()
        with tempfile.TemporaryFile(dir=scratch) as out:
            p = info['stream_start']
            for i in range(info['streams']):
                if time.monotonic() - began > seconds:
                    raise ResourceLimit('TIME_BUDGET')
                guard(scratch, total - out.tell() + IO_BLOCK)
                f.seek(72 + 4 * i)
                n = int.from_bytes(f.read(4), 'little')
                f.seek(p)
                remaining = n
                expected = min(BLOCK, total - i * BLOCK)
                produced = 0
                dec = zlib.decompressobj()
                signature = b''
                while remaining:
                    if time.monotonic() - began > seconds:
                        raise ResourceLimit('DECODE_TIME_BUDGET')
                    data = f.read(min(remaining, IO_BLOCK))
                    if not data:
                        raise CorruptSave('TRUNCATED_STREAM')
                    remaining -= len(data)
                    try:
                        raw = dec.decompress(data, expected - produced + 1)
                    except zlib.error as e:
                        raise CorruptSave('ZLIB_INTEGRITY: ' + str(e)) from e
                    produced += len(raw)
                    if produced > expected or dec.unconsumed_tail or dec.unused_data:
                        raise CorruptSave('EXPANSION_OR_TRAILING_DATA')
                    if i == 0 and len(signature) < 12:
                        signature += raw[:12-len(signature)]
                    out.write(raw)
                    digest.update(raw)
                    del raw, data
                if not dec.eof or produced != expected:
                    raise CorruptSave('STREAM_EOF_OR_LENGTH')
                if i == 0 and not signature.startswith(b'SFS_SAVEGAME'):
                    raise CorruptSave('DECODED_SIGNATURE')
                p = (p + n + 15) // 16 * 16
            if out.tell() != total:
                raise CorruptSave('DECODED_ACCOUNTING')
            out.flush()
            info.update(decoded_sha256=digest.hexdigest(), scratch_peak_bytes=total,
                        decoder_buffer_bound_bytes=IO_BLOCK + BLOCK + 1,
                        seconds=time.monotonic() - began)
            with mmap.mmap(out.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
                yield mapped, info
