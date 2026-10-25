# Codex research brief — RG2-D5G: Why some resource sources are predictable

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Authority:** Offline research and bounded read-only analysis only. **No Starfield launch/attach, live capture, game/save modification, staging, commit, push, release or publication.**  
**Status:** Implementation/research assignment; AC1–AC8 frozen below. B6 remains on hold.  
**Primary question:** Why can the existing model reproduce exact native resource-region geometry at the **original Feynman V**, **Carinae III-a**, and **Archimedes III** outposts, yet require an unknown source-construction query for other outposts—including the **second Feynman V** site? What differentiates those cases, and is the difference sufficient to predict resource geometry without an observed historical generation context?

## 1. Scientific motivation and non-negotiable distinction

The working hypothesis is that the procedural *geometry* generator is well reconstructed while *selection of its effective inputs* is less complete. **Do not treat that hypothesis as the conclusion.** A successful exact match might instead be conditional on runtime-supplied operands, source-selection choices, accidental invariance, or the narrow set of regions the native witness happened to expose.

Especially scrutinize the two Feynman V sites. They share the planet-level PNDT record, but **the original outpost spans two biomes**, while the second presents four mixed-mask source projections. Therefore neither “biome boundaries cause unpredictability” nor “the first site must be uniform because it matched” is acceptable without inspecting the actual source/query geography and native selection chain. A source can cross a biome boundary and still have a stable *effective construction mask*; a source wholly within one nominal biome can still have a varying mask or context under the engine's actual query transforms. Conversely, the originally successful outpost may merely have benefited from directly captured effective inputs.

Research the full relevant **PNDT → SFTR → SFPT → SFBK → BIOM → RSGD** lineage and any other *demonstrably relevant* planet-linked record or native selector. Do not presume that Feynman V has only one surface tree, one pattern, one block, or one relevant source instance. Enumerate actual installed relationships; do not invent alternatives. Trace node/branch selection, owner/root/component initialization, source identity, raster/mask sampling and the native demand caller separately. Distinguish graphical biome boundaries, installed biome selection, component descriptor selection, source-block selection and mask boundaries: these are different possible mechanisms.

## 2. Baseline, inputs and precedence

Start by reading the current repository guidance (`AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md` where present, `docs/SAVE_PROTECTION.md`, templates and independent-review guidance). Locate and cite, by real repo path and version/hash, the prior source-of-truth reports and comparison artifacts:

- D1 standalone exact native region controls, original Feynman V and Carinae III-a (four plus three controls); source/callback identity and exact matched binary32 geometry.
- D2/D3 Save52 inventory and the 19 recognized / 17 active-qualified cases; especially classifications and each prerequisite needed for replay.
- D4D/D4E Archimedes III construction and exact three-region controls; resolved component sixth slot and owner-map exchanges.
- D5 Feynman descriptor precedence and the 13 mixed-mask sources; D5A 26 mask alternatives, source matrix and discrimination comparison.
- D5B Phase B three exact **second** Feynman V native regions matching frozen mask 3, differing from mask 0; **no witnessed original query or generation epoch**.
- D5C source-pointer keyed process-local retained-population map and D5D ordinary coordinate/cell-demand path. These establish mechanisms, not an earlier outpost's unobserved history.
- D5E continuous-decision observer limitations, for context only. **Do not work on instrumentation in this assignment.**

Pinned executable version for provenance: Starfield 1.16.244.0, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Installed definitions and local primary evidence must be verified against their own recorded hashes before scientific use. Treat historical predictions, captured native outputs, installed definitions, and user screenshots as distinct evidence classes. Screenshots are positive visible/option observations, not complete geometry or negative inventory. Protected material is read-only and local-only; no raw proprietary payload or sensitive local path/bytes in the committed report.

## 3. Workstream A — explain the three successes at source level

Construct a **source-by-source, not just outpost-by-outpost**, matrix for the four original Feynman V native controls, three Carinae controls and three Archimedes controls. Include all relevant contributing source projections, including those that produced no accepted regions where the evidence supports their inclusion. Do not equate a control region with exactly one source, or one visible blob with one generated path.

For each case establish:

1. Planet/body and Workshop/beacon identity, geographic descriptor/frame, biome footprint and native source identity (geographic analytical key versus actual pointer).
2. Installed PNDT traversal into **all candidate** SFTR/SFPT/SFBK paths and any gating or precedence that chooses the effective path. Specifically test whether Feynman V offers distinct surface-tree, pattern or block branches for the two sites; record actual FormIDs, records, conditions and transforms. An absence conclusion requires enumeration of the relevant installed population, not merely a single resolved chain.
3. BIOM/RSGD, root/family, initialized components, candidate ordering and applicable ordinary/Special/Water selection. Identify which operands were independently derived, which were supplied by native runtime observations and which remain assumed/conditional.
4. Source-level construction-query mask uniformity *as a measured property*, when determinable, including raster cell boundaries and admissible sample domain. Explicitly mark untested/unknown domains.
5. Exactly why the historical prediction matched: invariant installed input; independent native selection rule; explicitly recorded native operand; conditional choice later validated by geometry; or ambiguity that does not affect these particular accepted regions.
6. Whether a competing viable input produces different native path bytes/regions but the same Workshop acceptance; do not mistake coincidence at the consumer for unique global source geometry.

Do not assign “uniform” merely because a predictor matched, or “nonuniform” merely because an outpost crosses a biome boundary. Preserve exact source/frame and confidence qualifiers from earlier work.

## 4. Workstream B — controlled two-Feynman comparison and broader contrasts

Perform a matched comparison of the **original and active second Feynman V** outposts. Fix shared PNDT and shared installed content first; then vary only independently established location/source-dependent operands. Examine differences across:

- PNDT-to-SFTR selection and whether there are multiple effective trees / branch routes;
- SFTR-to-SFPT selection; installed pattern overlays and FNAM/GNAM transpose/coordinate interpretation;
- SFPT-to-SFBK source blocks, relative origins and extents;
- BIOM/RSGD/component/root/family/rarity and effective overrides;
- terrain/biome transitions versus low-nibble mask boundaries;
- native original-query-to-raster conversion and the *domain of queries that can actually reach the same source*;
- data that depends on process-local source population retention or order of prior requests.

A comparison must be able to conclude **“same installed selector; different spatial mask”**, **“different installed source lineage”**, **“different component selection”**, **“native control supplied otherwise unknowable context”**, a mixture, or **unresolved**. Keep a separate category for evidence availability: the first Feynman V/Carinae/Archimedes exact controls may be easier to replay simply because key operands were witnessed; that is not automatically an intrinsic property of those sites.

Cross-check findings against Carinae and Archimedes as controls: Carinae's prior wrong SFPT/source anchor and Archimedes's sixth-slot/owner-map errors were **input/selection** errors, not proven failures of geometry mathematics. Determine whether their now-correct installed selectors are independently predictive without importing the observed native answer.

## 5. Workstream C — reachable-query invariance, not nominal-area invariance

Precisely define at least three nested domains for each inspected source when the evidence permits:

- **Nominal spatial domain:** the source's geographic footprint or raster block, which may contain multiple low-nibble masks.
- **Statically admissible caller domain:** construction query coordinates satisfying demonstrated native caller, transform, frame, source-enumeration and other gate conditions.
- **Actually witnessed demand domain:** observed runtime query locations, where they exist. This is not automatically exhaustive.

For every source in the ten native controls and all **13 frozen mixed-mask sources** (VI-b four, VII-b two, VIII-b three, second Feynman V four), compute or bound effective masks over each supported domain. If admissibility cannot be proven fully, present lower/upper bounds and an exact missing native condition; never label the unexamined remainder unreachable. Determine whether any nominally mixed source becomes **provably invariant over *all* statically reachable first-miss queries**. If not, say so.

Trace source enumeration/selection from ordinary coordinate or cell preparation (`D5D`) to the provider and original-query folding (`D5`), without assuming the beacon position is the triggering query. Verify how two distinct caller queries could enumerate the same live source and what still needs runtime proof. Do not search arbitrary masks to fit native paths. Keep construction-query/mask inference **separate** from empirical “mask 3 reproduces current D5B geometry”.

