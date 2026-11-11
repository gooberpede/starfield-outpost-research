# Item 7 publication decisions and execution sequence

**NOT READY / NOT CLEARED.** This handoff records work to authorize and
perform under item 7. The [publication policy](../../PUBLICATION.md),
[run card](../../PUBLICATION_RUN_CARD.md) and
[release gate matrix](../publication-readiness-b0/release-gates.md)
control the approvals and checks.

## Decisions before freeze

| Decision | Accountable role | Acceptance evidence |
| --- | --- | --- |
| Claim wording and access | Maintainer | Sign off on the exact selected wording, claim build and historical qualifications, included assets and reader access tiers. Use the 126 joins in the [current matrix](routes.json) and follow each named inherited action in [D5BG](../publication-claims-d5bg/actions.json). Record any approved narrower tier per affected claim and recompute its dependency closure. |
| Exact file disposition | Maintainer with rights/privacy reviewer | Approve by hash the proposed files, members, third-party notices, licences, contributor wording and permitted excerpts. Review the actual final content and source provenance, including the residual opaque-save and image limits. Retain the donor exclusion and separate the project GPL from rights to upstream content. |
| Transfer and retention | Maintainer and evidence custodian | Approve a destination and custodian for each indispensable file and access prerequisite. Keep protected originals and private receipts in existing authorized custody until a separate disposition. Nominate an exclusive ignored B6 scratch root, with explicit supplied paths and pre/post container and member hashes. Maintain reader access independently of the maintainer's disposable working directory. |
| Repository archive and exposure | Maintainer with documentation and rights/privacy reviewers | Approve a refreshed exact D5AX membership/link inventory and the proposed public refs. Record file paths, original blob and byte hashes, archive members, stable retrieval paths and preservation of scientific reports and negative cases. Audit all reachable Git history for secrets, personal paths and rights separately from the final checkout. |

## Seven asset groups

Each exact candidate is **PENDING RELEASE**. The [asset records and route
joins](routes.json) give the SHA-256, bytes, selected claim IDs and ledger
pointer. The indices below govern member identities. For any candidate whose
approved durable access fails, obtain a claim-specific maintainer decision
before B6. D5BP and D5BQ already select attributed historical tiers for E3's
and SD2's larger corpora, D1's saved-state contrast and D5AT's fixed-input
comparison. Their narrower witness tiers and the four historical-only
accounts have distinct dependencies. D5BQ identifies authored inspection
as the narrower local-link fallback if its required reader or member fails.

