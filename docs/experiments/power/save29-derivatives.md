# Save29 derivative preparation: NO-GO

**Prospective Save29 supersession, 2026-10-17:**
[Offline allocation-authority adjudication](save29-authority.md) selects
**C / STRONG** within ordinary Save29 conditions, from a grounded beacon CB
order and root-independent single-generator selection. Earlier mechanism-OPEN
language and temporal-capture recommendations below are retained history,
superseded for this bounded question. Reload PASS and writer NO-GO are unchanged;
historical instruction execution/general prediction remain unproved. No new live
or writer work follows; [review](save29-authority-review.md) controls disposition.

2026-10-17, Australia/Sydney. SOR-EXP-0041 / SOR-EV-0049 continuation.
[Authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_P1_Save29_control_reversal_overpower_preparation.md`).
[Player test card](save29-derivative-card.md), [review package](save29-derivative-review.md).

| Element | Scoped result |
|---|---|
| Question | Can the existing owned save tooling safely emit the three controlled C/R/O candidates? |
| Answer | **NO-GO for candidate delivery with the currently qualified serialization knowledge.** Decoding works; the actual BCPS header has opaque fields whose preservation/update rules are unqualified. No candidate saves were emitted. This is the brief's section 6(b) result, not proof that repacking is impossible. |
| Confidence / coverage | PROVEN / SAVE for original bytes, reader coverage counterexample and selected records. NO-GO is an engineering disposition. Tested only this hash-pinned Save29 and existing reader profiles; no general writer claim. |
| Evidence | Local `probe01/feasibility.json`: two reader paths agree on all 5,539,576 decoded bytes, all 22 chunks validate; complete R3 framing exhausts 20,825 records; three target Extra9C locators rederived. |
| Limitation | Neither reader validates all BCPS header fields. Agreement between readers sharing format assumptions does not establish serialization legitimacy or game acceptance. |
| Smallest prerequisite | Establish a source-backed serialization contract for the actual opaque BCPS fields, including whether unchanged decoded length permits preserving them when compressed bytes or powered bits change. Qualify its integrity and padding rules before emitting C/R/O. |

The accepted historical result remains **PASS**: three user-observed fresh-process
loads of unchanged Save29 gave #1 powered / #2 unpowered at the reported endpoints.
It is not reopened. Restoration versus effective recalculation remains **NOT
TESTED** by this assignment. No game launch, active Saves delivery, instrumentation,
original edit, database mutation, staging, commit, push or external disclosure occurred.

## Inputs, provenance and actual checks

The exact original is the brief's Save29 in the user's Documents/My Games/Starfield/Saves,
2,085,680 bytes, SHA-256
`ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe`.
Its existing protected archive under `.local-work/p1-save29/protected/` was the
decoded input. Both originals named Save3 in the earlier protection receipt,
original Save29 and that archive were freshly hash-checked before and after.
There was no indiscriminate save search and no new archive masquerading as C.

Original bounded [probe](../../../research/p1-power/save29_feasibility.py) reuses
project-owned `stream_save.py`, `analyze_manual_corpus.decode`, record framing,
plugin/token resolution, reference-prefix and `saved_instances.extra_view`.
This is same-repository reuse, not third-party code incorporation. Exact source,
interpreter and installed executable/ESM hashes are in the local receipt. Current
interpreter: CPython 3.14.3 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`,
zlib compile/runtime `1.3.1.zlib-ng`. Installed executable/ESM match the
[prior baseline](save29-test-plan.md#minimal-technical-basis); no inference is made
about the player's earlier loaded modules. Existing CPython/zlib and Bethesda
evidence credit is extended in [SOURCES](../../SOURCES.md#save29-derivative-feasibility)
and [CREDITS](../../../CREDITS.md#save29-derivative-feasibility).

Run from repository root with that interpreter, `-B
research/p1-power/save29_feasibility.py --run probe01` (use a fresh alphanumeric
name for another run). Reads only explicitly named prior receipts/protected saves,
installed game/ESM and project sources; writes exclusively ignored JSON plus a
temporary `.bin` coverage probe removed on context exit. Decoder scratch is removed;
empty scratch directory may remain. C:/D: 40,000,000,000-byte free-space guards
remain. No writer, new dependency, tool download or third-party parser was used.

Both reader paths reproduce decoded SHA-256
`b236f22dd601b2dab59d5640967b12ab1f4dd5b3e4aac58cfae593bf43989579`.
Offsets below are **decimal decoded-stream offsets**, half-open; words are
little-endian hex. These were rederived by framed identity and then checked
against direct bytes, rather than used as unverified write coordinates.

| Saved object | Record range | Extra9C tag+word range | Word / prospective powered byte |
|---|---|---|---|
| Solar `ff022841`, base `2031e1` | [1300005,1300509) | [1300167,1300172) | `840`; unchanged in every proposed stage |
| #1 `ff022917`, base `05ef19` | [1300577,1301023) | [1300659,1300664) | `840`; byte 1300660, mask `40` |
| #2 `ff02294d`, base `05ef19` | [1301249,1301671) | [1301324,1301329) | `800`; byte 1301325, mask `40` |

All three counted extra loops close. The earlier independently supplied
[console-position join](save29-test-plan.md#subsequent-user-console-identity-evidence)
assigns #1/#2 without assuming their powered states; historical live IDs remain
session-specific. Actual saved positions remain those in the preserved report.
Selected rows retain owner keyword `054ba6` to `ff022778` and CB word-1 edges to
that beacon. Framing closure does not remove semantic gaps elsewhere: the prior
positive-subset inspection reports 71 prefix queue bounds, 21 record-boundary and
76 self-reference gaps. No exhaustive graph census or equivalence claim follows.

## Specific serialization obstruction and alternatives

The owned [empirical container account](../manual-save-corpus-S0-S7C.md) expressly
leaves unused header fields unknown. `stream_save.header` qualifies BCPS1 signature,
table offset +8, stream start +24, decoded length +32, block size +48, ZIP marker
+68, size table, alignment and EOF. Zlib verifies individual stream checksums,
EOF, consumed input and exact output lengths. The distinct whole-buffer decoder
checks those same core assumptions; it is an independent code path, not an
independent specification. Neither qualifies opaque physical header fields +16,
+40, +56 or +64. The current Save29 has a nonzero four-byte value `0x98fa3403` at
+64. **Its meaning is UNKNOWN; it is not labelled a checksum.**

The probe flips one bit at physical +64 in a temporary `.bin`. Both readers
accept it and reproduce the entire original decoded stream. The counterexample
proves this field is outside their validation, not that the game ignores it or
that the mutated header is invalid. Ordinary CRC32/Adler32 checks on decoded
content, physical body, first 64 header bytes and size table do not equal the
+64 value. This bounded diagnostic neither rules out other integrity schemes
nor discovers that field's semantics. Raw probe and scratch were removed; no
`.sfs` derivative or proposed installable artifact was created.

| Route examined | Evidence / disposition |
|---|---|
| Existing qualified owned writer | Source inventory/search under `save-analysis/scripts` and `research` found readers and synthetic BCPS fixtures, not a qualified retail serializer. Synthetic fixtures zero unused fields; they test reader behaviour, not original-container compatibility. Exact consulted paths/hashes are in the receipt. |
| Whole-container recompression, preserve header | Core chunk mechanics are known. Copying opaque fields unchanged when their dependencies are unknown would assume the missing contract. Not admitted as a qualified candidate. |
| Replace only affected compressed block | Both target bytes lie in decoded chunk 4. Retaining every other block narrows the physical delta, but does not establish preservation of possible container-wide dependencies. Compressed length/alignment may change. |
| Preserve compressed sizes/offsets | No qualified equal-length compressor or filler rule exists here. Guessing padding, appending compressed data, or manufacturing a checksum match would bypass qualification. Original chunk-4 padding is nonzero, so zero padding is not presumed authoritative. |
| Byte-identical original copy | Safe archive, but does not exercise a writer round trip; cannot be relabelled C. |
| Existing native/static evidence | Bounded text search for BCPS and its integer magic in retained `.local-work/recon/*.tsv` found no applicable container serialization evidence. P1's mapped Extra9C saver establishes the inner field, not the outer compressor contract. No new Ghidra session or database alteration occurred. |
| Third-party editor or trial load to infer validity | No approved writer/dependency established; no new third-party execution or live load is authorized. Not attempted. |

The stop follows the brief's explicit feasibility gate. Further static
serialization research could supply the missing contract; no universal inability,
fundamental encryption barrier or save corruption is claimed. The smallest next
work is that narrow qualification, not a speculative player trial or a general
save editor. This uses the brief's explicit NO-GO completion alternative; it does
not assert that further bounded offline diagnosis inherently needs new permission.
Live execution and third-party reuse retain their separate authorization gates.

## Frozen output contract and limits

| Stage | Intended words #1/#2 | Required decoded delta, not executed |
|---|---|---|
| C | `840 / 800` | Exactly zero bytes; independently originate from original |
| R | `800 / 840` | Only mask `40` at bytes 1300660 and 1301325; originate from original |
| O | `840 / 840` | Only mask `40` at byte 1301325; originate from original |

No both-off variant. Preserve all non-target bits, metadata, settings, entities,
ownership, graph and generation/demand inputs. The local manifest deliberately
contains `candidates: []`; derivative hashes, full derivative delta audits,
independent read-back and game acceptance are **NOT TESTED / NOT APPLICABLE**,
never fabricated PASS entries. Complete decoded byte equality outside exact masks
would cover even undecoded inner bytes, but would still not prove post-load
semantic equivalence. The [test card](save29-derivative-card.md) is preregistered
documentation and cannot be executed from this assignment.
