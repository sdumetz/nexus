# Quality calibration at 2 px against upstream

Use **precision factor 1.5** for a conservative, common-factor comparison at
requested screen-space error **2 px**. This is the lowest tested common factor
that avoids material detail loss across these ten fixed views. It is a benchmark
calibration, not a change to the production default (2).

The combined geometry/texture error still couples refinement. Consequently,
this common factor gives several models noticeably *higher* quality than
upstream. It does not produce an exact equal-quality match for every model.

| At 2 px, ten models | Common factor 1.5 | Per-model calibrated factors |
|---|---:|---:|
| Total audited GPU cache saving | **34.58%** | **58.72%** |
| Median model cache saving | **−71.27%** (increase) | **4.60%** |
| Median source-relative PSNR change | +1.094 dB | +0.063 dB |
| Worst source-relative PSNR change | −0.134 dB | −0.134 dB |
| Worst retained upstream interior gradient RMS | 95.85% | 95.46% |
| Median NXS file saving | 7.77% | 21.13% |
| Total NXS file saving | 9.35% | 19.81% |

Total cache is **49.083 MiB upstream → 32.112 MiB at factor 1.5**, or 1.53× less.
Only four models use less cache with the common factor; the vase and tart drive
the total savings. The per-model result uses different export factors for each
model and selects them with knowledge of this view. It is a diagnostic of the
potential of calibration, not a deployable universal setting or a held-out
estimate. Neither result includes KTX2 encoding or mip-as-sidecar changes.

| Model | Upstream cache MiB | Factor 1.5 cache MiB | Saving | Source PSNR change |
|---|---:|---:|---:|---:|
| RWT14, rock | 1.099 | 1.705 | −55.2% | +0.967 dB |
| RWT76, mossy rock | 0.895 | 5.158 | −476.0% | +2.925 dB |
| RWT139, lion sculpture | 1.076 | 2.194 | −103.8% | +2.794 dB |
| RWT256, ornament | 3.632 | 2.997 | 17.5% | +0.117 dB |
| RWT292, vase | 15.305 | 3.104 | 79.7% | −0.020 dB |
| RWT319, cake | 3.027 | 2.907 | 4.0% | +0.087 dB |
| RWT408, skull | 2.346 | 4.395 | −87.4% | +1.222 dB |
| RWT471, tart | 20.544 | 4.573 | 77.7% | −0.134 dB |
| RWT500, graffiti wall | 0.618 | 2.313 | −274.4% | +2.727 dB |
| RWT514, tree trunk | 0.540 | 2.767 | −412.2% | +2.386 dB |

## Calibration and visual checks

Swept factors **0.25, 0.375, 0.5, 0.75, 1, 1.5, 2, 3, 4**. Larger factors tighten
the allowed texture tolerance and multiply its reported error, retaining more
texture precision and often upgrading geometry. No format or viewer change.

Source-relative foreground RGB PSNR alone was misleading: the cake at factor
0.5 improved PSNR while visibly softening. An 8×8 block luminance SSIM diagnostic
caught that loss. Factor 0.75 still softened the cake and lost 0.792 dB on the
tart. Factor 1 passed the source PSNR/SSIM checks, but retained only 82% of the
cake's upstream interior gradient RMS. Factor 1.5 retains 96.5% on the cake and
96.1% on the tart, while factors 2–4 cost more without being necessary for this
comparison. Factors need not improve source PSNR monotonically: atlas sampling,
JPEG, aliasing and cut changes also affect the image.

Final acceptance checks, applied **per model**, are source-relative PSNR loss
≤0.15 dB, block SSIM loss ≤0.005, and retained upstream interior luminance-gradient
RMS ≥95%. These are practical calibration tolerances, refined after inspecting
the captures, not a perceptual equivalence theorem or preregistered criteria.
The initial tighter screening (PSNR loss 0.1 dB, SSIM loss 0.002, source-gradient
error growth ≤2%) remains in `strict_quality_accepted` for transparency.
Source-gradient error is retained as a diagnostic, rather than an acceptance
check: blurring can reduce it, and a visibly sharper render can increase it.

