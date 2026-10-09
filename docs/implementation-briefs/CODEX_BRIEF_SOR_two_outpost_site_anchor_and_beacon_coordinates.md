# Codex Research Brief — Two-Outpost Site Anchors and Beacon Coordinates (Save25)

## Objective

Determine how Starfield relates an outpost beacon’s saved local position to its **planetary overlay/site-anchor longitude and latitude**. Use the new controlled Save25 containing **two outposts on Kreet within one continuously traversed landing area** as the primary discriminating sample.

The desired result is a reproducible explanation of whether the pair identifies a shared landing-area origin, an outpost-specific site anchor, or another body-associated placement frame—and, if supported, a method to derive a beacon’s global planetary position. Preserve the distinction between a **site coordinate** and the **precise beacon coordinate**.

This is an offline research and tooling task. No Starfield launch, new save, live observer deployment, or debugger attachment is authorized. Do not stage, commit or push.

## 1. Verified inputs and experimental provenance

New primary sample in the live Steam-managed directory:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\
Save25_D6036588M417474696C61204B6972616C79_000231_20261009102224_4_0_4.sfs
```

The user created Save25 by loading **pristine Save3** as the starting state and placing two ordinary outposts on Kreet:

- **SOR-002**: approximately the same location as the previous Kreet control beacon, within a few metres.
- **SOR-003**: approximately a couple of kilometres to the north of SOR-002, reached **entirely on foot within the same continuously traversed landing area**; no planetary landing-area transition between the two placements.

Treat the names as **labels for distinguishing the two documented placements**, never as evidence of planet identity or coordinate values. “North,” “a couple of kilometres,” and “within a few metres” are approximate user observations, not calibrated measurements. The save contains both outposts in one state; it is **not** a differential sequence with one beacon per save.

Copy Save25 into the ignored `.local-work/savegames/` research area (choose a noncolliding corpus-specific subdirectory if appropriate). Hash both live source and copy and verify byte equality **before analysis**. Do not move, rename, delete, modify or write to the live original. Keep raw/decompressed blobs untracked.

Consult, without altering, the established archived controls and durable findings, including:

- Save3, S0/S0C, S1/S1C and the relevant Kreet resaves (e.g. L2C), using their manifest-defined identities;
- Save2 near the Lodge as a fixed-site/location comparison;
- Save52 and the independently maintained outpost-network JSON for broader body/site diversity;
- the scoped ordinary-beacon detector and reviewed planet/body resolver;
- the approved planetary-surface-anchor report and native/ESM evidence establishing the saved pair as **longitude first, latitude second, in radians**, associated with an overlay/site anchor.

Do not assume the earlier Kreet beacon was placed in the exact same local reference frame or has the same outpost/site parent merely because the locations are geographically close.

## 2. Begin from reviewed findings, not rediscovery

Use as working knowledge, within stated coverage:

1. Ordinary player-buildable beacon references can be recognized in supported save-record representations.
2. Saved reference/body/overlay associations have resolved Kreet for the earlier controlled beacon and the 17 Save52 network outposts to their independently known bodies.
3. The body-associated double pair has STRONG scoped evidence for **(longitude, latitude), in radians**, for a planetary overlay/site anchor, **not necessarily the precise beacon position**.
4. Candidate local XYZ values have been recovered for beacons/placed objects but their relation to the planetary frame is not yet established.

Do not reopen these findings without a concrete contradiction. Use the project's confidence **and coverage** rules. Separate physical observed bytes, decoded structural relationships, strongly supported semantics, and new hypotheses.

## 3. Phase A — Extract and compare the two Save25 beacon chains

Use the read-only detector and existing decoding utilities. Independently verify that Save25 contains the two expected ordinary beacons; do not force exactly two if additional beacon-like references occur. Report all candidates and resolve which match SOR-002 and SOR-003 by grounded saved-name/reference associations.

For each identified beacon, capture at minimum:

- saved record type, offsets, enclosing logical record and stable candidate identifiers;
- effective base-form identity and saved enabled/disabled state if available;
- owning planet/moon and star-system association via **saved references plus ESM/PNDT**, not the outpost name;
- parent overlay/site/worldspace/cell references, wherever supported;
- exact saved longitude and latitude doubles (raw representation and interpreted radians);
- candidate local beacon XYZ and rotation, stating precisely what record each tuple comes from and whether its ownership is proved;
- association through which each value was resolved, including any unresolved steps.

Prepare a side-by-side evidence table for SOR-002 and SOR-003; include raw locators/byte or record offsets and readable values so independent review is possible.

## 4. Phase B — Test shared versus distinct anchors

Compare **separately**:

1. parent overlay/reference identity;
2. body identity;
3. angular-pair bitwise equality (not just rounded values);
4. candidate beacon local XYZ;
5. candidate coordinate-frame identity (worldspace/cell/landing-area identity, if recovered).

Do not assume same `lon/lat` implies identical parent references, or different references imply different angular coordinates. Explicitly allow all combinations.

Classify the best-supported outcome:

- **Shared anchor:** same verified overlay/site identity and angular pair, distinct local beacon positions.
- **Shared angles, distinct anchors:** different parent identities but identical angular values.
- **Distinct anchors:** different angular pairs with independently resolved associations.
- **Mixed or unresolved:** alternative representation, ambiguous match, or insufficient evidence.

If the two beacons share a site anchor, investigate whether their local displacement is consistent with two positions in the same local coordinate frame. If they have distinct anchors despite uninterrupted travel, investigate the smallest plausible outpost-specific placement/overlay distinction. Do not infer a tile boundary from geography alone.

## 5. Phase C — Correlate Save25 with earlier Kreet evidence

Compare SOR-002 and SOR-003 against the archived S1/S1C Kreet beacon:

- body and system;
- overlay parent and raw angular pair;
- local beacon XYZ and relevant worldspace/cell identities;
- evidence of any coordinate-frame change after loading Save3 and constructing new outposts.

SOR-002 is reported only *approximately* colocated with the earlier beacon. Distinguish a true equal anchor from nearby angular values and from a numerical coincidence. Never assume cross-session save-local tokens are stable identities.

Use Save2/New Atlantis and installed fixed-site ESM records only as cross-checks where they clarify orientation, transformation conventions or site-anchor reuse. Do not turn this into a general planetary atlas.

## 6. Phase D — Investigate beacon-global-position conversion

Starting from the actual native/ESM coordinate chain previously located, investigate the minimum additional information needed to map:

```text
planet/body identity
+ overlay/site (lon, lat)
+ local beacon XYZ
+ any necessary frame/orientation/scale data
    -> global planetary position of the beacon
