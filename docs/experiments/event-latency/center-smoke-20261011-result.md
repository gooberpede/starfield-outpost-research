# First center-only attempt — adapter failure before readiness

2026-10-11 Australia/Sydney; SOR-EXP-0026, SOR-D-0046. Session identifier
`center-smoke-20261011-022037-UTC`. **Live preflight passed, but adapter0.1.3
exited before READY or evidence-directory creation. No acquisition or successful
live qualification is claimed.** Independent postflight while Starfield survived
confirmed exact original code at both sites and no debugger. The user then
reported normal game exit and completed Steam sync; subsequent protected-input
checks pass. Root cause remains UNKNOWN. No retry occurred.

## Authorization and sequence

The user approved [the run card](center-only-live-run-card.md), explicitly accepted
an unrecovered debugger stall while Starfield remained running, and retained
Steam launch/load/operator actions. The accepted card authorized the bounded
center-only preflight/attachment attempt; no grid, forced recovery, save/config
mutation, staging, commit or push. Approval and exact operator reports are retained
locally in the [authorization](../../../.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/authorization.json)
and [operator-ready receipt](../../../.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/operator-ready.json).

Operator reported ordinary Steam with no loader launch options, exact Save25 at
SOR-003/Kreet, no missing-content warning, build mode closed and input held.
These are operator observations, not native semantic validation. No build-open
cue was issued and no acquisition action was requested after the failure.

| Observation | Direct result |
|---|---|
| Target PID / creation FILETIME | 17100 / 134361588499198318 |
| Image | Exact installed Starfield.exe path and pinned game SHA from the card |
| Discovered base | `0x7FF6A8CB0000` (runtime VA domain, this process only) |
| Entry VA / RVA | `0x7FF6A9BFAB80` / `0xF4AB80` |
| Common exit VA / RVA | `0x7FF6A9BFAC44` / `0xF4AC44` |
| Original 32-byte site guards | Both exact expected SHA-256, before and immediately before attempt |
| Debugger/modules | No debugger; no SFSE/observer module; inventory retained |
| Attachment launch | 2026-10-11T02:23:04.1284781Z; adapter PID8556, `--center-only` |
| Adapter exit | 2026-10-11T02:23:04.4462634Z; signed -1073740791 / `0xC0000409` |
| stdout / stderr | Empty; no caught-exception diagnostic |
| Session root / READY / WAL | None created |
| Independent postflight | PASS at receipt timestamp 02:23:16.183115Z; same live target creation/path/base, original windows, debugger absent |
| Operator exit | User reported game exited and Steam sync complete; later process inventory returned no Starfield |
| Post-exit integrity | PASS: approved game/tool/ZIP, four original/archive save files and four frozen files; both drives above40-billion bytes |

Loaded module paths were reviewed as installed game/Steam, Windows and NVIDIA
components, with no identified conflicting instrumentation. This is a scoped
inventory assessment, not an exhaustive third-party compatibility claim. Content
list matched the prelaunch receipt. Full 32-byte reads/module inventory stay in
private receipts; the prior card retains expected window hashes.

## Interpretation and limits

The adapter's source creates the evidence root/session WAL before calling
DebugActiveProcess. Absence of that root is consistent with failure before that
call, but this run contains no durable adapter event trace proving the exact
faulting instruction or execution boundary. Describe this as an **attachment
attempt without confirmed attachment/readiness**, not a completed live capture
or proven debugger-induced game failure. Do not assign a specific cause from the
exit status alone. A bounded Application-log query returned no matching adapter
1000/1001 entry at the time queried; this is not proof that no Windows report exists.

The postflight is direct evidence that the same surviving process had original
site bytes and no debugger at that check. It does not establish that bytes never
changed transiently, nor independently audit every thread's TF/suspend count.
There was no terminal/retirement WAL to verify, no native center sample, no
measurable breakpoint latency and no scientific comparison. Original disposable
qualification is retained but cannot substitute for this failed live readiness.

Approved adapter/source/tool/ZIP are unchanged. Preserve the failure and suspend
further attachment until the startup failure is investigated and any correction
is separately qualified/reviewed. No automatic second attempt or scope expansion.

## Local evidence and review

All private receipts are beneath
`.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/`: offline
before/live/failure/post-exit checks, both preflight receipts, attachment/exit JSON,
empty stdout/stderr, independent postflight, operator/authorization and state.
There is no WAL/raw capture. These receipts and proprietary/save/config inputs
remain local and excluded from patches.

- [Independent postflight](../../../.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/process-after-adapter-failure.json).
- [Post-exit protected-input check](../../../.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/offline-after-game-exit.json).
- [Task-only result patch](../../../.local-work/diffs/event-center-smoke-result-task-only.diff).
- [Complete HEAD patch including prior work](../../../.local-work/diffs/event-center-smoke-result-complete.diff).
- [File/hash/exclusion/check manifest](../../../.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/review-result/review.json).

Documentation-only result supplement; no implementation changes or new dependency.
No termination, exception suppression, game/config/save/database edits, deployment,
external disclosure, staging, commit or push. Await review; no live finding is
promoted. Suggested subject: `research: record failed center-only readiness attempt`.
