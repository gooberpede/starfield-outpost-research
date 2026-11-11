# Evidence and Identifier Standard

## Independent dimensions

Every research claim records its confidence, evidence basis, lifecycle status, and publication classification separately. Substantive semantic findings also state coverage and, where claimed, completeness. Do not collapse these properties into a single green status.

**Confidence:** `PROVEN` means decisive evidence within an explicit scope; `STRONG` means substantial independent support with a material gap; `PROVISIONAL` means an unconfirmed model. `OPEN` is a question without an accepted explanation. A counterfactual prediction is labelled `PREDICTION`, not a finding. Displaced interpretations are retained as `SUPERSEDED`; rejected ones retain the reason and counterexample.

**Basis:** `SOURCE-REPORTED`, `STATIC`, `RUNTIME`, `SAVE`, or `CROSS-VALIDATED`, with exact evidence references. Static evidence cannot by itself establish that a particular object took a path live. Prior-work validation and project-original discoveries must remain distinct.

**Publication classification:** `LOCAL-ONLY`, `REVIEW-REQUIRED`, or `CLEARED-FOR-PUBLICATION`, with reviewer/date/scope. Classification is not publication authorization. No confidence level clears rights or private data.

## Scoped conclusions and coverage

Report and use the strongest interpretation supported by reproducible evidence, stating its confidence and demonstrated coverage. Do not require exhaustive understanding of all engine exceptions before using a sound, scoped research result.

**Coverage** describes supported object classes, gameplay conditions, save versions, record representations and subsystems. Distinguish **tested**, **inferred** and **unknown** coverage in concise, testable prose; an exhaustive new schema is not required. **Completeness**, when claimed, requires an argument that every qualifying instance within the stated scope is covered. No known counterexample does not establish completeness, universality or absence.

The confidence definitions above remain unchanged. An accepted `STRONG` semantic association may serve as established working knowledge within its demonstrated coverage, with its material gap stated. Unresolved exceptional cases outside that coverage do not automatically downgrade the ordinary-case result. Recognizing a structure's role does not require decoding its entire representation, lifecycle, ownership or runtime authority; state which of these are established separately.

Report a concrete positive detection even when complete membership remains unresolved. A detector may find an ordinary beacon with a saved disabled flag clear while its active-player-membership answer remains `INDETERMINATE`. These are different claims. Preserve accepted findings as revisable; durable promotion or reclassification still requires user review under [WORKFLOW.md](../WORKFLOW.md).

Reopen an accepted finding when new evidence contradicts it within its claimed coverage, shows misstated coverage or provenance, exposes a decoding/analysis/experiment/inference error, or supports a materially better explanation of the same observations. First determine whether a new exceptional case falls within scope. Record an out-of-scope exception or coverage gap separately; it may justify a focused investigation without suspending unrelated results.

An objection must identify a concrete counterexample, observed alternative, relevant executable path, or explicit completeness gap that matters to the actual claim. Speculation that other representations may exist is insufficient to withhold a supported scoped conclusion; a demonstrated unhandled representation matters to an exhaustive claim. Preserve contradictions and negative results rather than insulating findings from falsification.

## Standards by claim and intended use

| Claim or use | Required support and limits |
|---|---|
| Research finding | A reproducible bounded semantic conclusion with confidence, coverage, decisive evidence and concrete limitations. Full engine reconstruction is not a prerequisite for every finding. |
| Read-only detector/report | State the property actually detected, supported versions/representations and uncertain states. A sound positive indicator need not establish complete player membership. |
| Definitive count or absence | “Exactly N active player-owned outposts” or “no active outposts” needs a justified completeness argument covering every qualifying representation within the claimed scope, including the membership predicate. Empty candidates, empty relationships or failed signatures alone are insufficient. |
| Save modification or production guarantee | May require substantially stronger correctness, preservation, recovery and compatibility proof, plus separate authorization. Do not impose that entire standard on exploratory research. |

Useful narrower negatives are allowed: “No ordinary beacon candidates were detected by this validated scanner in these supported record representations” reports a scoped detection result; it does not establish zero active outposts or exclude residual state. Keep persistence classes, integration status, lifecycle and publication eligibility separate as defined elsewhere in this document.

## Evidence evaluation and reporting

Within an approved research scope, independently formulate and test competing hypotheses. Select among authorized offline analyses by likely information gain rather than automatically pursuing the last undecoded field. Give priority to well-designed causal interventions and independent corroboration; static executable analysis can also establish semantics decisively. Evaluate evidence quality, provenance and relevance without a rigid hierarchy of methods. Static code alone still cannot establish that a particular object took a path live.

