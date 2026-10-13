# Round 4: reconstruction-loss approximation on ten ISTI models

**Historical benchmark:** all reconstruction variants below used divisor **1**.
The current builder always uses reconstruction error with default divisor **2**;
these CSVs and screenshots have not been rerun for that default. To reproduce
this exact comparison, use the builder, paired-export driver and runner from
commit `322f90c`. Current tooling exports only reconstruction variants.

Same deliberately selected models, fixed camera, source renders, viewport and
requested errors as [round 3](../isti-fine-10/README.md). This sample emphasizes
previous gains and outliers; its aggregates are not collection-wide estimates.
Every variant for a model is exported from one hierarchy.

| Variant | Texture dimensions | Stored texture error before saturation |
|---|---|---|
| round1 | Full baked sizes | Maximum texel footprint |
| fine | Round 3, multiples of four, ratio 1 | Maximum texel footprint |
| reconstruction | Full baked sizes | Footprint weighted by JPEG reconstruction loss |
| reconstructionFine | Round 3, multiples of four, ratio 1 | Footprint weighted by JPEG + resizing reconstruction loss |

The loss reference is the full-resolution baked atlas **at the same node**.
Compute RGB RMS loss over occupied UV regions after decoding the actual exported
JPEG and smoothly reconstructing its full dimensions. The experimental term is
`footprint * min(1, RMS / 8)`, with RMS in 0–255 RGB code values. The calibration of
8 is an explicit hypothesis. See [implementation and limitations](../../round4-reconstruction-error.md).

Changing only the metric leaves all geometry and JPEG payloads unchanged.
The resizing rule itself retains the original footprint criterion. Thus this
experiment separately evaluates traversal and texture dimensions, with no file
format or viewer changes. At the time of this benchmark, reconstruction was
opt-in and footprint was the default. That historical mode switch has since
been removed.

`graph.csv` contains MiB, savings percentages and image metrics per model,
variant and requested error; `results.csv` retains raw byte counts and audit
fields. `aggregate.csv` and `aggregate.json` contain summary statistics.
`screenshots/MODEL/gallery.html` provides comparisons against preceding variants
and the original glTF. Empty PSNR paired with an identical-image flag means
infinite PSNR.

The live GPU allocation audit includes all generated mip levels and geometry
buffers. Builds, sources and cameras are frozen in `selection.json`. Per-model
JSON retains exact allocations, static payload hashes and image comparisons.
`previous-round-validation.json` checks unchanged round1/fine payloads,
allocations, and byte-identical screenshots against round 3. Repeated exports
now initialize geometry padding; whole-file hashes can therefore differ from
round 3 even when semantic payloads match.

## Results

All ten models completed successfully at all three requested errors. All 120
Nexus run audits passed; unchanged baseline exports, allocations and all 120
round1/fine screenshots exactly match round 3. Geometry payloads match across
all variants. Original-size/reconstruction JPEGs match byte for byte, as do
fine/reconstructionFine JPEGs.

Changing only round 1's error metric (original texture sizes):

| Requested error (px) | Median cache saving | Byte-weighted saving | Median source PSNR change | Worst source PSNR change | >1% changed pixels |
|---|---:|---:|---:|---:|---:|
| 2 | 34.79% | 28.28% | -0.678 dB | -1.689 dB | 7/10 |
| 0.5 | 28.12% | 14.73% | -0.541 dB | -3.549 dB | 6/10 |
| 0.1 | 0.00% | 1.26% | +0.000 dB | -0.021 dB | 1/10 |

Combining reconstruction refinement with finer dimensions, versus original round 1:

| Requested error (px) | Median cache saving | Byte-weighted saving | Median source PSNR change | Worst source PSNR change |
|---|---:|---:|---:|---:|
| 2 | 47.52% | 71.75% | -0.677 dB | -1.689 dB |
| 0.5 | 51.91% | 68.55% | -0.921 dB | -3.549 dB |
| 0.1 | 34.34% | 57.26% | -0.081 dB | -0.959 dB |

These are **cache/quality tradeoffs**, not equivalent-quality savings. At 2 and
0.5 px, changing the metric changes geometry residency and shaded images on
7/10 models. At 0.1 px, 9/10 keep identical images and allocations when only the
metric changes. Fine/reconstructionFine have smaller sidecars; reconstruction
alone changes their error metadata, not the texture payload size. Comparing
reconstructionFine with reconstruction keeps geometry residency and shaded
images identical at every view: its extra savings are texture memory.

The lion sculpture (RWT139) is a clear counterexample to the reference:
at 0.5 px, reconstruction alone saves 61.76% cache but loses 3.55 dB of
source-relative PSNR. Viewed screenshots show softer mane and pedestal detail.
The rock RWT14 at 2 px drops from 40 to 27 resident nodes, saving 38.56% cache;
37.56% of foreground pixels change by more than 8/255.

The inexpensive reference cannot detect detail already missing in a coarse
baked atlas. Low JPEG reconstruction loss therefore does not imply fidelity to
the original textured surface. The benchmark originally recommended keeping
this mode opt-in. It has since been adopted as the only metric, with a divisor
of 2 for subsequent tuning; these quality limitations remain. The next error experiment
should include loss from baking/simplification relative to finer or original
source samples, rather than only loss added at export. That measurement could
still be computed by the builder and stored in the existing error field.

Reproduce the historical comparison with commit `322f90c`:

```sh
python3 tools/benchmark/build-pair.py BUILD_DIR --compile-only /tmp/nexus-reconstruction-pair
python3 tools/benchmark/texture-rounds.py --dataset /path/ISTI_dataset --pair /tmp/nexus-reconstruction-pair --node /path/node --out OUTPUT --scratch /tmp/nexus-texture-reconstruction-10 --variants round1,fine,reconstruction,reconstructionFine
python3 tools/benchmark/texture-rounds-summary.py OUTPUT --compare reconstruction=round1 --compare reconstructionFine=fine --compare reconstructionFine=round1 --compare reconstructionFine=reconstruction --previous ROUND3_OUTPUT
```

The runner can resume completed measurements under its frozen manifest.
`--reuse-builds` also reuses completed scratch exports following an interruption.
