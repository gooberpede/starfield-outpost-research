# SOR RG2 — D5CA: Final Repository Exposure and Release-Candidate Audit (Roadmap 7C)

**Assignment type:** read-only publication-readiness audit and decision preparation.
**Status at issue:** publication **NOT READY / NOT CLEARED**. This brief grants no public disclosure, release action, source mutation or scientific experiment.
**Repository:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`).
**Predecessor:** D5BZ (7B), committed and synced by the maintainer.
**Next gate:** a separately authorized exact-candidate freeze and isolated B6 preflight, followed by separate release-operation approvals.

## 1. Purpose and controlling decision

Determine whether the **actual proposed first-publication surface** is suitable to freeze for B6: the current repository tree, the complete Git object history reachable through the *proposed* public refs, both D5BZ archive containers and every member, active research inputs and methods, and nine proposed supplementary evidence assets. Produce a reproducible, independently reviewed **freeze-readiness dossier** with concrete exposures, blockers, accepted qualifications and explicit maintainer decisions. **Do not freeze, tag, change visibility or publish.** A successful D5CA result means *READY TO PROPOSE FREEZE*, not B6 PASS or public-release approval.

The selected scientific scope is the reviewed, bounded Starfield **1.16.244.0** runtime-and-persistence research archive in `docs/first-release-scope.md` and the accepted D5BV route overlay: **71 inherited claims, 31 inherited actions, 110 inherited edges, 68 selected distinct routes and 126 selected claim–route joins**. These are different denominators. No new research is presumed necessary. Historical negative findings, held stronger tiers, unknown original-save builds, conditional D5AG native stage and D5BD historical source reconstruction retain their existing dispositions. Do not manufacture a release blocker from a known, disclosed optional research gap.

### Controlling questions

- **D5CA-Q1 — Exact public exposure:** What files, ZIP members, Git objects/refs, sensitive material, rights, credits, metadata and operational surfaces would actually become reachable through the proposed publication, and what concrete issues remain?
- **D5CA-Q2 — Release-claim and method sufficiency:** Do the currently selected claims and indispensable reader/method dependencies have accurate authoritative wording, qualifying negative cases and proposed independent access routes after D5BZ relocation, without an undisclosed private `.local-work/` dependency?
- **D5CA-Q3 — Evidence custody and distribution decision:** For each of the **nine** individually selected candidate assets, are identity, actual content exposure, file-specific approval, lawful prerequisites, durable custodian, retention and proposed transfer/hosting route sufficiently documented to support the next gate?
- **D5CA-Q4 — Freeze readiness and B6 handoff:** Is there a complete, actionably classified decision dossier with actual candidate identifiers, exact proposed ref boundary, unresolved issues, reproducible checks, run-card reconciliation and a clear recommendation about readiness to freeze?

An answer of **BLOCKED** requires a demonstrated indispensable missing edge, reason, attempted non-destructive checks, smallest remedy and separate required approval. Ordinary found defects must be diagnosed within this assignment's authorized read-only scope. A controlling question is not COMPLETE merely because a scanner ran or a previous reviewer reported PASS.

## 2. Mandatory source reading and authority

Read complete relevant portions, following continuations of truncated tool output, and record their actual application in the audit ledger:

1. `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/templates/completion-contract.md`, `docs/EDITORIAL_STANDARD.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/PERMISSIONS.md` and `docs/DECISIONS.md`.
2. `docs/PUBLICATION.md`, `docs/PUBLICATION_RUN_CARD.md`, `docs/first-release-scope.md`, `docs/reference/evidence-access.md`, `docs/PROVENANCE.md`, `docs/SOURCES.md`, `CREDITS.md`, `THIRD_PARTY_NOTICES.md`, licensing and third-party policy files, and the current guides/reference/history entry points.
3. `docs/archive-verification.md`, `docs/archive-containers.json`, `docs/audits/{README.md,archive-index.csv,audits.zip}`, `docs/implementation-briefs/{README.md,archive-index.csv,implementation-briefs.zip}`, and current `research/archival/` verification methods. Historical D5BZ/D5BY/7A reports are now **ZIP members**: resolve through the exact archive indexes, do not assume old loose paths still exist.
4. Active sources at `research/evidence-data/`, particularly D5BG claims/actions/edges, D5BR readiness, D5BU original-source records, D5BV routes, D5BW candidate selection, D5BX supplement manifest, D5BF asset ledger and current-source edition; read their primary scientific/control crosswalks as needed. `docs/history/claims.md`, `docs/history/evidence-routes.md` and `docs/history/research-identifiers.md` are reader-facing access points, not substitutes for accepted original sources.
5. The B0–B5/RR1 gates and D5AW/D5AX design, D5BV handoff, D5BW and D5BX decisions, and D5BZ final attestation via indexed historical archive members. Preserve earlier independently reviewed statuses; no retroactive amendments.

Verify the current `HEAD`, index, worktree and applicable remote/ref facts at intake. The repository may have changed since the D5BZ seal: establish the **actual fresh denominator** and the exact checked revision, not historic inventories. An apparently clean `git status` is not proof of a clean disclosure history.

## 3. Authority and exclusions

**Authorized:** read-only Git inspection (`rev-list`, `show`, `cat-file`, `for-each-ref`, object reachability and inventory), safe text/ZIP/member examination and exact hash checks, bounded review of identified local candidate evidence **read-only** under its existing protection rules, static source and link analysis, no-network/offline checks, independently repeated source-only mechanical validation, and writing **new** audit outputs beneath `docs/release-candidate-audit-d5ca/` plus disposable, ignored scratch and the prescribed review patches. Read-only GitHub inspection is permitted only for repository/ref factual discovery, without any remote mutation. Obtain explicit approval before inspecting a genuinely new protected input or undertaking a broader protected-content decode not covered by previously approved reviews.

**Prohibited:** altering tracked scientific text, historical documents or archives; changing evidence originals; creating or deleting branches/tags/refs, committing, staging, pushing or rewriting history; changing remote visibility or GitHub settings; issuing a draft Release, transferring/uploading assets or sending data to third parties; running the game, injecting native code, starting new gameplay experiments, probing installed proprietary binaries beyond approved read-only identity checks, or performing new reverse-engineering work. No private credential or unnecessary sensitive payload should be copied into audit outputs. Scrub diagnostic excerpts to the minimum needed to demonstrate a finding; retain a secure internal locator separately where appropriate.

**Run-card choice:** `docs/PUBLICATION_RUN_CARD.md` already has A–G gates, a seven-plus-two inventory and a D5BZ handoff. For D5CA **audit** its currency and prepare a precise **proposed edit list or optional non-integrated patch in ignored scratch**, including any obsolete archival instructions, missing custodian/transfer columns and final freeze/B6 distinctions. **Do not modify the tracked run card in 7C.** Make its implementation and release-specific receipt population an explicit first action of a separately authorized B6 preparation task. Do not mark PENDING gates PASS, invent approvers, dates, URLs or test receipts. A genuinely dangerous reader-facing misstatement is a concrete 7C issue and may require a separately approved pre-B6 correction.

## 4. Required examination

### 4.1 Proposed refs, history and current tree — Q1

Build an exact, reproducible inventory of the current tree and all locally known refs; distinguish local branches, remote-tracking refs, annotated/lightweight tags, GitHub refs discoverable with read-only access, stash/reflog-only objects, unreachable/unpublished local objects and release-associated existing artifacts. **Reachability is computed from explicit candidate public refs**, not from every object in `.git` indiscriminately. State remote visibility and fetch limits honestly; do not claim an exhaustive remote history if API/ref access is incomplete. Record commit/tree IDs, ref target, object sets, types and sizes, unusual/bulk blobs, and overlap across proposed and nonproposed refs. Do not assert that an unpublished local ref would automatically become public.

**Default proposal:** disclose ordinary `main` ancestry; do not publish other branches, tags or Codex refs merely because they exist. Review the full proposed reachable history, not just HEAD. Search current text, archive members and reachable historical blobs for credentials/authentication material, private communications, material personal identifiers, absolute paths, proprietary binaries/save dumps, third-party material and deceptive prior authority. Use both targeted automated detection and manual examination of material positives and representative negatives. Classify separately: (a) confirmed significant exposure, (b) knowingly accepted historical path/basename or harmless provenance, (c) uncertain substantive risk needing decision, (d) false positive. Historical failure or superseded text is not itself a reason to rewrite history. Do not reproduce actual secrets in outputs.

Determine whether historical D5BD source commit `6e799a428a765aa196a24d3c1de8ae133260aa08` (tree `7a1f6fdd6728a8f98bc92ef7ee6c9b24a62f0e0e`) is reachable from the *proposed* public refs and independently usable under the source/edition contract. If not, report the effect on the advertised exact-source reconstruction and offer bounded choices: independently qualified frozen source provision, or documented authored-inspection-only tier. Do **not** widen public Git refs to rescue the method automatically.

Inspect exposed scripts and workflow instructions for upload-enabled automation, unsafe destructive steps, obsolete approval statements and accidental implicit authorization. Keep scientific authority, release permission and technical function integration separate.

### 4.2 Two sealed D5BZ archives and disclosure — Q1/Q2

Recheck both full ZIPs and CSV member indexes against `docs/archive-containers.json` and `docs/archive-verification.md`: **335 audit + 259 brief members = 594** at the sealed D5BZ edition (re-census the new tree independently). Check every member's path, size, SHA-256, extraction safety, actual content screening and exact historical classification, including the 7B governing brief, six pre-seal records and old policy/custody/path files. Distinguish ZIP member content from loose-tree content; hiding material in a ZIP does not remove it from public exposure. Do not rebuild or rewrite the sealed ZIPs. Validate the README/index retrieval instructions, download/extraction procedure and nonrecursive external attestation. Any changed archive identity is a blocker until separately reviewed.

Check active datasets and authored scientific files relocated from `docs/audits/` against the D5BZ migration map. Current code must use its qualified current operands; an old historical locator cannot silently substitute. Confirm no historical audit subdirectories remain at the proposed HEAD. Preserve the old scientific evidence/reviews through their approved current locations or exact indexed archive records.

### 4.3 Claim, current reader and method closure — Q2

Use the actual current D5BG/D5BR/D5BV active datasets and selected source edition to regenerate an inventory keyed by **claim ID, exact selected wording, evidence route ID, tier, indispensable dependencies, negative controls, version/build, execution prerequisite, current reader, authoritative citations and public access state**. Account for all 71 claims, 68 selected routes and 126 joins; do not convert inherited holds to clears. Identify any claim requiring unapproved inputs, missing tracked source or a nonfunctional path. Distinguish: tracked self-contained methods; source-first user-supplied lawful inputs; selected original save witnesses; recorded derivatives; conditional D5AG native execution; historical-only/attributed tiers. The latter are not advertising full replay.

Perform source-only checks suitable for this audit, including exact current method paths, import/manifest closure, archived-vs-active locator resolution, example arithmetic and safe synthetic refusals. For execution needing game inputs or protected originals, inherit accepted D5BU/D5BX/D5BZ receipts **only when the exact source/input version matches** and label this as inherited—not newly rerun. B6 is responsible for fully isolated reproduction. Check `docs/first-release-scope.md`, guide/reference descriptions and release notes proposal for genuine contradictions, misleading certainty, omitted limits and stale `PENDING RELEASE` status. Keep the accepted Q2/Q3 historical D5AG refusals and no universal winning-mask prediction. Include concrete reader-journey checks to find C19 and D5AG current answers and their historical dispositions.

### 4.4 Nine selected evidence assets, custodians and practical exposure — Q3

Evaluate the exact seven D5BW-approved groups and two D5BX supplementary groups identified in `docs/reference/evidence-access.md` and their machine manifests. The list is:

1. `sor-1.16.244.0-b4-f1-core-stored-provisional.zip` — 25 saves.
2. `sor-1.16.244.0-b4-f1-addendum-deflate-provisional.zip` — 14 saves + 13 JPEGs.
3. `d5as-feynman-geometry-v1.zip` — 33 members.
4. `c19-callbacks-v1.json` — one exact JSON file.
5. `d5bh-episode-witness-v1.zip` — 27 members.
6. `SOR-D5BI-N2-projected-evidence-v1.zip` — six members.
7. `SOR-D5BO-B2-projected-evidence-v1.zip` — two members.
8. `sor-d5bx-workshop-roots-v2.zip` — three members, exact canonical ledger inside.
9. `sor-d5bx-cargo-c3-v1.json` — exact unchanged JSON, including four approved historical path fields.

For each: record exact name, length, digest, archive/member inventory (if relevant), current local custody and genuine read accessibility, derivation/provenance, claim joins, file-specific privacy/rights decisions, material exposure findings and accepted residual limits. Verify exact candidate identity pre/post any permitted read. Do not recalculate prior scientific results unnecessarily, nor treat inability to see an existing lawful/private file as authority to acquire one from elsewhere. The existing accepted first-party save/screenshot policy and D5BW's bounded assessment stand; avoid reopening generic legal or speculative reconstruction questions. Flag only file-specific concrete exposure or materially new findings. Retain donor F061 exclusion, no raw saves in Git, and no claim of Bethesda permission or zero residual risk.

Produce an explicit proposed **custodian and retention/transfer matrix** independent of disposable `.local-work/`: named responsible role (individual name only if supplied), current sealed bytes, candidate durable location (normally versioned GitHub Release assets), transfer prerequisites and approved/unapproved states, prospective download validation method and expected custody through B6. **A proposed destination is not a verified URL.** If custody is not yet established, mark pending, distinguish *pre-freeze decision needed* from *B6/upload gate*, and state its impact on individual claims. No copying to public locations or upload is authorized.

### 4.5 Rights, public-facing instructions and final handoff — Q4

Review actual credit/contributor authority (R3), source and excerpt/granularity boundaries (R4), GPL-3.0-or-later scope, Bethesda/game-derived notices, third-party/dependency notices, SFSE header grant conditions, attribution and privacy throughout the proposed exposure. Assess actual current text and reachable historical content without assigning fictional authors/ownership. Document discrete remaining maintainer choices. Keep policy concessions already agreed intact.

Provide **a single ranked issue ledger** (BLOCKER, REQUIRED BEFORE FREEZE, B6/UPLOAD GATE, ACCEPTED RESIDUAL, NONBLOCKING/DEFERRED) with exact object/path/asset, tested evidence, materiality, consequence, smallest correction or claim-scope alternative, required approver and retest boundary. Do not automatically narrow selected claims or rewrite history. Produce a proposed **freeze card** naming candidate HEAD/tree, proposed refs/history boundary, nine asset pins, two archive pins, active evidence-source edition, method/link controls, version/build and conditional prerequisites. The card must remain *PROPOSED* and allow explicit maintainer corrections before freezing.

Run a bounded navigation/source-path audit, case-sensitive links/fragments, archive search/extraction directions, untested URLs, release instructions and mechanical Mermaid syntax. **Actual visual Mermaid rendering** and full isolated evidence execution belong to B6; give it the precise diagrams and methods to inspect. Check the run-card A–G fields and draft a change ledger for its B6 update, identifying stale instructions and all pending signoffs. Do not edit the tracked card here.

## 5. Deliverables

Create under `docs/release-candidate-audit-d5ca/` (subject to normal approved source-tree placement):

- `README.md` — question statuses, exact scope, verdict, release NOT CLEARED and navigable dossier.
- `intake-and-surface.md` plus machine-readable `tree-and-refs.json` and `exposure-inventory.csv` — current/old tree identities, proposed ref boundary, remote limitations, reachable objects, content-screen findings and archive treatment.
- `history-and-d5bd.md` — actual historical reachability and exact-tier options.
- `claim-and-reader-closure.csv` and `claim-and-reader-closure.md` — full selected-route/dependency reconciliation, with distinct inherited and newly observed evidence.
- `asset-and-custody.csv` and `asset-and-custody.md` — all nine identities, file reviews, availability/custodian/retention and proposed hosting/transfer decisions.
- `rights-and-exposure.md` — concrete R3/R4, licensing, privacy and disclosures including ZIPs and reachable historical blobs.
- `issue-and-decision-ledger.md` — ordered, actionably scoped findings and explicit maintainer choices.
- `freeze-readiness.md` — proposed candidate identities/refs and rationale for READY TO PROPOSE FREEZE or NOT READY, with required 7C corrections and exact B6 handoff.
- `run-card-reconciliation.md` — precise A–G updates needed, assignment of B6/freeze/upload owners and no fictitious passes; optional ignored scratch-only patch, not an integrated document change.
- `investigation-ledger.md` — applied reading, check methods, failed/negative cases, controls and remediation trace; `review.md` — verbatim independent review, criteria and scope limitations.

Make machine tables deterministic, documented and independently reproducible. Avoid unnecessary personally identifying excerpts and duplicate huge source data. If future reader paths require an index, use only an independently reviewed, narrow navigation amendment within this authorized new audit folder. Do not change D5BZ sealed packages or existing public-facing documents.

## 6. Mandatory acceptance criteria (frozen)

- **AC01 — Authority and intake:** complete applied reading, exact HEAD/tree/index/worktree identity, approved read-only bounds and evidence protection; preserve original files and history.
- **AC02 — Exact disclosure graph:** enumerated local/remote refs, candidate public set, reachable history/objects and stated incomplete views; manually challenged exposure positives/negatives, with no assumption that all local objects will be published.
- **AC03 — Historical exposure and D5BD:** real privacy/credential/rights scanning across reachable history, concrete severity classification, D5BD object reachability and bounded exact-replay disposition without unauthorized ref widening.
- **AC04 — Sealed archive coverage:** exact verification of both container/index/member sets (335+259 sealed edition), safe extractability and every member included in exposure screening; no ZIP or member changes; authoritative indexes usable.
- **AC05 — Scientific fidelity:** reconcile all 71 inherited claims/31 actions/110 edges with 68 selected routes and 126 joins, controlling source/review and distinct selected/held tiers; no unsupported promotion or covert narrowing.
- **AC06 — Method access:** assess tracked, relocated, conditional, original-witness and historical method dependencies with exact current source edition, private-source boundary and appropriately labeled inherited/new checks; give claim-specific effect of any gap.
- **AC07 — Nine assets:** exact identities, actual file/member exposure observations or explicit inability, prior selections, rights/privacy scope, concrete findings and intact protected originals; nine-by-nine accounting complete.
- **AC08 — Custody plan:** per-asset responsible custodian role, durable post-`.local-work/` retention and versioned hosting proposal, transfer/approval state, independent retrieval and hash-check plan, honest still-pending decisions.
- **AC09 — Rights/credits/safety:** R3/R4/third-party/GPL/SFSE/first-party policies applied to actual surface, with no invented permission, excessive speculative legal re-litigation or overlooked material issue.
- **AC10 — Documentation/run card:** current reader, index, diagrams and reproduction instructions surveyed; actual broken current-facing paths or stale approval claims classified; run-card A–G reconciliation prepared without changing tracked card or setting PASS.
- **AC11 — Freeze decision and gate separation:** precise proposed tree/ref/asset/archives/source-card and ranked blockers, accepted residuals, maintainer options, B6 isolation, native conditional and visual-rendering handoff; 7C is not the release or freeze itself.
- **AC12 — Independent completion and delivery:** independent reviewer reads original brief and primary evidence, challenges completeness and material exposure, returns D5CA-Q1–Q4 COMPLETE/INCOMPLETE/BLOCKED and AC01–12 PASS/FAIL/NOT TESTED, separate scientific/engineering/editorial verdicts, ACCEPT/REWORK/ESCALATE, verified exact patches and truthful limitations.

## 7. Work discipline, controls and review

Apply the project completion contract and editorial standard. First create an active audit ledger; identify all protected operands and scope before opening them. Preserve failed checks, rejected explanations, exact negative controls, method effects and original readings. No arbitrary deadline, proof-by-checklist or self-declared independent acceptance. Use a distinct read-only independent reviewer; follow the project single-active-specialist rule and report all reviewer iterations. Correct in-scope audit defects and rerun checks under **the same** D5CA assignment; preserve original frozen criteria and earlier review dispositions. If genuinely blocked by missing authority, provide the exact smallest approval needed; do not silently skip material inspection and call it a pass.

At finalization, produce the complete and task-only review patches in `.local-work/diffs/` with a descriptive `d5ca-` prefix (both, if there are unrelated uncommitted changes; otherwise at least complete). Include all new/untracked text; provide a path/status manifest, ignored/binary exclusions, `git diff --check`, LF/trailing-whitespace controls, internal links, byte-exact forward/reverse reconstruction and actual-tree reverse applicability. The controlling brief supplied under `docs/implementation-briefs/` is part of the complete patch, not task-only changes. **D5BZ's archive is sealed:** do not rebuild it to absorb D5CA or this brief. D5CA's own brief/audit documents are current pre-release materials; any proposal to append a new archival edition is a separate future decision, not an implicit completion requirement.

**Exit:** submit the independently reviewed dossier and a succinct recommendation: `READY TO PROPOSE FREEZE`, `NOT READY — SPECIFIC CORRECTIONS`, or `ESCALATE — MISSING AUTHORITY`. No stage/commit/push/tag/release/upload/visibility action. Publication remains **NOT READY / NOT CLEARED** until the separately approved freeze, B6, hosting checks and final signoffs are complete.
