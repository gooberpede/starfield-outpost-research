# RG2-D5P-R1 — SFSE Retained-Population Observer: Context Repair, Loss Resilience and Evidence Recovery

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Offline diagnosis, justified implementation, disposable Windows native qualification, independent review and *proposed* follow-up run preparation only.  
**Retail Phase B retry:** **NOT AUTHORIZED**. No Starfield/SFSE launch, Vortex action, protected-save operation or live instrumentation under this brief.  
**Scientific status:** D5P Phase B FAILED / hypothesis UNRESOLVED. **B6/publication ON HOLD.**  
**Principle:** **Permissive acquisition; conservative conclusions.** Freeze R1-AC1–R1-AC9 before implementing.

## 1. Purpose and starting evidence

Repair the existing D5P in-process SFSE observer where a demonstrable correction is possible, without abandoning its eleven-hook architecture merely because the first retail trial failed. The objective remains the D5P complete witnessed-region causal chain: initiating source query/context → visited/map decision → directly sampled resource mask → successful region geometry and retained ownership → subsequent reuse within a qualified source/manager lifetime. Do not confuse a candidate, first-observed event, map insertion, visited guard or wrapper allocation with retained, reused geometry.

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, the original `docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_SFSE_retained_population_observer.md`, D5P Phase A design/tests/reviews, `docs/experiments/resource-retained-population/d5p-phase-b-{authorization,review}.md`, `d5p-phase-b.md`, its source ledger, relevant original local evidence and readers. Inspect the actual plugin source, build identity and current branch before modifying anything. Preserve D5L–D5O methodological lessons and the preceding D5H/D5I conditional-mask baseline.

Observed Phase B facts to reconcile, not explain away: 1,592 authenticated admitted records; one reported admission drop followed by recorder retirement; 319 source-demand observations all context-invalid; seven query/mask pairs, six completed regions and eleven lookups without a qualified selected-source chain. A single drop did **not** prove the queue was full: the old counter conflated capacity with bounded CAS contention. Retirement prevents counting later missed events. The target remains second Feynman V `0:37536:20928:0029d20e` / Save52, but **no retail target operation is authorized**. Do not fit a mask, geographic key or pointer association to held-out expectations.

## 2. Mandatory diagnosis before substantive repair

Produce a concise, dated diagnosis/decision record **before changing the relevant production paths**, enumerating hypotheses, original evidence, inspection points, tested discriminators, remaining unknowns and intended minimal repairs. If source-level inspection or archived evidence cannot distinguish competing causes, document that limit and design narrow, safely bounded diagnostic observability. Do not retrospectively present a guess as a verified root cause.

**Native-context failures:** Decompose every composite invalid-context outcome into explicit, stable reason codes (read failure/partial read, pointer or ABI interpretation, manager/object identity, Grid extents, source membership, lifetime, other named predicates). Retain enough safe, bounded original operands and provenance to investigate the first failing predicate without treating unreadable memory as zero or retaining unsafe raw pointers as scientific identities. Reconcile call-site register/stack semantics and version-pinned native structures against actual retail binary/disassembly and available native controls. Check whether checks are incorrectly applied to legitimate non-target contexts. Do not simply weaken validation to make hits appear.

**Recorder admission failure:** Inspect producer concurrency, CAS retry exhaustion, queue occupancy, consumer throughput, write/flush latency and error paths. Separate queue-full from contention-retry exhaustion, intentional safety rejection and persistent output/recorder failure. Identify whether the observed single reported drop can be reproduced; if not, retain that uncertainty. Assess batching and bounded queue/producer improvements against native-hook latency and game safety. Preserve correct ABI/original-call semantics, source lifetimes, nested requests and hook-site/version guards; add/alter hooks only with explicit evidentiary justification.

## 3. Revised acquisition contract — non-negotiable

Ordinary dropped observations **do not stop the session, disable wrappers or retire the recorder**. Continue attempting admission through the agreed experiment endpoint, with automatic recovery when capacity returns. Never spin or block indefinitely inside a hook; bounded retries/backpressure only where demonstrably safe. No silent skipping, selective throttling or undiagnosed loss. An irrecoverable output failure may prevent further durable recording; report that distinctly and preserve existing evidence. A genuine native hook safety failure may require fail-safe deactivation, not continuation at the cost of process safety. The disk-space safety floor, originally **40,000,000,000 free bytes on each applicable C: and D:**, remains a hard guard; respect the repository's protected-input/STOP protocol.

