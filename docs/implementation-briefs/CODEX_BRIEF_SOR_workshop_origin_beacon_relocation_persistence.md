# Codex Research Brief — SOR: Workshop Origin, Beacon Relocation, Persistence and Radius

## Objective and authority

Investigate the live-observed `ExtraWorkshop`-associated float32 triple at **workshop `+0x60`**, determine its producer(s), consumer(s), persistence mechanism and relationship to the outpost's original center. Complement the native analysis with a controlled **Save25 → Save26** differential study. Maintain a direct line of inquiry into exact beacon planetary placement where the evidence warrants it.

**Additional authorized line of inquiry:** determine whether the outpost's buildable radius or boundary is encoded in game data, native constants, workshop state, or save data; establish its magnitude in native coordinate units and, if independently supportable, in physical metres. The user's estimate of roughly **100 metres is a hypothesis, not a calibration value**.

This is an **offline research task**. Broad exploration of promising relevant call chains and speculative tests is authorized. Do not terminate useful research because it expands into adjacent workshop, bounds, terrain or spatial systems. Prioritize demonstrable findings over arbitrary time/function-count limits; distinguish exploratory leads from validated conclusions. Do not launch Starfield, deploy a plugin, attach a live debugger, alter existing saves, stage, commit or push. If live evidence would be decisive, propose a separate experiment with exact questions and required observations.

## Research inputs

Use and verify existing durable sources rather than transcribing approximations from this brief:

- `Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs` and **the newly generated Save26**, from their archived and hash-verified project-local copies. Locate Save26 by the prior live-session manifest and verified filename/hash, not by a loose glob.
- The nine verified snapshots and raw sections from the broad-capture **SorBeaconObserver 0.1.0** live run, its journal, manifests and audit `docs/audits/beacon-observer-initial-live-results.md`.
- Earlier S1/S1C, Save25 and related controlled corpus evidence when it provides a useful independent test.
- The pinned Starfield 1.16.244.0 executable, the existing Ghidra database, installed ESMs and existing offline save-analysis tools.
- Related research on surface-anchor longitude/latitude, the 49,152-step projection, terrain frame and indexed coordinate conversions.
- Maintainer-authored `gooberpede` tooling (including `starfield-reference-handles`) as useful, with exact reuse provenance; embedded third-party material retains its own licence/permission requirements.

Preserve prior raw evidence, executable/ESM/Ghidra database hashes, and game saves unchanged. New scratch artifacts belong in ignored `.local-work/`; no raw dumps/saves or large decoded buffers in Git.

## Starting observation — reproduce it first

The observer found a three-float tuple at workshop `+0x60` that was zero before moving the SOR-003 beacon and afterward equaled **original beacon XYZ minus current beacon XYZ**. Adding the post-move tuple to the current XYZ recovered the original XYZ at the observed float32 precision. The tuple was observed again after the manual save/reload, while the runtime workshop pointer was reacquired. SOR-002 served as an unchanged comparison. The user observed no visible displacement of the buildable boundary.

Re-derive the values from the archived capture bytes and record exact float32 representations, timestamps, reference identities, locations, and before/after/reload provenance. Separate the directly observed arithmetic from hypotheses about *why* the engine maintains it. Survival after reload establishes a reconstructed runtime result, **not** by itself that the identical 12 bytes were serialized directly.

## Workstream A — identify the actual workshop field and its native uses

1. Establish that analyzed `+0x60` accesses refer to the **same concrete workshop/ExtraData object type** captured live, not an unrelated structure with a coincidental offset. Trace construction, accessors, parent/owner relationships and type-specific call paths as necessary.
2. Identify relevant writers and reads, including initialization, placement, beacon relocation, loading/reconstruction, workshop membership, boundary checks and coordinate conversions. Use cross-references, type flow, disassembly and call-site argument provenance; do not stop at textual offset searches.
3. Determine field width, layout, units, coordinate frame, and whether it is a delta, origin adjustment, accumulated offset or something else. Investigate whether it is composed, reset, rotated or transformed under other operations.
4. Follow relevant code paths sufficiently to explain **when** the value changes and **which observable behaviors** depend on it. Distinguish instructions directly proven to access the field from plausible but unverified consumers.
5. If competing meanings remain, construct falsifiable predictions and test those that are possible offline against existing captures/saves.

## Workstream B — Save25 versus Save26 persistence

Compare the exact, archived original Save25 against the exact new manual Save26 from the relocation session. Determine, with controlled-save and no-action context where available:

- Whether the same persistent beacon reference can be matched across files, and how its current XYZ changes.
- Which `ExtraWorkshop`, workshop state, original-center, bound/radius, overlay, parent and reference records change.
- Whether the observed `+0x60` float triple is literally present in encoded save state, transformed or represented elsewhere, or computed when loading.
- Whether planetary site-anchor lon/lat, body and terrain-origin associations remain stable across relocation and reload.
- Which changes are attributable to the move versus background save churn, changed compression or reference reordering.

Use record-aware comparisons wherever possible. An absent literal byte triple **does not prove** the value is not serialized in another encoding. Conversely, matching bytes outside validated record context do not prove direct serialization.

Produce an explicit candidate persistence/reconstruction chain from saved record through load-time runtime value. If a link cannot be established, identify its precise missing step.

## Workstream C — outpost center, boundary and radius

Investigate whether moving the beacon leaves an original workshop/outpost center fixed, and whether that center is determined by `beacon_current + workshop_delta`, a separate persisted origin, or another mechanism.

