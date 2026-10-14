# Revised native-oracle acquisition plan 01

2026-10-11. SOR-EXP-0031 / SOR-EV-0039 follow-up. **OFFLINE REVIEW PROPOSAL.**
The user requested a revised plan/card, not implementation or live execution.
No candidate binary, deployment, overlay/configuration change or new experiment
is authorized by this document. Historical source/card/result remain unchanged.

The recommendation is a diagnostic observer revision with two additional complete
CALL wrappers, retaining natural center/grid acquisition. First establish whether
the existing Save25/26 controls reach candidate queries and reference enumeration.
Do not repeat the old observer unchanged or promise that build mode invokes it.
Exclude the observed overlays and enforce module admission **before patching**.
The accompanying [proposed run card](revised-run-card-01.md) defines the first
bounded diagnostic session; it is blocked pending implementation, qualification,
artifact locking and explicit user approval.

## Question, contract and present evidence

| Element | Proposed contract / supported state |
|---|---|
| Task | Offline plan and run-card revision; no implementation in this assignment. |
| Question | Can a conforming observer discriminate upstream non-traversal, pre-enumeration gating and callback non-dispatch while preserving independent native acquisition? |
| Best-supported answer | Two known complete CALL boundaries can provide this discrimination if naturally reached; live reachability remains UNKNOWN. |
| Basis/coverage | STATIC on pinned retail 1.16.244.0, plus the prior zero-event session. Existing-site travel/build controls were tested only with 0.1.0; proposed diagnostics are NOT BUILT/NOT TESTED. |
| Mandatory proposal criteria | Explicit overlay disposition and pre-write gate; concrete native sites/contracts; linked diagnostic schema/outcomes; bounded operator card, safety/cleanup, qualification and approval requirements; reviewable diffs and independent review. |
| Negative criterion | This proposal may specify scoped no-observation outcomes. Neither the previous empty capture nor a future diagnostic-only result closes native equivalence or proves general infeasibility. |
| Continuation / exits | Offline document/static-evidence corrections within this request. Implementation, new hooks in a deployed binary, settings changes, a changed trigger or live execution need the specific approval described below. |
| Present science | Native equivalence NOT TESTED; frozen 23 predictions unchanged. Prior operational admission NOT SATISFIED. |

The [accepted result report](live-attempt-01.md) and
[independent review](live-attempt-01-review.md) establish the narrow starting
point: zero events, successful recorded retirement/removal, and a startup-gate
violation. They establish no overlay cause or corrective implementation defect.
Static exports and hashes are retained in [native-sources.csv](native-sources.csv).
Source provenance remains SOR-S-0127/0132/0142 and the existing project records;
these are project-authored interpretations of local exports, not new third-party
code reuse. The native-boundary specialist independently checked the proposed
sites and trigger limits; the independent reviewer assesses this proposal.

## 1. Resolve overlay admission without an implicit exception

Choose exclusion, rather than declaring the previous overlay combination safe.
For a future explicitly approved attempt, the user disables Steam's Starfield
overlay and NVIDIA overlay/capture features using their normal settings, before
launch. Record exact setting names/values and previous values locally. The user
controls these changes and any restoration after exit. No settings are changed
now; no service killing, DLL deletion/renaming, driver change or antivirus change
is part of the proposal.

The prior inventory contained `gameoverlayrenderer64.dll`, `nvspcap64.dll` and
`nvppex.dll`. Reject all three by case-insensitive module basename regardless of
path/hash; retain actual path/hash as evidence. A settings attestation alone does
not clear their presence. If disabling overlays leaves any of them loaded, refuse
installation and report NOT_READY. Do not relabel a module to make it pass.

An exact, reviewed module policy is also required: canonical path, SHA256, role,
permitted phase and reason the module fits the startup assumption. Unknown or
changed modules fail closed. The previous 90-module inventory is a discovery source,
not an allowlist: subtracting three overlays does not approve the remaining 87.
For example, `sl.interposer.dll` and security/graphics components require explicit
role/startup assessment; a Windows/Steam/NVIDIA path or valid signature alone is
not a compatibility proof. Do not disable essential/security components to obtain
a green result. If an essential component cannot satisfy the exclusion/startup
contract, return to offline architecture review; no broad injector exception is
included here. Module identities may be pinned offline; permitted phases need
review because main-menu rendering can load additional modules.

