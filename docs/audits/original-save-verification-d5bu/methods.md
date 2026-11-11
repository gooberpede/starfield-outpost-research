# D5BU portable methods and source effects

Use CPython 3.14.3 on Windows with `-I -B` and assertions enabled. All code
is stdlib and project-owned under SOR-P-0002. Keep supplied originals immutable.
Use an existing caller-owned ignored parent and new output names. The two-drive
caller-available guard runs before output and during streaming decode. Every
selected original is pinned before and after decoding.

| Entry point under save-analysis/scripts | Explicit arguments | Data reads and outputs |
| --- | --- | --- |
| verify_d5bu_geography.py | `--member ID PATH` for 1,2,3,40,47,49,53, `--esm`, `--planet-data`, `--output-directory` | Reads the seven exact D5BF originals, pinned main ESM and PlanetData BA2. Reconstructs the body index and three named v5 maps. Writes only a fresh local directory with map copies, seven decoded summaries and deterministic result JSON. |
| verify_d5bu_fabricators.py | `--hist-0036`, `--esm`, `--receipt` | Reads exact F064, pinned main ESM and authored recipe/facility tables. Rebuilds selected producer, extra and graph joins, traversing only this original. Writes one exclusive receipt. |
| verify_d5bu_controls.py sd2 | `--member ID PATH` for 40,42,51,64, `--esm`, `--addon`, `--receipt` | Reads exact selected originals, main/add-on ESMs and selected physical definitions. Writes one exclusive receipt containing fresh-owner and inline-base checks, zero/version controls. |
| verify_d5bu_controls.py roots | `--member ID PATH` for 40,42,43, `--root-context BASELINE TYPED ALLA`, `--canonical-context`, `--esm`, `--receipt` | Reads three exact provenance-pinned root inputs and the named canonical ledger, main ESM and selected originals. Rejoins every supported root/member and original beacon state, retaining unresolved groups. Writes one exclusive receipt. |
| verify_d5bu_controls.py construction | `--member ID PATH` for 11–16,29–39,41–45,51 and `--receipt` | Reads exact selected originals and authored root/bulldozing/variant tables. Checks paired core roots, budgets, placement registrations, gap ledgers and H255 variant extras. Writes one exclusive receipt. |
| verify_d5bu_cargo.py | `--save52`, `--c3-context`, `--receipt` | Reads exact F040 and recovered pinned C3 save01 context. Independently rebuilds finite C2/C3 selections and compares the retained projection. Writes one exclusive receipt. |
| verify_d5bu_output_links.py | `--l0 --l0c --l1 --l1c --l2 --l2c` paths and `--receipt` | Reads the six exact originals and three authored CSV oracles. Pins the actual buffer decoded, checks windows and payload controls, and writes one exclusive receipt. |
| d5bt_reader.py | `save29` or `hist-0021`, `--save`, `--output-directory` | Preserved accepted reader. Reads exact F054/F067, writes a fresh deterministic receipt, and removes temporary decoded scratch. |
| test_d5bu_verification.py | No data arguments | Eleven synthetic tests. Temporary synthetic files are caller-process-owned and removed by tempfile. No original input or game installation is used. |

The D5BF ledger is pinned by digest before selectors are resolved. A member ID
is an input selector, with the full original digest controlling identity.
Unsupported format, buffer, framing, queue, extra and source cases refuse or
retain the documented parser gap. A decoding failure preserves a separate
diagnostic and requires a fresh output name for correction.

## Source lineage

- Geography adapts the owned CS/B1 readers and exact-dyadic oracle. It uses
  the existing body, world, descriptor, Workshop and projection functions.
  It replaces the old body-index/survey scratch dependencies with explicit
  installed ESM reads and the finite seven-member set.
- Fabricators adapts the owned E3 saved/detail traversal. Authored recipe
  identities and a pinned ESM reread replace the absent loose E2/catalogue
  scratch files. Saved BF omission and definition-derived preset remain
  distinct. It retains incoming-cargo termination and UNKNOWN endpoint classes.
- Shared fixtures and construction reuse typed_records, the independent
  arithmetic walk, inventory root projection and the exact owned crew grammar.
  The BM1 B4/DE extension compiles that pinned Python function in memory,
  preserving its original module. It executes owned analysis code.
- Root reconstruction reuses research_workshop_roots.supplement with its
  original three pinned contexts. The canonical ledger is the named
  Workshop-population source record, pinned before access and after use.
- Cargo adapts the owned C1/C2 parser and recovered C3 probe. The archive,
  index and the two exact recovered C3 members retain their source hashes.
  No standalone derivative verifier is substituted for an original-byte read.

Existing Bethesda, CPython/zlib and project research attribution remains in
[CREDITS](../../../CREDITS.md) and [SOURCES](../../SOURCES.md). Exact method
ancestry, current module closure and final source identities accompany the
[receipt manifest](receipts.json). No third-party implementation was incorporated.

## Qualification and limits

Source-only qualification copied authored Python and required authored CSV/JSON
oracles into a new isolated tree. Explicit file arguments supplied only the
allowed external data. The observed open-file and module audit is local and
hash-bound. It records stdlib loading, source reads, temporary decode files,
declared historical contexts and caller outputs. No historical acquisition main,
active-save copy mode, broad save survey, native code or analysis database ran.

Original buffers are temporary read-only mappings. The largest pinned historical
contexts total approximately 645 MB and the largest selected decoded input is
62,194,872 bytes. The decoder streams chunks, while the root supplement holds its
qualified JSON inputs in memory. Actual disk guards and output accounting are
recorded separately from scientific results. Caller scratch is retained, and
there is no automatic cleanup of prior evidence or source-only trees.

The first geography receipts included decoder elapsed time and consequently
changed their downstream hashes. Final deterministic receipts exclude elapsed
time. E3 iteration and JSON ordering are fixed. Failed Cargo adaptations exposed
a missing local dictionary and an incorrect summary of nested unsupported extras.
The corrected reader retains the actual Extra30/D9 gap classification.
Synthetic source-generation failures and all predecessor receipts remain local.
These are engineering failures with no original modifications.
