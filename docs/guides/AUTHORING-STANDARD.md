# Subsystem guide and reference authoring standard

Write for a reader who already understands reverse engineering or Creation
Kit modding. Assume they have never read this project's brief identifiers,
observer schemas or local file conventions. The
[resource guide](resource-generation.md) and its
[technical reference](../reference/resource-generation.md) pilot this
structure. D5AX's [reader architecture](../audits/publication-architecture-d5ax/architecture.md)
and D5AW's [publication independence plan](../audits/deferred-work-d5aw/publication-plan-amendment.md)
govern the division of material.

| Layer | Authoring contract | Resource-generation pilot |
| --- | --- | --- |
| Guide | Answer the player's ordinary question first. Introduce the things involved, follow the normal route, distinguish runtime from saved state and explain one important counterexample. State the build, action and effective-input scope beside consequential claims. | A new source can rebuild identical deposits. The first eligible map miss controls the sample, while area lists and extractor rows are separate products. |
| Technical reference | Define identity domains, frames and input prerequisites. Map decisions, owners, lifetimes, writers, readers, failure branches and consumer effects. Link exact locators, evidence, review and a challenge for each major result. Use existing registers for full address inventories. | Separate the source pointer, visited token and FormID. Show the protected arbitration, the retirement/reset distinction and the envelope/body comparison. |
| Evidence and history | Keep reports, original reviews, controls and dated decisions at their existing paths. Explain changes in scope where the reader encounters the affected claim. | D5AU scopes the historical usual-winner question and D5AV makes action-dependent findings conditional. D5AS preserves the ineligible acquisition and classifies only qualified snapshots. |
| Glossary | Maintain a canonical definition per concept. Classify the entity and give purpose, behavior, domain, provenance and sourced ownership or lifetime where known. Keep aliases and explicitly separate subsystem-specific meanings. | “Map hit” identifies the protected pointer lookup, while historical “cache hit” needs the actual store named. |

## Evidence and notation

Build a claim-to-source crosswalk before drafting the decisive explanation.
For each claim record its ordinary or exceptional path, build/sample, exact
report and locator, evidence basis, review, counterexample and access tier.
Use the [evidence standard](../EVIDENCE_STANDARD.md) to distinguish STATIC,
SAVE, RUNTIME, controlled executions and derived analysis. Record confidence
and coverage separately. Distinguish a scoped accepted result from proposed
or historical dispositions.

Use hexadecimal for bit patterns, addresses, FormIDs and byte offsets, and
decimal for counts, coordinates and ordinary measurements. Name the base,
frame, units and byte domain where needed. Keep runtime handles, pointers
and saved IDs separate. For state, identify which object owns the value,
what the serializer writes and what the eventual consumer uses. Extend
the [glossary](../reference/glossary.md) when a new guide introduces a
concept or resolves a material ambiguity. Link terms at useful entry
points and keep the reading flow uncluttered.

## Figures and access

Use Mermaid for auditable decision and ownership diagrams. Label arrows
by behavior and state which branches the schematic abstracts. Use exact
tables or source-owned SVG for quantitative comparisons, with explicit
units, denominators, captions and tracked input locators. For spatial
figures follow the [visualization standard](../VISUALIZATION_STANDARD.md)
for validated frame, bounds, colors and geometry. Run local rendering
when available and record tool and inspection limits. Never infer an
outpost overlay from a source-only frame.

Label inspectable tracked text and calculations, conditional regeneration
with lawful installed inputs, provisional Release assets and unavailable
historical evidence separately. Identify indispensable missing routes as
**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING**. A report, hash or private
path is different from a reproducible public input. A newly cleared
derivative or hosted asset needs its own authority and exact validation.

## Navigation and acceptance

From the root, reach the guide within two clicks. The guide links directly
to the technical page. Each decisive technical claim leads directly to its
report and review or states the review's access status. Link a negative or
superseded interpretation. Test three journeys on the exact pages.

1. Understand the normal route and explain a practical consequence and limit.
2. Repeat a named available check using a fresh input set without the existing
   private working directory. Record exactly what the check demonstrates.
3. Challenge a claim by finding its original scope, review and counterexample.

Verify case-sensitive links and heading fragments, figure syntax and
appearance where feasible, and arithmetic from tracked inputs. Screen and
manually read the full changed prose under the
[editorial standard](../EDITORIAL_STANDARD.md). Independent review checks
scientific qualifications, glossary entity boundaries and exact final
prose before verified delivery export. Record access and rendering limits
separately from acceptance.