```

Use targeted Ghidra static analysis, xEdit/ESM inspection and bounded offline numerical tests where they add information. Codex may investigate competing transformations; do not prescribe a particular tiling, sphere projection, terrain scale, meridian, or coordinate conversion without evidence.

Try to establish, in order:

1. whether the site pair describes a common landing-region origin or an outpost-specific anchor;
2. whether the beacon XYZ is defined relative to that origin or an intermediate cell/worldspace transform;
3. the axes, units, handedness, orientation and scaling needed for transformation, if recoverable;
4. whether a concrete globally meaningful beacon coordinate can be computed, and with what accuracy/validation.

A **verified site anchor** remains useful even if exact beacon location is not attainable in this offline pass. State precisely the missing transformation or input rather than replacing it with guessed latitude/longitude.

The user’s rough northward movement may be used as a sanity check only after an independently derived axis convention exists, never to choose the convention.

## 7. Secondary leads, not additional primary tasks

Remain alert to findings concerning:

- planetary landing-area/tile/overlay registration and reuse;
- terrain projection and planet-oriented coordinate frames;
- resource overlay versus orbital appearance/texture mappings;
- polar axis, zero longitude/prime meridian and planetary rotation;
- existing prior technical research on Starfield planetary tiling.

Record promising leads with reproducible source locators, provenance/attribution, observed basis and suggested follow-up. Do not expand into general planet-generation, texture, resource-map or terrain-system reverse engineering unless required to answer the immediate coordinate question. Honor all third-party permission and code-reuse rules. Reuse reviewed prior-art records rather than repeating a broad web research sweep without purpose.

## 8. Testing and evidence standards

- Use exact numeric representations and documented precision; do not round equality tests.
- Record and verify source hashes, copies and relevant ESM/executable identities.
- Test the main hypotheses against independent evidence when available.
- Do not use outpost names or tracker JSON's `bodyId`/`systemId` as a decoder input. Those are validation or matching aids only after save-derived identity is established.
- Do not confuse a shared landing area observed by the player with an already verified shared *serialization overlay*.
- Distinguish strong scoped findings from remaining unknowns; provide the best-supported answer first.
- Preserve contradictory cases and do not force agreement with prior conclusions.
- No arbitrary total decoded-size ceiling; retain bounded processing, integrity/resource checks and the established 40 GB disk guard.
- Do not silently modify existing committed evidence or findings; make justified prospective updates with provenance and cross-references.

## 9. Deliverables and stop condition

Create a durable experimental report and supporting inspection utilities/evidence as needed. At minimum provide:

1. Save25 source/copy manifest and SHA-256 verification;
2. identities and saved-state evidence for both beacons;
3. body/system, parent overlay references, raw `lon/lat`, local XYZ and frame identifiers in a side-by-side table;
4. explicit shared-anchor versus distinct-anchor conclusion, with confidence and coverage;
5. comparison to S1/S1C and any relevant Save2/fixed-location control;
6. tested coordinate-transform hypotheses, decisive checks and counterexamples;
7. best-supported statement of what the pair locates and how local beacon XYZ relates to it;
8. global planetary beacon coordinates if defensibly derivable, **otherwise exact missing inputs/transform stages**;
9. bounded secondary-lead register, with attribution/provenance;
10. proposed smallest next discriminating step if necessary;
11. file inventory, validation/test results, `git diff` and `git status --short`.

The task is complete when the Save25 shared-versus-distinct anchor question is answered as strongly as available evidence permits and the remaining beacon-coordinate transformation is either demonstrated or bounded to explicit unresolved mechanisms. Do not continue decoding unrelated planetary systems merely because further work is possible.

No live game work, source-save modification, deployment, staging, commit or push. Return for critical review.

Suggested commit message **only after review and approval**:

```text
research: compare co-located outpost anchors and beacon positions
```
