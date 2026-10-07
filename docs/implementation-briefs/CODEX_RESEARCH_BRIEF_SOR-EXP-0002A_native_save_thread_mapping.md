# Codex Research Brief — SOR-EXP-0002A Native Save Invocation and Execution-Thread Mapping

**Repository:** `D:\Projects\starfield-outpost-research\`  
**Project:** `gooberpede/starfield-outpost-research`  
**Experiment:** `SOR-EXP-0002A`  
**Date:** 2026-10-06  
**Purpose:** improve SOR-EXP-0002 tooling before resuming the outpost membership experiment  
**Observer versioning:** begin at `0.1.0`  
**Live debugging:** authorized only within the bounded stages below  
**Commit/push:** not authorized by this brief

---

## 1. Objective

Pause SOR-EXP-0002 and investigate Starfield's normal save-request path so that the research observer can later create controlled checkpoint saves without using the console or relying on manual save UI.

Primary question:

> **How does Starfield 1.16.244.0 request and complete an ordinary manual save, which execution thread/context initiates that request, and what is the highest legitimate engine operation an SFSE observer can invoke to reproduce it safely and deterministically?**

Secondary tooling question:

> **Can the same demonstrated execution context be used for selected-reference native observations such as `GetWorkshop`, allowing one coherent checkpoint transaction: reacquire live state -> perform queries -> request save -> confirm save completion?**

This is a tooling-enablement experiment. It does **not** resume beacon/storage construction or attempt to complete A0-A2R.

---

## 2. Why this experiment exists

SOR-EXP-0002 produced two useful tooling findings:

1. the pinned SFSE build does not emit the save/load notifications originally assumed by the observer because the corresponding serialization hooks are disabled in the pinned source revision;
2. `SFSETaskInterface::AddTask`, although documented in `PluginAPI.h` as executing on the "Main thread", was observed live on multiple OS threads during A0/A0C.

The second finding means the project must not treat the SFSE task queue as a demonstrated execution-thread contract for native selected-reference calls.

Rather than patching around that blindly, investigate Starfield's own manual-save path. A valid save-request path may provide both:
- an evidenced engine execution context;
- a better checkpoint mechanism for SOR-EXP-0002.

---

## 3. Required reading

Before work, read the current committed state, especially:

```text
AGENTS.md
WORKFLOW.md
THIRD_PARTY_POLICY.md
CREDITS.md
THIRD_PARTY_NOTICES.md

docs/CHARTER.md
docs/RESEARCH_STATE.md
docs/EVIDENCE_STANDARD.md
docs/PROVENANCE.md
docs/SOURCES.md
docs/PERMISSIONS.md
docs/DECISIONS.md
docs/function-register.md
docs/state-register.md
docs/known-facts.md
docs/hypotheses.md

