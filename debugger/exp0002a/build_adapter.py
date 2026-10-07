# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline build only. Reads local sources/plan/version and installed MSVC/SDK.
Writes create-new ignored build folder, generated identity header, EXEs/OBJ/log
and manifest. No downloads, game access, launch, attachment or deployment.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VCVARS = Path(r"C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_window(path, name=b"Request"):
    data = path.read_bytes()
    pe = struct.unpack_from("<I", data, 0x3c)[0]
    sections = struct.unpack_from("<H", data, pe+6)[0]
    opt_size = struct.unpack_from("<H", data, pe+20)[0]
    assert struct.unpack_from("<H", data, pe+24)[0] == 0x20b
    section_start = pe+24+opt_size

    def offset(rva):
        for index in range(sections):
            row = section_start+40*index
            virtual_size, start, raw_size, raw = struct.unpack_from("<IIII", data, row+8)
            if start <= rva < start+min(virtual_size, raw_size):
                return raw+rva-start
        raise ValueError("RVA outside section")

    export = offset(struct.unpack_from("<I", data, pe+24+112)[0])
    count = struct.unpack_from("<I", data, export+24)[0]
    funcs, names, ordinals = struct.unpack_from("<III", data, export+28)
    for index in range(count):
        text = offset(struct.unpack_from("<I", data, offset(names)+4*index)[0])
        if data[text:data.index(b"\0", text)] == name:
            ordinal = struct.unpack_from("<H", data, offset(ordinals)+2*index)[0]
            rva = struct.unpack_from("<I", data, offset(funcs)+4*ordinal)[0]
            return rva, hashlib.sha256(data[offset(rva):offset(rva)+32]).hexdigest()
    raise ValueError("missing fixture export")


def build(output):
    output = output.resolve()
    if not output.is_relative_to(ROOT/".local-work/exp0002a-adapter-0.1.3"):
        raise ValueError("build must remain in ignored adapter evidence root")
    output.mkdir()
    version = json.loads((HERE/"tooling_version.json").read_text(encoding="utf-8"))
    plan = json.loads((HERE/"next_capture_plan.json").read_text(encoding="utf-8"))
    assert plan["live_enabled"] and not plan["stage_c_enabled"]
    assert version["adapter_semver"] == "0.1.3"
    assert version["adapter_version_integer"] == 65539
    assert version["adapter_executable"] == "save_request_adapter-0.1.3.exe"
    assert plan["thread_scope"]["mode"] == "S1_NONE_OR_S2_SINGLE_EXISTING"
    sources = sorted([*HERE.glob("native/*"), HERE/"build_adapter.py", HERE/"qualify_controls.py",
                      HERE/"next_capture_plan.json", HERE/"tooling_version.json"])
    hashes = {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in sources}
    source_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()

    def compile_one(source, target):
        # Paths are local trusted filesystem inputs, batch-file quoted, never JSON shell escaping.
        command = output/f"build-{target}.cmd"
        command.write_text(
            f'@echo off\ncall "{VCVARS}"\nif errorlevel 1 exit /b %errorlevel%\n'
            f'cl /nologo /W4 /WX /O2 /EHsc /std:c++17 /I"{output}" "{source}" '
            f'/Fe:"{output/target}.exe" /Fo:"{output/target}.obj" '
            '/link /INCREMENTAL:NO bcrypt.lib\nexit /b %errorlevel%\n',
            encoding="utf-8")
        result = subprocess.run(["cmd.exe", "/d", "/c", str(command)], cwd=output,
                                capture_output=True, timeout=60)
        (output/f"build-{target}.log").write_bytes(result.stdout+result.stderr)
        if result.returncode:
            raise RuntimeError(f"build failed: {output/f'build-{target}.log'}")

    compile_one(HERE/"native/request_fixture.cpp", "request_fixture")
    fixture = output/"request_fixture.exe"
    rva, window = export_window(fixture)
    header = {
        "SOR_VERSION": version["adapter_semver"], "SOR_SOURCE_ID": source_id,
        "SOR_FIXTURE_SHA": sha(fixture), "SOR_FIXTURE_WINDOW": window,
        "SOR_GAME_SHA": plan["game_sha256"], "SOR_GAME_WINDOW": plan["sites"][0]["sha256"],
    }
    (output/"identity.h").write_text(
        "\n".join(f'#define {key} "{value}"' for key, value in header.items())+
        f"\n#define SOR_FIXTURE_RVA 0x{rva:x}ULL\n", encoding="utf-8")
    compile_one(HERE/"native/adapter.cpp", Path(version["adapter_executable"]).stem)
    manifest = dict(version=version["adapter_semver"], source_id=source_id,
                    adapter_executable=version["adapter_executable"], thread_scope=plan["thread_scope"]["mode"],
                    sources=hashes, live_enabled=True, plugin_built=False,
                    package_created=False, fixture_rva=hex(rva), fixture_window_sha256=window,
                    binaries={p.name: sha(p) for p in output.glob("*.exe")},
                    compiler_setup=str(VCVARS), compiler_setup_sha256=sha(VCVARS))
    (output/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    print(json.dumps(build(parser.parse_args().output), indent=2))
