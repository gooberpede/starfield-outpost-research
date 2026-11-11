# SOR-EXP-0006 — Mature-save outpost and cargo validation

2026-10-08, Australia/Sydney. ANALYZED; critical review pending. SOR-EV-0012 / SOR-SAMPLE-0029 / SOR-F-0012 / SOR-ST-0015–0016. SAVE basis. Authored report, helpers and selected tables REVIEW-REQUIRED; source saves, private JSON, complete extraction, local manifests and exploratory outputs LOCAL-ONLY. No integration/publication approval.

## Result

Reader context added 2026-10-21: [Save52 identity and evidence availability](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/evidence-dependencies.md`)
explains the mature playthrough sample and private comparative JSON. The derived
tables below support understanding; exact independent replication needs those
local inputs. This annotation does not revise the historical observations.

The principal numerical observations reproduce: 141 valid streams, 36,934,800 decoded bytes, a bounded 1,588-byte payload containing 17 beacon references, 199 keyed groups and 246 endpoints; 324 distinct nonzero tokens each match a unique recognizable window. The save-only extraction yields 53 uniquely member-associated cargo markers, 25 regular and 28 interstellar, with 48 distinct pads in 24 reciprocal pairs. All 17 names, every per-outpost pad count/type and the full outpost-pair multiset match the comparative JSON.

Two important qualifications change the interpretation. First, a broader scan finds **61** marker-like windows, including eight without the observed beacon association; 53 describes the associated subset. Second, the beacon collection is **not demonstrated to enumerate all active outposts generally**: it is empty in S1/S1C/S2/S2C and S7/S7C while the previously validated beacon window remains. This is a bounded beacon-reference plus relationship collection, strongly correlated with the mature network. A universal active index is contradicted by the small-corpus lifecycle; the inclusion rule remains unresolved. Its correspondence to the JSON's active set is a scoped mature-save observation.

## Authority, plan, inputs and provenance

The user invoked the [retained brief](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_RESEARCH_BRIEF_mature_save_outpost_validation.md`) and requested suggested commit messages with no commit/push. SOR-D-0022 records this exact offline scope. Allowed: existing archive/JSON reads, hashing, narrow standard-library analysis, ignored derivatives and durable research documentation. No source editing, Starfield/SFSE/debugger execution, configuration/database changes, external disclosure, dependency acquisition, staging, commit or push.

Plan and stopping rule: validate framing independently; enumerate beacon/name and marker candidates from the save; freeze extraction before reading JSON content; compare names/counts/topology without fitting expected totals; challenge small-corpus generality and deterministic negative controls; record counterexamples and stop for review. Stop on integrity failure, unsafe free space, ambiguous essential identity or bounds failure. Cleanup retains all local evidence and partial runs; no source/live-save cleanup. Risks are false window matches, unresolved record ends, incidental playthrough churn and disclosure of private filenames/JSON. No source-save gameplay is inferred from filesystem dates.

Mature input: `.local-work/savegames/Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs`. Comparison discovered as the sole copied JSON in `.local-work/scratch/`: `starfield-outposts-cao-tran-319-2026-09-28-124324.json`. Complete absolute paths, lengths, SHA-256, modification/creation times are retained in `.local-work/mature-save-validation/source-inputs.md` and `run-07/inputs-before.json`; personal paths stay local. The copy's capture history and actual originating executable/module profile are UNKNOWN. Save header strings report `1.16.244.0` at decoded offsets 143 and 155. JSON filename reports a 2026-09-28 export, later than the save filename's 2026-08-18; filename conventions/capture timing are not independently validated. JSON is a manual comparative description, never engine authority.

Prior discovery: SOR-S-0124, preserved `.local-work/mature-save-offbook/` with every script/output hashed in `before.json`. Inspected anchor/count/ownership methods are source-informed project research. Only `local_decode.py` is imported/executed; its exact identity is in `run-07/inputs-before.json`. Exploratory drivers are not run because they write into the preserved workspace and some consult JSON before extracting. The new helper independently implements bounded cursor grammar, candidate enumeration and comparison, conceptually reusing exploratory methods. It imports the project's directory label constants and installed CPython/zlib facilities (SOR-S-0113). Prior cargo definitions and keyword names come from SOR-F-0002/0004, SOR-ST-0003/0004, SOR-S-0103/0104. No outside code/dependency or new permission basis.

