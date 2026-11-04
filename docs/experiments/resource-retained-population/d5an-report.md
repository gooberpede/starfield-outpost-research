# D5AN counter-admission investigation and repair

2026-11-04, Australia/Sydney. **COMPLETE / ACCEPT at the authorized offline scope.** No deployment or new gameplay authority is claimed.

| Element | Best-supported answer and scope |
| --- | --- |
| Original question | [D5AN-CQ and Q1–Q4](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AN_counter_admission_failure_investigation_repair.md): attribute the N1 counter fault, test its mechanism, repair safely and qualify the actual integrated candidate. |
| Historical answer | N1's nine originals authenticate READY followed by aggregate scheduler bit-2 refusal before ownership/HEALTHY_ACK and Save52 loading. The exact counter/site/thread/interleaving was not stored and remains UNKNOWN. |
| New mechanism evidence | The old 32-attempt algorithm can reject legitimate competing admissions at an active count of only 32. A rigorously explained shared-state fixture reproduces that behavior; the actual repaired integrated Producer survives forty controlled interferences. This is not N1 replay. |
| Repair direction | Strong saturating CAS with scheduling backoff, checked nonwrapping teardown, source-specific fixed fault provenance and truthful worker failure aggregation. Overflow, actual queue loss and safety/site guards remain protective failures. |
| Confidence | PROVEN / STATIC for original native fault paths and the scoped deterministic algorithm counterexample; authenticated RUNTIME bytes for N1's recorded outcome; no claim of its unique initiating cause. Exact-final engineering tests below pass; independent substantive and editorial acceptance is recorded. |
| Coverage | Owned integrated C++/assembly, native shared targets, startup/STOP, adverse diagnostics and operational fixtures. Retail reliability, latency bounds, winner distribution and universal liveness are not established. |
| Scientific state | N1 acquisition FAILED; PRED-02 INCONCLUSIVE; GC-10/D5R OPEN. No new prediction or eligible trial exists. |

## Original questions and current disposition

| ID | Status | Answer and remaining work |
| --- | --- | --- |
| Q1 attribution | COMPLETE | [Census](d5an-counter-census.md) maps original C++/ASM and worker aggregation to actual compiled code, independently authenticates N1 and preserves its unobservable origin. |
| Q2 mechanism | COMPLETE | Exact integrated interference, overflow, partial admission, recursion, queue loss, publication and startup/STOP controls pass. Counterexamples and conditional progress limits remain explicit. |
| Q3 correction | COMPLETE | New source, actual integrated binary, checked decrements, precise versioned diagnostics/readers and truthful late-STOP failure accounting pass positive/adverse tests. |
| Q4 readiness | COMPLETE | Final09, exact ABI/scheduler objects, replay, byte-identical reproduction, named package and 173-control owned operational pipeline pass. The source-locked future proposal remains NOT AUTHORIZED. |

No mandatory question is narrowed to a completed document or isolated helper.
The [active ledger](d5an-investigation-ledger.md) preserves tested branches,
failures, counterexamples and next actions. The original nine criteria remain
unchanged. Historical inability to name the exact N1 producer is not fabricated
away and does not itself prohibit the brief's explicitly bounded offline closure.

## Historical authentication and causal timeline

`evidence01.json` independently checks all nine original N1 hashes, matching
READY/terminal identity, the single 328-byte core frame, its kind-13 sequence-1
payload/CRC and flushed-prefix CRC, plus three identity-bound 96-byte header-only
sidecars. No ownership, request, arm or STOP artifact exists. Original DLL
`1596f2cffff18dd91bd18fb755076fb8740c757241cb7c81c33ffa3a3d672754`
matches the retained producer. The N1 terminal SHA-256 remains
`972e6f78820e3ec25b17ea77c113895e84c3c46a71bb9ff43e2e92451cecf99c`.

The worker initially passes its guards and publishes external READY. Scheduler
bit 2 is present by the failed terminal and independently suffices to refuse its
counter guard. Its exact onset may fall between the initial guard check and
READY publication, or later; it was not timestamped. The combined guard reason
does not rule out a simultaneous byte/relay failure or identify which short-circuit
guard first returned false. The worker retires before controller ownership.
This is the supported ordering, not a particular thread schedule. Zero reported
drops/activity do not prove no attempted work:
the admission/diagnostic increment can itself fail before event accounting.

The exact N1 explanation is therefore **aggregate bounded-counter refusal with
unrecorded origin**. The new scoped design finding is **a finite attempt quota
that can turn genuine benign interference into an experiment-ending failure**.
These are distinct statements. No memory corruption, spurious hardware CAS,
geometry regression or specific native caller is asserted as N1's actual cause.

