# Codex Research Brief — SOR E2: Organic Production Facilities, Selection Eligibility, Inputs and Native Contracts

**Project:** `starfield-outpost-research`  
**Classification:** Offline research and native-function mapping; no live experiment  
**Status:** Implementation/research brief for Codex, subject to subsequent maintainer review  
**Predecessor:** E1 inorganic extractors, production arithmetic, modifier stacking, clock domains and native UI rate provenance (committed and synced)  
**Next distinct phases:** Fabricators, storage, cargo logistics and end-to-end production-chain feasibility — **not** part of E2

## 1. Purpose and research endpoint

Map Starfield's **greenhouse and animal-husbandry** production systems to the point that another technically capable researcher can identify the existing native functions, definition relationships, runtime state and data contracts needed to understand and make use of the machinery. Do **not** implement an organic-production management tool, independent simulator, mod or logistics planner.

Organic facilities have a configurable selected output. Their selectable products arise from flora/fauna species, domesticability, planetary context, prerequisites and production definitions. They consume inputs as well as produce outputs. Determine what the game *actually* uses to construct the list, select and persist an output, decide operating eligibility, consume/schedule production, and expose its connections and state.

**The research is about native behavior, not merely re-creating a reference table.** Follow the definition records through to the native selection, production and consumption code. Make the distinction between static definitions, save serialization, and runtime engine state explicit throughout.

## 2. Starting sources — inspect before new archaeology

1. Research repository: current native function register, evidence pins, E1 reports, D1 disappearing-deposit ledger, save analyses and workflow instructions. Reuse the established methods, source formats, provenance and confidence conventions; do not create a competing reference architecture.
2. Existing **`starfield-outpost-network`** project: inspect available repository code, reference-source CSVs and any organic-resource transformation/validation logic. Determine what has already been resolved at the reference-data level, including input requirements and domesticability. Locate the actual files rather than relying on a presumed path or inventing contents. If inaccessible, explicitly report the access limitation and proceed using verifiable alternative assets.
3. User-supplied xEdit script: **`Starfield - Export Planet Biome Organic Resources(2).pas`**, headed `Starfield - Export Biome Organic Resources.pas`, **version 2.0.3**. Locate its accessible copy, inspect the *actual script implementation* and capture its hashes/provenance. Its declared output grain is **one row per Planet × Biome × Species**, with PNDT biome flora/fauna lists authoritative for this dataset's membership. It exposes domesticability, canonical resource resolution, and up to two production inputs with quantities.
4. Existing xEdit exporter or reference extracts for outpost recipes and organic resource definitions, if accessible. Treat data-derived hypotheses as hypotheses until cross-checked against native game logic.
5. Attached screenshot from Codos: a greenhouse currently configured for **Solvent**, with **Analgesic** also selectable; the selection of Analgesic displays **Water** as an input. The screenshot is gameplay evidence for configurable selection and an input presentation, **not** proof of menu-completeness, quantity, or the rule that constructs the list.

### Established export relationships to check, not assume to be complete native contracts

The v2.0.3 script states the following definition lineage:

- **Flora:** PNDT species-associated resource `MISC` → `CVPA` component → canonical `IRES` → `NAM2` production `COBJ` → `FVPA` production inputs.
- **Fauna:** PNDT fauna `NPC` → produced-resource CCT `OMOD` → `AVIF` → reverse reference to fauna-specific `IRES` → `NAM2` production `COBJ` → created `MISC` → `CVPA` → canonical `IRES`; inputs from the fauna-specific `COBJ`'s `FVPA`.
- **Domesticability:** flora `OutpostCanDomesticate` keyword (`KYWD:002AC11D`); fauna either `mod_CCT_Special_Domesticate` CCT object-template inclusion or direct `OutpostCanDomesticate` on NPC.
- The exporter **deliberately omits diet lineage**, biome chance/frequency, and most intermediate native record relationships from its output CSV. It includes production inputs even for non-domesticable species, which does **not** establish that those recipes are selectable in game.

The user's present understanding is that greenhouse inputs are Water and husbandry inputs are Water plus either Fiber or Nutrient, possibly selected through diet keywords. **Verify these as scoped rules, trace the actual deciding definitions/functions, and report counterexamples if any.** Do not assume the exporter proves a diet-keyword rule: it does not export diet lineage.

## 3. Native definition and facility inventory