Baseline: pre-task Git status had only the supplied untracked brief. Snapshot covers 254 existing repository/archive/offbook/scratch files. Existing controlled manifest identities are checked on read; 22 requested labels represent 21 unique controlled saves, with both archived incidental exits also checked separately (24 labels / 23 unique small saves). Mature sample is uncontrolled and provides no time/growth causality test.

## Physical framing and independent grammar

Independent audit reconstructs every mature zlib stream with checksum/EOF/input-consumption/expected-size checks and exact physical EOF **16,411,136**. Decoded SHA-256 `e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93` agrees with extraction. Compressed-size table ends at physical 636; declared first stream starts at 640, the next 16-byte boundary. Gap bytes are **`696e6700`**, not zero padding. This alignment rule also holds in all 24 small labels. Alignment is supported empirically; why these opaque bytes have that content, and a universal BCPS specification, remain unresolved. The historical exact-table-end decoder rejects this input; that failure is retained. No workaround bytes are inserted into the decoded content.

Mature logical directory at **2865** closes a counted uint32 table from 27,663,756 to 33,165,044 with 1,375,321 entries. R2=[1,807,297,1,861,722), R3=[1,861,722,25,081,364). The old directory detector fails because auxiliary word 205557 exceeds its 100000 cap. New detector uses ordered in-file pointers and exact uint32-table closure, without treating auxiliary words as known semantic counts. It finds one candidate in the same bounded early 8192-byte search and agrees with all small-corpus directory locations. This is a revised detector, not a correction to the old experiment's observed bytes.

Envelope: decoded **[1,860,043,1,861,639)**, header `7900000034060000`; uint32 little-endian length `34060000`=1588; payload **[1,860,051,1,861,639)**; successor `7a00000028000000`. Decoded stream 7, envelope-relative stream offset 25035. Compressed stream locators are in frozen `chunks`; no linear physical offset within compression is asserted. Payload SHA-256 `37a4fec9c010c33678d4e15f7de772aa26d0d501a4be0cb61a783a0a0bdc4f36`.

Grammar: encoded count uses low two bits as width tag 0/1/2 → 1/2/4 bytes; unsigned little-endian integer shifted right two. Tag 3 is unsupported and rejected. Each reference is three exact bytes, with no resolved runtime/FormID meaning. First count `44`=17, followed by 51 reference bytes. At payload +52, `1d03`=199 keyed groups. Each group has a three-byte key, encoded endpoint count and that many three-byte references. The total closes exactly at +1588 without trailing bytes or padding. [Every count-field step](mature-save-validation/count-fields.csv), [all 199 groups including starts/ends](mature-save-validation/groups.csv). No duplicate beacon tokens, group keys or within-group references in this unit; repeated references across groups remain legal and preserved.

[All qualifying small envelopes](mature-save-validation/envelopes.csv) include 9-byte examples omitted by the prior beacon-prefixed predicate. Every R2 `79000000` occurrence is inventoried locally before grammar testing. Qualification requires in-region uint32-length closure and the independent known successor; one envelope qualifies per sample. All 24 small envelopes and the mature envelope consume exactly with the same grammar. Earlier 12-byte examples carry one beacon, one zero-key group; 19-byte linked examples carry one beacon and two groups. Their `04` and `08` satisfy counts 1 and 2; the mature `1d03` extends support beyond those two values. Four-byte count width is synthetic-tested only; count/tag semantics outside this corpus remain provisional.

The eight controlled 9-byte examples (S0/S0C/S1/S1C/S2/S2C/S7/S7C), plus the manual exit, have `000400000004679bc3`: zero beacon references, one zero-key group with one reference. Beacon membership starts at S3, before the first controlled output link, and disappears with S7's extractor deletion/link cleanup although the beacon survives. That blocks equating this collection to a general active-beacon registry; object/relationship participation is an alternative, not an established owner rule.

Offsets use **envelope header** versus **payload start** explicitly. In the prior L0C–L2C narrative the values 425510/426830/426826 locate payload starts, eight bytes after envelope headers 425502/426822/426818. This is a coordinate clarification; the prior relationship byte transitions are unchanged.

## Negative controls and failures retained

Six unittest methods pass, including all proper truncations of the 19-byte fixture, zero/duplicate preservation, count widths, unsupported tags, implausible cardinalities, trailing bytes and bad envelope lengths/successors. Counts are unsigned; negative integers have no admitted encoding, and high-bit/all-FF stimuli fail bounds or tag checks. Multiplication/allocation is preceded by remaining-byte bounds. Duplicate keys/references are reported, not silently deduplicated.