Specifically search for and validate:

- The native predicates controlling **placement/buildable boundary**, ownership radius, distance-to-center, and any distinction between horizontal, vertical and spherical/volumetric bounds.
- Where radius/diameter constants or configurable values originate (game settings, ESM/record fields, scripts, class defaults, native constants, worldspace/terrain parameters, or save data).
- Whether the radius is one value or differs by outpost type, skill, planet, quest, mode or other conditions.
- Whether its units are the same as beacon local XYZ / terrain coordinates.
- Whether a radius represents the *visible build circle*, actual build permission predicate, interaction/claim range, or a different workshop range. These must not be conflated.
- Whether any radius/center information is serialized or instead reconstructed from engine/ESM defaults.

**Do not use “100 metres” as a fitted or expected result.** If a native radius is recovered in engine units, report the exact value and evidence. Convert to metres only when a defensible unit-scale source or calibration exists, and report conversion uncertainty separately. Do not rely on an assumed Fallout/Creation Engine unit conversion or the terrain-code factor `100` without confirming its meaning in this context.

The user's observation that the boundary did not visibly move is useful field evidence, but it does not establish a specific implementation. If the radius/center consumers reveal a direct link to the `+0x60` field, follow that lead as far as needed.

## Workstream D — connection to planetary coordinates

Determine whether the original center or compensation vector enters the grid origin, site-overlay, local-to-planetary or continuous/fractional beacon-position conversions. Preserve the previously established distinction between:

1. body identity;
2. overlay/site-anchor longitude and latitude;
3. terrain/grid frame and origin;
4. workshop/outpost center;
5. current beacon XYZ;
6. exact planetary beacon position.

It is acceptable to recover only some of this chain in the current pass, provided each recovered transformation is independently tested and the remaining unknowns are identified specifically. Follow terrain-grid/native callers where they directly explain a missing link; do not build an unrelated general terrain-generation model solely for completeness.

## Investigation method and evidentiary requirements

- Use **confidence and coverage as separate dimensions**; report strongest supported answers first.
- Independently reproduce the live arithmetic and any static claims from the actual archived sources.
- For native-function candidates, retain module-relative addresses, bytes/call sites, concrete object-type provenance and relevant argument/data flow. Avoid ambiguous names unsupported by code.
- Preserve and compare competing explanations; actively seek counterexamples in existing captures, controlled saves and mature saves if appropriate.
- Do not require universal engine behavior before recognizing a strong, scoped result, but do not call an indirect pattern a proved consumer/serializer.
- Give Codex latitude for useful speculative detours and additional offline scripts. Document their findings and why they matter. Avoid performative “no result” declarations when a bounded positive result exists.
- No arbitrary tiny analysis caps. Preserve the **40,000,000,000-byte available-space floor** on relevant C: and D: volumes for any substantial scratch output. Use bounded safe file handling and incremental output. Unexpected records, nulls and failed optional analysis paths are **observations to record**, not reasons to abandon independent work. Stop for actual evidence corruption, uncontrolled output/resource harm or inability to trust the analysis.
- Do not modify the installed executable, Ghidra project, ESMs or source evidence. Any third-party consultation or reuse must follow project permission/provenance policy.

## Desired outcomes

Produce a durable research report and supporting reproducible scripts/evidence identifying:

1. **Field identity and semantics:** exact `+0x60` type/layout, observed arithmetic and established native producers/consumers.
2. **Persistence:** precise Save25→Save26 differences and an evidence-backed explanation of how the runtime vector returns after reload.
3. **Original center:** strongest supported account of how a moved beacon relates to the persistent outpost center and its boundary.
4. **Radius:** any validated build-area radius/diameter, its native units, source and conversion to metres if defensible; distinguish other workshop ranges.
5. **Geographic connection:** which coordinate inputs and transformations connect (or fail to connect) the center/current beacon to planetary placement.
6. **Alternative explanations, confidence/coverage, counterexamples and concrete missing evidence.**
7. **Highest-information follow-up:** a narrowly specified live observation only if it would resolve an actual remaining question; no live run is authorized here.

A strong partial answer is valuable. It is not acceptable to bury directly supported field behavior beneath speculative completeness objections. Equally, failure to find a consumer in a finite set of xrefs is not proof no such consumer exists.

## Completion and review

Update relevant durable records and registers **only to the level supported**. Preserve historical evidence and its classifications; make any superseding interpretation explicit. Include a concise entry for interesting secondary leads such as radius constants, terrain rebasing or boundary geometry rather than dropping them.

Perform syntax/tests relevant to added scripts, numerical regression checks, corpus/hash preservation checks, `git diff --check`, Markdown link validation and `git status --short`. Ensure no raw saves, memory blobs, executable/database files or third-party assets have entered Git.

Return:

- answer-first executive findings, with confidence and coverage;
- exact original evidence/capture provenance;
- native function/address and field-consumer mapping;
- Save25→Save26 transition and persistence analysis;
- original-center/boundary/radius results with precise unit caveats;
- planetary-coordinate implications;
- independently reproduced tests and unresolved contradictions;
- scripts/documents changed and complete review diff;
- tests/checks and `git status --short`;
- one recommended next step if necessary.

**No game launch, plugin deployment, debugger attachment, in-game changes, staging, commit or push under this brief.** Return the full change set for critical review.

Suggested commit message, only after approval:

```text
research: trace workshop relocation offset and outpost bounds
```
