# RG2-D5Q — Resource Construction Call and Data-Flow Mapping

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Offline native research and durable mapping only; no retail Starfield execution or observer implementation  
**Status:** Implementation/research brief; freeze D5Q-AC1–AC8 before work  
**D5P/R3:** Production observer unchanged; retail NO-GO  
**Publication/B6:** ON HOLD

## 1. Scientific purpose and boundary

Map the native machinery that turns a resource-construction request into source selection, resource-mask sampling, geometry construction, retained population ownership, and later reuse. The result must be a **call-and-data-flow model of the compiled executable** supported by explicit instruction/call-site evidence, **not** an attempt to reconstruct Bethesda's original C++ types, names, source files, or intended architecture.

Answer, as far as static evidence allows:

1. What initiates a construction request, and what native boundary receives it?
2. Which explicit arguments and implicit state are used, where do they originate, and which values influence source selection and mask sampling?
3. Which operation samples or produces the effective resource mask, and under what conditions is it bypassed?
4. Which operations construct resource regions, copy completed geometry, and establish ownership by a retained source population?
5. Which lookups or guards reuse populations, and which observed mutations invalidate a claim of continuous ownership?

**Do not equate a static path with an observed historical path.** This assignment cannot by itself identify the first successful query that produced Save52's retained resource population or prove the first-construction/reuse hypothesis. A complete map may contain verified gaps. Negative or ambiguous findings are acceptable deliverables; do not fill gaps with guesses.

## 2. Baseline and source inspection