Required new behavior in the proposed instrument:

1. Persist the process identity, disk/module/source policy and initial module
   inventory before any game code/vtable edit. No observer worker exists yet.
2. Perform all file/preimage/relay checks; wait at most the existing 120 seconds
   for sole-thread startup. Re-enumerate modules and recheck the sole thread
   immediately before installation. Any enumeration/hash/policy failure refuses
   all six edits. Persist a refusal with `patches_installed=false` when true.
3. Start the worker only after installation; publish READY only after writer,
   patch guards and admission receipt succeed. A post-install failure retains
   resident code and discloses possible edits; it is not a pre-install refusal.
4. Monitor the phase-specific module policy during collection and before every
   operator action; detection of a forbidden/unknown module closes admission,
   requests retirement and blocks further gameplay phases. No hot removal.

This corrects0.1.0's sequence: its module inventory was written by the worker
**after** installation and did not enforce injector policy. An operator reading
that inventory could only halt further actions, not prevent the original edits.
The revision needs a new source/build review, not merely a new attestation.

Residual risk remains explicit: snapshots do not prove no future thread creation,
short-lived/unlisted injection or all-CPU synchronization. Exclusion, a reviewed
launch environment and the sole-thread gate bound the assumption; they do not
turn it into a supported concurrency interface. No suspension/debugger fallback
or weaker patch gate is proposed.

## 2. Observe the missing reachability chain

Static image base is `0x140000000`; runtime VA is actual loaded base + RVA.
The following sites were checked against existing exports and freshly rehashed
on-disk PE bytes. Implementation must repeat verification and qualify the guards;
disk CALL bytes do not establish ABI safety or runtime traversal.

| Proposed / retained boundary | Static VA; RVA | Natural call contract and purpose |
|---|---|---|
| NEW query wrapper Q | `0x140AD93FA`; `0x00AD93FA` → `0x140AD08D0` | RCX is the five-pointer query context, RDX candidate descriptor. Begin/end/abnormal events bracket this caller's query. Caller compares EAX with 1 at AD93FF; preserve the full consumed result, not an inferred AL-only bool. No consumed stack args identified; forwarding must be qualified. |
| NEW enumeration wrapper E | `0x140AD0AB5`; `0x00AD0AB5` → `0x140B1E190` | RCX collection, RDX callback object, R8B=0. Bracket reference enumeration and bind callbacks to this enumeration. Preserve full observed argument/return ABI; do not infer a void return from the decompiler. |
| Retained callback C | Vtable RVAs `0x04B916F0/0x04B916F8` → thunk `0x00AD8EC0` | Natural per-reference callback begin/end, raw reference/context identity. |
| Retained center/grid | CALL RVAs `0x00AD0C36` → `0x00F4AB80`; `0x00AD0D36` → `0x0096F5C0` | Original native output/input/result captures inside C; both channels enabled. |

Primary evidence: `engine-oracle-04.tsv:32–69` constructs Q's context and calls
AD08D0; `engine-oracle-02.tsv:48–164` shows the query gates and exact enumeration
CALL. `exp0002-selection-sites.tsv:827–915` shows collection/reference filters and
indirect `[vtable+0x10]` dispatch. The original
[architecture](architecture.md) supplies retained sites/contracts. Total proposed
patch set: four complete CALL replacements plus two vtable slots, installed as
one guarded startup transaction. No entry/prologue hook, arbitrary instruction
stealing, return-address rewriting, trap or engine call manufactured by Codex.

Fresh read-only PE verification on 2026-10-11 confirmed the game hash above and:

| RVA | PE file offset | Original complete CALL bytes | Decoded target RVA |
|---|---|---|---|
| `0x00AD93FA` | `0x00AD89FA` | `E8 D1 74 FF FF` | `0x00AD08D0` |
| `0x00AD0AB5` | `0x00AD00B5` | `E8 D6 D6 04 00` | `0x00B1E190` |

