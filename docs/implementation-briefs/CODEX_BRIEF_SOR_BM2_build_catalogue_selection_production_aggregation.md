# Codex research brief — BM2: Build catalogue, selection, eligibility and production aggregation

**Project:** `starfield-outpost-research`  
**Assignment:** BM2 — bounded offline scientific research and documentation  
**Status:** Proposed for maintainer-authorized execution; not a claim of results or authorization for live actions  
**Purpose:** Map Starfield's **general Build Mode catalogue and selection machinery**, including how construction options become visible, selectable, locked or rejected; what governs catalogue population and limits; and how independently scheduled producers contribute to a single displayed production rate. This is foundational research into installed mechanisms, **not an exhaustive construction catalogue or a brief to build a mod**.

## 1. Central questions and acceptance philosophy

Trace the ordinary end-to-end route:

**Installed definitions → discovery / registration → category and sub-item grouping → visibility and eligibility → selected candidate and item card → Build Mode command → existing validation / construction operation.**

Recover the *mechanisms* and decision points, not a list of every item's unlocks. The intended outcome is that a technically competent reader can answer questions such as: What existing avenues can hide or lock a construction option? How can sub-items such as beds, tables and chairs be organized and selected? Can the catalogue have 1,000 or 2,000 items, and what are its actual structural limits? Which parts of Build Mode presentation are definition-driven versus native/compiled-interface dependent?

Also establish, consolidate and independently check the existing native explanation for aggregation of multiple producers with different intervals into a single nominal **N/min** statistic. Do **not** make exact realized inventory growth, a flawless scheduling simulator or live production monitoring prerequisites.

Treat the previous findings as evidence to test and reuse, not conclusions to re-derive unnecessarily. Reasonable engineering confidence and explicit scoped negatives are acceptable; speculative alternate implementations without concrete evidence are not mandatory blockers.

## 2. Research workstreams

### A. Catalogue discovery, hierarchy, sub-items and actual bounds

1. Identify the installed construction records and the authoritative discovery/population route for ordinary outpost Build Mode. Trace menu-root membership, category/subcategory organization, recipe-to-constructible-form links, sorting and registration/override effects. Distinguish **definitions eligible for discovery** from **objects actually present in the current menu**.
2. Determine whether beds, tables, chairs and similar visually grouped choices are nested subcategories, lists or filters over recipes/forms, alternative candidates in a carousel, or another native/compiled UI structure. Trace at least one genuine sub-item example end-to-end and compare it with an ordinary distinct top-level entry. Differentiate catalogue sibling selection from BM1's **CHANGE** of an existing placed component.
3. Identify constraints on number of categories, groups, candidate entries and options. Investigate actual arrays/containers, counters, field widths, compiled interface expectations and relevant limiting checks. If limits are dynamic, explain their bounded allocation/growth and the distinction between **no observed fixed cap** and **unlimited capacity**. Do not claim a numeric ceiling based on a sampled count, memory speculation or an unexecuted stress test. If a meaningful fixed upper limit is present, locate its enforcing consumer. A bounded census can validate completeness of an examined source population; it is not a required exhaustive item-by-item unlock inventory.
4. Check whether expansion/plugins or changing load order can add/override records through the ordinary discovery route. Establish minimum required relationships and clearly separate existing native support from untested third-party customization.

### B. Availability and unlock mechanisms

Produce a **taxonomy of actual eligibility mechanisms**, explaining where evaluated, against which subject/context, and with what visible or construction-admission outcome. Investigate relevant existing examples of:

- Perks and ranks, including compound conditions and AND/OR semantics where evidenced;
- completed research and quest stages, progression/global variables and script-adjustable state;
- location, planet/environment, faction or other contextual conditions where installed examples exist;
- prerequisite constructions / current Workshop state, if supported;
- resource/material availability and ingredient sourcing;
- category quota / Build Limit / placement or territory rejection;
- explicit menu suppression, locked-but-visible presentation and later candidate denial.

