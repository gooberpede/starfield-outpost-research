# Existing-reference grid procedure tools

Project-owned 0.4.0 offline qualification and future operational helpers under
the [brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_existing_reference_grid_oracle_integrated.md).
Use the [integrated card](../../docs/experiments/existing-reference-grid/run-card.md)
only after joint approval. No helper grants live authority.

| Tool | Reads / writes / dependencies and effect |
|---|---|
|prepare_lock.py|Exact build/archive/sources, historical 310-pin lock and on-disk executable; exclusive ignored lock. Stdlib and project helpers. No executable target calls, deployment or configuration.|
|qualify.py|Pinned sources/protected files; runs original disposable fixture controls, loads own DLL in Python to test startup refusal, runs project test suites; exclusive ignored receipts/logs. No game access or deployment.|
|procedure.py|Audits file hashes, save inventory and process names; future admission reads cooperative receipts and limited creation metadata; monitor writes exclusive ACK/STOP/monitor records to owned fresh session only. No target memory, launch, debugger, native-call synthesis, save/config writes.|
|environment.py|Cooperative module inventory and read-only configuration assessment; missing nonessential modules recorded. External module snapshot disabled. Stdlib/existing project helpers.|
|test_procedure.py/test_inventory.py|Disposable synthetic trees/fixtures under ignored new task directories, no installed game edits. 29 controls.|
|package.py|Read-only Git/index/HEAD and task files; ignored manifests/diffs and disposable plain D:/tools forward-apply trees. No staging/ref/network writes.|

Prerequisites: installed pinned CPython 3.14 and project helpers; candidate build
requires installed MSVC/MASM/Windows SDK. No dependency downloads. All writes
use the 40 GB both-drive guard. Source/header rights and tool limitations are in
the [report](../../docs/experiments/existing-reference-grid/report.md).

Repeat qualification from root with exact build directory:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' research/existing-reference-grid/qualify.py --build .local-work/native-oracle-040/builds/qualification-08 --out .local-work/existing-reference-grid/NEW-SUPPLEMENT
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' save-analysis/scripts/verify_position_v2.py --output .local-work/existing-reference-grid/NEW-FROZEN-REPLAY
```

Each output must be new. Existing receipts are preserved. `prepare_lock.py
--build BUILD --out NEW_LOCK` pins exact final sources. `package.py --baseline`
is only for the initial clean tracked baseline; never regenerate it to hide
changes. `package.py` exports/verifies both final patches. None of these are a
Starfield runtime test.

## Offline fallback provenance audit

[identity_provenance.py](identity_provenance.py) reads 38 installed ESM headers,
selected definition fields and four existing hash-pinned saves using project
readers; it writes only exclusive derivatives/scratch to a NEW ignored directory.
It checks source hashes before/after and both-drive 40 GB guards. Raw receipts
remain LOCAL-ONLY; the saved inline-marker scan is conditional, not exhaustive.
Prerequisites include retained source-pin receipts under `.local-work` specified
in the source. Reproduce from root with the explicit installed CPython:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/existing-reference-grid/identity_provenance.py --out .local-work/fallback-grid/NEW-IDENTITY-REPRO
```

[fallback_provenance.py](fallback_provenance.py) reads the explicit immutable
schema 4 session, common raw transport in sibling retained sessions and the
unchanged 23 predictions. It writes JSON to stdout only; use a new ignored
derivative via a byte-preserving subprocess capture. It reuses project
`live02_analysis`/`route_inspect` with source provenance in the
[report](../../docs/experiments/fallback-grid-provenance.md). No game, process,
native calls, save/database edits, dependency or network access. Both-drive
40 GB guard precedes analysis. An unknown older schema is disclosed, not decoded
under schema 4 assumptions. `test_fallback_provenance.py` uses literal synthetic
arithmetic expectations and local raw evidence for missing/duplicate/changed
boundary controls; synthetic tests are not native observations.

From repository root:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/existing-reference-grid/fallback_provenance.py .local-work/native-oracle-live/session-36756-82447437
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s research/existing-reference-grid -p 'test_*.py' -v
```

Operational helpers and historical cards retain their approved historical
limits. Before future reuse, review their configuration against the prospective
[continuation policy](../../WORKFLOW.md#scientific-experiment-continuation-and-health);
the existing 2 GiB automatic output threshold is not a new default or an approval
to execute. This assignment changes no deployed observer or operational helper.