Create a version-pinned, reproducible catalogue of main-game greenhouse and husbandry facility bases and construction definitions, including any relevant tier/size/type and exceptions. Do not classify solely by EditorID patterns: establish the native conditions or form links that make a constructed object an organic producer.

For each type establish the route from constructed instance to base definition, producer/Workshop registration, currently configured product and production recipe. Identify differences between persistent identifiers in saves and runtime-only state. An existing save inventory can provide realistic examples; original saves must remain unchanged. Make clear which records have been observed in saves and which merely exist as construction definitions.

Capture how power, independent activation/halt conditions and current operating/eligibility status are represented. Reuse E1's status machinery if shared; map divergence without investigating overall power generation, switches or network sufficiency.

## 4. Output-selection contract: the central organic-specific question

Map the complete native process that builds the resource choices shown when the player selects a product in a greenhouse or husbandry facility.

Determine, and distinguish in both code and evidence:

- Which species and species-resource relationships are considered; what makes them eligible on the selected **planet/world**; and whether the facility's **local biome** or current spawned species actually constrains the menu.
- Which domesticability flags, special animal templates, scanning progression, knowledge/discovery, research, player skills or other prerequisites gate selection. Test these assumptions against definitions and native menu/data-model producers; avoid reconstructing the entire scanning system.
- Whether the species itself, produced organic resource, recipe, or some other native entity is the selection key; deduplication and sorting when multiple species produce the same resource; cases with multiple outputs and exceptional/ambiguous lineage.
- Differences between flora and fauna eligibility and between **visible**, **selectable**, **locked**, and **currently selected** menu entries if the native UI distinguishes them.
- How selection changes are applied, persisted and restored; implications for input recipe, timer, power, outgoing links and existing inventory. Record actual behavior only when established—do not presume a timer reset or link mutation.

The user's observation that a plant naturally confined to Savannah can be cultivated in a Sandy Desert greenhouse is a direct challenge to a naive local-biome-lock rule. Treat this as a testable lead, not a universal conclusion; determine the scope of the actual game rule.

Trace both **producer** and **consumer** boundaries of the resource-selector UI in the same evidence-disciplined style used for the prospective beacon *Available Resources* interface. Locate native functions and data layouts; record executable pin + RVA, calling context, argument meaning, outputs, lifetime and confidence.

## 5. Production inputs and local-link topology

Determine the required resource identities and **quantities** for the selected output. Trace the relevant record lineage and native recipe-consumption code, including which conditions cause a facility to reject or pause production. Avoid conflating the mere existence of a recipe with an actual active runtime production order.

Map incoming and outgoing links, including the **direction** of connections and native reference/handle identity. E1's transfer-link map and outgoing-destination query should be reused if applicable. Establish whether incoming links can be followed **upstream through local connected objects** and, where supportable, whether a path reaches a local producer of each required resource.

Report topology with meaningful distinctions, for example:

- Local producer reached via a verified link path.
- Link path reaches storage or an incoming cargo-link container; upstream remote provenance unresolved.
- No structural path identified in the inspected graph.
- Evidence missing, reference unresolved or semantics unknown.

Do **not** equate an identified path with sufficient resources or throughput. Do **not** mark a required input absent merely because a trace reaches incoming cargo storage. In the user's Montara Luna example, Water may trace to a local extractor while Fiber arrives via a cargo link; a local trace can end at that cargo boundary without identifying the remote supplier. This is a valid and useful terminal result.

**Excluded:** inventory counts, storage capacity/stock levels, sustained supply rate, transshipment mechanics, cross-outpost cargo transport, total energy supply and a full production-chain solver. Trace native input-availability checks sufficiently to identify what the organic producer itself tests, but do not expand into the implementation of storage or network systems.

## 6. Production machinery: reuse E1 rigorously

Establish whether greenhouse and husbandry facilities share E1's native production-registration, operation-status, elapsed-seconds clock, nominal/modified interval, requested quantity, realized item-creation and aggregate Workshop-statistic paths. Where shared, cite existing E1 source pins and function-register entries; where divergent, document precisely the new native path.

Include concrete, verified definition-based examples for **at least one greenhouse and one husbandry facility** where the installed data supports them. Document base interval, per-cycle quantity, input quantities, modifiers and status gates; distinguish definition-derived rates from observed runtime output. Reuse E1's findings on crew, robot, player-skill and magazine selection/stacking only if the production context and eligibility genuinely match. Identify organic-specific perks or research unlocks if directly relevant to the path.

