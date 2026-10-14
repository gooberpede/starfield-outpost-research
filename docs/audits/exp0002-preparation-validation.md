# SOR-EXP-0002 Gate-A implementation validation

2026-10-06 Australia/Sydney. Codex implementation self-check, **not independent critical review or approval to integrate**. SOR-D-0010/0011; SOR-P-0001. No staging/commit/push. Initial tracked tree/index was clean; the supplied brief was already untracked and is retained unchanged.

## Current review verdict

**Original observer, installable local package, explicit checkpoint trigger, native validator, executable bounded diagnostic and operator card are prepared offline for critical review. NOT DEPLOYED or live-qualified.** The original broad implementation stop was premature and has been superseded by source-informed native checks, exact header approval and original implementation. Historical report/audit and failed build/export evidence remain local. Gate B is still a separate user decision after review.

The only incorporated third-party code is the pinned MIT SFSE PluginAPI.h, accepted explicitly by the user. This exact approval supersedes the brief checklist's general no-third-party-incorporation expectation for that header alone; no broader exception. Complete notice retained. CommonLib/sibling research was referenced and credited, with no observer implementation or library code copied/adapted. The work is not described as clean-room.

## Exact local review build

Ignored current build directory: `.local-work/exp0002-builds/review12-anomalies/`.

| Artifact | SHA-256 |
|---|---|
| SorExp0002.dll | `ca167cb5e47ea90739729ee686ce1691766461238847d6a778f98530bf6ce94e` |
| workshop-trace.exe | `701033d459c11e54bbda5c4896a57f98940759f95e1a83034cbda2601295e36a` |
| SorExp0002-local-test.zip | `84bc87c0f7ba8f58c843f70d170bb6d31ea1e72a47a339c0e47e57f0b41a9ae1` |

VS 2026 Community 18.9.0, MSVC 14.51.36231 / compiler 19.51.36256, SDK 10.0.26100.0. Compiler/linker executable hashes, compiler passes, pinned PE/site hashes, complete native source hashes and logs in build.json / *-build.txt. Three native targets compile without compiler warnings/errors; no downloads or installation. Test DLL is loaded solely in a synthetic test process. ZIP includes original observer/config plus licence notices; SFSE runtime, Address Library, CommonLib and game content are excluded.

## Checks and limits

| Check | Actual result / limit |
|---|---|
| Parent/backup | Both 2,096,496 bytes, SHA-256 d06123ee32bd5b3e244650852fac9714697a19fd6243384966414d1d1f4ffbfe; direct byte equality; original/backup path, size, hash and mtime match initial manifests. No semantic parsing/write/load. |
| Baseline | All seven installed/pinned game/CK/SFSE/archive size/hash checks match SOR-ENV-0001. Runtime profile unqualified. |
| Ghidra | Read-only/no-analysis exports; all 77 before/after project files match path/size/SHA-256 across both roots. No edits to symbols/types/comments/bytes. |
| Static contract | Eighteen file-backed native site hashes; independently checked transform/callback/cell operands. CommonLib cell worldspace/flags discrepancy documented; type/handle leads not promoted to proven semantics. |
| Python design suite | Nine tests pass: metadata/byte comparisons, PE/RVA guards, schema/selection roles, path/size/overwrite/flush and manifest behavior. |
| Native synthetic suite | 125 checks pass (including 33 READY/startup and 44 anomaly/safety checks): bounded/missing/ambiguous/deduplicated/changing selection, finite identity, request ordering syntax, ASLR, SHA vector, path/write/flush limits, actual DLL wrong-version/non-game guard, trace phase/zero-hit/hit bounds. |
| Native output suite | 26 checks pass (including anomaly artifacts and rejection cases), parsing production serializer output; null/read-failure distinction, selected roles, finite coordinates, terminals/evidence kind; trace order/thread/stack/operand/time correlation and missing-terminal rejection. |
| Authority guards | Debugger run with no arguments rejects before process access; request.ps1 without approval switch rejects before writes. No exp0002-live directory created. |
| Target byte validation | Pinned PE and generated windows checked offline; actual loaded checks implemented but never run in Starfield. |
| Build/source coherence | Final source hashes, DLL/debugger/ZIP hashes match build.json. MSVC/Windows SDK external; no network build dependency. |
| Repository | Final UTF-8/LF, Markdown links, JSON/Python syntax, diff whitespace, status/index and ignored-artifact checks captured in validation-resumed.json; complete tracked/untracked patch in review-resumed.diff. |

