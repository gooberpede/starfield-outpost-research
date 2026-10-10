# SOR Implementation Brief — Broad-Capture Live Beacon Coordinate Observer

## Mission

Implement and qualify a **read-only Starfield/SFSE research observer** capable of collecting rich, durable runtime evidence across an **observe → move beacon → observe → manual save → reload → observe** experiment. The central research question is how the saved planetary site anchor (longitude/latitude), terrain-grid/frame state, and beacon's local transform combine to determine the **beacon's actual planetary position**. A secondary question is whether the outpost's original center/boundary remains fixed when its beacon is moved.

This is a **capture-first implementation and research task**, not another native-save automation experiment. The observer must never invoke the game's save function. The user controls gameplay, movement, manual saving and reloading.

**Prioritize one or two evidence-rich live sessions over repeated narrowly scoped probes.** Collection volume and surprising data are not failure conditions. The 40,000,000,000-byte free-disk guard on relevant C: and D: volumes is mandatory; other quotas inherited from past experiments must not be used as arbitrary reasons to abort.

## 1. Existing project basis and permission rules

Review the current committed research and the pinned versions/evidence before implementing. In particular, consult:

- The exact-beacon planetary-coordinate research and its recovered **49,152-step** projection, terrain indices, common-origin candidates, residual/frame-selection gaps, and evidence limitations.
- The two-outpost Save25 work (SOR-002, SOR-003), earlier Kreet S1/S1C controls, Save52, and the previously captured A0/A0C local-position evidence.
- Existing SOR observer/EXP0002 history, especially the false main-thread assumption and the explicit decision to defer native-save automation.
- `gooberpede/starfield-reference-handles` and its SFSE observer, reference-handle acquisition/resolution, teardown, and evidence-handling work. Reuse maintainer-authored material as needed under the standing gooberpede exception. **Record exact repository, path, commit/hash and nature of reuse**. Embedded third-party material retains its own licensing requirements.
- `AGENTS.md`, `WORKFLOW.md`, `THIRD_PARTY_POLICY.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_STATE.md`, and the relevant permission/provenance and experiment registers.

Pin Starfield/SFSE executable/module versions, file hashes, deployment artifacts, and code addresses to the actually installed environment. **Do not assume old Ghidra/SFSE offsets or thread promises apply unchanged.** Vortex is the exclusive deployment owner for SFSE plugins; build an installable package and have the user install/enable/disable it through Vortex. Do not modify Vortex staging or game plugin directories behind its back.

## 2. Two distinct science objectives

### Primary — exact beacon planetary position

Acquire the runtime context needed to determine how the engine combines:

1. planet/moon identity and effective worldspace/cell;
2. the saved **planetary site/overlay longitude and latitude (radians)**;
3. the identified terrain/grid frame, origin, resolution, indices and selection branch;
4. the beacon's current local XYZ/rotation and any residual/fractional data;
5. any native transform, pointer/reference association, intermediate coordinate or body-oriented position required to compute exact global placement.

The recovered discrete angular projection is established working knowledge within its validated scope; do not reopen it merely because the continuous-position path is incomplete. Seek either the actual engine transformation or a numerically equivalent, independently validated method. Preserve full floating-point precision and distinguish site-anchor coordinates from current beacon coordinates.

### Secondary — outpost origin and boundary

Test the user's plausible observation that moving a beacon within an established outpost **does not move the outpost's buildable boundary**. Seek separately identifiable original build center, workshop origin, radius/boundary data, and current beacon transform. Do not assume the boundary and beacon share a position or that the boundary is physically accessible through the initial observer. Failure of this secondary objective does not block the primary one.

## 3. Live capture philosophy: permissive, broad, durable

**Do not repeat the prematurely stopping “SETI telescope” pattern.** Unexpected scientific observations are evidence.

Prefer comprehensive, well-identified snapshots from trusted object roots over overly selective tiny captures. Relevant raw structure content may be large; collecting hundreds of megabytes can be justified. Preserve raw or byte-exact observations together with interpreted fields and provenance so later offline analysis need not require another live run. Allow capture of object graphs, relevant nearby memory/extra-data and terrain/worldspace state where memory-safe and properly attributed; do not dump unrelated process memory wholesale.

Do **not** introduce arbitrary small caps for byte volume, number of objects, graph nodes, elapsed observation time, file count or error count merely because earlier tooling had them. Any necessary operational limit must be justified as a **real integrity/safety requirement**, stated explicitly, and sized generously enough not to foreclose normal observations. The first qualified live run should generate empirical figures for acquisition time, resource consumption, output size and expensive traversals; calibrate later quotas from actual data.

