# RG2-D5Z — Visited-Source State: Provenance, Persistence, Reset and Capacity

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Type:** Offline native and conditional read-only save research  
**Status:** Implementation/research brief; approval of this brief authorizes *only* the specified offline work.  
**Parent questions:** D5R normal construction-query selection remains OPEN; D5X-B1 target-first construction remains unproved.  
**Retail/SFSE:** NO new game launch, attachment, plugin build/deployment or retry. **B2 and publication/B6:** NOT AUTHORIZED / ON HOLD.

## 1. Controlling objective and completion contract

**D5Z-CQ:** Determine how the ProcGen visited-source state is created, populated, read, preserved, cleared and—if applicable—serialized or reconstructed across process initialization, save loading, landscape streaming, ordinary construction and world/manager transitions; establish what triggers a broad ProcGen reset and whether visited-state capacity or memory pressure can trigger or constrain it.

Do **not** quietly narrow this to locating the visited-check instruction or listing known reset call sites. The objective is a usable state-transition model explaining the **initial condition inherited by destination streaming**, not merely individual function bodies. Distinguish source visits from PC visits and visited-list identity from source pointers and source-population cache keys.

Freeze these controlling questions at assignment start:

- **Q1 — State representation and complete writer/reader census.** What is the visited identity, what memory layout stores it (count/capacity/data/element width/allocation owner), and which native paths append, read, replace, erase, clear or reconstruct it? Include indirect and exceptional writers where relevant.
- **Q2 — Persistence and save-load provenance.** Is the visited list saved as such, restored from serialized data, rebuilt from other persistent state, or initialized transiently? Exactly which state and chronological operations establish the visited contents from process start through Save52 load and the first destination demand? Distinguish native-code capability from historical Save52 execution.
- **Q3 — Reset causality and purpose.** What direct and indirect conditions invoke broad ProcGen reset, what structures does it clear and in what order, and what operation follows? Determine whether resets arise from world/owner/component changes, load/reload/teardown, failure/recovery, state capacity or other evidenced causes. Investigate *why these conditions make a reset necessary* as competing architectural explanations, labelling design-purpose inference separately from compiled fact.
- **Q4 — Capacity and resource bounds.** Does visited state have a fixed logical maximum number of entries, dynamic capacity, allocator limit, memory-use limit or guard? How does it grow, what happens on allocation failure or overflow, and is any capacity/memory condition causally linked to reset? Quantify storage per member and capacity/memory calculations **only to the precision established by actual native instructions/allocator contracts**.
- **Q5 — Consequences for generation and observed B1.** Integrate the above into a concrete conditional sequence explaining how a selected source can reach visited-bypass without a source-map lookup; assess whether B1's reset and bypass evidence distinguishes restored state, earlier same-session processing or incomplete capture. Do not attribute B1 target identity or historical winner without evidence.

The outcomes are **COMPLETE**, **INCOMPLETE**, or **BLOCKED** per current `docs/RESEARCH_EXECUTION_PROTOCOL.md`. A supported negative finding that visited state is transient is a legitimate COMPLETE outcome **only with positive evidence of initialization/absence of relevant serialization pathways**, not merely an unsuccessful keyword search. INCOMPLETE requires REWORK under the same assignment while material authorized avenues remain; BLOCKED requires the exact indispensable missing edge/input, searches/alternatives exhausted, evidence of the barrier and smallest permission or capability needed. Do not treat a documented dependency as task closure.

## 2. Prior evidence and required baseline

Read the current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, reviewer procedure, and existing completion-contract template. Read D5Q, D5R, D5S, D5V, D5W, D5X, B1 and D5Y source/evidence records. Treat historical conclusions as evidence to check, not assumptions to be repeated.

Reverify the pinned installed Starfield executable, ESM, PlanetData, SFSE and actual Ghidra project identifiers before using hardcoded addresses or layouts. D5V's baseline is **Starfield 1.16.244.0**, preferred image base `0x140000000`; all native VAs are *static* unless explicitly relocated. Stop affected work and escalate an identity mismatch rather than transferring addresses to another build.

Known native anchors to verify and extend:

| Operation | Previously identified native site / field | What is already supported, not yet an exhaustive proof |
|---|---|---|
| Provider visited check | `0x14079fc37..0x14079fcd4` | Source `+0x68` identity compared with ProcGen visited count/data at `+0x48/+0x50`; hit bypasses construction before map lookup |
| Visited append | `0x14079ff3e` | Occurs after generator attempt; not gated on complete successful geometry |
| ProcGen broad reset | `0x14079ddf0` | Clears visited and retained population structures under manager/reset orchestration |
| Manager broad reset | `0x140788e70` | Drain and exclusive module-reset dispatch; ProcGen reset invoked through registered module slot |
| Owner/descriptor transition | `0x140789ce0` | Conditional same/different context branches may reset |
| World component release | `0x14078cf00` | Conditional reset when component identity changes |
| Load/phase/teardown | `0x141815620`, `0x141827960`, `0x141896280` | Drain and conditional reset routes; not a verified complete historical save-load timeline |
| Source retirement | `0x140982b70` | Removes source pointer-map entry without necessarily clearing visited identity |
| D5X-B1 | reset records, two reset-unlock witnesses; B1 report | No qualified target cold-first witness; target-compatible bypass-only observations are *conditional*, not certain native identity |

