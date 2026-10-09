# Offline Analysis Scripts

## Output-link L0–L2C validation

The invoked [link-validation brief](../../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_output_link_validation_L0-L2C.md) authorizes [validate_output_link.py](validate_output_link.py) and [probe_output_link_structure.py](probe_output_link_structure.py). [Results](../../docs/experiments/output-link-validation-L0-L2C.md). Installed CPython3.14.3 standard library only; use its explicit installed executable if the Windows `python` alias is unavailable. No downloads or effects on game processes/static-analysis projects.

`validate_output_link.py` without arguments reads the brief/prior manifests, records preregistered old candidates, exclusively copies six named originals and reuses S4C, verifies source/copy/source hashes/size/mtime, then writes decoded streams and bounded diff analysis. Existing archive/output roots cause refusal; do not rerun archive creation. `--run <fresh-name>` reads the existing exact manifest and parses only hash-verified local copies into a new analysis directory. It preserves absent old signatures as negative observations. Reads/writes are bounded to the named source saves and ignored `.local-work/output-link-L0-L2C/` / `.local-work/savegames/` paths. It imports the existing project decoder/diff/metadata/candidate constants without changing them.

`probe_output_link_structure.py` reads hash-verified decoded `analysis-01/` inputs plus historical S3C/S4/S4C and writes an exclusive local `structure.json`. Endpoint correspondence is based on old framing/base-like bytes and repeated tokens, independently of relationship state; nonunique/missing matches stop. The bounded envelope is an explicitly post-preregistration hypothesis, not a full parser. The first strict literal run stopped on missing old L0C beacon signature; partial outputs/preregistration remain intact. The final `analysis-01` and `structure.json` already exist and must not be overwritten.

Executed commands (prefix with the installed Python executable):

```text
save-analysis/scripts/validate_output_link.py
save-analysis/scripts/validate_output_link.py --run analysis-01
save-analysis/scripts/probe_output_link_structure.py
-m unittest discover -s save-analysis/scripts -p test_manual_corpus.py -v
```

Local `build_review_tables.py` reads only verified analytical outputs and writes four selected review CSVs; `validate_review.py` independently checks preservation, payload bytes/bounds/canonical comparison, links and Git state, and writes local validation/inventory/status/diff outputs. Neither stages anything. Raw windows and personal paths remain local; selected summaries require review.

## Historical S0–S7C tooling

The invoked [manual corpus brief](../../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md) authorizes these original, corpus-specific helpers. [Results and limits](../../docs/experiments/manual-save-corpus-S0-S7C.md). Installed CPython3.14.3 standard library only (SOR-S-0113); no dependency download, vendoring, target execution or save editing.

| Script | Reads | Writes / limits |
|---|---|---|
| [archive_manual_corpus.py](archive_manual_corpus.py) | Brief; exactly 17 live files for hash/metadata/copy; existing destination only for verification | Exclusive new copies in ignored `.local-work/savegames/manual-S0-S7C/`; manifest in `.local-work/manual-S0-S7C/`. Refuses manifest overwrite, fails missing/hash/mtime mismatch. Never parses originals. |
| [analyze_manual_corpus.py](analyze_manual_corpus.py) | Hash-verified copies named by manifest, constrained to archive | Fresh `--run` subdirectory, decoded streams/string inventories/analysis JSON; max64MiB declared decoded size, observed header/chunk/bounds/checksum/EOF checks; no general inner-schema decoder. |
| [probe_manual_candidates.py](probe_manual_candidates.py) | Hash-verified decoded streams plus analysis JSON | New `candidates.json`; rejects ambiguous main signatures. Corpus-discovered exact motifs; role/float interpretations are hypotheses. Untyped storage counter probe is exploratory and supplies no reported inventory semantics. |
| [test_manual_corpus.py](test_manual_corpus.py) | Synthetic in-memory fixtures only | Console unittest results; validates bounded transform/alignment, not game semantics. |

Run from repository root with the installed Python executable (no package installation):

```powershell
python save-analysis/scripts/archive_manual_corpus.py
python save-analysis/scripts/analyze_manual_corpus.py --run analysis-01
python save-analysis/scripts/probe_manual_candidates.py --run analysis-01
python -m unittest discover -s save-analysis/scripts -p test_manual_corpus.py -v
```

The archive and analysis-01 already exist: do not overwrite them. For a repeated analysis use a new run name after confirming scope; archive verification can compare manifest hashes without rerunning copy creation. Scripts have no effects on the game or static-analysis databases. Unexpected layout/bounds errors stop analysis rather than guess a fallback decoder. Keep generated bulk outputs local.

The local `build_review_tables.py` in `.local-work/manual-S0-S7C/` selects only numeric/timing/hash/candidate fields into the three review CSVs. It omits exact personal filenames, raw windows and unrelated extracted strings. Those summaries still require review before staging/disclosure. Local validation and review-export scripts are listed in the validation record; they do not grant Git write authority.

