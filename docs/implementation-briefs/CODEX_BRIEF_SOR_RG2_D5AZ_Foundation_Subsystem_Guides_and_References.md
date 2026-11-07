# Codex implementation brief — RG2-D5AZ: Foundation subsystem guides and technical references

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Task type:** Documentation synthesis, technical-reference authoring, navigation and independent audit  
**Date:** 2026-11-07 (Australia/Sydney)  
**Status:** Maintainer-requested brief; execution is confined to the authority below. This is **not** publication approval.  
**Governing pattern:** The accepted D5AY resource-generation pilot, particularly `docs/guides/AUTHORING-STANDARD.md`, `docs/guides/resource-generation.md`, `docs/reference/resource-generation.md` and `docs/reference/glossary.md`.

## 1. Objective and audience

Produce the next four **reader-facing guide/technical-reference pairs** under D5AX's approved three-layer architecture. Readers are comfortable with reverse engineering and Creation Kit modding, but have **not** followed this project's history, aliases, save experiments or Codex brief sequence. Explain **what the game does, what the actual engine/save entities are, how they relate, and what has and has not been established**. Avoid a chronology-led narrative and avoid a beginner tutorial on reverse engineering.

The four foundation subjects and exact intended output paths are:

| Subject | Guide | Technical reference | Essential distinctions |
|---|---|---|---|
| Outpost identity and membership | `docs/guides/identity.md` | `docs/reference/identity.md` | A saved owner association, physical Workshop root, active/registered outpost, beacon, UI list entry and canonical assembly are different things. Preserve 848 supported roots as **bounded evidence**, not an exhaustive active-player count. |
| Planetary location and position | `docs/guides/position.md` | `docs/reference/position.md` | Body, worldspace, saved site, beacon/reference, native centre, terrain cell, chart/face, local versus indexed XYZ and source anchor are distinct coordinate/identity domains. State validated horizontal limits and unknown loaded XYZ. |
| Nominal biomes | `docs/guides/nominal-biomes.md` | `docs/reference/nominal-biomes.md` | Discrete nominal base-biome coverage is not visually blended terrain, source BIOM, all deposits, available resources or usable/buildable outpost territory. Qualify source map, effective frame and boundary/seam assumptions. |
| Construction and placement | `docs/guides/construction.md` | `docs/reference/construction.md` | Catalogue visibility, recipe/condition eligibility, placement admission, actual placed object, budget/quotas, terrain/obstruction effects, variants and persistence are separate decision stages. Distinguish ordinary mechanisms from exceptional/untested CHANGE, override and restoration behaviours. |

A topic may need more or less depth than another. **Follow D5AY's evidence and navigation contract, not a rigid page length, diagram quota or identical heading list.** Cross-link these guides to each other and the completed resource-generation guide at consequential boundaries (e.g., a nominal biome does not establish extractor eligibility).

## 2. Frozen controlling questions

- **D5AZ-Q1 — Identity:** Can a new reader trace how an outpost is represented and associated with its placed objects, owners and saved forms, and identify the tested limits of membership claims, using exact accepted evidence rather than a GUI or registry shortcut?
- **D5AZ-Q2 — Position and biomes:** Can the reader distinguish the different planetary/site coordinate and biome representations, reconstruct the *qualified* geographic and nominal-biome mechanisms, and identify unvalidated transforms, seam and effective-area boundaries?
- **D5AZ-Q3 — Construction:** Can the reader follow discovery through eligibility, admission, placement and subsequent state/persistence, separating quotas, budget, scenery and variants with accurate native/save qualification and at least one genuine counterexample or negative result?
- **D5AZ-Q4 — Shared authoring, terminology and reader validation:** Are all eight pages internally consistent, accurately sourced, navigable from the guide/reference indexes, supported by appropriate auditable figures/tables, and independently readable/challengeable without relying on `.local-work/`?

**Question gate:** COMPLETE requires an accepted, evidenced answer in the agreed documentary scope. INCOMPLETE requires continued in-scope correction and REWORK; only an evidenced indispensable authority/input barrier qualifies for BLOCKED/ESCALATE. Do not stop at an editorial checkpoint. Historical research incompleteness is not itself a blocker to an honestly qualified guide.

