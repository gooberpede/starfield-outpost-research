# RG2-A — Offline Live-Validation Preparation and Test Design

**Project:** `D:\Projects\starfield-outpost-research`  
**Investigated baseline:** Starfield.exe `1.16.244.0`, existing hash-pinned installed definitions  
**Authority:** Offline research, preparation and synthetic verification only. **No** gameplay, game launch, save mutation, native attachment, instrumentation deployment, Git stage/commit/push, upload or publication. B6 remains paused.

## Objective

Prepare a small, independently discriminating RG2-B live test of the accepted RG1 offline reconstruction of inorganic vein geometries. Compare **actual in-game spatial resource classifications and boundaries**, not just outpost-wide resource-name lists, against predictions frozen in advance. Include controlled Kreet and mature Save52 outposts, single- and mixed-biome cases.

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, and applicable provenance, rights and publication rules. Use accepted RG1 source and review under `docs/experiments/resource-geometry/`, prior local inorganic availability and resource-region dependencies under `docs/experiments/native-availability-map/`, geometry/biomes, and historical saved evidence. Preserve prior native observer NO-GO and interference findings. Do not reopen completed mechanisms without an actual counterexample.

## AC1 — Evidence and permission integrity

Record initial HEAD/index/status, qualified Starfield `1.16.244.0` executable and installed input hashes, RG1 evaluator/version pins, original/protected save identities and operation boundaries. All original saves, ESM/EXE/BA2, Ghidra databases, traces and protected evidence immutable. Project-authored offline code and documentation can be created. Third-party prior art is subject to source-specific rights and attribution; no third-party code/data copied without established permission.

## AC2 — User-facing save identification

This is **mandatory**: the in-game Load menu does **not** show `Save39`, `Save52`, `SOR-002`, `HIST-*`. For **every proposed case**, produce an operator-facing table:

- research identifier/aliases and SHA-256
- original **full `.sfs` filename**; exact source and protected-copy ledger
- **character name** as displayed by Starfield's character-select/Load interface
- **save kind** (manual/auto/exit/quick), displayed location, character level, date/time and playtime, with uncertainty/timezone indicated
- target outpost's user-facing name, planet, exact Workshop/beacon identity, and route from saved player location
- precise disambiguation if the Load menu has visually identical entries

Decode metadata or consult the protected provenance records; do **not** infer name, save type or menu label solely from filename or target outpost. Where fields genuinely cannot be established, mark UNKNOWN and propose a bounded identification step. Character names are allowed in operator instructions. Maintain identity by hashes, not casual string matching. **Save52 = HIST-0267**, **Save41 = HIST-0255**; a save header location reflects the player, not all its outposts.

## AC3 — Candidate selection

Assess these six initial candidates; choose **four primary** and **two reserves** (or justify specific replacements), ranked by independent information gain and safe test cost:

1. **SOR-002 / Kreet:** RG1 predicted Iron intersection, Alkanes absence.
2. **SOR-003 / Kreet:** independent nearby spatial geometry/frame contrast.
3. **Save39 / Kreet Research Lab vicinity:** RG1 predicted no Lead or Silver intersection.
4. **Save52/HIST-0267 — Feynman V Cu Co Ni IL:** mature **mixed-biome** case.
5. **Save52/HIST-0267 — Carinae III-a Rc Fe:** mature likely **single-biome** case.
6. **One other Save52 outpost:** reserve with compelling vein boundary or competition.

These are hypotheses/candidate contexts, not independently observed truths. Verify each outpost's ownership, beacon/source frame and biome context. Search historical manifests for SOR-002/SOR-003 original filenames; never invent their `SaveNN` aliases. RG1's three Kreet predictions cannot be generalized to Feynman/Carinae without qualifying their sources first.

## AC4 — Qualified, frozen spatial predictions

Extend RG1's **offline** source/geometry reconstruction to selected mature cases where existing operands allow. Before any live observation, prepare hashed immutable predictions tied to exact source/evaluator revisions and hashes:

- planet/terrain chart/fine-cell, beacon and source coordinate frame, local offsets and nominal **150-unit** circle
- all generated candidate vein geometry intersecting or near the circle, including paths originating beyond it
- resource identities, ordered competition, geometry intersection decisions and uncertainty
- selected sample positions **clearly inside**, **clearly outside**, and **just inside/outside** predicted edges; overlap/competition points if supported
- coordinate transformation from model to an operator- or native-queryable position, sample tolerances and potential Z/terrain dependencies
- explicit UNKNOWN when source inputs or geometric classification remain unqualified
- reproducible compact machine-readable tables and human-readable maps; avoid tracked proprietary or massive derived dumps

