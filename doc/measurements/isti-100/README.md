# Quantitative comparison on 100 ISTI models

Start with [graph.csv](graph.csv) for plotting; [results.csv](results.csv) contains
the detailed counters and comparisons. Each file has **200 rows: 100 models ×
two quality targets**, including unsuccessful attempts. Empty measurements mean
missing data, not zero cache or zero image difference. The runner updates these
files as models complete; [completion.json](completion.json) is written only
when all selected models have been attempted.

The completed batch has **98 successful models and two upstream/prototype build
failures** (RWT494 Snail race and RWT550 USNM 346 Seriatopora Hystrix, both
SIGSEGV during level 1). At the high-detail target, round 2 saves **4.63% median,
16.63% mean, and 23.00% by total cache bytes**, relative to round 1. 61 of 98
models save cache, and 31 save at least 25%. At the ordinary two-pixel target,
the median is zero and only eight models save cache. See [aggregate.md](aggregate.md)
for the full distributions and comparison against v4-fixes.

All 196 round 1/round 2 shaded-image comparisons are identical. Textured losses
are generally small, but four models exceed 1% changed foreground pixels in at
least one target. Inspection of the retained captures shows visible softening
of fine texture detail in the cake (RWT319) and the vase base (RWT292), and smaller
changes in the architectural ornament and tart. Ratio 1 therefore has useful
savings on some models but is not a universal equal-quality result. The original
sculpture's 43% result overstates the median benefit across this larger sample.

## Sampling and method

The selection is frozen in [selection.json](selection.json), with model names,
categories, source locations/hashes, and attribution/license information.
Python random seed **20261012** selects 100 from 116 eligible models. Eligibility
is 10,000–150,000 triangles, one source atlas with both dimensions ≤4096, and UVs
on all primitives. Selection precedes building; failures are retained and never
replaced. This is a comparison of moderate textured models, not a representative
sample of every model size in the entire collection. Median input triangle count
is approximately 46k. All selected source nodes have identity transforms.

Every model uses the same standardized camera direction, distance **2.5 bounding
sphere radii**, 1280×800 viewport, lighting and material. There are two screen
error targets: **2 pixels** (ordinary LOD) and **0.1 pixels** (high detail).
The latter is not assumed to load every node: resident and total counts make
that distinction measurable. Full-resolution glTF is a quality reference.

The unchanged **v4-fixes** build (`1fe489d`) is `control`. The experiment is
round 2 commit `f763879` on that base. The same converted OBJ feeds both builds;
rounds 1 and 2 are exported from one hierarchy. Round 1 retains baked dimensions
(ratio 0), while round 2 uses **ratio 1**. All other builder settings are defaults.
Geometry and texture payload hashes check that a separate control build did not
silently introduce bake/simplification differences. For the isolated round 2
comparison, use `round2_geometry_matches_round1`.

The [existing browser harness](../../../tools/benchmark/README.md) audits actual
live Nexus-owned WebGL allocations, including exact RGBA8 mip chains. An
independent decoded node/image-size check must agree. Cache budget is infinite,
FPS adaptation and below-target prefetch are disabled, and loaded ancestors count.
Each variant/target uses a fresh browser document/context. This measures logical
GPU residency, not process memory, physical driver VRAM, or CPU/disk cache.
No performance conclusions are drawn from build or measurement duration.

## Columns for graphs

In `graph.csv`, filter `quality_target_pixels` to select a target. For round 2
graphs, require a recorded comparison with foreground pixels and successful
allocation audits (the detailed CSV provides the two audit flags). Use
`row_measurement_complete=True` when comparing all three variants.

- `model_id`, `name`, `category`, `input_triangles`, `input_texels`: labels and
  possible size/color axes.
- `control_gpu_mib`, `round1_gpu_mib`, `round2_gpu_mib`: cache sizes, using
  1 MiB = 1,048,576 bytes. Geometry/texture MiB columns split those totals.
- `round2_vs_round1_gpu_saving_pct`: primary effect of texture sizing.
  Positive means a saving; negative means increased residency. Zero is retained.
- `round1_vs_control_gpu_saving_pct`, `round2_vs_control_gpu_saving_pct`: whole
  prototype differences against v4-fixes. These do not imply equal visual quality.
- `round2_vs_round1_file_bytes_saving_pct` and
  `round2_vs_round1_export_base_texels_saving_pct`: static export savings,
  distinct from savings at the chosen camera/LOD cut.
