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
