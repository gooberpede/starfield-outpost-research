# Starfield native function catalogue

Use the [RVA index](index.md) to look up an address or the subject pages to
follow a mechanism. This reference describes observed internal implementation
for researchers and prospective SFSE plugin authors. External invocation,
hook placement, object lifetime and thread safety remain unvalidated. An
observed argument register is evidence about the cited path. Receiver types,
hidden outputs, return channels and other callers require their own evidence.

The first research release targets **Starfield.exe retail 1.16.244.0** with
SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The preferred image base is `0x140000000`. Each identity is the executable
hash, module and verified entry RVA. Subtract the preferred base from a
preferred VA. Add the RVA to the actual loaded module base for a runtime VA.
Another verified executable gets separate entries and any evidenced
cross-version correspondence is recorded separately. Starfield.esm has its
own independent pin. Save creation metadata and winning installed inputs
remain source- and sample-specific. [Build baseline](../reference/b3-baseline.md).

Instruction sites, call sites, globals, object member offsets, vtable byte
displacements, saved-file and decoded-stream offsets, and physical ESM offsets
retain their own domains. A wrapper, thunk or forwarding stub can have a
distinct verified entry from its target. Papyrus declarations and compiled
scripts have their own identity. `FUN_…` labels come from the analysis tool.
Descriptive labels are researcher-assigned. [Technical glossary](../reference/glossary.md).

| Depth | What the entry describes |
| --- | --- |
| A · Characterized | A scoped mechanism with meaningful operands, conditions and effects. |
| B · Partial | Useful behavior or a bounded contract, with material semantics or ABI still open. |
| C · Located | A verified entry and source-supported relevance, with limited individual characterization. |

Depth is separate from scientific confidence, evidence basis, review and
publication eligibility. Follow the original evidence for those classifications.
Proprietary binaries and raw native exports are local-only. Tracked links lead
to authored records and source locators. **PUBLICATION DEPENDENCY — EVIDENCE
ACCESS PENDING** where source-level replay requires a private export or receipt.
Publication remains **NOT READY / NOT CLEARED**. [Publication gate](../PUBLICATION.md).

## Subjects

- [Geography and resource generation](geography.md)
- [Workshop identity, construction and position](workshop.md)
- [Extractors, organic facilities and fabrication](production.md)
- [Power and generator fuel](power.md)
- [Storage, inventory and cargo](inventory.md)
- [Crew, robots and defense](population.md)
- [UI, save framing and lifecycle](interfaces.md)

## Data and provenance

- [Catalogue](catalogue.csv) has one row per `(exe_sha256, module, rva)`. `entry`
  points to the full entry in this directory. `va` is the preferred VA.
- [Aliases](aliases.csv) preserves aliases by kind, original path and physical
  CSV row or Markdown line. The canonical join uses `exe_sha256`, `module`
  and `entry_rva`. A blank `entry_rva` leaves a source-local locator unresolved.
  Export selectors can refer to several entries. Search for the exact alias and
  inspect the source before choosing a record.
- [Evidence](evidence.csv) records contributing source rows. On `function-entry`
  rows, derive the RVA from `va` using the current single-image base. A manifest
  overlap has its own domain and does not establish entry identity. `line` and
  `end_line` are inclusive physical lines in the original source. Private export
  locations remain in the original ledgers.
- [Coverage and reconciliation audit](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/native-function-catalogue-d5bd/README.md`)
  accounts for exclusions, unresolved locators, repeated aliases and all 18
  reference pairs. The [historical register](../function-register.md) retains its
  original groupings and identifiers.

For exact verification of the original catalogue and audit outputs, run
`python -B research/function-catalogue/verify.py` from a checkout of the frozen
D5BD source commit `6e799a428a765aa196a24d3c1de8ae133260aa08`. The verifier
reads repository text and curated source joins using the Python 3 standard
library. Its checks cover generated content, address arithmetic, known alias
collisions and generated relative links.

Later audit documents extend the scanner's inventory. D5BG verified the
original source set and found that the newer tree changes the generated
coverage and locator tables while preserving the catalogue, aliases, evidence,
index and subject pages. Use the frozen source set for exact reproduction of
the original audit outputs. See the
[D5BG reproduction decision](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-claims-d5bg/handoff.md#catalogue-reproduction`).
