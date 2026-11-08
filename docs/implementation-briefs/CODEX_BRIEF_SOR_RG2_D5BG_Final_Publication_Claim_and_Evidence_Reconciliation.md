# CODEX IMPLEMENTATION BRIEF — SOR RG2-D5BG
## Final publication claim and evidence reconciliation

**Status:** Implementation assignment; not a release or publication authorization.  
**Project:** `D:\Projects\starfield-outpost-research\` / `gooberpede/starfield-outpost-research`.  
**Target baseline:** retail `Starfield.exe` **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; preferred image base `0x140000000`. Main `Starfield.esm` SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`. Historical save origin, effective plugin load order and configurations remain claim-specific; do not silently assign the EXE hash to old saves.  
**Temporary concurrency exception:** **At most two concurrently active sub-agents for D5BG only.** This explicitly overrides, but does **not amend**, the standing limit of one concurrent sub-agent. The standing limit resumes immediately after this assignment. Primary Codex retains integration, challenge, gate and report ownership; an independent final reviewer must not merely ratify the sub-agents' work.

## 0. Purpose and authority

D5AW and D5AX established the publication-independence principle and dependency graph; B0–B4 established the scientific, method, source and rights gates; D5AY–D5BC established **18** subsystem guide/reference pairs; D5BD created the **2,095-entry** version-pinned native function catalogue; D5BE prepared D5AS and C19 bounded evidence derivatives and a publication run card; D5BF independently reviewed the **four-asset proposed release set**, including **25 CORE saves**, **27 ADDENDUM originals** (14 saves, 13 JPEGs), D5AS complete geometry evidence and C19 callback evidence. The assets remain staged locally; neither their presence nor their prior acceptance authorizes upload. Prior accepted conclusions, their exact confidence/coverage, and historical counterexamples remain authoritative unless a concrete contradiction is identified.

**The maintainer's controlling scope decisions:**

1. Aim to publish the **complete body of independently accepted research**, including all 18 guide/reference pairs, the D5BD native function catalogue, original experiment reports/reviews/negative cases, and later resource-generation findings through D5AS/D5AU/D5AV. Do **not** restrict the historical record to the four packaged evidence assets.
2. Distinguish **preserving a historical report** from **endorsing its conclusions as first-release current claims**. Preserve supersessions and qualified findings. Narrow or exclude a current claim only for a specific documented problem, not because wholesale historical session replay is impossible.
3. Apply **proportionate, claim-specific scientific and public evidence-access standards**. An original historical runtime observation needs a faithful independent route if indispensable to the claim; static reconstruction, saved-state interpretations and computations have different relevant routes. A private location or hash by itself cannot close an indispensable evidence dependency.
4. Reconcile and make narrowly bounded **documentation, manifest or reproduction-method corrections** where justified. Do not undertake new captures, broad native investigation, new large evidence packages or scientific reinterpretation merely to raise a readiness count; recommend separate scoped follow-up work for real unresolved blockers.
5. Continue to preserve the accepted four-asset D5BF proposal and its file-specific approvals for **proposed release**; retain `PENDING RELEASE` URLs and the distinction between proposal eligibility, B6 preflight and final release authorization.

The primary question is now **what exactly can this first release responsibly claim**, not whether every underlying engine function or historical session can be reproduced exhaustively.

### Controlling sources (inspect the exact current versions; do not assume these descriptions supersede them)

- `docs/PUBLICATION.md`, `docs/EVIDENCE_STANDARD.md`, `docs/DECISIONS.md`, `WORKFLOW.md`, `AGENTS.md`, `docs/PUBLICATION_RUN_CARD.md`.
- `docs/audits/deferred-work-d5aw/publication-plan-amendment.md`, `docs/audits/deferred-work-d5aw/dispositions.csv`, `docs/audits/publication-architecture-d5ax/claim-evidence-dependencies.csv`, `docs/audits/publication-architecture-d5ax/architecture.md`; read existing evidence-access assessments where present.
- `docs/audits/publication-readiness-b0/release-gates.md`, `docs/audits/publication-readiness-b0/versioned-baselines.md`, `docs/audits/publication-readiness-b1/claim-build-matrix.md`, `docs/audits/publication-readiness-b3/baseline-manifest.md`, `docs/audits/publication-readiness-b3/method-contracts.csv`, and the B4/F1 evidence indices.
- `docs/guides/`, `docs/reference/` (18 pairs and glossary), `docs/functions/` and `docs/audits/native-function-catalogue-d5bd/`.
- `docs/audits/evidence-access-d5be/` (including D5AS and C19 derivative manifests and assessment), `docs/audits/release-assets-d5bf/README.md` and `release-assets.json`, `research/evidence-access/verify_release_assets.py` and the D5BE scientific verifiers.
- Original primary `docs/experiments/` reports, sources, reviews and representative data. Cite them directly for disputed substantive claims. Consult related review results rather than relying solely on recent synthesis. Protect their exact names, assertions and historical dispositions.

