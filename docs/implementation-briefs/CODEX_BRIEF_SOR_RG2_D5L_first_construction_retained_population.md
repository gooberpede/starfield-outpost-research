# Codex research and implementation brief — RG2-D5L

## First-Construction and Retained-Population Behaviour — Phase A

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Authority:** **Phase A only: offline native research, instrumentation implementation, and disposable synthetic qualification.** No live Starfield launch, attachment, gameplay, forced cache reset, save modification, or Phase B acquisition is authorized by this brief.  
**Completion:** Produce an independently reviewed, scientifically discriminating **Phase B run card** for separate maintainer GO. Do not execute it.  
**Publication:** B6 and publication remain on hold.

### 1. Scientific purpose

Determine **whether and how the first successful construction query determines the generated resource population retained for a procedural source**, how a later demand uses that population, and which native transitions can invalidate or replace it. The experiment is intended to **test**, not assume, first-request-dependent geometry.

Distinguish these claims:

1. A qualified first demand traverses the visited guard and source-pointer map lookup, and takes a miss.
2. That *same invocation* supplies an original query, effective frame and sampled ordinary mask to a successful resource-generation operation.
3. The resulting region population is actually inserted into/owned by the ProcGen source map for a demonstrable source and manager lifetime.
4. A later demand for that source finds and reuses the same retained population, or demonstrably regenerates/replaces it.
5. Any observed resource-geometry change has a causally linked source-lifetime and reconstruction history, rather than merely coinciding with a new consumer scan.

Successful Phase A preparation means the observation method can distinguish these alternatives if their qualifying events occur. **It does not require a hypothesis-confirming result, nor guarantee that normal gameplay will create a first miss during a particular session.** Consumer-only evidence and incomplete decision records must be retained as such, not promoted to complete construction evidence.

### 2. Existing evidence and constraints (must be read, not rewritten)

Start from the durable records and their actual local primary evidence, especially:

- `docs/experiments/resource-population-lifecycle/` (D5C): source-pointer keyed retained population map, distinct `source+0x68` visited guard, insertion and reset/destruction, incomplete-population hazards.
- `docs/experiments/resource-construction-demand/` (D5D): ordinary cell/coordinate preparation can request construction before Workshop consumption; prior capture timing limits.
- `docs/experiments/resource-source-decisions/` (D5E): fixed decision-breakpoint collector and its tier/lifetime/completion limitations.
- `docs/experiments/resource-combined-acquisition/` (D5B): source-bound consumer-only Ionic Liquids/Fluorine/Copper regions at second Feynman V; exact frozen mask-3 geometry agreement does **not** witness the original mask/epoch.
- `docs/experiments/resource-query-reachability/` (D5H) and `docs/experiments/resource-query-variability/` (D5I): 19 conditional mask-invariant and six conditional mask-variable source projections within stated common initialized-state premises. Alternative **feasible** native first-miss paths are not historical gameplay observations.
- `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, `WORKFLOW.md`, `docs/templates/completion-contract.md` and the independent reviewer instructions.

Treat Starfield.exe and installed-definition identities as version-pinned scientific inputs (historical target executable **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`); confirm actual local pins before relying on them. Addresses in previous native studies may be **preferred static VAs** rather than module-relative RVAs. Document the domain of each address, with real module-base relocation for any future observer. No modification to installed binaries, saves, protected source exports, or archived evidence.

**Primary candidate:** second Feynman V source `0:37536:20928:0029d20e`; alternatives within its qualified first-construction route use masks **0/3**. D5B supplies consumer geometry but no producer epoch. **Other candidates:** Feynman VIII-b variable sources or a better-supported, naturally first-constructed source. Codex may select a different primary target only with explicit evidence that it improves the probability of a qualified ordinary first-construction observation; preserve the comparison and proposed fallback. A historical Gold/Antimony/Copper substitution report is a separate unproven hypothesis, not the desired result.

### 3. Required Phase A work

