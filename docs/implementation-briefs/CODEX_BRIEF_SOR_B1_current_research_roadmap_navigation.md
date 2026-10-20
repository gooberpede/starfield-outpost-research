# Codex implementation brief — B1: Current research roadmap and documentation navigation

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Assignment:** B1, release-readiness documentation implementation  
**Authority:** The maintainer has approved the scope described below. **Offline/documentation-only. No publication, Git staging/commit/push, deletion, save or game operations.**  
**Predecessors:** Accepted RR1 publication-readiness audit, B0 publication policy/release gates, RC1 gap reconciliation and capability-access audit, and the accepted subsystem reports.  
**Disposition:** Return a complete reviewed diff for maintainer critical review; do not integrate it yourself.

## 1. Purpose and governing approach

Transform the large research archive into a navigable, accurate **current research reference** while preserving the original investigations, revisions, negative results, qualifications and reviewer history. The first public release is a **version-bound research archive, not a software product**. B1 builds the documentation routes and a **proposed** release claim/build scope; it does not clear or publish the archive.

A new reader starting from `README.md` must be able to find (a) the best-supported current explanation of an outpost subsystem, (b) its definitions/native/Papyrus/save technical references, and (c) the history, counterexamples, primary evidence references and independent review. Treat these as three independently testable navigation journeys.

**Prefer synthesis and links over duplicating whole reports.** Organize the current roadmap by **game subsystem**, not experiment date or researcher workflow. Reuse accepted RC1 findings and the 60-question coverage matrix; do not create an alternative scientific authority by rewriting results. Clearly separate **current best-supported**, **qualified**, **superseded**, **disproved**, **historical** and **deferred/open** entries. These are navigational labels, not replacements for existing confidence, evidence basis, publication category or approval status.

## 2. Authoritative starting materials

Read and reconcile, at minimum:

- `docs/audits/publication-readiness-rr1/` — full RR1 report, 21 findings and documentation/navigation audit.
- `docs/audits/publication-readiness-b0/` — `report.md`, `release-gates.md`, `rr1-dispositions.md`, `scope-and-evidence-policy.md`, `versioned-baselines.md`, and related adopted B0 documents.
- `docs/audits/outpost-coverage-2026-10/` — original 60-question coverage and Build Mode/Locations and coordinate/biome assessments.
- `docs/audits/outpost-rc1-2026-10/` — reconciled 60 questions, capability-access matrix, Papyrus interfaces, remaining gaps and reviewed status.
- Current `README.md`, `docs/README.md`, `docs/subsystems/README.md`, `docs/experiments/README.md`, `docs/RESEARCH_STATE.md`, `docs/BACKLOG.md`, `docs/known-facts.md`, `docs/hypotheses.md`, `PUBLICATION.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PROVENANCE.md`, `docs/DECISIONS.md`, `docs/implementation-briefs/README.md` and appropriate evidence indexes.
- Accepted reports and reviews for outpost/site identity, position and spatial model, inorganic/organic/manufactured production, power, storage/output links, freight/cargo/fuel, crew/robots, numerical/build/spatial limits, attacks/Integrity, ordinary and shared containers/displays, Stored Resources, coordinate sufficiency, nominal biomes, BM1 variants, BM2 catalogue, LO1 Locations and RC1 capabilities.
- RR1/B0 publication restrictions, including claims tied to multiple Starfield builds, local-only evidence, rights and existing raw-save policy tensions. The current research's main baseline is 1.16.244.0; never imply every historical result used that build or has been revalidated on it.

Locate authoritative sources through existing links and source registers; do not manufacture a new claim from generic domain knowledge. Resolve apparent disagreements by accurately reporting source-scoped coverage and review/disposition, or flag the needed scientific decision. Preserve original history.

## 3. Authorized B1 changes

**Permitted:** Create a clearly linked current research roadmap (suggest `docs/research-roadmap.md`), create small subsystem entry/index pages and a supersession/history navigation register where they improve discovery, update `README.md` and documentation indexes to route users to them, and correct stale *editorial* project-status/navigation/next-step statements without changing their scientific meaning. Add a proposed release claim/build applicability matrix (see §5) and B1 navigation review records. Create a prioritized pseudocode-improvement register for B2.

**Controlled existing-document edits:** `README.md`, `docs/README.md`, selected `docs/subsystems/**/README.md` or subsystem-index pages, `docs/experiments/README.md`, `docs/RESEARCH_STATE.md` or other current editorial index/status pages, and precisely scoped stale `PUBLICATION.md` wording **only if** the existing release gate remains explicit **NOT CLEARED / NOT READY** and the change does not create policy exceptions or grant approval. Correct the known RR1 broken permission anchor only as a link repair if exact intended target is supported; do not rewrite permission policy. Maintain clear review of every changed existing file. If an edit to a policy-controlled document would alter authority, record a proposal instead and escalate that specific decision.

