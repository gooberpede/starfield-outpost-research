# RG2-D5BF — Final Evidence Selection, Clearance and Release-Asset Preparation

**Project:** `starfield-outpost-research`  
**Status:** Implementation assignment; **not** permission to publish  
**Target:** Starfield.exe retail **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`  
**Authorized concurrency:** **At most two concurrent sub-agents for D5BF only**. The standing one-concurrent-sub-agent rule resumes when this assignment ends.  
**Git policy:** No staging, committing, pushing, tagging, release creation, upload, or repository visibility change.

## 1. Purpose and controlling authority

Complete the **existing** evidence-asset selection and technical preparation for the first, executable-version-pinned research release. Deliver an exact, independently reviewed local asset set and a single authoritative proposal for later B6/publication approval. Do not commission another open-ended inventory or research programme. Reuse already assembled and qualified candidates unless a concrete defect or authorized selection change requires rebuilding.

Controlling material, in precedence order where relevant:

- `docs/PUBLICATION.md`, `docs/PUBLICATION_RUN_CARD.md`, `docs/DECISIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/audits/publication-readiness-b0/release-gates.md` and the B3 pinned baseline.
- B4-F1's actual local packages and reviewed selection: `docs/audits/publication-readiness-b4/f1/{README.md,assets.csv,members.csv,file-dispositions.csv,privacy-policy.md,coverage.md,review.md}`.
- D5BE's prepared derivatives, evidence index, manifests, verification scripts, original reviews and local candidate packages: `docs/audits/evidence-access-d5be/` and the exact artifacts/receipts it identifies.
- D5AX's claim–evidence dependency graph and D5AW's publication-independence requirement; existing historic reports and reviews. The 18 guides and native-function catalogue provide context, **not** replacement primary evidence.

The project's `.local-work/` is **disposable after publication**. Any indispensable released-claim dependency must eventually be in a tracked public file, an approved verified GitHub Release asset, or a truly reproducible public-input method. For this assignment, approved *staged* bytes may establish preflight readiness; do **not** declare them hosted or public. Maintain `NOT READY / NOT CLEARED` until the separate release gates are satisfied.

## 2. Maintainer decisions — do not reopen without concrete contrary evidence

### 2.1 Intended release set

The maintainer approves the following **four groups as the intended release set**, subject to exact file/asset checks and later final authorization:

| Group | Expected source and composition | Current starting point |
| --- | --- | --- |
| **B4-F1 CORE** | **25** unchanged first-party saves, including S-series, position controls, Save29, Save52/HIST-0267, HIST-0255 and HIST-0036 | Local provisional 104,046,934-byte ZIP; authoritative original-member manifest in F1 |
| **B4-F1 ADDENDUM** | **27** members: **14** unchanged first-party saves and **13** unchanged JPEGs | Local provisional 80,827,444-byte ZIP; optional to readers but intended to be included |
| **D5AS derivative** | The reviewed, complete-reference/30-sample canonical geometry comparison candidate, including its exclusions, classifications and provenance | Local D5BE candidate, expected 176,733 bytes; verify exact manifest, do not trust this number without rehash |
| **C19 derivative** | The reviewed 346-callback native UI input/output comparison candidate with ordered inputs, row identities and provenance | Local D5BE candidate, expected 189,747 bytes; verify exact manifest, do not trust this number without rehash |

**Default:** retain all 52 F1 originals, include the ADDENDUM as a separate optional download, and include both separate D5BE derivatives. Do **not** prune for small size gains. A particular item may be `HOLD` only for an evidenced material defect or unresolved specific distribution issue; record its exact claim consequence and maintainer decision. A missing protected original is not permission to invent or reconstruct it.

### 2.2 Maintainer's derivative-distribution policy

The maintainer has expressed an affirmative **project publication preference** to distribute the D5AS and C19 **bounded game-derived research derivatives as-is**, analogously to explanatory screenshots, clips, and gameplay/wiki analysis, **provided the inspected exact payload stays below the following boundary**:

- **Do not distribute** compilation-ready Bethesda/third-party source code, executable code or executable-equivalent reconstruction; whole extracted game archive assets; or complete/unmodified exported game resources that substitute for the executable, ESMs, libraries, content archives, configuration files, or third-party plugins/material.
- **Do not claim ownership, rights or sublicensing authority** over any of those upstream works. Clearly distinguish the copyright/licence for authored research/verifiers from the status of game-derived data in the derivative.
- The accepted *working premise* is that the small canonical geometry comparison bytes and UI input/row comparisons, as actually described in D5BE, are acceptable bounded, non-substitutive research evidence. **Inspect the exact staged bytes to confirm this premise** rather than relitigating generic screenshot-equivalence or demanding written permission by default.
- A concrete exception (e.g., unexpectedly embedded whole proprietary files, compilation-ready proprietary source, protected third-party content, credentials, identifiable account data, or a substantially substitutive reconstruction payload) requires a **file-specific HOLD**, precise location/impact and a proposed minimal remedy or maintainer choice. Do not infer that the policy confers a legal licence or removes any applicable upstream restrictions. Note residual legal uncertainty fairly and succinctly; do not turn unevidenced theoretical concerns into blanket holds.

No game-derived data is automatically relicensed under the repository's `GPL-3.0-or-later`; that licence applies only where the contributors have the necessary rights. Preserve the existing notices and attribution requirements. **Selection preference and documented risk acceptance are not the final explicit authorization to distribute/upload**; that occurs under the later B6/publication run card.

### 2.3 Original-save policy

For F1 saves and screenshots, preserve first-party producer/provenance, exact original filenames, byte identity, scoped privacy screening and individual membership decisions. **Never alter, sanitize, resave, redact, patch or re-encode original save bytes or screenshots.** Lossless enclosing archive compression is allowed with member-for-member verification. First-party eligibility and historic `C:\Users\User`/character-name policy were already settled in F1; do not restore the former generic written-permission hold. Exclude donor originals without separately approved redistribution authority. Reopen a member only for actual contrary evidence or newly established restriction.

## 3. Controlling questions and deliverables

### D5BF-Q1 — Final F1 original-evidence selection and archive identity

1. Confirm the **exact 25 CORE / 27 ADDENDUM members** against F1's selected original identities, paths, sizes, hashes and prior privacy/provenance determinations. Verify `Save52 = HIST-0267`, distinct from `HIST-0255`/Save41, and preserve the S4C/L0 dependency without duplicate logical members.
2. Verify the existing archives, extracted member bytes, safe member paths, original basenames, no duplicate/extra/missing members, completeness of the declared ZIP manifests, and exact container hashes against current local candidates. Check candidate input protection without touching originals. Do not unnecessarily recompress and thereby change accepted ZIP identity.
3. Review actual per-item distribution eligibility: unchanged first-party status, practical privacy, permitted content granularity, upstream notices, and exact claim utility. Carry forward F1 reviews when hashes match. Record any new concrete issue rather than perform speculative exhaustive decoding of unrelated game state.
4. Either qualify the original packages as exact **release-candidate assets** or identify precisely what is held. If rebuilding is necessary, give reason, old/new hashes, unchanged-original proof and independent full comparison. Never silently substitute or rewrite a selected item.

### D5BF-Q2 — D5AS and C19 final derivatives

1. Recover the exact prepared D5BE candidates, verify their byte identities, internal contents and claimed provenance against original source evidence and D5BE independent reviews. Do not accept a manifest without checking staged payload bytes and running both standalone verifiers with explicit paths.
2. Recheck the decisive D5AS contracts: **30** complete canonical sample bodies, two exact reference bodies, positions **7 and 13** matching the mask-0 reference, **28** mask-3 matches, exclusions/replacement, and separation between direct generating-mask observation and geometry-class proxy. Preserve distinctions between canonical body, envelope and other geometry byte domains.
3. Recheck the C19 contracts: **346** native row comparisons, **339** three-row and **7** two-row updates, **340** unchanged redeliveries, ordered/folded native inputs and output identities; operator A/B/C display evidence versus native callback evidence; unverified exact display timing and producer ancestry. Do not pretend the derivative reproduces the entire 2 GB WAL or all 35,573 preview evaluations.
4. Conduct the **exact-payload assessment against §2.2**, distinguishing bounded scientific observations from substitutive binary/assets/source material, third-party contributions, account/private metadata and author-created verification code. Record a reasoned recommendation per derivative, with any concrete exceptions. Do not recreate or upload Bethesda archives or other protected binaries.
5. Preserve the D5BE negative tests and implement only bounded corrections justified by an actual discrepancy. Leave raw witnesses protected and local.

### D5BF-Q3 — One coherent release-asset proposal

Produce a durable, machine-readable **proposed release-asset ledger**, plus readable overview, containing at minimum for each of the four intended groups:

- Stable group/asset ID and purpose; `CORE`/`ADDENDUM` optionality; intended inclusion/hold/exclusion.
- Intended final basename, codec, exact bytes and SHA-256; where meaningful, member count, **each** exact member path/name/bytes/SHA-256, original or derivative identity and direct evidence role.
- Source/producer and original review IDs, source/version qualifications, validation command, independent receipt, rights/privacy/attribution decision and named outstanding maintainer approval.
- Planned local handoff path or retrieval procedure (private paths in private receipts when appropriate), planned GitHub Release association with `PENDING RELEASE` URL, and the affected claims for any held/excluded asset.
- Zero unsupported assumptions that an unhashed/stale local artifact is currently available or that a provisional URL already exists.

Reconcile ledger membership and checksums with existing `docs/audits/publication-readiness-b4/f1/` and `docs/audits/evidence-access-d5be/` sources. Prefer **one authoritative new candidate ledger** and narrow cross-references/status changes over creating parallel competing inventories or rewriting historical F1/D5BE review records. Provide a deterministic verification method that checks the staged asset files and every declared member against the ledger; it must reject missing, duplicate, unexpected, corrupted and unsafe-path cases. Keep verification source tracked, with no dependency on `.local-work/` except **explicit asset input arguments**. Determine whether the manifest can travel publicly without exposing sensitive local source paths; keep private lookup in ignored receipts.

**Rights and selection states are independent:** `APPROVED FOR PROPOSED RELEASE`, `HOLD`, `EXCLUDED` or `SUPERSEDED` describes documented technical/distribution candidature only. Record maintainer-accepted policy separately from independent reviewer analysis, and from future exact B6 approval/hosting. No agent can approve its own public release.

### D5BF-Q4 — Publication run-card and B6 handoff

Update `docs/PUBLICATION_RUN_CARD.md` only as necessary to link the final asset proposal, explicitly cover all four groups and preserve the correct order:

1. **Freeze** exact selected commit/tree/history/ref exposure, claim matrix, candidate assets and clearance records.
2. **B6 independent preflight** on a truly isolated checkout with the approved *staged* bytes explicitly supplied; run tracked verification methods and inspect the actual proposed tree, refs/history and rights/privacy/attribution surface.
3. **Separate maintainer approval** for exact tag, draft/upload actions and asset set; only then create the approved tag/draft and upload.
4. **Hosted-byte validation** from actual download URLs, checking full containers and extracted members, and assessing changed disclosure surfaces.
5. **Separate maintainer visibility/timing authorization** before publishing, then post-publication URL/tag/asset/notice checks.

D5BF may fill **planning data** for asset rows and attach candidate/receipt references. Do **not** check off B6, assert a frozen release commit, invent a tag, claim public availability, or run any release action. Preserve `NOT READY / NOT CLEARED`. Supply a concise explicit list of all remaining maintainer decisions and any indispensable selected-claim evidence routes not closed by these four assets; do not expand into a new project-wide scientific audit.

## 4. Execution and review approach

This assignment is sufficiently separable to justify **up to two concurrent sub-agents**, authorized **for D5BF alone**:

- **Sub-agent A:** F1 original members, archive validation, first-party/provenance/privacy and original-byte identity.
- **Sub-agent B:** D5AS/C19 staged candidates, standalone replays, exact-payload derivative classifications and evidence fidelity.
- **Primary agent:** Authority/scope reconciliation, single proposed release ledger, run-card handoff, cross-asset dependency checks, integration and independent review coordination.

Sub-agent work is evidence, not independent acceptance; no reviewer approves their own authored material. Maintain independent scientific, engineering, editorial and file-specific rights/privacy review of the final integrated snapshot. Preserve correction/review history and exact receipts. Avoid unbounded reinterpretation of accepted F1/D5BE research or reopening upstream experimentation merely because the evidence is complex.

**Allowed:** Read/hash existing protected copies and approved candidate files, inspect archives in memory/read-only, run existing bounded verifier scripts, prepare locally staged package corrections when demonstrably necessary, author tracked manifests/verifier code/limited publication documentation, generate ignored local audit receipts and exact patch export. Perform targeted original-byte replay where already authorized and available without mutation.

**Not allowed:** Game or debugger launches, new native experiments, changes to original saves/screenshots, new dependency downloads, extract whole proprietary game archives for distribution, unapproved third-party inclusion, bulk historical rewrite, historical brief/audit archival, disposal of working evidence, public API/contact/permission outreach, Git index/ref edits, commits/pushes/tags, Release creation/upload, visibility changes or any publication action. Any operation beyond these boundaries requires separate maintainer authority. Preserve protected inputs and the prior sub-agent standing rule outside this task.

## 5. Acceptance criteria

| ID | Pass condition |
| --- | --- |
| **AC01** | Q1 accounts for all **25 CORE and 27 ADDENDUM** first-party originals, with provenance, correct Save52/HIST-0255 identity, exact preserved names/bytes and independent complete archive/member comparisons or explicit scoped HOLD. |
| **AC02** | Q2 re-verifies the exact D5AS complete-body candidate (30 qualified, two classes, one excluded attempt/replacement) against independent inputs/methods; no mask-winner overclaim. |
| **AC03** | Q2 re-verifies the exact C19 346-input/row derivative and relevant unchanged/change counts; does not invent a full WAL or screen-render replay. |
| **AC04** | Derivative file-specific decision applies the maintainer's §2.2 release preference and non-substitution boundary to inspected bytes; documents real exceptions only and neither assumes GPL rights in upstream data nor restores an unsupported generic hold. |
| **AC05** | Final proposal contains **four independently identifiable assets** with exact hashes, sizes, paths, member manifests, reproducible commands, claim links and distinct selection/clearance/hosted states. No invented URLs. |
| **AC06** | Tracked verifier, with explicit input paths, independently rejects mismatched, missing, duplicate/extra, unsafe or corrupted asset/member cases; standalone logic does not require preexisting `.local-work/` or private caches. |
| **AC07** | Existing F1/D5BE research, provenance, historical negative observations and originals are unchanged; approved local candidates are reused unless an evidenced change is explained and independently checked. |
| **AC08** | Run card accurately incorporates asset proposal and **preflight → approved draft hosting → hosted verification → separate final release authorization**; all premature gates remain PENDING and status remains NOT READY / NOT CLEARED. |
| **AC09** | Independent science, engineering, editorial and distribution/rights/privacy reviews inspect the **exact final snapshot** and reconcile all outstanding holds and input-access limits; substantive discrepancies lead to REWORK, not unchecked ACCEPT. |
| **AC10** | Exact changed-file manifest, complete/task-only diffs and byte/hash/forward/reverse checks are recorded; HEAD/index and protected inputs are preserved; no unauthorized disclosure, tag, upload or publication occurs. |

Report each Q1–Q4 as `COMPLETE`, `REWORK` or `BLOCKED` with independent reasons. A concrete `HOLD` on one group need not make all unrelated groups fail, but D5BF must not claim a four-asset **ready** set if indispensable selected bytes cannot be accounted for. A review pass is not distribution authorization.

## 6. Delivery and handoff

Return:

1. Exact changed-file list, hash manifest and task-only/complete patches (the latter may include the unchanged supplied brief), with clean HEAD/index status.
2. Final 4-group proposal ledger, actual staged asset identity and exact verification receipts; retain private local paths and sensitive findings in ignored receipts where appropriate.
3. Clear table of file-specific selection recommendations, maintainer policy applicability, holds/exclusions and claim consequences; distinguish *proposed-release eligibility* from *final authorization*.
4. Updated publication run-card planning links, outstanding release decisions and evidence routes outside this assignment.
5. Independent final dispositions for Q1–Q4 and AC01–AC10, with the actual tested snapshot and precise limits.

**Stop at local evidence/package preparation.** The next separately authorized steps are final maintainer selection and claim-dependency reconciliation, coordinated historical brief/audit archival near release, and independent B6 candidate assessment. The release target remains **Starfield.exe 1.16.244.0**. No release tag or asset publication is approved here.
