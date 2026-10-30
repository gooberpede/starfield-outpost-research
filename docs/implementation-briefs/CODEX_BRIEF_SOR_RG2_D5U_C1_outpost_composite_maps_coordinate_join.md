# SOR RG2-D5U-C1 — Outpost-centred composite maps and coordinate reconciliation

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Correct D5U's outpost-level visual interpretation without revising accepted source-level science. Offline, read-only research plus task-owned authored map/data/document updates.  
**Authority:** No Starfield/SFSE/Steam launch, attachment, Vortex operation, plugin change, save modification, unauthorized repository integration or publication. No stage/commit/push. Any focused access to existing protected save derivatives must follow approved read-only resource-access and protection rules.  
**Parent:** D5U's accepted source census; D2 source/site coordinate evidence and Save52 outpost observations. Frozen C1-AC1–C1-AC10 below. **D5P retail remains NO-GO; B6 remains ON HOLD.**

## 1. Why this correction is necessary

D5U's 38 maps are principally **individual resource-source plots**, not maps of an outpost's buildable territory and all its contributing resources. Attaching an outpost name to an individual source plot can misleadingly suggest it displays the whole outpost. The primary counterexample is the historical outpost **Feynman V Cu Co Ni IL** (case `D2-83388f`): observed Copper, Cobalt, Nickel and Ionic Liquids, but its D5U plots display one source family at a time.

D5U's accepted `d5u-names-and-centre-followup.md` records:
- U01–U04 all associate to this one outpost, across two family groups; U26 is **not** an outpost.
- The known buildable radius is **150 native units**.
- Historical D2 centre projections exist; D5U plots use **source-relative** coordinates (source anchor `(0,0)`, prospectively normalized generation context). A proved translation from historical native centre/beacon to each plotting frame was not completed.
- Prospectively normalized native geometry **must not silently be presented as an exact replay of historical outpost geometry**. Moving the frame can change seed inputs and generated regions.

**Controlling question C1-Q1:** Can the authenticated historical native outpost centre and 150-unit disk be located correctly in the D5U geometry frames for the seven recorded outposts, distinguishing centre, beacon and source anchors?  
**C1-Q2:** Can all relevant source contributions be assembled in a scientifically qualified common frame to show the whole buildable area and reconcile the four observed resource types for the primary Feynman V outpost?  
**C1-Q3:** Can reusable outpost-centred mapping methods and gallery labels make source-level versus outpost-level evidence unmistakable for subsequent research?

These are **outcome requirements**, not tasks satisfied by merely reporting that a join is unknown. Under the current research completion protocol, remaining tractable authorized dependencies require continued investigation, and a genuine BLOCKED return requires a precise demonstrated barrier.

## 2. Required evidence and decision order