The mandatory hard stop is insufficient disk space: **available bytes below 40,000,000,000 on either relevant C: or D:**, checked before capture and during writing. Also stop uncontrollable/runaway writing or loss of instrumentation integrity that makes further results untrustworthy or unsafe. Correctness constraints such as safe pointer validation, finite graph traversal with visited-address tracking, and bounded synchronous operations still apply; they are not arbitrary evidence quotas.

Nonfatal anomalies should be **recorded and acquisition should continue through independent components**, including:

- unreadable/null/unexpected field, object or structure size;
- handle not resolved, stale reference, absent extra data;
- unrecognized pointer/value, conflicting static interpretation;
- optional native query failure, missing event/notification;
- one incomplete snapshot, unknown terrain-frame branch;
- a value outside expected numerical range.

Distinguish `NOT_OBSERVED`, `UNREADABLE`, `UNSUPPORTED`, `UNEXPECTED`, `QUERY_FAILED` and `CAPTURE_PARTIAL`. Avoid unbounded retries of the same failed operation; log the failure once with context and move on. A failed terrain query must not suppress a healthy beacon or workshop capture.

Terminate or disable affected acquisition only for **actual** machine-safety or observer-integrity failures (e.g. disk guard, runaway writer, corrupted state, loss of trustworthy process/object identity, unsafe synchronization). If one collector fails, preserve healthy independent collectors. **Scientific completeness and instrumentation health must be reported separately.** A process crash after durable useful capture does not retroactively nullify those observations. Do not falsely claim capture completeness if required evidence was not acquired.

## 4. Acquisition strategy and implementation autonomy

Codex may design a broad, modular SFSE observer, borrowing from qualified reference-handles patterns, rather than relying on a single guessed field offset. Establish trusted roots (player/current worldspace, identified beacon reference(s), workshop/outpost, selected overlay/terrain manager) and capture:

- reference identity: FormID/base form, runtime ref handle, pointers and safe classification, object-instance relationships;
- transforms and location: exact floating-point XYZ/rotation, cell, worldspace, body, overlay parent, effective anchor pair;
- workshop state: identity, owned objects, center/origin/boundary/radius candidates, registration/links;
- terrain state: grid origin, resolution, per-axis indices, cell/frame selection, active-world/cache state, fractional residual, candidate matrices and converter inputs/outputs;
- supporting structural bytes/extra data sufficient for offline follow-up;
- timestamps, OS thread IDs, capture stages, program/build/module identity, field-validity flags, query results and source offsets;
- handle churn and reference reacquisition around save/reload, without reusing stale addresses.

Codex is free to expand beyond the initial field list when a concrete observation suggests nearby relevant structures or converter paths. It may use safe read-only calls/tracing where justified, but must not assume SFSE task callbacks run on the true main engine thread: establish actual execution context before calling context-sensitive natives. Prefer observing existing behavior to inducing unnecessary side effects. No manual-memory writes, byte patching, breakpoint installation or native save invocation without a separate reviewed decision.

The implementation should generate structured, timestamped JSON/JSONL and optionally binary raw sections with a manifest, checksums, version ID, pointer/object provenance and independently durable snapshot markers. Implement recoverable incremental writes so earlier snapshots survive a failed later stage. Raw data belongs under ignored `.local-work/` paths. Provide diagnostics for partial and absent evidence, not merely a success boolean.

Formal versioning begins at the next correctly versioned observer build: reconcile with the existing version-history rule before assigning a number (historical `reviewNN` packages remain historical; do not casually reuse an already assigned version). Keep plugin metadata, ZIP, manifests and capture records consistent.

## 5. Offline preparation and review gate

Before live deployment:

1. Map the specific Ghidra functions, field layouts, native APIs, reference acquisition and terrain-coordinate conversion sites needed for capture; differentiate source-proven from guessed offsets.
2. Determine a trustworthy way to select SOR-002 and SOR-003 from Save25 without relying solely on names or stale pointers. Use the reviewed ordinary-beacon detector and save-derived identity/overlay evidence where feasible.
3. Build the observer with broad collection and diagnostics, backed by offline/synthetic tests and a disposable-process qualification where it materially tests memory/read/evidence behavior.
4. Test partial failures, invalid pointers, cyclic reference graphs, change of process/thread context, reloading/reacquisition, writing/flush recovery, disk threshold and simulated runaway output.
5. Produce a deployment/operator handoff and measurement plan, including which parts are expected to work and what remains experimental.

