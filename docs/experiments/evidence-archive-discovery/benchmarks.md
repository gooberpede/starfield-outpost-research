# Compression, verification and resource measurements

[Raw compact measurements](benchmark-measurements.csv), [planning strata](planning-scenarios.csv),
[scope amendment](scope-amendment.md). All actual source members were replicated
to a marked disposable tree and matched prior expected SHA-256 identities before
compression. No actual research source was archived in place, altered or deleted.

## Current non-save samples

| Whole-file sample mix | Input MB | tar.zst MB / ratio | ZIP MB / ratio |
|---|---:|---:|---:|
| Native observation binary and JSONL | 1,944.078 | 41.348 / 0.02127 | 57.816 / 0.02974 |
| Large definition-analysis JSON | 1,777.793 | 122.062 / 0.06866 | 125.665 / 0.07069 |
| Resource observation journal and build log | 90.584 | 1.455 / 0.01607 | 2.555 / 0.02821 |
| Native TSV and preservation receipt | 18.321 | 3.634 / 0.19834 | 3.573 / 0.19505 |
| Total | 3,830.776 | 168.499 | 189.609 |

MB/GB here are decimal. The samples are purposive, not random: they include
large actual byte contributors and mixed data, not just tiny text fixtures.
They cover 11.63% of the current eligible pool. Neither their weighted ratio nor
the observed range is a guaranteed full-estate compression ratio.

The installed CPython 3.14.3 provides stdlib Zstandard 1.5.7; no dependency was
installed. The comparison uses tar.zst level 3 and ZIP/Deflate level 6. Tar.zst
is smaller across the combined sample, but is not uniformly faster in these
observations. Order is tar.zst then ZIP for each sample, with warmed copies and
uncontrolled host/cache effects. Single trials establish these actual costs,
not statistical throughput rankings. The CSV retains all phase timings.

Tar creation across current samples takes 28.257 measured seconds; ZIP takes
20.030. The full measured format phases, including validation, restore and extra
byte-equality checks, take 90.837 and 84.198 seconds respectively. These are
application wall observations, not CPU or physical-device I/O measurements.
Creation includes conservative free-space admission and container close.

The original benchmark preceded the save-file amendment and included one
additional save-copy mix. Its raw receipts remain local. Current tables exclude
that mix. The recorded setup takes 125.170 seconds for all original samples;
exact non-save-only setup time is UNKNOWN, bounded above by that sequential
total. Non-save intake reads/hashes and writes exactly 3,830,776,378 copied bytes.
Original non-save source hashes are checked again at the end. No save payload
is re-read to revise these tables.

## What is read and hashed

For each format, packaging reads and hashes every copied payload, initial member
validation decodes/hashes every member, and the archive is hashed before and
after final naming/index registration. Routine verify separately hashes the
complete encoded archive and then validates every included member. Restore
hashes the archive, streams/hash-checks members, rehashes restored files and
performs an additional independent copied/restored equality check.

That is seven payload SHA passes per format, plus intake and final original
checks: **61,292,422,048 non-save payload bytes hashed** across the experiment.
Encoded archive digest passes add **1,432,434,620 bytes**. Master-index hashing,
source-ledger checks and compressed decoder reads are additional control/input
work, not eliminated cost. Decoded SHA bytes are not physical disk bytes: caches
and decompression can supply those bytes without an equivalent device reread.
Physical I/O and isolated peak memory are UNKNOWN.

Successful full tar decoding is sequential and bounded by expected member sizes
and framing. ZIP also reads central/local metadata and may reread small regions;
its decoder I/O is not asserted to equal archive size. Source/decoder/control
reads are distinguished from cryptographic byte totals. No setup is counted as
a migration saving.

The prototype's full verify and restore receipts record archive hash time,
member verification time, restored-byte rereads, index hash bytes and member
counts separately. An archive digest is accepted only after an initial
authenticated member-to-source comparison. It never proves semantics or
authorizes release.

In the executed method, the `archive_hash_seconds` phase also includes master
index authentication/deserialization and lookup. It is not an isolated hashing
throughput measurement; full index byte cost is separately visible.

## Index and format scale

The final schema supports canonical members, original-location aliases and
cross-system references in one logical SQLite index. Disposable benchmark,
fault-test and scale indexes are separate test instances, not per-experiment
production sidecars. No production index is emitted.

The synthetic full-cardinality rehearsal uses all 242,995 eligible path shapes
under nine roots, with zero-byte fake payloads and fake digests clearly marked
`SYNTHETIC_SCALE_ONLY`. Its index is **203,890,688 bytes**, under the 256 MiB
prototype cap. Loading every root takes 17.901 seconds and repeats 1,835,016,192
index hash bytes. It validates index/name/cardinality handling, not real member
identity, real compression or a real migration. The separate 70,000-member tar
test exercises actual streaming container validation.

Tar supports at most 300,000 members per archive and bounded 4,096-byte names,
with a strictly limited PAX path override. ZIP is a sample-scale alternative,
limited to 65,534 members by this prototype; it is unsuitable for the 134,140-file
resource archive without separately qualified ZIP64 support. No silent truncation
or per-brief splitting is proposed to evade those limits.

Exact benchmark methods are retained in `benchmark01/methods/` and match its
freeze hashes. Later schema-2 alias mechanics and tighter safety reservations
are separately qualified. The current driver excludes saves and uses a stronger
whole-run reservation; historical timings are not reassigned to that version.

## Temporary storage, guards and conditional recovery

All prototype copies/restores and failed vectors remain local. The benchmark's
end logical temporary footprint was 12,692,158,698 bytes, including its now-held
save-copy artifacts and earlier task metadata. Later index/qualification outputs
increase that footprint. Final delivery records current totals/free space and
a conservative transient-journal margin. Logical/cluster totals are not exact
physical allocation; no temporary cleanup or real recovery is claimed.

Because outputs are retained, final retained logical bytes bound most earlier
temporary use; an additional 512 MiB covers the bounded index/journal window,
plus small compression buffers and truncated fault-vector differences. This is
a disclosed engineering bound, not an instrumented peak-device counter. SQLite's
own transient journal lifecycle is distinct from deletion of research evidence.

Both C: and D: retain the 40,000,000,000-byte guard. Packaging reserves conservative
container expansion, per-member metadata and bounded index/journal space; restore
reserves payload plus directory/file cluster overhead. Current benchmark replay
reserves seven times copied input plus 1 GiB for simultaneous copies, two format
archives/restores and metadata. The original run used a smaller initial aggregate
reservation, with per-phase guards and ample actual free space; no guard failure
was recorded. Metadata helpers subsequently gain explicit write reservations
for their fixed observed workloads; their original namespace/index timings stay
bound to the preserved executed versions. Stage B must reserve each next phase from actual archive lengths,
never delete sources just to admit the next write.

Projected one-replica allocation recovery is 18.91–30.69 GB under the transfer
scenarios; two replicas give 4.25–27.82 GB. Those are conditional estimates over
the frozen pool, not observed reclaimed disk or guaranteed intervals. From the
initial D: free space of 96.35 GB, add a selected recovery estimate and subtract
post-freeze Stage A growth and any retained restore/compatibility files. Final
free-space anchoring is provided in the delivery record. Held saves/containers
and loose unknowns remain in place in every calculation.

No baseline elapsed time for the historical 93,334-entry audit is reconstructed
from completion timestamps. Stage B must freeze a comparable loose/archived
verification workload and include all index, payload, archive, setup, restore,
backup and repeated work before claiming the eventual 80% objective.
