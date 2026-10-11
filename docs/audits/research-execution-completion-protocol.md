# Step-1 execution and completion protocol review package

2026-10-11, Australia/Sydney; SOR-D-0049. Documentation implementation only.
[Original frozen contract/brief](../implementation-briefs/CODEX_BRIEF_SOR_research_execution_completion_protocol.md).
The brief's sections 8-9 are this task's acceptance contract; no amendment.

Policy implemented; effectiveness in scientific work is **NOT TESTED**. The
recommended existing-data trial in [the protocol](../RESEARCH_EXECUTION_PROTOCOL.md#step-2-recommendation-only)
has not run. No scientific finding or confidence was changed. Maintainer
integration/publication approval remains separate from independent review.

## Capability assessment and primary receipts

Actual session exposes `collaboration.spawn_agent`, `followup_task`,
`send_message`, `wait_agent` and related management tools. Four concurrent agent
slots are advertised, including root; this task uses only root and one reviewer.
Shared filesystem and inherited tool access are advertised. A read-only reviewer
instruction is not an OS-enforced read-only sandbox. Separate worktree tooling
is exposed but isolation/worktree creation was not exercised or required.
No global agent profile, settings, extension, scheduling or dependency installed.
No CLI automation loop was inferred from CLI availability.

Observed commands: `Get-Command codex, python, git`; exact installed Codex path
`C:/Users/User/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe --version`
returns `codex-cli 0.162.0-alpha.17.2` plus a home-directory/PATH-alias warning.
`git --version` returns `2.53.0.windows.1`; explicit installed Python returns
`3.14.3`. The default WindowsApps `python --version` failed to start; checks use
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe` instead.
These are command observations, not proof of all CLI multi-agent features.
[OpenAI documentation](https://developers.openai.com/api/docs/guides/agents-api/multi-agent)
(SOR-S-0140, read 2026-10-11) supplies general coordination context only; local
invocation evidence controls claims here. No third-party code copied.

Primary local ledger and reproducible packaging/check script:

- [Reviewer returns and dry-run history](../../.local-work/completion-protocol/reviewer-results.md).
- [Frozen dry-run contract](../../.local-work/completion-protocol/dry-run-contract.md),
  [v1 fixture](../../.local-work/completion-protocol/dry-run-v1.md),
  [v2 fixture](../../.local-work/completion-protocol/dry-run-v2.md).
- [Check/export script](../../.local-work/completion-protocol/package.py) and
  [verification, source hashes, inclusion/exclusion inventory](../../.local-work/completion-protocol/verification.json).
- [Final status snapshot](../../.local-work/completion-protocol/status.txt).
- [Task-only patch](../../.local-work/diffs/completion-protocol-task-only.diff) and
  [complete patch](../../.local-work/diffs/completion-protocol-complete.diff).

Script reads Git HEAD/index/status, changed text and linked local documents;
normalizes task-authored documentation to LF (excluding the supplied brief);
writes ignored receipts, patches and disposable document-only replay trees.
Existing installed Python standard library/Git only; no game or analysis-project
effects, staging, commit, push, network or dependency downloads. Replays
apply/reverse patches only in disposable trees; reversing removes newly created
scratch document copies. It never applies/reverses patches on the repository
working tree or deletes source documents. Reruns retain prior replay directories.
Script/inputs/outputs are hashed in the receipt.

## Acceptance matrix (original brief sections 8-9)

| Mandatory criterion | Status | Evidence and explanation |
|---|---|---|
| 1. Integrate WORKFLOW preserving standing orders | PASS | [Controlling section](../../WORKFLOW.md#execution-and-completion-contract); existing policy retained in diff. |
| 2. Durable protocol, roles/statuses, halt examples, checklist/template | PASS | [Protocol](../RESEARCH_EXECUTION_PROTOCOL.md), [template](../templates/completion-contract.md), [reviewer checklist](../reviewers/research-completion-reviewer.md). |
| 3. Verified reviewer procedure/capability and feasible dry run | PASS | Capability observations above; actual fixture/rework returns in local reviewer ledger; manual fallback included. |
| 4. REWORK, negative ACCEPT and authority ESCALATE examples | PASS | [Worked examples](../RESEARCH_EXECUTION_PROTOCOL.md#worked-disposition-examples-illustrative-not-experimental-results); illustrative semantics separate from actual dry run. |
| 5. Links/index/decision/state/provenance integration | PASS | SOR-D-0049, SOR-S-0140, credits, docs/templates/audits/brief indexes and state entry; no semantic promotion. |
| 6. Review diffs/status/inventories/checks/task matrix | PASS | Local artifacts above; verification covers tracked and untracked text, patch inventory/content/applicability, whitespace and changed-document links. |
| 7. Step-2 recommendation and example contract, no execution | PASS | [Recommendation](../RESEARCH_EXECUTION_PROTOCOL.md#step-2-recommendation-only) includes provenance prerequisite, controls, scoped negative closure and reviewer loop. |
| 9. All artifacts internally consistent; fix in-scope errors | PASS | Verification receipt and independent review ledger; packaging failure/correction history preserved below. |

Independent decision and exact reviewed revision are retained in the reviewer
ledger. If no valid result is available, this package is NOT REVIEWED and cannot
be presented as independently accepted. Final implementer outcome is determined
only after the linked checks and reviewer disposition, not by this table alone.

## Coverage, failures, exclusions and disposition

Starting HEAD: `f5ccb3cf18243b52fcc54e3dc9c6fabdfbcea5c7`. Starting status contained
only the supplied untracked brief. It is preserved byte-for-byte, included only
in the complete patch and separately inventoried. Task-only contains all task
authored tracked/new documents. Review exports and fixture/check receipts stay
ignored/local. Other ignored raw saves/binaries/databases/evidence are neither
inspected nor incorporated; no claim of clearing historical ignored material.

Preserved execution failures: default Python alias could not run; explicit
installed Python resolves it. First multi-file patch failed preflight because
the decision heading is `Decision Register`; no partial writes occurred, and
the corrected patch was applied. Dry-run v1 deliberately lacks C2; it must not
be relabelled a PASS after v2. Later check/review corrections are retained in
the local ledger/receipts. These are workflow controls, not scientific evidence.

Scientific result/coverage: no new research; existing scientific unknowns remain.
Implementation integrity: documentation checks and bounded reviewer mechanics;
no claim of universal session availability or guaranteed future research success.
Target survival/restoration: not applicable, no target/game operations.
Authority/safety: documentation and dry-run only; no source-save/config/tool
mutation, stage/commit/push, external contact, upload or publication. No new code
reuse permission needed. External consultation was read-only official docs.

Await maintainer critical review and integration decision. The separate step-2
trial will test policy effectiveness; this assignment does not authorize it.

Suggested commit subject (not committed):

```text
docs: establish research completion contracts and independent rework protocol
```
