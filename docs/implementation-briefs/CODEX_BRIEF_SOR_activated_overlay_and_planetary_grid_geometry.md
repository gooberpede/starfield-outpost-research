# Codex Research Brief — Activated Overlay Restoration and Planetary Grid Geometry

**Project:** Starfield Outpost Research (`D:\Projects\starfield-outpost-research`)  
**Type:** Offline research / static analysis / bounded supporting tooling  
**Status:** Implementation and research authorized; findings require critical review  
**Primary objective:** Recover a reproducible, save-derived planetary position for the **durable outpost center**, not the movable beacon object.

## 1. Scientific objective and freedom of investigation

Determine how Starfield combines a saved planetary site anchor, a loaded/activated terrain frame, and the durable local workshop center to locate an outpost on its planet or moon. Resolve the relevant native and serialized mechanisms rather than settling for a numerically attractive fit.

You are authorized to follow promising code paths substantially beyond the immediately identified functions, including terrain-grid indexing, overlay activation, worldspace/cell association, coordinate conversion, and terrain-component layout. **Do not abandon a fruitful lead simply because it grows complex.** Conversely, do not attempt a full reconstruction of planetary procedural generation unless doing so is demonstrably necessary to answer the coordinate question.

The work should produce the strongest evidence-supported answer possible. A scoped strong conclusion must not be withheld because unrelated engine cases remain unexplored. If the transformation remains incomplete, identify exact missing variables, their producers/consumers, what was tested, and the most decisive next step; do not merely list general uncertainties.

## 2. Established evidence to build upon

Consult the committed research records and exact underlying evidence before starting. In particular:

- Planet/body identity has been resolved through saved references and installed ESM/PNDT data in the supported corpus, including S1 on Kreet and 17 Save52 outposts cross-checked against the network JSON. **Never derive body identity from an outpost's name.**
- Saved planetary site/overlay pairs are strongly interpreted as **longitude first, latitude second, in radians**. They describe site/overlay anchors, not necessarily exact beacon or workshop-center positions.
- The native planetary projection uses a **49,152-step** discrete coordinate scheme in the studied path; numerical reproduction of the saved angular pairs has been demonstrated. A `100`-unit fine-step relationship and other coarse/subdivision/origin parameters have been observed in particular paths. Do not assume these correspond directly to metres or visually recognizable terrain tiles.
- Save25 has two ordinary Kreet outposts, **SOR-002** and **SOR-003**, within a player-reported continuously traversable landing area, but with distinct angular anchors. SOR-002's angular pair matches the earlier Kreet S1 control.
- The loaded terrain origin `(10464, 21120)` and grid resolution `256` were observed in all nine archived live-observer snapshots from the Save25/Save26 investigation.
- Workshop `ExtraData` type `0xBC`, vector at `+0x60`, and its native consumers have been traced: within the tested relocation, `float32(current beacon XYZ + workshop compensation) = original durable workshop center XYZ` bit-identically across Save25/Save26. The vector's scoped direct save/load serialization is supported; the boundary/terrain system consumes the compensated center.
- **User-confirmed gameplay history:** The 19 mature Save52 beacon candidates were *not moved*. Their zero compensation vectors agree with that history. Do not reopen speculative reset/deletion scenarios for those particular beacons without new contradictory evidence.
- The previous offline investigation identified candidate activated-overlay translation fields and predicates, including studied payload offsets `+0x08`, `+0x0C`, `+0x30`, `+0x35`. These assignments are typed/path-scoped, not universal offset labels.

The ordinary outpost border/radius question is secondary and already separately studied. Do not let it displace the planetary-position objective.

## 3. Track A — Activated-overlay restoration and frame selection

Work from concrete saved outpost references and the identified native component type. Trace the full chain as needed:

1. How and where the relevant activated-overlay/component state is serialized, restored, initialized, registered, selected, invalidated and possibly rebased.
2. Which worldspace/cell/body/reference identities and bounding conditions govern the selection of a frame for a given workshop center.
3. How integer shifts, vertical translations, activation flags, cached pairs and terrain-manager origin/resolution participate in the transformation.
4. How a reference's saved local XYZ and the compensated **durable workshop center** are interpreted in the selected frame.
5. How the selected frame feeds the planetary grid/angle projection and, if present, a continuous subcell-position calculation.

