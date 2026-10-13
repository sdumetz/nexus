# Nexus atlas occupancy: ten ISTI models

This study measures texture packing from exported UV triangles, independently of
image colors, compression, and rendered quality. It reuses the ten purposively
selected moderate models and the identical exports from
[the 2px quality study](../isti-quality-2px-10/README.md): unmodified v4-fixes
`1fe489d`, our factor 1.5 candidate, and our default factor 2 candidate.
No builder, file-format, or viewer code changed for this measurement.

## Headline: occupancy at the complete finest LOD

Use **covered texels / allocated texels summed over all finest nodes**. These
nodes form the full-detail geometry cut: their triangle counts sum to the source
triangle count for every model. This is a source-resolution geometry comparison,
not a guarantee of identical texture quality; Nexus bakes/reprojects and our
variants resize those atlases. A finest cut also differs from a viewer cache,
which can retain ancestor textures. These are base-level atlas texels, not mip
chains or encoded file bytes.

| Model | Source occupancy | Upstream finest occupancy | Finest/source allocated texels |
|---|---:|---:|---:|
| RWT14 | 15.42% | 60.33% | 0.242× |
| RWT76 | 72.61% | 62.45% | 0.875× |
| RWT139 | 72.68% | 57.03% | 1.172× |
| RWT256 | 43.46% | 56.19% | 0.254× |
| RWT292 | 100.00% | 57.29% | 2.062× |
| RWT319 | 63.33% | 59.14% | 0.750× |
| RWT408 | 47.58% | 53.46% | 0.422× |
| RWT471 | 61.50% | 62.50% | 0.812× |
| RWT500 | 73.40% | 63.43% | 0.766× |
| RWT514 | 36.53% | 60.17% | 0.469× |

Upstream finest occupancy is **59.42% pooled by texels**, with a median across
models of **59.66%** (range **53.46–63.43%**). Approximately 41% of allocated
finest atlas texels are outside UV triangle interiors. That includes useful
seam padding: it is not a promise that all those texels can be removed safely.
Nexus packs moderately consistently across these models, but can either improve
or reduce occupancy relative to the source. Occupancy alone says nothing about
retained texel density or texture sharpness.

## Medium detail and node variability

`height_from_leaves=0` means finest nodes; 1 is one hierarchy step coarser, 2 is
two steps coarser. Height is computed from DAG connectivity, independent of the
stored combined geometry/texture error. Both minimum and maximum root depths
are retained per node. Levels have different numbers and areas of triangles;
these summaries describe node atlases, not a fixed screen-space render cut.

| Height from finest | Upstream nodes | Pooled texel-weighted occupancy | Node mean ± population SD | Node p10–p90 |
|---|---:|---:|---:|---:|
| 0 | 472 | 59.42% | 58.04% ± 8.27 pp | 47.89–68.38% |
| 1 | 399 | 55.58% | 52.94% ± 7.86 pp | 42.48–62.66% |
| 2 | 324 | 50.67% | 48.42% ± 8.66 pp | 37.68–59.46% |

Packing occupancy declines at coarser levels. A single average over the entire
hierarchy would conceal that. Recommended reporting is finest-cut weighted
occupancy as the source-comparison headline, then weighted occupancy by level
plus p10/median/p90 (and mean/SD where useful). Keep allocated texels beside the
occupancy: large atlases must carry more weight in memory-efficiency comparisons.
Pooling models weights large models more; the per-model CSV allows equal-model
summaries instead.

## Do our sizing changes change packing?

The fixed-512×512 reference occupancy and summed UV triangle area match exactly
for every corresponding node in all three variants. The UV layouts are
unchanged. Actual-resolution occupancy can differ slightly through raster
rounding and because different nodes receive different atlas sizes.

| Variant | Finest base texels, ten models | Pooled finest occupancy | Median per-model finest occupancy |
|---|---:|---:|---:|
| upstream | 114,491,392 | 59.42% | 59.66% |
| factor1_5 | 54,570,640 | 59.75% | 59.91% |
| factor2 | 69,437,504 | 59.80% | 60.19% |

Thus the existing savings come from texture size selection and refinement,
not improved atlas packing. These finest-LOD totals should not be substituted
for the previous 2px fixed-view cache measurements.

## Files and reproduction

- [finest-comparison.csv](finest-comparison.csv): 30 rows, directly graph source
  versus finest-cut occupancy and allocated texels for each model/variant.
- [nodes.csv](nodes.csv): 5,106 rows, one per node/variant (1,702 unique nodes).
  Contains triangle count, dimensions, connectivity height/depth, stored error,
  covered/allocated texels, occupancy, overlap fragment count, summed UV area,
  and reference-512 occupancy. Summed triangle UV area can double-count overlap;
  it is a diagnostic, not the occupancy metric.
- [summary.csv](summary.csv): model/variant/height summaries including weighted
  occupancy, mean, population SD, p10, median, p90, min/max, and unused texels.
  `height_from_leaves=all` includes every LOD and represents hierarchy storage,
  not a render cut. Fractions in CSVs are in [0,1]; percentage-point changes are
  explicitly named. Standard deviation is descriptive, not an uncertainty bound.
- [source-occupancy.csv](source-occupancy.csv): source OBJ UV-union occupancy at
  the original atlas dimensions, using the same raster metric.
- [provenance.json](provenance.json): input export hashes, source OBJ hashes,
  selection hash and extractor hash.
- [texmetro-validation.json](texmetro-validation.json): independent checks using
  the existing local TexMetro binary. Source RWT14 differs by 3 of 8,388,608
  texels; four finest/medium Nexus nodes differ by 0–3 texels (maximum absolute
  occupancy difference 0.0183 percentage points). Same occupancy definition;
  small boundary differences from OpenGL fixed-point/pixel-edge rules.

```sh
python3 tools/benchmark/texture-occupancy.py \
  --out /tmp/nexus-texture-occupancy-10
python3 -B tools/benchmark/texture-occupancy.test.py
```

The default input paths reuse the saved quality-sweep scratch exports and source
OBJs. The extractor also accepts arbitrary compatible exports with
`--nxs label=/path/model.nxs --model-id model --out /tmp/occupancy`.
Only uncompressed inline v2 geometry with the current position/UV/normal/index
layout and one unique atlas per node is supported. Unsupported signatures,
compressed geometry, or shared/multiple atlases are rejected. UVs are clipped to
the atlas, consistent with this packing metric; tiling/material texture
transforms require separate interpretation for other inputs.

Validation: analytic fixtures for triangle union, overlap, degeneracy, winding,
atlas clipping and weighting passed. Standalone and batch results matched;
finest cuts matched all ten source triangle counts; fixed-reference layout
metrics matched all variants. This is a small purposive sample, not an estimate
for the entire ISTI collection.
