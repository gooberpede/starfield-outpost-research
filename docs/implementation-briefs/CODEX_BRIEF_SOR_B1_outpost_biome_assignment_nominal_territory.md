# Codex research brief — B1: Outpost biome assignment and territory coverage

**Project:** `D:\Projects\starfield-outpost-research\`  
**Task:** bounded offline native/definition/save research and documentation  
**Authority:** this brief authorizes offline inspection, reproducible analyses and new research documentation only. It does **not** authorize launching Starfield, attaching to a live process, deploying instrumentation, creating/modifying saves, changing existing scientific conclusions, changing publication classifications, staging, committing or pushing.

## Objective and question

Establish how Starfield represents, assigns and queries planetary surface biomes, then explain how to determine **all distinct biomes with nonzero-area overlap with an ordinary outpost's nominal 150-native-unit territory**. Include a biome region wholly inside the territory even when it never crosses the circular boundary. Investigate effective territory after POI/location clipping as a **secondary, explicitly separable** objective; do not make resolving exclusion-zone geometry a prerequisite for the nominal result.

This is basic research into the underlying game and save model, **not** a design for an Outpost Tracker/Planner feature. Do not assume the world is continuous or that a 100-unit terrain cell has one biome. Establish the true biome granularity and relevant frames from native producers/consumers. Reuse the accepted geographic addressing and spatial findings without demanding exact continuous beacon longitude/latitude or instruction-for-instruction engine equivalence where neither is necessary.

**Central deliverable:** a causal model and explicit enumeration procedure/derivation for the ordinary nominal footprint, with an honest completeness argument tied to actual biome-region representation. It need not be a production-ready enumerator or census of all historical outposts.

## Sources and controls

Read project `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `THIRD_PARTY_POLICY.md`, relevant publication/provenance policy and current research state before execution. Reuse, with source pins and coverage limits, the coordinate-sufficiency report (Save37–39, Kreet Research Lab, SOR-002/SOR-003), the position-model and planetary-surface anchor/grid reports, native biome/resource-generation research, L3 spatial-placement/POI-clipping report, Workshop membership research and prior resource availability results. Do not assume prior hypotheses are findings.

Search the **broader historical save corpus**, not just Save52, for representative outposts and actual save/frame/biome correspondence. Specific user-supplied candidate leads (not prevalidated controls):

- **Save52, `Feynman V Cu Co Ni IL`** — user reports at least two biomes, a priority multi-biome candidate. Retain the precise label and verify its Workshop/beacon identity before analysis.
- **`Carinae III-a Rc Fe`** — user expects a single biome, a priority single-biome candidate; locate its actual saved witness rather than assuming Save52 or assuming single-biome status.
- **A historical outpost farming Memory Substrate and possibly Palladium** — user recalls substantial territory clipping but does not recall its save or exact identity. Search metadata/network names and historical evidence as a lead; do not force an identification or require recovery for nominal-territory acceptance.
- **L3 Kreet POI-exclusion Save30/31/33** — known effective-footprint clipping case, useful for the secondary comparison; do not presume documented biome classes for that site.
- Other appropriate held-out controls from the corpus, if actually identified and evidence-qualified.

Preserve source version/hash, original identity, full provenance, observations, confidence and any inaccessible/unsupported saves. Never write to the user's originals or their installed game/ESM. Only authorized read-only use of existing local analyses/tools; apply existing disk-space and evidence-integrity guards when copying/deriving evidence.

## Workstreams

### B1-A — Biome data and native assignment

Identify relevant native/record types, definitions, resource IDs, terrain/planet/worldspace context, biome names and identity, registration/selection machinery and any spatial region or mask representation. Determine whether assignment is per terrain cell, site, region, sample, procedural mask or a combination. Trace actual producer -> biome lookup -> consuming code; distinguish visual terrain/biome appearance from authoritative biome identity and from planetary biome catalogue membership. Establish boundary and mixed-cell behaviour rather than presuming single-biome 100-unit cells. Note any relevant seeds, inputs, caches, load-order or reconstructible context, and whether character/session state is actually consulted on mapped paths.