Receipt `.local-work/native-oracle/revised-plan-01/native-call-verification.json`
also records 32-byte window hashes. Original Python stdlib parsing read only the
installed executable and wrote that exclusive ignored receipt; no process access,
native execution, patch, tool download or database change. These candidate guards
are not a release lock and do not clear the unimplemented six-patch transaction.

Keep Q/E diagnostics compact and distinct from oracle records. Each includes
schema/version, global sequence, QPC/thread, unique invocation and parent ID,
boundary RVA, phase, pointer/read-validity masks and normal/abnormal completion.
Maintain nested TLS Q→E→C linkage, including explicit unknown/orphan parents for
calls outside the instrumented chain. Record the 40-byte Q context, bounded
candidate fields including its `+0x10` key, bounds/output flag before/after, actual
query return bytes, callback vtable/context, and relevant source/active-landscape
identity through already verified bounded layouts. Exact descriptor lengths and
new read layouts are implementation acceptance items, not guessed offsets.

No whole collection traversal, census, engine lookup or native diagnostic call.
Save source pointers and raw bytes separately from any interpreted gate fields.
Unreadable/racing identity remains unknown. Diagnostic context and a user site
label never qualify a native grid comparison by themselves.

The worker must durably publish monotonic health and control acknowledgements
even with no native events. Proposed heartbeat period 1 second; a 15-second missing
heartbeat/unique control-nonce acknowledgement prevents a new operator action
and triggers health-stop handling. These are safety deadlines to qualify offline,
not scientific no-hit time limits or proof the game is hung. Preserve an append-only
health history, current UTC/QPC, active Q/E/C scopes, queue/loss/depth counts,
admission/module status and flushed event sequence/offset. Never manufacture an
engine event as a positive control.

| Qualified durable observation within linked, normally completed scopes | Supported interpretation / next disposition |
|---|---|
| Healthy heartbeat/ack, Q=0 | This CALL was not observed under the controls. Upstream producer reachability remains unresolved; do not repeat identical controls indefinitely or claim no engine queries anywhere. |
| Q>0, descendant E=0 | Query observed, enumeration boundary not observed; investigate pre-enumeration paths. Does not identify the exact gate or prove an overlay/hierarchy mismatch. |
| E>0, descendant C=0 | Enumeration observed, callback not observed; collection/reference filtering and dispatch remain the next question. No claim that no outposts exist. |
| C>0, no center/grid | The callback is reachable; inspect its eligibility/early-return evidence. No model comparison occurred. |
| Paired identity-qualified center/grid | Analyze native bytes against unchanged predictions under existing identity/frame rules; distinguish replay from saved-to-loaded reconciliation. |
| Missing health, loss, abnormal/unpaired scope or integrity failure | An incomplete capture/health failure; zero-child counts are not a qualified branch negative. |

Do not aggregate unrelated query/enumeration/callback counts into causal ratios.
Some callbacks may have no Q/E parent; report them separately. A future runtime
gate diagnosis would need more evidence than this minimal patch set. Specifically,
natural helper-return observations at AD092C→ACCAD0, AD0976→96EFB0 and
AD0986→96FB40 could expose overlay and candidate/source hierarchies. They are
**excluded from this card**. Their qualification/review would preserve both 44-byte
hierarchies and the actual comparison-field mask at AD098B–AD0A0C; whole-buffer
equality or an earlier sampled flag is not proof of the native branch decision.

## 3. Trigger choice and acquisition strategy

Use the old Save25/26 SOR-003→002→003 controls first with the new Q/E diagnostics,
as a controlled change of instrumentation/environment, not as an established
positive trigger. Do not attribute any difference specifically to overlay removal:
both instrumentation and environment differ from attempt 01. A factorial overlay
experiment would reintroduce the excluded condition and is not proposed.

`durable-center-04.tsv:1994,2038,2212–2245` shows the known 77FC20 path searches
existing references via 77F900 and takes candidate search 77E350 only after a null
result. Existing-site travel therefore need not reach Q. This is why the new
instrument has upstream diagnostics and why no useful-oracle guarantee is made.

A new planetary landing-site selection is a stronger **trigger hypothesis** for
candidate processing, but not established live. It changes sites, terrain and
potential autosave state; a beacon placement preview is not statically proven to
invoke this graph. Neither is included as an improvised no-hit fallback. If Q
remains absent, preserve the diagnostic result and prepare a specific landing-site
trigger amendment with controlled save copies, exact body/site selection, UI
confirmation boundary, autosave protection and a natural producer argument.
That requires explicit user scope approval before implementation/live use. Do not
turn an unreviewed map preview into a claim of harmless or guaranteed acquisition.