Independent direct consumption agrees with all 24 small payloads and the mature payload. All **1588** proper mature truncations reject. All **96** structurally mismatched small envelopes reject the grammar; all **2000** deterministic random 12/19/1588-byte trials (seed 79) reject. Mature nearby shifts −16…+16 excluding zero reject. For controlled samples, **8 of 352** nearby shifts are grammar-valid: shift −4 at each controlled 9-byte payload. Those start inside the envelope length word and fail envelope framing. Nonminimal two-byte count encodings can admit such patterns; no unproven canonicality rule was introduced to hide them. Thus **grammar acceptance alone is not a detector or semantic proof**. Local negative receipts retain exact labels/offsets/results.

Preserved implementation failures: run-01 small-corpus directory cap; run-02 strict UTF-8 decoding of an unrelated shared string fails on byte 92; run-03 requires two animations but most mature windows contain fewer; run-04 broadly treats all keyword-motif occurrences as dynamic references; run-05 comparison uses nonexistent JSON `padId`; run-06 uses the actual `cargoPadId`. Shared strings retain exact bytes and escaped undecodable content; the observed outpost names are ASCII. Run-05, run-06 and final run-07 **save-extraction hashes are identical**, so the comparison-key repair did not change save evidence. Run-04 extraction is preserved as a failed overly broad reference interpretation, not an accepted graph.

## Beacon names and residual candidates

The first 17 references were obtained from the bounded unit before JSON content was opened. Candidates require a 3a+token prefix, repeat within the first 48 bytes and nearby `6c60e9` base-like bytes; names are resolved from uint16 indices preceding `1100190004`, with zero/one/two known animation indices. The mature sample has four two-animation candidates, fourteen one-animation candidates, one with no animation index. A fixed three-index assumption fails here; variable content does not establish complete object record boundaries. All 19 candidate identities and names are distinct; each collection token resolves once.

All locations below are **decoded logical offsets**. The [complete hop ledger](mature-save-validation/beacons.csv) includes base location, index bytes, name length/text positions, exact name bytes, animation indices and terminating motif. Name collection pointer field 2969 → 33,165,133; uint16 count 2094; uint16-length fields end at 33,219,408 (54275 bytes). This is a shared collection, separate from object windows and relationship unit.

| Token | Save-derived name | Window | Index offset / string index | Name text offset | In collection | JSON |
|---|---|---:|---|---:|---|---|
| 859e53 | Carinae V-b Cs | 6309514 | 6309688 / 1846 | 33212596 | yes | match |
| 828ee2 | Ternion III Poly H2O | 3546701 | 3546981 / 1718 | 33208647 | yes | match |
| 825f95 | Feynman VII-b Nd Al He3 | 3436622 | 3436983 / 1711 | 33208419 | yes | match |
| 82be17 | Carinae III-a Rc Fe | 3760058 | 3760299 / 1727 | 33208965 | yes | match |
| 84e101 | Feynman V Cu IL F | 5712362 | 5712570 / 1806 | 33211419 | yes | match |
| 830a80 | Feynman I Li Cu xF4 | 4187949 | 4188229 / 1738 | 33209284 | yes | match |
| 81a75b | Arch III W H2O Lub | 2924381 | 2924628 / 1671 | 33207281 | yes | match |
| 83388f | Feynman V Cu Co Ni IL | 4440430 | 4440737 / 1752 | 33209677 | yes | match |
| 832210 | Feynman III V U | 4284332 | 4284533 / 1745 | 33209489 | yes | match |
| 84b8fb | Eridani VIII-c Cs Li | 5605591 | 5605759 / 1805 | 33211397 | yes | match |
| 84ede9 | Feynman II Ag Pb | 5753536 | 5753677 / 1819 | 33211832 | yes | match |
| 82a0c0 | Feynman IX Eu Al He3 | 3616560 | 3616801 / 1721 | 33208740 | yes | match |
| 81bf2a | Feynman VI-b Al Be He3 | 3043343 | 3043728 / 1683 | 33207639 | yes | match |
| 844cc6 | Feynman VIII-b Au Sb | 5246278 | 5246603 / 1786 | 33210764 | yes | match |
| 84ff81 | Schrod II Ad | 5811569 | 5811792 / 1820 | 33211850 | yes | match |
| 832512 | Carinae V-c Pd Ni | 4310069 | 4310249 / 1751 | 33209658 | yes | match |
| 855619 | Codos Al Be Solv | 6080804 | 6080978 / 1836 | 33212274 | yes | match |
| 81b58f | Feynman VII-b U He3 | 3022692 | 3022866 / 1681 | 33207609 | no | absent |
| 8483f2 | Feynman II Ag U V | 5377946 | 5378060 / 1792 | 33210959 | no | absent |