Do not mistake a source-map cache hit for visited bypass, or a new process for proof that *no earlier post-load demands* occurred.

## 3. Required investigative work

### A. Visited state: data structure and all mutation routes

Trace direct and indirect xrefs to the visited fields, append/growth helpers, constructors, destructors, copies, serialization calls and reset code. Establish element identity and structure layout with native register/field evidence. Investigate count/capacity/data and thread synchronization, allocation/move/copy/free, integer overflow checks, allocator failure and any duplicate-prevention logic. Distinguish a dynamic allocator that can run out of memory from an explicit logical size cap or a capacity-triggered reset. Do **not** infer a maximum from a single observed capacity or a 32-bit counter type.

Create a table of each writer/reader/clearer with native address, owner/receiver, trigger, lock/ownership scope, effect on visited identity and source map, and evidence class. If exhaustive writer coverage cannot be demonstrated, identify the exact untraced alias or path and continue the authorized search.

### B. State transitions during process start, save load and destination demand

Work from both ends: trace serializer/deserializer registration and save-load callers **forward** toward ProcGen initialization; trace visited-store construction/reset/writes **backward** toward their data producers. Determine whether the ProcGen object is recreated, cleared or retained across load transitions and in what order landscape streaming and source-demand tasks become eligible.

For each load stage, distinguish (1) code permits, (2) native ordering guarantees, (3) existing capture confirms, and (4) remains unknown for Save52. D5X-B1's main-menu / pre-travel / arrival checkpoints may be used where independently authenticated; they do not supply exact native transition timestamps or guarantee no prior unrecorded activity.

**Save investigation is specifically in scope if justified by the persistence question.** Inspect existing save-format notes first; trace relevant save serialization and restoration paths. Where the state is plausibly serialized, inspect only authorized copies of protected Save52 and/or existing controlled saves **read-only**, with precise field/record/schema evidence and independent verification. No save mutation, game loading or resaving. If no direct visited serialization exists, look for indirect persistent inputs before concluding runtime reconstruction; support an absence claim by bounded complete path coverage, not search failure. No open-ended unrelated save archaeology.

### C. Reset: triggers, rationale, limits and consequences

Enumerate the complete relevant caller chains and predicates leading to ProcGen reset (including module dispatch/virtual calls), characterize reset sequencing, exclusive guards, worker draining, pending tasks, owner/world/descriptor transitions, memory cleanup and post-reset rebuilding. Explicitly test the hypotheses that reset:

- enforces a world/owner/component context change;
- reinitializes incompatible landscape and ProcGen state after load or teardown;
- recovers from failure or memory pressure;
- reclaims visited-array memory or responds to a maximum-entry condition;
- serves other evidenced lifecycle purposes.

For each, record supporting and contradictory evidence. A memory-pressure explanation requires an actual predicate/call chain, not general intuition about caches. Determine whether repeated source retirement without visited removal can accumulate identities in one epoch, what bounds an epoch, and how capacity growth or allocation failure is handled. Do not claim a gameplay bug from the difference between visited lifetime and cache lifetime.

### D. Integration with B1 and the gameplay-stage checklist

Revisit the preserved D5X-B1 evidence without altering originals. Establish the strongest warranted inference from reset/unlock counts and pre-travel watermark; distinguish matched cold certificate, mere reset-site execution, source-map hits and visited bypasses. If the 119 conditional target-compatible bypasses still cannot be linked to a definitive source identity or append event, say exactly why and identify the minimum missing observation. No new retail run or observer repair is authorized by this brief.

Create a **durable, flat, player-activity-grouped checklist** at `docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md` with the headings:

1. Game start / save load
2. Fast-travel initiation
3. Destination streaming / construction
4. Outpost arrival / Workshop and extractor consumers
5. Departure / return / reset

Use `- [x]` only when the specified *operation* has a grounded complete native explanation at its declared scope; `- [ ]` when a relevant dependency or actual player-action mapping remains open. For each line link the supporting evidence and distinguish **native mechanism mapped** from **specific B1 event observed**. Preserve all relevant items from the checklist discussed with the maintainer, and update checkmarks only for newly demonstrated findings. This checklist is a durable research navigator, not an assertion that every checked action occurred in B1.

## 4. Methods, figures and safeguards