These are **candidate avenues**, not a presumption each is used by the installed ordinary catalogue. Differentiate **absent/hidden**, **visible but unavailable**, **selectable but rejected at preview or placement**, and **successfully constructed**. For a mechanism without a qualifying installed exemplar, report bounded negative coverage or unknown, not invented capability. Explain how scripts can change condition operands without assuming scripts are a native catalogue API.

**Reuse** SD2 prerequisite tracing, L1 numerical gates, L2 build budget, L3 placement and BM1 variants; independently trace only missing catalogue-side orchestration and consequences. Do not conflate arbitrary material shortages with an item being definition-locked.

### C. Selected item, object card, feedback and UI scaffolding

Trace the principal installed interface asset(s), native providers/controllers, candidate descriptors, data binding/serialization and selected command callbacks needed to explain catalogue population and selection. Recover how the selected option obtains its name, icon/preview, category, build requirements, relevant cost/limit and operational descriptors (power, production etc.) where available. Explain significant refresh/invalidation routes for changed resources/conditions and distinguish initial population, display update and authoritative construction-time revalidation.

Provide the **general architectural scaffolding** only. Do not reverse-engineer the entire Scaleform-like runtime, pagination animations, camera, controller input system, complete UI style rules, localization catalogue or snapping/placement system. Trace the selected item far enough to identify the actual construction request and its handoff to already-established Workshop/L1–L3 machinery, rather than redoing low-level placement validation.

**Footer only where a real gap remains:** verify the precise counted entities for Cargo and Crew; finish ordinary footer outpost-name and planet/system-caption data binding if feasible. Reuse already traced Power, Build Limit, Integrity and production display bindings without reopening their basic calculations. Record evidence and limits for refresh epochs/overrides rather than asserting live timing without observation. Leave the distinct Locations/Outpost screen for its separate field coverage pass.

### D. Production stacking — a specific compulsory cross-check

Reexamine the existing accepted E1–E3, P1 and Build Mode coverage sources, and reproduce the ordinary **per-producer normalization and accumulation** in native code. Address explicitly:

- Which producer registration population is walked, and how inorganic, atmospheric, organic and manufactured producers enter it; what classes are excluded;
- the relevant effective interval, quantity/resource actor values, perks/modifiers and cached eligibility predicates;
- whether each producer's nominal `quantity * 60 / interval` (or different recovered expression) is computed separately then accumulated, with an **actual native expression and numeric types**;
- why asynchronous or noncommensurate production intervals do not require synchronization before addition;
- accumulation/rounding, output units, and the pathway to the Build Mode footer and Locations value, with decimal presentation distinguished from numerical total;
- whether the sum spans different output products indiscriminately, and how stalled/unsupported/full/damaged/underpowered producers differ between cached **nominal** and actual delivered output.

Provide one independently reproducible **mixed-producer worked example** grounded in actual installed definitions or positive saved registrations, showing each included term and the sum. Where current effective modifiers, runtime cache states or saved values are unavailable, distinguish a *definition-grounded illustrative calculation* from an *observed historical live total*; never manufacture a live measurement. If an existing calculation already decisively answers a subquestion, cite and verify rather than reconstruct a new scheduler. Actual production throughput verification and detailed remote catch-up remain **deferred**.

### E. Extensibility boundaries and persistence as relevant

Explain the minimum record, recipe, category/group, condition and asset relationships necessary for an ordinary new catalogue entry or sub-item to become discoverable and selectably constructible. Distinguish **definition-driven**, **script-assisted**, **native/compiled-interface-dependent**, and **unknown**, grounded in installed consumers rather than assumptions. Identify any saved state that affects eligibility (e.g., progression, selected Workshop state) and whether catalogue data itself is rebuilt rather than serialized. Use the historical mature-save corpus selectively for actual useful membership, prerequisite state and selected-source corroboration. Do not require a contrived persistent 'menu catalogue' save record.

## 3. Representative controls and evidence method

