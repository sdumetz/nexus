# Implementation and experiment commit separation

`decoupled_textures-code` is a PR-ready branch based on `1fe489d` (`v4-fixes`).
Its five commits contain only `src/` and `tests/` changes:

| Commit | Implementation |
|---|---|
| `15b10d7` | Round 1: combined geometric/texel error |
| `da84e7a` | Round 2: size textures against geometric error |
| `fd4c483` | Round 3: finer dimensions in multiples of four |
| `93fe9b7` | Round 4: baked-atlas reconstruction-loss metric |
| `77e96e9` | Always use reconstruction; expose divisor defaulting to 2 |

The branch's final source and tests match this experiment worktree exactly.
It contains no measurements, screenshots, experiment notes or benchmark tools.
The existing `decoupled_textures` history is preserved, including its earlier
mixed commits. Current implementation changes were committed separately as
`159d1ea`; subsequent notes and benchmark-tool updates use a separate commit.

A PR can use `decoupled_textures-code` directly, with `v4-fixes` as the base:

```sh
git diff 1fe489d..decoupled_textures-code --stat
git log --oneline 1fe489d..decoupled_textures-code
```

The tuning parameter is `--texture-error-divisor`, default 2. It divides the
loss-weighted texture contribution before combining it with geometric error.
Larger values relax refinement; smaller values tighten it. There is no metric
mode switch. Ratio 0 still preserves baked dimensions, but continues to compute
reconstruction error.

Previous benchmark CSVs and screenshots measure the original round 4 metric
(equivalent to divisor 1), not the new default. They remain frozen, with their
source and binary hashes. Current benchmark tooling records the divisor in its
manifest and scratch build configuration. Historical footprint comparisons must
use the historical builder and driver revisions identified in their reports.
