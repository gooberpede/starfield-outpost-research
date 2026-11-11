# Event-associated position oracle and build-mode investigation

2026-10-11 Australia/Sydney. SOR-EXP-0024 / SOR-EV-0032 / SOR-D-0043.
ANALYZED; authored conclusions/design **REVIEW-REQUIRED**, native exports and
raw/private evidence **LOCAL-ONLY**. [Authorized brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_event_associated_oracle_and_build_mode_failure.md`).

**Best-supported result:** the four-float observation is shared planetary
`BGSPlanet::ProcGen` state, with a conditional placement-state publisher and a
reset that clears radius while preserving XYZ. It is not an always-current,
per-workshop result. This supplies a concrete explanation for the *possibility*
of Phase 1 retention/zero radius; the actual sequence of publisher/reset/disable
events during those snapshots was not recorded. Confidence is high in the
scoped static contract, not in a retrospective event diagnosis.

The zero-compensation branch of `140f4ab80` still writes the caller's XYZ output.
No compensation-dependent skip of shared publication exists in the traced
publisher. An unmoved-beacon fast path therefore does **not** explain the stale
tuple by itself. Save25/002 retained 003, whereas Save26/002 refreshed to 002:
both outcomes remain controls, not a selected-away contradiction.

**Recommended next oracle:** capture the natural entry/return of the center
helper with its actual reference, output pointer, caller and frame, rather than
read the shared tuple later. Separately capture the terrain callback's native
grid result if naturally reached. The [ranked acquisition design](event-oracle/acquisition-design.md)
defines implementation and qualification gates; it authorizes no implementation
or live run. Center validation and planetary-grid equivalence remain distinct.

The spinner has an explicit UI data-model channel separate from the ProcGen
tuple. Native readiness/state paths and a discriminating failure-capture plan
are in the [preview investigation](event-oracle/preview-state.md). No failing
episode was captured in Phase 1. Zero in this buffer is already observed during
reported functional building, so it is not sufficient evidence of a placement
failure or a zero effective boundary. The intermittent bug's cause and any
shared upstream cause remain unproven.

## Coverage and evidence

This continuation follows the typed owner, allocation/destruction, full and
partial writes, activation, bounds callback, state dispatch, center helper's
direct callers, radius definition/default, terrain oracle and preview data/state
paths. It does not claim absence of every possible aliased writer in the game,
complete permissions logic, live hook safety, arbitrary-angle quantization or
continuous geographical coordinates. [Terminal dependency ledger](event-oracle/dependency-ledger.md)
distinguishes closed static edges from specifically missing runtime evidence.

- [Native ownership/writer/consumer map](event-oracle/native-map.md).
- [Ranked oracle design and frozen comparison rules](event-oracle/acquisition-design.md).
- [Preview, readiness and falsifiable hypotheses](event-oracle/preview-state.md).
- [Prior-art access and attribution ledger](event-oracle/prior-art.md).
- [Review package, actual checks and limitations](event-oracle/review.md).

Installed retail 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Every native address in this package is static VA, preferred base `140000000`;
RVA = VA minus that base. None is an observed runtime pointer. Existing
SOR-ENV-0002 and SOR-S-0127 native provenance apply. Ghidra 12.1.2/JDK 21.0.12.8
read existing analysis using `-readOnly -noanalysis`; no types/symbols/comments
or game bytes were changed. Exports `event-oracle-01` onward remain ignored.
Exact identities and commands are retained in the local review manifest.

Existing [Phase 1 results](engine-oracle/Phase1-results.md) supply 16 checkpoints;
the [initial session](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/beacon-observer-initial-live-results.md`) supplies 9.
Fresh integrity audit verified all 14,645 raw sections and four protected
Save25/26 original/archive paths. Integrity establishes preservation and journal
completeness, not semantics or atomicity. No new native runtime observation was
made; frozen predictions/protocol/checkpoint CSV remain unchanged.

## Evidence-state proposals

SOR-F-0029 proposes scoped STRONG static ownership/invalidation semantics;
SOR-FN-0056/0057 record lifecycle and preview acquisition paths; SOR-ST-0027
records transient UI state. These supplement SOR-FN-0054/0055 and SOR-ST-0026,
preserving their earlier wording and the failed freshness qualification.
No saved-layout classification, live equivalence, integration safety or bug
finding is promoted. Critical review is still required. No commit, push,
publication, deployment, game launch, debugger attachment or save modification.
