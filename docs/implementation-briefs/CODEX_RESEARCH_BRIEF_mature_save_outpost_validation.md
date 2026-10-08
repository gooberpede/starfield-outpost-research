# SOR Research Brief — Mature-Save Outpost Structure and Cargo-Network Validation

## Objective

Independently validate the off-the-books findings from the mature Starfield save, concentrating on **active outpost membership, the bounded `0x79` reference/relationship grammar, cargo-pad identities and reciprocal cargo connections**. This task is not a general save-format research programme and does not authorize cargo simulation, production decoding, live instrumentation or save editing.

The exploratory observations are **hypotheses to test**, not required parser outputs. The objective is to establish which claims are reproducible, which survive independent structural checks, and which remain unresolved.

This work is **offline only**. Do not launch Starfield, use SFSE, attach a debugger, modify source saves or JSON, stage, commit or push.

## 1. Inputs and evidence integrity

Use these existing project-local materials:

- `.local-work/savegames/Save52_BA75E3CDM43616F205472616E_580743_20260818064541_319_15_4.sfs` — mature-save copy.
- `.local-work/scratch/` — copied outpost-network JSON. **Discover and record its exact filename** rather than assuming it.
- `.local-work/mature-save-offbook/` — off-the-books scripts, exploratory outputs and validation receipts.
- The committed S0–S7C corpus, L0–L2C link-validation corpus, structural-containment reports, candidate registers and evidence indexes.

Before analysis, record full paths, lengths, filesystem times where meaningful and SHA-256 digests for the mature save, the JSON and each exploratory script actually reused. Confirm the source files are unchanged after analysis. Preserve existing off-the-books work unmodified; create new outputs in a separately named ignored workspace. No raw `.sfs`, decompressed raw blobs or private gameplay files should become tracked.

Treat the JSON as a **manually maintained comparative description**, not an engine-authoritative extract. Its provenance and capture date may differ from the save; describe discrepancies rather than forcing agreement.

## 2. Research questions and stopping point

Answer, with reproducible evidence:

1. Is the putative active-outpost/reference unit actually bounded, and what determines its boundaries?
2. Does a single count/reference grammar parse the mature unit and all qualifying small-corpus examples without sample-specific exceptions?
3. Which beacon-like records are active members, and can those members be resolved independently to names?
4. Can cargo-pad candidates, types and reciprocal connections be reconstructed **from the save alone**, then compared at individual endpoint granularity with the JSON?
5. What distinguishes the two additional beacon-like candidates from the active membership set, without inventing their deletion history?
6. Which findings are directly observed, strongly inferred, or unresolved?

**Stop when these questions have been addressed as far as existing evidence permits.** Do not expand into fabricators, organic farming, inventories, transport direction, transfer timing, production rates, ship serialization, or a universal save parser.

## 3. Stage A — Reproduce the exploratory observations

Inspect and run the existing off-the-books procedures where appropriate, recording script identity, inputs, command/configuration and outputs. Reproduce or falsify, without silently repairing the expected numbers:

- reported mature `.sfs` size **16,411,136 bytes**, decompressed aggregate **36,934,800 bytes**, and **141 zlib streams**;
- embedded reported build `1.16.244.0`;
- the four-byte alignment adjustment before the first compressed stream (verify whether it is framing/alignment or merely a local decoder workaround);
- outpost-associated bounded `0x79` payload reportedly at decoded offset **1,860,043**, length **1,588 bytes**;
- alleged **17 beacon references**, **199 keyed groups** and **246 referenced endpoints**;
- alleged **324 distinct nonzero tokens** resolving to candidate object windows across two prefix families;
- **53 cargo-marker candidates** (25 regular and 28 fueled/interstellar), reportedly yielding **24 reciprocal connections** involving 48 distinct pads;
- **two additional named beacon-like candidates** outside the active collection.

These are starting claims, not assertions to copy into durable documents. Record differences even if minor and retain the failed/counterexample cases.

## 4. Stage B — Challenge the framing and grammar independently

Do **not** merely count the exploratory parser's successful outputs as validation. Independently inspect the relevant bytes and framing, using small, auditable checks or a separately reasoned parser where helpful.