Distinguish save-resident state from ESM-defined constants, runtime reconstructed state, and active-terrain-manager state. Find concrete native read/write/call sites, with executable version, function/RVA, meaningful pseudocode or instruction evidence and limitations. Avoid treating a coincidental `+offset` access on an unrelated C++ type as proof.

If there are multiple legitimate execution paths, identify their selection predicates and state the tested coverage rather than insisting one universal path must be found before reporting any useful result.

## 4. Track B — Grid geometry, hierarchy and tile topology

Investigate the geometry of the **recovered coordinate grid**, independently of community labels for visible terrain tiles.

At minimum attempt to determine:

- What the `49,152` steps count: axis extent, hemisphere/domain extent, points, cells, or another index range. Establish bounds, seams, hemisphere transitions, pole behavior and periodic/wrap behavior from code where possible.
- Whether a saved angle pair denotes a **cell corner, cell center, lattice point, snapped site origin or other designated reference point**. Inspect indexing/rounding, half-cell offsets, forward/inverse transforms and consumers of the resulting indices. Do not infer “corner” from `floor` alone.
- Relationships among fine indices, coarse indices, observed 96-step origin spacing, 16 subdivisions, 100 local units/fine step in the studied path, and terrain resolution. Distinguish dimensional units and source-specific constants.
- How a traversable landing area, activated overlay, terrain-coordinate cell and visually recognizable procedural terrain tile relate; do **not** assume these are synonymous.
- Whether terrain components can occupy multi-cell footprints. Follow concrete data or code supporting possible **2×2, 3×3, 1×2, 2×4**, rotated/mirrored or variable-span layouts, if a promising lead emerges. Record actual permitted dimensions and their controlling records/functions where recoverable, not merely conjectured possibilities.

A definitive map of all procgen tile assets is **not required**. A robust geometrical interpretation of the coordinate lattice, sufficient for durable outpost positioning, **is** central to the task. Do not impose arbitrary function-count or investigation-depth quotas.

## 5. Prior art and attribution

Review prior project source records and, where accessible, the two community discussions supplied by the user:

- https://old.reddit.com/r/Starfield/comments/1vqcjk3/found_a_perfect_example_of_starfields_tiling/
- https://old.reddit.com/r/NoSodiumStarfield/comments/1cr7w8t/obervations_on_starfields_tile_system/

The second includes observational claims of larger 2×2-looking terrain components. Treat all community size, tiling, rotation/mirroring, and grid-layout assertions as **observational leads**, not verified engine specifications. Do not infer that 49,152 fine steps correspond to an estimated 8×8 array of visible terrain tiles.

If the threads are inaccessible, document the attempted retrieval and existing attributed summary, then proceed: **lack of Reddit access is not a scientific blocker**. Consult other technical work where relevant and maintain the usual `SOURCES`, `PROVENANCE`, `PERMISSIONS`, `CREDITS` and third-party code restrictions. Maintainer-authored `gooberpede` project material may be reused with traceable provenance under the established exception; embedded third-party material keeps its own restrictions. Do not incorporate outside code without the required permission decision.

## 6. Validation against existing independent cases

Use the pinned game executable, Ghidra database and installed ESMs, existing offline readers, and **verified local archives only**. Primary cases:

- Save25 and Save26 — SOR-003 before/after beacon relocation; the **durable center must be invariant** under the candidate transform. Include SOR-002 as a same-landing-area comparison with a distinct site anchor.
- All nine existing live observer captures, especially captured terrain origins, local reference transforms and workshop `+0x60`.
- S1/S1C — independent Kreet origin near SOR-002.
- Save52 — 17 independently documented mature outposts on multiple bodies, with zero relocation compensation for the 19 studied beacons as confirmed by the user.
- Save2 / New Atlantis and fixed ESM sites (Akila City, Cydonia) where they provide meaningful geometry or orientation cross-checks.

Avoid fitting parameters independently to each validation target. Identify development and held-out cases explicitly. Compare predicted indices, site angles, continuous coordinates where recoverable, and save/runtime center invariants; report floating-point error, grid/subcell precision and any meaningful surface-distance error **only when physical-unit conversion is grounded**.

Use the manually maintained Save52 network JSON as an independent body/system cross-check, **not** as a source for positional formulas or an unquestioned truth oracle. Names may align records for comparison but must never be location evidence by themselves.

