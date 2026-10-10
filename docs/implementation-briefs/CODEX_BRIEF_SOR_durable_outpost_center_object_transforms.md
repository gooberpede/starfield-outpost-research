# Codex Research Brief — Durable Outpost Center and Workshop-Relative Object Transforms

**Project:** `D:\Projects\starfield-outpost-research`  
**Status:** Implementation/research brief; critical review required  
**Authority:** Offline static analysis, existing-save analysis, numerical modelling, and independently authored research tooling. **No live game launch, observer deployment, save modification, staging, commit, or push.**

## 1. Central research question

Determine **how Starfield reconstructs the durable planetary position of a player-built outpost** from persistent save data and installed game definitions. The durable outpost center—not the current position of its movable beacon—is the primary target.

A successful method should produce a body identity and globally meaningful center longitude/latitude (or mathematically equivalent position), reproducibly from the save and required game definitions. Recover the engine's method or an independently validated equivalent. State numerical precision, grid quantization and unresolved calibration explicitly.

**Do not substitute the site's saved angular anchor for the exact durable center without evidence that they coincide.** Likewise do not substitute the beacon's current location for the outpost center.

## 2. Accepted starting evidence and working distinctions

Consult the committed primary reports, findings, source provenance and scripts for exact locators and supported interpretation. Starting evidence includes:

- Save-derived planetary body/system associations validated on Kreet and Save52's known network, without inferring bodies from outpost names.
- A saved pair interpreted at scoped **STRONG** confidence as **longitude first, latitude second, radians**, associated with a planetary overlay/site anchor.
- A source-informed, two-hemisphere **49,152-step planetary projection** reproducing saved site pairs and fixed-city examples within floating-point precision. This establishes the studied *discrete* projection, not the full continuous beacon transform.
- Save25's SOR-002 and SOR-003: two outposts on Kreet within one continuously traversed landing area with different site anchors, yet candidate shared terrain-grid origin.
- Save25 → Save26 and nine live observer captures: moving SOR-003's beacon changes its current local XYZ while the workshop `ExtraData` `+0x60` float32 compensation satisfies `P_original = P_current + delta`, persisting through reload.
- Native consumer and serialization evidence connecting `+0x60` to the compensated center and workshop boundary/terrain operations. The field is not necessarily immutable across every workshop lifecycle.
- The outpost radius and boundary geometry are now secondary/deferred; do not restart that investigation unless it directly resolves the coordinate frame.

Preserve the project's separate **confidence**, **coverage** and **completeness** dimensions. Treat accepted scoped findings as working knowledge unless new counterevidence demands revision.

## 3. Main workstream: reconstruct the durable-center transformation

Independently identify, recover and connect the transformations needed to map the **compensated original workshop center** in local XYZ into a globally meaningful planetary surface position.

Potential components worth examining—but **not prescribed as an implementation theory**—include:

- Selected planetary overlay/site anchor versus terrain-frame origin and the reference's occupied grid cell.
- Terrain manager, reference/worldspace/cell associations, 49,152-step projection, fine/coarse grid indices, spacing, resolution, orientation and local residuals.
- Frame rebasing and activation, cached angles, overlay/component-map paths, and code that maps a local point to a body-oriented position.
- Whether the outpost center has a separate orientation, or inherits the terrain/worldspace frame.
- Distinction between the terrain-frame site origin, durable outpost center, current beacon reference, and any actual continuous surface position calculated or reconstructed by the engine.

**Follow promising code paths as deeply as needed.** Significant terrain-grid or tiling analysis is authorized when it materially contributes to the coordinate relationship. Avoid unrelated procedural-generation work for its own sake; do not stop merely because a relevant investigation becomes complex.

Trace type provenance and callers for every interpreted field. A matching numeric offset on an unrelated native type is not a valid consumer. Distinguish directly demonstrated instructions from decompiler interpretations, inferred semantics and hypotheses. Preserve native addresses/RVAs, source hashes, function/register references, data layout and relevant call chains.

## 4. Primary invariance test — Save25 vs Save26

The outpost-center calculation must be evaluated against the deliberately moved SOR-003 beacon.

For each file, identify and correlate:

- Ordinary beacon reference identity (with save-local token remapping handled appropriately).
- Body identity and overlay/site association.
- Saved site lon/lat.
- Beacon current XYZ and rotation where available.
- Workshop `+0x60` compensation, or justified equivalent serialized representation.
- Compensated/original local workshop center.
- Relevant terrain frame/origin/grid state and continuous-position residuals.

**Required invariant:** the same durable outpost center should be calculated from Save25 and Save26 despite the changed beacon reference position, within the expected encoding/numerical precision. Report the exact deltas and errors; do not merely describe the coordinates as “matching.”

Preserve the distinction between bytes directly serialized and values reconstructed during load. Use the existing successful observer captures as independent live-context evidence, but do not require further live capture in this task.

## 5. Supporting workstream: ordinary placed-object transforms

Examine the storage, solar-array and extractor references in the controlled corpus and any well-grounded reference examples in Save52. Determine whether their positions and rotations are:

1. Stored in a common local terrain/worldspace frame, with workshop-relative offsets derivable by subtraction;
2. Stored directly relative to the workshop center;
3. Expressed through parent/attachment/snap transforms; or
4. A mixture of these representations.

Compare object identities, XYZ, raw rotations and relationship membership across known transitions (including object creation, solar movement, beacon relocation, and extractor deletion), avoiding unsupported token-identity assumptions across reload.

Investigate orientation conventions when feasible: rotation field encoding, axis order, radians/degrees, handedness, transform composition order, worldspace versus parent-relative frame, and any separate outpost/workshop origin orientation. A rotation-only transform is not automatically evidence that the outpost itself rotates.

