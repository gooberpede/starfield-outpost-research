# RG2-D5Y — D5X-B1 Retail Capture Forensics and Recorder Performance

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Offline, evidence-first research into the completed D5X-B1 capture, with **conditional authority** for narrowly justified observer/reader repairs and disposable qualification.  
**Live authority:** **NONE.** No Starfield/SFSE launch, Vortex operation, debugger attachment, live session-control writes, save changes or retry. B1 has been consumed; B2 remains **NOT AUTHORIZED**.  
**Publication/B6:** ON HOLD.  
**Status:** Implementation/research brief. Freeze D5Y-Q1–Q3 and D5Y-AC1–AC11 before substantive work.

## 1. Controlling question, baseline, and completion contract

**Controlling objective:** Establish why the completed D5X-B1 acquisition did not prove a construction path for the selected Feynman V source, and characterize the causes and consequences of recording pressure sufficiently to determine whether a targeted, scientifically safe engineering improvement is warranted. Do not confuse a genuine absence of target execution with an absence of authenticated target records.

Stable questions:

- **D5Y-Q1 — Target attribution:** What can *all* authentic B1 evidence establish about the target source, at every observation stage, and where precisely does attribution become unsupported or indeterminate?
- **D5Y-Q2 — Admission loss and throughput:** What explains the observed recorder pressure, in what temporal/operational phases was it experienced, and which causal and performance claims are or are not supported by the retained telemetry?
- **D5Y-Q3 — Appropriate remedy:** Is an observer, recorder, reader, telemetry, operational or no-change response justified by Q1/Q2? Where a tractable code defect is proven, implement the smallest safe repair and qualify it offline. If the present evidence cannot discriminate the cause, identify exactly the missing telemetry and the smallest independently justified way to obtain it.

The task is not completed by producing a good incident report that leaves a material authorized analysis unperformed. Follow dependencies within the offline and disposable scope. Under the current governance rules, report each question **COMPLETE**, **INCOMPLETE** or **BLOCKED**, with question-level evidence and an independent completeness challenge. A specific method may have a bounded negative result while the parent question remains open. Scientific completeness, engineering readiness and any prospective retail authorization are separate dispositions.

**Known B1 record, to reauthenticate rather than assume:** One authorized Save52 load followed by one ordinary travel to Feynman V Cu IL F; 19,780 admitted/authenticated records; 9,957 queue-full losses, no reported retry-exhaustion or output faults; 19 complete ordinary paths on *non-target* sources; 24 authenticated map decisions, none positively identifying target `0:37536:20928:0029d20e`; pre-travel checkpoint 110 admitted records and zero reported drops; final recorder and protected postflight accepted. This is **PARTIAL NATIVE COVERAGE**, *not* a full B1 PASS. The earlier acceptance was of the bounded partial-run account only. It does not provide B2 authority or evidence that the target did not execute.

## 2. Required starting material and authority boundaries

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, and `docs/reviewers/research-completion-reviewer.md`. Read the current D5X architecture/schema/report/review, B1 pre-authorization audit and amended card, B1 live authorization, ledger, report, reader/coverage reporter, recorder/hook source, relevant prior D5P–R3 lessons, and native source/key studies from D5Q–W. Check actual local paths and identities; do not assume that the text patch contains private raw B1 evidence.

Inputs may include authenticated original B1 raw frames, cumulative ACKs, READY/challenge/health/STOP receipts, PID/time identity, operator checkpoints, terminal status, archive members, exact local build/DLL/source pins, previously reviewed native fixture evidence and relevant source-location geometry. Read existing protected archives using the established access API. Preserve raw originals, archive membership and hashes. Use task-owned ignored scratch for derivatives and tests. Do not reinterpret fixture-host data as retail evidence.

**Allowed:** read-only analysis of existing records and native executable/Ghidra state; bounded task-owned scripts; disposable isolated Windows native fixtures; modifications to task-owned observer/recorder/reader code **only if justified by the diagnosis**; offline package preparation and independent review of any revised candidate.

**Prohibited:** Starfield/Steam/SFSE process launch; game injection/attachment; Vortex operations; modifying, loading or resaving protected saves in the game; changes to the installed game, plugins, configurations or active profiles; native hot-unpatching; automatic cleanup of protected evidence; staging, commit, push, third-party disclosure or publication. Do not alter existing scientific outcome classifications or retroactively mark B1 full PASS. Retain the 40,000,000,000-byte C:/D: caller-available floors where applicable.

## 3. Q1 — Exhaustive target-source attribution from existing evidence