These are offline structural checks, not live reference ownership, ABI safety, mod compatibility, coordinate meaning, crash durability or Windows attach/context/cleanup tests. Repeated views are non-atomic. A native call can block beyond cooperative observer budgets. Diagnostic no-kill-policy + detach double failure enters an explicit recovery hold to avoid exiting under Windows' default kill policy; it is not successful or ongoing bounded acquisition. Review that exceptional intervention before any diagnostic approval.

## Preserved deviations and limits

Initial Python PE helper rejected an attempted file-backed read of a runtime global; corrected to mark runtime-only. Broad coordinate scan capped, followed by focused scan; no absence claim. One Ghidra callback export is PARTIAL: an unquoted hex address containing e was interpreted numerically by PowerShell, and a missing center instruction caused script failure despite exit 0. Corrected quoted-address exports are independently indexed. First native build attempt failed command quoting, next compile failed a Windows constant; corrected before successful candidates. Candidate builds are retained and **not** the reviewed deployment target. One integrity invocation rejected a path where a simple JSON basename was required; the corrected invocation produced the final integrity record. Windows PowerShell 5.1 refused scripts; the existing PowerShell 7.6.5 ran the helper and its authority guard. No execution policy was changed or bypass flag used. Finalizer caught and repaired a documentation encoding conversion before final diff review. No failed attempt modified game/save/Ghidra state.

## Evidence state, files and handoff

SOR-SAMPLE-0001 parent; SOR-ENV-0002 checks; SOR-EV-0002 evidence; SOR-F-0005/0006 and SOR-FN-0010–0013 / SOR-ST-0007/0008 remain STATIC only. SOR-P-0001 is exact header permission; SOR-S-0114–0117 add SFSE, sibling/CommonLib research and Microsoft tooling credit. No persistence finding/hypothesis was promoted.

New deliverables: experiment, operator card, audit/evidence index; research/exp0002 offline helpers; runtime/exp0002 native source/build/guards/validators/docs and approved header/notice. Updated root README/CREDITS/THIRD_PARTY_NOTICES; decisions/permissions/provenance/state/sources; finding/function/state registers and indexes; original Ghidra reader and its docs. Complete exact file list is status-resumed.txt / validation-resumed.json.

Review artifacts under ignored `.local-work/exp0002/`: review-resumed.diff includes every tracked edit and untracked deliverable (including the original supplied brief), status-resumed.txt, validation-resumed.json, tooling/build/evidence manifests and tests. The patch is LOCAL-ONLY: the supplied brief contains private paths/sample filename and is not publication-cleared. No staging, commit, push, fork/PR, contact or upload; no deployment, game/console use, save modification or debugger attachment. The approved header fetch was read-only source retrieval, not external disclosure.

Next decisions: critical review of exact source/package and assumptions; explicit Gate B package/config/profile/operator-sequence approval; optional separate diagnostic decision after secure A2R. No additional code permission is pending for the implemented dependency scope. The [operator card](../experiments/EXP0002-operator-card.md) and [native limitations](../../runtime/exp0002/README.md) are part of the review.

Suggested commit after review (not executed):

```text
feat(research): prepare outpost membership live capture
```

LIVE EXECUTION NOT YET PERFORMED  
DEPLOYMENT NOT YET PERFORMED  
SAVE3 NOT LOADED OR MODIFIED  
DEBUGGER NOT ATTACHED

## Scoped READY correction — 2026-10-06

User requested only initialization/READY fixes, offline coverage, explicit deployment method and regenerated review artifacts; no deployment or commit. This section supersedes review 08's initialization behavior/build selection. No research finding, native observation point, dependency permission, save or Ghidra evidence was changed or re-collected.

SFSE listener registration now precedes worker creation. The running worker publishes READY before polling requests, by flushing/closing ready.pending and renaming without replacement to ready.json. Listener failure prevents worker creation; failed thread creation, write/flush or rename cannot produce READY. Snapshot/enumeration/profile failures and initialization/worker C++ exceptions attempt failure.json after session creation; storage/allocation failure can prevent even failure reporting. Snapshot handles are closed on error/exception. A registered listener keeps the DLL resident if later initialization fails, preventing a dangling SFSE callback; load return true alone is not readiness. No loader-thread startup wait or live execution was added.

