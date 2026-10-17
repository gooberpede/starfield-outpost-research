# E3 verification and independent review package

2026-10-17, Australia/Sydney. [Original authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_E3_fabricators_manufactured_production.md),
[frozen contract](contract.md), [answer-first report](report.md).
Proposed assignment disposition: **COMPLETE** bounded offline native research.
Independent formal review01: **ACCEPT** for the exact sealed package below.
Maintainer critical review and integration remain separate.

| Original mandatory criterion | Result | Evidence and limit |
|---|---|---|
| A: Population, native classes/variants/tiers and exceptions | PASS scoped definitions | definitions.md; facilities.csv; catalogue05: 45 keyword-classified CONTs, 30 construction-linked bases, 11/10/9 family catalogues; exceptional definitions retained |
| B: Native catalogue admission and possible filters | PASS instruction-backed | native.md; fresh e3/002 140f8be60 and e3/004 loader; AVIF category 9, flags mask 2 clear, IRES recipe/AV/base property presence; generic known true, recipe CTDA not itself enforced on inspected paths |
| B: Current choice, UI action, registration, reset and persistence | PASS scoped STATIC/SAVE | native.md; E2 event/apply and BF saver/loader; resource map serializer; saves.md's 17 preset/base/row joins are explicitly definition-derived, not explicit saved BF override |
| B/F: Exact E2 shared functions and divergences | PASS STATIC | reuse.md; generic versus species/knowledge branch, organic-only auto-initialization; shared recipe-keyed UI/application/input/lifecycle |
| C: Every ordinary recipe/input/output/count and identity | PASS scoped definitions | recipes.csv preserves IRES/AV/COBJ/MISC, inputs/counts/interval/conditions; 30 distinct ordinary outputs, all NNAM 1; 308 independent physical record rereads |
| C: Binding, structural support, sufficient inputs and unlock boundary | PASS STATIC | native.md; 1409e9960 structural source match distinct from 140f7f6f0 stock cap; construction RSPJ versus output COBJ metadata; no manual crafting substitution |
| D: Incoming/outgoing direction and compatibility on change | PASS STATIC/SAVE | destination-keyed registry, direct outgoing inversion, incoming transitive walker; concrete null/empty/keyword/product filter rules and at-most-first outgoing removal |
| D: Local upstream chains, buffers, cargo, multiple candidates and loops | PASS bounded SAVE/STATIC | saves.md; detail05: 17 consumer traces, 24 required-resource producer witnesses, 53 buffer and 29 incoming cargo path observations; visited adjacency retained, zero cycles detected in this sample, no universal cycle absence or stock claim |
| E: Current power/halt/operating states | PASS scoped STATIC | native.md plus E1 primary reason evaluator/power/halt evidence; reasons 5/7/9 distinct, reason zero current eligibility distinct from output; no invented activation Boolean |
| E: Intervals, quantity, modifiers, elapsed clocks/skipped time and creation | PASS STATIC/definition derivation | native.md and reuse.md; exact shared scheduler/timer/request paths, ordinary no-NNAM-multiply branch, 7.92-63.72 second definitions, manufacturing-specific actor predicates |
| E: Several concrete examples and intersecting UI/statistics | PASS scoped calculation | definitions.md across all three classes with exact recipes and 60/D nominal values; shared 140f7bf80/aggregate refresh bounded, no measured per-fabricator throughput |
| F: Coherent native reference and existing shared register | PASS proposed research | native.md layouts/operands/ownership/lifecycle/effects/uncertainties; existing native CSV N225-N234 additions and E1/E2 reuse; no competing registry or callable API claim |
| Mature inventory beyond Save52 and actual corroboration | PASS bounded SAVE | 278 inventory rows consulted; 184 positive-beacon candidates, 122 parsed, 41 parser qualification gaps, 21 unavailable frozen sources; 105 positive saves, 1,190 repeated producer observations |
| Deterministic verification/regression, protected inputs and prose | PASS audited scope | verification01: 417 checks, exact CSV cells, 163 available originals rehashed, ESM/executable/cache and 15 Ghidra project/database files preserved; E2 e3regression01 passes 90 recipes/six selected AV joins/six Water paths |
| Source/credit/evidence-state and seven delivery items | PASS authored package, review pending | report family, scripts/README, shared register/state/index/source/credit updates; raw LOCAL-ONLY and authored REVIEW-REQUIRED; exact patch receipts referenced below |
| Exact complete/task-only patches including untracked text | PASS | review01 exporter and reviewer checks HEAD/index, actual path inventory, complete and task-only exact forward/reverse bytes in disposable D:/tools trees; supplied pre-existing brief belongs only in complete patch |
| Mandatory independent review and substantive rework | PASS / ACCEPT | Fresh independent read-only reviewer inspected primary evidence, independently reproduced definition/save checks and challenged/corrected interpretation errors; actual disposition and reviewed snapshot below |