Use existing Ghidra state read-only, authenticated local static/source evidence, task-owned offline analysis scripts and disposable processes where necessary. Native code may be tested in isolated hosts only under the existing protected-input and ownership rules. No installation, Starfield launch, debugger attachment, SFSE change, Vortex operation, protected-save write, Git staging/commit/push or B6 publication. Verify the **40,000,000,000-byte** caller-available disk floors on each C: and D: where applicable. Keep proprietary disassembly, raw saves, memory dumps and analysis DBs local-only; provide tracked source provenance, not bulk proprietary payloads.

**Visual outputs are mandatory and must clarify causal sequence rather than decorate it:**

1. **Visited-state lifecycle SVG** showing creation, lookup, append, persistence/restoration (if any), source retirement, source-map relationship and reset, with supported and unresolved edges distinctly styled.
2. **Reset cause/effect SVG** showing verified call/predicate paths and state changes. Indicate conditional, inferred and contradicted reset purposes separately.
3. **Save-load → streaming timeline or state-transition SVG** distinguishing proven native order from B1 checkpoint windows. Do not fabricate durations, worker order or a complete historical timeline.

Use reproducible machine-readable backing data, legible labels and exact evidence links. These figures are non-spatial; **do not invent coordinate axes**. For any additional *spatial* figure, use documented **absolute native coordinate axes**, verified outpost/beacon centre and native 150-unit boundary where applicable, and full-extent companion view when useful. Never silently substitute source-relative display coordinates for native data.

## 5. Completion, reviewer duties and delivery

The independent scientific/completeness reviewer must explicitly challenge: (i) whether the visited writer/serialization path search was exhaustive enough for the claimed conclusion; (ii) whether reset call-chain coverage is adequate; (iii) whether count/capacity/allocator evidence really establishes an upper bound or lack of one; (iv) whether any open avenue could change the load-origin interpretation; and (v) whether historical B1 events have been wrongly inferred from static operations. Engineering/evidence and editorial reviews independently check actual source/fixture claims, code provenance, visuals, scientific phrasing and exact final snapshots. No ACCEPT for mere accurate documentation of incomplete controlling questions. Maintain the active ledger from near task start, with alternatives, corrections, counterexamples and specific dispositions.

### Frozen acceptance criteria

| ID | Mandatory requirement |
|---|---|
| **D5Z-AC1** | Exact provenance, approved offline scope, protected input and authority checks; no unauthorized native/game/save/Git actions. |
| **D5Z-AC2** | Freeze D5Z-CQ/Q1–Q5 and maintain a contemporaneous dependency/experiment ledger with exact evidence and no silent narrowing. |
| **D5Z-AC3** | Establish visited representation, identity, all relevant readers/writers/clearers, growth and synchronization to a defensible coverage standard; distinguish incomplete writer census. |
| **D5Z-AC4** | Determine save persistence or runtime reconstruction with positive native evidence; conduct justified read-only save inspection or demonstrate exact inability to do so. |
| **D5Z-AC5** | Establish triggers, call chains, ordering and effects of broad reset and compare architectural-purpose hypotheses without presenting inference as fact. |
| **D5Z-AC6** | Establish visited count/capacity/allocation mechanics, quantitative memory bounds where provable, failure/overflow behaviour and any demonstrated relationship to reset; no invented hard maximum. |
| **D5Z-AC7** | Integrate findings into a conditional save-load → demand → visited-bypass/construct state model and critically re-evaluate actual B1 evidence without false historical firstness. |
| **D5Z-AC8** | Deliver and validate the durable gameplay-stage checklist, with evidence links and clearly scoped ticks versus unresolved tasks. |
| **D5Z-AC9** | Provide three readable reproducible causal/state SVGs and backing data; figures preserve evidence strengths and do not invent timelines or coordinates. |
| **D5Z-AC10** | Enforce COMPLETE/INCOMPLETE/BLOCKED question-level review; scientific completeness reviewer challenges highest-value omitted avenue; independent engineering/evidence and editorial reviews. |
| **D5Z-AC11** | Durable report, state-transition map, source ledger, active ledger, visual gallery/checklist, test controls, complete and task-only diff manifests with exact byte checks, exclusions and status; no staging, commit or push. |

Deliver concise materials under `docs/experiments/resource-retained-population/` using established naming (`d5z-report.md`, `d5z-state-transition-map.md`, `d5z-investigation-ledger.md`, `d5z-sources.csv`, `d5z-review.md`, `d5z/` for SVGs/data), plus the checklist above. Propose any changed path only if repository convention requires it. Follow the editorial standard and independent exact-final-snapshot review. Supply exact hashes, applicable reproduction commands and documented limitations. Retain earlier results and protected originals unchanged.

**Terminal rule:** COMPLETE means the *original controlling objective* is answered within the stated ordinary native/save scope. If a consequential serialized field or reset trigger remains available to investigate, the task is INCOMPLETE and must continue under this same assignment. A genuine unavailable capability/permission may yield BLOCKED/ESCALATE with its exact proof and narrow next action. Neither a new diagram nor a discovered caller alone is completion.

