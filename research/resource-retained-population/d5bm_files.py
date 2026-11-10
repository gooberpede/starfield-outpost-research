# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate D5BM's first root and density-neighbor file inputs as data.

Reuses the owned D5BJ C1 source census and raster reader under SOR-P-0002.
Reads explicit local ESM and BA2 files. No extraction to disk or game code.
The projection supplies candidate members, separate from live tag/key/handle
qualification. Archive directory words identify the archive record domain.
"""
import argparse
from dataclasses import dataclass
import json
from pathlib import Path, PureWindowsPath
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
from d5bj_sources import ANCHOR, inventory

ARCHIVE = "5e848b813df9a278b0b080f9b14f1b764cc25b9082944049510a652ad626b13b"
ROOT_INT2 = (-16, 23)
DENSITY_INT2 = (-17, 24)
FOOTPRINTS = {
    ROOT_INT2: ((37512, 20940, 0x0024EF60), (37512, 20952, 0x00257F2C)),
    DENSITY_INT2: ((37512, 20952, 0x00257F2C),),
}
EXPECTED_LABELS = ("Talus", "FlatOuter", "Flow", "FlatInner")


@dataclass(frozen=True)
class Member:
    name: str
    index: int
    archive_key: tuple
    body: bytes

    def receipt(self):
        return {
            "name": self.name,
            "index": self.index,
            "archive_key": self.archive_key,
            "decoded_size": len(self.body),
            "decoded_sha256": host.digest(self.body),
        }


def source_fields(esm, ids):
    from inspect_outpost_definitions import esm_records

    found = {}
    for header, fields in esm_records(esm, {b"SFBK", b"BIOM"}, repeated=True):
        fid = header["formid"]
        if fid in ids:
            host.require(fid not in found, f"Duplicate definition {fid:#x}")
            found[fid] = (header["type"], fields)
    host.require(found.keys() == ids, "Missing expected C1 definitions")
    return found


def member_prefix(raw_anam):
    terrain = PureWindowsPath(raw_anam.rstrip(b"\0").decode("ascii"))
    parts = terrain.parts
    host.require(len(parts) >= 3 and parts[:2] == ("Data", "TERRAIN")
                 and terrain.suffix.lower() == ".btd" and ".." not in parts,
                 "Unexpected main-file terrain path")
    return "/".join(("textures", "terrain", *parts[2:-1], terrain.stem)).lower()


def read_members(archive, prefixes):
    with host.regular(archive).open("rb") as stream:
        host.authenticate(stream, ARCHIVE, "Starfield DensityMaps archive")
        magic, version, kind, count, names_at = struct.unpack("<4sI4sIQ", host.read_exact(stream, 24))
        end = stream.seek(0, 2)
        table_end = 32 + 36 * count
        host.require((magic, version, kind, count) == (b"BTDX", 2, b"GNRL", 7761)
                     and table_end <= names_at < end, "Unexpected DensityMaps archive header")
        stream.seek(32)
        records = list(struct.iter_unpack("<I4sIIQIII", host.read_exact(stream, 36 * count)))
        stream.seek(names_at)
        selected = {}
        for index in range(count):
            size, = struct.unpack("<H", host.read_exact(stream, 2))
            host.require(0 < size < 512, "Invalid density member name length")
            name = host.read_exact(stream, size).decode("ascii")
            if any(name.startswith(prefix + "_") for prefix in prefixes):
                host.require(name.endswith(".dds") and name not in selected,
                             "Invalid or repeated selected DensityMaps name")
                selected[name] = index
        host.require(stream.tell() == end, "Unexpected DensityMaps name table extent")
        members = {}
        for name, index in selected.items():
            stem_hash, extension, directory_hash, _, offset, packed, size, _ = records[index]
            host.require(extension == b"dds\0" and size == 980_128 and packed <= 2_000_000
                         and table_end <= offset <= offset + (packed or size) <= names_at,
                         f"Invalid selected member bounds: {name}")
            stream.seek(offset)
            body = host.read_exact(stream, packed or size)
            if packed:
                decoder = zlib.decompressobj()
                body = decoder.decompress(body, size + 1)
                host.require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
                             f"Malformed selected member: {name}")
            host.require(len(body) == size and body.startswith(b"DDS ")
                         and struct.unpack_from("<I", body, 4)[0] == 124
                         and struct.unpack_from("<I", body, 76)[0] == 32,
                         f"Invalid DDS framing: {name}")
            members[name] = Member(name, index, (stem_hash, int.from_bytes(extension, "little"),
                                                  directory_hash), body)
        stream.seek(0)
        host.authenticate(stream, ARCHIVE, "Starfield DensityMaps archive after member read")
        return members


def load(esm, planet, archive):
    esm = host.regular(esm)
    sources, _ = inventory(esm)
    for coord, expected in FOOTPRINTS.items():
        x, y = (anchor + delta for anchor, delta in zip(ANCHOR, coord))
        actual = sorted(key for key, (width, height, *_) in sources.items()
                        if -2 <= x - key[0] < width + 2 and -2 <= y - key[1] < height + 2)
        host.require(tuple(actual) == expected, f"C1 footprint mismatch for {coord}")
    with host.regular(planet).open("rb") as stream:
        host.authenticate(stream, host.BA2, "Starfield PlanetData archive")
        raster = host.raster_member(stream)
    host.faces(raster)
    _, _, count = struct.unpack_from("<BBI", raster)
    biomes = {}
    for x, y, fid in FOOTPRINTS[ROOT_INT2]:
        tile = (255 - y // 192) * 256 + x // 192
        biomes[fid], = struct.unpack_from("<I", raster, 6 + 4 * count + 4 + 12 + 4 * tile)
    host.require(set(biomes.values()) == {0x00145440}, "Unexpected selected source biome")
    definitions = source_fields(esm, set(biomes) | set(biomes.values()))
    prefixes = {}
    for fid in biomes:
        kind, fields = definitions[fid]
        anam = [value for key, value in fields if key == b"ANAM"]
        host.require(kind == "SFBK" and len(anam) == 1, "Unexpected C1 source definition")
        prefixes[fid] = member_prefix(anam[0])
    kind, fields = definitions[0x00145440]
    labels = tuple(value.rstrip(b"\0").decode("ascii") for key, value in fields if key == b"FNAM")
    host.require(kind == "BIOM" and labels == EXPECTED_LABELS, "Unexpected C1 biome labels")
    host.read_pinned(esm, host.ESM, "Starfield main ESM after density definition read")
    members = read_members(archive, set(prefixes.values()))
    projected = {fid: tuple(f"{prefix}_{tag.lower()}.dds" for tag in labels)
                 for fid, prefix in prefixes.items()}
    host.require(all(name in members for names in projected.values() for name in names),
                 "A projected C1 density member is missing")
    return projected, members


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--esm", required=True, type=Path)
    parser.add_argument("--planet-data", required=True, type=Path)
    parser.add_argument("--density-maps", required=True, type=Path)
    args = parser.parse_args()
    try:
        projected, members = load(args.esm, args.planet_data, args.density_maps)
    except (OSError, ValueError, struct.error, zlib.error) as error:
        parser.exit(1, f"D5BM density inputs refused: {error}\n")
    print(json.dumps({
        "scope": "Static C1 file-member projection; no live key or handle qualification",
        "esm_sha256": host.ESM,
        "planet_data_sha256": host.BA2,
        "density_maps_sha256": ARCHIVE,
        "requests": [{"int2": coord, "source_candidates": sources} for coord, sources in FOOTPRINTS.items()],
        "fnames_by_source": projected,
        "members": [member.receipt() for member in members.values()],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
