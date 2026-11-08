# Source and claim crosswalk

The [B1 matrix](../publication-readiness-b1/claim-build-matrix.md) has 16
parent and ten continuation rows. The [B4 register](../publication-readiness-b4/claim-evidence.csv)
supplies their stable IDs in the same order. The [F1 coverage index](../publication-readiness-b4/f1/coverage.csv)
retains its file-specific denominators. The [D5AX graph](../publication-architecture-d5ax/claim-evidence-dependencies.csv)
supplies the older route context. Follow the stable IDs into the [claim matrix](claims.json)
for exact original reports and reviews, evidence and split outcomes.

| Subsystem | Reader guide | Technical reference | Proposed claim IDs |
| --- | --- | --- | --- |
| Access and save framing | [Guide](../../../docs/guides/access-and-save-framing.md) | [Reference](../../../docs/reference/access-and-save-framing.md) | B4-C26, EXP0009-R3-FRAMING |
| Cargo | [Guide](../../../docs/guides/cargo.md) | [Reference](../../../docs/reference/cargo.md) | B4-C09, B4-C23, B4-C23-PRIVATE-COMPARATORS, B4-C23-SAVE52-ORIGINAL |
| Construction | [Guide](../../../docs/guides/construction.md) | [Reference](../../../docs/reference/construction.md) | B4-C11, C25-ORIGINALS, B4-C25 |
| Containers and displays | [Guide](../../../docs/guides/containers-and-displays.md) | [Reference](../../../docs/reference/containers-and-displays.md) | B4-C13, B4-C13-H21-DISPLAY-ORIGINAL |
| Crew and robots | [Guide](../../../docs/guides/crew-and-robots.md) | [Reference](../../../docs/reference/crew-and-robots.md) | B4-C10, B4-C24 |
| Defense | [Guide](../../../docs/guides/defense.md) | [Reference](../../../docs/reference/defense.md) | B4-C12 |
| Fabrication | [Guide](../../../docs/guides/fabrication.md) | [Reference](../../../docs/reference/fabrication.md) | B4-C06, C06-0036, C06-CENSUS |
| Identity | [Guide](../../../docs/guides/identity.md) | [Reference](../../../docs/reference/identity.md) | B4-C01, B4-C17, C17-ROOT-TABLE |
| Inorganic production | [Guide](../../../docs/guides/inorganic-production.md) | [Reference](../../../docs/reference/inorganic-production.md) | B4-C04, B4-C20, D5AU-EXTRACTOR, D5W-AREA-POINT-CONTROL |
| Locations ui | [Guide](../../../docs/guides/locations-ui.md) | [Reference](../../../docs/reference/locations-ui.md) | B4-C16 |
| Nominal biomes | [Guide](../../../docs/guides/nominal-biomes.md) | [Reference](../../../docs/reference/nominal-biomes.md) | B4-C03, C03-FRAME-CONTROL |
| Organic production | [Guide](../../../docs/guides/organic-production.md) | [Reference](../../../docs/reference/organic-production.md) | B4-C05 |
| Position | [Guide](../../../docs/guides/position.md) | [Reference](../../../docs/reference/position.md) | B4-C02, C02-ORIGINALS, B4-C18, C18-FULL-CONTROLS, C19-D1-SITE-TABLE |
| Power | [Guide](../../../docs/guides/power.md) | [Reference](../../../docs/reference/power.md) | B4-C07, B4-C07-SAVE29-THREE-LOADS, B4-C21, B4-C21-SAVE29-ORIGINAL |
| Resource generation | [Guide](../../../docs/guides/resource-generation.md) | [Reference](../../../docs/reference/resource-generation.md) | B4-C19, C19-CALLBACK, C19-D1-INCIDENT, C19-D1-SAVED, C19-D1-SITE-TABLE, C19-UPSTREAM, D5AC-B2-RETAIL, D5AG-FIXED-GEOMETRY, D5AK-EPISODE-A, D5AL-EPISODE-B, D5AO-N2, D5AP-N2-COMPETITION, D5AQ-C1-TABLE, D5AQ-EXACT-FIXTURE, D5AQ-REACHABILITY, D5AR-SNAPSHOT-SCHEMA, D5AS-ACQUISITION, D5AS-BODY, D5AT-EXACT-REPLAY, D5AT-INDEXED, D5AU-EXTRACTOR, D5AU-FIRST-MISS, D5AV-CACHE, D5U-U26-COUNTEREXAMPLE, D5W-AREA-POINT-CONTROL |
| Shared storage | [Guide](../../../docs/guides/shared-storage.md) | [Reference](../../../docs/reference/shared-storage.md) | B4-C14, C14-CENSUS, C14-FRESH-TRIO, C14-ORIGINALS, C14-TABLE |
| Storage and output links | [Guide](../../../docs/guides/storage-and-output-links.md) | [Reference](../../../docs/reference/storage-and-output-links.md) | B4-C08, B4-C22, B4-C22-L-SERIES-ORIGINAL |
| Stored resources | [Guide](../../../docs/guides/stored-resources.md) | [Reference](../../../docs/reference/stored-resources.md) | B4-C15 |

