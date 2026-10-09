# Codex Research and Implementation Brief — Save Decoder Capacity and Outpost Planetary Location

**Project:** Starfield Outpost Research (`D:\Projects\starfield-outpost-research`)  
**Work type:** bounded tooling improvement plus hypothesis-driven offline research  
**Commit policy:** do not stage, commit, or push; return a review diff  
**Live work:** no Starfield launches, save loads/resaves, SFSE deployment, or debugger attachment without separate authorization

## 1. Purpose and priority

Two separately testable workstreams:

**A. Remove arbitrary aggregate decoded-size restrictions** that prevent structurally valid large saves from being inspected. Keep genuine resource and integrity protection.

**B. Determine an outpost's planet/moon** from its serialized identity or relationships, then investigate **its planetary-surface position**. These are the scientific priorities, in this order:

1. Authoritative or strongly validated **body identity** (planet/moon), ideally resolved to a FormID or equivalent and then a star system.
2. **Planetary placement** in a globally meaningful frame (coordinates, tile, landing zone, or a reproducible mapping from save state to planetary position).
3. Local XYZ, cell, worldspace, orientation and other fields **only to the extent they help achieve 1 or 2**.

A collection of plausible local XYZ tuples is not sufficient to declare the location investigation complete. Conversely, a reproducibly validated body identity is a valuable standalone result even if surface coordinates remain unresolved.

## 2. Scientific ground rules

Apply the current `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md` and permission/provenance policies. Keep **confidence**, **coverage** and **completeness** separate; report the strongest scoped answer supported, without demanding universal completeness. Do not promote provisional location semantics solely by proximity, naming or coincidence.

**Do not infer a planet or system from an outpost name.** Even if default names resemble `{planetName} Outpost {N}`, and even if a manually assigned name contains a planet label, the name is neither an authoritative body identifier nor independent validation of body identity. Name matching may be used to help provisionally align entities across sources, but location claims must rest on other evidence. Explicitly disclose where alignment itself relies on names and seek a second independent identity signal.

The user-authored outpost network JSON is an **imperfect external comparison dataset**, not a specification or an authoritative runtime export. Do not train/fit a decoder on its expected locations and then cite that agreement as independent verification.

## 3. Inputs

Use existing project manifests and ignored archives to locate, identify and hash the exact inputs; do not guess paths beyond those established here:

- **Save2:** player was in New Atlantis, near the Lodge's front doors. Verify exact file and source/coverage. This is a known-location control, not proof of the saved coordinate frame.
- **Save3 and S1/S1C:** pristine no-outpost baseline versus a single new ordinary beacon on **Kreet**, from the controlled experiment; use the independently established gameplay conditions.
- **Save52:** mature save `Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs`, already archived in `.local-work/savegames/`. It contains a user-documented network of 17 active outposts and additional historical beacon-like state.
- **Network JSON:** copied to `.local-work/scratch/`; discover exact filename, record hash and provenance. Fields such as `systemId` and `bodyId` may be useful as comparison values, but independently establish what those IDs mean before treating them as game FormIDs. The JSON's UUIDs are application IDs, not proven game reference IDs.
- Earlier A0/A0C runtime player-position evidence, S0–S7C and L0–L2C save-corpus findings, beacon detector and structural-containment research.
- Existing read-only historical corpus, including **the three saves previously excluded by decoded-size limits**.
- Installed `Starfield.esm` and other locally available game data, xEdit scripts/results, Creation Kit evidence and pinned Starfield 1.16.244.0 static-analysis records where relevant.

Record the exact save and executable versions. Do not silently conflate current-version ESM identities with older save versions; verify cross-version interpretation where relevant.

## 4. Workstream A — replace artificial decoded-size rejection

Inspect the current decoder's limit and identify precisely whether it applies per chunk, per save, to output accumulation, or to a record/frame count. Document its original rationale and failure modes.

Implement **no arbitrary aggregate decompressed-size cap for valid saves**. Prefer bounded streaming/iteration and low-memory record processing rather than retaining the full decoded save. If necessary, use ignored scratch files with bounded output, cleanup and restartability.

Retain real safeguards:

- validate chunk headers, lengths, framing, compressed and uncompressed byte accounting, checksums where actually defined, and truncation;
- reject nonsensical size declarations *before* dangerous allocations, without confusing a large valid value with an impossible value;
- bound **individual allocations**, working memory and pathological expansion behavior; make operational budgets configurable/diagnostic rather than silent semantic limits;
- retain the project guard against dropping below **40,000,000,000 free bytes** on relevant C: or D: volumes, and avoid runaway scratch growth;
- report allocation/resource failures and structurally corrupt inputs distinctly;
- never modify source saves or overwrite existing verified evidence.

Review compatibility with existing CLI and test consumers. Avoid gratuitous redesign of unrelated parsers.

### A validation requirements

1. Re-run the **three previously size-excluded saves**, capturing exact disposition, versions, sizes, chunk counts and any remaining errors.
2. Re-run Save3, S1, Save52 and representative historical/launch-era samples to detect regressions.
3. Add synthetic tests for structurally valid large aggregate output, extreme/false header lengths, truncation, decompression expansion, low-space/integrity errors, and bounded memory/scratch operation.
4. Report peak memory or an adequately measured/estimated bound, and scratch disk use; do not claim streaming merely because a new aggregate cap is larger.
5. Keep this workstream's outcome independent of success or failure on location research.

## 5. Workstream B — body identity first

Start from the ordinary-beacon detector's located save records, not from a name-to-planet lookup. Use the **Save3 → S1** controlled contrast and the S1/S1C persistence control as the first case. Determine which saved facts lead the game to reconstruct the beacon on **Kreet**.

