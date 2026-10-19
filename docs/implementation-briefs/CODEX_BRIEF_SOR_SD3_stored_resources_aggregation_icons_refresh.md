# SD3 — Locations Stored Resources: source attribution, aggregation, icon provenance and refresh

**Project:** `starfield-outpost-research`  
**Assignment:** bounded offline native / installed-definition / compiled-UI / save investigation  
**Issued:** 2026-10-19  
**Integration gate:** independent review, then maintainer critical diff review; no automatic commit or synchronization

## 1. Question and objective

Determine **exactly what the Locations database's selected-outpost *Stored Resources* list reports**: how the selected outpost is resolved, which inventory or other data sources qualify, how item identities and quantities are collected/filtered/grouped, how remote/unloaded state and refresh work, and **where each displayed resource icon originates and how its asset is selected**. Follow the installed game's actual data flow, without assuming it simply sums containers or uses the same sources as crafting.

**User scope refinement:** pagination, scrolling, navigation animations, button/key handling, menu layout and other *UI mechanics* are **out of scope**. Limited compiled UI examination is authorized to establish the data-provider contract, item/quantity/name/icon bindings, presentation-relevant filtering/ordering and refresh—not to reverse-engineer the entire Locations screen. Icon provenance is mandatory even though UI mechanics are excluded.

SD3 follows accepted S1/S2 (industrial inventory and output links), SD1 (ordinary chests, display references, mannequins) and SD2 (Shared Outpost Storage and crafting/construction source walkers). Reuse established findings with their original confidence boundaries; **do not equate Stored Resources, crafting availability and industrial input availability**.

## 2. Context, protections and preparatory work

