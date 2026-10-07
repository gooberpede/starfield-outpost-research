# Research Charter

## Objective

> How does Starfield represent, operate, and persist player outposts, and how do those mechanisms interact throughout an outpost's lifecycle?

The primary deliverable is an evidence-backed explanation of outpost systems: runtime behaviour, state/relationships, saved representations, restoration, and their connections. Runtime knowledge is a first-class result, including knowledge useful for later mods; it is not merely a means to decode saves.

## Scope

Investigate the following as questions, not assumed engine architecture:

| Subsystem | Runtime focus | Persistence focus |
|---|---|---|
| Identity, location, membership | Outpost identity; enumeration; beacon/location/planet associations; ownership; constituent objects | Stored identities and relationships; resolution across reloads |
| Construction and lifecycle | Place/move/modify/remove; validation and limits; creation, registration, cleanup | Saved changes, deletions, relationship cleanup, restoration |
| Production, storage, local distribution | Resource/product choice; inputs/outputs; power/fuel; capacity; output connections | Configuration versus operating state; inherited and recalculated values |
| Cargo transport | Endpoint pairing; scheduling; movement of inventories; interruption/failure | Connections and in-progress state; save/load recovery |
| Assignments and modifiers | Crew, robots, skills, and other relevant modifiers | Assignment persistence; application and reapplication of effects |

Time and loading state cut across every subsystem: player present/absent, loaded/unloaded, waiting, travel, save/load, and other observed lifecycle transitions. Record conditions rather than assume continuous, event-driven, or catch-up simulation.

Shared record framing, identifier resolution, static game-data dependencies, scripting/native interfaces, and engine mechanisms are in scope when necessary to explain outposts. A complete unrelated save-format or engine reverse engineering effort is not required.

For important state, determine whether it is persisted, inherited from definitions, derived/reconstructed, transient, mixed, or unclassified; when it changes; and which values are authoritative. Map runtime and persisted identities only when demonstrated.

## Utility for future mods

Record observed/exposed interfaces, operations, events, preconditions, ordering, side effects, failure cases, and build dependencies. Label an internal mechanism separately from an integration point that has actually been tested. Do not assume direct memory mutation is sufficient or safe. A mod hook proposal is a hypothesis until separately validated.

## Non-goals at setup

No tracker import schema, production CLI, supported dump tool, gameplay change, save editor, library/package release, or importer implementation. No predetermined language or external implementation. Small research tools may be authorized later to answer or validate bounded questions; their existence does not decide the downstream product.

## First publication and completion

The programme is broad; the first publication scope/build matrix must be explicitly agreed after initial source/environment review and must include runtime and persistence objectives. Do not claim exhaustive understanding or mark the whole programme complete from one subsystem.

Within that agreed scope, completion requires documented mechanisms and representations, dependencies and limitations, reproducible evidence, validation beyond discovery examples, counterexamples addressed, and a rights/privacy-cleared publication corpus. A finding depending on unavailable evidence must disclose that reproducibility limit. Do not quietly remove required unresolved questions; scope changes need recorded user agreement.

The project starts private. Completed, reviewed research must be published under `GPL-3.0-or-later`. Later decisions about Starfield Outpost Network, a generic dump tool, or mods follow publication. See [PUBLICATION.md](PUBLICATION.md).

## Initial milestones, not execution authorization

1. Review candidate prior work and permissions; establish the actual local build/tool/save provenance and experimental safety plan.
2. Agree a small end-to-end case: identify a controlled outpost and a few objects live, record relationships, make one deliberate change with a no-action control, inspect the saved state, and observe reload/restoration.
3. Use the results to select bounded subsystem investigations and agree first-publication coverage.

No experiment has been executed or tool selected by this charter. See [RESEARCH_STATE.md](RESEARCH_STATE.md).

## Research infrastructure independence

SOR-D-0021: native/plugin-triggered save invocation is optional infrastructure, not a prerequisite. The programme can proceed through manual incremental checkpoint saves, controlled no-action saves, live observer/plugin evidence and offline differential save analysis. Live behavior and saved representation remain independently valuable and should be correlated. Deferring native saving is prioritization, not failure of the outpost programme.
