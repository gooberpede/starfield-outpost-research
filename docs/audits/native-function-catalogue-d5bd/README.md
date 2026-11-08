# D5BD native function catalogue audit

[Controlling brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BD_Native_Function_Catalogue_and_Developer_Reference.md) ·
[Developer reference](../../functions/README.md) · [Build pin](../publication-readiness-b3/baseline-manifest.md) · [Completion ledger](closure.md)

| Question | Investigation and required evidence |
| --- | --- |
| Q1 · Discovery and canonical identity | Census original tables and narrative locators. Classify entry, export selection and instruction site separately before normalizing. Audit each historical alias in its source namespace. |
| Q2 · Technical characterization | Preserve scoped source contracts, build/condition limits and unknown ABI. Challenge representative A/B/C entries against original evidence. |
| Q3 · Developer presentation | Check entry-by-RVA, subsystem, historical ID, unknown prototype and SFSE reader journeys. Verify generated paths and fragments. |
| Q4 · Reconciliation and quality | Cross-check all 18 pairs after original inventory. Preserve disagreements and source gaps. Obtain independent review on the exact candidate snapshot. |

## Coverage records

- [Coverage by source](coverage.csv) lists scanned files, physical lines for
  Markdown and data rows for CSV. Counts refer to inventory records. A source
  line may cite several entries and can also contain other locator candidates.
  The A/B/C columns count the catalogue depth of included observations in that
  source. They can exceed the number of distinct entries when sources overlap.
- [Exclusions and unresolved locators](locators.csv) retains physical source
  coordinates, aliases and candidate address strings. `candidate` records are
  a broad lexical queue. They include calls, globals, sites, repeated prose,
  historical alias mentions and addresses whose roles remain to be classified.
  `unresolved` rows identify exact-context narrative candidates whose entry
  identity or outpost relevance remains unqualified. An `excluded` row records
  the exclusion rationale. Verified interior windows are preserved with
  their separate containing entry in the evidence table.
- [Repeated aliases](repeated-aliases.csv) lists every repeated alias from the
  structured and curated mappings, with one row per source location and the
  number of distinct resolved entry RVAs. Narrative occurrences without a
  verified mapping are searchable in the locator ledger.
- [Reference pair crosswalk](crosswalk.md) records the semantic comparison.
  [Reference addresses](reference-addresses.csv) records the later numerical
  check. An overlap alone establishes neither entry domain nor agreement.

## Investigation ledger

| Branch | Check and disposition |
| --- | --- |
| Q1 · Structured original tables | Header census covers authored Markdown and CSV under experiments, subsystems, runtime, audits, save analysis and research, plus the function/state registers. Recognized entry tables were normalized before the reference pass. Export-only rows without a documented individual relation remain excluded. Source-manifest addresses without a direct entry proof remain unresolved. |
| Q1 · Narrative entry evidence | Curated positive entries use original experiment sections, with line locators in the generator inputs. An additional pass joins inline mechanism references to an exact function roster in the same experiment. The report mention supplies relevance and the roster supplies the entry address. Relevant addresses found by the reference pass were resolved back through original reports. The broad candidate ledger still contains unclassified narrative occurrences. |
| Q1 · Domain counterexamples | Locations failed entry lookups are excluded. The ordinary resource call at `0x14079be20` resolves to `0x14079c470`. The dependency decrement at `0x1427e61a4` lies inside `0x1427e5e80`. Workshop grid result `0x140ad0d3b` and center common exit `0x140f4ac44` are interior sites. Workshop Z dependencies' abbreviated `B56D0` remains source-local. |
| Q2 · Evidence depth | The selected A/B dossiers cite exact original sections. Structured contract rows supply B where inputs, outputs, effects and limits are recorded. C retains a located relation and leaves individual ABI and broader behavior open. |
| Q3 · Navigation | The subject pages and RVA index are generated from the same canonical rows. The links, build arithmetic and legacy collision fixtures are deterministic checks. |
| Q4 · Current reference reconciliation | All 18 pairs received a subject crosswalk and exact-token pass. The crosswalk distinguishes numeric matches and known interior tokens. The current references informed discrepancy resolution after the original pass. They supply no canonical entry proof. |
| Q4 · Rights and reproducibility | This documentary pass used authored records, local ledger metadata and original evidence pointers. Raw Ghidra exports and other proprietary inputs require authorized access for byte-level replay. |

The standing orders, workflow, charter and third-party policy constrained the
work to documentary changes and repository reads. The evidence standard and
relevant research-state entries drove the separation of version pin, scientific
confidence, static versus live basis, owner lifetime and publication access.
The completion and reviewer procedures govern exact-snapshot review and the
local patch handoff. The B2 notation and export-ID records govern address
domains and local selector namespaces. The B3 manifest and the original
provenance records govern the executable identity. In particular, neither a
common build nor a current module owner establishes a historical save or
request epoch. [Research state](../../RESEARCH_STATE.md) ·
[Provenance](../../PROVENANCE.md) · [Evidence standard](../../EVIDENCE_STANDARD.md).

## Identity and interpretation decisions

| Historical alias | Function register | Crew function table |
| --- | --- | --- |
| `SOR-FN-0062` | Resource-region callback, `0x021e0f50` | Add available unassigned actor, `0x02008540` |
| `SOR-FN-0063` | Harvester resource consumer and property-presence helper, `0x021f68f0` and `0x0044b610` | Assignment predicate, `0x004074f0` |
| `SOR-FN-0064` | Generator, `0x0079a330` | Player-clamped destination capacity, `0x004074a0` |

The resource meanings come from [the historical register](../../function-register.md)
line 31. The crew meanings come from the [crew table](../../experiments/crew/functions.csv)
lines 66, 2 and 29 respectively. Legacy composite headings can map to several
entries. The register's reuse of `SOR-FN-0061` for the organic investigation
also has a source-qualified heading locator in the alias table with no assigned
entry RVA.

