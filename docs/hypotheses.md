# Hypotheses and Open Questions

The following starting questions remain open. Reconnaissance now supplies the discriminating hypotheses below; they are not established runtime explanations.

| ID | Question | Status |
|---|---|---|
| SOR-Q-0001 | What constitutes an outpost and how can all its objects and relationships be identified live? | OPEN |
| SOR-Q-0002 | Which outpost state is persisted, definition-derived, reconstructed, transient, or mixed? | OPEN |
| SOR-Q-0003 | How do runtime and serialized identities map across saves and reloads? | OPEN |
| SOR-Q-0004 | How do production, storage, and transport behave under different time/loading conditions? | OPEN |
| SOR-Q-0005 | Which operations/interfaces can future mods use, under what constraints and demonstrated guarantees? | OPEN |

For a proposed `SOR-H-` record include its origin/source, exact claim, supporting observations, alternative explanations, a discriminating test and falsification criterion, build scope, confidence, and linked experiments. Do not seed hypotheses solely by treating earlier chat speculation as established mechanics. Retain rejected/superseded models and their counterexamples.

## SOR-H-0001 — A keyed reference relation underlies exposed workshop membership

PROVISIONAL; SOR-ENV-0001. SOR-F-0003's callback delegates through a global-keyed lookup; local flora/actor scripts consume GetWorkshop. Prediction: an ordinary placed storage object returns the beacon/workshop relation at a settled checkpoint, and a non-member control does not. Alternative: intermediate owner, location-derived/cache association, or a subset relation that is not authoritative. SOR-EXP-0002 compares both directions where possible and repeats after reload/independent placement. A different stable owner or disagreement with membership enumeration narrows/falsifies the simple direct-beacon model. No runtime test yet.

## SOR-H-0002 — Cargo animation is reconstructed from state distinct from visible 3D

PROVISIONAL runtime model; source-level OnLoad behavior proven by SOR-F-0002. Prediction: a reload reapplies animation consistent with the ActorValue observed before unloading. Alternatives: value is recomputed by another path, stale property or changed link initialization overwrites it. Future paired marker value/event/animation observations and save comparison can distinguish these. No stored ActorValue claim. SOR-S-0104; SOR-ENV-0001; not part of the first minimal membership tranche.
