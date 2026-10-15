# Codex correction and scientific reassessment brief

**SOR-EXP-0036 / SorNativePositionOracle 0.8.0 — prose repair and experiment go/no-go decision**

**Status:** Requested correction/reassessment; **supersedes the previous ACCEPT as a basis for committing or going live**. Do not treat this brief as authorization to deploy, launch Starfield, perform native invocation, commit, stage, push, delete or modify protected evidence.

## 1. Why this task exists

The pre-live 0.8.0 package passed extensive offline engineering qualification (reported 127 Python tests, native/lifecycle controls and 6,847 protected pins), and its independent reviewer accepted it. Subsequent critical review found two blockers:

1. Malformed, concatenated prose recurs throughout new and edited documentation; the previous reviewer missed it.
2. More importantly, technical qualification did not establish that a successful **first live session** would settle a consequential research question. The current thirteen-hook, A/B/C preview-oriented experiment does not capture complete source-region geometry, native candidate accept/reject decisions, or an authoritative region-generation completeness state. Several hypotheses either retest established 0.7.0 results, concern modest semantics, or cannot be resolved by the proposed data. A further capture may therefore have poor scientific return.

**The purpose of this assignment is to repair the textual defect and make an independent, evidence-based go/no-go decision about scientific value. It is NOT to justify the work already completed.** An explicit **NO-GO / reject the live experiment** is a fully successful outcome.

## 2. Authority and limits

- Work only within the current uncommitted 0.8.0 task changes and necessary focused verification/documentation. Preserve prior 0.7.0 and 0.8.0 historical evidence, receipts and candidate qualifications.
- **Do not modify, rebuild, enlarge, redeploy or rerun the 0.8.0 observer/native hook/DLL/Vortex ZIP in this task.** No new instrumented call sites, runtime experiments, synthetic native invocation, live Starfield execution, save modification, or additional hooks.
- Do not stage, commit, push, change deployed game files, remove or archive originals, or replace any protected asset. Do not revise earlier research findings merely to conform to a preferred experimental outcome.
- Perform the reassessment **before** any recommendation to revise instrumentation. If revision is the outcome, produce a separate proposal for user approval; do not implement it here.
- Respect the current `WORKFLOW.md` and research execution/review procedures. Use an independent reviewer with a substantive adversarial remit; no need to spawn additional specialists unless a specific gap justifies it. The reviewer must assess both writing quality and scientific decision quality, not merely test pass receipts.

## 3. Track A — repair and audit prose in the task patch

Audit **all added and changed Markdown/documentation prose** in the 0.8.0 task, including indexes, reports, run card, schemas, README files, contribution/credits text, and new entries in existing registers. Inspect in context, not simply by matching a handful of strings. Correct omitted spaces, fused words, concatenated version identifiers, unexplained token adjacency, broken sentences, encoding defects, and inconsistent terms without changing scientific claims or numeric evidence.

Known examples from `local-readiness-final-complete.diff` include:

- `CREDITS.md`: `project-owned070/060/evaluator`;
- `docs/RESEARCH_STATE.md`: `prepare observer0.8.0`;
- `docs/experiments/local-readiness/native-map.md`: `state0x68 includes vector triples`, `Source visit reads closure0x18, slot8`;
- `docs/experiments/local-readiness/release.md`: `session/event schema8, retail1.16.244.0`;
- `docs/experiments/local-readiness/contract.md`: `closure0x18 and source-value slot8`.

These are **examples, not an exhaustive checklist**. Take care: expressions like `0x68`, ABI names, exact identifiers and machine-readable schemas may legitimately remain adjacent in code, register names, column values or quoted native snippets. Fix prose based on meaning and style, not a global regex that might corrupt genuine technical identifiers or hashes.

Provide a focused before/after defect log with file paths and representative corrections, and a diff-scoped final prose audit. Record any ambiguous instances. Ensure no sweeping formatting or repository-wide churn. If a factual edit is necessary because the prose conceals a technical contradiction, explicitly flag it for review rather than silently rewriting the finding.

## 4. Track B — scientific value go/no-go reassessment

Reopen the **decision to run**, not only the question of whether the observer runs safely. Read the original local-readiness brief and the committed native mapping / resource-region dependency reports, the current `contract.md`, `native-map.md`, `schema.md`, `run-card.md`, `invocation-assessment.md`, qualification and review records, and the prior 0.7.0 evidence conclusions. Use their actual contents rather than assuming a planned event can answer an intended question.

For **every** hypothesis H1–H6 (and any asserted primary objective), prepare a decision matrix containing:

1. **Material question** and its relevance to the core scientific objective: minimum state/inputs required for a correct, current inorganic resource-availability determination.
2. **What is already known** from native code, 0.7.0 observation and Milestone B; why another live observation is needed.
3. **Competing hypotheses** consistent with current evidence, including cache/state-history alternatives.
4. **Precisely captured operands and events** in this immutable 0.8.0 candidate, plus relevant missing operands; distinguish natural callbacks, upstream/downstream events and correlation across asynchronous operations.
5. **Controlled in-game action** in the *actual first run card* expected to generate discriminating evidence; distinguish mandatory from opportunistic paths. Do not credit an established-Workshop or player-displacement result when the card does not require those scenarios.
6. **Discriminating outcomes:** for each realistically observable result, state what it would demonstrate, refute, or leave unresolved. Explain failure/negative controls, freshness, absence-of-event ambiguities and instrument-capacity loss.
7. **Proof category:** decisive test; bounded falsification only; illustrative/confirmatory; or **not testable**. Never equate observed source visitation with native acceptance, cache entries with complete generation, provider return with successfully constructed geometry, or a refresh flag with a changed result unless explicitly established.
8. **Scientific payoff versus cost/risk:** realistic incremental finding, information gain, thirteen-hook runtime risk, user time in game, evidence volume, verification and review burden. Already-sunk implementation effort is **not** a reason to run.