The GetWorkshop target and registration callback are distinct locators. The
original register calls `0x142073cf0` `LAB_142073cf0` and records no Ghidra
function at that entry in that export. The runtime operand contract qualifies
the callback boundary and its jump into `0x140517d60`. The historical label and
the target stay separate. [Function register](../../function-register.md) ·
[EXP0002 contract](../../../runtime/exp0002/STATIC-CONTRACT.md).

Later power work distinguishes queue insertion and rotation from discovery-vector
ordering. Earlier power contracts remain attributed at their original rows.
The original [P1 follow-up](../../experiments/power/followup.md) supplies the
correction in the `0x140677c50` entry. For resource generation, the source pointer, manager ownership and
runtime lifetime are separate observations. The first gate in the historic
generator report remains conditional. [Source decision report](../../experiments/resource-source-decisions/native.md).

The historical `SOR-FN-0049` group includes `0x140f515a0`. The original
population trace attributes producer-row serialization to that iterator under
`0x140f50660`. The paired `0x140f50880` is the Workshop loader. The group
alias alone does not assign a reader role. [Population lifecycle](../../experiments/resource-population-lifecycle/native.md).

The first independent review returned **REWORK**. The subsequent pass added
original roster joins, explicit transit and display entries, separate subject
links for crew contribution and the Extra33 helpers, and the entry-level
residual and deque corrections. Transit shorthand follows the original `tNNN`
namespace. [Original transit methods](../../experiments/cargo-links/transport/transit.md).

The second independent review returned **REWORK**. The revised inventory
joins explicit native role phrases to verified rosters across experiments.
An unassigned alias or generic supporting-operation label alone supplies no
relevance proof. The specific biome initializer pair uses its original path
and extension evidence. The effective resource-setting chain now traces the
constructor, lookup, dispatcher, DATA reader, setter and command route. The
setter's interior write at `0x140684b43` stays out of the index.
[Biome report](../../experiments/outpost-biomes/native.md) ·
[Settings report](../../experiments/resource-installed-settings/settings.md).

The third independent review returned **REWORK** on the omitted SFTR
exact-name factory registry. The revised catalogue includes registration,
lookup, map helpers and shutdown. The shutdown stub has a separate identity
from its target. Its original failed Ghidra selection remains part of the
source record. The census also recognizes source-manifest rows explicitly
declared as function bodies or function exports. A mechanism reference or
curated original role still determines relevance. Mixed-domain window rows
retain their source classification. [Original SFTR registry trace](../../experiments/resource-retained-population/d5ad-save-state-matrix.md#registry-namespace-qualification-and-retained-method-failures).

The fourth independent review returned **REWORK** on adjacent SFTR loaders,
the saved-destination frame and a single-cell preparation ingress. Those
entries now cite the original source reports. The census recognizes D5W's
explicit fresh and inherited function categories. To resolve the remaining
D5AD entry-domain discrepancy, a bounded offline check matched 357 nominated
header lines and source SHA-256 values across 78 retained text exports.
It distinguished 356 `FUNCTION` headers and one `DATA` header. Only the
function-boundary metadata is carried forward. The `DATA` row is the separately
documented SFTR shutdown stub and retains its distinct evidence.
[Boundary receipt](../../../research/function-catalogue/d5ad-boundaries.csv) ·
[Original D5AD ledger](../../experiments/resource-retained-population/d5ad-sources.csv) ·
[D5W ingress](../../experiments/resource-retained-population/d5w-normal-path-model.md).

The receipt joins the original D5AD physical `line`, preferred `va` and
`export_sha256`. The generator checks that join and still requires a documented
relevant relationship. Rebuilding the catalogue uses the recorded receipt
without rereading the exports. Replaying the header and byte-hash check depends
on authorized access to the original retained text exports.

The fifth independent review returned **REWORK** on the Landscape Grid
release and PCM save maps. The census now recognizes the D5V `NATIVE FUNCTION`
classification and admits specific D5AD ledger roles when the matching
`FUNCTION` boundary was independently verified. Generic proof descriptions
still require a separate mechanism reference. The save-framing subject links
the paired type-7 reader and writer, and the geography subject links the Grid
release with its distinct source-lifetime limit.
[D5V ledger](../../experiments/resource-retained-population/d5v-sources.csv) ·
[PCM save-state matrix](../../experiments/resource-retained-population/d5ad-save-state-matrix.md).

The sixth independent review returned **REWORK** on task completion and the
ready scan. The revised catalogue adds completion publication, its callback,
edge removal, ready scan and the paired bound comparisons. The nomination
check matched 200 `FUNCTION` headers and source hashes across the retained
D5AE and D5AF ledgers. The interior dependency decrement remains a locator.
[Scheduler report](../../experiments/resource-retained-population/d5ae-scheduler-causality.md) ·
[Scheduler boundary receipt](../../../research/function-catalogue/scheduler-boundaries.csv).

The seventh independent review returned **REWORK** on the provider's temporary
list append and cleanup helpers. Both now have separate entries and exact D5Q
source locators. The reviewed retained export has matching source hashes and
`FUNCTION` headers immediately before both nominated windows. The appended
pointer and the caller-owned list allocation have separate lifetime rules.
[Provider dataflow](../../experiments/resource-retained-population/d5q-call-dataflow-map.md).

The bounded lexical sweep cannot establish exhaustive narrative semantics.
Some candidates are mentions of already catalogued entry values. Others
still require source-context classification, including abbreviated and
mixed-domain locators. The complete per-file accounting and rows are above.
Historical source confidence and publication status remain independent of
these inclusion decisions.