The primary target is **second Feynman V** source `0:37536:20928:0029d20e` (owner FormID `0x0005e0de`), not merely any same-owner source. Do not confuse geographic keys, source-pointer allocations, visited identity, SFBK FormID, saved outpost/beacon identity or a nearby selected source. Verify the target key derivation against the pinned constructor/source descriptors, and distinguish valid bytes from partially populated or failed reads.

For **every** available authentic event class, not only complete chains or map decisions, investigate:

1. Provider entry, original Int2, invocation/parent/thread/frame and geographic demand context.
2. Selected cursor/source pointer, copied source-byte status, candidate geographic key and source-selection provenance.
3. Visited decision (including bypass), source-map lookup/result and actual decision epoch.
4. Converter/engine-local descriptor, generator call and direct sampler result, including incomplete or contradictory chains.
5. Lifecycle fences, cold/reset acknowledgements, invalidations, source retirement, pointer reuse, loss epochs and orphan/unknown records.
6. All relevant identifiers and admitted source keys elsewhere in the target's geographic support and the actual travel-period capture.

Produce **first-positive/last-positive and deepest-stage** accounting for the target, and explicitly distinguish: (a) no authenticated target event in a particular category, (b) a positive target selection that cannot be qualified later, (c) a witnessed bypass/hit/miss, (d) loss- or context-indeterminate material, and (e) positively qualified non-target paths. An incomplete selection with authenticated source bytes may be informative without qualifying a full chain; never turn unread or zero-initialized fields into observed source IDs. Prior invalid or missing events cannot be erased by a later valid-looking chain.

Reconstruct the geographical scope of actual admitted requests and selected sources against D5Q–W target-support evidence without inferring that every geometrically eligible request ran. If no target identity appears, examine whether observable requests could have reached it, what native branch could have skipped it, and whether loss intervals prevent a conclusion. Follow all tractable cross-record joins before concluding evidence is insufficient.

Do **not** infer the historical first winner or absence of target construction from the nineteen other-source chains. Preserve the B1 partial-coverage conclusion unless new **authenticated primary evidence** supports a more specific, narrower statement; changing the frozen B1 verdict requires separate authority, not this analysis.

## 4. Q2 — Admission pressure, burst chronology and causal diagnosis

Reconstruct the **observable** event rate, event-class distribution and writer progress with explicit denominators and uncertainty:

- Separate the startup, post-load/pre-travel, travel and arrival/STOP phases using actual authenticated receipts, QPC ticks, process identity and operator-reported checkpoints. Sequence numbers express admission order, not engine scheduler order. External checkpoint time precision must not be overstated.
- Chart admitted events by kind/site, source/owner where reliably known, thread, invocation, time bucket and, where supported, epoch. Distinguish provider volume from actual constructing misses and direct samples.
- Examine cumulative capacity-versus-retry loss counters, reported queue state/high-water marks if actually present, writer raw-write/flush/ACK progress, bounded drain behaviour and any terminal/status diagnostics. Derive occupancy or production rate only when the telemetry supports it.
- Test whether losses are concentrated in bursts or sustained. Specify what can be inferred from successive cumulative counters and what is unknowable between acknowledgements. A record-count difference is not necessarily a complete native event census.
- Identify whether hot-path cost, producer bursts, writer throughput, queue capacity, flush scheduling, or excessive nondecisive events are supported causes, ruled-out causes, or competing untested explanations. Do not label “queue full” as proof of why the queue failed to drain quickly enough.
- Compare measured retail accounting against the actual disposable D5X native stress controls, without treating fixture rates/latency as retail measures.

Where possible, use bounded **offline deterministic replays** of authenticated event timing and the actual transport algorithm to test hypotheses. Clearly label synthetic scheduling assumptions; never present them as measured native runtime arrivals. Do not use guessed timestamp precision or interpolate loss intervals as if all dropped records had known event types or source identities.

## 5. Q3 — Evidence-driven remediation and scientific safety

**Diagnosis precedes design.** Write a short decision record that explicitly compares:

- No code change, with improved interpretation/operational targeting.
- Recorder hot-path, admission, queue, drain or batching improvement supported by Q2.
- Bounded diagnostic enhancement to distinguish otherwise inseparable loss causes.
- Selective acquisition of target-relevant observations **only if** global prior-activity/lifecycle coverage and first-construction attribution remain independently sufficient.
- Any other narrower alternative supported by primary evidence.

If a proven tractable defect has a safe correction, implement and qualify it in the same assignment. Do not prescribe bigger queues, extra retries, throttling, disabled hooks or an architectural rewrite just to raise throughput. Preserve the original direct selection/decision/descriptor/sample contract, all fourteen hook identities unless a demonstrated reason changes them, and the D5X first-construction reader's conservative rules.