Select **mechanism-diverse controls**, not a complete object catalogue: ordinary storage or furniture, a bed/table/chair group, an extractor or fabricator, a hab, Shared Outpost Storage (multi-perk case), one research/quest-gated choice, and at least one rejected or hidden candidate with identifiable reason. Replace individual cases if the installed population suggests better discriminators, documenting the choice. Use actual ordinary records/paths and explicit negative controls. Contrast BM1's already-placed wall change against preconstruction option selection without rerunning BM1.

Read relevant current sources first, including `docs/audits/outpost-coverage-2026-10/build-mode-and-locations.md`, BM1 `docs/experiments/construction-variants/`, SD2 `docs/experiments/shared-outpost-storage/`, E1–E3, P1, L1–L3, and `docs/EVIDENCE_STANDARD.md`. The preceding audit predates BM1; do not perpetuate obsolete 'untraced CHANGE' language. Verify versioned native pins on the installed executable before reuse and preserve exact definition identifiers. Use installed compiled interface/game records/scripts read-only; respect game-derived material restrictions and source provenance.

Present hypotheses as hypotheses until corroborated. Preserve positive evidence, bounded negatives, counterexamples, source/version hashes and any relevant historical save joins. **Do not infer dynamic population ceilings from a finite census**. Do not demand a hypothetical fully universal negative proof when a scoped ordinary result is supported. If a meaningful essential test cannot be done offline, preserve the attempted routes and propose the smallest next observation requiring separate authorization; continue independent in-scope analysis.

## 4. Required deliverables

Create a durable research package at `docs/experiments/build-catalogue/` (adapt supporting filenames to repository conventions):

- `report.md`: **plain-English answer first**, conclusions and precise limits, meaningful research implications, coverage, confidence and clear distinction between installed capability and possible extension.
- `catalogue.md`: end-to-end discovery, grouping, sub-item selection, ordering, selection/admission path, actual population-limit evidence, structural diagram/table and concrete exemplars.
- `eligibility.md`: mechanism/condition taxonomy, hidden/locked/rejected states, context, source pins, positive and negative controls and practical extension boundaries.
- `ui.md`: bounded native-provider/compiled UI architecture, selected-candidate card, major refresh and handoff semantics; footer cargo/crew/name/body gaps where supported.
- `production.md`: independently reconciled native aggregation expression, producer inclusion, units, eligibility, numerical example, formatting and nominal-versus-realized caveat.
- `extensibility.md`: data/script/native dependencies for adding entries, categories/sub-items, assets and restrictions, with nonoverclaimed capabilities.
- `sources.csv` (and function/definition registers as needed): exact versioned primary source/record locators, evidence classification, and concise coverage/control inventory.
- `review.md`: frozen acceptance matrix, all tests/corrections, independent reviewer report, scope/integrity and patch receipts.

Update relevant index/backlog/research-state **cross-references only**, retaining original scientific history and statuses; no release cleanup or refactoring of old experiments. Prefer clear prose and tables over enormous raw record dumps. Explicitly validate UTF-8, spacing, prose formatting, links and generated tables (recurring malformed-prose issue).

## 5. Frozen compact completion contract — AC1–AC8

**Task type:** bounded scientific research and documentation. **Question:** What installed catalogue, grouping, selection, eligibility, production-aggregate and presentation machinery exists in ordinary outpost Build Mode, and what are its evidenced limits?

