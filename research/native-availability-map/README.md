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
