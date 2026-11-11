# D5AB bounded status handoff

2026-10-31, Australia/Sydney. **INCOMPLETE / REWORK. B2 NO-GO / NOT AUTHORIZED.
D5R OPEN.** The maintainer requested wrap-up after reporting a third product
cybersecurity block and excluded further code changes, native analysis and
executable instrumentation. Those activities stop here. This checkpoint does
not complete the [original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_observer_remediation_live_readiness.md`).

No retail episode, deployment, game attachment, original-save write, configuration
change, staging, commit, push or publication occurred. The offline protection
check created a local Save52 rehearsal COPY. B1 remains historical PARTIAL and
D5AA remains ESCALATE. Exact block triggers are not visible in tool diagnostics.

## Changes preserved

| Group | Files and purpose |
|---|---|
| Existing runtime | `runtime/construction-winner/observer.h`, `bridges.asm`, `transport.h`, `transport.cpp`, `plugin.cpp`: candidate schema 3, constructor/publication and consumed-token witnesses, reserve/store distinction, eighteen sites, larger queue, loss accounting, recursion/worker diagnostics and worker thread identity. |
| Existing build/fixture/reader | `runtime/construction-winner/build.py`, `fixture.asm`, `fixture.cpp`, `host.cpp`, `read_capture.py`, `README.md`: disposable qualification, measured memory, representative traffic, schema dispatch and instructions. |
| New runtime source | `runtime/construction-winner/reduce_v3.py`, `queue_stress.cpp`, `worker_health.py`: reducer, production-queue controls and read-only thread health helper. Future watch mode has not been exercised against a game. |
| New research methods | `research/resource-retained-population/d5ab_lifetime_export.py`, `d5ab_native_sites.py`, `d5ab_qualify.py`, `d5ab_queue.py`. |
| Documentation | [Ledger](d5ab-investigation-ledger.md), [native map](d5ab-native-map.md), [schema](d5ab-architecture-schema.md), [preliminary source index](d5ab-sources.csv), this report, [review](d5ab-review.md), [decision](d5ab-decision.md), [proposed B2 card](run-card-d5x-b2.md), credits/source/state and brief navigation. |
| Supplied input | The D5AB brief was already untracked at task start. Complete patch includes it; task-only excludes it. |

The gameplay checklist was not changed or newly ticked. Maps, source index and
run card are working documents, not a final compatibility/readiness manifest.
The source freeze `.local-work/d5ab/handoff-freeze01.json` pins all seventeen
changed/new source files at wrap-up. Only documentation/status/export work follows.

## Completed tests and their limits

| Check | Actual result | Local primary receipt |
|---|---|---|
| Compiled disposable suite | 61 cases; zero unexpected exits; sources unchanged during build. Native-shaped hooks, fault, STOP and crash controls. | `.local-work/d5x/d5ab-build08/build.json` |
| Representative callbacks/writer | All seventeen event categories; 21,061 durable records, zero losses; injected three-second raw-flush pause. Peak working set 16,015,360 bytes. | `.local-work/d5x/d5ab-build08/representative/terminal.json` and `fixture.json` |
| Current reader/reducer | 54 semantic and eight damaged-session controls pass. Current reader/reducer hashes match this receipt. | `.local-work/d5ab/controls-final02/receipt.json` |
| B1 compatibility | Full schema-2 reduction equals frozen reader output: 19,780 durable records, zero qualified first-construction chains. No B1 append observation is invented. | Same Final02 receipt |
| Production queue | Three repeats at each capacity; ID/count/sequence, wrap, delayed publication, overload, retry, recursion, diagnostic fallback and STOP controls pass. | `.local-work/d5ab/queue-final32000-02/receipt.json` |
| Worker helper | Nine own-Python-thread tests pass, including identity mismatch, actual exit and stale ACK rejection. Complete future controller integration is unqualified. | `.local-work/d5ab/worker-health02/receipt.json` |
| Original reserve helper | Six bounded helper controls pass with synthetic allocation callbacks; no complete allocator or retail OOM claim. | `.local-work/d5ab/append-native01/control.json` |
| Offline protection | 98 protected saves/backups, three installed inputs, 23 configuration files and verified Save52 rehearsal COPY. Historical strict failures remain preserved. | `.local-work/d5p/d5ab-offline-preflight01/protection.json` |
| Export preservation | Completed read-only/no-analysis exports preserve database pins. Export03 is incomplete and retained. Interpretation/completeness remains unfinished. | `.local-work/d5ab/lifetime-export01` through `04` |

The held-consumer workload offers 32,000 records, initially stalls three seconds
and defers draining until producers finish. These are compiled queue measurements.

| Cells | Compiled queue bytes | Held-burst losses in each repeat | Whole-process peak working-set range, bytes |
|---:|---:|---:|---:|
| 1,024 | 327,680 | 30,976 | 6,086,656–6,606,848 |
| 8,192 | 2,621,440 | 23,808 | 8,765,440–8,953,856 |
| 32,768 | 10,485,760 | 0 | 18,079,744–18,726,912 |

Unpaced overload still loses records at every capacity; its tests verify honest
accounting. These constructed workloads establish neither universal zero loss
nor native/retail completeness. A non-target fixture cannot close target D5R.

## Failures and unresolved work

- Build03's deliberately invalid source operand faulted at address `0x69` before
  the observer refusal test. Only that disposable host was stopped after PID/path
  verification. A corrected fixture substitutes the consumed operand; later full
  suites pass. Original failure and user screenshot/hash remain local.
- Early independent review returned REWORK. Corrections address loss history,
  lifetime joins, interleavings, collisions, QPC ties, bounded accounting and worker
  identity. No final exact-snapshot engineering/scientific acceptance exists.
- Native source-lifetime/free-path and identity-writer coverage is not closed.
  Additional census/cleanup evidence is preserved, not promoted to completeness.
- The future worker watcher/controller, controller-failure behavior and B2 protocol
  integration need qualification. No final identity-bound candidate bundle or
  accepted readiness audit exists. General asynchronous unwind coverage is limited.
- Full editorial review of changed source comments/docstrings and scientific
  qualifications remains unfinished. A clean patch export is not integration approval.
- The three user-reported product blocks have no exposed exact classifier reason.
  No bypass was attempted. The diagnosed fixture crash is a separate event.

## Original contract accounting

AB-Q1 through AB-Q5 all remain **INCOMPLETE**: source/lifetime proof; transition
qualification; final transport/safeguard review; interpretation/completeness review;
and integrated B2 readiness respectively. This is a user-directed stop, not a
scientific BLOCKED result or an accepted completion.

The matrix grades full criteria, not individual passing controls. NOT TESTED
means the entire mandatory criterion has not been verified.

| Criterion | Status | Reason |
|---|---|---|
| AB-AC01 | PASS | Recorded offline policy/identity boundary; no prohibited retail/Git action. |
| AB-AC02 | PASS | Frozen questions, active ledger and D5R OPEN preserved. |
| AB-AC03 | NOT TESTED | Full identity/lifetime proof and final challenge unfinished. |
| AB-AC04 | NOT TESTED | Store/helper tests pass; complete source/epoch qualification unfinished. |
| AB-AC05 | NOT TESTED | Fixture category coverage passes; essential native coverage not closed. |
| AB-AC06 | NOT TESTED | Scoped measurements pass; final integrity/operational review remains. |
| AB-AC07 | NOT TESTED | Extensive controls pass; comprehensive contract coverage not independently accepted. |
| AB-AC08 | NOT TESTED | Versioned tests and compatibility pass; final semantic sufficiency review remains. |
| AB-AC09 | NOT TESTED | Proposed card is not integrated, identity-bound readiness. |
| AB-AC10 | NOT TESTED | Final preservation/inclusion audit requires independent review. |
| AB-AC11 | FAIL | Required final substantive review is absent; preliminary REWORK retained. |
| AB-AC12 | NOT TESTED | Full editorial finalization remains unfinished. |

HEAD remains `1fe5c6c7a423300a9879dff15ed72e9a69b726cd`; index SHA-256 remains
`f2dadae3e3ec69de4889c54744fac79c4edaf3b99b4b8e5bda6419d3962f9942`.
Changes are unstaged and uncommitted. [Review exports](d5ab-review.md) provide
exact status, inclusion/exclusion inventory and patches. Binaries, native bytes,
raw captures, saves, databases, screenshot and private receipts remain ignored/local.

Suggested conventional commit message, not executed:

```text
chore(d5ab): checkpoint incomplete observer remediation
```
