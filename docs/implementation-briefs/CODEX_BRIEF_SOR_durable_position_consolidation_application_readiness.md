# Codex implementation/research brief — SOR: Durable Outpost Position Model Consolidation and Application Readiness

**Assignment type:** Offline consolidation, reproducibility, documentation and narrowly necessary consistency repairs.  
**Repository:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`).  
**Starting state:** The user's latest Workshop caller-semantics investigation was committed and synced. Start from the current repository HEAD; inspect `WORKFLOW.md`, `AGENTS.md`, the Research Execution and Completion Protocol, the existing position-model implementation, frozen predictions and all pertinent evidence registers before altering anything.  
**Authorization:** Offline/read-only access to protected saves and existing evidence, and edits to project-authored research code/docs/tests within this brief. **No Starfield launch, SFSE observer development/deployment, save mutation, live process access, external debugger, stage, commit or push.**

## 1. Purpose and governing principle

Consolidate the accumulated native, save-file and manual evidence into **one coherent, executable, evidence-linked description of durable ordinary-outpost positioning**. Determine which capabilities are usable now in the Outpost Tracker and prospective Outpost Planner, and which unresolved scientific questions have no demonstrated practical consequence yet.

**Do not reopen the Z mystery or seek new native observations.** This is not another attempt to demonstrate universal native XYZ equivalence. Instead distinguish:

1. Persistent outpost placement and identity: what the saved state durably specifies.
2. Coordinate representations and frame-specific transformations: which conversions are established and where.
3. Runtime reference lifecycle and caller-specific sampling: findings, counterexamples, and unresolved interpretations.
4. Application sufficiency: the exact downstream operations that require each claim.

A physically stable outpost need not have one universally immutable numeric XYZ triple across all native contexts. Conversely, do not presume different frames explain two mismatching native triples until the actual frame transform is shown.

## 2. Evidence baseline and non-negotiable distinctions

Reconcile the latest committed sources directly; the following are context for investigation, **not substitute evidence**:

- Controlled Save25/Save26 Kreet outposts SOR-002 and SOR-003, Save27/Save28 landing variants, Save3 control, mature Save52 and the larger controlled corpus.
- Save/ESM-derived body identity, site-anchor longitude/latitude, saved terrain-frame descriptors, hierarchy, grid cell and residual positioning, beacon reference and `ExtraWorkshop +0x60` relocation compensation.
- The deterministic `durable_position_model.py` and **23 historical frozen predictions**, which must remain byte-identical.
- Native observer 0.5.0: 40 Workshop grid observations, matching captured-input horizontal replay with nonzero translations and SOR-003 hierarchy carry; native Z values differing from saved Z.
- Native observer 0.6.0: initial setters and coherent center observations matching saved XYZ for the two outposts; substantial capture but non-exhaustive writer/lifetime coverage.
- Cross-session finding: caller/path/gameplay state differ, the terrain-query callback `AD0C36` was instrumented but not observed in 0.6.0; no proven causal frame transform or observer interference.
- Native grid agreement must be described at the actual comparison grain: **two distinct Workshop geometries** and repeated calls, not dozens of independent planetary controls. Generic ship-landing-marker grid evidence is a separate, narrower result.
- Existing static native geometry-frame translation and state flags are real mechanisms, but do not retroactively prove the historical Z difference.

Preserve separate labels for **direct native observation**, **saved data**, **manual gameplay observation**, **static code inference**, **offline-derived quantity**, **conditional prediction**, and **unresolved hypothesis**. A saved site anchor is not automatically an exact beacon longitude/latitude. An observed generic grid output is not automatically a Workshop result. A returned native center is only interpretable with its frame, identity and invocation context.

## 3. Required deliverables

### A. Consolidated position-model specification

Produce a durable technical specification in `docs/` using repository conventions. Define:

- Exact supported ordinary-outpost domain and identification rules, including exceptional representations explicitly excluded.
- Input schema and provenance: body/world identity, saved site and terrain descriptors, packed source keys, hierarchy components, qualified discrete cell and local residuals, reference XYZ, relocated beacon and Workshop compensation.
- Output schema, units/frames and distinctions: persistent site identity, grid/cell/subcell placement, compensated local Workshop center, model-predicted components and unknowns.
- Relevant operations in their correct order, including reflected-axis and snapping/carry rules, float32/mixed-precision behavior where established, and handling of missing upstream site-cell inputs without guessing.
- Supported reference equality/identity semantics and ambiguity handling. Explain specifically which representation is a durable serialization input versus a transient native caller result.
- Counterexamples, branch coverage and limitations; explicit specification of which inputs are **necessary and sufficient within a demonstrated scope**, and which sufficiency claims remain unproven.

Do not collapse scientific confidence, sample coverage and product readiness into one status.

### B. Deterministic self-check and consistency corrections

Deliver a reproducible, **read-only** validation entry point (or strengthen the established one) that:

- Executes the existing position model over the frozen predictions and relevant controlled/mature corpus cases; preserves all 23 prediction inputs/expected results unchanged and reports exact-bit versus structural/semantic agreements separately.
- Validates original evidence/reference identities, checksums/provenance as currently possible, and flags missing optional inputs as explicit `UNKNOWN` rather than inventing values.
- Exercises nonzero XY translation, SOR-003 hierarchy carry, reflected-axis branches, beacon relocation invariance, ordinary cases without qualified site cell, and negative/ambiguous cases.
- Separates independent native comparisons from model-internal round trips and saved-data-derived checks; never report 23 frozen predictions as 23 independent native oracle validations.
- Produces machine-readable and concise human-readable results with commands, scope, counts and failure reasons. Use existing tooling rather than inventing a parallel model.

Correct inconsistent project-authored code or documentation **only as needed to make the consolidated claims accurate**. Preserve backward compatibility where feasible; explain any interface change. A substantive scientific algorithm change must be grounded in evidence, not tuned to match frozen answers. Keep baseline vs repaired outputs visible.

### C. Evidence/capability register

For each principal claim provide an evidence ID/path, provenance, confidence, covered saved/native cases, excluded branches, repeat/independence grain, known counterexample, and application-readiness classification. At minimum classify:

- Ordinary beacon/outpost detection, body identity, multiple-outpost disambiguation.
- Saved angular anchors and terrain-grid hierarchical/frame representation.
- Local XY/grid conversion and nonzero displacement/carry.
- Beacon-move compensation and effective local center.
- Z serialization and initial loading, differing native sampled coordinate states, frame flags and writer gaps.
- Continuous planet geographic coordinates for exact subcell positions (deferred unless actually established).
- Native equivalence claims: component, Workshop 2D, full XYZ and generality across worlds/cases, all separately.

Use **confidence × coverage × practical-readiness** as separate dimensions rather than a single `VALIDATED` flag.

### D. Tracker/Planner application matrix

Conduct a concrete application dependency audit, clearly distinguishing current Tracker workflows from future Planner features. For each feature provide required positional capability, what is currently sufficient, available fallback, and a **specific blocked operation** if any. Include outpost and planet identity, multiple outposts on the same body, structure membership, local resource/deposit placement, construction placement, proximity/overlap/boundaries and future in-game planning. Do not silently claim that positioning alone establishes authoritative Workshop membership, ore availability or build placement eligibility: those are separate research domains.

Aim to answer whether unresolved Z or exact continuous longitude/latitude **actually block an identified current or planned feature**. If none is demonstrably blocked, defer without exaggerating certainty. Do not invent final product requirements; distinguish stated user constraints from speculative features.

### E. Disposition, integration sequence, and backlog

Produce an actionable research disposition with:

- **Usable now**, **conditionally usable**, **not ready** sections, each with precise domain qualifications.
- Explicit deferral of runtime XYZ frame reconciliation, Z restoration, continuous exact lon/lat and generic ship-landing provenance except where tied to a practical dependency.
- Reopen criteria for each deferred item: a concrete feature need **and** a prospective experiment with a defined measured quantity, independent identity/frame reference, competing predictions and a falsifiable outcome. More native samples alone do not satisfy this.
- A prioritized path to practical next domains (e.g., authoritative outpost membership; resources, extractors, production, power, cargo logistics) without making this assignment implement them.
- Whether the model should be promoted into a downstream integration interface now, and which explicit constraints the interface should expose.

## 4. Agent allocation and review

Follow `WORKFLOW.md` and the Research Execution and Completion Protocol. An **independent reviewer is mandatory**, with one specialist researcher permitted when it offers a genuinely separable contribution; **maximum two concurrently active sub-agents**, excluding the primary implementer.

Preferred split: primary agent owns evidence/model reconciliation, implementation and self-checks. Specialist independently evaluates actual Tracker/Planner positional dependencies and challenges overengineering, unsupported product assumptions or missing feature needs. Reviewer checks the original contract, implementation, evidence claims and primary receipts, rejects premature completion, and returns `REWORK` within this same assignment whenever defects can be addressed under existing authority.

Record specialist-specific discoveries and their effects on the final product matrix; do not spend routine effort re-evaluating the established usefulness of the independent reviewer.

## 5. Completion contract

This assignment ends successfully only when **all five deliverables A–E** are completed and independently reviewed. Failed tests, contradictory documents, missing evidence links or uncertain source semantics are **in-scope work**, not final handoff reasons. Preserve negative controls and genuinely irreducible unknowns rather than manufacturing native equivalence.

Acceptable dispositions:

- **COMPLETE — PASS:** reproducible consolidated model, evidence/capability register, application matrix and disposition all meet the supported scope, with tests and reviewer acceptance.
- **COMPLETE — EVIDENCE-BOUND NEGATIVE:** only for a precisely investigated, independently challenged proposition that genuinely cannot be established from permitted evidence; it does **not** excuse missing deliverables or failed required tests.
- **ESCALATE:** only for a real authority/safety/access boundary, with exact requested permission and what in-scope paths were exhausted.

The final handoff must explicitly include the scientific and application conclusions, not only postflight, checksums or a package link. A reviewer `ACCEPT` does not itself authorize launch, commit or deployment.

## 6. Guardrails and worktree hygiene

- Preserve original `.sfs`, native binaries, raw captures, frozen files, references and prior research findings; read-only analysis of protected inputs.
- Preserve provenance/permission/attribution rules. No need for public web research unless materially necessary to reconcile a concrete evidence gap; if consulted, source and license it.
- Keep at least **40,000,000,000 caller-available bytes** free on **both C: and D:** for substantial local evidence work, with integrity and genuine machine-safety failures as hard stops.
- Do **not** impose arbitrary elapsed-time, observation-count or evidence-volume cutoffs. Unexpected scientific results trigger investigation and continuation, not silent termination.
- No live Starfield, SFSE plugin development/deployment, new game saves, debugger, native call injection, protected-file modification, commit or push.
- Generate review diffs under `.local-work/diffs/` with descriptive `-complete.diff` and (when applicable) `-task-only.diff` suffixes; include untracked authored text in complete patches. Supply changed-file/status/exclusion/hash manifests, exact patch validation and test receipts; exclude proprietary, raw, ignored binary and save content.
- Do not stage files to construct diffs. Keep this work separate from other repos and do not assume the repo has a clean worktree without checking.

## 7. Expected final return

Provide links to: consolidated specification, executable self-check and receipt, evidence/capability register, application-readiness matrix, disposition/backlog, independent review and acceptance matrix, and complete/task-only patches. Summarize **what is safe to use now, what is conditional, what is deferred, and the next practical research dependency**. Identify every failed or skipped required check. Suggest a commit subject, but do **not** commit or push.

**Core acceptance question:** *What do we now know sufficiently well to use, what remains uncertain, and which uncertainties genuinely matter for Outpost Tracker or Outpost Planner?*
