# Codex implementation brief — RG2-D5AY: Resource-Generation Reader Guide and Technical-Reference Pilot

**Project:** `D:\Projects\starfield-outpost-research`  
**Task:** Documentation synthesis, visual explanation and independently reviewed reader validation  
**Date:** 2026-11-07 (Australia/Sydney)  
**Authority:** Maintainer-approved *single-subsystem* pilot of the D5AX reader architecture. This document authorizes bounded authorship, navigation and associated documentation checks **only**. It does not authorize gameplay, SFSE deployment, Ghidra or native experiments, save alteration, publication, Git staging/commit/push, archive migration, or evidence redistribution.  
**Release state:** `NOT READY / NOT CLEARED`. Do not change it.

## 1. Purpose and audience

Deliver an accessible **but technically substantive** entry point to Starfield's *outpost resource generation*: a single coherent guide, a deep technical reference, and a reusable authoring framework for the remaining subsystem guides. The intended reader is **already familiar with reverse engineering and/or Creation Kit modding** but has not followed this project's long research history. Do not assume familiarity with D5-series identifiers, local source-frame conventions, project-specific observers, the historical Feynman V experiments, or where the decisive evidence lives.

This is **not** a new scientific investigation, a source-code rewrite, a comprehensive terrain-generation manual, a guide for altering game resources, or a complete public release. It should synthesize established observations and interpretations, state necessary conditions and limits exactly, and make the original evidence and negative results easy to reach without forcing readers through investigation chronology.

The approved D5AX layers are:

1. `docs/guides/resource-generation.md` — current-facing explanation; practical outpost consequences and conceptual machinery first.
2. `docs/reference/resource-generation.md` — technical native/save/input/ownership and evidence contract, with exact qualifiers and source locators.
3. Existing `docs/experiments/`, reviews, technical registers and historical documentation — preserved as the research record; **do not move or archive** them here.

Also create or update minimal `docs/guides/README.md` and `docs/reference/README.md` indexes as needed, with restrained navigation from existing entry points. Produce a reusable **guide/reference authoring specification**, proposed at `docs/guides/AUTHORING-STANDARD.md` (or a clearly justified equivalent), for subsequent subsystem authors. Do not author the other 17 subsystem guides.

## 2. Frozen controlling questions

**D5AY-Q1 — Framework.** What repeatable structure, depth, provenance notation, visualization approach and navigation contract will let a technically capable reader understand a subsystem without reading its chronological research files? **COMPLETE** means a documented, piloted standard distinguishing current-facing guide, technical reference, decisive evidence and historical review; not just a proposed outline.

**D5AY-Q2 — Reader guide.** Can a new reader explain the established ordinary resource-generation journey, why final geography can vary, and why apparent persistence is not proof of retention? **COMPLETE** means a coherent, technically accurate authored guide with explicit observed-versus-conditional statements, working links, suitable figures/tables and a practical outpost-facing explanation.

**D5AY-Q3 — Technical reference.** Can a specialist locate and assess the exact mechanisms, identity domains, input contracts, native and saved-state boundaries, competing explanations and reproduction/access qualifications? **COMPLETE** means the page supplies verifiable, source-backed mechanism tables, predicates, important native locators, data representations, observed results, confidence boundaries and evidence access tiers.

**D5AY-Q4 — Reader and evidence validation.** Can an independent reviewer navigate guide → technical explanation → original evidence and review → historical limitations and repeat an *advertised available* check without the existing `.local-work/` directory? **COMPLETE** means actual tested journeys, verified figures and links, evidence-tier honesty and independent scientific/editorial acceptance of the exact final pages. This is a documentation pilot; unavailable later-approved raw evidence may remain a disclosed **publication dependency**, not a pretext for fabricating reproducibility or a reason to perform an unauthorized release-evidence task.

Preserve these question IDs. Treat mandatory deficiencies as REWORK of this same task; do not stop at an editorial checkpoint or downgrade a mandatory item to optional without recorded maintainer approval.

## 3. Mandatory baseline and source selection

Read and apply the complete relevant content (including truncated continuations) of:

- Repository `AGENTS.md`, `WORKFLOW.md`, `docs/CHARTER.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/VISUALIZATION_STANDARD.md`, `docs/PUBLICATION.md`, `docs/PROVENANCE.md`, `docs/SOURCES.md` and the compact `docs/templates/completion-contract.md`.
- D5AX `docs/audits/publication-architecture-d5ax/architecture.md`, `migration-plan.md`, `evidence-access.md`, relevant dependency rows and reader-journey specification; D5AW's `docs/audits/deferred-work-d5aw/publication-plan-amendment.md` and publication independence rule.
- The original `resource-generation-gameplay-checklist.md`, D5AU `d5au-gap-closure-decisions.md`, D5AV `d5av-report.md`, `d5av-player-action-matrix.md` and `d5av-cache-decision-matrix.md`.
- Decisive native/geometry evidence: D5R, D5S, D5T, D5U, D5V, D5W, D5AE, D5AF, D5AG, D5AH, D5AK, D5AL, D5AO, D5AQ, D5AS and D5AT reports/methods/reviews as relevant; D5AQ qualified C1 mask census; D5AS series closeout and producer profile; D5AT active-outpost associations; D5AH extractor continuity.
- Outpost/UI consumers: `docs/experiments/native-availability-map/output-contract.md`, its reviewed continuation, and any necessary nominal-biome, region-geometry and extractor documents. Avoid turning this into C19's separate evidence packaging task.

Use exact existing paths determined from the repository; this list is a routing guide, not permission to invent document names, native assertions, session observations or missing inputs. Build a claim→source/review crosswalk before writing decisive synthesis. Consult deep original reports selectively where a current summary lacks proof or qualified counterexamples. Earlier historical verdicts remain historical; the D5AU/D5AV decisions are current-scoped dispositions, not retroactive rewrites.

Required reading may occur in any chronology provided it is demonstrably complete and applied by final review. Reading order is **not** an acceptance criterion.

## 4. Reader-guide content contract

The guide must be organized as an explanation, not D5-series history. Cover at least:

1. **What is being generated?** Geographic source, outpost site/build area, resource identity, raster mask, generated regions/points, and why those are distinct. Explain that source geometry is not automatically all deposits inside an outpost boundary; nominal biomes and displayed Available Resources are other products.
2. **From ordinary demand to source population.** Valid frame/context, source selection, density/layer request cohorts, visited-token check, protected pointer-map lookup, first eligible map miss, original request's coordinate reaching the raster sample, generation, holder/collection ownership and consumer access. Describe timing-dependent winner selection without claiming uniform chances or a central canonical selector.
3. **Why geometry can differ.** Qualified Feynman C1: 196 original request coordinates with 28 mask `0x0` and 168 mask `0x3`; these are **candidate counts**, not measured winner probabilities. Fixed-input mask0 and mask3 geometry differ. D5AS: 30 qualified cold starts, two complete mask-0-reference-equivalent bodies, 28 mask-3-equivalent, zero other qualified; historical generating masks and winning requests not captured in those snapshots. Explain confidence and the scope of the 6.67% observed proportion. Other D5AT outposts have conditional candidates, not retail outcome-frequency estimates.
4. **Why deposits appear persistent.** Distinguish resident geometry, true map hits, visited bypass, copied Workshop resource lists, narrower retirement/Grid clear, broad reset, and fresh reconstruction. D5AK Feynman V → Lodge **exterior** → Feynman V is **rebuilt identical** with two distinct directly measured mask-3 samples. Neither same-area travel nor all planetary/system travel has a universal established rule. Save52's audited channels restore descriptors, PCM and separately persisted producer state rather than serialized full contour arrays.
5. **Outpost consequences.** Workshop available-resource display versus geometry generation; extractor placement point testing versus established extractor resource-keyed production; separate current power/capacity/registration gates; what a player can and cannot infer about identical deposits or attempts to reroll them. Never offer an unverified universal reroll recipe.
6. **Limitations and publication tier.** Clearly separate native proof, observed retail construction, qualified fixed-input controls, derived analysis and unresolved questions. The guide is a synthesis of pinned Starfield `1.16.244.0` research, not a proof covering every build/mod/load order or all effective generation paths.