Selective filtering must be explicit and independently tested: global reset, visited/map activity, lifetime fences, unknown prior accesses, missing records and any other events capable of invalidating a first-winner claim must not silently disappear. A derived filtered stream cannot be represented as complete native evidence unless coverage is separately guaranteed. If reduced detail is scientifically safe only after a positively identified target, demonstrate how earlier events relevant to cold attribution are retained. Loss remains nonfatal to acquisition but conservative for joins. Never add an arbitrary session record/byte cap or block indefinitely inside a native hook.

If code changes are warranted:

- Give revised version/schema identities where semantics or binary identity change; never substitute new bytes under an old reviewed retail package pin.
- Build reproducibly, pin source/compiler/SDK/DLL/ZIP/reader artifacts and verify source-to-binary provenance.
- Exercise the **actual compiled native hooks, recorder and independent reader** in disposable Windows processes, not merely mock JSON or a standalone reducer.
- Reproduce the relevant B1 pressure pattern or a bounded justified approximation, including unpaced concurrency, sustained bursts, early and late losses, STOP during production, crash/worker/output failure, and recovery after losses.
- Test target selection with non-target traffic, target missed due to actual bypass/hit, multiple source pointers, same geographic key/different allocations, reset/ABA/retirement, missing selected/lookup/sample events, and incomplete source reads.
- Require that correctly witnessed claims survive intact intervals and invalid claims cannot be constructed by omission/filtering/reordering. Retain a cold-episode counterexample and wrong-DLL/host/site refusal.
- If the reporter/reader changes, rerun the original 39 B1 audit capture cases and material adversarial/damage controls proportionately, plus an independent reader differential against the authentic original B1 evidence.

A code change that improves throughput without retaining sound scientific coverage is a FAIL. Do not package an automatic retail deployment or declare B1/B2 GO after offline tests. If evidence is insufficient to choose a code change, a justified no-change or precise BLOCKED result is preferable to speculative modification, but an available discriminating offline test must not be deferred.

## 6. Mandatory visual diagnostics

Visualization is part of the scientific delivery, not decoration. Produce reproducible **SVG** figures with accompanying machine-readable data and provenance:

1. **Capture chronology:** admitted records by event category over actual QPC time, with startup/load/travel/arrival markers where supportable, and visible unknown-coverage regions.
2. **Recorder loss and writer progress:** cumulative admitted/dropped counts and independently supported flush/ACK or queue indicators. Explicitly distinguish cumulative counts from instant event rates; indicate intervals in which the timing or cause of individual drops is unknown.
3. **Target observation depth:** a flow/stage visualization of the target (and useful nearest/same-owner controls), showing positive witnessed stages, invalid/unknown paths, map hits/bypasses and where attribution fails. Zero target records must not appear as proof of zero executions.
4. **Optional geographic demand coverage:** if native request coordinates can be placed safely in a qualified spatial frame, map them against the target source footprint, verified outpost centre and 150-native-unit boundary. Use **absolute native coordinate labels**, not a source/outpost-relative frame masquerading as native. If frame joining is unqualified, omit the geographic overlay and document why; never invent the transform.

Labels must distinguish retail primary evidence, fixture results, derived estimates and unknowns. Prefer legible charts and explanatory captions. The independent review must inspect **rendered SVG output**, not just SVG validity or generation hashes. Raw proprietary data stays ignored/local-only; tracked graphics and aggregates must satisfy the repository's disclosure/provenance policy.

## 7. Execution procedure and evidence discipline

Near the start, create an **active investigation ledger** with Q1–Q3, hypotheses, checked data paths, counterexamples, failures, evidence locations and every material branch's next action/disposition. Update it during work, not just on closure. Recheck actual approved primary artifacts/hashes and preserve prior acceptance distinctions. Investigate errors and missing local evidence under the existing resource access process rather than switching to unverified copies. If a required archive or input is genuinely inaccessible after documented attempts, ESCALATE the exact access need; continue independent authorized work.

No historical source, save, raw receipt or audit verdict may be rewritten. New forensic derivatives must name their input hashes, transformations and scope. Minimize persistent scratch while retaining decisive failed controls, counterexamples and reproducibility receipts. Follow exact-source permission rules for third-party materials; maintain publication eligibility separate from scientific acceptance.

## 8. Frozen acceptance criteria