The two excluded candidates have zero membership entries **and zero key/endpoint mentions** in the bounded unit. Their base-like windows, repeated tokens and name indices remain identifiable. No user-confirmed deletion history was supplied in this task. Removed, retained, inactive, unrelated or historical state remain possibilities; no tombstone flag, Unity history or authoritative deletion semantics was decoded.

## Relationship references and zero-key group

All **324 distinct nonzero tokens** resolve to exactly one matched prefix/repeated-token window in R3: 220 prefix 3a and 104 prefix 2a. [Exact window and association offsets](mature-save-validation/token-windows.csv). These are recognizable windows, not individually length-closed records.

198 nonzero keys have one named-beacon association in their first 128 bytes through the raw pattern `454ba6` followed by that beacon token. Their 236 endpoint occurrences independently have the same beacon association: **zero cross-beacon pairs**. Association keyword meaning/ownership is not assigned merely by its arithmetic value. The ten zero-key references lack a mapped source: `850cc5 856ed4 831aec 83bd68 84d23f 000000 81dce3 8351b3 85f564 822271`. One endpoint itself is zero; the other nine match windows. Zero-key group starts at payload +1478 and ends +1512; it is not the final group. Purpose unresolved. Do not call all 246 endpoint occurrences output links or cargo transfers. The earlier controlled output-link association remains proposed STRONG pending review, with no downgrade due to terminology.

## Save-only cargo graph and comparison

`run-07/save-extraction.json` was closed/hash-frozen before JSON content access, SHA-256 **`a1d4490a6b41c05ad08f68b2efa28f71d6ebac56cb9aabf55eb61356833b57e2`**. All 61 detected windows, associations, keyword-motif hits and reciprocal pairs are retained. `extraction-frozen.json` and `comparison.json` separate evidence phases. Extraction is conceptually source-informed by exploratory methods; it is independent of JSON topology, not a claim of clean-room discovery.

Classification basis: marker prefix 2a+token with repeated token, base-like bytes `6a6c3f` (mask low 22 bits → 002A6C3F) or `619523` (→00219523), compared with prior independently inventoried regular/fueled marker definitions. That supports type inference, not a universal save-tag specification. Fifty-three windows contain one member-beacon pattern at +58 (five) or +59 (48); eight contain none within the observed 128-byte extent. The latter are six regular and two fueled candidates, retained as unresolved and excluded from **associated network** counts only. Their omission cannot establish deletion or absence of ownership elsewhere.

Pairing uses occurrences of raw `655cc8` followed by a three-byte token in the 128-byte window, consistent with prior Active keyword 00255CC8. All motif occurrences remain in the ledger; only observed dynamic-family tags 80…bf participate in pad-reference reconstruction. Other occurrences have 00/04-leading bytes and are not interpreted as pointers. This is an empirical tag filter, not a complete typed-record decoder. Require the destination to be another uniquely identified pad, retain self repeats separately, and require reciprocal nonself references.

There are 48 nonself participating pads and 24 reciprocal pairs, all member-associated, with no unresolved nonself dynamic pad target in this sample. Three pads additionally repeat themselves (`8330f8`, `833191`, `8596f3`); those repeats are preserved and yield no extra connection. Five associated pads have no distinct partner: three regular at Feynman V Cu IL F, one interstellar each at Eridani VIII-c Cs Li and Codos Al Be Solv. All candidate bytes/offsets, including unassociated windows and nonreference motif hits, are in [pads.csv](mature-save-validation/pads.csv).

