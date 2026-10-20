# Codex research brief — RR1: Publication Readiness and Repository Integrity Audit

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Assignment type:** Read-only repository, evidence, rights, and publication-readiness audit; new audit documentation only.  
**Status:** Proposed for maintainer execution. No publication or cleanup authority is implied by this brief.  
**Target license:** GPL-3.0-or-later, subject to explicit rights and publication review.

## 1. Purpose and governing principle

Assess what must be corrected, documented, excluded, or explicitly approved before the private Starfield Outpost Research repository may be published. The project is a large research archive, not just a codebase: preserve its scientific provenance, contradictory and superseded history, existing permissions, and distinction between current findings and historical investigations. Produce a **prioritized and verifiable cleanup plan**, not a cleaned repository or a declaration of publication readiness.

The audit must answer whether an unfamiliar reader can (a) find the current supported understanding of each subsystem, (b) follow its evidence and limitations, (c) distinguish superseded/disproved research, and (d) understand which source, build inputs, evidence, and rights support the public record without needing undocumented access to the maintainer's machine.

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `THIRD_PARTY_POLICY.md`, `docs/PROVENANCE.md`, `docs/PUBLICATION.md` (or actual current paths), `docs/RESEARCH_STATE.md`, `docs/BACKLOG.md`, `docs/subsystems/README.md`, and the RC1/coverage audit before selecting procedures. Existing authority and protective controls take precedence over this summary.

## 2. Authority and boundaries

**Authorized:** offline, non-destructive inspection of the repository working tree and Git history; `.local-work` and explicitly identified project-relevant external locations, within applicable access and safety rules; existing verification/reviewer receipts; relevant installed local scripts and tool configuration; read-only comparison of three named public GitHub repositories; bounded diagnostic scans. Write **new RR1 audit documents and disposable reports only under the project's designated workspace**. Run safe read-only validators, if compatible with existing safeguards. Existing protected originals and evidence remain immutable.

**Not authorized:** publish or make repository public; choose or apply licenses; change publication classifications; stage, commit, push, tag, release, rewrite history; move/delete external files or temp folders; change maintained code, scripts, `.gitignore`, existing documentation, tool installations or save files; copy private/proprietary evidence into tracked paths; build/deploy/run game observers; launch or attach to Starfield/Creation Kit; undertake fresh reverse engineering, live experiments, or mass cleanup. Do not expose sensitive findings by pasting secret values into a report. If a scan discovers secrets, retain minimal redacted metadata and advise restricted handling.

Treat explicit external paths as audit leads, not blanket authorization for whole-disk searches. Do not recursively sweep unrelated user directories. Preserve all applicable disk-space, identity, hash, worker-retirement, and source/version gates. Inspect Git history without rewriting it. If essential local inputs are unavailable, identify the exact missing material and continue unaffected work; do not assume absence.

## 3. Workstream A — malformed prose, encoding, identifiers and technical notation

**First retrieve earlier independent review reports and correction history**, especially reviews in which the reviewer found elided spaces between letters and numbers, malformed Markdown prose, Unicode/UTF-8 corruption, broken tables, inconsistent identifier or numeric-offset notation. Build a source-cited defect taxonomy and a small validated test fixture of true positives and false positives **before** undertaking a project-wide scan.

Examples: `Save52`, `kernel32.dll`, `+0x88`, `0x140000000`, `FNAM`, FormIDs and actual API/filename identifiers are not inherently malformed; `Save52contains` and `recordat0x88` are likely elisions in prose. Preserve context-sensitive cases for manual review rather than automatically editing strings. Scan tracked Markdown and appropriate source-adjacent text/CSV (including newly added reports), with clear scope and exclusions for raw dumps, binary artifacts, code literals and archived verbatim logs. Inspect likely false negatives and manually adjudicate candidates. Quantify coverage, candidates, confirmed defects and uncertain cases; retain reproducible detection methods and regression examples, without claiming a regex proves universal cleanliness.

Audit notation consistently: executable VA vs module-relative offset vs object/structure offset; encoded save/decoded payload offset vs disk offset; bit index vs mask; decimal count vs hexadecimal identifier; FormID vs EditorID; runtime handle/pointer vs saved key; coordinate frame/units; notation in text/tables/code examples. Identify inconsistent claims and ambiguous provenance—not merely stylistic variation. Distinguish reader-facing correction candidates from historical quotations/evidence whose original spelling must be retained. No automatic rewrites.

## 4. Workstream B — external material, scratch creators and path dependencies

