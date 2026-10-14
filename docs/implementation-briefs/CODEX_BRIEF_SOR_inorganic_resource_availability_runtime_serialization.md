# Codex Research Brief — Outpost Inorganic Resource Availability: Runtime Oracle, Serialization, and Reproduction

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)

**Status:** Authorized for offline research and implementation within the limits below. **No Starfield launch, live attachment, SFSE deployment, game-save modification, staging, commit, push, or publication.** Return the results for maintainer/ChatGPT critical review.

## 1. Starting point and scientific purpose

Continue from the committed and synced repository HEAD, not from a hypothetical clean-room recreation. Read `WORKFLOW.md`, the Research Execution and Completion Protocol, current research state/backlog, source/permission registers, relevant save-reader and extractor-membership work, and installed resource-reference research. Verify actual files and revisions; do not assume every historical path is still present.

This is a study of **Starfield's outpost system**, not merely an Outpost Tracker importer or a speculative Outpost Planner feature. Investigate runtime calculation, persistence/serialization, and deterministic reconstruction as distinct but related scientific objectives. Produce technical findings useful to other mod authors and researchers, while keeping protected/proprietary evidence private.

The motivating in-game reference is the **Available Resources** display while an outpost beacon is *unplaced* and being moved around in prospective build mode. A supplied screenshot showed Iron, Alkanes, and Helium-3. This establishes a player-facing candidate-site resource set before an outpost or extractor is placed; it **does not** establish that a single native function returns the whole set, or that the UI itself checks every extractor's placement eligibility.

**Primary question:** For a prospective or established outpost site, which **inorganic** resources are locally available for extraction within the effective outpost area, and how does the engine produce or retrieve that set?

For this research, a resource is **locally available** when an appropriate extractor could be validly placed somewhere in the effective site/build area over that resource under the relevant resource-location rules, abstracting away shortages of materials, power, skill/unlock conditions, and unrelated build requirements. Examine whether the game UI's preview semantics match this operational definition; do not silently equate them if they differ. Even a small intersecting resource patch can qualify if it supports a valid placement. Do not confuse planetary resource population, biome resource population, local availability, build-menu visibility, and currently operating extractors.

## 2. Mandatory parallel research tracks

### A. Runtime/UI/native behavior — first-class priority

- Trace the unplaced beacon's **Available Resources** UI data backward through menu/Scaleform/Papyrus/native interfaces as evidenced by the installed version. Determine the producers and update triggers, effective prospective center/radius, resource identity representation, caching/invalidation, and whether moving the preview recomputes the set.
- Trace the corresponding behavior for an **established** outpost: whether it uses the same algorithm, a cached set, different inputs, or another API; account for beacon relocation versus durable Workshop-center placement where relevant.
- Investigate terrain-resource eligibility, extractor placement constraints, relevant native record types, and the roles of resource deposit/vein data without making complete vein geometry a prerequisite unless demonstrated necessary.
- Determine if the resource-set UI is a direct authoritative result, an aggregation of per-resource tests, or another mechanism. Record exact supported function/record names, addresses/RVAs for the pinned binary where appropriate, inputs, outputs, callers, and confidence.
- Investigate accessible Papyrus or modding API surfaces if available, and distinguish publicly documented signatures from independently verified retail-game behavior. Do not assume a convenient API exists solely because the UI displays the result.

### B. Save and installed-record representation — equal scientific legitimacy

- Examine controlled saves (including beacon-only stages), Save25/26/27/28 where relevant, mature Save52, and their qualified Workshop/body/site associations. Determine whether a resource set is explicitly serialized, cached, or reconstructible from sufficient saved state, and whether the absence of an obvious field is meaningful.
- Use the previously established **848 supported construction roots**, 63 recognized extractors and resource associations as **positive controls**, never as the availability population itself. An extractor's existence can support historical availability but cannot establish what other resources were available without extractors.
- Distinguish actual construction eligibility and resource location from installed `IRES`/`COBJ`/extractor definitions. Treat records and identifier domains carefully (base, small/medium plugin, runtime, saved dynamic IDs).
- Preserve negative and ambiguous save evidence and establish whether the relevant resource-set producer acts only on generated/live terrain state omitted from save serialization.