## 7. Persistent outpost center and object-frame distinction

Keep separate throughout:

1. Body identity;
2. Saved angular site/overlay anchor;
3. Activated terrain-frame origin and orientation;
4. Durable workshop center in local coordinates;
5. Current movable beacon reference transform;
6. Other placed-object transforms and rotations;
7. Derived global continuous surface position, if obtainable.

The goal is a save-derived position for item 4. Do not substitute the current beacon position as the outpost's durable center. The already established `+0x60` compensation may be applied within the supported lifecycle.

Where straightforward, characterize how storage/extractor/solar reference transforms and rotations relate to the same selected terrain frame, but do not allow unrelated placement features to eclipse the main transformation.

## 8. Hypothesis-driven research and stopping discipline

Codex has broad discretion to propose, discard and test models. Work toward falsifiable predictions, particularly across Save25/Save26 invariance and SOR-002/SOR-003 differences. Record counterexamples, including cases where a tempting offset/grid alignment fails.

Do not stop because an expected field is absent, one branch is unfamiliar, a grid arrangement is surprising, or an initial interpretation fails. Pursue productive alternate branches. Conversely, do not continue decoding unrelated terrain assets once the coordinate relationship is resolved or the remaining obstacle is convincingly localized.

**Acceptable outcomes:**

- **Complete:** a reproducible save-derived or equivalently reconstructed planetary coordinate for the durable outpost center, validated across independent cases, with clear units and resolution;
- **Strong partial:** a demonstrated transformation with one or more concrete missing component(s), producer/consumer path(s), and an actionable next test;
- **Negative/alternative:** evidence that the engine does not define a unique continuous outpost-center lon/lat in the assumed way, along with the most useful durable alternative location representation.

A bare catalogue of unknowns or “more engine work needed” is not an acceptable final conclusion. Lead with the best-supported answer and distinguish evidential confidence, coverage and completeness under the recently adopted methodology.

## 9. Research execution and safety

This brief authorizes **offline static analysis, read-only save/ESM examination, Ghidra research and new offline numerical/tests/scripts**. It does **not** authorize a new Starfield launch, live debugger attachment, SFSE observer deployment, save mutation, gameplay changes, or native save invocation. If a live observation is genuinely necessary, specify the precise missing value and propose the smallest high-information experiment for separate authorization.

Respect protected save/source/database hashes. Keep raw save, memory and binary evidence in ignored `.local-work/` locations. Maintain the existing **40,000,000,000-byte free-space guard on relevant C: and D:** volumes for substantial output; avoid accidental uncontrolled writers. Do not impose tiny arbitrary investigative limits.

Do not stage, commit or push. Do not silently edit committed prior findings to make them agree with a new hypothesis; introduce properly scoped new records or explicit correction notes with provenance.

## 10. Required durable deliverables

1. **Answer-first research report**: best-supported durable-center planetary-position model; confidence, coverage and remaining completeness gaps.
2. **Activated-overlay reconstruction map**: native and serialized components, ownership, selection branches, offsets, writers/readers/consumers and direct evidence for each link.
3. **Grid geometry report**: the meaning and arrangement of discrete indices, origins, seams and fine/coarse hierarchy, with distinct judgments on corner/center/reference-point hypotheses.
4. **Existing-case validation**: Save25/Save26 invariance, SOR-002/SOR-003, independent Kreet and multi-body tests, numerical errors and counterexamples.
5. **Tiling lead register**: concrete engine/ESM evidence for larger or non-square footprints if found, plus clearly attributed community observations and unresolved alternatives.
6. **Reproducible research tooling/tests** where helpful, with documented invocations and provenance.
7. Updated appropriate findings, hypotheses, state/function registers and `RESEARCH_STATE.md` **only where supported**; preserve original evidence.
8. **Next-step recommendation** conditional on the result, specifying any missing runtime measurement rather than proposing another broad investigation by default.

Validation: tests appropriate to changed tooling; source and evidence hashes; `git diff --check`; internal Markdown links; no newly tracked raw artifacts; `git status --short`.

Return exact changed files, validation results, a task-only diff where practical, full diff (including new files), and Git status for critical review. **No commit or push.**

**Suggested commit message after approval:**

```text
research: trace activated overlays and planetary grid geometry
```
