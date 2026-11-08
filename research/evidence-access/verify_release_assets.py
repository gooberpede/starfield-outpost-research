"""Verify a D5BF ledger and explicitly supplied local assets, without extraction."""

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
import zlib
from pathlib import Path


ASSET_IDS = {"B4-F1-CORE", "B4-F1-ADDENDUM", "D5AS", "C19"}
ZIP_CODECS = {"ZIP_STORED": zipfile.ZIP_STORED, "ZIP_DEFLATED": zipfile.ZIP_DEFLATED}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate key or asset argument: {key}")
        result[key] = value
    return result


def safe_parts(name):
    parts = name.split("/")
    for part in parts:
        require(re.fullmatch(r"[A-Za-z0-9_.-]+", part)
                and not part.endswith(".")
                and not re.fullmatch(r"CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9]",
                                     part.split(".")[0], re.IGNORECASE),
                f"unsafe member or asset path: {name!r}")
    return parts


def check_paths(names):
    occupied = set()
    directories = {}
    for name in names:
        parts = safe_parts(name)
        folded = name.lower()
        require(folded not in occupied, f"duplicate or case-colliding path: {name!r}")
        occupied.add(folded)
        for index in range(1, len(parts)):
            prefix = "/".join(parts[:index])
            first = directories.setdefault(prefix.lower(), prefix)
            require(first == prefix, f"case-colliding directory: {prefix!r}")
    require(not occupied.intersection(directories), "file/directory path collision")


def check_pin(pin, label):
    require(type(pin["bytes"]) is int and pin["bytes"] > 0
            and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), f"invalid pin: {label}")


def verify_stream(stream, pin, label):
    digest = hashlib.sha256()
    size = 0
    while chunk := stream.read(1024 * 1024):
        size += len(chunk)
        require(size <= pin["bytes"], f"byte count exceeds pin: {label}")
        digest.update(chunk)
    require(size == pin["bytes"], f"byte count mismatch: {label}")
    require(digest.hexdigest() == pin["sha256"], f"SHA-256 mismatch: {label}")


def verify_zip(stream, asset):
    members = asset["members"]
    with zipfile.ZipFile(stream) as archive:
        entries = archive.infolist()
        check_paths(entry.orig_filename for entry in entries)
        actual = {entry.orig_filename for entry in entries}
        require(actual == members.keys(),
                f"member set mismatch: missing={sorted(members.keys() - actual)}, "
                f"unexpected={sorted(actual - members.keys())}")
        for entry in entries:
            name = entry.orig_filename
            mode = stat.S_IFMT(entry.external_attr >> 16)
            require(entry.filename == name and mode in (0, stat.S_IFREG)
                    and not entry.external_attr & 0x10 and not entry.flag_bits & 1,
                    f"member is not an ordinary unencrypted file: {name!r}")
            require(entry.compress_type == ZIP_CODECS[asset["codec"]],
                    f"member codec mismatch: {name!r}")
            require(entry.file_size == members[name]["bytes"],
                    f"declared member size mismatch: {name!r}")
            with archive.open(entry) as member:
                verify_stream(member, members[name], name)


def verify_asset(path, asset):
    basename = asset["basename"]
    members = asset["members"]
    require(len(safe_parts(basename)) == 1 and path.name == basename,
            f"asset basename mismatch: expected {basename!r}, got {path.name!r}")
    check_pin(asset, basename)
    require(type(asset["member_count"]) is int and asset["member_count"] == len(members)
            and bool(members), f"ledger member count mismatch: {basename}")
    check_paths(members)
    for name, member in members.items():
        check_pin(member, name)

    with path.open("rb") as stream:
        verify_stream(stream, asset, basename)
        if asset["codec"] in ZIP_CODECS:
            verify_zip(stream, asset)
        else:
            require(asset["codec"] == "UTF-8 JSON" and set(members) == {basename},
                    f"invalid single-file asset inventory: {basename}")
            require(all(members[basename][key] == asset[key] for key in ("bytes", "sha256")),
                    f"single-file member pin differs from asset pin: {basename}")
            stream.seek(0)
            json.loads(stream.read().decode("utf-8"), object_pairs_hook=unique_pairs)
        # Bind the member check to the same opened file and check it again after reading.
        stream.seek(0)
        verify_stream(stream, asset, basename)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--asset", nargs=2, metavar=("ID", "PATH"), action="append", required=True)
    args = parser.parse_args()
    try:
        with args.ledger.open(encoding="utf-8") as stream:
            ledger = json.load(stream, object_pairs_hook=unique_pairs)
        require(ledger["schema"] == "sor-d5bf-release-assets/1", "unsupported ledger schema")
        assets = ledger["assets"]
        paths = unique_pairs(args.asset)
        require(assets.keys() == ASSET_IDS, "ledger must declare exactly the four D5BF asset IDs")
        require(paths.keys() == ASSET_IDS, "supply exactly one path for each of the four D5BF assets")
        check_paths(asset["basename"] for asset in assets.values())
        checked = []
        for asset_id, asset in assets.items():
            verify_asset(Path(paths[asset_id]), asset)
            checked.append({"id": asset_id, **{key: asset[key] for key in
                            ("basename", "bytes", "sha256", "member_count")}})
    except (OSError, ValueError, KeyError, TypeError, AttributeError, zipfile.BadZipFile,
            RuntimeError, EOFError, zlib.error) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"result": "PASS", "assets": checked}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