For every qualifying `0x79` envelope in the mature save and controlled corpora:

- establish the enclosing chunk/decompressed coordinate system, exact start/end, header, declared payload length and actual consumed length;
- show the proposed grammar step by step: beacon-reference count and entries, keyed-group count, each group's key/count/entries, and any trailing bytes;
- validate truncation, overflow, negative/implausible counts, boundary crossing, duplicate handling and zero-valued keys;
- demonstrate exact consumption **without special-case padding or retrofitted fields**;
- separate *parse-valid framing* from *known gameplay meaning*;
- specifically test the earlier 12-byte and 19-byte linked/unlinked payloads and any other qualifying examples from S0–S7C and L0–L2C;
- examine whether the earlier `04` and `08` values genuinely satisfy an encoded-count interpretation. Preserve alternative interpretations if still possible.

Negative controls are important: attempt the grammar at nearby/noncandidate offsets or structurally mismatched samples, and show that the validator does not broadly accept arbitrary data. Use deterministic offline tests and record results.

If the mature structure's count grammar fits but its gameplay semantics remain uncertain, promote the **framing observation** separately from any **outpost meaning**.

## 5. Stage C — Active outpost membership, names and residual candidates

Using the save-derived reference unit and independently traced beacon/name candidates:

- enumerate active beacon references before consulting JSON names;
- resolve each through the observed object-window/string-index mechanism and document every hop, offset, reference value and ambiguity;
- determine whether all extracted active entries have distinct identities and sensible names;
- then compare the extracted names against the JSON's active outpost set with an exact match/mismatch table;
- inspect the two extra named beacon-like candidates: `Feynman VII-b U He3` and `Feynman II Ag U V`;
- show whether they are excluded from the active collection and which residual structures remain identifiable;
- distinguish user-reported historical deletion from save-proven deletion/tombstone/inactivity semantics.

Do not call every beacon-like string an active outpost. Do not infer that the two excluded candidates are necessarily Unity remnants or particular deletion artifacts from this save alone.

## 6. Stage D — Cargo-pad topology, extracted before JSON comparison

Recover from the save, independently of JSON topology:

1. beacon/outpost association for each cargo-marker candidate;
2. candidate type classification (regular vs fueled/interstellar) and the **actual bytes/structural basis** for that classification;
3. candidate pad identity and any self-reference/repeated-reference patterns;
4. reciprocal pad pairing, preserving distinctions between unique pad endpoints and repeated/self references;
5. the resulting multigraph of outposts and pad-level connections, **including multiple links between the same outpost pair**.

Produce a machine-readable *save-derived* extraction before using the JSON. Freeze/hash that extraction as a comparison input; do not quietly rebuild it in response to expected values.

Only then compare with the JSON:

- active outpost names (complete set, not just total);
- cargo-pad count and type **for each outpost**;
- pad-to-pad connection count, distinct-pad participation and full outpost-pair **multiset**;
- separate whether a particular physical pad can be uniquely matched to a particular JSON pad. JSON UUIDs/labels are app-side identifiers and must **not** be assumed to exist in the save;
- account for ambiguous permutations of same-type pads, and do not overclaim an exact per-pad bijection when only topology/count/type evidence supports it;
- present mismatches, missing/extra items, conflicts and ambiguous matches explicitly.

Validation targets from off-the-books research (not forced expectations): **17 active outposts**, **53 pad candidates (25 regular, 28 interstellar)** and **24 reciprocal cargo connections**. The JSON may reflect a different moment or manual bookkeeping choices; don't force it into agreement.

Do not label all entries in the `0x79` unit as output links or cargo transfers. Distinguish the local outpost relationship structure from the separately detected cargo-marker references.

## 7. Structural role, boundaries and identity claims

Determine whether the bounded unit is best described as:

- an active-outpost index;
- an outpost-local relationship collection;
- a combination of both;
- or an unresolved container with strong correlations.

Show how it points to (or correlates with) separately serialized object windows and the shared name/string collection. Preserve the distinction between:

- physical file/chunk offset;
- decompressed logical offset;
- bounded record/envelope;
- compact save-local token;
- stable reference/base FormID **only if actually resolved**.

