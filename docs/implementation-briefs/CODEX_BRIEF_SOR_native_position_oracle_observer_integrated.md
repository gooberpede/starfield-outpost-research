# Codex implementation brief — SOR native position oracle observer and integrated live procedure

**Status:** IMPLEMENTATION AUTHORIZED; LIVE EXECUTION NOT YET AUTHORIZED  
**Project:** `D:\Projects\starfield-outpost-research`  
**Purpose:** Obtain fresh, identity-bound engine-generated position and terrain-grid observations capable of independently testing the deterministic durable-outpost-position reconstruction.  
**Required return:** One jointly reviewable implementation, qualification dossier, Vortex package, and **complete executable run card**. Do not split these into successive approval assignments.

## 1. Context and binding decisions

The offline reconstruction has progressed substantially: ordinary-outpost identities and bodies, site anchors, terrain-grid representation, saved frames, beacon relocation compensation, and a deterministic model with **23 unchanged frozen predictions**. The most recent resumption corrected reflected-axis handling for packed tags 2/3 and passed **152 tests**, but the independent reviewer correctly returned **ESCALATE** on full native equivalence because no fresh, invocation-associated grid result exists.

The passive SFSE `SorBeaconObserver` **0.1.1** has worked in actual Starfield. Its sampled `BGSPlanet::ProcGen` shared center/radius output is not a reliable current-workshop oracle: center can be retained while radius is reset; ownership/freshness cannot be established by polling. The external software-breakpoint debugger was conclusively **closed/abandoned** following unsafe queued owned traps, thread-suspension failures, and retirement problems. **Do not revive, repurpose, or attach it.** This assignment concerns a **new, narrowly scoped in-process SFSE observation design**. The build-mode spinning-reticle defect is deferred and must not become a task dependency.

Read the current committed repository first, particularly `WORKFLOW.md`, the research completion contract and reviewer instructions, the latest position-resumption report/review/acquisition design, the source and evidence ledger, observer 0.1.1, static maps, frozen position fixtures, and historical observer live-session evidence. Treat paths, addresses, hashes, version numbers, callback assumptions and underlying game binaries as **verify-before-use**, not as a substitute for current repo evidence. Preserve source provenance and maintain separation of independent native observations from offline-derived predictions.

## 2. Objective and acceptance contract

**The task is complete for pre-live review only when ALL these deliverables exist:**

1. An implementation that can capture **fresh, naturally executed native position/grid events**, with a positive identity chain identifying the invoking object/workshop and relevant body/frame, input values, actual engine output, exact provenance and event timing. Any valid observation must unambiguously distinguish native bytes from reconstructed or inferred values.
2. A carefully justified hook/callback architecture and tested lifecycle, including null/unreadable pointers, concurrency/reentrancy, recursion, teardown, invocation pairing, integrity/error recovery and safe non-observation. Prefer **the most narrowly instrumented event boundary that provides the necessary evidence**. Do not silently substitute a shared stale buffer or synthetic calculation for native execution.
3. A runnable, reviewed SFSE plugin build plus versioned **Vortex-installable ZIP** and manifests of binaries, hashes, installed paths and expected game/SFSE compatibility. Preserve observer 0.1.1 and prior baselines. If numbering continues, avoid falsely representing the abandoned external adapter's 0.1.2–0.1.4 as SFSE releases; document the distinct plugin version unambiguously.
4. Credible **disposable/offline qualification**, exercised against relevant native ABI/patch/trampoline behavior and failure conditions. Explicitly explain what disposable qualification **cannot** prove about live Starfield. Distinguish safe hook activation, useful events and model-validation sufficiency.
5. An **exact, ready-to-execute live run card produced now**, not in a later documentation task. Specify preflight programs/commands, verified version/hash/pointer/patch guards, protected saves, disk checks, desired site and operator actions, event readiness and identity requirements, provenance, telemetry, scope, halt and recovery paths, verification of restored/removed instrumentation, postflight, evidence analysis and scientific outcome classification.
6. A single combined critical review package with complete and task-only diffs, manifests, test results, a traceable acceptance matrix and an **independent reviewer decision**. No staging, commit, push, live launch, save modification, or Vortex deployment by Codex before our joint review.

