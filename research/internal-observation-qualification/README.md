# Disposable internal-observation qualification

Original project-owned fixture, GPL-3.0-or-later. Governing
[brief](../../docs/implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_internal_observation_offline_qualification.md`),
[report](../../docs/experiments/spatial-equivalence-feasibility/offline-qualification/report.md)
and [contract](../../docs/experiments/spatial-equivalence-feasibility/offline-qualification/contract.md).
This directory is offline engineering material, not an observer or reusable hook library.

Requires Windows x64 with OS-enabled AVX, installed MSVC/MASM/Windows SDK and
CPython. No installation, network, external code or SFSE is needed. Microsoft
headers/runtime are existing build-tool inputs; no outside implementation is
copied into authored sources. Invoke from the repository root:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/internal-observation-qualification/static_contract.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/internal-observation-qualification/build.py --name my-disposable-run
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/internal-observation-qualification/verify.py .local-work/internal-observation-qualification/my-disposable-run/geometry.bin
```

`build.py` reads its four native/build sources and installed compiler setup,
generates original assembly, snapshots sources, compiles and executes **only its
own fixture.exe**, and writes a new exclusive directory beneath ignored
`.local-work/internal-observation-qualification/`. It patches two one-byte sites
in that process's own original text, installs a process-local exception handler,
uses disposable allocations/threads and guarded failing reads, restores its
sites after worker quiescence and exits. Unexpected API/test failure is a failed
fixture, never authorization to touch another process. Assertions and output
write failures stop the disposable process. Its OS resources die with that process.
It does not open a game process, load game code, change executable files, query
Vortex, modify saves/configuration or change analysis projects.

`static_contract.py` reads the installed executable as data and an existing
pinned export. It checks three instruction hashes/continuations and 12 export
facts, writing only a local JSON receipt without native bytes. `verify.py` reads
owned synthetic binary records and imports the unchanged frozen Python evaluator;
it writes `decode.json` beside the input, including exact hashes and negative
decoder controls. Both have stdlib-only authored dependencies. `package.py`
checks text, pins and patches without staging; see its docstring for local writes.

Keep run directories, binary fixtures, logs and intermediate assembly local.
They are retained as the audit trail; no automatic deletion occurs. Future
cleanup may remove an individually verified disposable run directory once the
review package is retained. Never apply that cleanup policy to exports, saves,
game files, analysis databases or historical evidence. No tracked source contains
proprietary executable bytes or exported native listings.
