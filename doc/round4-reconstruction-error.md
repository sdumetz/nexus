# Round 4: loss-weighted texture refinement experiment

Reconstruction error is now the only texture refinement metric. There is no
footprint-mode opt-out. The CLI exposes `--texture-error-divisor`, default **2**,
and rejects zero, negative, nonnumeric and non-finite values.

The original round 4 measurements used the unscaled contribution (equivalent to
divisor **1**). Their captures and CSV values are historical evidence, not
measurements of the new default. Quality calibration remains future work.

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

   `texture_error = texel_footprint * min(1, reconstruction_rms / 8) / divisor`

6. Store `max(geometric_error, texture_error)` and enforce the existing ancestor
   monotonicity. Nodes with no occupied raster samples use the footprint
   fallback divided by the same divisor. Untextured nodes retain the geometric error.

The calibration of **8 RGB code values RMS** is a hypothesis, not a derived
conversion between color and geometric error. Low-loss textures drive less
refinement, while RMS >=8 reaches the round 1 footprint before division. An exactly reconstructed
constant texture has zero texture contribution. The aggregate node RMS can hide
small high-detail features; the maximum footprint remains conservative about
chart distortion.

Use `--texture-error-ratio 0` to keep baked texture dimensions while still
computing reconstruction error. Use ratio 1 to combine it with round 3's finer
sizing. `--texture-error-divisor 1` reproduces the initial round 4 contribution;
2 halves it, and 0.5 doubles it.

Larger divisors make traversal accept coarser texture detail. Halving the stored
error does **not** retain twice the precision: a larger stored error drives more
refinement at the same requested screen-space tolerance. The divisor is applied
only to the texture term before `max(...)`; geometry still supplies a floor.
It does not change texture dimensions, JPEG payloads or the sizing target. Texture sizing still uses the original footprint constraint,
so changing the error metric alone cannot change JPEG dimensions or payloads.
This separation isolates refinement from sizing.

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
known RMS, calibration and divisors, clamping before division, occupied-region
exclusion, scaled empty-mask fallback, and rectangular sizing plus earlier export
checks. CLI checks cover default/explicit divisors, invalid values and rejection
of the removed metric option. Actual binary
exports verify that the default divisor halves texture-only node errors and
ancestor errors, preserving
headers, node metadata, geometry, patches and JPEG bytes.

The exporter previously wrote uninitialized bytes in padded geometry buffers.
Those bytes are now zero-initialized. This makes the binary export comparison
reliable and leaves semantic geometry and textures unchanged.

The ten-model results are in [isti-reconstruction-10](measurements/isti-reconstruction-10/README.md).
