# Codex implementation brief — Research Execution and Completion Protocol

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment:** Workflow and documentation changes only (step 1 of the agreed two-step rollout)  
**Date:** 2026-10-11  
**Status:** For implementation and critical review; **do not begin the step-2 research trial**.

## 1. Purpose and governing distinction

The project's principal workflow failure has been **premature termination of assignments**, not a high rate of unsuccessful research hypotheses. The maintainer explicitly expects a research failure rate **greater than 50%** and regards a well-evidenced negative finding as a valuable *completed* result. The defect to correct is returning before a hypothesis has been adequately tested, before a required implementation has passed or been defensibly rejected, or when an in-scope failure simply requires more investigation.

Establish durable standing orders that make it difficult to confuse:

1. **Completed positive research** — hypothesis or model supported within a precisely stated scope and evidentiary standard.
2. **Completed negative research** — hypothesis or method tested adequately and rejected within that scope, with preserved counterexamples, limitations and reproducible evidence. Do not require universal impossibility proofs.
3. **Completed engineering implementation** — mandatory acceptance tests and deliverables satisfied.
4. **Unfinished work** — failed tests, unknown initiating faults, promising unexamined leads, missing validation, or unresolved in-scope obstacles; NOT a legitimate final handoff.
5. **Genuine escalation** — missing authority, user-only action, safety/integrity limit, inaccessible essential dependency, or actual execution-resource exhaustion; must be evidenced and specify a narrow request, not used as a euphemism for difficulty.

**Never incentivize Codex to conceal failure or invent a PASS.** If a research claim is falsified, preserve it and finish the negative-result deliverable. If an implementation cannot meet its contract after a serious, bounded and evidenced feasibility investigation, an independently reviewed abandonment decision can complete that *method* while the larger scientific objective remains open. Neither arbitrary test counts nor 'STRONG PARTIAL' constitute closure.

## 2. Work scope and repository discovery

Before editing, inspect the existing `WORKFLOW.md`, applicable `AGENTS.md` and documentation/index/decision conventions in this repo. Check current Git status, distinguish already-uncommitted changes from this task, and preserve all existing standing orders. Locate and cross-reference the established policies covering Codex briefs, review patches, disk protection, experiment integrity, permissions, operator-controlled live tests, archival evidence and version pinning. Prefer a concise controlling section in `WORKFLOW.md` plus a dedicated durable protocol document; avoid conflicting copies of rules. Preserve the established convention for review artifacts in `.local-work/diffs/` including `-complete.diff` and `-task-only.diff`.

This is a **workflow implementation**, not an experiment. Do not modify game binaries, saves, observers, reverse-engineering tools or scientific findings. No Starfield launch, debugger attachment, Vortex/SFSE deployment, online publication, staging, commit or push. Do not initiate the proposed trial on extractors or any other scientific domain.

## 3. Required policy: completion contracts

Define a reusable, minimal per-assignment completion contract, embedded in every substantive future brief:

- **Task type:** discovery, research hypothesis, deterministic reconstruction, engineering implementation, integration, audit, or documentation.
- **Question / deliverable:** what concrete claim, model, code or artifact will exist when the work is done.
- **Scope and bounds:** authorized investigations and interventions, prohibited operations, protected inputs, external/live permission gates.
- **Acceptance criteria:** observable criteria with evidence types, including independent oracle validation where the task actually requires it; distinguish mandatory from optional.
- **Negative-result criteria:** what evidence would *complete* an unsuccessful hypothesis, as distinct from simply encountering an obstacle.
- **Continuation authority:** Codex may investigate, fix, retest and refactor within the original approved scope without asking the maintainer for another brief every time a test fails.
- **Exit and escalation conditions:** exact non-negotiable safety/authority constraints; evidence and request for any escalation.
- **Review artifacts and disposition:** acceptance matrix, evidence ledger, diff, statuses and reviewer decision.

