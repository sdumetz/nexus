# Corrected texture precision factor: 1 versus 2

This compares the intended factor semantics on the same ten moderate ISTI models
and fixed views used for rounds 3/4. The sample deliberately includes gains and
quality outliers; it is not representative of the full collection.

The factor divides **allowed texture error**. Factor 1 preserves the original
round 4 sizing and metric; factor 2 halves the sizing tolerance and doubles the
reported texture contribution before taking the geometric/texture maximum:

```text
allowed_footprint = geometric_error * texture_error_ratio / factor
reported_texture_error = footprint * min(1, occupied_RGB_RMS / 8) * factor
stored_error = max(geometric_error, reported_texture_error)
```

Both dimension choices and refinement now tighten with increasing factor.
Sizes stay multiples of four and never exceed the baked atlas dimensions.
Values below 1 relax quality. Reconstruction remains the only production metric.
The initial inverse interpretation was corrected in implementation commit
`c4f83f2` (code-only branch: `fbe7536`). Its interrupted diagnostic measurements
were moved outside the committed reports; all data here uses corrected semantics.

## Setup and verification

Each model's factor-1/factor-2 files are exported from one baked hierarchy. A
frozen round1 control retains the original texture dimensions and footprint
metric. The source glTF provides the image-quality reference. All views use the
same camera at 2.5 bounding-sphere radii, 1280x800 viewport, requested errors
2/0.5/0.1 px, unbounded cache, disabled below-target prefetch and FPS adaptation.
GPU accounting audits live Nexus buffers and full RGBA8 mip chains; CPU heap,
renderer shell and driver overhead are excluded.

All ten models and all 90 Nexus runs completed and passed the allocation audit.
Semantic geometry hashes match across all variants. Factor-1 exports match the
historical round4 `reconstructionFine` geometry and JPEG payloads; every baseline
allocation and all 120 round1/factor1 screenshots match that earlier run byte for
byte. Factor-2 dimensions are never smaller than factor-1 dimensions at any node.
The manifest records source hashes, binary hash, factor semantics and baselines.
`previous-round-validation.json` records the replay checks.

## Results

**Visible softening generally improves at factor 2, at a substantial cache cost.**
The lion's mane and pedestal and the mossy rock surface regain detail. The cake
also gets sharper, but its PSNR against the source worsens: more detail in the
baked representation is not necessarily greater source fidelity. The underlying
full-resolution round1 image also differs from the source in that case.

Factor 2 versus factor 1 (medians over ten models):

| Requested error (px) | Extra GPU cache | Source-relative PSNR improvement | Worst source-relative PSNR change |
|---|---:|---:|---:|
| 2 | +72.00% | +1.394 dB | -0.656 dB |
| 0.5 | +69.07% | +0.896 dB | -0.726 dB |
| 0.1 | +39.41% | +0.059 dB | -0.726 dB |

Current factor 2 versus round1 (original sizes and footprint error):

| Requested error (px) | Median GPU cache saving | Byte-weighted saving | Median source-relative PSNR change | Worst source-relative PSNR change |
|---|---:|---:|---:|---:|
| 2 | 11.40% | 46.50% | +0.013 dB | -0.162 dB |
| 0.5 | 20.61% | 43.76% | -0.056 dB | -1.145 dB |
| 0.1 | 8.72% | 31.71% | -0.058 dB | -0.355 dB |

At 0.1 px, factor1/factor2 have identical shaded images in 9/10 models, so
most extra residency at that target comes from larger textures. At 2 and 0.5 px,
shaded images change on 8/10 and 7/10 models respectively: the metric also
selects finer geometry. These are cache/quality tradeoffs, not universal
equivalent-quality results. Similar source PSNR medians do not imply identical
images: see the full captures and close-ups.

Static exported file size increases by a median **11.01%** versus factor 1
(byte-weighted 9.53%). Exported base texels increase by median **45.47%**
(byte-weighted 62.19%). These are whole-file/static texture measurements; GPU
residency above also depends on the selected cut and retains loaded ancestors.

## Examples

