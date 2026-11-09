# D5BI review record

The original [D5BI brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BI_D5AO_D5AP_Public_Evidence_Derivative.md)
controls the review. The two specialist checks in [sufficiency](sufficiency.md)
are pre-design evidence. The final review is separate.

## Primary tests

| Test | Result and scope |
| --- | --- |
| Archive and source authentication | 174 evidence payloads in archive and loose roots plus identical embedded seal. All 484 source pins and original channel validators pass. Original protection/ABI receipts remain historical. |
| Rebuild | Authenticated rebuilds with the initial and corrected verifiers produced identical ZIP and manifest bytes on CPython 3.14.3 and zlib `1.3.1.zlib-ng`. Member bytes are bound by both checks. Temporary rebuilt ZIPs removed. |
| Isolated replay | Verifier and controls exited 0 in a fresh tracked HEAD export with proposed source overlays. A separately supplied exact copy was the only asset input. The Python audit hook refused unrelated file opens, writes and subprocess/socket access. This was a Python-level dependency test. |
| Adverse and model checks | 24 named refusals, including omitted and contrary history, wrong process/source/domain, operand changes, missing competition, disordered clock boundaries and a target mutation after generation. The missing-release oracle returned zero complete chains. Queue diagnostic changes did not select a route. |
| Scope | GC-10/D5R stay OPEN. Q4 release readiness remains BLOCKED by file-specific rights/privacy, authorized retention and transfer, B6 and hosting. |

Local primary receipts are under `.local-work/d5bi/` in
`candidate01/original-reconciliation.json`, `rebuild02/`,
`determinism-final.json`, `isolated.json`, `isolated-verification.json` and
`isolated-controls.txt`. The candidate SHA-256 and six member digests are
unchanged across both verification revisions.

## Initial independent return

`/root/review` returned **REWORK** for engineering and editorial while
independently accepting original-to-projection fidelity. It reauthenticated
all 174 archived/loose payload pairs and 484 source pins, then independently
decoded and compared 238,272 original frame payloads, every projected
operand and all 36 geometry holder rows. It independently reproduced the
cohort, seven lead comparisons, owner counts, pair accounting, five-reader
drain and peer-delay bounds, and rebuilt the same ZIP in memory. The initial
return, reviewed manifest and patches are retained under
`.local-work/d5bi/review01/`.

| Initial issue | Corrected evidence submitted for delta review |
| --- | --- |
| AC01 source-range and specialist chronology coverage | The applied-reading record now identifies complete documents, bounded relevant sections, recovered continuations, omissions and actual role start/end tool events. |
| AC04 lock enclosure | Same-thread original request, source, selection, epoch, native site and clock checks now bind acquisition and helper return before the miss and store before release. |
| AC06 progress and bypass order | Typed task progression, the later layer readiness/dispatch/provider partition and all 391 ordered shared-visit paths are verified. Earlier-source work and the foreign writer retain positive joins. |
| AC08 isolated semantic controls | Both corrected CLIs pass under a Python-level isolation guard. New adverse cases move acquisition, release, a provider, a visit and a target mutation across material boundaries. |
| AC12 delivery and status | The answer table states each original Q disposition and separates local engineering from actual release. Exact patches and evidence inventory were regenerated. |

## Independent acceptance of the corrected snapshot

`/root/review` returned **ACCEPT** for scientific sufficiency, engineering
and editorial review at the declared projection tier. Q1–Q3 are COMPLETE
at their local scopes. Q4 is COMPLETE for engineering and BLOCKED for
release readiness. The operative isolation export matched all methods,
manifest and asset bytes. It carried an earlier version of this review
prose, which is outside the executable dependency set. The reviewer
separately checked the exact submitted prose and both review patches.

| Criterion | Independent result |
| --- | --- |
| AC01 | PASS. Applied source ranges, continuations, exclusions and specialist termination were checked. |
| AC02 | PASS. The archive, seal, 174 archived/loose payload pairs, 484 source pins, interpreter, plan and process reauthenticated. HEAD, tree and index matched. |
| AC03 | PASS. Independent pre-design checks and the matrix substantiate the selected projection and omissions. |
| AC04 | PASS. Both clock adversaries fail after the original request, source, frame, owner and protected enclosure are joined. |
| AC05 | PASS. Both independent cohort censuses recover all 196 density and 196 layer tasks. The seven earlier geographic lifetimes contribute no source-scoped causal history. |
| AC06 | PASS. Seven leads, both peers, 518 writer and 23,194 reader triples, 72,015 conditional pairs, the five-reader drain and four-channel peer gap reproduce. The stage and bypass adversaries fail. |
| AC07 | PASS. All 238,272 records match independent original frame decoding. The session, 36 occupied holders, retained nested geometry and six member pins match. |
| AC08 | PASS. Both isolated CLIs succeed. All 24 controls refuse for their intended reasons, including the target mutation during the return-to-scan interval. |
| AC09 | PASS. Independent in-memory ZIP assembly and the primary's full corrected rebuild reproduce the exact asset. The primary manifest comparison matches. |
| AC10 | PASS. The fresh-context source audit, adverse challenge and corrected exact delta review are complete. |
| AC11 | PASS. D5BG keeps the two public edges held. The D5AQ crosswalk limits reuse to the recorded N2 side of a separate fixture. |
| AC12 | PASS. Both patches reverse and apply to exact bytes, include the expected inventories and preserve the index. |

The actual acceptance and exact reviewed snapshot are retained in
`.local-work/d5bi/review02/`. The delivery receipt SHA-256 is
`172fc53fb9996fb5e8656bcb5a69c78eaf95bbecbd8e809a6c7d4c45d3f586d1`.
The independent return SHA-256 is
`f9c2db24d249d736c23340a72d4e906617d787e21c4c38a56dda632e9814f92d`.
This closure records the review without altering operative methods, candidate
bytes or historical findings.

Suggested commit message is `feat(research): verify the N2 evidence derivative`.