## Structural containment of existing archives

[analyze_structural_containment.py](analyze_structural_containment.py), authorized by the [invoked brief](../../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_outpost_save_structural_containment.md), reads the two existing manifests, prior analysis hashes and hash-verified archived .sfs copies. Originals are read only for integrity hashing/stat checks. Reuses original decoder/candidate definitions with CPython standard library; no downloads, general save editor or process/database effects.

Run from repository root with the recorded installed Python executable:

```text
save-analysis/scripts/analyze_structural_containment.py --run <fresh-name>
```

Writes CSV summaries and provenance/analysis JSON into an exclusively new ignored `.local-work/structural-containment/<fresh-name>/`. It does not copy original saves or write decoded blobs. Missing/hash/bounds/ambiguous-directory/object/string correspondence stops; missing arithmetic token mappings are negative evidence. Positional unequal bytes include shifts/reordering and must not be called semantic edits. Directory/family names and tail-pair interpretation are hypotheses. Completed final run is `analysis-06`; earlier exploratory/partial roots are retained. [Report and complete helper/output inventory](../../docs/experiments/outpost-save-structural-containment.md). Local `build_review_tables.py` selects numeric summaries; local `validate_review.py` hashes inputs, independently checks pointers/name indices, checks documentation/Git state, and writes a full tracked-plus-untracked diff without staging.

`test_structural_containment.py` constructs synthetic in-memory directory/string/tail fixtures; checks ambiguous directory, inconsistent count bounds, dangling string indices, malformed lengths/pointers and trailing bytes. It reads no saves and writes only console test results. Run `-m unittest discover -s save-analysis/scripts -p test_structural_containment.py -v`.

## Mature-save bounded validation

[validate_mature_outposts.py](validate_mature_outposts.py) is authorized by the [mature brief](../../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_mature_save_outpost_validation.md). Reads the named existing mature archive, sole copied scratch JSON, S/L manifests and prior analysis identities, archived controlled saves, original project directory labels and preserved offbook decoder. Exploratory methods are conceptually reused with exact hashes under SOR-S-0124; no exploratory driver is executed. CPython standard library only, no installation or target/database effects. Reject missing/ambiguous essential identity, bounds/hash failures or C:/D: free space below 40,000,000,000 bytes. Maximum decoded file 64MiB, one save at a time; no decoded blob is written.

Run from repository root: `python -B save-analysis/scripts/validate_mature_outposts.py --run <fresh-name>`. Outputs exclusively new ignored `.local-work/mature-save-validation/<fresh-name>/`: input before/after identities, closed/hash-frozen save-extraction before JSON content access, separate comparison, all controlled envelope/grammar results, shifted negatives and tool provenance. Same-region successor framing and byte-bounded grammar are separate gates; grammar-only false accepts are reported. Candidate windows and tag/name interpretation are empirical, not a universal parser or complete records. Final run `run-07`; failures/earlier freezes retained.

[test_mature_outposts.py](test_mature_outposts.py): six stdlib unittest methods with synthetic in-memory fixtures, count widths, all small-payload truncations, malformed framing/counts, zero keys and duplicates. Reads no saves, writes console only. Run `python -B -m unittest discover -s save-analysis/scripts -p test_mature_outposts.py -v`.

Local `independent_checks.py` separately reconstructs physical streams and mature count/reference steps; `corpus_challenge.py` independently consumes all controlled and two incidental payloads, tests mismatched framing and every mature truncation; neither alters inputs or the game. Local authoring/review helpers and their actual checks are inventoried in [validation.md](../../docs/experiments/mature-save-validation/validation.md). No automatic rerun, staging, publication or expanded analysis follows.

## Historical inventory and narrow location probes

[inventory_historical_saves.py](inventory_historical_saves.py) reads authorized Saves originals and existing archive identities; imports the project-owned mature directory/envelope/pool methods. Writes fresh ignored `.local-work/historical-inventory/<run>/` provenance, flushed/fsynced per-file receipts, complete local manifest and completion receipt. No original writes, game/database effects, decoded blobs, downloads or external dependencies. Bounds: 128 MiB physical input, 64 MiB decoded/full scan, first stream only for larger declared sizes, 128 MiB output guard, 1800-second cooperative loop bound, C:/D: each at least 40,000,000,000 bytes. `--resume` requires unchanged source/tool identities; do not reuse completed run names. Parser failure never proves corruption or absence. Reproduce with installed Python `-B save-analysis/scripts/inventory_historical_saves.py --run <fresh-name>`. Final recorded run is scan-04; earlier runs retained. [Results, source methods and limits](../../docs/experiments/historical-save-inventory-triage.md).

