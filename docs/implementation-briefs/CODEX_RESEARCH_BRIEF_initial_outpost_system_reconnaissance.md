# Codex Research Brief — Initial Outpost-System Reconnaissance

**Repository:** `D:\Projects\starfield-outpost-research\`
**Project:** `gooberpede/starfield-outpost-research`
**Research mode:** bounded static reconnaissance and public prior-art survey
**Live game / debugger execution:** **NOT AUTHORIZED BY THIS BRIEF**
**Date:** 2026-10-06

---

## 1. Purpose

Begin the first substantive research phase for `starfield-outpost-research`.

The project asks:

> **How does Starfield represent, operate, and persist player outposts, and how do those mechanisms interact throughout an outpost's lifecycle?**

This first phase is intended to build a trustworthy map of the outpost system before the first controlled live/save experiment. It must establish the current research environment, identify the static game vocabulary and principal implementation paths, survey relevant public prior work, and produce a prioritized set of runtime/save questions and observation targets.

This is **not** an attempt to reverse-engineer the entire outpost system in one pass.

Do not build an importer, generic dump tool, large SFSE framework, gameplay mod, save editor, or comprehensive parser.

---

## 2. Required reading before work

Read the current repository guidance and durable records first:

```text
AGENTS.md
WORKFLOW.md
THIRD_PARTY_POLICY.md
LICENSING.md
THIRD_PARTY_NOTICES.md
CREDITS.md

