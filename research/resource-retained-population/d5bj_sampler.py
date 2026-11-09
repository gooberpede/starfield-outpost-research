# SPDX-License-Identifier: GPL-3.0-or-later
"""Replay the D5AQ-C1 numeric fixture from explicitly supplied local game files.

SOR-P-0002 lineage: D5AQ startup, D5S native keys/private page host and D5AQ
independent oracle. Only the listed PE pages are copied into this process.
The dispatcher, CRT import slots and definition lookup are private substitutes.
Run this as a disposable process. It reads local files and writes only stdout.
"""
import argparse
from collections import Counter
import csv
import ctypes as C
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import shutil
import stat
import struct
import sys
import types
import zlib

EXE = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ESM = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
BA2 = '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'
CRT = '3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9'
PYTHON = 'cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b'
ORACLE = '48e2c6dc6804c5b1d9ac4d9ceef01261aab2d62fc7667c6d7649a9921829d2ad'
CSV = 'f637e277c0acb00c930cdbb0b42a45abb86684b75ca21aa639dc17b63d31f953'
MEMBER = b'planetdata/biomemaps/feynman v.biom'
BIOM = 'bd06d24e8ca1788481f6a4388c0e262b863b8b376a521752cf3d286c69f23863'
FRAME = (0, (195, 109), (8, 0), (0, 0))
GRID = [(x, y) for x in range(-2, 12) for y in range(-2, 12)]
BASE = 0x140000000
PAGE = 4096
CODE = (
    0x1405de000, 0x14078d000, 0x14096e000, 0x14096f000, 0x142332000,
    0x142339000, 0x1434ca000, 0x14374d000, 0x14374e000,
)
DATA = (
    0x143a40000, 0x144f04000, 0x144f05000, 0x144f06000, 0x144f07000,
    0x145e91000, 0x145ea6000, 0x14881e000, 0x14882e000, 0x14882f000,
)
IMPORTS = {
    'cos': (0x1434ca8d6, 0x143a40570),
    'fmod': (0x1434ca960, 0x143a405c0),
    'atan2': (0x1434ca906, 0x143a40648),
}
BRANCHES = {'fma': 0x14374e650, 'nonfused': 0x14374dda0}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def regular(path):
    path = Path(os.path.abspath(path))
    if os.name == 'nt':
        require(len(path.drive) == 2 and path.drive[1] == ':', 'Use a local drive path')
        kernel = C.WinDLL('kernel32', winmode=0x800)
        kernel.GetDriveTypeW.argtypes = [C.c_wchar_p]
        require(kernel.GetDriveTypeW(path.anchor) in (2, 3), 'Use a local fixed or removable drive')
    for component in reversed((path, *path.parents)):
        try:
            identity = component.lstat()
        except FileNotFoundError:
            raise ValueError(f'Missing regular input file: {path}') from None
        require(not getattr(identity, 'st_file_attributes', 0) & 0x400
                and not stat.S_ISLNK(identity.st_mode), f'Reparse point in input path: {component}')
    require(stat.S_ISREG(identity.st_mode), f'Missing regular input file: {path}')
    return path


def authenticate(stream, expected, label):
    actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    require(actual == expected, f'{label} SHA-256 mismatch. Expected {expected}, got {actual}.')
    stream.seek(0)


def read_pinned(path, expected, label, *, keep=False):
    with regular(path).open('rb') as stream:
        authenticate(stream, expected, label)
        if keep:
            data = stream.read()
            require(digest(data) == expected, f'{label} changed while reading')
            return data


def read_exact(stream, size):
    data = stream.read(size)
    require(len(data) == size, 'Truncated PlanetData archive')
    return data


def raster_member(stream):
    magic, version, kind, count, names_at = struct.unpack('<4sI4sIQ', read_exact(stream, 24))
    length = stream.seek(0, os.SEEK_END)
    require((magic, version, kind) == (b'BTDX', 2, b'GNRL')
            and 0 < count < 10000 and 32 + 36 * count <= names_at < length,
            'Unsupported PlanetData archive header')
    stream.seek(32)
    entries = list(struct.iter_unpack('<I4sIIQIII', read_exact(stream, 36 * count)))
    stream.seek(names_at)
    matches = []
    for entry in entries:
        name_length, = struct.unpack('<H', read_exact(stream, 2))
        if read_exact(stream, name_length) == MEMBER:
            matches.append(entry)
    require(len(matches) == 1, 'Expected one exact Feynman V biome raster member')
    start, packed, size = matches[0][4:7]
    require(size == 655414 and packed <= 2_000_000
            and 32 + 36 * count <= start <= start + (packed or size) <= names_at,
            'Feynman V biome raster member bounds or size mismatch')
    stream.seek(start)
    data = read_exact(stream, packed or size)
    if packed:
        decoder = zlib.decompressobj()
        data = decoder.decompress(data, size + 1)
        require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
                'Feynman V biome raster decompression mismatch')
    require(len(data) == size and digest(data) == BIOM, 'Feynman V biome raster SHA-256 mismatch')
    return data


