# D5BM admission corrections

The corrected pump and tag components are candidates for separate native
receipts. The joined host is **STOP**. Stage A remains **INCOMPLETE** and
Stage B is gated under the [frozen brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BM_Native_Completion_to_Density_Eligibility_Qualification.md).
The [previous checkpoint](continuation-2026-11-10.md) retains the old
sources, executed component receipts, faults and adverse controls.

## Standalone controls and evidence

- The controller can cancel before a worker enters the hold or while it
  is held. The condition serializes that decision with worker admission
  and preserves the disposition and return. Positive release requires
  an unlocked receiver, the same worker and state 25 at wake, peer
  return, release and worker resumption. The original wake receives a
  refusing getter at the operand called by `0x1428d972c`, upstream of
  the alternative publication at `0x1428d974a`. Separate packet
  publication, entry and return records reject repeats. The third
  marker must execute on the resumed worker.
- `normal` runs both supplied pumps without arming. `pending` uses the
  held frontier and selected original wake. `missing` deliberately
  withholds the peer packet and verifies empty queues and eligible
  non-held workers at the semaphore boundary before cancellation.
  `fault` injects a controller exception at the hold and checks
  cancellation, return, shutdown and restoration. Published-peer
  progress is measured by the selected packet lifecycle and the
  eligible workers. A nonempty queue and a worker about to wake do
  not constitute proof of lost work. Persistent unclassified lack of
  progress requires a documented supervisor decision. Neither loop
  imposes an elapsed-time cutoff.
- Controller failures first cancel any hold, drain work and join all
  owned workers before CALL restoration or page release. The
  callback STOP, partial-startup and unsafe-cleanup routes fail the
  disposable child. The supervisor records a native fault or explicit
  owned-child stop and performs postflight. None of the four pump cases
  establish original JobSite construction, native pump publication,
  rectangle completion or layer preparation. Both sites, command
  segments, marker packets, publisher and pulse are supplied.
- The BIOM hash table spans `0x144d58000` and `0x144d59000`. The
  candidate checks all 256 words. The pinned PE names VCRUNTIME140
  `memmove` at thunk `0x14366317e`, slot `0x143a3fcc0`. The
  replacement is the same overlap-safe operation from the pinned
  system UCRT. It is a fixture import. First GNAM-owner creation reads
  scalar bits `0x3f800000` at `0x144f044e8`, verified on its own page.
  The sized delete thunk at `0x14365cdb0` is preserved. The object
  release binding is at its jump target `0x1422c7560`, outside the
  adjacent array-destruction entry `0x14365cdb8`.
- For BIOM `0x00145440`, the ESM parser requires four ordered FNAM
  groups with enabling BNAM values and full 0x54-byte GNAM rows.
  The native loader uses the BNAM nonzero flag at `0x1409e07c5` and
  checks it again at `0x1409e0d40`. All 141 selected rows take the
  ordinary ID branch in `0x1409e0cf0..0x1409e0d3a`. Their 80 distinct
  FormIDs resolve to unique source-file records, 77 PKIN and 3 LVLP.
  The exact TES4 header has record flags `0x81` and no MAST. The
  candidate supplies an ordinary full-file object with no dependencies
  and index zero, uses original master selection and FormID conversion,
  and checks the result against the authenticated source record. This
  qualifies a main-only input domain. The fixture supplies the subrecord
  reads, file object and intern strings.
- A later tag receipt must show native map initialization, lookup before
  and after publish, ordered counts 16/45/21/59, exact effective-row bytes,
  wrong-key contrast and the allocation graph. Bucket, object, array and
  intern ownership are separate. Array replacements must release the
  exact retired size. Standalone terminal disposal retires the entire
  synchronous fixture after native return. A non-null intern release
  takes STOP because native intern-cache teardown is outside that
  fixture. Joined admission requires a live map and qualified non-null
  release if reachable, plus original density enumeration of that map.

## Owned standalone route

The [supervisor](../../../research/resource-retained-population/d5bm_admit_component.ps1)
accepts one of the four pump cases or `tags` and an exclusive attempt ID.
Invoke it in a fresh PowerShell 7 process with `-NoProfile -File`.
It requires a local `D5BM standalone admission v2` record with decision
`GO`, independent reviewer identity, reviewed cases, Git HEAD/tree/index
pins, protected-inventory and CPython hashes, a `runtime` dictionary
for the installed CPython DLLs and extensions, and a `sources`
dictionary for the exact supervisor and import closure. Dictionary
keys are relative paths and values are SHA256 digests. The review
record's SHA256 is a separate argument. Review evidence is local. A
positive component admission has no effect on the joined gate.

