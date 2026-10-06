# Codex Research Brief — SOR-EXP-0002 Outpost Membership, Reload, and Location Capture

**Repository:** `D:\Projects\starfield-outpost-research\`  
**Project:** `gooberpede/starfield-outpost-research`  
**Experiment:** `SOR-EXP-0002`  
**Date:** 2026-10-06  
**Current authority:** preparation, implementation, and offline validation only  
**Live execution:** **NOT AUTHORIZED UNTIL SEPARATE USER APPROVAL AFTER REVIEW**

## 1. Purpose

Prepare the first controlled live/save experiment for `starfield-outpost-research`.

Primary question:

> **What runtime object or relationship identifies an outpost/workshop and associates an ordinary placed storage object with it, and what happens to that relationship across save/reload?**

Secondary question:

> **How is the outpost/beacon surface position represented at runtime, including any stable planetary/body-relative, map, worldspace, cell-local, or latitude/longitude-like coordinates?**

This phase connects static definitions to live reference identities and workshop membership, controlled save checkpoints, reload, and restored/reconstructed runtime state.

It is not yet an extractor/output-link experiment, cargo-link experiment, general outpost dumper, save parser, or gameplay-mod implementation.

## 2. Required reading

Read before substantive work:

```text
AGENTS.md
WORKFLOW.md
THIRD_PARTY_POLICY.md
docs/CHARTER.md
docs/RESEARCH_STATE.md
docs/EVIDENCE_STANDARD.md
docs/PROVENANCE.md
docs/DECISIONS.md
docs/SOURCES.md
docs/PERMISSIONS.md
docs/function-register.md
docs/state-register.md
docs/known-facts.md
docs/hypotheses.md
docs/subsystems/initial-map.md
docs/experiments/initial-outpost-system-reconnaissance.md
docs/experiments/evidence/initial-reconnaissance/README.md
```

The static reconnaissance and committed records are the evidence baseline. Do not strengthen their claims without new evidence.

## 3. User-provided experimental baseline

The user created this research save:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\Save3_D6036588M417474696C61204B6972616C79_000214_20261006013428_3_0_4.sfs
```

User-reported state:

- player character is on **Kreet**;
- player is positioned exactly at a buildable surface site;
- **no outpost has yet been constructed**;
- enough materials are present for one beacon, one ordinary solid storage container, one solid extractor, and one solar array;
- a backup copy already exists under `.local-work/savegames/`.

User-reported expected construction budget:

```text
Adaptive Frame x3
Aluminum      x10
Beryllium     x2
Copper        x3
Iron          x11
Tungsten      x2
```

Treat these quantities as expected budget, not an engine finding.

### Autosave configuration

User reports:

```text
Save on Rest   = disabled
Save on Wait   = disabled
Save on Travel = disabled
Save on Pause  = disabled
```

No in-game option to disable exit saves was found.

Treat any exit save as an **incidental artifact**:
- record it if produced;
- hash/copy it if useful;
- do not use it as a primary checkpoint;
- do not confuse it with A0/A1/A2;
- do not delete it merely to tidy the save directory.

Do not silently change save settings.

## 4. Two-gate execution model

### Gate A — AUTHORIZED NOW

Codex may:

- inspect repository and local environment;
- hash/register Save3 and its backup;
- compare those two copies byte-for-byte;
- inspect save-directory metadata without modifying save files;
- create project-authored instrumentation/tooling;
- build instrumentation offline;
- prepare deployment packages without installing them;
- create debugger scripts/configuration offline;
- inspect existing Ghidra state read-only;
- perform static analysis needed to identify coordinate or `GetWorkshop` observation points;
- create sample/checkpoint manifests;
- create an exact operator run card;
- run offline tests;
- update durable planning/provenance records describing the prepared experiment.

### Gate B — NOT AUTHORIZED YET

Until the user explicitly approves the reviewed preparation, do **not**:

- deploy/install instrumentation;
- change active mod/plugin configuration;
- launch Starfield;
- load Save3;
- create A0/A1/A2 saves;
- attach any debugger;
- invoke the console;
- modify any `.sfs`;
- execute any live hook/probe;
- terminate or deliberately crash the game;
- copy newly generated live saves into the research workspace;
- begin post-live save comparison.

At the end of Gate A, stop and return a review package.

## 5. Protect and register Save3

Locate:
1. the supplied original Save3;
2. the backup under `.local-work/savegames/`.

Do not alter either file.

Record for both:
- exact local path in local-only evidence;
- filename;
- size;
- SHA-256;
- last-write timestamp.

Compare bytes. Expected:

```text
original SHA-256 == backup SHA-256
```

If they differ, stop the path that assumes identity and report the mismatch.

Allocate an appropriate `SOR-SAMPLE-` record for the pristine parent. Durable prose should use the neutral sample ID.

Record:

```text
planet/body: Kreet (USER-REPORTED until independently confirmed)
outpost: none (USER-REPORTED until live-confirmed)
buildable-site position: USER-REPORTED
parent role: immutable pre-outpost experiment baseline
raw save publication status: LOCAL-ONLY
```

## 6. No-console rule

The primary experiment must use **ordinary in-game menu saves**, not `save <name>` or any console command.

Reasons:
- minimize variables;
- console use may alter Developer Mode / achievement-related state;
- console state is a worthwhile separate persistence question.

Do not use the console merely to force names.

Logical sample IDs will be assigned externally.

The later console/Developer Mode experiment is out of scope except as a follow-up note. Do not locate, clear, reset, or patch achievement/Developer Mode state here.

## 7. Planned checkpoint sequence

### Parent

```text
Save3
```

Immutable pristine parent.

### A0 — loaded baseline

After loading Save3 and reaching the defined settled checkpoint:

```text
SOR-SAMPLE-EXP0002-A0
```

Create an ordinary manual/menu save.

No outpost constructed.

### A0C — no-action control

Without deliberately changing outpost state:

```text
SOR-SAMPLE-EXP0002-A0C
```

Create a second ordinary manual/menu save.

Record unavoidable movement/UI activity between A0 and A0C.

### A1 — beacon only

Construct exactly one outpost beacon.

Do not construct storage, extractor, power, crew, robot, manufacturer, cargo link, transfer container, or another outpost object.

After the defined settling condition:
- capture beacon/runtime identities;
- capture workshop/member relationship information;
- capture location/coordinate information;
- create ordinary menu save `SOR-SAMPLE-EXP0002-A1`.

### A1C — beacon no-action control

Without deliberately changing outpost state, create `SOR-SAMPLE-EXP0002-A1C`.

### A2 — beacon + ordinary solid storage

Construct exactly one ordinary solid storage container selected by the reconnaissance/run card.

Do not construct extractor or solar array yet.

Capture:
- beacon;
- storage reference;
- `GetWorkshop()` result;
- owned/resource subset query outputs if narrowly useful;
- relevant positions/coordinate domains.

Create ordinary menu save `SOR-SAMPLE-EXP0002-A2`.

### A2R — reload A2

Reload A2 through normal UI.

Do not rebuild or move anything manually.

After load settles, repeat the runtime checkpoint and compare logical identities versus new pointers/handles. Capture coordinates again.

If useful, create a fresh ordinary post-reload save `SOR-SAMPLE-EXP0002-A2R`.

The run card must state whether A2R denotes the runtime reload checkpoint, a new post-reload save, or both.

### Deferred stages

Do not execute without separate approval:

```text
A3 — add extractor + solar array
A4 — connect extractor -> storage
```

## 8. Instrumentation objective

Build the **smallest project-authored observer needed**. Do not build a generic outpost framework.

At explicit checkpoints record, where technically available:

### Session/environment
- UTC/local timestamp;
- checkpoint ID;
- game version/build;
- loaded Starfield module base;
- instrumentation build/hash;
- relevant loaded module/plugin identity;
- player location/loading state if exposed.

