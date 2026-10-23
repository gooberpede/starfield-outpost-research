# Codex implementation/research brief — RG2-D1

## Minimal Installed-Data Corpus and Standalone Resource-Geometry Reproducer

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)
**Authority:** Offline research, local extraction, implementation and testing only. **No live Starfield launch/attachment, save modification, commit, push, release or publication.**
**Status:** Implementation brief for maintainer-approved execution; preserve all existing research and frozen evidence.

## 1. Purpose and scientific baseline

Build a genuinely **standalone, geometry-first** reproducer which accepts a supported planet/location/outpost-footprint request and a **minimal portable reference corpus**, then predicts the relevant inorganic resource regions and derives resource availability from their geometry. Determine and measure the thinnest installed-data slice sufficient for that supported capability. The reproducer must **not require installed ESMs, xEdit, Creation Kit, Ghidra, Starfield.exe, debugger traces, frozen output files, or local research caches at inference time**.

The project has established exact reproductions of **seven separately captured native regions**: four at Feynman V (`Cu Co Ni IL`) and three at Carinae III-a (`Rc Fe`). RG2-C1H resolved effective installed inactive-resource settings (notably Exotic 0.05); RG2-C2D derived selected SFPT through installed PNDT→SFTR and repaired source-block backlink resolution. Those are strong bounded controls, **not** proof of a complete runtime source/region census or correctness for every planet, seam, override, or cache epoch. Historical runtime overrides and effective epochs remain distinct open questions.

Read and follow the current `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/THIRD_PARTY_POLICY.md`, `docs/templates/completion-contract.md`, and reviewer procedure before work. Relevant scientific material includes `docs/experiments/resource-geometry/`, `resource-geometry-mature-context/`, `resource-installed-settings/`, `resource-source-enumeration/`, `resource-pattern-selection/`, `resource-carinae-source-context/` and native-availability findings. Reuse existing owned code with clear provenance; do not silently replace proved native arithmetic or rewrite frozen predictions.

## 2. Fundamental distinctions and non-goals

Separate **(A) the installed-data extraction/builder**, **(B) the resulting portable corpus**, **(C) the standalone reproducer**, and **(D) publication-oriented algorithm and schema documentation**.

- The **builder** may read verified locally installed game definitions during authorized offline preparation. Record source hashes, load/override assumptions, extraction lineage and transformations.
- The **corpus** contains the **minimum required game-derived values**, segregated from authored metadata. Keep actual extracted corpus payloads and large derived geometry **ignored/local-only**. Do not stage or include proprietary records, textures, native exports, installed game files or private saves in patches.
- The **reproducer** is a research implementation; **its publication is optional**, as is the builder's. Track authored code under existing project practice if useful, but do not assume tracked code or local-only payloads are automatically cleared for a public release. Clearly mark exclusions/rights, and prepare an explicit publication plan before any future repository exposure.
- The **algorithm specification, input dependency description and portable corpus format** are the principal publication-oriented research outputs. Make them understandable independently of a particular programming language, executable or extractor, with original explanations/pseudocode rather than wholesale decompilation or proprietary payloads. Publication intent does **not** waive provenance, licensing, privacy or separate final release authorization.
- Do **not** integrate with or modify `starfield-outpost-network` in D1. Do not make a website, shipping bundle, new public release, or player-facing app. Do not claim mathematically globally smallest corpus. Do not fit outputs to native captures.

## 3. Scientific workstream A — minimum field-level dependency closure

Construct an auditable **field-level dependency inventory** running from the request to final regions and availability. For every retained field provide: source record/type or derived rule, semantic domain, units/bit precision/endian where material, consumer stage, required/optional status, whether derivable, sharing scope (global/system/planet/biome/pattern/source), and original/game-derived versus authored provenance. In particular account for:

1. Planet/body identity, coordinate transform and requests (including supported chart/face, location precision, query XY/radius/upper and terrain/source lookup boundaries).
2. Installed PNDT→SFTR selection and referenced SFPT/SFBK source-block lookup, including native backlinks and legitimate fallback/unsupported cases.
3. Biome and per-biome component/RSGD selection, surface styles, resource-family/rarity/order and IRES identities; all resource dependencies required for cross-resource competition, not just requested output resources.
4. Native packed cell key, manager owner, surface/random seeds, SFPT registry order/settings, map orientation, selected source geometry, padding and relevant dimensions.
5. Installed GMST effective multipliers and other generator settings; preserve distinction between executable defaults and installed overrides.
6. RSGD generation blocks, chance/attempt/width/length/heading and native binary32/CRC/MT drawing schedule, collision/competition, region bounds and area/point availability consumer as supported.
7. Completeness/unsupported status for special/Everywhere, Water/atmospheric/biome-admitted resources, seams, missing provenance and historical cache state. Keep separate from ordinary inorganic vein geometry; never misclassify `UNKNOWN` as `ABSENT`.

