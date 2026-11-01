# P1 active identity and lifetime investigation

2026-11-01, Australia/Sydney. Parent D5AB INCOMPLETE / REWORK; D5R OPEN;
B2 NOT AUTHORIZED. [Frozen P1 contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P1_native_source_identity_lifetime_closure.md).

## Frozen controlling questions

- P1-Q1: Establish ownership and lifetime at every observation boundary,
  including aliases, detached work, cleanup and replacement. Completion requires
  positive native evidence for necessary edges or removal of unsafe dependencies,
  with adverse controls.
- P1-Q2: Distinguish allocation, geographic identity and visited token using
  initialized, stable semantic operands. Demonstrate a positive join and refuse
  ambiguous histories; refusing everything cannot complete the question.
- P1-Q3: Account for normal and exceptional lifecycle routes, virtual dispatch,
  cleanup and destruction, with independent challenge.
- P1-Q4: Qualify the exact final source/build/schema/consumer combination with
  native/adverse tests, impacted P2 regressions and independent review.

All four questions start INCOMPLETE. These summaries preserve the normative
questions and eight acceptance criteria in the linked brief without amendment.

## Checkpoint 1: admission and retained evidence

Initial Git status contains only the supplied untracked P1 brief. No tracked or
staged change is present. Required policies, original D5AB contract, C1/C2
assessment and matrix, accepted P2 report/provenance/review, D5S retirement and
D5V/D5Z lifecycle records are starting evidence, not new experimental results.
Observer inspection confirms a raw 0x70-byte read in `lookup_hook` whose lease is
not proved by the ProcGen lock. `definition()` includes padding at source
`+0x39..+0x3b`. Neither observation is accepted as safe merely because a fixture
passes. Existing selected/visited callbacks consume operands without dereferencing
the selected source.

The authorized experiment reads pinned installed bytes and existing analysis
state, exports narrow native records read-only, and builds/runs disposable owned
hosts if a candidate is developed. Outputs stay in fresh ignored task directories.
No game, deployment, protected-save write, database edit, network disclosure or
Git integration is authorized. Stop affected execution on identity mismatch,
failed C:/D: 40,000,000,000-byte free-space guard, corrupt evidence or actual
enforced refusal. Preserve originals and failed outputs; no cleanup of prior work.

## Branch register

The [C2 matrix](d5ab-c2-evidence-matrix.md) supplies the original primary locators
and counterexamples for every row. The table preserves admission dispositions;
later checkpoints and the final matrix record their resolution without deleting
the competing alternatives. No proven bounded C2 edge is reversed here.

| Branch | Starting evidence / competing interpretation | Disposition and next action |
|---|---|---|
| L01 | Constructor dedup/allocation E2; new birth differs from dedup. | OPEN: follow returned pointers and unwind. |
| L02 | Semantic initialization before birth; padding unproved. | OPEN: remove padding dependency and trace used operands. |
| L03 | Actual store differs from reserve sentinel; unpublished return exists. | OPEN: account for failed publication and exceptions. |
| L04 | E3 incomplete; E4 pseudo fragments lack parent mapping. | OPEN: bind PE unwind metadata to parent/source slots. |
| L05 | Three constructor callers and cell population retained. | OPEN: follow aliases to actual owners. |
| L06 | Dimensions and +0x178 later written; not current semantic identity. | OPEN: trace semantic writers; size census is insufficient. |
| L07 | Bulk erase/unlock/free reaches fence 3. | OPEN: exceptional and overlapping publication controls. |
| L08 | Standalone erase/unlock/free reaches fence 4. | OPEN: prove all relevant free callers. |
| L09 | Two Grid destructors reach clear. | OPEN: bind virtual dispatch. |
| L10 | Shift can retire source while Grid retained. | OPEN: retain counterexample; test invalidation/ABA. |
| L11 | Detached continuation lacks prep reader. | DISPROVED as protection shortcut: seek operand-only design. |
| L12 | Selected/visited observer does not dereference source. | OPEN: engine consumption and allocation continuity differ. |
| L13 | Map lock protects map, not proved selected-source lease. | OPEN: eliminate retrospective source copy or prove owner. |
| L14 | Named resets/destruction covered; context replacement unresolved. | OPEN: follow registration/installation and owner epochs. |
| L15 | Pointer/token/key/allocation equivalence disproved. | OPEN: independent reuse/collision and missing-fence controls. |
| L16 | Missing birth/publication refuses identity. | RETAIN refusal; demonstrate a qualified positive lifecycle. |
| L17 | Same-size census includes unrelated objects and unknown funclets. | OPEN: bind pointer origins; no type inference from size. |
| L18 | Cell/cursor copies are raw aliases. | OPEN: enumerate cell variants and cursor owners. |
| L19 | Pointer collection invokes virtual destructor. | OPEN: bind concrete vtables and pointees. |
| L20 | Population and fill/edge/corner insertions retained. | OPEN: resolve virtual cleanup and auxiliary 0x1409865e0. |
| L21 | Cell lookup provides no source lease. | OPEN: account for enumeration and use interval. |

