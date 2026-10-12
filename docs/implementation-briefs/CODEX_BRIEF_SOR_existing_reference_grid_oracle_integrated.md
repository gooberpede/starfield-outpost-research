# Codex implementation brief — SOR: Existing-Reference Native Grid Oracle and Integrated Live Procedure

**Assignment type:** implementation, disposable qualification, scientific acquisition design and integrated live-run preparation.  
**Repository:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`).  
**Starting point:** the committed/synced matching-source qualification, the established 0.3.0 Q-branch observer, existing live captures, and the current durable position reproducer.  
**Authority:** **offline development and disposable testing only** until the maintainer reviews and authorizes the exact build **and** its complete run card together. Do not launch or access Starfield, deploy through Vortex, stage, commit, or push under this brief.

## 1. Scientific objective and priority

Obtain **fresh, independently generated, identity-bound native terrain-grid evidence** for an ordinary outpost, preferentially through the existing-reference lookup/shortcut rather than requiring the Q→E fallback path.

The previous offline investigation identifies a native generic grid calculation at **`0x14077FEC0`** reached from an existing-reference path that can bypass Q and E. The qualified matching-source research associates candidate 16 with **SOR-003** and candidate 15 with **SOR-002**, with a matching saved context, but **neither runtime shortcut reachability nor actual input/output association has been demonstrated**. These are hypotheses to test, not predetermined successes. Verify addresses, guards, callsite semantics, argument/output contracts and evidence lineage against the pinned game binary and retained static analysis before implementing hooks.

Primary acquisition chain: ordinary selected-reference action → resolved native reference and ownership → existing-reference decision → generic grid invocation → native grid inputs/results → comparison to **frozen** offline model. Capture enough native provenance to identify **which computation** and **which reference/frame** was observed. A matching numeric grid value without identity, inputs and freshness is insufficient. Do not conflate the generic grid result with an outpost workshop center or planetary longitude/latitude.

Retain Q/E as a secondary diagnostic only when useful and technically proportionate; the goal is not to keep expanding hooks along an unproductive fallback path. Instrument the **deepest decisive stages** so a negative live run identifies the precise unobserved transition and produces a usable next hypothesis.

## 2. Required offline analysis before instrument design

1. Re-read and reconcile `docs/experiments/matching-source-qualification.md` and its review, the Q→E analysis, 0.3.0 qualification and captures, current position model/prediction protocol, and existing native disassembly maps. Start from the current committed tree; do not rewrite prior reports or change frozen predictions.
2. Independently trace the actual existing-reference route, including the selected reference's producer, reference/parent/world identity, conditions selecting the shortcut, native generic grid invocation and all relevant output/intermediate values. Clearly distinguish exact native instructions, inference and unobserved runtime behavior.
3. Establish the **minimum sufficient** observation set, verified CALL/entry/exit boundaries and relevant ABI/thread/lifetime constraints. Prefer passive observation or narrowly controlled natural call wrappers over aggressive patching. Do not use the closed external debugger, Windows debug breakpoints, synthetic game calls or memory injection.
4. Evaluate whether ordinary **Save28 → SOR-003** selection/travel can plausibly reach the shortcut. Include the possibility of direct existing-reference resolution bypassing Q entirely. SOR-002 is a conditional comparison only if justified by the recovered path. No artificial key insertion and no presumed equivalence.
5. If a new controlled save or operator action would materially improve the experiment, document exact hypothesis, prerequisites, construction steps and alternatives; do **not** execute or automatically authorize that scenario. Avoid difficult travel, console commands or further save proliferation without a substantive reason.

## 3. Implementation and engineering requirements

Deliver a **new versioned SFSE observer** based on established, permitted project-owned code as appropriate, retaining the proven evidence format/features where viable. Keep earlier binaries, archives, raw captures and 0.3.0 intact. Use clear version identifiers and source/build provenance.

The implementation must:

- Capture native outputs *during their producing invocation* with a stable invocation identifier and thread ancestry; record selected-reference identity, world/body/frame context, raw arguments, meaningful intermediate values and outputs, return path, preconditions and source callsite. Preserve original binary32/binary64 bytes and validity/unreadable markers without guessing.
- Independently identify shortcut selection, the generic grid operation and any still-relevant Q/E transition. An event counter alone is insufficient; report branch and call attribution, including absent/unpaired events without fabricating outcomes.
- Preserve calling convention, SIMD and floating-point control state, instruction semantics, exception propagation, concurrency/reentrancy and stack/unwind behavior. Guard every patch against exact game version, bytes, module identity and expected layout; fail closed on genuine patch-integrity or safety violations.
- Preserve event evidence across normal and partial runs through verifiable durable records, sequence/integrity checks and recoverable incomplete tails. Prevent optional/unreadable scientific fields from terminating otherwise healthy acquisition. Separate capture integrity, scientific completeness, target survival and retirement status.
- Maintain independent worker heartbeat/nonce acknowledgment and robust STOP/retirement behavior, with truthful limits on in-process unpatching and recovery. Never promise full restoration if only inert hooks until exit are implemented.
- Enforce **at least 40,000,000,000 caller-available bytes free on both C: and D:** as a hard guard. Do not introduce arbitrary small scientific event-count limits; operational safety constraints must be explained and documented prospectively.
- Accept **ordinary Steam and NVIDIA overlays** as the normal environment: inventory modules and evaluate demonstrated conflicts, but do not reject these overlays categorically or demand the operator disable them. Other unfamiliar modules are not automatically disqualifying absent a credible conflict. Maintain real identity/integrity checks.
- Use natural gameplay only. No Starfield launch, save modification or live hook execution for this assignment.

## 4. Correct Vortex deployment contract — important correction

**Preflight shall verify the effective deployed runtime payload, not presume Vortex installs every file contained in a ZIP.**

- Establish and document which files the SFSE observer **actually loads/requires at runtime**. If self-contained, the required deployed payload is **the plugin DLL only** at its correct SFSE plugin path, hash-matched to the approved package. A runtime-essential config or dependency must be justified by code-level evidence and included in the deployed-payload contract.
- README, changelog, package notes, manifests, qualification reports, source hashes and run cards are *review/repository/package artifacts*, not mandatory DLL-neighbor files. **Their absence from the installed plugin directory cannot fail preflight or require a waiver.**
- Hash/pin the approved archive, the DLL inside it and the effective installed DLL; verify that the expected version loads and conflicting old plugin versions are not active. Keep text documentation in the repository and/or ZIP for review without assuming its deployment path.
- Operator installs/enables through **Vortex only**. No manual copying to the game directory; no unapproved changes to launch options, Steam/NVIDIA settings, Vortex configuration or existing save/plugin state.
- Update the run card and any reusable preflight code accordingly; specifically eliminate the recurring optional-text-file waiver pattern.

## 5. Disposable qualification before delivery

Develop and test against disposable native fixtures that model the shortcut and generic grid observation sites with their real instruction/ABI constraints. Require controlled positive and negative scenarios:

- Existing-reference shortcut hit with valid identity and exact native grid input/output; differing reference, frame, coordinate and relocation contexts as applicable.
- Shortcut bypass/no-hit; Q/E fallback events independent of shortcut; unexpected branches; out-of-order, nested, concurrent and unpaired observations.
- Address/version/byte guard rejection without partial unsafe patching; native call/return preservation, floating-point/SIMD state, exception/unwind behavior and worker health under zero-event operation.
- Evidence durability, recovery from incomplete record tails, queue/backpressure, disk guard, worker STOP, startup refusal, failure-retirement and package/deployed-DLL hash verification.
- Preserve counterexamples and diagnostics; identify and correct any failed mandatory control **inside this assignment**, requalify the exact final binary and return only a completed, independently reviewed result or a demonstrable safety/authority blocker. Do not relabel a 5/6 qualification as finished.

Tests on fixtures do not claim Starfield-specific runtime reachability. Do not adjust frozen predictions or model tolerances to force agreement.

## 6. Integrated live run card — delivered alongside the observer

Prepare the exact executable run card **now**, not in a subsequent documentation task. It must be review-ready together with the approved DLL/ZIP candidate, contain all exact pinned hashes/paths and provide command/procedure checks where practicable.

**Default primary scenario:** load the verified **Save28** from the controlled Kreet lineage, use the ordinary game interface to select/travel to **SOR-003**, and observe the existing-reference shortcut and grid acquisition. Describe the expected scene, location/character/save safeguards, explicit operator handshakes and how to distinguish similarly labeled saves. Do not rely solely on dynamic menu ordinal; where on-screen identity remains ambiguous, halt for confirmation rather than guess. Save-menu metadata parsing remains a separate near-term backlog item, not a prerequisite to this implementation.

The run card shall:

1. Verify offline protected-save/frozen-input hashes and approved exact build, both-drive space guard, Vortex deployed runtime-essential files (DLL-only unless justified otherwise), no unintended competing observer versions, game/SFSE versions, code guards, module inventory and output directory uniqueness.
2. Define READY and fresh worker-health acknowledgments, a viable **measurable monitoring cadence** informed by prior 2.793-second observation gaps, stop/retirement semantics, and an operator-safe process for stalled/failed targets. Strict one-second polling is not required; genuine integrity/disk guards stay hard.
3. Explain permitted in-game operations and exact order, including what Codex does on the machine versus what only the user does in game. Do not automatically expand to SOR-002, additional landing points or construction; a **conditional SOR-002 step** may be pre-authorized in the same card *only if* source evidence supports it, is independently qualified, and presented clearly for joint review.
4. Identify branch-specific expected records and a per-invocation reconciliation table covering reference identity, chosen path, selected frame, native calculation, evidence freshness, outputs and comparison against untouched frozen predictions.
5. Treat absent grid calls, unmatched reference, wrong frame and disagreement as informative scientific outcomes; collect through the approved operator sequence without arbitrary hit quotas, and report precise reachability depth. Do not claim native equivalence from a convenient center match or a stable but stale buffer.
6. Define STOP, postflight hash checks, raw evidence preservation, incomplete-tail handling, normal game exit, incidental autosave inventory, and explicit non-overwriting of original protected saves. The user controls game interaction and all new manual saves.
7. Specify all operational hard stops and accepted noncritical variation. Passing the reviewed preflight permits Codex to initiate the already-authorized run **without a second routine review**, *after* the maintainer has jointly approved the exact observer and run card and deployed it through Vortex. Any new hook, altered build, expanded scenario or genuine safety waiver requires separate approval.

## 7. Independent review and agent limits

Follow `WORKFLOW.md` and the current Research Execution and Completion Protocol. The primary Codex implementer may use **no more than two concurrently active sub-agents:** one independent reviewer and at most one specialist researcher, used when genuinely beneficial. Reviewer must inspect primary code, fixtures, failure evidence, scientific attribution and the complete run card, not just the summary. Return REWORK for in-scope failures and complete that rework inside the same assignment.

Review specifically whether the **existing-reference shortcut** is actually distinguished from Q/E fallback; whether generic grid output is meaningfully independent of the offline model; whether the saved site can be associated with the runtime reference; whether the Vortex preflight improperly requires optional texts; and whether the trigger is well supported.

## 8. Required handoff and completion contract

Deliver together, before any live use:

1. Versioned, qualified **Vortex ZIP**, source/build receipts, exact archive/DLL SHA-256 identities and truthful list of runtime-essential deployed files.
2. Implementation and repeatable disposable qualification, with full passing acceptance matrix and retained negative controls.
3. Complete integrated live run card with preflight, operator actions, health/monitoring, stop/recovery, analysis and postflight; run-card/version/hash consistency checks.
4. Scientific provenance/decision ledger explaining native shortcuts, call contracts, known uncertainties and the anticipated identity-bound grid comparison.
5. Independent reviewer verdict and rework history; `git status --short`, changed/excluded file manifests and validated task-only and cumulative `-complete.diff` under `.local-work/diffs/`, **including untracked text files** without staging solely to make a diff.

Acceptable completion means a fully qualified implementation **and** review-ready procedure; native equivalence remains `NOT TESTED` until approved live observation. A genuinely terminal authorization/safety blocker must be demonstrated concretely rather than substituted for correctable incomplete work.

**Explicit prohibitions:** no live Starfield launch or attach, no plugin deployment, no new save creation, no external debugger revival, no staging, commit or push, no modification to frozen research inputs and no external upload/publication under this brief.
