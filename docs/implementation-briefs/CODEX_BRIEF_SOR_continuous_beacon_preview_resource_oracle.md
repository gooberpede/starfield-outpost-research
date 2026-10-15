# Codex implementation brief — Continuous Beacon-Preview Resource Availability Oracle

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment:** Offline implementation, qualification, complete integrated live procedure, and independent review. **No live execution in this assignment.**  
**Primary control:** Attila Kiraly **Save3**, Kreet surface, before any outposts exist.  
**Status:** Implementation authorized; deployment and the live experiment require a single combined maintainer/ChatGPT review and explicit approval.

## 1. Scientific objective and scope

Recover **the actual inorganic resource identities reported by Starfield's “Available Resources” panel for a prospective, still-unplaced outpost beacon**, continuously as its proposed placement position moves. This is about **resources present in the prospective outpost area**, not constructed extractors, extractor footprint feasibility, production, deposit geometry, or planet-wide resource lists.

Treat the player-visible Available Resources panel as the gameplay reference. Do not introduce unsupported skepticism about whether an ordinary listed resource is practically extractable. The native producer and UI may refresh at different times; investigate and record that distinction rather than assuming synchronous delivery. Inorganic resource presence must remain independent of extractor construction. Helium-3 on Kreet is an atmospheric, location-independent control; Iron and Alkanes offer a useful location-dependent contrast. Do not hard-code those resources or require a specific transition to call a valid scientific capture successful.

**Two milestones remain distinct:** (A) event-associated native resource-set observation with agreement against the displayed UI; (B) an independent offline reconstruction from available deterministic inputs. Milestone B is desirable but **not a gate** for A; the existing offline investigation established that producer save records are not a comprehensive local availability list.

## 2. Starting evidence and required source review

Read repository `AGENTS.md`, `WORKFLOW.md`, the Research Execution and Completion Protocol, current research/decision/evidence registers and provenance rules. Begin with the committed resource-availability investigation in `docs/experiments/resource-availability/` and its native dependency ledger. Verify the native producer `WorkshopAreaResourcesDataModel` (previously traced near RVA/VA `0x1421E07D0`), UI-row builder (previously near `0x141578500`), generated resource-region contribution, atmosphere contribution, and selected-biome water branch, **against the pinned executable**. Addresses here are research landmarks, never approval to patch without exact current-image guards.

Reuse existing SFSE observation patterns, qualification fixtures, WAL/decoder conventions, and save-menu identifier `save-analysis/scripts/save_menu.py` where suitable. Preserve source/revision provenance for reused project-owned code; respect licensing and permission restrictions on any external implementation.

Before choosing hooks, produce a dependency graph that identifies: preview beacon actor/reference or placement context; proposed position read **at the evaluation boundary**; input resource populations; de-duplication/aggregation; data-model handoff; and final UI row identities. Distinguish native invocation identity, UI update identity, and asynchronous queue/callback ancestry. Do not infer a position from the player character or from a later unpaired beacon sample.

## 3. Observer implementation

Create a versioned SFSE observer (choose an appropriate successor identity, avoiding collisions with preserved observer releases) that performs **continuous, event-associated acquisition** while beacon placement preview is active. It must be able to retain repeated unchanged evaluations as well as actual resource-set changes.

Capture, subject to source-backed native contracts:

- Evaluation identity, thread and monotonic ordering, native function/caller and execution branch or cache status when verifiable.
- Proposed **beacon** position (XYZ and relevant world/terrain/placement identity), with a flag distinguishing an actual evaluation-time argument from any independently sampled/non-atomic state.
- Resource identifiers and provenance for generated-region, atmosphere and biome/water populations, including observed duplicates and aggregation rules; capture the actual native union/output whenever feasible.
- Final resource identities delivered into the UI data model/rows, update/correlation identity where available, and whether the displayed set is new, unchanged or a delayed refresh. Do not claim UI rendering was directly observed if only a native data-model write was observed.
- Raw evidence sufficient to re-decode identities and investigate disagreement; distinguish unresolved IDs from empty sets.

Prefer the **smallest supported native hook surface** needed for the above. An observer that merely reports one unbound set or reads a stale shared buffer does not satisfy the contract. Do not add broad terrain-procgen, extractor-footprint, or game-save writing instrumentation. If an essential edge lacks a safe native observation, investigate alternatives and return a precise reviewed evidence/authority gate rather than inventing coverage.

### Transport and lifecycle

Preserve ordered, recoverable evidence with integrity hashes, explicit recording of overflow/write failures and **no silent loss**. Use buffering/backpressure appropriate to continuous capture, and distinguish admitted, written and durably flushed event counts. Capture rates must not silently discard samples. Failure or partial tail must never be represented as scientific absence. Qualify register, stack, SIMD/FP and control-flow preservation; nested/concurrent events; exception propagation; patched-site verification and rollback where possible; and safe retirement. Record limitations on true cross-thread atomicity and unexpected-crash durability.

## 4. Offline qualification and acceptance

Build disposable fixtures exercising at least: stationary player while moving the proposed beacon; resource sets constant across several evaluations; changed region resources (e.g. Fe versus Fe+Alkanes); constant atmospheric He-3; return to equivalent *set* without exact position reproduction; concurrent/nested updates; different ordering between native evaluation and UI delivery; cached/skipped UI refresh; unknown IDs; failed/partial read; high event rate and storage faults. Exercise A/B/C as **set conditions**, not exactly reproduced coordinates.

