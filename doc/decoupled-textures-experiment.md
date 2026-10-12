# Decoupled textures with the existing Nexus container

## Conclusion

Yes. Independent texture resolution and shared texture resources can fit the existing
Nexus container. The geometry DAG need not change, and the existing patch texture
reference is already the required indirection. The main changes are to texture
authoring, resource scheduling, and rendering. A small metadata extension becomes
useful for efficient selection and shared coarse-image fallbacks; a wholesale new
geometry format is unnecessary.

There are two distinct experiments:

1. Select and stream mips of the existing per-node textures. This keeps the current
   UVs and DAG and isolates the benefit of independent texture resolution.
2. Use stable texture pages across geometry levels. This removes repeated node
   atlases, but requires changing how the builder carries or projects UVs.

The first is the least disruptive starting point. It does not establish the savings
of the second. Neither mip streaming nor shared pages has been implemented or
measured in this worktree yet. [Round 1](round1-combined-error.md) implements the
preceding builder-only step: combining geometry and texture error in one field.

## Evidence and scope

The [Nexus benchmark](../../not-voyager/experiments/LOD/reports/10-nexus-benchmark.md)
measured median Nexus 3 / experimental-loader ratios of 3.96 for resident texels,
12.2 for GPU bytes, and 2.88 for required transfer bytes at equal textured PSNR.
Those are comparisons of delivered systems, with differences in geometry, texture
encoding, and loading policy. They are not an isolated causal measurement of
decoupling, nor a guaranteed 4x reduction on this branch. Resident texels also differ
from cumulative uploaded texels: replacement uploads and eviction can increase the
latter without increasing the former.

The [KTX2 prototype](../../nexus-ktx/KTX2_NOTES.md) demonstrates replacement of JPEG
blobs with KTX2 while retaining Nexus index record layouts. It targets the classic
`html/js/nexus.js` viewer, not the ES-module `nexus3d/src` implementation. Its whole
texture parse/upload does not yet provide mip streaming.

This worktree contains the v4 builder. Its behavior at the start of the experiment
matters independently of the Nexus 3 benchmark:

- [ExportNxs](../src/nxsbuild/export_nxs.cpp) writes version 2 files, creates one
  JPEG per micronode, and assigns that texture ID to all the node's patches.
- [MeshHierarchy](../src/core/mesh_hierarchy.cpp) chooses simplification strength
  partly from the texel/triangle ratio and drops textures during geometry merging.
- [Reparameterization](../src/texture/parametrization.cpp) creates new UV layouts
  and rebakes images at every geometry level. It also scales the destination node
  error using its triangle/texel ratio.

Thus even after runtime separation, a builder comparison must account for the
texture-dependent geometry and error settings.

## What the format already supports

The records in [dag.h](../src/common/dag.h) are:

| Record | Bytes | Relevant contents |
|---|---:|---|
| Header | 88 | Counts, signature, version, model sphere |
| Node | 44 | Geometry offset, counts, error, bounds, first patch |
| Patch | 12 | Replacement child, triangle-run end, texture ID |
| Texture | 68 | Blob offset and projection matrix |

Offsets use 256-byte units. Texture ranges are delimited by the next texture
entry, including a final sentinel. A texture ID is not required by the record
layout to equal a node ID, and several patches or nodes can reference the same
texture. A blob can hold a complete KTX2 mip chain; its internal level index can
describe byte ranges without adding a Nexus entry for each mip.

For explicit UVs, a page shared by many nodes needs no new binding field if all
those nodes already store UVs in that page's normalized coordinate system.
Sampling a lower mip of the same page uses exactly the same UVs.

The format is more general than the current browser loaders:

- Both [Cache.js](../nexus3d/src/Cache.js) and the
  [classic loader](../html/js/nexus.js) request the first patch's texture as the
  node texture. Readiness and eviction are tied to node lifetime.
- Both browser index readers approximate texture memory as ten times encoded
  bytes and add that cost to each node. Shared resources need separate accounting.