This autonomy does not expand authorization. [AGENTS.md](../AGENTS.md), [WORKFLOW.md](../WORKFLOW.md) and [THIRD_PARTY_POLICY.md](../THIRD_PARTY_POLICY.md) retain their gates, including separate live/deployment/save-modification authority, the maintainer-owned `gooberpede` exception with provenance, and embedded third-party rights. Preserve raw evidence and existing low-disk/output safeguards. Work beyond the brief, durable reclassification and commits remain subject to user review; a next-test recommendation grants no execution authority.

Begin each substantive semantic research report with a compact answer-first section or table containing:

| Element | Content |
|---|---|
| Research question | Specific bounded question investigated. |
| Best-supported answer | Strongest defensible answer, including useful scoped positive results. |
| Confidence | Existing classification applied to the stated claim; separate proposed from accepted status. |
| Coverage | Tested conditions/versions/representations, inferred extensions, unknown coverage and important exclusions. |
| Evidence | Decisive reproducible observations/tests and exact provenance/locations. |
| Limitations | Concrete unresolved cases and their impact on this answer. Include completeness justification if claimed. |
| Next step | Highest-information available next test if needed, with its authorization boundary. |

Minor observations and routine document updates need no lengthy table. If no answer is supported, identify the precise obstruction, routes tested, missing data or engine mechanism, and why current authorization/capabilities cannot resolve it. A failed method is not proof of fundamental impossibility. Unknowns must not obscure a useful supported conclusion.

## Worked applications — existing status preserved

These examples apply the methodology to durable records; they introduce no new validation or historical promotion. The linked reports/registers control exact evidence, confidence and review status. Existing semantic `STRONG` proposals remain proposals pending critical review.

