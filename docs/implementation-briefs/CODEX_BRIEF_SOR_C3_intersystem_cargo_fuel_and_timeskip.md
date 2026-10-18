# Codex research brief — C3 inter-system cargo fuel, endpoint asymmetry and time-skip interaction

**Project:** `starfield-outpost-research`  
**Type:** Bounded offline native/PEX/definition/save research; documentation and independent review  
**Authority:** Offline read-only investigation and authored research/documentation changes only. No game launch, live observer, deployment, modified saves, package/plugin implementation, staging, commit, push or publication. Preserve original saves, executable, ESM/BA2/PEX, analysis databases and repository history.

## 1. Research objective and scope

Complete the C1–C3 cargo-link research by explaining **how Helium-3 actually enables and sustains inter-system transport**: acquisition, availability, consumption, rate, endpoint-specific rules, replenishment, persistence, failure/retry and effects on scheduling. Examine the operational mismatch between **production catch-up** during wait/sleep and **one-shot cargo-transport timer progression**. Treat these as linked questions: fuel production and local delivery may accumulate while freight voyages do not.

The user reports a gameplay observation: an inter-system cargo link needs fuel at the **sending/origin** side to send freight, while the receiving side need not be fueled merely to receive it. Treat this as a positive user observation within its scope, **not** as proof that fuel at the receiving end can never affect unloading, return freight, subsequent departure or retry. Verify the native mechanism and evaluate those distinctions without retroactively imposing new acceptance conditions on the observation.

Reuse the committed C2 [report](../experiments/cargo-links/transport/report.md), [cycle](../experiments/cargo-links/transport/cycle.md), [timing](../experiments/cargo-links/transport/timing.md), [remote lifecycle](../experiments/cargo-links/transport/lifecycle.md), [saved evidence](../experiments/cargo-links/transport/saves.md) and subsequent native transit continuation (`transit.md`) if present. Reuse C1 pairing/UI, S1 capacities/fuel-receiver semantics, S2 local transfer and production, and E1–E3 elapsed production as established baselines; **do not reopen those investigations** except where their interfaces are needed to answer C3. Confirm real paths, provenance and installed executable/ESM/script identity rather than relying on assumed filenames or version values.

## 2. Mandatory scientific questions

### A. Fuel sourcing, accounting and consumption

Trace the *actual* native/PEX path from available Helium-3 inventory through recipe/eligibility checks and item withdrawal to cargo-link readiness, ship stage transitions and subsequent replenishment.

- Which physical inventories can provide fuel (incoming output-link graph, adjacent storage, pad fuel marker, cargo compartments, ship, or other)? Distinguish a logical fuel-receiving marker from an independently materialized container. Can items be transferred directly from source inventories without ever entering the marker?
- How much He-3 is required and **actually consumed**, at precisely which event(s)? Determine whether the amount is fixed, per outbound departure, per round trip, per leg, per retry or modified by system/distance/perks. Separate *admission/checking* from *removal*; a `CanProduceForWorkshop` result does not itself prove fuel was consumed.
- What happens when partial fuel is available, no fuel is available, or a supply becomes available after a failure? Is the relevant threshold checked when arrival, loading, departure or return callbacks run? Explain whether failed attempts consume fuel and whether retries repeat an unload or other freight operation.
- Identify potential modifiers and how they enter the actual fuel arithmetic—installed keywords, AVs, perks, actor state, script properties, mutable settings, and construction/upgrade variants. Do not presume an item description, quest comment or capacity perk proves a consumed quantity.

### B. Endpoint asymmetry and bidirectional operation

Distinguish **receipt of incoming cargo**, **unloading**, **loading reverse-leg cargo**, **return travel**, **initiating the next leg** and **continued operation**. Derive each stage's fuel predicate, identify which pad supplies it, and explain whether the same ship can carry reverse freight from an unfueled receiver. Check whether a fueled endpoint can restart a stalled shared route even when the ship is currently at the unfueled endpoint. Avoid assuming “origin” is a permanent role on a ship alternating between pads.

Include a concrete two-pad state table for origin fueled/unfueled × remote fueled/unfueled × ship at either endpoint, noting each stage that advances, stalls, consumes fuel or retries. If the code supports a narrower table, clearly label rows outside grounded coverage rather than fabricate outcomes. Compare ordinary cargo links as a negative control (`RequiresFuel=false`).