def faces(data):
    version, _, items = struct.unpack_from('<BBI', data)
    at = 6 + 4 * items
    require(version == 5 and at + 4 <= len(data), 'Unsupported biome raster header')
    require(struct.unpack_from('<I', data, at)[0] == 2, 'Expected two biome raster faces')
    at += 4
    masks = []
    for face in range(2):
        require(at + 16 + 5 * 65536 <= len(data), 'Truncated biome raster face')
        width, height, count = struct.unpack_from('<III', data, at)
        require((width, height, count) == (256, 256, 65536), 'Incompatible biome raster dimensions')
        if face == 0:
            tile = (255 - FRAME[1][1]) * width + FRAME[1][0]
            biome, = struct.unpack_from('<I', data, at + 12 + 4 * tile)
            require(biome == 0x145440, 'Wrong raster biome for the C1 source tile')
        at += 12 + 4 * count
        require(struct.unpack_from('<I', data, at)[0] == count, 'Biome raster mask count mismatch')
        at += 4
        masks.append(data[at:at + count])
        at += count
    require(at == len(data), 'Unexpected trailing biome raster data')
    return masks


def host_preflight():
    require(sys.flags.isolated and sys.dont_write_bytecode and not sys.flags.optimize
            and os.environ.get('PYTHONOPTIMIZE', '0') in ('', '0'), 'Invoke CPython with -I -B and no optimization')
    require(sys.platform == 'win32' and platform.machine() == 'AMD64'
            and C.sizeof(C.c_void_p) == 8 and sys.implementation.name == 'cpython'
            and sys.version_info[:3] == (3, 14, 3)
            and sys.getwindowsversion()[:3] == (10, 0, 19045),
            'Requires tested Windows 10 build 19045 and AMD64 CPython 3.14.3')
    read_pinned(sys.executable, PYTHON, 'CPython')
    kernel = C.WinDLL('kernel32', use_last_error=True, winmode=0x800)
    kernel.IsProcessorFeaturePresent.argtypes = [C.c_ulong]
    kernel.IsProcessorFeaturePresent.restype = C.c_int
    kernel.GetEnabledXStateFeatures.restype = C.c_uint64
    require(kernel.IsProcessorFeaturePresent(39) and kernel.GetEnabledXStateFeatures() & 6 == 6,
            'Host must enable AVX and SSE/YMM state')
    directory = C.create_unicode_buffer(32768)
    length = kernel.GetSystemDirectoryW(directory, len(directory))
    require(0 < length < len(directory), 'Cannot resolve Windows system directory')
    crt_path = Path(directory.value) / 'ucrtbase.dll'
    read_pinned(crt_path, CRT, 'System UCRT')
    kernel.VirtualAlloc.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.c_ulong]
    kernel.VirtualAlloc.restype = C.c_void_p
    kernel.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong, C.POINTER(C.c_ulong)]
    kernel.VirtualFree.argtypes = [C.c_void_p, C.c_size_t, C.c_ulong]
    kernel.GetCurrentProcess.restype = C.c_void_p
    kernel.FlushInstructionCache.argtypes = [C.c_void_p, C.c_void_p, C.c_size_t]
    return kernel, C.WinDLL(str(crt_path), winmode=0x800)


def protect(kernel, address, protection):
    old = C.c_ulong()
    require(kernel.VirtualProtect(address, PAGE, protection, C.byref(old)),
            f'Private page protection failed at {address:#x}')


def flush(kernel):
    require(kernel.FlushInstructionCache(kernel.GetCurrentProcess(), None, 0),
            'Private instruction cache flush failed')