**Not permitted:** Change accepted findings, hypotheses, function/offset evidence, experiment logs, reviewer verdicts, confidence/publication classifications, substantive rights or license policies, source code, scripts, saves, binary evidence, `.gitignore`, tool installations, or release assets. No new reverse engineering, Ghidra/xEdit execution, compilation, game launch, live observation, debugger attachment or tooling qualification. No moving/deleting ignored material, Git stage/commit/push/tag, visibility changes or external upload. No broad prose normalization or semantic pseudocode insertions under B1: those belong to B2 with substantive review.

Historical papers should normally be left byte-identical. For **high-impact superseded entry points**, a minimal status notice with precise successor link may be proposed only if it is plainly editorial and retains the historical text unchanged; prefer the central register and present-day index over mass edits.

## 4. Roadmap structure and reader experience

Build a readable **subsystem-first** route that covers, without silently dropping any accepted major domain:

- Outpost identity, active membership qualifications, Workshop ownership and save representations.
- Planetary locations, anchors/terrain addressing, nominal biome assignment and spatial/resource-region qualifications.
- Inorganic, organic and manufactured production; nominal production-rate arithmetic, eligibility and the distinction from realized inventory throughput.
- Power, He-3, storage, local output links and inventory movement.
- Cargo links: configuration, freight, scheduler, remote behaviour and fuel.
- Crew, skills, robots and their Workshop relationships.
- Construction: limits, budget, placement, territory and scenery, variants/CHANGE, build catalogue, prerequisites and user-facing status.
- Attacks, defenses and Integrity/damage/repair.
- Chests, displays, mannequins, Shared Outpost Storage, crafting sources and Stored Resources.
- Locations → Outpost information and its provider/refresh boundaries.
- Cross-cutting capability access (definition/Papyrus/configuration), native locator registers, evidence provenance and version applicability.

For each major subsystem, include a short accurate **what is established**, **scope/limitations** and **go deeper** route: current primary report, important technical detail or register, underlying saved/runtime evidence where available, independent review and historical research. Do not imply that a STATIC explanation was directly observed live, or that saved samples establish complete active-player membership. Link the RC1 capability matrix and Papyrus interfaces prominently; do not infer an SFSE requirement from lack of an identified interface.

Root README should become a concise landing page with overview, bounded research status, game-version qualification, links to roadmap/history/capability/evidence/policy, explicit publication status, and short “how to navigate” guidance. It should **not** be a chronological dump of dozens of experiments. Place chronology in an appropriate existing history/index rather than deleting it without preserving access.

## 5. Proposed release claim/build scope — not a release decision

B0 requires a proposed **first-release claim/build matrix**. Provide rows for major accepted research claims/subsystems, referencing source report and accepted review, tested or historical game versions/source pins, evidence basis and coverage, exclusions/remaining uncertainty and proposed inclusion status. Separate what is already supportable from **pending maintainer agreement, B3 baseline manifest, B4 rights/evidence decisions and B6 final release gate**. Do not promote scientific confidence, grant publication permission, or assert uniform build applicability. Coordinate/biome nominal models and realized throughput are particularly important to qualify correctly.

Identify any policy-controlled status line that currently asserts “no research complete”; propose/perform only a factually accurate editorial correction which **continues to state publication is NOT CLEARED**. Where source provenance is unavailable or historical build assignment cannot be made, label it rather than guessing.

## 6. Supersession and historical navigation

Create a compact, evidence-linked register of important displaced claims and earlier research routes. Each entry should contain:

- Original claim/document and **why** its current navigational label applies (historical-only, superseded, disproved, deferred/open or still current in narrower coverage).
- Specific later source or counterexample, its review disposition and authoritative current destination.
- Scope qualification; do not convert a superseded interpretation into the claim that its underlying experiment was invalid.

Use the registers from RC1, prior disposition/review documents and RR1 as starting points. Focus on misleading entry points and prior “next step” claims, not a census of every old sentence. Preserve negative trials and prior raw scientific records; do not rewrite them to be consistent with newer results.

## 7. Pseudocode-improvement register for B2

**B1 inventories candidates, B2 implements improvements.** Deliver a prioritized table with document/location, mechanism, current supporting accepted evidence, recommended expression (pseudocode, equations, decision table or diagram), benefit, fidelity pitfalls, and priority (`required` only when necessary for a coherent public explanation; otherwise `recommended`). Include representative candidates from Workshop registration/ownership, production scheduling and independent-rate aggregation, placement and construction eligibility, cargo freight, storage/crafting enumeration, biome coverage and Build Mode selection; mark those already adequately explained so no unnecessary rewrite is proposed.

A candidate does not authorize publishing decompiled source. Prefer original analytical pseudocode where it clarifies mechanics; don't insist on converting narrative history into algorithms. Any eventual pseudocode requires source-faithful scientific review, not merely Markdown validation.

## 8. Navigation verification and independent review

Provide a deterministic check/report that operates on the **proposed tracked tree** and validates:

1. Relative Markdown link targets, file case, referenced fragments where reasonably resolvable; distinguish intentionally external URLs, historical machine paths and identified local-only evidence.
2. Every roadmap subsystem links to a current accepted report and review, and has a route to historical experiments/evidence without implying that ignored files exist in public Git.
3. Three newcomer journeys from repository root: **understanding**, **technical reference**, **evidence/history**. Trace each using specific pages and links, with representative examples from at least production, construction and position/biomes.
4. Stale “all open”, “no research completed”, “next active task” assertions in current reader-facing entry points are corrected or explicitly qualified. Historical snapshots remain untouched.
5. All entries in proposed claim/build matrix have provenance and version qualification or an explicit unknown; `NOT CLEARED` remains visible.
6. UTF-8/Markdown table/anchor/known malformed-prose smoke checks on all **changed** documents. Do not substitute this for B2's full repository prose audit.

Apply the existing project's exact patch/document verification and review workflow. Tests must distinguish actual checked files from intended future public release content. Do not claim a fresh public checkout was run if not performed; simulate tracked-tree navigation locally and report its limits.

## 9. Freeze: eight mandatory acceptance criteria

**AC1 — Source and scope control.** Read RR1/B0/RC1 and prior accepted investigations; inventory changed/protected files, authorities and version boundaries. Make no prohibited modifications. Provide evidence for unchanged protected inputs, HEAD and index.

**AC2 — Current roadmap.** Deliver a subsystem-first, accurate, concise roadmap covering all major accepted domains with supported conclusions, limitations, source reports and independent review paths; preserve scientifically qualified coverage.

**AC3 — Root and index navigation.** Update README and appropriate indexes to make the roadmap, capability matrix, version applicability, primary evidence and historical navigation discoverable; no broken tracked-file routes or implied public access to ignored evidence.

**AC4 — Historical status/supersession.** Provide a reviewed supersession/navigation register and correct material stale editorial entry-point statuses while preserving historical results and publication gates.

**AC5 — Proposed claim/build matrix.** Prepare a source-linked, appropriately version-qualified first-release scope proposal without promoting claims, overriding permissions or approving publication.

**AC6 — B2 pseudocode register.** Deliver prioritized, evidence-linked candidates and risks; do not modify scientific explanations or insert unreviewed pseudocode in B1.

**AC7 — Navigability and documentation validation.** Demonstrate the three reader journeys, validate links/case/anchors and checks on all edited documents, account for intentional local/external paths, and retain exact receipts of any failures and subsequent corrections.

**AC8 — Independent review and complete delivery.** Have an independent reviewer assess the original frozen criteria and actual resulting tree/diffs; return PASS/FAIL/NOT TESTED with evidence paths, review decision (ACCEPT/REWORK/ESCALATE), corrections, package manifest and verified complete/task-only patches. No staging, commit, push or public release.

Criteria are frozen. Only the maintainer may approve material changes; retain original wording and written amendment record.

## 10. Compact completion and continuation contract

- **Task type:** Documentation implementation, consolidation and independent audit.
- **Question / deliverable:** Is the current accepted research reliably discoverable, scientifically accurate and clearly differentiated from historical/superseded work, with proposed release scope and B2 presentation opportunities recorded?
- **Scope:** Only the explicit documentation edits and new audit/navigation artifacts above. Preserve protected game/save/native/local evidence, historical research and installed tools; respect repository/publication permissions. No third-party redistribution or network publication.
- **Mandatory acceptance:** AC1–AC8 above; independent review mandatory, with actual evidence and tested versus inferred coverage.
- **Optional acceptance:** Extra navigation polish that is low-risk and directly supports the three journeys; do not proliferate redundant index pages.
- **Negative-result closure:** A missing historical source or inaccessible local-only evidence must be documented precisely, with searched/indexed routes and narrow limitation; it does not license fabricating or replacing evidence. Fix verified broken links within authorized editorial scope.
- **Continuation authority:** Diagnose, correct, retest, requalify and resubmit in-scope failed checks under the same assignment; no new brief for ordinary rework. Do not lower acceptance requirements to make a check pass.
- **Exit/escalation:** Stop the affected operation for a changed protected hash/HEAD/index, missing required authorization or essential inaccessible input after documented bounded recovery. Preserve checkpoint/evidence and ask narrowly; continue unrelated authorized work. Respect existing disk-space and integrity guards for any generated local outputs; no arbitrary healthy-run timeout.
- **Review artifacts:** Per-criterion acceptance matrix, primary evidence and source links, negative/regression ledger, path/status/inclusion/exclusion inventory, independent verdict, byte-exact complete and task-only patches including untracked text, verification and patch reconstruction receipts. Return scientific/editorial, tooling-integrity, target-integrity, permission and reviewer outcomes separately.

## 11. Expected delivery

Produce, under an appropriately selected `docs/audits/` B1 audit record path, a succinct implementation report, per-criterion review, navigation-journey receipts and changed-file manifest. Add the roadmap, proposed release claim/build matrix, supersession register and pseudocode candidates at clear, linked durable paths. Record the precise baseline revision. Use properly escaped relative links and readable Markdown, with prose/offset notation verified on changed files.

Return a concise completion summary, independent-review decision, substantive new/updated documents, outstanding editorial decisions, any deviations and exact complete/task-only patch locations. **Nothing staged, committed, pushed, tagged, released or published.**
