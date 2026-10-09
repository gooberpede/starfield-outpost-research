# Codex research brief — Exact Beacon Planetary Coordinates and Terrain-Frame Transformation

## Mission

Determine **how Starfield relates a saved outpost beacon's local position to its planetary position**. Recover either the actual engine transformation or an independently reproducible, numerically equivalent method for computing the beacon's global surface coordinates from saved information and the relevant game definitions.

This is the principal question. Do not confuse the **site/overlay anchor** with the **individual beacon's position**, and do not assume they are identical. Investigation of terrain grids, tiling, origin, scale, rotation, mirroring or planetary projection is explicitly authorized **as deeply as necessary to answer this question**. The investigator should decide when promising branches merit further work; do not stop merely because a branch looks complex or crosses subsystem boundaries.

The intent is not an indiscriminate reconstruction of all terrain procedural generation. If understanding a substantial portion of terrain-frame implementation is the price of establishing the coordinate transformation, **pursue it**. Record why each deeper line of inquiry serves the central objective and stop only when it ceases to have plausible bearing on it, is superseded by stronger evidence, or encounters a specific, documented blocker.

## Established research baseline

Consult the repository's **current committed research records and primary evidence** before interpreting or modifying anything. Relevant established scoped findings include:

- Ordinary player-buildable outpost beacon detection and saved disabled-state interpretation.
- Save-derived planetary body identity through beacon-related saved associations and installed ESM/PNDT identities, including the controlled Kreet case and Save52 network corroboration.
- A planetary overlay/site-anchor double pair interpreted at **STRONG** confidence, **longitude first, latitude second, in radians**; fixed New Atlantis/ESM evidence and native coordinate code support that interpretation.
- Save25's two Kreet outposts, **SOR-002 and SOR-003**, placed by walking within one traversable landing area, with **distinct site anchors** and different local beacon XYZ values; SOR-002's angular pair matches the earlier Kreet controls.
- Existing native-analysis leads involving indexed terrain coordinates, terrain-manager origin/resolution, and decomposition into grid-aligned and fractional local positions. Their complete semantics remain unresolved.

Treat these as accepted findings **within their stated coverage**, not universal facts. Reopen them only on new concrete contradictions or materially better evidence. Verify exact offsets, addresses, tuples, hashes and source references against durable records; do not rely on approximate values from earlier conversations.

## Authorized inputs and methods

Use existing verified project-local archives and manifests for:

- **Save25:** `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs`, with SOR-002 and SOR-003.
- **Save3, S1 and S1C:** pristine no-outpost baseline and first Kreet beacon controls.
- **Save52:** the mature save and its separately maintained outpost-network JSON, for independent multi-body corroboration.
- **Save2:** the player near the Lodge at New Atlantis.
- Installed **Starfield.exe / Starfield.esm and other relevant ESM records**, xEdit, Ghidra databases, installed source and existing research tooling.
- Fixed city references on Jemison, Akila and Mars, as useful.

Authorise substantial **offline** Ghidra/static analysis, xEdit/ESM inspection, code-path tracing, numerical experiments, small scripts, and comparison of archived save evidence. New live Starfield experiments, observer deployment, breakpoint tracing, or edits to original saves are **not authorised by this brief**; if truly needed, propose an exact test and its information gain for separate approval.

No staging, commit or push. Do not alter primary archived evidence or live saves. Respect the existing 40 GB free-space guard and resource/integrity safeguards without introducing arbitrary size exclusions for valid saves.

## Prior art: required critical review

Read and attribute relevant existing technical work and discussions, notably:

- https://old.reddit.com/r/Starfield/comments/1vqcjk3/found_a_perfect_example_of_starfields_tiling/
- https://old.reddit.com/r/NoSodiumStarfield/comments/1cr7w8t/obervations_on_starfields_tile_system/

The community discusses modular/repeated terrain pieces, approximate grid dimensions, rotation/mirroring and apparent **2×2 terrain components** that accommodate larger features. These are **observational hypotheses**, not engine-confirmed facts. Trace potentially useful claims to their sources and compare them against game records/code; do not adopt unsupported assertions as premises.

Distinguish at least: a modular **terrain tile/piece**, a larger traversable **landing area**, a **worldspace**, a planetary **overlay/site anchor**, a terrain coordinate **grid/index**, and an individual placed **reference**. Do not equate these merely because they are colloquially called “tiles.”

Apply `THIRD_PARTY_POLICY.md`, `docs/SOURCES.md`, `docs/PROVENANCE.md` and related permission rules. Read and cite prior work; do not incorporate third-party code/assets without appropriate permission. Maintainer-authored `gooberpede` repositories are reusable under the project's standing exception, with provenance and third-party carve-outs.

## Primary research questions

1. **Exact input identities:** Which saved fields and installed definitions specify the beacon, its site/overlay, its owning body, and the coordinate frame needed to position it?
2. **Coordinate transformation:** What functions/formulas convert a site longitude/latitude and local beacon XYZ to a body-global position, and what additional parameters are required?
3. **Frame semantics:** Where are the relevant origins? What do local X/Y/Z, elevation, axes, rotations and scaling represent? Where do terrain manager origin/resolution and indexed coordinates enter?
4. **Grid/tiling relationship:** Are indexed terrain positions the same as modular visible terrain tiles, finer subdivisions, or another layer? Are tile dimensions, footprint sizes, rotations/mirroring or varying resolution relevant to the beacon transform?
5. **Site versus beacon:** Does the saved angular pair refer to the landing area, an overlay's origin, an outpost-associated site, or another anchor? What displacement and/or snapping separates it from the beacon's exact surface coordinates?
6. **Global coordinates:** Can the method yield the engine's body-oriented lon/lat for the beacon itself? If the engine has an additional texture/geographical calibration, distinguish **engine-oriented angular coordinates** from a position measured on the orbital texture, resource overlay or external map. Do not invent a real-world-style meridian alignment.

