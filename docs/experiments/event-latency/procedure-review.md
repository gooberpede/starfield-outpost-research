# Center-only procedure preparation — review return

2026-10-11 Australia/Sydney, SOR-D-0046. **External adapter 0.1.3 is approved;
the live procedure is prepared for review, not executed.**

- [Exact run card](center-only-live-run-card.md).
- [Retained preparation brief](../../implementation-briefs/CODEX_BRIEF_SOR_center_only_live_procedure.md).
- [Original read-only operational checker](../../../debugger/event-smoke/checks.py).
- [Task-only patch](../../../.local-work/diffs/event-center-smoke-procedure-task-only.diff).
- [Complete HEAD patch, including prior uncommitted text](../../../.local-work/diffs/event-center-smoke-procedure-complete.diff).
- [Status, file/hash/exclusion manifest and verification](../../../.local-work/event-smoke-preparation/review.json).
- [Actual offline check receipt](../../../.local-work/event-smoke-preparation/offline-check.json).

Use ordinary Steam for the proposed first smoke; no SFSE loader or Vortex
deployment. Installed SFSE documentation calls its launcher `sfse_loader.exe`.
Check both launch options and loaded modules; reject SFSE/observer, conflicting
instrumentation or unresolved save/content compatibility. No configuration changes
are silently authorized. Proposed process preflight records PID, creation time,
full image path/hash, live base and both original 32-byte windows. Adapter READY
and valid ready/session WAL records precede the operator's one build-mode cycle.
Independent postflight checks original windows and debugger absence on the same
surviving process. Durable evidence is verified offline without repairing tails.

The card distinguishes zero-hit readiness, useful native acquisition, scientific
association and target survival. It preserves partial evidence and foreign
exceptions, two-site center-only scope, separate grid availability, 40-billion
caller-available-byte guard and exact restoration. STOP is cooperative, including
idle OS break-in. A blocked synchronous writer has no guaranteed rollback
deadline; forced debugger termination is not safe cleanup. Exited targets cannot
provide an independent live restoration check. These limits require acceptance
in the subsequent live authorization or a separately reviewed design change.

Actual checks: checker **offline mode PASS**, including approved game/tool/ZIP,
four original/archive save hashes, four frozen-file hashes, save inventory,
content-list receipt and disk guard. Source syntax and diff/whitespace/local-link
checks pass; both task-only and complete patches pass path inventory, reverse
applicability and forward exact-byte comparison. The manifest records counts and
hashes, approved-source identity and 0.1.2 baseline preservation. No live checker
mode, debugger attachment or game launch was exercised. Earlier six disposable
controls remain the qualification evidence; they were not rerun for this procedure
and do not establish live safety. No new runtime/scientific evidence ID is claimed.

New files: card, this review, retained brief and original operational checker.
Documentation supplements record approval/procedure/provenance in decision/state,
source/credit/provenance, brief index and previous latency card/README. No adapter,
collector, fixture, writer, decoder, inspector or qualified executable changes.
The task-only patch is against the captured starting uncommitted tree; complete
patch also contains the earlier implementation and supplied brief. No deletion or
rename. Raw/binary/save/config/database material stays outside both patches;
local private receipts are explicitly excluded. All outputs remain local.

No third-party code/dependency incorporation, external disclosure, launch/load,
process open/attach, deployment, original-save/config/database modification,
staging, commit or push occurred. The checker only ran its offline path. Approval
of this preparation is not automatic authority for attachment or another run.

Suggested commit subject after review (not committed):

```text
docs: prepare guarded center-only event adapter smoke procedure
```
