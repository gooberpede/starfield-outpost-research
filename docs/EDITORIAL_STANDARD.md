# Editorial finalization standard

Prospective requirement for every substantive Codex research, implementation and
audit delivery. This standard governs presentation and evidence qualifications;
it grants no execution, integration or publication authority. Existing frozen
contracts and historical evidence remain intact.

## Coverage and readable prose

Review the entire changed human-authored prose set: Markdown headings, tables,
captions, explanatory comments and docstrings, CSV labels and summaries, and
edits to existing documents. Generated numeric data needs schema/label and claim
review; opaque hashes, symbols, machine identifiers and quoted source bytes need
identity checks rather than stylistic rewriting. Do not bulk-clean legacy text.

Find joined words/numbers, missing punctuation spaces, concatenated lines,
replacement characters/mojibake, malformed Markdown and broken local evidence
links. Read sentences and tables in context: syntactic validity cannot establish
comprehensibility. Prefer complete sentences to compressed symbol chains.

## Proportionate technical notation

Normally prefix memory VAs/RVAs, member/byte offsets, bit patterns and FormIDs
with `0x`. Use decimal for counts, PIDs, thread IDs, source-grid coordinates and
displayed floating-point measurements. Give units, frames, byte order, owning
objects and source identity where ambiguity would change interpretation.
Familiar notation needs no redundant decimal tags or mechanical conversions.

Distinguish preferred static VA from relocated runtime VA; offset from address;
source ordinal from stable identity; FormID from saved token, handle or pointer;
and probability from percentage or multiplier. Literal symbols such as `Save52`,
`XMM3`, `FUN_14079b520` and filenames retain their spelling.

## Scientific semantics

Editorial correction must preserve evidence strength and coverage. DERIVED,
STATIC and PREDICTION cannot become OBSERVED through rewording. Generation
attempts differ from surviving paths; cache pointers do not establish epochs;
source, terrain and beacon biomes are distinct. Keep terminology consistent
across summaries and detailed tables, with the same traceable qualifications.
Unsupported certainty is a scientific defect and requires REWORK.

## Mandatory sequence and independent enforcement

1. Finish the investigation, implementation and relevant tests.
2. Run the [bounded screen](../research/editorial/screen.py) on changed authored
   text: `python -B research/editorial/screen.py --changed`. Retain diagnostics
   and inventory locally. Investigate every suspect; never automatically rewrite.
3. Actually read every changed prose file, including changed tables, labels and
   explanatory source text. Correct defects and rerun affected checks.
4. Obtain independent review of the exact final changed prose and material
   scientific qualifications under the [reviewer procedure](reviewers/research-completion-reviewer.md).
   Material defects yield REWORK of the same assignment.
5. Verify delivery diffs/manifests against that reviewed snapshot. A substantive
   later edit needs relevant independent delta review. A small self-describing
   review-record closure may receive delta review without repeating the science.

Retain a concise compliance record: screened files/snapshot, manual coverage,
findings and corrections, exceptions with rationale, tool limits and independent
disposition. Missing mandatory review blocks accepted completion. Reviewer
acceptance is distinct from maintainer integration and publication approval.

## Bounded screen and exceptions

The original stdlib checker scans added lines of changed existing files and all
eligible new Markdown/CSV files plus Python comments/docstrings. It skips raw
evidence directories, code fences, inline symbols and opaque data. Explicit
file mode is available for a full authored file. Diagnostics name file, line,
rule and severity; a nonzero exit means suspects remain, not automatic proof
of a defect. [Fixtures](../research/editorial/fixtures.json) include valid
technical notation and deliberately defective prose.

Use an inline `editorial: allow RULE -- rationale` annotation only for a
documented legitimate occurrence; include it in the compliance record. Code-span
exclusion protects identifiers, but must not be used to hide malformed prose.
The screen cannot detect every concatenation, malformed table, scientific
overstatement or semantic link error. Manual and independent reading remain
mandatory even when it reports zero diagnostics.
