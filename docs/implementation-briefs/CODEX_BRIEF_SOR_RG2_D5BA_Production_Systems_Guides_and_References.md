# Codex implementation brief — RG2-D5BA: Production Systems Guides and Technical References

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Task type:** Documentation synthesis, technical-reference authoring, and independent validation  
**Status:** Proposed assignment; execute only on the maintainer's separate instruction  
**Publication:** NOT READY / NOT CLEARED. Nothing in this brief grants release authority.  
**Scope:** Four production subsystems, eight new reader documents, shared glossary/navigation, review evidence. No new scientific investigation.

## 1. Purpose and audience

Continue the accepted D5AY resource-generation pilot and D5AZ foundation documentation batch. Explain how ordinary outpost producers are configured, become eligible, receive scheduling attention, consume fuel or ingredients where applicable, and ultimately provide power or items. Write for a reader familiar with reverse engineering and Creation Kit modding, but **not** with this repository's sequence of investigations, private observers, or brief IDs.

The deliverable is an accessible *current account* of the research, not a chronological digest of reports. Preserve the original reports, counterexamples and reviews; link to them to support and qualify conclusions. A page must distinguish established game behavior, instruction-backed conditional behavior, saved state, a derived calculation, reported operator observation and untested realization. The eight pages must stand on their own at the advertised public access tier and must not imply that `.local-work/` will remain available after publication.

## 2. Frozen controlling questions

| ID | Controlling question | Complete answer required |
| --- | --- | --- |
| **D5BA-Q1 — Inorganic extraction** | How does an ordinary inorganic extractor acquire its resource association and produce output, and which state is saved versus recalculated? | One guide and one technical reference explaining definitions/identity, placement versus registration, resource-keyed producer rows, current gates, interval and due-cycle path, outputs/links, restoration and material limits. |
| **D5BA-Q2 — Organic production** | How do ordinary greenhouse and husbandry producers select resources, determine knowledge/eligibility and operate? | One guide and one technical reference distinguishing planet/species/domesticability, flora versus fauna, knowledge/UI availability, recipe/water/other input requirements, current selection and production/restore paths; disclose unobserved current knowledge and husbandry coverage. |
| **D5BA-Q3 — Fabrication** | How do ordinary fabricators expose/select recipes and turn qualified inputs into products? | One guide and one technical reference covering construction variants and presets, supported recipe/catalogue identity, resource-property admission, reconfiguration and registration, ingredient-source graph, input caps/consumption, scheduling/output and saved versus current state. |
| **D5BA-Q4 — Power and generator fuel** | How is electrical generation selected and allocated, how do wiring and switching affect supply, and what survives save/load? | One guide and one technical reference covering definitions and conditional ratings, effective generation, fuel-gated operation, typed electrical graph, shortage/order rules, switches, saved flags/edges and load recalculation, including qualified Save29 outcome and historical contrary models. |

For **each** Q, completion requires correct technical depth, substantial accessible guide narrative, exact source/review links, concrete counterexamples, separate runtime/save coverage, independently verified navigation and claims, and a truthful public evidence tier. Do not classify a merely written file as Q COMPLETE if its core explanation is materially wrong or an in-scope evidence route remains misrepresented.

## 3. Exact new paths and permitted updates

Create these eight documents:

| Subject | Guide | Technical reference |
| --- | --- | --- |
| Inorganic extraction | `docs/guides/inorganic-production.md` | `docs/reference/inorganic-production.md` |
| Organic production | `docs/guides/organic-production.md` | `docs/reference/organic-production.md` |
| Fabrication | `docs/guides/fabrication.md` | `docs/reference/fabrication.md` |
| Power and generator fuel | `docs/guides/power.md` | `docs/reference/power.md` |

Also update **only as necessary** `docs/guides/README.md`, `docs/reference/README.md`, and `docs/reference/glossary.md`. Create a proportionate claim-to-evidence crosswalk and review/handoff record under a dedicated `docs/audits/production-guides-d5ba/` directory. Preserve the directory-local structure used by D5AY/D5AZ. Retain the existing root `README.md` and other broad public-navigation changes for the coordinated later stage unless an essential link would otherwise break. Do **not** move, rename, compress or delete any historical report, brief or audit.

The four guides and four technical references can be unequal in length. Follow `docs/guides/AUTHORING-STANDARD.md` as the common contract, not a rigid page template. Do not duplicate another subsystem's full reference to fill space.

## 4. Scientific boundaries and required distinctions

### Shared configured → eligible → scheduled → delivered model

