# Round 4: loss-weighted texture refinement experiment

The CLI exposes `--texture-error-metric reconstruction`. The default remains
`footprint`: this approximation has not been established as a quality-preserving
replacement for round 1.

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

   `texture_error = texel_footprint * min(1, reconstruction_rms / 8)`

6. Store `max(geometric_error, texture_error)` and enforce the existing ancestor
   monotonicity. Nodes with no occupied raster samples retain the footprint
   fallback. Untextured nodes retain the geometric error.

The calibration of **8 RGB code values RMS** is a hypothesis, not a derived
conversion between color and geometric error. Low-loss textures drive less
refinement, while RMS >=8 keeps the round 1 footprint. An exactly reconstructed
constant texture has zero texture contribution. The aggregate node RMS can hide
small high-detail features; the maximum footprint remains conservative about
chart distortion.

Use `--texture-error-ratio 0 --texture-error-metric reconstruction` to revisit
round 1 without changing any texture sizes. Use ratio 1 to combine it with round
3's finer sizing. Texture sizing still uses the original footprint constraint,
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
known RMS and calibration, clamping, occupied-region exclusion, empty-mask
fallback, and rectangular sizing plus all earlier export checks. Actual binary
exports verify that enabling reconstruction changes only node errors, preserving
headers, node metadata, geometry, patches and JPEG bytes.

The exporter previously wrote uninitialized bytes in padded geometry buffers.
Those bytes are now zero-initialized. This makes the binary export comparison
reliable and leaves semantic geometry and textures unchanged.

The ten-model results are in [isti-reconstruction-10](measurements/isti-reconstruction-10/README.md).
