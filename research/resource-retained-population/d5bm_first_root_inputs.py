# SPDX-License-Identifier: GPL-3.0-or-later
"""Project the first C1 layer root and all four density requests as data.

Reuses the owned C1 source census, archive reader and main-file BIOM reader.
Runs no game instructions and does not establish native file acquisition,
cache residency or an installed scheduler dependency.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d5bj_sampler as host
from d5bj_sources import ANCHOR, inventory
import d5bm_files as files
from d5bm_tags import BIOME, SHAPE, load_groups

BOUNDS = (-16, -16, 23, 23)
NEIGHBORS = ((-1, 1), (-1, 0), (0, 1), (1, 1))
ROOT = files.ROOT_INT2
REQUESTS = (ROOT, *((ROOT[0] + x, ROOT[1] + y) for x, y in NEIGHBORS))
ROOT_SOURCES = files.FOOTPRINTS[ROOT]
NEIGHBOR_SOURCES = files.FOOTPRINTS[files.DENSITY_INT2]
EXPECTED_FOOTPRINTS = (ROOT_SOURCES, NEIGHBOR_SOURCES, ROOT_SOURCES, NEIGHBOR_SOURCES, NEIGHBOR_SOURCES)


def footprints(sources):
    x_min, y_min, x_max, y_max = BOUNDS
    host.require(ROOT == (x_min, y_max) and REQUESTS[1] == files.DENSITY_INT2,
                 "Unexpected first native root or neighbor")
    host.require(not any(x_min <= x <= x_max and y_min <= y <= y_max for x, y in REQUESTS[1:]),
                 "Selected layer root has an in-bounds recursive neighbor")
    result = []
    for coord, expected in zip(REQUESTS, EXPECTED_FOOTPRINTS, strict=True):
        x, y = (anchor + delta for anchor, delta in zip(ANCHOR, coord, strict=True))
        observed = tuple(sorted((sx, sy, fid) for (sx, sy, fid), (width, height, *_) in sources.items()
                                if -2 <= x - sx < width + 2 and -2 <= y - sy < height + 2))
        host.require(observed == expected, f"Unexpected projected contributors for {coord}")
        result.append(observed)
    return result


def project(sources, groups, projected, members):
    selected = footprints(sources)
    host.require(tuple((name, len(rows)) for name, rows in groups.items()) == SHAPE,
                 "Unexpected authenticated tag groups")
    host.require({fid for _, _, fid in ROOT_SOURCES} == set(projected),
                 "Projected file source roster mismatch")
    for names in projected.values():
        host.require(len(names) == len(groups)
                     and all(name in members and name.endswith(f"_{tag.lower()}.dds")
                             for tag, name in zip(groups, names, strict=True)),
                     "Projected file roster differs from selected BIOM tag order")
    host.require(len({member.archive_key for member in members.values()}) == len(members),
                 "Archive key aliases distinct candidate names")

    root_keys = set()
    rows = []
    for index, (coord, contributors) in enumerate(zip(REQUESTS, selected, strict=True)):
        names = tuple(dict.fromkeys(name for _, _, fid in contributors for name in projected[fid]))
        keys = {members[name].archive_key for name in names}
        if index == 0:
            root_keys = keys
        else:
            host.require(keys and keys <= root_keys, f"Projected neighbor has a key absent from the root: {coord}")
        rows.append({
            "kind": "layer_root_file_request" if index == 0 else "density_neighbor_file_request",
            "int2": coord,
            "footprint_sources": contributors,
            "candidate_members": names,
            "candidate_archive_keys": [members[name].archive_key for name in names],
        })
    return {
        "scope": "Static first-root file and tag projection",
        "biom_formid": f"{BIOME:#010x}",
        "bounds": BOUNDS,
        "gnam_groups": [{"tag": tag, "row_count": len(group), "sha256": host.digest(b"".join(group))}
                        for tag, group in groups.items()],
        "requests": rows,
        "root_unique_key_count": len(root_keys),
        "new_neighbor_key_counts": [0] * len(NEIGHBORS),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--esm", required=True, type=Path)
    parser.add_argument("--planet-data", required=True, type=Path)
    parser.add_argument("--density-maps", required=True, type=Path)
    args = parser.parse_args()
    try:
        projected, members = files.load(args.esm, args.planet_data, args.density_maps)
        sources, _ = inventory(args.esm)
        groups = load_groups(args.esm)
        result = project(sources, groups, projected, members)
    except (OSError, ValueError, struct.error, zlib.error) as error:
        parser.exit(1, f"D5BM first-root inputs refused: {error}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