| Asset and exact index | Local qualification and reader conditions | File-specific acceptance |
| --- | --- | --- |
| `sor-1.16.244.0-b4-f1-core-stored-provisional.zip` · [D5BF](../release-assets-d5bf/release-assets.json) · [F1 member IDs](../publication-readiness-b4/f1/members.csv) | 25 original saves. D5BF custody plus D5BU named original methods. Supplies position, Save29, cargo, SD2, fabrication, L0, roots and construction witnesses according to the route matrix. | Approve each original identity and basename. Carry forward scoped F1 screening and accept or disposition opaque fields and embedded previews. Preserve original bytes and donor F061 exclusion. |
| `sor-1.16.244.0-b4-f1-addendum-deflate-provisional.zip` · [D5BF](../release-assets-d5bf/release-assets.json) · [F1 member IDs](../publication-readiness-b4/f1/members.csv) | 14 original saves and 13 JPEGs. Required wherever the exact selected L-series, display, biome or placement witness uses it. D5BU inspected nine selected JPEGs and left image/save epochs, rejected XYZ and rendered reload unjoined. | Approve exact saves and screenshots separately. Apply existing JPEG segment and practical visual checks, including residual fine image detail, and the save privacy checks. |
| `d5as-feynman-geometry-v1.zip` · [D5BF](../release-assets-d5bf/release-assets.json) · [D5AS manifest](../evidence-access-d5be/d5as-manifest.json) | 30 qualified canonical bodies, two complete fixed references and one manifest. D5BE/D5BF replay and independent D5BH checks, including changed point word, wrong domain/class and missing/duplicate input. CPython 3.9+ for standalone. Attempt 6 remains excluded, attempt 31 replaced it. | Approve the full bounded Bethesda-derived geometry, FormIDs, capture UUIDs, hashes and representation metadata. Keep upstream snapshots and startup/custody records private. |
| `c19-callbacks-v1.json` · [D5BF](../release-assets-d5bf/release-assets.json) · [C19 manifest](../evidence-access-d5be/c19-manifest.json) | 346 complete ordered native callbacks. D5BE/D5BF replay and original callback review, with missing/duplicate, ordering and wrong operand/row/domain controls. CPython 3.10+ standalone. Native row agreement leaves screen timing and upstream ancestry open. | Approve alias/row/constructor and sequence fields and operator labels. Keep WAL, raw pointers and upstream execution records in local custody. |
| `d5bh-episode-witness-v1.zip` · [27-member index](../evidence-derivative-d5bh/asset.json) | Independent original Raw2 and isolated projection checks for A0 and D5AK/D5AL. Reject geometry-equal wrong A0, changed point words, wrong owner/lifetime and alternate-geography ambiguity. Windows CPython 3.14.3 import closure binds kernel32 symbols. | Approve complete geometry and projected events, including historical process IDs, creation times, QPC, session tokens and expired addresses. Review the copied journal and receipt fields in the [proof](../evidence-derivative-d5bh/proof.md). Retain the original seals and evidence privately. |
| `SOR-D5BI-N2-projected-evidence-v1.zip` · [six-member index](../evidence-derivative-d5bi/manifest.json) | Review02 accepted projected N2 construction and competition. Controls challenge owner/frame and acquisition, release, provider and visit boundaries. The Windows CPython 3.14.3 route uses D5BH source imports. The D5BH ZIP is unnecessary. N2 shows no target overtake. | Review the copied descriptor, scheduler and lock operands, runtime identifiers, address exposure and timing correlation against the [file-specific assessment](../evidence-derivative-d5bi/proof.md#file-specific-rights-and-privacy-disposition). Keep raw N2 inputs private. |
| `SOR-D5BO-B2-projected-evidence-v1.zip` · [two-member index](../public-evidence-d5bo/b2-asset.md) | Review05 accepted the local projection, isolated check and 24 adverse cases, including removal of the earlier request and false cold-firstness. The Python verifier checks the bounded observed overtake. Native insertion timing and the full reset history remain unmeasured. | Approve the exposed QPC, invocation IDs, target tuple and FormIDs, requests and reduced lifecycle fields. Keep original B2 diagnostics and timing context private. |

Use [F1 privacy policy](../publication-readiness-b4/f1/privacy-policy.md)
and the [file disposition ledger](../publication-readiness-b4/f1/file-dispositions.csv)
for the actual clearance review. Existing first-party eligibility and
proposed-release decisions are scoped. Retain Bethesda and third-party
notices. Later hosting receipts must match the approved full container
and every declared member, including the standalone JSON file identity.

## Exact reader prerequisites

- For D5BU, use the named Python entry points, source manifest and explicit
  operands in [methods](../original-save-verification-d5bu/methods.md). Geography
  requires lawful pinned main ESM and PlanetData BA2. Fabrication needs the
  main ESM and tracked recipe tables. SD2 needs the pinned main/add-on ESMs.
  Workshop roots require the three exact historical context files plus the
  canonical authored ledger and main ESM. Cargo requires the selected
  recovered C3 context. The pinned [roots reader](../../../save-analysis/scripts/verify_d5bu_controls.py)
  and [cargo reader](../../../save-analysis/scripts/verify_d5bu_cargo.py)
  state the context byte counts and digests. Bind them to an approved
  durable retrieval route, or obtain a scoped access change. A public
  checkout and the two original ZIPs alone cannot supply those contexts.
  Use CPython 3.14.3 on Windows and the method-specific scratch and disk guards.
- The two D5BT integrations have independent review02 acceptance and
  accepted D5BU receipts. Save29 F054 supports the ordered saved graph and
  original/swapped calculation. HIST-0021 F067 supports the selected
  saved display-item and backpack control. Historical load execution and
  rendered reload remain outside those checks.
  [D5BT review](../reader-qualification-d5bt/review.md)
- D5AG uses one of the seven assets, D5AS. Its native command consumes
  two fixed references after preflighting all 33 members. Freeze exact
  reader sources, the C1 oracle, Windows/AMD64/CPython/UCRT/AVX prerequisites
  and lawful matching EXE, main ESM and PlanetData BA2. Retain the
  wrong-operand and host refusals and the full population comparison.
  General lawful access to the legacy game build remains unestablished.
  The standalone D5AS precomputed comparison has its own qualified tier
  when the native prerequisites are unavailable. Hold the conditional
  native route pending an approved access or claim-scope decision.
  [D5BO contract](../public-evidence-d5bo/d5ag-reader.md)
- The historical D5BD exact source rebuild is qualified by D5BS. It needs
  Git commit `6e799a428a765aa196a24d3c1de8ae133260aa08`, tree
  `7a1f6fdd6728a8f98bc92ef7ee6c9b24a62f0e0e` and the exact source and
  support sets in the [historical edition manifest](../../../research/function-catalogue/editions/d5bd.json).
  If exact historical reproduction is advertised and the approved public
  surface omits the object, approve and separately qualify a lawful
  frozen-source provision or select the authored catalogue inspection
  tier. The current tree and technical test edition have distinct scan
  sets. [D5BS acceptance](../native-function-catalogue-d5bs/review.md)

## Execution after decisions

### Evidence receipts for the clean checkout

The independent B6 reviewer records the frozen method revision, qualified
host, exact supplied paths and hashes, output identity, exit and adverse-case
results for each applicable row. Use the exact arguments and expected
comparisons in the linked contracts. Keep protected inputs immutable and
record pre/post identities. The source-only B6 checkout receives explicit
operands. Private builders and historical acquisition routes stay outside it.
Run the [six-case isolated framing check](../publication-readiness-b3/method-reproduction.md#runnable-representative-synthetic-record-framing)
before the selected saved-state methods. For authored routes, record the
tracked source and arithmetic inspection oracles in the route matrix.
Apply the exact B3 input contract wherever the advertised tier requires
a lawful definition, script, raster or native-instruction reread.

| Group | Method and acceptance receipt |
| --- | --- |
| CORE | Run the [D5BF streaming verifier](../release-assets-d5bf/README.md#verification) and match all 25 members. Check the selected CORE operands across D5BU A1–A4 and A6 using the exact [methods and inputs](../original-save-verification-d5bu/methods.md). Bind results and controls to the corresponding D5BU route receipts, including the root and C3 context pins. |
| ADDENDUM | Match all 27 members with the same streaming verifier. Check the cross-archive A1, A4 and A6 comparisons with CORE supplied once, and F067 in A5. Record the selected visual review with its saved-state timing limits. Compare the exact outputs and refusal cases to [A1–A6 acceptance](../original-save-verification-d5bu/review.md#final-independent-d5bu-review). |
| D5AS | Match all 33 members and the [standalone full-body comparison](../evidence-access-d5be/d5as.md#reader-comparison). Record 30 matches split 2/28, the exclusion/replacement and six rejected controls. |
| C19 | Match the whole JSON member and use the [C19 verification contract](../evidence-access-d5be/c19.md). Record 346 ordered row comparisons, six refusals and the separate synthetic fold check. |
| D5BH | Match 27 members. Run the [episode verifier and controls](../evidence-derivative-d5bh/README.md) on the qualified Windows host. Compare three complete normalizations, 196 pairs, 390 increments, four typed endings and the frozen forecast. Require all 14 documented refusals. |
| D5BI | Match six members. Run the [N2 verifier and controls](../evidence-derivative-d5bi/README.md) on the qualified Windows host. Compare the recorded 238,272 projected frames and the selected construction and competition predicates. Require all 24 documented refusals. |
| D5BO | Match both members. Run the [B2 verifier and controls](../public-evidence-d5bo/b2-asset.md) on the 32,141-frame projection. Compare the protected decision inversion and retained negative history. Require all 24 documented refusals. |

For the conditional D5AG route, apply the [separate fixed-stage contract](../public-evidence-d5bo/d5ag-reader.md)
under explicit native-execution authority. Record both sampler branches,
144 packed keys, all three complete populations, repeated full-native
equality, both canonical references and the independent planar checks.
Preflight must refuse incompatible files or host conditions. For the D5BD
exact historical tier, bind the [D5BS source-only check](../native-function-catalogue-d5bs/README.md)
to the approved historical object and compare all 16 files and the original
link closure.

### Approval and release steps

1. **Documentation owner and custodian.** Under a separately approved scope,
   implement the selected D5AX archive/member map and reconcile inbound
   links, code references and stable historical locators. Reconcile all
   additions since the original census, including this audit. Preserve
   filename and path case, hash exact members, test isolated safe extraction
   and check navigation. Keep indispensable reader dependencies in the
   approved surface. Review both current tree and reachable history.
   [D5AX design](../publication-architecture-d5ax/archive-plan.md) ·
   [D5AW sequence](../deferred-work-d5aw/publication-plan-amendment.md)
2. **Maintainer and candidate custodian.** Freeze exact release ID, proposed
   tag target, commit/tree, public refs and reachable objects. Include
   Starfield 1.16.244.0 EXE SHA-256
   `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
   main/add-on/BA2 and host pins by method, version-qualified historical
   sources, final wording, method hashes, approved asset/container/member
   digests and rights, custody and access records. Use the
   [B3 baseline](../publication-readiness-b3/baseline-manifest.md) and method
   contracts. Document every unavailable or excluded exact route.
3. **Independent B6 reviewer.** Under a separate brief, qualify the exact
   candidate in a clean isolated checkout with no access to existing
   `.local-work/`. Supply only approved immutable assets and lawful exact
   inputs to an exclusive local staging namespace. Check the 40 GB
   caller-available drive guards where applicable, method effects, exact
   source and dependency closure, claim-scoped checks, links and current
   tree plus history exposure. Accept only against the frozen identities
   and record observed outputs, adverse cases and hashes.
   Use the four D5BF candidate integrity checks and the corresponding
   independent methods for all seven asset groups. Check rendered diagrams,
   examples and navigation from the exact checkout. Native fixture execution
   needs explicit authority in the B6 scope. First-time assets may pass
   staged preflight with a reviewed durable hosting plan. Actual hosted
   access remains pending until the download checks.
4. **Maintainer and authorized release operator.** After B6, obtain separate
   authorization for the exact Git/tag and draft upload operations. Verify
   the actual draft downloads, archive members, URLs, tag target and
   changed exposure. Obtain separate visibility and timing approval.
   After authorized publication, verify the public bytes, members, links
   and refs again. Changes to any approved surface require affected
   re-review. [Publication run card](../../PUBLICATION_RUN_CARD.md)