docs/experiments/SOR-EXP-0002-outpost-membership-reload-location.md
docs/experiments/EXP0002-gate-b-run.md
docs/experiments/EXP0002-review14-run.md
docs/experiments/evidence/exp0002-review14-live/README.md
```

Also inspect the existing EXP0002 observer/tooling before changing it.

Do not reinterpret the incomplete primary experiment as a completed membership test.

---

## 4. Third-party/SFSE permission and attribution rules

SFSE is third-party work and must remain explicitly credited and permission-scoped.

### 4.1 Existing approved reuse

The repository already records:

```text
SOR-P-0001
```

for the exact pinned use of:

```text
ianpatt/sfse
sfse/PluginAPI.h
commit 48535cc4306ab345252bf740c20a1c6194929b0e
```

under the recorded MIT permission basis accepted by the user.

That approval is **only** for the recorded header/use.

Do not silently broaden it.

### 4.2 Allowed source consultation

Read-only inspection of publicly visible SFSE source is allowed as research under project policy.

Where SFSE source materially informs:
- save-path identification;
- task scheduling interpretation;
- message behavior;
- interface semantics;
- naming or experimental design,

record and credit it in the durable source/research record.

Use exact commit/path/lines or equivalent pinned provenance where practical.

### 4.3 No additional code incorporation without approval

Do not copy, adapt, port, translate, or substantially reimplement SFSE hook/source code beyond the already approved `PluginAPI.h` scope unless:

1. the rights basis is documented;
2. the exact material/use is surfaced;
3. the user explicitly approves that use;
4. required notices are preserved.

Reading `Hooks_Serialization.cpp` to discover addresses/call structure is not permission to copy its hook implementation.

A project-authored implementation informed by observed engine behavior must honestly record source influence where applicable and must not be falsely described as clean-room if it is source-informed.

### 4.4 Credit

Update as justified:

```text
docs/SOURCES.md
docs/PERMISSIONS.md
CREDITS.md
THIRD_PARTY_NOTICES.md
```

Do not imply SFSE authors endorse this research.

---

## 5. Observer versioning begins here

The next observer build is:

```text
0.1.0
```

Do not retroactively assign semantic versions to historical `review08`, `review12`, `review14`, etc. Those remain historical package labels/hashes.

For SOR-EXP-0002A and later EXP0002 fixes:

```text
0.1.0
0.1.1
0.1.2
...
```

Increment patch by `0.0.1` for each reviewed correction within this experiment/tooling line.

Move to a new minor version only for a materially expanded capability after discussion.

### 5.1 Single source of truth

Define the version once and propagate it consistently to:

- SFSE plugin version metadata;
- human-readable observer version;
- package/build manifest;
- `ready.json`;
- session metadata;
- checkpoint/anomaly/failure records;
- debugger/tool metadata where it identifies the observer;
- ZIP filename;
- documentation/report;
- hashes/package inventory.

Suggested package naming:

```text
SorExp0002-0.1.0.zip
SorExp0002-0.1.1.zip
```

Do not use `reviewNN` as the primary package identity once semver begins.

Document the integer encoding used for `SFSEPlugin_Version.pluginVersion`.

A suitable convention is:

```text
0x00010000 = 0.1.0
0x00010001 = 0.1.1
...
```

if compatible with the current build code. The exact convention must be documented and tested.

---

## 6. Save3 remains protected

The pristine parent remains the existing Save3 sample and backup.

Do not modify or overwrite either.

Before any live stage:

- rehash original;
- rehash backup;
- confirm byte equality;
- confirm unchanged size/mtime/hash relative to durable baseline;
- record discrepancy and stop if not identical.

Manual-save tracing may load Save3 or another disposable derived sample through normal UI as authorized below, but source/backup integrity must remain protected.

No console use.

---

## 7. Save-file clutter and archive policy

If plugin-triggered saves become viable, they should not permanently clutter:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\
```

However, **do not delete or move a newly created save while Starfield is still running until this experiment establishes that doing so is safe**.

### 7.1 Default cleanup model

Prepare for:

```text
Starfield creates save normally
        ↓
identify exact save file
        ↓
confirm save operation completed
        ↓
record filename / size / SHA-256
        ↓
game exits or reaches a separately demonstrated safe cleanup point
        ↓
copy to:
.local-work/savegames/...
        ↓
verify copied bytes/hash
        ↓
remove original from live Saves directory
```

Do not move instead of copy-first.

Do not delete before source/copy hash equality.

### 7.2 Investigate bookkeeping

Determine whether Starfield maintains relevant in-memory or external metadata for:
- save-list UI;
- cloud synchronization;
- exit-save replacement;
- deletion;
- current save identity.

If an engine-supported deletion route is safer than external post-exit deletion, document it.

Do not implement automatic deletion until its safety is established.

---

## 8. Experiment structure

Use three stages.

```text
Stage A — static mapping and debugger preparation
Stage B — trace one or more ordinary manual saves
Stage C — prototype plugin-triggered save only if B establishes a credible contract
```

Each stage has its own evidence and stop boundary.

Do not jump to Stage C merely because a candidate function address exists.

---

# STAGE A — Static save-path mapping and capture preparation

## 9. Map the current manual-save path

Use current pinned:

```text
Starfield.exe 1.16.244.0
CreationKit.exe where useful
Ghidra existing analyzed projects
```

Read-only by default.

Review the pinned SFSE source as a credited lead, including the known declarations around:

```text
SaveGame_Call
SaveGame_Original
BGSSaveLoadGame
Hooks_Serialization
```

Do not assume the old names/signatures remain semantically exact for the current retail binary.

### 9.1 Find the highest useful save-request layer

Do not begin with the lowest serializer by default.

Identify candidate layers such as:

```text
UI/manual-save request
save-manager request/queue
BGSSaveLoadGame method
VM/script serialization
file/container writer
```

Determine which layer establishes necessary:
- save state;
- menu/game-mode conditions;
- locks;
- current-save name/state;
- scripting coordination;
- notifications/events;
- asynchronous work;
- completion bookkeeping.

Prefer the highest layer that can be invoked deterministically without reproducing unrelated UI behavior.

### 9.2 Candidate record requirements

For each implicated function:

- original name/symbol if present;
- static VA;
- RVA;
- pinned executable hash/build;
- callers/callees;
- relevant strings;
- object/type context;
- candidate signature;
- side effects;
- thread assumptions;
- confidence;
- evidence source.

Update `docs/function-register.md` only where justified.

Do not bulk-rename Ghidra functions.

---

## 10. Thread-context mapping

Prepare to identify separately:

```text
plugin-load thread
SFSE loader-reported primary thread
manual-save request initiating thread
candidate save-manager call thread
serializer/file-worker threads
SFSE AddTask dispatch threads
```

Do not label any of these "main thread" solely by assumption.

Where thread creation/provenance can be determined:
- record OS TID;
- creation time/order if available;
- current RIP/caller when captured;
- whether the thread corresponds to process startup.

The key question is:

> Which thread/context does the ordinary game use when entering the save-request operation we may later invoke?

---

## 11. Stage-A debugger design

Prepare a narrow debugger trace around the ordinary manual-save path.

Use Ghidra debugger or x64dbg according to whichever offers the better bounded trace for the identified sites.

The user explicitly permits crash-tolerant/kamikaze traces where worthwhile evidence can be persisted first.

### Desired evidence

Capture, as applicable:

```text
thread ID
runtime module base
entry RIP
caller/return chain
RCX
RDX
R8
R9
relevant stack arguments
save-manager / BGSSaveLoadGame instance
save-name pointer/string
unknown argument values
pre-call state
return/result
immediate post-call state
related save-in-progress flags
file creation/completion timing
```

If the normal save path is asynchronous, capture enough to distinguish:
- request acceptance;
- actual file write;
- save completion.

### Finite bounds

Keep the first capture narrow.

Examples:

```text
one manual save request
or <= 100 relevant hits
or <= 10 seconds armed after explicit operator action
```

The actual selected bound should be justified by the mapped call path.

Persist records incrementally.

A post-evidence crash is acceptable.

A pre-evidence crash is incomplete.

---

# STAGE B — Live manual-save trace

## 12. Stage-B authorization

This brief authorizes a bounded live manual-save trace after Stage A has produced and internally validated the exact capture configuration.

Codex may proceed from Stage A to Stage B **without a new large brief** only if:

- target build/hash still matches;
- target sites/bytes are validated;
- trace bounds match this brief;
- no new third-party code incorporation is required;
- Save3 remains protected;
- no target-memory/register mutation beyond ordinary debugger execution-control mechanics is introduced;
- no console is used.

If any of those conditions change materially, stop for review.

### Deployment

Any SFSE plugin used is deployed exclusively through Vortex.

The user performs installation/deployment/retirement manually as directed.

Do not edit Vortex staging/database state directly.

---

## 13. Manual save as the oracle

The first live trace must observe **Starfield's own ordinary manual save**.

The user performs the save through normal UI.

Do not:
- use console `save`;
- trigger the save from the plugin yet;
- patch the save manager;
- infer arguments from old SFSE source alone.

The manual save is the oracle for:
- call path;
- thread;
- manager instance;
- arguments;
- name semantics;
- completion behavior.