def cpu_check(kernel):
    address = kernel.VirtualAlloc(None, PAGE, 0x3000, 4)
    require(address, 'Could not allocate private CPUID probe')
    try:
        # Read CPUID leaf 1 and return ECX while preserving the caller's RBX.
        probe = bytes.fromhex('53 b8 01 00 00 00 0f a2 89 c8 5b c3')
        C.memmove(address, probe, len(probe))
        protect(kernel, address, 0x20)
        flush(kernel)
        features = C.WINFUNCTYPE(C.c_uint32)(address)()
        required = (1 << 28) | (1 << 27) | (1 << 12)
        require(features & required == required, 'CPU must support AVX, OSXSAVE and FMA3')
        return features
    finally:
        require(kernel.VirtualFree(address, 0, 0x8000), 'CPUID page release failed')


def pe_sections(data):
    pe, = struct.unpack_from('<I', data, 0x3c)
    require(data[:2] == b'MZ' and data[pe:pe + 4] == b'PE\0\0', 'Invalid PE signature')
    machine, count = struct.unpack_from('<HH', data, pe + 4)
    options, = struct.unpack_from('<H', data, pe + 20)
    magic, = struct.unpack_from('<H', data, pe + 24)
    base, = struct.unpack_from('<Q', data, pe + 48)
    require((machine, count, options, magic, base) == (0x8664, 9, 0xf0, 0x20b, BASE),
            'Unexpected PE32+ section table or preferred image base')
    sections = []
    for at in range(pe + 24 + options, pe + 24 + options + count * 40, 40):
        name, virtual, rva, size, offset = struct.unpack_from('<8sIIII', data, at)
        flags, = struct.unpack_from('<I', data, at + 36)
        sections.append((name.rstrip(b'\0'), BASE + rva, virtual, size, offset, flags))
    return sections


def pe_pages(data, code=CODE, data_pages=DATA):
    sections = pe_sections(data)
    pages = {}
    for page in (*code, *data_pages):
        section = next((s for s in sections if s[1] <= page < s[1] + s[2]), None)
        require(section is not None, f'No qualified section for {page:#x}')
        name, start, virtual, size, offset, flags = section
        require((page in code and name == b'.text' and flags == 0x60000020
                 and page + PAGE <= start + min(size, virtual))
                or (page in data_pages and name in (b'.rdata', b'.data', b'_RDATA')
                    and not flags & 0x20000000 and page + PAGE <= start + virtual),
                f'Wrong PE section for {page:#x}')
        backed = max(0, min(PAGE, start + size - page))
        at = offset + page - start
        require(not backed or at + backed <= len(data), f'Truncated PE section for {page:#x}')
        pages[page] = data[at:at + backed].ljust(PAGE, b'\0')
    return pages


def allocate_pages(kernel, pages):
    for base in sorted({page & ~0xffff for page in pages}):
        require(kernel.VirtualAlloc(base, 65536, 0x2000, 4) == base,
                f'Preferred address unavailable at {base:#x}. Use a fresh process.')
    for page, data in pages.items():
        require(kernel.VirtualAlloc(page, PAGE, 0x1000, 4) == page,
                f'Private page commit failed at {page:#x}')
        C.memmove(page, data, PAGE)


def bind_imports(crt, imports):
    for name, (entry, slot) in imports.items():
        thunk = C.string_at(entry, 6)
        require(thunk[:2] == b'\xff\x25'
                and entry + 6 + struct.unpack_from('<i', thunk, 2)[0] == slot,
                f'Unexpected {name} import thunk')
        C.c_void_p.from_address(slot).value = C.cast(getattr(crt, name), C.c_void_p).value


def set_numeric_globals():
    # Return a null form override for the qualified interior reconstruction.
    C.memmove(0x1405de3b0, bytes.fromhex('31 c0 c3'), 3)
    C.c_uint32.from_address(0x145ea66f0).value = 10
    C.c_uint32.from_address(0x145ea6770).value = 2


def map_fixture(kernel, crt, pages):
    allocate_pages(kernel, pages)
    bind_imports(crt, IMPORTS)
    set_numeric_globals()
    for page in pages:
        protect(kernel, page, 0x20 if page in CODE else 2)
    flush(kernel)


def dispatch(kernel, branch):
    entry = 0x14374dcc0
    page = entry & ~(PAGE - 1)
    protect(kernel, page, 4)
    jump = struct.pack('<Bi', 0xe9, BRANCHES[branch] - entry - 5)
    C.memmove(entry, jump, len(jump))
    protect(kernel, page, 0x20)
    flush(kernel)


def put(buffer, at, fmt, value):
    struct.pack_into(fmt, buffer, at, value)


