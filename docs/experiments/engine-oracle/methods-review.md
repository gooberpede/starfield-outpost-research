# Sibling-project methods review

2026-10-10. SOR-S-0133 / SOR-P-0002. Read-only consultation and conceptual reuse;
no sibling code, tests or datasets copied into the position model. Exact consulted
file hashes and local Git content checks are in the local source receipt.

Connected GitHub metadata reports default branch `main` for both repositories.
`fetch_commit(main)` returned the same revisions as the local checkouts:

| Repository | Consulted current revision |
|---|---|
| [resource research](https://github.com/gooberpede/starfield-resource-research) | `a23e1c337bc369232d6ce463552a53617bb918e2` |
| [resource reproducer](https://github.com/gooberpede/starfield-resource-reproducer) | `a8ff1c788bca415f571f06769ab3e712fa674f75` |

Research files read: `README.md`, `AGENTS.md` evidence rules,
`docs/v1-research-baseline.md`, `docs/PROVENANCE.md`, `docs/function-register.md`,
`docs/experiments/v1-holdout-validation.md`. Reproducer files read:
`README.md`, `docs/ARCHITECTURE.md`, `docs/DOMAIN-RULES.md`,
`docs/V1-VALIDATION-BASELINE.md`, `docs/IMPLEMENTATION-WORKFLOW.md`,
`docs/experiments/05D-runtime-bounded-rng-split.md`,
`src/starfield_resource_reproducer/prng.py`, `validation.py`, and
`tests/test_special_guard_order.py`, `tests/test_load_oracle.py`.
Selected files, rather than the entire sibling suite, were inspected; their
published validation counts are SOURCE-REPORTED here, not newly rerun.

History inspected: reproducer log and the actual PRNG implementation diff at
`3eb4f01d13040f56d1b873bfc2cb44ed92d8abf4`; change inventory at
`f19c0a395e8a34dba9b8e4c65fc02f3bdbb2e97b` and its current sequencing regression.
The former preserves a conflict: modulo reproduced Kreet shuffle but failed
Algorab's descendant selection. Native tracing resolved two different operations,
and the model exposed intermediate probability/scaled-index/rejection state.
It did not reorder candidates to fit the oracle. The latter records guarded
fallback provenance and Special-before-Common-guard sequencing; a final matching
resource set alone could have missed the wrong branch/order.

| Practice | Adoption for outpost position |
|---|---|
| Separate generation and oracle | Model accepts saved inputs only; native outputs and comparison are separate. Reject unexpected expected-output fields. |
| Recover order/intermediates | Record zero-vector bypass, saved frame branch, float32 multiply/floor, signed remainder, hierarchy and native result freshness. |
| Evidence owns semantics | Existing classifications remain intact; this package proposes new findings for critical review. Source reports are not independent replications. |
| Counterexample-led regression | Retain mature negative-X/site-frame counterexample, both-axis seam, signed-zero branch and missing input controls. |
| Discovery versus holdout | Save25/26, S1/S1C and Save52 are known regressions. A future independent outpost is frozen before new native observation. |
| Trace provenance | Pin retail executable hash/RVA and export hashes; no CK address transfer. |
| Different oracle channels | Stored terrain center validates a local native consumer. Indexed terrain callback validates body/grid. Neither alone validates continuous geography or all permissions. |

Not adopted: the sibling corpus size as an acceptance threshold; CK's Galaxy View
as an outpost-placement oracle; resource PRNG/cache architecture as a positional
architecture; a new public repository or downstream product. The resource
projects' 1,444 canonical and 10 holdout agreements are a methodological benchmark.
Their CK executable SHA-256 is not recorded in the consulted provenance baseline;
that limitation is not imported into this project's pinned retail baseline.

Local Git initially refused sibling reads for ownership. Per-command
`-c safe.directory=...` enabled read-only history inspection; no persistent Git
configuration, checkout, fetch, fork, PR or upstream communication occurred.
