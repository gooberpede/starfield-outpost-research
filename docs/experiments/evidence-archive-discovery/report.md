# Consolidated evidence archives: Stage A discovery

2026-10-25, Australia/Sydney. Offline discovery and disposable qualification under
the [original brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_consolidated_evidence_archival_stage_a.md`)
and accepted [save-file scope amendment](scope-amendment.md). **No real evidence
has been migrated or deleted; no archive boundary or verification policy is active.**

| Element | Supported answer |
|---|---|
| Question | Can a few system archives preserve the evidence estate and provide a measured basis for later consolidation? |
| Answer | Nine focused candidates, or six broader candidates, cover the proposed non-save pool through one central owner/path index. Authenticated streaming tar.zst restoration and bounded failure handling work on disposable inputs. |
| Confidence | Measured namespace/counts and sample byte equality; qualified prototype mechanics. Whole-estate compression and recovery are scenarios, not completed migration. |
| Coverage | Entire observed `.local-work/` namespace metadata; 199 top-level directory groups, 11 thematic areas; 3.83 GB of current-scope actual samples; synthetic adversarial and full-cardinality index tests. |
| Backup feasibility | 10 GB appears plausible, but is not demonstrated: transfer scenarios are 2.87–14.66 GB including an index. No off-device backup, storage entitlement or upload authorization is confirmed. |
| Evidence | [Areas](research-areas.csv), [descending inventory](directory-inventory.csv), [options](archive-options.csv), [benchmarks](benchmarks.md), [retention](retention.md), [review](review.md). |
| Next decision | Approve or amend the proposed research-system boundaries and retention policy. A separate exact-path Stage B authorization is required before deletion. |

## Measured estate and current scope

The corrected metadata traversal observes **245,097 paths / 48,361,119,803 logical
bytes**, or about 45.04 GiB. That is consistent in scale with the reported
approximately 45 GB; the earlier approximately 230,000-file estimate was not a
frozen full-tree baseline. No causal 15,000-file growth claim follows from it.
Traversal reports zero access/reparse omissions and 245,093 file objects; four
extra hardlink names occur in earlier disposable qualification fixtures.

The earlier 93,334-pin inventory contains 93,307 inside paths, all present here,
and 27 outside `.local-work/`. Another 151,790 observed paths are not in that
inventory. Those are path-set differences, not new unique scientific observations.
Metadata inventory does not verify their payload bytes. The previous
[preservation optimization](../preservation-verification-optimization/report.md)
remains **REWORK / AC4 FAIL**.

After the maintainer set saved files aside, the current eligible proposal is
**242,995 files / 32,930,782,429 bytes**. The remaining 2,102 paths and
15,430,337,374 bytes stay held or loose. [Scope accounting](scope-accounting.csv)
reconciles every path: saves, raw decoded/probe save streams, opaque containers,
save-corpus roots, current Stage A work and unresolved working data. None is
called disposable to improve the 10 GB calculation. Analytical JSON/CSV reports
derived from saves remain research evidence; raw saved payloads do not enter
the current proposal.

The frozen inventory includes 113.89 MB of this task's initial working files.
Later benchmark/qualification/index outputs add temporary storage outside that
frozen estate. Both effects are disclosed in [resource accounting](benchmarks.md).

## Candidate roster for maintainer editing

Scheme A keeps nine focused system/support archives. Each eligible original
path has exactly one proposed physical archive owner; other systems use central
references. Counts below exclude every held/loose class.

| Proposed archive / research system | Files | Logical GB |
|---|---:|---:|
| Identity, location and lifecycle | 21,229 | 17.572 |
| Resources, production and power | 134,140 | 8.003 |
| Crew and robots | 1,399 | 2.188 |
| Shared native observation and methods | 40,353 | 1.757 |
| Governance, review and publication evidence | 42,074 | 1.491 |
| Construction, limits and defense | 903 | 1.098 |
| Storage and local links | 1,540 | 0.705 |
| Shared corpus research indexes/receipts, excluding saved payloads | 303 | 0.082 |
| Cargo transport and fuel | 1,054 | 0.035 |

The largest directory is `workshop-inventory`: 12.31 GB, predominantly successive
large analytical outputs. Their names do not prove byte reproducibility, so they
remain retained. Resources/production dominates file count; earlier fixture and
review products are not automatically disposable. The complete thematic list is
sorted both [by theme](research-areas.csv) and [by size](research-areas-by-size.csv).
Linked experiment IDs are source mentions, not inferred exclusive membership.

Scheme B merges identity with construction, production with storage/power, and
native methods with governance, yielding **six** candidates. Both schemes remain
under the hard ceiling of 30. If separately approved duplicate archive replicas
are required, nine identities would mean 18 files, or six would mean 12; replicas
are not additional research systems or confirmed off-device backups.

Decisions to edit: whether power merits its own system; whether shared methods
and governance should merge; whether the large identity/lifecycle area should
split along actual research boundaries; and how to retain unresolved loose data.
Do not split merely by brief or make one archive per experiment.

## Retention, backup and projected recovery

The conservative complete non-save set is 32.931 GB; essential is 32.893 GB.
The only proposed omission is 4,120 deterministic stand-in payloads, 37.81 MB,
proved against their exact builder, original fixture manifest and current hashes.
All primary observations, failed trials, actual test receipts and unresolved
derivatives stay essential. No named/old file is declared regenerable by inference.

Four actual non-save sample mixes total **3,830,776,378 bytes** and encode into
**168,499,306 tar.zst bytes**. These purposive samples cover 11.63% of eligible
logical bytes, including a large native binary, JSONL, a large definition
derivative, native TSV and hash receipts. ZIP is a practical comparison, not the
chosen large-population format. Full preservation, creation, restoration and
setup costs are separate in the benchmark report.

Fitting essential content below 10 GB requires a ratio at most **0.3040**.
The 2.87–14.66 GB scenarios transfer observed text ratios, allow binary data to
be incompressible in the cautious case, and store unmeasured types. They are not
statistical uncertainty intervals or bounds on every file. The separate raw-tar
serialization budget is 33.33 GB including the synthetic index; it is not a
claim about zstd framing or actual full-estate output. Prioritize unique native
observations, their identity/provenance, original methods and counterexamples if
backup space proves insufficient; do not delete originals or trim unknowns to fit.

Conditional approved consolidation of the full non-save pool projects 2,112
frozen-namespace files with one archive/index replica, or 2,122 with two. Those are ceilings on
consolidation opportunity, not promises: operational consumers, source-version
holds and archive/index replicas can require additional loose files. Net estimated
allocation recovery is 18.91–30.69 GB for one replica, or 4.25–27.82 GB for two.
Resident-file accounting, future compatibility holds and post-freeze temporary
growth make actual values uncertain. **Actual recovery in Stage A is zero.**

## What Stage B still has to prove

[The non-executed plan](stage-b-plan.md) proposes a complete cargo-system pilot:
1,054 files / 34.60 MB, with two current hash passes and 510 matching prior source
identities. Three retired packager paths have historical source-version holds;
their current hashes match B5's later creator inventory. Older execution hashes
remain separate, and those paths cannot be deleted while provenance is unresolved.
Other missing historical expectations remain UNKNOWN, not retroactively validated.

No existing absolute-path consumer becomes archive-aware automatically. Static
discovery finds 52,741 literal mentions in 1,103 source files, with a complete
local mention ledger and a compact [dependency table](dependencies.csv). Dynamic
paths and untracked external consumers remain coverage limits. Stage B must
qualify extraction/adapters before its separately approved cutover.

The eventual 80% routine-verification objective is **not achieved or claimed**
here. Future comparison must freeze equivalent evidence/protection scope and
measure handles, enumeration, actual compressed/payload/index hash bytes, setup,
restoration and elapsed time. The current prototype rehashes its full master
index per call: the full-cardinality synthetic index is 203.89 MB, and nine calls
read/hash 1.835 GB of index data. Fewer handles alone do not establish savings.