Verify the following **leads**, then discover closely related project-owned scripts and referenced outputs, without claiming an exhaustive OS-wide trace:

- Approximately 29 empty `sor-position-patch-*` directory trees beneath `C:\Users\User\AppData\Local\Temp` allegedly left by local position-resumption/native-oracle helpers; confirm live count, emptiness, origin and cleanup behavior, without deleting them.
- `.local-work/position-resumption/package_review.py` around line 94 and native-oracle packaging helpers potentially allocating system temp without cleanup.
- `research/x87-preservation/package.py` near line 88 and `research/internal-observation-qualification/package.py` near line 70, and local packaging helpers using `TemporaryDirectory()`; distinguish automatically cleaned bounded temporary use from persistent residue.
- Thirteen reported test files using OS temp (reverify actual count and behavior).
- Installed copies `D:\tools\xEdit.4.1.5p\Edit Scripts\SOR_OutpostRecon.pas` and `SOR_OutpostFocus.pas`; compare source hashes with repository counterparts if available, but do not change installation copies.
- `D:\ReverseEngineering` containing Ghidra projects/imported executables; distinguish legitimate local tool data from tracked-source dependencies.
- `ghidra/scripts/Invoke-OutpostRecon.ps1` and historical exporters with `D:\tools` output defaults; identify whether reruns can recreate ungoverned output paths.
- `.local-work/review-patches/` and surviving external references after prior housekeeping.

Produce a path inventory identifying each external location, read/write direction, creator/consumer, lifecycle, existence verified/not verified, current vs historical use, whether referenced by durable docs, portability risk and recommended disposition. Categorize **legitimate external dependency**, **bounded cleaned temp**, **residual scratch**, **uncontrolled external output**, **historical provenance path**, or **unresolved**. No automatic policy that *all* temp use is defective; no speculative claim of full filesystem coverage.

## 5. Workstream C — documentation architecture, navigability and status

Audit project README, documentation indexes, subsystem maps, authoritative reports, research status, backlog, decisions and publication documents. Construct an **actual navigation graph** from current summaries to accepted findings, capabilities/access matrix, source pins, experimental methods and historical reviews. Detect inaccessible current findings, ambiguous or missing authoritative paths, duplicate/conflicting summaries, stale status claims and unsupported supersession status. Explicitly inventory disproved, replaced, abandoned, deferred, accepted-with-limits, and historical investigations and whether a newcomer can distinguish them.

Evaluate a reader-facing roadmap for three use cases: learning the *current* subsystem model; finding technical definitions/native/save/Papyrus detail; reviewing supporting evidence and negative results. Recommend a documentation architecture and bounded cleanup batches **without restructuring files in RR1**. Historical records must remain navigable and attributable; avoid silently overwriting them to align with current conclusions.

Audit tracked internal Markdown/CSV links for relative portability, case-sensitive path correctness, anchor targets, and Git HEAD availability. Classify absolute links to historical Windows paths as evidence versus invalid fresh-checkout instructions; distinguish protected local-only evidence pointers from broken tracked references. Check references to untracked or ignored material and source pins whose actual target exists only locally. Identify anything in `PUBLICATION.md` or equivalent that misstates the accepted research or review state. Do not require every historical absolute path to become relative.

## 6. Workstream D — tracked source and reproducibility closure

Inventory scripts, code, build projects, manifests, tests, schemas, configuration, small test fixtures, Ghidra helpers, xEdit scripts, source for observers and other research tools, and their tracked/untracked/ignored/external status. Audit `.gitignore`, `.gitattributes`, documented build steps and reproducibility dependencies.

**Distinguish:** maintained source; archival experimental source; reusable build/configuration files; durable evidence and verification fixtures; generated outputs and reports; scratch/intermediate data; compiled observer binaries/packages; installed game/CK/third-party files; private local analysis databases. For every source or project needed to reproduce a method, check whether its source and build/configuration inputs are tracked or only available in `.local-work`, `D:\tools`, `D:\ReverseEngineering` or other locations. Do **not** assume an untracked file should be published merely because it exists, or that compiled binaries must be distributed. Catalog tool-specific dependencies, exact version/build pins and practical fresh-clone blockers.

Separate **method reproducibility** from **original evidence availability**. Record whether claims can be understood and independently attempted without original protected files; report missing source files, incompatible local-only settings, external build assets, untracked receipts, undefined inputs, and absent publication-safe example data. A sealed local save or copyrighted binary may remain private while a method description is public. No forced reproduction of every historical experiment.