If a named source has moved, resolve its authoritative tracked location transparently. Inventory/check against frozen starting HEAD, index and working tree. A synced repository may have a newer HEAD than the prior briefs; do not silently assume the historical HEAD is current.

## 1. Scope and operating constraints

### Allowed

- Read-only inspection of tracked source material, existing original analyses, manifests and *specifically necessary* retained local evidence when authorized and available. Prefer tracked original research. Avoid indiscriminate crawling of private working storage; no need to restore the full historical raw corpus.
- Authored claim/release-scope matrix, dependency reconciliation, source crosswalk, decision ledger and small portable validation utilities as needed. Update short current-facing qualification/links where the finding is already established and the correction is within assignment scope.
- A bounded, cited plan for additional derivatives or separate investigations if indispensable evidence is truly missing. Identify source availability and actual prerequisite limits, rather than pretending future assets are available now.
- Proposed, reversible, reviewed updates to the **planning** portions of `docs/PUBLICATION_RUN_CARD.md`. All release execution gates remain pending.

### Not allowed

- No Starfield launch, SFSE hook/instrumentation, new game/save/runtime experiment, debugger, Ghidra/xEdit analysis, protected-file mutation, historical save rewriting, executable or archive extraction for publication, remote disclosure, Git ref/tag/branch/history edits, staging/commit/push, GitHub release creation, uploads or visibility changes. Do not change historical scientific reports/registries to hide contradictions or resolve weak access by retroactive promotion.
- No unilateral release scope **approval** or claim exclusion; maintainer makes material scientific, evidence-tier, distribution and release decisions. All files of the four-asset proposal remain local and `PENDING RELEASE`.
- No blanket revalidation of 2,095 functions or re-performance of D5BF custody checks. Where the selected claim depends on a native entry, use D5BD's build-pinned source/caveat and only check representative consequential joins and any concrete inconsistency.
- No archival/migration of implementation briefs or administrative audits; those are to be coordinated **near the end** of publication preparation, before B6 freeze. Do not inadvertently impose `.local-work/` retention: it may be deleted after publication.
- No new public binary assets under this brief. If a small proposed derivative is justified, document a separate approval path. Do not claim rights over any proprietary source material.

### Concurrency/work allocation

Up to **two** concurrently active sub-agents may be used **only while executing D5BG**. Suggested nonexclusive division: (1) identity/position/biomes/construction/resource-generation/historical resource observations; (2) production/power/logistics/crew/defense/inventory/UI/save-state. **Primary Codex** handles common standards, function catalogue, cross-subsystem dependencies, D5BE/D5BF mappings, shared data model, merged disposition and final integration. Prevent simultaneous writes to common files: assign separate work products and integrate centrally. An independent reviewer must test the assembled snapshot after both agents stop. Keep original authors and reviewer roles distinct.

## 2. Four controlling questions

### Q1 — Which first-release claims are presently endorsed, and at what precise scope?

Create an **authoritative proposed release claim matrix** covering the current B1/B4 claim universe, all 18 subsystem subjects and technically consequential post-B1 work (notably resource generation and D5BD). Preserve B4 claim IDs as historical join keys; add stable, source-qualified entries for genuinely new claim groups rather than silently overwriting existing identifiers. One source subsystem may legitimately support multiple distinct claims; don't assume one topic equals one scientific proposition.

Each row must distinguish, in a readily auditable form:

- Stable claim ID and short reader-facing proposition; exact current authoritative guide/reference/report/review and historical B1/B4 correspondence.
- **Nature of assertion:** native/static interpretation, saved-state reconstruction, derived calculation, historical observed runtime event, or inference/generalization; multiple bases where genuinely necessary.
- Actual build/definition/save/session input pins and demonstrated population/conditions. Mark `N244` versus `H?` and other source/version domains explicitly.
- Evidence basis and scientific confidence **per `docs/EVIDENCE_STANDARD.md`**, coverage and completeness separately; concrete counterexamples, negative controls, supersessions and unknowns.
- **Proposed publication disposition** (`READY`, `READY — QUALIFIED`, `ACTION REQUIRED`, `MAINTAINER DECISION`, `HISTORICAL ONLY`), precise boundary of what is endorsed, and any requested maintainer choice. These are D5BG **recommendations**, not newly approved research conclusions. Do not change a prior PROVEN/STRONG/PROVISIONAL label by substituting a publication readiness label.
- Reader-oriented summary: how a reader should phrase/cite the finding without implying unwarranted universality or live mod-invocation safety.

A historical report can remain in Git even if its superseded or unreviewed claim is `HISTORICAL ONLY`. Preserve all accepted reports, source records and counterexamples. Explicitly differentiate the current *selected claim* from old narrative or exploratory interpretation. Avoid gratuitous weakening of well-supported bounded findings; an objection must identify a concrete relevant issue.

### Q2 — Which indispensable evidence dependencies actually have durable public routes?

Starting from `docs/audits/publication-architecture-d5ax/claim-evidence-dependencies.csv` and current B1/B3/B4/D5BE/D5BF work, **reconcile at claim and transitive-dependency grain**. Avoid a fresh undifferentiated file inventory. A source count alone does not close an evidence route.

For each selected claim and decisive evidence edge identify:

- Source object/claim and the actual event, bytes, mechanism or calculation it substantiates.
- Materiality (`INDISPENSABLE` versus contextual/provenance/supporting), evidence method, reproduction tier and reason for that choice. Why is the specific raw artifact indispensable, or why does an accessible authored derivation suffice for this precisely scoped claim?
- **Route:** tracked inspectable report/method/data; approved local D5BF release-asset **candidate** awaiting hosting; lawful independently reproducible method (with exact external prerequisites); `LOCAL-ONLY` support; or missing/blocked. Distinguish *proved reproducibility*, *conditional documented procedure*, *reported prior replay*, *proposed hosted asset*, and *actual hosted URL*. An intact local artifact, manifest or checksum is not yet a public route.
- Exact originating report/review, applicable selector/version/hash, source-availability tier, effect/safety contract, access rights and known missing content. Where dependency A requires B, record the transitive relationship and the failure consequence.
- **Consequence of loss/absence:** which portion of the current claim is no longer justified at the advertised tier, and minimal possible closure route. Do not promote missing inputs into “nonessential” merely because they are expensive to distribute.

Reconcile the four D5BF groups faithfully: 25 first-party saves in CORE; 14 saves plus 13 JPEGs in optional ADDENDUM; 30 qualified D5AS canonical bodies against 2 reference bodies (generating mask unobserved in series); 346 C19 native callback comparisons (not the D1 incident, 35,573 upstream evaluations or full asynchronous provenance). Verify their exact source/claim joins in the ledger rather than assuming either derivative has broader coverage. If an **optional** addendum contains indispensable evidence for a claim, explicitly say that the claim's independent inspection requires that optional download.