### C. Independent model and validation

- Implement a deterministic **offline resource-availability evaluator** where recovered native dependencies and available inputs make that scientifically supportable. Do not invent a full evaluator by using planetary resource lists or extant extractor counts as a proxy.
- If complete offline evaluation genuinely requires an absent terrain/runtime operand, deliver independently runnable **partial calculations and a precisely typed missing-input contract**, with executable checks, rather than fabricating resource lists.
- Seek negative cases, changes with beacon preview position, multiple resources within one boundary, and resource presence where no corresponding extractor was built. Compare against independent UI/gameplay reference where already available, and distinguish screenshot testimony from native/source evidence. Do not invent new controls.
- Keep expected and observed resource sets in separate evidence channels. Exact set equality, false positives, false negatives, and coverage must be reported explicitly when meaningful independent controls exist.

## 3. Special cases and research bounds

- **X-Tech:** treat the Terran Armada-related extractor/build requirement and X-Tech's exceptional availability rules as distinct from ordinary inorganic deposits. Identify whether X-Tech participates in the same preview/eligibility pathway. Preserve unsupported cases as such; lack of a placed X-Tech extractor is not a reason to generalize incorrectly or stall ordinary-resource research.
- Organic greenhouse/animal-husbandry production, active extraction/output rates, power, production chains, cargo transfer, container inventories, and classification of all existing constructions remain outside this assignment.
- Do not require recovering exact deposit polygon geometry if a native/UI resource identity set or another proven sufficient method answers the target question. Conversely, don't call a menu listing a verified extractor-placement site without evidence.
- The preview-before-placement and established-Workshop cases are distinct populations; do not infer equivalence without demonstrating it.

## 4. Completion contract — substantial research, no premature handoff

Apply the repository's Research Execution and Completion Protocol. Ownership of in-scope failed tests, contradictory evidence, missing edges and reasonable dependency tracing remains with the implementer. The specialist and reviewer must work from primary evidence, not merely implementation summaries. Do not redefine a narrower deliverable as complete without an explicit evidence-based disposition.

**Outcome A — Supported reconstruction:** Specify the runtime producer(s), their inputs/outputs and update conditions; establish preview versus established-site semantics; deliver an executable evaluator or supported API-based procedure producing independent resource sets in an explicitly qualified domain, with positive and negative validation. Describe serialization separately and accurately. This need not be globally complete for every DLC/body if scoped coverage is justified.

**Outcome B — Completed evidence-bound result:** Exhaust the credible offline UI/native/save/record leads and demonstrate exactly which unavailable runtime inputs or unobserved operations prevent complete independent set reconstruction. Deliver a *decision-ready* minimal future acquisition plan with specific observations, falsifiable competing hypotheses, and a directly player-visible set-comparison protocol. Outcome B is **not** permission to finish at the first non-obvious function or missing save field. It may include strong, independently established partial scientific findings.

**Escalate only for genuinely new authority:** If the next decisive action requires a live SFSE observer, controlled save, interactive beacon preview, or other non-authorized action, explain the required permission and precise discriminating observations. **Do not implement or run live instrumentation now.** A separate future brief can integrate plugin, qualification, Vortex package and complete run card in one review, as previously agreed.

## 5. Agent roles and research integrity

Maximum **two concurrently active sub-agents** in addition to the main Codex agent: one independent reviewer, and optionally one specialist researcher. Use the specialist on the separable **runtime/UI/native availability producer** or save/record study according to the actual division of work; main implementer owns synthesis and executable evidence. Reviewer must challenge resource-presence inference, false negatives with no extractor, preview/established equivalence, DLC edge cases, and whether Outcome B truly exhausts authorized leads. Record the specialist's material contribution when used; no requirement to continually re-evaluate the established reviewer role.

