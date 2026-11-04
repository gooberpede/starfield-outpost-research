# CODEX IMPLEMENTATION BRIEF — RG2-D5AQ
## Ordinary Construction-Mask Invariance and Different-Mask Winner Reachability

**Status:** Proposed, maintainer-authorized **offline investigation only**. **Date:** 2026-11-04 (Australia/Sydney).  
**Project:** `D:\Projects\starfield-outpost-research` (`starfield-outpost-research`).  
**Primary parent:** **GC-10**, within the still-open **D5R** resource-generation investigation.  
**Target:** Feynman V Cu IL F, source `0:37536:20928:0029d20e`, body FormID `0x0005e0de`, pinned Starfield executable version **1.16.244.0**.  
**Deliverable status:** Authored source and synthesis REVIEW-REQUIRED; raw proprietary evidence LOCAL-ONLY; publication ON HOLD. No installation, launch, attachment, injection, target execution, save mutation, Git staging/commit/push, or live experiment is authorized by this brief.

## 1. Decision and scientific purpose

Five qualified retail constructions identified **five distinct original constructing requests**, yet each **directly sampled ordinary raster mask `0x3`**:

| Observation | Original constructing request | Direct sampled mask | Qualification |
|---|---|---|---|
| B2 | `(5, 0)` | `0x3` | Later requester passed protected map miss despite an earlier target visited check from `(4, -1)`; the precise lock-admission race was not instrumented |
| D5AK Episode A, A0 | `(8, 3)` | `0x3` | Qualified initial retail population |
| D5AK Episode A, A1 | `(-1, 11)` | `0x3` | Qualified within-process re-creation after departure and return |
| D5AL Episode B, B0 | `(0, 0)` | `0x3` | Qualified new-process construction |
| D5AO N2 | `(-2, 11)` | `0x3` | Full task/owner history; density publication-frontier request retained a progress lead |

These are **five constructions across four retail sessions, not five independent cold-start draws**. D5AG's fixed-source original-instruction controls show a genuinely different ordinary output for mask `0x0` (74 regions / 193 points) versus `0x3` (78 regions / 180 points), even though resource identities coincide; `(4,-1)` produced `0x0` and `(4,1)` and `(5,0)` produced `0x3` under those *specified controlled inputs*. Do not silently transfer those fixture inputs, source frames or other preconditions to every retail observation.

The research problem is not to show that `0x3` is common, nor to manufacture a different output. It is to determine whether ordinary engine rules **constrain different-mask requests from becoming construction winners**, or whether otherwise valid ordinary execution permits race-dependent mask selection. If no invariant exists, demonstrate the reachability and limitations rigorously before contemplating a statistical account.

**Frozen parent question (do not reword GC-10 to fit the result):** What determines the resource construction winner under ordinary gameplay, and how consistently does that mechanism operate? D5AQ is a specifically scoped offline sub-investigation of the *apparent ordinary mask invariant*, **not completion of GC-10**. Keep D5R/GC-10 open absent their original completion evidence.

## 2. Frozen D5AQ controlling questions

**D5AQ-Q1 — Exhaustive ordinary candidate/mask mapping.** For the actual observed 14×14 density request cohort (`x,y ∈ [-2,11]`) and the qualified source/descriptor inputs, what effective mask would each of the 196 original requests sample **if it reached ordinary construction**? Can the full conversion and sampling pipeline be reproduced and independently checked against known native and retail observations? Which candidate classes, input variants or unresolved samples cannot be assigned conclusively?

**D5AQ-Q2 — Different-mask winning-request reachability.** For each non-`0x3` candidate or distinct effective-input class, can a request ordinarily pass all required ingress, task, lifecycle, readiness, provider/source, visited, exclusive-owner and map-miss constraints **before a `0x3` request**? Is there an actual native ordering/eligibility/input invariant preventing that, or a complete normally reachable counterexample? Do not equate “possible with an arbitrarily chosen scheduler” to “possible under the complete ordinary execution contract.”