Read current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md`, `THIRD_PARTY_POLICY.md`, `docs/templates/completion-contract.md`, `docs/RESEARCH_STATE.md`, `docs/BACKLOG.md`, appropriate subsystem pages and accepted S1/S2/SD1/SD2 source pins/reviews. Respect current repo policy if a procedural detail here is underspecified; report any material conflict before acting. Revalidate installed executable/ESM/compiled UI/script identities, version-dependent native locators, approved decoder qualifications, and source/provenance constraints. Never silently inherit unverified offsets.

Use the authorized mature-save corpus broadly and deliberately, not Save52 alone. Record accessible/unsupported/missing saves, item decoding coverage and input hashes. Preserve all original saves/game binaries/scripts/assets unchanged, including backed-up evidence; compiled assets remain **LOCAL-ONLY**. The user-supplied **Schrod II Ad Locations screenshot**, showing a mixed list of inorganic, organic and manufactured resources, is a *UI observation*, not an automatically joined save state. Do not fabricate contemporaneous inventory totals or attribute the screenshot to an arbitrary historical save.

## 3. Bounded research workstreams

### A. Selected outpost and provider chain

Locate the actual *Locations → selected outpost → Stored Resources* data provider across compiled UI, engine, native services and scripts as applicable. Trace selection identity (location/outpost/beacon/Workshop reference and ownership), lookup or registry, lifetime, and invocation of the row producer. Trace from source producer into the specific bound item/quantity/icon fields the UI consumes. Record exact executable functions, compiled-UI linkage, symbols/forms/keywords/actor values and negative controls, with source pins. Distinguish a screen label from the authoritative provider; avoid inferring semantics from strings alone. Scope surrounding Locations functionality only as needed to resolve identity and data delivery.

### B. Inventory membership and explicit exclusions

Establish the **ordinary inclusion predicate**, not a mere list of search hits. Trace the enumeration root, qualification tests, reference liveness/ownership/location conditions, any separate resource registry, and whether inventory stacks are consulted at all. Explain each category as **included / excluded / conditional / unresolved**, naming the exact branch or counterexample:

- Solid, liquid, gas and warehouse storage (all relevant capacities);
- extractor output buffers, greenhouse, husbandry and fabricator outputs;
- incoming and outgoing cargo-link compartments, Transfer Containers;
- ordinary chests and lockers;
- weapon/display cases, racks, loose displayed-item references and mannequin actor inventories;
- physical Shared Outpost Storage fixtures **versus** SD2's player-held backing inventory;
- player inventory, selected ship cargo and any otherwise eligible remote inventory.

Distinguish membership in a Workshop from crafting eligibility (`OutpostBuildContainer`), S1 output-link eligibility and SD2 shared-storage substitution. Those are known *possible* tests, not assumed database rules. Avoid false duplicate contributions caused by PackIn children, repeat handles, display inventory plus mounted reference, or many Shared Outpost Storage access fixtures. Establish whether outposts without a valid active beacon or with unloaded/inaccessible references can contribute; apply the project's proven active-membership limitations rather than inventing a completeness proof.

### C. Item and quantity semantics

Identify whether displayed numbers are stack *counts*, total mass, available-for-use counts, cached production counts or another actual quantity. Trace base-item identity, condition for qualifying as a resource, item category keywords / list filters, default versus added inventory, item instances with different extras, merged forms, repeated source references, zero/negative/absent rows and duplicate suppression. Establish the effective grouping key and quantity arithmetic as implemented. Explain treatment of individual modified or stolen items *only insofar as it affects the row count/filter*. Inspect names, localization selection, and item ordering only where they are part of the provider's output data contract (not paging/sorting controls). Give precise negative contrasts: an inventory that exists but is excluded, or an item physically present but absent from the list, where evidence supports one.

### D. Resource-icon provenance (mandatory, bounded)

Trace **the per-row resource icon from item identity to the actual image or atlas entry**. Determine whether selection derives from a form field, resource-class keyword, icon string/path, UI symbol mapping, texture path, material, inventory icon renderer, or other installed mechanism; use real paths and conditions. Resolve the installed asset source (e.g. actual BA2/resource archive or compiled-UI embedded asset) and the lookup/fallback behavior for items missing an icon or unsupported classes, to the extent the mapped provider uses it.

At minimum give reproducible **item FormID / class → icon selector → referenced asset identifier/path → containing installed asset** examples for representative inorganic, organic and manufactured resources (e.g. examples from the screenshot where actual evidence permits). If the game dynamically renders icon portraits rather than looking up static textures, demonstrate that pipeline and its input instead of inventing filenames. Distinguish shared category glyphs from unique per-item imagery and localized labels. No wholesale UI artwork extraction, icon remastering or general asset-catalogue project. Existing game images and extracted raw assets are LOCAL-ONLY; do not embed proprietary binary imagery in tracked documentation.

### E. Freshness, unloaded outposts and update signals

Trace initial list construction, stored aggregate lifetime (if any), dirty/invalidation events, explicit requests, inventory mutation callbacks, remote reference resolution and reload/update conditions. Separate **underlying inventory update**, **aggregation/cache update**, and **UI repaint**. Distinguish a background producer whose inventory changes from a menu that has not refreshed. Investigate when the player is far from the outpost, on another planet, or viewing an unloaded Workshop, within the actual native/script paths. State precisely what is STATIC-derived versus demonstrated by captured saved/runtime observations. Don't imply remote cargo voyages replay during waits (C3's existing boundary). If settled current-value behavior cannot be proven offline, describe a single minimal discriminating *proposed* live test, **not executed**.

### F. Saved correspondence and contrasting consumers

Find a representative populated outpost with positive identity and inventory-reference joins, preferably across multiple inventory classes. Decode several exact item identities and quantities in a qualified save; where possible show a **mixed-source include/exclude case** that discriminates candidate predicates. Do not require exhaustive decode of every historical inventory or SD2's still-unresolved player-held shared backing contents merely for an otherwise supported provider finding. If a mandatory semantic claim *does* turn on those bytes, diagnose the acquisition path within authority or classify unresolved rather than guessing. Preserve date/snapshot pairing and distinguish an observed UI total from reconstructed saved-source totals. Compare Stored Resources' actual population explicitly with (1) SD2 crafting/research source availability and spending and (2) E1–E3/S1/S2 industrial input/output availability; do not redo those subsystems.

## 4. Deliverables

Create `docs/experiments/stored-resources/` (or justify a repository-consistent alternative):

- `plan.md`: frozen hypothesis/controls, authorized inputs/version pins, selected tests, limitations, stop/escalation.
- `report.md`: answer-first causal summary, claim-level confidence/basis/coverage, honest unknowns.
- `provider.md`: selected outpost identity and complete source-to-row data contract, native/compiled-UI chain.
- `membership.md`: comprehensive ordinary source-inclusion matrix with predicate, comparison control and qualification for each category listed above.
- `aggregation.md`: item filtering, identity, grouping/count arithmetic, zero/duplicate handling and producer refresh/cache semantics.
- `icons.md`: icon selector, source archive/assets and representative exact identity-to-asset joins with fallbacks and evidence; no raw copyrighted assets.
- `saves.md`: corpus census, qualified decoding, representative positive joins, failures, screenshot non-joins and coverage.
- `review.md`: original eight-criterion matrix, independent reviewer disposition and actual test, evidence, provenance and patch receipts.

Concise CSV function/source/asset/case registers where useful; no indiscriminate dumps. Update relevant subsystem pages, `docs/BACKLOG.md`, `docs/RESEARCH_STATE.md`, and `docs/implementation-briefs/README.md` proportionately. Link primary evidence alongside claims. Keep provenance/rights classifications separate from scientific confidence and integration approval.

## 5. Scope, authorization and safeguards

**Authorized:** offline read-only inspection of permissioned installed game definitions, executable, Papyrus and compiled UI/asset mapping, original historical saves and existing repository results; disposable derived tests/helpers, bounded qualified decoders, documentation and independent review. In-scope diagnosis, corrections and requalification are part of this assignment. Offline extraction of minimal asset *metadata and source paths* is allowed under project provenance/rights rules.

**Not authorized:** Starfield launch, gameplay, live observation, attach/debug/inject/instrumentation, user gameplay instructions as an executed experiment, new captures/saves, active or historical original save mutation, deployed mods, installed-game modifications, third-party asset redistribution, destructive cleanup, staging, commit, push, publication or service actions. Do not silently broaden into Locations UI pagination/navigation/layout, the entire inventory interface, general icon rendering/texture extraction, SD1/SD2 duplication or cargo/production simulations.

Honor actual repo protected-input and hash identity checks, writer/worker teardown, both-drive disk guards (including applicable 40,000,000,000-byte minimums), STOP conditions and output/evidence retention. Preserve failing runs. Don't introduce arbitrary healthy-science time/sample ceilings as exit criteria. Material new limits or live operations require maintainer approval. If an authorized needed source is inaccessible or a required live experiment is indispensable, preserve progress and escalate the *specific* blocked condition; continue independent authorized work.

## 6. Compact completion contract — eight mandatory frozen criteria

**Task type:** bounded scientific discovery/reconstruction plus documentation, offline-only.  
**Question/deliverable:** Explain what Stored Resources counts, why it counts those sources, how the displayed quantities and resource icons are obtained, and how remote changes become visible, grounded in the actual provider and saved examples.  
**Scope/bounds:** Sections 2–5, governing repository policies, immutable originals, explicit live/deployment/Git/publication prohibitions.

**Mandatory acceptance (freeze before execution; material change requires maintainer approval):**

1. **Provider and selected identity:** Demonstrate actual Locations Stored Resources row provider and selected-outpost resolution, native/compiled-UI data path and real source pins, with a discriminating non-provider control.
2. **Ordinary inclusion predicate:** Explain actual source enumeration and membership conditions; provide category-by-category include/exclude/conditional/unknown matrix for **all** listed inventory populations, with native predicates and counterexamples or explicit bounded uncertainty; don't assert a complete rule from name matches alone.
3. **Aggregation semantics:** Trace item admission/filtering, item FormID/group key, quantity calculation and duplicate/zero treatment into displayed number/name fields, including at least one differentiated negative case, with honest coverage of exceptional item instances.
4. **Resource icon provenance:** Trace actual per-row icon selector and asset/render source through installed data with positive reproducible item/class-to-asset (or documented dynamic-render) joins for inorganic, organic and manufactured examples, including known fallback behavior or explicit bounded absence; no general UI mechanics investigation.
5. **Refresh and remote:** Trace when the list is constructed, which caches/dirty events/refresh calls govern source and row freshness, and the unloaded/remote access boundary as far as actual native/script paths permit; mark unobserved live timing as unknown rather than presumed current.
6. **Save and cross-system corroboration:** Qualified broad historical search and at least one positive item-level saved-outpost source join **if accessible and representable**; mixed-source evidence or documented discriminating bounds; screenshot appropriately qualified; comparison with SD2 crafting/shared storage and industrial availability. A genuinely unsupported or absent positive witness requires documented exhaustive *qualified bounded* coverage and the precise minimal proposed next test, not fabricated numbers.
7. **Scientific quality and boundaries:** Answer-first report, original source version/provenance and function/asset pins, competing hypotheses/counterexamples, reasonable engineering confidence, explicit negative-result coverage, SD1/SD2 reuse and no UI paging/layout analysis or undocumented expansions.
8. **Evidence integrity and independent review:** Original/protected file identity/hash and free-space safeguards; deterministic tests including icon/provider mapping checks where feasible; malformed prose / spacing / UTF-8 audits; preserved initial failures and fixes; all eight PASS/FAIL/NOT TESTED with evidence references; independent original-criteria reviewer of actual final revised snapshot and `ACCEPT` / `REWORK` / `ESCALATE`; verified applicable forward/reverse **complete and task-only** diffs including untracked text, manifests, status and inclusion/exclusion inventories; nothing staged, committed or pushed.

**Optional:** extra saved witnesses, wider icon classification inventory, standalone read-only diagnostic, or a proposed controlled live run card. Optional achievements do not compensate for a failed mandatory criterion.

**Scoped negative-result closure:** An asserted exclusion or absent caching/sharing mechanism requires bounded inspection of the actual provider/consumer and controls; lack of a matching string, unsupported save header or missing object in one save is not sufficient. A supported scoped negative is a valid finished scientific outcome. Engineering test failures require continued correction, not relabelling as research limitations.

**Continuation authority:** Investigate, correct, retest, independently review and requalify in scope without new briefs; frozen mandatory criteria stand unless maintainer amends them. Preserve failures, checkpoints and counterexamples. No live/Git/publication authority is implied.

**Exit/escalation:** Halt unsafe operations on protected hash drift, identity/disk guard failure, process teardown fault or actual integrity risk; retain receipt and seek narrow recovery approval. For inaccessible essential sources or required unauthorized live confirmation, document exact missing input, attempted feasible offline routes and next permitted checkpoint. Continue unrelated safe work. Follow the research-execution protocol on healthy continuation and real resource/session exhaustion.

**Review outputs:** Original eight-criterion PASS/FAIL/NOT TESTED matrix with paths/grounds; separate scientific, instrumentation, safety, review and publication status; primary evidence and failed-case ledger; independent verdict; complete/task-only patches with exact reconstruction checks; source rights/provenance and file inclusion manifest. Return an unstaged package and suggested commit message only.

## 7. Expected Codex return

Provide the strongest actual mechanism findings first; eight criteria and independent verdict; important remaining unsupported or live-only questions; original-input/asset/prose and test receipts; report/review paths and exact verified complete/task-only diff paths; suggested commit message. Return for maintainer review, **do not integrate**.