### Selected reference identity

For beacon and storage independently:
- logical role;
- base FormID/base form identity;
- reference FormID if available;
- runtime pointer/address;
- reference handle if available;
- current location;
- cell;
- worldspace;
- loaded/unloaded state if exposed;
- position and rotation.

Do not collapse these into one ID.

### Workshop relationship

For each selected reference where valid:
- `GetWorkshop()` result;
- result FormID/reference identity;
- result pointer;
- result handle if available;
- explicit null/no-result state;
- invocation order/timestamp.

If owner/resource subset queries are used:
- record which API produced each list;
- do not call either exhaustive membership unless proven;
- cap output to avoid a broad dump.

### Relationships

If cheaply exposed:
- selected linked references relevant to membership;
- keyword/location values relevant to the question.

Observer calls may affect caches/scheduling. Log each invocation. Avoid background polling; prefer explicit one-shot checkpoints.

## 9. Planetary/outpost coordinate research

This is required.

### Static preparation

Inspect current CK/Starfield static material only far enough to identify promising APIs/fields/types/strings/functions around:

```text
latitude
longitude
planet coordinates
surface coordinates
planet map
landing site
planetary location
biome map position
worldspace
cell coordinates
planet/body transform
```

The user's recollection that CK may expose latitude/longitude is a **lead**, not a fact.

Do not expand into general planetary-generation reverse engineering.

### Live capture design

Prepare to capture cheap coordinate domains available from ordinary reference/location APIs, including as applicable:

```text
reference transform XYZ
cell-local XYZ
worldspace XYZ
planet/body-relative XYZ
surface-map coordinates
latitude / longitude
other planet-surface coordinates
```

Do not assume equivalence.

At A1, A2, and A2R compare:
- beacon position;
- storage position relative to beacon;
- cell/worldspace identity;
- any body-relative/map/lat-long values;
- pointer/handle changes versus stable spatial values.

A stable value after reload is not automatically `PERSISTED`; it may be reconstructed or derived.

## 10. SFSE implementation requirements

If SFSE is used:

- write new project-authored code;
- do not copy/adapt sibling reference-observer code;
- consulting sibling architecture is only a provenance lead;
- no unapproved third-party dependency;
- build against verified current game/SFSE baseline;
- document compiler/build environment and hashes;
- produce an installable package **without deploying it** during Gate A;
- include an experiment-specific guard/configuration where practical;
- keep output local/ignored;
- persist checkpoint records robustly enough to survive a later crash;
- include checkpoint IDs and terminal completion markers;
- bound file growth.

If SFSE is not the cheapest route, justify the alternative.

## 11. Debugger preparation

Prepare, but do not execute, the smallest trace needed for the native `GetWorkshop` path.

Current static targets:

```text
GetWorkshop callback:
    static VA 0x142073cf0
    RVA       0x02073cf0

tail target:
    static VA 0x140517d60
```

Future live trace must:
- resolve runtime ASLR base;
- validate target bytes against pinned executable;
- validate calling convention/arguments;
- identify the selected storage reference where feasible.

Desired evidence:

```text
thread ID
runtime RIP/site
module base
RCX
RDX
R8
R9
R8 object identity where resolvable
[R8 + 0xC8]
runtime value corresponding to static global 0x145f0b3d8
key/form/symbol resolution if possible
arguments entering 0x140517d60
lookup result / return value
caller / return provenance
selected storage identity
returned workshop identity
```

Nearby memory/type observations may be added only when narrowly justified.

No huge memory dump.

Prepare a default bound such as:

```text
selected operation only
OR <= 100 matching hits
OR <= 5 seconds armed
```

whichever comes first.

Crash-tolerant interpretation:

```text
evidence completeness: COMPLETE
scientific result: SUCCESS
target outcome: CRASHED
```

can still be a successful experiment.

A pre-flush crash is not success.

