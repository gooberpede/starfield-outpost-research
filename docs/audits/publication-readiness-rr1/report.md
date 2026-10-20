# RR1 publication readiness and repository integrity

2026-10-20, Australia/Sydney. **NOT CLEARED for publication.** This audit supplies
a cleanup and decision plan; it does not change any existing publication label,
scientific conclusion, permission, licence, source or historical record.

The archive has substantial supported research and useful source provenance.
Its immediate publication problems are an unsettled release corpus and rights
boundary, missing public method inputs, and misleading navigation/status text.
Unresolved gameplay questions are not automatically publication blockers.

| Question | Supported audit answer |
|---|---|
| Can a newcomer find the supported model? | Many subsystem reports are well linked, but the latest RC1 capability/access synthesis and coverage audit are absent from the main indexes. Chronological summaries still contain old “current” instructions. |
| Can a fresh checkout reproduce methods? | Some synthetic readers and observer sources are tracked. Recent acquisition/orchestration helpers and original evidence frequently remain ignored. Claim-specific method closure is needed; distributing original saves or binaries is not required. |
| Is the text clean? | No. Context-checked prose elisions, six documents with encoding damage, one malformed table row and one missing permission anchor remain. UTF-8 decoding alone passes and misses the corruption. |
| Are all external paths defects? | No. Installed tools/databases and historical evidence paths are legitimate. Twenty-nine empty system-temp trees are residue; two old exporters can recreate them. Context-managed temporary directories are a separate case. |
| Are secrets or proprietary binaries demonstrated in reachable Git? | None matched the stated credential/private-key or binary indicators across 2,751 reachable blobs. Machine-local user paths are present. This bounded negative is not a legal, privacy or security clearance. |
| What blocks release? | An agreed runtime/persistence release scope, item-specific rights/privacy disposition and exact tree/history approval remain necessary under the existing publication gate. |

## Scope and preservation

The [invoked brief](../../implementation-briefs/CODEX_BRIEF_SOR_RR1_publication_readiness_repository_integrity_audit.md)
defines AC1–AC8. Starting HEAD is
`5ae7fe0fdb28a2710aafcc6c0e95dd0bf28c7ecc`; the working tree initially had
1,554 tracked files and only the supplied RR1 brief untracked. The local
baseline hashes all 1,555 files plus the Git index. Reads covered governing
policies, RC1/coverage and historical reviews, Git-visible text/history,
project-local ignored source metadata, named external leads, and three public
comparators. Original game/save/database payloads were not modified or decoded.

The initial scan inspected 1,040 tracked text files, including 775 Markdown
files and 104,755 text lines; source metadata covers 510 tracked and 15,008
ignored source/configuration candidates. These counts are inventories, not
percentages of semantic validation. The local ignored inventory contained
80,916 files at that scan; snapshots/build outputs account for many duplicates.
Only named external paths and closely related project material were examined;
there was no recursive whole-disk search.

Both drives passed the existing 40,000,000,000-byte guard before writes.
Git HEAD/index and every starting Git-visible file are rechecked by packaging.
This is not a new hash audit of the whole installed game or every private save.
No game, debugger, Ghidra, xEdit, build, observer or research experiment ran.
Only Python standard-library diagnostics, Git read/apply checks in isolated
scratch, filesystem metadata reads and public read-only retrieval were used.

## Audit package

- [Ranked findings and exact locations](findings.md).
- [Historical defect taxonomy, controls, prose and notation](prose-and-notation.md),
  with [classified candidates](prose-candidates.csv).
- [Reader journeys, actual graph and supersession](navigation-and-supersession.md),
  with [link occurrence inventory](link-inventory.csv).
- [External paths, temp creators and lifecycle](external-material.md), including
  [test allocation inventory](temp-test-inventory.csv).
- [Source and reproducibility closure](source-and-reproducibility.md),
  [source metadata](source-inventory.csv) and [CSV pin paths](source-pin-inventory.csv).
- [Evidence candidate families](evidence-candidates.md) and
  [selected screenshot integrity checks](screenshot-checks.csv).
- [Licensing, security/history and public comparators](licensing-and-comparators.md).
- [Original criterion matrix, failures and independent review](review.md).

All new audit text and inventories remain review candidates. The inventories
contain paths, hashes and metadata, not copied game payloads. Local diagnostic
receipts/scripts remain under `.local-work/rr1/`; final patches remain under
`.local-work/diffs/`. Their exact manifests and independent decision control
the final snapshot, not this implementer's summary.

## Proposed cleanup sequence

These are recommendations for separate briefs after maintainer critical review.
No batch is executed by RR1.

| Batch / priority | Bounded work and owner | Decisions, risks and verification gate |
|---|---|---|
| B0 / first | Maintainer agrees a first-publication claim/build matrix and evidence-access tier per claim. | Include runtime and persistence; retain meaningful scoped results and negative history. Decide author credit and rights-review responsibility. Gate: approved scope, exact public tree/ref boundary, unresolved decisions explicit. |
| B1 / first cleanup brief | Documentation author adds one current reader roadmap, indexes RC1/coverage, qualifies stale publication/status text, repairs the identified permission anchor. | Preserve historical claims/verdicts and link to successor records. Gate: three reader journeys, HEAD/case/anchor checks and independent review; no raw evidence promotion. |
| B2 / next | Documentation author makes occurrence-specific encoding/prose/table/notation corrections from the RR1 ledger. | Historical quoted defects and valid identifiers stay intact. Gate: protected identifiers/digits/addresses checked, link slugs checked, exact correction-only patch and independent contextual review. |
| B3 / next | Method owners select minimal owned acquisition/build/configuration source needed by B0 claims. | Review local helpers for embedded data and third-party lineage before promotion. Replace machine defaults prospectively; keep historical receipts immutable. Gate: fresh-checkout synthetic example and documented legally obtained prerequisites, no automatic downloads or live execution. |
| B4 / parallel decision | Maintainer and appropriate rights/privacy reviewer classify exact evidence candidates and reachable-history material. | Controlled versus mature versus donor saves remain separate. Decide minimal excerpts/screenshots, exclusions and privately retained evidence. Gate: item-specific provenance/notice/privacy decisions; no blanket GPL grant over game-derived material. |
| B5 / later housekeeping | Maintainer approves named scratch/obsolete-exporter disposition. | Verify paths/emptiness again, preserve review evidence and recovery plan. Gate: creators first fixed or retired under a new brief, then explicit cleanup authority; no broad Temp or D: sweep. |
| B6 / final release review | Independent reviewer and maintainer reassess the exact proposed contents and refs. | Repeat secret/privacy/rights/link/source-closure checks over final surface. History cleanup, if needed, requires a separate decision. Gate: explicit release approval; audit ACCEPT is insufficient. |

Selection and issuance of the first bounded cleanup brief await the maintainer's
review of RR1, as required by the invoked brief. The batch table is an ordering
proposal only. No tracker importer, mod, production dump utility or new scientific
experiment is a prerequisite to reviewing this audit.