**A. Native lifecycle and evidence contract.** Identify precise provider-entry, visited-source branch, map lookup hit/miss, original query and mask sampling, generation-completion, population insertion/ownership, map reuse, reset/destruction/replacement and (if pertinent) consumer boundaries. Pin function/instruction evidence and registers, stack/structure fields and object lifetimes. Be especially careful that *map insertion precedes synchronous generation* in the inspected path: an inserted wrapper or visited marker alone is **not** proof of successful populated geometry. Establish a defensible completion witness with the resulting actual region data, or demonstrate an equivalent causal completion condition. Distinguish manager identity, geographic source identity, runtime source pointer and lifetime/epoch identity; handle address reuse.

**B. Instrumentation choices.** Assess at least the viable combinations of existing D5E continuous decision monitoring, D5B producer/consumer capture, and a minimal completion/lifetime witness. Choose the smallest defensible observation architecture; do not require a new framework or forbid instrument changes if genuinely necessary. Show how it retains decision coverage through unrelated events, concurrent tasks and breakpoint-slot limitations. If a complete causal chain cannot fit within four hardware slots, evaluate a sound alternative acquisition strategy instead of silently lowering the evidence tier. Every unavoidable gap must have explicit scientific consequences. Avoid pretending timestamps, matching resource names or shared geographic keys alone establish lifetime ancestry.

**C. Actual implementation and qualification.** Implement only what is needed for the chosen evidence contract, reusing existing controller/receipt/teardown infrastructure. Exercise a real disposable Windows process when debugger functionality is involved; synthetic model-only tests do not substitute for breakpoint and thread behavior. Include at minimum: first miss → successful population → insertion → subsequent hit; visited bypass; miss with failed/incomplete generation; source pointer reuse and manager reset; two different initial-query masks across distinct lifetime scenarios; unrelated source traffic, overlapping/concurrent threads, nesting, interrupted acquisition, corrupt/missing evidence, durable acknowledgements and clean STOP. Prove the reduction and reviewer reject unqualified joins and faithfully preserve contradictory observations. Run relevant inherited regression tests; avoid full unrelated test programmes without a concrete reason.

**D. Natural experimental opportunity.** Evaluate when and where ordinary gameplay would trigger the first qualifying construction. Consider main-menu pre-load coverage as a protection against missing events, *not* a presumption of eager save-load population. Use ordinary cell/planet preparation and D5D demand pathways. Assess whether existing/previously visited Feynman V locations are likely to yield a first miss, and consider an alternative source whose creation is more reliably triggered. No live probe in Phase A. Do not propose cache deletion, forced regeneration, outpost modifications or a scripted placement as the default. Explain what a qualified non-hit, cache hit, visited bypass and missed observation each mean.

**E. Completion and review-ready run card.** Produce one bounded Phase B proposal listing: target/source and why chosen; protected save and exact game/tool pins; earliest arming and coverage-readback barrier; operator gameplay actions; allowed and forbidden interventions; event and identity checks; genuine safety/disk guards; evidence preservation; STOP/teardown and recovery; outcomes (including valid negative and incomplete results); explicit criteria for when a captured *complete* construction→retention→reuse chain is established; and what requires a separate authorization. Do not require arbitrary time limits, event quotas or healthy-session cutoff. Phase B remains **NOT AUTHORIZED** even if all Phase A criteria pass.

### 4. Research-workspace policy — important

**Read-only pertains to originals, authoritative scientific inputs and installed content; it does not render the scratch workspace immutable.** Under task-owned `.local-work/` paths, Codex may create, overwrite, reuse and remove its own disposable scripts, diagnostics, temporary JSON, failed fixture outputs and intermediates. Do not globally pin every scratch artifact or make old failures permanently protected filesystem objects simply because they were emitted. Do not touch other tasks' or historic evidence without independent authority.

