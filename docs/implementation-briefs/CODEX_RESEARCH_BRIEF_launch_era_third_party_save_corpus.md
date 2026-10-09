# Codex Research Brief — Launch-Era Third-Party Save Corpus Inventory and Structural Compatibility

## Purpose and scope

Perform a **bounded, read-only offline inventory** of the September 2023 Starfield save package published by **TheDailyXPerience** on Nexus Mods. Determine whether launch-era saves expose the outpost-related framing and reference structures already studied in this project, identify plausible outpost/no-outpost cases, and shortlist a few samples for a later focused investigation.

**Do not turn this into a general Starfield save-format project.** Do not inspect unrelated quest, inventory, ship or exploration systems beyond metadata necessary to classify samples. Do not launch Starfield, load or resave historical saves, attach a debugger, deploy SFSE, stage, commit or push.

This is a **separate supplemental third-party corpus**, not an extension or renumbering of the previously frozen 278-save historical inventory. The controlled Save3 programme and the owner's mature-save corpus retain their distinct evidential roles.

## 1. Source and permission boundary

- Author/uploader: **TheDailyXPerience**.
- Source: `https://www.nexusmods.com/starfield/mods/1798`.
- Local source archive (exact operator-supplied path):

  `C:\Users\User\Downloads\Over 110 saves-1798-1-1694378623.7z`

- Working interpretation of permissions: **local examination and independently authored derived research are permitted; do not re-upload or redistribute the original archive, save files or substantial verbatim extracted payloads**. Before publication, ensure the exact current listing permissions are retained as provenance and any ambiguity is reported for review rather than assumed away.
- Attribution and provenance are mandatory: credit TheDailyXPerience and link the source listing in suitable `docs/SOURCES.md`, `docs/PROVENANCE.md`, permission and/or experimental records according to project conventions. Do not imply the donor endorsed the analysis.
- September 2023 upload date, early game-version provenance and presumed vanilla/mod-free status are **leads**, not verified facts about every contained save. Extract embedded build and mod/load-order indicators where available.

Retain source URLs, author, download/archive filename, locally observed archive SHA-256, archive size and timestamps, and exact permission evidence/reference. Do not incorporate third-party scripts or code merely because saves are permitted for study.

## 2. Safe intake and extraction

