# Codex Research / Implementation Brief — Durable Outpost Position: Engine Oracle and Algorithm Reconstruction

**Project:** `starfield-outpost-research`  
**Status:** Implementation/research authorization for offline work only; **review required before a live Starfield run, Vortex deployment, commit or push**.  
**Primary objective:** Recover a complete, reproducible model of how Starfield reconstructs and uses the **durable planetary position of a player-built outpost**, and validate it against independent engine behavior.

## 1. The standard of completion

The user wants the level of understanding achieved by the sister projects `gooberpede/starfield-resource-research` and `gooberpede/starfield-resource-reproducer` for inorganic resource generation: **a recovered algorithm, an executable independent model, and meaningful oracle comparison**, not merely another inventory of correlated fields or a collection of strong partial observations.

The resource projects' current README records a recovered v1.0 algorithm and exact reproduction across 1,444 canonical cases, with independent Creation Kit and retail holdout results (10/10). This is a **methodological benchmark**, not a requirement to manufacture a comparably sized outpost corpus or claim the Creation Kit and retail game use identical routines.

The goal here is to reach the analogous state **for the supported outpost-position domain**:

- known saved inputs and their authoritative provenance;
- frame/reference selection and transformation steps, in execution order;
- rounding, quantization, signedness, precision and exceptional branches;
- independently authored, deterministic reference implementation;
- comparison with an **independent native engine oracle**;
- coverage limits, counterexamples, version boundaries and tests.

A mere match between two tools that both implement our inferred formula is **not** independent oracle validation.

The principal subject is the **durable workshop/outpost center**, not the current movable beacon mesh and not a speculative exact geographical latitude/longitude. Exact continuous geographical coordinates remain deferred unless the engine's own relevant algorithm establishes them.

## 2. Required study of the two sibling repositories

Inspect the current default branches and relevant durable history in:

- `https://github.com/gooberpede/starfield-resource-research`
- `https://github.com/gooberpede/starfield-resource-reproducer`

Read at least the root README, research baseline/evidence standard, native-function register or corresponding map, the reproducer's architecture/domain rules, validation baseline, and the implementation workflow. Inspect selected tests and implementations to understand **how the research evolved from hypotheses to a fully specified algorithm**, rather than copying terminology from the READMEs.

Extract transferable *research practices*:

1. distinguish source inputs from independently generated outputs and validation oracle;
2. recover native branch order and intermediate state, not just final values;
3. keep native-function provenance and executable/version attribution;
4. implement a deterministic reference model separate from game code;
5. maintain targeted regressions, pathological cases and independent holdouts;
6. reconcile counterexamples with the model instead of patching around them;
7. distinguish evidence/provenance ownership from reference-implementation ownership.

The resource projects use Creation Kit live tracing for their validated CK path and retail observations as a separate corroboration layer. **Do not transpose CK addresses or claims to `Starfield.exe`.** Record which parts of the research methodology are actually applicable to outpost position and what differs.

The repositories are maintainer-owned (`gooberpede`): authorial permission for reuse of maintainer-authored scripts, tests or utilities is granted; self-credit is not needed; **provenance is mandatory** (repo, path, commit/hash, nature of reuse). Embedded third-party material retains its own restrictions. Respect all existing SFSE and third-party rules. Do not fork or submit upstream changes.

Record the exact revisions consulted, not simply “latest GitHub.” Prefer the connected GitHub access or local checkouts; document unavailability if applicable rather than inventing findings.

## 3. Existing outpost evidence and settled distinctions

Start from the committed evidence and implementation in `starfield-outpost-research`, especially:

- Save25 (SOR-002 and SOR-003) and Save26 (SOR-003 beacon relocated), plus verified archived copies;
- nine successful 0.1.0 observer captures and their raw evidence;
- Save3 / S1/S1C original Kreet controls;
- Save52 and its separately maintained outpost-network JSON, for wider coverage;
- saved planetary body association and site-anchor longitude/latitude;
- 49,152-step discrete/two-hemisphere projection and tested cell-center mapping;
- saved-frame reconstruction, grid-cell identification and fractional residual;
- workshop `ExtraData +0x60` relocation-compensation vector and its direct persistence;
- compensated center `float32(current_beacon_XYZ + workshop_delta)`;
- activated-overlay/frame selection, rebase and terrain-grid investigations, including the last static-exhaustion ledger.

**Accept established scoped results as working knowledge** unless contradicted. The 19 mature beacons' zero compensation vectors are consistent with the user's direct statement that those beacons were never moved. Do not restart generic flag, radius or continuous-lat/long arguments.

The remaining question is: **Which exact native game operation reconstructs or consumes the outpost's durable body/frame/grid/subcell position, and can our independent model reproduce that operation?**

