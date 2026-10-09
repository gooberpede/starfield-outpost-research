# Codex Research Brief — Historical Starfield Save Inventory and Triage

**Project:** `starfield-outpost-research`  
**Task type:** Offline, read-only discovery and candidate selection  
**Status:** For implementation; no live-game actions or Git commit authorized

## 1. Purpose and research boundaries

Inventory available historical Starfield saves and select a **diverse, small shortlist** for later outpost-focused structural research. Mature saves complement, but **do not replace**, controlled micro-experiments based on pristine Save3.

Two distinct research tracks must remain separate:

- **Controlled Save3 experiments:** deliberately isolate outpost actions, with no-action controls, to test semantics and causality.
- **Historical/mature saves:** observational datasets that expose large collections, topology, unusual states and version differences. They may contain accumulated bugs, residual references, incomplete or obsolete structures, and unknown gameplay histories; do **not** use them as controlled intervention baselines.

An eventual **old-version save → current game load → new save** migration experiment is a promising *future* task, but **not authorized now**.

The key new question for this inventory is:

> **Can we identify mature saves that contain no outposts at all?**

Do not equate an empty beacon-reference collection with zero active outposts. Prior controlled samples demonstrate that such a collection can be empty even when an outpost beacon is present.

## 2. Authorized inputs and file safety

Codex is authorized to **read and inspect**, but never alter, files within:

```text
C:\Users\User\Documents\My Games\Starfield\Saves\
```

Permitted: enumerate files, inspect metadata, hash, read headers, safely decompress for bounded offline inspection, and copy selected candidate files to an ignored location under `.local-work/savegames/` after hashing.

Prohibited: moving, renaming, deleting, overwriting, modifying, repairing or saving over any original; changing Steam/cloud-managed state; starting Starfield; loading historical saves in game; deploying SFSE; attaching a debugger; staging, committing or pushing.

Existing context:

- Preserved Save3 remains the controlled micro-experiment baseline and must not be modified.
- A previously examined mature save (`Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs`) is already copied into `.local-work/savegames/`.
- The associated manually maintained network JSON is in `.local-work/scratch/`.
- Prior exploratory work remains in `.local-work/mature-save-offbook/`.
- Existing committed mature-save validation and small-corpus reports are the starting methodological references.

Do not assume every historical save belongs to a single universe/Unity cycle or a strictly linear timeline. Do not infer sequence or state equivalence from filenames, character names, level, or filesystem timestamps alone.

## 3. Method: two-tier inventory

### Tier 1 — Whole-directory catalog

Enumerate all available `.sfs` candidates in the authorized directory. For every candidate record, where accessible:

- exact filename/path, size, relevant filesystem timestamps and SHA-256;
- recognizable save metadata (character identifier/name, level, playtime or save type if obtainable), with provenance of each field;
- embedded Starfield/game/save version and container/format version **if recoverable**, carefully distinguishing these from filename tokens;
- structural support status: `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`, `MALFORMED_CONFIRMED`, or `UNDETERMINED`;
- known chunk/stream framing or a reason it was not inspected;
- any prior source/archive identity or duplicate-content hash;
- bounded parsing errors and version-specific differences.

Prioritize non-destructive, bounded operations. Maintain progress/resume receipts so one unusual save does not interrupt the directory inventory. Apply the existing disk-space guards to C: and D: (stop unsafe artifact creation if available bytes fall below **40,000,000,000** on either relevant volume); enforce limits on decompression, file output and runtime work. Prefer summaries rather than dumping large decoded buffers.

**Do not reject older-game-version saves solely because they are older.** Include unsupported or partially understood versions in the catalog and potentially in the shortlist. A decoder failure is not proof that the save contains no outposts or that it is corrupt.

### Tier 2 — Bounded outpost-specific fingerprints

For candidates where the existing bounded parser can safely inspect the relevant structures, recover, **without full general save decoding**:

- presence and framing of the familiar outpost-reference/relationship unit (including `0x79` candidate), payload size and whether the count/reference grammar consumes it exactly;
- count of references in its beacon collection, keyed groups, and associated endpoints;
- beacon-like object-window candidate count, with naming evidence where resolvable;
- associated cargo-pad/marker candidate count and regular/interstellar candidate breakdown, if safely supported;
- distinct reciprocal cargo connections and any unpaired, self-reference or ambiguous markers;
- recognizable outpost names and associated string-index links;
- sizes of relevant logical regions (relationship, object, reference-table candidate, shared strings), not just overall save size;
- evidence of residual/historical beacon-like objects not participating in the observed network collection;
- confidence, counterexamples and extraction limits for each metric.

Separate **observed counts** from **semantic interpretations**. Treat the validated mature-save interpretation as a hypothesis/testable parser model, not as a universal format specification.

There is no requirement to perform exhaustive deep decoding of every file. If a complete Tier 2 scan across the inventory is expensive, use a deterministic, documented bounded scan and state which saves received which analysis depth.

## 4. Explicit “no outposts” classification

The user especially wants to know whether mature saves with no outposts can be detected. Treat this as a classification problem with **positive and negative evidence**.

Use a scheme along these lines:

- `OUTPOSTS_CONFIRMED_PRESENT` — convincing outpost-specific structures/names/references are present.
- `NO_ACTIVE_OUTPOSTS_SUPPORTED` — multiple independent, applicable indicators support absence of *active* outposts; coverage and counterexamples described.
- `NO_OUTPOST_STATE_SUPPORTED` — stronger conclusion that no detectable current or residual outpost-related state exists **only if the parser's coverage and negative controls genuinely justify it**; do not infer this just from zeros.
- `POSSIBLE_RESIDUAL_OR_INACTIVE_STATE` — beacon-like or relationship remnants without confirmed active membership.
- `INDETERMINATE` — insufficient evidence, unsupported format, ambiguous data or incomplete inspection.

Avoid false certainty. In particular:

1. The `0x79` beacon-reference collection can be empty even when an outpost is present in the controlled S1/S2 samples.
2. Beacon-like windows can persist for apparently deleted outposts; their mere presence does not establish active membership.
3. A mature save might legitimately have zero active outposts yet contain historical outpost-related state.
4. An older or partially parsed format cannot be called outpost-free on that basis.

Use the known **Save3/no-outpost control** and its controlled successors (S0/S0C, S1/S1C, etc.) as calibration/counterexample material, without claiming they cover every version and game state.

For any purported no-outpost mature save, produce an auditable negative-evidence checklist: which independent indicators were checked, which were absent, which could not be checked, and how confidently the conclusion follows. Prefer `INDETERMINATE` when exclusion is not defensible.

## 5. Version differences as opportunity, not exclusion

Produce a version-stratified summary showing which structural signatures are preserved, changed, unsupported or unknown across available versions. Avoid causal attribution of differences to game upgrades when gameplay histories differ.

Record interesting old-version candidates for a **future, separately authorized migration experiment**:

```text
preserve original and verified copy
→ load historical save under current game (later authorization)
→ create distinct new manual save
→ create current-version no-action resave/control where useful
→ compare framing, IDs and outpost-related state
```

**Do not conduct this sequence now.** Note compatibility, Steam/cloud and original-preservation safeguards for future planning only.

## 6. Candidate selection

Recommend approximately **3–5** historical saves for deeper analysis, prioritizing distinct *structural profiles* and question-answering value rather than just the largest files or highest-level character.

Useful diversity may include:

- convincing active multi-outpost/cargo network;
- apparently no active outposts or no outpost state (if supported);
- intermediate/small network;
- nontrivial residue or mismatched active vs beacon-like counts;
- version-specific framing changes or unsupported older formats;
- contrasting cargo topology, including parallel connections.

A sparse historical archive may not provide all categories. Do not manufacture candidates, presume a chronological chain, or demand one save per Unity passage. Include a reasoned confidence/coverage/risk assessment and concrete research question for each choice.

Copy shortlisted saves only when useful and safe, to ignored project-local paths. Verify source/copy hashes and record source identity. Do not duplicate files already preserved and hash-identical.

## 7. Methodology updates and terminology

Make a **minimal** durable methodology update establishing:

- Save3 controls test causality and semantics;
- mature historical saves are observational structural/topology evidence, potentially anomalous or bug-affected;
- cross-version load/resave is a distinct future experimental category requiring explicit authorization;
- absence claims need stronger safeguards than presence claims.

Do not rewrite committed prior experimental results or prematurely promote exploratory findings. Existing semantic limits remain, especially the lack of a universal active-outpost-index proof and ambiguity between some save-side pads and manually labeled JSON pad IDs.

## 8. Deliverables

Produce:

1. **Inventory manifest**, machine-readable and durable-safe: per-file provenance, hashes, versions, parsing status and depth.
2. **Compact inventory report**: corpus coverage, version distribution, size distribution, structural-fingerprint contrasts, and data-quality/compatibility limitations.
3. **Outpost presence/absence matrix**: classifications with indicator-level justifications, including apparent no-outpost candidates.
4. **Candidate shortlist**: 3–5 saves if available, with priority, rationale, expected research value, uncertainty and archival status.
5. **Version-variation notes**: hypotheses worth later checking with controlled old→new migration.
6. **Methodology update** and relevant narrow state links, without restructuring unrelated documents.
7. **Tooling/provenance record**: reused scripts, adjustments, input hashes, limitations and validation results.

Large per-save derived data, raw blobs and copied `.sfs` files must stay ignored under `.local-work/`; commit-eligible docs should contain only useful summaries, stable identifiers and reproducibility instructions.

## 9. Validation and review handoff

Before finishing:

- rehash and verify any copied files against originals; preserve originals unchanged;
- verify the mature-save baseline remains consistent with validated findings;
- test known positive (e.g. linked mature save, S1+) and known negative (Save3/S0) controls and explicitly retain the empty-collection counterexample;
- validate decoder failure/unsupported-version treatment and any no-outpost classification logic;
- verify bounded decompression/resource safeguards;
- run `git diff --check`, internal-link validation and `git status --short`;
- verify no `.sfs`, raw dump, decompressed save blob or other forbidden evidence becomes tracked.

Return:

- inventory count, versions and parser coverage;
- exact criteria and results for candidate saves with **no outposts**;
- strongest structural anomalies and differences;
- selected shortlist and reasoning;
- any version-compatibility blockers and migration candidates;
- files changed, tests/checks, audit references;
- complete review diff (including untracked text files) and Git status.

**Do not stage, commit or push. Do not load any historical save in Starfield.**

Suggested commit message *only if later approved*:

```text
research: inventory historical saves and triage outpost evidence
```