### C. Timing, retry, remote state and elapsed-time discontinuity

Carry C2's **30/15/30 source-second defaults**, cached conversion through the ground-calendar setting, native quantized game-time timer, wait/sleep suppression, one-shot rearm, and separate AI movement/package completion as *historical findings to verify at interfaces*, not new discoveries to redo wholesale.

- Map the precise fuel-shortage retry call chain and its effects on cargo already aboard, partial unloading, incoming storage, ship inventory, and next timer. Identify which state change permits resumption and whether there is an event-driven wake-up or only retry polling.
- Explain how supply changes during travel, during wait/sleep, after a timer becomes overdue, and when a pad/ship is unloaded or unresolved affect a route. Distinguish graphic unload, native handle resolution, VM binding and actual AI completion.
- Determine what fuel production, local transfer, storage saturation and cargo shipment can *each* accomplish during an extended wait/sleep or other time jump. Work through an illustrative **explicitly conditional** network where He-3 and freight production continue but transport dispatch is suppressed; derive what may accumulate, what may stop at capacity and what voyage stages are missed. Reuse exact E1/S2 clock and insertion rules rather than assuming linear production or infinite stock.
- Differentiate normal distant gameplay from explicit waiting/sleeping, fast travel, load/reload and paused/disabled timers. Identify what is persisted as timer/VM/ship/fuel/inventory state and what is rebuilt; don't conflate saved count with current fuel-ready state.

### D. Saved evidence and runtime correspondence