- **Ordinary beacon indicator:** [SOR-F-0014 / SOR-EXP-0009](experiments/active-outpost-identification.md#initial-data-base-identity-and-saved-state) records zero inline case-5 diagnostics in Save3/S0/S0C, one disabled-clear diagnostic after ordinary placement, and 19 in mature Save52 split 17 disabled-clear / two disabled-set. `PROVEN / SAVE` applies to sampled framing/field bytes, with `STATIC` loader/IsDisabled mapping under its preconditions. This is useful positive evidence of the ordinary beacon representation and saved disabled state. Active-player membership remains `PROVISIONAL` in [SOR-H-0006](hypotheses.md#sor-h-0006--disabled-state-promotion-and-reconstructed-workshop-membership); exceptional faction/quest control and alternate reconstruction prevent complete enumeration. No enabled/disabled observation alone proves ownership or runtime activity.
- **Output-link relationship:** [SOR-F-0010 / SOR-EXP-0004](experiments/output-link-validation-L0-L2C.md) records creation, removal and recreation correspondence, within-session no-action controls, retained endpoint candidates and payload length 19→12→19. `PROVEN / SAVE` covers bytes; the output-link semantic association is **proposed STRONG pending review**. L0→L0C is cross-session/reload churn, not a within-session control; the original literal fails after reload. The bounded association can be evaluated separately from logical ownership, direction, count/framing semantics, generality and load authority. Later [SOR-F-0012](experiments/mature-save-outpost-validation.md) adds bounded count grammar without closing those semantic questions.
- **Cargo topology:** [SOR-F-0012 / SOR-EXP-0006](experiments/mature-save-outpost-validation.md#structural-role-and-evidence-classifications) records 24 reciprocal pairs and exact agreement with the independently maintained manual network's names, pad counts/types and outpost-pair multiset. Observations/comparison are `PROVEN / SAVE`; cargo interpretation is **proposed STRONG pending review**, scoped to this mature sample. Fifty-three associated pads are a subset of 61 windows. Two parallel pairs permit permutation and three unlinked same-type pads are interchangeable; physical pad UUID mapping, transfer direction, contents, timing and load authority remain unresolved. Those gaps do not erase observed topology correspondence.
- **Local position:** [SOR-F-0009's coordinate correction](experiments/manual-save-corpus-S0-S7C.md#offline-comparison-with-earlier-exp0002-live-player-coordinates) records numerical distances 6.830539 / 8.997486 / 26.000118 between save-side candidates and independently captured earlier player XYZ, with no assigned units. Captured values/arithmetic are `PROVEN`; a same/related local Cartesian frame remains `PROVISIONAL`, [SOR-H-0004](hypotheses.md#sor-h-0004--save-position-candidates-may-share-or-relate-to-the-live-local-frame). Cross-session, non-atomic observations and unresolved transform ownership/frame prevent authoritative object transforms, planetary-body mapping or latitude/longitude claims. Numerical compatibility is a useful result within those limits.

This refinement is prospective under [SOR-D-0027](DECISIONS.md#sor-d-0027--prospective-scoped-conclusions-and-coverage). Existing evidence, classifiers and scientific conclusions are unchanged; no bulk confidence recalculation or reopening of deferred faction/quest work follows.

## Stable record IDs

Use a four-digit sequence within each category; never recycle an ID. Empty templates use `<ID>`, not an allocated number.

| Prefix | Record |
|---|---|
| `SOR-F-` | Research finding |
| `SOR-H-` | Hypothesis |
| `SOR-Q-` | Open research question |
| `SOR-FN-` | Native/script function or operation |
| `SOR-ST-` | State item, structure, relationship, or saved record |
| `SOR-EXP-` | Experiment |
| `SOR-EV-` | Evidence item/bundle |
| `SOR-S-` | Outside source |
| `SOR-P-` | Permission/reuse decision |
| `SOR-D-` | Project decision |
| `SOR-ENV-` | Executable/tool/environment baseline |
| `SOR-SAMPLE-` | Controlled save/input sample |

## Minimum evidence

Record the question and claim, conditions, build/sample/tool provenance, exact observed material, relevant controls, alternative explanations, and what would falsify it. Provide decisive locations/ranges rather than only linking a huge dump. A checksum proves integrity of an artifact, not its source's truth or the correctness of an interpretation.

Use a no-action control when comparing saves and independent examples or repetitions appropriate to the claim. Record randomness, timing, cell/loading state, interventions, load order, and player actions where relevant. Do not silently turn incidental variation into a controlled variable.

For an explicitly authorized crash-tolerant capture, report evidence completeness (including successful persistence/flush), scientific result, and target-process outcome separately. Complete evidence collected before a crash can remain useful; a crash before the required evidence is collected is not success. Disclose intervention-induced failures and missing/truncated records. The bounded authorization requirements remain in [AGENTS.md](../AGENTS.md).

## Address and identity discipline

The [reader notation guide](reference/notation.md) provides
domain-specific examples without changing historical address or evidence pins.

Label each location explicitly: runtime virtual address; module-relative RVA; static-analysis address; original compressed-file offset; decompressed-stream offset; record-relative offset; or another defined domain. Include the actual module/image base and build. Preserve original function names/addresses; semantic labels are aliases unless their source is established. Address Library IDs, when used, need version/provenance; they are not universal identifiers.

A runtime pointer, reference handle, FormID, saved identifier, script instance identifier, and logical outpost ID are different concepts until a mapping is demonstrated. Explain mapping scope and whether it survives reload or another save/playthrough. For binary claims record lengths, endianness, encoding, compression/transformations, bounds, flags, and failure cases only where established.

## State and integration claims

For important state identify origin, ownership, lifecycle, updates, consumers, authority, and persistence class: `PERSISTED`, `DEFINITION-DERIVED`, `RECONSTRUCTED`, `TRANSIENT`, `MIXED`, or `UNCLASSIFIED`. Avoid concluding absence from a failed search alone.

For future mod use distinguish `OBSERVED-INTERNAL`, `EXPOSED-INTERFACE`, `PROPOSED-INTEGRATION`, and `VALIDATED-INTEGRATION`. Record preconditions, side effects, ordering, cleanup, failure cases, and the exact validated build. A proposed hook is not an approved deployment.

## Original and derived artifacts

Keep raw captures local. Promote only specifically reviewed evidence into Git with provenance and permissions. Hash original bytes before transformation. Record a separate derivative, its input/output hashes, purpose, tool version, and exact transformation. Never alter the original to make a test pass.

Evidence byte files under `docs/experiments/evidence/` have Git text conversion disabled. Authored `README.md` files are the exception and are normalized. Verify the staged blob when exact byte identity matters. Document normalization, privacy redaction, and any resulting reproducibility limitation.

## Historical-save methodology — SOR-EXP-0007

[Inventory and triage](experiments/historical-save-inventory-triage.md): pristine Save3 and controlled action/no-action successors test causality and semantics. Mature/historical saves are observational structural/topology evidence, potentially anomalous or bug-affected; filenames, levels and timestamps do not establish a shared universe or linear history. Old-version load/current-version resave is a separate future experimental category requiring explicit authorization and immutable originals. Absence requires stronger coverage and independent negative indicators than presence: empty reference collections, parser failures or zero window counts alone never establish no outposts; distinguish provisional active-state absence from exclusion of all residual state.

## Supplemental third-party corpus methodology — SOR-EXP-0008

Older game versions remain eligible observational research inputs, with version-specific applicability and missing ground truth explicit. [Launch-era inventory](experiments/launch-era-third-party-save-corpus.md) is a distinct donor corpus, never a renumbering/extension of frozen HIST records or a substitute for controlled Save3 causality tests. NO_ACTIVE_OUTPOST_INDICATORS_DETECTED is a multiple-indicator detection label, not verified active-state or total residual absence. Empty compatible grammar is useful structural evidence; unexplained nonempty groups remain inconclusive. Original third-party archives/saves/substantial extracted material are excluded from publication; privacy/rights eligibility and confidence remain independent. Live load/resave requires a separate brief.