## Repair and source-specific diagnostic design

New `d5an_*` native sources derive from the owned 0.9.1 sources and retained
0.7.0 build scaffold, with [immediate lineage](d5an-reading-provenance.md).
Original files, old binaries, failed packages, prediction freezes and sealed
evidence roots remain unchanged. The [census](d5an-counter-census.md) describes
counter identities, all producer families, guard/worker edges and address domains.

The shared noinline increment helper uses strong CAS and refuses MAX without
wrapping. A genuine comparison failure yields with Sleep(1) rather than setting
a retry-exhaustion bit. Checked leave refuses zero without wrapping and releases
other independently held counts even if one is corrupt. Partial constructor and
assembly rollback paths retain exact acquired-counter ownership.

Fault records use fixed atomics: schema, source bitmap, counter ID, producer,
fault class, observed value, thread, enabled sample, object VA and producer return
VA. Metadata binds the observer DLL base and exact helper RVAs. Direct serial/
written failures use a noinline diagnostic boundary, avoiding dependence on a
future compiler's inline return-address domain. The worker emits diagnostics;
the new counter/diagnostic helpers allocate no memory, perform no disk I/O and
read no target memory. Existing capture paths still copy their approved fields.

Fields/bitmap and the originating aggregate publish before completed state 2.
A paused first claimant plus a competing fault can still produce state 1; the
reader labels it INCOMPLETE and ignores partial first-record fields. State 2
identifies the first successful diagnostic claimant, not necessarily the first
physical fault across threads. The independent reader binds actual DLL bytes,
export RVAs/image bounds and source/producer/class/bitmap/native-mask consistency.
Retained N1 is explicitly LEGACY_NO_PROVENANCE. It cannot acquire invented IDs.

Sidecar hard failures now refuse worker health. The final quiescent failure check
also covers a producer faulting after the last pre-STOP guard and preserves any
earlier specific output/write/disk reason. A failed terminal is required; reader
leniency is not used to repair false health. Registry/identity scientific
uncertainty alone remains distinct from a hard recorder failure.

## Safety, progress and observer effects

The counter primitive has no arbitrary contention-fatal quota and uses bounded
storage. Its CAS update is lock-free; the full operation uses blocking scheduler
backoff and has conditional progress. It assumes eventual thread scheduling and
finite producer work; no per-thread latency bound or wait-free guarantee follows.
Sleep(1) requests one millisecond and can resume much later. Native helper calls
and scheduler vector-register saves add observer work. Neither a successful
fixture nor a QPC timing table proves unchanged arbitration or retail frequency.

The helper acquires no gate itself, but scheduler publication can retain an odd
registry serial while allocating tokens, and causal registration can retain its
registration flag while incrementing counters. Yielding can extend those gates,
RegistryBusy/unknown-baseline windows and STOP latency. Competing clients refuse
or record uncertainty; the helper does not wait on their gates, so no new lock
cycle is identified. Existing busy controls establish refusal, not frequency or
duration. The superseded helper comment “No lock is held across the sleep” was
limited to helper-owned locks. Its caller-gate qualification is retained here
and is explicit in the corrected source.
Some calls also lie inside an existing native reader/writer interval. Backoff
can extend native critical-section exposure as well as observer gates. No new
retail delay distribution is measured by the owned timing control.

Original finite queues and their bounded reservation work remain. Actual full
queue, reentrancy or reservation exhaustion is lost evidence and still fails
the capture truthfully. Passing counter accounting alone cannot establish full
event, task, owner or source coverage. Counter MAX/corruption injections restore
only explicitly owned fixture state to allow closeout; they are not production
recovery procedures or authority to modify a protected target.

Benign shared-target contention runs with initialized channels and enabled
capture. Before-ownership refusal is a separate startup control. Counter helpers
do not depend on controller ownership or ACK identity; those operational stages
are independently exercised. No fixture establishes actual retail startup
reliability. Resident-inert disables capture but does not mean every resident
wrapper stops executing or that a transient active snapshot remains zero forever.

## Frozen engineering identity and actual checks

The definitive snapshot is `.local-work/d5an/final09/`: all **180 expected
exits** pass, compilation succeeds and all 53 build inputs remain unchanged.
Expected private crash/refusal cases retain their nonzero expected exits; this
does not mean 180 healthy captures. Eight authored native sources, 46 derived
files, four generated inputs, actual objects/map and exact at-launch builder
bytes are retained with the [specialist handoff](../../../.local-work/d5an/native-specialist-final09.json).

