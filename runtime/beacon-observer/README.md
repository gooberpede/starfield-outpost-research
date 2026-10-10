# Beacon coordinate observer 0.1.1

EXP0021 adds independent **stored native workshop output** acquisition from the
fresh terrain root's `+0x130` owner, before and after the reference census:
center XYZ at `+0x90`, radius at `+0x9c`, and raw flags at `+0xe8/+0xe9/+0xea`.
The plugin copies bytes; it does not calculate that center. The native writer
`1421b29ac/29b1` and downstream bounds consumer `1407a6540` establish the
typed chain. Equal bracket values do not prove freshness, active workshop
identity, common frame or atomicity. Missing/stale/different-frame results remain
unassessed. See the [oracle contract](../../docs/experiments/engine-oracle/oracle-contract.md)
and [prospective run card](../../docs/experiments/engine-oracle/run-card.md).
This extension is built and disposable-qualified only; separate critical review
and live authorization are required. Historical 0.1.0 captures are unchanged.

Offline review candidate under [the brief](../../docs/implementation-briefs/CODEX_IMPLEMENTATION_BRIEF_SOR_live_beacon_coordinate_observer.md). **Not deployed or Starfield-qualified.** Read-only memory acquisition on a dedicated observer worker. No engine calls, handle acquisition/release, callbacks, tasks, hooks, breakpoints, memory writes or native saving. Guarded reads are non-atomic and do not retain engine objects. SFSE loads the DLL; it remains resident until normal process exit.

The observer collects fresh player, terrain and ordinary beacon roots on each explicit request. It scans the finite native 2,097,152-slot reference pool, preserving its complete 32 MiB byte view in chunks, and captures ordinary ACTI stored-base `002C60E9` references. It checks slot generation/index association without invoking handle resolution. The pool includes unloaded references when present; absence is NOT_OBSERVED, never proof of no outpost. Alternate/changed bases are outside this selector. Saved tokens are not runtime FormIDs. Label SOR-002/SOR-003 only after matching baseline base/transform/body/world evidence against the Save25 table, with operator location as corroboration. Ambiguous matches stay ambiguous; reload reacquires everything.

Additional schema-directed reads capture reference transform and identity prefix, stored CELL/worldspace, extra chains (cycle detection), cached planetary extra `0x81`, workshop extra `0xbc` and its complete initialized 24-byte table capacity. Unknown extras retain headers. Terrain capture includes mode/origins, body candidate, active-state/world chain, grid-owner/resolution chain and stitching settings. Raw prefixes preserve unclassified nearby fields; they are not full C++ object layouts or an exhaustive object graph. The world/component-map overlay fallback and continuous residual consumer remain unsupported. No native GetWorkshop or coordinate query is called. Stored native center/radius have static producer/consumer support; their freshness and runtime authority remain unvalidated.

Each snapshot gets its own directory, `records.jsonl`, individually flushed `raw-N.bin` sections with SHA-256, root/parent-field provenance, runtime VA and byte extent, plus an independent `complete.json`. Begin records identify version, executable/DLL hash, PID/process creation, module base and actual worker TID. Startup records hash all loaded native modules. Startup module list is not a plugin load order. Raw float32 data is authoritative byte evidence; JSON uses nine significant digits and explicit nonfinite strings. Addresses must not be reused across checkpoints. `complete.json` can say CAPTURE_PARTIAL; scientific completeness and instrumentation health are separate.

Every 64 KiB write checks available bytes on C: and D: against **40,000,000,000**. Failure to query space stops writing. No arbitrary evidence-volume, object-count, file-count, error-count, session-time or checkpoint-count quotas exist. Fixed lengths are inspected structure prefixes, the exact native pool capacity, or chunk sizes, not collection caps. A command produces one finite traversal; repeats require a new unique request. Cycles, overflowing extents and changed/unreadable objects terminate only that component. STOP interrupts acquisition cooperatively between writes. Runaway recurrence is prevented by single consumption of each label, finite fixed-pool traversal and visited-address tracking. A corrupted acyclic extra chain or plausible corrupt table length can still cause excessive work; STOP is the operator recovery, with disk guard as hard backstop. This remaining risk requires review, not concealment as qualification.