Independent read-only native specialist is examining L04 and L18-L21. The primary
owns acquisition, integration, controls and final qualification. No source change
or native execution has occurred at this checkpoint.

## Checkpoint 2: primary acquisition and candidate redesign

Read-only `p1-export01` and `p1-export02` complete with unchanged database pins.
Constructor FuncInfo at static VA `0x1454c00e4` maps two cleanup actions: lock
holder `+0x60` calls `0x1402b6280`; allocator-functor object `+0x68` calls
`0x1402c5b40`. IP states place string call `0x1409830d9` in state 0, with only
lock cleanup. The earlier `0x143784550/560/570` fragments belong to caller
`0x140849670`, not this constructor. E3 remains incomplete historical evidence.
Microsoft's installed `ehdata4_export.h` was consulted for metadata semantics;
no header code, decoder implementation or new dependency is incorporated.

Concrete fill/edge/corner vtables bind deleting destructors `0x1409858d0`,
`0x140985c20`, `0x140986050`. These free their receivers, not source slots.
Auxiliary `0x1409865e0` and `0x140988b60` copy raw source pointers into Grid
`+0x28` records; their consumers remain under investigation. Grid `+0x38/+0x40`
contains modifiers, not the cell array. The specialist followed a further raw
source alias at GridFile `+0x278`; its owners/consumers must be accounted for.
L04 is supported at constructor-local unwind scope; L05/L06/L17-L21 remain open
until the actual alias graph is closed. No size-only exclusion is adopted.

Schema-4 candidate removes the native source read in `lookup_hook`. Lookup
events retain stack/map operands and zero source payload; the new reducer
reconstructs a copy from a qualified constructor witness through lookup time.
Semantic comparison excludes padding. Schema-3 reducer remains byte-identical.
Birth/publication/entry/decision epochs must agree, so an omitted fence with
changed native epoch cannot silently bridge a lifetime. This intentionally
refuses sources carried across a reset without a fresh birth witness.

Preliminary independent review found bypass-prefix validation and admission-only
"later" ordering defects. The candidate now requires a complete matching
Entry/Selected/Visited prefix and native order, including cross-thread tie
refusal and native prior-decision checks. Reviewer also identified a tautological
birth-versus-reconstructed-lookup comparison; it was removed. Immutability must
come from native writer evidence, not that comparison. Reproductions and exact
final tests are still required before any completion claim.

Original-instruction controls use only private mapped ranges and a recording
allocator callback. `p1-native-instructions01` failed before instruction execution
because the mapper used page rather than Windows allocation-granularity alignment.
The corrected mapper reserves 64 KiB regions; `p1-native-instructions02` passes
nine receiver/cleanup controls with inaccessible source slots. This is not a
complete engine constructor or retail unwind test. The development DLL build
`p1-native01` overlaps later edits and cannot qualify final source identity.

## Checkpoint 3: source-rooted closure and qualification

Fifteen complete read-only exports now account for the ordinary source-rooted
receiver graph. The additional GridFillFile alias, modifier consumers and both
late provider helper routes read semantic scalars/file holders without writing
selected identity or releasing raw source allocations. Ten ambiguous free
funclets map through exact FH4 metadata to twelve parent entries and locally
allocated non-geographic object families; the `.rdata` action-reference cross-check
has no unmapped literal. L05/L06/L17-L21 therefore have positive receiver/argument
evidence, rather than size-based exclusions. The matrix and source ledger retain
exact addresses, function spans, source hashes and limits.

L14's last competing hypothesis was post-reset construction on an old retained
Grid. Direct primary and independent reviewer inspection found that
`0x140785190` acquires landscape owner `+0x08` before Grid capture and holds it
through both synchronous callback routes, stack-functor destruction and population
updates. `0x1407846d0` takes the same lock around Grid null/release. X13 proves
the normal `0x140784c40` and overlay `0x140adb6b0` callbacks do not escape.
Construction precedes reset or uses the post-reset slots. Detached density only
selects sources; its old births fail the changed-epoch join. An extra owner fence
was evaluated and rejected because the existing proof covers this edge and a
naive outer fence would disturb Cold qualification.

