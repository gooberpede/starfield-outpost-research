# Outpost Subsystem Research Map

**Vertical reference restoration, 2026-10-13:** [Producer/consumer investigation](../experiments/workshop-z-restoration/report.md) separates persisted initial XYZ, reference frame/registration mask02, actual loaded position writes, selected edge heights and Workshop compensation. Scoped negative reconstruction and [minimal acquisition design](../experiments/workshop-z-restoration/acquisition.md) preserve known XY results; full XYZ remains unvalidated. No new live authority.

**Ship relocation and outpost positioning, 2026-10-13:** [Source-grounded assessment](../experiments/ship-relocation/report.md) separates player commands, marker lookup/reuse/creation, ship-size admission and Workshop rectangle exclusion. Shared native grid relevance is supported; selected/save/Workshop equivalence remains untested. [Future acquisition design](../experiments/ship-relocation/acquisition.md) is a proposal only.



**Landing/reference identity, 2026-10-12:** [Fallback provenance](../experiments/fallback-grid-provenance.md) separates ship landing marker, runtime reference/cell/world IDs, installed base, saved template references and selected Workshop identity. Generic zero-offset agreement remains distinct from persisted site/load linkage and compensated-center equivalence.

**Matching source, 2026-10-12:** [Two-candidate qualification](../experiments/matching-source-qualification.md) links saved ordinary beacons to site/secondary-world origins, reconstructs native source production and preserves runtime remapping limits. Existing-reference selection can bypass Q and reach a separate generic grid CALL. Full composed native position equivalence remains untested; [review/disposition](../experiments/matching-source/review.md).

**Position acquisition, 2026-10-12:** [Native-oracle0.2.0 live attempt02](../experiments/native-oracle/continuation-020-live-attempt-02.md) establishes18 complete natural candidate-query invocations during one approved new Kreet landing interval, with no linked enumeration/callback/native position/grid. Existing-site controls remain zero. Exact pre-enumeration gate, Workshop identity and saved-to-loaded selected-frame equivalence remain open. Operational retirement/removal/protected hashes pass; [independent review](../experiments/native-oracle/continuation-020-live-attempt-02-review.md) and private evidence/patches accompany the scoped diagnostic result.

The [initial reconnaissance map](initial-map.md) now records scoped static evidence and unresolved live/save questions across ten areas. The original agenda below remains open; no runtime or save behavior is established by static mapping.

| Area | Initial questions | Runtime / persistence / validation status |
|---|---|---|
| Identity, location, membership | What constitutes an outpost? How are all outposts and constituent objects enumerated, including unloaded ones? Which relationships survive reload? | All OPEN |
| Construction and lifecycle | What happens on placement, movement, modification, deletion, and cleanup? Where are limits enforced? What persists? | All OPEN |
| Production, storage, local distribution | How are selected outputs, inputs, power/fuel, capacity, inventory, and local connections evaluated and restored? | All OPEN |
| Cargo transport | How are endpoints paired and transfers scheduled/executed? What happens on interruption and save/load? | All OPEN |
| Assignments and modifiers | How do crew, robots, skills, and other modifiers apply, persist, and reapply? | All OPEN |

Time, loading/streaming, presence/absence, wait/travel, serialization, and restoration cut across all rows. Track those conditions within each investigation, not as assumptions shared without evidence.

## Adding a subsystem note

Create a focused Markdown note here when work begins; no empty per-subsystem packages are needed. Include:

- Open questions and scope; relevant source IDs and outside claims.
- Runtime model, lifecycle, operations/interfaces, failure cases, and evidence.
- Saved representation, identifier mappings, dependencies, and restoration behaviour.
- Persisted/default/derived/transient distinctions and authoritative-state questions.
- Validation, counterexamples, build limits, and proposed versus tested mod integration points.

Link findings, state/function registers, experiments, and evidence instead of copying their entire contents. Keep runtime and persistence explanations together even when one remains unresolved. See [the charter](../CHARTER.md) and [evidence standard](../EVIDENCE_STANDARD.md).