| Outpost | Regular save / JSON | Interstellar save / JSON | Result |
|---|---:|---:|---|
| Arch III W H2O Lub | 0 / 0 | 3 / 3 | match |
| Carinae III-a Rc Fe | 0 / 0 | 3 / 3 | match |
| Carinae V-b Cs | 0 / 0 | 2 / 2 | match |
| Carinae V-c Pd Ni | 0 / 0 | 2 / 2 | match |
| Codos Al Be Solv | 0 / 0 | 1 / 1 | match |
| Eridani VIII-c Cs Li | 0 / 0 | 1 / 1 | match |
| Feynman I Li Cu xF4 | 4 / 4 | 0 / 0 | match |
| Feynman II Ag Pb | 1 / 1 | 0 / 0 | match |
| Feynman III V U | 1 / 1 | 1 / 1 | match |
| Feynman IX Eu Al He3 | 1 / 1 | 2 / 2 | match |
| Feynman V Cu Co Ni IL | 3 / 3 | 2 / 2 | match |
| Feynman V Cu IL F | 3 / 3 | 0 / 0 | match |
| Feynman VI-b Al Be He3 | 4 / 4 | 2 / 2 | match |
| Feynman VII-b Nd Al He3 | 4 / 4 | 2 / 2 | match |
| Feynman VIII-b Au Sb | 4 / 4 | 1 / 1 | match |
| Schrod II Ad | 0 / 0 | 3 / 3 | match |
| Ternion III Poly H2O | 0 / 0 | 3 / 3 | match |

The full multigraph preserves parallel links; [outpost-pair multiset](mature-save-validation/multigraph.csv) and [pad-level connection ledger](mature-save-validation/connections.csv) agree with all 24 JSON links. Connection identities were not deduplicated merely because names repeat.

| Save pad tokens | Endpoint A name | Endpoint B name | Types | Compatible JSON pairs |
|---|---|---|---|---:|
| 81aeb5 ↔ 82dcf9 | Feynman II Ag Pb | Feynman VIII-b Au Sb | regular / regular | 1 |
| 81ca84 ↔ 84d26f | Feynman VIII-b Au Sb | Feynman VII-b Nd Al He3 | regular / regular | 2 |
| 8250f6 ↔ 8579b4 | Feynman III V U | Feynman VI-b Al Be He3 | regular / regular | 1 |
| 82a221 ↔ 83876a | Feynman IX Eu Al He3 | Feynman I Li Cu xF4 | regular / regular | 1 |
| 82c3c4 ↔ 83444c | Feynman VII-b Nd Al He3 | Feynman I Li Cu xF4 | regular / regular | 1 |
| 82c40c ↔ 844493 | Feynman VII-b Nd Al He3 | Feynman V Cu Co Ni IL | regular / regular | 1 |
| 83133d ↔ 839fe9 | Feynman VI-b Al Be He3 | Feynman I Li Cu xF4 | regular / regular | 1 |
| 837602 ↔ 84d265 | Feynman VIII-b Au Sb | Feynman VII-b Nd Al He3 | regular / regular | 2 |
| 83a02e ↔ 844440 | Feynman I Li Cu xF4 | Feynman V Cu Co Ni IL | regular / regular | 1 |
| 8428a3 ↔ 850325 | Feynman V Cu Co Ni IL | Feynman VI-b Al Be He3 | regular / regular | 1 |
| 852960 ↔ 857a02 | Feynman VIII-b Au Sb | Feynman VI-b Al Be He3 | regular / regular | 1 |
| 81ac91 ↔ 844964 | Schrod II Ad | Carinae V-b Cs | interstellar / interstellar | 1 |
| 820ce1 ↔ 82b86b | Carinae III-a Rc Fe | Feynman IX Eu Al He3 | interstellar / interstellar | 1 |
| 820cf6 ↔ 84611c | Carinae III-a Rc Fe | Feynman VII-b Nd Al He3 | interstellar / interstellar | 1 |
| 8217b5 ↔ 84fad9 | Schrod II Ad | Feynman V Cu Co Ni IL | interstellar / interstellar | 1 |
| 82b2b3 ↔ 8330f8 | Feynman VII-b Nd Al He3 | Arch III W H2O Lub | interstellar / interstellar | 1 |
| 82ceb2 ↔ 833a3a | Ternion III Poly H2O | Feynman V Cu Co Ni IL | interstellar / interstellar | 1 |
| 82ceff ↔ 83d8c6 | Ternion III Poly H2O | Feynman VI-b Al Be He3 | interstellar / interstellar | 1 |
| 82f63f ↔ 8382d2 | Feynman VIII-b Au Sb | Carinae III-a Rc Fe | interstellar / interstellar | 1 |
| 833191 ↔ 83dfda | Arch III W H2O Lub | Schrod II Ad | interstellar / interstellar | 1 |
| 8449af ↔ 850485 | Carinae V-b Cs | Feynman IX Eu Al He3 | interstellar / interstellar | 1 |
| 8503a2 ↔ 8596f3 | Feynman VI-b Al Be He3 | Arch III W H2O Lub | interstellar / interstellar | 1 |
| 85090f ↔ 8559c5 | Feynman III V U | Carinae V-c Pd Ni | interstellar / interstellar | 1 |
| 85917b ↔ 85ed59 | Carinae V-c Pd Ni | Ternion III Poly H2O | interstellar / interstellar | 1 |

