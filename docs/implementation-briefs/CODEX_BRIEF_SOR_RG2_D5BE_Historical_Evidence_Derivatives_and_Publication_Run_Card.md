# Codex implementation brief — RG2-D5BE
## Historical Evidence Access: D5AS and C19, and Publication Run Card

**Project:** `D:\Projects\starfield-outpost-research\` / `gooberpede/starfield-outpost-research`  
**Authority:** Maintainer-approved D5BE task only. This brief is the implementation contract; existing `AGENTS.md`, `WORKFLOW.md`, `docs/PUBLICATION.md`, `docs/EVIDENCE_STANDARD.md`, `docs/DECISIONS.md`, B0–B6 governance, and protected-input rules remain controlling.  
**Nature:** Bounded evidence derivative preparation, standalone verification, and release-operation documentation; **not a publication or raw-evidence distribution authorization**.  
**Target research baseline:** `Starfield.exe` **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`; preferred image base `0x140000000`. Main `Starfield.esm` existing B3 SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`. Preserve claim-specific historical input qualifications; these pins do not prove the original save creation build or effective load order.

## 1. Objective and decisions already made

Prepare two **scientifically adequate, bounded and verifiable historical evidence derivatives** for the initial version-pinned research publication, and establish a **single central publication run card** for the later exact release operation.

The maintainer explicitly decided:

1. **D5AS and C19 together**, each with its own source acquisition, verification, substantive verdict, and evidence-access decision. The provisional B4-F1 original-save CORE/ADDENDUM archives are **a separate subsequent task**; do not repack or alter them here.
2. Produce **claim-sufficient evidence**, not merely a table of asserted outcomes or a huge blanket raw corpus. Preserve decisive original input/row or geometry comparison information, inclusion/exclusion rules, source provenance, independent analysis paths and limitations. No arbitrary byte ceiling.
3. Prepare appropriate files/verification tools now. For content with unresolved distribution rights, privacy, source authenticity, or selection, keep the payload in **controlled local staging** and publish only a truthful tracked manifest/index marked `PENDING` or `LOCAL-ONLY`. Do not stage restricted payloads in tracked paths or call them public evidence.
4. `.local-work/` is **disposable after publication**. Every indispensable public claim must eventually be supported by (i) tracked material, (ii) approved/versioned GitHub Release asset, or (iii) independently reproducible public inputs and methods. Local paths/hashes alone cannot satisfy this. Indispensable dependencies still pending must remain explicit publication blockers or require an authorized claim narrowing.
5. A **publication run card** is required for eventual execution: release candidate baseline, scientific and rights gates, asset inventory, package and member hashes, creation/verification of tags, clean-checkout checks, post-upload download verification, user approvals, rollback/hold decisions and release-specific signoff. **Its creation is not permission to execute it.** Reuse or improve an existing fit-for-purpose run card if found; do not create a conflicting second release authority.
6. All initial claims are tied to **Starfield 1.16.244.0**, not an unspecified latest Starfield. Future game builds receive separate qualification and potentially separate research releases; do not overwrite historic address mappings or assume cross-build equivalence.

### Temporary concurrency exception

**Up to two simultaneously active sub-agents may be used for D5BE alone.** Suggested partition: one on D5AS geometry and one on C19 UI reconciliation. The primary agent owns integration, provenance, publication-policy conformity, run card and final review; sub-agents cannot independently authorize publication or act as their own independent reviewers. This **one-off override expires at D5BE closeout** and the standing **one-concurrent-sub-agent** rule resumes automatically. No need to occupy both slots continuously. All existing tooling and access limitations still apply.

## 2. Controlling questions

- **D5BE-Q1 — D5AS:** Can an independent reader inspect complete canonical geometry representations and reproduce the **30 qualified sample-to-reference comparisons** and their classifications, while preserving the exclusion and the source/claim limits?
- **D5BE-Q2 — C19:** Can an independent reader reconstruct **all 346 recorded native UI comparison results** from released/proposed bounded inputs and recorded native row outputs, without needing the entire ~2 GB WAL and without inventing timing or unique producer ancestry?
- **D5BE-Q3 — Evidence independence and provenance:** Are the derivatives actually generated from authenticated available original evidence, verified by independently runnable methods, with exact source→transform→artifact→claim linkage, and with a meaningful read-only/clean-snapshot test that does not depend on `.local-work/` **for the advertised public verification**?
- **D5BE-Q4 — Distribution and handoff:** For each proposed tracked file or external asset, is the exact byte identity, privacy/rights status, eligibility, indispensable-claim role, proposed destination, and unresolved approval decision recorded truthfully without actual upload or disclosure?
- **D5BE-Q5 — Publication run card:** Is there one maintainable, version-specific final release run card that integrates existing B0–B6 gates, scoped evidence/assets, Git tree/history/refs, tags, verification receipts and explicit maintainer authorization, with genuinely usable blank fields and order-of-operations rather than premature PASS claims?

Q1–Q5 each require an explicit `COMPLETE`, `REWORK` or `BLOCKED` result, with independently reviewed qualifications. An inaccessible indispensable witness can yield a truthful partial deliverable, but not a false `COMPLETE` for its evidence route.

## 3. Binding research baseline and non-overstatement rules

### 3.1 D5AS

Primary starting points (follow exact source-ledger links from these, not just the new reader summary):

- `docs/experiments/resource-retained-population/d5as-series-closeout.md`
- `d5as-producer-profile.md`, `d5as-analysis-protocol.md`, `d5as-handoff.md` and existing acquisition/pre-freeze/closeout ledgers and local archives where actually present.
- `docs/guides/resource-generation.md`, `docs/reference/resource-generation.md` are secondary cross-checks; D5AS originals and original evidence definitions are the scientific source of authority.

Known published claims and required distinctions:

- Feynman V geographic source `0:37536:20928:0029d20e`, body `0x0005e0de`, source-planar origin `(-200,-200)` in the qualified comparison frame.
- **30 qualified, independently cold-started captures**: roster positions 7 and 13 match the **complete mask-0 reference geometry**, the other 28 match **complete mask-3 reference geometry**. No qualified third geometry class.
- Canonical **body** mask-0 geometry **4,966 bytes**, SHA-256 `bba4c877bc14d8abd3cfe36313e4cd62fd98e510dbf18441b250eacb57b942c4`; mask-3 **4,858 bytes**, SHA-256 `7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653`. **Do not conflate** these with envelope-inclusive or historical normalized representations (including the D5AK 5,090-byte comparison domain).
- Attempt 6 UUID `7edfc207-4f95-4cdc-9617-ce847107c49c` was **excluded for `SOURCE_LIFETIME_RETIRED`** under a prespecified eligibility rule, then replaced. Exclusion is not a third qualified outcome. Preserve full chronological roster and exclusion reason.
- Geometry-class equality **does not directly observe which request won** or its actual generating raster mask; eligible request counts (28 mask-0 / 168 mask-3 under fixed C1) **do not measure winner probabilities**. Any confidence intervals or p-values are conditional on their specified IID/binomial models, not proofs of independence. Operator visit/save assertions are not per-start native observations.

**Q1 implementation:** Inventory and integrity-check actual retained source/capture archive members; distinguish original bytes, manifests, reference construction and derived comparisons. Extract/generate bounded claim-complete canonical bodies for both references **and each qualified sample** or an alternative lossless representation independently sufficient for full-body equality verification. Include exact sample ordering/UUIDs, size/hash/body-domain markers, provenance for source and transform, and the exclusion/replacement trace. Build a reader-facing method and standalone verification command for all 30 matches, counts, and any reported statistics; verify the verifier detects a deliberately altered body, wrong domain, missing sample, duplicate sample and incorrect classification. Do not replace original capture proof with a CSV of `MATCH` outcomes. If raw data availability does not support independent provenance or the bytes cannot lawfully be distributed, stage the correct derivation under local control and mark the public route pending rather than fabricating an equivalent.

### 3.2 C19

Primary starting points:

- `docs/experiments/continuous-beacon-preview/live-scientific-report.md`
- `docs/experiments/continuous-beacon-preview/live-attempt-01.md`, `validation.md`, `review.md`, original source and acquisition ledgers.
- `docs/experiments/native-availability-map/output-contract.md` and associated UI consumer method; the recent guide/reference are explanatory cross-checks, not original evidence substitutes.

Bounded scientific claims:

- **35,573 preview evaluations plus one initialization**, **346 complete native UI callback comparisons**, **611,926 records**, original WAL **2,036,489,728 bytes**.
- The 346 native input/population/append→row identity folds all agree: **339 three-row, seven two-row** updates. The original operator A/B/C displayed labels are (Iron, He-3), (Iron, Alkanes, He-3), (Iron, He-3), with receipt timestamps distinct from exact render events.
- The selected-water append is specific; a source biome population containing Lead is **not automatically included** as a displayed resource row. Respect original FormID mapping, pointer deduplication / first-occurrence order, row ordinals and input snapshot/producer lineage where the evidence actually supports them.
- UI row agreement is an original bounded observed comparison, **not** replay of the upstream resource generator or proof of a unique preview evaluation causing a displayed frame. Native UI callback output is not itself direct proof of precise Flash rendering time.

**Q2 implementation:** Identify the actual archived raw/derived inputs and their hashes; inspect original capture and verification methods under safe/read-only authority. Produce a bounded per-callback representation of **every** qualified comparison: required upstream source inputs and selected append inputs, identity/order/ordinal information, expected recorded final native rows, scope/phase labels where warranted, and enough context to independently recompute and challenge the entire 346-row-callback census. Include readable definitions/mapping for item/resource IDs and a standalone verifier calculating each result from input records, not just comparing precomputed `matches=true`. Preserve unchanged redeliveries and exceptions rather than selecting only phase-change examples. Distinguish *derivative scientific sufficiency* from *independent verification of derivative fidelity to the original WAL*. No need to publish the whole WAL if a small derivative is sufficient; if derivation fidelity cannot be checked from still-available originals, record that gap and do not call it proved. Use changed-row / wrong-order / missing-callback negative tests.

## 4. Source control, scientific independence and safe method boundaries

1. Establish baseline HEAD, clean staged index, supplied brief, existing user changes, protected inputs and relevant approved tools. Confirm source locations and hashes **actually exist** before reporting successful recovery. Do not trust stale `.local-work/` path strings as available data.
2. Handle protected saves, original captures, binary exports, WAL, source archives, local profiles and installations **read-only**. Do not run Starfield, Ghidra analysis/rewrite, xEdit or debugger instrumentation, deploy an SFSE plugin, alter save/configuration files, mutate original archive contents, delete inputs or start fresh live observations. Only use already authorized local offline methods and safe derived scratch under the task's own namespace; avoid uncontrolled scans/writes outside task scope.
3. Keep **source identity and consumer-independent reconciliation** separate. Verify original archive entries/member bytes and the derivation itself where feasible. Independent review should challenge methodology and source→derivative fidelity, not merely rerun the same Python implementation.
4. Put freely publishable authored methods and cleared text/tabular data in tracked paths only after scoped assessment. If a payload might contain restricted proprietary bytes, privacy-sensitive metadata or unapproved third-party content, keep it outside Git under controlled local staging and include only a safe index/manifests and pending classifications. Do not assume a small derivative is automatically cleared. No raw 2 GB WAL in Git and no raw save files in Git.
5. A public verifier may use Python standard library or clearly disclosed available lawful dependencies. From a clean **staged stand-in checkout** with no `.local-work/`, verify all advertised calculations on the prospective public data and any explicitly provided candidate asset data. Report what still cannot be reproduced until assets exist. Do not equate a locally staged restricted file with public availability.
6. Preserve original experiments, receipts, invalid outcomes and historical interpretations. Do not silently update old scientific verdicts to current terminology. Any newly revealed scientific contradiction is a separate review issue, not carte blanche to refactor accepted results.
7. No staging, commit, push, tag, Release creation, asset upload, permission/visibility change, repository publication, contact with external services or approval claims.

## 5. Deliverable layout and provenance manifests

Use appropriate scoped paths, preferably `research/evidence-access/d5be/` for **authored scripts/configuration** and `docs/audits/evidence-access-d5be/` for decisions, instructions and crosswalks. Use a stable tracked `docs/evidence/` index/subdirectory **only if suitable for safe, authorized public candidate data**. Stage unapproved payloads under task-specific ignored `.local-work/d5be/` (not `/docs` or another automatically tracked directory). Existing project conventions take precedence over these suggestions; document deviations. Do **not** put proposed GitHub Release URLs in the index before the assets exist.

Produce, for each evidence family:

- Manifest with evidence ID, exact artifact path/member, size, SHA-256, format/version, input files/member hashes, producing command/script version, source evidence and reviewer, source/derivative distinction, claim/necessity class and currently supported access tier.
- Clear mapping from each decisive result to its original report, review, protected inputs and transformed rows; distinguish full original capture, selected claim-complete derivative and synthetic/verifier test fixture.
- Readable format and command instructions, explicit version and byte/order rules, comparator oracle, error/negative controls and expected outcomes.
- Rights/privacy/attribution/third-party material assessment for the exact proposed files, with a `TRACKABLE CANDIDATE`, `LOCAL-ONLY`, `PENDING SPECIFIC APPROVAL`, or equivalent unambiguous disposition. No implicit publication clearance.
- Small, targeted cross-reference changes to current-facing guides/references and `docs/PUBLICATION.md` **only if necessary**, without changing their scientific claims or release status.

If recovery genuinely fails, record the exact missing source/input, the tests completed, and the narrow next dependency; leave the relevant Q/AC blocked. Prefer a clear shortfall to fabricated coverage or an ever-expanding, unrelated evidence census.

## 6. Publication run card — required new/updated durable artifact

Search the existing repo for an actual release-point **run card** as distinct from B0 policy/checklists, the B4 package plan or the proposed D5AW sequence. If one serves the purpose, improve it and link the canonical location; otherwise create **`docs/PUBLICATION_RUN_CARD.md`** (or an equivalently obvious canonical path). Link it from `docs/PUBLICATION.md`, and if useful from an existing publication index. Treat it as a **reusable blank operational checklist and gate ledger** for the real later release. The run card must be editable, preserve `PENDING / PASS / FAIL / NOT APPLICABLE` plus receipt/approver fields, and use concrete stop/hold decisions rather than marking future checks as already passed.

At minimum, include these ordered sections:

**A. Release identity and freeze** — research release identifier/version TBD; exact target **Starfield 1.16.244.0** and EXE SHA-256/B3 pins; intended release title, selected scope/claim matrix and exclusions; frozen repository commit, branch, tree, candidate Git refs, working-tree state, document/package versions; explicit decision on historical save-origin caveats. Future game-build release requires a separately reviewed qualification, not in-place relabeling.

**B. Scientific and evidence validation** — B0/B1 agreed release scope, independent reviews, all required runtime/persistence questions, accepted limitations, required negative cases; D5AS/C19 and other indispensable claim-to-evidence routes; evidence-manifest validation; B3 method/input/dependency checks; B5 selected creator safety; B6 independent clean-checkout reproduction **without `.local-work/`**. Block if selected indispensable evidence remains private/unavailable and no approved scope narrowing exists.

**C. Rights, privacy and attribution** — exact checked tree, linked text/examples, code, files, scripts, screenshots and proposed reachable Git **history/refs**; file-specific rights/privacy/credits/notices and GPL-3.0-or-later consistency; author/contributor confirmation; game-derived/proprietary and donor exclusions; approval and receipt fields; no blanket rights assumption.

**D. Packaged assets and member manifest** — full tabular schedule for planned GitHub Release assets, especially B4-F1 **CORE (25 unchanged first-party saves)** and optional **ADDENDUM (14 saves + 13 JPEGs)**, and D5AS/C19 derivatives **only if approved**, plus any later authorized packages. For each record capture: required/optional, exact basename, purpose/claim, source producer, file count, byte size, archive codec, SHA-256, exact member paths/names/sizes/hashes, permission/privacy disposition, staging location, attached tag/release, upload status, final hosted URL, download hash check and extracted-member hash check. Keep all as `PENDING RELEASE` until actual verified hosting. Do not manufacture filenames, members or package hashes; later fill them from finalized manifests. Decide explicit inclusion/exclusion of optional assets and whether to expose large supplementary audits.

**E. Tags and publication actions** — proposed tag(s) and naming/version policy (TBD pending maintainer), whether annotated/signed if applicable, exact commit each tag will reference; distinguish **Git research release tags** from Bethesda game versions and from Release asset names. A tag should identify the frozen research commit; it must not be created before independent B6 acceptance and explicit maintainer authorization. Capture commit/compare command receipts, existing-tag collision check, sequence of release draft/asset uploads, change-review boundary and visibility/timing approval. Document the chosen procedure without executing it.

**F. Final release validation and post-upload verification** — frozen checkout links/anchors, Mermaid rendering (previously source-only), examples/verifier results, external lawful dependencies, readable release notes/version statement and download instructions, actual hosted URL fetchability, full downloaded asset hashes, archive member byte integrity, manifest consistency, exact final Release tag and target commit, and review of changed Git surfaces/history/asset links after hosting. Define holds/re-review triggers on any changes to candidate bytes, refs, URLs, assets, disclosures or approvals. Separate initial preflight approval, upload authority, and final visibility/timing approval.

**G. Signoffs and incident/rollback/stop policy** — responsible operator, independent reviewer(s), maintainer explicit action authority, exact approved scope of Git operations, signoff timestamps/receipts, status ledger and STOP points. If a step cannot be reversed (e.g. public tag/release/history exposure), flag it as such; do not promise impossible rollback. No releases, tags or public changes in D5BE.

Ensure the run card **references** the authoritative B0–B6 plans and B4-F1 manifests instead of copying their entire history. A one-page release-at-a-glance checklist at the top is useful, followed by the practical detailed fields/tables. Explicitly distinguish **preparation** from **execution** and mark any unapproved name, release version, tag, target commit, and asset URL `TBD`.

## 7. Validation and independent review

For each evidence package, separately test:

- Full original-archive/source hashing where present; matching protected inputs; provenance chain and exact normalization/row contract.
- Positive demonstration of the advertised claim; negative controls intentionally changing meaningful geometry bytes or UI rows, missing/duplicating a sample/callback, and incorrect domain/ordering.
- Rebuild equality and deterministic authored verification on two runs where applicable; source mutation guard; exact byte/member manifests.
- No dependency on private user machine paths for the **reader-facing** public verification procedure; if an asset is pending, demonstrate verification with a staged stand-in while marking real hosted access unresolved.
- A reader journey from guide/reference → evidence index → original source/review → actual available verifier and expected limits.

For the run card, independently perform a **dry-run walkthrough using hypothetical placeholders**: can a future operator identify every necessary asset and tag, record clearances and compare exact final bytes, detect an unapproved or omitted asset, stop for a failed gate, and distinguish hosted links from proposals? Do not create, upload, or stage real release assets/tags during that exercise. Confirm it covers D5AS/C19 and B4-F1, rights/history, science, user signoffs, clean-checkout, rendered diagrams and post-host download checks. If another run card exists, resolve duplication to one canonical authority.

All substantive content needs independent scientific, engineering, rights/privacy classification and editorial scrutiny of the **final exact snapshot**. With the one-off two-sub-agent limit, make sure the reviewer is independent of the sub-agent who authored the material; the primary can use the established independent-review process and disclose independence limitations. Report each Q and AC separately, not only an overall success banner.

## 8. Acceptance criteria

- **AC01 — Source custody:** Original D5AS/C19 source inventories are verified against actual files and known hashes where present. Missing inputs and source/original distinctions are reported explicitly; protected bytes remain unchanged.
- **AC02 — D5AS sufficiency:** All 30 qualified full-geometry comparisons (not labels alone), both reference classes, sample identity/order, exclusion/replacement and byte-domain distinctions can be checked against the proposed derivative; direct-mask and probability limitations remain correct.
- **AC03 — C19 sufficiency:** All 346 callback inputs and actual row-output comparisons can be independently recalculated from the proposed derivative, with correct ordering, selected append behaviour, unchanged cases and operator/timing limitations; no invented producer lineage.
- **AC04 — Fidelity:** Exact source-to-derivative transformations, source/member identities, hash and size manifests and independent validation are provided; review identifies what cannot be independently traced back to historic raw captures.
- **AC05 — Independence:** Advertised public-tier checks run from an isolated text snapshot without `.local-work/` and without privileged historical sources, and negative tests reject altered, missing or duplicated cases. Pending assets are not mislabelled publicly accessible.
- **AC06 — Publication classification:** Every proposed file/asset has exact rights/privacy, licensing/provenance, indispensability and disposition records. No restricted payload is staged in a tracked path without approval.
- **AC07 — Central run card:** The canonical run card exists, is discoverable from publication navigation, provides a working release-state/checkoff and evidence/asset/tag schema, and does not preapprove or execute release actions.
- **AC08 — Gate completeness:** The run card covers initial pinned baseline, B0–B6, selected claim closure, tracked tree/history/refs, original evidence, B4-F1/core/addendum, D5AS/C19 candidates, contributor/privacy/licensing, clean-checkout, diagram rendering, tag/commit, hosted downloads/member hashes, changed-surface review, approvals and stop/review gates.
- **AC09 — Scope/preservation:** Existing reports, scripts and historical verdicts remain intact; no saves, game/native tools, restricted evidence, Git index/refs, published repository or Release assets are changed. Two-concurrent-sub-agent override used only for D5BE.
- **AC10 — Independent completion:** Scientific, engineering, editorial and evidence-access/rights reviews sign off on the exact final snapshot; each Q and AC has explicit disposition with outstanding dependencies separate from successful local validation.

An AC requiring material not actually available must be **BLOCKED/REWORK**, not passed by substituting a high-level summary. The task may return independently accepted partial packages, but should not call D5BE complete if the indispensable result is missing.

## 9. Handoff format

At completion, provide:

1. Concise Q1–Q5 and AC01–AC10 disposition matrix and separate independent-review verdicts.
2. Exact changed-file list, task-only and complete patch paths/hashes, starting and ending HEAD/index state, and any supplied-brief handling.
3. D5AS/C19 source and proposed output file/member manifests (sizes and SHA-256), permissions/dispositions, reproducibility commands, positive/negative test receipts, and missing/restricted evidence.
4. Link to canonical publication run card and its dry-run evaluation; explain its pending later approvals and tags/assets.
5. Specific next dependencies (particularly B4-F1 membership/asset authorization and B6) without claiming their closure.

**Do not commit, stage, push, tag, upload, publish, or change repository visibility.** The maintainer will critically review the diff before deciding on integration. Publication status remains **NOT READY / NOT CLEARED** until separate B6 and maintainer release authorization.