**Prioritized challenge cases** (review their *actual current* evidence, don't predetermine hold/pass):

1. **B4-C19 D1 historical disappearing-deposits incident**, distinct from C19 continuous preview folds; historical header-rejected H249 control and any alternative evidence route.
2. **B4-C07 power three-load observations** versus static/Save29 adjudication; does a current claim require replaying the three-load event?
3. **B4-C09/C23 cargo timing and VM/network** claims versus native scheduling contract and included saved-state witnesses; no invented exact voyage timer or runtime transit guarantee.
4. **B4-C18 position/coordinate** broader original corpus and old controls versus included coordinate saves and scoped static arithmetic.
5. **B4-C06/C14 component/Shared Storage census** and withheld historical inputs versus tracked calculations and currently selected originals.
6. **D5AS / D5AK / D5AL / D5AO / D5AQ / D5AT and D5AU/D5AV resource generation**, distinguishing complete body matches, original acquisition/eligibility custody, actual native owners, later historical events, conditional hypotheses and sample-specific causal claims. Do not infer generating masks from class proxies.
7. **D5BD native catalogue**: whether each advertised characterization tier is backed by appropriately accessible original locators, authored explanations and stated raw-replay limits, without requiring every Level C internal entry to have a separate downloadable decompilation.
8. Any consequential new topic or later accepted result not captured by the old B4 matrix. Record why it was included or excluded.

Do not automatically hold an accurate STATIC or SAVE claim because a raw historical UI capture is unavailable *if that event is not indispensable to the actual scoped assertion*. Conversely, an actual historical runtime occurrence cannot be proved by an algorithm that could have produced such an outcome in theory. Every disputed route needs a traceable explanation.

### Q3 — What precise resolution is necessary for every remaining gap?

Provide a **decision-ready exceptions and follow-up ledger** with, at minimum:

- Claim(s) and evidence edge, precise unsupported assertion, observed gap and **evidence** for the gap (e.g., unavailable historical file, missing selector, unapproved derivative, missing rights clearance, unsupported input version).
- Minimal viable choices, in preference order as warranted: reuse already tracked evidence or selected D5BF candidate; independently document/reproduce from lawful pinned inputs; small proposed derivative under separate authorization; narrow reader-facing assertion; preserve `HISTORICAL ONLY`; or hold until targeted investigation. Include effort/risk, affected reader claim and consequences of each choice.
- Clear disposition separating **already resolved**, **bounded in-task editorial/method correction**, **requires maintainer decision**, **separate authorized implementation/evidence task**, and **genuinely blocks the selected release claim**.
- No fabricated evidence or unearned readiness. If source proof is unavailable, do not replace it with a plausible story or a “full replay” promise. Do not demand acquisition merely to make the ledger aesthetically complete.
- Link to concrete current source or acceptance review and the minimum acceptance test for any future action. Prioritize blockers relevant to accepted first-release scope over optional scientific extensions.

The result must support a short maintainer decision meeting: what can be accepted as is, what exact qualified wording is needed, what remains held, and what separate work—if any—must precede coordinated archival and B6. Only the maintainer can authorize a materially changed claim tier or exclusion; mark it **PROPOSED** until approved.

### Q4 — What remains before an isolated B6 release-candidate review?

Produce a **publication handoff** describing:

- Counts of release claim dispositions by category, with a reconciled complete denominator and transparent exceptions; resolved, conditional and actually blocking evidence edges without double-counting.
- The exact four D5BF asset proposals, status **APPROVED FOR PROPOSED RELEASE / PENDING RELEASE**, relevant claim joins and remaining hosting obligations; no actual URL, tag or release identity invented.
- Remaining maintainer choices: agreed claim/build matrix, evidence-tier/narrowing decisions, residual rights/privacy/credit/excerpt wording if materially pending, later historical archive design, target release identity/tag policy and exact tree/history exposure approval at appropriate later stages.
- Ordered proposed work between D5BG and B6: claim-specific blockers, then coordinated archival of implementation briefs **and** administrative audits near the end, then candidate freeze and independent B6 isolated audit. Do not silently turn every deferred experiment into a required release gate.
- Read-only amendments to the *planning* sections of `docs/PUBLICATION_RUN_CARD.md`, with links to the new reconciliation, pending decisions and testable gates. **Do not check PASS for candidate freeze, B6, hosted asset verification, tags, upload, rights final signoff or release execution.**

The handoff must distinguish current technical preparation from final release approval. B6 will need a clean checkout, actual intended public ref/history scope, approved staged asset bytes, validated lawful methods, and eventually actual hosted download verification after separately authorized draft upload. The previous plan of conducting staged-asset preflight **before** upload is controlling.

## 3. Deliverables / suggested locations

Prefer one cohesive, reasonably compact collection such as `docs/audits/publication-claims-d5bg/` (use an existing publication reconciliation location if clearly better). Choose exact names based on existing conventions; record them in a collection README. Suggested deliverables:

1. `README.md` — purpose, actual snapshot/source scope, results and outstanding decisions; **do not** declare release ready.
2. `claims.csv` or `.json` — authoritative **proposed** claim matrix with stable IDs, B1/B4 crosswalk and evidence/characterization/publication dispositions.
3. `evidence-edges.csv` or `.json` — selected and transitive evidence routes, materiality, exact source, access state, dependency consequence and claim join.
4. `exceptions.md` plus a structured actions ledger — specific disputed decisions and smallest credible closure mechanisms.
5. `crosswalk.md` — reconciliation against all 18 subsystem pairs, D5BD function catalogue, later resource-generation topics, original reviews, and historical B1/B4 positions.
6. `handoff.md` — counts, proposed scope choices, asset boundaries, publication-readiness gaps and recommended next steps.
7. Small deterministic verification script **only if needed** to assert crosswalk completeness, unique IDs, evidence-edge closure/status consistency, valid paths and ordered status counts; if added, document its inputs and run it on a clean tracked snapshot without `.local-work/`.
8. Focused, explicitly justified changes to current reader-facing qualification/navigation or `docs/PUBLICATION_RUN_CARD.md` where supported by accepted research. Avoid mass generated edits to the 18 guides or historical reports. Link new proposed claim matrix from existing planning navigation where it adds value, clearly marking it **PROPOSED**.

**Document design:** A release engineer should quickly find the exact claim, its evidence path, whether it can be advertised, and which decision is needed. A research reviewer should be able to challenge the claim with its original report, negative case and accepted disposition, not be forced to trust the most recent summary. No auto-numbered synthetic findings, no orphaned relevant post-B1 conclusions and no ungrounded binary “all published” verdict.

## 4. Method and verification requirements

1. **Freeze baseline of work:** record HEAD/branch/index/working tree, standing untracked brief, source inventories and authoritative currently selected build. Read relevant standards. No stage/commit/push. Make no implicit Git clean or history rewrite.
2. **Make source-led crosswalk first:** reconcile the historical B4 claim set to 18 current guide/reference pairs and later accepted work; prove which original claims split, merge, become historical or are outside the selected release. Each important promotion or coverage change needs primary source and reviewer witness. Include negative/superseded observations.
3. **Evaluate evidence edges independently:** adjudicate source availability, actual claim materiality, working method and source pin. Distinguish locally held data from promised public access and hosted public access. Do not confuse a method's ability to decode selected inputs with completeness for all historical controls.
4. **Cross-agent challenge:** the primary agent reviews each sub-agent's treatment of the other's shared evidence where relevant (e.g., position/resource placement, cargo/power scheduler, UI resource generation and native function identity); perform at least one adversarial case in each family. Merge without contradictory statuses.
5. **Check reconciliation correctness:** stable unique claim IDs, traceable crosswalk to old claims and all 18 pairs, consistent sums/denominators, explicit basis/confidence/coverage and materiality, non-orphaned indispensable edges, no unsupported READY statuses, and no mismatch between readiness labels and the 4 staged assets. If using automation, test at least an intentionally missing dependency, an incorrectly “hosted” pending candidate, a duplicate ID and a contradictory disposition.
6. **Independent scientific/engineering/editorial review of the exact final snapshot:** independently inspect meaningful originals and a representative risk-weighted sample of ready/qualified/action/maintainer/historical claims; challenge the prioritized cases, transitive evidence routes and counterexamples; check links, CSV quoting, source rights language, status semantics and clear next decisions. Document what was **actually independently repeated** versus merely copied from prior reviews. Correct defects and re-review changed bytes. Do not automatically approve every claim because a script reports zero diagnostics.
7. **Clean, reviewable delivery:** return source and any tests, summary, independent review, exact changed-file list, task-only and complete diff if in established workflow, relevant SHA-256/patch receipts, evidence of no unintended protected/target/Git mutation, and a proposed commit message. The user will separately review and commit.

### Adversarial scientific checks to include explicitly

- D5AS positions 7 and 13 are **reference matches**, not observed generating mask=0.
- C19 346 native callback folds **are not** D1's older disappearing-deposits incident and do not establish screen-timing ancestry.
- Saved/local registered cargo links and fuel-cycle path **are not** demonstrated exact voyage clocks, throughput or loaded transit guarantees.
- An observed first-party save and a documented static function **are not** interchangeable evidence of a past runtime event.
- A D5BF candidate ZIP/JSON with a digest and `PENDING RELEASE` **is not** an accessible hosted asset until separately authorized and independently verified.
- The D5BD function's verified RVA **does not** mean a stable future-build mapping or a safe external call signature.
- `LOCAL-ONLY` supporting evidence may remain as qualified provenance, but cannot be the **sole** purported durable route for an indispensable selected claim.
- Inaccessible original captures do not require blanket rejection of all related accepted source-level findings; preserve narrow, accurate conclusions.

## 5. Acceptance criteria (AC01–AC10)

**AC01 — Scoped complete claim set.** Every historical B1/B4 candidate claim and the 18 current subsystem topics have an explicit mapped status; later accepted resource findings and the D5BD function catalogue are accounted for. Unmapped/merged/split/historical entries have a documented reason. No blanket new scientific confidence declarations.

**AC02 — Scientific correctness.** Original research/reviews and exact current qualifiers support the proposed propositions; static, saved, calculated, observed and generalized assertions are distinguished, with scope, completeness, negative cases and supersessions intact.

**AC03 — Build integrity.** Native functions and analyses are explicitly pinned to Starfield.exe 1.16.244.0 and its SHA-256, main ESM independently pinned; historical saved creation/configuration remains qualified. No cross-version address or source authority invented.

**AC04 — Evidence graph closure accounting.** All indispensable dependencies for selected claims are classified and traceable through transitive inputs with one honest present/future access tier; counts reconcile and no claims are marked READY based solely on hypothetical assets or LOCAL-ONLY missing indispensable originals.

**AC05 — Known hard cases.** The D1/C19 split, power three-load versus Save29, cargo/VM, position, C06/C14, resource-generation sequence, D5BD limitations and other actual later high-risk cases are adjudicated with direct sources and counterexamples, not bulk label updates.

**AC06 — Specific decisions, not generic holds.** Every ACTION REQUIRED or MAINTAINER DECISION row identifies the exact issue, a minimal viable closure/narrowing choice, consequences, source and an acceptance test. HISTORICAL ONLY stays discoverable; justified qualified findings remain eligible without impossible universal replay.

**AC07 — D5BF consistency.** Four groups, membership counts and scope match the current proposal; eligibility for proposed release is distinguished from final selection/hosting; no invented URLs or distribution grants, no silent loss of selected asset or claim reliance on an optional file.

**AC08 — Publication run card / handoff.** A decision-ready handoff and updated planning links state what remains before coordinated archival and B6; later freeze, rights signoff, draft/hosted checks, tag and publication statuses remain PENDING.

**AC09 — Reproducibility and preservation.** Portable tracked-data validation where reasonably possible, link/source/case checks, stable structured schema, reviewed exact patch and unaffected historical primary records/protected assets; no unapproved operation or external disclosure.

**AC10 — Independent acceptance and concurrency.** Independent final exact-snapshot scientific, engineering and editorial review explicitly reports Q1–Q4 and AC01–AC10 with defects/limits and reproducible receipts. At most two concurrently active sub-agents used during D5BG; restore the standing one-agent rule afterward. **D5BG ACCEPT is not publication clearance.**

## 6. Final Codex response contract

Report: (a) the proposed release-claim count and categorized outcomes; (b) number of indispensable edges truly ready versus conditional/held, with denominators; (c) exact remaining maintainer decisions and smallest follow-up assignments, if any; (d) exact changed files and independent review result; (e) verification and preservation outcomes; and (f) explicit **NOT READY / NOT CLEARED** publication status until remaining approved gates are met. Propose a conventional commit message. **Do not stage, commit or push.**

Stop and report **REWORK** if a substantive claim cannot be honestly reconciled, if source records contradict the proposed release assertion, or if a dependency is being declared closed solely because it would be inconvenient to preserve. A partial defensible matrix and visible blockers are preferable to an unearned universal PASS.
