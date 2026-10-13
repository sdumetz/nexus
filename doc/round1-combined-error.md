# Round 1: combined geometry and texture error

This describes a historical experiment. The current builder always uses
[round 4 reconstruction error](round4-reconstruction-error.md), at precision factor 2
by default; ratio 0 now preserves sizes without reverting the error metric.

Round 2 now enables export-time texture sizing by default. Use
`--texture-error-ratio 0` to reproduce the round 1 behavior described here;
see [round 2](round2-texture-sizing.md) for the new default.

The builder exports `Node.error = max(geometric_error, texel_error)` before the
existing ancestor saturation pass. It uses the existing version 2 container and
viewer traversal. Texture dimensions, JPEG encoding, geometry simplification
targets, and the texel/triangle sizing heuristic remain unchanged for round 2.

The implementation is in [export_nxs.cpp](../src/nxsbuild/export_nxs.cpp) and
[texel_error.h](../src/texture/texel_error.h). It computes texture error from each
node's final UVs and actual texture dimensions, once at export, without adding
checkpoint or on-disk error fields.

For each triangle, let `U` contain its two UV edges expressed in texture pixels,
and `P` contain the corresponding world-space edges. The pixel-to-world mapping
is `J = P * inverse(U)`. Its largest singular value is the largest world-space
footprint of a pixel, accounting for chart stretching, rotation, and rectangular
images. The node's texel error is the maximum across its triangles. A collapsed
UV triangle uses its world-space diameter; every triangle footprint is bounded
by that diameter for subpixel charts. Zero-area world triangles return zero.

Both terms are world-space lengths and therefore use the viewer's existing
projection into pixels. Round 1 uses equal pixel tolerances for geometry and
texture. Ancestor saturation can raise the final stored error above this local
maximum to preserve hierarchy ordering. The sink remains zero.

The previous texture/triangle multiplier in `reparametrize_clusters` has been
removed. That multiplier acted on newly created micronodes before their geometry
error was assigned. Micronode geometry error now starts at zero, including final
roots that never undergo another simplification step. The geometric term is
still the existing simplifier's mesh-size estimate; this experiment does not
replace it with a measured surface-deviation bound.

Use a fresh hierarchy build for comparisons. Old checkpoints can contain errors
from the previous code (and the current checkpoint saving does not reliably
persist the later error updates to preceding levels). Export-time texture
measurement does not repair those old geometric estimates.

`-V verbose` prints `geometric_error`, `texel_error`, and the local
`combined_error` for every exported node. The CLI now applies its existing
verbosity option to the logger. The logged combined value precedes saturation.
The current CLI writes the final file as `test.nxs`, irrespective of `-o`; this
pre-existing behavior has not been changed by round 1.

## Validation

Build `src/nxsbuild` with its existing Qt6, VCGLib, Trueform, METIS, Draco, PNG,
and JPEG dependencies. With a completed Unix Makefiles build, run:

```sh
python3 tests/run_round1.py /path/to/nxsbuild-build-directory
```

The tests reuse that build's exporter objects and create temporary artifacts.
They check analytically known densities, resolution scaling, rectangular
images, stretched and rotated UVs, collapsed/subpixel charts, and zero-area
geometry. Synthetic two-level exports check both geometry- and texture-dominated
nodes, geometry-only behavior, ancestor saturation, the zero-error sink, and
unchanged header version and node/texture counts. Checks remain active in
Release builds.

Validation in this worktree passed with a Release build using the locally
available Trueform checkout and its standard allocation backend. A full CLI
smoke build of a textured planar grid (512 source triangles, 128x128 PNG) also
passed: it exported five real nodes and five JPEG textures, with finite errors
and monotonic parent/child ordering. This exercises loading, simplification,
reparameterization, and export; it is not an image-quality or savings benchmark.

The maximum footprint is deliberately conservative: a small stretched chart can
drive refinement for an entire node. Round 2 can evaluate density-aware sizing
and alternative aggregation rules against equal measured image quality.
