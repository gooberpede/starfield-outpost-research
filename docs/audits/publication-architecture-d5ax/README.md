# D5AX publication architecture audit

Publication remains **NOT READY / NOT CLEARED**. This package describes the frozen candidate tree and proposes later work. Start with the [report](report.md), then use the relevant dataset.

| Question | Reading path | Data |
| --- | --- | --- |
| Q1 | [Link and history analysis](link-analysis.md) | [Path census](tracked-inventory.csv), [reference inventory](reference-inventory.csv), [ref boundary](ref-boundary.csv), [history indicators](history-indicators.csv) |
| Q2 | [Evidence access](evidence-access.md) | [Claim dependency graph](claim-evidence-dependencies.csv) |
| Q3 | [Reader architecture](architecture.md), [archive plan](archive-plan.md) | [Member inventory](archive-members.csv), [inbound counts](archive-inbound.csv) |
| Q4 | [Migration and release decisions](migration-plan.md) | [Investigation ledger](ledger.md), [review](review.md), [acceptance](acceptance.csv) |

The reference inventory is a grouped detection ledger. Its count column preserves multiplicity. Use the source path and first-line coordinate to see the original context. Some locators contain machine-local provenance and some rows represent proposed routes. The inventories themselves require a B6 disclosure decision. No route in this package changes the authority of historical material.
