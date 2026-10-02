# Outpost Subsystem Research Map

This map is a research agenda, not an assertion about the engine's implementation. No subsystem findings have been established in this project.

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
