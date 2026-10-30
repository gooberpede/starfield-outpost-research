# RG2-D5S — Construction-Query Winner Determinism: Completion-Contract Investigation

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Continue the D5R scientific question through its necessary upstream scheduling, streaming and source-lifetime dependencies. **Offline/read-only research**, with narrowly triggered read-only save investigation where justified.  
**Parent question:** D5R — can the resource population for a specified outpost location be determined from location, game data and reproducibly derived state? **OPEN**. D5R is a historical accepted milestone, **not** closure of that question.  
**Status:** Proposed Codex research brief. Freeze D5S-Q1–Q3 and D5S-AC1–AC10 before execution; no silent amendments.  
**D5P retail/plugin:** **NO-GO**, unchanged. **B6/publication:** **ON HOLD**.

## 1. Controlling questions and required terminal outcome

The following are the controlling questions, not optional directions for a bounded reconnaissance. Treat their intended generality as frozen.

- **D5S-Q1 — Query-winner determinism.** For the **second Feynman V source**, analytical identity `0:37536:20928:0029d20e`, under a clearly specified normal arrival/initialization scenario and pinned game/data baseline, determine **which original Int2 query first reaches the source's effective constructing source-map miss**, or establish a supported rule/set of possible winners and whether actual execution can vary. Trace the necessary initial-state, gameplay/location, focus/streaming, work registration, dependency, dispatch, cancellation and synchronization inputs. No invented ordering guarantees.
- **D5S-Q2 — Reproducible generation inputs and outcomes.** Determine whether the winning query, or proven equivalence among admissible winners, is sufficient to reproduce the ordinary resource-generation inputs from location and static game data; identify each indispensable additional input. Evaluate whether the differing D5R mask/weight alternatives **materially change surviving geometry** where this is necessary to discriminate the central determinism claim. Separate candidate-coordinate determinism, actual winner determinism, query-specific mask/weights, and final-geometry invariance. Do not claim full resource-population determinism on weight evidence alone.
- **D5S-Q3 — Within-invocation source safety.** Establish the minimum source ownership/synchronization guarantee across cell selection and the active provider/generator invocation, including landscape shift/retirement, and state exactly what is proven versus unresolved. No requirement to correlate later cache hits or reconstruct historical cache objects.

**Permitted terminal disposition:** `COMPLETE` only if Q1–Q3 receive evidence-backed answers at the claimed scope (including a valid controlled negative result, such as proven nondeterminism, where supported). `BLOCKED` requires the protocol's terminal-barrier proof and a **specific minimal authorization/input/capability request**; it maps to `ESCALATE`, not scientific completion. `INCOMPLETE` while authorized, material investigative avenues remain means `REWORK` and continued work on **this assignment**, not a polished final ACCEPT. An independently accepted *subfinding* does not close the parent questions. Do not switch to the weaker task of merely enumerating candidate orders without maintainer authorization.

**Important qualification:** Do not assume a unique winner exists or that ordinary retail results are perfectly invariant. A rigorously bounded demonstration of genuinely variable outcomes is a legitimate scientific answer. Likewise, a truly unavoidable opaque/external scheduling input may justify `BLOCKED` if the evidentiary burden is met. No universal impossibility proof is required for a properly controlled scoped falsification.

## 2. Baseline, prior findings and research authority

