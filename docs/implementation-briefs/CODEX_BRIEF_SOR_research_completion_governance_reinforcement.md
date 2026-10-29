# SOR — Research Completion Governance Reinforcement

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)

**Assignment:** Documentation-only governance implementation and independent adversarial validation. **No new scientific investigation** under this assignment.

**Status:** Proposed Codex implementation brief. Freeze GOV-AC1–GOV-AC9 before execution. The maintainer has authorized preparing this brief, not staging, committing, pushing, live execution, publication, or a material relaxation of existing rules.

## 1. Problem and completion contract

The existing [Research Execution and Completion Protocol](../RESEARCH_EXECUTION_PROTOCOL.md), [compact completion contract](../templates/completion-contract.md), [reviewer instructions](../reviewers/research-completion-reviewer.md), and [WORKFLOW](../../WORKFLOW.md) already require continuation, strict criteria, and independent review. Recent D5R closure nonetheless demonstrates a governance failure mode: a correct *bounded* intermediate research account was accepted while the controlling scientific question—whether upstream scheduling uniquely determines the winning construction query—remained unanswered and authorized native leads were still available. **Do not treat these rules as absent, and do not replace them wholesale.** Identify the enforcement gap and tighten it with minimal, enforceable changes.

**Controlling objective:** Make premature closure of substantive research detectably nonconforming. An investigator must pursue relevant authorized dependencies until the contracted scientific question is answered (including a qualified negative answer), or a specific, evidenced terminal barrier to further authorized investigation is demonstrated and independently challenged. Good documentation, a scoped sub-result, completed deliverables, or a reviewer’s agreement with the *accuracy* of a report cannot substitute for completion of the controlling question.

**Outcome contract:** `COMPLETE` (positive or adequately scoped negative result), `BLOCKED` (specific demonstrated barrier and narrow escalation), or `INCOMPLETE` (answer outstanding, viable authorized work remains). `INCOMPLETE` may be preserved as a checkpoint or handoff, **not** independently accepted as a completed scientific assignment. An independently accepted *method-abandonment* result must not close its parent scientific question. An unqualified `ACCEPT` must be impossible when a mandatory controlling objective remains `INCOMPLETE`; an evidenced `BLOCKED` must be reported as `ESCALATE`, not silently converted to scientific completion.

**Task type:** Governance/documentation implementation. **Mandatory deliverable:** targeted changes to standing instructions, completion contract, reviewer procedure and one practical verification/example record. **Negative result:** If an instruction cannot be made enforceable within the actual available reviewer/execution mechanisms, demonstrate the exact limitation, preserve a manual fallback and escalate the smallest missing capability. Mere writing of policy text is not proof of enforcement.

