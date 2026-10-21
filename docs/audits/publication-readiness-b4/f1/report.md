# B4-F1 selection and local packaging report

2026-10-21, Australia/Sydney. **PROPOSED; NOT CLEARED for publication.**

The 71 original B4 identities reconcile to **25 CORE / 27 ADDENDUM / 15 LOCAL-ONLY / 4 EXCLUDE / 0 SPECIFIC HOLD**. Original B4 distribution was 50 held, 13 proposed exclusions and eight local-only. No extra candidate was added. Each row is revisited in [file-dispositions.csv](file-dispositions.csv); [coverage](coverage.md) relates the unchanged 26 B1 claim rows to marginal utility and withheld replay. This selection is a proposed practical minimum for the named checks, not a proof of globally minimal file count.

Core avoids result-only control cherry-picking: S0/S0C through S7/S7C retain baseline, placement, linking, rename, solar movement and deletion, including incidental-fauna/rename movement qualifications in the original report. The coordinate triplet and earlier two-outpost pair are different geometry witnesses. Save29 preserves ordered allocation. Save52, HIST-0255 and HIST-0036 answer noninterchangeable topology/organic, crew/damage/variant and fabricator/storage questions. A synthetic fixture or explanation can teach these methods but cannot reproduce the exact observed source bytes.

The addendum is curated: complete unlink/relink and L3 checkpoint sequences plus distinct earlier biome, Vasco ship-rank, helmet-display and UI/preview witnesses. HIST-0210 repeats core named site descriptors; H77/H83 add independent stock comparisons without a new selected mechanism; the six D1 historical comparisons remain local because incident timing/vein geometry and causality remain unresolved. Seven redundant/contextual photographs remain local. Incidental exit saves and the unrelated same-number Save26 are excluded, as is the donor. This preserves their historical scientific results rather than reclassifying or replacing them.

## Exact historical identity

- B4-F040, Save52 / HIST-0267: `Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs`, 16411136 bytes, SHA-256 `6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
- B4-F051, Save41 / HIST-0255: `Save41_BA75E3CDM43616F205472616E_480619_20260706053644_309_12_4.sfs`, 24870320 bytes, SHA-256 `635c07a4914c3313bbf12f031523f707183e4757324ce070f361bec0edfe10b4`.
- B4-F064, HIST-0036: `Autosave1_BA75E3CDM43616F205472616E_580731_20260818031907_319_15_4.sfs`, 16861680 bytes, SHA-256 `7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37`.

Protected `.local-work/historical-inventory/scan-04/inventory.json` was joined by SHA-256 to the public frozen inventory and B4 source/copy manifests; original basenames for every historical shortlisted save were recovered without re-decoding for names. Current source-copy hashes are checked before/after packaging. Absent old source locations remain explicitly missing, not recreated. Nonhistorical controls/images use B4 verified source/copy origin basenames. [Members](members.csv) supplies the full map; all 71 private locators are local.

## Measured packaging

Both methods were measured on **all 52 selected files**, not extrapolated from size. Four archives were actually built. [Measurements](compression.csv) contain exact sizes/hash/options. Negative savings denote ZIP overhead.

| Group | Method | Original bytes | Archive bytes | Savings |
|---|---|---:|---:|---:|
| CORE | stored | 104040960 | 104046934 | -0.005742% |
| CORE | deflate | 104040960 | 103059612 | 0.943232% |
| ADDENDUM | stored | 81684979 | 81690475 | -0.006728% |
| ADDENDUM | deflate | 81684979 | 80827444 | 1.049807% |

Stored core favors grouping and avoids compression work for negligible benefit; DEFLATE addendum saves about 0.86 MB, enough to retain the measured smaller variant. The one-percent convenience threshold selects encoding only, never evidence membership. Both alternatives remain ignored and verified; only the two chosen assets below are proposed for later release. CPython 3.14.3 stdlib zipfile, zlib runtime 1.3.1.zlib-ng; DEFLATE level 9, fixed 1980 timestamp, regular 0644 entries, no comments. Path syntax/ADS/traversal/device names, unique member paths/hashes and exact expected sets were checked. B4-ID directory prefixes preserve exact original basenames and avoid ambiguous lookup.

- **CORE**, 25 files, 104046934 bytes: local `.local-work/b4-f1/packages/sor-1.16.244.0-b4-f1-core-stored-provisional.zip`; SHA-256 `b27bb842770d51499bec30042660789f1e539a3187d0d63f226fafcedd405105`.
- **ADDENDUM**, 27 files, 80827444 bytes: local `.local-work/b4-f1/packages/sor-1.16.244.0-b4-f1-addendum-deflate-provisional.zip`; SHA-256 `d904b452fcfe1a82e6c4ceae5dfd1396b4fa088868587605ced7e2e57de278a3`.

Every one of 104 member extractions (52 in both variants) passed ZIP CRC, exact member-set/length/SHA-256 and streamed direct byte comparison against immutable source copies. Extraction destinations were allowlisted per member under separate local scratch trees. Original sources were rehashed after extraction. Same stdlib write/read is not independent codec validation, and archive integrity is not a live load test or semantic validation. Local `extraction.json`, `members.json`, `compression.json`, `assets.json` and `assembly-completion.json` are primary receipts. The tracked [member manifest](members.csv) excludes private source paths. No eligible selected member was left unpackaged.

## Safety, failures and checks

Baseline captures starting visible text, HEAD/index and protected identities; all writes stay in authored documents or bounded ignored F1/review roots. Before meaningful packaging writes, both C:/D: caller-free space remained above 40,000,000,000 bytes plus output allowance. Initial values were 94,545,342,464 / 111,831,117,824 bytes. No protected source directory, installed game/tool or original byte was written. No game, debugger, Ghidra, network, external disclosure, staging, commit or push occurred.

A first assembly helper invocation stopped on an unmatched-parenthesis SyntaxError before executing any packaging statement. Correcting the original authored helper enabled the successful run; no partial archive from that failure exists. Targeted privacy binary false positives and limitations are retained in [privacy/policy](privacy-policy.md). No failed packaging check is relabelled PASS.

[Independent review](review.md) controls contract disposition. Scientific conclusions/source pins and original B0/B4 reviewer records are preserved; local preparation supplies no integration or publication approval. B6/maintainer must approve exact membership, final public history/contents, author/excerpt decisions and actual GitHub assets/links. [Index and handoff](README.md) records the remaining verification.
