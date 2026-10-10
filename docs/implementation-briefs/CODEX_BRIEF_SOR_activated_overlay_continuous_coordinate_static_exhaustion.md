# Codex Research Brief — Activated-Overlay and Continuous-Coordinate Static Exhaustion

**Project:** Starfield Outpost Research (`starfield-outpost-research`)  
**Status:** Implementation/research instruction; review required  
**Mode:** Offline static analysis and existing-evidence analysis only  
**Primary objective:** Resolve the durable outpost center's continuous planetary position from save-derived state and installed game definitions—or demonstrate a precise, independently reviewable reason why the remaining relationship cannot presently be recovered by authorized static methods.

## 1. Why this follow-up exists

Continue the **existing** activated-overlay/grid-geometry investigation; do not restart it, replace its findings, or declare victory by repeating them. The previous pass made substantial progress but stopped at two unresolved joins:

1. **Selected-frame join:** How a loaded outpost/reference selects the applicable activated-overlay edge, world/cell context, rebase state and translation from saved state.
2. **Fractional-coordinate join:** How the surviving local/fractional position is transformed into a continuous planetary position, beyond the already reproduced discrete 49,152-step projection.

The reviewed research also supports the cell-center interpretation of discrete grid outputs, origin snapping, installed 2×2 subdivision footprints and related orientation transforms. These are established working results *within their documented coverage*, not questions to keep reopening without contradictory evidence.

**A further “STRONG PARTIAL” report is not an acceptable stopping rationale while promising, authorized static leads remain unexamined.** The purpose is not to force an invented answer: it is to trace the dependencies rigorously until they are resolved, falsified, or blocked by a demonstrated limitation of available offline evidence.

## 2. Scientific target and distinctions

The principal target is the **durable outpost center**, not the current movable beacon position or its build-area radius.

Use the existing findings:

- Planet/body identity is recoverable from saved associations and installed definitions.
- Planetary site/overlay anchors use longitude first, latitude second, in radians, within the tested scope.
- A reproducible 49,152-step, two-hemisphere discrete planetary projection is available; its output corresponds to cell centers in the studied path.
- The compensated workshop center is recoverable from the current beacon XYZ plus the `Workshop::ExtraData +0x60` float32 vector.
- The compensated local center remains exactly invariant across Save25 → Save26 following beacon movement.
- The compensation vector is directly represented in studied workshop serialization paths.

Distinguish explicitly:

1. planetary site/overlay anchor;
2. selected runtime terrain/activated-overlay frame;
3. durable workshop center in its applicable local frame;
4. continuous planetary position of that center;
5. optional current beacon/object transform.

Do not equate the site's pair with the precise outpost center without demonstrating the relationship. Do not impose an assumption that a native API must explicitly materialize continuous beacon/outpost latitude and longitude: an equivalent, independently reproducible transform is an acceptable complete result.

## 3. Mandatory static-lead exhaustion procedure

Create and maintain a **durable dependency ledger** for each unresolved join. Begin with leads already identified in previous reports, including relevant native addresses and source/evidence citations; verify addresses against the pinned executable before use.

Each ledger entry must identify:

- unique lead ID; dependent question; input/output values and their types;
- producing function(s), callers, callees, indirect dispatch targets, data accesses and relevant versioned addresses/offsets;
- evidence examined (disassembly/decompilation, cross-references, save records, ESM fields, existing runtime captures, numerical tests);
- competing hypotheses, predicted observations and test results;
- follow-up dependencies, including branches not yet covered;
- **disposition**: `RESOLVED`, `FALSIFIED_OR_IRRELEVANT`, or `STATICALLY_BLOCKED`, with a detailed justification.

`NOT_TRACED`, `TOO_COMPLEX`, `TIME_EXPIRED`, `UNKNOWN`, a list of functions, or “recommend live tracing” is **not** evidence of exhaustion. Such entries are unfinished work, not terminal dispositions.

Use an expanding dependency graph rather than attempting to prove that no unknown function exists anywhere in the executable. For an indirect edge, virtual dispatch, data-driven accessor, or opaque component type, make a reasoned attempt to recover relevant targets through vtables, registrations, xrefs, dataflow, type recovery or call-site constraints. Record why an edge is or is not relevant; do not quietly ignore it.

After each material finding, actively repeat **hypothesis → trace → test → revise**. Continue down useful leads within this authorized offline scope without repeatedly returning for permission. Write the report after investigating the unresolved dependencies, not merely after the first round of useful discoveries.

## 4. Track A — activated-overlay restoration, ownership and selection

