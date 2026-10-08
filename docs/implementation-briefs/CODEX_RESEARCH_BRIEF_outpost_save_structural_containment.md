# SOR Research Brief — Structural Containment of Outpost Save Data

## Purpose

Determine **where outpost state lives structurally inside Starfield save files** without turning this task into a general reverse-engineering project for the entire save format.

The central question is:

> **What is the minimal logical serialization footprint required to represent an outpost, and how is that footprint organized inside the save?**

The task should work outward from already-established outpost evidence and stop once the structural neighborhood is understood well enough to support future outpost research.

This is an **offline analysis task only**.

Do not launch Starfield, deploy SFSE, attach a debugger, modify live saves, stage, commit, or push under this brief.

## 1. Scope

The objective is **not** to decode the entire Starfield save format.

The objective is to identify the structural container(s), record family/families, reference mechanism(s), and boundaries that hold the already-known outpost state.

Preferred end states, in order:

1. one bounded logical outpost/workshop region;
2. a small set of bounded logical regions / record families plus a reference/index mapping tying them together;
3. a repeatable cluster of chunks/regions that contains nearly all known outpost-related state and changes predictably with outpost complexity.

A negative finding that outpost state is structurally distributed is acceptable if demonstrated clearly.

## 2. Existing evidence anchors

Use the already-established outpost evidence as the starting point:

- `SOR-001` rename anchor;
- beacon candidate;
- storage candidate;
- extractor candidate;
- solar-array candidate;
- STRONG output-link relationship candidate.

Use the exact durable definitions from the existing corpus reports, findings/state registers, and output-link validation report.

Do not redefine candidates merely because a new interpretation would be convenient.

Also retain the terminology correction:

> Prefer **relationship/collection region** or **relationship region with apparently variable entry content** over prematurely calling the structure a “list”.

The semantic association to output-link state may remain STRONG while the internal container schema remains unresolved.

## 3. Save corpus to use

Use the already archived and verified manual-save corpora:

```text
S0
S0C
S1
S1C
S2
S2C
S3
S3C
S4
S4C
S5
S5C
S6
S6C
S7
S7C

L0
L0C
L1
L1C
L2
L2C
```

Use existing archived copies and manifests.

Do not duplicate raw `.sfs` evidence unnecessarily.

Preserve all existing hashes and provenance.

## 4. Structural levels must remain distinct

Throughout the analysis, distinguish explicitly among:

```text
A. raw .sfs physical offsets
B. compressed stream/chunk boundaries
C. decompressed logical regions / record structures
D. reference relationships between logical records
```

Do not treat physical contiguity in the compressed `.sfs` file as equivalent to logical contiguity.

The project cares most about logical containment, record-family membership, and reference relationships.

## 5. Primary structural questions

For each known outpost anchor, answer as far as the evidence permits:

1. Which compressed stream/chunk contains it?
2. What are that stream's boundaries?
3. What are its compressed and uncompressed sizes?
4. What immediately encloses the candidate after decompression?
5. Is there evidence of a record header?
6. Is there evidence of type/tag, length, count, version, flags, checksum/integrity field, or index/key?
7. Is the candidate part of a repeatable record family?
8. Does the same logical container remain recognizable across saves?
9. Does the candidate move physically while remaining logically identifiable?
10. What parent structure, if any, contains it?

Apply this to `SOR-001`, beacon, storage, extractor, solar array, and output-link relationship.

## 6. Test the bounded-outpost-region hypothesis

Explicitly test:

> Outpost data may occupy one bounded logical region or a small set of related regions.

Do not assume this is true.

Ask whether `SOR-001`, beacon, storage, extractor, solar, and relationship data occur:

- in one compressed stream;
- in one decompressed logical record;
- in adjacent records of one record family;
- in several bounded record families linked by references;
- or in unrelated scattered structures.

If one model fits best, document why.

## 7. Change-density analysis by structural region

Across the controlled save sequence, calculate change density by compressed chunk, decompressed region, and logical record family where possible.

At minimum compare:

```text
S0C -> S1   beacon creation
S1C -> S2   storage placement
S2C -> S3   extractor + solar creation
S3C -> S4   output-link creation
S4C -> S5   rename
S5C -> S6   solar move
S6C -> S7   extractor deletion
L0C -> L1   unlink
L1C -> L2   relink
```

For each chunk/region, measure or summarize:

- absolute size;
- growth/shrinkage;
- bytes changed;
- change density;
- number of candidate records changed;
- whether change persists through adjacent controls.

Also compare no-action controls to estimate background churn.

## 8. Test the large/growable-outpost-region hypothesis

The user hypothesizes that outpost data may be among the largest or most growable save regions, perhaps alongside ship-related state.

