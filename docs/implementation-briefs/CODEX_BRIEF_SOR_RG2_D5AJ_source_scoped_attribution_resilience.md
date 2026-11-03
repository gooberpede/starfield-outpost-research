# Codex implementation / research brief — RG2-D5AJ

**Title:** Source-Scoped Attribution, Episode A0 Evidence Recovery, and Experimental Resilience  
**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Issued:** 2026-11-03 (Australia/Sydney)  
**Task type:** Offline native research, bounded evidence reanalysis, corrective reader/reducer/controller engineering, adverse qualification, operational-design review.  
**Parent:** D5AI (offline instrument) and the separately authorized but incomplete Episode A. D5R and GC-25/30/31/10 remain OPEN.  
**Authorization:** This brief authorizes **offline work only**; it does **not** authorize Starfield launch, Vortex deployment, SFSE attachment, any new gameplay episode, protected-save modification, publication, staging, commit or push.

## 1. The problem to solve

Episode A reached Feynman V Cu IL F and collected **one structurally complete A0 geometry snapshot**, but the source-bound checkpoint refused attribution. The approved run card required a qualified A0 before departure, so the maintainer stopped. No departure, A1, independent repeat, or Episode B occurred. The game displayed no reported unusual behaviour. **The refusal is a limitation of the scientific interpretation machinery unless further evidence demonstrates an actual game-state anomaly; it is not an observed engine defect or an operational hazard.**

Frozen observed basis (do not alter or reinterpret these as already-qualified target evidence):

- Core: **32,155** durable records; lifetime: **5,968** durable records; zero reported core/lifetime losses or output faults; postflight and archived raw evidence reported PASS.
- A0 structural map: **36 holders, 102 resource slots, 2,984 regions, 7,372 points**. Complete capture structure is not equivalent to correct source attribution.
- Source birth diagnostic **2082**, publication **2083**, lookup **7479**, descriptor **7480**, generation **7481**, return **7497**, with reported allocation 932 and epoch 215; target association remains diagnostic, not qualified.
- A0 snapshot epoch **233**. Nine **Grid-clear begin/end pairs**, covering core sequence **31904–32155**, account for 18 observer epoch increments after the relevant births; their `proc` values differ from the A0 snapshot `proc`.
- Existing `d5ai_reduce.py::source_identity` rejects birth/snapshot epoch mismatch and any intervening `kind 10/11` fence, without an owner-scoped assessment. `envelope` refuses the complete candidate if *any* occupied holder remains unidentified. The frozen checkpoint returned `Unidentified occupied holders prevent unique geographical selection or absence`.
- **No broad claim:** Different ProcGen identities on recorded Grid clears suggest an overbroad refusal, **not** proof that those clears are harmless. An observer epoch is an uncertainty fence, not by itself a source lifetime or a ProcGen cold-reset boundary (D5AC).

The original Episode A report, refusal, raw capture, receipts, frozen D5AI predictions and historical statuses are immutable. A new version of the analysis may derive a qualified A0 from these bytes **only if** independently supported by native ownership and lifecycle evidence. Recovering A0 must not be assumed possible or manufactured by loosening tests. Even if it is recovered, no A1 exists and Episode A's principal departure/return comparison remains incomplete.

## 2. Frozen controlling questions and success conditions

**D5AJ-Q1 — Actual source-scoped invalidation.** Which native Grid-clear, source retirement, map-erase, owner replacement, broad reset and destruction operations can invalidate a given geographic source allocation or population, under which exact owners/locks/aliases? Identify whether the nine actual other-ProcGen clears could affect the A0 target, other holders, owner context, or the consumer's map. A complete answer requires a proven relationship, not simply `proc != snapshot.proc` or `epoch changed`.

**D5AJ-Q2 — A0 evidentiary recoverability.** Does the immutable Episode A capture supply a complete, loss-free, causally joined and geographically unique target A0? Evaluate all 36 occupied holders and the target's birth/publication/generation chain, frame, owner, lifetime and mutation/ending coverage. If target attribution is not recoverable, identify the **specific missing edge/field**, not merely the pre-existing blanket refusal. Distinguish **structural completeness**, **identified target**, **unidentified non-targets**, and **negative/unavailable target conclusions**.