Across the four subjects, explain **configured or registered capability**, **current eligibility**, **elapsed/due-cycle or allocation decision**, **accepted creation/transfer**, and **actual realized inventory or powered state** separately. This is a conceptual crosswalk; do not invent a single universal native state machine or pretend electricity is an inventory item.

- A saved property, visible menu row, nonzero nominal rate or cached eligibility byte is not a measurement of current operation or accepted output.
- Distinguish positive resource property *presence*, positive *selected value*, recipe identity, registered producer row, reference/base identity and current power/inputs.
- Where current power, actors, inventory, output capacity, time, load ordering or effective overrides are absent from evidence, state that the realized result is unobserved. Do not fabricate a formula for output counts.
- Distinguish direct producer insertion from accepted delivery to a selected connected receiver; the machine's own inventory may not be a sufficient output oracle.
- Explain which aspects are persisted, definition-inherited, recalculated, runtime-transient, or conditional on successful handle resolution and registration.

### Q1 — Inorganic extraction

Use the bounded E1 and later interval/rate findings. Cover native category recognition, ordinary solid/liquid/gas and exceptional categories only to the extent actually supported; resource AVIF → IRES → recipe/product association; point-geometry admission for **new placement** versus resource-keyed production by an **established** extractor. Include relevant positive saved examples and the scoped D5AH producer-continuity result without implying universal output across changed geometry. Separate powered state, halt predicate, production reason, elapsed interval, multiplier and outgoing local-link effects. Explicitly link to the resource-generation guide for geographic contours and to the future logistics reference for transport.

### Q2 — Organic production

Use E2 original reviewed findings. Distinguish planetary flora/fauna species and domesticability from the local biome and currently spawned wild actors. Explain what a known/unknown menu row means, when choice is supported versus currently selected, and how flora/fauna resource/recipe identity is recovered. Preserve the observed input distinctions (e.g. water and qualified dietary ingredients) and native effective input gates; do not treat knowledge UI and available ingredient stocks as one condition. Disclose limited saved husbandry coverage and missing actual live knowledge/rate/output values.

### Q3 — Fabrication

Use E3 and the exact installed recipe catalogue. Preserve **11 simple, 10 compound and nine ordinary multiplex products** as qualified main-file results; do not promote the exceptional Comm Relay to an ordinary tenth multiplex choice. Distinguish 45 category-qualified facility definitions from the 30 ordinary construction-linked presets, construction eligibility from output recipe selection, COBJ identities from IRES producer keys and ingredient AVs, and catalogue support from current input sufficiency. Explain selection-change effects on producer rows/countdowns, local reachable input graph and due-cycle caps, and what remains unknown about effective current stocks and accepted delivery. Do not turn this assignment into a storage or cargo simulation.

### Q4 — Power and generator fuel

Use P1 definitions/graph, allocation and switch follow-ups and the independently reviewed Save29 authority study. Distinguish planet-conditioned generator **ratings** from currently effective contribution, no-atmosphere build eligibility from a zero-output variant, and the ordinary mapped absence of solar time-of-day/weather operands from a universal statement about modded conditions. Explain the electrical topology and **cumulative, discovery-order demand allocation**, including the 10-supply / ordered 6,6,1 example with its applicable conditions. Avoid claiming global wired-first/unwired-first priority. Explain switch effects, saved ExtraCB connections and Extra9C bits versus recalculated post-load authority. The qualified Save29 ordinary load result supports a particular deterministic graph-based explanation, **not** universal settled-load convergence. Cover ordinary fueled generators' fuel and timing under their demonstrated path; explicitly route cargo-link Helium-3 fuel accounting to later cargo documentation rather than merging the two.

### Cross-subsystem boundaries

Inorganic geometry and placement are not equivalent to established extractor output. Organic menu knowledge is not runtime ingredient supply. Fabricator manufacturing *recipe* input is not necessarily its upstream stock origin. Power supplied by an electrical component is not simply all nominal capacity at the same outpost. General local output links and storage, cargo timing/He-3 transport, resource geometry and workshop catalogues have their own forthcoming or existing references. Provide brief context and accurate links, not duplicate in-depth treatment. Do not imply observations of operating instances where only definitions, saved examples or static native paths exist.

## 5. Mandatory source and governance grounding

Read complete relevant portions of the governing documents **by final substantive review** (not necessarily in a mandated order), and document how they shaped the output:

