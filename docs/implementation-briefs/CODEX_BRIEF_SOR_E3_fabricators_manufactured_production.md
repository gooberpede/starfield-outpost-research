# Codex Research Brief — SOR E3: Fabricators and Manufactured Production

**Project:** `starfield-outpost-research`  
**Assignment:** Offline native-function and game-definition research; no implementation of a production tool  
**Status:** Ready for Codex  
**Predecessors:** E1 inorganic extraction and production arithmetic; E2 organic production, recipes, selection and local-link topology

## 1. Purpose and completion standard

Map Starfield's **automated outpost fabricator** machinery sufficiently that another researcher can identify the existing native functions, data structures, definitions, execution paths and constraints needed to understand or leverage manufactured-resource production. This is research into **what the game actually implements**, not a request to create a fabricator calculator, simulator, mod or reverse-engineered source distribution.

Treat the prior E1/E2 native findings as established within their documented confidence limits; cite their registers, original evidence and scripts rather than re-deriving shared subsystems without cause. Follow the task to meaningful answers on the *fabricator-specific* contracts; do not end with an inventory of addresses but no explanation of the calculation or selection process.

Evaluate assignment completion independently of evidence confidence:

- **COMPLETE:** Essential in-scope native contracts are mapped with appropriate offline evidence; ordinary lack of live measurements does not prevent COMPLETE.
- **INCOMPLETE:** A consequential in-scope question remains unanswered despite available, authorized investigation routes; specify exactly what remains to investigate.
- **BLOCKED:** An identified access, evidence or technical restriction prevents resolution; specify the blocker and minimum realistic evidence needed.

Mark claims individually as definition-backed, saved-state corroborated, instruction-backed, observed at runtime (only pre-existing evidence), reconstructed/tested, or unresolved. Do not use `CONDITIONALLY COMPLETE` simply to denote ordinary offline evidence limits.

## 2. Research questions and required outputs

### A. Fabricator population and classification

1. Enumerate the ordinary automated outpost fabricator **types**, native bases/variants and relevant tiers. The working expectation is three main types, each with a roughly ten-product fixed catalogue, **to be verified, not assumed**.
2. Identify how the engine recognizes a fabricator/producer and distinguishes its type from greenhouse, husbandry, inorganic extractor, storage, and manual crafting station.
3. Report exceptional or nonstandard automated production definitions separately when actually encountered; do not silently enlarge E3 into unrelated production systems.
4. Provide a reproducible, source-backed definition table including record identity and reference to native class/keyword/property classification. Do not infer completeness from names alone.

### B. Output choice, allowed catalogue and persistence

1. Trace the native menu population: how a specific fabricator determines which manufactured items/recipes it can offer; whether the permitted catalogue is solely type-invariant or subject to other requirements, conditions, unlocks or runtime filters.
2. Identify the **currently selected recipe/product** and how it is represented during execution and, where established, persisted/restored across saves.
3. Trace the native selection/action path from UI choice to configuration, producer registration and resource association. Explain what happens to existing production countdown, incoming/outgoing links and active production when the selection changes. Separate positive native findings from unknowns.
4. Compare the relevant selectors with E2 organic production: identify **exact shared native functions** and fabricator-specific divergences, not merely UI similarity.

### C. Recipe and production inputs

1. Resolve every ordinary selectable product to actual game recipe/input records and report the input resource identities, quantities, output identity and requested output count. Identify recipe families, exceptions and data-source provenance.
2. Document how the engine binds the chosen recipe to a fabricator, evaluates required inputs, and handles production eligibility. Distinguish structural input links from item possession or adequate supply.
3. Where relevant, trace gating by research/unlocks or other prerequisites; differentiate constructible *fabricator* from selectable *fabricated output*. Reuse E1 research-project findings when appropriate.
4. Confirm that any same-named outputs or distinct recipes retain correct native identities rather than being collapsed by display text.

### D. Input/output links and local upstream topology

1. Identify the current incoming and outgoing connections, their direction, native ownership and source/destination identities, building on E1/E2 transfer-link research.
2. Trace local upstream chains where the established native data and traversals permit, including loops, buffers and multiple candidates. Distinguish **local producer reached**, **storage/buffer boundary**, **incoming cargo boundary**, **no identified path**, and **unknown**; do not claim that a connected link guarantees sustained inputs.
3. Determine whether output changes preserve or prune links and document the actual compatibility decision if identifiable.
4. Do not count storage inventory, evaluate item availability or trace cargo supply across planets or systems in E3.

### E. Operating state and production arithmetic

1. Map native observation/derivation of the fabricator's **current powered, activated/halted and operating** states, only distinguishing them when supported. Do not reconstruct the outpost power network or power-switch machinery.
2. Establish fabricator-specific base intervals, quantity per cycle, effective rate/quantity modifiers and the applicable native gates. Document their units and clocks; explicitly test whether the E1 **engine elapsed-seconds** scheduler and skipped-time treatment are shared, qualified or different.
3. Determine the role and eligibility of crew, robots, player skills, magazines, research and special effects **at the fabricator production boundary**. Reuse E1's contributor and stacking findings; do not assume inorganic-only bonuses apply to manufacturing.
4. Differentiate **nominal capacity**, **conditional effective production**, and **actual accepted item output**. Recover the normal native requested-production path; do not attempt exact delivered-throughput simulation dependent on storage/cargo.
5. Give several concrete definition-based worked examples across the fabricator classes, citing exact recipes and intervals; do not invent numeric examples or use manual workbench crafting rates as automated-fabricator rates.
6. Identify native production statistics or UI consumers where they already intersect the mapped path, but no new live instrumentation or UI feature implementation.

