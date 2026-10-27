# D5L retained-population observer methods

GPL-3.0-or-later. [Scientific contract](../../docs/experiments/resource-retained-population/report.md),
[native register](../../docs/experiments/resource-retained-population/native.md),
[tests](../../docs/experiments/resource-retained-population/validation.md),
[proposed card](../../docs/experiments/resource-retained-population/run-card.md).
**Phase A executes only disposable fixtures. Retail requires separate explicit
GO and fresh Steam Cloud state confirmation; no game operation is authorized here.**

## Methods, effects and prerequisites

| File | Reads / prerequisite | Writes and target effect |
|---|---|---|
| build_native.py / build.py | Owned sources/quoted headers, existing MSVC/SDK/MASM; C:/D: floor | Fresh ignored build/source snapshots/tool receipts. Build tools only; no download or game. build.py also retains historical packet build support. |
| controller-tail.inc / native-capture.h | Pinned PE, real debug events/CONTEXT, bounded external native-layout reads | Fixed fourteen software probes, all-stop/peer suspension, one-instruction RIP/TF rearm and owned debug-status clearing; stdout. STOP/failure disposes the selected research target. Separate fixture and future-retail binaries. |
| native-fixture.cpp / .asm | Explicit synthetic modes and owned native-shaped memory | Disposable allocations, copied geometry and shaped stacks/returns. Test-only new-thread injection/oracle never enters retail. No game algorithm or native calls. |
| qualify_native.py / qualify_pump.py | Exact build, owned SRO1/independent decoder | Fresh local journals, fsynced receipts/ACKs, reductions, failures/target-absence results. Execute only sibling disposable fixture controller. |
| native_reduce.py | Pure native events, raw fields/context, explicit synthetic domain | In-memory bounded decisions/chains; no writes/process calls or fixture epoch/oracle use. |
| check_native.py / check_admission.py | Actual captures or completed offline metadata | Fresh local counterexample results; corrupt copy or in-memory synthetic admission only. No target operations or genuine GO file. |
| verify_native.py | Installed PE, existing read-only export, built fixture PE, SRO1 | Fresh local verification JSON: actual RVA/file-offset/length/flow/body backing and independent framing. No disassembler dependency. |
| review_capture.py | Journal, every receipt and ACK, independent decoder | One fresh local checked reduction. Default retail domain; synthetic needs explicit flag. Missing/corrupt/unbound evidence fails. |
| prepare_native.py | Active archive-backed inputs, protected saves/backups, Steam metadata, build/tests | Fresh local offline readiness receipts and one Save52 rehearsal copy. No original/config/Cloud/baseline changes; cannot grant GO. |
| preservation_native.py / test_preservation.py | Completed pre/post receipts, original build snapshots or disposable synthetic inputs | Fresh ignored comparison or disposable scratch. Operational Python amendment binding preserves exact native/tool pins; metadata changes are diagnostic. Focused tests never attach or create live authority. |
| collect_native.py | Separately authorized exact admission/preflight/build/code, PID/time | Future-only attachment transport, fresh local SRO1/ACK/journal/READY, one-use admission sidecar. It does not launch Starfield. STOP/loss intentionally terminates admitted target; no safe detach claim. |
| ReadD5LNative.java / ExploreD5L.java / ExportD5LSites.java | Existing Ghidra saved state; -readOnly -noanalysis, JDK21 | Exclusive task-local exports/logs/cache. No symbols/types/comments/analysis edits. |
| fixture.cpp / qualify.py / reduce.py / check_reduction.py | Historical twelve-site packet prototype and owned transport | Historical disposable qualification/replay only; never substitute for native reader. |

Use the installed Python with `-B`. From repository root, to reproduce final
synthetic qualification choose fresh task-owned labels (never overwrite evidence):

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B research/resource-retained-population/build_native.py native-rebuild01
& $py -B research/resource-retained-population/qualify_native.py .local-work/resource-retained-population/native-rebuild01 .local-work/resource-retained-population/native-requalification01
& $py -B research/resource-retained-population/qualify_pump.py .local-work/resource-retained-population/native-rebuild01 .local-work/resource-retained-population/native-repump01
& $py -B research/resource-retained-population/check_native.py .local-work/resource-retained-population/native-requalification01 .local-work/resource-retained-population/native-recounterexamples01
```

`review_capture.py --synthetic` verifies a single case directory; invoke it for
every case before aggregating. Current exact native export command arguments are
in local native-sites-command04.json, using existing Ghidra 12.1.2/JDK21 and
separate task settings/cache/home. Exports and project databases remain LOCAL-ONLY.
Do not invoke future-retail main or create live admission during Phase A.

The [2026-10-28 amendment](../../docs/experiments/resource-retained-population/cloud-metadata-amendment.md)
changes operational metadata gates only. Run its focused offline regression with
`python -B -m unittest discover -s research/resource-retained-population -p test_preservation.py -v`.
The full debugger qualification is not required for this amendment. Full preflight
and after-exit audits still hash protected content; main-menu admission retains
the existing lightweight names/sizes checks. An equal-size content substitution
is detected by full hashes, not claimed detectable by those lightweight checks.

Owned D5B controller/read helpers and geographic decoding, D5E orchestration,
C1B/C1D SRO1 transport, Tungsten independent framing, C2B save policy, D5H scoped
archive verification and exact-review exporter are reused under SOR-P-0002.
See CREDITS.md and the source ledger. ASM scaffolding represents documented ABI
facts and original synthetic behavior; it is not a port of Bethesda generation
or a claim of clean-room research. No new external code/dependency is introduced.