- `round2_vs_round1_textured_changed_pixels_over_8_pct`: percent of foreground
  pixels with any RGB channel differing by more than 8/255. Plot against cache
  saving to assess the quality/residency tradeoff.
- `round2_vs_round1_textured_psnr_db`: image PSNR between the two rounds.
  Exact equality gives infinite PSNR, represented by a blank **and**
  `round2_vs_round1_textured_identical=True`; missing data also has a blank PSNR
  but lacks the equality flag.
- `*_vs_source_textured_psnr_db` / `*_changed_pixels_over_8_pct`: quality relative
  to the full-resolution source. Source materials are standardized for comparison.
- `round2_vs_round1_shaded_identical`: whether the geometry/normal-only render
  changed. Textured differences alone are not automatically geometry differences.
- `status`, `row_measurement_complete`, `round2_comparison_has_foreground`:
  measurement validity. The detailed CSV additionally has per-stage status,
  diagnostics, hashes checked, resident counts, and the viewer's legacy estimate.

The detailed CSV uses **bytes** and pixel-change **fractions** (0–1), whereas
`graph.csv` converts those plotting columns to **MiB** and **percent** (0–100).
PSNR and changes use the union of non-background model pixels, rather than being
diluted by the empty viewport. Foreground IoU is a background-color approximation;
texture color at edges can affect it even with identical geometry.

Useful first graphs are a scatter of `round1_gpu_mib` versus `round2_gpu_mib`
with a diagonal equality line, a histogram of `round2_vs_round1_gpu_saving_pct`,
and a scatter of savings versus `round2_vs_round1_textured_changed_pixels_over_8_pct`.
Keep the two quality targets separate. Do not drop zero savings or treat failed
models as zero; report the valid sample count alongside each graph.

## Evidence and reproduction

Per-model compact raw measurements are in `models/RWT*.json`; diagnostic logs
are in `logs/RWT*/`. PNG captures are retained for the first eight preselected
models and any model with >5% changed foreground pixels between rounds. Their
locations are in `screenshot_directory`; attribution is in the selection manifest.
Intermediate OBJ/NXS/hierarchy files are removed after each model to bound disk
use. Rebuild a model using the manifest source and hashes when full intermediates
are needed. JSON comparison filenames refer to captures from the original run;
only the retained screenshot subsets remain on disk.

Build an unchanged control and the prototype as described in the harness notes,
then compile the paired exporter once and start the batch:

```sh
python3 tools/benchmark/build-pair.py /path/to/prototype-build \
  --compile-only /tmp/build-pair
python3 tools/benchmark/isti-batch.py \
  --dataset /home/sebastien/Documents/3DModels/ISTI_dataset \
  --control /path/to/v4-fixes-build/nxsbuild --pair /tmp/build-pair \
  --node /path/to/node --out doc/measurements/isti-100 \
  --scratch /tmp/isti-batch --workers 2
python3 tools/benchmark/isti-summary.py doc/measurements/isti-100
```

Requires Pillow, Node 22+, Chromium and the three.js package used by the harness.
Builds can overlap, but software-GL measurements are serialized. Each build has
a ten-minute timeout; each browser batch has fifteen minutes, with the harness's
shorter per-view timeout. Timed-out processes are terminated as a group. Rerunning
the same command resumes completed model records with the frozen selection.
[summary.json](summary.json) reports distributions, sample counts, image changes,
failures, and size-weighted aggregate savings; medians weight each model equally.

The [aggregate report](aggregate.md) presents those figures in tables. Temporary
cuts were initially rendered while loading; the remaining runs use traversal-only
loading with the same cache scheduler. [Loading validation](loading-validation.json)
confirms exact node/allocation/PNG equivalence at both targets. Comparisons now
reuse the captured pixels rather than rendering again for each reference;
[pixel validation](captured-pixel-validation.json) confirms identical images and
metrics. These affect batch runtime, not the recorded endpoint or quality target.

After completion, retain additional captures for every >1% changed-pixel case:

```sh
python3 tools/benchmark/isti-recheck-images.py \
  --out doc/measurements/isti-100 --control /path/to/v4-fixes-build/nxsbuild \
  --pair /tmp/build-pair --node /path/to/node --scratch /tmp/isti-rechecks
python3 tools/benchmark/isti-summary.py doc/measurements/isti-100
```

This repeats those cases and requires identical geometry/texture payload hashes, allocations
and image metrics before retaining captures. The CSV keeps the original
measurements. [Image rechecks](image-rechecks.json) records that verification.
Whole-file hashes can differ between builds even when decoded payloads and
recorded rendering results match; rechecks record whole-file equality separately.