Do not prepare a method dependent on arbitrary game-byte patches, gameplay register changes, exception suppression, long stepping, hidden retries, or forced termination as normal completion. If debugger control intrinsically needs narrowly scoped context changes, identify them explicitly for review.

## 12. Save checkpoint archive plan

Prepare a machine-readable manifest containing:

```text
SOR-SAMPLE ID
logical checkpoint
parent sample
actual Starfield filename
creation timestamp
size
SHA-256
game build
plugin/module profile
player/body/location state
observer checkpoint IDs
operator actions since parent
incidental save artifacts
publication classification
```

Never overwrite Save3 or its backup.

After future live execution and known game exit/crash state, copy new `.sfs` checkpoints into ignored local research storage. Do not move/delete originals automatically. Hash source and copy.

If an exit save appears:
- register as incidental;
- record which checkpoint/session produced it;
- do not rename into A0/A1/A2;
- do not use as a no-action control unless later justified.

## 13. Operator run card

Create an exact user-facing run card. It must minimize manual transcription and specify:
- preflight;
- save to load;
- launch path;
- observer readiness;
- checkpoint trigger;
- build action;
- save action;
- completion marker;
- reload step;
- stop condition.

Do not require the user to identify pointers, transcribe registers, operate Ghidra, diff saves, or use console commands.

Construction sequence:

```text
A0/A0C: build nothing
A1/A1C: place only the beacon
A2: add one ordinary solid storage container
A2R: reload A2; rebuild nothing
```

Extractor and solar array remain unused in this phase.

Unexpected events must be reported, not silently corrected:
- accidental save;
- exit save;
- autosave despite settings;
- accidental object movement/placement;
- resource shortage;
- NPC/combat interruption;
- observer failure;
- wrong object definition;
- crash;
- UI anomaly;
- profile mismatch.

## 14. No-action controls and timing

A0/A0C and A1/A1C are required.

Define a simple consistent settling rule, e.g.:
- observer ready;
- player stationary;
- build menu closed;
- console closed;
- no deliberate waiting/sleeping/travel;
- short fixed real-time settling interval only if necessary.

Record elapsed real/game time where available.

No-action controls characterize background save variation; they do not prove bitwise determinism.

## 15. Save-format analysis boundary

Gate A may prepare offline comparison tooling but must not semantically inspect/modify Save3 beyond hashing and ordinary metadata unless necessary to verify container readability without semantic claims.

Later save comparison may establish:
- container/file differences;
- compressed/decompressed size changes;
- background versus repeatable changing regions;
- candidate correlations.

Do not label changing bytes as workshop ID, reference handle, coordinate, achievement flag, or outpost record without independent mapping evidence.

Do not modify any save.

## 16. Console / Developer Mode follow-up

Create only a backlog/follow-up note.

Later experiment should branch from pristine Save3 and distinguish:

```text
console never opened
console opened/closed without deliberate command
console command executed
```

Do not execute console, force save names, clear/reset achievement state, or patch saves here.

## 17. Gate-A validation

Before handoff:

### Baseline
- Save3 original exists;
- backup exists;
- bytes/hashes match;
- neither changed;
- executable/SFSE baseline still matches SOR-ENV-0001 or discrepancy reported.

### Tooling
- build succeeds;
- tests succeed;
- wrong-build guard tested where practical;
- output-path guard tested;
- checkpoint schema validated;
- selected-reference filtering tested offline/synthetically where possible;
- flush/completion-marker behavior tested;
- output bounded;
- no unexpected network/dependency download.

### Debugger preparation
- target bytes reconfirmed against pinned Starfield.exe;
- runtime-base resolution logic tested offline/synthetically;
- record schema validated;
- no live attach.

### Repository
- `git diff --check`;
- Markdown/internal links;
- UTF-8/line endings;
- `git status --short`;
- proprietary binaries/raw saves/build outputs remain untracked;
- no third-party code incorporated;
- no fork/PR/upstream communication;
- no deployment;
- no game launch.