**D5AQ-Q3 — Closure of candidate native mechanisms.** Which still-live native writers, readers, callers, initializer/installer transitions, coordinate converters, raster samplers, cache/visited/map mutators, or downstream normalizers could make varying winners converge on mask `0x3` or make different-mask winners impossible? Can Codex close those paths using a receiver-/call-/alias-indexed dependency inventory, with counterexamples and explicit remaining uncertainty?

**D5AQ-Q4 — Evidence-constrained scientific disposition.** Do Q1–Q3 support (a) a qualified structural ordinary-execution invariant, (b) a complete ordinary-reachable different-mask winner, or (c) a precisely demonstrated missing native edge/essential runtime input? What each conclusion can and cannot establish about normal retail behavior, and what *minimal* future measurement—if any—would discriminate remaining cases? Statistical frequency must not be fabricated from candidate counts, scheduler fixture cases or five retail observations.

### Mandatory distinctions

Keep separate throughout: request enumeration; task *eligibility* and readiness; publication/dispatch/claim; source selection; visited check; writer pending/ownership; protected pointer-map miss; original Int2-to-descriptor/frame conversion; ordinary raster sample; optional Special/Everywhere passes; **complete represented geometry**; and actual retail frequency. Source and task allocations, visited tokens, pointer-map keys, Grid owners and ProcGen owners are distinct identities. A same-mask fixture is not an equal-full-generator certificate without the other effective inputs.

## 3. Workstream A — Complete 196-request map

1. Authenticate the exact native source/descriptor, game build, generation/raster methods, original provenance and selected retained evidence. Establish the actual density cohort from N2's complete typed task record; independently verify its rectangle, coordinate ordering and task identities. Do not assume all 196 are equally eligible or equally likely to win.
2. Derive the request-to-raster transform and sample from the **compiled ordinary code**, using existing D5T/D5U/D5AG methods where their input contracts actually match. Record relevant source origin, descriptor anchor, frame, clip, cell/raster keys, stage/readiness assumptions and applicable extra-pass conditions. Identify whether the transform uses the constructing original Int2, a transformed/query-derived Int2, a substituted canonical query, or some other authority.
3. Compute and persist **one row per candidate**: original `(x,y)`, task family/identity relationship, effective coordinates and mask, input-contract provenance, stage validity, classification (PROVEN / CONDITIONAL / UNRESOLVED), native site/operand evidence, and reproducible verification handle. Rows for unresolved candidates must remain explicit; no inferred fill or guessed mask.
4. Supply a **complete machine-readable 14×14 mask grid** and a clear human-readable plot/table showing every cell and its class. Provide totals by mask and unresolved cells, and overlay *retail winners* separately. Include an independently coded reference/oracle that checks coordinate conversion and every mask against native controlled cases. At minimum test the historically known `(4,-1)→0`, `(4,1)→3`, `(5,0)→3` within their authentic **D5AG fixed-input** contract; where any contract differs, show the divergence rather than claim a match.
5. Explicitly test boundary/phase, alternate descriptor/owner, absent raster, failed allocation, and applicable nonordinary resource passes so the map is not promoted beyond its justified contract. Treat the full mask census as a **conditional outcome map**, not a winner-probability distribution.

**Deliverables:** `d5aq-request-mask-map.csv` (196 rows), concise rendered/Markdown matrix, input-contract/verification receipts, counts, independent oracle and research note describing what changed when controlling inputs changed. All derived files must identify their evidence basis and limits; do not include Bethesda proprietary raw binary content in tracked publications.

## 4. Workstream B — Reachability and counterexamples

Investigate the *ordinary* complete path for different-mask candidates, starting from the outcome classes in Workstream A. Use prior D5S, D5AE, D5AF, D5AM and D5AP findings as constraints, not as interchangeable demonstrations of live feasibility.

For each meaningful candidate class, trace:

- Ordinary source/focus/cell-demand ingress, enumeration and deduplication; any caller-specific gates.
- Density versus layer task creation, dependency counts, registration, readiness, activation, ready-tree ordering and direct dispatch possibilities.
- Worker-local/owner/peer/shared queue service, successful claim versus merely observed claim-return; potential overtaking before and at the watched exclusive lock.
- Provider traversal order over sources; target source validity and lifetime; source's actual owning Grid and current ProcGen manager/descriptor.
- Shared visited token result, callback-return/observer gap, exclusive pending and admission, full pointer-map lookup and actual miss authority.
- Snapshot of effective input *at the selected generation*, not at an unrelated prior query or current manager state after reset; mask sampling and the applicable ordinary/extra passes.

Produce both **supporting paths and adverse alternatives**. A candidate whose request would yield mask `0x0` in isolation is not a demonstrated ordinary alternative unless all preceding constraints permit it to be the **first constructing miss**. Conversely, an observed mask-3 publication-frontier lead is not proof of a universal ordering invariant. B2's earlier visited contender and later winner must be treated as a genuine contrary history to oversimplified first-check/first-publication rules; it does not by itself demonstrate a different-mask winning construction because its losing candidate's retail mask was not directly recorded.

If a different-mask ordinary-reachable path is claimed, require a **fully instantiated, feasible continuation** from qualified ordinary startup premises: real dependencies, readiness, worker/queue transitions, native lock-state operations, same-owner competitors, source/visited/map lifetime, generation input contract, no invented native priority/mutation, and an independently executed/verified native-control witness where feasible. Report clearly whether the witness demonstrates **native feasible** or **actual retail observed**; do not relabel one as the other. Attempt to falsify the witness via earlier guaranteed winners or hidden readiness constraints.

If an invariant is claimed, state its exact scope and prove the **exclusion mechanism** across all relevant different-mask classes and ordinary paths. A bounded set of examples, an overwhelmingly mask-3 map, or a lack of observed contrary winners is insufficient proof.

## 5. Workstream C — Closed native-dependency inventory

Create an actively maintained, evidence-indexed inventory for each plausible convergence/exclusion mechanism. Use actual PE instructions (verified against installed build), safe disposable Ghidra copies and existing native host controls as appropriate. Include:

1. Relevant native **readers, writers, callers and aliases** for selection/raster input and owner/source/visited/map state; note indirect/vtable/computed and separate native owner branches instead of declaring a one-caller closure from direct xrefs alone.
2. Full ordinary call-chain placement of any suggested canonicalization, substitution, special-stage, regeneration or later overwrite. Distinguish *before* construction from *after* content copying or consumer caching.
3. Evidence that rules out hidden ordering constraints, or identifies them; actual mutex/semaphore, task dependency, waiter, owner-wide lock and worker action semantics are required to claim ordering. Do not convert a lock's ability to overtake into a measured normal overtake rate.
4. Material alternative explanations explicitly challenged: equivalent-mask convergence; conditional frontier/readiness dominance; different-mask exclusion; postselection input canonicalization; later geometry replacement; persistent/retained state; partial generation/failure; genuine race-dependent output.
5. A closure ledger where every candidate is **PROVEN, REFUTED, CONDITIONAL or UNRESOLVED** with actual evidence, tested counterexample, unanswered dependency and next action. “No further locations to look” is not a proof; name the bounded graph and why any excluded path cannot affect the conclusion.

Do not spin up a new observer or game run to compensate for missing static analysis. If a genuinely indispensable runtime operand is unavailable, explain exactly how it would decide between live theories and why remaining authorized offline alternatives cannot recover it.

## 6. Statistical possibility — analysis, not assumed answer

The complete 196-cell mask census is mandatory even if a structural invariant is ultimately found. Show:

- Number and percentage of candidate coordinates in each mask class, with eligible/conditionally eligible/unresolved cohorts separated.
- Why **candidate counts are not winner probabilities**. State the additional, empirically justified scheduling/eligibility model required to infer a distribution. No uniform or independent-race assumption without evidence.
- If a supported conditional model makes a statistical forecast, expose its assumptions, sensitivity to queue service/latency/order, and plausible bounds. Explicitly assess substantial contrary-mask probabilities (including a scenario ≥20%) against the limited, nonindependent observed retail history. Treat 20% as a user-specified scepticism threshold for *investigation*, **not** an automatic pass/fail probability or proof of impossibility.
- If the native contract admits several masks but ordinary probabilities cannot be established offline, say **reachability known / prevalence unknown**. Do not force a statistical explanation or accept five identical masks as a mathematical guarantee.

## 7. Offline methods, safety and permission boundaries

- **No live Starfield, Vortex deployment, SFSE attach, debugger attach, injected timing/priority changes, forced native construction, protected save/config writes, or gameplay.** No native observer DLL modifications or new retail instrumentation under D5AQ. Authorized work is analysis, owned disposable original-instruction fixtures, bounded offline tools and reproducible evidence.
- Preserve protected Save52, all protected saves/backups, sealed B2/D5AK/D5AL/N2 archives, and prior code/snapshots. Use only read-only original data, verified disposable Ghidra copies and fresh local scratch. Never open/change original Ghidra analysis project. Preserve original recorder and historical prediction statuses.
- Respect the existing caller-available **40,000,000,000-byte minimum on both C: and D:** for applicable tool outputs; no arbitrary healthy investigation quota. For any tool limitation, report the actual failure and a justified alternative rather than prematurely closing research.
- Use pinned interpreter with `-E -B`; production research entry points must refuse optimized Python before safety-sensitive imports. Actual code must preserve explicit failure, input provenance and output identity. No new third-party code/service or publication without separately approved policy.
- Required reading: `AGENTS.md`, `WORKFLOW.md`, project charter/research state/decisions, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, relevant D5T/U/S/AE/AF/AG/AM/AO/AP/retail reports, native sources and save-protection policy. **Reading completion and applied understanding are mandatory, but reading order is not an acceptance criterion.** Reviewer must substantively check important premises.
- Two active specialist sub-agents maximum. Primary owns integration; any independent substantive reviewer must be non-implementing, read-only and evaluate the exact final snapshot. Document exceptions without implying they change scientific facts, and request maintainer disposition where required.
- No stage, commit, push, remote publication or user-visible proprietary evidence unless separately permitted.

## 8. Frozen acceptance criteria

**AC01 — Authority, reading, scope and preservation.** Full required reading with demonstrable application; compliant offline permissions, sub-agent count, file/input protection, unchanged raw/saves, appropriate logs and verified disk floors. Reading chronology is not a pass/fail requirement.

**AC02 — Exhaustive request/mask census.** All 196 original density coordinates accounted for with authentic source/descriptor input contract, effective conversion and mask or explicit unresolved reason; independent oracle and human/machine-readable full map; exact retail/fixed-stage distinctions.

**AC03 — Mask input and full-output semantics.** Independent checks of mask 0 versus 3, same-mask equivalence under bounded inputs, extra-pass applicability, relevant source/descriptor/raster readiness, and semantic limitations. No general equation of mask and complete population without premises.

**AC04 — Ordinary winner reachability.** Actual all-stage ordinary constraints investigated for every materially distinct non-3 class; concrete valid feasible counterexample or supported exclusion, with all unconstrained alternatives honestly identified. Unsupported arbitrarily scheduled fixture does not count.

**AC05 — Native closure.** Cross-checked causal dependency inventory of relevant direct/indirect caller, writer, reader, alias, lifecycle and normalization paths; opposing alternatives actively tested with evidence. Completeness challenges answered, not silently deferred.

**AC06 — Statistical interpretation.** Full mask-class counts separated from winner probabilities; no assumed uniform probabilities; conditional probability model only if actually supported. Explicit analysis of user-concerned materially large contrary outcomes, without inventing occurrence rates.

