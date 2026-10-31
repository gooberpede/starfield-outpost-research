# CODEX BRIEF — SOR RG2-D5AB-P2: Controller, Reducer and Transport Qualification

**Status:** Proposed implementation brief. Assignment authorizes **offline** code changes, builds, disposable tests, integration, documentation and independent review **within P2**. It does **not** authorize Starfield launch, live process attachment, observer installation/activation, Vortex changes, protected-save modification, B2 execution, staging/commit/push, release or publication. These require separate maintainer authority.

**Repository:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`). Start from the committed D5AB checkpoint and C1/C2 assessments; verify actual HEAD/source identity. Do not silently transfer offsets or claims across executable builds.

**Parent contract:** D5AB's five controlling questions and twelve acceptance criteria remain unchanged. This is a bounded engineering work package, **not** permission to declare D5AB complete, source lifetime qualified, or B2 ready. D5R (historical target first construction) remains open. In particular, preserve C2's unresolved L1/L2 source ownership, lifetime, identity initialization and alternate cleanup edges for P1/P3.

## Required reading and baseline

Read current `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/SAVE_PROTECTION.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/reviewers/research-completion-reviewer.md`, and `docs/templates/completion-contract.md`. Read original `CODEX_BRIEF_SOR_RG2_D5AB_observer_remediation_live_readiness.md`; the D5AB bounded-handoff report; D5AB-C1 assessment/matrix/decision; D5AB-C2 audit/evidence-matrix/decision; D5X schema, transport and B1 run-card safeguards; D5Y/D5AA recorder and chronology findings. Preserve historical verdicts and evidence. Pin source snapshots, executable/build identities, schemas, fixtures and receipt hashes; distinguish authoritative existing evidence from claims not locally accessible.

Create an **active P2 investigation ledger near the beginning**. Maintain per-requirement unresolved dependencies, attempted remedies, test outcomes and counterexamples throughout the assignment, not only at closeout.

## Frozen P2 questions and completion conditions

- **P2-Q1 — Transport:** Does the final P2 recorder transport preserve all admitted records, order/correlation and durable acknowledgments under explicit representative concurrent workloads, accurately count losses under intentional overload, and fail safely on worker/IO/session faults? **COMPLETE** only with exact-source compiled integration tests, zero drops in each *qualified lossless* workload, adverse controls and honest limits; model replay or a larger queue alone is insufficient.
- **P2-Q2 — Worker/controller:** Does the actual session controller monitor the **real recorder worker** and distinguish healthy operation, transient delay, termination, write/flush fault, operator STOP and partial evidence finalization, without arbitrary time/volume/cadence retirement? **COMPLETE** only with integrated executable tests and reproducible receipts, not just Python-owned thread mocks.
- **P2-Q3 — Reader/reducer:** Can the exact versioned producer/reader/reducer combination accept qualified records and reject damaged, incomplete, cross-epoch, ambiguous-identity or loss-contaminated firstness claims, including unsuccessful versus successful visited append? **COMPLETE** only after reconciling the Build08-versus-later-reducer discrepancy and passing positive and adversarial fixtures against the final implementation.
- **P2-Q4 — Scoped integration and handoff:** Is the final P2 source/build/test lineage reproducible, independently reviewed, and clearly limited to P2 engineering? **COMPLETE** requires final exact-snapshot provenance, all scoped acceptance criteria, detailed P1/P3 dependencies, and explicit **B2 NOT AUTHORIZED**.

## Implementation authority and technical boundaries

**Authorized:** Refactor/correct recorder queue and writer, health-monitoring/controller integration, evidence framing/ACK/reader/reducer, schemas and their compatibility handling, offline harnesses and tests; build and execute these components and **existing native observer DLL in a disposable offline host where safely and meaningfully exercisable**. Investigate and repair in-scope faults; retest without seeking a new brief for routine corrections. Measure actual native layout, memory consumption and throughput. Preserve all original capture and protection mechanisms.

**Not authorized:** New Starfield executable reverse engineering/disassembly, new native source-lifetime hooks, changed assembly bridge sites or source-identity acquisition semantics, assumptions closing C2 L1/L2 gaps, gameplay launch/deployment, modification of protected saves, or a live B2 run. If an in-scope test exposes a defect requiring out-of-scope native modifications, preserve the failure and identify exact dependency for P1/P3; do not silently relax a test or redefine an acceptance gate. Do not suppress global resets, unrelated sources, append outcomes or other events needed for firstness just to reduce traffic.

### Transport and loss controls

1. Baseline the 1,024 / 8,192 / 32,768 configurations (or document stronger equivalent comparison), with measured compiled cell size, memory and competing workload characteristics. Treat 32,768 as the current candidate, **not** a prescribed proof of reliability.
2. Test concurrent producers, producer reservation/publish races, queue wraparound, sustained throughput, finite bursts, slow and stalled worker, delayed wake, multi-second I/O/flush pauses, contention/retry exhaustion and intentional queue saturation. Check every admitted sequence, counts, ordering relations, queue high-water and loss-cause metrics. Qualified lossless workload: **zero lost events**, no fabricated ACKs and fully consistent raw/ACK/terminal totals. Intentional overload must report loss honestly and invalidate any affected historical-first claim; it need not remain lossless.
3. Inject write, flush, ACK, CRC/frame, truncated-tail, session-identity, status/guard and STOP/teardown faults. Distinguish bytes written, durably flushed, acknowledged, admitted and lost; never promote complete admitted-record finalization into full native-event coverage. Preserve evidence, nonrecursive logging, disk guards of **40,000,000,000 caller-available bytes on both C: and D:**, identity/guard controls, resident-inert shutdown constraints and the existing protection policy.
4. Preserve project policy: no arbitrary scientific time, byte, event-count or routine-monitoring-cadence cutoff; delayed response alone is not worker failure. Where a safety-critical engineering bound is indispensable, document it and obtain approval before any live use.

### Actual worker and controller integration

1. Integrate monitoring with the **actual recorder worker lifecycle** and session controller rather than relying solely on synthetic/Python thread handles. Confirm whether existing APIs can inspect worker status without unsafe interference; keep failure and health signal provenance explicit.
2. Exercise normal progress, delayed but healthy worker, unexpected worker exit, failed writer/raw flush/ACK flush, queue losses, stale controller identity, controller restart/disconnect, operator STOP, and incomplete finalization. The controller must surface correct health and uncertainty, preserve original data and perform only authorized recovery/STOP actions.
3. Qualify combined workflow in a disposable process/host where possible, including load, steady producer traffic, impairment, STOP, raw/ACK reconciliation and readback. Do not equate disposable host behaviour with Starfield retail execution.

### Reader, reducer and source/version correspondence

1. Pin the **exact final** producer, schema, transport, controller, reader and reducer versions together, with build recipe and reproducible receipts. Resolve the C2 historical Build08 reducer mismatch by new tests of the final combination, not by editing old receipts.
2. Retain backwards compatibility only where supported and tested; reject mismatched schema/identity instead of guessing. Test old D5X evidence separately from new schema evidence.
3. Include positive and negative native/synthetic fixtures: reset-to-unvisited, cache hit versus visited bypass, reserve attempt versus `0xffffffff` failure versus actually executed token store, source lifetime ambiguity, pointer/token/key collision or reuse, reset/retirement/epoch transitions, lost event or unarmed interval, missing descriptor/sample, cross-thread ordering, damaged/truncated frames, duplicated and malformed ACKs. Native source-lifetime joins unresolved by P1 **must remain unqualified** even if fixture logic is correct.
4. Verify the reader can reject an unsupported scientific assertion without discarding valid lower-level evidence. Where no later bypass naturally occurs, a qualified first construction must not require an artificial bypass as a prerequisite.

## Specialist sub-agent and independent review

Codex **may** delegate a bounded substantive technical workstream to a specialist sub-agent (preferably transport/concurrency and real-worker integration). The primary agent owns design, integration, code changes, tests, acceptance matrix and final delivery; it must verify specialist conclusions and preserve all specialist findings, patches, failed cases and fixtures. Specialist may challenge/recommend a different in-scope design, not modify the original D5AB completion contract.

**Maximum two concurrently active sub-agents**, not a total invocation limit. The independent reviewer must not have implemented or authored the work it reviews; a specialist implementer cannot serve as the final independent reviewer. Give the reviewer the original P2 brief, D5AB parent criteria, current complete source, ledger, primary evidence, failing tests, specialist output and exact final snapshot. If the sub-agent system cannot provide independence, use the project's documented independent-review fallback; never invent reviewer acceptance.

## Cybersecurity interruptions

Previous D5AB blocks were unexplained and are treated as an unresolved apparent anomaly, **not** a blanket reason to refuse or narrow otherwise authorized research. Do not preemptively euphemize or remove legitimate technical work, alter objectives or weaken tests out of concern for a hypothetical block. If an actual enforced refusal occurs, record its exact available message, time/context, attempted action and effect. Respect the refusal: do not disguise or circumvent the blocked operation or repeatedly retry it as evasion. Continue unaffected authorized work where feasible; escalate if an indispensable requirement remains genuinely inaccessible. Preserve the original criteria and do not classify an interruption as proven false positive without evidence.

## Required artifacts and primary evidence

Place durable P2 documents under `docs/experiments/resource-retained-population/`, using descriptive `d5ab-p2-*` filenames:

- Active investigation ledger with chronological meaningful checkpoints, hypotheses, counterexamples, failed approaches and next actions.
- Engineering report identifying final architecture/deltas, test matrix, measured workloads, transport/worker health and observed limits.
- Source/schema/build provenance ledger resolving the Build08/reducer mismatch and binding **final** component versions to executable tests.
- Test receipts and reproducible scripts/fixtures, including full positive/negative/impairment results and non-passing cases; proprietary/raw local artifacts remain local under `.local-work/`.
- Exact P2-to-D5AB question/criterion mapping, P1/P3 dependencies and B2 NOT AUTHORIZED disposition.
- Independent final-snapshot engineering/completeness review, separate scientific-readiness and editorial dispositions, exact verified delivery manifest, `d5ab-p2-task-only.diff` and `d5ab-p2-complete.diff` (when there is no unrelated uncommitted work, at least complete); don't stage/commit/push.

Retain the existing 31-item gameplay-stage research checklist; update it only for newly demonstrated native/gameplay facts, never for merely passing offline engineering tests.

## Mandatory acceptance criteria (frozen)

1. **P2-AC01 Scope and baseline:** Verify project permissions, committed C2 baseline, actual changed-file/source identity and parent D5AB contract. No unauthorized native hook research, game operation or publication.
2. **P2-AC02 Transport:** Exact-source tests of representative concurrency, queue wrap, backpressure, measured capacity/throughput, lossless and deliberately lossy conditions, correct loss/ACK/STOP/integrity accounting; faults corrected and regressions rerun.
3. **P2-AC03 Worker/controller:** Real-worker/controller integrated tests for normal/delayed/dead/faulted/STOP cases with accurate health classification, evidence preservation and documented operational boundaries.
4. **P2-AC04 Reducer:** Pinned final producer/schema/reader/reducer; Build08 mismatch resolved through final-source qualification, comprehensive positive and discriminating negative controls, fail-closed chronology claims at losses, identities and epochs.
5. **P2-AC05 Integration and regression:** Disposable offline host exercises actual native observer DLL where safely feasible; final combined component tests, reproducible source/build receipts, failure log, verified compatibility and explicit limitations. If unsafe or genuinely blocked, apply terminal-barrier proof, not silent test omission or equivalence to mocks.
6. **P2-AC06 Provenance and bounded parent mapping:** Per-question/criterion outcome ledger P2-Q1–Q4 and original D5AB-Q1–Q5/AC01–AC12; no unwarranted L1/L2 closure, B2 readiness or historical target construction claim.
7. **P2-AC07 Independent completeness and editorial review:** Independent reviewer challenges original criteria, specialist work, test coverage, highest-value omitted cases, evidence integrity and exact final source; all substantive fixes requalified and reviewed; final prose audited per `EDITORIAL_STANDARD.md`.
8. **P2-AC08 Delivery and preservation:** Verified exact complete/task-only diffs, manifests, original test failures and inputs preserved; no staging/commit/push, deployment, save mutation or live run; explicit engineering, scientific and editorial verdicts.

## Completion and escalation contract

Apply `docs/RESEARCH_EXECUTION_PROTOCOL.md` and the compact completion contract. **COMPLETE / ACCEPT** requires all four frozen P2 questions and eight mandatory P2 criteria proven by primary reproducible evidence on the final source plus independent review. A valid scoped negative finding is not a substitute for a missing mandatory *engineering* requirement. If accessible work or corrections remain: **INCOMPLETE / REWORK**, continue within this assignment. Claim **BLOCKED / ESCALATE** only with exact indispensable missing edge/capability/authority, actual attempts, alternatives, barrier class and smallest needed permission or resume checkpoint. An accepted P2 changes neither D5AB's unfinished L1/L2 obligations nor B2's unauthorized status. No completed planning documents or partial tests should be presented as engineering readiness.

**Delivery summary:** state changed files, all test counts and failures, observed throughput/loss limits, original D5AB status, independent review verdict and precise remaining P1/P3 obligations. Recommend a commit message only after final review; leave repository changes unstaged.
