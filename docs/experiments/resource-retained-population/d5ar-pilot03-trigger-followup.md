# D5AR Pilot03 trigger follow-up

2026-11-05, Australia/Sydney. The controlling question is whether an ordinary
post-arrival command can attempt a protected resident census without depending
on a particular Build Mode transition. The trigger design and lock primitive
control are complete at their stated offline scope. An integrated replacement
instrument and retail trigger qualification remain INCOMPLETE.

## What Pilot03 established

Pilot03 authenticated startup, accepted one command, and published a finalized
`REFUSED` record with `copy_status=OPERATOR_STOP` for the same process, session
and capture UUID. The operator reported one ordinary Build Mode entry and exit
without edits between arm and STOP. The folder check before STOP found only
the three startup receipts. The final record has no selection observations,
owner binding, copy times or source rows. The protected postflight passed.
These observations establish a missing capture, successful cancellation and
working finalization for that refusal. They do not identify a particular
executed native branch. Local evidence is pinned in
`Pilot03-operator-evidence01.zip`, SHA-256
`8833f02f6ff13dea4bc38f1201ecf91228a203996818a6062d8ef396d0f7f28a`.

The command waits for `WorkshopEngine::StateUpdatePlacement` at preferred
static VA `0x1421b2570` to enter after arm, with zero at operation `+0x630`.
It then requires the original resolver release witness and the area call
returning to `0x1421b26c1`. The area consumer must reach the occupied-holder
callback at `0x1421e0f50`. The UI opening alone does not establish any of these
events. Native evidence maps additional area callers in a preview update
and a reference transition. Pilot03 deliberately ignores these as capture
triggers. A cached skip or empty map **within an admitted returning scope**
normally yields a refusal. Exact DLL modes 6 and 30 demonstrate these two
completion paths. This makes a missing eligible scope the leading explanation
for the silence before STOP, while leaving the exact transition unresolved.
A STOP arriving during completion can supersede another disposition, so the
terminal label alone does not prove every intermediate branch was absent.
[Operation and caller evidence](d5ar-identity-investigation.md#ordinary-established-operation-trigger-scope) · [All three area callers](../native-availability-map/functions.csv)

The earlier D5AK A0 and D5AL B0 trials used a broader observer at the native
area shared-reader acquisition. I rehashed their original `geometry-1.bin`
files against the pinned A0 and B0 evidence and decoded the header. Each
reports the area boundary, reader word 1, 36 holders, 102 resource slots,
2,984 regions and 7,372 points. The archived consumer operand was R14, which
the updater loads from RCX, its context pointer. It cannot establish which
caller reached the updater. These earlier successes support a natural reader
window on that route. They cannot show that Pilot03 saw it or that broadening
the caller filter would reliably trigger every pilot. The broader observer
also cannot independently attach the old selected-reference certificate to a
preview or transition scope. [A0 report](d5ak-a-report.md) · [B0 report](d5al-b-report.md) · [Owned area bridge](../../../runtime/construction-winner/d5ai_bridge.asm)

## Proposed trigger for the next technical pilot

Use one post-arrival `SORSnapshot` command to request a **single immediate
attempt by the existing worker**. Remove the Build Mode action from this
technical pilot. On invocation, keep the existing command-ingress exclusion,
unique request identity and STOP handling. The console handler initiates the
request. The worker acquires protection and owns the result. Every admitted
request should get one terminal status when output remains available. Record
an explicit `NATIVE_READER_BUSY`, no-current-binding or no-resident-data result
as applicable. Use no polling of native memory and no automatic retries.

1. The worker tries the existing observer lifetime gate first. It requires no
   active lifecycle phase and validates the ordinary protected manager binding
   before addressing its ProcGen lock. Confirm the owner and attached ProcGen
   under the lease. Refuse an invalid, unaligned or unavailable lock operand.
2. On this pinned build, the native reader takes one count at ProcGen `+0x44`
   with `lock xadd`. Its slow path waits and can admit an exclusive owner
   recursively. A worker must avoid both cases. One atomic compare-exchange
   from `0` to `1` gives the same count as the original idle fast path. It
   refuses an existing reader, a queued writer, exclusive ownership and a race
   that changes the word before the exchange. This synchronization step
   writes the lock counter and may delay a writer during the copy.
3. Recheck current binding before traversal. Copy represented geometry with the
   existing measured-capacity copier, source-ending checks and per-read STOP.
   Keep current owner, source and map identities separate. This worker has no
   selected-reference lease or physical area witness. Label outpost identity
   and area association `UNKNOWN`. A complete empty resident map, absent owner,
   and failure to take protection require separate dispositions.
4. Release the native reader exactly once in `finally`, then release the
   observer lease, then finalize owned output. The original area release at
   `0x1421e0a82..0x1421e0aa4` decrements the reader and wakes one queued writer
   when the released count is the last reader. `0x1402c45a0` is an exclusive
   release helper and must not substitute for this reader release. Preserve
   the production diagnostics for release and writer failure. An unproven
   process exit or absent output must not be inferred as successful release.

This design keeps the established lifecycle and source-ending requirements. It
avoids the extra native callbacks that were used only to await the old area
trigger. Whether those hooks can be removed from a specific build requires
integration review. The old native-reader route remains a fallback design
for observations that specifically require a natural area evaluation or a
selected-reference lease. Arming before travel would change the capture time
and could consume an earlier owner. It would not validate a post-arrival census.

## Executed qualification and handoff

The [owned control](../../../research/resource-retained-population/d5ar_trigger_controls.py)
executes the pinned original native reader, writer, shared release excerpt and
exclusive release in a disposable process. The harness supplies call shadow
space and a return at the shared-release boundary, maps original imports to
the installed Windows wait/wake functions, and records the wake call. It
reads only the pinned EXE and writes a fresh ignored receipt. This adapts the
project's owned D5AR range mapping and source-retirement controls under
SOR-P-0002. No outside implementation is incorporated.

Eleven cases pass. The candidate and original reader agree on the idle count.
Eight nonidle states refuse with byte-equal lock words. The original reader can
join the candidate reader, and a real original writer entering after the CAS
queues behind it, wakes on the original release and returns the lock to zero.
The first attempt failed before executing lock instructions because the owned
reservation used an address outside a Windows allocation boundary. The revised
fixture reserves the containing 64 KiB blocks. Both receipts are retained.
The passing local receipt `trigger-lock02.json` has SHA-256
`ea7885bb898a9c14756f98827eb00a22e3722103c85d71961e1c1396aa9b1350`.

Before a new pilot package can be reviewed, integrate and challenge the detached
worker's owner-lifetime and current-binding path. Exercise real adverse
replacement, lock contention, empty/absent state, STOP and C++/SEH release paths,
and the decoder's full success and refusal records. Independently verify the
exact build, then use the one-load/direct-arrival route with one command and no
Build Mode action. Check the fresh `COMMAND_READY`, match the single terminal
file to the armed UUID, and perform protected exit, disablement and postflight.
This pilot would qualify the technical resident census only. Outpost attribution
and effective-input eligibility for the 30-sample series remain open.

## Pilot04 implementation and offline acceptance scope

The [0.2.0 worker](../../../runtime/outpost-geometry-snapshot/README.md) uses a
single command generation, the existing lifecycle gate and the zero-only
native reader claim. It revalidates the binding before and after copying.
Native release runs before observer release and publication. A separate
Windows timer polls STOP and the drive floors. Its callbacks are drained
before the worker decides whether to publish. The worker retains both source
ending CALLs and the five lifetime entries. The area, placement and selected
reference sites remain only in historical controls or source records. The
reader wake and timer drain use documented Windows APIs. [WakeByAddressSingle](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-wakebyaddresssingle)
· [WaitForThreadpoolTimerCallbacks](https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-waitforthreadpooltimercallbacks)

Modes 62–76 cover success, queued writer, missing owner and attachment, empty
map, changed binding, active lifecycle phase, C++ and private SEH faults,
STOP with both leases active, same-address reuse, inaccessible lock memory,
malformed geometry, overlapping commands and the seven-site patch/guard,
sidecar and receipt path. Mode 76 patches a disposable image with the pinned
original span bytes and drives the registered command against owned objects.
Those local preimages are excluded from the review and Vortex ZIPs. The
independent raw decoder checks the exact bytes of copied geometry and the
shape of refusal evidence. The fixtures do not exercise the retail SFSE
loader or provide scientific proof of a live outpost association.

| Dependency | Evidence and disposition |
| --- | --- |
| Worker admission, cleanup and publication | Exact DLL controls and independent raw decoder. The first mode 76 fixture misread the rollback flag on successful installation and refused before publication. The original receipts remain local. |
| Native lock interoperation | Eleven original-instruction controls repeated in `trigger-lock03.json`, SHA-256 `39ea60b0659ef728f2b2da5da43717a414feebbcc516d5898c54695fb861ffbd`. |
| Exact package and local target | Two clean build receipts and Vortex packaging receipt under `.local-work/d5ar`. The package carries the exact tested DLL and notices. |
| Retail one-shot capture | **INCOMPLETE** pending a separately approved run under the [Pilot04 card](run-card-d5ar-pilot04-proposal.md). The exact DLL test uses a disposable host, owned objects and synthetic startup evidence. |
| Original comparison and study eligibility | **INCOMPLETE**. No selected-reference lease, physical area attribution or effective-input equivalence follows from the new trigger. |

Offline implementation and verification are submitted for review. Exact artifact
reproduction and independent decoding are separate from independent substantive
acceptance and retail authorization.

## Pilot04 review corrections

The first independent review returned REWORK on the original 0.2.0 ZIP.
The replacement keeps the DLL version and raw encoding and uses a separate
private package directory and source lock. Startup now hashes the exact bytes
used to parse the sidecar and retains its later file checks. The operator
compares the ARMED output path with the package receipt. The console help
describes a single worker attempt.

The copy timer stops after releasing both leases. The writer then checks STOP
around serialization, during output and readback, and immediately before
rename. A STOP refusal established during copying can still publish. A STOP
observed during publication leaves any partial for diagnosis. A later STOP
can race rename. The operator records any interrupted attempt as incomplete.
Publication checks available output space against the floor and remaining
encoded bytes. This is a point-in-time check. Serialization memory and
concurrent external disk use remain separate limits.

Mode 77 executes the pinned original writer and exclusive release on an
owned lock. It observes the original writer waiting with word `0x1001` behind
the compiled DLL reader, then requires acquisition after the DLL's release
and return to zero. The local original bytes are excluded from both ZIPs.
Mode 78 inserts STOP after the writer has produced and verified the partial
and before rename, with both copy leases already released. Mode 79 exercises
the access-violation filter with an injected exception. Mode 80 decodes an
empty holder and establishes why a finalized copy alone cannot pass the
operator card. The pinned raw decoder reports validated geometry entries,
regions and points and the process, session and build identities. A zero
point result does not qualify as a technical capture.
