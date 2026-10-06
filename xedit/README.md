# Bounded outpost reconnaissance reader

`SOR_OutpostRecon.pas` is original project code for the initial brief, targeting installed SF1Edit 4.1.5p x64. API documentation: [Tome of xEdit](https://tes5edit.github.io/docs/13-Scripting-Functions.html), source SOR-S-0103. No existing script was copied or adapted. Operator runs and limits are recorded below; no other version is qualified.

Input: selected records from a clean, completed `Starfield.esm` load (and required masters), using the signature and EditorID filters in `Process`. This is a vocabulary-led discovery sample, not a complete dependency graph. No winning-override assumption; each row identifies its source plugin. File FormIDs and session/load-order FormIDs are separate columns, neither a runtime pointer nor save identifier. String values are xEdit interpretations, not independently decoded bytes.

Output: timestamped `.tsv` and `-meta.txt` under the already-created repository `.local-work/recon/` directory. TSV columns are plugin, file FormID, session FormID, signature, EditorID, indexed element path, display value. Tabs/newlines in cells become spaces. TStringList output encoding is implementation-dependent; inspect bytes before normalizing. Metadata lists loaded plugins, reported tool version, counts and truncation flags. Retain both original files together. At most 3,000 record headers, 120 detailed records, 300 leaves per detail and depth 10; cap hits mean incomplete coverage, not absence. Selection order affects detailed coverage. The helper neither follows references recursively nor exports whole ESMs.

Effects: reads plugin records; writes only two export files; no setters, record creation/removal, plugin saves or configuration changes. xEdit itself may write ordinary logs/cache/UI preferences. Requires xEdit's script API and built-in Pascal runtime only; no new dependency. Abort on script errors, unexpected plugin modification prompt or wrong input. Never save plugin changes. Existing timestamp collision aborts rather than overwriting. Cleanup leaves exports local for inspection; installed helper may be removed after the session with owner approval.

## Operator procedure

1. Open `D:\tools\xEdit.4.1.5p\xSF1Edit64.exe` in Starfield mode, preferably with `-view -DontCacheSave`. Select only `Starfield.esm` plus automatically required masters and wait for background loading to finish. Do not load the experimental ESP or use a cleaning mode.
2. Select the `Starfield.esm` root in the left tree; right-click **Apply Script** (not **Apply Script Into**); choose `SOR_OutpostRecon`.
3. After completion, retain the Messages output and tell Codex the two output filenames. Codex can read them locally; uploading is unnecessary. If an error occurs, provide the exact error; do not edit/save a plugin to work around it.
4. Close without saving plugin changes. Script success requires inspecting both outputs, not just the completion message.

Headless limitation: the consulted xEdit overview describes graphical operation and command-line configuration but did not establish a fully unattended Starfield extraction route. No speculative command-line launch or alternate unapproved parser was used. The user's explicit interactive fallback applies; this is not a claim that headless xEdit is impossible.

## Focused second pass

`SOR_OutpostFocus.pas` shares the original reader logic but replaces the vocabulary match with an explicit 20-name allowlist from the first result, includes COBJ details and allows 800 leaves per selected definition (depth still 10). Output prefix is `xedit-focus-`; the same read-only/encoding/identity caveats apply. Select the Starfield.esm root and Apply Script → SOR_OutpostFocus. It does not resolve arbitrary dependencies or write plugin records.

Actual first run: the initial missing `end.` unit terminator caused an xEdit parser error. Corrected source hash `3c072b34316c3eca74a28ec5290302687f4e270225dcc6a81a3fcd9f7bb212a7` ran successfully per operator, scanning 3,829,247 records in 1:43. Output contains 1,743 matched record headers from 54,855 signature-eligible records, 120 detailed records and a detail-cap flag. Detail fell entirely in AVIF/FLST due to selection order; this motivated the focused pass, not a broader dump. The first scan's unselected/missing records cannot establish absence.

Focused run: operator reported successful completion in 1:39 over the same traversal. Both files were inspected: 15 matched/detailed definitions, no truncation flags. Five CK-name guesses did not match actual EditorIDs; their absence is not a missing-concept finding. Source SHA-256 `6b21e33de6bf1d63b05de686077590bffeaf401497a45b3b87fb52f9e3696345`. Installed copies match repository scripts. Starfield.esm SHA-256 unchanged before/after both runs. No third-party parser used for independent decoder validation.