**No arbitrary maximum event count, capture-byte quota or extra time limit.** Maintain a bounded in-memory queue and the explicitly scheduled operator run endpoint; stream to durable storage, using rotation/segmentation only if justified by filesystem reliability or recoverability, with verifiable continuity across segments. No cap silently imposed by fixtures, ring buffer, parser, manifest, ZIP packaging or postprocessor. A resource-related safety bound must be documented, motivated, exposed and distinguished from scientific sampling limits. A future retail run card must permit a normal scheduled finish despite ordinary drops, unless an established operational STOP condition occurs.

Expose independently meaningful, overflow-safe diagnostics: total admitted/write/flush/verified counts; losses by cause; known exact drop counts versus **unquantifiable disabled/unobserved intervals**; first/last loss boundaries; queue occupancy/high-water mark; producer retry/contention and consumer progress; output/flush faults and recovery transitions. Use cheap atomic aggregates and bounded gap/watermark markers so the diagnostics themselves do not provoke a new drop storm. Make monotonic sequence and durable provenance semantics explicit: sequence gaps alone must not be interpreted as exact counts where sequence allocation occurs after admission. Preserve correct identities, framing, CRC/hash, crash-prefix recovery and startup/READY/closure compatibility or supply versioned reader migration.

## 4. Scientific reduction of incomplete recordings

Decouple **capture/session health** from **record authentication** and **claim qualification**. Independently authenticate every recoverable segment/record, including a valid durable prefix after a crash or failed final flush. Analyse useful observations before and after a drop without claiming an uninterrupted session. Produce at least: **qualified**, **candidate/incomplete**, **contradictory**, and **indeterminate** findings, plus explicitly unqualified source/map/geometry/retention/reuse stages. A healthy run with no selected-source observation is not automatically a qualified negative; an incomplete run cannot justify absence from silence.

Define a conservative **loss influence model**: bound loss windows when possible; track which causal joins require uninterrupted observation of generation, ownership, source/manager lifetime or invalidation; propagate contamination to chains that may cross those windows. Do not assume independent sources or unaffected lifetimes merely from observed pointer/key inequality. Retain a chain as qualified across loss only when an independently demonstrated witness or logically sufficient continuity certificate excludes all missing decisive events. Preserve partial successfully copied regions, contradictory payloads and orphan observations without stitching identities across resets, ABA reuse or unsupported aliases. Keep every accepted historical finding immutable and show scientific deltas explicitly.

## 5. Implementation and qualification

Implement only diagnosed, reviewable corrections. Reuse the existing eleven-hook SFSE plugin and native fixtures wherever defensible; record rationale and risk for any architecture or evidence-format change. Version the plugin, reader, evidence schema, build inputs and resulting identities. Rebuild reproducibly and exercise the **actual compiled native interception/recorder code** in disposable Windows processes, not merely mocked JSON emitters. Do not claim synthetic success proves retail Starfield integration.

Mandatory adversarial controls:

1. Reproduce or discriminate each Phase B composite context-invalid route with exact failing predicate, including valid non-target contexts, ABI/pointer and manager/Grid/source membership tests; demonstrate one genuinely valid context and correct rejection of invalid/ambiguous contexts. Where actual retail cause is still unverified, retain explicit uncertainty.
2. Force **one** and **many** queue-full and contention losses, then recover under concurrent, nested and bursty production; prove later authentic records and valid unaffected causal chains survive through **scheduled end**, without permanent observer retirement or hangs.
3. Sustain an **unpaced** load representative of or more demanding than the observed retail bursts, quantify throughput/queue peaks and loss behavior. The former paced 34/34 synthetic qualification alone is not sufficient. Do not set an artificial record-count ceiling; finite-duration stress fixtures are permissible for repeatable tests and must be labelled as such.
4. Exercise source retirement, map erase, reset, Grid clear, pointer reuse/ABA, partial append/copy, failed population, contradictory geometry and lost lifetime/invalidator records. Demonstrate conservative contamination and zero false complete chains.
5. Exercise torn/corrupt records, multi-segment continuity, disk guard, write/flush failures, shutdown without final acknowledgement, and crashes before/after durable acknowledgement. Confirm correct differentiation of durable prefixes, missing tails, unknown loss totals and authenticated but scientifically insufficient data.
6. Verify exact version/hook-location/prologue/relocation and trampoline/original-call safety; measure hook hot-path overhead and detect recursion/deadlock/unsafe blocking. Compare the scientific controls proportionately; do not redo unrelated geometry experiments.

