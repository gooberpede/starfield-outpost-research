# <SOR-EXP-ID> — <bounded question>

**Status:** PLANNED; execution not authorized by this template.

**Date/time/timezone:** UNKNOWN

**Governing brief / user action approval:** NONE

**Subsystem / linked question and hypothesis IDs:** <IDs>

For a completed substantive semantic report, begin with the compact [answer-first elements](../EVIDENCE_STANDARD.md#evidence-evaluation-and-reporting): question, best-supported answer, confidence, coverage, decisive evidence, concrete limitations and next test if needed. Keep this planned template's execution status explicit.

## Question, scope, and predicted distinction

State the question; what is in/out of scope; prior findings and outside sources; alternative models; expected distinguishing observations; success and falsification criteria. A question need not already have a preferred hypothesis.

## Permissions and permitted operations

List source/permission IDs, exact tools/versions and allowed use. State whether actions include game launch, attach/pause/breakpoints, instrumentation/deployment, Ghidra changes, gameplay actions, save creation, or file changes. Record effects on timing/state, prerequisites, risk, stop criteria, backup, cleanup, and who performs each step. Missing approval blocks that action.

## Baseline, inputs, controls

Record environment/build/tool/script IDs and hashes; game/save format versions as observed; plugin/load order; neutral sample IDs and immutable original hashes; runtime/loading/time conditions; no-action controls and comparison cases; independent ground truth. Unknowns stay UNKNOWN.

## Ordered procedure

Write reproducible steps with finite question/action scope, output locations, health checks, stop conditions and cleanup. Expected output sizes and capture windows are planning estimates, not automatic cutoffs. Apply [scientific experiment continuation and health](../../WORKFLOW.md#scientific-experiment-continuation-and-health): time, volume, operator delay or routine cadence overrun alone must not stop a healthy run. Preserve both-drive 40,000,000,000-byte caller-available guards and all identity, instruction, protected-input, evidence-integrity, worker-failure and operator STOP protections. Any essential additional hard limit requires concrete justification and maintainer approval before the run. Warn and continue safely during delay; consult before terminating solely for delay. Record violated approved criteria honestly. Protect active/original saves. Do not claim an unexecuted procedure was run.

## Actual execution and observations

Record actual timestamps, operator, deviations, errors, negative outcomes, control behaviour, and raw observations. Link precise evidence IDs/locations and hashes. Separate runtime observations from save observations and from cross-domain mappings.

## Interpretation and validation

Describe what each observation supports and does not support; confidence/basis; inferred semantics; dependencies; alternative explanations; counterexamples; repeat/holdout coverage; and unresolved identity/offset domains. Distinguish proposed mod integration from validated behaviour.

## Handoff and durable updates

State result status, completed/not-run checks, cleanup/deployment state, remaining blockers, affected finding/state/function/subsystem records, source credits, publication classifications, and next bounded question. Attach a complete review package, including new files. Do not stage/commit/push without explicit instruction.