Locate representative inter-system links in the protected historical save corpus (including C2's previously qualified stocked examples) and join: both pad markers, cargo child containers, physical fuel-source references, local incoming graph, shared ship/hold, link endpoints and relevant saved script/timer/producer state *where supported*. Use positive instance-level identities and contents, not guesses from EditorID names or a single screenshot. Document the complete correspondence between persisted data and native decision inputs, with explicit unsupported extras or unjoined fields. Distinguish saved inventories from present-time runtime values and historical transitions that the snapshots cannot establish.

Do **not** create a generic save extractor or fuel simulator as a deliverable. Small bounded read-only evidence helpers and arithmetic tests are allowed when necessary for the research.

## 3. Reporting and evidentiary standard

Begin `docs/experiments/cargo-links/fuel/report.md` (or another consistent C3 directory selected after inspecting the repo) with an **answer-first table**, including: exact consumption amount and timing; fuel source; departure/receipt/return asymmetry; retry and recovery; distance/perk effects; and the wait/sleep production-versus-freight implication. For each give **established / strongly supported / unresolved**, source type and any meaningful limitation. Follow with native causal traces, readable state diagrams/tables, saved-case joins, and worked fuel/time examples.

Use **reasonable engineering confidence and explanatory sufficiency** agreed in P1. Identify concrete positive native paths and corroborating save/definition evidence; no demand to exhaustively disprove hypothetical unseen alternatives. Conversely, do not promote a predicate or recipe into demonstrated consumption, or an executable route into proof of its particular historical execution. A bounded review of relevant known consumers/callers supports meaningful negative statements; record precisely what was searched. Select the strongest supported conclusion and stop when it explains the ordinary covered behaviour. Distinguish scientific confidence from assignment completion, live verification and publication classification.

Before major new instrumentation or parser engineering, assess information gain and proportionality. A live validation proposal is permitted **only** for a consequential discriminator that cannot be resolved offline, with preregistered outcomes, minimal user action and expected value; do not implement or execute it here. Do not turn an incidental unknown into an automatic new project.

## 4. Modding applications backlog — mandatory documentation

Add a **separate future modding application** to `docs/BACKLOG.md`, provisionally **Cargo Link Time-Skip Reconciliation**. Capture the observed/predicted mismatch: production and local delivery can advance via elapsed-time work while cargo timer stages are one-shot and not automatically replayed for each missed voyage during wait/sleep. Describe the resulting possible outgoing freight and He-3 buildup, remote manufacturing starvation, and saturation **as conditional consequences, not verified universal gameplay outcomes**.

Record possible design directions for future scoping (not implementation): reconcile missed voyage stages or simulate bounded abstract freight transfers during skips; account for temporal order, available stock, outbound/reverse freight, per-stage fuel consumption, effective capacities, partial unload, returned cargo, pauses, broken routes and conservation of items. Explicitly distinguish reproducing the game's ordinary transport rules from intentionally changing balance. State no mod, plugin, hook or save modification is authorized. Preserve the existing **native cargo-link UI enhancement** backlog entry separately; do not merge them.

Also update any C2/C3 backlog boundary that still inaccurately attributes remote transport generally to C3. Preserve prior historical entries and links instead of silently rewriting their original conclusions.

## 5. Deliverables and frozen completion contract

**Task type:** Scoped offline scientific research plus documentation, not tooling/product implementation.

**Mandatory acceptance (all eight):**

1. Answer-first fuel model explains actual source, threshold, quantity, consumption event(s) and meaningful modifiers, or grounds a *specific* unresolved operand/path after serious bounded investigation.
2. Stage-by-stage endpoint asymmetry table covers arrival, receipt, loading, reverse trip, onward departures, four fuel-side combinations and an ordinary-link control without conflating readiness and consumption.
3. Native/PEX fuel-failure and retry path traces all material inventory/timer transitions; distinguishes no fuel, replenishment and changing supply during a voyage.
4. Explains interaction of production, storage and one-shot transport timers through ordinary distant operation, wait/sleep, travel and reload with at least two reproducible worked cases and explicit source-derived time/conversion rules.
5. Provides grounded saved-instance runtime correspondence and clearly identifies any unqualified fuel/VM/timer/inventory fields instead of presenting a broad census as a decoded join.
6. Adds and reviews the requested **Cargo Link Time-Skip Reconciliation** future mod backlog item; existing UI enhancement remains separate and existing C1/C2/S1/S2 conclusions are preserved.
7. Updates research-state, source/function/provenance/decisions and relevant subsystem indexes proportionately; reports confidence, coverage, falsifiers, negative findings, scope exceptions and required source/permission gates. No unauthorized game/process/save/Git action.
8. Independent review against this frozen brief, primary evidence, checks/regressions and final exact task-only/complete review package; explicit PASS/FAIL/NOT TESTED matrix, retained failures/deviations, protected-input before/after comparisons and readable executive conclusion.

**Optional:** additional independent saved examples or concise proposed player validation if they genuinely discriminate a material remaining question. Optional work cannot become a retroactive gate.

**Negative-result closure:** A finite, independently reviewed inability to establish a particular fuel predicate or serialization join can close that narrow research claim if covered paths, failed attempts, contrary evidence and the exact missing prerequisite are documented; it must not be reworded into global impossibility. An unexplained failure of any mandatory *engineering/checking* criterion remains REWORK rather than scientific completion.

**Continuation authority:** Diagnose and fix in-scope evidence/analysis/test failures, rerun and obtain independent review within the same assignment. No separate follow-up brief for ordinary correctable failures. Approval is required to alter mandatory criteria or expand into live/plugin/save-write work.

**Exit/escalation:** Stop unsafe or unauthorized actions and preserve their evidence; identify any genuinely inaccessible essential input or approval requirement narrowly. Preserve original executable/ESM/PEX, original saves, stopped databases, HEAD/index and both-drive **40,000,000,000-byte free-space safeguards** where the workflow requires them. Avoid invented time, event-count or file-size termination limits; retain integrity, worker/STOP and evidence protection rules.

**Review package:** Follow `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/templates/completion-contract.md` and reviewer procedures. Pin native addresses to the verified build, identify specific functions/VM methods, file bytes/hashes and supported record cases. Run relevant existing regression suites and bounded independent checks. Author UTF-8/LF text with no mojibake and verify links. Create task-only and all-uncommitted complete textual diffs, include untracked authored files without staging, with inventories/ignored-binary exclusions, `git status --short`, hash-bound manifest and exact forward/reverse patch reconstruction in disposable trees. Obtain independent **ACCEPT** for the final reviewed snapshot. Do not stage, commit or push; suggest a Conventional Commit subject for user-approved integration.

## 6. Scope exclusions

No new cargo-link UI plugin, time-skip reconciliation mod, save writer, generic inventory extraction tool, retail observer, gameplay test or deployment. Cargo-link management UI was C1; normal freight and movement/scheduling machinery C2, whose findings are reused. No general reopening of extractor/fabricator production arithmetic, local graph logistics, general chest/display storage or outpost-power investigations. Trace their *interfaces to C3 fuel behaviour* where necessary. If a documented C2 finding is materially contradicted, preserve the counterexample and explain the correction rather than silently rebuilding C2.
