# D5M debugger repair and Phase A qualification

2026-10-28, Australia/Sydney. [Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5M_debugger_reliability_repair.md),
[historical failure](phase-b-postmortem.md), [proposed versioned card](run-card-d5m-v1.md),
[local source and receipt pins](debugger-repair-sources.csv).

**Phase A qualification passed with independent engineering and scientific acceptance. Phase B remains NOT AUTHORIZED.**
The confirmed borrowed-handle defect is repaired. The existing dump narrows the
fault state to an armed Grid-clear breakpoint, but does not establish the
historical initiating cause. The exact engineering and scientific review returns
are retained below; an implementer assessment is not acceptance.

## Historical failure and new dump observation

The complete D5L journal includes exits of TIDs 21752 and 22888, lifetimes 93
and 89, at lines 95–96 before native sample 1. There are no further thread exits
between samples 1 and 492. The old controller closed borrowed event handles on
both early exits. This is a confirmed ownership defect, not proof that either
close caused the subsequent Grid-clear failure. The original captures,
post-mortem, superseded review and correction remain unchanged.

An existing `Starfield.exe.8352.dmp` was read without a debugger or symbol
download. Its SHA-256 is
`1de425e1c61671863b6360cc12e37d61d2f70d955b90506d9d26841b7bf6649d`.
The dump's valid process fields identify PID 8352 and creation Unix second
1793144211, matching the captured creation FILETIME `134376178118454456`
truncated to seconds. Its Starfield module base matches `0x7ff620be0000`.
The qualified exception stream gives thread 9144, exception `0x80000003`,
address and RIP `0x7ff6215629b0` (module RVA `0x9829b0`), EFLAGS `0x200`
and TF clear. The captured bytes start with `0xcc` at the armed Grid-clear site.
Other recorded thread suspend counts are retained in the local receipt.
The module's version is 1.16.244.0; image size 144,449,536 bytes and PE timestamp
1780354072 match the pinned installed executable. Faulting TID 9144 is lifetime 1
in the original barrier. The dump timestamp is 2026-10-27 23:42:58 UTC, consistent
with the preserved Windows fault record. These are identity checks, not a
continuation history.

The dump is readable by the sandbox through an explicit read/execute ACL;
its owner is the ordinary user. The matching WER archive directory is visible,
but opening `Report.wer` under the sandbox was denied. Existing preserved Windows
event records supply that report's prior correlation. No permission, ACL or
security setting was changed, and no fresh retail dump was created.

The new observation confirms the faulting instruction state. It does not encode
the debugger's last disposition, a continuation return, an in-flight rearm owner
or the exception's first/second-chance delivery history. A dump RIP at the fault
address is not the earlier debugger-event RIP. No historical root cause is claimed.

| Explanation | Status and discriminating prediction |
|---|---|
| Borrowed-handle closure invalidated an aliased/reused handle | Confirmed defective ownership; causal contribution UNKNOWN. A causal trace would need the numeric handles, lifetimes and close results missing from D5L. |
| An owned breakpoint was continued as unhandled | Consistent with the final breakpoint exception; not established. The repaired journal records chance, exact address, chosen disposition and actual continuation result. |
| Queued trap handling or rearm lost site/thread ownership | Plausible, not established. It predicts a mismatch among queued site, RIP, step owner or code readback; new diagnostics and concurrent fixtures cover these transitions. |
| A continuation or peer-control API failed | UNKNOWN historically. The old evidence lacks per-event return/error records; deliberate real API failures now require fail-closed disposal and durable diagnostics. |
| Foreign control state, an unrelated trap or target exception intervened | Not excluded historically. New checks distinguish the system attach trap, owned probes, foreign first/last-chance traps and exceptions during rearm. |