The 33 added native checks exercise production startup/publication helpers using injected listener/thread failures, a thread-start exception, worker-before-listener rejection, a private real Windows thread delayed before publication, complete marker readback, non-overwrite, simulated partial write/flush failure and rename failure. Total 81 native checks and 15 existing output checks pass; build has no compiler warnings/errors. These synthetic tests do not test SFSE delivery or Starfield startup, disk power-loss durability or live safety.

**Superseded deployment proposal:** the earlier temporary manual method was never executed. The user now requires Vortex as the exclusive owner: the user manually installs, deploys and retires the reviewed ZIP through Vortex. No direct file-copy/delete deployment path remains authorized. See the current operator card.

Historical READY review artifacts: `.local-work/exp0002-ready-fix/review.diff` (complete tracked + untracked package), `changes-this-request.diff` (only this correction), `status.txt`, `validation.json`, and `hashes.json`. Native build manifest and package are in the review 09-ready-fix directory above. Prior review 08 artifacts and pre-correction files are preserved. Full patch remains LOCAL-ONLY because it includes the supplied private-path brief. No new permission issue, staging, commit, push, installation, game launch, save access or debugger attach.

Suggested separate correction commit after review: `fix(observer): publish READY only after initialization`.


## Scientific anomaly / Vortex correction — 2026-10-06

The user requested exclusive Vortex deployment ownership and a distinction between scientific anomalies and terminal safety/instrument failures. The user manually installs/deploys/retires the reviewed ZIP through Vortex after Gate B approval. Nothing has been deployed, launched, attached, staged or committed. This section and review 12-anomalies supersede earlier package selection and terminal-on-unexpected-observation behavior; earlier evidence/builds are preserved.

Count disagreement and selection ambiguity persist bounded candidate copies, expected/observed counts and completeness/truncation flags, without selected-reference calls. Successful but changing collection/identity views, player/load changes and cooperative observation-budget expiry abandon the current task and persist anomalies while allowing a fresh explicitly requested checkpoint. No stale selection is reused. Structural read failures, wrong build/sites, invalid requests/permissions, failed persistence and low/unknown disk space remain terminal. Both C: and D: must have at least 40,000,000,000 available bytes. An in-flight native call cannot be cancelled by the disk/budget guard.

The original six checkpoint slots remain finite: a recorded anomaly consumes its slot, requires explicit operator acknowledgement before the next request, and cannot be silently retried. A sequence containing anomalies is marked CHECKPOINT_SEQUENCE_RECORDED_WITH_ANOMALIES, not successful completion; it cannot unlock the optional diagnostic. Anomaly files are capped at 32 KiB and 16 copied candidates; incomplete counts are qualified. No new game-memory reads occur during anomaly serialization. The runtime README contains the individual condition decisions and limits.

Actual checks: 125 native synthetic checks and 26 production-output checks pass; three native targets compile with no compiler warnings/errors. Coverage includes persisted mismatch/ambiguity followed by a usable fresh checkpoint, zero query calls for failed selection, changing versus unreadable repeated views, bounded candidates, explicit nonfinite values, failed anomaly persistence, disk boundaries and all prior READY checks. PowerShell AST parsing passes; invocation without GateBApproved rejects before session access/writes. The review 11 attempt exposed a synthetic fixture read-counter reset error, corrected before this fresh review 12 build; its failed artifacts remain local. These results do not qualify live SFSE delivery, native lifetime/ABI safety, game behavior or actual low-disk operation.

Current complete review: `.local-work/exp0002-anomaly-fix/review.diff`; scoped correction: `changes-this-request.diff`; checks/status/hashes: `validation.json`, `status.txt`, `hashes.json` in that directory. Build/package hashes above and the evidence index identify review 12-anomalies. Full patch is LOCAL-ONLY because the supplied brief includes private paths. No new source reuse, permission issue, scientific finding, native address/layout change or save/Ghidra research was introduced. Earlier baseline/save/Ghidra results in this audit are historical, not rerun by this correction.

Suggested correction commit after review (not executed): `fix(observer): preserve scientific anomalies and require Vortex deployment`.