Before a child starts, the supervisor checks the protected originals,
caller disk floor and game-process absence and copies the reviewed
sources into a new isolated directory. The child receives pinned
lawful files by read-only paths, `-I -S -B -X faulthandler` and the
single case. Its PID and a per-attempt token are recorded. For a concrete
unsafe condition, `stop.request` may contain that exact token on the
first line and the reason on the second. The supervisor can stop only
its own child. The supervisor checks caller-available disk space while
the child runs and stops on a floor failure. It waits for termination,
preserves both streams and records exit, stop reason, source and
protected-input checks. A persistent low disk reading is reported
separately from protected and source identity checks. A child that
exits during the stop request still has its exit and streams recorded.
A platform
security refusal stops the affected operation without retry or alternate
route. A review hash mismatch, unstaged-source pin mismatch, unsupported
case, protected file mismatch, running game, disk or host mismatch
refuses the attempt. The route requires read-only review before any
native use.

## Shared-host admission and ownership

One exact executable method must own a single page map, binding table,
pool generation and shutdown. Each row below needs one implementation
and qualified route or an evidenced unreachable branch. A conflicting
or unlisted live operand must refuse before the relevant original call.
Installing the existing standalone binders in sequence is prohibited.

| Native seam | Required single owner and routing | Evidence required before or at joined execution |
| --- | --- | --- |
| Arena `0x1422c7ad0` / `0x1422c7d40`, state `0x145e60398` and owner `0x145e603c0` | Shared allocator and typed lifetime ledger for pool, server, ready files and tags. Dispatch by exact caller/owner and allocation class. Release by recorded address, class, origin, size and release convention. | Show unique backing, allocation/replacement/free accounting and preflight refusal of ownership mismatches. No static `size` heuristic as sole identity. |
| Command memory `0x1422ce9f0` / `0x1422ceb20`, TLS `0x1482dfa10` | Pool owns the native block allocator/free and per-thread memory slot. Server follow-up uses the corresponding issuing context and the actual release owner, with controller TLS only for controller-owned work. | Verify transferred page and packet identity, worker membership, balanced references and refusal of foreign blocks or TLS. Retire server's single-context substitutions. |
| Wait/wake `0x143a402c8` / `0x143a402d8` | One import owner, routes by exact live word and operation. Preserve pool synchronization and native wait semantics. Register each constructed JobSite word and each authenticated pending/ready file word with a bounded lifetime. | Show that the matching wait is satisfied by the same object's wake. Refuse foreign/stale address or wrong operation. Neither server's single wake nor the two-site marker callback can service ready files. |
| Decode and vectors `0x1402ba260` / `0x1402ba340` and intern release `0x1428caea0` | One typed route for the 1,960,000-byte file decoder and actual GNAM vector allocations. Pair by identity and convention. Intern owner accounts for holders, live map references, and non-null terminal release where reachable. | Positive size, caller and owner discrimination and negative cross-release. Live C1 tags and original enumeration must remain available through density claim. |
| Object allocation `0x1422c7320`, object release `0x1422c7560` and native array destroy `0x14365cdb8` | Account for the pool and tag object origins under one release owner. Preserve the separate array-destroy binding and its stride/count/destructor contract. Preserve the sized delete thunk at `0x14365cdb0`. | Confirm distinct typed routes for the original object and array callers, independent of coincidental size or adjacency. |
| Copy import `0x14366317e` / `0x143a3fcc0` | One overlap-safe `memmove` owner for tag and file consumers with the exact import and replacement pins. | Verify both caller families and their live source and destination bounds. |
| Reservation `0x1422cdf60`, commit, wake and constructors | Exact owner of the original receiver-bound command segments, native reservation/commit and getter-bound ProcGen and ContentManager construction. Shared worker generation owns both sites. | Distinguish the actual rectangle packet from the target page, the layer commands, and supplied markers. Trace queue visibility, generation, servicing worker and reuse/teardown. |
| Source/owner globals and frontiers | Assign one owner per global or import, including `0x145fd9c38`, `0x1461e1d78`, `0x1461e1db0`, `0x1461e1dc0`, `0x1461fabe8`. Supply coherent C1 source, descriptor and generation state and record read/write effects before binding. | Reject wrong owner, generation, coordinates, file, BIOM or mode. Verify native graph objects and their lifetimes. Review complete import and global closure before run. |

Admission requires the matching 1,600 genuine rectangle placement
operations or a source-and-effect-qualified equivalent, including any
earlier target demand. It then requires the original matching receiver
to consume the completion and remove its node/key and release the
reader, the separate category-zero page to release the coordinate
edge, genuine coordinate dispatch, and actual application of the
layer AddDependency and Commit. Track the tag-1 handle and provider
frontier while a ready-file density job is published and claimed on
the same started pool. Compare against ordinary layer progress,
held or stale completion, held follow-up, wrong or absent file,
and genuine file pending with its later readiness transition.

The C1 root's eight keys cover the neighbor sets of 4/8/4/4. Establish
pending at the selected key's first acquisition, including placement,
then follow the same file handle and dependency through the transition.
An empty collection and a state-2 node are separate observations.
Without the executable method, matched receipts, adverse controls and
independent review, Q1–Q4 remain incomplete. The prior standalone
receipts keep their original qualifications.