Freeze the predictions without fitting them to later live answers. Resource list agreement alone is **not** geometry validation. Where one mature frame cannot be qualified with current offline evidence, investigate concrete in-scope alternatives and report exact missing operands/authority rather than inventing a prediction.

## AC5 — Assess observation/oracle options and their safety

Compare (A) noninterfering observation of the game's naturally executing native region/point predicate with (B) manual hand-scanner patch and extractor placement observations, plus other **actual** supported interfaces. Each option must state what it measures, frame/loaded-state/epoch attribution, uncertainty, independence from RG1 assumptions, positive and negative controls, feasibility and risks.

Consult previous native availability, region dependencies, thread-control failure and observer interference/NO-GO documentation. Do not present existing debugger/Ghidra/SFSE machinery as qualified merely because it was previously built. Propose minimal additional instrumentation qualification *only if genuinely necessary*, for separate approval.

No actual Starfield launch, game load, process attach, debugger, injected observer, Creation Kit execution or game file modification in RG2-A. Offline synthetic tests allowed within published safety/output boundaries.

## AC6 — Prospective operator run cards

Provide run cards clearly marked **PROSPECTIVE — NOT AUTHORIZED**, one per primary case (reserve cards conditional). They must use **actual Load-menu labels including character name**, exact identity/hash and clear travel to the intended outpost, plus:

- preflight, unmodified save/no-action controls and outpost identity confirmation
- frozen predicted spatial points, directions and tolerances
- actionable observation steps; distinguish UI/scanner rendering or extractor footprint from true point membership
- captures, timestamps, naming, hashes, coordinates/frame, load/refresh epochs
- explicit positive, negative and near-boundary comparisons
- nominal footprint versus POI-clipped usable build area
- abort/STOP conditions, save protection, restoration and permission gates
- PASS / MISMATCH / INDETERMINATE outcomes without post-hoc prediction changes

Avoid requiring six live sessions by default; choose no more than four primary tests unless a concrete need emerges.

## AC7 — Durable answer-first package

Create `docs/experiments/resource-geometry-live-prep/` (or existing conventions) with:

- `report.md` — concise status, selected experiments, strongest oracle, actual limitations
- `save-selection.md` and structured identity table
- `case-selection.md`
- `prediction-contract.md` and version/hash-indexed predictions
- `observation-options.md` with past unsafe paths and qualified alternatives
- `run-cards.md` (prospective)
- `review.md`, source/verification records and minimal navigation updates

Document supported installed data versus inferred mechanism versus **unobserved runtime equality**. Use consistent hexadecimal/offset notation and clear project-local analysis labels. No publication status change and no scientific promotion from hypothetical predictions.

## AC8 — Independent review and exact delivery

Run relevant RG1 and new evaluator/math tests, frozen prediction integrity checks, source/hash/identifier and link/encoding checks, protected-input preservation and package reconstruction. Have an independent reviewer inspect original AC1–AC8, primary evidence, actual changed tree, candidate selection, ability to find saves in the Load menu, source qualification, geometry discrimination, oracle safety and run-card permission gates. Fix REWORK within same authority and preserve history. Report actual ACCEPT/REWORK/ESCALATE without claiming unrun tests passed.

Return verified **complete and task-only `.diff` files**, inclusion/exclusion inventory, exact patch reconstruction receipts and independent verdict for maintainer critical review. Nothing staged, committed, pushed or uploaded.

## Completion and escalation contract

- **Task type:** offline scientific preparation and test-design with bounded original evaluator work.
- **Mandatory results:** AC1–AC8. No live confirmation claimed.
- **Negative closure:** a real unavailable source/oracle requires detailed attempted alternatives and smallest actionable blocker; speculative exceptions are not enough.
- **Continuation:** investigate and correct ordinary in-scope failures, retest and resubmit independently without requiring a new brief.
- **Safety:** stop only actions outside authority or at genuine integrity/resource limits; preserve checkpoint, errors and protected inputs. Existing drive-space/worker/STOP constraints apply; do not impose arbitrary healthy-run time quotas.
- **Next authorization:** RG2-B needs separately approved live operator/instrumentation run cards; reviewer acceptance never grants live, Git or publication permission.