docs/CHARTER.md
docs/RESEARCH_STATE.md
docs/EVIDENCE_STANDARD.md
docs/PROVENANCE.md
docs/SOURCES.md
docs/PERMISSIONS.md
docs/DECISIONS.md
docs/PUBLICATION.md
docs/known-facts.md
docs/hypotheses.md
docs/function-register.md
docs/state-register.md
docs/subsystems/README.md
```

Also inspect the repository templates relevant to source records, experiments, findings, and provenance/environment records.

Do not assume that any claim from an earlier conversation or sibling repository is already established here.

---

## 3. Standing-order amendment to make first

Before beginning the research, update the applicable durable policy documents to record the following settled decision.

### 3.1 Evidence value and target survival are separate outcomes

The project prioritizes useful evidence over keeping the game process alive after capture.

The policy must make clear that:

> **A debugger trace or other bounded live capture may be intentionally crash-tolerant. If it is expected to answer important research questions before Starfield exits, a post-capture crash does not invalidate complete evidence collected beforehand. Evidence completeness/scientific value and target-process survival are separate outcomes.**

Use concise wording consistent with the repository's existing evidence and safety rules.

### 3.2 What this does and does not authorize

The amended standing orders should establish that future approved research may include short, high-information, “kamikaze” debugger traces.

It must **not** create blanket authority for arbitrary live debugging.

Future live briefs still need to declare:

- target build and save/sample;
- breakpoint/hook/trace scope;
- expected information;
- finite capture bounds;
- writes or mutations, if any;
- source-save protection;
- evidence flush/persistence behavior;
- process-exit/recovery policy.

A quick crash-producing trace that answers many questions may be preferable to lengthy stable instrumentation that answers little.

However:

- preserve protected/source saves;
- do not treat a pre-evidence crash as success;
- do not conceal debugger-induced failures;
- record evidence completeness, scientific result, and target outcome separately;
- unexpected corruption outside the declared experiment boundary remains a stop condition.

### 3.3 Documents to consider

At minimum review/update:

```text
AGENTS.md
WORKFLOW.md
docs/EVIDENCE_STANDARD.md
docs/DECISIONS.md
docs/RESEARCH_STATE.md
```

Update only those actually needed. Avoid redundant policy prose.

---

## 4. Research questions for this phase

Answer as far as static/public evidence genuinely permits:

1. What static game records, scripts, native types/functions, keywords, actor values, globals, form lists, quests, aliases, components, or other definitions appear to constitute the outpost system?
2. What appears to define an outpost's identity and workshop membership?
3. What static mechanisms appear to govern beacon/outpost creation, placed-object membership and lifecycle, construction/removal, power, resource extraction, storage/local connections, manufacturing, cargo links, crew/robot assignment, relevant time/loading behavior, and persistence/reconstruction?
4. Which operations are implemented in Papyrus versus native code?
5. Which native implementation paths are the best candidates for later runtime observation?
6. Which parts of the system have already been investigated by publicly visible mods, repositories, technical documentation, or research?
7. What can those external sources tell us, and what remains unverified?
8. What is the highest-information first live/save experiment after this reconnaissance?

Do not force conclusions where only names, call relationships, or suggestive strings are available.

---

## 5. Phase A — establish the project-specific environment baseline

The sibling `starfield-reference-handles` project may be consulted as an **environment/tooling lead**, not as proof of this project's baseline.

The user reports that the current environment includes Ghidra, Ghidra debugger capability, pinned current `Starfield.exe`, pinned current `CreationKit.exe`, x64dbg, SFSE, capability to build live-observer plugins, xEdit, live Starfield play, ability to create new controlled save files, and protected `Save2` from the reference-handles work.

Verify what can be verified locally without launching the game.

Record a new project-specific environment/provenance baseline covering, where available:

```text
Starfield.exe
CreationKit.exe
game/CK versions
file sizes
SHA-256 hashes
static image bases
Ghidra version
relevant Ghidra project/program identities
SFSE version/install identity
x64dbg version/path
xEdit version/path
relevant master/plugin set
operating system / architecture
```

If an item cannot be verified, record `UNKNOWN` or `NOT CHECKED`.

Do not simply copy values from `starfield-reference-handles`.

Cross-check against the sibling project where useful and explicitly say whether each item is independently reverified, merely consistent with the sibling project, or unavailable.

Do **not** launch Starfield or Creation Kit merely to fill a baseline field.

---

## 6. Phase B — public prior-art and mod/repository survey

This is a required research phase.

### 6.1 Goal

Identify publicly accessible mods, repositories, technical documents, discussions, or research that meaningfully interact with or explain Starfield outpost systems.

The purpose is to discover terminology, known native/script interfaces, relevant forms/keywords/actor values, functions/types/offsets, runtime observations, save/persistence observations, useful experimental methods, known limitations/failure modes, and candidate investigation leads.

### 6.2 Sources to search

Search broadly enough to catch relevant work, including where appropriate:

- GitHub and other public source repositories;
- Nexus Mods pages and publicly exposed documentation/source links;
- SFSE/CommonLibSF-related public material;
- xEdit scripts or technical documentation;
- Creation Kit documentation;
- public mod documentation/changelogs;
- public reverse-engineering writeups or technical discussions.

Candidate leads already present in `docs/SOURCES.md` must be rechecked rather than assumed correct.

Also search for outpost-adjacent terminology, including likely Bethesda/internal naming such as:

```text
outpost
workshop
beacon
cargo link
extractor
manufacturer
resource link
power
crew assignment
robot
production
storage
linked ref
workshop object
```

Use discovered terminology to broaden the search where justified.

### 6.3 Mandatory third-party boundary

Follow `THIRD_PARTY_POLICY.md` strictly.

**Allowed:**

- read publicly visible pages and source that authors have made publicly accessible;
- inspect public repository files through normal read-only access;
- record names, versions, commit hashes, URLs, licence notices, authorship, and factual/research claims;
- summarize what a source says;
- use a third-party finding as a lead for independent verification;
- quote only very small portions when technically necessary and lawful, with attribution.

**Not authorized:**

- forking;
- opening pull requests;
- contacting authors;
- filing issues/comments;
- copying third-party code into this repository;
- adapting/porting/reimplementing third-party code from source;
- vendoring dependencies;
- copying substantial text, diagrams, datasets, templates, tests, or binary formats;
- treating a public licence as automatic user approval for reuse.

A public repository being readable means it may be **consulted**. It does not mean its implementation may be reused.

### 6.4 Attribution and provenance requirements

For each source that materially influences the research, create/update an `SOR-S-` record with author/project, exact title/repository/page, URL, commit/tag/version where possible, access date, visible licence/rights information, what was inspected, what claim/terminology/method/lead was obtained, whether it was independently verified, affected findings/questions, and whether future reuse would require a separate permission decision.

Credit substantive contributions at the point where they influence a report or finding.

Update as appropriate:

```text
docs/SOURCES.md
CREDITS.md
THIRD_PARTY_NOTICES.md
docs/PERMISSIONS.md
```

Do not add ceremonial credits for sources that did not influence the work.

### 6.5 Evidence-status rule for external claims

External claims remain `SOURCE-REPORTED` or equivalent source-specific notes until this project independently validates them.

If independently reproduced later, preserve both facts:

```text
original source reported X
this project independently reproduced X under Y conditions
```

Independent reproduction does not erase credit.

---

## 7. Phase C — xEdit / static game-data reconnaissance

Use xEdit and/or existing static ESM inspection methods to identify the principal records supporting outposts.

The purpose is a **map**, not an exhaustive export of the entire game database.

Investigate likely relevant record types and relationships for:

- outpost beacon/workshop;
- constructible/build-menu definitions;
- workshop categories;
- placed outpost objects;
- extractors;
- storage;
- manufacturers/fabricators;
- cargo-link structures;
- power generation/distribution;
- resource definitions used by outpost systems;
- crew/robot assignments;
- relevant quests/aliases;
- relevant keywords;
- actor values;
- globals;
- form lists;
- script attachments/properties;
- components or native-backed definitions.

Record exact FormIDs/EditorIDs/source plugins where useful.

If a small project-authored xEdit export script is necessary to avoid manual transcription, it may be created **only if it is genuinely small and directly serves this reconnaissance**.

Do not copy an existing third-party xEdit script.

Any new script must state its input scope, output schema, read/write behavior, xEdit version, and whether it mutates plugin data. Default must be read-only.

Do not perform a huge indiscriminate ESM dump.

---

## 8. Phase D — vanilla script / exposed-interface map

Map the relevant vanilla script layer using the game's legitimately accessible script sources or declarations available in the installed development environment.

Identify script names, owning objects/forms, significant properties, important events, native calls, linked-reference relationships, workshop/object APIs, cargo-link APIs, resource/production APIs, assignment APIs, and lifecycle/save/load-relevant events.

Do not import a third-party mirror of Bethesda scripts into the repository.

If a public mirror is used to locate a lead, credit it as a discovery aid, but independently inspect the authoritative/local material where possible before promoting any claim.

For each important operation, classify it as:

```text
SCRIPT-IMPLEMENTED
NATIVE-DECLARED
MIXED
UNKNOWN
```

Do not infer native implementation details solely from a Papyrus declaration.

---

## 9. Phase E — Ghidra static reconnaissance

Use the existing analyzed/pinned programs for:

```text
Starfield.exe
CreationKit.exe
```

Prefer read-only analysis/export.

Do not modify Ghidra symbols, function names, comments, types, bytes, or analysis state unless a later brief explicitly authorizes it.

### 9.1 Creation Kit

Use `CreationKit.exe` where it offers useful strings, RTTI/type names, editor-visible terminology, validation/construction pathways, or native names/structures that illuminate corresponding runtime concepts.

Do not assume the CK implementation is identical to retail runtime behavior.

### 9.2 Starfield.exe

Identify the first useful layer of native implementation behind the static/script map.

Prioritize:

1. workshop/outpost ownership or membership;
2. outpost/beacon creation and destruction;
3. placed workshop-object lifecycle;
4. local resource/storage linking;
5. cargo-link endpoint pairing and transfer;
6. production/extraction;
7. assignment;
8. save/load or reconstruction paths implicated by the above.

For candidate functions/types record original Ghidra/native name if present, static address, RVA where applicable, executable build/hash, strings/RTTI/xrefs/callers/callees supporting the association, relevant parameters/fields only where supported, proposed semantic alias, confidence, and unresolved alternatives.

Do not bulk-rename functions or recursively export huge call graphs.

Create only narrowly scoped exports that answer a concrete mapping question.

### 9.3 Persistence leads

Actively note—but do not fully reverse-engineer in this phase—candidate paths involving:

```text
serialization
save/load
change forms
reference reconstruction
workshop reconstruction
script state restoration
linked-reference restoration
inventory persistence
runtime-generated reference creation
```

Record why each is a lead.

Do not label a function “the outpost serializer” without direct evidence.

---

## 10. Phase F — build the initial subsystem map

Create/update durable subsystem documentation under `docs/subsystems/`.

The initial map should cover at least:

```text
outpost identity / beacon / workshop membership
construction and placed-object lifecycle
power
resource extraction
storage and local links
manufacturing
cargo links
crew / robots / assignments
time / loading-state behavior
persistence / reconstruction
```

For each subsystem record static forms/data, scripts, native candidates, external research leads, known interfaces, state/relationship candidates, persistence leads, open questions, and best proposed runtime observation points.

Do not treat every subsystem as equally understood.

---

## 11. Registers and durable documentation

Update only when evidence warrants it.

### `docs/function-register.md`

Add `SOR-FN-` records for genuinely implicated functions/operations. Do not register every function encountered.

### `docs/state-register.md`

Add `SOR-ST-` records only for state/relationship candidates concrete enough to identify. Use `UNKNOWN` where persistence is not established.

### `docs/known-facts.md`

Promote only decisive findings supported by this project's evidence. Static mapping alone can support a narrowly scoped `STATIC` finding, but not a runtime or persistence claim.

### `docs/hypotheses.md`

Add discriminating hypotheses/questions suggested by the reconnaissance. Preserve alternatives.

### `docs/PROVENANCE.md`

Record the project-specific environment baseline and important static-analysis/tool provenance.

### `docs/RESEARCH_STATE.md`

Update the current state and identify the exact recommended next experiment.

### `docs/DECISIONS.md`

Record the crash-tolerant debugger policy decision and any other genuinely settled project-level decision.

---

## 12. Required focused report

Create:

```text
docs/experiments/initial-outpost-system-reconnaissance.md
```

Suggested structure:

```text
# Initial Outpost-System Reconnaissance