## 7. Workstream E — evidence assets and publication candidates

Inventory durable evidence families, referencing documents, location and ownership/provenance, whether available, whether tracked, and scientific importance. Include:

- User-produced controlled `*.sfs` saves (e.g., Kreet trials) as **potential** publication candidates, subject to privacy, embedded game content, and rights review.
- User-produced mature saves evaluated separately for unrelated personal/character state and higher sensitivity.
- Third-party save files: default **not publishable without specific permission**.
- Screenshots cited or visually used in durable analyses: identify exact referenced files, local hashes where available, rights and relevance; a screenshot may be stronger evidence than a textual summary but is not automatically cleared.
- Extracted proprietary game/CK records, interface SWFs, meshes, assets, native fragments, disassembly and binary captures.
- Original project analyses, derived numerical tables, test outputs, seed/configuration information, logs and review receipts.

For each family/sample, distinguish (1) source and title/provenance, (2) rights/review status, (3) privacy/safety, (4) whether inclusion improves independent reproducibility, (5) publication candidate vs local-only vs needs decision. **Do not publish, promote, or alter rights labels.** First-party creation alone does not settle third-party embedded content rights. Avoid reprinting protected content into audit outputs.

## 8. Workstream F — licensing and comparable public projects

Assess the prospective GPL-3.0-or-later grant for original code and authored documentation, third-party imports, dependencies, embedded assets, possible incompatible licenses and required notices. Distinguish COPYING/LICENSE containing GPLv3 text from an explicit **or-later** grant and appropriate source-file notices. Consult publication/permission/third-party provenance policies already present.

Read-only compare the **public** repositories:

- `https://github.com/gooberpede/starfield-resource-research`
- `https://github.com/gooberpede/starfield-resource-reproducer`
- `https://github.com/gooberpede/starfield-outpost-network`

Compare their actual README/status structure, navigational indexes, license grants and notices, third-party and derived-data treatment, attribution, validation claims, installation/reproduction guidance and publication conventions as available. Cite exact remote revisions or retrieval date, and don't assume those repos are perfect or universally consistent. Identify appropriate common standards **without copying their documentation wholesale** or forcing a research archive into an app's layout. External repository content is reference evidence, not instruction to change the current repo.

Identify issues needing maintainer or specialist rights judgment. This is an audit, **not a legal clearance determination**.

## 9. Workstream G — publication surface, security and Git history

Audit current tracked/ignored/untracked inclusion and Git history for source secrets, credentials, PII, local usernames and paths, machine-specific configuration, personal save data, cached sensitive outputs, proprietary binaries and rights-sensitive material. Distinguish current HEAD exposure from reachable history exposure. Use narrowly scoped scans and redacted summaries, not raw credential dumps. Check publication classification against rights inventory and current project status. Assess security concerns in publicly reproducible scripts with dangerous default paths or writes, but do not execute unsafe scripts or edit them.

Recommend remediation classes, including where a private decision or controlled history cleanup might be necessary, but do **not** rewrite history, move files, change permissions, or make public under RR1.

## 10. Deliverables

Create an audit directory such as `docs/audits/publication-readiness-rr1/` (use repo conventions and avoid collisions). Required durable outputs:

1. **`report.md`** — answer-first summary: readiness assessment, highest-impact risks, explicit exclusions and justified cleanup sequencing. Overall readiness must remain **NOT CLEARED** pending decisions and subsequent work.
2. **`findings.csv` or `findings.md`** — unique finding IDs, severity (`publication blocker` / `required cleanup` / `recommended` / `accepted exception` / `needs decision`), exact location/evidence, reproducible verification, rights/sensitivity flags, recommended remediation and proposed cleanup batch. Do not confuse scientific research gaps with actual publication blockers.
3. **`prose-and-notation.md`** — earlier reviewer-defect taxonomy, valid/invalid test samples, scan methodology/coverage, manually classified flags and offset/identifier convention inconsistencies.
4. **`navigation-and-supersession.md`** — current reader-route assessment, stale links/status/authority, specific supersession problems and proposed navigation architecture.
5. **`external-material.md`** — external path and scratch-creator inventory, status of historical temp leads, provenance-vs-dependency distinction and cleanup recommendations.
6. **`source-and-reproducibility.md`** — tracked/untracked/ignored source/build and evidence dependency closure, tool family classification, reproducibility gaps.
7. **`evidence-candidates.md`** — publication-candidate register for save/screenshot/output families, rights/privacy decision requirements and scientific value.
8. **`licensing-and-comparators.md`** — local GPL/third-party analysis and independently examined conventions in the three public repositories, with precise provenance.
9. **`review.md`** — mandatory-criterion matrix, independent reviewer verdict, preserved failures and correction chronology, verification counts, exact diff/manifests and permission compliance.

