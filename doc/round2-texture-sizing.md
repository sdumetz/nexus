# Round 2: size textures from geometric error

This describes a historical experiment. The current builder always uses
[round 4 reconstruction error](round4-reconstruction-error.md), at precision factor 2
by default; ratio 0 now preserves sizes without reverting the error metric.

The default texture error ratio is **1**. At export, choose the coarsest
successive halving of the baked image whose world-space texel error does not
exceed the node's geometric error. Recompute texel error at every candidate
dimension, using the round 1 metric. Never upscale an image that is already
texture-dominated. If the geometric target is zero, preserve the original size.

First propagate geometric error alone from children to parents, using the
existing 1.01 ancestor margin. This gives a final root with zero local error a
useful inherited target. Texture errors must not contribute to this sizing
target: doing so would allow texture reduction to justify further reduction.
After choosing dimensions, store the maximum of this geometric term and the
new texel error, then apply the existing combined-error/bounds saturation pass.

Downsampling uses Qt's smooth image scaling before JPEG encoding. Geometry,
UVs, baked images, and hierarchy construction are unaffected; the export only
changes texture payloads, texture offsets, and node errors. The Nexus container
version and record layouts remain unchanged, and no viewer changes are needed.
This reduces exported texture sizes and potential viewer residency, but does
not reduce intermediate baking work or memory.

The CLI option is:

```sh
nxsbuild model.obj --texture-error-ratio 1
nxsbuild model.obj --texture-error-ratio 0   # round 1 control: retain baked sizes
nxsbuild model.obj --texture-error-ratio 0.5 # keep texture detail one step sharper
```

Positive ratios multiply the saturated geometric error to produce the sizing
target. Zero explicitly disables resizing and preserves the round 1 local-error
combination. Negative, nonfinite, and nonnumeric values are rejected. The CLI
still has its pre-existing hardcoded `test.nxs` output behavior; run comparisons
in separate directories. `-V verbose` logs original/exported dimensions, the
texture target, both error terms, and their maximum before final saturation.

## Validation and limits

Run `python3 tests/run_round1.py /path/to/nxsbuild-build-directory` after building.
The suite retains the round 1 checks and tests default ratio 1, ratio 0.5, and
the disabled control. On a known two-level hierarchy, 256x256 textures become
32x32 at ratio 1 and 64x64 at ratio 0.5 where geometry dominates; the
texture-dominated node stays 256x256. The selected resolutions meet the target
and the next coarser dimensions exceed it. Tests decode the actual JPEGs, check
their gradient/orientation, compare actual geometry/UV payloads across exports,
and verify that baked dimensions are not mutated. A zero-error hierarchy keeps
all its original dimensions. Geometry-only exports also retain their errors.

A Release build and the suite passed. Full CLI builds of a 512-triangle planar
grid with a 128x128 source PNG produced:

| Mode | Exported node textures | Stored base texels | File bytes |
|---|---|---:|---:|
| Ratio 0 | 3 x 32x32, 2 x 64x64 | 11,264 | 32,512 |
| Ratio 1 | 3 x 16x16, 2 x 64x64 | 8,960 | 32,512 |

This smoke case removes 20.5% of base texels. Its small JPEGs still occupy the
same 256-byte padded ranges, so file size does not decrease. This is a functional
check, not a real-model quality, transfer, or GPU-memory benchmark. Invalid CLI
ratios were also tested and rejected.

The geometric term remains the existing estimator. The maximum texel footprint
can be driven by a small stretched chart, and shrinking atlases can reduce chart
gutters or photographic detail. Ratio 1 is the first candidate to benchmark at
equal rendered quality, rather than a claim that such quality is guaranteed.
Fresh hierarchy builds should be used for comparisons because of the checkpoint
limitations described in the round 1 notes.