### F. Native technical reference

Extend the existing native function register and outpost research documents rather than starting competing registries. For each important new function record its pinned build and VA/RVA, role, arguments, output and state mutations, callers/consumers, object field layouts, ownership, initialization/lifecycle/thread prerequisites, evidence reference and uncertainties. Supply a coherent dataflow from facility definition → selectable catalogue → selected recipe → links/gates → scheduler → requested item creation. Explicitly identify shared E1/E2 functions.

## 3. Available research inputs

- The committed E1 reports on inorganic extractor definitions, per-resource production intervals, size/rate effects, crew/robot/player perk stacking, power/halt/eligibility, scheduler clocks, produced quantities and native transfer-link registry.
- The committed E2 reports on greenhouse and animal-husbandry eligibility and selectors, persistence, production recipes, transitive incoming-link traversal, reconfiguration, and shared producer lifecycle.
- The private `starfield-outpost-research` repository's native code evidence, structured function register, installed main-game definitions, xEdit exports, and historical saves, with all established preservation rules.
- The `starfield-outpost-network` reference-source project and relevant recipe/industrial-workbench datasets **as leads/reference data only**. Cross-check against underlying game definitions and native automated-production paths. The user specifically excludes Industrial Workbench mechanics from E3.

Before assuming a save lacks fabricators, inspect the available mature save inventory, not Save52 alone. If there are usable saved examples, corroborate selected output and connection topology with them. If examples are absent/unavailable, state the coverage limit; do not invent or modify saves.

## 4. Hard boundaries

**Offline only.** Do not launch Starfield, deploy/inject DLLs, build an observer, issue arbitrary native calls, modify saves or protected data, or restore backup saves. Do not stage, commit or push. Do not request further authorization merely to execute the authorized offline research.

Out of scope: Industrial Workbench and manual crafting; full storage/inventory accounting; cargo links and cross-system logistics; aggregate power generation, power-switch graph analysis; organic species ecology outside shared selection findings; full fabrication-chain optimization; creation of a player-facing tool, mod, calculator or simulator. Native dependencies may be **named and bounded** without solving the entire connected subsystem.

The eventual ability to trace a multi-planet production chain remains a **future integration assessment**, not an E3 acceptance condition. Previous D1 disappearing-deposit predictions remain durable historical leads, not tasks to reopen here.

## 5. Method and evidence discipline

1. Inventory existing E1/E2 knowledge and reusable scripts first. Identify genuine fabricator-specific unknowns before writing new analysis tools.
2. Validate fabricator populations, product/recipe mappings and quantities using exact definition relationships and checks on exceptions.
3. Follow native call/dataflow for output selection, registration, production eligibility, link traversal, scheduling and actual item request; preserve provenance of addresses and build identity.
4. Corroborate with existing saved examples when relevant and qualified. Keep save observations separate from static definitions and native runtime logic; **no new live observation is claimed**.
5. Distinguish core native behavior from hypotheses. If there are unresolved branches, specify a credible falsifier or bounded gap; do not inflate every untested runtime state into research incompleteness.
6. Document negative findings only for actually inspected code/definition populations. No claim of universal absence from a failed search.

## 6. Review, testing and delivery

Use the repository's `WORKFLOW.md` and research execution/completion protocol. Mandatory **independent reviewer**, with at most one additional specialist when useful and no more than two active sub-agents. Reviewer must challenge functional completeness, provenance, direction of links, exceptions, numerical examples and premature scope-based downgrades. Address substantive objections **within this assignment**.

Perform appropriate deterministic definition/source checks and existing relevant regressions; check protected-input hashes and report the exact audited scope; verify generated/referenced documents and links; conduct a **prose-quality audit**, explicitly checking for fused numbers, RVAs, version strings and malformed spacing seen in earlier tasks. Do not perform unrelated mass formatting.

Deliver:

1. `E3` main technical report with a clear **COMPLETE / INCOMPLETE / BLOCKED** disposition and evidence-tier summary.
2. Fabricator-type and allowable-output catalogue; recipe/input/output table with provenance and exceptions.
3. Native selector/configuration/persistence/registration contract; link-topology and operating-state contract; production interval/quantity/modifier/scheduler contract.
4. Updated shared native function register and a brief E1/E2/E3 reuse-versus-divergence matrix.
5. Saved-instance corroboration where available, without making runtime measurements a prerequisite.
6. Focused verification scripts/tests, receipts, reviewer findings/rework, protected-input report and authorship/provenance updates consistent with repo practice.
7. Task-only and complete diffs under `.local-work/diffs/`, **including added/untracked text**, plus patch forward/reverse checks and a hash manifest. Summarize changed files, tests, unresolved questions and a proposed Conventional Commit; do not stage, commit or push.

**Completion question:** Has the research sufficiently mapped Starfield's existing automated fabricator native machinery that another researcher can locate the relevant outputs, input requirements, state, link connections and production-rate calculation—without needing to rediscover the subsystem? A defensible offline **COMPLETE** is a valid and desirable result when this contract is met; unperformed live qualification remains a stated evidence limitation, not an automatic failure.
