# Workshop original and projected qualification

The frozen original reader returned the accepted D5BU roots receipt
`e51360ceacffac7448e1b1f6151be8358df19140422a97ba3dfc451d0df08f79`.
The builder compared the entire original and projected supplement objects.
The only normalization replaces the historical `source` object in the comparison
with its two published identity fields. The projected reader independently
replayed all 657 baseline roots and 8,628 pre-supplement role records from
the saved-link operands, then reapplied the owned supplement predicates.
The comparison includes per-root owner, base, class provenance, saved flags,
member identities and offsets, original and corrected roles, and every owner
record. The independently read F040 saved bytes confirm projected framing,
type, buffer override, saved prefix, linked extras and selected owner edges.
[Original Workshop population research](../../experiments/workshop-population/report.md) ·
[D5BU methods](../original-save-verification-d5bu/methods.md) ·
[Credits](../../../CREDITS.md#d5bx-workshop-and-cargo-reader-access)

| Case | Reproduced control |
| --- | --- |
| Supported roots | 657 baseline plus 191 supplemental, for 848 total. The main ESM supplies 51 STAT, 89 FURN and 51 PKIN supplemental bases and confirms the type, record offset and flags for 827 root definition references. The other 21 retain historical add-on definition provenance. The three ChairGeneric saved references stay distinct. |
| Typed membership | All 6,345 ordered member tuples match D5BU. All 8,753 retained typed reference records rejoin by identity, type, decoded offset and buffer override. The ordinary partition is 653 single roots, 195 PackIn roots, 2,282 foundation members and 5,497 generated members. One nonordinary target remains unresolved. |
| Saved owner state | 17 saved-disabled-clear and two set. F040's 17 inline fixtures join to distinct clear ordinary owners. F042 and F043 each retain their separate PackIn beacon root. |
| Canonical ledger | 31 group rows resolve into six already supported roots, one ship mapping, eight Hab dummy duplicates and 16 unresolved canonical groups. All 31 source counts and recorded R3 presence values match F040, including 115 separately checked typed DA sources. Both Hab cases retain their absent group representatives, four wall sources each and disabled dummy replacement joins. DA source and inherited world/location association establish context. Ordinary ownership and construction origin remain unresolved. |
| Omitted and unsupported | Supplemental `Extra9C` stays null for all 191 additions. `DYNAMIC:ff03fb72` and `DYNAMIC:ff05ccc5` retain `EXTRA_EA_UNSUPPORTED`. Overall population completeness remains false. |
| ALLA | All 2,643 projected pairs yield zero keys for `0x054ba6`, `0x000191` and `0x000192` in the main ESM namespace. The raw low 24 bits also exclude those exact object IDs in all projected pairs. A fresh main ESM read matches 2,077 QUST records, 22,190 aliases and 1,792 pairs. The other installed ESM census facts are inherited. |

## Commands and evidence

Use Windows CPython 3.14.3 with assertions enabled and existing exclusive
scratch parents. The builder reads four exact historical inputs and writes the
ZIP and one private fidelity receipt. The reader writes an exclusive JSON
receipt and uses guarded temporary decoding of F040, F042 and F043. The
commands accept explicit operands and make no game, debugger or network calls.

```text
python -I -B save-analysis/scripts/build_d5bx_workshop.py --baseline BASELINE --typed TYPED --alla ALLA --canonical LEDGER --archive WORKSHOP.zip --fidelity FIDELITY.json
python -I -B save-analysis/scripts/verify_d5bu_controls.py roots --member 40 F040 --member 42 F042 --member 43 F043 --root-context BASELINE TYPED ALLA --canonical-context LEDGER --esm MAIN.esm --receipt ORIGINAL.json
python -I -B save-analysis/scripts/verify_d5bx_workshop.py --member 40 F040 --member 42 F042 --member 43 F043 --archive WORKSHOP.zip --esm MAIN.esm --receipt PROJECTED.json
python -I -B save-analysis/scripts/test_d5bx_workshop.py WORKSHOP.zip -v
```

Local qualification staged the proposed ZIP, the three exact extracted CORE
originals and a hash-checked copy of the lawful main ESM. The clean source tree
contains selected Git-tracked owned methods plus the pending projected-reader
edition and its asset index. It has no private evidence directory. The separate
Python process logged open events and imported modules, denied undeclared
Python file opens, and verified identical before/after pins. The observed
external input opens were exactly F040, F042, F043, `Starfield.esm` and the
Workshop ZIP. Source opens included the D5BF and D5BX indexes and the owned
methods listed in the local receipt. The audit covers Python open events and
module filenames. It is process-level instrumentation with no OS sandbox claim.

The `workshop-qualified-v2-final` directory under ignored `.local-work/d5bx/run01/`
contains `receipt.json`, `run.log`, `effects.json` and `pins.json`. Its result
matched the authoring-tree result byte for byte, the frozen D5BU result field
for field, and the full private `projection-fidelity-v2.json` supplement.
The separate `source-crosscheck-v2.json` records exact field and row selection
comparisons against the original contexts, including each canonical DA count.
The earliest historical helper intake pin is still missing. This qualification
authenticates the inputs now in custody.

## Refusals

The clean reader refused a missing archive, substituted Cargo JSON, a changed
ZIP, duplicate F040 selection, wrong ESM and exchanged CORE members. Archive
tests challenged absent, duplicate, traversal, drive-qualified and unexpected
entries, order, symlink metadata, equal-length wrong member content, wrong
canonical identity and a stale schema with recomputed member hashes. Actual
projected-row tests removed a group member, a Hab wall and a canonical DA
source. They introduced forbidden 191 and 192 keys, changed an ALLA raw word
while retaining its resolved key, and promoted an unsupported extra to closed.
Each produced its expected semantic refusal. An audit probe attempted a synthetic undeclared
read and was denied. Local logs are `tests-v2.log` and `adverse-v2/` under the run.
