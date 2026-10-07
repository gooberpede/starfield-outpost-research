# SOR Research Brief — Manual Save Corpus Archival and Differential Analysis (S0–S7C)

## Purpose

Resume the Starfield Outpost Research programme using the approved primary path:

> **manual incremental/control saves + offline differential save analysis**

This task is deliberately **offline-save-analysis only**. Do not launch Starfield, deploy the observer, attach a debugger, or resume native-save instrumentation under this brief.

The immediate goals are:

1. create verified project-local copies of the manually generated save corpus;
2. produce a durable manifest and experimental sequence record;
3. characterize background/no-action save churn;
4. identify save regions/records/structures that correlate with deliberate outpost changes;
5. use strong anchors such as the outpost rename, object movement, output-link creation, and object deletion to begin locating persistent outpost state.

Do **not** assume this pass must fully decode the Starfield save schema. A successful result may simply narrow the search to candidate regions/records and establish repeatable correlations for later experiments.

## 1. Source saves

The live originals are currently in:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\
```

The user intends to leave them there temporarily because Starfield saves are Steam-cloud-managed and eventual cleanup should be performed through the game.

Create **copies only** in:

```text
.local-work/savegames/
```

Do not move, delete, rename, or alter the live originals.

The corpus is:

```text
S0  - no outpost
Save4_D6036588M417474696C61204B6972616C79_000215_20261007082316_3_0_4.sfs

S0C - no-action control
Save5_D6036588M417474696C61204B6972616C79_000215_20261007082336_3_0_4.sfs

S1  - beacon
Save6_D6036588M417474696C61204B6972616C79_000216_20261007082418_3_0_4.sfs

S1C - no-action control
Save7_D6036588M417474696C61204B6972616C79_000216_20261007082433_3_0_4.sfs

S2  - solid storage
Save8_D6036588M417474696C61204B6972616C79_000217_20261007082516_3_0_4.sfs

S2C - no-action control
Save9_D6036588M417474696C61204B6972616C79_000217_20261007082535_3_0_4.sfs

S3  - iron extractor + solar array
Save10_D6036588M417474696C61204B6972616C79_000217_20261007082620_3_0_4.sfs

S3C - no-action control
Save11_D6036588M417474696C61204B6972616C79_000218_20261007082651_3_0_4.sfs

S4  - link extractor -> storage
Save12_D6036588M417474696C61204B6972616C79_000218_20261007082746_3_0_4.sfs

S4C - no-action control
Save13_D6036588M417474696C61204B6972616C79_000219_20261007082801_3_0_4.sfs

S5  - rename outpost "SOR-001"
Save14_D6036588M417474696C61204B6972616C79_000219_20261007082843_3_0_4.sfs

S5C - no-action control
Save15_D6036588M417474696C61204B6972616C79_000219_20261007082858_3_0_4.sfs

S6  - move solar array
Save16_D6036588M417474696C61204B6972616C79_000220_20261007082934_3_0_4.sfs

S6C - no-action control
Save17_D6036588M417474696C61204B6972616C79_000220_20261007082951_3_0_4.sfs

S7  - delete extractor
Save18_D6036588M417474696C61204B6972616C79_000221_20261007083042_3_0_4.sfs

S7C - no-action control
Save19_D6036588M417474696C61204B6972616C79_000221_20261007083056_3_0_4.sfs

