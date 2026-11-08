# RG2-D5BD — Native Function Catalogue and Developer Reference

**Assignment:** D5BD  
**Project:** `starfield-outpost-research`  
**Type:** Bounded documentation, evidence reconciliation, and read-only validation  
**Status on issue:** Implementation brief; not research-publication or integration authorization  
**Primary target:** Retail `Starfield.exe` **1.16.244.0**  
**One-off staffing exception:** **At most two concurrently active sub-agents for D5BD only.** The standing limit of one concurrent sub-agent resumes immediately on completion/termination of this assignment. This exception does not authorize additional workstreams outside D5BD.

## 1. Purpose and controlling decisions

Make the project's accumulated native-function discoveries useful as a **developer-facing, searchable, version-pinned reference**, especially to prospective SFSE plugin authors. Consolidate **everything positively identified and relevant**, not merely functions whose prototypes are fully understood. Preserve unknowns rather than filling them with guesses. The deliverable is a catalogue of *observed internal implementation*, **not a list of functions certified safe for external calls**.

The existing `docs/function-register.md`, experiment-level function tables, native reports and original research evidence remain in place. This new collection is **additional**, not a replacement or revision of historical research. Build it **bottom-up from original source/evidence inventories**, then cross-reference the 18 accepted subsystem guide/reference pairs for contextual coverage and discrepancies. Do not treat the recently authored guides as the authoritative source for an address, prototype, body boundary or control flow.

### Controlling questions

- **Q1 — Discovery and canonical identity:** What positively located native functions are documented across the research, what evidence establishes their entry points, and how can they be deduplicated without conflating unrelated functions?
- **Q2 — Technical characterization:** What can we actually establish about each function's role, parameters, return, operands, effects, callers/callees and behavioural sequence, at explicit levels A/B/C?
- **Q3 — Developer presentation:** Can a reader browse by subject or address, find a function quickly, understand the version/ABI limitations, and follow precise original evidence?
- **Q4 — Reconciliation and quality:** Does the catalogue cover the source inventories, preserve colliding historical aliases, agree with—or explicitly qualify contradictions in—the 18 subsystem references, and pass independent review?

## 2. Build-pinned address and identity contract

The **entire first research release** is targeted to the pinned executable, not assumed applicable to future patches. Bind function identities and displayed addresses to:

| Field | Value / rule |
| --- | --- |
| Module | `Starfield.exe` |
| Retail resource version | `1.16.244.0` |
| Executable SHA-256 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Preferred image base | `0x140000000` |
| Canonical primary key | **Executable SHA-256 + module name + verified function-entry RVA** |
| Address conversion | `RVA = preferred_static_VA − preferred_image_base`; actual runtime VA requires the process's actual loaded module base |

Use `docs/audits/publication-readiness-b3/baseline-manifest.md` and original per-investigation source pins for build and byte provenance. Distinguish preferred static VA, RVA, relocated runtime VA, internal instruction site, call site, member offset, vtable byte displacement, saved-file/decoded-stream offset and physical ESM offset. **Never index an interior site as a callable function entry.** Do not equate a thunk, forwarding stub or wrapper with its target; preserve distinct entries and explicit relations where verified.

