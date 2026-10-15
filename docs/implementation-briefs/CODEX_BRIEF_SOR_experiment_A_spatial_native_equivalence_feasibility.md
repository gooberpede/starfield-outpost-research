# Codex research brief — SOR Experiment A: Native Spatial Predicate Equivalence, Offline Feasibility Gate

**Status:** Research/design assignment only. **No observer implementation or live execution authorized.**

## Purpose and scientific question

Determine whether a **single, bounded, observation-only native experiment** could independently validate the reconstructed Starfield inorganic-resource spatial predicates against the game's actual per-candidate accept/reject decisions. The primary deliverable is an evidence-backed **GO / REVISE / NO-GO** judgment, not instrumentation. A correct NO-GO is a successful outcome.

Our Milestone B executable spatial evaluator represents geometric predicates inferred from static native analysis. Its tests presently use synthetic inputs; the 0.7.0 capture contains many query descriptors and final resource populations, but **not** complete native candidate-region operands paired with each native geometric decision. Previous 0.8.0 local-readiness observer was **NO-GO**: its headers/source-visitation events could not close this gap. Do not assume the existing observer is suitable simply because it has passed offline engineering tests.

**Target claim to test:** Given the *same complete query and region operands*, the independent spatial evaluator produces the *same acceptance or rejection* as Starfield's native evaluator. This is about spatial-predicate equivalence, **not** remote resource querying, planetary generation completeness, cache-readiness, UI aggregation, or extractor placement.

## Source of truth and scope

Start by reading the repository's current `WORKFLOW.md` and pertinent durable research documentation, including Milestone B's spatial reconstruction, function register/native map, pinned disassembly/decompilation, 0.7.0 capture analysis, the native availability-map and region-dependency studies, and the 0.8.0 scientific-value reassessment. Use existing project names/paths and executable-version pins, rather than inventing new addresses or signatures.

Keep hypotheses, instruction-derived facts, historical runtime observations, and your proposed instrumentation clearly separated. Cross-check consequential decompiler statements against pinned native instructions. If a needed file or native export is absent, document the absence; do not substitute speculation. Preserve all protected game, save, Ghidra, archived evidence and research inputs.

## Workstream 1 — Define the independent comparison

Trace the recovered geometric evaluator from the native query call through the **actual point of the candidate-level native decision**. Identify the narrowest trustworthy native execution boundary or boundaries at which the relevant operands and result could be paired. Provide exact pinned build, module/RVA, caller/callee relationship, relevant instruction ranges, and the observed/inferred calling convention or object layouts **with evidence references**.

Prepare a field-level **minimum capture contract**; assess each field as directly readable at the candidate boundary, obtainable through verified ancestry, inferred (not admissible as independent input), or unavailable. Include, insofar as the actual code requires them:

- Query XYZ, coordinate-frame/domain identity, radius and separate upper-coordinate operand; binary representation and unit conventions.
- The native translation-table / transform operands **actually used**, not just an approximated conversion derived from final outputs.
- Candidate identity and source/resource association sufficient to disambiguate multiple regions and repeated evaluations.
- Native candidate geometry: centers, relevant region bounds, **complete ordered point arrays and widths**, point counts, and any additional branch-specific operands.
- The native branch taken (zero-point, single-point, multi-point, broadphase, taper, vertex/edge checks as applicable), and the **actual Boolean accept/reject result**, including negative candidates.
- Invocation identity, thread/nesting provenance, object lifetime and mutation/concurrency safeguards sufficient to prevent pairing an operand from one event with another event's result.

Check which fields are strictly essential at the chosen decision boundary: do **not** insist on capturing upstream representations that are already reduced to sufficient native operands. Conversely, a region header, source visit, final resource union, UI rows or inferred acceptance is **not** a substitute for the candidate-level comparison.

## Workstream 2 — Discriminating cases and independent oracle

Construct a coverage matrix of the reconstructed native spatial branches. For each branch, specify what **realistically occurring native inputs** would exercise it, what native outcome would be captured, and how the independent implementation would replay it. Prioritize true and false decisions; coordinate/height cases; transitions at region boundaries; and relevant floating-point edge behavior. Do not promise artificial edge cases will occur naturally.

The **native decision** is the oracle for predicate equivalence. The replay must use the captured operands without calibrating the calculation to the same native decision. Define a method for distinguishing genuine, independent input/decision pairs from repetitive callbacks and for retaining counterexamples. Report valid comparison coverage by branch and unique operand configuration, not merely event count. Specify the result of zero/insufficient qualified pairs as **NOT TESTED**, not PASS.

