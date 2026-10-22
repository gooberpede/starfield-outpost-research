# Codex continuation brief — RG2-A1-F1: Mature vein observation and geometry reconciliation

**Task type:** Focused offline research continuation, documentation correction, independent critical review and cumulative delivery. **Repository:** `D:\Projects\starfield-outpost-research`. **Authority:** The maintainer will provide this brief to the *existing Codex session before any RG2-A1 commit*. It does not replace the original RG2-A1 frozen criteria or authorize a new general investigation.

## 1. Why this continuation exists

RG2-A1 reconstructed the Creation Kit seed lineage, mature ordinary-initialization inputs and conditional geometry predictions for active Save52 outposts **Feynman V Cu Co Ni IL** (mixed biome) and **Carinae III-a Rc Fe** (single biome). The independent reviewer accepted its **qualified offline** scope. Subsequently, the maintainer asked exploratory questions, supplied **eleven in-game Save52 screenshots**, and corrected an earlier statement: **Feynman V Cu IL F is NOT deleted**. Some durable documents were changed following those informal exchanges, after the reviewed snapshot was packaged. The current cumulative diff therefore differs from the formerly accepted patch; neither its new observations nor the changed bytes have received a fresh independent review.

The screenshots materially challenge the predicted *mature resource presence and geometry*, especially **Ionic Liquids at Feynman** and **Iron at Carinae**. The Copper resource patch at Feynman appears notably circular; this is a **geometry clue**, not proof of a new primitive. The terrestrial-style Water extractor is present although the model predicts no localized Water vein. This may follow an already identified alternative extractor-admission mechanism; investigate its actual branch rather than automatically treating it as a vein failure.

**Goal:** Account for observed-vs-predicted contradictions as far as the accepted native paths, frozen predictions, saved state and supplied screenshots allow; correct or qualify the current mature model accordingly; bring **the entire final cumulative RG2-A1 snapshot** through a fresh independent review before commit. Do not hide a real mismatch behind generic cache/epoch uncertainty, and do not force an explanatory correction without evidence.

## 2. Inputs and precedence

Read before analysis:

- Original invoked RG2-A1 brief, frozen AC1–AC8, RG2-A1 `report.md`, `review.md`, `seed-lineage.md`, `sources.md`, `predictions.md`, `predictions-mature-v1/v2.json`, `points-mature-v1/v2.csv`, and `post-review-screenshots.md` / `.csv`.
- The **current uncommitted working tree**, its actual `git status`, and both the previously independently reviewed RG2-A1 snapshot and the newer cumulative full diff. Recover exact snapshot identities and distinguish changes made *after* acceptance.
- Accepted RG1 native/geometry/evaluator, RG2-A `prediction-contract.md`, resource-availability native admission work, B1 biomes, L3 restrictions, and Save52 identity / Workshop membership research. Existing reviewer counterexamples (sphere broadphase, source frames, early exits) remain valid.
- The maintainer's **eleven in-game screenshots and descriptive observations**, retained/protected under the actual local evidence paths listed in `post-review-screenshots.csv`; verify file existence, SHA-256 and mapping before analysis. Do not infer pixel geometry, numerical coordinates or a saved-reference join that the screenshots cannot support.

Evidence hierarchy: installed definition/native instruction support, original saved identities, independently observed UI screenshots, qualified model predictions, hypotheses. **Native predictions are not a substitute for new observations; UI screen patches are not automatically the same as the generator's internal shape.** Preserve original prediction files as immutable historical baselines and version any new model/prediction.

## 3. Research tasks

### A. Reconcile the observations in a claim-level table

For **each resource** shown or predicted for the two mature outposts, tabulate: nominal radius-150 *bounded_region* result; *tapered_strips* result (including UNKNOWN); in-game presence and distinct visual patches; existing extractor and its source/reference evidence where available; and whether the screenshot shows admission success, a red failed placement, or merely a coloured patch.

Explicitly analyze:

