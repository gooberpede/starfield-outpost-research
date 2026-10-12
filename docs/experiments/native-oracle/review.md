# Combined pre-live review — SOR-EXP-0031 / SOR-EV-0039

**Independent reviewer ACCEPT — Phase A pre-live engineering package.**
No Starfield launch, attachment, deployment, save/config change, staging, commit
or push occurred. Full native equivalence remains NOT TESTED. User's Phase B
joint review and exact live authorization remain required. Original
[authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_native_position_oracle_observer_integrated.md)
and [contract](contract.md) preserve all six mandatory deliverables.

## Result and actual boundary

New SFSE component SorNativePositionOracle0.1.0 associates natural center and
grid CALLs with a callback invocation, actual reference/context, native input
hierarchy/floors and native result bytes. It changes two complete CALLs and two
callback table slots only during guarded sole-thread pre-main startup; it never
calls the game to manufacture an observation. [Architecture and static evidence](architecture.md)
explain producer/consumer contracts and plausible terrain-arrival triggers.
Callback-only or passive shared-buffer sampling cannot supply these fresh private
outputs. [Schema/comparison](schema.md) preserves native versus derived values.

Startup admission, useful events and model-validation sufficiency remain separate.
Installed Starfield startup is untested; sole-thread snapshot admission is
conditional on exclusive synchronous pre-main loading, not an unconditional
thread-creation barrier. Capture stops/drains where possible and keeps patches/DLL
inert and resident until exit. No hot unhook guarantee. Source world/frame
reconciliation and blinded native holdouts remain unresolved.

## Acceptance matrix

| Original requirement | Actual result / evidence | Limit |
|---|---|---|
| 1. Fresh native identity-bound implementation | IMPLEMENTED; callback/center/grid-before/grid-result/exit records; raw identity or unreadable/race flags; [source](../../../runtime/native-oracle/README.md), schema | Live reachability, outpost identity and saved-to-loaded frame authority NOT TESTED |
| 2. Narrow architecture and lifecycle | DISPOSABLE PASS; real CALL/relay/vtable execution, ABI sentinels, SEH/C++ propagation, nested/rejected/concurrent scopes, in-flight STOP, queue/depth/IO failure | Live timing/lifetime/CFG/CET/recovery unqualified; no dynamic unhook |
| 3. Runnable versioned plugin/ZIP/manifests | BUILD/ARCHIVE PASS; final-review-04 below, both channels, source/toolchain/hash pins and notices | No deployment/live compatibility test; prior0.1.1 preserved |
| 4. Adverse disposable qualification | 477 native assertions and17 inspector tests PASS; [qualification/failures](qualification.md), full retained logs | Synthetic evidence cannot prove game semantics/full equivalence |
| 5. Exact executable card now | PRODUCED; [full card](run-card.md), pre/postflight/control commands, protected saves, routes, health/STOP/exit/removal/results | Phase B authorization and user Vortex deployment pending |
| 6. Combined critical package | PASS; replay-checked complete/task diffs, inventories/manifests and [independent ACCEPT](independent-review.md) | Acceptance grants no Phase B/live/integration authority |

## Exact candidate and hashes

Directory: `D:/Projects/starfield-outpost-research/.local-work/native-oracle/builds/final-review-04/`.

| Artifact | SHA256 |
|---|---|
| SorNativePositionOracle-0.1.0.zip | `4769f2482f06d009126395c34e280b3011763fe0e5a979598bdc4b8217d6ec79` |
| Data/SFSE/Plugins/SorNativePositionOracle.dll | `c4c3e23c9a741d7d2937fce7ffb38013b0036e4d5a07143c1d6c57d4045c2584` |
| Data/SFSE/Plugins/SorNativePositionOracle.config | `6894da75d4face7b9d366a67c436fe75b100a434e073f7184bcca55e19d953c9` |

`build.json` contains every packaged file, source, game/SFSE guard, protected input,
compiler/assembler/linker and vcvars hash, initial/final caller-available disk.
Command files/diagnostics, `qualification.txt` (477 PASS) and
`inspection-tests.txt` (17 OK) are retained alongside. Staged-input receipt
`.local-work/native-oracle/operations/offline-preflight-04.json` is PASS; it is not
a deployed/live preflight. Earlier tasklist access denial was a test failure;
direct Toolhelp process enumeration replaced that dependency without attachment
or process-memory access. Failed iterations remain intact.

Starting HEAD `aa76d2dee8b5f18b8833b94cc52570ae5b5a9a09`; index SHA256
`a9c3892aa4679b1c3bdd05c59c78c01fb5905a1d2ffdf42c4fc2fcab1fa69ba2`.
Baseline exact483-file inventory/bytes remain in `.local-work/native-oracle/`.
Patches `.local-work/diffs/native-oracle-complete.diff` and
`native-oracle-task-only.diff` include new text correctly; task-only excludes only
the unchanged supplied brief. `.local-work/native-oracle/package.json` records
every file/hash, full status, exclusions, link/whitespace checks, preserved
starting files and exact forward application in disposable plain directories.
[Static export identities](native-sources.csv) preserve primary provenance.
Raw saves/native exports/binaries/databases remain local and untracked.
Publication eligibility is unchanged; engineering confidence cannot clear it.

## Independent review and rework

The authorized independent reviewer received the original brief/contract and
read-only source/evidence access. Preliminary REWORK identified nested admission
leakage, inspector unpacking/pairing/FP issues and ASLR vtable handling; all were
repaired and requalified. An independent specialist confirmed CALL bytes/targets,
consumed ABI, overwritten locals and terrain candidate reachability separately.

Final-review-02's independent rerun passed463/11; review nevertheless found a
worker control-starvation counterexample and weak FP-negative coverage. These
were resolved by per-record production control polling, a sustained-backlog STOP
test, production patch-failure test and qualified FP/order negative tests.
Final-review-03 requalified477/17. Final-review-04 repeats477/17 with identical
executable source and corrected UTF8 documentation/source-pinned README; it
supersedes all earlier candidates.

Final verdict [ACCEPT](independent-review.md) covers all six deliverables against
final-review-04 source/build/logs, the full card and replay-checked diffs. Reviewer
independently reproduced477 assertions/17 tests, verified all pins/ZIP/diff
application and confirmed unchanged reviewed tree/index. The exact reviewed
snapshot remains in `.local-work/native-oracle/reviewed-snapshot-04/`; the final
documentation refresh adds the verbatim decision and updates this outcome only.
Current inventory/diffs are regenerated after that refresh. Full engineering
artifact hashes, including tests.exe and logs, are in local artifact-ledger files.
All six pre-live deliverables are complete for joint review. This is not approval
to integrate, deploy, launch, publish or claim native equivalence.