The secondary objective should provide useful, scoped conclusions even if the durable-center geographic mapping remains open. Do not let a comprehensive rotation schema become a blocker for the primary result.

## 6. Validation strategy

Use the existing archived and verified material; do not request new gameplay controls before exhausting pertinent offline evidence:

- **Primary:** protected Save25 and Save26; nine SOR-003 move/save/reload observer snapshots.
- **Controlled references:** Save3, S1/S1C and SOR-002 from Save25; local XYZ and site anchors from prior Kreet work.
- **Generality:** selected Save52 outposts, including two on the same body with distinct locations, using the network JSON only as a cross-check, not as an input to the geographic derivation.
- **Independent fixed points:** Save2 at New Atlantis/Lodge and relevant ESM fixed-location examples (New Atlantis, Akila City, Cydonia) where the same transform actually applies.
- **Existing source:** pinned Starfield executable/Ghidra database, installed ESMs/xEdit extracts and prior coordinate-projection scripts.

Separate model-development cases from held-out validation cases where possible. Do not derive per-outpost correction constants that simply force agreement. Try negative coordinates, hemispheres, grid boundaries, two-outpost same-landing-area cases and changed-beacon/static-center cases. Quantify angular residuals, grid resolution and surface displacement **only when scale/radius is independently supported**; do not assume Earth-like geometry or a speculative game-unit-to-metre conversion.

If an exact continuous coordinate is unattainable with the present evidence, identify the **precise missing value, transformation or executable path**; demonstrate why candidate formulas cannot be distinguished; provide a concrete minimal experiment or acquisition plan that would resolve it. Do not treat a generic “terrain complexity” statement as a satisfactory blocker.

## 7. Prior art and exploratory leads

Investigate relevant published work where useful, particularly the previously identified *Celestial Positioning System — GPS for Starfield* lead and the two Reddit discussions of planetary terrain tiling and purported 2×2 larger features. Verify access and contents independently; source-reported claims remain unverified unless independently demonstrated.

Record exact author, title, URL, access date, permission/license conditions and relevance in established provenance/source records. **Do not incorporate third-party code/assets** without the project's permission process and user approval. Maintainer-authored `gooberpede` work may be reused under the standing exception with exact provenance; embedded third-party materials retain their own restrictions.

Capture promising leads on resource/texture overlay mapping, tile grid sizing, orientation, poles, prime meridian, and variable-size grid components. Follow them when useful to the main coordinate objective; otherwise preserve them as explicitly unverified follow-ups. Do not turn the task into a general atlas or procedural-terrain recreation exercise.

## 8. Research autonomy and evidence discipline

Codex has broad authority to propose and test competing hypotheses, extend offline parsers, write numerical validators, trace native consumers/constructors, and revisit previous interpretations when supported by concrete contradictions. The objective is a defensible answer, not compliance with a favored formula.

- Start each report with the best-supported answer, its **confidence**, **coverage**, and actual degree of **completeness**.
- Preserve raw observations and exact provenance; separate `OBSERVED`, `INFERRED`, and `HYPOTHESIZED` statements.
- Accept strong scoped findings without requiring a universal Starfield coordinate API.
- Do not silently promote or rewrite previously committed findings; propose justified updates with source links.
- Do not invent calibrated geographical precision, object ownership, coordinate origins or rotation semantics.
- Respect mandatory 40,000,000,000-byte free-space safeguards on relevant drives for material scratch output; avoid runaway or unbounded-error output. Large useful offline intermediate datasets are acceptable in ignored storage.
- Keep input saves and installed binaries/databases unchanged; no native save invocation or live observer deployment.

## 9. Deliverables

Produce durable reports and inspectable tooling as appropriate:

1. **Executive answer:** best-supported durable-center planetary position model; what is settled versus unresolved.
2. **Transformation map:** each stage from save fields through local/workshop/terrain/body frames to planetary coordinates, with formulae or pseudocode and exact native evidence.
3. **Save25/Save26 invariance table:** source identities, raw and derived XYZ, compensation, site anchor, computed center and numerical error.
4. **Cross-outpost validation:** SOR-002, earlier Kreet control and independently chosen Save52/fixed-location checks.
5. **Object-transform matrix:** beacon, storage, extractor, solar; translation ownership/frame and rotation encoding/status.
6. **Frame/orientation assessment:** whether the outpost has a separate transform/orientation and what evidence supports it.
7. **Uncertainties/counterexamples:** concrete competing models and evidence that discriminates them.
8. **Prior-art/secondary leads:** attribution, permissions and clearly labeled unverified hypotheses.
9. **Next step:** only the smallest targeted live observation or other work genuinely necessary after substantial offline investigation.
10. **Changed files, verification/tests, complete diff and `git status --short`.**

A complete result is a reproducible save-derived durable-center planetary position that remains invariant across beacon movement and generalizes without per-sample fitted corrections. A strong partial result identifies the exact missing runtime/terrain parameter and demonstrates a meaningful invariance or transform relationship. Do not withhold independently supported object-transform findings while a different stage remains unresolved.

## 10. Completion and review gate

Run numerical and synthetic tests, validate documentation links, run `git diff --check`, ensure input hashes unchanged and verify no raw saves, dumps or bulk memory evidence are tracked. Retain large derived data and analysis scratch under ignored `.local-work/` paths. No staging, commit or push.

Return all findings and the complete change set for critical review. **Any new live-game experiment, SFSE observer deployment, in-process instrumentation or debugger attachment requires separate authorization.**

Suggested commit message *only after review*:

```text
research: investigate durable outpost center and object transforms
```
