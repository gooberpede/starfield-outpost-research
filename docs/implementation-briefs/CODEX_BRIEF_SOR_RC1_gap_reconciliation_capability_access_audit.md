# Codex research/documentation brief — RC1: research-gap reconciliation and capability-access audit

**Project:** `D:\Projects\starfield-outpost-research\`  
**Assignment:** RC1 — reconcile the accepted outpost research and document existing definition, Papyrus, and game-configuration access routes.  
**Task type:** Bounded offline documentation/evidence reconciliation; targeted read-only verification of existing definitions and Papyrus declarations is allowed.  
**Authority:** This user-approved brief authorizes preparation and verification of the described documentation only. It **does not** authorize Starfield launch, debugger attachment, instrumentation, new gameplay, new save creation or modification, substantive new native reverse engineering, deployment, alteration of protected inputs, publication, licensing changes, staging, commit, or push.

## 1. Purpose and editorial principle

Produce a trustworthy reader-facing map of (a) what remains unresolved after the completed research and (b) **which existing interfaces allow a particular outpost-system capability to be configured, invoked, observed, or extended**. This is foundational documentation of Starfield's machinery, **not** a feasibility study for a specific mod, a modding implementation guide, or an SFSE recommendation engine.

Crucial distinction: **native implementation is not the same as native extension required**. A native function can expose behavior through an ordinary plugin record, a Papyrus function/event/property, or a game setting/actor value/global. Conversely, failure to find one of those routes is only an evidence-bounded absence: **“No supported interface identified in the examined evidence.”** Never turn that finding into “requires SFSE,” “must patch Starfield.exe,” or comparable engineering prescriptions. Do not propose how to build absent interfaces.

Preserve the project's established confidence/evidence/coverage/lifecycle/publication distinctions. State the strongest supported positive result first, then material gaps. Avoid hypothetical counterexamples that do not bear on a claim's demonstrated scope. Do not convert untested extensions into demonstrated ones, or negative searches into universal impossibility claims.

## 2. Read first; frozen baseline

Read and apply repository `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md`, and relevant reviewer instructions. Observe existing evidence/protected-file safeguards and the current pinned game/version provenance; do not assume paths or hashes remain unchanged merely because a prior report said so.

**Baseline:** the accepted 2026-10 coverage audit, especially:
- `docs/audits/outpost-coverage-2026-10/coverage.md` (60 questions),
- `docs/audits/outpost-coverage-2026-10/report.md`,
- its Build Mode / Locations and position / biome / source-gap assessments and review.

**Subsequent accepted research to reconcile:**
- `docs/experiments/coordinate-sufficiency/` — qualified ordinary terrain-cell geographic address, local offsets and Papyrus `GetCurrentLocation()`;
- `docs/experiments/outpost-biomes/` — qualified base-biome assignments and complete nominal 150-unit territory coverage;
- `docs/experiments/construction-variants/` — Snap Behavior, manual CHANGE, automatic connections, replacement children, materials and damage-stage contrasts;
- `docs/experiments/build-catalogue/` — menu discovery/grouping/selection/eligibility, population bounds and nominal mixed-producer aggregation;
- `docs/experiments/locations-outpost/` — field lineage and previously unexamined counts, ownership/faction/level and graphics.

**Other established subsystem evidence:** earlier Workshop and save identity/membership/position investigations; E1–E3 production; P1 power; S1/S2 storage/links; C1–C3 cargo; CR1–CR3 crew; R1 robots; L1–L3 limits; DA1 defense; SD1–SD3 containers/shared storage/Stored Resources. Consult `docs/BACKLOG.md`, `docs/RESEARCH_STATE.md`, subsystem indices and the authoritative reports *only as necessary* to assign grounded dispositions and identify existing access routes. Do not reopen those accepted experiments or recompute their primary findings.

Treat user decisions as governing prioritization: exact realized-production prediction is **deferred**; accurately monitoring actual live production within reasonable tolerances is a distinct potential capability, not an already implemented measurement system. Exact continuous beacon lon/lat was intentionally left as an **engineering precision/implementation question** after coordinate sufficiency; do not resurrect it as an obligatory foundational research failure. Biome-map accessibility for an offline implementation likewise is an engineering dependency, not a missing base-biome model. Exact POI-clipped biome coverage remains separate from nominal territory coverage.

## 3. Gap reconciliation: exact requested work

Start from **every one of the original 60 question IDs**. For each, retain its identity and historical audit disposition; add current status after the five accepted investigations, best-supported answer, exact authoritative references, remaining material uncertainty, demonstrated coverage, and proposed next action/disposition. Do not silently delete, renumber or rewrite the historical matrix. Where one original question contains separable remaining gaps, use stable linked child IDs in the new reconciliation rather than pretending the original question never existed.

Suggested dispositions: **RESOLVED**, **CONSOLIDATE**, **TARGETED RESEARCH CANDIDATE**, **DEFERRED**, **PUBLICATION BLOCKER**. Distinguish these editorial dispositions from evidence confidence and from project authorization. A publication issue may be remediated by qualifying/retiring a claim, not necessarily by performing new experiments. Flag direct contradictions only when supported by a concrete competing finding or counterexample. Do not invent newly closed gaps from titles or summaries alone.

Ensure explicit treatment of these cross-cutting cases:
- Qualified ordinary Workshop/outpost active-player membership versus exhaustive save-import counts.
- Geographic terrain-cell addresses, exact subcell longitude/latitude, fresh-character repeatability and practical geographic navigation as different claims.
- Base biome map, complete **nominal** footprint enumeration, qualified frame context, and **effective POI-clipped** footprint.
- Biome/resource-generation relationship versus positive site deposit availability.
- Construction variants, build catalogue, count/limit mechanisms, menu population and LO1 field bindings: what's now solved and which exceptional/live details remain.
- Nominal production aggregation (closed) versus realized throughput prediction (deferred) versus potential monitoring instrumentation (distinct).
- Shared-storage backing inventory contents, exceptional effective inventory states and stale/remote snapshots.
- Save/restoration, historical counterexamples, physically loaded versus scripted/native state, and actual test coverage.
- Evidence/publication status inconsistencies, unavailable local sources and reproducibility dependencies; these are **flags**, not authorization for cleanup or release.

Do not change original scientific finding classifications or their source reports. New reconciliation documents may propose classification updates for later maintainer review, with clear original/current citation and rationale.

## 4. Capability and access matrix: what it must mean

Create a **capability-level**, not merely subsystem-level, matrix. Example row granularity: “register a new Build Mode recipe,” “add an STBH wall alternative,” “alter a producer's configured interval,” “query a current Location,” “read an outpost's nominal Stored Resources aggregate,” “change a construction prerequisite,” “observe inventory changes,” “apply a destruction-stage model,” or “configure cargo endpoints.” These are **questions to classify**, not predetermined proof that each interface exists.

For each capability record:
1. Capability and bounded behavior (distinguish **configure**, **invoke**, **read/observe**, **receive event**, **change existing state**, and **create a new behavior**).
2. **Definition-driven route:** specific installed record types/fields, keywords, form lists, conditions, components and their relationships, where positively identified.
3. **Papyrus route:** exact accessible function/event/property/script name and signature, registration/declaration and relevant semantics where positively identified; differentiate a Papyrus callable from a native-only internal function and from a script merely calling native code.
4. **Game-configuration route:** identified globals, game settings, actor values, perks or other exposed mutable configuration operands, together with their consumers. Distinguish authoring a definition from changing a running value if that matters.
5. Native consumer or behavior being configured, **without** interpreting native implementation itself as an extension requirement.
6. Concrete limits and prerequisites supported by the sources; actual category/argument scope, game-version scope and known counterexamples.
7. Evidence class: **DEMONSTRATED**, **STATICALLY ESTABLISHED**, **PROVISIONAL**, or **NOT ESTABLISHED**, independently for each route where appropriate, plus precise source pins/links.
8. Missing evidence or the **bounded** checked surface if no access route is identified.

The three access routes may all apply to one capability. Use explicit **not investigated** where the source corpus has not checked a route; do not write “not possible.” Distinguish definition-/script-exposed behavior from arbitrary user-desired new functionality. Do not assert “requires SFSE,” “must be native,” or name any implementation technology as a prescribed workaround when available interfaces are absent.

**Papyrus audit scope:** targeted reread of installed `.psc` declarations, existing scripts and accepted call-path evidence for relevant interfaces, not a comprehensive Papyrus API census. Verify exact capitalization, owning script/class, parameter and return types, and whether calls are public, hidden/internal, native-registered, event callbacks or ordinary scripts where evidence allows. Do not infer availability from a guessed method name or native address. `Game.GetPlayer().GetCurrentLocation()` is a useful negative control: it returns a `Location` object rather than longitude/latitude.

Provide meaningful coverage across the major outpost systems: placement/membership, production/power, storage/inventory/crafting, output/cargo, construction limits/prerequisites, personnel/robots, defense/damage, construction variants, catalogue/selection and geographical/biome lookup. **Prioritize existing positive evidence**; where records offer no founded access-route answer, say so and cite the limits. Avoid exhaustive per-form/per-item listings and avoid speculative extensibility promises.

## 5. Deliverables and reader usability

Create a durable set under an appropriately named `docs/audits/` location (e.g. `docs/audits/outpost-rc1-2026-10/`), including:
- `report.md`: answer-first summary, meaningful resolved/deferred/publication changes, standout access-route findings, limitations, decisions requested from maintainer, and suggested later work, **not** engineering prescriptions.
- `gap-reconciliation.md` or equivalent structured table: complete 60-ID crosswalk, any justified child issues, historical versus proposed present dispositions and evidence links.
- `capability-access.md` or equivalent structured table: capability-level definition/Papyrus/configuration access matrix with evidence statuses and no unsupported “requires native plugin” classification.
- `papyrus-interfaces.md` if necessary for exact callable/event/property definitions and declaration references (otherwise incorporate directly into the matrix).
- `review.md`: acceptance-matrix, errors/corrections, evidence status, validation receipts and independent-review disposition.

Use **relative links** between repository documents. Keep material source pins and explicit absence/permission limits navigable. Existing machine-local source locators are allowed as documented evidence references, not portable public checkout instructions. Correct new-document typography, line wrapping, Markdown tables, code snippets and punctuation; prohibit repeated malformed prose/encoding regressions. Keep large generated machine evidence out of versioned docs and avoid requiring redistributable copies of game binaries, extracted Bethesda scripts/assets or personal saves.

Optionally propose a short entry-point link from the existing docs index if permitted as documentation integration; do not rewrite legacy research or silently adjust `PUBLICATION.md`, licenses or publication categories.

## 6. Method, authority and preservation

1. Record initial git status, `HEAD`, index condition, selected relevant file identities, tool/game provenance and existing protected-input rules. Respect tracked/untracked/ignored user work; do not clean or reset it.
2. Read accepted audit and latest five research packages; construct the complete question crosswalk before editing conclusions. Maintain a source-evidence ledger distinguishing original claims from proposed interpretations.
3. For capability entries, prefer accepted concrete source relationships. Perform **small read-only checks** of installed definitions or Papyrus declarations only to confirm a specific named route/signature; record when no suitable source is available. Do not start a fresh reverse-engineering investigation to resolve an unclear cell.
4. Write only new audit documentation and necessary narrow index links. Preserve history, negative evidence and published scientific meanings.
5. Check completeness of all 60 baseline IDs, broken/absolute-link issues in new files, duplicate IDs, contradictory proposed classifications, source provenance, encoding/prose, and consistency of labels and boundaries. Preserve test receipts and actual failures.
6. Submit the frozen contract and evidence to an **independent reviewer** under the repository's review protocol. Address REWORK in scope without asking for a fresh brief; never modify acceptance criteria without maintainer approval.
7. Package verified **complete and task-only diffs**, including untracked text; exact forward/reverse patch reconstruction and file inclusion/exclusion manifests; baseline/ending git status, protected-input hashes where applicable, test results, reviewer decision and suggested commit. **Do not stage, commit or push.**

No hard time/count stop for healthy authorized analysis. Preserve required disk guards, worker health, file integrity and STOP controls where relevant; do not introduce unnecessarily heavy new infrastructure. A genuine blocker (missing essential source, unsafe integrity condition or authorization) must be documented precisely with preserved progress and the minimum approval/input needed. Continue unrelated authorized work.

## 7. Frozen compact completion contract — AC1–AC8

**Task type:** Offline documentation and evidence-reconciliation research.  
**Question/deliverable:** What gaps remain after accepted research, and what concrete definition/Papyrus/game-configuration access routes do our existing findings establish?  
**Scope/bounds:** Existing repository research and provenance, limited targeted read-only interface/source verification, new audit documents and narrow index references; no live work, substantial new native investigation, protected-source edits, publication changes or Git integration.

**Mandatory acceptance:**

- **AC1 — Baseline and protection:** Actual initial provenance/status/permissions/protected-input state recorded; no protected source or unexpected workspace modifications.
- **AC2 — Complete 60-question reconciliation:** Every baseline question present exactly once in the crosswalk (with separately linked child gaps if needed), historical and proposed dispositions distinct, and primary citations supporting changes.
- **AC3 — Post-audit findings integrated:** Coordinate sufficiency, B1, BM1, BM2 and LO1 incorporated accurately; realized-production, geography/biome and active-membership boundaries stated without false reopening/closure.
- **AC4 — Concrete access-route taxonomy:** Representative capability-level matrix across subsystem families; three overlapping avenues distinguished; every asserted route tied to actual records, calls, settings or definitions; evidence classification and absence language correct.
- **AC5 — Papyrus accuracy:** Targeted API/event/property entries grounded in exact available declarations/registrations or marked unverified; native-only calls not mislabeled as Papyrus; `GetCurrentLocation()` semantics correctly separated from coordinates.
- **AC6 — Editorial boundaries and publication flags:** No SFSE/native-extension necessity claims or engineering implementation prescriptions; historical evidence untouched; publication and documentation issues distinguished from scientific gaps; clear reader guidance.
- **AC7 — Durable quality:** Answer-first report and navigable crosswalk/matrix, checked relative links, precise provenance and coverage, UTF-8/prose hygiene, documented negative and incomplete checks.
- **AC8 — Verification/review/delivery:** Reproducible validation with retained failures/corrections; independent reviewer ACCEPT against **these eight unchanged criteria** (or properly evidenced REWORK/ESCALATE when unfinished); verified complete/task-only reversible patches, manifest and integrity/status receipts, no staging/commit/push.

**Optional:** Provide an unimplemented suggestion for a public-facing access-capability index or a small concise FAQ; do not let optional polish delay closure.

**Negative-result closure:** A properly bounded absence of an observed interface is a valid documented result when the inspected surface and positive controls are reported. Never require proof that all unknown interfaces are impossible; never assert that an unexamined alternate avenue does not exist.

**Continuation authority:** Diagnose/correct/retest in-scope documentation, classification and verification failures under this assignment; reviewer REWORK does not need a new brief. Preserve original criteria and failure history.

**Exit/escalation:** Stop prohibited operations, any integrity-risking write or work requiring material new native/live investigation; retain the checkpoint and request only the minimum authorization or missing essential source. Do not relabel unfinished mandatory deliverables PASS.

**Disposition/reporting:** Return AC1–AC8 PASS/FAIL/NOT TESTED with primary evidence paths, scientific interpretation separately from tooling/safety/reviewer outcomes, explicit gaps and proposed dispositions, independent reviewer reference, full verified patch package and suggested commit. Maintainer must critically review before integration.