Address whether existing offline native evidence already suffices for one or more branches without another live capture. Avoid repeating an established result merely to accrue new telemetry.

## Workstream 3 — Feasibility, safety and value decision

This is an **offline feasibility assessment only**. Determine from existing pinned instructions, project tools and prior observer qualification whether an observation-only hook at the proposed site could capture all essential operands **and** its corresponding result safely and unambiguously. Check:

- Instruction/ABI integrity, live object validity, region-array traversal safety, recursion/nesting and lifetime rules.
- Effects on timing, threading, high-frequency callbacks, event transport, overflow handling and STOP retirement.
- Whether complete variable-length geometry can be captured without unsafe synchronous allocation, file I/O or waiting locks inside a native callback.
- Whether the proposed site can report both accepted and rejected candidates, rather than only successful downstream results.
- Whether its native decision is available without reconstructing it from downstream effects.
- Whether prior 0.8.0 infrastructure is useful or should remain historical; there is **no requirement to reuse or rehabilitate** the rejected experiment.

Define an evidence threshold for worthwhileness **before** recommending a build: if every planned event were captured perfectly, which substantial unresolved assertion could be supported, contradicted or bounded? What would remain unknown? Account for engineering complexity and operator burden. Reject an experiment that can only record partial headers, unions, refresh flags or source visits and cannot support true independent spatial comparisons.

Do not invent arbitrary runtime duration, event-count or data-volume quotas. Safety-capacity bounds are distinct from scientific stopping rules; a future run should preserve partial evidence and record overload as an integrity failure. If further live work is recommended, reference shared phase-aware preflight/ACK/STOP/postflight and lossless verified archival infrastructure, but **do not operate it in this task**.

## Mandatory disposition

End with exactly one recommendation:

- **GO:** An observation-only capture has a sufficiently qualified native boundary, an explicit complete paired-operand/decision contract, plausible branch coverage and a material scientific payoff. Provide the bounded proposed experiment and its limitations.
- **REVISE:** A potentially valuable test exists but requires a specifically described prior offline fact or smaller alternative design to establish feasibility. Identify the **minimum** prerequisite investigation; no open-ended reverse-engineering campaign.
- **NO-GO:** Complete independent native comparisons cannot be credibly obtained with justified cost/risk from the known boundaries. Document the blocking reason and what evidence would warrant reconsideration.

Neither GO nor any particular scientific outcome is preferred. **Do not engineer an experiment to justify past sunk costs.** Independent review must challenge whether *perfect execution* would settle an important unanswered question, as well as the accuracy of the proposed native boundaries.

## Deliverables

In an appropriately scoped `docs/experiments/` location, produce:

1. A concise **feasibility report** stating the verdict and its reasoning, linked to pinned native evidence.
2. A **native boundary and operand inventory**, with field-by-field availability and provenance and RVA/build references.
3. A **branch coverage and comparison matrix**, specifying valid comparisons, limitations and counterexample handling.
4. A **scientific-value and risk assessment** describing what the result would prove or fail to prove, including whether to abstain from a live experiment.
5. A **short independent review** with reviewer objections, rework and final disposition; primary investigator plus at most one specialist and one independent reviewer, maximum two active sub-agents, consistent with `WORKFLOW.md`.
6. Review artifacts: task-only and complete textual diffs (include new/untracked text), test/verification receipts, preservation status, and an appropriate suggested Conventional Commit subject. Do not stage, commit or push.

Carry over existing spatial implementation and research documents only when necessary for accurate references or bounded corrections. Maintain readable Markdown prose: audit changed documentation for fused words, missing spaces around numeric labels, RVAs, version strings and inline code, and have the independent reviewer explicitly check prose quality. Avoid broad repository-wide rewriting.

## Non-authorizations and deferred work

**Do not** write or change SFSE/DLL native instrumentation, create a Vortex package, rebuild 0.8.0, deploy, launch Starfield, invoke native functions, change saves, alter protected evidence, or conduct any live test. Do not expand into remote outpost support, cache completeness or generation-readiness research, or mod-specific implementation recipes.

**Experiment B is explicitly deferred.** Preserve as contextual motivation, not a workstream: the player has observed temporary disappearance of veins at mature outposts (including a Vytinium/Helium-3 site in the Decaran system and a Gold/Antimony case in the Feynman system) while already installed extractors continued producing. A later, separately authorized investigation could examine resource-geometry caches, placement validation and persistent extractor associations. The present task must not investigate or instrument that behavior.

**Success is a rigorous, actionable feasibility decision—not a live observer.**
