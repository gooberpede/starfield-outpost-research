# Approved native-oracle 0.2.0 notice-path correction

2026-10-12. SOR-EXP-0031 / SOR-EV-0039. **APPROVED and adopted.**
The maintainer explicitly approved the proposed notice-path correction and asked
Codex to record it, rerun preflight and give launch go-ahead only if all checks pass.
No staging, commit or push is authorized.

This addendum corrects only the deployed notice paths in the approved
[0.2.0 run card](continuation-020-run-card.md). Preserve that exact reviewed card,
ZIP, DLL/config and release lock without modification. Vortex deployed the runtime
files at their reviewed Data/SFSE/Plugins paths and placed the three notice files
under Data/ResearchNotices. Their contents match the reviewed package hashes.

Accepted installed paths relative to the Starfield game directory:

| Installed notice path | Mandatory SHA256 |
|---|---|
| Data/ResearchNotices/PROJECT-LICENSE.txt | 3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986 |
| Data/ResearchNotices/READ-ME.txt | 4f863b8a425673a5ecb3b1c744e3b8787e687f9193c4eb6adf695d4dfd609064 |
| Data/ResearchNotices/SFSE-PluginAPI-LICENSE.txt | 7795510c3ee9970b5843639d79b7ab6d87d1a14a1e110e92fd0b09ff0e7628da |

Preflight accepts these actual notice-only paths rather than requiring game-root
ResearchNotices. Postflight checks removal at these paths and any game-root
counterparts if present. No file movement, reinstall, binary/source/configuration
change or weakened native safety guard follows. The approved controls and
conditional N1, overlays, protected inputs, finite bounds and health/admission/stop
rules remain as reviewed. User launches via Vortex sfse_loader.exe and remains at
the main menu until runtime admission and a fresh durable nonce ACK pass.

The original blocked supplement and proposed correction remain retained under
`.local-work/native-oracle-020/operations/`. Fresh authorization and preflight
receipts are separate files; no prior failure is overwritten or relabelled.
All35 automated runtime checks plus the corrected five-member deployment check
must pass before launch release. Preflight is file/process metadata verification,
not proof of future runtime reachability or native equivalence.
