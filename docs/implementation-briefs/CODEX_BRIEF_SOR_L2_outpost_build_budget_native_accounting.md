# Codex research brief — L2: Starfield outpost build-budget accounting and enforcement

**Project:** `starfield-outpost-research`  
**Task:** Bounded offline native/definition/UI/save research with independent review  
**Authority:** Read-only analysis and authored research artifacts only. No Starfield launch, new gameplay, save changes, runtime instrumentation, injection, deployment, staging, commit, push, or publication. Preserve all protected original saves, installed game data and analysis databases.

## 1. Research question and intended outcome

Explain **Starfield's own Build Limit system**: what the construction overlay's thin budget meter measures; how an individual constructed object or assembly receives a cost; how the engine efficiently obtains that cost; how per-outpost usage and maximum allowance are updated, validated and persisted or rebuilt; and how these values reach the UI and construction-rejection logic.

**Mechanism matters more than an exhaustive cost catalogue.** Follow a representative construction end to end from eligible construction definition and runtime cost source, through admission and budget mutation, to the displayed meter. A list of budget values without a causal native chain does not satisfy this assignment.

Keep **L1** (outpost count, cargo-pad/turret and other per-category limits, Planetary Habitation eligibility) accepted and closed. Reserve **L3** (beacon placement, territory clipping, collision, POI exclusions, terrain/procedural scenery suppression and reappearance) for the separate spatial investigation. Turret ownership belongs to the later turret phase. Crew and robot count limits are already mapped; reuse their evidence.

## 2. Baseline and investigative leads

