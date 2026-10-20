# Codex brief — Project-wide outpost research coverage and gap audit

**Project:** `D:\Projects\starfield-outpost-research\`  
**Assignment:** Read-only scientific coverage and gap audit (documentation outputs permitted)  
**Date:** 2026-10-20  
**Status:** Brief for maintainer-authorized execution; no live, destructive, Git-integration or publication authority

## 1. Purpose and outcome

The planned core investigations into Starfield outposts have concluded, including production, logistics, power, personnel, construction limits, placement, attacks, containers, Shared Outpost Storage and the Locations **Stored Resources** list. The repository also holds earlier Workshop, save-file, resource availability and planetary-position investigations, some with substantial qualified results and deferred questions.

**Produce a trustworthy project-wide coverage inventory that identifies what is actually established, which older gaps were resolved by later evidence, and which remaining questions merit research before publication or future application development.** This is an **audit of existing work**, not another substantive reverse-engineering experiment.

An accepted investigation can be complete *within its frozen scope* even when documented exceptional cases or live confirmations remain untested. Do not equate every OPEN item with a failure, or retrospectively impose new acceptance criteria on completed assignments.

## 2. Read first and obey

Treat the repository's current versions as authoritative, especially:

- `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md`, `THIRD_PARTY_POLICY.md`.
- `docs/templates/completion-contract.md` and the independent reviewer procedure.
- `docs/RESEARCH_STATE.md`, `docs/BACKLOG.md`, `docs/subsystems/`, `docs/position-model/`, relevant experiment reports/reviews, decision and finding registers, and linked original criteria.
- All completed core workstreams, including E1–E3, P1, S1–S2, C1–C3, CR1–CR3, R1, L1–L3, DA1 and SD1–SD3. Locate actual canonical paths rather than assuming folder names.

Read the *latest* evidence and review/disposition documents while preserving chronology. A recent summary does not automatically supersede an earlier independently accepted finding; establish their actual relationships. Do not conflate evidence provenance, scientific confidence, completion status and publication classification.

## 3. Authorized actions and prohibitions

**Permitted:** Read existing repo text, indices, source locators, registers, scripts and offline artifacts where already accessible under existing permissions; perform lightweight, bounded read-only cross-checks (links, identifiers, evidence traceability, conflicting assertions); create/update **new audit deliverables** under a suitable `docs/audits/` directory; package review evidence and diffs in permitted local working locations. Follow existing protected-input, disk-space and output-integrity guards for any tooling used. Limit automated scans and output to justified, controlled operations.

**Not authorized:** Launch/operate Starfield or the Creation Kit; attach debuggers; deploy instrumentation, mods or DLLs; generate new gameplay/save checkpoints; edit source game/save evidence; restart deferred investigations; perform new deep Ghidra/native experiments; modify accepted historical reports, registers, conclusions, classifications or prior review decisions; make repository cleanup, licensing or publication changes; stage, commit, push or publish. Do not alter original evidence or protected inputs. If an essential action exceeds these limits, preserve the audited portion and request the narrow permission separately.

This brief authorizes producing the audit documents, not conducting any follow-up experiments it recommends. No broad archival rewrite; where existing documents disagree, document the conflict and cite both.

## 4. Audit coverage and required named questions

Survey the full project, not only recently completed subsystems. Include earlier save framing, beacon identity/active membership, Workshop object membership and reconstruction, native resource availability, spatial/terrain and planetary location work, and historical unsuccessful or superseded observer/tooling branches, alongside the recent core subsystem investigations.

### 4.1 Build Mode

Create a field/mechanism-level coverage inventory, with emphasis on:

- **Production footer** value, unit, constituent producers, power/damage/operational gating, aggregation, rounding and refresh; distinguish Build Mode from the Locations presentation. The screenshots showing about `1.66/MIN` and `1.67/MIN` are prompts, **not** proof of calculation or formatting.
- Build-menu category and recipe population, candidate availability versus locked/hidden state, prerequisites and item variants; identify already answered components in L1–L3 and SD2 before suggesting new work.
- Hab wall/door/window and other variant selection: construction versus reconfiguration versus automatic adjacency; representation, persistence and known gaps.

Do not expand this audit into a full build-menu UI or new native trace.

### 4.2 Remaining Locations / Outpost screen

Itemize every displayed informational field and relevant source/refresh question: name, planet/system, outposts built/limit, cargo links, crew, needed/total power, production, Stored Resources, Build Limit where applicable, faction, planet image/system diagram/level, and other observed metrics. Mark whether each **particular displayed field** is already connected to an authoritative source, merely resembles an understood subsystem value, or needs a bounded trace. Do not redo SD3's pagination/navigation or other excluded UI mechanics.

### 4.3 Planetary position, biome(s), and site resources

Provide a **dependency-focused assessment**, not another attempt to compute unverified exact coordinates. Separate:

1. Planet/system and landing-area identity;
2. Saved planetary surface/site anchors and validated angular interpretation;
3. Terrain grid/cell positions and available projections;
4. **Exact continuous beacon longitude/latitude**, including residual/frame/anchor requirements;
5. **Biome catalogue on the planet**;
6. **Biome at the specific outpost beacon/site**;
7. **All biomes intersecting the outpost's actual buildable territory** (including boundary/POI clipping where relevant);
8. **Resources actually available at that site** versus a planetary resource list.

Treat single-biome and biome-boundary outposts as distinct use cases. Do not assume site biome(s) or site resources can be derived merely from the saved beacon's local XYZ or an approximate lon/lat. Identify relevant existing terrain/biome/PNDT/native-query work and the **specific** missing input, transform, data source, or causal witness. Identify reuse opportunities from L3 only if justified by an existing cited link. Recommend the smallest next discriminating investigation, with any required live authority clearly separated.

### 4.4 Remaining subsystem, persistence and historical gaps

Search across research-state/backlog/registers and actual current reports. Ensure coverage of, where actually still open:

- Production: realized rates, producer participation, remote resolution and catch-up.
- Cargo: remote voyage/loading/arrival behavior and time-skip qualifications.
- Exact active outpost membership, unusual Workshop roots/assemblies, exceptional source relationships and owner attribution.
- Damage/repair/load ordering and historical attack limitations.
- L3 environmental-object reappearance and unresolved photographed-reference joins.
- SD2 saved shared-backing inventory quantities and consumption order; SD3 refresh timing and exceptional inclusion/override cases.
- Long-running position/frame/height/procgen and native-observer feasibility questions.
- User-observed but unproven behavior, separately from native/serialized findings.

This is a starting checklist, not a mandate to reopen the items or an assertion that each remains open. Look for newer findings resolving old questions.

### 4.5 Publication-impact research gaps

Identify unsupported or overbroad *central scientific claims*, missing evidence/provenance, and published-facing references relying on unavailable/private material. **Do not run a full release-readiness cleanup or third-party licensing audit now**; flag candidate risks with locations and refer them to the separate release-readiness program. Preserve `LOCAL-ONLY`, `REVIEW-REQUIRED`, `CLEARED-FOR-PUBLICATION` distinctions and do not upgrade classifications.

## 5. Classification and priority rules

Assign every gap/question **one proposed disposition**:

- **ALREADY RESOLVED:** Later evidence substantively answers it; supply exact later source and scope, and identify any stale older reference.
- **NEEDS CONSOLIDATION:** Evidence exists but current cross-reference, canonical explanation, or scope boundary is unclear.
- **TARGETED RESEARCH CANDIDATE:** A material unanswered question with a specific tractable next discriminator.
- **DEFERRED:** Open but presently low impact or dependent on costly, speculative or separately authorized work.
- **PUBLICATION BLOCKER:** A concrete publication-impacting defect, unsupported central claim, rights/provenance issue or reproducibility dependency; explain whether qualification/document repair can resolve it without fresh science.

These are **proposed dispositions for maintainer decision**, not changes to the repository's accepted scientific status or permissions. Separately record priority (`HIGH`, `MEDIUM`, `LOW`), affected use (research accuracy / save importer / Outpost Planner / future mods / public release), and confidence/coverage impact. Do not treat severity and research difficulty as synonyms.

For each unresolved entry, state *what is known*, *what exactly is missing*, and *what evidence could falsify or establish the candidate answer*. Negative claims require bounded and documented coverage, not universal proofs.

## 6. Deliverables

Place new, readable Markdown and appropriately compact TSV/CSV material in a dedicated audit directory, e.g. `docs/audits/outpost-coverage-2026-10/` (use repo conventions if a more appropriate existing location exists). At minimum:

1. **`report.md`** — answer-first executive synthesis: achieved coverage; genuinely unresolved high-value questions; duplicate/superseded gaps; priorities and recommended *decisions*, not automatically scheduled work. Distinguish science closure from publication readiness.
2. **`coverage.csv` or `coverage.md`** — project-wide, question-grained matrix: unique audit key; area/question; best-supported answer; precise existing source/evidence and review references; confidence/basis/coverage/status as recorded; exact gap; proposed disposition/priority; relevance and narrow next test/repair. One row per meaningful capability/question, not one per sentence in every source file.
3. **`build-mode-and-locations.md`** — field-by-field Build Mode and Outpost/Locations screen coverage; distinguish shared underlying metrics from independently traced UI providers. Record icon provenance as resolved by SD3, without reopening pagination.
4. **`position-biomes-dependencies.md`** — the separate levels and missing dependencies enumerated in §4.3; emphasize site/territory biomes, planetary surface precision, and true site resource coverage.
5. **`source-and-gap-reconciliation.md`** — older OPEN/DEFERRED assertions compared with later studies, including apparent contradictions, superseded interpretations and unresolved evidence. Make traceable rather than silently editing prior records.
6. **`review.md`** — frozen criteria matrix, tested/not-tested coverage, provenance/integrity, verification results, reviewer disposition and distinct science/integration/publication statuses.

Use **portable repository-relative Markdown links** in new docs. Absolute local paths may be quoted *only as historical evidence identifiers*, prominently labeled machine-local; not as instructions that readers could execute from a fresh clone. Link to the original sources rather than copying large passages or local-only evidence. Avoid false hyperlink precision. Consistent UTF-8 prose; verify no malformed joined/split words, Unicode corruption, broken links or fabricated locators.

## 7. Mandatory acceptance criteria — freeze before execution

**AC1 — Project-wide coverage.** Cross-check current backlog/research state/subsystem and finding registers with actual representative accepted reports, reviews and old deferred lines. Cover early native/save/Workshop/position research and recent core areas. Include a documented inclusion/omission method; don't equate the backlog alone with the full corpus.

**AC2 — Answer-first coverage matrix.** Deliver traceable, question-grained entries with factual answer, citation, basis/confidence/coverage and distinct status; no unsupported automatic promotions or artificial completeness.

**AC3 — Disposition and gap reconciliation.** Apply all five proposed dispositions and separate priority/impact; reconcile older versus newer claims with precise evidence and dated provenance. Preserve historical failures and negative results; identify real contradictions explicitly.

**AC4 — Build Mode audit.** Explicitly account for production footer, menu population/conditions, hab variants, and known dependencies, distinguishing established underlying engines from untraced screen-specific providers.

**AC5 — Locations screen audit.** Inventory displayed fields including counts, power, production, Stored Resources, faction and planetary information; classify exact provider versus adjacent subsystem knowledge without redundant SD3 UI work.

**AC6 — Coordinates, biomes and site resources.** Distinguish planetary biomes, beacon-site biome, *territory-intersecting biomes*, and actual site resource availability. Describe existing supporting evidence, exact missing dependencies, and next discriminating step without claiming unverified outpost lon/lat or biome results.

**AC7 — Scope, evidence and publication separation.** Record unresolved remote/persistence/exceptional cases, a short list of scientific versus publication risks, clear limitations and possible next actions; perform no new experimentation, no publication reclassification and no existing scientific-history rewrite.

**AC8 — Audit quality and independent review.** Preserve protected inputs, run proportionate deterministic document/lineage/link/prose and manifest checks, prepare independently assessed complete/task-only diffs with exact forward/reverse reconstruction, and obtain the independent reviewer decision against these **original** eight criteria. Report counts and checks only if actually executed. No staging, commit, push or publication.

An independently reviewed scoped negative conclusion is valid if the tested records establish that the particular gap remains unsupported; “not yet found” without sufficient search and controls is not a negative conclusion. Optional enhancements (charts, broad file normalization, additional classifiers) must not displace mandatory work.

## 8. Completion/continuation contract

- **Task type:** Documentation/research coverage audit and scoped evidence reconciliation, not new scientific experimentation or an implementation of unresolved features.
- **Question/deliverable:** Project-wide best-known outpost capability coverage, discriminating gap inventory, field audits, and position/biome dependency assessment in §6.
- **Scope/bounds:** Offline read-only existing research/evidence plus new audit files and local validation/review artifacts; permissions and exclusions in §3 are hard boundaries. Existing originals, repository history, game/save data, third-party material and local private evidence remain protected.
- **Mandatory acceptance:** AC1–AC8 above, with primary document evidence, exact source locators and independent reviewer.
- **Optional acceptance:** Nonessential reader aids or additional examples only if they improve traceability without scope expansion.
- **Negative-result closure:** A qualified bounded absence within explicitly examined records/representations may close a specific audit assertion; preserve uninspected branches and no universal absence claim.
- **Continuation authority:** Within approved offline bounds, resolve inconsistencies, repair *new audit outputs*, rerun checks and resubmit to reviewer without another brief. Do not silently change the frozen criteria or historical conclusions.
- **Exit/escalation:** Stop prohibited activity or threatened protected-input integrity. For a missing essential artifact/access, record attempted paths, observed status, impact and narrow user decision. Continue independent auditable work. Observe repository's disk/output/integrity/STOP safeguards; do not impose arbitrary duration or volume cutoffs on a healthy run absent an approved concrete risk.
- **Review artifacts/disposition:** Original eight-criterion PASS/FAIL/NOT TESTED matrix with evidence locations; failed runs/counterexamples; source and inclusion/exclusion inventories; independently reviewed complete/task-only diffs; patch reconstruction and protected-input receipts; separate scientific, documentation, safety and publication outcomes; reviewer ACCEPT/REWORK/ESCALATE.

## 9. Handoff

Return a concise summary emphasizing the **highest-value open questions, already-answered apparent gaps, biome/site-coordinate dependency, and publication blockers**, with durable audit paths. Provide verified complete/task-only patch paths and reviewer verdict. **Do not stage or commit.** The maintainer will conduct critical diff review and decide subsequent scoped briefs.
