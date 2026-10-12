# ISTI texture rounds: cache residency and rendered quality

The experiment commits were rebased cleanly onto `v4-fixes` (`1fe489d`):
round 1 is `9386ec4`, round 2 is `f763879`. Ratio 1 is unchanged. Both rebuilt
and passed the analytical/export/JPEG tests after the rebase.

Use the [benchmark harness](../../../tools/benchmark/README.md) to reproduce these
measurements. Performance is outside scope. Chromium/SwiftShader, three.js 186,
1280×800 pixels, standardized lighting, an infinite Nexus cache, disabled FPS
adaptation and suppressed below-target prefetch were used throughout. Each
measurement starts a fresh browser document and GL context. All allocation
audits passed; the JSON files record the exact browser, cameras, hashes and counts.

## Models and controls

These are moderate single-texture scans from the local ISTI dataset:

| Dataset | Model | Triangles | Source texture | Attribution from dataset metadata |
|---|---|---:|---|---|
| RWT139 | Lion Sculpture | 75,901 | 4096×4096 | GSXNet; CC Attribution-NonCommercial |
| RWT408 | Lion Skull | 110,188 | 2048×2048 | Auckland Museum; CC Attribution |

Source location: `/home/sebastien/Documents/3DModels/ISTI_dataset/`.
[Provenance](provenance.json) preserves the dataset metadata, attribution/source
URLs, artifact hashes, and original/exported texture dimensions for every node.

The primary **control** is an unchanged build of `v4-fixes`. Source glTF was
converted to OBJ once, then the same OBJ was fed to each builder using defaults.
Rounds 1 and 2 were exported from one hierarchy using the paired-export driver.
The control was built separately, but all three artifacts have identical decoded
geometry/UV/normal payload hashes. Control and round 1 additionally have identical
texture payload hashes. This verifies that their differences are stored errors
and resulting traversal, rather than a different bake.

**nexus3** is the installed older Nexus 3 builder, using `-c` (no vertex colors)
and its defaults on the same OBJ. Its hierarchy and bake differ from v4; its
comparison measures the whole pipeline, not the isolated effect of either round.
The full-resolution glTF supplies an additional quality reference.

## Ordinary fixed views, target 2 pixels

Views 0, 1 and 2 place the camera at 6, 2.5 and 1.2 bounding-sphere radii along
the same direction. Cache values are MiB of logical live Nexus GPU storage,
including exact mip chains and loaded ancestors, not CPU memory or physical VRAM.

| Model | View | v4-fixes | Round 1 | Round 2 | Nexus 3 |
|---|---:|---:|---:|---:|---:|
| Sculpture | 0 | 0.174 | 0.851 | 0.851 | 6.981 |
| Sculpture | 1 | 1.076 | 3.273 | 3.273 | 112.788 |
| Sculpture | 2 | 3.709 | 9.147 | 9.147 | 244.565 |
| Skull | 0 | 0.491 | 1.755 | 1.755 | 11.741 |
| Skull | 1 | 2.346 | 4.647 | 4.647 | 52.646 |
| Skull | 2 | 6.572 | 9.879 | 9.879 | 52.646 |

Round 1 increases residency relative to v4-fixes because its combined error
requests more detail. Visual inspection shows sharper photographic detail; both
textured and shaded comparisons improve against the source. At view 1, textured
PSNR against the source improves from 27.94 to 31.34 dB for the sculpture, and
from 24.81 to 26.56 dB for the skull. These are improvements, not proof that the
error corresponds to a strict two-pixel perceptual bound.

Round 2 has **no cache or image effect at any of these six model/view pairs**.
Its PNGs are byte-identical to round 1 in both textured and shaded modes. The
sculpture's resized textures belong to its finest level, and none are requested
in these cuts. The skull does not resize at ratio 1.

Nexus 3 is substantially heavier but also visibly sharper than v4 at these
settings. For example, view 1 source-relative textured PSNR is 37.50 dB for the
sculpture and 34.58 dB for the skull. Its large cache cannot be presented as an
equal-quality saving achieved by this prototype.