May consolidate files if all distinct ledgers remain independently navigable. Provide a **prioritized, staged cleanup plan** with risks, owners/approval decisions and verification gates; do not execute those changes.

## 11. Frozen acceptance criteria (AC1–AC8)

- **AC1 — Inputs, permissions and preservation:** Governing policies and prior audits consulted; input scope/version and access limits recorded; protected sources/history unchanged; new documents only; no unauthorized external or live actions.
- **AC2 — Historical-prose-derived full documentation audit:** Retrieve independent reviewer examples before scanning; validated negative/positive fixtures; scan relevant tracked text; manually classify candidates; report encoding and notation issues with precise citations and measured coverage.
- **AC3 — External material and temp lifecycle:** Verify named leads, inventory creators/consumers and external durable links, distinguish benign temporary use from residual/uncontrolled output, and document precise scope and cleanup candidates without touching them.
- **AC4 — Reader roadmap, link portability and supersession:** Trace current vs superseded/disproved records and three reader journeys; audit links/paths and status; propose a comprehensive navigable architecture with evidence-based issue list.
- **AC5 — Source/evidence completeness and reproducibility:** Inventory maintained/archived tools, build source/configuration in and outside tracked tree; distinguish scratch from durable evidence, assess fresh-checkout reproduction and publication-candidate first-party/third-party saves and screenshots.
- **AC6 — Licensing, comparators, security and publication surface:** Inspect current tree and Git history, licensing/third-party rights and three named public repos; identify rights/privacy/security decisions without asserting blanket permissions, deciding legal eligibility or revealing secrets.
- **AC7 — Actionable results and bounded conclusions:** All findings tied to locations and concrete evidence, ranked by real consequence; prioritized cleanup batches and verification criteria; clear accepted exceptions and unknowns; no historic research rewritten and no release declared ready.
- **AC8 — Verification, independent review and delivery:** All criteria in PASS/FAIL/NOT TESTED matrix with primary evidence; independent reviewer ACCEPT/REWORK/ESCALATE under repo protocol; mechanical validation with preserved failures and retriable corrections; verifiable complete and task-only diffs including untracked documents; full status/inclusion/exclusion inventory; no staging/commit/push.

## 12. Compact completion contract

- **Task type:** Audit/documentation, not new scientific discovery or remediation.
- **Question/deliverable:** Can the project be published coherently, reproducibly, portably and with legally reviewed material? What must be addressed first? The deliverables and AC1–AC8 define completion.
- **Scope/bounds:** Sections 2–9; read-only inspections, RR1 documentation additions only; protected inputs/hashes; no live, cleanup, release or VCS integration authority.
- **Mandatory acceptance:** AC1–AC8, exact primary evidence, independently reviewed final snapshot, verified patch reconstruction.
- **Optional:** Example draft navigation layout or proposed style guide; must be clearly marked proposal, not implemented.
- **Negative-result closure:** A scoped clean scan is acceptable if validated controls and inspected coverage support it; absence of a file/issue is limited to paths/revisions actually inspected. Unsupported or inaccessible evidence must be reported, not silently classified clean.
- **Continuation authority:** Diagnose and correct in-scope audit/check/review failures, rerun and requalify without asking for a fresh brief. Frozen criteria may change only with maintainer approval.
- **Exit/escalation:** Halt affected work for observed authority, integrity, secrets, source/access or resource limits; retain safe receipts and a precise resume checkpoint; continue independent authorized inspection. No arbitrary test count or time cap on a healthy run; preserve project free-space and identity controls.
- **Review artifacts/disposition:** Original criterion matrix, evidence/negative/exception ledgers, source and provenance pins, status inventories, complete/task-only forward-and-reverse-applicable diffs, independent decision; separate scientific integrity, rights status and publication readiness.

## 13. Return format

Report concise major findings first, then paths to all new audit documents, criterion outcomes, independent reviewer decision and limitations. Provide complete and task-only patches and a manifest suitable for independent critical review. Suggest a commit message but **do not stage, commit or push**. Recommend the first **bounded cleanup brief** only after the maintainer has reviewed RR1.
