# D5J methods, provenance and reproducibility

The original brief's AC1–AC8 remain the frozen completion contract. The plan
was identity/preservation checks, targeted installed definition/script reads,
placement and body joins, resource-oracle assessment, comparison and review.
No criterion or authorization was amended.

Starting HEAD: `ed040843b062d2182714360035dc9b8c94a7ee92`.
Starting index SHA-256:
`0a6ba4245b8ce1cfd33c63c2646c57f84fbceb21c22fd87dba2ea016ac683ee6`.
Only the supplied, unchanged D5J brief was initially untracked.
`.local-work/terran-armada-recon/start.json` records the actual baseline.
Initial caller-available free space was 89,506,635,776 bytes on C: and
89,477,156,864 bytes on D:, above both 40,000,000,000-byte guards.

## Inputs, effects and limits

Existing CPython 3.14 and stdlib execute the four small
[scan](../../../research/terran-armada-recon/scan.py),
[join](../../../research/terran-armada-recon/joins.py) and
[check](../../../research/terran-armada-recon/check.py) and
[shared-script](../../../research/terran-armada-recon/shared.py) methods.
All code/reader reuse is maintainer-owned at starting HEAD under SOR-P-0002.
The scan adapts the existing bounded GNRL BA2 directory/member method;
ESM parsing uses `inspect_outpost_definitions.py`, and PEX parsing uses
`research/c2-transport/pex.py`. Inherited method hashes are in sources.csv;
new helper hashes are in the exact review-package manifest and local post-input
receipt, rather than the initial source table.
No third-party code, new dependency, external tool executable or network source
was introduced. Bethesda supplies the installed game content and compiled
scripts; outputs do not acquire redistribution rights from our reader.

Reads: installed plugin headers, selected ESM fields, ten selected compiled
quest/actor script members, three shared compiled members, one English string
table, installed configuration identities and current archive/protected-input
policies. Writes: four task Python
helpers, authored documentation/tables and ignored local receipts/extracts.
No retail launch, attachment, game-native call, script VM execution, save edit,
configuration/plugin write, CK operation, archival migration or Git
index/ref mutation occurs. Additional Ghidra operations read existing analysis
with `-readOnly -noanalysis`; they write only local exports/cache/logs and do
not change analysis content. Decoded scripts and raw fields stay LOCAL-ONLY;
authored synthesis remains REVIEW-REQUIRED. Stop on unexpected protected
changes, identity mismatch, parser bounds failure or either disk floor failing.
No installed content or save cleanup is necessary; ignored receipts are retained.

The initial discovery enumerated all installed ESM quest editor IDs and found
the SFTER namespace in SFBGS050. The scan walks selected record types with
16 MiB per-record framing/decompression bounds and retains a local header/name
catalogue plus 111 selected records. The catalogue is a locator, not a claimed
complete Workshop census; it is excluded from Git and patches. BA2 member
reads are capped at 5 MB with exact decompression closure. Script object/file
closure is asserted. Neither parser executes the inspected content.

The join method walks 39 installed ESM/ESP header/group graphs, resolves MAST
indices for SFBGS050 overrides, preserves beacon group ancestry and reads
selected main-file bodies/properties. Availability and active runtime resolution
remain separate. No universal light-plugin/runtime remapper is implemented.
The negative override result concerns installed forms owned by SFBGS050;
it does not exclude overrides of shared main-file conditions or every archive
script collision. These limits prevent a certified effective-load-order claim.

## Preservation and checks

The existing `remaining_inputs.py` diagnostic was invoked with its LOCAL
variable bound to this task's starting receipt and output directory; the code
and policy were unchanged. It authenticates the active resource archive/index
and compares 93,334 historical expectations as 91,933 archived matches plus
1,401 loose hashes. All 12,974 protected-policy rows and the active-save namespace
pass. It retains the earlier acknowledged four-ZIP incident and historical strict
postflight FAIL label; that earlier failure was not rerun or relabelled here.
Current diagnostics report zero missing historical rows and zero input/save
differences. Cargo remains on its separate active archive-backed baseline;
none of its payloads is used or migrated by D5J.

