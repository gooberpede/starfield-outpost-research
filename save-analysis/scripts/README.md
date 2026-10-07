# Offline Analysis Scripts

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