- The classic draw loop merges triangle runs without correctly making texture
  changes a merge boundary. Multiple texture IDs within one node require fixing
  this, not merely changing the patch table.
- The native [loader](../src/common/nexusdata.cpp) already iterates patch texture
  references and counts users, but still loads complete images with node geometry.

The projection matrix is used by the native renderer for projected texturing.
It should not be repurposed as arbitrary mip or resource metadata.

## Experiment A: independent mips of current node atlases

Retain all geometry, patch IDs, UVs, and texture identities. Replace each JPEG
with a KTX2 containing its mip chain using the sibling prototype's rewrite approach.
Keep sentinel and padding rules, and verify all node byte ranges when rewriting:
the v4 exporter places the sink offset after textures, so the final real node's
inferred range can include the texture tail. It is not sufficient to assume that
every node range ends before the textures.

Introduce texture resources keyed by `(mesh, texture ID)`, with independent
request, transcode, upload, residency, and eviction state. Deduplicate requests
and maintain all waiting geometry users. Deleting one user must not abort a
resource needed by another. Geometry may refine once its required textures have
a usable coarse mip; it must not wait for their finest levels.

Choose texture detail from projected texel size, with its own pixel threshold.
For an initial implementation derive world-units-per-texel conservatively from
triangle positions and UV gradients after geometry decode, and aggregate demand
over visible drawn runs and all instances. Use bounds for distance, hysteresis
for level changes, and defined handling of degenerate UVs and the camera inside
bounds. Node geometry error is not a texture-density metric. A later baked metric
can avoid repeatedly deriving it and permit selection before geometry arrives.

Load KTX2 metadata and the coarse mip tail first, then finer level byte ranges.
The existing LOD [runtime](../../not-voyager/experiments/LOD/docs/runtime.md)
demonstrates subset reconstruction for `KTX2Loader`: retain codebooks and selected
image descriptors for ETC1S, rewrite dimensions and level indexes, and preserve
payload alignment. A level payload alone is not a decodable ETC1S KTX2 file.
UASTC and ETC1S must be tested separately.

Account actual transcoded block sizes, mip levels, geometry allocations, and
in-flight reservations in a common GPU budget. Track CPU and persistent encoded
cache bytes separately. Never infer GPU cost from JPEG size or KTX2
`uncompressedByteLength`. Measure replacement upload cost as well as steady-state
memory: rebuilding a GPU chain can upload already resident coarse mips again.

**Container impact:** unchanged Nexus record layouts; new texture payload type.
**Expected benefit:** fewer resident texels than whole-node uploads in distant
views, plus compressed GPU storage. **Limit:** every geometry level still owns
its rebaked atlas, so this does not remove cross-level duplication or allow a
coarse node to use detail absent from its baked image.

## Experiment B: stable pages shared across geometry levels

Assign texture domains independently of geometry nodes. Retain source-image
domains where practical, or bake regional pages once. Preserve seams and tile
ownership through simplification, or project simplified geometry into the same
stable domains. Existing geometry-only merging and per-level atlas creation
cannot do this unchanged. Merely redirecting existing coarse texture IDs to fine
textures would render incorrect images.

For each node, order triangles by `(replacement child, texture page)` and emit
one patch per run. Multiple patches may name the same replacement child; retain
their coverage and require all its runs to disappear together when that child
replaces them. Duplicate wedges where a UV/page seam needs different coordinates.
Maintain the node's 16-bit vertex and face count limits. Extra patch records cost
12 bytes each, and more runs may increase draw calls; this must be measured.

Each page is a single texture-table entry containing one KTX2 chain. Patches at
different geometry depths refer to it using page-space UVs. Geometry traversal
still determines surface coverage; texture scheduling determines the mip used
to shade that coverage. No texture parent relation is inferred from geometry
edges, which do not describe UV placement.

