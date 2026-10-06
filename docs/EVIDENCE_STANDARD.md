# Evidence and Identifier Standard

## Independent dimensions

Every research claim records its confidence, evidence basis, lifecycle status, and publication classification separately. Do not collapse them into a single green status.

**Confidence:** `PROVEN` means decisive evidence within an explicit scope; `STRONG` means substantial independent support with a material gap; `PROVISIONAL` means an unconfirmed model. `OPEN` is a question without an accepted explanation. A counterfactual prediction is labelled `PREDICTION`, not a finding. Displaced interpretations are retained as `SUPERSEDED`; rejected ones retain the reason and counterexample.

**Basis:** `SOURCE-REPORTED`, `STATIC`, `RUNTIME`, `SAVE`, or `CROSS-VALIDATED`, with exact evidence references. Static evidence cannot by itself establish that a particular object took a path live. Prior-work validation and project-original discoveries must remain distinct.

**Publication classification:** `LOCAL-ONLY`, `REVIEW-REQUIRED`, or `CLEARED-FOR-PUBLICATION`, with reviewer/date/scope. Classification is not publication authorization. No confidence level clears rights or private data.

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

Label each location explicitly: runtime virtual address; module-relative RVA; static-analysis address; original compressed-file offset; decompressed-stream offset; record-relative offset; or another defined domain. Include the actual module/image base and build. Preserve original function names/addresses; semantic labels are aliases unless their source is established. Address Library IDs, when used, need version/provenance; they are not universal identifiers.

A runtime pointer, reference handle, FormID, saved identifier, script instance identifier, and logical outpost ID are different concepts until a mapping is demonstrated. Explain mapping scope and whether it survives reload or another save/playthrough. For binary claims record lengths, endianness, encoding, compression/transformations, bounds, flags, and failure cases only where established.

## State and integration claims

For important state identify origin, ownership, lifecycle, updates, consumers, authority, and persistence class: `PERSISTED`, `DEFINITION-DERIVED`, `RECONSTRUCTED`, `TRANSIENT`, `MIXED`, or `UNCLASSIFIED`. Avoid concluding absence from a failed search alone.

For future mod use distinguish `OBSERVED-INTERNAL`, `EXPOSED-INTERFACE`, `PROPOSED-INTEGRATION`, and `VALIDATED-INTEGRATION`. Record preconditions, side effects, ordering, cleanup, failure cases, and the exact validated build. A proposed hook is not an approved deployment.

## Original and derived artifacts

Keep raw captures local. Promote only specifically reviewed evidence into Git with provenance and permissions. Hash original bytes before transformation. Record a separate derivative, its input/output hashes, purpose, tool version, and exact transformation. Never alter the original to make a test pass.

Evidence byte files under `docs/experiments/evidence/` have Git text conversion disabled. Authored `README.md` files are the exception and are normalized. Verify the staged blob when exact byte identity matters. Document normalization, privacy redaction, and any resulting reproducibility limitation.