Readable prose, short explanatory examples and tables are encouraged. Introduce project-specific symbols and acronyms before use. Do not reduce the guide to lists of function addresses. Link prominently to the reference and to the original report plus its review for each key claim.

## 5. Technical-reference content contract

Present a cohesive technical contract rather than a chronological digest. Include:

- A terminology/identity-domain table: source geographic key, body/terrain FormID, saved outpost identity, Grid/source allocation, source token, pointer-map key, population holder, nested collections, original Int2 request, mask, native frame, observed capture ID and producer reference/handle. Explicitly distinguish these domains.
- A mechanism diagram and qualified pseudocode or decision table for visited check → pointer-map hit/miss → raster sample/generator → retained geometry; identify where allocation and visited-append failures prevent unconditional claims. Do not portray a synthetic pseudo-flow as complete native instruction-level control flow.
- A source/reader/owner diagram: Grid owner and source allocation, ProcGen pointer-map, holder/collections, visited store, Workshop spatial reader and existing producer rows; explain shared/exclusive locking and important lifetime guards at the actual audited scope.
- A lifecycle transition matrix: movement under threshold, overlap-preserving shift, nonoverlap retirement, Grid clear, broad reset, full save load, same-process departure/return, new-process restart, consumer/cached list, and the actual observed D5AK case. Separate **native predicate** from **player action**, and mark actual observed versus conditional or unknown action mapping.
- A qualified data-flow and generation input table: descriptor, raster/BIOM/RSGD, source and request coordinates, original-query conversion, ordered definitions and seeds, generation origin/clip, ordinary versus Special/Everywhere and any held-fixed operands; link to D5AQ and native controls rather than asserting global exhaustiveness.
- Complete-geometry and empirical-evidence comparison table: D5AQ conditional masks, D5AG fixed-input bodies, D5AK rebuilt-identical A0/A1, D5AL fresh independent equal pair, D5AO directly observed query/mask and D5AS 2/28 historical full canonical comparisons. Respect distinct canonical-body versus envelope representations and byte domains; use precise labels rather than conflating them.
- Source/build/provenance tables linking exact original reports, observed episodes, native/static claims, negative controls, confidence and source locators. Use existing function/source registers for addresses, offsets and binaries instead of transcribing thousands of locations. Show a minimal, decisive native locator set when it adds technical value.
- Save/load and established extractor association boundaries; don't conflate serialized producer resource keys with saved geometry.
- Reproduction/access table: which tables, scripts or arithmetic can be checked from tracked repository and lawful external installed inputs, what optional B4-F1 Release assets are still provisional, and which historical native capture operands remain private/unavailable pending a separately authorized evidence derivative. A hash and `.local-work/` locator are **not** public evidence access.

This page should stand on its own for specialists, while linking to source reports, negative cases, and reviews in stable `docs/experiments/` paths. Avoid publishing proprietary disassembly, bulk native exports, raw captures, game executable/data files or unverifiable synthetic claims.

## 6. Visualizations and diagrams

Use diagrams, tables and plots **where they materially improve understanding**, not to meet a decorative quota. The content strongly warrants at least a request/decision-flow diagram, source/holder/consumer ownership diagram, retention versus reconstruction lifecycle depiction, and a clearly labelled comparison of **candidate mask shares** versus **observed retail geometry-class shares**.

Prefer GitHub-renderable **Mermaid** for flowcharts and simple source-owned **SVG** or Markdown tables for figures requiring precise comparisons. Version-controlled chart input data should derive from tracked approved counts/values and provide exact source references. Do not invoke internet image search or generate decorative imagery. No arbitrary 3-D image, invented outpost boundary overlay, nonverified geographic placement, or unqualified curve smoothing.

Follow `docs/VISUALIZATION_STANDARD.md` for domain, coordinate frames, source masks, axes/units, stable colors and actual validated geometry if spatial figures are used. For statistics distinguish 28/196 candidate cells from 2/30 observed full-geometry classes and note that neither implies IID/uniform request scheduling. If statistical intervals are presented, label their IID assumptions and source. Inspect rendered GitHub Markdown/Mermaid/SVG appearance where feasible using safe local methods; report any rendering limitation explicitly. Figures must be accessible through captions, textual descriptions and adjacent exact-data tables.

