# RG2-D5D — Resource-Source Construction Triggers and Demand Timing

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Assignment:** Offline native investigation and retrospective evidence audit  
**Authority:** Phase A only — **no Starfield launch, attachment, retail observer operation, save manipulation, or live test**  
**Status:** Implementation/research brief for Codex; acceptance criteria AC1–AC8 frozen on issue.

## 1. Why this investigation exists

RG2-D5C established native **process-local retention and reuse** of generated resource populations: a ProcGen-manager-owned map explicitly keyed by a runtime source pointer, with lookup, construction/insertion and destruction/reset paths. That proves a cache-like reuse capability. It **does not** establish that the population for a distant outpost is eagerly generated when Save52 loads, nor that D5B's Feynman V consumer-only observation was a cache hit.

RG2-D5B directly observed the second Feynman V Workshop consume Ionic Liquids, Fluorine and Copper regions exactly matching the previously frozen **mask-3** geometry and differing from mask 0. It **did not capture a qualified initial construction query or effective mask**, despite other generation events; observer scheduling gaps and preceding demand remain possible explanations. The historical generation epoch and first mask remain unknown.

The next highest-information question is **what normally requests construction of a source population, and when relative to game operations**. Investigate ordinary demand and acquisition coverage **before** planning a comprehensive save-load observer. Do not treat an absent observed construction as proof of a cache hit, save restoration or eager load-time generation.

## 2. Boundaries and research questions

### A. Retrospective evidence audit

Examine the previously recorded native evidence and durable reports, especially:

- **Original Feynman V** native geometry/selection controls (four exact regions).
- **Carinae III-a** native geometry/selection controls (three exact regions).
- **Archimedes III** native observation, including D4D witnessed construction and subsequent D4E reconstruction (three exact regions).
- **Second Feynman V** D5B Phase B combined-acquisition evidence and D5C lifecycle conclusions.

For each distinct acquisition, determine exactly what was observed: provider entry/return, source-map lookup, explicit hit, explicit miss, generator call, inserted population, accepted geometry, Workshop transfer, manager/source identity, event timing and debugger coverage. **Do not call an observation a cache hit unless the native hit branch or equivalent decisive state was actually witnessed.** Distinguish *construction witnessed*, *geometry consumed*, *reuse path possible*, and *not instrumented*. Don't infer a hit from a missing constructor event.

Build an evidence matrix with acquisition ID, source/outpost, relevant source-pointer or geographic identity (with lifetime qualification), native probes/receipt references, capture timing, exact affirmative finding, missing data, and confidence/limitations. If old receipts lack enough information, explicitly say so; do not manufacture retrospective cache evidence.

### B. Native demand-path analysis

Starting from the D5C manager map and provider boundaries, trace **actual callers and triggering paths** sufficiently to distinguish:

1. Terrain/cell or planetary streaming and preparation;
2. Planetary landing, travel or worldspace transitions;
3. Outpost/Workshop initialization and area-resource evaluation;
4. Save deserialization, restore callbacks and load-time initialization;
5. Other relevant background or task-scheduled requests encountered on the path.

Identify **which operations can reach a map miss and synchronous population construction**, which merely read existing populations, and which call sites are conditional. Trace upstream to a meaningful trigger, not merely the immediate function pointer. Record exact native VAs, caller/callee and guard details, object/manager lifetime boundaries, and evidence provenance under the pinned build. Avoid unbounded surveys of all terrain or save systems.

In particular, determine whether any **positive native call path** links loading Save52 (or a generic saved-game load) to construction of resource populations for **distant, unvisited outposts**. Absence of a path in a bounded trace is *not* a global proof that no such path exists. Conversely, a generic world-init caller is not proof that Feynman V is populated at load.

### C. Timing and acquisition-window reconstruction