- Root `AGENTS.md`, `WORKFLOW.md`, `docs/CHARTER.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/VISUALIZATION_STANDARD.md`, `docs/PUBLICATION.md`, `docs/SAVE_PROTECTION.md`, `docs/templates/completion-contract.md` and reviewer procedure.
- `docs/guides/AUTHORING-STANDARD.md`; D5AY/D5AZ guides, references, glossary, their independent review and claim crosswalks; D5AX architecture and evidence-access plan; D5AW publication-independence decision.
- E1: `docs/experiments/inorganic-extractors/` `report.md`, `definitions.md`, `native.md`, `links.md`, `arithmetic-report.md`, `arithmetic-production.md`, `resource-intervals.md`, applicable reviews and exact source ledgers.
- E2: `docs/experiments/organic-facilities/` `report.md`, `native.md`, `links.md`, `saves.md`, reviewed definitions/species and sources, review.
- E3: `docs/experiments/fabricators/` `report.md`, `definitions.md`, `facilities.csv`, `recipes.csv`, `native.md`, `reuse.md`, `saves.md`, review and sources.
- P1: `docs/experiments/power/` `report.md`, `definitions.md`, `fuel.md`, `native.md`, `saved.md`, `followup.md`, `availability.md`, `save29-authority.md`, `save29-authority-review.md`, original review/source ledgers.
- Where relevant, D5AH extractor continuity, S2 local output links, resource-generation reference and the B1 claim/build matrix.

Filenames above are locators to verify, not authority to invent content or ignore renamed files. Resolve exact existing sources and read original qualifications, corrections, exceptions and independent dispositions. Follow additional direct references where indispensable to a claim. Do not rewrite older reports to make them agree with a new synthesis. Record contradictions and strongest-supported current interpretation with provenance.

## 6. Glossary, diagrams, quantitative examples and navigation

Extend `docs/reference/glossary.md` with shared terms actually needed for these four subjects. Definitions must be **plain-language, noncircular and concrete**: state if the subject is a native function, data structure, saved record, FormID, runtime property, callback, derived quantity or research label; describe what it contains/does, who owns or invokes it where established, and resolve material homonyms. Distinguish engine/CK names from researcher descriptions and retain historical aliases. One canonical entry per meaning; no invented ownership or implementation certainty. Avoid a quota or unnecessary glossary links on every occurrence.

Use **Mermaid** for inspectable decision, lifecycle, allocation or ownership diagrams where appropriate. Use tables and sourced plots for actual calculations, recipes, state conditions and example outcomes. Diagrams need a plain-text equivalent, a caption explaining scope/omitted branches and source links. For quantitative figures state denominators, units, time basis, effective operands and installed-game version; never dress a schematic or conditional calculation as retail measurement. Validate Mermaid syntax and, where tooling supports it, actually inspect rendered diagrams; otherwise disclose this as a later GitHub-rendering check. Follow the visualization standard rather than inventing an outpost overlay or source geometry.

Update the two local indexes and connect each guide to its reference, glossary and decisive original reviews. Verify three reader journeys **per subject**: (1) understand a normal producer or power path and a practical limit; (2) reproduce a bounded, available calculation or table with tracked data and lawful declared inputs, with no existing `.local-work/` reliance; (3) challenge the result by finding its original scope, counterexample and independent review. Report explicitly if a proposed reproduction tier is unavailable; do not substitute an untested claim.

## 7. Evidence independence and authority limits

`.local-work/` is **disposable** after publication; it is not a permanent private evidence vault. During this assignment, do not disturb any active local evidence or protected input. A reference to a local path or hash can support provenance but **cannot** close an indispensable public evidence dependency. Identify public tracked routes, genuinely reproducible methods with lawful inputs, or prospective approved Release assets. Mark missing indispensable historical inputs with `PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING` and the affected claim/strength, rather than quietly reducing the claim or fabricating public data. Current guide acceptance does **not** resolve B4 evidence or B6 clearance.

**Authorized:** offline reading of tracked research and non-invasive existing evidence where allowed by the project rules; creation/editing of the eight documents, named indexes and glossary, and task-specific audit/crosswalk/check files; appropriate static arithmetic and link/diagram tests using tracked inputs; independent review and in-scope corrections.

**Not authorized:** game/SFSE launch or deployment; new native experiments, reverse engineering, Ghidra database changes, save/config edits, installation or third-party sourcing; rewriting accepted historical evidence, archival compression/relocation, cleanup/deletion of `.local-work/`, evidence Release packaging, publication, Git staging/commit/push, tag/release or visibility changes. If a newly identified essential evidence access decision belongs to B4/B6, record it without doing that separate task. No extra engineering framework merely to write guides.