**D5AJ-Q3 — Correct source/owner-scoped qualification.** If native evidence justifies relaxing the global epoch/fence checks, implement a **versioned** source-aware reducer/checkpoint qualification that accepts valid continuity and refuses unsafe associations. Preserve owner/ProcGen source identity, allocation and pointer reuse, affected Grid and map ownership, generation and content-holder lifetime, reset and invalidation, uncertainty from lost/missing events, and frame/consumer context. Do not silently weaken the original reducer. If no safe positive rule can be demonstrated, deliver a controlled negative with the exact counterexample and keep the historical refusal.

**D5AJ-Q4 — Proportionate experimental gates.** Which future Episode A admission, continuation and STOP conditions genuinely protect game/user data, capture integrity or indispensable evidence, and which are merely nonfatal scientific uncertainty? For each existing gate classify an observed or hypothetical failure as **SAFETY**, **INTEGRITY**, **SCIENTIFIC PREREQUISITE**, or **RECOVERABLE SCIENTIFIC UNCERTAINTY**. Recommend the least restrictive scientifically meaningful behaviour consistent with explicit finite operator actions and protective requirements; do not override an already approved historical card retrospectively.

**Overarching outcome:** Establish whether a corrected, independently demonstrated method can qualify the retained A0 and a future departure/return experiment without treating ordinary unrelated lifecycle changes as catastrophic. The task may reach COMPLETE with a well-evidenced negative A0 result **only if** Q1–Q4 and the agreed scoped corrective/qualification obligations are actually resolved; a mere report of absent information while viable in-scope paths remain is INCOMPLETE/REWORK. Historical Episode A scientific completion is **not** a possible deliverable from this task.

## 3. Method, required investigations and evidence