**Ambiguity:** 22 connections have one compatible JSON endpoint pair under owner/type/partner signature; this is conditional structural matching, not proof of physical-pad identity or an engine UUID mapping. The two regular parallel links between Feynman VIII-b Au Sb and Feynman VII-b Nd Al He3 each match either of two JSON pairs (2! assignments). Three unconnected same-type pads at Feynman V Cu IL F have 3! assignments. JSON UUIDs and labels stay in local `comparison.json`; none are asserted serialized game identities. No count/name/type/topology mismatch was found. Transfer direction, cargo contents, timing and authority after load were not tested.

## Structural role and evidence classifications

**OBSERVED / PROVEN within these inputs:** bounded framing/length/counts; exact grammar consumption; direct name/index bytes; 324 uniquely matching windows; 53 member-associated pad windows among 61; reciprocal pad references and exact JSON comparison. Publication REVIEW-REQUIRED, SAVE basis.

**INFERRED / proposed STRONG pending critical review:** beacon/name reference mechanism; regular/interstellar marker interpretation; correspondence of reciprocal pairs to the manually described cargo connections; an outpost-local relationship collection associated with a separate beacon-reference subset. The controlled output-link lifecycle, mature same-owner relationships, name equality and cargo multigraph equality are separate supporting evidence lines.

**HYPOTHESIZED / PROVISIONAL:** precise inclusion rule, logical owner, zero-key purpose, retention/deletion meaning, complete object schema, keyword consumers, transfer direction and canonical count tags. Universal active-index interpretation is rejected at current evidence scope by S1/S2/S7. “Member” means member of this serialized collection unless explicitly qualified as JSON membership; runtime active status is UNKNOWN.

The bounded unit combines beacon references and keyed local relationships. It points/correlates through compact save-local tokens to separately stored object windows; beacon windows index the shared string collection. This strengthens distributed Model C without finding one contiguous complete-outpost container. R2 is 54425 bytes; R3 23219642; reference-table candidate 5501288; shared collection 54275. Growth versus S4C is confounded by the whole playthrough and is not an outpost law. Complete record ends, stable cross-session/runtime identities, load authority and safe integration remain UNKNOWN. Tail arithmetic is not promoted to a stable identity resolver; previous reload counterexamples remain decisive and this brief adds no validated resolver.

## Acceptance, durable changes and next step

All bounded questions are addressed to the preserved evidence limit. Exact reproduction and structural checks pass; semantic “all active outposts” is narrowed with a counterexample, additional marker candidates and pad ambiguity are explicit. No semantic promotion is automatically approved. SOR-F-0012 records observed grammar/network correspondence; SOR-ST-0015 is the bounded reference/relationship representation; SOR-ST-0016 is associated marker topology; SOR-H-0005 retains the unknown inclusion/ownership rule and a falsifier. SOR-D-0022 records authorization, not an engine result. Evidence index SOR-EV-0012 locates this report, tables and local frozen artifacts. Existing structural report receives only a dated cross-reference; historical evidence is preserved.

Smallest useful next step, proposed only: after critical review, a controlled beacon/storage/producer addition-removal sequence could discriminate the reference collection's inclusion trigger and whether cargo association survives independent pairing changes. It needs a separate live brief. No fabricator, organic, inventory, simulation, transport-direction, ship or universal parser work was begun.

[Validation and complete review inventory](mature-save-validation/validation.md). Reproducible analysis: from repository root, installed Python `-B save-analysis/scripts/validate_mature_outposts.py --run <fresh-name>`. Unit checks: `-B -m unittest discover -s save-analysis/scripts -p test_mature_outposts.py -v`. Local `independent_checks.py` separately reconstructs mature streams and counts; `corpus_challenge.py` checks all small payloads, mismatched frames and truncations. Their exact hashes, inputs and outputs are in the ignored bundle. No raw decoded files written; maximum decoded bound 64 MiB per save. Output remains finite and small.

Suggested commit after review only: `research: validate mature-save outpost relationships and cargo topology`.