### B1-B — Nominal outpost territory (primary)

For ordinary beacons use L3's nominal 150-native-unit radial domain and properly qualified reference/Workshop frame. Derive how to transform/relate the outpost address and candidate biome regions to a shared spatial frame. Establish an explicit enumeration algorithm which returns **all** biome identities with a **positive-area intersection** with the footprint, including wholly enclosed patches; do not rely on testing only beacon/edge samples. If each eligible 100-unit cell proves to have one biome, enumerate every intersecting cell; if not, derive the appropriate subdivision/mask/region traversal. Address seams, cell borders, tangencies, numeric tolerances and exceptional non-land or unsupported terrain conditions as supported. Explain why enumerated coverage is complete within the claimed scope; an unqualified sparse sampling grid is insufficient.

### B1-C — Saved evidence and spatial controls

Recover and report qualified identity links from beacon/Workshop to planet, terrain frame and relevant biome lookup inputs. Use a positive multi-biome case and a plausible single-biome contrast if available, corroborated independently by native, save, or trustworthy recorded in-game evidence. Test at least one held-out/independent case rather than fitting parameters to all observed examples. A user's outpost label, resource combination or recollection alone is not proof of biome coverage. Explicitly distinguish persisted biome assignments, persisted references/coordinates and reconstructed/transient procedural context. If save evidence does not encode biome IDs, describe the reconstruction route and its qualification. Do not assert direct UI-observed biome membership from saved resources.

### B1-D — Effective territory/POI restrictions (secondary)

Reuse L3's clipped-territory findings to characterize the additional operation needed to enumerate biome coverage of the **effective buildable footprint**. Where supported, derive the eligibility predicate or geometric clipping and demonstrate an ordinary clipped control. Distinguish (1) nominal coverage, (2) biome portions removed by restrictions and (3) buildability of actual object placement, which may have additional collision/terrain checks. Do not block B1-B merely because a complete POI exclusion polygon or exceptional runtime border is unrecoverable. If this secondary investigation cannot be completed offline, state precise remaining inputs and smallest proposed test; don't launch it.

### B1-E — Relation to resources

Describe the biome-selection inputs consumed by inorganic/organic resource-region generation and whether resource and biome boundaries coincide or differ. Reuse existing PNDT/BIOM/RSGD/RSCS and native-availability findings, identifying actual cross-references. Avoid a full extraction/deposit geometry census, production simulation or exhaustive resource-placement prediction. Do not infer biome membership from the presence of Copper/Nickel/Ionic Liquids or other extracted resources without a proven selection relationship.

## Required outputs

Place documentation in an appropriately named `docs/experiments/outpost-biomes/` directory (or existing equivalent per repository convention): answer-first `report.md`, `plan.md`, native/definition causal chain with source pins, nominal territory derivation/algorithm and completeness justification, saved-case matrix including positive/negative evidence and identity caveats, secondary effective-territory status, resource-relationship notes, function/source register as warranted and `review.md`. Update only the minimum navigational indexes/links and current-state register for discoverability; preserve historical research claims and document their relationship without silently reclassifying them. Do not create an entire new tooling framework or implementation unless genuinely necessary to perform approved offline verification; any tool changes need their own tests and clearly enumerated diff.

Start report with a compact question -> best-supported answer -> confidence/basis -> tested/inferred/unknown coverage -> decisive evidence -> limits -> next discriminating step. No generic 'more context may exist' obstacle without a concrete counterexample or material missing operand. Conversely, don't claim exact territory coverage if the biome spatial representation or geometry is not sufficiently established. A valid bounded negative result requires demonstrated tested coverage and a precise falsification, not an unsupported assertion of impossibility.

## Frozen mandatory acceptance criteria

**AC1 — Evidence and inputs.** All authoritative sources and selected saves have verified identities, hashes/version pins and protected provenance; prior accepted results and relevant L3/geography findings correctly cited; historical corpus search coverage/discards recorded.