Pay special attention to the previously identified mismatch:

- H1 (does every updater scan source maps?) may largely rediscover cache behavior.
- H2 (does provider return certify completed geometry?) cannot be proven by headers alone.
- H3 (does source visitation mean spatial acceptance?) cannot be proven without actual native candidate decisions.
- H4 (does refresh imply a changed set?) is testable but may be a minor clarification.
- H5 (does UI reflect the originating evaluation?) overlaps the established 0.7.0 aggregation/lineage result and may lack sufficient ancestry.
- H6 (are preview and established descriptors equivalent?) is not deliberately exercised in the first run card.

**Challenge this preliminary analysis where the actual patch provides evidence to do so; do not merely repeat it.** Identify whether *any* combination of attainable results from the planned live session would close an important uncertainty about source readiness, resource-region completeness, spatial equivalence, local query input sufficiency, or player-position requirements.

The decisive gate is:

> Assuming every 0.8.0 instrumented site runs safely and every planned record is captured correctly, what important previously unresolved proposition will this first session decisively settle, or what substantial competing explanation will it eliminate?

If the answer is insubstantial, speculative, dependent on unplanned scenarios, or unobservable with existing fields, recommend **NO-GO**. A session that merely creates more trace data does not pass.

## 5. Valid decisions (no preferred outcome)

Return **one** of these, with a clear rationale:

- **GO as-is:** The *existing immutable* observer and actual run card can decisively resolve one or more consequential uncertainties. State the exact test, expected disambiguation and interpretation of outcomes. This is a recommendation for **subsequent separate live authorization**, not permission to launch now.
- **REVISE before considering a live run:** A specific, high-value discriminating test exists but the current observer or run card cannot perform it. Explain the minimum additional evidence/controls and why it is worth the cost. **Propose only; do not implement, rebuild or deploy.** If revised instrumentation would be a broad new project, say so.
- **NO-GO:** No proportionate first live experiment is supported at present; preserve the qualified observer as an unadopted historical candidate, document what was learned in the preparatory work and stop. No implied obligation to plan another experiment.

Do not relabel a non-decisive result as an acceptable "bounded outcome" merely because the original brief allowed evidence-bound findings. Distinguish legitimate bounded scientific findings from *predictably low-information experiment design*.

## 6. Independent reviewer remit

The reviewer must independently examine the changed prose **and** attempt to disprove the scientific-value case. Require the reviewer to ask:

- Can the asserted decisive observation actually be recorded by this exact schema and thirteen-hook set?
- Does the real operator script force or reliably present the necessary runtime path?
- Are upstream, UI and asynchronous events improperly joined by timing or assumed ancestry?
- Could identical output occur under several materially different cache/readiness states?
- Has the analysis overlooked a lower-cost answer available from already retained static or runtime evidence?
- Does the recommendation favor deployment because of sunk effort or because the observer has passed tests?
- Is the full changed-documentation surface free of malformed prose?

A simple independent `ACCEPT` without hypothesis-level critique is insufficient. Record findings, rework and final reviewer decision. If the reviewer and implementer disagree, preserve both positions and reasons; do not resolve by assertion.

## 7. Deliverables and handoff

Produce a compact, durable assessment under `docs/experiments/local-readiness/` (e.g. `scientific-value-reassessment.md`) containing the hypothesis matrix, evidence cited by paths/native RVAs and event-field names, GO/REVISE/NO-GO decision, uncertainty boundaries, and explicit treatment of original run-card coverage. Update `review.md` / appropriate status/index entries to **supersede the earlier pre-live ACCEPT for authorization purposes** and distinguish offline engineering qualification from experimental scientific merit. Avoid marking the experiment live-ready unless an explicit GO case is accepted and later authorized by the user. Keep native findings and provenance unaltered.

Provide:

- Focused prose correction log and results of a **diff-scoped** manual/document audit.
- Scientific reassessment and independent-review record.
- Exact file list and high-level nature of edits.
- Offline validation appropriate to documentation-only changes; rerun focused tests only if actually impacted. Do not suggest that passing tests validates the scientific hypothesis.
- Updated **task-only** and **complete** diffs under `.local-work/diffs/`, including newly created textual documents, with forward/reverse patch checks or equivalent integrity receipts.
- Review package/checksums and unambiguous recommended disposition of the current pre-live package and proposed live session.
- A conventional commit subject **only if** there is a coherent commit-worthy disposition; note separately that no commit or live deployment is authorized here.

**Stop after this reassessment.** Present the corrected patch and decision for ChatGPT/user critical review. Do not continue into a new instrument implementation or runtime session without a separate brief and authorization.