## 4. Stage A — Discover and qualify the engine oracle

Investigate authoritative candidate native operations that consume or resolve the restored state, including workshop-center consumers, selected activated-overlay frame and translation, terrain/grid coordinate resolution, boundary/terrain coverage, and other directly relevant paths.

You have broad latitude to follow call chains, indirect calls, data dependencies and adjacent terrain or worldspace subsystems as necessary. Do not impose an arbitrary function-count or investigation-time quota. Reuse earlier Ghidra work and the published research methodology, updating typed function maps where necessary.

For each oracle candidate determine:

- pinned executable and precise RVA/function identification;
- semantic inputs, outputs and called consumers;
- whether it calculates a result independently of the offline reconstruction;
- exact object/extra-data identities and ownership;
- runtime initialization and required scene/load state;
- thread/context requirements, potential side effects and read/observe options;
- whether it returns a local center, selected grid address/residual, loaded-world coordinate, or something else;
- whether the value is authoritative for durable workshop placement or only a UI approximation.

**Independence test:** Merely asking the plugin to reread beacon XYZ and `+0x60` and add them does not qualify as an independent oracle for that sum. It may be used as a diagnostic, but prefer observing a native consumer's selected frame, output or downstream placement decision. Several complementary oracle operations may be needed.

If the game does **not** compute a continuous latitude/longitude for arbitrary workshop references, do not make that a failure. The target is the engine-native positional identity and placement algorithm actually used.

## 5. Stage B — Recover a branch-complete model of the supported algorithm

Construct a documented, falsifiable transformation pipeline from persisted inputs to native placement result. Preserve the actual engine's distinctions among:

1. planetary body and persistent reference identity;
2. saved site anchor and world/overlay descriptor;
3. saved-frame selection and activation/rebase state;
4. terrain origin, grid resolution and integer cell address;
5. signed and fractional position components;
6. durable workshop center and beacon movement compensation;
7. any relevant orientation or grid rotation/reflection;
8. output used by the native position/terrain consumer.

These are investigative prompts, **not a mandated architecture**. Revise or replace the pipeline when code evidence demands it. Explicitly identify branch conditions, fallback cases, valid/invalid states, precision conversions, and the distinction between saved-state reconstruction and mutable later runtime rebasing.

For each unresolved primary dependency maintain an auditable ledger: producer, consumer, native location, proven inputs/outputs, attempted hypothesis, tests/counterexamples, and disposition (`RESOLVED`, `FALSIFIED/IRRELEVANT`, `STATICALLY_BLOCKED` with precise reason, or `ACTIVE — continue investigating`). `STRONG PARTIAL`, `too complex`, or the discovery of one unexamined branch is **not** exhaustion. Do not end while materially promising authorized static paths remain unexamined.

## 6. Stage C — Independent executable reference model

Implement a small, deterministic, inspectable **research-grade positional reproducer** or extend an appropriate existing offline tool. It must:

- accept explicitly versioned, provenance-backed saved-state inputs;
- output the durable body/frame/grid/cell/residual/center identity and any native coordinate representation demonstrated by the evidence;
- expose decisive intermediate values and trace branch decisions;
- avoid consuming native expected output as an algorithmic input;
- avoid fitting per-save parameters to each validation case;
- preserve float32/float64, integer conversion and rounding semantics where essential;
- fail clearly on missing or unsupported inputs rather than fabricating an outpost position.

Do not split this into a new public repository unless separately authorized. The research/reproducer sibling separation is a methodological example; keep implementation in the existing outpost research project for now, with clean separation of evidence and model/validation code.

## 7. Stage D — Precommitted oracle validation design

Before examining new oracle outputs, document inputs, predictions, comparison fields, precision/error policy and holdouts. Primary cases:

- **SOR-002 / Save25:** ordinary unmoved workshop center;
- **SOR-003 / Save25:** independent workshop in the same traversable area;
- **SOR-003 / Save26:** same durable center after beacon relocation, saving and loading.

The same model must predict the invariant durable position in Save25/Save26 and distinguish SOR-002 from SOR-003 without per-case fitting.

Use S1/S1C and selected Save52 outposts as independent or expanded cases where the required native context is available. Mature JSON is a comparison dataset, not an algorithmic input; names are not planetary evidence. Do not require Save52 deployment in the first live session.

Compare intermediate states and final native placement outputs; distinguish exact bit matching, numerical tolerance derived **before** seeing results, equivalent positions under rebase, and different coordinate frames. A result in a different frame is not necessarily a failure, but a purported equivalence must be demonstrated.