1. Verify the specified archive exists and is readable. **Do not search unrelated user directories** if it is absent; report a specific blocker.
2. Hash the original archive, record its metadata, and **never modify, rename, move or delete it**.
3. Use an available local 7z-capable utility, without installing extra software unless separately agreed. Prefer a read/list pass before extraction.
4. Inspect archive member names, size totals and compression metadata; reject or quarantine suspicious traversal/absolute paths, symlinks/reparse points or unexpected content. Do not execute anything from the archive.
5. Check sufficient free space and the project's established **40,000,000,000-byte disk-space guard** on relevant C:/D: volumes before and during bulk operations. Bound decompression output, individual file size, total file count, total expanded bytes and runtime; document chosen limits. Never disable the safety guard to complete intake.
6. Extract a **copy** to a clearly named ignored subtree such as `.local-work/third-party/the-daily-xperience-1798/` (or the project's established equivalent); do not deposit saves in Starfield's live Saves directory.
7. Verify extracted file hashes/sizes, record paths relative to corpus root, archive member identity and any extraction exceptions. Preserve original archive and extracted files unchanged.
8. Confirm Git ignores the archive, `.sfs`, decompressed binary payloads and derived raw fragments. Only independent scripts, manifests with non-sensitive metadata, bounded analytical summaries and documentation may be considered for tracking under existing policy.

Do not produce a distributable ZIP or repackaged corpus. Avoid storing usernames, absolute local paths or other personally identifying donor/player details in public-facing tracked records; retain needed private path provenance only in ignored local receipts.

## 3. First-pass manifest and classification

Inventory all contained candidate `.sfs` saves, recording as recoverable:

- stable **corpus-local identifier** (new namespace, distinct from `HIST-*`, `SOR-SAMPLE-*` and existing experimental identifiers);
- archive member path / safe extracted path, byte size, SHA-256, filesystem/member timestamps and parser status;
- embedded Starfield build/version strings, keeping multiple ambiguous version fields separate;
- character/profile metadata and progression clues **without asserting chronology/Unity continuity from filenames**;
- container/header/chunk signatures, stream counts and verified decompressed totals within limits;
- outpost-related structural indicators and any recognizably named outposts;
- presence/absence/inconclusive classification with the explicit indicators and limitations supporting it.

**No-outpost classification:** expressly distinguish:

1. `OUTPOST_EVIDENCE_PRESENT` — identifiable outpost state/signatures;
2. `NO_ACTIVE_OUTPOST_INDICATORS_DETECTED` — multiple independent negative indicators, **not proof of total absence**;
3. `INCONCLUSIVE` — incomplete, unsupported or ambiguous decoding.

Use project conventions if established labels differ. An empty beacon-reference collection by itself is **not proof** of no active outpost: the controlled corpus already contains counterexamples. Residual beacon-like objects are not automatically active outposts. Do not equate parser failure with corrupted saves or outpost absence.

## 4. Structural compatibility — narrow questions

Compare samples against the project's **existing validated candidate structures**, using current durable reports and parsers as the source of exact definitions:

- save header and directory/chunk framing, including known alignment and version variation;
- the bounded `0x79` count/reference grammar, explicitly verifying declared lengths and exact consumption when present;
- beacon/reference collections, without treating them as a universal active-outpost registry;
- name/animation string-index associations and provisional location/body-name leads;
- beacon/object windows and candidate cargo markers or reciprocal connection signatures where present.

For each structure report `recognized`, `absent in successfully decoded applicable area`, `ambiguous`, or `unsupported by this version/decoder`. Keep **syntactic recognition**, **semantic identification**, and **negative absence evidence** separate. A zero-length or empty compatible structure is itself valuable: report it even if no outposts are otherwise found.

For each version group, state what is genuinely comparable with the current version and what appears to have changed. Do not explain differences as version migrations when gameplay-state differences could also explain them. Do not reverse engineer unrelated systems merely to make the version matrix complete.

## 5. Progression and sample selection

The Nexus package is described as containing over 110 saves from a playthrough. Verify actual member count and metadata. Identify possible groups or trajectories only where timestamps, versions, character identifiers and structural state jointly support them. Preserve uncertainty around ordering, Unity transitions and saves that might come from divergent branches.

Select approximately **three to five** high-information candidates, preferably spanning distinct useful conditions such as:

- a well-supported mature **no-active-outpost-indicators** candidate;
- any positive outpost-containing candidate, even a small one;
- early or anomalous outpost grammar/framing;
- distinct embedded game versions/format layouts if genuinely present;
- a plausible same-character progression pair with meaningful outpost-state variation, if supported.

Do not force one of each category if the files do not contain it. Rank by **information value**, not size or character level alone. Record selection rationale and counterexamples. Copying is unnecessary because safely extracted, hash-verified candidates already live inside ignored local-work; if the project prefers a shortlist directory, use verified copies only and avoid needless duplication.

## 6. Scientific approach and negative controls

- First reproduce existing corpus parsing conventions; reuse maintainers' own tooling with provenance if adapted.
- Run bounded structural checks and independent spot checks of counts/lengths, especially for novel version layouts.
- No claim that a save is vanilla, outpost-free, corrupt, or migration-compatible without specific supporting evidence.
- Record unsupported layouts and counterexamples, not just positive matches.
- Treat mature saves as **observational topology/structure sources**, not controlled causal evidence. Leave Save3-based micro-experiments separate.
- Do not infer location coordinates from plausible floats alone; location is a secondary compatibility lead only, not a new decoding workstream.
- Do not load or resave any third-party historical save under this brief. Cross-version load/resave remains a **future separately authorized** controlled experiment, requiring preservation and explicit handling of cloud/live-save risks.

## 7. Durable documentation and publication boundaries

Create one focused experimental report and supporting manifest/validation records following existing project nomenclature. Update research-state/methodology and third-party source/provenance/permission records only as necessary to:

- register this distinct corpus and its author;
- record that older game versions remain eligible for research;
- distinguish controlled Save3 experiments from observational mature/historical corpus work;
- explicitly prohibit publishing/re-uploading the third-party raw saves/archive and substantial original extracted material.

Do not retroactively modify or merge the frozen 278-save historical inventory. Do not promote unreviewed structural candidates to `PROVEN` or `STRONG` merely because the parser recognizes them. Preserve existing evidence and avoid rewriting established records except for necessary cross-references or demonstrable corrections.

For public-facing manifests, use corpus-local IDs, hashes, sizes and structure metrics; minimize identifying user/character fields where not essential. Treat other-person save contents as potentially personal data.

## 8. Success criteria and stopping rule

The task succeeds when the following can be answered reproducibly:

1. How many candidate saves are in the package and how reliably can they be read?
2. Which actual embedded game versions and format variants occur?
3. Does the recognized chunk and `0x79` framing exist in launch-era samples, including empty ones?
4. Which saves have positive outpost indicators, credible negative indicators, or inconclusive results?
5. Which three to five cases best justify further investigation?

**Stop at inventory, compatibility and triage.** Do not fully decode cargo simulation, ships, quests, inventories, world exploration, or the entire save format. If none of the saves contain useful outpost state, report that honestly; even compatible empty structure and negative evidence are useful.

## 9. Validation and review handoff

Before returning:

- verify original archive SHA-256 and extraction/copy integrity, preserving all originals;
- check archive member totals and decompression bounds;
- run appropriate parser unit/synthetic tests and independent spot checks;
- validate no raw source saves, archives or raw decompressed blobs are Git-tracked;
- run `git diff --check` and internal Markdown-link checks;
- inspect `git status --short`;
- preserve ignored scratch artifacts with a bounded validation receipt and exact paths.

Return for critical review:

1. source archive verification, author/source/permission provenance and extraction disposition;
2. actual inventory count, version distribution, errors/unsupported cases;
3. structural compatibility matrix and exact grammar/framing evidence;
4. outpost-presence classification counts with strongest positive/negative examples;
5. any discovered early empty outpost units or meaningful counterexamples;
6. progression claims and their uncertainty;
7. ranked shortlist (3–5 where available), rationale and source hashes;
8. observed / inferred / hypothesized distinctions;
9. changes to durable methodology/provenance records;
10. tooling/tests, validation outcomes and known limitations;
11. exact files changed, task-only and comprehensive review diffs, and `git status --short`.

**Do not stage, commit or push.** Do not launch Starfield or alter live game saves.

Suggested commit subject *only if later approved*:

```text
research: inventory launch-era third-party save corpus
```
