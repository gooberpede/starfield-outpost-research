# Hypotheses and Open Questions

## SOR-H-0005 — Beacon collection membership may depend on object/relationship participation

PROVISIONAL / SAVE, SOR-ST-0015, SOR-F-0012, SOR-EV-0012. [Mature validation](experiments/mature-save-outpost-validation.md) finds 17 named mature members matching JSON, but the same grammar's beacon collection is empty in S1/S1C/S2/S2C and S7/S7C despite retained beacon windows. Inclusion begins at S3, before the first controlled output link, and ends at S7's extractor deletion/link cleanup. A universal active-beacon registry is contradicted; relationship participation, a production-related subset, cache or another subsystem registration remain alternatives. Do not infer an engine list owner, deletion state or load authority from membership.

Discriminator, proposed only: independently identified beacon/storage/producer candidates with controlled additions/removals and no-action saves could locate the membership trigger. A beacon-only case reliably represented as a member, or an included unrelated beacon without qualifying relationships, would weaken a simple participation rule; mixed transitions may require a different subset model. Cargo-only examples could separate registration sources. No new experiment is authorized by this record; semantic review first. Publication REVIEW-REQUIRED.

## SOR-H-0004 — Save-position candidates may share or relate to the live local frame

PROVISIONAL; SOR-ST-0013, SOR-EV-0004 (EXP0002 A0/A0C) and SOR-EV-0009 (manual corpus S0–S7C). The [verified numerical comparison](experiments/manual-save-corpus-S0-S7C.md#offline-comparison-with-earlier-exp0002-live-player-coordinates) finds identical recorded live player tuples and distances 6.830539 / 8.997486 / 26.000118 to beacon/pre-S6 solar/post-S6 solar candidates. These modest numerical separations are compatible with placement at the reported same site and strengthen a same or closely related local Cartesian frame interpretation, without validating it. Prior capture reports game1.16.244.0; save headers report the same version, but actual originating save-session executable identity is not independently acquired.

Alternatives: coincidental numerical proximity, translated/scaled frame, different reference or child-object ownership, or cross-session frame differences. Unknown: origin, units, axis semantics, ownership, planetary/body-relative interpretation and latitude/longitude conversion. The earlier live captures are non-atomic; numerical agreement does not establish an authoritative transform, unit scale or matched runtime/save identity.

Future discriminator, recommendation only: paired, independently identified runtime/save positions at matched checkpoints, including one controlled displacement, should exhibit a consistent relation. Inconsistent displacements or unexplained varying offsets would weaken/falsify the simple shared-frame interpretation; proximity alone cannot select between frames. No such observation is authorized or implemented by this correction. The recommended next live experiment remains output-link present→removed→recreated, predicting motif present→absent→present while principal objects remain unchanged; it still requires separate authorization.

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

## SOR-H-0003 — DR0-associated single-step failure escaped adapter capture

PROVISIONAL causal model, Starfield1.16.244.0 / SOR-ENV-0003 only. [SOR-EV-0007](experiments/evidence/exp0002a-dumps/README.md) decisively places both failed runs at REQUEST_ENTRY with STATUS_SINGLE_STEP, DR0=site, DR7=1, valid saved DR6=0, identical bounded stacks and matching WER signature. Neither adapter logged the research exception. S0/S1 passed; broad and single-thread DR0 failed. High confidence in the observed shared signature, unresolved confidence in why event delivery/capture failed. Do not infer the hardware's first-chance DR6 from a later saved context.

Alternatives: debugger association/delivery failure; exception/context transformation or other in-process handling; selected-thread suspend/context intervention; software-raised single-step. The recommended next discriminating control is S1.5: same selected-thread suspend/read/resume lifecycle without DR0/DR7 writes, separately reviewed and not authorized here. A matching failure with clean DR registers weakens a DR-write-specific explanation; a pass strengthens it without uniquely proving the delivery defect. No thread widening or Stage C. Stronger claim that REQUEST_ENTRY was never reached is contradicted by SOR-F-0008; strongest claim that owned_hit's DR6 predicate alone caused the loss is unproven because no exception event was logged.

SOR-D-0021 priority update: S1.5 remains a scientifically valid future discriminator but is not to run now and is no longer the preferred next action. One final software-breakpoint capture may cheaply advance the contract. Otherwise defer SOR-H-0003's debugger-delivery investigation; it does not block live outpost observation or manual differential save research.

## SOR-H-0004 follow-up — historical name-adjacent tuples, 2026-10-09

[SOR-EXP-0007](experiments/historical-save-inventory-triage.md) reproduces the S1 beacon tuple at name/animation-index-subunit end +5 and records 36 finite float32 triples in four historical samples. Seventeen additional name links use an exploratory animation-predecessor fallback after inventory freeze, without changing inventory classifications. PROVISIONAL local/related-coordinate interpretation only; units, owning reference/child, frame, body association, authoritative restore and lat/long conversion UNKNOWN. Mutable/default-looking body names are leads, not decoded planet identifiers. Alternative: unrelated variable subunits or child transforms. A controlled beacon move/return plus matched runtime/save and planet-map observations could falsify/qualify the model, but no new experiment is authorized. Existing SOR-H-0004 evidence/limits remain unchanged.
