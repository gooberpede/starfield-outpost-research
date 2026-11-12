# Historical audits and reviews

Edition **D5BZ-2**, 2026-11-12 (Australia/Sydney), preserves 350 exact
original files with their full repository-relative paths. Publication is
**NOT READY / NOT CLEARED**.

Start with the [guides](../guides/README.md) for player questions, the
[technical references](../reference/README.md) for current findings and
verification, or [research history](../history/README.md) for negative and
superseded results. The [research identifier index](../history/research-identifiers.md)
and [claim and evidence-route lookups](../history/README.md) lead to primary
scientific sources. The [archive verification record](../archive-verification.md#d5bz-2-audit-update)
records edition integrity and custody.

## Archive lookup

Open the [member CSV](archive-index.csv) for exact paths in alphabetical
order. Filter its topic, record ID and historical status columns, or search
from the repository root with Python 3.14:

```text
python -B research/archival/archive.py search docs/audits/archive-index.csv D5BZ
```

Use a case-sensitive path from the CSV to retrieve a member of
[audits.zip](audits.zip). For example:

`audits.zip :: docs/audits/documentation-synthesis-d5by/review.md`

A fragment in a historical citation identifies a heading inside the recovered
document. Use the member path up to the fragment when locating it in the CSV.
Dates and dispositions reflect identifiable historical metadata. Blank fields
leave identification to the original record. Exact bytes and the pre-migration
Git blob identify different representations when line endings differ. Files
with a current replacement have a separate active path in the CSV.

## Safe extraction

Keep the ZIP and CSV together and use a fresh, caller-owned output directory.
The verifier checks the complete member inventory, names, metadata and SHA-256
before writing each file. It checks the extracted bytes again.

```text
python -B research/archival/archive.py verify docs/audits audits --extract NEW_DIRECTORY
```

Historical commands, links, machine paths, permissions and verdicts describe
their original revisions. Use the [current evidence access contract](../reference/evidence-access.md)
for supported reader instructions. Historical Git revisions remain available
through the repository history.

## Subject groups

| Subject to filter in the CSV | Members |
| --- | ---: |
| Other historical records | 41 |
| Position, coordinates and world state | 1 |
| Production, power and logistics | 4 |
| Publication, evidence access and repository governance | 264 |
| Resource generation and observation | 4 |
| Save research and experiment methods | 22 |
| Workshop, construction and membership | 14 |

## Audit packages

| Audit subject or package | Members |
| --- | ---: |
| Standalone audit records | 21 |
| archival-d5bz | 6 |
| d5bj-interruption-d5bk | 8 |
| d5bj-preservation-d5bl | 8 |
| d5bm-completion-eligibility | 10 |
| d5bm-deferred-d5bn | 9 |
| deferred-work-d5aw | 8 |
| documentation-synthesis-d5by | 14 |
| evidence-access-d5be | 8 |
| evidence-access-d5bx | 9 |
| evidence-closure-d5bv | 6 |
| evidence-derivative-d5bh | 5 |
| evidence-derivative-d5bi | 9 |
| evidence-distribution-d5bw | 9 |
| evidence-readiness-d5br | 6 |
| evidence-reproduction-d5bj | 6 |
| foundation-d5az | 2 |
| logistics-guides-d5bb | 2 |
| native-function-catalogue-d5bd | 7 |
| native-function-catalogue-d5bs | 3 |
| original-save-verification-d5bu | 11 |
| outpost-coverage-2026-10 | 7 |
| outpost-rc1-2026-10 | 8 |
| production-guides-d5ba | 3 |
| public-evidence-d5bo | 10 |
| publication-architecture-d5ax | 18 |
| publication-claims-d5bg | 8 |
| publication-decisions-d5bp | 2 |
| publication-decisions-d5bq | 2 |
| publication-readiness-b0 | 7 |
| publication-readiness-b1 | 6 |
| publication-readiness-b2 | 21 |
| publication-readiness-b3 | 13 |
| publication-readiness-b4 | 18 |
| publication-readiness-b5 | 17 |
| publication-readiness-rr1 | 15 |
| reader-pilot-d5ay | 4 |
| reader-qualification-d5bt | 4 |
| release-assets-d5bf | 2 |
| release-candidate-audit-d5ca | 15 |
| remaining-guides-d5bc | 3 |
