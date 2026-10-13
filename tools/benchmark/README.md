# Fixed-view cache and image benchmark

Use the repository's JavaScript Nexus renderer with Chromium automation through
the Chrome DevTools Protocol (the protocol Puppeteer uses). No Puppeteer install
is required. Requires Node 22+, Chromium, and an installed three.js package.
This measures residency and image changes, not rendering performance.

```sh
node tools/benchmark/run.mjs \
  --model control=/absolute/path/control.nxs \
  --model round1=/absolute/path/model.round1.nxs \
  --model round2=/absolute/path/model.round2.nxs \
  --source /absolute/path/source.gltf \
  --three /absolute/path/node_modules/three \
  --out /tmp/nexus-results --views 6,2.5,1.2 --taus 2
```

`--source` is optional. Each model is compared with every preceding model and
the full-resolution source. The first Nexus model supplies the common bounding
sphere. `--views` specifies camera distances in its radii, in one fixed direction;
`--poses poses.json` instead accepts explicit position, target, optional up/fov,
near and far for each view. All models use exactly the same poses, lighting,
material, viewport (default 1280×800), and pixel ratio 1.

Outputs include `results.json`, `summary.md`, `gallery.html`, textured and
uniformly shaded PNGs, and absolute difference images amplified by four.
Pixel metrics exclude pixels where both images are background: PSNR, mean
absolute channel difference, fraction with maximum channel difference above
8/255, and silhouette intersection/union. These support visual inspection;
they do not establish perceptual equivalence automatically. Source rendering
retains base-color maps with standardized lighting/material rather than authored
PBR effects. Inspect both textured and shaded views to separate texture changes
from geometry/normal changes.

## Cache accounting and completion

The cache budget is infinite, FPS adaptation is disabled, and each measurement
uses a fresh document and WebGL context. Below-target prefetch is suppressed:
otherwise an infinite budget eventually loads the whole model. Loaded ancestors
remain resident and count toward cache usage. The view must have all required
nodes ready, no pending request or texture decode, and an unchanged allocation
signature for twelve frames. Timeouts and browser/WebGL errors fail the run.

The default loading mode is `traverse`: it runs the same view update, traversal
and cache scheduler without repeatedly rasterizing temporary cuts while data
loads. The settled view and all captures use the real renderer. Use
`--loading-mode render` to rasterize every loading frame as in the original
two-model experiment. Both targets were validated against the original path:
node IDs, cache bytes, triangle counts and PNGs match exactly. Timing remains
outside the benchmark's scope.

The authoritative number is **logical live Nexus GPU allocation bytes**, with
geometry and textures reported separately:

- Intercept actual `bufferData`, image uploads, mip generation, and deletion.
  Count each live Nexus-owned WebGL handle once, excluding three.js shell buffers.
- RGBA8 textures include every mip level down to 1×1 using exact dimensions,
  including rectangular and non-power-of-two textures. Generated mips count as
  resident storage, not additional uploaded payload.
- Independently verify buffer sizes against decoded node vertex/triangle counts
  and textures against decoded image dimensions and referenced texture IDs.
  A disagreement aborts measurement.
- Keep the existing viewer's `Cache.cacheSize` estimate as a diagnostic column.
  This module runtime estimates texture bytes as ten times their encoded ranges;
  that is not a dependable measure of decoded GPU residency.

This is not a measurement of physical VRAM, driver padding, CPU heap, or browser
HTTP/disk cache. `residentEncodedRangeBytes` unions index, node and referenced
texture ranges to avoid overlap (the last real node can span the texture tail).
It is a format/transfer diagnostic, not a claim that encoded buffers remain in
CPU memory. HTTP bytes and request counts are also diagnostic, not timing data.

[PR #178](https://github.com/cnr-isti-vclab/nexus/pull/178) addresses accounting in
the classic `html/js/nexus.js` viewer. Its decoded RGBA/mipmap approach motivates
this audit, but it does not fix this module runtime. The native cache also uses
RGB base-image sizing; using nxsview would still require auditing its GPU storage.

The harness locally adapts the current three integration's Vector4 viewport to
the array expected by traversal, and resets three's GL state each frame because
Nexus uploads/draws through raw GL. These changes prevent invalid traversal and
black captures. Production viewer sources are untouched. Raw NXS and Corto NXZ
are supported; MECO, Deepzoom and compressed GPU texture formats are rejected.

## Build comparable artifacts

Build `v4-fixes` unchanged as the primary upstream control. For rounds 1 and 2,
export both from **one** hierarchy to avoid independent bake/simplification
variation. With a completed Unix Makefiles nxsbuild directory:

```sh
mkdir -p /tmp/nexus-pair
cd /tmp/nexus-pair
python3 /absolute/path/nexus-decoupled/tools/benchmark/build-pair.py \
  /absolute/path/build model.obj -o /tmp/nexus-pair/model.nxs -V verbose
```

This produces `model.round1.nxs` (ratio 0) and `model.round2.nxs` (ratio 1,
or an explicit `--texture-error-ratio`). The driver respects `-o`; the existing
builder CLI currently writes `test.nxs`, so run the control in its own directory.
Fresh builds are required; checkpoint reuse is deliberately disabled.

To additionally compare the older Nexus 3 builder on identical source geometry,
convert an uncompressed external-buffer glTF to OBJ once and feed the same OBJ
to all builders:

```sh
node tools/benchmark/gltf-to-obj.mjs source.gltf /tmp/source/model.obj
nxsbuild-v3 -c -o /tmp/upstream-v3.nxs /tmp/source/model.obj
```

This small converter was adapted from the previous LOD experiment. It bakes node
transforms and copies base-color images; it is intended for ordinary scan assets,
not a general glTF conversion tool. Nexus 3 uses a different hierarchy and texture
baking pipeline, so its comparison cannot isolate the two prototype changes.

Validation:

```sh
node tools/benchmark/accounting.test.mjs
python3 tests/run_round1.py /absolute/path/build
```

Also run a model twice under two labels: identical captures and cache allocations
across fresh contexts check benchmark reproducibility.

## Current reconstruction exports

The current builder always uses reconstruction error and exposes
`--texture-error-divisor` (default 2). The paired driver now exports only
`reconstruction` (full baked sizes) and `reconstructionFine` (fine dimensions,
ratio 1), with the requested divisor on both. Run the targeted runner with
`--texture-error-divisor 1` to test the original round 4 contribution, or 2 for
the current default. Larger factors tighten texture sizing and refinement; values below 1 relax
quality. The factor is frozen in the manifest and scratch build
stamp, so resumed builds cannot silently reuse exports at another setting.

For historical round1/round2/fine controls, use the source and driver revisions
recorded in the reports: `e3d884c` for round 3, `322f90c` for round 4. The CSVs and
screenshots are preserved as historical measurements.

The PR-ready branch `decoupled_textures-code` excludes this benchmark tooling and
all measurement artifacts; see [commit separation](../../doc/texture-pr-preparation.md).

Use `--divisor-comparison --baseline-scratch PATH --baseline-report PATH` for
paired factor-1/factor-2 exports from one hierarchy and a frozen historical
round1 control. The driver exports `divisor1` and `divisor2` in addition to the
regular reconstruction variants. It validates factor 1 against the old round 4
semantic payloads before rendering. `texture-rounds-summary.py` can also check
allocations and PNGs with `--divisor-baseline BASELINE_REPORT`.