From existing journals/logs and static control flow, reconstruct only the timing that evidence supports: process start/main-menu, save-load activity, travel/landing, source creation, Build Mode and Workshop evaluation, and controller arming/phase switches. Identify the earliest **ordinary demand point** and earliest practical **continuous observation point** for the selected second Feynman V source `0:37536:20928:0029d20e`.

Explicitly analyze D5B's two breakpoint-phase gaps and whether construction may have occurred before relevant arming, during travel/streaming, or during gaps. Do not assert relative timestamps that existing evidence lacks. Differentiate geographic source key from 64-bit runtime source-pointer identity and distinguish cache/manager lifetimes.

### D. Hypotheses and subsequent experiment

Test competing explanations against the actual evidence, at least:

- Lazy construction during landing/terrain preparation, followed by Workshop consumption;
- Construction during an interval not covered by D5B;
- Reuse after another request earlier in the same process;
- Construction during save-load initialization;
- Restoration of a persisted population without ordinary construction.

For each: supportive evidence, contradictions, missing decisive operand/event, and an observation that could discriminate it. The last two are **not default hypotheses**. Prioritize a minimal, early, source-qualified observer placed around the **first plausible ordinary demand**. Recommend a fresh-save/load lifecycle observer only if the findings warrant it or simpler demand windows cannot resolve the question. Preserve Feynman VIII-b resource substitution as a later failure-mode question, not a reason to bias canonical timing results.

## 3. Inputs and preservation

- Repository durable materials: RG2-D4D/D4E, RG2-D5A, RG2-D5B Phase A/B, RG2-D5C and their native evidence/receipts, provenance and review records. Discover actual paths within the repository rather than assuming guessed filenames.
- Installed, pinned native build: Starfield.exe **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; consult repository pins for associated assets before use.
- Follow project `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md` where present, completion contract and independent-review protocol. The latest applicable durable instructions take precedence where they are more specific; report any conflict rather than silently deciding.
- Installed assets, protected saves/backups, original captured receipts and historical frozen analyses are **read-only**. Never write to them. Keep raw native/proprietary bytes, screenshots and machine-local acquisition outputs in approved ignored local-work locations. Publish only reproducible, appropriately sanitized authored evidence and references. Do not migrate large local evidence into Git.
- Preserve D2–D5C results and the seven indeterminate Save52 resource associations. Do not change the resource predictor or force a mask choice; D5B's exact mask-3 geometry correspondence is not a direct historical mask observation.

## 4. Method and expected deliverables

1. **Scope/authority manifest:** actual HEAD, pre-existing working changes, native evidence pins, observed inputs, expected protected artifacts and exact offline permissions. If the earlier Codex brief is an existing uncommitted file, identify it separately in complete versus task-only accounting.
2. **Retrospective acquisition matrix:** each prior site's precise positive and negative *instrument coverage* findings, with cache hit/miss only when proven; especially distinguish the original Feynman V, Carinae III-a and Archimedes III evidence from D5B.
3. **Native trigger/call-path register:** caller and callee addresses, conditionals and ownership context, manager/source identities, path to possible construction, relevant native code/extract provenance, and evidence classification. Document call graph portions needed to justify conclusions, not pages of uninterpreted pseudocode.
4. **Demand/timing assessment:** which events could construct before Build Mode, what can genuinely happen on save load, and coverage limits of old experiments. Provide an evidence-based ranking of earliest meaningful observation windows.
5. **Hypothesis/discriminator matrix:** competing explanations, counterevidence, what would distinguish them, and whether any can be ruled out.
6. **Recommendation and optional *draft* run card:** one least-intrusive next experiment with target, instrument boundary, coverage start, source-identity qualification, positive success tiers and no-hit handling. Label **NOT AUTHORIZED**. If no test is justified, state what static finding is needed next. Do not build an elaborate live observer in this brief.
7. **Durable report and editorial pass:** place documents under a discoverable `docs/experiments/` investigation directory, update navigation/links, and distinguish verified native facts from inference.
8. **Verification and independent review:** repeatable pin/protection checks, bounded relevant tests (if helpers change), scientific and engineering review plus editorial finalization, frozen AC matrix, reviewed completion record, verified complete and task-only diff manifests and SHA-256s. No stage/commit/push.