## Scope and baseline
## Methods and sources
## Third-party prior-art survey
## Static game-data map
## Script/interface map
## Creation Kit native leads
## Starfield native leads
## Persistence leads
## Initial subsystem map
## Established static findings
## Strong interpretations
## Provisional interpretations
## Open questions
## Recommended first live/save experiment
## Candidate observation/breakpoint targets
## Remaining permission/rights issues
## Files/evidence produced
```

Clearly distinguish:

```text
PROJECT-VERIFIED STATIC
SOURCE-REPORTED
STRONG INTERPRETATION
PROVISIONAL
OPEN
```

Do not use a stronger evidence label merely because multiple public sources repeat the same claim.

---

## 13. Design the first live/save experiment, but do not execute it

The report must end with a concrete recommendation for the first controlled live/save experiment.

The preferred starting question is:

> **What runtime object or relationship is authoritative for an outpost/workshop, and how are placed objects associated with it?**

However, the reconnaissance may recommend a better question if the evidence clearly points elsewhere.

The proposed experiment should probably use a deliberately minimal save series such as:

```text
A0 — before creating an outpost
A1 — beacon only
A2 — beacon + one ordinary storage object
A3 — beacon + one extractor
A4 — extractor connected to storage
```

This exact sequence is **not mandatory** if static reconnaissance demonstrates a better discriminating sequence.

Specify the starting save/play state, controlled actions, runtime values/relationships to observe, which SFSE probe/debugger breakpoint/combination would yield the most information, save comparisons, likely evidence artifacts, discriminating outcomes, and whether a crash-tolerant trace would be worthwhile.

Do not launch the game, deploy a plugin, attach a debugger, create these saves, or alter Save2 under this brief.

---

## 14. Scope boundaries

Do **not**:

- launch Starfield;
- launch Creation Kit for interactive/live testing unless required solely for already-authorized static file inspection and no game state is affected;
- attach Ghidra debugger or x64dbg to Starfield;
- deploy/build an SFSE observer except tiny offline scaffolding absolutely required for analysis—and preferably do not build one yet;
- modify any save;
- use protected Save2;
- create live experimental saves;
- modify plugins/ESMs;
- edit Ghidra analysis state;
- patch executable code;
- perform broad memory scans;
- implement an outpost importer;
- implement a production save dumper/parser;
- fork repositories;
- submit PRs/issues/comments;
- contact mod authors;
- reuse third-party code;
- silently adopt third-party terminology or findings;
- commit, push, tag, publish, or change repository visibility.

If a tool or source becomes necessary but falls outside these bounds, document why and stop that affected path.

---

## 15. Success criteria

This phase succeeds if it leaves us with:

1. a verified project-specific environment baseline sufficient for later reproducible work;
2. an attributed public prior-art/source register covering meaningful existing outpost-related work;
3. an initial static map of the outpost subsystem;
4. a script/exposed-interface map;
5. a bounded set of CK and Starfield native candidates;
6. an initial set of persistence leads;
7. populated function/state registers only where justified;
8. durable separation between external reports, project evidence, interpretation, and hypothesis;
9. the crash-tolerant debugger policy durably recorded;
10. a concrete, high-information first live/save experiment ready for review.

A large number of addresses, repositories, or files is not success by itself. The goal is to reduce uncertainty and identify the **best next experiment**.

---

## 16. Validation

Before completion:

- verify all new/changed Markdown links;
- run `git diff --check`;
- check UTF-8 / line-ending expectations;
- inspect `git status --short`;
- confirm no proprietary executable, Ghidra database, raw save, decompressed save, memory dump, private correspondence, or unreviewed bulk artifact became tracked;
- confirm every materially used third-party source has provenance and credit;
- confirm no third-party code was copied/adapted;
- confirm no fork/PR/upstream communication occurred;
- confirm no live run occurred;
- confirm policy changes do not accidentally authorize unrestricted destructive debugging;
- confirm no source-reported claim was promoted beyond its evidence.

If generated evidence is large, keep it local unless a small reviewed subset is necessary for durable support.

---

## 17. Final response

Stop after this reconnaissance.

Return:

1. concise summary of what was established;
2. environment baseline status;
3. prior-art sources reviewed and the most useful leads;
4. principal outpost subsystem map;
5. most important script/native candidates;
6. persistence leads;
7. established findings and confidence;
8. unresolved questions;
9. recommended first live/save experiment;
10. whether a crash-tolerant debugger trace is recommended for it and why;
11. third-party permission/credit status;
12. files added/changed;
13. tests/checks actually run and their results;
14. `git diff`;
15. `git status --short`;
16. suggested commit message.

Do **not** commit, push, deploy, launch the game, or begin the recommended live experiment.

---

## 18. Suggested commit message

If the reviewed diff is accepted later:

```text
docs(research): map initial outpost system
```
