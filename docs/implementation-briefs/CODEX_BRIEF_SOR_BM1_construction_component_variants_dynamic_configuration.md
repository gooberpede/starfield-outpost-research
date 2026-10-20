# Codex research brief — BM1: Construction-component variants and dynamic configuration

**Project:** `starfield-outpost-research`  
**Assignment:** BM1 — bounded, offline research and documentation  
**Status:** Proposed for maintainer-authorized execution; this brief is not an evidence record or permission to perform live work.  
**Research purpose:** Explain Starfield's existing mechanisms for selecting, creating, replacing, automatically adapting, dynamically changing and persisting construction-component variants. This is basic engine/game research, **not a brief to design or implement a particular mod**.

## 1. Question and intended outcome

What mechanisms actually govern the variants of constructed components (particularly hab walls, doors, windows, floors and ceilings), and what makes an additional variant discoverable, selectable, applicable and persistent?

Produce a sufficiently explicit, evidence-backed **mechanism taxonomy and extensibility map** that a technically competent author can determine (a) which relevant mechanisms exist in installed Starfield, (b) what data, script and native relationships they require, (c) their limits and object-identity consequences, and (d) where a proposed behaviour would need genuinely new functionality. **Do not build an example mod**; investigate mechanisms, not a particular implementation objective.

Use ordinary outpost hab-wall **CHANGE** as the primary, deep, end-to-end case. Examine other construction families as discriminating contrasts; do **not** assume that anything visually called a “variant” is implemented through the same system.

## 2. Scope and representative cases

**Primary case: ordinary outpost habs.** Trace the actual installed definitions and runtime paths for:

- Initial wall/component configuration at hab construction.
- Manual **CHANGE** on an existing wall: available choices, eligibility, action and result.
- Automatic doorway/wall changes when habs connect, disconnect or are reconfigured.
- Interior versus exterior sides and component-level versus whole-assembly replacement, where applicable.
- Associated wall/window/door geometry, snapping/connection state and saved restoration.

**Required contrasts, chosen for mechanism diversity:**

1. **Hab floors and ceilings:** determine whether variants are actually provided, and if so whether they use the wall mechanism. A substantiated absence/limited support is a valid result.
2. **Airlock stairs:** geometry/assembly substitution or configuration if one exists.
3. **Cargo-link containers/components:** state-driven or selectable representation, and whether that is a construction variant at all.
4. **Storage-container decals/appearance:** material, texture, decal, mesh or component choice, as applicable; establish whether there is a usable installed mechanism rather than inventing one.
5. **Damaged versus intact wall:** distinguish native destructible stages, material/mesh swaps and scripts from a manual construction variant; trace a representative state change and repair/restoration relationship if available.
6. **Ship hab walls/floors/ceilings:** a **bounded architectural contrast** only: shared mechanism, separate mechanism or insufficient supported linkage. No comprehensive Ship Builder research.

For each contrast, establish an installed positive exemplar where available, or provide a bounded definition/native census and reasoned negative/unknown classification. A missing cosmetic option is **not** proof that the underlying mechanism is impossible to extend.

## 3. Mandatory research questions

### A. Fundamental units and definition model

Identify, with actual records and code paths, whether variations operate at the level of construction recipe, placed root, PackIn/assembly child, component/reference, snap node, model, material, decal, destructible state or some other object. Explain the relevant form/record types, fields, links, keywords, properties, lists and asset references; separate installed data relationships from guesses based on editor-facing names.

Trace how available alternatives are **discovered** and grouped; whether candidate membership is data-driven, script-mediated, hardcoded or mixed; whether restrictions arise from direction/adjacency, component type, worldspace, progression, connection geometry or other conditions. Distinguish a selectable alternative from a variant that appears only because of automatic state.

### B. Selection and execution

Trace Build Mode's ordinary manual **CHANGE** path from menu choice to authoritative operation, including classification, validated candidate, failure/admission reasons, any cost/resource handling, and resulting object state. Investigate initial construction and automatic adjacency-driven change **separately**; show their points of convergence or difference with concrete calls/definitions. Do not turn this into an audit of all Build Mode pagination, cameras or UI controls.

### C. Identities, connectivity and side effects

Determine for representative operations what remains stable and what is rebuilt/replaced: Workshop owner, construction representative/root, child references, component selection, form/base identity, snap/connection relationships, orientation, collision and attached furnishings. Where relevant connect to prior L1/L2/L3, Workshop membership, P1, DA1 and SD1 findings without repeating them. Distinguish **actual ordinary-path guarantees** from plausible but unverified downstream effects (e.g. effect on power wiring or attachments).

### D. Dynamic state, damage and scripting

