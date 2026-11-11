# D5P-R1 diagnosis and repair decision

2026-10-29, Australia/Sydney. Written before production repair under the
[R1 brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5P_R1_observer_resilience_context_repair.md`).
R1-AC1–R1-AC9 are frozen unchanged. Offline inspection, task-owned edits and
disposable Windows qualification only. Retail remains NO-GO; B6/publication
remain on hold. The initial branch is `main`, HEAD
`82f961712e397e4f60c0725205ce8215e1ad074c`; exact source and evidence hashes,
index identity and both disk floors are in `.local-work/d5p-r1/initial.json`.

## Diagnosis before repair

The [historical Phase B account](d5p-phase-b.md) remains FAILED / UNRESOLVED.
Its authenticated 1,592 records, 319 invalid demands, seven query/mask pairs,
six completion snapshots and eleven lookups cannot establish the selected
source chain. The one reported drop conflates capacity and retry exhaustion;
subsequent disabled observations are unquantifiable.

| Hypothesis | Inspection/discriminator performed before repair | Supported decision |
|---|---|---|
| Queue full caused the retail drop | `emit` has separate capacity and 32-attempt CAS exhaustion paths but one counter. No occupancy or cause was retained. | UNKNOWN historical cause. Separate counters and never retire on either ordinary loss. |
| Writer throughput is insufficient for bursts | `drain` performs two writes per record and flushes every snapshot; historical build13 overflow and paced build14 do not qualify unpaced throughput. | Measure real unpaced production and writer progress; retain bounded producer work. |
| The visited bridge passes an incorrect stack or register | Original provider export `resource-milestone-b-producers-01.tsv`, preferred VAs `0x14079f860`–`0x14079f8d3`, establishes W = entry RSP − `0x3c8`, R13 = RCX; the bridge saves 192 bytes and passes W. Source is W+`0x38`, query pointer W+`0x3d8`. | Inspected bridge arithmetic agrees. This does not establish every retail object predicate. |
| An early read or current-manager mismatch explains all demands | All 319 original demand payloads have copied source bytes, query words, owner `0x0005e0de`, mode 2 and nonzero descriptor. Short-circuit evaluation reaches these only after the early reads and manager/ProcGen equality. | Those early predicates passed in these records. Failure remains in the later ProcGen/Grid/type/extent/membership chain. No exact failing predicate can be recovered. |
| Grid/type/membership predicate is wrong or rejects a legitimate context | `native-full.tsv`, `native-owner-copy04.tsv` and `native-sites04.tsv` support the ordinary Grid vector and expected types; the original fixture mirrors the selected layout and cannot distinguish a legitimate alternate runtime type. No failed operands were retained. | Do not relax predicates. Add stable first-failure reason codes, read-result/operand provenance and explicit unsupported coverage. Retail cause remains unverified. |
| Losses can be joined using unequal pointers | Missing invalidators may affect every source and permit ABA. The admitted sequence is allocated only after reservation. | Global loss generation contaminates all overlapping causal chains. Pointer inequality supplies no exemption. New complete invocations after a fully quiescent loss boundary may qualify within the existing scoped hook contract. |

## Intended minimal changes and qualification

Retain eleven hooks and original-call/guard semantics. Version evidence rather
than reinterpret historical payloads. Add bounded context diagnostics without
using failed reads as observed zeroes. Keep a bounded MPSC queue; count capacity,
contention and fatal output/safety failures separately. Ordinary loss advances a
conservative continuity generation and acquisition continues. Durable receipts
must expose loss totals and queue progress independently of record sequences.
Readers authenticate prefixes independently of session health and reject chains
that cross a possible missing decisive event. No first-ever or absence claim
follows from an incomplete stream.

Before claiming offline readiness, exercise actual compiled interception and
transport with valid/invalid contexts, forced single/multiple losses, concurrent
unpaced bursts, recovery through scheduled fixture end, lifetime/ABA and damaged
output/crash controls. Measure rather than assume throughput and bounded latency.
Any unvalidated context contract or native safety concern keeps retail NO-GO.
Do not prepare a deployment candidate or executable retail card unless qualification
supports one. No deployment, save operation or game process action is authorized.

The alternatives are diagnostic repair in the existing architecture, a bounded
no-repair result if essential semantics cannot be grounded, or a separately
authorized future live discriminator. Replacing the architecture cannot recover
the missing historical operands. Only the first two routes are authorized here.
Original captures and accepted D5H/D5I conditional-mask findings remain unchanged.

## Decisions during qualification

Independent context inspection identified an omitted current/retained Grid
distinction and a conflated observer/native extent predicate. The repair now
records W+`0x100`, rejects Grid disagreement, and gives the 256-member coverage
bound its own reason. Neither is promoted to the historical initiating cause.

Engineering review then questioned the generator's fifth argument, inherited
under the name `grid`. Before changing that production alias, existing native
evidence was checked: provider `0x14079fb16` calls `FUN_14078ee90`, saves the
result in R15 at `0x14079fb1b`, and forwards it at `0x14079ff03`. The complete
getter in `.local-work/recon/exact-beacon-08.tsv` resolves a form and checks
type byte `+0x2e` against `0xa0`; generator `0x14079b625` reads the argument's
member `+0x28`. It is not the retained Grid. The operand was renamed `definition`
without inventing a Grid equality predicate. Disposable originals ignore that
argument, so their coverage is ABI forwarding rather than definition semantics.

The first revised build passed its initial oracles. Build02's recovery oracle
failed because the fixture requested a new construction but omitted the next
reuse call. That failed control is retained; the fixture now performs both.
Review also requires a loss inside an actual invocation, late output failures
after an acknowledged prefix, and explicit unqualified labels on recovered
orphan/unacknowledged records. These are in-scope qualification corrections,
not amendments to R1-AC1–R1-AC9.