[probe_inventory_locations.py](probe_inventory_locations.py) reads a completed local inventory and one to five selected hash-verified authorized originals within the same resource limits; writes an exclusive local JSON. Uses known name-index links first, exploratory animation-predecessor fallback otherwise; index-subunit end +5 float triples remain local-position hypotheses. Never updates inventory classifications or writes decoded blobs. Recorded command: `-B save-analysis/scripts/probe_inventory_locations.py --run scan-04 --ids HIST-0267,HIST-0268,HIST-0259,HIST-0250 --output location-final.json`. Later fresh outputs need fresh filenames; paths/hashes in a new inventory determine its applicable IDs. No planetary-coordinate claim.

[test_historical_inventory.py](test_historical_inventory.py) runs ten synthetic stdlib tests for framing/EOF/checksum/output bounds, header version scope, empty-collection positives, absence gates, residual markers, window prefixes, low-disk stops and variable-index location probes. No proprietary fixture or game/save I/O. Run `-B -m unittest discover -s save-analysis/scripts -p test_historical_inventory.py -v`. Tool and test identities, local copy/control/summary authoring commands and complete review export are retained in the local review receipts.

## Supplemental launch-era corpus

[inventory_launch_corpus.py](inventory_launch_corpus.py), SOR-EXP-0008, reads only the operator-named archive, installed 7z and project parsers. Lists/validates <=256 members, <=4GiB expanded total, <=128MiB/file; extracts exclusively into ignored donor storage. Maintains C:/D: 40,000,000,000-byte free-space guard, 300-second extraction deadline, 64MiB per-save decoded limit, 128MiB receipt limit and 1800-second cooperative scan bound. Hash/stat originals before/after, size/CRC-check every member, independently walk each relationship payload. No decoded blobs, target effects, network or dependencies. Fresh run: `python -B save-analysis/scripts/inventory_launch_corpus.py --run <fresh-name>`. Existing extraction is never overwritten; `--reuse-extracted` revalidates the preserved member set/content in a fresh run. Final run scan-03; initial accounting failure retained. Exact paths and limitations: [report](../../docs/experiments/launch-era-third-party-save-corpus.md).

[summarize_launch_corpus.py](summarize_launch_corpus.py) reads the frozen scan-03, writes exclusively new numeric review CSVs under docs and one ignored audit receipt. Independently checks five selected saves' physical stream lengths/checksums/alignment/EOF/decoded hashes, directory/table closure, strings and grammar. Refuses existing output directory; do not rerun over review outputs. Source identity checked before/after. No raw strings/locators/payload emitted. Tooling hashes retained in final validation receipt.

[test_launch_corpus.py](test_launch_corpus.py): four synthetic unittest methods cover unsafe member paths/attributes/links/sizes, casefold collisions, detection gates and independent grammar truncation/tag/consumption failures. No game fixtures/I/O. Run `python -B -m unittest discover -s save-analysis/scripts -p test_launch_corpus.py -v`; run historical/mature suites for imported methods. All source raw material remains local and no publication/commit authority follows.


## Conservative membership follow-up

[outpost_membership.py](outpost_membership.py) accepts decoded bytes and an explicit conditional definition catalog, frames R3, tests inline bases and returns R1 template-adjacency leads. Conditional REFR cases4–7 track separate queues/body cursors, omitted flags stay unknown, and supported leading extras stop at unknown/versioned payloads. All current semantic results are INDETERMINATE; no complete player-ownership/absence claim. [Report](../../docs/experiments/active-outpost-membership-completion.md) gives exact scope and reason codes.

[inspect_outpost_definitions.py](inspect_outpost_definitions.py) reads two explicit installed ESMs, bounded group/record/subrecords and compressed payloads, verifies source hashes before/after, writes exclusive ignored definition JSON. No xEdit, target or database effects; no override merger or historical-equivalence guarantee. Run `python -B save-analysis/scripts/inspect_outpost_definitions.py --run <fresh> --data <installed-Data-path>`.

[challenge_outpost_membership.py](challenge_outpost_membership.py) reads frozen sample identity manifests and verified ignored copies; archives missing copies once by hash, never modifies originals. Writes fresh ignored features/preservation/tool receipts; ≤128MiB physical/64MiB decoded, C/D40GB guards and final cooperative1800s bound. Run `--run <fresh> --definitions <definitions.json>`; optional `--labels` selects identity labels outside classifier logic. Conditional regex plugin sequence is not full load remapping. Prior outcome labels, outpost names and JSON are never classifier inputs. No decoded blobs, network, dependency, live action or source-save writes.

[test_outpost_membership.py](test_outpost_membership.py) has nine synthetic regression methods for token domains/bounds, four conditional initial cases, omitted flags, disabled/deleted separation, transform/self validation, promoted player-reference decoys, extra version/array/boundary stops and ESM subrecord bounds. `python -B save-analysis/scripts/test_outpost_membership.py`. Tests establish parser behavior, not membership semantics.