Trace both forward from the known saved fields and backward from the native functions consuming or producing terrain positions. Follow the strongest evidence even if it requires investigating lower-level planetary coordinate infrastructure.

## Research autonomy and stopping discipline

Codex may generate and test competing hypotheses and build narrowly useful intermediate decoding/analysis tools. It is encouraged to pursue promising terrain/grid branches beyond the initial vocabulary search if they are likely to resolve the transform. **Do not use an arbitrary small exploration budget as an excuse to stop.** Avoid repeated requests for permission to pursue offline leads already within scope.

However, do not replace progress with indiscriminate code browsing. Maintain a hypothesis/evidence log recording candidate formula, prediction, test, result, counterexample and next discriminating question. Use observed return values, data flow, types, mathematical identities and cross-save constraints, rather than symbol names or rough visual fit alone.

A persuasive stop without a full solution requires a **specific, evidenced** obstacle: the exact missing variable or unavailable linkage, efforts undertaken to recover it, tested alternatives, and the smallest experiment that would resolve it. “Terrain procgen is complicated,” “more research is needed,” or “another representation might exist” are not sufficient.

## Numerical validation — no circular fitting

Use some existing examples to derive a method, and reserve independent cases for validation. Do not fit an arbitrary transform to the two Save25 points and then call those same points confirmation.

At minimum:

- Reconstruct/compare **SOR-002 and SOR-003** from Save25 without individually adjusted parameters.
- Check the nearly colocated earlier **S1/S1C** Kreet beacon against SOR-002.
- Validate generality against a subset of **Save52** outposts on different bodies, including the two Feynman V outposts if useful. The JSON is a manually authored **cross-check**, not a source of coordinates or an input to the algorithm; never derive body/location from the outpost's name.
- Use **Save2/New Atlantis** and fixed city ESM records where they provide genuinely independent coordinate-frame constraints. Distinguish fixed-site locations from actual movable player/reference position.
- Preserve the user's “roughly north” and “couple of kilometres” description for SOR-003 as contextual estimates, not calibrated truth.

Report numeric errors using the appropriate metric: serialized-value equality, angular residual in radians/degrees, distance in engine-derived surface units if a trustworthy radius/scale is available, and any uncertainty from local transforms, quantisation or float precision. Never assume Earth radius, metres per engine unit or a prime-meridian orientation without evidence. Test difficult cases (negative angles, wrapping, high latitudes and cross-body examples) wherever available.

Do not require byte-identical engine source code if an equivalent formula reproduces all relevant behavior independently.

## Secondary planetary-system leads

Preserve promising reproducible leads on:

- Modular terrain tiles, possible variable footprints and apparent 2×2 larger components.
- Terrain rotation, mirroring, coordinate indexing and resolution.
- Planetary visual/orbital texture orientation, poles and prime meridian.
- Resource-overlay placement and whether it shares the terrain or body coordinate frame.
- Terrain streaming/worldspace/landing-area ownership and elevation.

For each lead record the exact function/RVA, ESM FormID/record path, data field or external source, what was actually observed, what remains conjectural, and a focused follow-up question. If a secondary lead becomes necessary to solve the coordinate transform, promote it into the active investigation; otherwise keep it as a future lead rather than a required deliverable.

## Evidence and output standard

Follow the now-adopted methodology: distinguish **confidence, coverage and completeness**; use accepted scoped `PROVEN`, `STRONG`, `PROVISIONAL` terminology appropriately. Report the **best-supported answer first**, then decisive evidence, validated scope, concrete limitations and alternatives. A correct partial mathematical relationship is a useful finding; an exact-beacon claim requires validating the remaining terms.

Deliver:

1. **Direct answer**: an executable/reproducible procedure to calculate individual beacon planetary coordinates, or a precise bounded explanation of what still blocks one.
2. **Data-flow map** from saved beacon/local XYZ and site lon/lat through relevant records/native routines to terrain/global position.
3. **Formula/algorithm** with every parameter's source, units, frame and confidence clearly stated; tested reference implementation if justified.
4. **Validation matrix** for Save25, S1 and independent multi-body/fixed-location cases; numerical residuals and counterexamples.
5. **Grid/terrain findings**, separating verified mechanisms from Reddit/community hypotheses and defining terms carefully.
6. **Secondary lead register** for texture, resource, pole/meridian and terrain-tiling topics.
7. **Provenance/attribution**, scripts and evidence references; record new findings/hypotheses in the appropriate durable project records without overstating them or silently rewriting historical evidence.
8. **Prioritised next step** only if the primary objective remains incomplete; identify what new evidence would be decisive.
9. **Review package**: exact files changed, tests and integrity results, `git diff --check`, internal link checks, input preservation checks, task-only and complete diffs, and `git status --short`.

Do not stage, commit, push, or undertake new live experiments. Suggested commit message **only after review**:

```text
research: resolve beacon planetary coordinate transformation
```