## 3. Primary sources and required reading

Read the relevant portions **in full by substantive acceptance**, following linked corrections, reviews and original negative results; do not rely on titles or truncated excerpts. Record source-by-source application in a claim crosswalk.

**Standards and publication boundary:** `AGENTS.md`, `WORKFLOW.md`, `docs/CHARTER.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/VISUALIZATION_STANDARD.md`, `docs/PUBLICATION.md`, `docs/audits/publication-architecture-d5ax/architecture.md`, `docs/audits/publication-architecture-d5ax/migration-plan.md`, and the accepted D5AY deliverables. Reading chronology is not an acceptance criterion; complete substantive coverage is.

**Identity:** `docs/experiments/workshop-membership/report.md`, its `schema.md` / `validation.md` / `review.md`; `docs/experiments/workshop-population/report.md` and `review.md`; `docs/experiments/active-outpost-membership-completion.md`; appropriate RC1 and D5AT active-site results where the distinction matters.

**Position:** `docs/experiments/coordinate-sufficiency/report.md`, `repeatability.md`, `saves.md`, `review.md`; `docs/position-model/specification.md`, `review.md`, `capabilities.md`; relevant native/source and frame proofs in the position model and resource geometry work. Verify **which** saved and loaded frames any diagram refers to.

**Nominal biomes:** `docs/experiments/outpost-biomes/report.md`, `nominal.md`, `effective-and-resources.md`, `saves.md`, `review.md`; selected resource-availability and terrain/source material needed to prevent false conflation; D5AY's distinction among biome, source, deposit and available resources.

**Construction:** `docs/experiments/build-catalogue/report.md`, `eligibility.md`, `catalogue.md` and review; `docs/experiments/limits/report.md` and review; `docs/experiments/build-budget/report.md`, `saves.md`, review; `docs/experiments/spatial-placement/report.md`, `persistence.md`, review; `docs/experiments/construction-variants/report.md`, `saves.md`, review; relevant state/function registers. Do not silently replace failed historical geometry, photograph or reload attribution with a general rule.

**Release framing:** `docs/research-roadmap.md`, `docs/audits/publication-readiness-b1/claim-build-matrix.md`, `docs/audits/publication-architecture-d5ax/evidence-access.md`, and D5AW's publication-independence plan. These are **proposal/qualification inputs**, not permission to elevate a claim or release it.

Additional direct source/review links discovered while writing are part of the in-scope evidence task. Distinguish evidence consulted from references merely found by search.

## 4. Research-to-reader synthesis workflow

1. **Freeze the starting tree and scope.** Record HEAD, index, existing files, selected build/source pins, the original supplied brief's hash, material authority, protected-input rules and task-only outputs. Create a compact active claim/evidence ledger before substantial drafting. Separate historical evidence and current accepted authority.
2. **Build four claim crosswalks before writing definitive prose.** For each consequential claim capture: guide/reference section, native/save/CK identity or mechanism, applicable build and sample, exact research report and independent review, evidence basis (STATIC, SAVE, observed retail, control, inference), confidence and applicability, counterexamples, public availability tier, and unresolved external data needed to reproduce it. Do not promote a researcher's hypothesis into an observed mechanism through synthesis.
3. **Write the guides as explanations.** Open with the practical player/outpost question, then move through the normal path and its consequential exceptions, persisted versus runtime state, what the reader can actually conclude, and an evidence/limitations route. Historical experiment names are **citations**, not chapter headings or prerequisites.
4. **Write the technical references as mechanism maps.** Explain concrete native and serialized object types, ownership, identity/remapping, coordinate frames, inputs, predicates, writers/readers, output and failure boundaries. Use verified addresses/offsets selectively with build/VA/RVA and units clearly labelled; link the existing function/state registers rather than reproducing giant lists.
5. **Synthesize across the four documents.** Cross-check terms and relationships: an outpost's owner isn't its visual registry listing; saved beacon/site coordinates don't prove current runtime centre; nominal biome doesn't prove material deposits; being present in a build menu doesn't establish valid placement or the resulting persistent object. Add direct links to the D5AY resource-generation pair where explanatory dependencies cross that boundary.
6. **Extend the project glossary** `docs/reference/glossary.md` with necessary distinct cross-subsystem concepts and aliases. Every new definition must be **noncircular**, start from the actual entity type (runtime structure, saved record, CK form, reference, operation, UI construct, researcher term), and give purpose, meaningful distinctions and verified provenance. Avoid duplicating existing entries or claiming a recovered research label is an official Bethesda name.
7. **Update only bounded navigation:** `docs/guides/README.md`, `docs/reference/README.md`, and directly necessary new-page cross-links. Maintain the accepted pilot and existing experiment paths. A comprehensive root README redesign remains for coordinated documentation completion; change root only if an already-approved narrow navigation requirement explicitly needs it, and disclose why.
8. **Verify and review the exact proposed result.** Perform source-based review, calculations and figures, reader journeys, documentation validation, editorial screen, independent substantive/editorial review, corrected reruns and exact patch verification. Do not stop early because a reviewer accepted only an editorial checkpoint.

