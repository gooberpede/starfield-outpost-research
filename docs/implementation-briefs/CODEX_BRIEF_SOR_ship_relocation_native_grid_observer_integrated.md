# Codex implementation brief — SOR ship-relocation native grid oracle and integrated live procedure

**Assignment:** Resume the committed/synced `starfield-outpost-research` work following the accepted offline ship-relocation assessment. Produce a qualified SFSE observer, installable Vortex package, exact run card, offline acceptance evidence, and independent review **in one assignment**. No Starfield launch or deployment, staging, commit, or push before maintainer review.

## 1. Research objective and baseline

The purpose is **independently observed, identity-bound native positioning evidence** that can validate parts of the durable outpost-position reconstruction. Do not confuse a ship landing marker with an ordinary Workshop or claim full Workshop equivalence from a generic grid result.

Carry forward the accepted static research in `docs/experiments/ship-relocation/` and the 0.4.0 observer/capture history. In particular, investigate native travel and landing-route production, the ship-relocation decision, selected landing reference, terrain descriptor, and the shared grid routine `0x14096F5C0` (verify executable build/RVAs/ABI from pinned local evidence before instrumenting). Retain the distinctions between retrieving an existing marker, generating/selecting a natural site, moving a ship, and moving the player. Treat prior 0.4.0 zero-offset generic agreement as scoped evidence, not proof for an outpost.

The central experimental contrast, based on the maintainer's **manual, uninstrumented Save25 observations**, is:

- **Control:** Travel locally SOR-003 → SOR-002 → SOR-003; the ship has often remained at its original natural landing area **LZ1** (near SOR-002). This is an observation, not a guaranteed invariant.
- **Experimental:** From a new, distinct Kreet natural landing location (**LZ-new**), fast-travel to SOR-003; previously this moved the ship to a natural area around 450 m from SOR-003 (**LZ3**). The exact marker and ship behavior in a new session are **not** guaranteed.

**Important:** Save25 does not contain the later LZ2/LZ3/LZ4 markers; never assume those sites are already present/selectable. The live session should generate **one new landing location** through ordinary gameplay rather than require a preparatory Save29. Do not assert a specific landing-site generation mechanism from visible ship relocation alone.

## 2. Implementation and scientific requirements

1. First verify the retained static call contracts and previous captures. Choose **the smallest source-supported instrumentation set** that connects, as far as practical: user travel request/destination → ship relocation decision → landing-route producer (previously identified at `0x14078B030`, independently verify) → selected reference/marker identity and provenance → grid inputs and actual native in-place output. Include the Workshop-specific compensated-center/grid path as a separately identified secondary oracle **only where safely and naturally observable**. Preserve Q/E diagnostics selectively if useful; don't add hooks solely for completeness.
2. Every scientifically relevant sample must retain raw native input/output bytes, site/route labels, thread and invocation ancestry, sufficient reference/handle/base-form/site/world/frame identification, branch/decision evidence, and timing/order information. Distinguish selected-reference *identity* from its base FormID and from a runtime pointer. Record null, unreadable, absent, stale, lost, nested, and unpaired values honestly.
3. Capture the **native** grid calculation (including nonzero offsets and carry if encountered), not an offline reconstruction pretending to be a runtime result. Compare with the **unchanged** 23 frozen predictions only for independently qualified cases. Explicitly classify generic terrain-grid, ship marker, Workshop center, and full durable Workshop-equivalence evidence separately.
4. If the action has no intended native hits, the observer must still distinguish worker health from callback reachability and identify the deepest observed route. Do not invent an event quota or force additional travel to manufacture hits.
5. Preserve the prior observer, documentation, raw archives, frozen predictions, Save3/25/26/27/28 and other protected inputs, and version the new build. Reuse owned project code with recorded provenance; separately respect third-party rights.
6. Full disposable qualification is mandatory for ABI/register/FPU integrity, nested and concurrent calls, callback lifetime, exception paths, patch identity and rollback, worker liveness, durable evidence/integrity, lost/incomplete events, and orderly game-exit semantics. The independent reviewer must examine primary evidence and return REWORK until in-scope defects are corrected. No claim that fixture qualification proves Starfield runtime compatibility.

