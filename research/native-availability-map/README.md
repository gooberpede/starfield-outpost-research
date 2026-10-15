# Local native availability mapping

Offline continuation of SOR-EXP-0034 / SOR-EV-0042, using SOR-EV-0043.
[Authorized brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_local_inorganic_availability_native_mapping_corrected.md).
[Report and contracts](../../docs/experiments/native-availability-map/report.md).

`verify.py` reads the structured function register, existing local native exports,
their pinned instruction windows, and the installed executable (hash only). It
checks build/base, original names/RVAs, source identity and the distinct cache,
caller-argument and provider dependencies. It also runs the existing availability
and spatial tests. These are static transcription and synthetic controls, not
execution of recovered native functions. Inputs are read-only; output is one
exclusive ignored JSON receipt. Dependencies: installed CPython 3.14.3 stdlib and
owned project tests. No download, process access, save/analysis-project effects.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/native-availability-map/verify.py --run checks01
```

`export-review-package.py` is an adaptation of the project's Milestone B exporter
at the task's recorded HEAD. It reads Git and authored text, writes exclusive
ignored patches/manifests and disposable D:/tools apply trees, and checks exact
forward/reverse reconstruction. It does not stage or modify Git refs/index.
Its baseline is `.local-work/native-availability-map/baseline.json`.

Original exports/captures remain local and are not copied into deliverables.
The full-capture census reuses `research/resource-availability-milestone-b/coverage.py`
with a new output directory. Preserve the 40,000,000,000-byte guard on C: and D:.
Stop affected processing on missing input, pin mismatch, malformed evidence or
guard failure; preserve failures and originals. No cleanup of protected evidence.

## Resource-region continuation

[Authorized contract](../../docs/experiments/native-availability-map/region-contract.md)
and [report](../../docs/experiments/native-availability-map/region-dependencies.md).
`verify-region-dependencies.py --run NAME` uses only Python stdlib, reads the
additional pinned exports and checks focused instruction/decompilation assertions.
It exclusively creates `.local-work/resource-region-dependencies/NAME.json`.
Run existing `verify.py --run region-dependencies01` for executable/source/register
pins and availability/spatial regressions, then the new checker. Existing verifier
receipts remain in `.local-work/native-availability-map/`; the continuation
checker/packaging/preservation receipts use their separate local directory.
No script invokes native game code or modifies a save/analysis project.

The existing owned preservation and exporter helpers are adapted locally from
baseline HEAD `6475a1fb4a70711d3035e2c89a05085b9b57f5b4`, with only task-local
base and patch-prefix changes. They remain ignored; hashes and exact commands
are in continuation validation. The initial attribution baseline contains only
the user-supplied brief; authored files created while the input hash audit ran
are correctly task changes. Disposable apply trees remain in D:/tools, with no
working-tree apply or index mutation.