### Naming

The save may use whatever name Starfield normally generates.

Do not contaminate the experiment merely to force a deterministic name.

---

## 14. Stage-B success criteria

Stage B should determine as many of these as possible:

1. Which engine function is the first practical save-request layer?
2. Which OS thread invokes it?
3. What object is passed as `this` / save-manager instance?
4. What are the live values/roles of the other arguments?
5. Is a save name/path passed at that layer?
6. Does the name permit deterministic caller-supplied names?
7. Does the function return before the `.sfs` is fully durable?
8. What observable event/state marks completion?
9. Does the save path spawn/dispatch work to other threads?
10. What state must be set before the request and cleared after it?
11. Does the save list/cloud layer require separate bookkeeping?
12. Is the same initiating thread a plausible context for `GetWorkshop` and related callbacks?

Do not force answers where the trace does not establish them.

---

# STAGE C — Prototype plugin-triggered save

## 15. Entry gate

Proceed to Stage C only if Stage B supports a credible, bounded native invocation contract.

If the contract remains materially ambiguous, stop and report.

Do not guess unknown arguments.

Do not invoke the lowest serializer merely because it appears callable.

---

## 16. Observer `0.1.0`

Build the next reviewed observer as:

```text
SorExp0002 0.1.0
```

Its immediate purpose is tooling qualification, not completing A0-A2R.

It may include:

- experiment request intake;
- execution-thread observation;
- thread-specific pending-operation dispatch;
- a single native save-request operation;
- save-completion observation;
- manifest generation;
- local evidence recording.

Do not add unrelated outpost functionality unless required to test whether the same thread can safely service a selected-reference query.

---

## 17. Thread-specific dispatch

Do **not** rely on `SFSETaskInterface::AddTask` as a proven single-thread scheduler.

Design a bounded dispatch mechanism based on the execution context established in Stage B.

A candidate pattern is:

```text
worker/request intake
    ↓
pending operation
    ↓
small engine-thread hook/dispatcher
    ↓
if current TID != designated TID:
    record bounded scheduling observation
    leave request pending
    return normally
    ↓
if current TID == designated TID:
    execute exactly one pending operation
```

Do not spin/requeue inside the same SFSE task-drain loop.

Do not busy-wait on the game thread.

Use finite wall-clock and dispatch-count bounds.

If the designated thread does not appear:
- persist `query/save_thread_not_observed` or equivalent;
- retain observed TIDs/counts;
- do not guess another thread;
- leave the instrument coherent.

### Permanent dispatcher

A small permanent hook/task is acceptable if:
- its no-request path is trivial;
- it is bounded;
- it has explicit provenance;
- it does not copy unapproved SFSE hook code;
- it has a documented install/uninstall/deployment model.

If implementing such a hook requires third-party code reuse beyond current approval, stop for permission review.

---

## 18. Save-request transaction

For the prototype, the desired order is:

```text
operator confirms settled state
    ↓
plugin request accepted
    ↓
designated engine thread services request
    ↓
capture pre-save session/thread/context
    ↓
invoke validated save-request layer
    ↓
observe completion
    ↓
identify exact .sfs
    ↓
hash / manifest
    ↓
terminal record
```

Do not yet require outpost `GetWorkshop` queries in the same transaction unless Stage B/C evidence supports the execution context.

If added as a narrow test, keep it clearly separable:

```text
native-query qualification
save qualification
```

A successful save does not prove the thread is safe for every native callback.

---

## 19. Deterministic save names

Investigate whether the validated save-request layer safely accepts a caller-supplied save name.

If yes, prefer neutral experiment names such as:

```text
SOR_EXP0002A_SAVE_001
SOR_EXP0002_A0
SOR_EXP0002_A1
```

subject to actual engine naming constraints.

No console use.

If caller-supplied naming requires unsupported assumptions or lower-level invocation, defer it.

Correct save creation is more important than naming convenience.

---

## 20. Save-completion semantics

Do not equate:

```text
native function returned
```

with:

```text
save safely complete on disk
```

