# Fixed planetary POIs — conditional independent validation candidates

2026-10-10, SOR-D-0041 / SOR-EV-0030. Retains the user's requested validation
direction; **candidate plan**, not new native equivalence or a live experiment.
No arbitrary minimum outpost count is required. Select cases by independent
provenance, branch/frame coverage, boundary discrimination and counterexamples.

Existing [EXP0013 fixed anchors](../planetary-surface-anchor/fixed-anchors.csv)
and [native/definition report](../planetary-surface-anchor-semantics.md) provide
a starting shortlist. Labels are navigational; exact PNDT/WRLD joins govern.

| Candidate | Body PNDT | Fixed WRLD | Existing evidence and qualification still needed |
|---|---|---|---|
| New Atlantis / Jemison | 0003F5A1 | 0001251B | Fixed CNAM pair agrees bit-for-bit with saved Save2 parent-associated pair; useful anchor provenance. Must demonstrate relevant world/terrain quantization and frame consumers, rather than assume city anchor equals a beacon center. |
| Akila fixed city world | 0005E2B6 | 0027CFA2 | Selected installed CNAM fixed-world entry; selection by WRLD matters because PNDT has other entries. Confirm exact reference/anchor and relevant execution path before an oracle comparison. |
| Mars fixed world | 0003F59A | 002CFC4A | Selected installed CNAM fixed-world entry on a different body; exact location/reference identity and relevant native path must be qualified. Do not infer them from a display name alone. |

Prior source: pinned retail Starfield.esm SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`,
SOR-S-0129/0132 as recorded in EXP0013/0020. Native preferred static VA14076ec00
reads PNDT's pre-BDST CNAM fixed-world entries, swaps disk latitude/longitude
into the component pair and calls140773090. This establishes common **anchor
ingestion**, not by itself common outpost-center/grid/residual reconstruction.
No new ESM extraction or native tracing is claimed by this note.

## Qualification and independence requirements

1. Identify the fixed POI's precise body, world, anchor/reference and source
   definition; distinguish procedural site, fixed-city world, map marker and
   actual reference position. Retain build/hash/offset domains and overrides.
2. Follow producer/consumer evidence to the relevant native coordinate operation
   (for example shared hierarchy selection/projection/frame conversion), recording
   branch, resolution, axis/chart convention and runtime initialization. Same
   spherical-angle names or nearby map pixels do not prove algorithm identity.
   A non-Workshop POI may never execute the Workshop compensation branch.
3. State exactly which model stages it can validate: body/anchor/grid/frame
   stages may be testable independently while compensation and durable Workshop
   authority are inapplicable. Do not manufacture a Workshop input for a city.
   The current `sor-position/1` Workshop model rejects unsupported inputs; a
   future shared-coordinate test harness/domain extension needs explicit review.
4. Freeze independent inputs and predictions before inspecting new native
   output. Capture the native operation's output/intermediates independently of
   the reproducer. Reuse of an existing model-derived cell as both input and
   oracle is circular. Existing New Atlantis/three anchor cases are known
   corroboration cases, **not blind holdouts** for anchor semantics.
5. Apply the same predeclared exact/conditional-frame policy as the
   [validation protocol](validation-protocol.md). Record mismatches and missing
   branches rather than adjusting per-POI offsets. Newly selected unseen fixed
   POIs can become holdouts only with appropriate precommitment and provenance.

A qualified fixed POI can provide an independent validation channel without
creating additional player outposts. It does not replace Save25/26's controlled
relocation invariance, which tests a distinct Workshop-specific mechanism.
This direction is separate from **Phase1**; no POI travel/deployment/live capture
or arbitrary collection target is added to its run card.
