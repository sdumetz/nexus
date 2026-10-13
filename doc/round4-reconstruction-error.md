# Round 4: loss-weighted texture refinement experiment

Reconstruction error is now the only texture refinement metric. There is no
footprint-mode opt-out. The CLI exposes `--texture-error-divisor`, default **2**,
and rejects zero, negative, nonnumeric and non-finite values.

The original round 4 measurements used the unscaled contribution (equivalent to
factor **1**). Their captures and CSV values are historical evidence. The
corrected factor-2 comparison is in [isti-precision-10](measurements/isti-precision-10/README.md).
Quality calibration remains future work.

For each node:

1. Preserve its full-resolution baked RGB atlas as the reference.
2. Encode the exported dimensions to JPEG at the existing quality of 92, decode
   that exact JPEG, and reconstruct it at the reference dimensions with Qt smooth
   scaling.
3. Rasterize the node's UV triangles into a binary occupied-region mask. Exclude
   chart padding and unused atlas regions from the comparison. Image orientation
   matches the JPEG exporter: UV v increases upward, image rows downward.
4. Compute RGB RMS reconstruction difference over occupied pixels in 0–255 code
   values. This includes JPEG loss and any export-time resizing loss. It does not
   measure linear-light or perceptual color difference.
5. Compute the experimental world-space heuristic:

   `reported_texture_error = texel_footprint * min(1, reconstruction_rms / 8) * divisor`

6. Store `max(geometric_error, texture_error)` and enforce the existing ancestor
   monotonicity. Nodes with no occupied raster samples use the footprint
   fallback multiplied by the same precision factor. Untextured nodes retain the geometric error.

The calibration of **8 RGB code values RMS** is a hypothesis, not a derived
conversion between color and geometric error. Low-loss textures drive less
refinement, while RMS >=8 reaches the round 1 footprint before precision weighting. An exactly reconstructed
constant texture has zero texture contribution. The aggregate node RMS can hide
small high-detail features; the maximum footprint remains conservative about
chart distortion.

The divisor applies to the **allowed texture error**, rather than dividing the
stored error field. It is a precision factor with default **2**:

| Factor | Allowed texel footprint | Reported texture contribution | Intent |
|---|---|---|---|
| 0.5 | `2 * ratio * geometric_error` | `0.5 * reconstruction_error` | Lower quality, smaller textures, less refinement |
| 1 | `ratio * geometric_error` | `reconstruction_error` | Original round 4 behavior |
| 2 | `ratio * geometric_error / 2` | `2 * reconstruction_error` | Higher quality, larger textures, more refinement |

The dimension search uses `ratio * geometric_error / divisor`. Dimensions
remain multiples of four; baked images are never enlarged. The reported error
is weighted by the divisor before `max(...)`, which makes the existing viewer
refine more when needed at the same requested screen-space error. Geometry
continues to supply a floor. Both sizing and refinement follow the same tuning
direction; changing the factor can change JPEG dimensions and payloads.

`--texture-error-ratio 0` keeps baked dimensions but still computes and weights
reconstruction error. `--texture-error-divisor 1` reproduces the original round
4 sizing and error contribution; 2 tightens the tolerance and 0.5 relaxes it.

An earlier implementation applied the factor inversely to the stored metric
and left dimensions unchanged. That interpretation was incorrect and has been
replaced. Its interrupted diagnostic run was moved outside the committed
reports; it is not part of the corrected benchmark.

## What this reference misses

A coarse baked atlas can be perfectly reconstructed and still lack considerable
detail from the input textured surface. Each hierarchy node uses its own baked
reference; there is no cross-level or original-surface comparison. This metric
only measures the **additional export loss** at that node. Consequently, it can
lower errors on blurry coarse nodes and stop refinement too early. Comparisons
against the original glTF are necessary to detect this failure.

The geometric component is also an existing edge-length heuristic, not a
measured deviation from the original surface. Neither the original nor revised
maximum is an image-quality bound.

## Validation and reproducibility

`python3 tests/run_round1.py BUILD_DIR` verifies exact/constant reconstruction,
known RMS, calibration and divisors, clamping before precision weighting, occupied-region
exclusion, scaled empty-mask fallback, and rectangular sizing plus earlier export
checks. CLI checks cover default/explicit divisors, invalid values and rejection
of the removed metric option. Actual binary
exports verify that the default factor doubles texture-only node and ancestor errors when sizes
are fixed (zero geometric target), preserving headers, node metadata, geometry,
patches and JPEG bytes in that case. Actual JPEG dimensions also verify higher
precision at 2 and lower precision at 0.5, including the historical factor-1
sizing results.

The exporter previously wrote uninitialized bytes in padded geometry buffers.
Those bytes are now zero-initialized. This makes the binary export comparison
reliable and leaves semantic geometry and textures unchanged.

The ten-model results are in [isti-reconstruction-10](measurements/isti-reconstruction-10/README.md).
