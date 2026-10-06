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
