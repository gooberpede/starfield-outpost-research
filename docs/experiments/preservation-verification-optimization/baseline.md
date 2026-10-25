# Frozen baseline and accounting domains

[Report](report.md), [source identities](sources.csv). Primary reconstruction is
`.local-work/preservation-verification/reconstruction.json`; per-path current
metadata is in `private-inventory.json`. No broad historical payload audit was
rerun to obtain timings.

## Receipt reconciliation

| Inventory | Pins / normalized paths | Added from previous | Removed | Shared changed hashes |
|---|---:|---:|---:|---:|
| D5C | 77,893 | Not applicable | Not applicable | Not applicable |
| D5D | 78,435 | 542 | 0 | 0 |
| D5E | 78,435 | 0 | 0 | 0 |
| D5G | 93,334 | 14,899 | 0 | 0 |

Before and after receipt contents are equal within each task. D5D and D5E have
identical pin mappings despite their different task HEAD/index fields. These
counts identify path records, not unique content hashes, observations or archive
members. Lexical Windows case/separator normalization finds no duplicate paths;
current stat device/file IDs identify 93,334 distinct file objects. No historical
hardlink topology is inferred. Five ZIP paths are counted as five files, without
opening or enumerating their members. Compression/decompressed representations
remain different physical paths.

| Task | Before completion UTC | After completion UTC | Audit elapsed |
|---|---|---|---|
| D5C | 2026-10-25T04:16:58.163957+00:00 | 2026-10-25T04:29:52.161640+00:00 | UNKNOWN |
| D5D | 2026-10-25T05:19:25.709968+00:00 | 2026-10-25T05:35:57.952305+00:00 | UNKNOWN |
| D5E | 2026-10-25T06:22:22.008046+00:00 | 2026-10-25T06:40:38.132153+00:00 | UNKNOWN |
| D5G | 2026-10-25T08:49:50.600350+00:00 | 2026-10-25T08:57:55.635867+00:00 | UNKNOWN |

These timestamps follow successful completion and receipt writing. Subtracting
them includes intervening scientific work and omits the before scan's start.
There are no valid start/elapsed fields in these audit time receipts. Historical
wall/CPU/peak memory, scratch use, actual read bytes, physical I/O and cache state
remain UNKNOWN. Eight-worker D5G after parallelism is established by source;
neither throughput nor device saturation is established.

## What is counted and what is not

D5G before verifies the union of D5 and D5D after-pins: 78,435 expected hashes,
with no conflicting overwritten digest. It then recursively enumerates five
local task directories and hashes the expanded 93,334-path union. The before
method is retained as `audit-before-method.py`; the final tracked audit adds
eight-worker parallelism only to the after branch. After reads the fixed before
list and rehashes each path once. Thus 265,103 scheduled payload SHA-256 calls
are supported by source and successful receipts. Unique paths across this
schedule are 93,334. Actual physical reads are UNKNOWN, including cache reuse.

The following are additional, separate work domains:

- `protection.audit()` runs before each branch and may read the same files again;
  its 12,974 historical rows are not 12,974 protected active saves.
- D5G scientific expected-input comparisons, installed projections and native
  control checks are independent of the broad inventory.
- Review rehashing, patch verification, source-ledger reads and archive member
  validation are not included in the 265,103 scheduled-call subtotal.
- HEAD/index hashes and metadata reads are control-plane operations, separate
  from payload hashes. A successful hash receipt establishes neither semantics
  nor complete namespace coverage.

## Current metadata and category limits

The [aggregate CSV](inventory-breakdown.csv) provides four separate partitions:
directory, extension, heuristic task relevance/evidence category, and the
historical strict-pin class. Do not sum across those dimensions. The category
partition applies priority in this order: save/backup candidates; nine explicit
D5G `input-pins.json` identities; installed/analysis candidates; derivative or
diagnostic names; evidence suffixes; other/unknown. It does not reclassify any
historical protection or establish that a build EXE is the installed EXE.

| Heuristic category | Paths | Current stat bytes |
|---|---:|---:|
| Critical original or backup candidate | 409 | 4,023,637,952 |
| Explicit D5G input-pin entry | 9 | 2,528,866 |
| Critical installed or analysis candidate | 203 | 3,556,518,391 |
| Historical derivative or diagnostic | 39,798 | 499,276,741 |
| Historical evidence candidate | 24,920 | 535,864,231 |
| Other or unknown | 27,995 | 1,740,107,334 |

All 93,334 current metadata reads succeeded; total current stat size is
10,357,933,515 bytes. The 11.1308042-second metadata/accounting interval is a new
measurement, not historical audit timing. Sizes are current observations, not
proof of unchanged content or measured historical hash bytes. The two largest
directories are combined-acquisition (40,551 paths) and source-decisions
(14,860); the latter largely explains D5G's expanded path inventory.

Relevance has explicit overlap and uncertainty. A historical native export can
also be task-used; a receipt can be the scientific input to this audit. The
D5G source ledger cites 37 rows including methods and three installed labels;
its nine-entry expected-input manifest is not complete read coverage. Nothing
outside those nine is thereby declared irrelevant or disposable. No full
read-set trace exists, so exact D5G task-used coverage is UNKNOWN. The residual
categories remain pinned. Current data cannot honestly assign every path to
critical, scientific, immutable, intermediate or transient semantics.

## Frozen representative workflows

`run04/freeze.json` fixes expectations, byte sizes, workloads and five paired
trial orders before the corrected evaluation. Earlier run01/run02 fail at journal
setup before emitting measurements; run03 is a preserved superseded attempt with
the same denominators. The frozen synthetic historical category is
4,096 files in 16 subdirectories plus their root: 4,113 entries, 35,651,584 bytes.
Each group of 64 has 48 files of 1,024 bytes, 15 of 16,384 and one of 262,144.
These are generated stand-ins, not copies of game evidence.

W1 models ordinary offline inherited/union verification, a fixed-list after
pass, 17 scientific inputs and eight critical inputs. Legacy historical hashing
has three passes; full replacement has two; conditional journal mode has zero
historical payload passes and two journal gates. Filesystem enumeration, logical
pin traversal, opens, unique files, hash calls/bytes and wall/CPU are separate
metrics. All modes freshly hash every scientific/critical fixture input twice.

W2 uses full/full before/after protection and backup equality, installed EXE/ESM
stand-ins and both-drive free-space guards. Neither arm uses historical skipping.
The guards query actual free space; no game, real save or installation is touched.
The frozen mandatory 80% target applies to comparable W1 historical work, never
to a changed denominator or a weaker protection promise.

`perf_counter` measures wall time; `process_time` measures this Python process's
CPU. Files are warm from creation; order alternates to expose some order effects.
No cache eviction, physical-I/O instrumentation or per-trial peak-memory counter
was used, so those values are UNKNOWN. Fixture and manifest byte counts describe
logical scratch content, not allocated NTFS blocks. All setup is separately
charged in the report; repeated baseline loads and journal reads are included in
routine timings. Compression/member CRC work for the synthetic scientific ZIP
adds reads beyond payload hash bytes and is identical across W1 arms.