Treat this strictly as a hypothesis.

Ask:

- Does one region/chunk grow as outpost complexity increases?
- Does growth correlate with beacon creation, placed-object count, relationship creation, rename metadata, or object deletion?
- Does the same region shrink after deletion?
- Does it remain large across reload/resave?

Do not label a large region "outposts" merely because it is large.

If another obviously large/growable region appears to be ship-related, note it only as a comparison hypothesis. Do not start reverse-engineering ship serialization.

## 9. Header / directory / index investigation

Because large saves require efficient serialization/deserialization, inspect the save header and early structural metadata for evidence of:

- section directory;
- chunk table;
- record counts;
- offset table;
- type table;
- compressed-size table;
- uncompressed-size table;
- reference table;
- integrity/checksum fields;
- versioning/framing.

Do not decode unrelated entries unless necessary.

The key question is:

> Is there an index/directory that tells the game where logical regions or record families live?

If so, determine whether the known outpost-containing regions can be identified through it.

## 10. Save-size control and sparse-state hypothesis

Use the existing evidence to test whether Starfield appears to serialize complete world objects or instead base/reference identity plus only changed/persistent state.

For known placed objects, look for evidence consistent with:

- base-form identity;
- dynamic/persistent reference identity;
- transform;
- workshop/outpost relationship;
- changed fields only.

Do not attempt to decode every field.

## 11. Save-local identifier mapping

Treat compact identifiers such as the previously observed three-byte tokens as a first-class subgoal.

Known behavior includes token remapping across reload/resave while logical object candidates remain recognizable.

Determine whether such tokens appear to map through a reference table, index table, record table, created-object table, persistent-reference table, or other compact-ID mechanism.

The desired bridge is conceptually:

```text
save-local token
    ->
stable serialized reference identity
    ->
dynamic reference and/or FormID
    ->
base-form identity where applicable
```

Do not assume this exact architecture. Test it.

## 12. Relationship to ESM/static identities

Look specifically for evidence connecting candidate outpost objects to:

- ESM FormID;
- base-form identity;
- dynamic reference identity;
- persistent reference identity;
- other stable game identifier.

Distinguish where possible:

```text
"this is a Solid Storage base object"
```

from:

```text
"this is this particular placed Solid Storage instance"
```

Do not broaden into general FormID/save-reference research beyond what is needed for the outpost candidates.

## 13. Reload/resave interpretation

Be explicit:

```text
S4C / L0
```

did not mutate.

It is an immutable original file.

The important comparison is:

```text
L0
    ->
load into Starfield
    ->
runtime reconstruction
    ->
save again
    ->
L0C
```

Any differences between L0 and L0C are therefore differences in a **new serialization of reconstructed runtime state**, not changes to the original save.

## 14. Cross-save logical identity

For each outpost candidate, determine whether logical identity can be preserved even when physical offset changes, token value changes, entry order changes, or compressed chunk offset changes.

If yes, document what invariant permits the match.

Possible invariants include:

- record framing;
- neighboring fields;
- base-form identity;
- reference relationships;
- string/name anchor;
- structural pattern;
- container membership.

Do not rely on literal byte equality alone.

## 15. `SOR-001` as an outpost-level anchor

Use the rename anchor aggressively.

Determine:

- which compressed stream contains `SOR-001`;
- what record/container encloses it;
- whether the old `Kreet Outpost 1` value occupied the same logical structure;
- whether nearby fields look like workshop/outpost identity, beacon reference, location/body reference, object-reference collection, or metadata.

This is one of the strongest candidates for finding an outpost/workshop-level record distinct from individual placed-object records.

## 16. Placed-object family analysis

Determine whether beacon, storage, extractor, and solar appear to belong to the same logical record family or to different families.

Look for repeated framing such as:

```text
[type/tag]
[length]
[reference]
[base identity]
[position]
[state]
```

without assuming exact semantics.

If a repeated placed-object record structure exists, characterize its boundaries.

## 17. Relationship-region containment

For the STRONG output-link candidate, determine:

- which chunk/stream contains it;
- its enclosing logical structure;
- whether it is endpoint-owned, outpost/workshop-owned, a separate relationship region, or a separate relationship/collection region.

Do not call it a list unless actual list framing/count behavior is established.

Look for count changes, length changes, entry-sized changes, endpoint identifiers, and parent identifiers.

## 18. Error containment / bad-data resistance

Look for structures that would allow the game to avoid cascading corruption:

- record lengths;
- section lengths;
- counts;
- type tags;
- versions;
- checksums;
- sentinels;
- compressed-size fields;
- uncompressed-size fields.

Do not assume checksums exist.

The question is:

> What structural framing lets the game know where one serialized unit ends and another begins?

## 19. Stop rule