## 18. Required durable outputs from Gate A

Create/update only where justified:

```text
docs/experiments/SOR-EXP-0002-outpost-membership-reload-location.md
docs/experiments/evidence/<exp0002-index>/README.md
docs/PROVENANCE.md
docs/RESEARCH_STATE.md
docs/DECISIONS.md
```

Update function/state/hypothesis registers only if preparation establishes new static facts.

Document any project-authored observer, debugger capture script, sample-manifest helper, or coordinate-inspection helper.

Do not claim live validation for offline-only tests.

## 19. Experiment document contents

Include:

```text
## Question
## Baseline
## Protected parent sample
## Checkpoint/sample plan
## Observer design
## Identity fields
## Workshop query plan
## Coordinate-domain plan
## No-action controls
## Debugger fallback plan
## Crash-tolerant outcome model
## Save-copy/hash plan
## Exit-save treatment
## Console exclusion / later follow-up
## Operator run card
## Risks and stop conditions
## Offline validation
## Live execution gate
## Expected discriminating outcomes
```

Keep planned and executed state unmistakable.

## 20. Scientific success criteria for future live run

The eventual live run should answer or narrow:

1. What does `GetWorkshop` return for beacon and ordinary storage?
2. Which identities remain stable across A2 -> A2R: FormID, handle, pointer, workshop result identity?
3. Do owner/resource subset queries include the selected storage, and what do omissions mean?
4. Which coordinate domains identify the beacon/outpost location?
5. Which coordinate values remain stable after reload?
6. Is workshop relationship preserved/reconstructed after reload?
7. Which unresolved questions specifically require the native debugger trace?
8. What save differences exceed no-action background controls?

A crash is neither success nor failure by itself.

## 21. Stop conditions during preparation

Stop the affected path and report if:
- original/backup Save3 differ;
- original Save3 changes unexpectedly;
- executable identity differs from SOR-ENV-0001;
- instrumentation requires unapproved third-party code;
- instrumentation cannot be bounded to explicit checkpoints;
- coordinate work expands into unrelated planetary-generation research;
- debugger preparation requires unapproved target modification;
- build/deployment would alter unrelated mods or Vortex state;
- a required live assumption cannot be tested without launching the game.

Continue unrelated authorized preparation where safe.

## 22. Final Gate-A response

Stop before deployment/live execution and return:

1. Save3 parent/backup integrity result;
2. allocated sample/environment IDs;
3. instrumentation design and files;
4. observer output schema;
5. coordinate domains prepared for capture;
6. debugger target/capture design;
7. exact crash-tolerant bounds;
8. sample manifest design;
9. exact operator run card;
10. offline test results;
11. known limitations;
12. any decisions still needed before live execution;
13. files added/changed;
14. `git diff`;
15. `git status --short`;
16. suggested commit message(s).

Explicitly state:

```text
LIVE EXECUTION NOT YET PERFORMED
DEPLOYMENT NOT YET PERFORMED
SAVE3 NOT LOADED OR MODIFIED
DEBUGGER NOT ATTACHED
```

Do not proceed to Gate B until explicit user approval after review.

## 23. Gate B — future authority template

After review, separate user approval may authorize:
- deployment of the exact reviewed instrumentation package;
- launching Starfield with the reviewed launch path;
- loading Save3;
- user-performed A0/A0C/A1/A1C/A2/A2R sequence;
- checkpoint capture;
- normal menu saves;
- copying/hashing resulting samples after session;
- optionally a separately confirmed bounded debugger trace after save/reload checkpoints are secure.

Any material change to plugin binary/hash, configuration, save parent, game build, load order/profile, debugger target, capture bounds, or operator sequence must be surfaced before execution.

## 24. Suggested commit message

If Gate-A preparation is accepted:

```text
feat(research): prepare outpost membership live capture
```

If changes are overwhelmingly documentation/tooling rather than executable instrumentation, choose the closest conventional type and explain the choice.
