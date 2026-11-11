# Cargo C3 exact-file provision

The proposed standalone `sor-d5bx-cargo-c3-v1.json` is exactly the recovered
`save01.json`. It has 3,598,255 bytes and SHA-256
`557f6148a357cc0a354336637a939ae1c3736a63f7a5f7cea27c189cd5095920`.
The file was copied in binary mode and verified before and after the rehearsal.
Its four maintainer-approved provenance fields remain exact.

| Field | Historical locator retained in the payload |
| --- | --- |
| `source.path` | The Save52 custody copy, including its original basename. |
| `prior.path` | The prior storage analysis receipt. |
| `cache.path` | The historical cache receipt. |
| `tool.path` | The acquisition probe source. |

The [D5BW access review](../evidence-distribution-d5bw/access-routes.md)
records the exposure. The [B02 baseline](../../experiments/cargo-evidence-cutover/active-baseline.json)
and [D5BU receipts](../original-save-verification-d5bu/receipts.json) bind the
private archive/index and recovered member lineage. The private archive, raw
sources and historical acquisition receipts stay in existing custody. The
supplementary file is ready for proposed exact-file retention and has no
mandatory wrapper.

```text
python -I -B save-analysis/scripts/verify_d5bu_cargo.py --save52 F040.sfs --c3-context sor-d5bx-cargo-c3-v1.json --receipt CARGO.json
```

The unmodified reader ran in a separate process in the same clean source tree.
The only external evidence opens were F040 and the C3 JSON. Local effects,
method and before/after input pins, command and full receipt are under
`.local-work/d5bx/run01/cargo-qualified-v2-final/`. Receipt SHA-256 is
`fdb2b73aeab8e18b0e5098367bedd63d391e26b0b2f10a3134decd67dcfcfcc6`,
identical to D5BU's accepted `rework01/cargo-final.json`.

The result includes the eight C3 comparator keys (`producer_rows`,
`records`, `rows`, `edge_envelope`, `edges`, `downstream`, `markers`,
`ships`). The C3 comparator contains 205,557 framed records, 944 selected rows,
34 producer rows, 246 edges, 75 marker entries and 24 ships. The C2 summary
contains 929 selected rows, 61 qualified markers and 24 ships. The reader
reproduces the four selected He-3 stocks, both no-incoming-edge pad branches,
explicit overrides, the shared zero-stock hold, four Extra30 unknowns, one
ExtraD9 unknown and three malformed Extra33 refusals. A same-length C3 byte
change and substituted F042 each refused in separate adverse processes. The
substituted F042 produced an error-only receipt with `error` and `detail`.
The comparison remains scoped to the selected saved observations and retained
unknowns. The rehearsal used neither the B02 archive nor the historical path
values as lookup operands.