**Scope/authority:** Offline read-only analysis of protected saves, installed records, scripts, executable and UI assets under existing project access/source rights; creation of bounded research documentation, verification outputs and task-local offline analysis is permitted. No Starfield launch, process/debugger attach, observer, live gameplay, save/ESM edits, deployment, third-party redistribution, publication, staging, commit or push. Obey `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, third-party/provenance/publication rules and applicable input-integrity/disk guards.

**Mandatory acceptance criteria (freeze on execution):**

- **AC1 — Baseline and bounded controls:** Current reviewed prior-work dependencies identified; installed version/source pins and sufficiently diverse real controls selected, inclusion/exclusion inventory and actual relevant corpus coverage recorded. No invented or exhaustive unlock catalogue.
- **AC2 — Population and grouping:** Native/definition/compiled-UI discovery and category/subcategory/sub-item selection mapped end-to-end, including a bed/table/chair-type case; candidate ordering and genuine structural limits or qualified lack of detected fixed caps explained without conjectured ceilings.
- **AC3 — Availability taxonomy:** Supported avenues to hide, lock, enable and later reject a candidate traced with actual contexts, conditions and representative exemplars, distinguishing unconfirmed hypothetical mechanisms from positive installed support and reusing SD2/L1–L3.
- **AC4 — Candidate and UI handoff:** Real selected-entry description, recipe/asset/cost and request path mapped through native provider and relevant compiled UI scaffolding to ordinary construction admission; key refresh distinctions and footer cargo/crew/name/body fields investigated within the agreed bounded scope.
- **AC5 — Production aggregation:** Consolidated **actual native expression**, producer-type eligibility, independent per-producer interval normalization, accumulation and precision/formatting; reproducible mixed-type numerical example appropriately labelled, with nominal versus delivered-rate distinction and no demand for a new production simulator.
- **AC6 — Extension and persistence model:** Evidence-based minimum relationships for additional entries, grouping and restrictions, separate selected preconstruction options from BM1 placed variants, and explain pertinent saved versus reconstructed state; bounded native/ship/external dependencies, no prototype mandated.
- **AC7 — Evidence and readable research outputs:** Required durable reports/registers, concrete positive/negative source evidence, explicit confidence/coverage/limitations, failed approaches retained, no unsupported universal absence or runtime claims; proofreading/UTF-8/link validation and coherent concise report.
- **AC8 — Integrity, reviewer and delivery:** Protected input identity/hash checks, permissions and applicable safeguards; independently executed review against original AC1–AC8 with `ACCEPT` / `REWORK` / `ESCALATE` and criterion-by-criterion `PASS` / `FAIL` / `NOT TESTED`; failures/corrections documented; validated complete and task-only diffs (including new untracked text), exact forward/reverse reconstruction, status and inclusion/exclusion manifests and verification receipts. Nothing staged, committed or pushed.

**Optional (not acceptance blockers):** exhaustive catalogue item/unlock census; live UI refresh timing; runtime stress-testing 1,000/2,000 candidates; source-code changes or example plugins; definitive every-variant compatibility; exact live realized throughput; general Scaleform internals.

**Negative-result closure:** A scoped, properly evidenced absence of a specific category, hard cap or restriction is legitimate; state population and mechanisms checked, actual alternatives, and residual unknowns. Do not infer infinite capacity or universality from absence of a fixed bound. A failed mandatory test is unfinished and requires in-scope correction/review, not a relabelled success.

**Continuation authority:** Diagnose, correct and rerun in-scope offline work and reviewer-identified defects under the same assignment. Freeze criteria; obtain maintainer approval for material changes. Preserve checkpoints, evidence and previous failures. No automatic arbitrary time/volume/cadence cutoff on a healthy run; justified safety bounds remain controlling.

**Escalation:** Stop only an unauthorized, unsafe or genuinely blocked operation; record exact blocker, attempts, evidence, smallest required user action or permission, and resume point. An inaccessible essential archive, integrity/hash mismatch or failed disk guard must not be bypassed. Continue independently authorized work when possible.

**Review disposition:** Implementer cannot self-accept; independent reviewer inspects original contract and primary records, requests in-scope REWORK if necessary, and reports independently accepted scientific coverage distinct from actual runtime validation or publication clearance. Integration remains maintainer-controlled.

## 6. Return-to-maintainer summary

Return a concise substantive findings summary, the original eight-criterion matrix, verified complete and task-only patch paths and manifest, exact untracked/staged/unstaged status, integrity findings, review verdict, remaining *material* uncertainties, and a proposed commit message. **Do not commit or push.**