## Actual checks, preserved failures and boundaries

Local primary receipts reside in `.local-work/e3-fabricators/`; [source pins](sources.csv)
locate exact files. Final definition receipt is `catalog05.json`; historical
inventory is `saved01/summary.json` and per-save `HIST-*.json`; detailed saved
corroboration is `detail05.json`. Intermediate catalogues/details remain preserved.
Details depend on the pinned earlier catalogue04 population, historical scan on
catalogue02; final catalogue05 changes flag-mask checking, not those populations.

`research/e3-fabricators/verify.py --run verification01` passed 417 checks:
CSV content/identity/membership, exact recipe fields, 30 ordinary count metadata,
17 base/producer corroborations, 184 inventory outcomes, 163 available original
save hashes, executable/ESM/E2-cache pins, native register source functions/RVAs,
15 Ghidra project/database file hashes, HEAD/index, supplied brief, Python AST,
UTF-8/LF/whitespace and prose corruption/fused address/version-label checks.
Later verification receipts cover the completed report/review prose.
The audited original-save scope is those 163 available candidate sources; 21
missing original paths are unavailable, not verified intact by this run. No
claim is made about unaudited game/configuration files or every save on disk.

`research/e2-organic/verify.py --run e3regression01` passes the existing E2 table,
340 physical-check receipts, 3,851 source-pattern receipts, six selected AV joins,
six directed Water paths, 40 original register rows and current pinned sources.
It rechecks existing E2 results; it is not a fresh derivation of every E1/E2 claim.
E3's catalogue performs the fresh 308 physical definition rereads and complete
ESM group/header walk. Hashes prove integrity; independent instruction/operand
review supports semantics. No native code was invoked.

Native exports001-005 use the existing owned OutpostRecon and unchanged local
E2ReadSession wrapper, Ghidra 12.1.2_PUBLIC / Temurin 21.0.12+8, **readOnly and
noanalysis**. Requests, TSVs, done markers and invocation log remain local.
The script enumerates existing functions/data; no symbols, types or comments
are changed. Wrapper stop file ended the read session. Ghidra database/project
before/current hashes agree for all 15 recorded content files; transient locks
are not analysis content. Initial launcher settings lookup failed with access
denied before project access; the existing direct-Java workflow succeeded using
local settings/cache. No permission escalation or altered global configuration.
Two guessed selectors (`1409c8990`, `140f7cc80`) returned NO_FUNCTION_AT; the
supported halt entry is `140f7cc70` from E1. Complete other requested exports
remain usable; no absence semantics were inferred from those locator failures.

Preserved research diagnostics: catalogue01's incorrect EditorID prefix omitted
resources; catalogue03 replaced name filtering with exact NAM1 relationships.
Flag checking was corrected from mask 1 to mask 2 under native loader/callback
review; actual ordinary flags satisfy the corrected predicate. Historical scan
initially stopped on unavailable HIST-0167, then resumed with explicit unavailable
outcomes and revalidated prior hashes. Initial details assumed a leading BF and
then an explicit selected AV; closed extra parsing and definition-derived preset
evidence corrected those assumptions. No failed attempt is called a semantic
negative or concealed by deleting its receipt.

