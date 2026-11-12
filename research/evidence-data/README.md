# D5BZ current evidence source edition

The [current-edition manifest](current-edition.json) binds active copies and
changed source paths to their exact bytes and prior identities. The
[relocation map](../archival/relocations.json) identifies their original
paths in the [audit archive](../../docs/audits/README.md#archive-lookup).
The audit ZIP preserves original manifests, paths, checksums and receipts.
Historical JSON locators describe their original source or private custody.
The [relocation verification table](../archival/relocation-verification.csv)
lists each destination, its consumer, both hashes and the relevant checks.

| Consumer | Operands and boundary |
| --- | --- |
| D5BU shared controls and Workshop | The byte-preserved D5BF release asset ledger supplies the exact original member pins. |
| D5BX projected Workshop | The byte-preserved D5BX supplement index and D5BF ledger supply the Workshop archive and original member pins. |
| D5BX Cargo | The reader takes the exact C3 JSON and F040 explicitly. Its source has no relocation delta. |
| D5BI N2 | The byte-preserved D5BI manifest supplies candidate and member pins. |
| D5BG, D5BV and D5BY | Current validator copies check the graph, selected routes and reader navigation. D5BV resolves original path and source identities using the crosswalk, audit members or the exact baseline Git object. It validates current source identities separately. |
| B3 | The [current baseline](../../docs/reference/b3-baseline.md) and [method contracts](../../docs/reference/b3-methods.md) link the selected authored source and versioned metadata. |

From the repository root using Python 3.14 with assertions enabled:

```text
python -B research/evidence-data/publication-claims-d5bg/verify.py --negative-controls
python -B research/evidence-data/evidence-closure-d5bv/verify.py --negative-controls
python -B research/evidence-data/documentation-synthesis-d5by/verify.py
python -B research/archival/verify_assets.py
```

The B3 metadata check compares exact historical source bytes. In a disposable
copy of the checkout, restore CRLF line endings in these three files under
`research/historical-methods/b3/` before running it.

- `l2-budget/native/TransitCalls.java`
- `c2-transit/native/E2ReadSession.java`
- `cr3-lifecycle/native/Cr1Recon.java`

Keep all other bytes, including the final newline, as checked out. Confirm each
restored file against the SHA-256 in [promoted-sources.csv](publication-readiness-b3/promoted-sources.csv).
Then run `python -B research/evidence-data/publication-readiness-b3/check.py`
from the root of that disposable copy. This reconstructs the three historical
byte identities from the LF Git blobs.

These checks read source and metadata. They leave original evidence, receipts,
the Git index and references untouched. For original-witness and derivative
readers, supply the exact lawful files explicitly under the
[evidence access contract](../../docs/reference/evidence-access.md).
The [catalogue instructions](../function-catalogue/README.md) retain the
original D5BD and D5BS Git revisions. Historical packaging and review exporters
with original loose-path contracts belong to their historical checkout.