Use the **general maximum of one concurrently active sub-agent** for D5BA, either specialist or reviewer; sequential use is allowed. Do not inherit D5AV's temporary two-sub-agent exception. Promptly disclose any minor cap overage and assess actual impact on review independence, integrity, budget and safety; minor isolated lapses alone are not automatic criterion failures under the prospective rule. The independent reviewer must not accept their own authored correction.

## 8. Active investigation and completion contract

Create an active task ledger before substantial synthesis, with Q1–Q4/AC01–AC09, questions, source claims, negative cases, evidence gaps, correction history and completion status. Freeze this brief's criteria. Do not stop at an editorial checkpoint while in-scope scientific and writing work remains. Diagnose and remedy test/review failures within this assignment. Mark a controlling question `COMPLETE` only when its original scope is answered and the evidence/crosswalk/reader checks are adequate. `INCOMPLETE` means REWORK and continue; terminal `BLOCKED` requires a demonstrated indispensable missing input, action or authority plus alternatives attempted, impact and smallest resolution, resulting in ESCALATE. Do not relabel optional evidence-access work as completed publication clearance.

If reading unpublished/private source material or creating generated receipts, preserve original bytes and use task-local ignored scratch with nonoverwriting names, required identity/authorization checks and existing C:/D: caller-available space guards. Do not run a full protected save audit when protected files are not accessed; state the actual non-access boundary. Never claim tested runtime behavior from a synthetic table or a complete historical event without its original evidence.

## 9. Mandatory acceptance criteria

| Criterion | Required evidence / result |
| --- | --- |
| **AC01 — Governance, scope and evidence safety** | All mandatory reference content applied by final substantive acceptance; correct one-sub-agent limit; unchanged game/save/protected inputs and HEAD/index; no unauthorized action; active ledger and honest verification coverage. |
| **AC02 — Four guides** | All four specified guides exist, are technically coherent for new readers, explain runtime/save boundaries and consequences, cite current qualified research and material counterexamples, and avoid chronological brief-by-brief narration. |
| **AC03 — Four technical references** | All four specified references identify concrete definitions, native decision/data and ownership boundaries, conditions, save/restore roles, failures and consequential limits, with exact source and review routes. |
| **AC04 — Critical production distinctions** | Each subsystem correctly separates configuration, eligibility, scheduling/allocation, and realized output/state; E1 placement versus established production, E2 knowledge versus stock, E3 catalogue versus recipe-input supply, and P1 allocation versus persisted flags are explicitly verified. |
| **AC05 — Quantitative and historical accuracy** | E3 ordinary 11/10/9 and 45/30 counts, qualified E1 intervals, E2 recipes, P1 topology/order and Save29 conclusions agree with original reviewed records. No fabricated realized rates, UI measurements or universal load guarantee. Original disagreements and exceptional cases are traceable. |
| **AC06 — Glossary, visualization and navigation** | Concrete noncircular shared glossary additions; appropriate auditable figures and text equivalents; both indexes updated; all new/affected current-facing relative paths and heading anchors checked; rendering status disclosed. |
| **AC07 — Reproduction and evidence-access boundaries** | Claim crosswalk identifies build, evidence basis, original source/review, counterexample and access tier; 12 subject-specific reader journeys tested; runnable checks use available inputs without permanent `.local-work/` assumptions; missing indispensable historical evidence remains an explicit release dependency. |
| **AC08 — Editorial and independent review** | Full changed prose/manual contextual inspection and bounded editorial screen; independent scientific/completeness, engineering/evidence and editorial review of exact final snapshot; defects receive correction and relevant re-review. |
| **AC09 — Delivery accounting** | Complete file inventory, source and changed-path hashes, guarded outputs, PASS/FAIL/NOT TESTED matrix, Q1–Q4 status, preserved failed checks, independent decision, exact verified task-only/complete diffs with forward/reverse reconstruction and status; no staging/commit/push. |

## 10. Required final handoff

Return concise links to the eight authored pages, updated index and glossary, claim crosswalk/review, sample verification receipts and source/diagram caveats. State each Q1–Q4 disposition and AC01–AC09 result separately from scientific confidence and publication access. List genuinely unresolved dependencies for B4/B6 without proposing another D5BA implementation cycle to package evidence. Provide exact final diff/manifest identities, independent substantive/editorial disposition, protected-input non-access or checks actually performed, and an appropriate proposed commit message. Leave integration to maintainer approval.