Do not claim exact oracle validation from static code and offline simulation alone. Clearly label such comparisons `STATIC/REPRODUCER` until actual independent runtime oracle observations are obtained.

## 8. Stage E — Instrumentation design and offline qualification

Prefer reuse/extension of the successful SFSE `SorBeaconObserver` 0.1.0 and relevant maintainer-owned `starfield-reference-handles` techniques. Choose the least intrusive method that obtains **independent engine results**, but do not reject a necessary qualified native call, hook or targeted debugger trace solely because earlier save-function debugging was troublesome.

Where a native query is contemplated, qualify ABI, object lifetime, execution context/thread, side effects, and fresh reacquisition after loading. A worker-thread read is not a guaranteed safe game-thread invocation. Observation of natural engine execution may be preferable to actively calling the function.

Prepare broad, useful evidence collection (input/output snapshots, selected frame, raw supporting structure, thread and timestamp provenance), while following established policy:

- no arbitrary tiny count, volume or duration quotas before empirical need;
- **40,000,000,000 bytes minimum available** on relevant C: and D: volumes, with genuine runaway-output/instrument-integrity failures terminal;
- unreadable fields, unexpected values and isolated partial failures are recorded, **not automatic stops**;
- preserve durably flushed partial evidence;
- no false promise of atomicity or pointer validity;
- Vortex exclusively manages SFSE plugin deployment;
- controlled manual saves remain the method; do not reopen native-save automation.

**Implement and offline/disposable-qualify** an observer extension only after the oracle acquisition contract is credible. Version the changed binary/package and associated evidence consistently. Produce a practical operator run card for prospective Save25/Save26 validation.

**Review gate:** Do not deploy or run Starfield under this brief. Return code, preflight/qualification evidence, exact proposed engine oracle, predictions and run card for critical review. The user will operate any Vortex deployment and live gameplay after separate authorization.

## 9. Completion criteria and blocker standard

Stage A–E completion means a documented, testable native-oracle strategy and independently executable position model, with offline qualification and a clear live validation plan. **It does not permit claiming algorithmic equivalence before live oracle results exist.**

After a later authorized live test, the desired terminal research state is analogous to the resource-reproducer milestone: model matches engine oracle across supported cases and adverse/boundary regressions, with named untested domains and holdouts.

If a complete model or usable oracle cannot yet be prepared, report the **strongest supported result**, then show a concrete, auditable blocker:

- exact missing input or operation;
- responsible native producer/consumer;
- each meaningful static path investigated and its disposition;
- why offline evidence cannot discriminate the alternatives;
- a specific live observation or new sample that would resolve the ambiguity.

Do not call unfinished tracing an impossibility proof. Do not insist on unsupported universal coverage to withhold a scoped working model. The continuous-geographic lat/long investigation remains deferred unless its evidence directly resolves an engine-native placement dependency.

## 10. Scope, publication, preservation

Offline/static analysis only; no Starfield launch, live debugger attachment, SFSE deployment, native game-state mutation, save modification, staging, commit or push.

Read approved pinned binaries/ESMs, existing Ghidra databases, saves and observer evidence without modifying protected inputs. Work in ignored scratch paths as needed. Keep raw saves, process-memory outputs, proprietary game-derived blobs and binaries outside Git. Respect the project's third-party provenance and reuse policies.

Do not silently revise prior accepted evidence classifications. New contradictory evidence must be preserved and reconciled explicitly. Record sibling-repository study and exact commit provenance, and maintain a separate oracle-vs-reference-model evidence trail.

## 11. Required deliverables

1. **Sibling-project methods review** — actual files/commits consulted and concrete practices adopted or rejected.
2. **Native oracle candidate and selected acquisition contract** — typed functions, RVA, context, independence and side-effect analysis.
3. **Algorithm reconstruction** — executable/specification-level stages, branch conditions, precision and known coverage.
4. **Dependency/exhaustion ledger** — all remaining primary leads with meaningful terminal/active dispositions.
5. **Reference reproducer** — source, tests, example inputs/outputs, provenance, no oracle leakage.
6. **Validation protocol** — precommitted Save25/Save26 predictions, precision/error policy, negative and holdout cases.
7. **Observer changes, if warranted** — versioned build, offline/disposable qualification, package manifest and proposed run card; otherwise a technically justified acquisition alternative.
8. **Durable research documentation** — answer-first result, confidence versus coverage, oracle limitations, counterexamples and research-state implications.
9. **Review receipts** — files changed, tests/checks, raw-evidence hash preservation, `git diff --check`, internal links, ignored-artifact checks, complete diff and `git status --short`.

Return for **critical review before any live work or commit**.

Suggested future commit title (only after review):

```text
research: reconstruct durable outpost positioning and prepare engine oracle
```