**Return the implementation and preflight evidence for critical review before the first Starfield live session.** Do not automatically deploy or launch Starfield merely because the build succeeds. This gate concerns the new plugin's safety and evidence quality, not a demand for comprehensive semantic certainty before capture.

## 6. Proposed live procedure (for approval, not yet execution)

Use a protected/verified copy of the already constructed **Save25**, with SOR-002 and SOR-003 on Kreet. Vortex installs the research SFSE plugin; the user performs gameplay operations manually.

1. Load the suitable controlled save; observer acquires fresh reference context.
2. Capture **baseline** rich snapshot of both beacons and their shared/individual world, overlay, workshop and terrain state.
3. Capture **no-action control** without deliberate changes.
4. User moves one existing beacon within its established buildable outpost, keeping the other unchanged; record approximate direction/distance and any perceived boundary movement. The user confirms that beacon movement is possible. Do not assume it changes the workshop center.
5. Capture **post-move** rich snapshot; compare both beacons and any center/boundary candidate.
6. User creates a **normal manual save** (never observer-triggered); capture another observation if useful.
7. User reloads that manual save, plugin reacquires all relevant objects/handles, and captures **post-reload** rich snapshot. Never dereference saved pre-reload pointers.
8. Optionally, if essential and supported by observed data, perform a second deliberate displacement or grid-boundary test, retaining the evidence-first approach.
9. Exit, archive/hash the manual save and observer output, and examine all raw data offline.

One or two rich live sessions are preferred; do not fragment into many tiny live probes by default. The exact checkpoints, operator interaction/handoff mechanism, and evidence directories should be supplied in the implementation review.

## 7. Scientific analysis and success standards

Use the committed projection work, Save25/S1/S1C, Save52 and fixed ESM anchors to correlate captured native frames with save-derived data. Do not fit separate arbitrary transformations to each outpost and call it a validated model.

Report at each stage:

- best-supported answer, confidence and coverage;
- actual source/provenance of numerical values;
- full precision and quantified agreement/error;
- frame/origin/resolution decision path;
- whether site anchor, current beacon and original outpost center differ;
- raw evidence supporting the conclusion;
- concrete alternative interpretations and contradictions.

Primary success: recover the actual or numerically equivalent transformation that locates a beacon globally on the planet and validate it on independent cases. Partial success: settle a material part of frame selection or residual projection with reproducible evidence and specify the remaining inputs. Secondary success: determine whether workshop origin/boundary remains anchored after beacon relocation.

Preserve and register useful secondary leads about terrain tiling, possible 2×2 multi-cell assets, grid resolution/rotation, resource and appearance overlay orientation, poles/prime meridians—without treating unverified Reddit visual observations as confirmed engine behavior. Previous prior-art attribution and third-party reuse requirements still apply.

## 8. Scope boundaries, validation and deliverables

- **No** native-save automation, save mutation, forced game-memory writes, broad external debugger campaign or production save importer.
- Vortex exclusive deployment owner; user's explicit cooperation for installation, move, manual save and reload.
- Source saves, Ghidra databases, pinned binaries and existing evidence must remain unchanged.
- Source/third-party permissions, provenance and notice requirements remain in force. Maintainer-authored gooberpede material may be reused with documented provenance.
- No staging, commit or push before review.

Return for review:

1. implementation design, actual acquisition roots and validated execution/thread context;
2. source files, scripts, versioned DLL/package and package SHA-256;
3. reusable sibling-repo provenance and other third-party permissions/notices;
4. exact captured fields and raw-evidence formats, including partial/error classifications;
5. disk/runaway/instrumentation integrity behavior, and evidence of no arbitrary small quotas;
6. synthetic/disposable qualification results and remaining risks;
7. proposed operator card, Save25 checkpoint plan and live handoff;
8. objective-specific evidence coverage plan and scientific vs instrumentation-health measures;
9. changed files, `git diff --check`, internal-link checks, input/source hash preservation, `git diff`, and `git status --short`;
10. any concrete blocker preventing a usable broad-capture observer, with attempted solutions and the least obstructive correction.

Suggested commit only after review and successful appropriate qualification:

```text
research: build broad-capture beacon coordinate observer
```
