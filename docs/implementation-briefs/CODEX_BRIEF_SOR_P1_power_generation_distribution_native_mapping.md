# Codex Research Brief — P1: Outpost Power Generation, Distribution, Wiring and Native Contracts

**Repository:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research`)  
**Task type:** Bounded, offline native-function and game-definition research  
**Authorization:** Research and documentation only; no live Starfield execution, SFSE observer, native invocation, game/save changes, installation/deployment, staging, commit or push.

## 1. Purpose and research standard

Map Starfield's existing outpost power machinery sufficiently that an independent researcher can identify the native functions, object structures, persistent representations, calculation paths and current-state readouts for power generation, consumption, wiring and switching. Do **not** build a power simulator, gameplay mod or network-management tool.

Use the now established outcome convention: **COMPLETE** means the essential authorized offline mapping objectives have adequate answers at their corresponding evidence level; **INCOMPLETE** identifies an important unanswered in-scope question that available authorized avenues could still address; **BLOCKED** identifies an actual evidence/access barrier. Record evidence confidence *separately*. Absence of live measurement is not by itself incompleteness. No automatic `CONDITIONALLY COMPLETE` label.

Build upon E1–E3's mapped power/production-state tests and runtime reference contracts rather than tracing them from scratch. Give precise pinned build identifiers and VA/RVA conversions for any native addresses. Do not mistake hypotheses or reverse-engineered pseudocode for verified native behavior.

## 2. Required source review

Before new tracing, inspect:

- Existing repository `WORKFLOW.md`, research state, native function register, E1 inorganic, E2 organic and E3 fabricator reports, associated saved-reference/link studies and existing power-state findings.
- `gooberpede/starfield-outpost-network` (local checkout or linked repo if accessible), its planetary/reference data and pertinent xEdit scripts. Record paths, revisions and any access limitation rather than asserting content was checked when unavailable.
- The supplied **`Starfield - Export Planet Directory.pas`**, version 4, xEdit/SF1Edit 4.1.5p: a *reference implementation* for definition-derived basic Solar Array/Wind Turbine output, not proof of complete runtime dynamics. If the script is unavailable in Codex's working environment, find and verify the project's corresponding installed script; document that limitation if neither is accessible.
- Mature saved outposts with multiple generators, switches, wired and unwired equipment wherever identifiable. Compare more than Save52 and distinguish actual serialized evidence from inferred native operation. Preserve all saves and byte hashes.

The attached exporter declares these **definition-derived basic outputs**, subject to native verification and exceptional-case handling:

| Planet property | Basic solar | Basic wind |
|---|---:|---:|
| Deep Freeze | 2 | — |
| Frozen / Cold | 4 | — |
| Temperate / Hot | 6 | — |
| Scorched / Inferno | 8 | — |
| No atmosphere | — | 0 |
| Thin atmosphere | — | 3 |
| Standard pressure | — | 6 |
| High / Extreme pressure | — | 10 |

The script treats non-landable bodies separately and warns about unmatched keywords; it specifies a wind fallback of 6 for recognized atmospheres without recognized pressure. Verify these values and precedence through game records/native functions, including non-basic generator variants. Do not assume temperature implies actual sunlight or atmosphere implies dynamic wind/weather simulation.

## 3. P1-G — Generation and effective output

1. Enumerate relevant constructible generator forms and variants with identity, technology/size, base rating, resource or planetary eligibility and any special requirements. Distinguish definitions, power-producing runtime references and generator-like wiring relays.
2. Trace the native output calculation from planet environment/definitions to generator effective generation, including modifiers and dependencies. Investigate solar, wind and fueled generators, including Helium-3 generator fuel prerequisites and consumption: recipe, interval/amount, native input-link and gating contracts where available. Do not branch into the general inventory/storage system.
3. **Temporal dynamics must be tested as a code question**: does effective output respond to illumination, local time of day, day/night, weather, wind events or other changing conditions, versus fixed planet-derived output (apart from on/off/fuel/condition state)? Identify actual checks, callers and update triggers. If the static code does not settle it, label precisely unresolved and propose a discriminating achievable test, not speculation.
4. Separate nominal rated output, actual current output, effective available supply and UI-displayed totals, noting which are stored/cached versus recalculated.

## 4. P1-D — Unwired ('simple') power and shortage allocation

Treat the user's 'simple' or unwired pool as a hypothesis, not engine terminology. Map registration and ownership of producer and consumer power contributions, aggregate generation and demand, powered-flag updates, recalculation triggers, and whether distribution is Workshop-wide, spatial, group-based or otherwise.

**Mandatory deficit question:** with supply below demand, determine how individual consumers lose/retain power: common failure, ordering, priority, construction sequence, wiring status, connected groups or other rules. Distinguish explicitly supported behavior from iteration artifacts or assumptions. Trace effect on current power state rather than theoretical capacity. Do not conflate the extractor's active/halted state with powered state.

## 5. P1-W — Wiring, relay eligibility, switches and mixed allocation

**Do not assume which objects can act as wire relays.** Investigate the authoritative native checks for creating or refusing a wired connection between any two references. Establish category/keyword/component checks, connection limits, directionality or bidirectionality, range/location restrictions and special cases. Include generators, power-consuming objects, lampposts, switches and seemingly unpowered objects as candidates to test in definitions/native code. Record exceptions; distinguish visible wire art/geometry from authoritative logical graph data.

Trace the wiring graph's representation and functions for add/remove/query/traverse, save/load persistence and reconstruction, branch nodes, chains of switches, cycles, and the behavior of nodes that both generate and relay. Identify switch state representation, gating propagation and any shared or independent pool accounting. Don't assume that lampposts draw no power or that generators act as relays until established.

**Mandatory mixed-case question:** if wired and unwired consumers coexist at an outpost whose generation is insufficient, is either group favored, or are they allocated using a unified rule? Examine a single-generator graph and a graph with generators wired together, but treat these as conceptual discriminating configurations, not instructions to build them live. If static analysis cannot decide precedence, identify exact native ambiguity and a minimal realistic observation that would distinguish outcomes. Cover switch-controlled consumers versus otherwise comparable unswitched consumers where relevant.

## 6. P1-S — Saved versus runtime contracts

For each generator, consumer, wire edge and switch, distinguish:

- What can be recovered from **saves plus version-matched game definitions**, with verified parsing and caveats.
- What is computed or read **at runtime**, including a native function, field, lifetime, required Workshop context and current-state access point.
- What is documented by static analysis only, actually corroborated by saved instances, or directly runtime-observed in earlier evidence.

Provide native output contracts for current powered state, generator contribution, consumer demand, wiring graph membership/edges, switching state, shortages and operating consequences. Identify necessary handles/translation rules; do not claim a safe arbitrary external invocation API merely from an RVA.

## 7. Scientific safeguards and boundaries

- Where a question cannot be settled, state the exact unresolved predicate, competing plausible mechanisms and *smallest achievable discriminating test* only if genuinely justified. No instrumentation or live experiment under this brief.
- Prioritize meaningful native mapping, not a complete electrical-engine recreation. Use existing system functions instead of designing alternate algorithms.
- Keep storage quantity accounting, cargo transport, crafting, chest/display inventories, combat/turret behavior, robot staffing, aggregate outpost limits and attacks outside P1 except for minimal references needed to explain power functions.
- Do not change previously preserved experimental outputs, frozen predictions or raw evidence. Treat saved links and current runtime graph links as potentially different representations.
- Avoid time/event quotas for proposed future live work; preserve scientific-value GO/NO-GO gating.

## 8. Deliverables

Place a cohesive, navigable set of durable documents under a suitable `docs/experiments/` power-research directory, integrated into existing indexes and native function registry. At minimum:

1. Technical report, scope, evidence table and clear answers to generation dynamics and shortage/wired precedence questions.
2. Definition catalogue of generator/consumer/relay candidates and qualified solar/wind/fuel calculations.
3. Native function register additions and dataflow maps: generation, allocation, wire eligibility, graph traversal, switch gating and consumer state.
4. Save-versus-runtime contract matrix with representative inspected saved examples and exact evidence provenance.
5. Hypothesis/uncertainty table with falsifiers and minimal achievable further tests where in-scope evidence genuinely stops.
6. Independent review record, preservation checks, tests and proposed Conventional Commit message.
7. Task-only and complete textual diffs under `.local-work/diffs/`, including untracked text in the complete diff, plus manifest/checksums. Exclude protected raw binary/native/save evidence from review diffs.

Follow `WORKFLOW.md`, including substantive independent review and rework within the task, with bounded optional specialist support where useful. Review actual numerical examples and wire-eligibility claims. Perform a prose-quality audit specifically detecting fused labels, missing spaces around version/address/count notation and malformed Markdown. Never state tests passed without corresponding executed receipts.

## 9. Completion test

At completion, another researcher should be able to find the existing native functions and representations needed to answer: (a) what generator contributes and under what planet/fuel/dynamic conditions; (b) what each device consumes and whether the game presently considers it powered; (c) which pair of objects may be connected by wires, how the graph is stored and traversed, and how switches affect it; (d) what happens during a deficit, including mixed wired/unwired equipment; and (e) which answers are obtainable from a save versus needing current engine state.

An evidence-bounded result may leave particular runtime-only behavior unverified, but may **not** call the core mapping COMPLETE merely because ordinary current-state measurement was excluded if substantial authorized native tracing remains undone. Conversely, do not penalize absence of live evidence that the assignment never authorized.

**No staging, commit, push, deployment or game launch.** Present the reviewed diff and findings for maintainer decision.
