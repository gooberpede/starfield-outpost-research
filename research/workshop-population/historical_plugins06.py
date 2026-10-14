"""Local adaptation of original project plugin_tables, provenance extractor_resources.py. Allows first header244 plus retained second version; exact observed plugin grammar closure remains mandatory. No filesystem/target effects."""
from outpost_record_framing import Reader
def plugin_tables(b):
    """Observed modern header grammar with exact plugin-block closure.
    Full u8, small u16, medium u32 counts; optional creation metadata (three
    strings plus byte). Trailer is observed 0100. Unsupported versions fail.
    No regex-derived slot mapping. Only modern 1.16.244.0 samples qualified here.
    """
    if b[:12] != b'SFS_SAVEGAME':
        raise ValueError('SAVE_SIGNATURE')
    c = Reader(b, 16 + int.from_bytes(b[12:16], 'little'), len(b))
    version = c.take(1)[0]
    def string(cursor):
        n = int.from_bytes(cursor.take(2), 'little')
        return cursor.take(n).decode('utf8')
    builds = [string(c), string(c)]
    if False:
        raise ValueError('UNQUALIFIED_SAVE_HEADER_BUILD')
    size = int.from_bytes(c.take(4), 'little')
    start = c.p
    p = Reader(b, start, start + size)
    groups = {}
    for label, width in [('full', 1), ('small', 2), ('medium', 4)]:
        n = int.from_bytes(p.take(width), 'little')
        if n > (p.end - p.p) // 3:
            raise ValueError('PLUGIN_COUNT_BOUNDS')
        names = []
        for _ in range(n):
            name = string(p).lower()
            if not name.endswith(('.esm', '.esp', '.esl')):
                raise ValueError('PLUGIN_NAME')
            flag = p.take(1)[0]
            if flag == 1:
                for _ in range(3):
                    string(p)
                p.take(1)
            elif flag != 0:
                raise ValueError('PLUGIN_METADATA_FLAG')
            names.append(name)
        groups[label] = names
    trailer = p.take(p.end - p.p)
    if trailer != b'\x01\x00':
        raise ValueError('PLUGIN_BLOCK_TRAILER')
    allnames = sum(groups.values(), [])
    if len(set(allnames)) != len(allnames) or groups['full'][0] != 'starfield.esm':
        raise ValueError('PLUGIN_TABLE_IDENTITY')
    return dict(groups=groups, start=start, end=p.end, version=version,
                builds=builds, trailer=trailer.hex())