- **Feynman:** Nickel, Cobalt, Copper, Ionic Liquids, Fluorine and Water. Ionic Liquids is the primary previously predicted-absent/observed-present discrepancy. Record whether Fluorine's absence from the visible extractor list is actually probative. Water is a separate admission-path question. The apparent circular Copper region is a shape control.
- **Carinae:** Alkanes, Iron, Rothicite. The player observes approximately two distinct Iron patches and two Alkanes patches, and visibly distinct Rothicite geometry. Do not equate connected visible regions with generator path counts.
- Distinguish *resource definition available*, *generated resource region*, *displayed extractor option*, *placement preview overlay*, *successful extractor construction*, and *placement rejection*; a red ghost caused by radius overlap or out-of-build-area is not evidence of resource absence.

### B. Explain geometric primitives before changing the generator

For the **Feynman Copper** candidate, inspect existing generated output (including path count, **single-point paths**, point radii/widths and source membership) and compare at least:

1. Single-point **disk** geometry (and native single-point convention).
2. Unions of multiple disks and short paths producing one nearly circular visible patch.
3. Native bounded-region disks/rectangles and sphere broadphase versus **tapered-strip** availability geometry.
4. The separate raster / displayed extractor-placement visualisation, *if* an actual consumer mapping can be established from evidence.

Test the same representations against the disconnected Iron and Alkanes patches at Carinae. A screen image cannot by itself prove disk geometry or exact circularity. Do not manufacture polygon coordinates from camera perspective. If the predicted regions cannot be registered to screenshots spatially, state precisely what additional common-frame evidence would allow it.

### C. Investigate the source-context mismatch causally

Use the existing RG2-A1 provenance to test whether one or more **specific** assumptions cause resource absence or misplaced regions: manager owner/key; source-frame selection and transforms; selected BIOM/resource family/RSGD; atmosphere/effective state; resource masks/weights; procedural RNG consumption; source lifetime/cache or historical saved epoch; geometric consumer mismatch. Prioritize competing hypotheses with actual evidence; do not embark on an engine-wide search or invoke Russell's-teapot alternatives.

Where permitted, recover constructed extractor references and positions from Save52 as **independent positive spatial witnesses**, distinguishing saved hardware location from exact vein/source area. Determine whether predictions can be discriminated using these saved observations without relying on post-hoc fitting. Any adjustment must have a supported native/definition/saved basis and be evaluated on held-out cases; no arbitrary offsets or tuned seeds.

### D. Water must be traced separately

Identify the actual ordinary **terrestrial Water extractor** definition shown at Feynman and trace its effective resource-admission actor values/properties and native path. Compare explicitly to atmospheric water and ordinary vein-based extractors. Establish whether its presence can legitimately arise with **no generated local Water vein**, and under which terrain/biome/atmospheric conditions. Reuse the resource-availability investigation; do not assume that model appearance or the catalogue label selects a particular native branch. If the exact installed definition cannot be joined, report that limitation without invention.

### E. Correct active-site status and research record

The maintainer **withdraws the statement that Feynman V Cu IL F is deleted**. Correct the current RG2-A1/RG2-A documentation where it repeats the unsupported deletion/exclusion claim, but **do not automatically make this outpost a mandatory test site**. If used as a reserve, confirm active Workshop status using established saved flags and ownership; otherwise leave it as a separately identified optional candidate. Continue to exclude genuinely disabled/deleted outposts from ordinary test populations.

Preserve the chronology: original reviewed conditional predictions; subsequent maintainer screenshots and correction; today's evidence-backed reconciliation. Do not overwrite frozen v1/v2 predictions or rewrite original reviewer returns. If the current prediction model is corrected, issue an explicitly versioned new prediction plus a reproducible change log and counterexamples.

## 4. Completion and negative-result requirements

Return a concrete disposition for **each material mismatch**: explained, model correction supported, spatially untestable from these screenshots, or unresolved with a named missing input. Explain the shortest discriminating observation if needed (e.g. the naturally consumed native frame/geometry and epoch, or a qualified spatial placement measurement). **Conditional offline acceptance cannot be promoted to observed runtime equivalence by internal mathematical regression alone.** The absence of live native measurements is a declared limitation, not a mandate to invent them.