The ultimate scientific aim is to compare **fresh engine-produced grid/frame/position outputs** with frozen offline predictions and establish precisely which algorithmic branches agree, disagree, or remain unobserved. This implementation phase must be designed to do so; it **must not claim full native equivalence before live evidence exists**.

## 3. Acquisition requirements and feasibility discipline

- Recheck the existing static acquisition proposal and actual game functions/call sites. Establish the native **producer and consumers** for the chosen observation boundary and whether it carries the selected frame/grid, translated XY and/or center output. Distinguish the workshop-center helper (`0x140F4AB80` in earlier static mapping) from the terrain-grid selection path (`0x140AD0D3B` in earlier mapping); these are research leads, **not automatic hook approvals**.
- Determine when the function actually runs and what plausible, non-destructive gameplay actions trigger it. A successful hook without a reachable event does **not** establish a usable oracle. Explain reachability evidence and what a no-hit session would mean.
- If direct inline patching is needed, qualify complete-instruction replacement, instruction relocation, RIP-relative operands, register/flags/stack/XMM state, unwind implications, cross-thread execution, hook installation and removal, outstanding in-flight calls, and precise restoration guarantees. Do not reuse external-debugger INT3/replay machinery. Prefer a framework/technique already qualified for the installed SFSE/game version if its contract suffices, but assess its provenance and safety rather than assuming it does.
- Avoid intrusive original-game function calls, fabricated native input, scripted saves and interpretation-changing modification. Observation should follow natural engine invocation. Do not modify outpost centers, build radius, terrain decisions or gameplay. If an approach needs unsafe patching or has unqualified retirement, **do not deploy it**.
- Preserve raw native inputs/outputs and source context before interpreting them. Record invocation identity, native reference/workshop identity (or explicitly incomplete identity), thread, phase, site/form/module identities, source-frame metadata, event sequence and available parent linkage. Do not manufacture complete identity from temporal proximity or player-reported location. Store unknowns as unknowns.
- Derive comparison expectations from the pre-existing **frozen** predictions only after primary evidence capture; don't retune expected values or inject reconstructed outputs into the acquisition channel. The independent reviewer must test the validity of comparisons and branch coverage.
- If grid and center paths are independently observable, design separately enabled collection channels and justify both. **Grid evidence is the priority** because center tuples alone have not independently validated the terrain-coordinate transformation. Do not make a low-value center-only session the default if static evidence indicates the grid producer is reachable via a different user action.
- Keep data capture generous and durable; don't impose arbitrary short counts or time caps. Continue through expected partial scientific observations. Stop for machine/instrumentation integrity failure, disk guard failure or operator-directed stop. Explicitly separate scientific completeness, observer health, game survival and clean teardown.

## 4. Vortex build, qualification and safe operations

- User controls all **Vortex installation/deployment** and in-game controls; Codex may build/archive and provide exact installation and verification instructions. Do not directly copy plugins to the game folder or alter Vortex profiles.
- Pin the actual executable, SFSE and plugin builds to observed local hashes, versions and required module layouts. Verify native instruction signatures at runtime before instrumentation, fail closed on mismatch. Any compatibility difference requiring code changes means return for new review, **not** an automatic live workaround.
- Strictly retain **40,000,000,000 caller-available free bytes on both C: and D:** before and during relevant evidence writing. Preserve read-only provenance and integrity of Save25/Save26 originals/archives and frozen fixtures. New local evidence in ignored directories only; do not commit raw `.sfs`, game binaries, dumps or proprietary assets.
- Where a failed target may be left unstable, preserve already committed evidence and never promise guaranteed recovery that the mechanism cannot provide. The run card must address hook teardown and whether disable-on-process-exit rather than dynamic unhook is safer; record remaining risks candidly.
- Offline/disposable qualification should attempt adverse and overlapping paths, not just the happy path. Test incomplete captures and event association, shutdown while in-flight, backpressure/writer failure, pointer validity, no-hit and duplicate-hit cases, and source/binary identity checks; document what is simulated versus observed.

