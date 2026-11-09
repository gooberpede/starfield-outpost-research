# Checkpoint and evidence inventory

Local `main` and the local upstream-tracking ref both pointed to
`0009caec62b2303670e8f6d2f074652bcdfa967e`, tree
`a1a6aa639d43d4a73085d87e2b7ce00f55172083`, parent
`2b7c7c0ebb125e5845c59e7f260a096c3e7959e9`. Git reported +0/−0 against
the local ref. Remote sync is maintainer-reported. The snapshot has 3,976
index entries and no staged or tracked working-tree differences. The only
pre-existing untracked path was the supplied D5BK brief, SHA-256
`3d745bf0f642f12f2507f4aa4620cb772122620cbe6243521950cee830587647`.
The index SHA-256 was
`bcb85094fa2a62b0d143fb7b333ed71327b58daa9886bde319b88f6edd6bc173`.

The checkpoint commit combines the bounded D5BJ final02 delivery (23 paths
including its supplied brief) with five new continuation methods. All five
prior entrypoint hashes match final02 and the later retained isolation
receipt. All 23 final02 file hashes match the committed blobs. The later
isolation receipt's ten method hashes match its retained
export. Eight of those ten match HEAD. The two exceptions are
`d5bj_preparation.py` and `d5bj_continuation.py`. The commit message describes
a recovery checkpoint. Its object tree does not preserve ignored evidence.

## Local-only custody

The private inventory and reproducible data-only reader are in the new ignored
`.local-work/d5bk-audit01/` directory as `inventory.json` and `inventory.py`.
The reader hashes the exact committed blobs and worktree counterparts, reads
scoped files as bytes and parses selected JSON. It writes a new inventory with
exclusive creation and neither imports project code nor opens game files.
Initial Git index entries and porcelain status are also retained there.
Each inventory entry carries a repo-relative locator, byte count, UTC mtime and
SHA-256. Times describe the retained filesystem metadata.
The inventory covers 286 files across the scoped namespaces below. It includes
the original candidate archives and staged copies as separate objects.