## Historical scope and split decisions

| Historical ID | B1/B4 candidate | Proposed mapping |
| --- | --- | --- |
| B4-C01 | Identity, membership and Workshop ownership | B4-C01 |
| B4-C02 | Planetary location and position | B4-C02, C02-ORIGINALS |
| B4-C03 | Nominal biomes and resource regions | B4-C03, C03-FRAME-CONTROL |
| B4-C04 | Inorganic production and nominal rates | B4-C04 |
| B4-C05 | Organic production | B4-C05 |
| B4-C06 | Manufactured production | B4-C06, C06-0036, C06-CENSUS |
| B4-C07 | Power and generator fuel | B4-C07, B4-C07-SAVE29-THREE-LOADS |
| B4-C08 | Storage and local output links | B4-C08, B4-C22, B4-C22-L-SERIES-ORIGINAL |
| B4-C09 | Cargo configuration, freight and inter-system fuel | B4-C09, B4-C23, B4-C23-PRIVATE-COMPARATORS, B4-C23-SAVE52-ORIGINAL |
| B4-C10 | Crew, skills and robots | B4-C10, B4-C24 |
| B4-C11 | Construction limits, placement, variants and catalogue | B4-C11, C25-ORIGINALS |
| B4-C12 | Attacks, defenses and Integrity | B4-C12 |
| B4-C13 | Chests, displays and mannequins | B4-C13, B4-C13-H21-DISPLAY-ORIGINAL |
| B4-C14 | Shared Outpost Storage and crafting sources | B4-C14, C14-CENSUS, C14-FRESH-TRIO, C14-ORIGINALS, C14-TABLE |
| B4-C15 | Stored Resources | B4-C15 |
| B4-C16 | Locations to Outpost information | B4-C16 |
| B4-C17 | Identity | B4-C17, C17-ROOT-TABLE |
| B4-C18 | Position | C02-ORIGINALS, B4-C18, C18-FULL-CONTROLS |
| B4-C19 | Availability/deposits | B4-C19, C19-CALLBACK, C19-D1-INCIDENT, C19-D1-SAVED, C19-D1-SITE-TABLE, C19-UPSTREAM |
| B4-C20 | Rate arithmetic | B4-C20 |
| B4-C21 | Power | B4-C07-SAVE29-THREE-LOADS, B4-C21, B4-C21-SAVE29-ORIGINAL |
| B4-C22 | Local movement | B4-C22, B4-C22-L-SERIES-ORIGINAL |
| B4-C23 | Cargo | B4-C09, B4-C23, B4-C23-PRIVATE-COMPARATORS, B4-C23-SAVE52-ORIGINAL |
| B4-C24 | Crew/robots | B4-C10, B4-C24 |
| B4-C25 | Construction | C25-ORIGINALS, B4-C25 |
| B4-C26 | Access and interfaces | B4-C26, EXP0009-R3-FRAMING |

All 26 historical IDs have a primary row. Extra rows distinguish different
evidence propositions such as an arithmetic reconstruction, a raw original
comparison and an eyewitness event. Preserving a report and its original
confidence or verdict is independent of proposing its assertion as current.