## 2. Inspect existing authority before editing

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/DECISIONS.md`, `docs/RESEARCH_STATE.md` and relevant governance decisions. Inspect the D5R brief, report, review and query-scheduling map, plus D5P-R3's brief, report and review. Check actual current files/HEAD and preserve the original classification of every historical result.

Record briefly **which existing safeguards already address** continuation, scoped negative closure, independent review and escalation, and **why their existing wording or review procedure permitted a D5R-style premature closure**. Distinguish a weak original contract from a review that accepted compliance with a narrow contract; neither may be fixed by retrospectively changing frozen D5R acceptance criteria or rewriting prior decisions.

Prioritize small, nonduplicative amendments in existing documents. `AGENTS.md` should give the short standing directive and point to the authoritative protocol; `WORKFLOW.md` should describe operational handoff; the protocol should define outcome and enforcement semantics; the compact template should require the question and terminal proof; the reviewer instructions should make adversarial completeness review mandatory. Amend `EVIDENCE_STANDARD.md` only where genuinely needed to distinguish scientific sufficiency from claim coverage. Do not scatter competing rules across multiple new policy files.

## 3. Required governance rules

### G1 — Controlling scientific question and no silent narrowing

Every substantive research brief must state one or more **controlling questions**, their success/falsification conditions and the level of generality actually required. Intermediate discoveries, diagrams, correct bounded analyses and complete documentation do not change the question. The investigator cannot change a controlling question, reduce its applicability, change mandatory criteria, or redefine `BLOCKED` without explicit, recorded maintainer approval. The reviewer checks the *original frozen* question and amendments, not a reformulation in the final report.

A scoped negative conclusion may be `COMPLETE` when it actually meets the original falsification/insufficiency contract. Do not require a universal impossibility proof or force an endless search after a decisive, qualified falsification. Conversely, a constructed model with unresolved engine ordering does not settle the real scheduling question.

### G2 — Follow dependencies within authority

A discovered upstream caller, work queue, scheduler, streaming ingress, input provenance, relevant native writer, or reasonable alternative observation method is **work to investigate**, not an automatic new-project boundary. Track the dependency and pursue it while it remains material to the original question and within authorized read-only/static/fixture or otherwise explicitly authorized operations. Crossing a subsystem or document boundary is not, by itself, grounds to stop.

Do not silently turn an essential dependency into an optional follow-up, or declare a bounded mapping complete merely because a new boundary is identified. Prioritize by expected discrimination and avoid irrelevant combinatorial exploration; for a genuinely unbounded search, record justified boundaries and why remaining paths cannot change the conclusion. Do not expand into live launches, plugin deployment, Ghidra database edits, protected save writes, network disclosure or third-party reuse without the relevant separate authority.

### G3 — Active durable investigation ledger

Require an **active** ledger, created near the start and updated during the work, recording: stable question/criterion IDs; current hypotheses; native/data boundaries; evidence-backed results; counterexamples; dependencies discovered; source and investigation paths actually checked; viable/untried leads; failed alternatives with reasons; and explicit disposition for every material branch (`resolved`, `disproved`, `irrelevant with evidence`, `blocked with evidence`, `open`). Include next concrete action and reproducibility pointers. Timestamp/checkpoint only when meaningful; no fabricated chronology or excessive routine logs. An end-of-task retrospective alone does not satisfy active maintenance.

Use existing experiment/local scratch and durable-document conventions; avoid a redundant global ledger framework. Maintain readable summaries and exact evidence links while keeping raw proprietary data local. The ledger is a control against losing investigative branches across long sessions and context compaction, not a substitute for findings or independent verification.

### G4 — Hard `BLOCKED` proof and narrow escalation

A terminal blocker must identify: the precise missing data/value, function/edge, safety boundary, access limit or indispensable action; why it is necessary to answer the controlling question; attempts and verified observations; alternative routes considered and why they fail or remain unavailable; residual avenues and their impact; whether the barrier is intrinsic to the method, tool/session/resource-limited, or merely unapproved; and the **smallest permission, input, experiment or capability** that would permit progress. Do not claim intrinsic impossibility from a failed technique. Tool/session exhaustion is documented with a durable resume checkpoint, not called a scientific result.

`Codex could not find`, `unknown upstream caller`, `would need further research`, `no time`, and `the reviewer accepts the report` are not blockers without the required proof. A prohibition on live work is an authorization boundary: continue all independent authorized offline work and escalate only the needed live action. A safe STOP must always override any pressure to continue.

### G5 — Independent reviewer as completeness challenger

The independent scientific/completeness reviewer must receive the **original brief/contract, investigation ledger, primary evidence and negative controls, current tree and proposed final claims**, not only the implementer's report. Require a branch-by-branch challenge: Is each unresolved dependency irrelevant, disproven, proven blocked, or still tractable within scope? Independently identify at least the highest-value omitted or untested avenue, or record the evidence showing none remains. Reviewer should inspect counterexamples, source coverage and alternative methods and must return **REWORK** when a tractable mandatory lead is left open. Where lack of authority or evidenced terminal limit is the only obstacle, return **ESCALATE** and preserve the unfinished scientific question. `ACCEPT` is reserved for completed mandatory contract outcomes, including valid scoped negatives.

Keep engineering/evidence, scientific/completeness and editorial dispositions distinct. Independent reviewer must not self-review its edits; match actual tool capabilities and preserve the existing manual two-pass fallback. Exact reviewed hashes and any post-review delta remain governed by current rules.

### G6 — Precise closure and historical integrity

Every substantial delivery reports (a) controlling-question status `COMPLETE` / `BLOCKED` / `INCOMPLETE`; (b) criterion-by-criterion PASS / FAIL / NOT TESTED; (c) scientific claim coverage; (d) engineering/operational integrity separately; (e) reviewer `ACCEPT` / `REWORK` / `ESCALATE`; (f) a short unresolved-dependency disposition table. An objectively completed, separately authorized *bounded subtask* may be accepted as such, but **must explicitly leave its parent objective open**, with the parent ID/status visible. Reviewers must not allow a parent-level completion claim to be inferred from subtask acceptance.

Prospective only: do not retroactively relabel D5R or D5P-R3 acceptance records, rewrite their criteria, purge historical negative evidence or reclassify published claims. Governance changes must be recorded through existing decision conventions and cross-linked to the policy; maintainer integration remains separate.

## 4. Adversarial governance verification (mandatory)

Create concise, repeatable decision-table fixtures and reviewer test prompts against the **final amended rules**. At minimum evaluate:

1. **D5R-style premature closure:** Query-weight differences, 40,320 model permutations and accurate mapping, but upstream streaming ingress and actual winner remain uninvestigated despite permitted read-only routes. Expected: `INCOMPLETE` / reviewer `REWORK`, **not scientific COMPLETE**; note that historically frozen D5R criteria are not retroactively changed.
2. **D5P-R3-style method NO-GO:** An unsafe large-Grid counterfactual is disproven by allocation-alias and concurrent-reallocation controls, production repair unqualified. Expected: the unsafe implementation method may receive an independently accepted *bounded negative feasibility finding*, with production engineering NO-GO and parent objective explicitly open; no fabricated PASS for repaired implementation. Show when the same case would be REWORK because viable authorized routes remain in the *same controlling assignment*.
3. **Decisive scoped falsification:** Appropriate controls refute the original bounded hypothesis. Expected: `COMPLETE` negative is allowed, without universal impossibility work.
4. **Real authorization barrier:** Essential live observation required after offline routes demonstrated insufficient. Expected: `BLOCKED` / reviewer `ESCALATE` on that action, with exact proposed discriminating test and evidence-preserving checkpoint; no unauthorized launch.
5. **Misleading clean report:** All prose, hashes and diagrams valid but a mandatory native branch never inspected. Expected: `INCOMPLETE` / `REWORK` despite editorial acceptance.
6. **Scope amendment:** Investigator quietly narrows the objective. Expected: rejection pending explicit maintainer approval; preservation of original contract.

Run both a literal rubric/structure check (documents contain necessary rules and references) and an **independent adversarial application** to the cases. Report expected versus actual decisions, defects and corrections. Do not claim a reviewer was independent unless a separate context/session actually reviewed evidence; if tools are unavailable, use the documented manual fallback or report `NOT REVIEWED`, which prevents accepted closure unless explicitly allowed by the frozen contract.

## 5. Authorization, preservation, and editorial boundaries

Documentation-only: edit only relevant governance documents, the test/example record, supporting deterministic check if justified, and focused decision/navigation entries. No Starfield, SFSE, Vortex, debugger, live instrumentation, Ghidra mutation, protected-save reading or writing, new scientific analysis, bulk repository reorganization, dependencies, external communication, publication, staging, committing or pushing. No arbitrary evidence/time/volume ceilings. Existing save protection, disk-space guards, provenance and publication restrictions remain unchanged. Raw data, native exports, protected saves and review scratch remain private/local-only.

Retain complete and task-only review patches (including untracked text and the supplied brief), exact changed-file manifest, source/HEAD/index status, exclusions and patch applicability/content checks under `WORKFLOW.md`. Run `docs/EDITORIAL_STANDARD.md` screening, full changed-prose reading and independent final-snapshot review. Supply original failed attempts and final reviewer returns where they exist; do not summarize failure away.

## 6. Required deliverables

- Targeted amendments to `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, and `docs/reviewers/research-completion-reviewer.md`; amend `docs/EVIDENCE_STANDARD.md` only for a demonstrated need. Respect authoritative cross-links and avoid duplicate/conflicting definitions.
- A brief gap analysis showing prior wording, identified failure mode and new enforceable requirement, with exact section/file pointers.
- A compact governance validation report with the six adversarial cases, expected/actual dispositions, independence limits and all corrective iterations. Store it alongside existing governance review conventions rather than spawning a policy directory.
- A focused decision record under `docs/DECISIONS.md` if required by current decision-log conventions, plus only necessary navigation updates.
- Independent scientific/completeness and editorial review of the final policy and cases; engineering/implementation verification for the checker if one is written.
- Complete/task-only diff exports, exact manifests and hashes, verified applicability and working-tree status. Nothing staged, committed or pushed.