Identify mechanisms that can change visible configuration **after construction**: adjacency updates, native replacement, property changes, destructible stages, materials/decals, script/API operations or event reactions. Assess whether a state-driven “damaged wall versus intact wall” is supported by an existing mechanism and whether it is independent of the CHANGE catalogue. Do **not** reopen combat simulation, AI, general Havok, pathfinding or damage calculations except for an essential link to representation.

### E. Persistence and extension constraints

For each distinct mechanism, identify the persisted authoritative state and reconstruction/load path: chosen variant, component root/reference identity, replacement linkage, display/material state, adjacency connections and damage stages where applicable. Search the **wider mature-save corpus** for representative positive contrasting witnesses; use the existing protected reader and qualified formats. Do not treat a missing serialized field as absent gameplay state without checking definition-derived reconstruction. Do not claim live rendered restoration merely from a decoded save.

Provide a concrete extension map: minimum installed record/script/native relationship needed to introduce another variant to an existing family, where the selected mechanism demonstrably supports it; constraints/gates; and whether the result is **definition-driven**, **script-assisted**, **native-dependent**, or **unknown**. Only label a capability native-dependent after identifying an actual native requirement/closed catalogue or a material obstruction, not merely a missing convenient exemplar.

### F. Outpost versus ship mechanism

Compare the relevant definitions, selection paths and persistence at a **mechanism** level. State explicitly which terrestrial findings transfer to ship habs and which do not. Stop before unrelated ship building, ship interior generation or ship combat.

## 4. Evidence method and controls

1. Review the existing accepted Workshop/assembly membership, construction and replacement, L1–L3, DA1, SD1/SD2, Build Mode audit and historical position findings. Cite durable sources precisely, including version/pins when reusing native addresses. **Do not quietly promote provisional older findings.**
2. Inventory concrete installed exemplars for manual wall variants, automatic connection changes and at least several mechanically distinct contrasts. Capture definition/record and source-function pins, call/condition chains, code excerpts only within project rights rules, and negative census boundaries.
3. Trace actual **producers and consumers** of the selection/configuration state. Naming or a screenshot alone is not an execution trace. Explain manual operation, automatic/initial variants and dynamic state independently, even if a shared helper exists.
4. Use existing saved witnesses wherever suitable; prefer positive reference/root/child/variant associations and contrasting change states. Search beyond Save52 when necessary. Distinguish positive observed saved evidence, definition/native predictions and live-untested claims. If no paired save exists, document qualified coverage and the minimal discriminating potential live test; **do not demand or create new saves**.
5. For any tested claims of completeness of a variant list or family, use an enumerated population and a defensible completeness argument. For ordinary mechanism claims use reasonable engineering confidence; no universal exhaustive proof of imaginable alternative code paths is required. Keep concrete counterexamples and true exceptional cases visible.
6. Reuse existing read-only offline tooling rather than creating a speculative general framework. Any utilities developed under this brief must be bounded, documented and independently verified. Limit new infrastructure to what materially answers the questions.

## 5. Deliverables

Create a durable `docs/experiments/construction-variants/` research package using existing experiment naming/format conventions (adapt file names to the repository style), comprising:

- **`report.md`** — answer-first plain-English conclusions; scope, confidence, covered mechanisms, differences between habs and other families, limitations and practical interpretation.
- **`mechanisms.md`** — taxonomy table: mechanism, installed exemplar, fundamental unit, source definitions/conditions, discovery, action, identity effects, persistence, evidence and confidence.
- **`manual-and-automatic.md`** — traced manual CHANGE, initial construction and automatic connection/disconnection workflows with concrete native/script/form references.
- **`extensibility.md`** — per-family extension map with minimum required relationships and appropriately qualified definition-driven/script-assisted/native-dependent/unknown outcomes; ship comparison included.
- **`saves.md`** — historical search inventory, qualified positive witnesses, missing representation limitations and native-to-save joins. Avoid invented witness details.
- **`sources.csv`** and/or function/record registers consistent with repository standards; evidence hashes, locators, definition/file versions, source-specific scope, negative-control coverage.
- **`review.md`** — complete frozen-criterion matrix, test checks, independent-review history, explicit distinction between scientific acceptance and unsupported extension ideas.
- Update relevant subsystem/backlog/research-state indexes **only to register these new reviewed findings and cross-references**, preserving historical reports and independent classifications. Do not undertake project-wide cleanup or release-readiness work.

All prose must be readable and correctly spaced/encoded; explicitly audit for the recurring malformed prose/UTF-8 issue, especially after automated edits.

## 6. Compact frozen completion contract (AC1–AC8)

**Task type:** bounded scientific research and documentation; no mod, plugin, UI or in-game implementation.

