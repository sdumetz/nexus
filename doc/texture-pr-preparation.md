# Implementation and experiment commit separation

`decoupled_textures-code` is a PR-ready branch based on `1fe489d` (`v4-fixes`).
Its six commits contain only `src/` and `tests/` changes:

| Commit | Implementation |
|---|---|
| `15b10d7` | Round 1: combined geometric/texel error |
| `da84e7a` | Round 2: size textures against geometric error |
| `fd4c483` | Round 3: finer dimensions in multiples of four |
| `93fe9b7` | Round 4: baked-atlas reconstruction-loss metric |
| `77e96e9` | Always use reconstruction; expose factor defaulting to 2 (initial direction) |
| `fbe7536` | Correct factor semantics: tighten sizing and refinement at 2 |

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
**allowed texture tolerance** for sizing and multiplies the reported texture
contribution before combining it with geometric error. Larger values tighten
precision and retain more texture detail; smaller values relax it. Factor 1
preserves the original round 4 behavior. There is no metric mode switch. Ratio
0 still preserves baked dimensions but continues to compute weighted error.

The initial factor direction in `159d1ea` was corrected separately in
`c4f83f2`; source-only branch commit `fbe7536` contains that correction.

Previous benchmark CSVs and screenshots measure original round 4 (factor 1).
The new corrected factor-2 benchmark is in `doc/measurements/isti-precision-10`.
Measurements and tooling stay on the experiment branch in separate commits.
Current benchmark tooling records the tuning semantics and factor in its
manifest and scratch configuration. Historical footprint comparisons use the
historical revisions identified in their reports.

The subsequent upstream quality calibration is in
`doc/measurements/isti-quality-2px-10`. At requested screen-space error 2 px,
factor 1.5 is the lowest tested common value that passes the source-quality and
detail-retention checks across ten fixed views. Its total audited cache saving
is 34.58%, while the median model uses 71.27% more cache because quality
overshoots upstream on several models. Per-model calibration gives 58.72% total
saving. These are benchmark settings; the production default remains 2.