If the seed/geometry reconstruction remains well-supported but screenshots refute particular mature predictions, say both things clearly. No demand for universal planet support, complete terrain renderer, or perfect screenshot polygon tracing. Provide an answer-first, plain-language report separating established mechanics, measured UI outcomes, unresolved frame correspondence and optional future live validation.

## 5. Frozen acceptance criteria (continuation; unchanged original RG2-A1 AC1–AC8)

The reviewer must re-evaluate the **complete corrected cumulative RG2-A1 work against the original AC1–AC8**, and additionally check:

1. **Evidence identity:** All eleven images, timestamps/paths/hashes and chronological additions inventoried; no false save/frame/geometry joins.
2. **Observation reconciliation:** The per-resource table correctly distinguishes positive, negative, UNKNOWN, visual and placement outcomes for Feynman/Carinae.
3. **Copper geometry:** Single-point disk, multi-region union and distinct native geometry products tested or bounded with actual native/model evidence, without overinterpreting the photograph.
4. **Water admission:** Actual terrestrial extractor definition and selected native gate established or exact blocked dependency recorded; no unsupported atmospheric inference.
5. **Causal challenge:** Specific model input/consumer hypotheses tested against evidence, and any model change qualified independently without post-hoc fitting.
6. **Outpost status:** Correct active-site treatment; maintain frozen predictions and historical review chronology.
7. **Documentation and reproducibility:** Scientific claims/provenance intact, current report revised appropriately, clear outstanding limits, source and run receipts.
8. **Independent full-snapshot review and delivery:** Fresh independent verdict and original-criteria matrix; tracked changes, input protection and exact cumulative **complete and task-only** patches verified forward and reverse.

The focused checks supplement the frozen original criteria; they are not permission to weaken them or assert a live result.

## 6. Permissions, protection and delivery

**Authorized:** bounded offline inspection and new original analysis/code; read-only use of installed definitions, previously qualified native exports, protected Save52 and screenshot copies; safe synthetic/offline tests; changes to relevant RG2-A1 explanatory records and narrowly necessary cross-references. Preserve existing protected evidence, historical snapshots, reviewer receipts and function/source pins.

**Not authorized:** launching/loading Starfield or Creation Kit; debugger/observer/SFSE attachment or injection; changing saves, game files, installed tools or private databases; destructive cleanup; third-party code/data incorporation without the existing attribution and permission checks; Git stage/commit/push; publication or resuming B6.

Before writing, identify actual project baseline, original ACs, prior reviewed and current working snapshots, source/evidence hashes and protected inputs. Check space and active workers per WORKFLOW; avoid large duplicate scratch/diff artifacts. Stay in the **same ongoing Codex session** and continue the existing branch/working tree. Don't treat exploratory questions as requiring formal review; it is **the final durable changed tree** that must receive independent review.

Deliver one concise completion summary listing files changed, model dispositions, tests, limitations, review outcome and remaining work, plus:

- Updated durable report, observation/geometry comparison and evidence/source references, including any separate Water note.
- Frozen/updated model-prediction records (new version only if scientific changes warrant it), and verified safety/validation receipts.
- **Fresh independent-review receipt** explicitly ACCEPT/REWORK against *entire cumulative final B2-equivalent RG2-A1 snapshot* (i.e. the RG2-A1 final tree), unchanged AC1–AC8 and the above focused checks. Preserve all previous reviewer failures/ACCEPTs as historical.
- Newly regenerated **complete and task-only diffs** from the actual final reviewed tree, exact forward/reverse byte reconstruction, SHA-256/manifest, tracked inclusion/exclusion inventories and unchanged protected HEAD/index/input hashes.

If the reviewer returns REWORK, correct within the authorized scope and repeat the review. No implicit maintainer approval to commit is granted. Final recommendation must differentiate **scientific closure** from **documentation/assignment acceptance** and leave B6 on hold.