## 7. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **GOV-AC1 — Baseline and permissions** | Read current actual governance and case records; preserve frozen historical science, protected inputs and authority boundaries. No unauthorized operational actions. |
| **GOV-AC2 — Enforcement-gap diagnosis** | Identify exactly how existing continuation/reviewer rules failed to prevent bounded intermediate closure; explain changes without pretending prior safeguards did not exist. |
| **GOV-AC3 — Outcome/contract semantics** | Implement controlling-question identity, complete/blocked/incomplete statuses, prospective no-silent-narrowing and clear reviewer mappings without confusing scoped negative work or method abandonment with scientific closure. |
| **GOV-AC4 — Dependency pursuit and blocker proof** | Enforce pursuit of material authorized dependencies, evidence-backed terminal barriers, scoped escalation and durable active-ledger dispositions; maintain safety and permission gates. |
| **GOV-AC5 — Independent completeness mandate** | Reviewer directly audits primary evidence, unexamined avenues and the original contract; REWORK/ESCALATE cannot be replaced by editorial acceptance or self-review. |
| **GOV-AC6 — Adversarial validation** | Execute and document all six discriminating policy cases against final wording; review omissions and correct detected ambiguities before final acceptance. |
| **GOV-AC7 — Focused implementation** | Coherent minimal existing-file edits, accurate links/decision records, no unrelated documentation sweep, no retrospective rewriting. |
| **GOV-AC8 — Editorial and evidence integrity** | Changed-text screen, full manual prose pass, primary-evidence traceability, exact-snapshot independent editorial and technical/completeness review with actual returns and disclosed limits. |
| **GOV-AC9 — Delivery and independence** | Frozen acceptance matrix; status/exclusions; exact-hash complete/task-only diffs and applicability; no stage/commit/push; no false independent review claims. |

**Nonclosure rule:** A failed or untested mandatory criterion is `REWORK` if rectifiable within existing authority, or `ESCALATE` for a demonstrated terminal blocker. Merely reporting the failure does **not** satisfy this governance task. The maintainer alone approves integration. After accepted governance integration, D5R's still-open *parent scientific question* may be commissioned as a separate D5S investigation with a question-level completion contract; this brief does **not** authorize D5S science.