**AC07 — Falsification, original question and status.** Distinguish native-feasible, observed retail and untested; falsify leading account against B2 and N2; preserve five historical observations, prior forecasts and unchanged GC-10/D5R/GC-31 scopes. No retroactive claim of deterministic invariant or normal frequency from five masks.

**AC08 — Reproducibility and durable handoff.** Active ledger, input/source pins, method/results, all-196 results, unresolved table, contrary witness or proof, and concise decision for the smallest next experiment if required. Source/derived artifacts should be auditable independently without distributing proprietary raw data.

**AC09 — Independent scientific and editorial review.** Non-implementing reviewer challenges all four original questions, especially the 196-mask oracle, ordinary-reachability completeness, inferred constraints and statistical claims; verifies source, fixture and regression evidence within stated method; reviews final exact files and complete/task-only patch provenance. Separate scientific completeness and engineering/editorial dispositions.

## 9. Completion and escalation standard

D5AQ completion cannot be earned by producing a plot, retelling the scheduler, enumerating feasible masks, passing test counts or documenting an unsupported interpretation. The final report must state a defensible answer to Q1–Q4 and one of the following **scientific outcomes**:

**A — Structural invariant established:** Proof specifies the qualified ordinary source/inputs, how all other mask classes are excluded or converged before/at generation, and why relevant native alternatives cannot overturn it. Does not assert universal behavior across builds/locations.

**B — Different-mask ordinary winner is reachable:** A complete valid native ordinary-execution counterexample is established, with exact required conditions and evidence that no skipped prerequisites/hidden ordering invalidate it. Explicitly distinguish native reachability from actual retail occurrence, and treat frequency as unknown unless separately measured.

**C — Essential uncertainty remains:** Identify exact missing native edge, input or executable condition, independently demonstrated inability of available *authorized* methods to resolve it, viable alternatives exhausted and the smallest next discriminating method/authority. Q1–Q3 must be completed to their original scope or individually marked INCOMPLETE/BLOCKED. **Do not turn outcome C into unqualified overall ACCEPT if any mandatory controlling question remains unresolved.** Follow the project completion protocol and request a narrow escalation only upon real documented barriers.

Independent acceptance of a completed bounded negative or reachability proof is possible without asserting GC-10's broader normal-frequency conclusion. Keep parent GC-10/D5R OPEN until their actual questions are answered.

## 10. Deliverables and Codex handoff

Put tracked authored research documents under `docs/experiments/resource-retained-population/`, methods under `research/resource-retained-population/`, and raw/derived proprietary receipts in fresh ignored `.local-work/d5aq/` paths. Use names such as:

- `d5aq-report.md` — answer-first Q1–Q4, confidence, coverage, native/retail distinction, unresolved status.
- `d5aq-request-mask-map.csv` and `d5aq-mask-map.md` — all 196 coordinates, conditional assumptions, counts and visual matrix.
- `d5aq-mask-method.md` and reproducible owned Python/native oracle and receipts.
- `d5aq-reachability.md` — class-by-class feasible/infeasible paths and counterexample or exclusion evidence.
- `d5aq-native-dependency-inventory.md` — bounded caller/writer/reader/alias closure and competing explanations.
- `d5aq-statistical-limits.md` — counts versus probabilities and sensitivity assumptions.
- `d5aq-investigation-ledger.md`, `d5aq-review.md`, necessary checklist/state changes, and exact final handoff manifest/diffs.

Codex summary must give the **scientific disposition first**, then Q1–Q4 and AC01–09 outcomes, candidate masks/counts, what is actually demonstrated versus still open, independent review result, and clickable local links to the report, 196-cell map, reachability/dependency records, review and both diffs. Do not manufacture a ready-to-run package or a new experiment. No staging, commit or push.

---

**Research priority:** Establish whether normal Starfield construction makes a different-mask winner **impossible**, **possible under complete ordinary conditions**, or **still undecidable for one specifically identified reason**. A map of candidate outputs is necessary, but the actual answer lies in their native reachability and any invariants on the path to the protected construction miss.