Read `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, the accepted L1 and R1 reports, Workshop construction-root and population work, and the existing Kreet controlled-save experiment records. Confirm actual paths, installed executable/ESM version hashes, original save identities and current repository status rather than assuming filenames or RVAs.

Begin with a **small, targeted examination of Fallout 4 settlement-budget research** to discover useful names, actor values, dataflow patterns or probable engine inheritance. Record its sources, permission/provenance and leads. **Do not import its semantics into Starfield without independent evidence.** The final Starfield reports must be organized and explained in Starfield terms; any Fallout 4 comparison belongs only in a short investigative provenance section, not the explanatory model. Do not broaden this into research on Fallout 4, other games or the general renderer.

Use existing Kreet control snapshots where positive construction changes are known (beacon only, storage, Iron extractor, solar array, removal/control checkpoints), with specific source IDs and hashes. They are comparisons of actual saved constructions—not assumed meter measurements. Choose additional mature saves only if they offer a discriminating cost/usage/counter or robot/hab witness; distinguish unrelated snapshots from controlled before/after evidence.

## 3. Required native and data-flow investigation

### A. Budget definition and fast cost determination

Identify the actual budget dimensions and units, where maxima originate and which source determines object or assembly cost. Examine whether costs come from installed definitions, precomputed model metadata, runtime mesh/render measurements, construction-root bookkeeping, cached values, or a mixture. Trace cache creation, lookup, invalidation and any fallback/recomputation to the extent needed to explain how construction can validate a candidate efficiently. Separate **candidate cost calculation**, **existing accumulated usage**, and **rendering cost**; do not assume they are identical.

Investigate whether multiple dimensions independently impose a cap and how a single UI meter summarizes them. Trace selected exact native functions, structures, actor values, settings, script calls and their callers/consumers. If some metadata ultimately originates in a renderer, establish the relevant boundary and stop rather than reverse-engineering renderer internals unrelated to the budget.

### B. Budget enforcement and lifecycle

Trace actual admission/rejection, accounting and display updates for: entering build mode; previewing a candidate; placing one; deleting it; moving/rotating an existing construction; loading/restoring an outpost; and changes to maximum budget or effective current values. Distinguish UI gating from native authoritative validation and ordinary object creation from PackIn constituent references. Determine whether usage is maintained incrementally, recomputed from placed objects, or both; specify conditions under which the counter and visible meter might differ.

Inspect what happens when an outpost is already beyond its effective limit: is construction denied, is existing content retained, and is this a supported native rule or only an untested prediction? Do not expand into L1 category counts or L3 geometric placement eligibility.

### C. UI Build Limit meter

Trace the concrete provider and render path for the thin Build Limit bar visible in the user's supplied build-mode screenshot. Identify its numerator/denominator, normalization, rounding/clamping, refresh triggers and displayed full-state behavior; establish whether it represents a single dimension or a selected/composite budget. If compiled Scaleform content is involved, locate the exact binding sufficiently to explain the UI without recreating the entire menu system. Do not infer budget semantics from the bar's appearance alone.

### D. Targeted contrasts

1. **Hab interiors:** Does placing an otherwise comparable furnishing inside a hab differ in budget cost or charge path from placing it outside? Determine whether habitat membership, room/interior state, portals/windows or visibility matter to the *budget calculation*. Do not assume enclosed means occluded or launch a general renderer/visibility investigation. A supported same-cost finding is as valuable as a different-cost finding.
2. **Constructed robots:** Do R1's direct robot constructions enter the Build Limit budget, independently of the separate numerical robot cap? Identify their construction roots, cost/accounting representation and possible actor-specific branch. Combat, AI and pathing are excluded.
3. **PackIns and simple objects:** Contrast a direct ordinary container/facility with an assembled construction where existing Workshop root research makes instance accounting unambiguous.
4. **Procedural scenery:** Only determine whether pre-existing/suppressed environmental objects participate in budget accounting **if** the identified budget consumer reaches them. Their collision, suppression and reappearance mechanisms belong to L3.

Use a small number of actual, evidence-grounded examples, not an all-objects price list.

### E. Persistence and controlled-save correspondence

Establish what save files explicitly retain (counters, actor values, cost-bearing state, constructed population), what comes from definitions and what is recalculated upon load. Apply the native model to the supported Kreet snapshots wherever the required inputs are recoverable; give concrete calculated examples only with qualified operands. **An explicitly serialized build-budget value is not mandatory:** demonstrate native reconstruction when that is the design, and do not mark its absence as a research failure.

Do not silently equate all saved REFRs with constructed items: use accepted construction-root, PackIn and Workshop membership rules. Unsupported representation or missing historical HUD reading must remain UNKNOWN, not a fabricated zero or counter delta.

## 4. Required report structure and evidentiary standard

Lead with a concise, plain-English answer to: **What consumes Build Limit? How does the engine calculate costs rapidly? What enforces the cap? How is the meter populated?** For each answer distinguish established native mechanism, definition evidence, saved observations, predictions and unobserved current runtime state. Follow with an end-to-end path table/diagram, exact version-pinned native locators and operand provenance, worked Kreet/PackIn/robot/hab contrasts, and a short Fallout 4 *lead-only* provenance note.

Use the project's `PROVEN`/`STRONG`/`PROVISIONAL`/`OPEN` confidence vocabulary separately from assignment completion. Apply **reasonable engineering confidence**: coherent positive native mechanism plus suitable corroboration can establish the bounded ordinary model without proving the absence of every hypothetical exceptional path. A negative finding is meaningful when the relevant callers and data producers were actually bounded and inspected, not merely when a text search found nothing. Explicitly identify a concrete missing dependency before recommending a follow-up; do not automatically request live instrumentation or an endless geometry investigation.

Preserve prior L1 results; propose corrections transparently if contradictory evidence appears. Update `docs/RESEARCH_STATE.md`, relevant indexes/registers and the L2/L3 boundary/backlog as warranted, without rewriting historical accepted evidence as though it never existed.

## 5. Compact frozen completion contract

- **Task type / deliverable:** Offline explanatory research; answer-first L2 report, causal native/data/UI/accounting model, targeted examples, provenance/verification and independent review.
- **Authority and bounds:** Existing pinned executable/ESM, owned project scripts/readers, controlled Kreet and selected mature-save copies, analysis exports. No live operations, save editing, new runtime observer, build/deploy, external publication or Git staging/commit/push. Apply all existing source/permission and 40 GB free-space/protected-input controls for local tools and scratch work.
- **Mandatory acceptance:**
  1. Establish the actual budget metric(s), limits and exact meaning of a full budget, or give a specific evidence-backed unresolved operand with its consequence.
  2. Trace how object/assembly cost is obtained **efficiently**, including any actual precomputation/cache/lookup and the boundary of renderer dependencies.
  3. Trace construction admission/rejection and budget accounting for add/delete/move, and explain restoration/recalculation and over-limit handling where supported.
  4. Trace the Build Limit meter's provider, displayed formula/selection and refresh to the supported native/UI boundary.
  5. Resolve or specifically bound hab-interior, constructed-robot and PackIn-vs-direct-object comparisons, using actual definitions and native branches.
  6. Use independently identified Kreet control-save witnesses and other positive evidence as appropriate; distinguish byte-backed facts from hypothetical example calculations, and explain save/runtime correspondence without requiring a saved budget field.
  7. Provide reproducible primary evidence with exact pins, native instruction/function references, source permissions, relevant offline tests and protected-input checks; document failed approaches and important counterexamples.
  8. Independent reviewer acceptance against **these original criteria**, plus manifest, task-only/complete text diffs (including untracked authored text), exact forward/reverse patch reconstruction, Git/encoding/link/whitespace checks and explicit private/binary exclusions.
- **Optional improvements:** Additional object-cost examples or precise UI screenshots if independently available; neither is permission to expand the core question.
- **Negative-result closure:** A bounded, independently reviewed negative or unresolved path requires named entry points, explored consumers and why evidence does not discriminate; no invented universal absence, no automatic engineering abandonment on an ordinary failure.
- **Continuation:** Correct and retest in-scope failures under the same brief; preserve original mandatory criteria unless maintainer explicitly amends them.
- **Escalation:** Stop only the blocked action on an actual safety/resource/authority/access problem, retain receipts and report a narrow restart condition; continue independent authorized work. Do not impose arbitrary time/event quotas on healthy research.
- **Review disposition:** `ACCEPT`, `REWORK` or `ESCALATE` from an independent reviewer; distinguish completion, scientific confidence, tool integrity, live coverage and publication eligibility. No review result authorizes commit/push.

## 6. Handoff

Propose a suitable Conventional Commit subject for the complete L2 research package. Supply the exact task-only and complete diff paths plus immutable final package/verification receipts; leave the working tree uncommitted. L3 retains POI exclusion zones, clipped buildable territory, dynamic actor/flora collision, procedural scenery suppression and rocks reappearing after travel. Turret ownership/operation remains reserved for the turret phase.
