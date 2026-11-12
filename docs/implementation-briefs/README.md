# Implementation briefs and amendments

Edition **D5BZ-2**, 2026-11-12 (Australia/Sydney), preserves 262 exact
original files with their full repository-relative paths. See the
[publication run card](../PUBLICATION_RUN_CARD.md) for current release status.

Start with the [guides](../guides/README.md) for player questions, the
[technical references](../reference/README.md) for current findings and
verification, or [research history](../history/README.md) for negative and
superseded results. The [research identifier index](../history/research-identifiers.md)
and [claim and evidence-route lookups](../history/README.md) lead to primary
scientific sources. The [archive verification record](../archive-verification.md#d5bz-2-brief-update)
records edition integrity and custody.

## Archive lookup

Open the [member CSV](archive-index.csv) for exact paths in alphabetical
order. Filter its topic, record ID and historical status columns, or search
from the repository root with Python 3.14:

```text
python -B research/archival/archive.py search docs/implementation-briefs/archive-index.csv D5BZ
```

Use a case-sensitive path from the CSV to retrieve a member of
[implementation-briefs.zip](implementation-briefs.zip). For example:

`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BZ_Comprehensive_Historical_Repository_Archival.md`

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
python -B research/archival/archive.py verify docs/implementation-briefs implementation-briefs --extract NEW_DIRECTORY
```

Historical commands, links, machine paths, permissions and verdicts describe
their original revisions. Use the [current evidence access contract](../reference/evidence-access.md)
for supported reader instructions. Historical Git revisions remain available
through the repository history.

## Subject groups

| Subject to filter in the CSV | Members |
| --- | ---: |
| Other historical records | 29 |
| Position, coordinates and world state | 6 |
| Production, power and logistics | 20 |
| Publication, evidence access and repository governance | 37 |
| Resource generation and observation | 90 |
| Save research and experiment methods | 26 |
| Workshop, construction and membership | 54 |

## Brief and amendment identifiers

| Identifier or subject | Members |
| --- | ---: |
| A1 | 2 |
| B0 | 1 |
| B1 | 2 |
| B2 | 2 |
| B3 | 1 |
| B4 | 2 |
| B5 | 1 |
| BM1 | 1 |
| BM2 | 1 |
| C1 | 2 |
| C1A | 1 |
| C1B | 1 |
| C1C | 1 |
| C1D | 1 |
| C1E | 1 |
| C1F | 1 |
| C1G | 1 |
| C1H | 1 |
| C2 | 2 |
| C2A | 1 |
| C2B | 2 |
| C2C | 1 |
| C2D | 1 |
| C3 | 1 |
| CR1 | 2 |
| CR2 | 1 |
| CR3 | 1 |
| D1 | 2 |
| D2 | 1 |
| D3 | 1 |
| D4 | 1 |
| D4A | 1 |
| D4B | 1 |
| D4C | 1 |
| D4D | 1 |
| D4E | 1 |
| D5 | 1 |
| D5A | 1 |
| D5AA | 1 |
| D5AB | 7 |
| D5AC | 1 |
| D5AD | 1 |
| D5AE | 1 |
| D5AF | 1 |
| D5AG | 1 |
| D5AH | 1 |
| D5AI | 2 |
| D5AJ | 1 |
| D5AK | 2 |
| D5AL | 2 |
| D5AM | 4 |
| D5AN | 1 |
| D5AO | 2 |
| D5AP | 1 |
| D5AQ | 1 |
| D5AR | 1 |
| D5AS | 1 |
| D5AT | 2 |
| D5AU | 1 |
| D5AV | 1 |
| D5AW | 1 |
| D5AX | 1 |
| D5AY | 1 |
| D5AZ | 1 |
| D5B | 1 |
| D5BA | 1 |
| D5BB | 1 |
| D5BC | 1 |
| D5BD | 1 |
| D5BE | 1 |
| D5BF | 1 |
| D5BG | 1 |
| D5BH | 1 |
| D5BI | 1 |
| D5BJ | 1 |
| D5BK | 1 |
| D5BL | 1 |
| D5BM | 1 |
| D5BN | 1 |
| D5BO | 1 |
| D5BP | 1 |
| D5BQ | 1 |
| D5BR | 1 |
| D5BS | 1 |
| D5BT | 1 |
| D5BU | 1 |
| D5BV | 1 |
| D5BW | 1 |
| D5BX | 1 |
| D5BY | 1 |
| D5BZ | 1 |
| D5C | 1 |
| D5CA | 1 |
| D5CB | 1 |
| D5CC | 1 |
| D5D | 1 |
| D5E | 1 |
| D5G | 1 |
| D5H | 1 |
| D5I | 1 |
| D5J | 1 |
| D5K | 1 |
| D5L | 1 |
| D5M | 1 |
| D5N | 1 |
| D5O | 1 |
| D5P | 4 |
| D5Q | 1 |
| D5R | 1 |
| D5S | 1 |
| D5T | 1 |
| D5U | 2 |
| D5V | 2 |
| D5W | 1 |
| D5X | 2 |
| D5Y | 1 |
| D5Z | 1 |
| DA1 | 1 |
| E1 | 5 |
| E2 | 1 |
| E3 | 1 |
| EXP0002A | 7 |
| L0 | 1 |
| L1 | 1 |
| L2 | 1 |
| L3 | 1 |
| LO1 | 1 |
| Other historical records | 16 |
| P1 | 6 |
| Position, coordinates and world state | 5 |
| Production, power and logistics | 2 |
| Publication, evidence access and repository governance | 13 |
| R1 | 1 |
| RC1 | 1 |
| RG1 | 1 |
| RG2 | 1 |
| RR1 | 1 |
| Resource generation and observation | 7 |
| S0 | 1 |
| S1 | 2 |
| S2 | 1 |
| SD1 | 1 |
| SD2 | 1 |
| SD3 | 1 |
| SOR-EXP-0002 | 1 |
| SOR-EXP-0002A | 1 |
| Save research and experiment methods | 9 |
| Workshop, construction and membership | 24 |
