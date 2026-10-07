# EXP0002A — Steam launch correction and one-request adapter

User instruction, 2026-10-07 Australia/Sydney; SOR-D-0016. This retains the current request and supersedes the Stage-B launch requirements in earlier briefs, not their historical observations.

1. Prospective Stage B uses ordinary Steam launch without SFSE.
2. Remove Vortex/SFSE-profile requirements from the current operator card and capture plan.
3. Preflight explicitly verifies SFSE and SorExp0002 are not loaded.
4. Vortex/SFSE deployment remains for Stage C only, when observer0.1.0 is eventually built and separately authorized.
5. Remove or clearly mark obsolete profile flags in disabled historical x64dbg tooling.
6. Implement the reviewed one-request Win32 hardware/RF adapter.
7. Run only bounded fresh disposable qualification for late attach, delayed operator trigger, one hit, no-hit timeout, new-thread handling, retirement/cleanup and delayed target health.
8. Return adapter and qualification diffs for review.
9. Do not launch Starfield.
10. Do not commit.

The [reviewed design](../audits/exp0002a-debugger-correction.md) and [one-site plan](../../debugger/exp0002a/next_capture_plan.json) retain their capture/ownership/cleanup bounds. Maintainer reuse follows SOR-P-0002 with exact provenance. No installation, game deployment/attachment, save modification, plugin-triggered saving, staging, push or external disclosure. A failed disposable qualification remains a failure; do not substitute register restoration or process presence for healthy progress. Preserve failed evidence and return for review.

Deliverables: native adapter and bounded fixture/runner/build sources; current operator card/plan; provenance; actual results and limits; task-specific and complete working-tree diffs including new files; Git status; suggested commit message only.