Require deterministic raw decoding, supported site/world identity, invocation pairing, explicit missing-edge statuses, replayable assertions and an independent native/UI reconciliation method. Test integrity of protected saves, archives, prior observer builds, frozen position predictions and other pinned research evidence. Keep all earlier scientific classifications unchanged.

The final engineering package must include full test receipts and a transparent **PASS / FAIL / NOT TESTED** acceptance matrix. A functioning DLL without qualified event-to-beacon-position and UI-resource association is not an acceptable completed implementation. Resolve in-scope fixture failures before handoff under the existing completion protocol.

## 5. Integrated live run card — prepared now, executed later

Deliver the exact run card alongside the implementation, versioned Vortex ZIP and manifest. **No Starfield launch, deployment or live save action now.** Following one combined review and the maintainer's explicit authorization and Vortex deployment, Codex may conduct machine-side preflight and coordinate the approved run without another routine approval, provided all mandatory checks pass.

**Primary save:** Save3, **Attila Kiraly — Kreet - Kreet — Level 3 — 10/6/26, 12:34:27 PM**, as previously validated by `save_menu.py` and the load-screen control. Reverify the hash-bound source identity and use the utility to generate the operator's instruction before launch. Do not ask the operator to repeat the full label after providing the instruction unless there is real ambiguity. Save3 contains no constructed outposts and is preferred over later Kreet saves. Alternative saves must have a documented scientific or operational reason and receive review if the run card's scope changes.

Proposed operator sequence:

1. Start via reviewed SFSE/Vortex configuration. Verify pinned game/SFSE/DLL, guarded native sites, log/admission/worker health and disk integrity before loading Save3.
2. Operator loads Save3, reaches legal beacon-placement preview without confirming the placement, and reports that the Available Resources panel is visible.
3. Observer captures continuously; operator may remain stationary and move **the preview beacon**, seeking at least two differing displayed resource sets if conveniently available. Iron-only versus Iron+Alkanes is useful, not mandatory; Helium-3 is the atmospheric control. No exact return to A is required. An optional return to another position showing the earlier set is sufficient.
4. Collect user-visible list observations or screenshots at useful transitions, with simple operator phase markers and timestamps. The run card must explain how the native evaluations will be paired with these observations without asserting exact UI timing from a handwritten observation.
5. Cancel preview without placing the beacon. Request STOP; drain/retire, exit game normally, remove the Vortex deployment, perform protected-input postflight, seal evidence, and **complete the scientific report and independent review** before final handoff. The operator may request a short postflight-only update, but this should not be misread as cancellation of the scientific report.

No new manually saved checkpoints, construction, console commands or other gameplay experiments are authorized by this prospective card. If preflight shows Save3 is unsuitable, return an evidence-backed alternative for review rather than silently changing controls.

### Operational requirements

Only runtime-required payloads (normally `Data\SFSE\Plugins\SorNativePositionOracle.dll`) may be mandatory in Vortex deployment checks. READMEs/manifests/other optional text files are not required beside the DLL. Normal Steam and NVIDIA overlays are accepted and inventoried. Maintain **40,000,000,000 bytes available on each of C: and D:**, exact executable/DLL/native-site integrity, protected saves and evidence-health checks, and the operator's explicit STOP. Do **not** introduce arbitrary session timers, operator deadlines, event quotas or output-size stop thresholds. A genuine safety/integrity failure remains a hard stop; if a new cutoff is essential, justify it and ask the maintainer *before* execution.

## 6. Required deliverables and review discipline

Return together:

1. Native/UI source and call graph with evidence-linked instrument choice, including separate resource populations.
2. Qualified SFSE observer source, build provenance, byte-pinned Vortex ZIP and effective DLL deployment contract.
3. Streaming/recoverable recorder, decoder and inspector with adversarial/disposable tests and fixture evidence.
4. Complete executable Save3 run card, exact preflight, operator instructions, STOP/retirement/postflight, and evidence reconciliation plan.
5. Scientific and engineering acceptance matrix, known limitations, source/provenance register and independent reviewer verdict.
6. Both task-only and complete cumulative review diffs in `.local-work/diffs/`, including untracked authored text, status, hashes, inclusion/exclusion manifest and exact patch verification. Do not stage to create these diffs.

Use the established **primary Codex + at most two concurrently active sub-agents**: independent reviewer required; one specialist permitted when substantively helpful, preferably for independently auditing the native UI resource-data flow and linkage of preview position to resulting set. Specialist findings should be attributed in the internal research record and reconciled by the primary implementer. The reviewer must challenge event/position correlation, false UI-equivalence claims, insufficient native observation coverage and unapproved scope changes; actionable REWORK remains within this assignment.

### Authority and final status

This assignment authorizes **offline research, implementation, disposable qualification and procedure preparation only**. Do not launch Starfield, change saves, deploy, modify game settings, stage, commit or push. No external-debugger revival. Preserve all historical results and protected evidence. A completed outcome must enable a concrete, defensible combined maintainer review of the exact observer and run card; do not reclassify missing implementation or failing mandatory tests as a convenient scoped success.