Trace the complete applicable path from saved outpost/reference records to the activated-overlay translation chosen for the durable center.

At minimum address:

- How the activated-overlay component/edge is stored, reconstructed, registered and made available after load.
- The provenance of its world key, parent/cell identity, effective frame and validity/selection indicators.
- How active, requested, cached and rebased coordinates differ and which selection predicates operate on them.
- The rebase writer(s): trigger, coordinate origin, persisted versus transient components and effects on currently loaded references.
- How the workshop/reference context selects the particular translation, including cell bounds and negative-axis/grid-edge cases.
- Whether all necessary inputs are derivable from protected saves, installed data, and previously archived live evidence; if not, the exact missing value and its runtime producer.

Treat the previously identified paths (including the coordinate-pair producer, activated-overlay reader and rebase writer) as **starting points, not endpoints**. Confirm exact addresses and types from the pinned binary and follow their relevant caller/consumer chains in both directions.

## 5. Track B — continuous residual projection and grid geometry

Trace what happens after quantized grid selection to the remaining fractional local components. Establish whether the engine calculates a continuous spherical/body-oriented location, a local-to-planet transform, or a sufficient alternative representation.

Investigate as justified:

- Producers, storage locations and consumers of fractional/residual XYZ;
- the role of integer/fine/coarse grid indices, 100-unit scale and origin resolution;
- `floor`/rounding/truncation and center versus corner conventions;
- hemispheric seams, negative coordinates, longitude wrap and pole behavior;
- local-axis orientation, frame rotation/reflection, vertical contribution and terrain origin rebasing;
- the relationship between coordinate-index grids and terrain-pattern/subdivision footprints.

The project already has evidence of 1×1 and 2×2 installed terrain-pattern footprints. Explore variable/non-square footprints where actual installed data or code suggests them, but distinguish *terrain asset footprints* from *coordinate-grid cells* and *traversable landing areas*. Do not infer 3×3, 1×2 or 2×4 support merely from engineering plausibility.

Follow adjacent terrain systems as deeply as needed to close the transform. Do not create a generalized terrain generator unless that work is genuinely necessary to reconstruct the outpost-center position.

## 6. Test corpus and non-negotiable invariants

Use existing, hash-verified local evidence before proposing additional gameplay:

- Save25 and Save26, and the nine observer captures from the successful SOR-003 movement/save/reload session;
- S1/S1C and the earlier controlled Kreet samples;
- Save52 and its separate, manually authored network JSON for independent body/location cross-checks;
- Save2 at the known New Atlantis/Lodge location and installed fixed-site ESM definitions;
- relevant pinned `Starfield.exe`, Ghidra project, ESMs, xEdit exports and prior research scripts.

**Mandatory invariance test:** the same algorithm and frame assumptions must return the same durable center for SOR-003 in Save25 and Save26. It must not accidentally follow the moved beacon.

**Generality test:** use the same method on other independently identified sites, including SOR-002 and at least some other bodies, without per-outpost fitted parameters. Reserve independent examples when possible rather than using every sample to tune the model.

Report exact/float32/float64 agreement, quantization uncertainty and, where justified by sourced body scale, physical distance errors. Do not invent metres-per-unit conversions.

User-confirmed context: the 19 mature beacons considered in prior work **were not moved**. Their zero workshop-compensation vectors are compatible with that known history. Do not demand an additional proof that they never moved or restart hypothetical reset investigations without relevant contradictory evidence.

## 7. Static research authorization

Codex is authorized to:

- carry out sustained Ghidra/disassembly/decompilation/type-recovery and cross-reference investigations;
- write, adjust and run bounded offline analysis scripts and independent numerical tests;
- inspect relevant installed ESM records, xEdit outputs and current durable research documents;
- revisit hypotheses or previously inferred types when new evidence warrants it;
- investigate neighboring terrain, spatial-index, reference, component and serialization mechanisms when they can plausibly close either join;
- consult prior technical research/discussions, recording accurate links, authorship, access limitations, provenance and evidence tier;
- reuse maintainer-authored material from `gooberpede` repositories with exact provenance under the standing exception, while preserving third-party license/permission requirements for embedded material.

No arbitrary function-count, iteration-count or research-duration cap is imposed. Preserve instrument integrity and machine safety, including the 40,000,000,000-byte free-space guard for relevant volumes and avoidance of runaway output; these protections must not become arbitrary scientific-stop rules.

**Not authorized:** launch or manipulate the game, deploy or alter SFSE plugins, attach a live debugger, change protected saves, alter pinned binaries, stage/commit/push, publish protected raw evidence, or install/incorporate third-party material contrary to policy. If a live observation becomes the only credible way forward, document it as a proposed separate experiment, not an action under this brief.

