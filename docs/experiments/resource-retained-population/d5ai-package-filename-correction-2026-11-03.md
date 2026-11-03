# D5AI Vortex package filename correction

2026-11-03, Australia/Sydney. Packaging-only addendum to the reviewed D5AI
handoff; no native rebuild, implementation, prediction or run-card change.

The maintainer requested a distinct versioned archive name to avoid a Vortex
collision and suggested `SorConstructionWinner-0.5.0.zip`. The qualified D5AI
plugin already identifies itself as version **0.7.0** (`0x00070000` in the
retained derived plugin source). The new install filename therefore matches
that existing version: `SorConstructionWinner-0.7.0.zip`.

Install archive: `.local-work/d5ai/vortex-package01/SorConstructionWinner-0.7.0.zip`.
It is a byte-identical copy of the retained build16
`SorConstructionWinner-D5X-review.zip`; the original is preserved so historical
build, freeze and handoff hashes remain valid. Both episode cards use this same
candidate. No source/binary version was changed merely to rename the archive.

Archive SHA-256:
`9b81fac5b62fc97ad2582dc48e9717d138643b6fa1a1e78fe8eb6912f31f830c`.
Contained DLL SHA-256:
`9df5a04ef770887b402dca7c61ee3af52f6046711fcd4e997b66922055bbe67c`.

Checks: exact archive-byte equality, ZIP CRC test, exact three-member inventory,
qualified DLL identity and both caller-available disk floors. The archive retains
`Data/SFSE/Plugins/SorConstructionWinner.dll`, `COPYING` and the existing SFSE
notice. No new third-party material is incorporated. The local receipt is
`.local-work/d5ai/vortex-package01/receipt.json`.

Run cards remain [Episode A](run-card-d5ai-episode-a.md) and
[Episode B](run-card-d5ai-episode-b.md), with the existing
[operator commands](d5ai-operator-commands.md). No deployment, installation,
gameplay, staging, commit or push was performed by this filename correction.
