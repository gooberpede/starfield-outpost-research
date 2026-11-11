# Experiment-local native export references

2026-10-21. A function's preferred VA identifies code in a pinned image. A
scientific source pin identifies exact evidence bytes. A local export number
identifies an acquisition/selection within one experiment. These are different
identities. This navigation guide does not publish raw native outputs.

## SD1 lookup example

In [SD1 native contracts](../experiments/containers-displays/native.md),
`n010` abbreviates SD1 request/output stem `010.request`, specifically
`.local-work/sd1-containers/native/010.request.tsv`. It is not the tenth function,
a global symbol, or a publication-cleared attachment. The retained request lists
selectors; its TSV holds multiple FUNCTION sections. The `.request.done` companion
is a reader-completion marker, not proof every section or decompiler type is sound.
See [methods](../experiments/containers-displays/methods.md),
[functions](../experiments/containers-displays/functions.csv) and
[source pins](../experiments/containers-displays/sources.csv).

The SD1 register contains one row per function address, retaining the first
encountered output in sorted request-file order. It does **not** enumerate every
later re-export. This follows the surviving original `sd1-registers.py` metadata
generator. For example, `141eadb50`'s registered export is `033.request.tsv`,
while SD1 n039 is a later surviving export containing the same FUNCTION.
`1419aa500` and `1419a41d0` register n040 but also occur in n041. The
[checked lookup table](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/focused-export-lookups.csv`) preserves both the registered
export and the actual cited export; neither is silently renamed.

| Scoped ID / output | Tracked function correspondence | Lookup |
|---|---|---|
| SD1 n010 / `010.request.tsv` | Includes `141eaf090`, `141eafe00`, `141eb01a0` and other functions. | Match static_va in functions.csv, distinguish its retained export from any later cited re-export, then match that cited full path and SHA-256 in sources.csv. |
| SD1 n039 / `039.request.tsv` | Includes `141eadb50` and inventory/equipment functions such as `140641180`. | One request selects several functions; the number alone identifies no particular branch. |
| SD1 n041 / `041.request.tsv` | Includes `141eadf60`, `140b67a30`, `1419aa500`, `1419a41d0`, `14146bc10` and selected reference results. | A `refall:` selector is reconnaissance, not a function name; inspect actual FUNCTION headers and coverage limits. |
| SD1 n042 / `042.request.tsv` | Includes `141eae1f0` and its menu filter/inversion reads. | Instructions establish object-field reads independently of inferred decompiler types. |

Tracked explanations/registers give public readers the bounded mechanism and code
identity. With authorized local access, verify the pinned TSV's imported EXE
hash/base, find its FUNCTION section and inspect exact instructions. Raw exports
are **LOCAL-ONLY**; missing access limits byte replay without demanding proprietary
decompilation publication. If no matching register/output survives, mark the
reference **unresolved local export locator**. Never infer a mapping from digits
or a similarly numbered file in another experiment.

## Other verified local namespaces

These defaults come from existing document declarations and tracked function/source
registers. Explicit prior-work qualifiers such as CR2 or S1 override a document's
default. Identical `n010` labels in different experiments do not identify the same
function/output. `NNN` is the request stem here, not a universal identifier format.

| Explanation / registry | Local namespace and lookup |
|---|---|
| [L2 native](../experiments/build-budget/native.md) | nNNN → `.local-work/l2-budget/native/NNN.request.tsv`; functions.csv supplies path/hash/coverage. |
| [BM2 catalogue](../experiments/build-catalogue/catalogue.md) | nNNN → `.local-work/build-catalogue/native/NNN.request.tsv`; functions.csv links sections/hashes. |
| [C1 native](../experiments/cargo-links/configuration-ui/native.md) | Local n labels → `.local-work/c1-cargo/native/NNN.request.tsv`; dNN instead uses `.local-work/recon/c1-cargo-NN.tsv`. |
| [C2 functions](../experiments/cargo-links/transport/functions.csv) | `.local-work/c2-transport/native/NNN.request.tsv`; use the actual export path, not a C1 row with the same number. |
| [BM1 manual/automatic](../experiments/construction-variants/manual-and-automatic.md) | nNNN → `.local-work/construction-variants/native/NNN.request.tsv`; functions.csv supplies sections/hash/limits. |
| [CR3 native](../experiments/crew-lifecycle/native.md) | nNNN → `.local-work/cr3-lifecycle/native/NNN.request.tsv`; explicit inherited CR2 labels retain the CR2 root. |
| [CR2 native](../experiments/crew-skills/native.md) | nNNN → `.local-work/cr2-skills/native/NNN.request.tsv`; pins and semantic aliases remain separate. |
| [L1 native](../experiments/limits/native.md) | nNNN → `.local-work/l1-limits/native/NNN.request.tsv`; distinct rNNN retains the original document's declaration. |
| [S2 native](../experiments/local-output-links/native.md) | nNN → `.local-work/recon/s2-links-NN.tsv`, through n13; not SD1's three-digit request filename. Prior S1 cNN retains S1 provenance. |
| [LO1 native/UI](../experiments/locations-outpost/native-and-ui.md) | nNNN → `.local-work/lo1-locations/native/NNN.request.tsv`; mNNN is inherited SD3 ABC-method data, not a native request number. |
| [Biome native](../experiments/outpost-biomes/native.md) | nNNN → `.local-work/outpost-biomes/native/NNN.request.tsv`; function rows retain export limitations. |
| [DA1 integrity](../experiments/outpost-defense/integrity.md) | Native numbers → `.local-work/da1-defense/native/NNN.request.tsv`; functions/source pins resolve local selections. |
| [R1 functions](../experiments/robots/functions.csv) | `.local-work/r1-robots/native/NNN.request.tsv`; exact path/VA/hash in the register, not a global n namespace. |
| [SD2 methods](../experiments/shared-outpost-storage/methods.md) | nNNN → native/NNN.request.tsv under `.local-work/sd2-shared/`. |
| [SD3 methods](../experiments/stored-resources/methods.md) | nNNN → native/NNN.request.tsv under `.local-work/sd3-stored/`; compiled ABC method numbers in JSON are separate. |
| [L3 native](../experiments/spatial-placement/native.md) | nNNN → `.local-work/l3-placement/native/NNN.request.tsv`; original line ranges and coverage govern. |

Equivalent locators remain distinct: S1 sNNN is declared in
[storage/native.md](../experiments/storage/native.md); cNN uses
[capacity-source pins](../experiments/storage/capacity-sources.csv).
E1 aNN is declared in [arithmetic-production.md](../experiments/inorganic-extractors/arithmetic-production.md).
Older uppercase N labels follow the [native-availability function register](../experiments/native-availability-map/functions.csv);
no request-number meaning is inferred for those register IDs. For other shorthand,
follow its own report/register. No new export or tool execution is authorized.
