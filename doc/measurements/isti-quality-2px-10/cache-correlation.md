# Do cache savings target the earlier problem cases?

The savings correlate strongly with **upstream texture burden**, rather than
looking like an arbitrary subset. At factor 1.5 and requested error 2 px, the
four models that save cache are exactly the four with the largest upstream
texture/geometry GPU-memory ratios in this ten-model sample. Rank correlation
between that ratio and cache saving is **Spearman ρ = 0.915**. This is descriptive
evidence from a small, deliberately selected sample, not an independent
collection-wide statistical test.

| Model | Upstream texture/geometry bytes | Cache saving | Change in drawn triangles | Source PSNR change |
|---|---:|---:|---:|---:|
| Rock RWT14 | 0.90× | −55.2% | +38.4% | +0.967 dB |
| Mossy rock RWT76 | 0.59× | −476.0% | +384.2% | +2.925 dB |
| Lion RWT139 | 0.68× | −103.8% | +113.9% | +2.794 dB |
| Ornament RWT256 | 1.48× | **17.5%** | +3.6% | +0.117 dB |
| Vase RWT292 | 10.15× | **79.7%** | +22.9% | −0.020 dB |
| Cake RWT319 | 3.79× | **4.0%** | 0% | +0.087 dB |
| Skull RWT408 | 0.80× | −87.4% | +88.8% | +1.222 dB |
| Tart RWT471 | 24.20× | **77.7%** | 0% | −0.134 dB |
| Graffiti RWT500 | 0.51× | −274.4% | +376.6% | +2.727 dB |
| Trunk RWT514 | 0.74× | −412.2% | +295.6% | +2.386 dB |

Negative cache saving means an increase. All comparisons use identical camera,
viewport and source inputs; selected geometry can change despite identical
geometry payloads in the exports.

The clearest corrections are the **vase and tart**: upstream allocates 10.15× and
24.20× as many bytes to textures as geometry at this view. We reduce their cache
by about 80%, with similar source-relative quality and approximately 96% retained
interior gradient detail. The tart draws exactly the same triangle count; the
vase draws more triangles. Their savings therefore do not come from displaying
less geometry. The ornament and cake have smaller gains; the cake also draws
the same triangle count.

Three of the four winners (ornament, vase, tart) were already the models in this
sample benefiting from round 2 at 2 px, before the reconstruction-error changes.
Historical round-2/round-1 savings were 17.29%, 51.88%, and 79.10%, respectively.
The cake had no resident-cache saving then at 2 px, though it benefited at 0.1 px.
The remaining six had no round-2 cache saving at 2 px. The lion was not in the
historical 100-model sample, so it has no historical observation for that join.

For the six models whose cache increases, upstream textures are only 0.51–0.90×
geometry memory. Under our combined geometric/texture error, those models draw
**38–384% more triangles**, and all have higher source-relative PSNR (0.97–2.93 dB).
The increase is substantially extra refinement and quality, not evidence that
these models were damaged. It is nevertheless inefficient for a comparison
that seeks to match upstream quality. An increased cache percentage can be large,
although the absolute increase starts from roughly 0.54–2.35 MiB upstream.

## What this says about early saturation

These measurements do **not** record a finite-cache-budget stall: the cache is
unbounded by design. A large texture burden increases the likelihood of hitting
a given GPU-memory budget; it does not establish that a historical viewer did so.
Its previous encoded-byte cache estimate is also too imprecise to infer the actual
GPU-memory ceiling from the configured limit.

If “early saturation” means reaching the model's finest geometry or maximum cache
usage already at 2 px, the measurements do not show that either. Across the nine
models with historical controls, upstream cache at 2 px is only **0.9–23.3%** of
its cache at 0.1 px. At 0.1 px eight reach all nodes and draw exactly the source
triangle count; the graffiti wall draws 95.5% of source triangles (174/196 nodes).
All nine substantially refine beyond their 2 px cut. The lion lacks that historical
control observation and is not counted. These observations apply to this fixed
view and the unbounded cache, not arbitrary close-up views or finite budgets.

The defensible interpretation is: **the changes target oversized resident
textures, while the shared error mechanism over-refines the texture-light
models.** They are not proven to repair a former inability to refine all the way.
To establish that link, repeat the affected views with specified finite budgets,
using audited sizes for admission/eviction as well as reporting, and record whether
the requested error is reached. Comparing only the viewer's old cache-size estimate
would repeat the accounting problem.

[cache-correlation.csv](cache-correlation.csv) contains graphable per-model
texture burden, refinement, previous savings, and 2 px/0.1 px cache ratios.
[cache-correlation.json](cache-correlation.json) records descriptive correlations
and overlap checks. Reproduce with:

```sh
python3 tools/benchmark/cache-correlation.py doc/measurements/isti-quality-2px-10
```
