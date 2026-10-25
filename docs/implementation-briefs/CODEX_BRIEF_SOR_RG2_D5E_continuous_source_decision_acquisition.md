# Codex implementation brief — RG2-D5E

## Continuous Source-Decision Acquisition: Phase A implementation and qualification

**Project:** `D:\Projects\starfield-outpost-research\`  
**Repository:** `starfield-outpost-research`  
**Authority:** Phase A only: offline native analysis, implementation, and disposable synthetic Windows qualification. **No Starfield launch, attachment, gameplay, save modification, forced source regeneration, staging, commit, push, or publication.** Phase B requires a separately reviewed run card and explicit user GO.  
**Status:** Implementation brief; acceptance criteria AC1–AC8 are frozen.

## 1. Purpose and inherited findings

RG2-D5C established process-local retention and reuse of resource populations in a ProcGen-manager map keyed by runtime **source pointer**, with a separate visited-source guard, lookup hit/miss, construction-on-miss and teardown/reset paths. RG2-D5D traced ordinary coordinate/cell preparation capable of demanding generation before Workshop consumption and audited historical captures: C1G, D4A and D4D witnessed construction, but **none established an explicit source-map hit**. D5B observed three accepted native regions at the second Feynman V outpost exactly matching the **frozen mask-3** geometry alternative; it did **not** capture that source's construction query, effective mask or generation epoch. Its mode switching introduced observation gaps. Eager population of distant sources at Save52 load is **not** established and must not be assumed.

**Scientific question:** During a qualified observation window, what provider decisions occur for the selected source—visited-source bypass, retained-map hit, or retained-map miss—and, on a qualified miss, what actual original construction query and effective mask are used?

**Primary geographic source:** `0:37536:20928:0029d20e`, at the **active second Feynman V** outpost (not the original Feynman V control). Frozen competing ordinary masks: `0` and `3`. Feynman VI-b is a separately authorized fallback; Feynman VIII-b historical deposit mutation is outside scope.

Read the *current* repository files before editing: `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md` if present, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, and the D5B/C/D reports, reviews, run cards and relevant `research/` collector code. Follow actual repo conventions and resolve path/name discrepancies from source rather than inventing parallel architecture. Record the pinned game/build and native address domain precisely. Previously identified `0x14079f860` (provider), approximate `0x14079fcd0` (map-decision neighborhood), coordinate preparation `0x140aed020`, and consumer `0x1421e07d0` are **investigation leads, not automatically qualified breakpoint boundaries**. Independently validate each actual instruction site, registers and lifetime assumptions against pinned native exports.

## 2. Scope and precedence

### A. Native observation contract

Trace and document, at instruction/branch and operand level:

- Provider entry and source-pointer/manager identity, with a separate stable geographic identity association (never equate a pointer with a lifetime).
- Visited-source guard identity (including the D5C source `+0x68` identity distinction), decision and bypass branch.
- Retained source-map lookup, **hit vs miss** and wrapper identity; no inference of a hit solely from an absent construction event.
- On a miss, the **original** construction query coordinates and native effective ordinary mask, including where/how the mask is sampled; later cell-query coordinates are not substitutes.
- Construction outcome and insertion/retained-wrapper evidence where achievable *without compromising continuous decision coverage*.
- Manager resets, source replacement and pointer recycling sufficiently to avoid merging lifetimes.
- Any concurrency/lock semantics that determine whether observations can be assigned to a single invocation.

Document evidence fields, access paths, breakpoints, reads, validation predicates, instrumentation assumptions and reasons an event is rejected. Clearly distinguish an original query operand, a sampled mask and a mask inferred retrospectively from geometry.

### B. Implement continuous decision acquisition

Extend the **existing** debugger controller/receipt/transport design rather than create an unrelated observer. Treat the four hardware-breakpoint slots as a hard constraint unless the repository's qualified architecture supports a different justified method. Prioritize uninterrupted source-provider/decision coverage even while unrelated source requests execute. Read other operands synchronously from stopped-thread register/stack/validated memory where safe. Selective downstream breakpoints are permissible only with explicit coverage accounting; the primary boundary must not silently disappear on unrelated calls. Preserve all source-qualified decisions in encounter order, including contradictory queries/masks, repeated hits, bypasses, resets, and overlapping thread events.

Provide a durable machine-readable event schema containing acquisition/session identity, manager/source lifetime, source geographic association and validation status, thread/invocation correlations, source-decision type, native operands, observation time/order, coverage intervals, native-read completeness and rejection reason. Capture raw supporting values; reduce conservatively. No promotion of mere common pointer, timestamp, geographic key or resource names to proved generation ancestry.

Do not silently change the existing D5B consumer acquisition semantics. Geometry capture is optional/secondary for this assignment; **do not trade decision coverage for repeated geometry controls**.

### C. Offline scientific reducer and comparator

Implement or extend a reproducible offline classifier with explicit statuses:

- **A — Qualified miss with original query, effective mask, and construction/insertion evidence** (best outcome).
- **B — Qualified map hit or visited bypass**, with source and manager lifetime; distinctly label the two branches.
- **C — Qualified decision, incomplete necessary operand**, with named missing field.
- **D — Consumer-only / no qualified provider decision**, not a resolution of the primary question.

Report **first observed** decision separately from **first-ever** construction/decision; the latter requires actual lifetime and continuous-coverage proof. Compare directly observed masks to the frozen `0`/`3` alternatives, without fitting them to D5B native geometry. Do not reclassify any of the seven remaining indeterminate Save52 associations based on conjecture. A cache-only or visited-bypass outcome is valid evidence of that *observed decision*, not proof of when the population originally arose. Never infer eager save-load caching from no-hit observations.

### D. Synthetic Windows qualification

Qualify real debugger/instrumentation behaviour against **disposable Windows processes**, not solely mock parsers. Include, at minimum:

1. Target source: miss with query/mask `0`, successful construction/insertion, then repeated hit and visited bypass.
2. Separate lifetime/source reuse with query/mask `3`, preserving both outcomes without conflation.
3. Unrelated sources and heavy interleaving while selected-source decision coverage stays armed.
4. Concurrent threads, nested invocations and lock-contention ordering.
5. Visited bypass that does not imply a complete population; hit that does not imply historical construction epoch.
6. Source-pointer reuse, manager reset/replacement and stale-memory rejection.
7. Incomplete/invalid native reads, partial/failed insertions, misleading identifiers and transport corruption.
8. Breakpoint-slot pressure, arming/phase transition, lost/uncovered intervals, durable acknowledgements, stop after successful capture and interrupted/failed teardown.
9. Multiple source requests in one lifetime where only the first constructs and later requests hit/bypass.
10. Successful continuous observation across an **explicit pre-load arm barrier** and an unrelated busy interval, proving no silent suspension of the decision site.

For each case store reproducible configuration, expected and observed event/coverage results, logs/receipts and pass/fail. Explicitly report if a continuous guarantee cannot be attained rather than manufacturing a passing test.

## 3. Proposed Phase B run card — design only

Prepare a complete **NOT AUTHORIZED** single-session run card targeting the second Feynman V source in pinned Starfield `1.16.244.0`, via a fresh process, main-menu attach and a verified fully armed barrier **before** the operator loads hash-verified Save52. Observe during load and ordinary travel/arrival, optionally Build Mode if scientifically needed. This is a coverage measure, **not** a presumption of eager save-load population. Include operator actions and milestone timestamps, source/workshop identity confirmation, save-protection/preflight/postflight, rollback/abort, storage capacity, durable receipts, controlled stopping, exact scientific success levels, no-hit meaning, coverage gaps, and how the instrument remains armed despite unrelated activity.

Do not automatically quit on an initial qualified map hit or visited bypass if further normal requests might occur during the **already approved bounded session**; preserve every qualified decision and a predetermined end boundary. No forced regeneration, save edits, unapproved retries, silent alternative-source switch or experimental source perturbation. Feynman VI-b requires an independent explicit GO. Any proposal needing more risky or intrusive execution should be a separate alternative, not hidden in the default run card.

Distinguish observation after a fresh process starts, observation after the pre-load arm barrier, and inference about the source's original historical epoch. Do not claim that observing a miss during Save52 loading proves routine distant-source eager construction without qualified actor/call-path context.

## 4. Preservation, regression and boundaries

- Preserve protected saves, historical evidence, installed ESM/executables, pinned native exports, analysis projects and ignored local-only evidence. No mutations of native inputs.
- Preserve frozen RG2-D2 through D5D scientific outcomes, D5A mask alternatives, D5B geometry matches, the ten exact native geometry controls and the original source/corpus data. If the predictor is unchanged, integrity verification of geometry controls may be used instead of a rerun, but state **exactly** which was performed.
- Raw retail/proprietary data, process dumps, protected saves and personally identifying local paths remain uncommitted in the designated ignored local-work area. Track only publication-safe authored method, reduced evidence and reproducible helper code.
- Record any limitation that materially affects the next live study as an explicit blocker or caveat, with an actionable remedy; no unbounded investigation outside the selected source-decision contract.
- **B6 publication/release verification remains on hold.** No Outpost Tracker integration or Feynman VIII-b bug-reproduction work.

## 5. Frozen acceptance criteria

**AC1 — Authority and preservation.** Phase A-only execution respected; pinned inputs and protected evidence unchanged; no retail launch/attach, staging, commit, push or publication.

**AC2 — Native decision contract.** Evidence-backed, instruction-level identities for visited guard, map hit/miss, source/manager lifetime and supported query/mask operands, with explicit limitations and no fabricated native semantics.

**AC3 — Continuous coverage.** Implemented instrument plus Windows synthetic evidence demonstrates durable observation of selected-source decisions through unrelated calls, with explicit, tested coverage-gap detection and pre-load arming barrier.

**AC4 — Construction operands.** On supported qualified miss, obtain actual initial query and sampled mask (and insertion outcome where feasible), or classify the precise technical blocker without substituting inferred mask-3 geometry.

**AC5 — Scientific classifications.** Accurate and independently testable visited vs hit vs miss decisions, manager/source lifetimes, first-observed vs first-ever and evidence tiers A–D; preserve contradictory observations.

**AC6 — Live-readiness package.** One bounded, operator-usable, explicitly **NOT AUTHORIZED** Feynman V Phase B card with pre-load barrier, no-hit/coverage interpretation and save safeguards; VI-b remains separate-approval fallback.

**AC7 — Durable verification and editorial quality.** Reproducible Windows synthetic matrix, checked preservation/regression scope, compact evidence/provenance reports, clear uncertainty treatment, finished editorial pass, and complete/task-only patch manifests and cryptographic hashes.

**AC8 — Independent review.** Independent scientific, engineering and editorial assessment of the **actual final substantive snapshot**, frozen AC1–AC8 matrix, resolved issues, completion-record finalization and separately checked final narrow deltas if any. Reviewer must inspect underlying decisive evidence and synthetic qualification, not merely accept executor claims.

## 6. Required deliverables and completion contract

Follow the repository's canonical locations and templates. At minimum produce:

- Working existing-framework observer changes, transport/reducer/comparator and disposable synthetic targets/tests.
- Native source-decision contract, event schema and explicit continuous-coverage specification.
- Research report and evidence/proposition matrix relating D5C/D5D to new instrument capability.
- Full test/qualification record with actual results and honest caveats.
- Proposed Phase B run card marked **NOT AUTHORIZED**.
- Independent scientific/engineering/editorial review and AC1–AC8 disposition, including correction loop and final-snapshot closure.
- Preservation and regression inventory with precise distinction between executed tests and integrity-only checks.
- Verified **complete** working-tree diff and **task-only** diff, byte-precise inclusion/exclusion manifests, SHA-256 digests, forward/reverse reconstruction checks, branch/HEAD/index state and suggested commit message. Account for any supplied brief as pre-existing if applicable. Do not stage, commit or push.

For each unresolved assertion, report its **specific missing operand/event** and the smallest safe discriminator; do not silently close it by choosing the mask that fits D5B. Final summary should state whether Phase A is **ACCEPT**, **REWORK**, or **ESCALATE**, supported by the independent reviewer and actual evidence.

**Suggested commit message (only if accepted after external review):** `feat(research): qualify continuous source-decision acquisition`