## 5. One review and conditional live authorization — required operating sequence

**Phase A — Codex, now (offline):** inspect evidence, select justified narrow observation sites, implement/qualify the plugin, produce the Vortex ZIP, **produce the full live run card**, run independent reviewer/rework, and submit one complete package for us to assess. **No launch of Starfield, Vortex deployment, native attachment or live experiment at this phase.**

**Phase B — One combined review:** we review the implementation, qualification, package and exact run card **together**. User deploys the specifically approved ZIP via Vortex and authorizes the specific live experiment and its stated risks. Authorization may be granted **conditional on specified preflight checks passing**. It does not extend to different hooks, saves, site visits or trigger actions.

**Phase C — Codex post-deployment preflight and live experiment:** after authorization, Codex performs machine-side preflight, verifies the *deployed* plugin and environment, and initiates the authorized launch/test while coordinating operator actions with the user. **If all approved mandatory preflight checks pass, continue to the approved live experiment without requesting a second routine approval or writing a new run card.** The user performs save selection, travel/build-mode actions and responds to in-game conditions. If any gate fails, stop and preserve receipts; do not silently change configuration, code or permissions.

**Phase D — Results:** preserve original raw captures/hashes, protected-input postflight and observer health; analyze native outputs against frozen predictions; report exact support, counterexamples and missing branches, with an independent reviewer where practical. Further experiments, changed configurations or code modifications require review only when they exceed the already approved card's scope.

**Important:** The current brief authorizes **Phase A only**. The future Phase C is a pre-agreed procedure, not permission to start it before our Phase B authorization. No automatic commit/push; user will decide after result review.

## 6. Workflow completion and agent limits

Apply the committed Research Execution and Completion Protocol. A failed test, new implementation obstacle or missing event is an **in-scope problem to investigate**, not an automatic end-of-task summary. Resolve and requalify in the same assignment; an independently reviewed negative feasibility finding is acceptable only when evidence establishes why this authorized acquisition method cannot meet the contract. Never label a partial candidate **COMPLETE/PASS**. Explicit authority/safety blockers may be escalated with exact evidence and a narrow requested decision.

Codex may spawn **at most two simultaneously active sub-agents**, excluding the primary implementer: **one independent reviewer** and **one specialist researcher** on a separable problem (e.g., native event reachability and exact ABI/return contract). Specialist use is discretionary, and must produce independent findings rather than duplicated implementation. Preserve reviewer independence: original contract, source/evidence access, critical counterexample seeking, **ACCEPT / REWORK / ESCALATE** and rework in the same assignment where within authorized scope. The reviewer must inspect the executable run card as well as code and test evidence.

## 7. Review artifacts and final report

Place patches in `.local-work/diffs/` using established `-complete.diff` and `-task-only.diff` conventions; include new untracked text files correctly, full status, changed-file/exclusion inventory, source/build/package hash ledger and replay/applicability validation. The package and candidate binaries stay under ignored local work with versioned identifiers; retain reproducible baseline and failed evidence. Report:

1. Observation architecture, actual native boundary and why it meets the independent-oracle objective.
2. Exact pass/fail/untested acceptance matrix and reviewed negative tests; relevant static dependencies and trigger/reachability argument.
3. Native capture schema and deterministic postcapture comparison workflow.
4. Qualification evidence, limitations and remaining live risks.
5. ZIP/hash/deployment manifest plus **complete ready run card** with exact preflight and operator instructions.
6. Independent reviewer verdict and resolved rework history; if escalation, articulate exact *new authority* needed rather than asking for another generic brief.
7. Confirmation that no live Starfield activity, deployment, protected-file mutation, stage, commit or push occurred in Phase A.

**Do not return a plugin alone and ask for a later run-card brief. Do not return a run card alone and ask for a later preflight brief.** One reviewed package is the authorized deliverable.