## Post-B1 subjects and predecessor routes

| Origin | Proposed claim IDs and reason for a separate route |
| --- | --- |
| D5AK/D5AL and B2 | D5AK-EPISODE-A and D5AL-EPISODE-B distinguish two complete equal bodies with different documented process/source histories. D5AC-B2-RETAIL records an observed map hit versus the ordinary static rule. A0 equality is a baseline for B0, without requiring the later A1 departure sequence. |
| D5AO/D5AP/D5AQ | D5AO-N2 and D5AP-N2-COMPETITION preserve the observed winner and recorded competitors. D5AQ-C1-TABLE, D5AQ-REACHABILITY and D5AQ-EXACT-FIXTURE separate fixed table arithmetic, native feasibility, and exact native control reproduction. D5AE scheduling and earlier D5W path models remain original prerequisite explanations. |
| D5AR/D5AS | D5AR-SNAPSHOT-SCHEMA covers the authored representation. D5AS-BODY carries the complete comparisons conditional on the D5BF asset. D5AS-ACQUISITION holds the distinct original custody proof. A body match does not observe the generating mask. |
| D5U/D5W/D5AG | D5U-U26-COUNTEREXAMPLE preserves the separate source's three complete outcome classes. D5W-AREA-POINT-CONTROL distinguishes fixed-point eligibility from equal area identities. D5AG-FIXED-GEOMETRY keeps the earlier independent fixture comparison distinct from D5AQ and D5AS. |
| D5AT | D5AT-INDEXED preserves the amended 17-site table and family-specific conditional counts. D5AT-EXACT-REPLAY separates original Save52/definition/grid and fixed native control requirements. |
| D5AU/D5AV | D5AU-FIRST-MISS, D5AV-CACHE and D5AU-EXTRACTOR explain the qualified ordinary first-miss, owner lifetime and saved producer-continuity mechanisms. Historical reset/hit/construction witnesses remain individually governed by their rows. Preserve optional warm-return, usual winner and changed-geometry runtime questions as separate deferred research. |
| D5BD | D5BD-LEVEL-A, D5BD-LEVEL-B and D5BD-LEVEL-C cover the three advertised characterization depths. Use the [native catalogue crosswalk](../native-function-catalogue-d5bd/crosswalk.md) for its original-locator links to all 18 subjects. |
| RC1 and EXP0009 | B4-C26 covers the declaration/consumer selection. EXP0009-R3-FRAMING makes the supported saved framing claim explicit. Neither assigns a caller ABI or exhaustive membership. |

## How the graph was reconciled

The older D5AX graph records 547 predecessor rows across the 26 B4 and nine
resource groups. Its source, method, candidate member, residual and scratch
records describe different tiers. The D5BG graph rolls them up by the precise
claim and tier, with exact predecessor keys for material joins:

- Older `claim` and `source-N` entries follow the historical ID, exact
  original report/review and authored route in the matrix. A tracked synthesis
  cannot replace an indispensable original runtime event.
- Candidate `B4-Fnnn` nodes are reconsidered only for each selected exact
  witness. Member names and pins follow D5BF. Other member nodes remain
  supporting or unselected at this tier, with the original F1 disposition
  unchanged. The group ZIP alone supplies neither the reader nor a replay.
- `methods`, `domain-method` and `installed-inputs` retain the
  [B3 contracts](../publication-readiness-b3/method-contracts.csv) where needed.
  Exact lawful reconstruction needs the relevant versioned input and reader.
  Authored inspection does not inherit a full native/real-save replay promise.
- `residual` and named missing operands are tracked in the relevant split
  rows and [exceptions](exceptions.md). Disposable `scratch` does not close
  an evidence edge. The workspace has no post-publication retention obligation.
- The resource groups carry source/custody relationships separately from
  current explanations. For instance, the canonical D5AS bodies require
  the bounded roster and proposed derivative. Rechecking acquisition custody
  additionally requires evidence that the derivative leaves local. The D5AV
  conditional cache model can be inspected without claiming a historical
  return took that particular route.
