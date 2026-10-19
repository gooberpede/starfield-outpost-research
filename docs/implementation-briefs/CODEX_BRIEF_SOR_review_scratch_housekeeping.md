# Review scratch housekeeping

Authorized directly in chat on 2026-10-19: move the `D:/tools/sor*` directories
into `.local-work/review-patches/`, update current directory references, and
make reusable packaging scripts create their scratch trees there.

## Scope and completion

- Preserve every source directory name, file byte and empty subdirectory.
  Check resolved source/destination boundaries, refuse collisions and reparse
  points, and verify per-file SHA-256 inventories before and after moving.
- Update current documentation describing review scratch paths. Keep actual
  tool installation paths, supplied historical briefs, frozen snapshots,
  receipts, old patches and failed-run scripts unchanged.
- Update maintained exporters and reusable local packaging helpers. Create
  the ignored scratch parent explicitly before allocating a unique child.
  Bound Git discovery at `.local-work/` so nested scratch directories remain
  independent `git apply --no-index` targets while root Git reads still work.
- Record the uniform relocation convention and preserve historical locators.
  No full publication-readiness exercise or change in evidence classification.
- Check syntax and the changed scratch-allocation paths without executing
  historical exporters or experimental code. Export complete/task-only review
  diffs, manifests, exclusions and actual verification results.

Allowed writes: the requested moves, document/exporter edits, this brief and
ignored verification artifacts. Python standard library and read-only Git
inspection/patch checks suffice; no new dependency or third-party reuse.
No game/process, save, database, deployment, configuration, staging, commit,
push, network or publication action. Stop on an unexpected boundary, collision,
content mismatch or unrelated concurrent edit. Preserve originals/receipts.

Review remains separate from implementation completion. Any unavailable
independent review is disclosed; this task grants no integration authority.

## Relocation convention

On 2026-10-19 the existing `D:/tools/sor*` directories are relocated beneath
`D:/Projects/starfield-outpost-research/.local-work/review-patches/`, keeping
each directory name and its internal relative paths. For an old locator,
replace the leading `D:/tools/` with that new parent. Historical manifests,
patches and copied snapshots retain their original bytes and original paths.
This note documents relocation; it does not automatically redirect a path.

The `.local-work/diffs/` patch-export location is unchanged. Both local-work
areas remain ignored and local; moving material does not clear publication.
