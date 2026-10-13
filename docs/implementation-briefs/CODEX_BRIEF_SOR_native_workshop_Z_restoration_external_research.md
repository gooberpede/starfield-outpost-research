# Codex Research Brief — Native Workshop Z Restoration, Vertical Coordinate Frames and External Research

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment:** Offline investigation, deterministic reconstruction and independent review  
**Starting state:** Continue from the latest committed and synced repository, including SorNativePositionOracle 0.5.0 live capture, scientific report and Z/frame follow-up. **Do not restart prior investigations or overwrite frozen evidence.**  
**Authority:** Offline read-only game/save/native-analysis inspection, independently authored analysis tools and tests, and focused public technical research. No Starfield launch or process access, no new observer/hook, no debugger revival, no save mutation, no staging/commit/push.

## 1. Scientific objective

Determine **why saved Z and fresh native Workshop-center Z differ** for SOR-002 and SOR-003, and recover the dataflow, frame semantics and any native reference-restoration or height-selection transformation connecting them. A native center is a reference position in a particular engine frame; do **not** presuppose that Z is height above ground, global planetary elevation, or even that the saved and live values should be numerically equal.

Previous evidence establishes the horizontal result much more strongly than the vertical result: forty fresh Workshop grid observations, twenty per geometry, nonzero XY translations, exact native XY/grid agreement with frozen Save25/26 predictions, a radix-12 carry for SOR-003, and the matching native query-world/source-frame descriptor. The native grid routine's translation operand is **XY only**; a third copied word was unrelated adjacent stack data. Do not revive that false Z-translation interpretation.

### Fixed comparison controls (verify exact values against durable records)

| Workshop | Captured native center Z (approx.) | Saved/frozen Z (approx.) | Saved minus native (approx.) |
|---|---:|---:|---:|
| SOR-002 | +3.643147 | +18.352507 | +14.709360 |
| SOR-003 | -9.516418 | -31.890842 | -22.374424 |

These figures orient the investigation; use exact serialized/native bit patterns from the preserved source records in all actual tests. The opposite-signed differences reject a simplistic common Z shift. ExtraWorkshop relocation compensation was zero for these captures; check its precise contract and frame rather than introducing an invented compensation term. Keep SOR-003's moved-beacon Save26 case and the workshop-center invariance evidence in view.

**Success means a supported vertical transformation or a conclusive, scoped account of why presently available offline evidence cannot determine it—not a narrative guess calibrated to two Z differences.**

## 2. Required investigation — native dataflow

Follow the *producing writes and consumers*, not just field reads. Reconstruct, with instruction-level evidence and concrete ownership/identity boundaries:

1. The serialized reference's Z-bearing fields, their record/case structure, parent/world/cell context and lifetime across Save25, Save26 and other relevant controlled/mature saves. Distinguish site-anchor data, beacon transform, cached terrain data and runtime object position.
2. The loaded reference-position producer(s), including deserialization, parent/world/cell restoration, local-frame selection, potential origin rebasing, placement adjustment and applicable post-load writes. Determine **when** the saved value becomes the value consumed by the Workshop-center helper.
3. The frame-related byte at reference `+0xD3`: identify bit-level reads/writes and verify its meaning from code and actual captured or saved context; do not assign semantics from a suggestive flag name alone.
4. Height/terrain-selection paths: where terrain heights, offsets, vertical origins or restored Z enter **if they do**; inspect cache, landscape and procgen dependencies only as far as needed to establish the actual chain.
5. The Workshop center operation and its `ExtraWorkshop +0x60` compensation. Establish exactly which frame each term belongs to and whether any later transform affects the observed center Z.
6. The difference between the native query source-frame identity (now established for XY) and the individual reference's own loaded-parent/vertical-frame identity (not yet established). A matching packed source key is not proof of full XYZ frame equivalence.
7. Relevant negative controls and alternative native paths: explain why seemingly plausible formulas fail, record evidence and preserve counterexamples. Examine static fixed POI instances only if demonstrably governed by the same Z restoration mechanism.

Follow all relevant in-scope native dependencies to a defensible stopping point; do not stop upon finding the next untraced callee or missing operand. Maintain a compact dependency ledger with producer, transform, consumer, evidence, and remaining uncertainty.

## 3. Focused independent public research — specialist assignment

Use **one specialist sub-agent** primarily to investigate public prior art and independently challenge the Z-frame hypotheses. Suggested targets: SFSE/CommonLibSF; xEdit record/save research; Creation Engine reference transforms, cell/world origins and heightmaps; Starfield planetary terrain/procgen restoration; relevant Skyrim/Fallout 4 analogues **only where version-specific mechanism is demonstrated**. Search primary code, documentation, issue reports and technical discussions rather than relying solely on summaries.

For each useful external finding record: author/project, primary URL, revision/date when available, actual claim, supporting code/behavior, relevance to Starfield 1.16.244.0 and what our existing evidence corroborates or contradicts. Separate public third-party findings from project-derived facts and new inference.

**Permissions/provenance:** Follow repository `WORKFLOW.md` and source/credit policy. Read public sources under their terms; do not import/copy third-party code without the required rights/permission. Preserve original licenses and attributions where authorized. All `gooberpede` project-owned reuse follows existing project provenance practice. No new dependency or material license exposure merely to complete this research.

Require the specialist's final work product to be independently useful: a lead matrix, specific disproved hypotheses, native symbols or record relationships worth checking, and a concrete evaluation of which findings actually changed the reconstruction. Do **not** rerun the established reviewer-effectiveness evaluation; report specialist value briefly and substantively.