A perfectly bounded active-index/relationship unit does **not** imply one contiguous container holds complete outposts. Complete object-record boundaries, stable cross-session identities and authoritative load behavior should remain unresolved unless independently demonstrated.

## 8. Evidence standards and promotion criteria

For each claim classify:

- **OBSERVED / PROVEN:** exact raw bytes, framing, lengths, validated counts, enumerated references, extracted strings, repeatable cross-save behavior;
- **INFERRED / STRONG:** semantic identification supported by independent correspondence, controlled transitions and cross-checks;
- **HYPOTHESIZED / PROVISIONAL:** ownership, directional semantics, unknown groups, retained/deleted meanings, gameplay authority and other unproven interpretations.

Keep independent evidence lines distinct: a correct grammar, a match to controlled link transitions, matching names, and a matching cargo topology support different facets of the model. Do not substitute one for another.

Specifically preserve the terminology refinement already agreed: call a structure a **relationship/collection region** or **region with apparently variable entry content** unless an actual list schema has been established. The previously reviewed `STRONG` output-link association need not be downgraded merely because “list” is too specific.

## 9. Durable research record

Create a **separate mature-save validation report** with byte-level evidence, tables, counterexamples, limitations, script provenance, reproducible commands and acceptance criteria. Create small source-controlled helper scripts only where justified; keep bulk/generated outputs ignored.

Do **not** rewrite the existing committed structural-containment experiment to retroactively incorporate the off-the-books discoveries. Allow only necessary cross-references or genuinely evidenced corrections, clearly identified as later work.

Update `RESEARCH_STATE`, findings, hypotheses, state/decision registers and evidence index **only for findings that survive reviewable validation**. Keep any not-yet-reviewed semantic promotion marked proposed/pending critical review. Do not invent formal IDs: follow the project's existing numbering and evidence-standard conventions.

Record the exploratory material as prior, unreviewed discovery with precise path/hash/version, stating what was copied, adapted, independently checked or rejected.

## 10. Validation, safety and repository boundaries

- Source mature save and JSON must remain byte-identical before/after; verify SHA-256.
- Existing controlled corpus artifacts must remain unmodified.
- No source save editing, memory patching, Starfield launch, SFSE deployment or debugger session.
- Respect C:/D: free-space safety policy (40,000,000,000 bytes threshold where applicable); prevent unbounded decompression/temp output. Use streamed/bounded output and record maximum sizes.
- No new third-party code reuse without the project's standing permission/provenance requirements; maintainer-authored `gooberpede` reuse exception applies with provenance, but does not waive embedded third-party obligations.
- Run unit/negative tests, `git diff --check`, Markdown-link validation, ignored/raw-artifact checks, and `git status --short`.
- Do not stage, commit or push.

## 11. Required deliverables and review response

Provide:

1. source-save/JSON exact paths, sizes, hashes, timestamps and provenance;
2. reproducibility results for the exploratory claims, listing confirmed and contradicted claims;
3. independent `0x79` envelope/grammar validation, including all qualifying small-corpus instances, negative controls and exact-consumption checks;
4. active beacon/name resolution table (including any unmatched entries);
5. the two excluded beacon-like candidates and the precise evidence for their exclusion;
6. save-derived cargo-marker/pad extraction **before** JSON comparison;
7. per-outpost pad-type/count comparison and full 24-link multigraph comparison with explicit ambiguity levels;
8. explanation of the zero-key group, or a clearly unresolved classification;
9. bounded-unit architectural interpretation and what remains distributed;
10. findings classified OBSERVED / INFERRED / HYPOTHESIZED;
11. contradictions, counterexamples and alternative interpretations;
12. exact additions to durable findings/state records, clearly marked proposed if awaiting critical review;
13. smallest next outpost-focused research step, if one is necessary;
14. files changed, tests/checks/results, relevant offline scripts and evidence paths;
15. complete review diff including new files and `git status --short`.

**Stopping rule:** When membership, framing, cargo topology and structural role have been tested against the preserved evidence, return for critical review. Do not expand into unrelated serialization subsystems.

Suggested commit subject **only after approval**:

```text
research: validate mature-save outpost index and cargo topology
```
