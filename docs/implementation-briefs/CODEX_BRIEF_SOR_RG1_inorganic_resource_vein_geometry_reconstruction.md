# Codex research brief — RG1: inorganic resource vein geometry reconstruction

**Project:** `D:\Projects\starfield-outpost-research`  
**Type:** bounded offline scientific reconstruction and original evaluator, with prior-art and permissions review  
**Research baseline:** Starfield executable **1.16.244.0**, using the pinned installed definitions and existing provenance; historical saves may originate under older builds  
**Authority:** this maintainer-approved brief authorizes the specific offline research, original helper/evaluator development and durable documentation described here. **No live Starfield, debugger/process attachment, SFSE deployment, save modification, executable/installed-data mutation, evidence publication, staging, commit or push.** B6 release verification remains on hold.

## 1. Research question and success boundary

Recover the *actual inorganic resource vein/region geometry* around an ordinary player-built outpost beacon, starting with its nominal **150-native-unit radius**, not merely the list of resource types that could occur on the planet or in its biome. Determine the underlying game representation and generation mechanism rather than assuming an overlay texture. A separately generated mask, cached raster, region graph, procedural contours, point sets or combinations are competing hypotheses, not prescribed solutions.

The objective is an evidence-grounded explanation and sufficiently reconstructive **original offline evaluator** to identify spatial membership and which resource geometries overlap the nominal territory. Include just enough of the surrounding generation area and source dependencies to identify veins entering the footprint from outside. The outpost's **effective POI-clipped buildable territory** is secondary and must not obstruct completion of a qualified nominal-territory model.

A vein's geometric presence must remain distinct from: a planet-wide resource catalogue; BIOM/RSGD/RSCS eligibility; atmospheric resources and water; the prospective UI's aggregated resources; an extractor's construction admission or skip-vein bypass; and what is currently being produced or stored. State which result each reconstructed path actually answers. Do not scope findings to any particular app/mod implementation.

**Sufficiency test:** a coherent source/context-to-region generation model which predicts resource membership at independently chosen positive and negative spatial points and supports a justified region-versus-circle intersection decision, with clearly stated coordinate/frame, resolution, boundary and coverage limits. Do not demand rendering fidelity or native instruction-for-instruction equivalence where an original faithful spatial model suffices. Conversely, agreement with one already aggregated resource list is not proof of geometry reconstruction.

## 2. Mandatory starting review — existing work and prior art

Read and reconcile, without repeating completed investigations:

- `docs/experiments/native-availability-map/` — particularly `region-dependencies.md`, `region-lifecycle.md`, `region-requirements.md`, `region-uncertainty.md`, `output-paths.md`, `output-contract.md`, functions/source pins/reviews.
- `docs/experiments/resource-availability/` and associated schema, native/preview/save and validation records; `save-analysis/scripts/resource_spatial.py` where relevant.
- `docs/experiments/outpost-biomes/` (qualified nominal biome coverage), `docs/experiments/coordinate-sufficiency/` (terrain chart/cell and local offset), `docs/position-model/`, L3 spatial placement, previous PNDT/BIOM/RSGD/RSCS and resource-family work.
- Relevant B0–B5 publication/provenance/permission policies, `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, the completion-contract template, and the standing prior-art/third-party rules.

Begin with a **documented prior-art pass** across relevant public research, Creation Kit/modding documentation and applicable external implementations, including the possibility of planetary overlay masks or resource maps. Verify whether any candidate actually represents **inorganic vein geometry**, rather than biome maps, POI overlays, cosmetic resource textures or terrain masks. Record exact URLs, authors, versions, dates, evidence type, findings and differences from project-original work. The user has not authorized incorporation of third-party source merely by requesting a search.

**Permissions/attribution gate:** before copying, adapting, executing as a dependency or incorporating any third-party implementation, dataset or substantial text, establish its actual license/permissions and attribution conditions according to project policy; record approval or obtain the required maintainer authorization when not covered. Prefer independent original reconstruction using lawful installed inputs. If permission is absent or unclear, do not incorporate the material; cite its public claims and continue independent work. Never copy game binaries, proprietary asset dumps, bulk decompilation or disassembly into tracked outputs. Short bounded analytical assembly/pseudocode with provenance follows established publication policy. Identify source-reported claims separately from independently verified results.

## 3. Native geometry mechanism and dependencies

Starting from the already mapped *consumer* of resource-region geometry, trace upstream only as far as needed to recreate the spatial population and evaluation:

1. Producer/source selection by planet, worldspace, biome/resource definitions and spatial source index; source ordering and eligibility.
2. Generation of each resource's geometry: seed/PRNG and advancement, weights/chance, candidate order, source frames, translations/scales, grid or raster resolutions, contour/point/shape representation, resource priority, previous accepted geometry and exclusion/overlap behaviour.
3. Manager-owned source/resource maps and caches: who creates them, when they are valid, and how their contents relate to a requested location and evaluation epoch. Distinguish immutable world inputs from loaded/transient bookkeeping.
4. Native geometric predicates used for point membership, overlap or area availability, and the separate UI/resource aggregation path. Follow data producers and consumers with exact source/definition pins and scoped address domains.
5. Determine whether the related raster path is equivalent to, derivative of, or different from the source/resource regions. Avoid substituting an easier raster that has not been proven to answer the same geometry question.

Record a compact causal call/dataflow and original, explanatory pseudocode. If procedural generation needs limited terrain-generation components, reconstruct them. Do not expand into vegetation, POI placement, graphics, full surface rendering, unrelated physics, or arbitrary terrain simulation merely because they share a code path.

## 4. Offline evaluator and outpost-territory intersection

Implement the smallest original, inspectable offline model that can accept the qualified planetary/source definitions and **beacon geographic-cell plus local-frame position** and determine inorganic resource region membership in a finite neighborhood. Retain explicit contracts for inputs, transforms, resolution, source version, mutable seed/state and failure/unknown outcomes. Avoid calibrating arbitrary constants to individual target outposts.

For the nominal footprint, give an explicit overlap algorithm that can detect small intersecting slivers and a region entirely contained inside the circle. Define treatment of tangent-only contact (zero area), quantized/raster edges, floating point tolerance and uncertain boundaries. If native representation cannot support exact geometric intersection without further operands, report a conservative sound bound or qualified approximation, not unsupported completeness.

Output should include at least: source IDs/resource identities, representation and spatial frame, provenance, generated geometry or sufficient deterministic representation, point-membership outcomes, footprint intersections, and diagnostic limits. Keep evaluator scope scientific: not a production save importer, mod, full generalized API, or public release package. Newly authored source/build/test files may be tracked when safe and useful under the standing source-first policy; generated proprietary extracts remain local-only.

## 5. Evidence and independent validation

Select contrasting sites and controls using **existing** outpost saves and existing research inputs first. Relevant candidates include the qualified Kreet Save37–39 outpost, Kreet L3 controls and selected mature multi-resource outposts, but do not infer available vein geometry from outpost names, extracted production or biome names. Verify each instance's identity, input version and spatial frame rather than fitting to its label. Search existing captured native source-region evidence for original point/region geometry before requesting additional acquisition.

Require independent positive **and** negative spatial tests; choose held-out locations, resource identities and/or frame boundaries that discriminate competing models. Report which comparisons use: (a) exact native captured region/point evidence; (b) qualified installed definitions and independent model checks; (c) save-position correspondence; (d) screen observations that only show aggregate membership. Explicitly identify lack of a native spatial oracle if applicable. Test a nontrivial boundary/intersection and at least one independent site when evidence permits. Preserve failed hypotheses, falsifying cases and acquisition problems.

Offline reconstruction is authorized; **new live observer or save acquisition is not**. If a decisive causal test requires fresh native runtime geometry, identify the smallest specific live action, capture operands and expected discrimination in a proposed separately approved run card. Continue all other authorized analysis. Do not claim independent runtime agreement without measurement, and do not close a mandatory reconstruction target merely because a hypothetical unobserved alternative cannot be exhaustively eliminated. Use the project's reasonable scoped-confidence standard.

## 6. Deliverables

Create a cohesive experiment record in a new appropriate `docs/experiments/` subdirectory, with discoverable links from the current roadmap/register/backlog as appropriate. Include:

- Answer-first `report.md` with strong supported conclusions, actual limitations and next decision.
- Prior-art and permissions/attribution ledger; source-reported versus project-original distinction.
- Native provider/representation/dependency map, function and definition pins, and analytical pseudocode.
- Evaluator contract, source and bounded synthetic/actual-input tests; no proprietary copied inputs in tracked tree.
- Explicit nominal outpost circle intersection/completeness reasoning and any secondary clipped-territory qualification.
- Evidence/validation ledger with positive, negative, held-out and counterexample results; separate STATIC/SAVE/RUNTIME basis.
- `review.md` with original criterion matrix, test receipts, primary evidence, unresolved items and independent decision.
- Complete and task-only diffs, inventories (tracked modified/untracked/ignored/excluded), byte-exact forward/reverse reconstruction and protected-input/HEAD/index checks.

Keep historical reports and native source pins unchanged. The user's incidental observation about inconsistent hexadecimal offset notation and possibly malformed prose in `region-dependencies.md` is a **separate release-readiness follow-up**: record a concise lead for the future B6/prepublication quality pass, but **do not edit that historical report as part of RG1** unless a specific correction is indispensable to avoid a false RG1 finding and separately approved.

## 7. Frozen compact completion contract — AC1–AC8

**Task:** scientific reconstruction with bounded original offline engineering; no game/deployment/publication authority.

**AC1 — Authority, input and source provenance.** Confirm baseline, permissions, untouched game/save/native original inputs, guarded disk/worker integrity and actual Git baseline. Document allowed actions and initial state.

**AC2 — Prior art and permission gate.** Produce a scoped source/claims ledger, test relevance of overlay/raster alternatives, distinguish attribution and third-party reuse rights, and use no unapproved third-party material.

**AC3 — Causal resource-region geometry model.** Recover a positive, source-pinned ordinary upstream generation/data representation account beyond the known final resource-list consumer; include materially relevant ordering, frames, dependencies and cache lifecycle, with no fabricated operands.

**AC4 — Original evaluator.** Supply reproducible source/contracts and passing tests for the qualified geometry and point-membership path or, if genuinely blocked by missing authority/input, document the actual tested paths and precise minimal blocker for independent ESCALATE. A merely descriptive call map alone is not a PASS for AC4.

**AC5 — Nominal territory intersections.** Demonstrate a justified geometry-versus-150-unit-circle inclusion method, including partial and contained regions, with explicit boundary/error rules; qualify completeness according to representation and supported contexts.

**AC6 — Independent controls and falsification.** Execute meaningful independent spatial positive/negative checks and a held-out or contrasting case when available; distinguish test oracle quality; preserve contradictions and do not pass off predicted results or aggregate UI lists as independent native geometry.

**AC7 — Scientific and documentary quality.** Deliver the concise answer-first report, source/version/evidence registers, valid analytical pseudocode, test documentation, scope/coverage/unknowns, and clearly separated downstream resource/biome/UI/production semantics. Do not alter established findings or publication classifications without approval.

**AC8 — Independent critical review and reproducible delivery.** Obtain fresh reviewer ACCEPT on AC1–AC8 and exact final revision, correct REWORK within this assignment, preserve failure history, verify complete/task-only patches forward and reverse, links/prose/notational integrity, baseline hashes and no unauthorized mutations. Reviewer ACCEPT does not grant publication/commit approval.

**Negative research closure:** Scoped negative claims require bounded, concrete tested counterexamples and competing-path coverage, not absence of search hits. **Continuation:** resolve in-scope technical faults and rerun checks without requiring another brief; hold the affected action if authorization, disk integrity, source rights or genuinely unavailable critical input prevents progress. **Escalation:** give exact blocked criterion, attempts, evidence and narrow required permission or operator action. Do not automatically declare success on an approximate substitute that fails the agreed geometry objective. No artificial test-count, clock-time or healthy-run volume stop; obey existing protected-input, free-space and safety guards.

## 8. Final handoff

Return the principal geometric findings and limits, the evidence supporting native correspondence, artifacts and test results, each frozen criterion's PASS/FAIL/NOT TESTED result, independently recorded ACCEPT/REWORK/ESCALATE, complete/task-only patch paths, protection/status inventories and a proposed commit message. **Nothing staged, committed, pushed, uploaded or made public.** No B6 action; release process remains paused pending this investigation and subsequent scope-specific documentation/evidence review.