Separate **nominal**, **effective**, and **realized** output; do not demand a storage/logistics simulation as a prerequisite to a usable native contract.

## 7. Opportunistic integration findings — no scope creep

Record unexpected shared functions with inorganic extraction or builders/fabricators, particularly menu selection, production recipes, input-link traversal, time base and item creation. These are interface discoveries for future research, **not authorization to map fabricators in E2**.

Maintain D1 hypothesis references only when actual E2 evidence bears on them. Do not reopen the rare disappearing-deposit investigation.

Record a future **integrated research sufficiency test**: when inorganic, organic, manufactured production, local transfers, storage and cargo-links have each been mapped, assess whether the documented native contracts are sufficient to follow a multi-planet, multi-system production chain. This is a roadmap question, **not a deliverable to implement or solve now**.

## 8. Research standards and stopping rules

1. **Offline only.** No Starfield launch, SFSE observer, native runtime invocation, save restoration/modification, Vortex package, live testing or deployment.
2. Follow existing `WORKFLOW.md` research execution/completion protocol: substantive primary-agent work, independent review, and at most one optional specialist simultaneously (maximum two sub-agents). Reviewer must test substantive claims and send correctable defects back for rework within the task.
3. Protect game files, Ghidra projects, saves, prior evidence, exports and pinned bytes. No destructive or unauthorized changes. No stage, commit or push.
4. Source pin everything consequential: game build, form/plugin identities, native VA/RVA, decompilation/instruction evidence, scripts, reference definitions, saves and screenshots. Separate **static native inference**, **definition-derived results**, **save-supported facts**, and **retail runtime observations**. Never describe an unperformed runtime test as validated.
5. Prefer conclusive bounded answers over broad unresolved question lists. Within scope, follow reachable native leads before returning an evidence-bounded result; do not expand into entire scanning, storage, power, cargo or creature systems.
6. Audit **all newly authored and changed prose** for malformed joins (e.g. missing spaces around versions, addresses and identifiers), wrong terminology, broken references and unsupported certainty. Review this explicitly.
7. If a central contract cannot be settled offline, identify the *smallest achievable discriminating observation*, its natural execution boundary and expected possible conclusions. No observer implementation and no automatic recommendation for a live experiment. Apply the scientific-value GO/REVISE/NO-GO discipline.

## 9. Required deliverables

Integrate into established research layout without inventing conflicting files. At minimum deliver:

- **E2 report:** scope, definitions and evidence, distinct greenhouse/husbandry findings, results and limitations.
- **Definition and recipe catalogue:** provenance-pinned, reproducible enumeration with input identities/quantities, output identities, eligibility and exceptional cases, without treating definition rows as runtime selectable results.
- **Native function/register additions and dataflow:** menu eligibility/selection, production inputs, current state, scheduling, link traversal, relevant memory/ownership and serialization.
- **Link topology contract:** exact supported tracing operations; cargo/storage boundary semantics and non-binary result statuses.
- **E1 reuse matrix:** which native mechanisms are shared, conditionally shared or different.
- **Evidence-backed completion assessment:** COMPLETE, CONDITIONALLY COMPLETE or INCOMPLETE under the research endpoint; explain exactly which contracts remain unqualified.
- **Independent review and verification:** scoped tests, preservation receipts, source references, prose audit and review responses.
- **Review-ready patch artifacts:** complete and task-only diffs including untracked textual additions, output manifest and hashes, summary of modified files and suggested Conventional Commit subject. Put large raw/private assets outside diffs.

## 10. Acceptance standard

Accept when the mapped native contracts explain, sufficiently for an independent researcher, **how a given organic facility is identified, how its possible outputs are chosen, how the current output and required inputs are represented, how incoming/outgoing links can be examined locally, and how its current status and production process operate**.

A qualified unresolved runtime detail is acceptable if the relevant function and state boundaries are documented and no further in-scope offline evidence can settle it. Do **not** declare completion merely because the exporter can generate a production table; do **not** make an end-to-end logistics implementation or storage quantities a requirement.

**Suggested commit subject (subject to actual findings):** `docs(research): map organic production selection and native contracts`

**Authority:** This brief authorizes only the described offline research and review. Return results for maintainer assessment before any staging, commit or later activity.