Native03 passes all 66 expected-exit cases with unchanged source. Repro01 passes
three controls with the same inputs. Original-instruction Final04 passes eleven
controls. Consumer Final01 passes 300 checks. Final02 adds explicit boundary
oracles but fails one incorrectly written expectation: it demanded deletion of
an earlier valid visited identity when retirement occurred later at lookup.
That earlier observation is sound partial evidence. Final03 correctly requires
one earlier identity, an invalid lookup, and zero completed chains; all 316 checks
pass, including complete historical schema-3 comparisons and unchanged B1 output.
The failure remains in Final02's progress file and is not reclassified as a pass.
Fifty-four unchanged original schema-3 semantic oracles and nine worker-lease
regressions pass. Controller/queue/sharing batch completes successfully against
Native03; exact aggregate provenance and final review remain to be verified.

P1-Q1–Q3 have proposed COMPLETE scoped answers in the final matrix, subject to
independent full-contract challenge. P1-Q4 remains INCOMPLETE until the exact
combined provenance, complete prose review and verified delivery package pass.
All branches L01–L21 now have a scoped disposition; no material native lead is
silently abandoned. This does not complete D5AB or establish retail safety.

## Checkpoint 4: final-review getter branch reopened

The first exact-snapshot reviewer return accepted the package, but the primary's
last completeness challenge exposed a specific gap in that acceptance: concrete
cell getter bodies do not establish the safety of every consumer of their returned
source pointer. The reviewer explicitly superseded its unconditional ACCEPT with
REWORK. This is a tractable P1 proof branch, not a P3 deferral or terminal barrier.
The tested runtime source remains frozen; further native evidence and documents
will receive independent delta review.

Branch **L18-G** extends original L05/L06/L18 without changing the frozen questions.
Known additional callers are Grid helpers `0x1409868f0`, `0x1409869a0`,
`0x140986a50`, and upgrade helper `0x140986080`. The provider is one of three
direct callers of cell lookup `0x140985870`; the caller at `0x14078dd73` enumerates
through the known cursor route, while `0x14078e9c2` needs its containing body.
Source-to-file map keys and forwarding into another cell appear distinct from
source ownership, but their actual argument/return flows must be checked.
The specialist is acquiring the missing caller and a bounded Grid-cell consumer
census. P1-Q1/Q3 and P1-AC02/03 remain INCOMPLETE until this branch closes;
earlier engineering/hash/editorial checks do not substitute for that evidence.

## Checkpoint 5: getter return-flow closure

L18-G now has primary return-flow evidence. The source getters feed one known
comparison, four upgrade-to-corner insertion calls and eight pointer-key map
lookups returning file holders. The remaining direct cell-lookup caller uses
only a cell type enumeration; another Grid interface uses a cached file key and
returns a file holder. None adds a selected-source writer or release route.
The bounded Grid-component census corroborates these classifications across
31 functions, 5,083 instructions and 251 relevant contexts; it is not substituted
for the individual pointer-flow bodies or presented as a whole-program proof.

The independent reviewer read the additional bodies, verified the two new export
hashes/counts and accepted the corrective proof delta. Runtime source, DLL and
test oracles did not change. The final source ledger now has seventeen exports,
ninety-three full function records and one receiver-census record. P1-Q1–Q3
again have proposed COMPLETE scoped answers. Final updated documentation,
provenance, editorial coverage and verified manifests return for exact delta
review before P1-Q4/AC08 completion. Initial ACCEPT, subsequent REWORK and the
corrective proof review remain separate outcomes.

## Checkpoint 6: independent whole-package acceptance

Review04 restores engineering/scientific and separate editorial ACCEPT on the
updated exact snapshot. P1-Q1–Q4 are COMPLETE and P1-AC01–AC08 PASS within the
frozen offline scope. The reviewer independently matches thirty file hashes,
54 receipt hashes and 21 runtime component hashes, inspects the new diagnostic,
provenance delta and complete changed proof/review prose, and explicitly accepts
the intentional literal-path screen exception. No mandatory P1 branch remains
open at this scope. No experiment is rerun by the reviewer.

Only self-describing review/Q4/AC08 closure metadata changes after that verdict;
the final package is refreshed and sent for narrow independent closure review.
Source, DLL, schemas, test oracles and experimental receipts remain unchanged.
D5AB remains INCOMPLETE / REWORK, D5R OPEN, P3/P4 OPEN and B2 NOT AUTHORIZED.
Maintainer critical review/integration and publication remain separate gates.
