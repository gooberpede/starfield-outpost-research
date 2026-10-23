# C2A executed qualification and acceptance evidence

2026-10-23, Australia/Sydney. [Frozen AC1–AC8](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_C2A_carinae_native_iron_region_qualification.md).
All commands below were run from the repository root with
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B`.
They execute only original disposable fixtures or offline analysis, never retail.
Exact selected file hashes and result summaries are in [sources.csv](sources.csv)
and [qualification-summary.json](qualification-summary.json). Raw Windows contexts,
SRO1 bytes, executables, saves and native exports remain ignored/local.

## Executed tests and preserved failures

| Command after interpreter | Actual result and primary local receipt |
|---|---|
| `research/resource-carinae/build.py --name build05` | MSVC x64 build exit 0. `build05/build.log` records compiler 19.51.36256.0; retail and fixture controllers are separate executables. |
| `research/resource-carinae/qualify.py --build .local-work/resource-carinae/build05 --output .local-work/resource-carinae/qualification05` | 40 cases PASS; each case retains config/events/SRO1/ACK/result bytes and explicit incomplete/fatal-loss accounting. |
| `research/resource-carinae/test_compare.py` | Six tests PASS against qualification05. Bit changes, order, resource identity, invalid reads and wrong/missing transfer ancestry are challenged. |
| `research/resource-carinae/compare.py --receipts .local-work/resource-carinae/qualification05/good --output .local-work/resource-carinae/synthetic-comparison02.json` | Complete synthetic positive transfer join, no exact geometry match to the pinned real baseline; source/frame identity UNKNOWN. No retail Phase C. |
| `research/resource-oracle-collector/qualify.py --build .local-work/resource-oracle-collector/build08 --output .local-work/resource-oracle-collector/qualification-c2a01` | All 19 inherited C1C tests PASS, including transport and isolation. Expected detector failures remain negative controls, not hidden failures. |
| `research/resource-oracle-retail/qualify.py --build .local-work/resource-oracle-retail/build14 --output .local-work/resource-oracle-retail/qualification-c2a01` | Unit decoder checks and all 13 C1D cases PASS. |
| `research/resource-region-ancestry/qualify.py --build .local-work/resource-region-ancestry/build06 --output .local-work/resource-region-ancestry/qualification-c2a01` | All 32 unchanged C1E cases PASS. |
| `research/resource-selection-operands/qualify.py --build .local-work/resource-selection-operands/build05 --output .local-work/resource-selection-operands/qualification-c2a01` | All 27 C1G cases PASS. |
| `research/resource-installed-settings/test_settings.py` | All 15 tests PASS, no skips. Full frozen regeneration, four exact Feynman paths, three chance comparisons, Copper/no-extra-IL control and unchanged Carinae population verified. |
| `research/resource-carinae/preflight.py --build .local-work/resource-carinae/build05 --qualification .local-work/resource-carinae/qualification05/qualification.json --name offline-preflight02` | Pinned EXE, 39 definitions and 271 live/backup saves verified; Save52 scratch restoration matched its protected hash. No launch or active-save restoration. |

Offline postflight recorded zero save/backup/definition/config additions, changes
or deletions. All 7691 protected pins, including prior evidence and predictions,
were rehashed unchanged; HEAD and index also matched the starting receipt.

The C2A final fixture modes are: good, generic-resource, short-circuit, rothicite,
wrong-cell, partial-page, source-reuse, no-hit, retained-cache, alkanes, reject,
multi, maximum, multi-reject, sources, nested, threads, mixed, invalid-procgen,
wrong-workshop, wrong-source, wrong-resource, wrong-caller, stale-transfer,
outside-region, empty, partial, corrupt, oversized, byte-budget, invalid-source,
source-budget, empty-collection, corrupt-collection, invalid-collection,
guard-mismatch, ackfail, crash-before, crash-after and completion.

`wrong-cell` supplies an interior CELL and must refuse binding; it does not prove
detection of a different valid exterior cell with the same Workshop identifier.
`partial-page` places the point read across a protected page boundary. The native
fixture singleton decision succeeds while the external geometry read remains
incomplete. `short-circuit` explicitly skips the second same-resource region
after the first insertion; no event is fabricated for that unvisited region.
`source-reuse` overwrites one source slot between callbacks while preserving
different wrapper identities. These are controlled mechanisms in the original
fixture, not claims of executed Carinae retail behavior.

The first attempted command used the inaccessible WindowsApps `python.exe` alias;
no Python task ran. The exact installed interpreter was then used throughout.
`qualification01` passed its first 18 emitted cases, then failed because the
runner listed `wrong-cell` twice and tried to recreate its directory. That
incomplete run and its source-pinned build01 remain preserved. No overall PASS
was issued. Qualification02 completed 38 cases; qualification03 completed 39
after adding the explicit short-circuit test and renaming the legacy control
to Alkanes. Qualification04 adds the generic resource test and durable incomplete/
fatal-loss counters, completing all 40. Build05 repeats the same 40 cases after comment-notation correction and final
fixture-path pinning. Earlier builds/receipts remain local.

## Frozen criteria and independent dimensions

This implementer matrix is submitted for independent review; the actual
[review decision](review.md) controls acceptance of the final snapshot.

| Criterion | Implementer disposition and decisive evidence |
|---|---|
| AC1 | PASS: before/after protected-file receipts, unchanged HEAD/index, exact EXE and installed pins, save/backup preflight and postflight; no retail execution. |
| AC2 | PASS for Phase A preparation: exact saved Workshop/extractor joins, pinned Save52 and [runtime identity plan](contract.md), with no token-to-handle extrapolation. |
| AC3 | PASS: compiled C2A controller/decoder/sample extension, 40-case raw events and closed receipt verification; actual region/query/source/transfer collection implemented. |
| AC4 | PASS: real Windows attachment, hardware breakpoint and external-memory trials on original disposable fixtures, plus all four inherited suites; no fixture promoted to a retail oracle. |
| AC5 | PASS: exact nonfitting comparator and six mechanical tests, full pinned baseline, unchanged Feynman/C1H regressions and explicit identity/coverage limits. |
| AC6 | PASS for preparation: [one-session card](run-card.md) includes actual commands, pins, approval/identity/guard/backup gates, natural trigger, no-hit handling, disposal/postflight/recovery and prospective Phase C. Neither phase executed. |
| AC7 | PASS subject to final editorial receipt: code, [source lineage/effects](sources.md), selected numeric receipts, retained failures, uncertainties, exclusions and durable navigation. |
| AC8 | Independent disposition and exact-file hashes are recorded in [review](review.md); complete/task-only patches and delivery manifest remain local. Acceptance is not self-awarded. |

Scientific outcome: Carinae Iron disagreement remains OPEN; no new retail
region, producer identity or census is established. Engineering outcome: the
bounded synthetic instrument and comparator qualify within tested conditions.
Target outcome: disposable synthetic targets exited normally, crashed or were
terminated as specified by their test; no Starfield process was operated.
Safety outcome: protected originals remain read-only; no active-save changes,
installation, network disclosure or Git publication. Independent review and
maintainer integration remain distinct from these test results.

No universal scheduler/XSTATE, allocation-failure, full source-producer lifetime,
retail survival or correct identification of every possible exterior-cell alias
was tested. The stored CELL supplement is fail-closed for unreadable/interior/
mistyped inputs, not an invented saved-cell mapping. A complete native region
in one accepted traversal does not establish complete outpost resource coverage.