## 7. Navigation, evidence independence and boundaries

Provide minimal navigation from existing `README.md` and/or `docs/research-roadmap.md` to `docs/guides/README.md` and the new resource guide; guide to reference in one click; reference to decisive report **and review** in one click; and a route to historical interpretation or a negative result. Do not turn this pilot into a broad migration of other subsystem links or reorganize existing research reports.

**`.local-work/` is disposable after publication.** Current authorship may read relevant existing historical summaries, but guide/ref claims may not advertise private files as if downloadable. A chosen indispensably historical empirical observation with no cleared public evidence route must carry `PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING` (or an equally unambiguous public-facing qualifier), cross-referenced to D5AX's claim dependency graph, without deleting or downplaying the original observation. The guide can distinguish *reported/scientifically reviewed* evidence from *publicly independently reproducible* evidence. Publishing a compact D5AS or C19 derivative is separate later work and **is not authorized here**. B4-F1 save selections remain proposed, not hosted; no invented release URLs.

No existing research report, review, historical brief, audit, dataset or source path may be relocated, archived, deleted, or semantically rewritten here. Do not update `docs/PUBLICATION.md` to READY or claim the first-release scope has been approved. No release packages, local-work cleanup, Git history change or external disclosure.

## 8. Method and execution safeguards

- Work from the current committed tree. Before edits, record HEAD, index and working-tree status, plus the existing provided brief identity. Do not incorporate or overwrite unrelated local changes.
- Use bounded read-only analysis of tracked materials and only necessary private receipts, if safely accessible and already authorized. Avoid bulk reads or packaging of 70 GB local corpus. Do not read protected original saves, game proprietary inputs or launch installed analysis tools to support a writing task.
- Write only authored pilot pages, narrowly needed navigation, authoring standard and durable task report/ledger. Diagnostic fixtures, draft renderings and review receipts may be created in fresh ignored task-owned scratch; protect live evidence and refuse overwrites.
- Keep the caller-available free-space floor of 40,000,000,000 bytes on **both C: and D:** before significant scratch operations. Stop affected writes on a guard failure; do not clean or alter protected data without authority.
- **Maximum one active sub-agent at a time** under the general D5AT rule. A specialist and independent reviewer may work sequentially only. Record any minor overage and assess actual consequences; promptly disclosed nonmaterial lapses are not automatic criteria failures, whereas material evidence, reviewer independence, authorization or safety effects can be failures.
- Use an independent substantive/completeness reviewer and independently check all final changed prose and figures. Reviewer cannot approve its own substantive edits. The delivery requires exact final-snapshot validation and all mandatory-criterion accounting.
- No stage/commit/push, release, tool installation, network publication, game operation, SFSE/native deployment, save modification or Git-history rewrite.

## 9. Required outputs

At minimum:

1. `docs/guides/resource-generation.md` — finished guide, not outline.
2. `docs/reference/resource-generation.md` — finished specialist reference, not outline.
3. `docs/guides/AUTHORING-STANDARD.md` or equivalent reusable pilot-derived structure/design contract.
4. `docs/guides/README.md`, `docs/reference/README.md` and only narrowly necessary entry-navigation changes.
5. A durable D5AY claim/evidence crosswalk and completion report (e.g. `docs/audits/reader-pilot-d5ay/README.md`, `claims.csv`, `review.md`), with exact chosen names documented and minimal administrative clutter.
6. Task-local evidence and test receipts, editorial screen results, link/figure validation, final file inventory, independent review and verified exact task-only/complete diffs.

Do not add the bulk D5AX inventories to reader-facing guide directories. All task-owned new archival evidence is **authored documentation only**, not primary retail/native experiment evidence.

## 10. Mandatory acceptance criteria (AC01–AC09)

**AC01 — Scope, governance, and preservation.** Mandatory source content actually read and applied; starting tree/HEAD and chosen inputs recorded; current tree changed only within this authorized documentation scope; active evidence untouched, no prohibited operations. Sub-agent cap observed or disclosed and consequence-assessed; historical decisions and protections preserved.