Where possible, compare alternative input vectors using the **unchanged frozen predictor**, quantifying ordered native resource paths, accepted area intersections and whether geometries are exactly equal versus merely same catalogue membership. Preserve competition/order coupling (e.g. second Feynman V Copper varies even at weight 1.0). Don't alter generator math, seeds, thresholds, geometries or input candidates to improve matches.

## 6. Workstream D — isolate decisive variables and assess generality

Produce a falsifiable **difference/causality ledger**, not just an inventory:

| Observed difference | Native/installed evidence | Changes effective generator inputs? | Necessary or sufficient for predictability? | Counterexample / limit |
|---|---|---|---|---|

Test candidate explanations in a reasoned order: (i) availability of witnessed runtime operands vs independent derivability; (ii) mask invariance over reachable queries; (iii) differences in SFTR/SFPT/SFBK selection; (iv) BIOM/RSGD/component selection; (v) source lifespan/retention only if needed. A correlation with biome count is not a causal explanation without its mask/selector mechanism. Distinguish *input uniqueness*, *output equivalence despite input differences*, and *observational underdetermination*. Answer which mechanisms the data **rules out**, not only which remain possible.

Deliver a concise plain-language answer to the user's questions:

1. Why were the first three outposts predictable exactly?
2. What is specifically different about the second Feynman V and other indeterminate sites?
3. Does the first Feynman V biome boundary actually create or fail to create construction-mask ambiguity?
4. Which planet-linked records matter, and which candidate record differences have been disproved or remain open?
5. Does the evidence support a general predictability criterion for *new* outposts?
6. What smallest missing static fact or live observation would change an unresolved case into a prediction?

If the analysis does **not** establish one decisive difference, explicitly report multiple contributing mechanisms and the exact distinguishing tests. **A scientific negative or ambiguous result is acceptable; circular explanation is not.**

## 7. Execution, reproducibility and evidence protection

- **Offline-only.** Existing Ghidra/native exports, pinned installed files, protected historical receipts, and existing repository research code may be read. No Starfield.exe live process, attachment, game state manipulation, save restoration or forced source regeneration.
- Keep all raw native exports, copies of installed records, private corpus, complete predicted geometry and screenshots in the protected/ignored local evidence location. Check save and installed-file pins before/after; fail closed on missing or altered protected inputs.
- Bounded scripts/tables are permitted to read the installed selector population, compute masks and replay frozen alternatives. Explain exact input provenance, native address domain, FormID versus source pointer and algorithm version. Prefer extending **research-only analysis** rather than mutating production/shared generator modules; no Outpost Tracker or in-game integration.
- Establish *independent* prediction provenance: capture candidate sets and the chosen selection rules before looking at exact native regions; where historical familiarity prevents strict blindness, disclose that and use mechanical freezing/competing-hypothesis comparisons. Never fit selector, seed or query to a known region.
- Maintain every inherited exact native control as immutable. If generated geometry or predictor code changes at all, rerun all ten exact controls; if not, verify their hashes/integrity and be explicit that this is **not** a rerun. Preserve frozen D2–D5E output classifications, D5B mask-3 observations, all Save52 source associations and all 13 mixed-source cases. No silent reclassification of the seven indeterminate historical associations.
- Use rigorous status labels: **STATIC/native-derived**, **INSTALLED**, **RUNTIME-witnessed**, **DERIVED conditional**, **SAVE-positive**, **SCREENSHOT-positive**, **UNKNOWN**. Distinguish source geometry, Workshop intersection, resource admission, and historical source-population identity.
- New live instrumentation is **out of scope**. If still necessary, provide one focused falsifiable next-test recommendation with missing operand, target source/transition, anticipated discriminating outcomes and confounders. A proposed run card must be marked **NOT AUTHORIZED**, and must not be substituted for scientific analysis.

## 8. Required durable deliverables

Use repository conventions for the exact destination. Suggested experiment directory: `docs/experiments/resource-predictability-contrast/`.