`checks.json` verifies all three title/base/ancestry/reference-type joins,
exact keyword equality and radius/budget distinctions. It reparses the ten
members and rejects 30 truncated/bad-signature controls; all 40 branch targets
are bounded. These are parser/identity sanity checks, not semantic or runtime
functionality tests. The ESM and BA2 are hashed before/after the scan, and all
39 plugin files are rehashed in the final check. Main EXE and PlanetData identities
agree with their earlier pins. Geometry controls are preserved through the
archive-backed check, rather than regenerated. No historical science result changes.

Preserved diagnostics: an initial console print failed because cp1252 could not
encode decoded bytes; subsequent display used UTF-8. An exploratory all-type
main-file payload walk hit the existing 16 MiB bound; targeted type reads
replaced it without relaxing the bound. The first check compared Python tuples
with JSON lists and failed; canonical JSON comparison corrected that check.
The failed executions did not modify game inputs or create partial authored
tables. Legacy paths and partial graph receipts remain local diagnostics.

For a fresh reproduction from the repository root:

```powershell
$fresh = '.local-work/terran-armada-recon/reproduce-next'
& $python -B research/terran-armada-recon/scan.py --out $fresh
& $python -B research/terran-armada-recon/joins.py --out $fresh
Copy-Item -LiteralPath .local-work/terran-armada-recon/preservation-after.json -Destination "$fresh/preservation-before.json"
& $python -B research/terran-armada-recon/check.py --out $fresh --doc "$fresh/tables"
& $python -B research/terran-armada-recon/shared.py --out $fresh
```

`$python` denotes `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`.
Choose a fresh, nonexistent `$fresh` path. Both receipts **and authored tables**
are redirected locally by these arguments; default paths intentionally refuse
existing files. Extracted PEX writers now use exclusive creation too. The copied
receipt is retained evidence, not a newly executed preservation check. Before
a scientifically new run, rerun the existing archive-backed diagnostic against
that run's HEAD/index/start receipt and pass its authentic result instead.
The shown reproduction was actually executed as `reproduce02` for scan/join/check
using the current after-check receipt; it changed no accepted or task tables.
The shared-script check was separately executed at the original local root.
Do not delete retained evidence or edit protected baselines to rerun commands.
The methods are bounded research helpers tied to this installation, not a
standalone content dump tool. Local receipts pin executed inputs; full plugin
and proprietary decoded payloads are excluded from publication and review diffs.

## Independent-review follow-through

Candidate01 returned REWORK for the unexamined shared beacon binding, native
request edge and reproduction/editorial records. [Native follow-through](native.md)
records the corrected science. Four new bounded exports through the existing
owned `research/workshop-population/export.ps1` / `ReadSpecialist.java` locate
symbols, inspect two conditions, follow alias loading/filling into the request
queue and inspect the generic Workshop-extra accessor. Every completed export
has an END marker. Native call effects are inspected, never executed.

The new [byte exporter](../../../research/terran-armada-recon/ReadD5JBytes.java)
reads seven explicit existing function bodies, capped at 262,144 bytes, and
writes one exclusive ignored TSV. The local `verify-native.py` reads that TSV,
the installed PE, four completed exports and the database-content baseline;
it writes only `native-verified.json`. It compares every exported body range to
the installed PE and rehashes all 15 database files. The database baseline was
sampled concurrently with initial read-only exporter startup; it is not claimed
as a strictly earlier process-launch snapshot. No analysis-content write API
was used. Export logs, all native bytes and decoded script bodies remain ignored.
The byte export's initial comment incorrectly said eight functions; the final
source corrects the comment to seven without changing executed statements.

The automatic screen output is retained in the local editorial receipt. Manual
coverage includes all new reports/tables, Python explanatory text, Java comments
and changed navigation/source/credit prose. The final review manifest records
the exact screened/read/reviewed bytes; no zero-diagnostic result substitutes
for either manual or independent reading.