| Identity | SHA-256 or actual metadata |
| --- | --- |
| DLL, actual SFSE version metadata `0x00090200` | `f1ed9cd341190a9b9bcd9672345e6d0871b6d1323a1740e3c4738ee73407ee94` — version 0.9.2 |
| [NOT AUTHORIZED ZIP](../../../.local-work/d5an/package-r1/SorConstructionWinner-0.9.2-D5AN-counter-r1-NOT-AUTHORIZED.zip) | `626672036e74918e2d6fb840d26f57af60dc29a76ba26115ba4eafda1a50a88f` |
| Native source set, canonical manifest in package receipt | `e1f94653dd28ab147b7a527ecd308ee8bc2fb6fb447be9912f9f1ff23ac7a386` |
| [N2 proposal](../../../.local-work/d5an/n2-proposal04/n2-plan-proposal.json), authority NONE | `7107991d91cf559aa5385eb955f7d69669e21190bc1f6ac7e186107f586d6280` |
| Proposal source lock, 468 exact inputs | `d5c5acb47cba95eb44d47434f680671956310dec5156cead9a390edf8d9adb48` |
| [Proposed card](run-card-d5an-n2-proposal.md) | `4ae39477f70f89c9fcbd0c5b5f0c6ae9ae2f03647622a686a3ba79e334865074` |

| Exact-final check | Actual result and limit |
| --- | --- |
| `final09/build.json` | Original 157 plus 23 new expected exits PASS; all input/source checks pass. Shared counters and actual causal/scheduler assembly execute together; six original geometry/causal alias/refusal controls remain. |
| `abi-final09/qualification.json` | 3,905 assertions, 160 Windows unwind contexts and ten causal bridges PASS on the exact final object and actual new helper. |
| `scheduler-final09/qualification.json` | 113 controls PASS on the final integrated scheduler object and matching production header, including original task/native/ABI/STOP/overflow/identity controls. Generated component framing is explicitly derivative, not a retail spool. |
| `counter-final02/qualification.json` | 176 independent emitted-provenance/framing/adverse consistency controls PASS across all 23 new native cases. State-1 records remain incomplete; failed terminals never become complete captures. |
| `replay-final02/qualification.json` and nested `native-replay/qualification.json` | Six exact composition reader controls plus 111 actual native/STOP/invalid-operand and adverse identity/join replay controls PASS. One exact owned task/core join and complete 3/78/180 geometry survive; invalid native operands are retained and refused. |
| `native-final01/census.json` | Original/new objects and DLLs inspected, 1,112 selected references retained, relocation-masked code matches and address domains recorded. Unretained/inlined COMDAT bodies are not invented as live functions. |
| `package-r1/package.json` | Independent fresh build from frozen source/recipe is byte-identical; actual SFSE version, exact original/new exit roster, notices and every ZIP payload verify. |
| `operations-final04/qualification.json` | 173 controls PASS: actual owned READY/challenge/ACK, one arm/query, reconnect, minimal STOP despite broad-lock failure, normal exit, content-first timestamp/refusal checks, new readers/postflight and seal/create/every-member archive verification. All 29 payloads verify; no cleanup error. Retail admission/protection discovery and owned namespace comparison remain declared fixture seams. |
| `optimization-final03.json` | All 21 new Python modules pass 63 early `-O`, `-OO` and inherited optimization refusals with source unchanged. |

The final contention matrix uses 2, 4, 8 and 16 threads, 256 iterations each,
seed base `0xd5a00000`, real competing counter objects and original shared native
helper pages. It retires every synthetic task before storage reuse and verifies
zero registry/identity errors and balanced active/bridge counts. Per-thread
foreign lock words isolate intended native lock state; they do not measure a
retail owner-lock distribution. Its scheduler prefix has 7,746 authenticated
frames. Final healthy timing uses 640 active-hook calls in twenty drained bursts
against 1,000 unhooked owned calls: QPC frequency 10,000,000 Hz, median 26 versus
2 ticks, 95th percentile 50 ticks and maximum 297 ticks. This is an owned,
uncontended model, not a bound on Sleep(1), game performance or contested locks.

All receipts are local under `.local-work/d5an/`. Development/superseded results
are explicitly separated from final acceptance; see the [ledger](d5an-investigation-ledger.md).
Initial byte authentication passes nine N1 originals and twenty selected
protected files. The second audit rehashes all 2,704 preserved original inputs.
Exact development causal objects pass 3,905 ABI assertions/160 Windows unwind
contexts; exact superseded scheduler objects pass 113 controls. These results
cannot qualify a later changed object.