Use a compact template/checklist, not a mandatory sprawling form for trivial work. Keep evidentiary standards proportional to the task and risks; do not invent universal case quotas or demand proof of universal impossibility for a scoped negative result. A completion contract is frozen for acceptance purposes unless the maintainer approves a material change; Codex may not redefine criteria retroactively to match its output.

## 4. Required policy: implementer ownership and stopping discipline

Codify the principle **'a newly discovered obstacle is work, not a handoff.'** The implementer must continue through in-scope failures: determine cause, pursue technically plausible branches, implement warranted corrections, rerun relevant regression controls, preserve counterexamples and produce an outcome meeting the completion contract. This includes diagnostics and requalification; those are **part of the original assignment**, not automatically separately commissioned tasks.

Intermediate checkpoints are encouraged for durability (notes, source control where explicitly authorized, raw evidence, interim test ledgers); they do not become final returns merely because they are well documented. Reject '5 of 6 tests pass' as engineering completion when all six are mandatory. Similarly reject 'not observed yet' as a scientific negative finding unless the controlled absence itself meets an explicitly defined negative-result criterion.

Provide a clear and honest path for **genuine blockers**: safety limits, protected file integrity, inability to access necessary external resources, user-only gameplay actions, absent approvals, and real tool/session/context resource limits. On these conditions halt the prohibited action; preserve state/evidence; describe precisely what is blocked and what minimal authorization or input is required. Never attempt unsafe work to satisfy a 'no unfinished results' rule. Do not falsely claim asynchronous/background continuation across sessions; within authorized execution opportunities, work must actually be performed before presenting a result.

## 5. Independent pre-handoff review and mandatory rework

Establish **Implementer**, **Independent Reviewer**, and **Maintainer** roles with explicit powers:

- Implementer owns investigation, implementation, testing, artifacts and evidence, including remediating defects identified by the reviewer.
- Reviewer inspects the *original contract and primary evidence* (tests/logs/diff/working tree), not only the implementer's narrative; challenges premature stop, untested claims, excluded failed cases, shifted criteria and unjustified abandonment. Reviewer is principally read-only and must not silently alter the implementation under review.
- Maintainer retains authority for scope expansion, live experiments, destructive actions, external disclosure, irreversible changes, approvals and changes to acceptance criteria.

Reviewer decisions are strictly **ACCEPT**, **REWORK**, or **ESCALATE**, each supported by contract-by-contract reasons and evidence references. **REWORK returns the same assignment to the implementer**; the implementer must resolve and resubmit without requesting a new user brief. **ESCALATE** is appropriate only where specific authority or a genuinely terminal, evidenced blocker is needed. A proposed method abandonment must be adversarially reviewed, identifying actual alternatives explored, observed failures, remaining plausible branches and cost/safety justification; it must not require universal proof that all conceivable techniques are impossible.

### Verify actual multi-agent support rather than assuming it

Inspect the available Codex environment/CLI capabilities and repository-specific instructions for independently spawned agent execution, worktrees, access boundaries, reviewer invocation and return-to-implementer iteration. Document **what was actually verified**, including command/version or configuration evidence where appropriate. Never invent agent features or claim an automated multi-agent loop merely because a Markdown policy describes one.

- **If supported:** create a concise, usable reviewer instruction document/agent profile and a practical invocation/handoff procedure. Keep reviewer read-only or isolated as supported, and explicitly prevent a reviewer from accepting its own changes. Validate the mechanics with a harmless documentation-only dry run, with no game/process operations. Do not allow autonomous staging/commit/push.
- **If not supported or uncertain:** document the limitation and deliver a **manual two-pass fallback** in which a separately initiated reviewer session audits the same contract/evidence and issues ACCEPT/REWORK/ESCALATE; provide exact inputs and the rework handoff. Do not claim this substitutes for automatic orchestration. This should not block implementing the durable policies.

Do not add speculative dependencies, install third-party extensions or change global Codex settings without authorization.