Read current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/VISUALIZATION_STANDARD.md`, `docs/SAVE_PROTECTION.md`, reviewer/editorial procedures and the accepted D5U/D5T/D5S records. In particular, inspect:

- `docs/experiments/resource-retained-population/d5u-names-and-centre-followup.md`
- `docs/experiments/resource-retained-population/d5u/README.md`, D5U geometry export and plot generator
- `docs/experiments/resource-save52/report.md`, `cases.csv` and the historical centre-projection evidence
- `docs/experiments/resource-predictability-contrast/source-matrix.csv`
- Existing D2 native centre/beacon projections, source origins, chart/body transforms and outpost-disk controls

Begin by recording the immutable case/source associations and exact original evidence locations. Confirm U01–U04 (`D2-83388f`, Feynman V Cu Co Ni IL), U05–U08 (`D2-82be17`), U09–U12 (`D2-81a75b`), U13–U16 (`D2-81bf2a`), U17–U18 (`D2-825f95`), U19–U21 (`D2-844cc6`) and U22–U25 (`D2-84e101`). U26 is an unassociated static research source and **must never be assigned a fictitious outpost disk**. Verify against current records rather than treating these associations as executable authority.

Trace independently: saved/site outpost native centre; beacon native position; resource-source anchor; source origin and padding; the generation-coordinate frame; and SVG transform (origin/scale/Y direction). Show equations, units, chart/face/origin assumptions, transformations and uncertainty. Compare at least one independent D2 numeric control and back-transform known coordinates. Identify whether the historical disk can be truthfully overlaid on **prospective** source plots as a reference only; do not imply that coordinate translation alone makes the prospective geometry historical. Confirm the circle's 150-unit radius after transformation and ensure it is not clipped.

## 3. Primary acceptance test: Feynman V Cu Co Ni IL

Produce an **outpost-centred composite SVG** for `D2-83388f`, with the verified native centre, 150-unit boundary and separately identified beacon if supported, plus appropriately qualified geometries/contributions from U01–U04 together in the same plotted coordinate system. Show source anchors and distinguish each source's provenance without overwhelming the map.

The outpost is observed to offer **Copper, Cobalt, Nickel and Ionic Liquids**. These are historical observations, **not** permission to invent model predictions. Provide a resource-by-resource reconciliation table with at least:

| Resource | Observed historical availability | Contributing source(s) | Qualified modeled geometry intersecting actual outpost disk? | Evidence status and discrepancy |
|---|---|---|---|---|
| Copper | Observed | Demonstrate | Determine | Explain |
| Cobalt | Observed | Demonstrate | Determine | Explain |
| Nickel | Observed | Demonstrate | Determine | Explain |
| Ionic Liquids | Observed | Demonstrate | Determine | Explain |

If a predicted source contributes none of one observed resource inside the verified disk, **investigate the mismatch**: candidate source coverage, source-to-site association, placement/boundary overlap, frame/seed mismatch, selected mask/effective definition, alternate native generation outcome, terrain/consumer scope, or defective plotting. Preserve it as unresolved if investigation cannot close it; do not erase the discrepancy by adjusting the plot or relabeling observed data.

Distinguish **observed historical availability**, **prospective qualified native geometry**, and **unknown historical winner/outcome** in legend and report. If multiple independent source variants occur, show only joint configurations supported by common initialization/scheduling evidence. Do **not** take a Cartesian product of source outcomes and call every combination achievable. If joint feasibility is unresolved, use separate source contribution layers or explicitly conditional composite alternatives, not a false single "actual" configuration.

## 4. Remaining outposts and map suite

For each of the other six associated outposts, create or revise a usable **outpost-level composite** with source contributions and its verified 150-unit disk. Preserve the original 26 source-support maps and their scientific classification as distinct artifacts. Use explicit naming and gallery sections: **Outpost composite maps**, **Individual source query-support maps**, **Individual source native-generation maps**, and **Unassociated sources**. Mark any conditional model/reference overlay prominently, including the data provenance and native version.

An outpost-level map must not be counted complete solely because individual source maps exist. If a particular outpost-centre join or geometry model remains unresolved after exhausting authorized methods, record exact per-case blocker, missing evidence and what can safely be shown. A clearly labelled source-only view is a fallback/handoff, **not** an outpost-map PASS. Keep all historical observations distinct from generated native geometry.

Use consistent native coordinate orientation and scales within comparisons, sensible zoom that includes the entire 150-unit disk, IRES-derived resource colors where available, and contrasting marker/stroke for the disk and native centre. Where a beacon has a different qualified position, show it separately; where its relationship is unknown, label it unknown rather than coincident. Provide a legend for line/symbol provenance. No decorative simulated deposits or fabricated exact boundary shapes. Native region point/bounds and stated SVG rounding caveats remain authoritative.

Generate an additional **method/diagnostic SVG** if it materially improves understanding of how different source origins align to one native outpost centre. Visualize observed/predicted resource overlap and discrepancy when reliable coordinates make such views meaningful. Supply machine-readable composite geometry/reference data and deterministic build commands; validate SVGs by parsing, rendering, inspecting and checking canonical-frame positions against independent numeric controls.

## 5. Method and continuation rules

Reuse the D5U native outputs, source IDs, IRES palette and reproducible renderers. Avoid rerunning complete procedural generation without a discriminating reason; **do** investigate and run bounded offline native/geometry work when necessary to determine whether a prospective source contribution can truthfully be placed in the outpost frame. Original accepted scientific results are immutable historical findings; changes to interpretation or identified errors must be documented, not silently rewritten.

Create a live investigation ledger **before substantive analysis**, containing C1-Q1–Q3, hypotheses, exact joins/offsets, transform checks, failed alternatives, discovered dependencies, status and next action. Follow all material authorized branches until COMPLETE or an evidenced terminal BLOCKED; do not turn a new upstream dependency into an unapproved deferral. If an indispensable input specifically points to persisted data, conditionally inspect existing protected material through read-only approved access and report checks; do not perform general save archaeology.

If the historical centre and prospective geometry cannot be made comparable without changing the generation frame and thus the seeded result, either reproduce the qualified generation under the historical frame **offline** or separate the map into truthful historical reference and prospective relative-generation layers, explaining why they cannot be combined as a definitive prediction. This is a scientific qualification decision that independent review must challenge.

No live operations, plugin deployment or protected-file mutation. Retain identity and free-space protections, source/licensing controls, local-only proprietary materials and publication gates. Do not stage, commit, push or modify unrelated repository material.

## 6. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **C1-AC1 — Authority, pins and preservation** | Check inputs, versions, repository baseline and protection; no unauthorized live, saved-state, plugin, database, publication or Git integration operations. |
| **C1-AC2 — Question freeze and active ledger** | Freeze C1-Q1–Q3, scope, acceptance and explicit uncertainty before work; maintain evidence-backed chronology, dependencies and failed alternatives. |
| **C1-AC3 — Historical centre/beacon evidence** | Recover and authenticate actual D2 centre evidence, beacon correspondence and per-outpost/source association; do not conflate source anchor and native centre. |
| **C1-AC4 — Coordinate-join proof** | Derive and independently test native centre-to-source and native-to-SVG transformations, including origin/units/orientation/radius/round trip; quantify residual uncertainty. No unqualified overlay. |
| **C1-AC5 — Primary four-resource outpost map** | Produce a real Feynman V Cu Co Ni IL composite with all relevant U01–U04 contributions, verified centre and 150-unit disk, and clearly distinguished source/observation/model layers. |
| **C1-AC6 — Resource reconciliation** | Account for observed Copper, Cobalt, Nickel and Ionic Liquids individually, with source attribution, geometry/boundary evidence and any discrepancy investigated rather than suppressed. |
| **C1-AC7 — Other associated outposts** | Deliver six further outpost composites with verified centres and disks, or demonstrate precise per-case terminal blockers. Source-only views do not satisfy this criterion. U26 remains source-only. |
| **C1-AC8 — Fidelity and presentation** | Stable resource colors, geometric integrity, axes/frame/scale, labelled centre/disk/beacon, clear historical-versus-prospective distinctions, readable direct comparisons and no silent clipping or unsupported joint variants. |
| **C1-AC9 — Reproducibility and scientific integrity** | Machine-readable composite exports, deterministic generation/verification, numeric transform controls, SVG parse/render/visual QA, source provenance and documented approximation limits. |
| **C1-AC10 — Adversarial completeness review and delivery** | Independent scientific/completeness, engineering/evidence and editorial reviews against original questions/criteria; reviewer specifically tests missing resource layers, unqualified transforms and false historical claims. Exact hashes, complete/task-only diffs, status and exclusions; no staging/commit/push. |

## 7. Terminal results and delivery

**COMPLETE / ACCEPT** requires the controlling questions and all mandatory criteria satisfied, including a defensible four-resource primary map and true outpost-centred composites (or only explicitly maintainer-approved changes to the contract). **INCOMPLETE / REWORK** applies when relevant authorized analysis remains or a mandatory map/reconciliation is missing. **BLOCKED / ESCALATE** requires an indispensable specific evidence/access/authority barrier, tested alternatives and the narrowest resume request; BLOCKED is not COMPLETE and cannot silently pass a mandatory criterion.

Suggested durable outputs, adapted to established repository conventions:
- `docs/experiments/resource-retained-population/d5u-c1-report.md` and active ledger.
- A coordinate-join/validation document with case/source numeric transformations and source ledger.
- `docs/experiments/resource-retained-population/d5u/outposts/` with seven composite SVGs, backing geometry/reference data and a clear README.
- A four-resource discrepancy/reconciliation table for Feynman V Cu Co Ni IL, and concise coverage tables for remaining cases.
- Focused updates to `docs/VISUALIZATION_STANDARD.md`, D5U gallery/navigation and current research state, preserving original source-level results and historical reviews.
- Independent criterion matrix/review, source/provenance ledger, exact final manifest and review patches.

Before authoring new plots, identify any necessary deviations from these paths, document them, and preserve the original evidence and names. **No task result authorizes retail use, publication, staging, commit or push.**