**AC02 — Complete tested authoring framework.** A reusable structure and evidence/notation/visualization convention exist and demonstrably govern the delivered pilot. It addresses newcomer-to-project assumptions, not newcomer-to-RE/Creation-Kit background.

**AC03 — Reader guide is substantive and accurate.** The guide covers generation, competing requests/masks, complete output variation, apparent retention, reset/save and outpost consumer/producer consequences in coherent order, with all material scientific qualifiers and sources preserved.

**AC04 — Technical-reference completeness.** The reference covers identity types, native decision/lifetime/reader rules, input and output frame contracts, saved reconstruction, exact major evidence and negative cases, evidence tier and specialist source/review navigation. No pseudocode or address is presented as stronger evidence than supported.

**AC05 — Figures and data verified.** Relevant editable/inspectable diagrams, at least one useful distribution comparison and supporting exact data tables are present. Native/observed/conditional distinctions, visual domain and count denominators are explicit. All diagram/chart facts cross-checked against frozen source records; appearance, legibility and accessibility assessed. No invented source geography or misleading probabilistic comparison.

**AC06 — Evidence independence and public honesty.** All decisive claims have live tracked links and evidence-access classification. No false public `.local-work/` links, fake Release URLs, unapproved payloads or claims of full event reproducibility. Indispensable unprovided historical evidence is an explicit unresolved **publication dependency** rather than silently treated as available. B4-F1 and C19/D5AS separate release work remain unchanged.

**AC07 — Reader journeys and navigation.** From project entry point, a reviewer can reach resource guide within two clicks, its technical reference within one further click, decisive report/review and challenge/supersession in direct links. Validate exact relative path, heading fragment, casing, Mermaid syntax and local links for changed paths. Run at least one tracked-input computational/table check with clearly disclosed availability limits, without existing `.local-work/`.

**AC08 — Scientific consistency and editorial quality.** Every important claim/figure has a source and evidence strength; comparisons and caveats reconcile with D5AU/D5AV/D5AS/D5AT and original decisive reports. Entire changed prose set manually reviewed and editorial screen performed; independent scientific and editorial reviewer covers exact final bytes. No material source contradictions or fabricated citations.

**AC09 — Verified handoff and independent acceptance.** Q1–Q4 map to PASS/FAIL/NOT TESTED criterion matrix with COMPLETE/INCOMPLETE/BLOCKED outcomes, explicit limitations, historical preservation, exact manifest, original/reviewed file hashes, verified task-only and complete diffs with forward/reverse reconstruction, and independent ACCEPT/REWORK/ESCALATE disposition. Any remaining mandatory deficiency is REWORK rather than declared complete. No Git integration/publication is performed.

## 11. Negative results, escalation and completion

A scoped documentation pilot may show that a historical observation is not publicly independently replayable yet. That does **not** make scientific evidence disappear or authorize invention. Preserve the observation and mark its release-access dependency. If a source is contradictory or absent and the **guide's required scientific explanation** cannot be supported, pursue available authorized references and correct the output; return REWORK if a material tractable synthesis gap remains. Only report **BLOCKED / ESCALATE** for an evidenced indispensable missing resource/authority/capability after authorized alternatives have actually been exhausted, with the narrowest requested action and durable resume evidence. Do not reclassify a broader publication problem as a reason to stop this independent pilot.

A small visual or editorial defect warrants fixing and resubmitting under **D5AY**, not another implementation brief. An independent reviewer must challenge each controlling question, evidence accessibility, missing counterexamples, invented universality, guide usability, and the highest-value omitted source. Preserve first failed reviews and corrective rounds, but do not stop at them. Completion requires **all four controlling questions COMPLETE and all nine mandatory AC PASS**, followed by maintainer critical review and integration decision.

**Return:** Concise scientific/editorial/engineering disposition; new/changed files and exact paths; link and reader-journey results; diagrams/tables and sources; pending D5AS/C19 evidence-access decisions; independent exact-final-byte review; no-authority boundary; proposed conventional commit message; both verified diff paths. Do not stage, commit or publish.