unless demonstrated.

Establish a completion signal using one or more of:

- higher-level save-manager state;
- file appearance plus stable size;
- final rename/close;
- engine completion callback/event;
- explicit state flag;
- other traced completion path.

Document latency and race conditions.

Do not archive/delete while write completion is uncertain.

---

## 21. Project archive and cleanup

Once a prototype-generated save is confirmed complete:

- register its generated filename;
- size;
- SHA-256;
- parent/run;
- observer version;
- request ID;
- save-request thread;
- completion evidence.

### Default archive path

Use a local ignored structure such as:

```text
.local-work/
  savegames/
    exp0002a/
      attempt-001/
```

or another equally clear project-local structure.

### Cleanup

For the first qualification run:

- do not automatically remove the live `.sfs` while Starfield is running;
- exit Starfield normally unless the trace crashes it;
- wait for/confirm sync state according to current workflow;
- copy the save to project-local ignored storage;
- verify hash equality;
- only then remove the live copy if the user has authorized cleanup and the engine/cloud state is known-safe.

The user wants automatic checkpoint saves ultimately removed from the load list, but safety takes priority until bookkeeping is understood.

Retain incidental exit saves separately.

---

## 22. Save deletion/bookkeeping investigation

As part of Stage B/C, investigate:

- whether save-list metadata is derived directly from directory contents;
- whether Starfield caches the list in memory;
- whether Steam/cloud sync observes file creation/deletion directly;
- whether a native delete-save operation exists and performs required bookkeeping;
- whether external deletion after process exit is sufficient.

Do not implement automatic deletion unless established safe.

If no engine-side bookkeeping is found, record that as an open question rather than assuming none exists.

---

## 23. Console/achievement boundary

Do not open the console anywhere in SOR-EXP-0002A.

The separate Developer Mode/achievement persistence question remains deferred.

A plugin-triggered native save is valuable partly because it may give deterministic naming without introducing console state.

Do not make any claim about achievement eligibility unless separately tested.

---

## 24. Instrument behavior on anomalies

Retain the current research principle:

> **Unexpected scientific observations are evidence unless they make continued acquisition unsafe.**

Do not kill the instrument merely because:
- thread count differs;
- thread IDs differ from expectation;
- argument value is unexpected but readable;
- completion latency is longer than predicted;
- extra save-related activity is observed.

Persist bounded evidence.

Hard-stop only for genuine integrity/safety conditions such as:
- wrong executable/site bytes;
- unreadable structure where continuing would dereference unsafe state;
- evidence write failure;
- low disk space;
- package/profile mismatch;
- source-save corruption risk;
- unbounded output;
- unauthorized mutation requirement.

Retain the existing low-disk-space protection:
- at least 40,000,000,000 bytes available on relevant C: and D: volumes before/through capture.

---

## 25. Observer output and version identity

Every observer-generated artifact must include:

```text
observer_semver
observer_plugin_version_integer
package SHA-256
DLL SHA-256
game build/hash
SFSE version/hash
session ID
request ID
thread IDs relevant to operation
timestamp
```

The observer should refuse or flag evidence if its runtime/package identity does not match the reviewed package.

---

## 26. Evidence and durable records

Create/update as justified:

```text
docs/experiments/SOR-EXP-0002A-native-save-thread-mapping.md
docs/experiments/evidence/<exp0002a-evidence-index>/README.md
docs/PROVENANCE.md
docs/RESEARCH_STATE.md
docs/DECISIONS.md
docs/function-register.md
docs/state-register.md
docs/known-facts.md
docs/hypotheses.md
docs/SOURCES.md
docs/PERMISSIONS.md
CREDITS.md
THIRD_PARTY_NOTICES.md
```

Do not touch every file mechanically.

Promote findings only where evidence warrants it.

Distinguish:

```text
SFSE SOURCE-REPORTED
PROJECT-VERIFIED STATIC
PROJECT-VERIFIED RUNTIME
PROVISIONAL
OPEN
```

A source comment saying "main thread" is not runtime proof.

---