Other routes considered: unchanged 0.1.0 retry has little discrimination; passive
shared-center polling remains stale/ownership-ambiguous; global helper-entry hooks
increase scope/ABI burden; gate helper wrappers add patches before the parent path
is known reachable. The two CALL additions provide the smallest currently evidenced
separation of query, enumeration and callback. No external debugger route reopens.

## 4. Required engineering before this card can be executable

Proposed distinct component revision: SorNativePositionOracle0.2.0, schema 2.
These are reserved proposal labels, not a release. Preserve 0.1.0 and observer 0.1.1,
all failed evidence and the frozen fixtures. No ZIP/DLL/hash or event size exists
for 0.2.0 yet. No current 0.1.0 build satisfies the revised card.

| Mandatory future qualification | Evidence required before approval |
|---|---|
| Exact sites and native contracts | Hash-pinned installed PE verification, complete E8 call bytes/targets/rel32 reach, consumed args/returns, relay/unwind/CFG/CET limits and six-patch guard/rollback ledger. |
| Pre-write overlay/module gate | Forbidden module, unknown module, changed hash, failed enumeration, late load, thread-gate timeout tests. Assert zero game edits for every pre-install refusal; no READY on refusal. |
| Startup and lifetime | Pre-main sole-thread gate unchanged in strength; all-or-refused six edits, rollback/residency failure paths, STOP and abnormal native unwind through nested Q/E/C. No unload/live unpatch. |
| Positive and negative diagnostic controls | Disposable real machine CALL/vtable chain Q→E→C→center→grid; Q-only, E-without-C, C-early-return, orphan/nested/concurrent/exception cases. Verify full ABI/FP/LastError and exact forwarding. Synthetic positives remain QUALIFICATION, never native Starfield evidence. |
| Durable health/transport | No-event heartbeat and nonce ack, sustained backlog, disk floor/query errors, writer failure, queue loss/depth, STOP while active scopes and control starvation. Validate deadlines and bounded producer overhead; do not silently sample away counts. |
| Inspector and scientific separation | Version 2 schema/pairing/hash validation, parent scope matching, diagnostic-only outcomes, incomplete-prefix treatment, existing frozen 23 predictions unchanged; strict ordinary identity/frame requirements. |
| Package/tools | Reproducible versioned Vortex ZIP, source/module-policy hashes, exact install/remove manifest, future preflight/postflight commands and limitations. Postflight hashes actual installed SFSE/loader, not just a staging directory. |
| Independent review | Original contract, adverse evidence, complete/task-only diffs, source/build/policy/card hashes, acceptance matrix and reviewer decision. No current Phase A acceptance transfers to 0.2.0. |

Implementation may use only already authorized project/SFSE material with retained
provenance. New dependency/framework/third-party adaptation needs its existing
rights and user gates; none is proposed. Build scripts must remain offline with no
download/update/upload step.

## Review and exact future approval boundary

This proposal is complete only as an offline plan/card package with critical
review; it does not complete acquisition engineering or native equivalence.
[Independent proposal review](revised-plan-01-review.md) records the decision.

The next scoped decision would authorize offline implementation/qualification of
the two CALL additions, pre-write module policy and durable health protocol, and
review of the resulting versioned ZIP with this filled card. A later explicit
approval would name that exact ZIP/policy/card and the user's overlay-setting
changes plus Save25/26 diagnostic sequence. Neither approval includes additional
gate hooks, new landing sites, placement, saves, forced calls, debugger attachment,
configuration workarounds or an automatic retry. After conditional live approval,
all mandatory gates passing is sufficient to proceed without a second routine
approval; a failed gate stops rather than weakening the condition.

No staging, commit, push, publication or external disclosure is requested or
performed. Raw exports/session/module details remain ignored/local. Proposal
diffs and checks are under `.local-work/native-oracle/revised-plan-01/` and
`.local-work/diffs/native-oracle-revised-plan-01-*.diff`.