Explicitly trace transitive dependencies and show why a field is retained. Produce a **removal/ablation ledger** for major groups: demonstrate failure, changed output, or defensible redundancy if omitted. No obligation to individually brute-force every byte; clearly distinguish tested minimum from unproven global optimality. Consider shared deduplication and derived-versus-precomputed sources.

## 4. Engineering workstream B — corpus builder and measured alternatives

Implement a deterministic, hash-pinned offline builder that writes a versioned, validated portable corpus into an **ignored local directory** under `.local-work/` or other existing policy-approved ignored location. Never overwrite primary receipts or source ESM files. Builder output must identify game version/definition hashes, schema revision, coverage set, field counts, source lineage and validation checksums without embedding sensitive absolute local paths into distributable metadata.

Measure at least **two genuinely distinct** corpus representations, for example:

- **Normalized/dependency-based**: compact shared tables and per-planet references, reconstructing anchors/regions on demand.
- **More precomputed**: carefully bounded expanded source mappings or geometry-related intermediates, retaining enough dependencies for exact output.

Report actual serialized byte sizes, compressed sizes if used, record counts, duplicate elimination, build cost, load/startup cost and prediction-time measurements for **one outpost**, **one planet** and **multiple planets**, where supported by the local evidence. Separate shared fixed overhead from growth per planet/site. State which variant is recommended and *why*; size alone cannot trump correctness or complete uncertainty reporting. Do not set an arbitrary absolute corpus size threshold or publish the actual ESM-derived corpus.

## 5. Engineering workstream C — standalone, geometry-first predictor

Implement a clean predictor interface taking **only** the portable corpus and explicit request arguments. Prefer a clearly documented structured request/response contract that can be implemented in another language. Required output includes:

- Supported body/location and coordinate/frame provenance, actual query footprint, and schema/definition identity.
- Resource identity with generated region/path coordinates, widths, bounds and enough ordered representation for exact comparison; an availability result derived from the regions and qualified area predicate.
- Status/coverage metadata distinguishing `PRESENT`, `ABSENT_WITHIN_PROVEN_SCOPE`, `UNKNOWN`, and other necessary structured incompleteness states. Explain whether the returned region set and source coverage are exhaustive for the bounded request.
- Deterministic arithmetic/numeric policy; preserve original binary32 bit identities when making exact claims, including native ordering and random draws where needed for replay.

**No runtime side channels:** prove by a negative-dependency test that inference still executes when ESMs, game installation, Ghidra/xEdit, local native exports, historical C1E/C2A captures, frozen prediction JSON, and prior request caches are inaccessible. Avoid embedding historical native answers in the corpus as a lookup table. Test in an isolated, controlled working directory with explicit read allowlist and capture attempted forbidden accesses. The builder may use protected game data, but this standalone test must use only the completed corpus and caller inputs.

Test Feynman V and Carinae III-a from location/footprint requests **without caller-supplied hand-selected source anchors, SFPT IDs or expected regions**. Treat the seven native regions as held-out verification only. Compare exact geometry where justified, and classify missing/extra regions, spatial membership and source coverage independently; report all positive/negative/unknown assertions transparently. Preserve existing frozen predictions and Feynman's four and Carinae's three native controls. A reproduced seven-path result does not alone certify a complete planet/outpost source census.

Retain deliberately negative and unsupported request tests (wrong schema/definition version, missing required record, unsupported chart/seam, corrupted corpus, boundary uncertainty and partial source coverage); failure to resolve should produce a structured result, not fabricated zeros or default substitutions.

## 6. Publication-oriented scientific deliverables

Create or update tracked **authored** documents for:

1. **Algorithm specification:** deterministic pipeline, native-equivalent transformations, randomization, resource processing/competition, region construction and area evaluation, with pseudocode/equations and explicit supported limits.
2. **Minimal-data specification:** normalized input schema, each required field's domain and provenance, referential integrity, extraction/normalization rules, versioning and compatibility; show game-derived versus authored metadata distinction.
3. **Reproducibility and validation:** how another researcher would build or supply a conforming corpus and implement predictor semantics; exact independent tests, observed native controls and uncertainty conditions.
4. **Storage trade-off study:** measured representation alternatives, ablation/redundancy findings, scaling estimates with stated assumptions.
5. **Rights/publication classification:** authored research intended for future publication subject to final clearance; actual extracted corpus LOCAL-ONLY; builder and reproducer code publication undecided; no implicit redistribution rights for transformed ESM content.