Any disk/writer/code-integrity exception stops acquisition, preserving prior flushed records. Under low disk there may be no final failure marker; journal recovery requires complete JSON lines and hash/size agreement, with orphan raw files retained but unclassified. No retry loop repeats failed reads. Read failures, unknown fields and missing roots continue through independent collectors. Output resides only in ignored `.local-work/beacon-observer-live/`; absolute local paths remain private. Output path rejects reparse ancestors at startup. Changing output paths while running is unsupported.

Build from repository root with installed CPython and MSVC:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B runtime/beacon-observer/build.py --name review-NEW --sfse '<exact Vortex-staged or deployed sfse_1_16_244.dll>' --vcvars 'C:/Program Files/Microsoft Visual Studio/18/Community/VC/Auxiliary/Build/vcvars64.bat'
```

Build reads installed executable, explicitly selected SFSE DLL/loader and exact Save25 original/archive from the frozen sample manifest for hash preservation, generates local code-window guards, executes original tests in a disposable process, and writes a new ignored build directory, manifest, DLL and ZIP. SFSE is currently Vortex-staged and absent from the game directory; staged-byte identity does not establish a loaded runtime. No database, save, deployment or source binary changes. Python standard library, installed MSVC/Windows SDK and Windows system DLLs only. Existing approved SFSE PluginAPI.h remains unmodified at its original path; licence included. No CommonLib/Address Library/sibling third-party dependencies. The sibling census/association algorithm is adapted under SOR-P-0002; see [provenance and review](../../docs/audits/live-beacon-observer.md).

Version source is `version.json`; generated metadata uses `(major<<24)|(minor<<16)|patch`: 0.1.1 = `0x00010001`. Historical reviewNN/0.1.0 packages are not renumbered. Native-save observer 0.1.0 was never built; debugger adapter 0.1.x is a distinct component. Request helper reads that same version source.

After critical review and separate live approval, user installs/enables the exact ZIP through Vortex. Do not copy DLL/config into game or staging directories. User performs all gameplay/save/reload. Session ready marker identifies the live session. Commands only write observer control files:

```powershell
python -B runtime/beacon-observer/request.py '<session>' baseline-003 --settled
python -B runtime/beacon-observer/request.py '<session>' control-003 --settled
python -B runtime/beacon-observer/request.py '<session>' post-move-003 --settled
python -B runtime/beacon-observer/request.py '<session>' post-save-003 --settled
python -B runtime/beacon-observer/request.py '<session>' post-reload-003 --settled
python -B runtime/beacon-observer/request.py '<session>' STOP
```

Wait for that snapshot's marker before further deliberate gameplay. SETTLED is operator attestation, not an engine synchronization guarantee. Save25 starts at **SOR-003**. Capture baseline/control there first. Capture both beacons if present in the pool; preserve absent/unloaded classifications. If SOR-002 needs a local frame, travel there on foot or fast-travel, record route/loading change and elapsed time, then request baseline-002/control-002. Travel is a separate condition, not a no-action control. Do not abandon a valuable experiment to avoid travel. Prefer moving SOR-003 first, with SOR-002 unchanged; secondary boundary comparison may need both sites. After manual save/reload retain pointer/handle churn without assuming stable saved token mapping. Detailed card and coverage plan are in the review document.

On completion, request STOP, let the user exit normally and disable through Vortex. Preserve output, hash/archive new manual save copies without overwriting originals. No automatic installation, launch, save, process termination, commit or push is part of this tool.

Offline `inspect_capture.py <snapshot> --output <new-file.json>` validates every journal-referenced raw SHA-256 and length, inventories partial/error states, preserves float32 bit patterns, and decodes mode/body/packed origins/grid settings where captured. It recovers an incomplete final journal line, refuses corrupted referenced bytes and refuses overwriting its output. It makes no coordinate conversion, ownership or boundary claim.