The superseded 177-case full runs each retain three exit-91 failures in
saturation, timing and causal-counter. Truthful sidecar failure caused the old
fixture to stop waiting before the final core prefix drained. Saturation/timing
also exposed genuine sidecar loss, which cannot be called healthy performance.
The derived fixture retains the workload, waits for actual final drainage and
requires positive named queue-loss evidence plus zero unrelated faults before
accepting protective overload. Healthy timing is a separate active-hook control;
disabled execution is excluded. Compile/linkage and private sole-thread fixture
installation failures remain preserved rather than weakening production guards.

Final07 also reached 180 expected exits, but it is superseded: static review
found a plain worker-written-counter test mutation and a new callback pointer
read racing the real worker's causal drain. The final written injection instead
runs under sole_thread before CreateThread, restores the exact prior value and
requires actual failed startup without READY/ACK. Both new callback slots are
atomic with one local load. A runtime pass never excused those invalid tests.

Earlier optimization/pipeline false negatives were checker wording mismatches,
not guard bypasses. The first replay wrapper correctly refused an old D5AM-only
output namespace; a separate owned D5AN replay derivative fixes routing without
editing the original. The first operational pure-refusal test failed before
host launch for different guard wording; the corrected exact proposal/pipeline
passes. Failed outputs and superseded proposals remain local and unpromoted.

All original raw/package/selected save and analysis-core preservation checks
remain separate from scientific success. The historical N0/N1 archives retain
32/35 payloads with exact original/root/member identities; no sealed root is
changed. A final preservation audit and independent exact-snapshot verification
bind the closing handoff. This is not a fresh full 98-save retail preflight.

## Future admission and remaining authority

The [proposed N2 delta](run-card-d5an-n2-proposal.md) preserves N1's finite gameplay
procedure and adds new candidate/diagnostic/source identities, five prior-process
exclusions and a separate prospective trial/forecast decision. The local proposal
has authority NONE and remains pending. It is not a new freeze or maintainer GO.
Require fresh reviewed bindings, explicit N2 approval, actual installed-candidate
verification, full protected preflight and READY followed by owned HEALTHY_ACK
before Save52 load. N1's consumed forecast cannot be recycled.

No game, deployment, debugger, original analysis-project open, protected-save or
configuration write, upstream contact, dependency download, staging, commit,
push or publication occurs. Both caller-available disk floors remain mandatory.
Raw saves, recordings, binaries, analysis files and bulk native outputs remain
LOCAL-ONLY. Authorial publication eligibility and scientific confidence remain
separate; authored findings are REVIEW-REQUIRED.

## Original acceptance matrix

| Criterion | Current result | Exact remaining gate |
| --- | --- | --- |
| AC01 | PASS | Applied-reading record, initial/continuing preservation, both disk floors, two-specialist cap and no prohibited action; final closing audit follows. |
| AC02 | PASS | Census, exact original/native linked-code inspection and nine-file N1 authentication; historical origin remains explicitly unknown. |
| AC03 | PASS | Exact final 32/40-interference witness, integrated matrix and adverse overflow/queue/startup/STOP controls; preserved alternatives and progress limits. |
| AC04 | PASS | Counter diagnostics/reader 176 controls, checked teardown and actual late-STOP failure; hard losses remain fatal. |
| AC05 | PASS | Final180, exact ABI/unwind, scheduler113, composition6/replay111 and byte reproduction. |
| AC06 | PASS | Owned operations173, archive29, source/package binding and optimization63; declared fixture seams and content-equivalent timestamp controls. |
| AC07 | PASS | Actual unique 0.9.2 ZIP, hashes/source set and minimal source-locked proposed N2 delta with authority NONE. |
| AC08 | PASS | Report/census/active ledger and scoped state preserve N0/N1, PRED-02 INCONCLUSIVE and GC-10/D5R OPEN. |
| AC09 | PASS | Independent whole-contract substantive/editorial ACCEPT of delivery01/handoff01; final status-only closure and exact exports are bound in the review record and final handoff. |

Whole-assignment offline acceptance satisfies AC01–AC09. Scientific mechanism
evidence, evidence/preservation integrity, target survival (no retail target
operated), editorial review and authorization are reported separately. No self
completion summary supplies integration or future-use approval.

The [validation record](d5an-validation.md) gives actual commands and reproduction
limits. The [independent review record](d5an-review.md) separates executed byte
checks from inspected native-suite receipts and records the final disposition.