Do not paste raw game-derived records into tracked fixtures. Use authored synthetic fixtures to test schema/algorithm where possible, and brief bounded native/output facts only under existing quotation and publication policies.

## 7. Sequence, authorization and continuation rules

**Authorized:** offline inspection of existing project evidence; read-only local installed definitions; authored code and documentation; isolated corpus build; deterministic tests, benchmark and synthetic fixtures; read-only use of existing protected receipts, with hashes. Standard local scratch and disposable tests are authorized within documented disk budgets.

**Not authorized:** Starfield launch or debugger attach, Creation Kit execution, save manipulation or creation, new live observation, repository integration into Tracker, network upload, publication, staging, commit or push. If live evidence is essential, return a **specific missing operand and approval-ready run card**, without executing it.

Follow the frozen completion protocol, independent reviewer and protected-source rules. If a vital dependency is genuinely unavailable, clearly distinguish **implemented supported subset**, **unresolved input/coverage**, and **constructive acquisition path**; do not claim a general predictor based solely on conditional examples. Favor useful partial implementations over indefinite speculation, but AC3/AC5 below must be met within stated supported conditions.

## 8. Frozen acceptance criteria (AC1–AC8)

**AC1 — Authority, preservation and provenance.** Existing game files, saves, native evidence, original frozen predictions, HEAD and index untouched; actual corpus ignored/local-only; first-party and third-party rights correctly classified and no unapproved operation.

**AC2 — Complete bounded field-dependency inventory.** Trace every input needed for the supported geometry and spatial query, including transitive source/tree/biome/RSGD/GMST/competition dependencies, with explicit omissions, derivations and uncertainty.

**AC3 — Standalone geometric prediction.** Demonstrate an actual predictor that runs from a portable corpus plus location/footprint request, with **no installed-file or historical-capture runtime reads**, and reproduces the seven held-out native paths exactly within the evidence-supported Feynman/Carinae scope. Never achieve this by storing expected native answer paths or accepting witness source IDs as requests.

**AC4 — Minimum-corpus investigation.** Build and validate two alternative representations, provide field-level removal/redundancy analysis and measured sizes/performance for bounded single-site/planet/multi-planet cases. No unsupported mathematical minimum claim.

**AC5 — Availability and coverage honesty.** Derive ordinary vein availability from geometry; demonstrate qualified site classifications where possible, distinguish incomplete source enumeration or unsupported consumer cases from true absence, and preserve exact numeric/output semantics.

**AC6 — Publication-ready research specification.** Authored algorithm and corpus schema understandable without the proprietary game binaries or particular implementation, including source/rights classifications and reproducibility limits. Actual corpus not tracked or published; code publication remains optional.

**AC7 — Testing and final editorial quality.** Deterministic regression tests including seven native region controls, corruption/negative isolation cases, measured receipts, protected-input audits and documented results; apply `docs/EDITORIAL_STANDARD.md` automated screening **and manual reading of every changed prose file**. Conventional hex addresses/FormIDs/offsets, no redundant decimal labels, no fused words/numbers or unsupported scientific promotions.

**AC8 — Independent critical review and exact delivery.** Reviewer evaluates original frozen criteria, primary receipts, negative tests, ablation/size claims, rights, and exact final authored-text snapshot. Resolve REWORK defects; perform final delta review after any change. Deliver PASS/FAIL/NOT TESTED matrix; separate scientific/engineering/publication dispositions; immutable logs and versioned reports; verified complete/task-only diff, hashes and file manifest. **Do not stage, commit, push, publish or delete protected evidence.**

## 9. Deliverable format

Return a concise implementation summary with links/paths to the report, corpus spec, algorithm spec, predictor, builder, benchmark results, independent review and ignored local corpus manifest. State the exact invocation commands, tests run, results and limitations. Supply exact complete and task-only patch paths and SHA-256, hash-bound review/manifest receipts, and suggested conventional commit message. The maintainer will review the supplied diff before integration.

**B6 publication-readiness verification remains ON HOLD.** RG2-D1 authorizes neither publication nor automatic Tracker integration.