| Local family | Retained evidence and limits |
| --- | --- |
| `d5bj/continue01` | Development outputs, companion stderr, `model_compare.py` and `diagnose.py`. The latter is historical code for inspection only. Empty stdout with diagnostic stderr is preserved for early component, preparation and map attempts. |
| `d5bj/continued-isolated01` | 24 command records, 48 matching stdout/stderr hashes, staged-input pins and ten exported method hashes. There are 13 exit-zero rows, ten exit-one refusals and one exit-two CLI refusal. The export's recorded base HEAD is the parent of the current commit. The receipt checks a scoped set of originals and its own source/input inventories. |
| `d5bj/isolated04`, `final02`, `independent-review-final0{1,2}.md` | Prior isolated streams, patch manifest and independent REWORK returns. Final02 manifest is `cb56718f9cd06a9aaae8e6bd07715b160811166d92e7a00ec576b4159c8cfce1`. Earlier drafts, iterations and seven D5BJ-related diffs remain local. |
| `review-patches/d5bj-*` | Retained source-export directories and staged candidates/negative controls where present. The ten cited exported method files are checked individually. The wider exported tree is identified by the original receipt's 3,969-source before/after comparison. |
| D5AQ / D5AS / D5BI | Selected D5AQ input, historical replay, census, geometry and review receipts and both local candidate ZIPs are present. Both ZIPs match the expected hashes in the [reader guide](../evidence-reproduction-d5bj/README.md#supply-these-files). [Accepted D5AQ inventory](../../experiments/resource-retained-population/d5aq-native-dependency-inventory.md) · [D5AS asset](../evidence-access-d5be/d5as.md) · [D5BI candidate](../evidence-derivative-d5bi/manifest.json) |

The bounded inventory covers the task-local files, named receipt dependencies,
staged assets and historical patches. It excludes unrelated local material,
raw saves and full analysis/export databases. A source-bound later receipt or
exact-final review for the last two edits was not located. No final-run stderr,
exit code or method hash is inferred for those edits. A late development patch
is a candidate source artifact. Its existence supplies no run provenance.

## Reconstructed source history

Complete visible chat file-change hunks apply exactly to the retained isolated
source. Text-only reconstruction in memory checks each old line and context,
hunk position and count. The final result for each file equals the committed
blob byte for byte. The local, data-only reconstruction script and the selected
visible hunks are preserved under `.local-work/d5bk-audit01/`. No reconstructed
fixture source was written or executed.

| Method and stage | SHA-256 |
| --- | --- |
| Preparation, older isolated source associated with the 06-equivalent output | `aa584787083d56b196afa340b533347d605bd77aeb3e5494705475245dda12a8` |
| Preparation, reconstructed source before the visible 07 command, 14,193 bytes | `578b7162dfca6bed601987f4097fcfcf05563efe002f7dc9ec660d0352a42028` |
| Preparation, final edit matching committed source | `3d9cf72221cf14cae3fa69df80d04defe96b9af211427c17ac113ce408841371` |
| Continuation, older isolated source | `8849e3a5e0f2af1b6baec444bc02e24af4bb2570d90f4dca88563dc328e9a2aa` |
| Continuation, reconstructed intermediate requiring the post-receiver observation | `e8fa945823957729613eab3070b1eb45898f7d97c55e5ff75d6f047d6fb366e3` |
| Continuation, final edit requiring the native layer-producer result and matching committed source | `fece3c4d2c995cdee7e80d356a1a4cedf236398c30d89babca077f2d40d80a84` |

The 07 intermediate is a derived source identity from chronology and exact
text. The original execution receipt contains no source-at-execution hash.

Preserve the original streams, failed attempts, source snapshots, receipts,
staged and original candidate archives, historical patches and retained chat
locally. Use the inventory for a later separately authorized private backup and
verify its bytes against these pins before relying on it. Keep distinct
snapshots and their matching receipts together. The audit copied or moved no
originals. Neither this inventory nor Git constitutes a verified second copy.

## Key original outputs

Locators below are relative to ignored `.local-work/d5bj/`. Empty companion
stderr for the six development success records has the standard empty-file
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The receipt binds the isolated pair hashes separately.

| Locator | Bytes | SHA-256 |
| --- | ---: | --- |
| `continue01/components05.json` | 585 | `2f3a584fe16dead94a1e4b466cd6ffac940026f8f7e6f4d6347fb9fab4d146ee` |
| `continue01/model-comparison.json` | 888 | `024634d1c0a63d387580bb2bf1aea968e8ffdcee04c4cb49ca75ab30acefa160` |
| `continue01/preparation06.json` | 459 | `2f2c7a6b80d2ad259f88b568fdecd1974d24b473fc82f0d16e5837de4ea04ea3` |
| `continue01/preparation07.json` | 545 | `7b9930019d82240ba36188865980728a26cb2dd351b6fa39790597252febd7e9` |
| `continue01/workers04.json` | 280 | `c4361daf6499e0b27727f2baa7a889e3330dbbd59e181189139e9fd3b263ceb0` |
| `continue01/first_miss03.json` | 372 | `9779fd5b0df39aab1570e7799baeed2cbf8a641c1eae4bb68994526e2be58501` |
| `continued-isolated01/receipt.json` | 21694 | `0b176dd905f2a6c5a3a274fd8a4315c0cfbcacf685cae655af757a2b43974747` |
| `continued-isolated01/continuation.stdout` | 757 | `0e95d639225b5dec0dd7fe5e4607c4666f3745973c2a276db263bf8bb5ba0199` |

## Committed paths

The snapshot has 28 changed paths relative to its parent. SHA-256 below
identifies raw Git blob bytes at HEAD.

| Path | SHA-256 |
| --- | --- |
| `CREDITS.md` | `6e8e67e6661f106d733eabe094c88d124801658a0f47198c129ec9f18916805c` |
| `README.md` | `a4f9f72981656d67d4480db9dd24afd02443b835e01178427d69152242b66c3b` |
| `docs/DECISIONS.md` | `d022e88afa2ad2ecb723b4e482fb54818d29788b13a0ad90ce2e1ddfc1da2090` |
| `docs/PUBLICATION.md` | `7084faf89d5fa087c9bb4086a565150d458397eccb7f052f952a69f956a52af5` |
| `docs/PUBLICATION_RUN_CARD.md` | `dd3be2f54995dee4fee2255ce3d01b1692221829c6e86aecf9e21830b2f8b09d` |
| `docs/RESEARCH_STATE.md` | `4f04ce98bf881754d690b01fbfd4aed7d6a5122f0a3068e587c797c600cc9024` |
| `docs/SOURCES.md` | `204bd5f44f408a3ddd0205bfb6fa592519f389ab67be54771c66ecc9c49b8d50` |
| `docs/audits/evidence-reproduction-d5bj/README.md` | `b8745a213984d63ecec576182fa9807f28b8aecfb43a0cd6e8ee486682683543` |
| `docs/audits/evidence-reproduction-d5bj/continuations.md` | `c3f76efec0fbcbc5572019b271ea44d3ec24b05977ae2ac3fb5385c31cacc1a5` |
| `docs/audits/evidence-reproduction-d5bj/dependencies.md` | `2a8de673dc37855cedc3b2017283653736af953686296915c674a2b764e3a64b` |
| `docs/audits/evidence-reproduction-d5bj/investigation-ledger.md` | `9db2af3b5ef6ae33f61c88bb5da87a9473d24ebef1e809e66cb762b82f4a9781` |
| `docs/audits/evidence-reproduction-d5bj/qualification.md` | `0d7b092c7f4ae44b92f745c95a27333c009c75f0773d0507b78b400f9684c71e` |
| `docs/audits/evidence-reproduction-d5bj/reading.md` | `74a8f33f5cbb32aeb25e9370e4cdbdefa0379b8524248322a6010ab589ed5a47` |
| `docs/audits/publication-claims-d5bg/actions.json` | `b15c69c9a6f0bacfee35c8e7c07c2e7a50723b0c36e0fdf23f2e0267beab227c` |
| `docs/audits/publication-claims-d5bg/claims.json` | `d8e81b76a06e6955f1833a12b773210da5a0bbc9f040a4a67fac2fb0c9bc43eb` |
| `docs/audits/publication-claims-d5bg/evidence-edges.json` | `f484393a42982e2c1eb2c6108be1b2a825285f2504cc1d94dfc6bd51c3dedee3` |
| `docs/audits/publication-claims-d5bg/handoff.md` | `0bb2ee9caee4a890353da7ab99c2ed0de9f2daec210436aa7aedc0dc44656cb2` |
| `docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BJ_D5AQ_Native_Fixture_Public_Reproduction.md` | `93f2c1ef9c2a8ba37329f998755e06fb49c0d28a3c57d40747e5fb40c1ec6b84` |
| `research/resource-retained-population/d5bj_components.py` | `35238cc17e85fe2d1ab6ed24865037c431bf98c28fd3efd2b39a162daa4edf58` |
| `research/resource-retained-population/d5bj_continuation.py` | `fece3c4d2c995cdee7e80d356a1a4cedf236398c30d89babca077f2d40d80a84` |
| `research/resource-retained-population/d5bj_dispatch.py` | `075aedd84838bba344f35edf111375857876e1748503a73ca1e012104c0394fd` |
| `research/resource-retained-population/d5bj_first_miss.py` | `254fcb0e907b0dacd7318a2b6eff687e64c8caa001980e2f5b014fac16f4da96` |
| `research/resource-retained-population/d5bj_geometry.py` | `cdd9f268751bc9e99a7b6f549d3d6f05cb65fd053fee070cb1088fc6b89a97b3` |
| `research/resource-retained-population/d5bj_n2.py` | `78ffd375054a38fd9d1a818cb08635299a5561055d30ec2ffa91703e27888db7` |
| `research/resource-retained-population/d5bj_preparation.py` | `3d9cf72221cf14cae3fa69df80d04defe96b9af211427c17ac113ce408841371` |
| `research/resource-retained-population/d5bj_sampler.py` | `ffb9b40e85d48489b15493fc4db2635c2e9341e7f12813ead3b7c0268db46631` |
| `research/resource-retained-population/d5bj_sources.py` | `0c9a6a7c87df3c39296654046ba281fc5c9da008f83611e0480e4a6c3ebe9fb6` |
| `research/resource-retained-population/d5bj_workers.py` | `02b690bb81f7d948be0ad33267b3d9f5d87a9c1fab02afa1d2d5e2ba061294db` |