Stop once Codex can explain, with evidence:

- where the known outpost candidates live structurally;
- what contains them;
- which record families they belong to;
- how they relate across saves;
- how save-local identifiers participate;
- and whether one bounded outpost region exists or a small linked set of regions is required.

Do not continue decoding unrelated adjacent sections after that point.

This task must not become a generalized Starfield save-format project.

## 20. Desired structural models

At the end, classify the evidence against one of these models where possible.

### Model A — Monolithic outpost region

```text
Outpost/workshop record
    ├── name
    ├── location
    ├── beacon
    ├── placed objects
    └── relationships
```

### Model B — Outpost header + placed-object family + relationship family

```text
Outpost/workshop record
    ├── name
    ├── location
    └── references

Placed-object records
    ├── beacon
    ├── storage
    ├── extractor
    └── solar

Relationship region
    └── output link
```

### Model C — Distributed change records tied by reference mapping

```text
change-record families
    +
save-local reference/index tables
    +
outpost/workshop ownership references
```

### Model D — unresolved / another model

If none fit, describe the observed structure without forcing a model.

## 21. Evidence classification

For all conclusions, distinguish:

```text
OBSERVED
INFERRED
HYPOTHESIZED
```

Do not silently promote inference to fact.

## 22. Tooling

Reuse existing corpus-analysis tooling where practical.

Small new offline scripts are acceptable for chunk inventory, stream boundaries, size/growth analysis, change-density mapping, record-framing search, candidate containment, token mapping, reference correlation, and cross-save logical identity.

Keep tooling narrow and inspectable.

Do not build a general save editor or unrelated parsers.

No live debugger work is authorized.

No SFSE deployment is authorized.

## 23. Desired outputs

Produce at minimum:

### A. Structural save map

A bounded map of the save at the level needed for outpost research:

```text
header
chunk/index metadata
candidate outpost-containing chunks
candidate record families
reference tables
```

Do not map unrelated regions in detail.

### B. Outpost-anchor containment table

For each of `SOR-001`, beacon, storage, extractor, solar, and output link, report:

- chunk/stream;
- decompressed region;
- record/container;
- parent/container;
- physical offset;
- logical identity basis;
- cross-save stability.

### C. Chunk/region growth table

Show how candidate regions change in size across `S0 -> S7C` and `L0 -> L2C`, especially as outpost complexity changes.

### D. Change-density table

Identify the chunks/regions most repeatedly affected by deliberate outpost operations.

### E. Reference/token mapping report

Document what is known about compact save-local identifiers and any bridge toward stable game/ESM identities.

### F. Structural-model conclusion

State whether evidence best supports Model A, B, C, or D.

### G. Bounded-region conclusion

Answer directly:

> Is there a bounded, discrete, logically contiguous region that can reasonably be called "the outpost data"?

If not:

> What is the smallest linked set of logical regions required to represent one outpost?

## 24. Success criteria

This task is successful if it establishes one or more of:

- a bounded outpost/workshop region;
- a bounded placed-object record family;
- a bounded relationship/collection region;
- a save-local reference/index mapping;
- a stable logical identity mechanism across reload/resave;
- a reliable set of chunks/regions whose growth tracks outpost complexity.

A clear demonstration that outpost state is distributed across several defined record families is also a successful result.

## 25. Git and artifact policy

Do not stage, commit, or push.

Do not modify raw saves.

Do not track raw `.sfs` files or raw decompressed save blobs unless existing policy explicitly allows it.

Generated summaries/scripts/documentation may be tracked if consistent with project policy.

## 26. Validation

Before returning:

- verify all source evidence hashes remain unchanged;
- verify no raw save/dump/binary became tracked;
- run `git diff --check`;
- validate internal Markdown links if documentation changed;
- inspect `git status --short`;
- record all new tooling and generated outputs.

## 27. Return for review

Return:

1. structural map of the relevant save architecture;
2. chunk/index/header findings relevant to outposts;
3. anchor-containment table;
4. region/chunk growth analysis;
5. change-density analysis;
6. `SOR-001` containing structure;
7. placed-object record-family findings;
8. output-link relationship-region findings;
9. compact-token/reference mapping findings;
10. any bridge to ESM/FormID/base-form/dynamic-reference identity;
11. cross-save logical identity findings;
12. bounded-outpost-region conclusion;
13. best-supported structural model (A/B/C/D);
14. observed vs inferred vs hypothetical distinctions;
15. strongest current interpretation;
16. alternative explanations;
17. smallest next experiment/analysis, if needed;
18. files changed;
19. checks run/results;
20. `git diff`;
21. `git status --short`.

Do not commit or push.

Suggested commit message only if later approved:

```text
research: map structural containment of outpost save data
```
