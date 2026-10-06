# Decision Register

Record user decisions, rationale, scope, and supersession. A decision to investigate is not automatically permission to deploy, copy outside code, disclose results, or integrate changes. Use a new entry for changed decisions; preserve the earlier record.

The following decisions were established in the setup conversation and recorded here on **2026-10-01**. The recording date is not a claim that every earlier discussion occurred on that date.

| ID | Decision | Scope / rationale |
|---|---|---|
| SOR-D-0001 | Independent research-first project | Complete and validate the agreed research before publication and downstream product decisions. |
| SOR-D-0002 | Broaden save research to live outpost systems and persistence | Runtime knowledge has independent value for future mods; investigations may move between both. Supersedes the save-only objective. |
| SOR-D-0003 | Name `starfield-outpost-research` | One repository; subsystem-oriented documentation with connected runtime/persistence views. |
| SOR-D-0004 | Private initially; publish under `GPL-3.0-or-later` | Retains original licence choice. No visibility change or publication until authorized after review. |
| SOR-D-0005 | Third-party approval and credit rules | No fork/PR without prior discussion and approval; no code reuse without documented permission and user approval; explicit credit; respect licensing in letter and spirit. |
| SOR-D-0006 | Direct scaffold ZIP, not initial Codex brief | Use the supplied reference-handle scaffold as a structural reference; do not import its established findings/environment. |
| SOR-D-0007 | Durable briefs and critical reviews for later work | Downloadable implementation/audit Markdown; short corrections may be inline but accepted changes must be recorded. |

## Recording future action approvals

### SOR-D-0008 — Bounded crash-tolerant captures

Accepted 2026-10-06 by the user's instruction to execute section 3 of the [initial reconnaissance brief](implementation-briefs/CODEX_RESEARCH_BRIEF_initial_outpost_system_reconnaissance.md). Future separately authorized traces may prioritize complete, high-information evidence over process survival. All scope, finite bounds, mutation, save protection, flushing, exit/recovery and corruption-stop requirements in [AGENTS.md](../AGENTS.md) remain mandatory. No live capture is authorized by this decision or reconnaissance.

### SOR-D-0009 — Execute initial static reconnaissance

User instruction dated 2026-10-06 authorizes the attached brief, read-only local/public inspection, project documentation and a small original xEdit extraction script when needed. The user additionally authorizes placing a copy in xEdit's `Edit Scripts/` directory and requesting a user-operated run if headless/alternative ESM inspection is unavailable. No plugin/save mutations, live game/debugger run, Ghidra analysis edits, third-party code reuse, staging, commits, pushes or external contribution. Stop after reconnaissance and propose commit messages; integration remains subject to critical review.

Each action decision must identify the request, date, user approval evidence, exact scope, affected workspace/repository/version, permitted and prohibited operations, linked source/permission IDs, duration or stop boundary, and whether it supersedes a prior decision.

Do not record an agent's recommendation as a user decision. A permission register may link here but must keep rights-holder permission distinct from user authorization.

### SOR-D-0010 — Execute SOR-EXP-0002 Gate A only

On 2026-10-06 the user explicitly instructed Codex to follow the [SOR-EXP-0002 brief](implementation-briefs/CODEX_RESEARCH_BRIEF_SOR-EXP-0002_outpost_membership_reload_location.md), return suggested commit messages, and not commit or push. This authorizes the brief's bounded offline preparation, save integrity registration, original tooling and read-only static work. It supersedes SOR-D-0009's stop boundary only for this Gate A scope. No SDK/code-reuse acceptance, deployment, launch/load, console, debugger attach, new saves, post-live analysis, stage/commit/push or external disclosure. Stop at the review package; Gate B needs separate approval after review. The initial partial preparation and subsequent original implementation are reported in [SOR-EXP-0002](experiments/SOR-EXP-0002-outpost-membership-reload-location.md); this record does not accept an agent's proposed alternative implementation.

### SOR-D-0011 — Continue Gate A; external-mod/reference clarification

2026-10-06: user reports successful SFSE observer builds in the sibling reference-handle project, permits use of mods such as Address Library while respecting code boundaries, and confirms CommonLibSF reference use with permissions/credit. User explicitly requests continuing the brief. The earlier broad stop was premature: unresolved implementation questions are to be investigated offline, not automatically classified as permission blockers. Existing brief prohibition on copying/adapting sibling observer code remains; consultation is a credited lead, not live validation of this package. Gate B and Git/publication boundaries unchanged. SOR-P-0001 separately records the subsequent explicit approval of the pinned MIT SFSE interface header.

### SOR-D-0012 — Primary Gate B authorization

2026-10-06: after the reviewed anomaly/Vortex correction, the user stated: "we're now good for Gate B: primary live A0–A2R experiments are authorized. Please proceed when ready. Do not commit or push changes". This authorizes the six primary checkpoints, including A0C/A1C controls, ordinary menu saves, A2 reload, normal exit and subsequent protected archival under the [operator card](experiments/EXP0002-operator-card.md). Vortex remains the exclusive deployment owner and the user performs deployment/retirement and ordinary game UI. The user subsequently confirmed deployment had not yet occurred and that they would install through Vortex. No debugger trace, console, forced termination, extra construction, save modification, staging, commit, push or external disclosure is authorized. Existing bounds and stop conditions remain in force. This supersedes SOR-D-0010's Gate-A-only boundary for the primary experiment; it does not assert that live execution has occurred.

Preflight found a CRLF configuration defect in review12's ZIP before launch. A separate corrected ZIP removes only the CR byte, retaining the exact reviewed DLL and all other payload bytes. The changed package/configuration identities have been surfaced under brief section 23; user confirmation and deployed-file verification remain pending. Exact hashes, preflight and the operator handoff are in the [Gate B run record](experiments/EXP0002-gate-b-run.md).

### SOR-D-0013 — Fresh primary run with review14-settled

2026-10-06: after the synchronization correction review, the user explicitly approved a fresh A0–A2R primary run using review14-settled, confirmed user-managed deployment through Vortex profile Starfield - SFSE, and reported SFSE as the only other enabled mod with the game not launched. This authorizes the six primary checkpoints and the existing ordinary UI save/reload/normal-exit/archive sequence with operator-settled attestations and fresh acquisition. ZIP SHA-256 `970dce992d665eeda0fcf8fcdbcb4d363016756e02e2e3a9ca4c7eeed4a37ff4`; DLL `9a1636adacdcd0967e7873fcdbc161fed04876d3c368f9e37735f707e9e191ed`. No debugger trace, console, extra construction, automatic retry, forced termination, staging, commit, push or external disclosure. The failed first session remains preserved. Current progress: [review14 run record](experiments/EXP0002-review14-run.md).