For every control, provide invocation, native DLL/build identity, expectations, actual count/results, counterexamples and limits. Independent reviewers should rerun representative executable tests where feasible, explicitly distinguishing performed reruns from inspection of receipts. Any unresolved material root cause, unvalidated context contract or unresolved instrumentation safety concern is **NO-GO for retail**, even if the revised recorder survives drops.

## 6. Authority, deliverables and reviews

**Codex may** inspect repository/local evidence read-only, edit task-owned source/tests/analysis/docs, build and run disposable native fixtures, and replace its own ignored scratch. **Codex may not** install/enable/disable/remove through Vortex, deploy to Starfield, launch Starfield/Steam/SFSE, load Save52, change protected saves/game configuration, force generation, repeat the live trial, publish/B6, stage, commit or push. Observe the baseline archive-backed and 40 GB free-space protections. The maintainer owns all future game/Vortex actions after a separate explicit GO. Do not treat Phase A repairs as an implicit Phase B authorization.

Deliver:

- A D5P-R1 diagnosis and design record **written before production repair**, identifying confirmed versus suspected causes and the actual sequence of decisions.
- Corrected plugin source/build/test harness, versioned schema/readers, reproducible tests and local-only raw receipts; if repair is not feasible, a bounded no-repair diagnosis with precise missing capability rather than fabricated success.
- A concise D5P-R1 result and scientific-impact report, preserving D5P's FAILED/UNRESOLVED history and identifying evidence that can/cannot be salvaged from Phase B.
- A **proposed only** revised retail run card, with precise READY and postflight guards, maintainer-owned Vortex/SFSE operations, scheduled stop and loss-resilience behaviour; no deployment is authorized. Prepare a reviewable package only when qualification supports it; freeze exact DLL/ZIP identities and manifest hashes.
- Independent **engineering, scientific and editorial** reviews against the frozen criteria; substantive concerns addressed before final review. Include exact complete and task-only diffs, hash-bound source/binary/evidence manifests, status/exclusions and no staged/committed/pushed changes. Follow repository conventions for document location and provenance. Avoid massive redundant logs, unrelated housecleaning or needless proliferation of records.

## 7. Frozen acceptance criteria

| ID | Acceptance requirement |
|---|---|
| **R1-AC1 Authority/protection** | No retail launch/deployment/Vortex/save changes, no unauthorized commit/publication; protected inputs and evidence remain unchanged, guards retained. |
| **R1-AC2 Historical diagnosis** | Phase B source records and actual code audited; context and admission causes separated; decision record precedes substantive changes; unknowns disclosed. |
| **R1-AC3 Native qualification** | Reason-coded context checks, grounded ABI/object/source semantics, safe original-call behaviour, no loosened proof or fabricated source identities. |
| **R1-AC4 Resilient acquisition** | Single/multiple ordinary drops do not retire acquisition; recovery through scheduled end, cause-specific loss metrics, bounded hook work, no arbitrary event/data cap. |
| **R1-AC5 Scientific conservatism** | Authenticated partial evidence independently analysed; gap/lifetime contamination sound; no unqualified first-construction, retention, reuse or negative claim. |
| **R1-AC6 Durability/failure safety** | Segments/flush/crash and disk/output failures qualified; durable prefixes retained, uncertain tails/losses stated, fail-safe native behaviour demonstrated. |
| **R1-AC7 Actual native tests** | Built plugin interception/recorder exercised in adversarial disposable Windows tests, including unpaced contention and post-loss qualified chains; results reproducible and limits clear. |
| **R1-AC8 Future operations gated** | Corrected package/run card are proposals only; exact pin and READY checks, scheduled termination, 40 GB guards, operator-only actions, separate explicit retail GO. |
| **R1-AC9 Independent review/delivery** | Engineering/scientific/editorial reviews, focused durable reporting and versioned schema, complete/task diffs with exact hashes; no stage/commit/push. |

**Completion rule:** A repaired synthetic observer is not proof of retail reliability or the target hypothesis. Return **ACCEPT for offline readiness** only if all relevant criteria pass; otherwise **REWORK or NO-GO** with precise remaining defects. **No D5P-R1 outcome authorizes a second live session.**