**Container impact:** unchanged record layouts, changed counts/references and
geometry UV payloads. **Implementation impact:** substantial builder work plus
multi-texture loading and drawing. **Potential benefit:** one authored image
chain per stable page rather than a separately baked atlas per geometry node.

Mips replace lower-resolution copies only within a stable image domain. The
current differently packed coarse atlases are not those copies. Likewise, the
source-image pyramid used as an out-of-core baking cache is distinct from the
on-disk hierarchy and need not be removed for this experiment.

## Where a small extension helps

For A and B, KTX2 already describes dimensions, encodings and level ranges.
Texture demand can initially be derived at runtime. Use an optional experimental
sidecar keyed by texture/patch IDs for baked support bounds and texel scale if
needed; specify its asset identity so stale metadata is rejected. This keeps
the initial Nexus container unchanged and makes the metadata schema reviewable
before embedding it.

Shared coarse images spanning several fine pages need more: an explicit parent
resource ID and child-to-parent UV scale/offset, plus the levels each resource
covers. Those relationships cannot generally be recovered from the current
tables. The [coarse-texture report](../../not-voyager/experiments/LOD/reports/25-coarse-texture-hierarchy.md)
and [resource-forest report](../../not-voyager/experiments/LOD/reports/27-texture-resource-forest.md)
also show that packet boundaries can change filtering and that sharing has GPU
memory and encoding-overhead tradeoffs.

If measurements justify this step, embed a versioned texture extension after
the existing index and before payloads, and update stored offsets. Retain the
88/44/12/68-byte core records. Define extension length, resource records, optional
binding transforms, and feature requirements explicitly. Ordinary page-space
bindings need no transform; bindings through a shared coarse parent do.
Do not store an extension in alignment slack or overload existing matrix fields.

Layout compatibility does not imply old-reader compatibility. Legacy JPEG
decoders cannot read KTX2; current readers do not consistently reject unknown
header versions or flags. Updated readers must validate features, and legacy
clients need a separate compatible artifact or an unmistakably rejected format
identifier. Audit `nxsedit`/compression rewrites before allowing them on extended
files: copying known tables and blobs is not enough to preserve new metadata.

## Controlled measurement

Start on one ordinary scan and one texture-dominant scan, then expand to the
benchmark collection. Keep the geometry cut, camera, shading, and quantization
fixed when measuring A; compare B separately because UV authoring may affect
simplification and vertex counts.

| Variant | Purpose |
|---|---|
| Original JPEG, whole node textures | Baseline |
| Original node atlases, KTX2, whole chains | Isolate encoding/GPU compression |
| Same KTX2 atlases, independently selected mips | Isolate resolution selection |
| Same atlases, mip range fetching | Isolate transfer/cache savings |
| Stable shared pages, independently streamed mips | Measure cross-level sharing |
| Optional shared coarse resources | Measure first-frame/request/draw tradeoffs |

Compare at equal measured image quality, including an all-finest-textures image
for each geometry cut to separate texture selection error from geometry error.
Record resident texels, actual GPU bytes, cumulative upload texels/bytes, encoded
cache size, transfer bytes, requests, first frame, settle time, draw calls, and
frame stalls. Report ETC1S's quality ceiling and test UASTC where it matters.
Keep prefetch policy and frame-rate adaptation controlled and apply the viewport
fix from the benchmark harness if testing the ES-module three.js integration.

Validate mixed geometry cuts, multi-page nodes, shared users, failed requests,
eviction during requests, camera motion, seams, and mixed mip levels. Check
texture ranges/sentinels and KTX2 decoding independently of rendering. For B,
verify coverage and cracks after patch splitting, rather than assuming repeated
child references are harmless to every consumer.

The decision after A is whether per-node mip selection captures enough of the
benefit. Proceed to B if persistent atlas duplication, regional over-fetch, or
insufficient coarse-node texture detail remains material. Add a texture forest
only if the shared-page measurements justify its extra metadata and filtering
rules.