[Microsoft debugging events](https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events),
[ContinueDebugEvent](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent)
and [exception handling](https://learn.microsoft.com/en-us/windows/win32/debug/debugger-exception-handling)
provide the API semantics. The dump reader uses the installed Windows SDK
minidump layouts and the documented
[process identity/time flags](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_misc_info).
No Microsoft example implementation was copied.

## Ownership, admission and event control

| Handle or alias | Origin and closure owner |
|---|---|
| CREATE event process/thread handles | Borrowed from Windows; never closed by this observer. |
| Retained thread handles | Explicit checked `DuplicateHandle`; registered as owned before fallible diagnostics. Maps retain separate TID, creation time and monotonic lifetime. One checked close at EXIT or final/failure cleanup. Dead peers remain registered until their EXIT event. |
| `pi.hProcess` | Independently created fixture handle or opened retail query/read/termination handle. Used for admission and disposal; its owner is cleared after successful closure. |
| `process` | Independently owned duplicate of the full-access CREATE process-event handle, with explicit process origin and PID check. Used for memory operations and closed once through the registry after exit/drain. The borrowed origin is never closed. |
| `pi.hThread` | Independently returned by fixture creation; distinct from the debug-event duplicate and closed once during cleanup. Retail never fabricates this handle. |
| CREATE/LOAD image file handles | Debugger-owned under Windows' documented rule. Adopted before event processing, checked close on normal/terminal/drain paths, or discovered by failure cleanup. |
| Token and fixture synchronization handles | Temporary independently opened/created handles with checked normal closure and failure cleanup. No token privileges are changed. |
| Fixture-only created peer handle | Independent `CreateRemoteThread` result; checked closure, or explicit ownership registration for the controlled exit fixture. This injection is excluded from retail compilation. |

Successful ownership transitions precede logging that can throw. A diagnostic
failure after duplication therefore cannot orphan the handle; a failure after
closure cannot leave a closed handle in the registry. A numeric handle or reused
TID is not a lifetime identity. A duplicate CREATE for a live TID or EXIT for an
unknown lifetime fails closed.
Plain process/thread/gate owners are also cleared immediately after successful
closure, before final logging can fail. A separate post-close diagnostic-failure
fixture requires zero remaining owners and exactly one close per origin, while
preserving a scientific chain completed before the deliberate controller error.

Before consuming a live admission, Python queries real caller/target token SIDs,
account names, elevation and Windows sessions. It refuses sandbox accounts,
different accounts/sessions and elevated contexts. The native controller repeats
the ordinary-user check before attachment. A pre-attachment identity refusal never authorizes
retail disposal. The one-use sidecar, image/path hash, process creation time,
stopped-process recheck, original instruction guards and Cloud/save protections
remain required. The new preparation requires every named D5M case for the exact
build, rather than accepting an arbitrary passing subset of the old matrix.

Initial arming accepts only a first-chance breakpoint at the verified system
ntdll `DbgBreakPoint` export on a thread starting at `DbgUiRemoteBreakin`.
The remote DLL's file identity must match the current local system DLL before
export offsets are transferred. This is a qualified Windows-specific admission
rule; an unsupported origin refuses arming rather than swallowing a target trap.

The versioned card also resolves the known launch-only Plugins.txt timestamp
condition. A separately pinned metadata helper verifies unchanged size/hash and
all other guards, retains the original receipt/chronology and prepares one
review-required derivative. Independent review of its exact delta is mandatory
before admission; no automatic retry or new authority follows. Ten synthetic
controls exercise its narrow transformation and refusal rules. No real launch
or launch-derived receipt was created during Phase A. This is separate offline
orchestration, not a change to the qualified native executable or a game
configuration write.

`control.jsonl` is separate from samples and SRO1 evidence. The controller owns
its exclusive creation and records event sequence, process creation time, TID and
lifetime, exception address/code/chance, site, original/current bytes, RIP/TF,
step owner, peer suspend/resume counts, handle results and terminal state.
Transitions while the debug event is stopped are buffered within a 1 MiB
integrity bound. The full batch and chosen disposition are flushed before each
continuation; its actual return and error are separately flushed afterward.
Fatal/end records flush pending diagnostics too. A diagnostic failure stops the
observer; it does not fabricate a scientific sample or erase a prior receipt.

All fourteen probes remain permanent, including Grid-clear. An owned trap must
match address, first-chance status, RIP and current expected instruction byte.
Only observer-owned control/debug groups are written. Queued peer traps remain
fenced, rewind and retrap after the owner step rearms the site. TF clearing has
an immediate context readback. Foreign first-chance traps outside rearm pass to
the target's handler; unhandled last-chance traps remain exceptional exits.
Unowned exceptions during an open rearm window fail closed. There is no
exception-suppression or safe-detach claim.

## Qualification and preserved counterexamples

The Phase A execution envelope uses only hash-bound, project-authored disposable
targets and the installed Windows/MSVC/Python tools. Outputs are fresh local
builds, control journals, SRO1/ACK receipts, reductions and verification records.
Allowed interventions are attachment to those fixtures, fourteen software
breakpoints, bounded memory reads, owned control/debug-register writes and peer
suspension/resumption. Focused fixtures additionally create/terminate a synthetic
peer, temporarily hold the step owner, signal a duplicated fixture event and
use `DBG_REPLY_LATER` to replay a genuine pending trap. Those extra controls are
excluded from retail compilation. None supplies game execution authority.

The risks are intentional fixture termination, modified scheduling and declared
coverage loss on unsafe state. Stop on identity/guard/ownership, receipt, worker,
pipe or disk failure, explicit STOP, or the fixture's natural endpoint. The
observer disposes only its admitted disposable target and drains debug events;
target absence is checked independently. Preserve decisive failures and final
receipts. Both 40,000,000,000-byte disk floors apply. Fixed fixture input loops
and bounded teardown recovery are not healthy-session or scientific-event
cutoffs. Protected saves, installed content and analysis state are not fixture
inputs and receive no writes.

The final native build and qualification identities are listed in the source
ledger. Reproduction uses installed Python/MSVC/MASM and the existing owned
build/transport/reader/reducer, with no downloads. Read each script's I/O and
target-effect header before running it. Run fixture qualification from an
ordinary unelevated user context; no retail controller command appears here.

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B research/resource-retained-population/build_native.py fresh-d5m-build
& $py -B research/resource-retained-population/qualify_native.py .local-work/resource-retained-population/fresh-d5m-build .local-work/resource-retained-population/fresh-d5m-qualification
& $py -B research/resource-retained-population/qualify_pump.py .local-work/resource-retained-population/fresh-d5m-build .local-work/resource-retained-population/fresh-d5m-pump
```

The scientific positive fixture executes an actual miss, original query/direct
mask, successful region append and copied points, final source-slot ownership
and later same-wrapper/collection/region hit. It uses original synthetic memory
and instructions, not Bethesda's generation algorithm. Failed generation,
unequal copy, visited bypass, incomplete coverage, pointer reuse/reset, nested
calls, unrelated sources and contrary geometry remain distinct. First observed
construction is not first-ever history or an intended full-resource census.

The real debugger matrix retains the 27 inherited native cases and adds early
post-arm exits, actual TID/handle reuse, concurrent same-thread/peer Grid-clear
and SourceInit traffic, same/different-site queued traps, thread exit during
rearm, deliberate continuation/duplicate/close/readback failures, diagnostic
transition failures and foreign first/last-chance breakpoints. The separate pump
tests cover collector loss, broken pipe and STOP. Replay/adversarial tests are
supplementary; they do not substitute for those real processes.

The original build12 stress profile completed its traffic and scientific chain
but observed no parked traps, and its explicit queue-coverage assertions failed.
A same-build repeat also lacked those paths. Both failed-coverage results remain
unchanged. The final profile keeps the traffic stress test and requires two
additional focused cases: a real trapped thread is suspended and deferred with
`DBG_REPLY_LATER`; another thread opens rearm; the first exception is replayed
while that owner is held. The shared queue handler must park, rewind and retrap
it at the same site or a different site, respectively. Both focused final-build
cases passed. Moving this coverage into dedicated required cases changes the
fixture method, not AC5 or the retail observer mechanism.

Development failures remain local. The first dump parser rejected repeated empty
directory entries; it now skips only zero-sized unused streams. An attempted test
before its build receipt existed was refused. A qualification attempted after
source changes was refused by the existing exact source pins. These are harness
diagnostics, not scientific results.

The first forced peer-exit fixture terminated a thread before CREATE processing;
the observer encountered suspend access denial and correctly failed closed.
That did not exercise EXIT during rearm. A subsequent suspended-start fixture
delivered CREATE after the owner step and exposed a stale fixture-only TID key.
The corrected fixture holds the step owner, fences the new real thread, requests
its termination, observes EXIT during the open rearm window, retires the test
identity and releases the owner. The failed runs are preserved. Superseded
development matrices were intentionally retired after material source changes;
their partial outputs are not passing final qualification or bounded non-hits.

The first complete build08 matrix passed 38 of 39 cases. Its close-error fixture
used `INVALID_HANDLE_VALUE`, which this Windows environment accepted as a
pseudo-handle close; the expected error and abort never occurred. That FAIL is
preserved. The corrected fixture passes a null handle, records the actual close
error and retains the real owned handle for cleanup. The focused corrected test
passes. The entire matrix is requalified against the corrected build; an earlier
passing case is not relabelled as final-build execution.

The final runner uses three bounded independent batches of the existing native
qualifier. Every mode still runs in its own real process. After completion it
preserves the original batches and verifies each file in the aggregate copy
against its original bytes. Receipt metadata retains original batch paths. This
is lossless packaging of disposable evidence, not an alteration of a capture.

Manual audit also corrected a candidate-specific access-rights regression:
reusing the retail pre-admission handle for memory operations would omit write
and page-protection rights, although fixture creation supplied broader rights.
The final observer instead duplicates the debug-event process handle and checks
its PID. The same owned duplicate performs memory operations in fixture and
retail builds. Every final case checks its explicit origin. This repair was
statically reviewed and qualified offline; no retail failure was induced to
discover it.

The continuation-error fixture deliberately submits invalid API status 0 while
retaining the handler's recorded disposition. Windows rejects that call; the
pending event remains owned until disposal/drain. This injected API rejection is
distinct from actually continuing a breakpoint as unhandled.

### Final exact-build results

The final manifest is `.local-work/resource-retained-population/d5m-build13/build.json`,
SHA-256 `6b82b0c27d860af0e130d3100a4c484183f061f0b266f7885eff0af72f9c91ea`.
All 51 manifest pins match their current files. The native retail controller is
`3f41cbcd49ffdbf268fc7148c53c86a6a9f158d1ffd26e3f1bceaae0fac157cc`;
the fixture controller is
`ab5e8bbc8c24e1f30d5c31f89520ef8255c145fa00856e6c1dbd212316323ce2`;
the fixture target is
`b6dd11c3e82c4084927773ef10b8b06269a68084b2d67b3a428235c93245a3fb`.
The standalone metadata helper was added after this build and is separately
pinned and qualified; it is not a native observer input.

| Check | Actual result and boundary |
|---|---|
| `d5m-qualification-final07/results.json` | All 42 real Windows cases PASS. Required adverse cases include deliberate target/controller failure; PASS does not mean survival or controller exit zero. |
| Receipt/control verification | Independently decoded 1,250 SRO1 receipts and ACKs, reproduced reductions, inspected 2,805 events and 51,447 control rows, paired continuation intent/result and checked zero registered/plain owners. |
| Final stress coverage | 624 receipts; 271 thread lifetimes, 223 distinct TIDs and 31 distinct duplicate-handle values; 30 same-site and 19 different-site queued traps. Real early-exit case: 261 lifetimes, 225 TIDs, 32 handle values. |
| Focused queue coverage | Both same-site and different-site cases each retain 20 receipts and 35 events, with the required queued transition observed. |
| `d5m-focused-final02` | Ordinary-user, post-close diagnostic failure and actual close-error controls all PASS on build13. |
| `d5m-pump-final05` | Normal completion, pre-arm STOP, idle collector loss and idle broken pipe all PASS; targets absent. |
| `d5m-adversarial-final05` | All 27 native actual-receipt adversarial controls PASS; replay supplements real-process qualification. |
| Additional controls | Twelve preservation unit cases, fourteen inherited invented-byte controls, ten synthetic metadata-bridge controls and nine in-memory admission controls PASS. No synthetic control creates live authority. |
| Instruction preservation | Fourteen sites, thirteen backed functions/ranges and 16,736 installed PE bytes match the pinned inputs. No game instruction was executed or patched. |
| Final protection | `d5m-offline-final02/preflight.json` and `protection-comparison.json` PASS; protected inputs, original dump, HEAD and index unchanged. C: 75,883,225,088 and D: 87,384,190,976 caller-available bytes. |

Paths in this table are under `.local-work/resource-retained-population/` except
the comparison and independent verification records under `.local-work/d5m/`.
The [source ledger](debugger-repair-sources.csv) pins decisive receipts and
methods, including retained failed and superseded results. The postflight uses
91,933 archive references plus 1,401 surviving loose hashes and protects all 98
save names/backups. It does not restore the obsolete loose-payload audit.

## Authority, evidence state and review

No Starfield process was launched or attached, and no save, installed content,
Steam configuration, backup or analysis database was modified. Protection uses
the active archive/index baseline and surviving inputs, not a recreated loose
93,334-payload audit. Both drive floors remain 40,000,000,000 caller-available
bytes. Historical strict ZIP failures remain historical. `remotecache.vdf`
remains diagnostic; protected local/remote saves and backups remain strict.

The scoped engineering result does not resolve the retail construction question,
historical winning mask, persistence, exclusive query causation or game survival.
The frozen D5L and earlier scientific classifications remain unchanged. The
versioned Phase B proposal retains Save52, second Feynman V and the pre-load
barrier; even an engineering GO recommendation supplies no live authorization.

| Frozen criterion | Current assessment | Evidence / limit |
|---|---|---|
| AC1 authority/protection | PASS, scoped Phase A | Full pre/post comparison, both floors, target absence and unchanged HEAD/index; no live action. |
| AC2 fault investigation | PASS for scoped investigation | Full post-mortem, early-exit ordering, qualified existing dump and alternatives; historical initiating cause UNKNOWN. |
| AC3 debugger correctness | PASS within tested envelope | Final exact-build ownership, disposition, queue, failure and cleanup controls; independent engineering ACCEPT. |
| AC4 scientific coverage | PASS for preserved synthetic claims | Final positive/negative controls and decoded receipts preserve the frozen distinctions; no new retail scientific conclusion. |
| AC5 Windows qualification | PASS | All 42 cases, transport, focused faults and adversarial controls; counterexamples retained. |
| AC6 retail proposal | PASS as proposal | Versioned exact-build card, ordinary-user gates and reviewed-derivative hold. Phase B NOT AUTHORIZED. |
| AC7 durable record | PASS | Methods, source ledger, outcomes, limits and preserved history; manual reading, zero-diagnostic screen and exact forward/reverse application checks pass. |
| AC8 independent acceptance | PASS with final closure gate | Both exact-snapshot independent reviews ACCEPT. Delivery requires both closure-delta ACCEPT records and matching final hashes described below. |

Independent engineering and scientific reviewers both accepted `review01`,
whose complete/task-only patch hashes are respectively
`78bcaa91b0d8a8dedc01a0df3b411149a197b7c0cf6b51fbf10dfc891e94a1da`
and `5898dca7bfefcc0bc4050927caa7293992c3e722e7ba2da57f154bb34c304920`.
Each independently decoded all 1,250 receipts/ACKs, reproduced all 42 reductions
and checked all 51,447 control rows, 51 build pins and 44 ledger pins. Their
verbatim returns and criterion matrices are `.local-work/d5m/engineering-final-review.md`
and `.local-work/d5m/scientific-final-review.md`. Neither reran target experiments;
full protected-input measurements and exact application-tree results are supplied
primary records, with engineering additionally performing read-only application checks.
Both editorial dispositions accept the changed prose/comments.

Only this closure text and the research-state acceptance line change afterward.
Their independent delta dispositions are retained as `engineering-closure-review.md`
and `scientific-closure-review.md` in the same local directory. The final delivery
is valid only with both ACCEPT returns and matching `final-delivery.json` hashes;
that external receipt binds final patches, manifests, exclusions, actual status,
manual/screen checks and both review stages without self-referential hashes.

**Recommendation: GO to seek separate explicit Phase B approval for the exact
reviewed versioned card. Current retail execution is NO-GO.** The passing result
is an offline engineering/scientific capability, not confirmation of the retail
hypothesis, authorization to integrate, or publication clearance.

No criterion is relaxed to fit a development result. Final review returns,
editorial inventory, complete/task-only patches, exclusions, exact application
checks and delivery hashes are retained in `.local-work/d5m/`. Raw dump/context,
native/fixture binaries and all receipts remain LOCAL-ONLY. Authored changes are
REVIEW-REQUIRED; no staging, commit, push, integration or publication is performed.