### A. Establish immutable inputs before analysis

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/reviewers/research-completion-reviewer.md`, the original D5AI brief/accepted correction, Episode A run card/report/review, D5AC, D5AH, D5AI ownership/lifetime design and the current reducer/checkpoint code **before substantive execution**. This requirement is about complete, correct governing context. Record a concise compliance receipt; if the exact mandated reading sequence in the current project governance adds no demonstrated integrity value, **do not silently waive it**—flag the policy issue separately for maintainer consideration. The user has agreed the value of that sequencing rule deserves review outside the scientific task.

Pin repo HEAD/index, exact original scripts and executable/site versions, protected Save52 and package identifiers, the raw Episode A archive/session roots and their retention policy. Hash the original evidence; write only fresh ignored task-local analysis outputs. Preserve the frozen A0 failure and the prediction register unmodified. Verify task-local disk/protection requirements including the existing 40,000,000,000-byte caller-available floors on both C: and D: where applicable. Never delete or rewrite original recordings, protected saves/backups, databases or sealed archives.

### B. Prove invalidation scope instead of trusting a global epoch

Start from the nine recorded fence pairs: exact kind, `proc`, allocation/owner if available, entry/exit, thread/QPC/ordering, and relation to source birth, map-generation history, owner-install/reset fences and consumer snapshot. Reconcile all other relevant fences and source events; account for the **complete** captured interval, including adverse or unidentified histories.

Trace native destructor/clear/erase and owner-management paths on the pinned build (1.16.244.0) to establish which objects each fence actually owns and frees. Demonstrate conditions under which two `proc` identities might nevertheless share an affected Grid/source, a manager context or a stale/reused pointer. Follow material aliases, lookups and synchronization across necessary subsystem boundaries. Use **verified disposable read-only Ghidra project copies**; do not open the original project if its housekeeping may mutate it. Retain static proofs, controlled native execution and B2/D5AC counterexamples separately from observed Episode A events.

Do not make the exact source attribution predicate depend on global equality unless a native proof requires it. Conversely, an unrelated `proc` value does not automatically permit acceptance: check owner lifetime, source allocation continuity, context replacement, lifetime journal begin/end coverage, loss history and every relevant invalidator. Treat a native writer/fence that cannot be reliably attributed as uncertainty, not as proof of harmlessness.

### C. Resolve unknown holders and positive target uniqueness

Audit the exact `source_identity`, `owner_context`, `generation`, `envelope`, prefix-checkpoint and lifetime-journal contracts. Assess whether all 36 holders really require positive geographical identification to establish **positive target uniqueness**, or whether a safe narrower proof can exclude unidentified holders from being alternate instances of the target. Negative claims (target absence/unavailability) may require a stronger census than positive presence; prove the distinction under actual map/identity structure, not by assuming unknown holders are unrelated.

Explicitly test:

- Same source pointer after free/reallocation (ABA); same token for different geographies; same geography in different ProcGen owners; duplicate publication; unpublished or pre-arming source.
- Retire/free/owner replacement genuinely affecting the target versus nine unrelated Grid clears, including overlapping or nested fences and ambiguous callback order.
- Missed/lost invalidation, lifetime journal cutoff, contradictory or missing owner event, crossed reset, unknown Grid→ProcGen association and context change during snapshot.
- Multiple occupied holders with one positively identified target plus unknowns; two genuine target-key holders; absent target with unknowns; partial/empty/mutated content.
- Exact independently verified source/frame/consumer query, geometry byte identity, generation output holder, and source-specific evidence coverage.

A positive target claim requires an independently defensible uniqueness and lifetime proof. **Do not** accept it merely by dropping the `if unknown:` refusal. An absence claim may remain INCONCLUSIVE even if one positive target can now be identified. Keep every rejected counterexample visible.

### D. Versioned correction and prospective operational design

If Q1–Q3 support a correction, create a new versioned reducer/checkpoint method (or an explicitly versioned evidence qualification mode) with an unchanged historical-interpretation path. Re-run the **original frozen** method to reproduce its refusal first. On the immutable A0 data, produce both results side-by-side, with exact method/source hashes, each changed predicate, reasons and evidence references. Do not mutate original data or silently change historical D5AI statuses.

Maintain fail-closed behavior for actual source invalidation, unknown relevant lifetime/fence origin, broken content ownership, capture loss/corruption and incorrect consumer identity. Changes to producer hooks/geometry schema should be avoided unless a demonstrated indispensable need emerges: this brief permits **offline reader/reducer/controller and testing corrections**, not production native instrumentation changes or deployment. If a production hook change is indispensable, document the precise missing witness and escalate that authorization; continue independent offline research.

Audit prospective Episode A gates, including `BASELINE_PREFIX_QUALIFIED`, `GEOMETRY_ARMED`, controller and dual-recorder health, protected-file/disk checks, snapshot quality, target attribution and departure prerequisites. For each gate record its actual purpose, which observations are still valuable if it fails, and whether the approved finite itinerary can continue without compromising a necessary comparison. Preserve the operator's exclusive STOP/exit ownership. **A scientific qualification failure is not a machine safety failure.** A prerequisite can justify not departing if no interpretable A0/A1 comparison is possible, but other safely acquirable data should not be discarded by blanket retirement rules. Never impose arbitrary elapsed-time, evidence-volume, check-cadence or recording-count cutoffs on healthy acquisition.

Deliver proposed run-card/control changes for review **only**, not an authorization to execute them. If the existing cards require material amendments, submit exact diffs, fresh offline tests and independent review. Existing Episode A and Episode B authorizations remain unchanged: B has never been authorized; Episode A's consumed scope cannot be reused as a retry. Preserve `D5AI-PRED-01` frozen unchanged and NOT TESTED.

## 4. Required deliverables

Under `docs/experiments/resource-retained-population/`:

1. `d5aj-report.md` — answers to the original Q1–Q4, direct/plain-language conclusion, limitations, integrity and permission accounting.
2. `d5aj-invalidation-matrix.md` — exact native owner/source/holder/consumer relationships, B2/D5AC and A0 witnesses, every nine-Grid-clear classification and counterexamples.
3. `d5aj-a0-recovery.md` — original refusal versus qualified new analysis, all 36 holder dispositions, target-key uniqueness, complete geometry status, missing evidence and method versions; **never invent A1**.
4. `d5aj-gate-audit.md` — each safety/integrity/scientific gate, demonstrated need, response, preserved evidence, optional prospective run-card changes.
5. `d5aj-investigation-ledger.md` — active question/dependency/hypothesis tracking with exact native/source/capture pointers, unresolved viable branches and continuation results.
6. `d5aj-review.md` — independent scientific, engineering, editorial and permission decisions, original criterion matrix, exact final snapshot and full diff coverage.
7. Source-bound tests/analytical scripts and applicable versioned reducer/checkpoint changes, with reproducible local receipts. Keep raw proprietary data, saves, native code exports, binaries and private session evidence **LOCAL-ONLY**.
8. Update `resource-generation-gameplay-checklist.md` and its justification references where actual outcomes justify a change. Stable IDs and original meanings preserved; GC-25/30/31/10 and D5R must not be marked resolved by recovered A0 alone. Add a newly discovered material gap if appropriate. Keep extractor continuity and physical resource overlap outside this assignment.
9. Verified `<task>-complete.diff` and `<task>-task-only.diff`, tracked/untracked inclusion/exclusion manifest, preservation/identity checks and precise handoff. Do not stage, commit, push or publish.

## 5. Mandatory acceptance criteria (frozen)

**D5AJ-AC01 — Authority, baseline and preservation.** Complete required source/protocol reading before substantive work; pin original Episode A evidence, unchanged frozen failure and forecast, exact repo/source/native identities and permissions. No game/deployment/saves/DB mutation. Record any deviation honestly; it does not automatically invalidate scientifically sound evidence but remains a procedural failure.

**D5AJ-AC02 — Native source-specific invalidation.** Evidence-backed ownership/writer/clear/reset/retirement model demonstrating which of the nine recorded other-ProcGen Grid-clear pairs can or cannot invalidate the relevant A0 sources, under actual conditions. Include direct contrary schedules, alternative owners, pointer reuse and uncertainty.

**D5AJ-AC03 — Complete A0 attribution audit.** Independently authenticated immutable A0 inputs, exact event census and complete 36-holder decision accounting; positive target uniqueness/absence standards explicit and separate. Return a supported positive or exact negative/inconclusive source result, not simply an epoch-mismatch restatement.

**D5AJ-AC04 — Versioned implementation and qualifications.** When native evidence justifies change, implement the minimal source-scoped reader/reducer/checkpoint correction with complete positive/adverse native or owned-oracle tests, exact final-source regression and unchanged historical reducer reproduction. If a proven correction is impossible within authority, return precise indispensable evidence/permission, not a fabricated PASS.

**D5AJ-AC05 — Honest prospective resilience.** Complete gate classification and minimal prospective amendments, preserving true safety, protected saves, identity/guards, both drive floors, STOP, output/transport integrity and source-specific scientific prerequisites while removing unjustified global scientific hard-stops. Never mislabel scientific non-qualification as operational failure.

**D5AJ-AC06 — Evidence sufficiency and reproducibility.** Controls for all material ABA, source collision, unrelated/relevant fence, unknown-holder, owner-reset, journal-loss and content-mutation counterexamples. Independently repeat deterministic derivations; preserve failures and distinguish actual engine execution from synthetic controls. Zero original-capture edits.

**D5AJ-AC07 — Checklist, anomaly and original-contract fidelity.** Update justified checklist evidence and anomaly findings; retain GC/D5R and frozen prediction statuses, original episode failure and no-departure facts. Do not demote mandatory dependencies to optional or claim retail stability from one A0 capture.

**D5AJ-AC08 — Independent review and exact delivery.** Optional bounded specialist, no more than two concurrently active sub-agents; independent non-implementing reviewer challenges original frozen Q1–Q4 and every criterion, adverse proofs, remaining viable avenues and safety gates. Apply editorial standard, verify current final-source and all untracked text, complete/task-only patches and preservation receipts. Independent ACCEPT/REWORK/ESCALATE with criterion-specific reasons.

## 6. Outcome/continuation rules

- **COMPLETE / ACCEPT:** Every mandatory D5AJ Q and criterion met at its original scope; if actual A0 remains unqualified, that negative result has a concrete proof of its indispensable missing inputs and a complete successful corrective-design answer. Do **not** call A0 recovered if it is not.
- **INCOMPLETE / REWORK:** Any tractable native ownership, identity, unknown-holder, reducer, qualification or gate dependency remains unexamined or a mandatory test fails. Diagnose, correct and retest **within D5AJ**, rather than handing off a routine defect.
- **BLOCKED / ESCALATE:** Only on a specific demonstrated terminal missing primary event, essential unapproved action or resource/authority barrier; give prior attempts, why available alternatives fail, smallest permission or input, and a durable resume point. An analysis method's limit does not automatically close the parent problem.
- A scientifically unexpected or false prediction is a research result, not an engineering failure. This task **does not test PRED-01** and must not revise it.
- If a cybersecurity guardrail interrupts a particular operation, record actual circumstances and respect enforcement; do not invent causal claims or pre-emptively shrink legitimate authorized research. Continue independent permitted work where possible; no circumvention.
- **No additional live attempt** or production DLL deployment is granted. The owner decides separately on any new A episode, modified run card, or future B episode.

## 7. Final maintainer-facing answer requirement

Summarize in plain language, separately: **(a)** what the nine Grid clears actually did to the captured source(s) on available evidence, **(b)** whether the old A0 can now be attributed, and under exactly which versioned proof, **(c)** whether subsequent ordinary observations could safely continue in a future equivalent situation, and **(d)** which actual observations remain necessary for GC-30/31. State the material uncertainty without treating routine gameplay housekeeping as an engine defect.