## 6. Mandatory completion accounting

Every substantial review return must supply a succinct **acceptance matrix** with each original mandatory criterion marked **PASS / FAIL / NOT TESTED**, evidence link/path, and a one-line explanation. Include all regressions and counterexamples, not just the latest successful rerun. Separately report:

- Scientific finding (including negative result), **evidence coverage** and open scientific unknowns.
- Instrumentation/implementation integrity and qualification.
- Target/application survival and restoration where applicable.
- Authority/safety compliance.
- Final reviewer decision (or explicitly **NOT REVIEWED** if a reviewer could not be run).

Set the overall outcome from the *mandatory criteria*, not from prose optimism. A missing reviewer result cannot be silently labelled accepted if review is a contract requirement. Preserve evidence provenance, source versions/hashes, and clear labels for measured versus inferred claims. Support durable checkpoints with distinction from handoff. Keep the existing review-diff packaging convention and verify completeness, including untracked text.

## 7. Proportional verification and method-selection discipline

Introduce an early feasibility/verification-burden check: enumerate viable routes and principal intervention risks before large tool-building, favour smaller or noninvasive methods when they answer the research question, and reassess whether infrastructure has displaced the scientific aim. Do not lower hard safeguards or fabricate pass criteria. Do not add endless new acceptance gates without a specific new risk and maintainer authorization of material changes. A narrowly and defensibly falsified hypothesis is a success for the research process, not a reason to keep testing indefinitely.

The external-debugger history may be used as a short *retrospective example*, accurately distinguished: its final independently supportable outcome was abandonment of that acquisition approach, not falsification of the underlying outpost position model. Do not reopen debugger engineering in this assignment.

## 8. Deliverables

1. Updated `WORKFLOW.md`, clearly integrating the standing orders without clobbering existing policy.
2. A durable supporting **Research Execution and Completion Protocol** (use the repository's document naming and indexes), including roles, statuses, halt/escalation examples, reviewer checklist and a concise completion-contract template.
3. Verified, implementable reviewer procedure, automated only to the extent genuinely supported; otherwise an honest manual fallback. Include a harmless dry-run result if practical within the environment.
4. A worked example showing how a failed required test triggers **REWORK**, whereas a properly tested negative hypothesis can be **ACCEPT**. Include at least one example of a genuine safety/authority ESCALATE.
5. Applicable links/index/decision/state changes in the repository's documentation scheme, recording provenance and any capability limits.
6. Task-only and complete review diffs under `.local-work/diffs/`, status snapshot, changed-file and exclusion inventories, patch completeness/whitespace/link checks, and an acceptance matrix for **this workflow task**. No staging/commit/push.
7. A **Step-2 trial recommendation only**: propose a contained, existing-data Starfield research task (e.g., extractor/resource association in controlled saves) with an example contract and how the reviewer loop would operate. **Do not conduct the trial.**

## 9. Acceptance requirements for this task

The task is **COMPLETE — PASS** only when all required policy/documentation artifacts, capability assessment and reviewer fallback/invocation procedure, integration links, dry-run evidence where feasible, and review diffs/checks are produced and internally consistent. The implementer must correct in-scope errors before returning. A documentation-only dry-run is not proof that future research will automatically succeed.

If actual agent automation is unavailable, that is *not* a task failure: deliver the verified manual two-pass procedure. If no independent reviewer invocation can be executed within the current authorization/environment, disclose that limitation and mark the review result **NOT REVIEWED** rather than self-certifying; provide a ready-to-run reviewer handoff. The maintainer can then review the workflow change before the separate step-2 trial.

No incomplete implementation, invented reviewer operation, retroactively weakened success criteria, or task-splitting into fresh user briefs. The only early escalation is a documented genuine permissions, safety, tool access or resource blocker. When presenting the result, distinguish **policy implemented** from **policy effectiveness not yet demonstrated**; the latter is what step 2 will test.
