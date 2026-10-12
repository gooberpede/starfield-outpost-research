# Codex brief — SOR: Q-Branch Observer 0.3.0 Controlled Live Acquisition Procedure

**Assignment type:** Offline preparation, run-card authoring, qualification of operational checks, and independent review. **Not** authorization to launch Starfield, deploy the plugin, attach instruments, alter saves, stage, commit, or push.

**Repository:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`). Begin from the **committed and synced** Q-to-E reconstruction and offline-qualified SorNativePositionOracle **0.3.0**. This is a continuation of the research, not a new instrument design. Follow `WORKFLOW.md`, the Research Execution and Completion Protocol, scientific/evidence and provenance policies, and the existing complete/task-only review-diff convention.

## 1. Objective and bounded acceptance contract

Produce a **single, executable, independently reviewed live acquisition procedure** for the existing byte-identical 0.3.0 SFSE observer. The purpose is to capture the missing **identity-bound Q branch-helper operands and native outcomes**, explain the Q-to-E paths seen during the previous 18-call Kreet landing observation, and, if naturally reached, collect downstream E/callback/center/grid evidence relevant to durable-position equivalence.

The deliverable is the **procedure and qualified readiness evidence**, not a claim that the native calls have already occurred. This assignment completes only when all mandatory pre-live acceptance criteria below pass or a demonstrated, genuine authority/safety blocker is escalated with precise evidence. No unfinished run card or speculative trigger proposal qualifies as completion. Resolve routine defects within this assignment, using mandatory independent reviewer rework.

The previous evidence is fixed: the 0.2.0 Kreet N1 session captured **18 paired Q calls returning 1**, no observed E/callback/center/grid events; recovered caller semantics indicate `1` means *continue scanning* and E is optional. The offline Q-to-E study identified missing helper, overlay, landscape and hierarchy operands. Observer 0.3.0 was separately authorized, developed and offline qualified; **760 native fixture checks**, decoder/inspector regressions and **23 preserved frozen position predictions** were reported passing. None establishes that its new helper sites are reachable in retail. Do not reclassify the 18 observations or assume a success/failure meaning for `1` beyond the recovered caller contract.

## 2. Preserve and inspect existing work first

Read the relevant committed evidence, source and qualification records, including:

- `docs/experiments/q-to-e-control-flow.md` and `docs/experiments/q-to-e/review.md`;
- `docs/experiments/q-branch-030/qualification.md` and `docs/experiments/q-branch-030/review.md`;
- `docs/experiments/native-oracle/continuation-020-live-attempt-02.md` and its independent review;
- relevant observer 0.3.0 source, release/package manifest, inspector/decoder and previous run cards;
- durable-position reconstruction, frozen predictions, Save25/26 and new Save27/28 provenance and protected-input manifests.

Locate the **actual 0.3.0 ZIP and DLL** and their existing source/build/hash receipts. Verify exact identities and qualification status. **Never invent or reuse a 0.2.0 hash for 0.3.0**. If the established reviewed 0.3.0 package is unavailable or cannot be reproduced byte-identically, explicitly identify the gap and obtain a new review rather than silently replacing it. Do not alter the compiled plugin, hook map, admission logic, inspector schema, or frozen inputs as part of this task. A discovered code defect must be documented and brought back for an explicit new implementation/requalification decision; do not circumvent this gate by swapping DLLs.

## 3. Select and justify the trigger

Do the **offline native-code/evidence analysis needed to specify a defensible action sequence**, rather than simply recycling last run's instructions. The primary proposed trigger is **one previously unused, accessible landing location on Kreet**, since a new landing (not travel between the established SOR-002/SOR-003 sites) generated the 18 Q calls in the previous session.

1. Determine whether reloading a **pre-landing Save27** and repeating the earlier landing could meaningfully retrigger candidate selection, given landing-site persistence/caching. Distinguish confirmed mechanics from hypothesis. Do not represent Save28 as an unvisited pre-landing baseline.
2. If uncertainty remains, provide an operator-feasible alternative: **one new, previously unused Kreet landing site** reachable with the low-level controlled character, with exact selection criteria and a contingency if no eligible site can be found.
3. Check both save identities/provenance and the actual initial operator location. Ensure the intended source save cannot be confused with adjacent saves. Until the separate save-menu parser exists, give full existing filename/hash, in-game visible menu text/date/time/playtime/character **only where actually verified**, and a clear explicit operator confirmation; do not manufacture menu labels. If visual labels collide, flag ambiguity and require confirmation before loading rather than relying silently on list order.
4. A new controlled **before/after checkpoint pair** may be **proposed** where justified and practicable, with fresh identifiers and protected copies. **Creating saves or performing new landings is not authorized by this offline brief**; include these specific actions in the combined run card for maintainer approval. Never overwrite, rename, delete or replace protected files; account for ordinary autosave/exit-save rotation separately. No new outpost, construction, high-level travel, console commands or speculative extra gameplay without separate authorization.
5. The operator retains control of gameplay. Codex may prepare machine-side actions and subsequent execution commands, but the user loads saves, chooses the landing point and conducts all in-game actions.

## 4. Required integrated run card

Create a practical run card in `docs/experiments/q-branch-030/` (or a better established repository location) that can be executed **after a single combined maintainer review/authorization and Vortex deployment**, without another routine approval after passing preflight. Include exact command lines, paths or justified placeholders resolved from the actual installation, evidence/session naming and abort/retirement procedures.

The card must contain, in coherent execution order:

**Preparation and identity:** Pinned Starfield.exe version/hash, SFSE version, exact approved 0.3.0 ZIP/DLL/config/schema hashes; Vortex-only user deployment (never silently copy into the game directory); read-only inventories of game, module/load order and plugin installation; new ignored unique evidence directory; preservation/hashing of protected saves, baselines, raw prior captures and frozen predictions. Maintain **at least 40,000,000,000 caller-available bytes free on both C: and D:** as a mandatory operational hard guard, with failed queries as failures. Check required resources/paths, existing plugin conflicts and availability of the relevant Python/inspector tools.

**Normal operating environment:** **Steam and NVIDIA overlays are accepted baseline components.** Inventory and log them; their mere presence is not an automatic blocker. Distinguish known overlays from an actual conflicting native-code instrument or unreviewed patch. Retain hard rejection of executable/native-site identity mismatch, unsafe startup state, evidence-writer integrity failure, disk safety failure and protected-input mismatch. Do not suppress or work around these gates. Avoid demanding an artificially clean, overlay-free environment.

**Startup and health:** Define how the operator launches via the approved SFSE/Vortex profile and how Codex independently confirms plugin admission/installation, expected hooks/guard checks, READY/health state, fresh nonce/ACK and durable worker progress before an operator cue. Spell out what constitutes a plugin that is alive but has **zero Q events**. Do not mistake an absence of events for a failed worker or for proof of an unexecuted engine operation. Specify a realistic, measurable external monitoring cadence, replacing the previous impossible strict one-second obligation; retain the **15-second health gate** unless evidence supports a reviewed safer alternative. No relaxed cadence may weaken immediate native integrity, worker failure or disk-space stop rules.

**Operator sequence:** A short fixed sequence covering baseline, approved Kreet landing, optional separately named before/after controlled checkpoints, UI settlement, STOP and normal game exit. State whether and why existing Save25/26 controls add scientific value to this particular branch-observation run; omit redundant travel unless it supplies a concrete control. Do not require arbitrary event-count targets or unlimited repetitive attempts. Exactly **one controlled live session** is proposed. A failed trigger produces useful negative reachability evidence; it does not automatically authorize extra sites, more hooks, repeated attempts, or new research activities.

**Capture and correlation:** Acquire and retain full available raw Q begin/end, seven helper observations and E-entry diagnostic, with invocation/thread/caller identity, native output and provenance. Define inspector requirements for matched versus incomplete chains, contradictory helper samples, missing operands, return semantics and Q-to-E branch attribution. Treat sequential helper snapshots as non-atomic and distinguish observed from inferred branch outcomes. If E, callback, center or grid naturally fire, preserve all qualifying evidence and compare with **already frozen** predictions without changing tolerances or retrofitting predictions. Never claim full native equivalence from Q-only observations.

**Closure and incident handling:** Explicit STOP/retirement, worker drain/health receipt, target survival and normal exit, hashes of original raw evidence, independent decoder/inspector validation and input postflight; record ordinary save rotation. Distinguish scientific result, data completeness, plugin health, conformance and game survival as separate statuses. Unexpected findings should be captured, not treated as premature failure; genuine integrity/storage/patch safety faults stop the run. State what Codex may do autonomously after approved preflight and where it must stop for fresh authority.

## 5. Offline qualification of the procedure

The already-qualified 0.3.0 binary must remain unchanged. Conduct read-only/fixture-only validations of any new preflight scripts, run-card invocations, evidence paths and failure gates. Verify hash identities against actual manifests, paths, no destructive save actions, correct protected-copy handling, decoder compatibility, review-package completeness, and recovery instructions. Where feasible, test dry-run/mock STOP/ACK/inspector workflows without contacting Starfield.

Do not run Starfield, open a live game process, install Vortex package, create saves or modify game configuration during this assignment. If a new tool change proves unavoidable, keep it outside the qualified plugin and test it, or escalate if it changes the security or native instrumentation contract.

## 6. Independent completion review and sub-agent allocation

Use the repository's mandatory **independent reviewer**. At most **two concurrently active sub-agents**, excluding primary Codex: reviewer plus, if it adds value, one specialist investigating native trigger reachability or save/landing provenance. The reviewer must examine original brief, actual source/qualification identities, proposed run card, primary previous live data and tool outputs—not just Codex's summary.

Reviewer challenges must include: whether the proposed landing discriminates Q branches; whether repeated landing from Save27 is genuinely fresh; correctness of accepted Steam/NVIDIA overlay policy; protected-save handling; observed-versus-inferred Q/E branch classification; whether a zero-event session is scientifically interpretable; realistic cadence; and whether any authority boundary was crossed. Reviewer outcomes: **ACCEPT / REWORK / ESCALATE**. Resolve all in-scope REWORK within **this assignment**. No acceptance matrix can mark mandatory untested conditions PASS.

## 7. Final deliverables and halt policy

Return all together, for our **single combined review**:

1. **Executable run card**, including initial/save selection and explicit optional one-new-landing scenario.
2. **Evidence-based trigger justification**, with confidence and alternatives, not merely a proposal to instrument more code.
3. **Exact 0.3.0 package identity and deployment guidance**, including ZIP/DLL/config hashes derived from verified artifacts, no guessed identities.
4. **Preflight and postflight tools/check results** for offline-tested components, with safe failure behavior.
5. **Independent review transcript/decision references**, rework ledger, PASS/FAIL/NOT TESTED acceptance matrix and exact residual risks.
6. **Task-only and complete uncommitted text diffs** in `.local-work/diffs/`, including untracked text, plus `git status --short`, changed-file/exclusion/hash manifest, applicability and review checks. Do not stage to build diffs.
7. **A concise operator handoff**: precisely what the user must deploy, confirm, and do once the package/run card is approved.

The expected outcome is **COMPLETE — PROCEDURE READY FOR REVIEW**, not a completed native science claim. A true blocker requiring new authority may be escalated with direct evidence; ordinary missing documentation, broken scripts, failed checks, ambiguous save labels and unverified paths are in-scope work to resolve before return.

**Stop at the combined review gate.** No live authorization is conferred by this brief. After the user approves the exact run card and deploys the reviewed ZIP via Vortex, passing its mandatory preflight authorizes Codex to run that **specified** test without a second routine review; game actions remain with the user. Any change to DLL/hooks, protected-save policy, experimental geography or significant safety gate needs new approval.

## 8. Separate near-term backlog — not part of this assignment

Record, if not already on the project backlog, a read-only save-menu identification extractor mapping research IDs to **character name**, manual/auto/exit-save type, in-game location text, level, visible date/time and playtime, with collision detection and support for character-filtered game menus. The user's examples include distinct characters such as Cao Tran and Atilla Kiraly. **Do not implement or investigate that parser now.** It must not delay the 0.3.0 procedure.