exit - incidental terminal sample
Exitsave0_D6036588M417474696C61204B6972616C79_000221_20261007083107_3_0_4.sfs
```

## 2. Corpus provenance and known conditions

Record the following experimental conditions durably.

All saves were produced:

- during **one continuous Starfield session**;
- without restarting or reloading the game between checkpoints;
- from the same general outpost site;
- with the player stationary for nearly the entire sequence.

Known deviations/confounds:

### S5 movement confound

Immediately before `S5`, the user moved closer to the outpost beacon in order to perform the rename operation.

Therefore the transition:

```text
S4C -> S5
```

contains at least:

```text
outpost rename to "SOR-001"
+
player-position / movement-related state changes
```

Do not assume every change in that transition belongs to the rename.

### Hostile-fauna/combat confound

The user was attacked by hostile fauna once during the session.

Approximate timing:

> likely **after S3 (extractor + solar array)**, but the user cannot recall whether the attack occurred before or after `S3C`.

Known consequences likely include:

- 7mm ammunition reduction from approximately `190+` to `100+`;
- transient combat/aggro state;
- possible actor/combat/AI-related state;
- increased wall-clock delay while the user waited to see whether the creature or other hostiles returned.

Use timestamps, save diffs, and—if ammo inventory representation can be identified—to narrow the attack window if practical.

This is a **known confound**, not an instruction to remove or normalize data.

### S3 is intentionally non-atomic

`S3` adds both:

```text
iron extractor
+
solar array
```

Therefore a candidate structure appearing in:

```text
S2C -> S3
```

cannot initially be attributed uniquely to one of those two objects.

### S7 may contain relationship cleanup

`S7` deletes the extractor after an output link had previously existed between extractor and storage.

Therefore:

```text
S6C -> S7
```

may contain both:

```text
extractor deletion
+
consequential removal/alteration of output-link state
```

Do not assume all changes belong solely to object deletion.

## 3. Archive and manifest requirements

Before analysis, copy every source save into the project-local ignored research area.

For each source/original and local copy, record:

- checkpoint label;
- semantic description;
- exact filename;
- source path;
- local-copy path;
- file size;
- relevant filesystem timestamps;
- SHA-256;
- copy-verification result;
- action/control/incidental classification.

Verify:

```text
SHA256(live original) == SHA256(project-local copy)
```

before using the copy for analysis.

Do not analyze or mutate the live original.

The exit save should be preserved and manifested as:

```text
INCIDENTAL_TERMINAL_SAMPLE
```

It is not another deliberate experimental checkpoint.

Raw `.sfs` files must remain ignored/untracked.

## 4. Experimental pairing model

Preserve these action/control pairings explicitly:

```text
S0  -> S0C     background/no-action baseline

S0C -> S1      beacon placement
S1  -> S1C     beacon no-action control

S1C -> S2      solid-storage placement
S2  -> S2C     storage no-action control

S2C -> S3      extractor + solar-array placement
S3  -> S3C     no-action control / possible combat-window overlap

S3C -> S4      extractor -> storage output-link creation
S4  -> S4C     link-state no-action control

S4C -> S5      rename to "SOR-001" + player-movement confound
S5  -> S5C     renamed-outpost no-action control

S5C -> S6      move solar array
S6  -> S6C     moved-object no-action control

S6C -> S7      delete extractor + possible link cleanup
S7  -> S7C     post-deletion no-action control
```

Use these pairings as the primary differential model.

## 5. First-pass analysis philosophy

The first pass should be primarily **descriptive**.

Do not prematurely assign save-format semantics where the evidence only supports correlation.

For each save and transition, characterize as far as existing tooling permits:

- total file size;
- known container/compression structure;
- decompressed/decoded size where applicable;
- changed regions;
- changed record/chunk counts where meaningful;
- clustering/distribution of changes;
- additions;
- deletions;
- replacements/mutations;
- changes shared with nearby no-action controls;
- changes specific or strongly enriched in action transitions;
- candidate changes that persist into the following control.

A useful candidate for deliberate action state should ideally:

```text
appear or change during ACTION transition
+
persist through the following CONTROL save
```

while ordinary background churn may continue changing independently.

## 6. Establish background churn first

Use all no-action pairs:

```text
S0 -> S0C
S1 -> S1C
S2 -> S2C
S3 -> S3C
S4 -> S4C
S5 -> S5C
S6 -> S6C
S7 -> S7C
```

to characterize recurring/no-action differences.

Look for repeatedly changing headers/counters, timestamps/session fields, transient actor/world state, compression-layout changes, inventory/combat churn, record-order changes, shifting offsets caused by variable-length data, and regions that remain highly stable.

Do not subtract background changes mechanically unless their equivalence is established.

## 7. High-value semantic probes

### S1 — beacon placement

Look for candidate structures that:

- appear in `S0C -> S1`;
- remain present through `S1 -> S1C`;
- persist into later saves unless changed/deleted;
- may correlate with known outpost/workshop/beacon concepts from existing research.

### S2 — solid storage placement

Use this to distinguish:

```text
outpost/workshop-level state
from
ordinary placed-object state
```

where possible.

### S3 — extractor + solar array

Use this to look for repeated placed-object patterns established by S2, but do not attribute new structures uniquely to extractor vs solar array without further evidence.

### S4 — output link creation

Because the principal objects already exist, look for structures that:

- appear/change in `S3C -> S4`;
- persist in `S4 -> S4C`;
- differ from object-creation patterns;
- plausibly represent a relationship between existing objects.

### S5 — rename to `SOR-001`

Search all usable decoded/decompressed representations for:

```text
SOR-001
```

and reasonable encodings such as ASCII/UTF-8, UTF-16LE, length-prefixed strings, and string-table references where existing tooling exposes them.

Record first appearance, persistence, containing record/chunk/structure, nearby identifiers/offsets, and any relationship to candidate outpost/workshop structures from S1.

### S6 — move solar array

Look for:

```text
same underlying object identity persists
+
one or more transform/position-related fields change
```

Compare `S5C -> S6` and `S6 -> S6C`.

### S7 — delete extractor

Look for candidate object structures that existed from S3 onward and disappear, become tombstoned, or otherwise change in S7, then remain correspondingly changed in S7C.

Also examine whether candidate S4 link state disappears or changes.

## 8. Combat/ammo confound analysis

If existing save tooling can identify player inventory/ammunition without turning this into a new reverse-engineering project:

1. inspect relevant checkpoint values;
2. identify where 7mm ammo drops from roughly `190+` to `100+`;
3. correlate that with timestamp gaps and combat-state noise;
4. record the likely attack interval.

Do **not** let ammunition decoding become a blocker. If it is not cheaply accessible, record:

```text
combat window unresolved
```

and proceed.

## 9. Persistence analysis across the whole sequence

Track promising candidate structures across:

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
```