Block SSIM uses nonoverlapping 8×8 blocks, BT.709 luminance, population moments,
constants C1=6.5025/C2=58.5225, and foreground-pixel weights. It is **not** the
standard Gaussian-window SSIM implementation. The separate detail diagnostic
uses Pillow's integer BT.601 luminance, adjacent horizontal/vertical differences,
and a shared mask requiring both edge endpoints to be foreground in both
images. It excludes silhouette edges. Gradient RMS measures detail/contrast,
not fidelity by itself; inspect it together with source metrics and screenshots.

[Whole-model and native-pixel close-up comparisons](comparisons/index.html)
cover the mossy rock, lion, cake and tart at the chosen common factor. The cake
and tart are the relevant softening checks; the rock and lion illustrate quality
overshoot. Crops magnify actual capture pixels 4×, without rerendering or sharpening.
Original textured captures for every factor/model are in `screenshots/`.

## Data, controls and accounting

- [graph.csv](graph.csv): 90 candidate rows, all quality, GPU cache and file metrics.
- [comparison-factor-1_5.csv](comparison-factor-1_5.csv): the ten common-factor results.
- [aggregate.csv](aggregate.csv): factor curves; negative saving means a cost increase.
- [matched-per-model.csv](matched-per-model.csv): minimum-cache passing factor per model.
- [matched-aggregate.csv](matched-aggregate.csv): diagnostic per-model calibration totals.
- [validation.json](validation.json): quality criteria and audit/baseline validations.
- [detail-diagnostics.json](detail-diagnostics.json): shared-mask gradient measurements.
- `selection.json`: source hashes, binary hashes, factors and sample metadata.
- `models/*.json`: semantic export checks and compact measurements.
- `screenshots/*/results.json`: full allocation and image-comparison reports.

Same purposive ten-model sample as earlier rounds; not a random collection-wide
estimate. Fresh unmodified **v4-fixes 1fe489d** control exports and renders for all
ten, including the lion omitted by the historical 100-model sample. Identical
converted source inputs, geometry payload hashes, fixed camera at 2.5 radii,
1280×800 viewport, and original glTF source render. The nine overlapping controls
exactly reproduce historical export payloads, camera, cache allocations and
source image metrics. Factor 1/2 payloads reproduce the prior corrected experiment.

Every unique upstream/candidate job (100 total) starts a fresh browser context
with unbounded cache. Stable cut, no pending requests/decode, 12 unchanged frames,
no below-target prefetch. GPU cache is the live sum of unique decoded Nexus GL
buffers and RGBA8 textures including exact rectangular/NPOT mip chains and
resident ancestors. Every job passed the independent WebGL allocation audit.
It excludes CPU memory, driver overhead and unrelated renderer objects. Nexus's
encoded-byte cache estimate is not used for gains. All geometry payloads are
identical across exports; selected cuts can differ.

Only textured captures and the selected comparison sheets are committed. Raw
reports also name shaded/difference images, which are regenerated by the runner.
The initial sweep included finer targets before the user narrowed calibration
to 2 px; those captures were not used or included in this report.

## Reproduce

The prototype builder objects must already be built in `BUILD_DIR` and an
unchanged v4-fixes builder supplied as `UPSTREAM_BUILDER`. Retained converted OBJ
sources are under `SOURCES/RWT*/source/model.obj`; `gltf-to-obj.mjs` can recreate
these from the selected glTFs. Run from the repository root (Node 24, Chromium,
Pillow and the existing Three.js package are required).

```sh
python3 tools/benchmark/build-pair.py BUILD_DIR --compile-only /tmp/quality-pair
python3 tools/benchmark/quality-sweep.py \
  --pair /tmp/quality-pair --upstream UPSTREAM_BUILDER \
  --sources SOURCES --factors 0.25,0.375,0.5,0.75,1,1.5,2,3,4 \
  --out /tmp/quality-results --scratch /tmp/quality-builds
python3 tools/benchmark/quality-detail.py /tmp/quality-results
python3 tools/benchmark/quality-sweep-summary.py /tmp/quality-results \
  --psnr-loss 0.15 --ssim-loss 0.005 --gradient-growth inf \
  --min-detail-retention 0.95
node tools/benchmark/softening-screenshots.mjs --quality-factor 1.5
```

The last command presents committed-path captures, not `/tmp/quality-results`.
The experiment-only `NEXUS_BENCH_FACTORS` exporter builds one hierarchy per model
and exports the sweep from that hierarchy. Production builder options/defaults
remain unchanged. Measurements, notes and benchmark tools belong to a separate
experiment commit; `decoupled_textures-code` stays source-only.