- Sculpture: [measurements](lion-sculpture/summary.md), [gallery](lion-sculpture/gallery.html), [JSON](lion-sculpture/results.json).
- Skull: [measurements](lion-skull/summary.md), [gallery](lion-skull/gallery.html), [JSON](lion-skull/results.json).

## Export sizing and higher-detail view

The sculpture shrinks 58 of its 296 textures, all in the finest level. Stored
base texels decrease from 25,198,592 to 13,795,328 (**45.25%**), and NXS bytes
from 9,999,360 to 9,118,976 (**8.80%**). The skull's 294 textures, 2,531,328 base
texels, and 8,069,632-byte file stay unchanged.

At view 1 with a 0.5-pixel target, round 1 and round 2 still request the same 158
nodes, none resized, and both use 13.802 MiB. Their captures are identical.
[Measurements and images](lion-sculpture-0.5px/summary.md).

At the same camera with a **0.1-pixel target**, all 296 nodes are resident:

| Round | Geometry MiB | Texture MiB including mips | Total MiB |
|---|---:|---:|---:|
| Round 1 | 6.822 | 128.166 | 134.988 |
| Round 2 | 6.822 | 70.166 | 76.988 |

Round 2 saves **58 MiB / 42.97%** of total cache in this full-detail case. Both
runs load exactly the same nodes; shaded images are identical. Textured images
have 51.19 dB PSNR between them and mean absolute channel difference 0.375/255;
no model pixel exceeds the 8/255 channel-difference threshold. Visual inspection
shows no meaningful change at this tested camera and viewport. Against the
source, textured PSNR changes from 40.07 to 39.86 dB. This is a small measured
loss, not mathematically identical texture output or a guarantee for other views.
[Measurements](lion-sculpture-0.1px/summary.md),
[gallery](lion-sculpture-0.1px/gallery.html),
[JSON](lion-sculpture-0.1px/results.json).

The reported silhouette IoU uses a background-color foreground mask. It is an
approximation and can change slightly with texture color at edge pixels even
when geometry is identical; the shaded comparison isolates geometry more cleanly.

## Accounting findings

The existing module viewer's texture estimate uses ten times encoded texture
ranges. It can undercount or overcount; it is not an authoritative residency
measure. At sculpture view 1, Nexus 3 reports **44.403 MiB** against the audited
**112.788 MiB**, a 60.6% underestimate. Conversely, skull round 1 reports
4.809 MiB against 4.647 MiB. Exact live handle accounting agrees independently
with decoded geometry counts and unique texture/image/mip dimensions.

[PR #178](https://github.com/cnr-isti-vclab/nexus/pull/178) concerns the classic
viewer, while this benchmark uses the module runtime. Its concern about decoded
texture residency applies here too. The harness records both numbers rather
than silently treating the existing estimate as accurate. Native nxsview would
also need an audit because its texture counter uses RGB base-image bytes.

## Validation and scope

The four allocation/image unit checks and the rebased round 1/round 2 C++ suite
passed. Repeating the skull artifact under another label in a fresh context
produced identical GPU allocations and textured/shaded images. The standard
runs completed with all required nodes ready and no GL/browser errors. A browser
profile cleanup race after the sculpture run was fixed with bounded removal
retries; its measurements were already complete and its summary was regenerated
from the recorded JSON. Two concurrent supplemental attempts were terminated
before completion and are excluded; supplemental comparisons were rerun alone.

The earlier Chauvet case is diagnostic only. Pichet and Marsoulas attempts on the
pre-rebase code failed during building; they are not benchmark results. The ISTI
models above both build successfully on the stability fixes.

These results establish a useful full-detail saving on one moderate model, but
not a general fourfold saving or an independent texture LOD system. Ratio 1 is
conservative and only changes finest-level sizes on the sculpture. It produces
no savings in the tested ordinary LOD cuts; selecting more useful intermediate
texture resolutions remains an open follow-up. Keeping the combined error in
the existing field does work without a file-format or production-viewer update.