The prose audit checks UTF-8 codepoints and manual reading for fused numbers,
VAs/RVAs, version strings and malformed spacing. Earlier E2 encoding failures
are a known hazard; no unrelated mass formatting is performed. Link checks cover
authored/modified documents, retaining pre-existing missing-target exceptions.
Scripts' inputs, outputs, prerequisites and cleanup are in the
[research README](../../../research/e3-fabricators/README.md).

## Packaging and outcome dimensions

Review patches use `.local-work/diffs/e3-fabricators-<revision>-complete.diff`
and `-task-only.diff`; package manifests are
`.local-work/e3-fabricators/package-<revision>.json`. Complete includes all current
uncommitted tracked and untracked text. Task-only excludes the unchanged supplied
brief, the only pre-existing untracked file. Manifest records file hashes, path
coverage, status, HEAD/index and exact forward/reverse reconstruction checks.
No index is used to construct patches. Disposable application trees remain local.

Excluded: raw/original/decoded saves, game binaries/assets/definitions, memory,
Ghidra databases/native decompilation, private bulk receipts and D:/tools scratch.
Metadata/source hashes locate these without packaging their bytes. Exclusion is
disclosed; neither privacy nor publication eligibility is cleared by completeness.
No outside implementation, dependency installation, download, communication,
fork, PR or new licence basis is introduced. Credits/source lineage are updated.

Scientific result: positive bounded offline map. Actual loaded state and accepted
output: NOT TESTED. Integrity: PASS within audited scope. Target survival: not
applicable; no game process. Cleanup: temporary decoded scratch cleaned by owned
decoder; original inputs and existing analysis content preserved. Authority:
offline-only; no launch, attachment, injection, native call, save/configuration
mutation, staging, commit, push or disclosure. Reviewer acceptance, if returned,
will not authorize integration or expansion.

## Independent review01 and final package

The independent reviewer returned **ACCEPT** for package-review01 SHA-256
`7d9d56d17c70e98f46ae9739aedd970172ea6225bd1524d6d22f61c4c9a189ac`.
The actual return is preserved verbatim in local `independent-review01.md`.
The reviewer independently ran verification `reviewer01` (421 PASS assertions),
`reviewerCatalog01` (fresh complete ESM walk and 308 physical rereads, exact
catalogue05 result), and `reviewerDetails01` (same 17 configuration joins,
307 endpoints and 24 required-resource producer paths). Only decoder elapsed
seconds differ in the repeated detailed receipt; that nonsemantic difference
was isolated after an initial exact JSON comparison failed. All substantive
fields agree; this is not a suppressed content mismatch.

Review additionally checked 46 source pins, all 26 manifest file hashes,
actual tracked/untracked path coverage, both patch hashes and inventories,
reverse applicability against the actual tree, forward applicability against
baseline scratch, 1,180 Markdown targets and `git diff --check`. Earlier primary
instruction review challenged the generic callback, COBJ conditions, incoming/
outgoing policy, flag mask, saved BF/preset distinction and NNAM/request count.
Substantive corrections are incorporated within this assignment. The supplied
brief and original mandatory criteria are unchanged. The independent reviewer
did not edit the repository.

Final status/prose recording and package references are the only follow-up edits.
Final artifacts are `.local-work/diffs/e3-fabricators-final01-complete.diff` and
`.local-work/diffs/e3-fabricators-final01-task-only.diff`, with file/hash manifests,
status, exclusions and exact applicability/content checks in
`.local-work/e3-fabricators/package-final01.json`. The final prose/protected-input
receipt is `verification03.json`; final status edits are submitted for narrow
snapshot confirmation. Independent ACCEPT supplies no maintainer integration,
commit, publication or live authority.