## 3. Save selection: replace redundant operator confirmations with an advance instruction

The maintainer supplied screenshot **`20261013121245_1.jpg`**, depicting the **Attila Kiraly** character's Starfield Load menu on 13 October 2026. Use it as a **human-supplied visual reference**, not as proof of binary save-to-menu metadata extraction. Record the following menu identification in the durable run card (dates/times are the **displayed local UI values**):

| Research identifier | Visible label (ignore `[C]`) | Displayed date | Displayed time | Level | Order in this screenshot |
|---|---|---|---|---|---|
| Exit save | `EXIT SAVE Kreet - Outpost` | 10/13/26 | 10:18:26 AM | 4 | 1 |
| **Save28** | `Kreet - Landing Area` | 10/12/26 | **12:18:28 PM** | 4 | 2 |
| **Save27** | `Kreet - Outpost` | 10/12/26 | **12:11:19 PM** | 4 | 3 |
| **Save26** | `Kreet - Outpost` | 10/10/26 | **12:24:53 PM** | 4 | 4 |
| **Save25** | `Kreet - Outpost` | **10/9/26** | **9:22:22 PM** | 4 | 5 |
| **Save3** | `Kreet - Kreet` | 10/6/26 | 12:34:27 PM | 3 | 6 |
| Autosave | `AUTO SAVE Kreet - Landing Area` | 10/6/26 | 12:30:18 PM | 3 | 7 |

The list index is dynamic, as is the Creation Club `[C]` marker; **do not use either as a durable identifier**. Character name comes from the maintainer's statement, not visibly from this screenshot. For the primary control, Codex should instruct succinctly **before** the in-game action, e.g.:

> **Load Attila Kiraly Save25 — Kreet - Outpost, dated 10/9/26 at 9:22:22 PM (Level 4).**

Do not follow an unambiguous advance instruction by asking the maintainer to restate the character, label, timestamp, or save number. Record the instruction, user action acknowledgement, and any observed mismatch. If the entry is absent, UI metadata conflicts materially, character filter differs, or two entries cannot actually be distinguished, **ask one targeted question or request a fresh screenshot** rather than guessing; do not silently rely on ordinal position. Physical file hash and provenance preflight remain machine-side responsibilities. Don't demand that the user certify a menu-to-file identity the UI cannot expose. Save-menu metadata parsing (including **character name**, type, place, level, date/time, playtime and collision detection) remains a **separate near-term backlog task**, not a prerequisite here.

The run card must be workable even if a new ExitSave rotates or the menu order changes. New manual saves, if any, require new names/receipts and may require a fresh screenshot; don't assume a research identifier corresponds to the dynamically displayed index.

## 4. Integrated prospective live run card (to be delivered, NOT executed yet)

Prepare a fully executable, operator-friendly procedure together with the build. Recommended phases:

1. Machine-side preflight: verify exact Steam Starfield executable/SFSE compatibility, Vortex **effective deployed DLL** hash and native code-site guards, no incompatible instrumentation, approved normal Steam/NVIDIA overlays, protected save/frozen-input hashes, both drives' **40,000,000,000 bytes caller-available free-space** minimum, and evidence-root uniqueness. **Only require the DLL and demonstrated runtime-essential dependencies** in deployed `Data\SFSE\Plugins`; never require optional TXT/README/manifest alongside it. Independent worker-health admission must pass.
2. You prompt the maintainer **once, in advance**, to load **Attila Kiraly Save25 — Kreet - Outpost, 10/9/26 9:22:22 PM, Level 4**. Maintainer controls the game; Codex handles checks, telemetry, coordination and launch only after the combined review and live authorization.
3. At SOR-003 with the ship initially at LZ1 if the observed state supports it, run a **normal local fast-travel control** SOR-003 → SOR-002 → SOR-003; log actual visible ship location/behavior without assuming no relocation.
4. Choose **one previously unvisited, accessible Kreet landing location** (LZ-new), land using normal gameplay, and record the visible ship/player positions and acquisition. No distant-system travel, console calls or artificial native triggers. This action may itself yield useful grid evidence.
5. From LZ-new, fast-travel normally to SOR-003; record whether ship stays, relocates, or chooses a new natural landing marker, its observed relationship to the outpost, and the exact native request/marker/grid events.
6. **Optional**: one new manual checkpoint *after landing at LZ-new*, only if useful for repeatability or saved-state comparison and explicitly coordinated with the maintainer during the already authorized sequence; do not overwrite protected saves. If uncertainty about the proposed checkpoint or available save slot materially changes the scope, consult the maintainer rather than creating a surprise file.
7. Finish with clean STOP/retirement and normal game exit as appropriate, raw evidence sealing, integrity/health checks, save and ExitSave-rotation inventory, original input hash verification, and scientific comparison. Preserve the actual failed attempts and counterexamples. No automatic additional trip, new outpost construction, new plugin, expanded hooks, or repeated session.

**Operational policy:** No arbitrary session clocks, event counts, 2 GiB caps, routine monitoring-cadence overrun termination, or operator-response deadlines. Delays should elicit updates, not automatic failure. Only established integrity, disk-space, true instrumentation-health/safety failures, operator STOP, or separately justified and **prior-approved** hard limits may stop a healthy capture. On unforeseen noncritical conditions, consult the operator when necessary instead of quitting. Capture-first policy applies; distinguish scientific completeness, instrumentation integrity, and target survival. Respect user responsibility for in-game actions.

**Authorization boundary:** This brief authorizes offline development, tests, packaging and run-card preparation **only**. After a **single combined maintainer review** of exact binary hashes, qualification, independent reviewer verdict and complete run card, the maintainer can deploy via Vortex and approve the defined experiment. Once approved, Codex may preflight and launch/run the exact procedure without another routine approval if all mandatory preflights pass. No Starfield launch or live process attachment, Vortex deployment, save editing, staging/commit/push in the current assignment.

## 5. Completion protocol and deliverables

Apply the committed Research Execution and Completion Protocol. Failed tests, missing helper outputs, reviewer objections and in-scope engineering defects require continued implementation, diagnosis and requalification **within this assignment**. Do not present an unfinished candidate as COMPLETE. A genuine safety/authority requirement is an ESCALATE, not a workaround. Independent reviewer mandatory; one independent specialist permitted when genuinely useful, maximum **two concurrently active sub-agents** excluding the primary agent. Reviewer tests contract, actual code and primary evidence; specialist's distinct technical contribution should be documented without repetitive evaluation of reviewer effectiveness.

Return in one review package:

- Versioned observer DLL and Vortex ZIP, exact source/build/toolchain and ZIP/DLL SHA-256, runtime-essential dependency manifest.
- Source-supported native hook and capture design, qualified fixture and adverse-case evidence, complete preservation/integrity receipts, acceptance matrix and explicit scientific limitations.
- Full **prospective** live run card with operator prompts, save identity table above, deployment/preflight/STOP/postflight actions, clear safety/continuation rules and run-specific evidence schema.
- Updated durable docs and research-state/provenance ledger; no rewriting of historical raw observations.
- Independent reviewer verdict and implementer REWORK closure, plus complete and task-only diffs in `.local-work/diffs/`, Git status, changed-file and excluded-artifact manifests and patch verification. Never stage solely to generate diffs.

**Success for this assignment is an offline-qualified, independently reviewed observer *and* executable live procedure together, not a promise that live acquisition will validate native Workshop positioning.**