Before substantive work read current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/RESEARCH_STATE.md`, and the existing D5D/D5H/D5I/D5Q/D5R native records, matrices, report, sources and counterexamples. Specifically consult:

- `docs/experiments/resource-retained-population/d5q-call-dataflow-map.md`
- `docs/experiments/resource-retained-population/d5r-query-scheduling-map.md`
- `docs/experiments/resource-retained-population/d5r-determinism-matrix.csv`
- `docs/experiments/resource-retained-population/d5r-report.md`
- `docs/experiments/resource-retained-population/d5r-review.md`
- the newly strengthened governance protocol and reviewer instructions, **as presently committed**.

Reverify installed identities before relying on native addresses: D5R's reference executable is Starfield **1.16.244.0**, EXE SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; corroborate ESM/PlanetData, Ghidra databases, raster and fixture versions from durable receipts. Addresses below are **preferred static VA**, image base `0x140000000`; they are not live addresses and must not be transplanted to other builds.

Relevant established anchors, to **verify and extend**, not treat as complete:

| Boundary | Static VA | Current significance |
|---|---|---|
| Cell preparation / region requests | `0x140aed020`, `0x1407b1420`, `0x1407a1580` | Query ingress and rectangular enumeration; upstream gameplay/focus origin remains unresolved |
| Coordinate/dependency acquisition | `0x1403625e0`, `0x1407b5a00`, `0x1407a1260` | Key/dedup/dependency construction |
| Layer/density workers | `0x1407b5160`, `0x1407a1940`, `0x14076c560` | Provider callers, readiness and aggregate reuse |
| Source provider | `0x14079f860` | RCX ProcGen, RDX original Int2 pointer, R8 aggregate output holder |
| Source selection / construction | `0x14079fa90..0x14079fa93`, `0x14079fcb3`, `0x14079ff18` | Selected source; exclusive map-miss and generator call |
| Resource sampling | `0x142339340` | Original-query-derived raster **low nibble**, numeric rarity control (not membership bits) |
| Focus and Grid shift | `0x1407b2390`, `0x140986da0`, `0x1407856b0` | Candidate upstream initialization and source-lifetime dependencies |

Preserve D5R's verified conditional prefixes: **L** query `(37540,20927)` -> mask 0 -> ordinary vector approximately `[0.05, 0.20, 1]`; **H** query `(37540,20929)` -> mask 3 -> `[1,1,1]` for Ionic Liquids, Fluorine, Copper. These are qualified *separate* continuation scenarios, not proof that both compete in one ordinary retail arrival or have different final geometry. D5R's 40,320 permutations are a **model**, not an empirical or full native scheduler census. Do not reframe the 50/50 split as a probability.

## 3. Start an active investigation ledger; pursue dependencies to their determining boundary

Create `docs/experiments/resource-retained-population/d5s-investigation-ledger.md` near assignment start, updated during work at material decision points. Use stable identifiers per hypothesis/edge. At minimum include controlling Q/AC, hypothesis, exact native/data boundary, candidate producers and consumers, evidence location, counterexample/negative control, attempted investigative actions, result/confidence, remaining alternative paths, and next discriminating action. Mark each material branch **resolved / disproven / irrelevant (with reason) / blocked (with proof) / open**. Preserve earlier failed hypotheses and meaningful chronology; never fabricate checkpoint timestamps or silently relabel unanswered branches as optional.

Trace *backward* from both provider callers through request registration and dispatch to the closest justified initial location/gameplay ingress. Trace *forward* from initialization, focus coordinates and streaming-region updates to the requests they actually generate. Pursue necessary dependencies across scheduler, landscape, worker, manager and data subsystems using the authorized read-only tools. Merely finding a further upstream caller, queue, callback, native writer or task boundary is **not a reason to end this assignment**. If a branch genuinely explodes, describe a defensible coverage boundary and prove why omitted branches cannot change the conclusion.

In particular determine, with exact instruction/call and field evidence:

1. **Initial-state and location inputs:** the origin and update rules of the focus/streaming coordinates, region bounds, current discriminator, task/manager initialization and loaded component state; how normal arrival determines their effective values. Separate static world data, outpost location, state regenerated after loading, and runtime-dependent or persisted inputs.
2. **Requests generated and admitted:** root and rectangle derivation, enumeration, keying/deduplication and original Int2 retention; both layer and density routes; neighboring requests, file prerequisites, callbacks, aggregate reuse, stale/cancelled/restarted requests, pending and visited branches.
3. **Real winner rule:** exact eligibility/dependency edges, publication/claim/inline execution, worker-pool and synchronization constraints, relative sequencing with landscape updates and source-map miss. Distinguish first registered, ready, started, source selected, unvisited, map miss, sampler call, region copied and retained output. Identify what a real engine trace or an exact offline scheduler proof would have to discriminate. Do not substitute a generic race model for native feasible interleavings.
4. **Source lifetime:** landscape shift owner and worker quiescence, Grid/cell contributor mutation, retirement-before/after map lock, reference acquisition and release. Determine whether the provider can access a selected raw source across a retirement interval and under which preconditions. Establish intended safety only to the level the evidence warrants, without chasing later allocator ABA unrelated to the invocation.

## 4. Determinism tests and a reproducible input contract

Build a complete input-dependency matrix and, where practical, a **focused offline executable evaluator** of the decisive queries/weights/geometry. Classify each required value as static data, derived from location, reproducible runtime state, order-sensitive runtime state, verified serialized state, or unresolved. Explicitly distinguish a *missing search result* from *an indispensable external input whose origin is evidenced*.

Require discriminating cases that separate: (a) fixed ingress and priority, (b) equivalent query samples, (c) distinct weights but equal surviving outputs, (d) different surviving outputs, (e) truly order-dependent first-writer selection, and (f) source/restart/previous-cache effects. Reuse existing native geometry and raster controls before inventing replacement simulation. If comparison of full ordinary geometry for L/H is necessary to answer Q2, follow the native generation/copy path far enough to compare **successfully owned destination regions** under equivalent pinned seeds, definitions, resource ordering, allocations and prerequisites. Account for Special/other routes when making whole-population claims. Record which alternatives are admissible in the actual engine versus constructed models.

If a unique original query can be derived for a specified normalized arrival state, provide its exact input provenance and the resulting selection recipe; independently test nearby/contrasting cases to challenge overfitting. If uniqueness cannot be established, determine the **smallest consequential unresolved input or scheduling edge**, whether its alternatives yield equivalent output, and what would distinguish them. Do not choose a candidate to match Save52 geometry after the fact.

### Conditional read-only save investigation

Use save-file analysis **only** when the dependency ledger identifies a specific indispensable input that cannot be recovered from executable, static data or derivable location/initialization state, and demonstrates a plausible persisted origin. Then inspect existing approved save documentation and protected copies (including Save52 if authorized by existing safeguards), read-only, looking for **that particular field/input**. Preserve input identities and source offsets, and distinguish serialized presence from proven causal use. No automatic large save archaeology, no save modification, no Starfield loading. If access needs fresh permission or material is inaccessible, prove the narrow blocker and escalate that action while continuing unrelated offline work.

## 5. Completion contract and hard escalation gate

This brief adopts the project-wide strengthened completion protocol, not the looser D5R outcome-D interpretation. Codex has authority to follow **material, technically plausible offline dependencies**, run disposable native tests, improve/re-run research-only scripts, repair evidence/test methods and continue after ordinary failures **within this single assignment**. No new brief is required just because a hypothesis fails or an additional native path is found.

Do **not** stop at “unable to find,” “further upstream work recommended,” “timing not established,” “static cannot prove concurrency,” or a formally correct but insufficient diagram. Before claiming `BLOCKED`, present for every indispensable open edge:

- Exact function/field/input/decision boundary and why resolving it is necessary for Q1/Q2/Q3.
- Exhaustive **relevant** approaches actually attempted, direct evidence and counterexamples; any reasonably available unused route and why it cannot discriminate.
- Barrier classification: missing authority, inaccessible data/capability, proven unsafe method, genuine external nondeterministic input, or actual execution/tool/resource exhaustion. Do not mislabel an incomplete search as an impossibility.
- Smallest specifically proposed external action, input or experimental discriminator, expected outcomes and how each would resolve the question; safe checkpoint to resume.
- The independent completeness reviewer's challenge to omitted routes and its disposition.

If genuinely blocked on one branch, continue independent authorized branches. If an indispensable live observation becomes necessary, **do not execute it**; prepare a narrowly defined proposed intervention and ask for maintainer authorization. A positive scoped result on Q2 does not silently waive an unresolved mandatory Q1 or Q3. If tools/session limits prevent completion, preserve the ledger, evidence and precise resume state; do not assert continued work will occur autonomously.

## 6. Preservation, review, and forbidden operations

Read-only Ghidra project/database investigation (prefer established `-readOnly -noanalysis` export), pinned binaries/data and existing archived research evidence; task-local ignored scratch and disposable native processes only. Never alter the installed game, runtime state, Ghidra database/symbols/types, Vortex, SFSE plugin, saves or protected originals. No Starfield/SFSE/Steam launch, debugger attach to retail, injected observation, plugin deploy, save-writing, dependency download or unrelated refactor. Keep decompiled proprietary material, raw binaries, dumps and protected saves local-only and untracked. Maintain the repository's protection and free-space guards where applicable, including 40,000,000,000 bytes caller-available on C: and D:; no arbitrary observation quotas. No stage, commit, push, public disclosure or B6 advancement.

Apply `docs/EVIDENCE_STANDARD.md` and `docs/EDITORIAL_STANDARD.md`: exact addresses/operand origins, binary identities, comparison controls, hypothesis falsifiers, evidence classes, manual prose review and independent exact-snapshot review. A static call edge proves a compiled path, not that Save52 actually followed it. A byte hash verifies identity, not scientific semantics. Do not rewrite historical D5R outcomes or acceptance: this task continues its **parent open question** prospectively.

**Independent completeness review is mandatory and adversarial.** Provide original D5R questions, this frozen brief, live ledger, complete source/negative evidence and exact current tree. Reviewer must identify the most valuable untested authorized avenue, or cite evidence that none remains. It must return **REWORK** if a material authorized route is open; **ESCALATE** for a demonstrated terminal authority/input barrier; **ACCEPT** only when every controlling question is COMPLETE and all mandatory ACs pass. Engineering/evidence and editorial reviews remain separate. Reviewer may not redefine criteria, approve its own modifications or confer retail/integration authority. Record actual reviewer access/execution limits; an absent reviewer is `NOT REVIEWED`, not acceptance.

## 7. Required deliverables

Use the established layout, with proportionate files and no redundant manifest sprawl:

- `d5s-investigation-ledger.md` — **active**, evidence-linked dependencies, counterexamples and branch dispositions.
- `d5s-query-winner-model.md` — exact upstream/downstream call/data-flow, real scheduling/lock constraints, normalized arrival-state input contract, candidate/winner rules, and source-lifetime proof/limits.
- `d5s-inputs-and-tests.csv` (or a justified equivalent) — all causally relevant inputs, provenance, consequence and adversarial tests, including conditional save trigger.
- `d5s-report.md` — answer **Q1, Q2, Q3 individually first**, with COMPLETE/INCOMPLETE/BLOCKED status, evidence, tested applicability, confidence, negative controls and remaining discriminators. No summary statement of completion that contradicts the question statuses.
- `d5s-sources.csv` and `d5s-review.md` — exact primary source references, immutable acceptance matrix and independent scientific/completeness, engineering and editorial dispositions.
- Necessary focused reproducible local scripts, receipts, negative controls, binaries/tool hashes, preservation and permitted-output manifest. Reviewed complete and task-only diffs, actual status/HEAD/index and exclusions; verify untracked-file coverage, patch applicability, whitespace and links. No staging/commit/push.

If truly BLOCKED, deliver the same evidence and ledger as an **escalation checkpoint**, with minimal permission request—not a misleading accepted final research completion. If INCOMPLETE, keep working within the authorized scope; a convenient intermediate report is not final delivery.

## 8. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **D5S-AC1 — Authority and pins** | Reverify exact game/data/Ghidra baseline and protections; stay offline/read-only, no runtime/plugin/save mutations or publication; report exact provenance and exclusions. |
| **D5S-AC2 — Question and ledger** | Freeze Q1–Q3, success/falsification scope and parent linkage; create/update active ledger before major analysis, preserve negatives and disposition every material dependency. No silent narrowing. |
| **D5S-AC3 — Upstream ingress** | Pursue both D5Q/D5R provider routes through focus, landscape streaming, location-derived roots, request creators and initial-state gates until their determining source or an evidenced terminal boundary; exact ABI/data/control evidence. |
| **D5S-AC4 — Actual winner arbitration** | Resolve the admitted query set and execution-order constraints far enough to answer Q1 at the stated scope, **or** prove a specific indispensable unavailable discriminator. Models and static locks alone do not establish real winner ordering. |
| **D5S-AC5 — Determinism/outcome discrimination** | Verify Q2 against fixed inputs and meaningful L/H counterexamples; distinguish masks, effective weights, complete successful geometry and population. Pursue necessary geometry equivalence tests or evidence a precise blocker. |
| **D5S-AC6 — Invocation source safety** | Follow landscape shift/retirement synchronization and both worker routes to answer Q3 within one provider/generator invocation, or demonstrate its specific terminal barrier. Do not require later cache-hit continuity. |
| **D5S-AC7 — Missing-state/save gate** | Maintain full input provenance; conditionally perform only targeted read-only save analysis for evidenced indispensable state; document triggers or nontrigger with actual searches, not guesses. |
| **D5S-AC8 — Continuation and blocker proof** | Follow material authorized dependencies across subsystems; no “not found” or unexamined viable lead as closure. Any BLOCKED meets the protocol's exact evidence/alternative/minimal-request standard. |
| **D5S-AC9 — Independent completeness review** | Scientific reviewer adversarially challenges unresolved ledger branches and highest-value omitted avenue; engineering and editorial reviews examine primary evidence and exact final snapshot. Enforce COMPLETE→ACCEPT, INCOMPLETE→REWORK, BLOCKED→ESCALATE. |
| **D5S-AC10 — Durable delivery** | Reproducible map, input/test matrix, source ledger, report and review; verified exact complete/task-only diffs, hashes, status, exclusions and human-readable editorial quality; no staging/commit/push. |

**Completion requires the controlling scientific questions to be resolved within the claimed domain, not simply the completion of ten documents/checks.** Any future change to Q1–Q3, their generality or the mandatory acceptance contract requires explicit maintainer approval and an archived amendment. D5S confers no retail GO or publication permission.
