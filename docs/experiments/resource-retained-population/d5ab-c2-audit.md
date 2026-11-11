# D5AB C2 existing-evidence closure audit

2026-11-01, Australia/Sydney. **Existing evidence establishes specific native
boundaries and bounded fixture results; it does not qualify the observer or B2.**
D5AB remains **INCOMPLETE / REWORK**, B1 PARTIAL, D5AA ESCALATE, D5R OPEN and B2
NOT AUTHORIZED. The [edge matrix](d5ab-c2-evidence-matrix.md) is the primary
claim ledger; the [decision](d5ab-c2-decision.md) maps the unchanged parent contract.
Audit acceptance is governed by the [independent review](d5ab-c2-review.md).

## G1/G2 — authority and source correspondence

The user invoked the [C2 brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_C2_existing_evidence_closure_audit.md`).
The [original D5AB brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_observer_remediation_live_readiness.md`)
and [C1 brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_C1_continuation_assessment.md`)
are unchanged. Current HEAD is `18300618eacdfa50b6dc10303aa2fe30151e007b`;
the committed D5AB checkpoint is `623b49c878a8dfea051278d9cac41688342dd323`.
The historical report correctly describes its earlier uncommitted baseline
`1fe5c6c7a423300a9879dff15ed72e9a69b726cd`. The handoff prefix is not a tag.
Initial status contains only the supplied untracked C2 brief; index SHA-256 is
`6e14b03f3ab6af5d87a7f3e03c01343b9deb821bd161780d6ad86d503a367c16`.

All seventeen Freeze01 source pins match current bytes. S002's hash
`526cb1d575310474c6ec2d430312cc55c729c5d7a9befefd427200646387d527`
matches the retained **Build05** `sources/runtime/construction-winner/observer.h`.
Build08 and current source instead match
`ec2d731e861ede71a5159f1aae1c0cacb39d04a73c7da7b6771a184233801e81`.
This resolves which retained version S002 identifies; it does not establish why
the index was left at that version. Neither the index nor historical hashes are
repaired. Initial receipt's `47fb1e5e...` observer is a third, starting version.

Schema 3 has seventeen kinds in a 312-byte event and eighteen sites. Build08's
native source matches the final frozen native source. Its packaged reducer is
`f0b1f2d409f1baa5300d6ea18daa832ba4c6ddfd39cc21a660318df137699081`;
Final02/current reducer is
`c3226c3050d5d41143c92ee736e23e6474b77018b845f1f3613790e4444322c3`.
The direct reducer diff adds `Counter`, counts birth allocation IDs, and rejects
zero/duplicate allocation IDs and source values below `0x10000`; it changes no
native producer. The reader is unchanged at `2c50e5756680fe41a58ec0d7ce35827d758dc81929ea8082e1ff7b4c63134ca1`.
Final02 is later interpretation of retained native sessions, not a new combined
package build. A consumer-only change does not by itself invalidate the compiled
observer; an exact final distribution/qualification manifest is still missing.

Only existing exports, source and receipts were examined. No game executable was
opened for fresh inspection, no disassembler/exporter/build/qualification entry
point was executed, and no target, save, deployment, configuration, index, ref or
external service was changed. Original proprietary exports, raw sessions and
private receipts stay local. No new third-party material was incorporated.
Existing SFSE provenance remains the scoped inherited permission; C2 grants no
new reuse or publication rights. The 31-item gameplay checklist is untouched.

## L1/L2 — creation, ownership and lifetime

Export02's constructor has decisive positive evidence: Grid lock acquisition,
anchor deduplication, a 0x1a0-byte allocation, prefix initialization through token
`+0x68`, and the actual source-array store. The birth site precedes the string
operation and later initialization; publication is a separate successful store.
Reserve failure can leave a nonnull returned allocation unpublished. Deduplication
returns an existing allocation without a fresh birth. A native hash/string-derived
token is neither an allocation lease nor an injective geographic identifier.

The known bulk-clear and standalone-retirement paths erase the ProcGen pointer
map, release its lock and then free source memory. Grid destructor wrappers reach
bulk clear; shift reaches the predicate/retirement route. Existing global fences
cover those named entry routes, conservatively rejecting overlapping joins.
They do not prove that every alias, writer or exceptional cleanup reaches them.
The allocation-size census includes many unrelated objects; size agreement cannot
make them source objects, and a size scan cannot establish writer completeness.
The matrix inventories all 59 size candidates, including context-only unresolved
objects, and distinguishes classified constructor families from unresolved cleanup
and indirect aliases. Export03's two complete helpers have no preservation receipt;
Export04 supplies additional records, without retroactively completing Export03.

D5S's detached-density/shift-38 witness defeats **Grid-retention-only safety**.
The retained `native-retirement04.json/ordinary_shift_series` records 37 preserving
shifts and retirement at step 38 with Grid reference count 2. Its driver substitutes
terminal retirement/free with callbacks; actual source free is established by the
separate static retirement export, not by that fixture.
The retained reader-owning layer path protects a different invocation. Its manager
reader cannot be transferred to detached descendants after preparation-node
destruction. A generation-triple validity check is not a lifetime lease. Shift
can retire a source while the Grid object survives. This is a static adverse
schedule, not an observed retail crash and not proof that the current observer
necessarily misattributes every such schedule: its retirement fence may reject it.

Selection and visited callbacks do not dereference the selected source. Birth
copies a 0x70-byte prefix, including padding and dimensions that native code writes
later. Only the semantic identity fields/token have proven initialization before that copy;
RR also compares raw padding at `+0x39..+0x3b`, whose initialization/stability is
not established. Dimensions at `+0x18/+0x1c` are written after birth and excluded
by RR;
the visited witness records the engine-consumed
RDI token. However, the protected lookup's map lock alone does not prove source
ownership: the source is read by native code before that lock, and retirement
frees after unlock. A complete owner/alias argument remains necessary for the
lookup copy and birth-to-visited correspondence. ReadProcessMemory bounds/failure
handling prevent an unchecked copy, but do not prove identity or synchronization.

The reducer requires unique observer allocation IDs, one publication, ordering,
matching token, no observed intervening lifecycle span and matching loss generations.
These are useful conditional checks. They cannot detect an uninstrumented free or
identity write. Observer IDs are capture identities; they are not native cookies.
Pre-arming sources and unpublished births deliberately remain unqualified.
ABA, owner replacement, unknown invalidation and cross-thread ties need the exact
controls listed in the matrix; no absence-of-counterexample safety proof is made.

## S1 — reserve and actual store

The retained provider shows reserve call `0x14079ff3e`, sentinel test
`0x14079ff54`, skip at `0x14079ff57`, and token write `0x14079ff60`.
These are preferred static VAs for image base `0x140000000`, on the recorded
Starfield executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
They are not freshly verified runtime addresses or cross-build claims.

The store bridge replays the write before invoking `stored_capture`; a fault before
the callback cannot yield its store witness. Reserve exceptions emit an exception
status and rethrow. The helper receipt tests six index/count/sentinel cases using
substituted callbacks, without backing allocation. The compiled fixture also uses
a modeled reserve implementation. Thus the executed-store boundary is statically
supported, while complete allocator, exception/unwind, source and epoch qualification
is unresolved. Successful append proves visited insertion, not nonempty geometry. Direct existing
frame inspection (`.local-work/d5ab-c2/frame-inspection.json`) finds reserve/store
in the 17-frame normal fixture, reserve without store in the 16-frame failure
fixture, and store without birth/publication in the 15-frame unknown-birth fixture.
The 16-frame skipped-sample case has a store but no sample. These are frame/type
and CRC checks on retained bytes, not a rerun of native or semantic qualification.

## T1 — transport and recorder

Queue02's nine retained runs measure 320-byte compiled cells. Its generated source
is the checked-in 12,000-offer harness transformed to **four times 8,000 = 32,000**
offers. The source comment/default alone is not the tested workload. Consumer
draining follows the initial three-second pause **and producer joins**, so this
is a held burst, not proof of a fixed three-second production window.

| Capacity | Queue bytes | Held losses, each of three runs | Concurrent overload losses, repeats 0/1/2 |
|---:|---:|---:|---|
| 1,024 | 327,680 | 30,976 | 53,467 / 59,957 / 63,962 |
| 8,192 | 2,621,440 | 23,808 | 56,976 / 53,125 / 52,638 |
| 32,768 | 10,485,760 | 0 | 17,975 / 26,597 / 12,546 |

Representative fixture: 21,061 durable records, all seventeen kinds, zero reported
losses, a three-second raw-flush pause and peak working set 16,015,360 bytes.
Queue bytes and whole-process working set are different measurements. These
positive controls justify a bounded capacity benefit, not a retail guarantee.
B1's 9,957 lost attempts have no recovered timestamps or category distribution;
they must never be added as modeled arrivals to D5Y/D5AA retained-arrival replays.
Their 19,780 admissions, 1,024-cell pressure and 1,206.5674-ms maximum combined
flush time identify constraints without uniquely diagnosing a bottleneck.

Production code uses acquire/release ticket publication, a finite drain snapshot,
64-record batches, raw-before-ACK flushing, bounded retry/loss counters, overflow
disablement, guarded targets/relays, both-drive disk checks and active-producer
shutdown. ACK telemetry preserves loss history outside the event stream; sampled
loss bounds can explicitly become uncertain. Wake/drain/write/raw/ACK/guard/disk/
shutdown diagnostics exist independently of queue admission. Their presence and
bounded passing fixtures do not close recorder/controller death detection.
`watch()` never calls `verify_ack()`, does not send STOP, and classifies an exit
from STOP-file presence. Worker02 tests its own Python thread, not the recorder
or controller. Integration and authenticated STOP ownership remain exact gaps.

## R1 — interpretation and counterexamples

Final02 records 61 native-session interpretations, 54 semantic expected/actual
matches, eight damaged-session refusals and unchanged schema-2 B1 interpretation.
The matrix indexes every case with the actual source version and oracle. No
qualification case was rerun. Hash checks authenticate retained inputs/outputs;
they do not independently reproduce the semantic outcome.

The expected constants derive from explicit fixture actions. Semantic derivatives
start from the normal capture, mutate specified fields and sometimes renumber
sequence/ticks; they are models. Seed 547 shuffles list arrival only; it does not
test every inter-thread causal order. zlib versus native bitwise CRC provides a
separate framing calculation, not an independent lifetime oracle. Missing append,
identity collisions, lost retirement, unmatched fences and pre-arming selection
have useful refusals; native coverage is still a premise.

No retained case supplies an integrated real empty/partial-geometry oracle,
exception between reserve and store, detached retirement with actual reuse, or
recorder/controller death/restart protocol. Direct mask zero is not an empty
geometry test. `map-hit` models the outcome; it does not establish the actual
competing native wait schedule. Current source QPC and epoch tests reject some
ambiguities; they cannot recover unobserved engine history. Required discriminating
controls and their authority are in the decision. No B1 target first query, direct
mask or append has been recovered, and no new B2 episode has occurred.

## Preservation and reproducibility

Read-only audit receipts are under `.local-work/d5ab-c2/`: `baseline.json`,
`evidence-before.json`, `preservation-before.json`, `consistency.json`,
`function-census.json` and the final preservation/check receipts. They record paths,
byte sizes, hashes, mismatches and exact versions. Documentation-only editorial
and patch checks are separate from instrumentation qualification. The review
record supplies the final manifests, exclusions and patch verification. Existing
evidence remains LOCAL-ONLY; authored C2 synthesis is REVIEW-REQUIRED.