## 8. What qualifies as a defensible static blocker?

A claimed `STATICALLY_BLOCKED` lead must specify:

1. the *exact* necessary unknown value, mapping or state transition;
2. the consumer that requires it and all relevant producers investigated;
3. evidence that static/serialized inputs do not uniquely determine it, or the precise inaccessible representation preventing determination;
4. alternative static paths and why they were falsified, excluded or exhausted;
5. at least two remaining viable interpretations, if ambiguity is the issue, and how they differ observationally;
6. the smallest discriminating runtime capture or new controlled sample needed to resolve them;
7. why further available static work is unlikely to distinguish those cases.

Where the fundamental issue is runtime-variable state, establish whether it changes the **durable outpost center** or only the currently active/loaded terrain frame. This distinction may itself close the question without observing every runtime path.

Absence of an identified consumer, or the fact that a code path is complex, is not by itself a blocker. Do not claim universal negative certainty from a bounded static search. Clearly delimit what was actually searched.

## 9. Required conclusions and reporting format

Lead the report with the **best-supported answer** for the durable center, followed by confidence, coverage, completeness and decisive evidence. Separate conclusions:

- exact discrete planetary-grid placement;
- exact or approximate continuous center placement;
- saved-to-loaded activated-frame selection;
- status of residual/fractional transformation;
- terrain-footprint/grid findings and secondary leads.

Retain existing `PROVEN`, `STRONG`, `PROVISIONAL` standards and independent coverage/completeness fields. Do not downgrade accepted scoped findings merely because exceptional cases remain. Conversely, do not call a promising inferred equation exact without independent validation.

Report one of two terminal outcomes:

**A. RECONSTRUCTED:** a reproducible save-derived computation of the durable center's continuous planetary position, with implementations/formulas, identities, precision/error, independent validation and documented scope.

**B. STATIC_EXHAUSTION_DEMONSTRATED:** one or both joins remain unresolved, but **every relevant entry in the investigated dependency graph has a reasoned terminal disposition**, the irreducible missing value(s) are named, and a precise discriminating live experiment is specified. This outcome cannot be claimed if the ledger still contains relevant untraced leads.

Strong partial discoveries should be reported along the way, but **“strong partial” alone is not a terminal outcome**.

## 10. Deliverables

Produce, in durable project locations consistent with existing conventions:

1. Main continuation report, with answer-first summary and explicit scope.
2. **Static dependency/exhaustion ledger**, with function addresses, evidence links, graph edges, dispositions and remaining blockers.
3. Activated-overlay registration/reconstruction/selection call-and-dataflow map.
4. Fractional-residual producer-to-consumer map and proposed or recovered coordinate transform.
5. Validated formulas/scripts and output comparisons against Save25, Save26, S1 and independent sites.
6. Grid geometry findings, clearly separating indexed positions, cell centers, subdivisions, footprints and visible terrain tiles.
7. Reproducible evidence receipts, source/provenance notes, negative cases, and any proposed future live capture.
8. Relevant scoped updates to research-state, finding/hypothesis/function/state registers and decision documentation; do not rewrite older raw evidence or retroactively inflate confidence.
9. Source changes and tests, if new offline tooling is required.

## 11. Quality and preservation checks

Before review, verify protected saves, observer evidence, relevant binaries and Ghidra content by their recorded hashes; distinguish harmless index timestamp churn from actual content changes. Ensure generated bulk/raw evidence remains ignored under `.local-work/` and no protected artifact becomes tracked. Run appropriate automated/numerical tests, `git diff --check`, internal-link validation and `git status --short`.

Do not modify any source save, deployment or game state. No staging, commit or push.

## 12. Return for critical review

Return:

- strongest current reconstruction or exact impossibility/ambiguity statement;
- all resolved, falsified and statically blocked leads with evidence;
- explicit confirmation whether any relevant static dependencies remain unexamined;
- Save25→Save26 invariance and independent-site validation results;
- frame-selection and residual-transform conclusions separately;
- terrain-grid/footprint findings and optional leads;
- any specific proposed future runtime measurement, with why static work cannot supply it;
- all files created/changed, tests/results, source hashes and limitations;
- full review diff (including new files), task-only diff if useful, and `git status --short`.

**Return for review; do not commit or push.** The present working tree is the base for a continuation, not a reason to declare the earlier static investigation complete.

Suggested commit subject *only if subsequently approved*:

```text
research: exhaust activated-overlay and continuous-coordinate static paths
```