| ID | Mandatory result |
|---|---|
| **D5Y-AC1 — Authority and provenance** | Current repo/installed/native/D5X/D5X-B1 source and evidence identities verified; raw inputs and protected files unchanged; no live, Vortex, save/config, staging/commit/push or publication action. |
| **D5Y-AC2 — Controlling questions and ledger** | Q1–Q3 frozen, linked to the open D5R parent and the accepted B1 partial trial; active, independently reviewable ledger traces material avenues and failed/negative work. |
| **D5Y-AC3 — Complete retained-evidence target forensics** | Examine *all relevant authenticated B1 event categories*, not just full paths, with precise target identity, deepest-stage and explicit attribution/loss uncertainty. |
| **D5Y-AC4 — Geographic/source controls** | Compare recorded owner/source/query identities with qualified Feynman V target geography and known source keys; preserve descriptor, pointer, epoch and native-frame distinctions. |
| **D5Y-AC5 — Recorder-pressure characterization** | Evidence-backed event/time/producer/writer/loss analysis, testing plausible bottlenecks and exposing missing telemetry rather than assuming a cause from drop counts. |
| **D5Y-AC6 — Remedy decision and conditional implementation** | Pre-code decision compares no-change and focused alternatives; warranted defects repaired/qualified within scope, speculative changes rejected with evidence; scoped NO-GO/BLOCKED permitted with proof. |
| **D5Y-AC7 — Scientific integrity and regression** | Any altered observer/transport/reader/filter retains conservative first-winner qualification, global invalidation/loss semantics, wrong-context refusals and honest weaker outcomes; actual compiled native testing and relevant old-capture regressions pass. If unchanged, demonstrate why this testing requirement is inapplicable. |
| **D5Y-AC8 — Visual diagnostics** | Reproducible SVG chronology, loss/writer and target-stage figures, machine-readable backing data, correct labels and rendered independent visual QA; optional geography only with validated native coordinate join. |
| **D5Y-AC9 — Reproducibility and delivery** | Complete report, source/claim ledger, technical decision record, reproducible scripts/receipts, exact source/package hashes if changed, full inclusion/exclusion inventory and verified complete/task-only patches. |
| **D5Y-AC10 — Independent completeness and technical review** | Independent scientific/completeness reviewer challenges unresolved material avenues and first-target attribution; independent engineering/evidence reviewer checks code, performance and preservation; independent editorial reviewer checks every changed prose/figure. REWORK/ESCALATE enforce controlling questions, not just tidy documentation. |
| **D5Y-AC11 — Final authority and future gating** | Explicit question-level COMPLETE/INCOMPLETE/BLOCKED, engineering/retail NO-GO or eligible-for-separate-review, exact limits and next discriminating action; no automatic B1 retry, B2, install, launch or publication. |

## 9. Completion and escalation

**COMPLETE** for Q1 requires the deepest defensible attribution determination from all accessible B1 evidence, including an evidence-backed characterization of any remaining ambiguity; it does **not** require inventing the target's unobserved history. For Q2, it requires a supported bottleneck/contributing-factor conclusion *or* a demonstrated insufficiency of existing telemetry after testing all material offline alternatives. For Q3, it requires a supported decision and qualified implementation where genuinely warranted; arbitrary modifications are not mandatory. Where an indispensable determination remains unavailable and an authorized route still exists, status is **INCOMPLETE / REWORK**. A genuine indispensable unavailable input/authority/capability is **BLOCKED / ESCALATE**, supported by exact proof and minimum resume request. Preserve distinctions between a completed bounded forensic question and the parent D5R scientific question.

No reviewer may accept a polished report if a high-value offline discriminator has not been attempted. Independent reviewers must identify the highest-value omitted avenue or demonstrate that none remains necessary for the specified scoped conclusions. They must inspect actual source evidence and negative cases rather than only the implementer's chosen summaries. Reviewer ACCEPT is not maintainer authorization to integrate or run.

## 10. Deliverables and handoff

Follow current repository naming conventions (adjust filenames only where necessary and document the choice):

- `docs/experiments/resource-retained-population/d5y-report.md` — answers to Q1–Q3, observed/unknown boundaries, performance diagnosis, decision, scientific and engineering limits.
- `docs/experiments/resource-retained-population/d5y-investigation-ledger.md` — material work/branch checkpoints and dispositions.
- `docs/experiments/resource-retained-population/d5y-sources.csv` — auditable provenance, primary receipts and native/context references.
- `docs/experiments/resource-retained-population/d5y-review.md` — frozen criteria, independent completeness/engineering/editorial dispositions, exact accepted snapshot.
- `docs/experiments/resource-retained-population/d5y/` — readable SVGs and documented aggregate/structured data backing each visualization.
- Task-owned code/fixtures and, **only if repaired**, a fully pinned revised observer/reader/source package and proposed—not authorized—retail readiness follow-up.
- Exact-hash final delivery manifest; **complete and task-only diffs**, clean HEAD/index proof, changed-file and excluded-private-artifact inventories. A prior uncommitted file must appear in complete coverage, not be silently absorbed into task-only changes. Never stage to manufacture a diff.

Suggested integration message may be proposed by Codex after review; this brief grants no integration authority.

**No D5Y result authorizes another retail session.**