## 5. Figures, tables and navigation

Use appropriately scoped **editable Mermaid flowcharts**, state/ownership diagrams and concise tables for actual relationships. Examples: owner versus membership evidence hierarchy; coordinate-frame translation with declared origins and axes; nominal biome cell traversal and boundary cases; catalogue → eligibility → placement → persistence decision flow. A plot or spatial diagram needs authenticated plotted values, source, frame, units, bounds and explanatory caption. Do **not** invent a map of a saved outpost or a 150-unit circle without the proven centre/frame transform. Distinguish a conceptual diagram from measured output.

Review Mermaid/graphic syntax and, when supported, inspect actual renderings. If rendering is unavailable, record that precise limitation, use a readable text/table fallback and leave rendering as a later GitHub-facing visual check. No arbitrary minimum number of figures or new visualization infrastructure is required.

For each subsystem, test three reader journeys: **understand** a normal mechanism and its limit, **inspect or reproduce** one named available claim at its actually advertised evidence tier, and **challenge** a claim by reaching a direct original report, review, and qualifying/counterexample record. Links must resolve case-sensitively with heading fragments. Test current-facing paths without relying on deleted/moved historical sources. Each source-specific example must be honest about reproducibility and what it verifies.

## 6. Evidence availability and publication independence

`.local-work/` is disposable and **not a future protected archive**. It may currently contain evidence used to interpret historical reports, but a present private locator, hash or local receipt does **not** by itself establish an accessible public reproduction route. Do not relocate, delete, stage, upload or distribute any evidence under this brief.

For each material claim, label its advertised evidence level: inspectable tracked report/data; reproducible calculation with lawful pinned external inputs and documented method; proposed Release asset **PENDING RELEASE**; or historical observation whose decisive evidence still needs an approved derivative/asset. Mark an indispensable missing route **PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING**. A guide may be accepted as documentation while its selected *release claim* remains held for evidence access; do not silently downgrade the release gate or pretend an undocumented private file will survive publication.

B4-F1's 25 CORE original saves and 27 ADDENDUM files are provisional, not hosted or cleared. D5AS/C19 evidence derivatives and any selected new foundation evidence belong to separate claim-led packaging and rights review. Do not repeat the full 70 GB inventory. Preserve the source-version scope, `GPL-3.0-or-later` policy and Bethesda-derived-content rights boundaries.

## 7. Authority and safety

**Authorized:** offline reading of tracked research, appropriately protected existing local records when required and permitted by current project rules; source identity/hash checks; bounded arithmetic or synthetic verification; authoring the eight new Markdown pages, glossary additions, source/claim crosswalk and bounded guide/reference navigation; creating ignored verification receipts; independent review and correction in the same assignment.

**Not authorized:** launching Starfield/SFSE, Vortex deployment, live observation, debugger/Ghidra modification, save editing, protected-input restoration, game/installed content mutation, creation of new raw-capture evidence, importing new third-party implementations, broad documentation or experimental-history rewrite, moving/compressing/deleting historical briefs or audits, B4 evidence packaging, network publication, Git staging/commit/push or changing repository visibility. A read-only history/path check is permissible when needed for an exact attribution; a full new B6 history audit is not required.