## 27. Required tests before any plugin-triggered save

At minimum test offline/synthetically:

### Versioning
- `0.1.0` appears consistently;
- plugin integer encoding matches documented semver;
- package filename/version agree;
- mismatch guards work.

### Thread dispatcher
- wrong thread -> request remains pending, no native invocation;
- designated thread -> exactly one invocation;
- repeated wrong threads -> bounded evidence, no spin;
- timeout/dispatch cap -> anomaly, not arbitrary fallback;
- no same-drain requeue loop.

### Save transaction
- state machine ordering;
- one request cannot invoke twice;
- completion marker required;
- failed/incomplete save remains distinguishable;
- manifest correlates the correct generated file;
- archive routine copies before delete;
- hash mismatch blocks deletion.

### Safety
- low-space guard;
- output-size bound;
- wrong-build/site guard;
- evidence-write failure;
- no console path;
- no protected-parent overwrite path.

Do not represent synthetic passing tests as live qualification.

---

## 28. Live capture boundaries

Allowed within this brief after Stage-A preparation:

- user-managed Vortex deployment of the exact reviewed package;
- launch through the reviewed SFSE path;
- load protected-parent-derived disposable state through normal UI;
- one or more ordinary manual saves for tracing;
- bounded debugger attach/trace;
- one plugin-triggered qualification save if Stage B has established the contract;
- normal exit;
- post-exit archive/hash cleanup;
- crash-tolerant capture when evidence is persisted.

Not allowed:

- console;
- save editing;
- arbitrary memory patches;
- exception suppression;
- unrelated outpost construction;
- completing A1-A2R;
- PR/fork/upstream contact;
- new unapproved third-party code incorporation;
- commit/push/publication.

---

## 29. Stop conditions

Stop the affected stage and report if:

- Save3 parent/backup differ;
- build/hash changes;
- manual-save trace fails to establish a credible call contract;
- save function arguments remain materially unknown;
- plugin-triggered save writes an unexpected file or overwrites an existing save;
- save completion cannot be distinguished from request acceptance;
- output grows unexpectedly;
- free space falls below 40 GB on guarded volumes;
- invoking the save path requires unapproved third-party code;
- cleanup would require unsafe live deletion;
- source save integrity changes unexpectedly.

A crash after complete evidence is not by itself a stop for the research record, but the next attempt requires recovery/review according to current policy.

---

## 30. Success criteria

SOR-EXP-0002A succeeds if it establishes, with evidence:

1. the practical manual-save request path for Starfield 1.16.244.0;
2. initiating execution thread/context;
3. save-manager/object identity and live argument contract;
4. save-name behavior;
5. request versus completion semantics;
6. any relevant save-list/cloud bookkeeping;
7. a defensible designated execution context for a plugin request;
8. whether observer `0.1.0` can create one valid controlled save without console use;
9. how that save can later be archived/removed safely;
10. whether the same context is a promising candidate for resuming `GetWorkshop` work.

It is acceptable for the result to be:

> plugin-triggered native saving is not yet safe/understood.

Do not force Stage C success.

---

## 31. Handoff and review

At completion, stop and return:

1. experiment stage(s) completed;
2. exact observer/tool version(s);
3. manual-save call-path findings;
4. thread map;
5. recovered live argument contract;
6. save completion findings;
7. plugin-save qualification result, if attempted;
8. save-name behavior;
9. archive/delete/bookkeeping findings;
10. SFSE sources consulted and credit/permission updates;
11. third-party code actually incorporated, if any;
12. crash/evidence completeness/target outcome separately;
13. generated save artifacts and hashes;
14. files changed/added;
15. tests/checks and results;
16. unresolved questions;
17. recommended changes before resuming SOR-EXP-0002;
18. `git diff`;
19. `git status --short`;
20. suggested commit message.

Do not commit or push.

---

## 32. Suggested commit message after review

If the work establishes the tooling successfully:

```text
feat(research): map and qualify native save requests
```

If it only produces research findings without a usable save prototype:

```text
docs(research): map native save execution path
```
