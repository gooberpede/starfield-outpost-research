# D5BG proposed publication claims and evidence routes

**PROPOSED · NOT READY / NOT CLEARED**  
2026-11-08, Australia/Sydney.

| Controlling question | Proposed answer |
| --- | --- |
| Q1 · What may the first release claim? | Use the [claim matrix](claims.json) for the exact propositions and reader wording. Retain the original reports, reviews and negative cases as the research record. |
| Q2 · Which evidence can readers inspect independently? | The [evidence graph](evidence-edges.json) separates tracked authored material, conditional methods and proposed asset bytes from unresolved exact-witness dependencies. Follow each edge through its prerequisites. |
| Q3 · What decisions and work remain? | The [exceptions](exceptions.md) explain the material distinctions. The [actions ledger](actions.json) binds each outstanding disposition to its evidence, options and acceptance check. |
| Q4 · What precedes B6? | The [handoff](handoff.md) describes the scope decision, closure work, coordinated archival and exact preflight in that order. The [run card](../../PUBLICATION_RUN_CARD.md) controls execution. |

Start with the [crosswalk](crosswalk.md) for a subsystem or historical B4 ID.
Each claim links its current guide/reference pair, original sources, existing
confidence or source disposition, coverage, limits and evidence IDs. Reports
and reviews retain authority over their own scientific assessments.

## Status and evidence semantics

| Proposed claim status | Meaning in D5BG |
| --- | --- |
| READY | The stated tier has a present tracked route with its necessary operands and sources. Release authorization remains a separate gate. |
| READY — QUALIFIED | The stated narrower tier has a present tracked route. Publish the exact claim with the listed coverage, negatives and limits if approved. |
| ACTION REQUIRED | The proposed assertion or exact tier still needs an identified prerequisite. A proposed D5BF asset qualifies for isolated staged preflight only after exact selection. |
| MAINTAINER DECISION | The maintainer must choose the exact tier, retain a narrower statement or authorize a specific follow-up. |
| HISTORICAL ONLY | Proposed treatment for an older report component, superseded assertion or unresolved extension. Its original source and disposition remain visible. |

An **INDISPENSABLE** edge is necessary for the stated tier of the proposition
that reaches it. A **SUPPORTING** edge records useful corroboration or
provenance. `requires` lists transitive prerequisites. `predecessors` identifies
exact D5AX `(claim, node)` joins where one exists. `READY` edges support the
specified tracked inspection or calculation tier today. `CONDITIONAL` edges
need a named asset or lawful procedure/input qualification. `HELD` edges lack
an adequate present or approved candidate route. `CONTEXT` records a
nonessential source without treating it as an independent reproduction route.
See the route and consequence fields for the limit of each assertion.

[D5BH](../evidence-derivative-d5bh/README.md) records the D5AS tier selection
separately from the inherited route dispositions. It also assesses a local
common D5AK/D5AL witness. The exact episode publication routes remain held.

[D5BI](../evidence-derivative-d5bi/README.md) records Option C and the local
D5AO/D5AP N2 projection. The public evidence edges remain held pending exact
rights/privacy review, authorized transfer, B6 and hosting.

[D5BP](../publication-decisions-d5bp/README.md) selects five first-release
tiers. Their `MAINTAINER DECISION` rows retain the inherited classification of
the stronger exact-replay propositions. The selections and pending witness
checks are recorded separately from those held routes.

[D5BQ](../publication-decisions-d5bq/README.md) selects the power, cargo,
local-link and historical evidence tiers. The four HISTORICAL ONLY rows
remain attributed history. The bounded D1 saved-state tier is selected.
Its inherited MAINTAINER DECISION row retains the stronger original-byte
proposition and HELD edge. The separate transcribed-field comparison
retains its READY route. Exact selected Save29, Save52, local-link and
Kreet callback checks remain conditional.

## Snapshot and safeguards

The starting branch was `main`, HEAD
`678450f563f299bfa6dc46afcc00ba59b98e7637`, tree
`99e9a9db8c4d3cbdd9d8a15354eeedf72c3c0a2a`. The index and tracked working
tree were clean with 3,928 index entries. The only untracked path was the
[supplied brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BG_Final_Publication_Claim_and_Evidence_Reconciliation.md),
SHA-256 `8ce64e354da7e3796e0d7b29a69c619dac142c798908874e77bd7b62fc0e866f`.
It remains separate from task-authored changes.

N244 refers to retail Starfield.exe 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
preferred image base `0x140000000`. The main Starfield.esm pin is
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
These are documentary pins from the [B3 baseline](../publication-readiness-b3/baseline-manifest.md).
H? marks unestablished originating build for historical saves. Header versions,
effective configuration, loaded modules and winning definitions keep their own
claim-specific records.

The [charter](../../CHARTER.md) and [research state](../../RESEARCH_STATE.md)
keep runtime and persistence in scope together. The [evidence standard](../../EVIDENCE_STANDARD.md)
drives the independent basis, confidence, coverage and completeness fields.
The [standing orders](../../../AGENTS.md), [workflow](../../../WORKFLOW.md),
[third-party policy](../../../THIRD_PARTY_POLICY.md) and
[publication policy](../../PUBLICATION.md) limit this pass to source inspection
and preparation of authored text. Original research, raw game data and release
assets stay on their existing routes. The [completion protocol](../../RESEARCH_EXECUTION_PROTOCOL.md)
requires the original Q1–Q4 and AC01–AC10 to control independent review.

## Verify the text package

From a checkout, run `python -I -B docs/audits/publication-claims-d5bg/verify.py --negative-controls`.
The standard-library script reads this collection, B4 IDs, the D5AX graph,
guide/reference paths and the D5BF ledger. It checks structured joins,
dependency closure, proposal status, source paths and unique counts. It writes
no files and requires no assets, installed game, network or `.local-work/`.
The negative controls exercise a missing dependency, a falsely hosted pending
asset, a duplicate ID and an unjustified READY disposition. These checks leave
scientific interpretation, source rights and B6 to their separate reviews.