Use the existing protected-save and evidence-integrity guards **when accessing protected data**; do not invent global 70 GB retention or force unnecessary archive reads. Verify the 40,000,000,000 caller-available-byte floor on **both C: and D:** before material local output work. If identity/integrity cannot be established, stop the affected operation, preserve what exists, and continue unrelated authorized documentation. No original is restored automatically.

**Sub-agents:** The general limit of **one concurrently active sub-agent** applies. A specialist and an independent reviewer may be used sequentially, not at the same time. Promptly disclose minor lapses and assess their actual effects rather than automatically failing an acceptance criterion; material compromise of independence, authorization, evidence, safety or budget remains consequential. No D5AV two-agent exception carries forward.

## 8. Frozen acceptance criteria (AC01–AC09)

| Criterion | Mandatory test |
|---|---|
| **AC01 — Governance and source coverage** | Required controlling standards, D5AY pattern and all material foundation reports/reviews read and **applied**; exact HEAD/input/authority protection and provenance documented. Reading chronology alone is not a criterion. |
| **AC02 — Identity pair / Q1** | Both identity pages give an accessible ordinary mechanism and technically accurate saved/native ownership model, including supported membership population and negative/exhaustiveness limits with review-linked evidence. |
| **AC03 — Position pair / Q2** | Both position pages distinguish all consequential coordinate/identity domains, reproducible **qualified** conversions and explicit unverified loaded/seam/frame claims. |
| **AC04 — Nominal biomes pair / Q2** | Both biome pages explain the correct discrete nominal traversal and its input/coverage conditions, distinct from deposits, UI availability and effective buildable area. |
| **AC05 — Construction pair / Q3** | Both construction pages accurately separate discovery, requirements, admission, budget/quotas, physical constraints, actual placement, persistence and variant limits, with decisive evidence and counterexample coverage. |
| **AC06 — Shared terminology and crosswalk / Q4** | Eight new pages and glossary changes are source-mapped; glossary definitions are concrete, noncircular, disambiguated and provenance-qualified; cross-subsystem terminology and historical supersessions are consistent. |
| **AC07 — Diagrams and reader usability / Q4** | Meaningful auditable visualizations and tables, source and units where needed; guide/reference indexes work; all three reader journeys tested per subsystem, with explicit rendering/access limits and no false links or invented reproduced inputs. |
| **AC08 — Publication boundary and preservation** | No release/evidence migration or unauthorized runtime/destructive action; `.local-work/` non-retention policy applied; indispensable private evidence access flagged; history and original findings protected; HEAD/index unchanged. |
| **AC09 — Independent review and exact delivery** | Genuine independent substantive, engineering/evidence and editorial review of exact final content; original criteria and highest-value omitted avenue challenged; failures preserved and corrected in scope; full and task-only byte-verified diffs, manifests, PASS/FAIL/NOT TESTED matrix, status, source/evidence crosswalk and handoff delivered. |

An accepted guide is **not** an implicit selection or clearance of every scientific claim for release. No silent amendment to these criteria after evidence arrives; any material change requires maintainer approval. Scientific scope and authoring correctness are separately evaluated.

## 9. Required handoff and continuation

Return Q1–Q4 as COMPLETE / INCOMPLETE / BLOCKED, AC01–AC09 as PASS / FAIL / NOT TESTED, and independent scientific, editorial and engineering dispositions separately. List all eight pages and navigation/glossary changes; explain which evidence routes remain pending. Give diagram inventories and whether rendering was actually inspected, reader-journey results, protected-input status, exact reviewed patch hashes, source and untracked inventories, and a proposed conventional commit message. Make no commit or publication claim.

An ordinary defect returns **REWORK of D5AZ**, not a new brief. A genuine terminal BLOCKED requires exact missing indispensable data/action, attempted authorized alternatives, reason, minimal authority/capability needed, and durable checkpoint. Continue in-scope work until acceptance or a justified blocker; editorial checkpoints do not end the assignment. The later batches B/C/D remain **unstarted and unauthorized**.