1. `report.md` — executive answer first, then method, comparative result, negative evidence, implications and unknowns.
2. `source-matrix.csv` — ten exact region controls mapped to contributing sources and provenance, with multi-source relationships shown explicitly; include every source needed for the controlled comparisons.
3. `feynman-lineage.csv` — installed record-chain comparison for both Feynman V outposts, including enumerated alternates, selection rules and hashes.
4. `query-domains.csv` / `mask-invariance.csv` — all 13 mixed sources plus successful controls, nominal/admissible/witnessed masks and proof status.
5. `causal-ledger.md` — candidate differences, necessary/sufficient status, counterexamples and independent falsifiers.
6. `methods.md` or equivalent bounded analysis scripts with pinned inputs, freeze discipline and repeatable command instructions.
7. `review.md` — frozen criterion matrix, exact substantive reviewer verdict and editorial completion, including any corrections and final narrow delta review.
8. Updated navigation/experiment index and durable provenance; complete/task-only verified git patches, SHA-256, exact file manifests and exclusions, including any pre-existing brief or unrelated workspace changes. Full raw receipts may remain LOCAL-ONLY.

Do not force predetermined filenames if current repo organization establishes a better consistent location; document the mapping. Make every table's keys and field semantics legible to future researchers.

## 9. Frozen acceptance criteria

**AC1 — Scope, authority and preservation.** Offline-only, pinned installed/native/save inputs, local-only evidence protection, baseline worktree audit; no retail action, staging or commit.

**AC2 — Honest successful-case audit.** All ten exact native regions and their source/selector prerequisites classified, explicitly separating independently derived inputs from native-witnessed/conditional inputs; no unsupported blanket claim that original Feynman V is uniform.

**AC3 — Two-Feynman structural comparison.** Enumerate and compare the actual installed PNDT/SFTR/SFPT/SFBK/BIOM/RSGD chain, selection precedence, source and coordinate frames for *both* Feynman V sites, including any other relevant planet-linked records, and account for the first site's biome boundary.

**AC4 — Reachable-query and mask test.** Explicit nominal versus statically reachable versus witnessed query domains; all 13 mixed sources and successful controls accounted for; no unsupported exclusion of possible queries or circular mask selection.

**AC5 — Explanatory discrimination.** Identify which factor(s) are necessary/sufficient/underdetermined for exact prediction; test counterexamples and alternative selectors; distinguish geometric equality from resource-option/area equivalence and observational luck.

**AC6 — Frozen scientific comparison.** Independent hypotheses and frozen geometry predictions remain intact, Save52 classifications not rewritten without new independent evidence, full ten native controls rerun only if their computational inputs/code change (otherwise provenance/integrity checked).

**AC7 — Durable and editorial completion.** Reproducible analysis, clear user-facing conclusions, precise provenance, no contradictory terminology, navigation and local/public evidence separation, protected-file/patch integrity verified.

**AC8 — Independent substantive and final-delta review.** Reviewer examines native/installed support, matrices, calculations, alternative explanations, failure modes, full exact snapshot and complete/task-only diff; independently records ACCEPT/REWORK/ESCALATE. Author corrects and resubmits until accepted or explicitly escalated. Review final completion-record-only delta separately. No claimed acceptance until its real receipt exists.

## 10. Completion contract

Before editing, identify HEAD, branch, dirty/untracked baseline and the exact supplied brief status. Before closing, report each AC1–AC8 with evidence path and honest limitations. Apply the project's independent completion-review workflow and `docs/EDITORIAL_STANDARD.md` if present. Report hashes/pin comparisons, syntax/tests, whether exact controls were rerun or merely integrity-checked, scientific coverage and correctness **separately**, and every unfinished question. Produce **complete and task-only** diffs matching the final workspace, independently validate forward/reverse reconstruction and hash each final patch; enumerate all changed, new and excluded paths. Never self-stage/commit/push. Do not claim new native observations where only static analysis or old evidence exists.

**Stop condition:** A reviewed, evidence-backed explanation (including bounded uncertainty) of why exact geometry was recoverable at the original Feynman V, Carinae and Archimedes controls and why unresolved sites differ. Only then recommend whether any further lifecycle instrumentation has enough expected scientific value to justify a separate assignment.