Before analysis, inspect the actual repository, current branch/HEAD, `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, and the current research navigation/provenance documents. Read D5A–D5I, D5L–D5P/R1–R3 relevant experiment reports, native ledgers and review records, especially D5P/R3's rejected Grid-membership scan and R3's consumer-selection alternative. Reuse existing verified exports/annotations, but check their exact provenance and distinguish previous inferences from direct observations.

Pinned research baseline to verify before using any address: Starfield **1.16.244.0**, `Starfield.exe` SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Verify associated ESM/PlanetData, SFSE and Ghidra database identities against local durable records where relevant. Addresses in this brief are **preferred static virtual addresses at image base `0x140000000`**, never presumed live addresses. If installed pins or Ghidra state differ, stop affected conclusions, report the mismatch, and do not silently translate offsets.

Use the existing Ghidra project **read-only** (prefer established `-readOnly -noanalysis` export procedures). Do not reanalyse or rewrite the shared database merely to generate the map. Task-owned exports, scripts and transient data may live under ignored `.local-work/`; do not resurrect historical enormous loose-file audits or introduce unrelated infrastructure work. Never call native game functions from the live game to infer semantics under this assignment.

## 3. Required mapping strategy

**Map in both directions, reconciling at independently observed boundaries:**

- **Backward:** from the effective mask-sampling operation and source-specific construction call to argument assembly, source selection, coordinates, context acquisition and initiating callers.
- **Forward:** from the construction request through visited guard, retained-map lookup/miss, geometry generation, successful region copy, final ownership and subsequent retrieval.
- **Cross-cutting:** source/manager identities, lifecycle and mutable Grid/consumer-container relationships; identify when two pointers refer to the same object and when that assertion is not justified.

For each material function or call site record: executable VA and RVA; concise behavioural name **assigned by research**; caller(s)/callee(s); call-site address; observed argument register/stack position or state offset; data width/representation where supported; return/side effects; relevant control-flow conditions; source instruction range/export receipt; and confidence classification. Do not present inferred declarations as original C++ signatures. Disambiguate arguments from object fields, globals, thread-local state, post-call outputs and values calculated downstream. Unresolved ABI details must be marked explicitly.

Track individual values, not only functions: query point/co-ordinates and coordinate transforms, source geographic descriptor, native source pointer, retained/current Grid pointer, manager/context, resource/definition inputs, sampled mask, region bounds/ordered point words, wrapper/resource-map ownership, visited status, and lookup result. Trace transformations and units where supported; avoid imposing an invented world-space interpretation. Explicitly distinguish **a source-map lookup from actual successful construction**, and **map insertion/wrapper allocation from fully copied, retained geometry**.

### Priority consumer-selection provenance route

Investigate R3's alternative to scanning a mutable ordinary Grid:

- Spatial-cell lookup at `0x140985870`.
- Enumeration via virtual `+0x10` and materialization into caller-owned chunks.
- Cell helper `0x140988240` and downstream `0x140988ab0` (known to append to caller storage, **not** an observer-safe membership query).
- Provider's retained Grid field at `W+0x100` and selected entry copied into `W+0x38` at `0x14079fa90`–`0x14079fa93`.

Determine exactly **what selection is witnessed**, how it flows into the construction provider and whether that witness can be correlated with mask sampling and retained source population without relying on complete ordinary-Grid membership. Resolve, where static evidence permits, chunk-container layout, ownership, iteration termination, aliasing, consumer selection criteria and mutation hazards. Identify the precise remaining assumption(s) that would make invocation-selected provenance insufficient for the full scientific chain. Do not call the helper, take the Grid lock or propose a detour as already safe merely because it is identifiable.

### Retained-Grid hazards and alternative

Preserve R3's observed Grid properties: dynamic count/capacity/backing array, eight-byte members, growth which frees old storage before publishing replacement, count publication before slot fill, and lock at Grid+`0x5c`. Do **not** treat page readability, count≤capacity, repeated header reads or equal pointers as independent allocation/lifetime proof. Document any writers, guards or lifetime boundaries that a future observer would need to qualify. Writer-qualified Grid observation remains a competing alternative, not the default solution. The rejected `n<=256` bypass/counterfactual is **never** deployable production code.

## 4. Evidence and inference discipline

Each edge in the resulting map must carry one of these labels:

- **ESTABLISHED (static):** supported by exact instruction and call-site evidence for the pinned executable; does not establish an actual retail invocation.
- **ESTABLISHED (executed):** independently supported by existing qualifying native fixture/live evidence, with the evidence envelope identified.
- **INFERRED:** plausible interpretation constrained by inspected instructions but not uniquely established.
- **UNRESOLVED:** missing call path, data origin, side effect, synchronization or evidence needed to distinguish interpretations.

Use these distinctions consistently in diagrams, tables and narrative. If evidence conflicts, preserve both observations and record the specific contradiction. Never use a successful geometry match to retroactively choose a mask, or mistake first-observed construction for first-ever construction. Source pointer equality without qualified lifetime is not historical identity. Clearly separate the *mask as a sampled generation value* from the data-flow path that determines it; verify whether its representation really is a resource-membership bitset before assigning individual bits to resources. The research must not assume the illustrative binary explanation of masks is the verified native semantic contract.

Maintain a compact evidence ledger binding important claims to exact binary and Ghidra/export provenance, addresses, raw instruction windows or existing durable primary receipts. Place proprietary disassembly/decompiler bulk outputs and protected raw captures in local-only ignored storage; tracked docs should contain minimal defensible descriptions and navigation references, not large copied native dumps. Provide falsifiers or missing evidence for every significant inferred link.

## 5. Execution plan and proportionate verification

1. **Inventory and baseline:** Verify pins and previous source/provenance ledgers; establish a small scope matrix of known/unknown call boundaries.
2. **Initial path inventory:** Locate specific producer/consumer, source-map, mask and region-copy sites in the existing Ghidra state. Record direct edges before offering semantic labels.
3. **Parameter/data provenance:** Trace argument definitions, implicit context fields and output consumers across call boundaries; resolve key ambiguities by cross-checking distinct callers and control-flow branches.
4. **Consumer-selection priority:** Map the R3 candidate route and explicitly compare its evidence value and hazards with writer-qualified Grid observation.
5. **Construction and retention:** Extend to sampled mask, point/bounds generation, successful copy, owned population, lookup hit and invalidation paths. Mark branches not actually traversed in available evidence.
6. **Internal cross-check:** Verify address and field arithmetic, call-target resolution, alternative branches, ABI assumptions and consistency with D5I/D5P/R2/R3 receipts. Re-run only focused existing non-retail readers/fixtures if essential and safe; no new observer code or retail testing.
7. **Independent review:** Obtain separate technical/scientific and editorial assessments of claim strength and completeness, correct material defects and bind final exact artifact/diff identities.

Don't expand into full engine reconstruction, global callers of every ProcGen utility, unrelated outpost systems or speculative C++ retyping. If some branch fans out beyond practical bounded analysis, document the boundary, the reason and the smallest follow-up question. Do not stop merely because the primary consumer-selection path remains ambiguous: map the independently accessible request, mask and retention edges and preserve partial results.

## 6. Deliverables

Use existing repo conventions, minimizing redundant documents:

1. `docs/experiments/resource-retained-population/d5q-call-dataflow-map.md` — navigable function/call and data-origin map, tables of boundary inputs and outputs, confidence labels, diagrams (Mermaid or text), and a concise explanation of the construction-to-reuse hypothesis and limits.
2. `docs/experiments/resource-retained-population/d5q-report.md` — aims, methods, pinned sources, established and unresolved findings, consumer-selection versus Grid alternatives, implications for future SFSE instrumentation, and specifically what remains unknowable without live evidence.
3. `docs/experiments/resource-retained-population/d5q-sources.csv` (or existing ledger format) — auditable claim-to-evidence mapping with source identities and classifications.
4. `docs/experiments/resource-retained-population/d5q-review.md` — frozen criteria matrix, independent dispositions, retained disagreements/limits and closure evidence.
5. Focused updates to existing durable research navigation/roadmap documents **only where findings justify them**. Retain local-only task-owned native exports and reproducible read-only commands, without indiscriminate data retention.
6. Complete and task-only patch exports, hash manifest, current Git HEAD/index/status and explicit exclusions; no staging, commit or push.

Do not prepare a retail deployment ZIP or an executable R3/R4/D5Q run card. The result may recommend a **future** diagnostic boundary or required follow-up investigation, not authorize it.

## 7. Authority, safety and preservation

**No Starfield or SFSE launch, debugger attachment to the game, plugin installation/enable/disable, Vortex operation, save/config mutation, live native invocation, or changes to protected game files.** Do not modify or rebuild the production SFSE observer as part of D5Q. Existing R1 `0.2.0`/schema-2 and R3 NO-GO remain unchanged. Do not turn speculative alternative instrumentation into production source.

Preserve original evidence and relevant protected identities; verify only the proportionate protections relevant to read-only work and disclose checks not performed. Respect both existing **40,000,000,000-byte** C:/D: free-space floors for any substantial local acquisition/export. Preserve the workflow division between Codex preparation and maintainer-only live operation. Existing task-owned scratch may be replaced or removed subject to repository preservation rules; do not delete historical decisive evidence. No B6 release or publication authority is granted.

## 8. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **D5Q-AC1 — Authority and provenance** | Correct pinned executable/database and existing research context established; no live/game/plugin/save mutation; protected primary evidence preserved; scope and exclusions stated. |
| **D5Q-AC2 — Query and caller map** | Identified construction/request interfaces and traceable initiating callers with exact address/call-site/argument evidence, or bounded, explicitly justified unresolved edges. No invented top-level signature. |
| **D5Q-AC3 — Parameter and mask provenance** | Explicit and implicit inputs traced through relevant conversions to actual sampling boundary; distinguish what determines mask from mask representation/output; evidence and unknowns documented. |
| **D5Q-AC4 — Construction/retention/reuse** | Forward graph distinguishes visited guard, hit/miss, generation, successful copy, final retained ownership, later retrieval and invalidation, without false causal joins. |
| **D5Q-AC5 — Consumer-selection and Grid alternatives** | R3 candidate selection path studied deeply; witness strength, container semantics/hazards, missing correlation links and alternative writer-qualified Grid route compared; no unsupported claims of complete Grid membership. |
| **D5Q-AC6 — Research evidence discipline** | Function-and-data-flow map cross-referenced to exact source ledger; every major edge classified established/inferred/unresolved; counterevidence and material unknowns preserved; no speculative original C++ reconstruction. |
| **D5Q-AC7 — Focused verification and durable output** | Reproducible read-only extraction/checks, proportional verification, clear navigable outputs and narrowly scoped roadmap updates; no unnecessary production implementation or new retail package. |
| **D5Q-AC8 — Independent review and delivery** | Independent scientific/engineering/editorial review, corrective closure where justified, exact final hashes, complete/task-only diffs and unchanged index; no staging/commit/push, retail GO or publication. |

## 9. Completion and handoff

The assignment succeeds when it produces a **truthful, evidence-linked functional map** that can inform future observer design, even if one or more links remain unresolved. A partial map must say precisely where evidence ceases and which minimal additional static, disposable or separately authorized retail witness would resolve it. Independent acceptance is of the **research account and mapping quality**, not automatic approval of a source-attribution strategy or the historical retained-population hypothesis.

**No D5Q outcome authorizes a new live experiment or changes the standing D5P retail NO-GO.**