Try to describe lifecycles such as:

```text
absent
created
stable
mutated
linked
renamed
moved
deleted
```

only where supported.

## 10. Offset handling

Be careful with absolute file offsets.

If compression, variable-length structures, or earlier changes cause downstream offset shifts, do not treat a changed absolute position as a different logical record automatically.

Prefer stable logical identifiers/record structure/chunk identity where existing tooling supports them.

## 11. Existing project knowledge

Consult durable research records where useful, especially prior findings concerning workshop interfaces, beacon identity, `GetWorkshop`, owned/resource objects, placement/removal/output-link events, selected xEdit relationships, and the subsystem map.

Use those as hypotheses/context only. Do not force save evidence to agree with them.

## 12. Tooling expectations

Reuse existing project tooling where practical.

Small new offline scripts are acceptable for manifest generation, hashing, save decomposition, structured diffing, persistence tracking, string searching, and candidate correlation.

Keep new tooling narrow and inspectable.

Do not build a general Starfield save editor/parser unless clearly justified.

No live debugger work and no SFSE deployment are authorized under this brief.

## 13. Evidence standard

For every substantive finding, distinguish:

```text
OBSERVED
INFERRED
HYPOTHESIZED
```

Do not silently promote inference to fact.

## 14. Desired outputs

Produce at minimum:

1. a durable save corpus manifest;
2. a transition matrix for all action/control pairs;
3. background-churn characterization;
4. candidate outpost-state report;
5. detailed `SOR-001` rename-anchor analysis;
6. candidate lifecycle tracking;
7. combat-confound note;
8. recommended smallest next experiment/analysis.

## 15. Success criteria

This pass does **not** require a complete save-format decode.

It succeeds if it materially narrows the representation of outpost state—for example by establishing a beacon-related record family, a placed-object structure, a persistent rename/string anchor, a transform-bearing object candidate, an output-link candidate, an object-deletion lifecycle, or a reliable distinction between background churn and action-correlated state.

## 16. Do not clean up live saves

Do not delete the live originals.

The user will clean up the Steam-managed save directory manually/in-game after analysis and archival verification.

## 17. Git and artifact policy

Do not stage, commit, or push.

Do not track raw `.sfs` files or raw decompressed save blobs unless existing project policy explicitly permits that form.

Generated summaries/manifests/scripts/documentation may be tracked if consistent with repository policy.

## 18. Validation

Before returning:

- verify every project-local save copy against its live original by SHA-256;
- verify originals remain unchanged;
- verify no raw `.sfs` became tracked;
- run `git diff --check`;
- validate internal Markdown links if documentation changed;
- inspect `git status --short`;
- record all new scripts/tool outputs and locations.

## 19. Return for review

Return:

1. exact corpus manifest and copy-verification status;
2. timestamps and inferred/known experimental timing;
3. quantitative/descriptive transition summary;
4. background/no-action churn characterization;
5. `SOR-001` search result;
6. strongest beacon/workshop candidate structures;
7. strongest placed-object candidates;
8. S4 output-link findings;
9. S6 movement/transform findings;
10. S7 deletion/link-cleanup findings;
11. fauna/ammo-window finding or limitation;
12. candidate lifecycles across the sequence;
13. observed vs inferred vs hypothetical distinctions;
14. strongest current interpretation;
15. alternative explanations;
16. recommended next smallest experiment/analysis;
17. files changed;
18. checks run/results;
19. `git diff`;
20. `git status --short`.

Do not commit or push.

Suggested commit message only if later approved:

```text
research: characterize manual outpost save corpus
```