Honor source authorship, licensing, permission, and provenance rules. Maintainer-authored `gooberpede` repository material can be reused per project policy with precise source/revision provenance; third-party implementations need appropriate reuse permissions. Public references are evidence, not blanket permission to copy code. No distribution of Bethesda proprietary files, private savegame bytes, raw memories, secrets, or Ghidra databases.

Protect original saves, frozen predictions, raw live evidence, existing observer binaries, and historical audit records. Preserve exact scientific claims and historical negative findings. Maintain the mandatory **40,000,000,000 caller-available bytes free on both C: and D:** for substantial local evidence processing. No arbitrary elapsed-time/event-count/evidence-volume stop gates; genuine machine/instrumentation integrity failures remain terminal when required.

## 6. Deferred research: explicit backlog preservation

As part of this assignment, **verify and, if necessary, update the durable research backlog/disposition** to retain questions shelved during position-model consolidation, **without reopening them now**:

- Historical 0.5.0 versus 0.6.0 Workshop native XYZ/Z coordinate-state discrepancy; own frame flag/parent, activation epoch and transformation not resolved.
- Complete saved-to-live vertical-coordinate frame/restoration behavior and terrain-procgen dependencies, potentially relevant near public release or if a concrete feature requires them.
- Exact continuous planetary longitude/latitude for subcell Workshop placement, if ever needed beyond qualified site anchors and discrete grid positions.
- Any deferred native-equivalence branches or unresolved historical outpost-position cases recorded by the consolidated position-model disposition.

Mark their present status **DEFERRED**, with existing evidence pointers, reopening triggers (concrete application need, independently discriminating evidence, or pre-public-release research review), and explicit separation from this resource task. No promise to resolve them before public release, and no speculative new observer work authorized by a backlog entry.

Keep the small controlled-save test concerning remnants of deleted four-wall Habs at removed outposts on the backlog separately, with its ownership-versus-location uncertainty preserved; do not fold that into inorganic resource research.

## 7. Required artifacts

1. **Scientific report/specification:** Definitions, UI/runtime pipeline, preview and placed-Workshop pathways, save representation, native record/function evidence, uncertainties and provenance.
2. **Reproducible code and focused tests:** Prefer existing save-reader/resource tool infrastructure. Provide a deterministic resource-set evaluator if justified, otherwise executable partial reconstruction with a typed missing-input contract. No guessed eligibility masquerading as measured availability.
3. **Evidence/validation ledger:** Per-site/preview controls, known extractor positives, known absences/unknowns, DLC exceptions, exact source/identity references, tested coverage and independent versus model-derived expectations.
4. **Decision-ready future acquisition assessment:** Only if needed, specify shortest native/UI observation needed to distinguish hypotheses, expected outcomes, trigger feasibility and controls; do not default to a broad instrumentation plan.
5. **Backlog/disposition updates:** Ensure frozen Z/coordinate/terrain questions remain discoverable and deferred, and the Hab controlled-save question remains distinct.
6. **Independent review:** Frozen acceptance matrix, reviewer verdict, resolved REWORK issues, and candid distinctions among scientific result, implementation health and scope.
7. **Review package:** Complete and task-only diffs in `.local-work/diffs/`, changed-file manifest, exclusions, `git status --short`, integrity/test checks, and concise recommended **Conventional Commit** message. Handle untracked text files in the complete patch. No staging, commit or push.

Use clear authored prose and preserve native symbols; avoid both missing prose spaces and indiscriminate splitting of legitimate identifiers.

## 8. Start and handoff

Start with a read-only inventory of the current repository, available source data and documented gameplay screenshot. Establish what is already known about the preview resource display before building new infrastructure. Trace the real producer and its dynamic inputs, then implement only what is supported and test it against independent controls.

Do **not** stop merely because the save lacks an explicit resource list; for this assignment, native runtime reconstruction is at least as important as serialization. Complete the authorized investigation, obtain independent review and return scientific results **together with** the code, verification and reviewed diffs. No live game work or publication is authorized by this brief.