Preserve the scientific essentials: primary irreplaceable observations, decisive counterexamples and failed *scientific* controls, exact methods/versions needed to interpret conclusions, qualification summaries and review-grade decisive receipts. A failed intermediate Python invocation does not require permanent retention of every temporary file; the final record should state material failures and fixes without exhausting disk space. Apply task-scoped hash checks to scientific inputs, preserve saves/archives, and use the **active archive-backed baseline**, not the obsolete 93,334-loose-file verification. Do not initiate any archiving, cleanup or preservation-infrastructure project. Check the actual C: and D: disk floors (40,000,000,000 bytes each) before significant temporary writes; minimize durable output volume. If old strict namespace checks fail solely from the previously disclosed four intentionally removed ZIPs, report that failure honestly and separately test all surviving protected authoritative scientific inputs; do not invent restoration or alter the baseline.

### 5. Fixed acceptance contract (AC1–AC8)

These mandatory criteria are frozen before work. A valid scoped negative finding may satisfy the *scientific* deliverable when proved with controls, but inability to implement/qualify a mandatory complete witness **cannot** be relabeled success. Preserve the precise missing capability and return REWORK/ESCALATE when warranted. The maintainer alone may approve material amendments.

| ID | Mandatory requirement |
|---|---|
| **AC1 — Authority and integrity** | Phase A only; no retail Starfield, protected/save or installed-content mutation; valid task-scoped pre/post preservation and active archive-backed baseline. |
| **AC2 — Native causal contract** | Instruction/field-bound lifecycle and completion contracts distinguish query, sampled mask, first miss, successful geometry, owned insertion, reuse, replacement and false-success markers. |
| **AC3 — Discriminating hypotheses** | Explicit competing predictions and an evidence matrix identifying what proves, refutes or leaves each claim unresolved, without requiring confirmation. |
| **AC4 — Qualified acquisition** | Demonstrate credible end-to-end association of source-bound initial query/mask, completed generated population, retained lifetime and subsequent hit/reuse in real disposable Windows qualification; record unavoidable native qualification limits. An instrument that can only return incomplete decision evidence does not pass. |
| **AC5 — Target/trigger justification** | Defensible primary source and naturally reachable first-construction opportunity; compare alternatives, and disclose cache-only/non-hit risk. |
| **AC6 — Bounded Phase B readiness** | An executable reviewed run card with protected saves, earliest coverage, exact identities, operator actions, STOP, uncertainty outcomes and **separate explicit GO**. |
| **AC7 — Reproducible durable record** | Concise scientific report, crucial source/evidence pins and decisive test outcomes, relevant regressions, proportionate scratch and editorial completion; existing geometry controls/predictor/frozen D2–D5I results unchanged. |
| **AC8 — Independent review and exact delivery** | Independent scientific, engineering and relevant safety/editorial assessment of the exact delivered implementation and original AC1–AC8; complete/task-only diffs, untracked text, hashes, inclusion/exclusion manifest, and final-delta review where substantive changes occur. No stage/commit/push. |

### 6. Required output and disposition

Place durable authored materials in a suitable `docs/experiments/` directory with concise `report.md`, `native.md` or equivalent exact boundary register, `validation.md`, `review.md`, and **proposed** `run-card.md`; use task-owned research source files only where needed. Follow established documentation and provenance patterns without proliferating boilerplate files. Provide links to completed artifacts and exact complete/task-only diffs for maintainer critical review.

Report separately: (i) scientific findings and falsifications; (ii) instrumentation qualification and missing event/identity coverage; (iii) target survival/restoration (not applicable in Phase A); (iv) integrity and execution authority; (v) independent acceptance and final snapshot identity. Do not count a synthetic full-lifetime proof as retail evidence. **Do not change model predictions to fit future observations; matching a desired native result is not an acceptance criterion.**

If AC4 cannot be met after genuine in-scope engineering investigation, document attempted viable architectures, actual failures, safest remaining path and exact missing dependency/authority, and return REWORK or narrow ESCALATE—not another nominally approved tier-C-only collector. If accepted, Phase B still awaits a separate maintainer decision.