**Question/deliverable:** Which construction-variant mechanisms exist and what do their definitions, runtime paths, saved states and demonstrated extension boundaries permit?

**Scope/authority:** Offline, read-only access to installed game records, executable/static analysis, scripts/assets and protected historical saves; may create new analysis outputs and research documentation in working tree as permitted by repository safeguards. No game launch, live observer, debugger attachment, deployment, save/ESM modifications, third-party distribution, repository publishing or staging/commit/push. Use existing permissions, provenance and third-party-use gates. Record proposed future live observations separately; they are **not** authorized.

**Mandatory acceptance:**

- **AC1 — Prior-work and corpus basis:** Explicit source-based baseline and bounded installed exemplar census for the primary hab variants and required contrasting families; controls and inclusion/exclusion inventory.
- **AC2 — Variant definition/discovery model:** Explain actual record/script/native relationships and eligibility/selection predicates for supported variants, distinguishing whole-assembly, subcomponent, model/material and state mechanisms; justify negative/unknown findings.
- **AC3 — Manual CHANGE end to end:** Trace ordinary hab-wall CHANGE from available menu choice to accepted native state transition and identity/cost/construction consequences with source pins, not just labels or UI screenshots.
- **AC4 — Initial/automatic and dynamic paths:** Trace initial construction and connection/disconnection changes independently and map representative dynamic/damage/material mechanisms. Explicitly separate them where distinct; bound missing cases.
- **AC5 — Cross-family and ship comparison:** Mechanism-based comparisons for floors/ceilings, stairs, cargo components, decals, damaged wall and ship hab, with demonstrated transferability or justified limits rather than blanket generalization.
- **AC6 — Persistence and positive witnesses:** Recover authoritative save/reconstruction channels and appropriate concrete mature-save examples for supported mechanisms; preserve coverage and explicitly distinguish missing live rendering from actual saved positives.
- **AC7 — Extension map and reporting:** Produce durable mechanism taxonomy, practical necessary relationships, three-level extensibility classification plus unknown where warranted, confidence/evidence distinctions, counterexamples and readable prose; do not solve the suggested mods.
- **AC8 — Independent review and integrity:** Follow `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, and `docs/templates/completion-contract.md`; protect inputs and hashes, verify outputs/links/encoding, retain all tests and failure corrections, provide independent reviewer ACCEPT/REWORK/ESCALATE against **these frozen criteria**, and exact verified complete and task-only patches with manifest and receipts. Return no staged/committed/pushed changes.

**Optional, not gating:** Complete catalogues of every cosmetic variant; measured in-game CHANGE experiment; fresh ship interior tests; working extension prototype; visual render-after-reload validation; full external asset authoring workflow.

**Negative-result closure:** A bounded positive/negative case may conclude absence of an installed mechanism or a demonstrably separate mechanism. Report the actual searched record populations/code paths and controls. Do not equate “no example found” with “not possible”; do not demand disproving unsupported Russell's-teapot-style alternatives. A missing essential positive path or unexamined in-scope plausible candidate is unfinished, not a substitute conclusion.

**Continuation authority:** Within the offline assignment, investigate failures, refine traces, correct factual/prose defects, rerun pertinent validations, and obtain independent re-review without a second brief. Mandatory criteria remain frozen absent maintainer-approved amendment. Retain original reviewer decisions, counterexamples and historical state.

**Exit/escalation:** Stop affected operations on failed protected-input hash, guard or disk verification; preserve diagnostics and request precise maintainer decision. If a mandatory criterion genuinely needs new live authority, unavailable installed material or an essential operator action, exhaust authorized offline avenues and escalate that specific dependency with an exact minimal proposed test, not a generic “needs more research.” Continue unrelated authorized work. Do not impose arbitrary test-count/time caps on a healthy research run; preserve all applicable STOP/free-space/worker safety controls.

**Review artifacts/disposition:** Original AC1–AC8 PASS/FAIL/NOT TESTED matrix with exact evidence locators, source/hypothesis coverage, source licenses/publication classes, prior failures, status/inclusion/exclusion inventory, independent reviewer decision and reviewed revision, complete/task-only diffs and forward/reverse reconstruction receipts. Distinguish research conclusion, engineering integrity, protected-input safety and publication eligibility. **No automatic commit or distribution.**

## 7. Return format

Return a concise substantive summary of the confirmed mechanisms and limits, full report/review paths, acceptance matrix outcome, actual counts/check receipts, protection/permission results and **verified** complete and task-only patch paths. Provide a proposed commit message only. Do not state a variant mechanism is reusable by mod authors unless the required data/API/engine link is actually established. Await the maintainer's critical diff review before integration.