| Model / requested error | Factor 1 GPU MiB | Factor 2 GPU MiB | Round1 GPU MiB | Source PSNR change, factor 2 vs 1 |
|---|---:|---:|---:|---:|
| RWT139 / 0.5 px | 5.278 | 7.699 | 13.802 | +2.404 dB |
| RWT76 / 0.5 px | 17.327 | 30.044 | 29.320 | +1.431 dB |
| RWT319 / 0.1 px | 5.978 | 13.809 | 21.403 | -0.726 dB |

The lion at 0.5 px recovers **2.40 dB** relative to factor 1 but remains **1.15 dB**
below round1. It uses 7.699 MiB instead of factor1's 5.278 MiB and round1's
13.802 MiB. Factor 2 therefore retains a 44.22% cache saving against round1 in
that case while reducing the previous softening.

The cake at 0.1 px uses 13.809 MiB instead of 5.978 MiB (+131%), with PSNR
**0.726 dB lower** than factor 1. Its grain is sharper, but that does not remove
existing bake/sampling differences relative to the source. It remains only
0.078 dB below the full-resolution round1 control. The benchmark does not isolate
which bake/sampling differences cause the source disagreement.

[Whole-model and matching 4× close-up comparisons](comparisons/index.html)
include the lion, rock, cake and remaining lion difference from round1. Close-ups
use the original fixed-view pixels, not a nearer camera that would refine again.

## Upstream comparison

Nine models also occur in the historical 100-model `v4-fixes` benchmark. RWT139
is absent from that sample. The common 2/0.1 px views were joined only after
checking identical source hashes, cameras, viewport, semantic round1 payloads,
baseline allocations and source-relative pixel metrics. All checks passed.
There is no upstream 0.5 px measurement in that run. This is a nine-model subset
comparison, not a fresh collection-wide estimate.

Current factor 2 versus upstream:

| Requested error (px) | Median GPU cache change | Byte-weighted cache saving | Median source-relative PSNR change |
|---|---:|---:|---:|
| 2 | +66.82% | 22.03% | +1.386 dB |
| 0.1 | -6.90% | 31.04% | -0.035 dB |

At 2 px the median model still costs **66.82% more cache** than upstream while
rendering closer to the source. Byte-weighted saving is positive because a few
large-cache models dominate totals. At 0.1 px the median saving is **6.90%**,
with median source-relative PSNR change -0.035 dB. The weighted saving is 31.04%.
Do not describe the 2 px result as a typical cache reduction against upstream.

## Files and reproduction

- `graph.csv`: plotting table with MiB, savings percentages and source metrics.
- `results.csv`: raw byte counts, audits and comparisons against factor1/round1.
- `aggregate.csv`: median and byte-weighted summaries.
- `upstream-comparison.csv` / `upstream-aggregate.csv`: checked nine-model join.
- `models/*.json`: compact run records and static artifact hashes/dimensions.
- `screenshots/MODEL/gallery.html`: full captures, source references and diffs.
- `comparisons/index.html`: selected whole-model and magnified comparison sheets.

```sh
python3 tools/benchmark/build-pair.py BUILD_DIR --compile-only /tmp/nexus-precision-comparison-pair
python3 tools/benchmark/texture-rounds.py --dataset /path/ISTI_dataset --pair /tmp/nexus-precision-comparison-pair --node /path/node --out OUTPUT --scratch /tmp/nexus-texture-precision-10 --divisor-comparison --baseline-scratch ROUND4_SCRATCH --baseline-report doc/measurements/isti-reconstruction-10 --reuse-builds
python3 tools/benchmark/texture-rounds-summary.py OUTPUT --compare divisor2=divisor1 --compare divisor1=round1 --compare divisor2=round1 --divisor-baseline doc/measurements/isti-reconstruction-10
python3 tools/benchmark/precision-upstream.py OUTPUT doc/measurements/isti-100
node tools/benchmark/softening-screenshots.mjs --precision
```

The historical round1 control is an existing file, not an opt-out in the current
builder. Recreate it with the historical `322f90c` driver if scratch files are
unavailable. Measurement artifacts and tool changes are committed separately
from the implementation; `decoupled_textures-code` remains source/tests only.