## 4. Executable reconstruction and validation

Where sufficient evidence exists, implement a deterministic Z restoration submodel in the existing offline positioning code (or an explicitly isolated diagnostic module if the native contract remains incomplete). The model must identify required frame and height inputs, exact arithmetic/order/precision when grounded, and return **UNKNOWN** instead of guessed values where operands cannot be recovered. Do not fit a two-point interpolation to SOR-002 and SOR-003 or infer planetary elevation from a single Z coordinate.

Preserve the **23 frozen predictions byte-for-byte**, original native capture blobs/hashes, save files and prior model behavior. Add independent positive/negative fixtures, saved/loaded frame variants, relocation controls, floating-point exactness checks where justified, and systematic tests of alternative Z hypotheses. Distinguish comparisons against genuine native observations from tests generated using the model itself. Report coverage by meaningful algorithm branch, not arbitrary sample count.

For each SOR-002/SOR-003 comparison supply: native observation ID and raw bits; saved reference/field and raw bits; Workshop identity confidence; source and loaded-frame provenance; any captured or inferred Z inputs; formula, predicted output, exact/tolerance comparison; and unresolved fields. Repeated events for one Workshop geometry do not count as independent geometries.

## 5. Acquisition assessment (design only)

If the missing transformation cannot be resolved offline, identify the **specific first unavailable producer/value** for each remaining plausible path. Rank minimal future acquisition options by their ability to distinguish competing explanations and advance *Workshop* XYZ equivalence, not by ease of hooking. Specify exact reference/frame identity joins and which observations must occur in the same invocation. A new SFSE observer, fresh controlled saves and new live experimental actions may be **proposed** but are **not authorized** by this brief. The closed external software-breakpoint debugger path must not be reopened.

Avoid a broad terrain-procgen project or a detailed ship-landing-marker generation reconstruction unless a proven Z dependency makes it essential.

## 6. Completion contract and independent audit

Follow the committed **Research Execution and Completion Protocol**. The primary agent owns in-scope failures, failed assumptions, corrections and regression testing within this assignment. An unexpected blocker or a specialist's negative lead is work to investigate, not a default stopping point. Do not present an unfinished chain or a list of further research tasks as completion.

Maximum **two concurrently active sub-agents**, excluding primary: one specialist and the independent reviewer. Review must use a separate context, original acceptance criteria and primary source/evidence, not just the implementer's summary. Reviewer verdict **ACCEPT / REWORK / ESCALATE**; any REWORK must be addressed in the *same assignment*. A genuine new live/action permission requires escalation, not an invented authorization.

Valid final scientific dispositions:

- **A — RECONCILED VERTICAL MODEL:** Evidence-supported native Z transformation and executable reproduction, with independently tested comparisons and scoped qualifications.
- **B — COMPLETE EVIDENCE-BOUND NEGATIVE:** Relevant native producers/consumers, save joins, plausible explanations and external leads substantially exhausted; exact unavailable inputs demonstrated; decisive minimal acquisition design returned. No claim of full equivalence.

Neither a passing internally generated test suite nor a strong horizontal result alone satisfies A. A scoped, well-defended B is valid research completion; a merely partial dependency trace is not. Retain evidence of falsified hypotheses and corrections.

## 7. Workflow and operating constraints

- **Strictly offline:** no Starfield.exe launch/open/attach, no live SFSE deployment, no in-game save creation, no executable patching of retail process, no debugger reuse.
- Original Saves, 0.5.0 captures, raw sections, binaries and frozen predictions remain immutable. Verify before/after with hashes and exact inventories; no raw/proprietary or private artifacts staged or bundled into patches.
- Both C: and D: must retain at least **40,000,000,000 caller-available bytes** for any substantial evidence processing; a failed check stops risky I/O. No arbitrary elapsed-time, evidence-size or operator-delay cutoffs beyond proven safety/resource requirements.
- No staging, committing or pushing. Retain local diagnostic evidence in ignored `.local-work` locations.
- Produce complete cumulative (`-complete.diff`) and task-only (`-task-only.diff`) review patches in `.local-work/diffs/`, including untracked authored text and a status, file/hash and exclusion manifest; verify patch applicability. Follow `WORKFLOW.md` and existing documentation conventions.
- There is **no requirement to create or update an observer** as a substitute for finishing the offline native Z investigation.

## 8. Required deliverables before final handoff

1. Durable scientific report giving the Z problem, established evidence, dataflow diagrams/ledger, tested hypotheses, exact results and confidence/coverage distinctions.
2. External research/provenance ledger clearly separating published findings, Starfield-specific verification and unsustained leads.
3. Deterministic code/tests or a precise demonstration of why an exact Z submodel is unsupported, with useful executable partial functions where warranted.
4. Per-Workshop comparison ledger including both SOR-002 and SOR-003 and all relevant source/reference/frame provenance.
5. Decision-ready ranked acquisition assessment, if any residual native input is missing.
6. Independent reviewer verdict, acceptance matrix with primary evidence pointers, specialist contribution assessment, and documented REWORK resolution.
7. Complete and task-only diffs, verification receipts and a concise final summary stating **A or B**, what is and is not validated, and suggested commit subject.

**Do not end at postflight/preservation-only status.** Scientific synthesis and independent review are part of the assignment. A genuine new permission question is an escalation; do not hide a missing scientific conclusion behind a successful test count.