### Scope control

Prefer targeted Ghidra/native-reference research, local receipt interrogation and small read-only verification helpers. Disposable synthetic tests are allowed if they answer an identified question. No new general-purpose observer framework, save parser, extensive dynamic instrumentation or geometry-model rewrite. If investigation exposes a larger dependency, record a bounded follow-up instead of silently expanding the assignment.

## 5. Frozen acceptance criteria

- **AC1 — Authority, baseline and preservation:** Offline-only execution; HEAD and index preserved; protected native assets, saves, evidence, screenshots and local analysis projects unmodified; current repository instructions followed.
- **AC2 — Prior-acquisition audit:** Original Feynman V, Carinae, Archimedes and D5B classified by exact native evidence and probe coverage; no inferred cache hit from non-observation.
- **AC3 — Construction-trigger provenance:** Trace and cite relevant native callers, guards and manager-map lookup/miss/construct/reuse boundaries through meaningful upstream demand operations.
- **AC4 — Load-versus-demand distinction:** Explicitly assess travel/terrain/outpost/save-load mechanisms and limitations without presuming eager Save52 cache population or globally proving its absence from bounded negative findings.
- **AC5 — Timing and identity:** Reconstruct supported observation windows and D5B gaps, distinguish geographic keys from lifetime-qualified source pointers, and determine best feasible earliest demand window.
- **AC6 — Discriminating next step:** Rank hypotheses, identify missing decisive evidence, recommend the least intrusive qualified next observation; any live run card remains an unapproved draft.
- **AC7 — Reproducibility/editorial:** Durable scoped registers, cited native pins and receipt identifiers, reproducible read-only checks, frozen predictions/controls preserved, clean editorial finalization.
- **AC8 — Independent acceptance and delivery:** Independent scientific/engineering and editorial review of final snapshot and completion record; AC1–AC8 explicitly assessed; final complete/task-only diffs, exclusions, manifests and hashes verified; no staging, commit or push.

## 6. Evidence and interpretation rules

- Use **observed**, **proved by pinned static branch**, **conditional inference**, **plausible**, **unknown** and **not instrumented** consistently; avoid percentage correctness over an incomplete Save52 ground truth.
- An exact native geometry comparison establishes geometry correspondence, **not** initial construction-query provenance.
- A source-pointer map hit establishes reuse within its qualified manager/source lifetime; it does **not** demonstrate process-crossing or save-crossing persistence.
- A provider entry or return without branch-state evidence may not distinguish hit from miss; a generation event on another source does not inform the selected source's cache status.
- No generation observed under incomplete coverage is **not** evidence of no generation. A missing positive native path in bounded static tracing must be scoped.
- D5C static cache implementation is inherited native evidence; separate what this investigation independently rechecks.
- An unqualified source address can be reused for a different lifetime. Preserve identity and temporal uncertainty.
- Existing ten native geometry controls must remain intact; as this is an audit/documentation task, record whether they are **integrity-checked** or actually **rerun**, not both by implication.

## 7. Stop conditions and completion report

Stop and report if protected inputs or provenance cannot be verified, if a necessary native boundary is unavailable without retail execution, or if further work would require expanding to a general save parser or a newly instrumented Starfield session. These are bounded scientific outcomes, not authorization to proceed live.

Codex's final response should summarize (a) which earlier captures positively prove construction versus reuse, (b) what the native demand paths support about ordinary timing, (c) the remaining ambiguity around Save52, (d) the recommended next discriminating test and its authorization status, (e) exact tests and protection verification performed, (f) independent ACCEPT/REVISE result and any limitations, and (g) complete/task-only patch paths and suggested commit. **Do not stage, commit or push.**

**Publication gate:** B6 remains on hold. **Live phase:** NOT AUTHORIZED.