**AC2 — Biome machinery.** Establish the installed biome definition/identity model and actual native assignment/lookup pipeline, including the spatial granularity and conditional branches that materially affect ordinary cases, with code/data evidence and explicit boundaries.

**AC3 — Geographic/frame correspondence.** Explain how a saved ordinary outpost/Workshop site is related to terrain/biome spatial inputs, reusing the accepted cell/local-offset model, with actual recovered control operands and no unqualified assumption of exact continuous lon/lat.

**AC4 — Nominal coverage.** Provide an explicit method to identify every distinct biome with positive-area overlap with the nominal 150-unit radius, including fully enclosed biome regions, plus a justified completeness/resolution argument for the stated ordinary native model. If the method is blocked by an essential **demonstrated** missing input, give that concrete blocker, attempted alternatives and bounded tested result for independent disposition; do not substitute sampling or an invented PASS.

**AC5 — Representative corroboration.** Search for and evaluate at least one multi-biome and one single-biome contrast, prioritizing the named candidate leads, with positive identity/evidence where possible; test an independent example or a meaningful negative/counterexample, and explicitly distinguish claimed from observed biome membership.

**AC6 — Clipping and resource relationships.** Explain the secondary L3 effective-territory operation and its current evidence limit without blocking nominal completion; establish the relevant biome/resource machinery connections and exclusions without reopening resource-deposit census.

**AC7 — Durable reporting and scientific discipline.** Produce clear answer-first reports, reusable source/function and save ledgers, explicit confidence/coverage, positive and negative findings, smallest practical follow-up(s), scope/permission adherence and navigable relative links. Validate prose/encoding and avoid malformed spacing or unsupported blanket claims.

**AC8 — Independent review and verifiable delivery.** Independent reviewer evaluates **AC1–AC8** against original frozen criteria and primary evidence, documents ACCEPT/REWORK/ESCALATE and criterion PASS/FAIL/NOT TESTED; preserve failures and fixes; run available relevant checks; include status/inclusion/exclusion inventories, complete and task-only patches, hashes and exact forward/reverse reconstruction receipts. No staging/commit/push.

## Compact completion contract

- **Task type / deliverable:** bounded offline scientific research; biome model, qualified nominal-territory enumeration/completeness explanation, saved controls and documented effective-territory limits.
- **Scope / authority:** inspect existing installed definitions/native analyses, read-only original sources and historical saves, offline computations and new documentation; no retail process, live instrumentation, new gameplay/saves, overwrite of protected source, changes to game settings, licensing, publication classification, staging, commit or push.
- **Mandatory acceptance:** AC1–AC8 frozen above. Secondary clipping findings must be accurately scoped; nominal coverage is primary. Material contract changes require maintainer approval and a preserved dated amendment.
- **Optional improvements:** stronger independently recovered clipped-site witness; additional planets; a disposable demonstrator enumerator where justified. Optional work never masks a mandatory gap.
- **Negative-result closure:** tested scoped counterexample or documented concrete irreducible obstacle after in-scope alternatives, evaluated against AC4/AC5 by independent review; no invented universal impossibility or silent downgrading of criteria.
- **Continuation authority:** diagnose, correct, rerun and requalify authorized in-scope work without a new brief; preserve regression failures and rejected hypotheses. Never use this clause to obtain live/process/save/publication authority.
- **Exit/escalation:** stop the affected action on integrity, permission, truly inaccessible essential evidence or qualified resource guard; preserve logs/hash evidence and return specific blocked step and minimal request. No arbitrary cutoff for healthy offline work; observe all applicable both-drive free-space, output, identity and worker safeguards.
- **Review:** independent evidence-based review on actual final revision, original criterion matrix and primary logs; accepted science, implementation health, input integrity, and publication status assessed separately; verified complete/task-only patches and explicit no-Git-mutation statement.

## Return to maintainer

Summarize causal findings, single/multi-biome controls and completeness status, secondary clipping status, resource relationship, genuine remaining limitations and independent reviewer verdict. Provide exact paths to authored report/review, full patch and task-only patch, manifest/checks and a proposed commit message **only**; await maintainer critical diff review before integration.