class NativeRaster:
    def __init__(self, masks):
        self.raster = C.create_string_buffer(0x30)
        self.faces = C.create_string_buffer(0x60)
        self.buffers = [C.create_string_buffer(mask) for mask in masks]
        put(self.raster, 0x18, '<Q', C.addressof(self.faces))
        for index, buffer in enumerate(self.buffers):
            struct.pack_into('<II', self.faces, index * 0x30, 256, 256)
            put(self.faces, index * 0x30 + 0x20, '<Q', C.addressof(buffer))

    def sample(self, sampler, angles):
        return sampler(C.addressof(self.raster), C.addressof(angles))


def numeric_fixture():
    manager = C.create_string_buffer(0x210)
    index = C.create_string_buffer(0x70)
    master = C.create_string_buffer(0x90)
    put(manager, 0x20, '<B', 2)
    put(manager, 0x120, '<Q', C.addressof(index))
    put(index, 0x58, '<Q', C.addressof(master))
    struct.pack_into('<III', master, 0x50, 256, 0, 86469)
    put(master, 0x5c, '<I', 5)
    for at, value in zip((0xc8, 0xcc, 0xd0, 0xdc, 0xe0, 0xec, 0xf0), (0, 195, 109, 8, 0, 0, 0)):
        put(manager, at, '<I', value)
    return manager, index, master


def callsite(address, arguments, result=C.c_void_p):
    return C.WINFUNCTYPE(result, *([C.c_void_p] * arguments))(address)


def verify_preimage(manager, master, angles):
    quantize = C.WINFUNCTYPE(C.c_void_p, C.c_void_p, C.c_void_p, C.c_uint32)(0x14096ecb0)
    snap = callsite(0x14096efb0, 3)
    center = callsite(0x14078d4b0, 3)
    descriptor = C.create_string_buffer(48)
    landing = C.create_string_buffer(48)
    local = (C.c_int32 * 2)()
    quantize(descriptor, angles, 256)
    snap(master, landing, angles)
    center(manager, local, angles)

    def decode(buffer):
        return [buffer.raw[0], *(struct.unpack_from('<i', buffer, at)[0] for at in (4, 8, 20, 24, 36, 40))]

    expected = [0, 195, 109, 8, 0, 0, 0]
    require(decode(descriptor) == decode(landing) == expected and list(local) == [0, 0],
            'Native numeric startup preimage mismatch')
    return {'quantized': decode(descriptor), 'snapped': decode(landing), 'center': list(local)}


def run_numeric(kernel, masks, expected, shifted):
    manager, index, master = numeric_fixture()
    raster = NativeRaster(masks)
    # Each synthetic face encodes one nibble of the 17-bit atlas index. Probe
    # the exact native sample address without patching the sampler or accepting
    # a coincidentally equal mask from an adjacent cell.
    probes = [NativeRaster([bytes((pixel >> shift) & 15 for pixel in range(face * 65536, (face + 1) * 65536))
                            for face in range(2)]) for shift in range(0, 20, 4)]
    convert = callsite(0x14078d660, 4)
    project = callsite(0x142332410, 2)
    sampler = callsite(0x142339340, 2, C.c_uint8)
    results = {}
    for branch in BRANCHES:
        dispatch(kernel, branch)
        rows = []
        for x, y in GRID:
            want = expected[x, y]
            query = (C.c_int32 * 2)(x, y)
            square = C.create_string_buffer(24)
            angles = (C.c_double * 2)()
            convert(manager, square, C.addressof(manager) + 0xc8, query)
            project(angles, square)
            mask = raster.sample(sampler, angles)
            pixel = sum(probe.sample(sampler, angles) << (4 * i) for i, probe in enumerate(probes))
            chart, offset = divmod(pixel, 65536)
            row, column = divmod(offset, 256)
            normalized = list(struct.unpack_from('<2d', square, 8))
            require([chart, column, row, mask, normalized]
                    == [want['chart'], want['column'], want['row'], want['mask'], want['normalized']]
                    and square.raw[0] == FRAME[0]
                    and all(map(math.isfinite, angles)),
                    f'Native atlas or converter mismatch at {branch} ({x}, {y})')
            rows.append({'query': [x, y], 'mask': mask, 'chart': chart, 'column': column,
                         'row': row, 'angles': list(angles), 'normalized': normalized})
            if (x, y) == (0, 0):
                preimage = verify_preimage(manager, master, angles)
        counts = dict(Counter(row['mask'] for row in rows))
        require(counts == {0: 28, 3: 168}, f'Native mask counts differ for {branch}')
        phase_masks = []
        put(manager, 0xf0, '<i', 1)
        for x, y in GRID:
            square = C.create_string_buffer(24)
            angles = (C.c_double * 2)()
            convert(manager, square, C.addressof(manager) + 0xc8, (C.c_int32 * 2)(x, y))
            project(angles, square)
            phase_masks.append(raster.sample(sampler, angles))
        put(manager, 0xf0, '<i', 0)
        require(phase_masks == shifted, f'Native fine Y +1 control differs for {branch}')
        phase_counts = dict(Counter(phase_masks))
        require(phase_counts == {0: 14, 3: 182}, 'Wrong changed-phase mask census')
        results[branch] = {'counts': counts, 'preimage': preimage, 'rows': rows, 'fine_y_plus_one': phase_counts}
    return results