Codex may formulate and challenge its own models. Investigate whatever directly relevant record relationships are needed, including body, location, worldspace, cell, parent/owner, landing region, reference maps, records and base forms. These are *investigative possibilities*, not an imposed serialization model.

Look for a reproducible evidence chain, for example:

```text
recognized beacon reference
    → persisted containing/parent location identity or relationship
    → game body/planet/moon identity
    → star system (where verifiable)
```

Do not accept an isolated nearby planet name, an outpost-name prefix or a plausible local coordinate as sufficient.

### Fixed-point geographical anchors

Use ESM/xEdit records for known locations as comparative anchors, including **New Atlantis on Jemison**, **Akila City on Akila**, and **Cydonia on Mars**, where relevant records can be verified. Do not rely on hardcoded guessed FormIDs.

**Save2 near the Lodge doors** is an especially useful player-location control: identify the saved player reference's relevant location/worldspace/cell associations and compare with verified New Atlantis/Lodge ESM records. Carefully distinguish player-position data from outpost-beacon data; the two need not use the same frame or serialization path.

The objective is not a general atlas of fixed points of interest. Use them only to test and interpret the save→body or surface-position mechanism.

### Save52 network comparison

Extract candidate body/system identities from Save52 **before** consulting expected JSON values for each outpost. Preserve a blind candidate table with save-derived reference identifiers, raw fields and proposed body IDs.

Then compare with the JSON's documented `bodyId` and `systemId` per outpost, disclosing how each save-side beacon was aligned to its corresponding JSON entry. Because names are manually chosen, name equality must not itself validate the location. Seek identity corroboration from body/reference structure, outpost relationships, cargo-network topology, or other independent save evidence where feasible.

Report per-outpost matches, mismatches, unresolved identity correspondences and alternative explanations. Include different moons/planets in the same system to demonstrate that the method resolves the **body**, not merely the star system. Do not force a 17/17 result or adjust parsing rules using expected answers without separate challenge validation.

## 6. Workstream B — planetary placement, after body identity

Once the body question is addressed, investigate how a particular outpost site on that body is identified. Aim for globally meaningful planetary coordinates or a mapping to them. Distinguish:

- global/body-relative surface position, latitude/longitude or a known alternative surface-location system;
- landing/tile/region/cell/worldspace identity that may establish such position;
- local Cartesian XYZ and orientation of beacon/player/nearby objects.

Use S1's known single-beacon case, the save-derived tuple candidates, A0/A0C live coordinates, Save2/Lodge and fixed-location ESM anchors only when their coordinate frames are demonstrably relevant. The earlier numerical proximity between an A0 player XYZ and beacon candidate is supporting evidence, **not** proof of a common frame or planetary coordinates.

A body ID without latitude/longitude is meaningful partial progress. A coordinate conversion that cannot distinguish bodies is not a complete location solution. If coordinates remain unresolved, specify the exact missing transform/reference relationship and the strongest evidence for it, not a generic list of uncertainties.

## 7. Investigative autonomy and stop criteria

Within these offline boundaries, Codex has broad latitude to inspect records, build small tooling, reverse-engineer relevant ESM structures and pinned code, form new hypotheses and falsify them. Do not divert into generic save-format decoding, ship systems, quest progression or cargo simulation except when indispensable to resolving body identity or surface location.

Continue through justified offline alternatives rather than stopping at the first ambiguous field. A report of only local XYZ is not adequate completion. Return a best-supported answer for **planet/moon**, with confidence and coverage, or an evidence-backed explanation of what specific inaccessible/missing relationship prevents such an answer and which targeted experiment would address it.

Do **not** start new live experiments, load old saves, modify ESMs, or deploy SFSE without authorization. If a live observation becomes the highest-value next step, specify a bounded proposal rather than performing it.

## 8. Reporting and durable record

Report **answer first**, separately for A and B:

- **A:** whether large saves now parse; results for each formerly excluded sample, test/budget limits, resource usage, and remaining blockers.
- **B, body:** best-supported planet/moon identification for S1, and Save52 cross-check matrix; confidence, coverage, concrete evidence chain and contradictions.
- **B, surface:** coordinates or best-supported positioning mechanism, with explicit frame/units uncertainties and specific remaining obligations.

Record provenance, exact raw offsets/decoded record identities when meaningful, reproducible commands/scripts, counterexamples and negative findings. Keep physical file offsets, compressed chunks, decoded record fields and logical game identity distinct.

Update relevant experiment reports, evidence and state/finding/hypothesis registers only as evidence justifies. Do not retroactively promote unrelated findings. Do not commit source saves, JSON if publication rights/policy forbid it, substantial extracted payloads, or large ignored outputs.

Provide a compact cross-source comparison of beacon identity → saved spatial fields → resolved body/system → planetary position evidence. Show what is *observed*, *strongly inferred*, *provisional* and *unknown*, with coverage made explicit.

## 9. Validation and return package

Before returning, verify all original/archive hashes unchanged; confirm no raw save/dump/binary newly tracked; run relevant synthetic, regression and structural tests; run `git diff --check` and internal Markdown link checks; report exact touched files and `git status --short`.

Return:

1. A/B executive results and confidence/coverage;
2. size-limit diagnosis and implementation explanation;
3. former excluded-save dispositions and test/resource metrics;
4. Save3/S1 beacon→body evidence chain;
5. Save2/Lodge and fixed-point ESM cross-check;
6. per-outpost Save52 vs JSON body/system matrix, including correspondence method and discrepancies;
7. best-supported planetary-location/coordinate conclusions;
8. falsified hypotheses, missing information and smallest high-value follow-up if needed;
9. documentation and script changes, validation results, task-only/full diff and Git status.

**No staging, commit or push.** Suggested later commit title, subject to review:

```text
research: expand save decoding and investigate outpost planetary location
```
