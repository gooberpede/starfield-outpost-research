# Explicit archived evidence access

Cargo retirement and baseline activation were separately authorized and
[executed](../../docs/experiments/cargo-evidence-cutover/execution.md) on
2026-10-26. Routine Cargo checks now use the
[active selection](../../docs/experiments/cargo-evidence-cutover/active-baseline.json)
and its pinned `routine_command`: archive/index plus three loose holds, with
zero retired-member payload hashes. Historical proposals/preparers below remain
available for inspection; they are not the current routine boundary. The
[original continuation brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_archived_evidence_resolution_cargo_cutover.md`)
retains its earlier implementation-only authority. Use installed CPython 3.14 with `-B`
from the repository root; no installation, network or game operation is needed.

| Method | Reads and prerequisites | Writes and effects |
|---|---|---|
| `access.py locate --member ORIGINAL` | Exact original relative path, externally expected index/archive/inventory hashes, current source if present | JSON locator on stdout; changed loose bytes fail rather than trigger fallback |
| `access.py verify` | Authenticated index, archive and complete embedded inventory | Deep verification result on stdout; every member checked |
| `access.py verify --routine` | Same pinned index/archive objects, canonical inventory metadata | Hashes index/archive bytes once each; zero member payload hashes; proposed routine mode only |
| `access.py restore --destination FRESH_PATH [--member ORIGINAL ... or --experiment NAME]` | Authenticated full archive; exact member set or one of five Cargo experiment names | Fresh disposable tree, original relative paths, flushed regular files, `LEASE.json`; no execution |
| `access.py cleanup --destination PATH --lease-sha256 DIGEST` | Independently retained lease digest, archive and unchanged restored members | Removes only the exact disposable lease files and empty directories; refuses unknown outputs, changed bytes and hazardous paths |
| `access.migrate(before, retired, store, expected_before)` | Versioned caller-pinned full Cargo baseline and exact retired subset | Pure in-memory shadow proposal; does not change any current verification utility |
| `access.rollback(shadow, expected_before)` | Independently retained prior-baseline digest | Exact prior rows; caller must still verify surviving originals before any future activation |
| `retirement.prepare(...)` | Externally pinned exact allowlist and recovery receipt, archive and every current source | Dry-run decision only; no delete function or real journal writer |
| `qualify.py` | Installed stdlib, owned Stage B packager, Windows APIs | Fresh synthetic fixtures/results under ignored task and Stage B roots; modifies/deletes its own synthetic data only |
| `pilot.py --label NAME` | Exact frozen 1,054 sources, Cargo archive/index, authored text, prior baseline metadata | Fresh census, allowlist, shadow baseline, full disposable restore, consumer outputs, allocation/read/timing receipts; no originals changed |

Cargo trust roots are defaults copied from the independently reviewed Stage B
decision record, not discovered from the candidate index. `--index`,
`--index-sha256`, `--archive-sha256` and `--manifest-sha256` accept a separately
authenticated version for deliberate testing. Never refresh expected values
from an unknown candidate to make verification pass. Paths, owner and version
must agree exactly; case aliases, ambiguous paths and missing members fail.

For example, from PowerShell:

```powershell
$cargoPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $cargoPython -B research/evidence-access/access.py verify
& $cargoPython -B research/evidence-access/access.py locate --member .local-work/c1-cargo/WorkshopTargetMenu.swf
& $cargoPython -B research/evidence-access/access.py restore --experiment c1-cargo --destination D:/Projects/starfield-outpost-research/.local-work/cargo-evidence-cutover/example-lease
```

Retain the returned `lease_sha256` independently. Feed that lease to
`research/c1-cargo/menu_abc.py` or `research/c2-transport/pex.py` with the existing
`--run` argument and all three explicit options: `--evidence-lease PATH`,
`--lease-sha256 DIGEST`, `--output-directory FRESH_PATH`. The output directory
must be separate from the lease, beneath `.local-work/cargo-evidence-cutover/`.
The lease is reauthenticated against archive membership and reread before use.
Default historical CLI behavior remains available while originals survive.

Only those two payload workflows are qualified here. Restoring an old acquisition,
native launcher, documentation writer or packager does not authorize running it.
The frozen admission verifiers still require their original HEAD/index and
external prerequisites. Their historical identity failures are preserved.

Leases expire when that explicit analysis finishes. They are not added to the
mandatory preservation baseline. Keep the digest and recovery receipt, then run
`cleanup` while source/archive verification remains available. Unknown outputs
or an interrupted cleanup require explicit reconciliation; there is no recursive
fallback cleanup or automatic recovery of missing evidence. Interrupted restores
remain quarantined `.partial-...` trees and cannot be opened as completed leases.
Start a fresh named restoration; do not infer completion from a directory name.

Safety depends on exclusive ownership of ancestor directories and trustworthy
Windows/kernel behavior. Locked handles deny concurrent source write/delete;
the implementation rejects reparse ancestors, hardlinks and alternate streams.
Process-interruption tests do not establish actual power-loss survival. Restored
metadata is newly assigned; source timestamps, ACLs, streams and executable
permissions are not imported. D: is authoritative storage; C: is not used for a
permanent replica. Both-drive 40,000,000,000-byte guards apply before writes.

Provenance: owned Stage B `engine.py` supplies locked handles, strict index loading
and source checks; owned Stage A `archive.py` supplies path/tar validation and
space guards. Both are reused under SOR-P-0002 with exact hashes in the pilot
receipt. `pilot.py`, the access/lease/baseline adapter and tests are project-authored
stdlib/Windows work. CPython and Git are existing tools; Bethesda-derived restored
assets and reports remain local-only. See the [report](../../docs/experiments/cargo-evidence-cutover/report.md)
and [recovery procedure](../../docs/experiments/cargo-evidence-cutover/recovery.md).