def independent_oracle(masks):
    source = Path(__file__).with_name('d5aq_oracle.py')
    data = read_pinned(source, ORACLE, 'D5AQ oracle', keep=True)
    oracle = types.ModuleType('d5bj_d5aq_oracle')
    exec(compile(data, str(source), 'exec'), vars(oracle))
    path = Path(__file__).resolve().parents[2] / 'docs/experiments/resource-retained-population/d5aq-request-mask-map.csv'
    table = read_pinned(path, CSV, 'D5AQ coordinate table', keep=True)
    raster = {'faces': [{'mask': mask} for mask in masks]}
    rows = list(csv.DictReader(io.StringIO(table.decode('utf-8'))))
    require([(int(row['original_x']), int(row['original_y'])) for row in rows] == GRID,
            'D5AQ historical coordinate order or domain differs')
    expected = {}
    for query, row in zip(GRID, rows):
        value = oracle.sample(FRAME, query, raster)
        historical = {
            'chart': int(row['chart']), 'face': [int(row['face_x']), int(row['face_y'])],
            'normalized': [float(row['normalized_x']), float(row['normalized_y'])],
            'column': int(row['raster_column']), 'row': int(row['raster_row']),
            'byte': int(row['raster_byte'], 16), 'mask': int(row['mask'], 16),
        }
        require(value == historical, f'Independent atlas differs from D5AQ table at {query}')
        expected[query] = value
    fine = (0, FRAME[1], FRAME[2], (0, 1))
    shifted = [oracle.sample(fine, query, raster)['mask'] for query in GRID]
    changed = sum(shifted[i] != expected[query]['mask'] for i, query in enumerate(GRID))
    require(changed == 14, 'Fine Y phase control failed')
    return expected, shifted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--esm', type=Path, required=True)
    parser.add_argument('--planet-data', type=Path, required=True)
    args = parser.parse_args()
    try:
        kernel, crt = host_preflight()
        inputs = [regular(path) for path in (args.exe, args.esm, args.planet_data)]
        drives = {path.anchor for path in inputs} | {Path.cwd().anchor, Path(sys.executable).anchor}
        require(all(shutil.disk_usage(drive).free >= 40_000_000_000 for drive in drives),
                'Keep 40,000,000,000 caller-available bytes on each involved volume')
        exe, esm, archive = inputs
        pages = pe_pages(read_pinned(exe, EXE, 'Starfield EXE', keep=True))
        read_pinned(esm, ESM, 'Starfield main ESM')
        with archive.open('rb') as stream:
            authenticate(stream, BA2, 'PlanetData archive')
            masks = faces(raster_member(stream))
        expected, shifted = independent_oracle(masks)
        features = cpu_check(kernel)
        map_fixture(kernel, crt, pages)
        results = run_numeric(kernel, masks, expected, shifted)
    except (OSError, ValueError, AttributeError, struct.error, zlib.error) as error:
        parser.exit(1, f'D5BJ sampler refused: {error}\n')
    print(json.dumps({
        'scope': 'D5AQ-C1 conditional native numeric replay with supplied fixture state',
        'inputs': {'exe': EXE, 'main_esm_identity_only': ESM, 'planet_data': BA2, 'biome_member': BIOM},
        'host': {'python': PYTHON, 'ucrt': CRT, 'windows_build': 19045, 'cpuid_1_ecx': features},
        'code_pages': {hex(page): digest(pages[page]) for page in CODE},
        'data_pages': {hex(page): digest(pages[page]) for page in DATA},
        'independent_oracle': ORACLE, 'historical_coordinate_table': CSV, 'fine_y_plus_one_changed': 14,
        'branches': results,
    }, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