A cross-version correspondence is a **separate, evidenced relation**, not the primary identity. Design the catalogue so another verified EXE build can later gain distinct entries and an optional version-to-version mapping without overwriting 1.16.244.0. This assignment does **not** research a second build or select a public release tag/versioning number. Note `Starfield.esm` is independently pinned (SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`) but its data records do not redefine native-function identity. Keep per-claim historical save and installed-input qualification rather than assuming a universal historical load order.

### Historical-ID collisions are mandatory regression cases

Identifiers such as `SOR-FN-0062` **are not globally unique**. At minimum:

- `SOR-FN-0062` in `docs/function-register.md` denotes resource-region callback **static VA `0x1421e0f50`** (RVA `0x021e0f50`).
- `SOR-FN-0062` in `docs/experiments/crew/functions.csv` denotes the crew **Add available unassigned actor** function **static VA `0x142008540`** (RVA `0x02008540`).
- Investigate reported collisions on `SOR-FN-0063` and `SOR-FN-0064`, and systematically audit *all* historical identifiers, including experiment-local `Nxx`, `e1-xx`, export IDs and investigator labels.

Model historical aliases as **source-qualified, many-to-many mappings**: historical ID, exact source file/row or heading, module/build context, mapped canonical function (when resolved), and any ambiguity. The *same* alias text may name distinct functions in different files. The *same* function may have multiple names/aliases. Do not silently rewrite historical IDs, choose the latest alias as authoritative, or merge entries on labels, textual names or legacy IDs. When a source gives only an interior site or ambiguous address, preserve it as a **locator**, not an invented function record; provide an unresolved/source-local locator ledger or reported exclusion where useful.

## 3. Discovery and normalization — original evidence first

Perform a repository-wide, traceable inventory of **research-relevant, positively identified native Starfield functions**, drawing from these source classes:

1. Existing `docs/function-register.md` and `docs/state-register.md` as discovery aids, **not** infallible unique-key authorities.
2. Structured per-experiment `functions.csv`, native-function CSVs, source manifests, line-window inventories, native analyses and review corrections, including resource availability/generation, construction, positions, production, storage, cargo, crew, robots, power, defense, UI and save/runtime interfaces.
3. Original authored reports and accepted corrections when their function entries are absent from CSVs. Use reproducible extraction/search methods, not just a few handpicked examples.
4. Existing local exports or read-only Ghidra evidence **only where already available, permitted and needed to resolve an important source discrepancy**. Do not initiate broad fresh native analysis, regenerate massive export corpora, or modify Ghidra projects/databases.
5. The 18 current `docs/reference/*.md` pages and guides **last**, to find omissions, conflicting interpretations and helpful cross-references.

The inventory is **claim/function-led**, not an indiscriminate enumeration of every incidental `FUN_` string or opaque helper in giant decompilations. Include a function with a verified entry and a documented relevant relationship, even if only Level C. For vague incidental mentions, call-site-only references, unverified address strings or arbitrary unrelated imported library helpers, record the rule and count/reason for exclusion or flag them as unresolved candidates. Do not turn a finite, useful research register into a demand to annotate the entire game's binary.

Deduplicate on the canonical key **after** parsing and verifying address domain and entry classification. Source overlap must not erase differing operands, contradictory interpretations, qualification or original citations. Keep a provenance record for every contributing evidence item and a list of meaningful conflicts/decisions. Preserve negative/superseded observations under their source context.

## 4. Characterization policy and entry schema

Use **three nonexclusive depth levels** based on *characterization*, not confidence or publication readiness:

| Level | Meaning | Minimum requirement |
| --- | --- | --- |
| **A — Characterized** | Substantive validated/scoped mechanism, with meaningful operations, operands, effects and useful detailed description or pseudocode where evidence permits | Verified entry identity; accurate role; source-pinned behaviour, preconditions/effects and significant qualifications; parameter/return details when supported |
| **B — Partially characterized** | Verified entry and useful bounded behavioural evidence, but important semantics or prototype/control flow unresolved | Verified entry, limited role, exactly what is known/unknown and source |
| **C — Located** | Verified entry and relevance/call relationship, with limited independent semantics | Verified entry, reason for inclusion, explicit unknowns and source |

A high-confidence *address* can be Level C; a plausible full decompiler signature is not automatically Level A. Store **confidence, basis, review and evidence-access classification separately** according to `docs/EVIDENCE_STANDARD.md`. Where a precise detail is unverified, use `unknown`/`inferred`/`conditional` rather than an invented type or default. Don't promote function roles to universal callers or actual retail invocation based only on static evidence.

A full entry should support the following fields, omitting or marking unknowns as appropriate:

- **Identity:** canonical build/module/RVA; preferred static VA; optional observed runtime VA clearly session-scoped; stable source-derived catalogue record ID if useful (not legacy `SOR-FN`).
- **Names:** researcher-assigned plain-English descriptive label; Ghidra symbol **verbatim as seen** (`FUN_...` is an auto label, not a recovered Bethesda name); authentic symbol/RTTI name only if supported and typed; multiple source-specific aliases.
- **Purpose:** concise plain-English description and subsystem classification; material alternative interpretations.
- **Arguments/return:** exact observed input registers, calling convention/ABI evidence, parameter types or pointer classes and return register/meaning **only to their supported precision**. Disambiguate function signatures inferred by Ghidra from independently supported ABI facts. Note uncertainty about hidden `this`, output pointers, flags, virtual dispatch, XMM operands, etc.
- **Data:** object member offsets with owner/byte domain, constants, global addresses, vector/map layouts, state flags, lifetime and locking prerequisites where relevant.
- **Behaviour:** notable predicates, ordered branches, side effects, allocation/locks, failure/cleanup paths, meaningful callers and callees, and related producer/consumer dependencies; distinguish entry from interesting inner instruction sites.
- **Pseudocode:** **original, evidence-grounded reconstruction** for useful Level A (and selected B) functions; mark abstraction versus near-instruction-faithful reconstruction, omitted branches and exact evidence. Do not copy extensive proprietary decompiler bodies into public docs. No requirement to invent pseudocode for every function.
- **Evidence:** direct links to original function CSV rows/report sections, review/correction, native export/line-window locator (if private, clearly marked), executable/build pin, coverage/confidence, and pending independent-public-access classification.
- **External-use status:** `internal-only observation / external invocation not validated` unless an existing *specific* validated integration witness establishes otherwise. Never turn a signature/locator into a callable SFSE API claim.

Distinguish exact native name, Ghidra's automatic `FUN_...` name, user-assigned descriptive title and historically reused register ID. Use `docs/reference/glossary.md` for shared technical terminology, adding minimal new entries only where they clarify distinct entities. Do not conflate exposed Papyrus declarations, compiled script functions, virtual method slots and native executable entry points; if useful, cross-reference them from the native entries without treating them as the same function.

## 5. Deliverables and presentation

Create an accessible, maintainable addition under **`docs/functions/`**:

1. **`README.md`** — audience, build pin, legal/source-access constraints, A/B/C legend, address notation, read-first warnings about version compatibility and unvalidated external invocation; links to indexes and themes.
2. **`catalogue.csv`** (or an equally simple, documented text-native structured master format) — deterministic machine-readable records, keyed by build/module/RVA. Prefer a canonical record table plus **`aliases.csv` and `evidence.csv`** if a flat row cannot preserve multiple sources without lossy/opaque blobs. Any additional machine-readable sidecars must have a documented join/schema and deterministic verifier. No embedded proprietary disassembly/decompilation or private paths represented as publicly accessible files.
3. **`index.md`** — concise **RVA/address-ordered** master table containing static VA/RVA, descriptive label (or genuinely recovered name if available), short purpose, A/B/C level and link to full details. One canonical function per row. Keep it scannable; for large catalogues, deterministic generated per-range index pages or sections are permissible so long as there is one obvious master entry point and reproducible address sort.
4. **Thematic pages** — group detailed entries by actual function subject area, with navigation between subject pages and canonical index; suggested groupings: geography/resource generation; Workshop identity/position/construction; production; power; local storage/cargo; crew/robots/defense; UI/save/lifecycle. Adjust groupings based on discovered inventory and avoid multiple independently divergent full entries for a shared function. Use small cross-links when one entry serves many subjects.
5. **Evidence/coverage and reconciliation ledger** in `docs/audits/native-function-catalogue-d5bd/` (or a comparably discoverable audit folder): source inventories scanned, included/excluded/unresolved locator counts by source and level, canonical-identity dedupe, alias collisions, original-to-current-reference crosswalk, source-access qualifications, and any reported contradictions or source gaps.
6. **Deterministic validator** in a suitable tracked location (for example `research/function-catalogue/verify.py`) and minimal documented invocation. Check identity uniqueness, source-qualified aliases, calculated RVAs, canonical entry versus interior locator domain, sorted index, entry links, coverage ledger and deterministic regeneration/consistency. Python standard library is preferred; do not add dependencies merely to display a table.
7. **Bounded navigation updates** to `docs/reference/README.md`, `docs/guides/README.md` if genuinely useful, and the glossary/authoring standard only if needed. A minimal top-level README link may be added *if needed for two-click discoverability*; no broad repo-homepage rewrite. Keep `docs/function-register.md` intact as historical research; do not archive or replace it now.

Keep detailed tables readable; don't make the index a dump of every source alias, every instruction window or every unknown parameter. Put uncertainty and implementation details on linked pages/structured records. A machine-readable row may point to one full detail section, with other thematic consumers linking there.

## 6. Reconciliation and independent validation

Independent review must examine *the final exact snapshot*, challenge representative A/B/C classifications and read a meaningful cross-subsystem selection of native-backed entries. Include known difficult cases (resource-generation provider and consumer split; shared production scheduler; source versus runtime owner; crew assignment vs robot contribution; cargo fuel versus voyage; Locations UI adapter; save-framing helpers).

Required checks:

- **Known collision regression:** `SOR-FN-0062` remains associated with **two different canonical entries** from the two named source locations. Test `0063/0064` and report every other repeated alias, including source-qualified meaning. No collision may silently merge unrelated function identities.
- **Canonical dedupe:** multiple sources mentioning the exact same build/module/verified entry RVA converge without loss of citations, conflicting hypotheses or roles. Equal label with different RVA remains separate. A source using a call-site RVA does not turn into an entry.
- **Version/address rules:** all 1.16.244.0 entries use the declared executable hash, module and preferred base; RVA arithmetic and fixed-width/address sorting check. No cross-version locator is asserted from analogy.
- **Depth/evidence:** A/B/C level is justified by observed evidence; low-confidence prototypes and missing return paths remain explicitly unknown. Source confidence, scientific coverage and external-invocation status are independent.
- **Bottom-up coverage:** programmatic inventory of the original function tables and selected narrative reports with source accounting, inclusion/exclusion explanations and review of material omissions. Cross-check the 18 completed subsystem reference pairs **after** inventory; preserve historical interpretation conflicts and report rather than silently overwrite accepted research.
- **Reader journeys:** (1) start with a known RVA and locate its role/evidence; (2) start with a subsystem and find significant functions/caller relationships; (3) start with a colliding historical ID and distinguish both functions; (4) start with an unknown prototype and see exactly what is not established; (5) start with an SFSE integration goal and find the explicit no-safety-guarantee and qualified ABI facts. Verify links/anchors case-sensitively and a clean tracked-data-only catalogue rebuild/check without `.local-work/`.
- **Preservation/security:** no proprietary code dump, complete decompiler text, raw copyrighted game files, source-private path-as-public-evidence illusion, protected-save modification, binary patch/hook, runtime injection, new mod, or live experiment. Audit diff for unexpected material and leaked local credentials/private data. No staging, commit, push, release or public exposure.

Review scientific meaning, engineering schema/data integrity, editorial readability and completeness **separately**; report Q1–Q4 and AC below independently. Record any rendering or unavailable-input limits honestly. A local successful build/verifier does not by itself clear release rights or inaccessible original evidence. Publication remains **NOT READY / NOT CLEARED**.

## 7. Acceptance criteria

- **AC01 — Source-led inventory:** A reproducible census of all relevant original native-function tables and material narrative/legacy-register sources exists; included/excluded/unresolved rows and rationale are traceable, not selectively sampled without disclosure.
- **AC02 — Build and canonical identity:** Every function has a verified build/module/entry-RVA key; address domains and relocations are correct; instruction sites/thunks/wrappers are not silently conflated.
- **AC03 — Collisions and aliases:** Historical IDs are source-qualified and searchable; all collisions audited; `SOR-FN-0062`, `0063` and `0064` tested. No alias-based false deduplication.
- **AC04 — Accurate depth:** A/B/C classification matches evidence. The source uncertainty, argument/return/ABI, current-state and safe-invocation limitations are explicit and not invented.
- **AC05 — Useful full entries:** Subject pages describe the established roles, operands and effects of identified functions at supported depth; significant Level A entries include useful independently written pseudocode where appropriate; every material claim links to source evidence.
- **AC06 — Developer index:** Master index is correctly address-sorted, compact and linked to full entries, thematic pages and a pinned build notice. Machine-readable source and human index agree.
- **AC07 — Research reconciliation:** Bottom-up results have been checked against all 18 accepted subsystem references, recording gaps and conflicts without revising accepted science or erasing history.
- **AC08 — Independent reader checks:** Deterministic validator and the five reader journeys pass on the exact final tracked snapshot without private working data; all cited links and anchors are checked. Explain any checks that cannot be reproduced independently.
- **AC09 — Reviews and preservation:** Independent scientific, engineering and editorial reviews issue explicit dispositions and scrutinize collision handling, representative difficult entries, pseudocode, source rights and unintended edits. Work remains unstaged/uncommitted/unpublished.
- **AC10 — Publication/build policy and staffing:** The catalogue and documentation state the first-release pinned executable target and future version-specific extension rule without claiming newer-version support. **No more than two D5BD sub-agents are concurrently active; the exception is task-only and the standing single-agent cap remains unchanged thereafter.**

A missing nonessential prototype or low-level detail is not an AC failure **if** its genuine uncertainty is represented and the function is placed at the appropriate depth. But an address error, false identity merge, fabricated signature, hidden major source omission or falsely published accessible evidence is material and requires correction. If exhaustive ingestion of the finite research corpus becomes unexpectedly impractical, report exact skipped source classes/counts and rationale rather than claiming full coverage or silently narrowing scope.

## 8. Execution boundaries and handoff

**Authorized:** read/search repository and already lawful local source ledgers; bounded scripts for extraction, normalization, CSV/Markdown generation and validation; necessary documentary additions/edits; independent review. Existing protected source files may be hash-checked/read only within already permitted access boundaries. Prefer existing accepted native findings and source exports; fresh native interpretation must be narrowly justified by a specific discrepancy and reported, not pursued as an open-ended investigation.

**Not authorized:** modify `.git` refs/index or stage/commit/push; change original experiment reports, historical `docs/function-register.md`, protected saves, installed game inputs, Ghidra projects, private archives or original receipts; run/instrument the game; alter binaries, attach a live debugger, prototype SFSE hooks or perform plugin injection; invent mod-safe API signatures; archive/move existing briefs/audits; create public Release assets; publish or change repository visibility. Do not require all `.local-work/` data to remain after release. Indispensable source dependencies without a tracked or approved reproducible public route are labelled **PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING** and referred to later publication work.

**Staffing:** The user expressly authorizes **up to two active sub-agents at once for this D5BD assignment only**. They may divide original-source inventory and developer-documentation/reconciliation work, but coordinate on one canonical identity/schema and avoid simultaneous conflicting edits. The supervising agent is responsible for integration and a **genuinely independent** final critique of the merged snapshot. This exception expires when D5BD finishes or is abandoned; future briefs revert to one unless the user explicitly changes the limit again.

**Final delivery:** Supply a short Codex summary listing Q1–Q4, AC01–AC10, source census and characterization counts, collision findings, documented unresolved sites, generated paths, command/verification receipts, reviewer verdicts, exact task-only and complete patch hashes/manifests, any publication dependencies, and the fact that nothing was staged/committed/pushed. Preserve original input brief if that is the repository's normal workflow. Suggested commit message (for maintainer use only): `docs(research): add version-pinned native function catalogue and reference`.
