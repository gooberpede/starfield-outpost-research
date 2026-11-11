# P1 source identity and lifetime closure

2026-11-01, Australia/Sydney. **P1 COMPLETE / ACCEPT for its offline identity
and lifetime contract.** D5AB remains INCOMPLETE /
REWORK, D5R OPEN and B2 NOT AUTHORIZED. This work neither identifies B1's missing
first event nor validates retail behavior.

[Frozen contract](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AB_P1_native_source_identity_lifetime_closure.md`),
[active ledger](d5ab-p1-investigation-ledger.md),
[native matrix](d5ab-p1-source-identity-lifetime.md),
[provenance](d5ab-p1-provenance.md),
[parent mapping](d5ab-p1-parent-mapping.md), [review](d5ab-p1-review.md).

## Direct answers and scope

| Question | Independently reviewed outcome | Answer and evidence |
|---|---|---|
| P1-Q1: ownership and lifetime | COMPLETE | The observer reads source memory only while constructor-private. It records already consumed pointer/token operands at selection, visited and store, and stack/map operands at lookup. Schema 4 removes the unsafe lookup dereference. Birth/publication, matching producer epochs, lifecycle fences, loss and native ordering qualify or invalidate allocation continuity. The source-rooted matrix accounts for cells, cursors, auxiliary records, modifiers, terrain files, detached work, cleanup and context replacement. No source lease is invented. |
| P1-Q2: identity correctness | COMPLETE | Allocation witness, raw pointer, geographic scalars and visited token remain distinct. Every used semantic byte is initialized before birth; padding and unused/mutable fields are excluded. Native alias/writer tracing supports the chosen immutable scalar scope. Normal and later-bypass fixtures qualify positively; reuse, collisions, missing publication and ambiguous order refuse stronger attribution. |
| P1-Q3: native lifecycle coverage | COMPLETE | Constructor unwind is bound to its actual metadata, concrete cell/file/modifier virtual methods are resolved, all ten ambiguous free funclets have non-geographic allocation-slot origins, and creation/reset synchronization closes old-Grid construction across owner changes. Existing fences cover the source releases in that ordinary graph. This is build-specific graph closure, not protection against arbitrary corruption, injected writers or replacement vtables. |
| P1-Q4: exact final qualification | COMPLETE | Native03, identical-input Repro01, Original Instructions04, Reader Final03 and affected P2 regressions pass with exact source/component pins. Independent Review04 accepts the complete engineering/scientific/editorial snapshot; the review record governs final closure verification. |

Confidence is high in the pinned static paths and finite offline controls.
Coverage is the ordinary native receiver/argument graph on Starfield 1.16.244.0,
executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The semantic identity fields are stable within that graph; this does not make a
content-derived token globally unique or a source pointer a reference-counted
lease. A future authorized episode may qualify a freshly witnessed Feynman V
source, including bypass, under these premises. Target occurrence and successful
retail observation have not been tested.

## Chosen design and rejected alternatives

Schema `sor-d5x/4` keeps eighteen production sites, seventeen event kinds and the
312-byte payload. The only production acquisition change removes the selected
source read after protected map lookup. Lookup payload source bytes are zero;
the consumer reconstructs semantic identity from an independently qualified
private birth through lookup time. It does not claim a second runtime source
snapshot or a runtime mutation detector. Version 0.4.0 identifies the new DLL.
Schema 2 and schema 3 dispatch to their historical interpretation paths.

The consumer requires one matching Entry/Selected/Visited prefix and native
causal order even for a standalone bypass. Birth, actual publication, entry,
visited and lookup must share the producer epoch. Missing/late lifecycle events,
changed epochs, hazards or loss refuse continuity. A source surviving reset
without a new birth is intentionally unqualified. Later bypass is optional, must
belong to the same allocation and ProcGen epoch, and must occur after the actual
store in native time. Delayed admission and cross-thread timestamp ties cannot
manufacture that order. Colliding tokens or geography across distinct allocations
refuse firstness; sound earlier observations remain available.

Grid retention and the ProcGen map lock were rejected as source leases because
the D5S detached-retirement counterexample and unlock-before-free paths disprove
those shortcuts. Retrospective raw copying was removed rather than defended by
read success. Token uniqueness, pointer equality, geographic singleton support
and a refusal-only reducer were rejected as substitutes for positive identity.
A global deallocator hook would broaden interception and recording pressure
without need after the actual source-owner graph was resolved. An outer owner
installation fence was considered, but existing lock/callback evidence closes
that edge; a naive added fence would invalidate Cold semantics.

All original event categories remain unfiltered. The capability comparison,
exact native addresses, semantic byte selection and L01–L21 accounting are in
the matrix. The historical schema-3 observer's lookup premise remains historically
unqualified; its captures are not reinterpreted as schema-4 evidence.

## Qualification and independent oracles

| Suite | Actual result | Scope and independent oracle |
|---|---|---|
| Native03 | 66/66 expected exits | Actual DLL, bridges, recorder and disposable host. Existing 61 cases plus inaccessible lookup, retirement/reset at lookup, unpublished object and modeled constructor exception. Source unchanged during build/tests. |
| Repro01 | 3/3; identical DLL | Same complete source inputs; normal, later bypass and inaccessible lookup. Supplements the full suite. |
| Original Instructions04 | 11/11 | Pinned constructor dedup/bounds-refusal, cell destructors and constructor cleanup helpers execute in an owned process. Explicit bounds/origin/lock/free callbacks; inaccessible source slots and exact receiver-write/free oracles. Not a full engine allocator or constructor-exception replay. |
| Reader Final03 | 316/316 | Final packaged consumers; explicit positive, omission, loss, collision, epoch, damaged evidence, malformed bypass and native/admission inversion oracles. Includes all 60 retained P2 schema-3 session comparisons and full schema-2 B1 equality. |
| Original schema-3 semantic regressions | 54/54 | Unchanged original AST oracle block, accepted P2 captures, final compatibility reader and byte-identical schema-3 reducer. |
| Actual recorder/controller | 26/26 | Original P2 worker death, controller restart, identity/ACK/STOP, loss and closed-readback controls, bound by the P1 regression wrapper to all current runtime sources including the new reducer. |
| Sharing | 1/1 | Actual worker interoperability; old share policy returns Windows error 32, current owned STOP/loss/readback reconciles. |
| Queue | 9/9 | Production header recompiled at 1,024/8,192/32,768 cells, three repeats; exact admitted-ID/order/count oracles. All paced lossless envelopes lose zero; deliberate overload remains counted failure of losslessness. |
| Legacy worker lease | 9/9 | Original schema-3 own-thread authentication/exit controls on the broadened schema-3/4 lease admission. |
| Exceptional metadata | 12 parent records | All ten named action literals and their allocation origins accounted for; zero decode errors or unmapped `.rdata` action references. Static metadata, not retail unwind execution. |

The [selected result metadata](d5ab-p1-test-results.json) and provenance ledger
bind exact receipts, component hashes and commands. Hashes authenticate bytes,
not ownership semantics. The DLL SHA-256 is
`f12dfa2714ad97152c6130ef07e3139630382c00dce2d1ff0819a9469a9e361f`.
The native representative case has zero counted loss/output faults; its retained
counts and measured high-water are in the selected result. These are finite host
workloads, not retail service-rate or universal race/frequency guarantees.

## Failures and counterexamples retained

Native01 passes nine cases but overlaps later edits and fails final source
identity. Native02 passes seven development cases; subsequent consumer changes
prevent using it as the final combination. Native03 and Repro01 are the qualified
runtime pair. Original Instructions01 fails before instruction execution because
its mapper used page instead of allocation-granularity alignment; corrected runs
are separate. Reader Final02 retains its failed oracle that wrongly discarded a
sound pre-retirement identity. Final03 requires that partial identity to survive
while rejecting continuity through the invalid lookup. The first provenance
verifier assumes a nonexistent queue receipt field and fails; Provenance02
verifies the actual `passed`/loss fields without altering the queue evidence.

Preliminary independent review found malformed bypass-prefix acceptance,
admission-only later ordering and a tautological reconstructed-definition check.
They were corrected before final qualification; their explicit adverse oracles
are retained. The native investigation preserved and corrected the cleanup-parent
misassociation, modifier/cell owner confusion, base/derived file distinction and
the initially omitted late provider alias. None is converted into a historical
success or absence result.

## Frozen acceptance matrix

| Criterion | Implementer result | Evidence and limit |
|---|---|---|
| P1-AC01 | PASS | Admission ledger/baseline, installed/database pins, both-drive guards, offline-only operations and unchanged HEAD/index. No save access or new live preflight claimed. |
| P1-AC02 | PASS | L01–L21 matrix, seventeen exports, ninety-three function records, a bounded receiver census, exact ten-funclet parent/origin accounting and independent L14/L18-G challenge. |
| P1-AC03 | PASS | Source read removed from lookup; private initialized semantic identity; qualified construction/bypass positives and explicit ambiguity refusals. |
| P1-AC04 | PASS | Constructor/pub controls, inaccessible source memory, detached-retirement premise, concrete alias/destructor proof, strict epochs, reset/owner proof and reuse/loss counterexamples. |
| P1-AC05 | PASS | Native03, Original Instructions04 and Reader Final03 provide distinct native, compiled-host and modeled oracles. Failures remain preserved. |
| P1-AC06 | PASS | Exact final source/schema/packaged consumer pins, identical DLL reproduction and all affected P2 suites. Unchanged production bridge/queue/transport/controller contracts separately verified. |
| P1-AC07 | PASS | All original five questions/twelve criteria mapped without changing historical outcomes; D5R OPEN, P3/P4 OPEN, B2 NOT AUTHORIZED. |
| P1-AC08 | PASS | Independent Review04 restores whole-package engineering/scientific and editorial ACCEPT, including L18-G, verified patches and manifests. The review record governs narrow closure verification. |

Engineering/evidence integrity passes the tested offline contract. Scientific
retail readiness and the parent D5AB contract remain incomplete. No Starfield
target ran; target survival/recovery is not applicable. Expected disposable crash
cases retain their declared exits. Installed content, analysis databases and
protected saves are unmodified. No staging, commit, push, deployment, disclosure,
new third-party incorporation or publication is authorized or performed.

Following independent P1 ACCEPT, the recommendation is to prepare a separate
P3 native-integration brief. P3/P4 and B2 are not started by this work.

The first exact-snapshot ACCEPT was superseded by REWORK after a final challenge
found additional actual source-getter consumers. L18-G followed their return
flows and the remaining cell lookup/file interface through primary bodies and a
bounded Grid-method census. Independent proof review accepts that correction;
Review04 restores whole-package acceptance on the updated documents and manifest.
Runtime source and all engineering tests remain unchanged by this proof addition.
