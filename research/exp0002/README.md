# SOR-EXP-0002 offline preparation tools

These are original project-authored tools, not a game observer or deployable package. Authority and limitations are in the [experiment](../../docs/experiments/SOR-EXP-0002-outpost-membership-reload-location.md). This directory incorporates no third-party code. The later [native implementation](../../runtime/exp0002/README.md) separately uses the approved SFSE header; no dependency download or sibling implementation reuse. Use installed Python 3.14.3 and its standard library as a separate tool; no package installation. Source inputs/tool attribution: SOR-S-0104/0105/0112/0113 in [sources](../../docs/SOURCES.md).

## Reads, writes and prerequisites

| File | Reads | Writes / effects |
|---|---|---|
| `prepare.py` | Explicit protected save paths for metadata/hash/byte equality only; prior local recon baseline; exact executables; six selected archive script entries | CREATE_NEW JSON beneath ignored `.local-work/exp0002`; maximum 2 MiB/report; fsync; never parses a save, changes a source, opens a process or edits Ghidra |
| `capture_contract.py` | Caller-supplied records only; no runtime acquisition | Two local plan templates when run; callable validator and fixed-name checkpoint writer, 32 KiB/checkpoint, six names maximum; no overwrite/retry |
| `test_offline.py` | Authored modules and synthetic fixtures | Temporary files, cleaned by Python; bytecode cache ignored; no real saves/game inputs |
| `debugger-plan.json` | Nothing; declarative design | Declarative companion to runtime/exp0002/trace.cpp; this JSON executes nothing |

Run from the repository root. Python is `<python>` below; resolved local tool path/hash is in SOR-EV-0002. The original and backup paths are taken from local `integrity-before.json`, not committed filenames. Output basenames must be new; never erase old evidence to rerun.

```powershell
& <python> research/exp0002/prepare.py integrity --original <original> --backup <backup> --output integrity-new.json
& <python> research/exp0002/prepare.py pe --executable <pinned-game-executable> --output pe-new.json
& <python> research/exp0002/prepare.py coordinates --focused --binary <pinned-game-executable> <pinned-ck-executable> --archive <ContentResources.zip> --output coordinates-new.json
& <python> research/exp0002/test_offline.py
& <python> research/exp0002/capture_contract.py
```

Coordinates: at most 80 matches per executable/encoding and 100 lines per script entry; explicit truncation markers. Broad scan includes worldspace and biome terms; focused scan excludes those noisy terms. ASCII/UTF-16LE printable strings of 6–1024 characters only. Strings, decompiler types and labels are leads, never validated coordinates. Inputs should be independently pinned before scanning; only the `pe` command itself enforces the game hash. Save integrity checks record timestamps before/after each read; they do not lock against external writers. Stop if anything changes.

## Capture contract

`template()` defines the executable Python record schema. `validate()` checks its shape, identity-domain formatting, role restrictions, finite coordinate vectors, query timestamps and explicit evidence kind. Each field distinguishes OBSERVED, NULL_RESULT, UNAVAILABLE and NOT_APPLICABLE and carries a source. Position domains carry units/frame even when UNKNOWN. Record completion is structural, not a claim that scientific evidence is sufficient; all-unavailable records cannot answer the research question. This validator does not verify supplied values against a process.

`manifest()` creates the machine-readable sample plan with actual filenames, timestamps, sizes, hashes and profile left null. A2R is a runtime checkpoint only by default; no new A2R save is required. Future actual filenames and private identity data belong only in ignored manifests. This module provides no archive/copy command, so Gate A cannot accidentally begin post-live collection.

The bounded writer is a single-session prototype. It fsyncs complete JSON before return and rejects duplicate output files. It does not atomically guarantee evidence after power loss or qualify game-crash recovery. There is no runtime bridge or UI trigger; a future bridge must maintain these guarantees, add its own hash/profile attestation, and undergo review. Do not rename SYNTHETIC records to RUNTIME.

## Debugger design limitations

ASLR addition is tested with synthetic module bases. Actual module enumeration, byte validation in process, ABI qualification, hardware-breakpoint context management, selected-reference resolution, return-site correlation, independent timeout and detach remain unimplemented. A debugger logging recipe alone would not satisfy the five-second zero-hit bound. No runnable debugger script is supplied under a misleading claim of readiness.
