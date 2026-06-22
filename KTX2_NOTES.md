# KTX2 supercompressed textures in Nexus — prototype notes

Prototype enabling `.nxs` files whose node textures are KTX2 (Basis Universal:
ETC1S or UASTC) instead of JPEG, and rendering them in a THREE.js scene.

## What was built

1. **Baking** — `tools/nxs_ktx2.mjs`: an external Node script that rewrites the
   textures of an existing `.nxs` in place of touching the C++ `nxsbuild`.
2. **Rendering** — `html/js/nexus.js` + `nexus_three.js` changes that sniff each
   texture blob and, when it is KTX2, decode it through THREE's `KTX2Loader`.
3. **Verification** — `tools/serve.mjs` (range-capable static server),
   `html/ktx2.html` (demo), `tools/shoot.mjs` (headless screenshot).

### Which JS codebase
The repo ships two parallel viewers: the actively-maintained monolithic
`html/js/nexus.js` (global-script, `<script>`-tag, used by the committed demos)
and a newer ES-module npm package under `nexus3d/`. The KTX2 work targets
**`html/js/nexus.js`** — the mainline engine. (`nexus3d/` is left untouched.)

## Design choices

### Baking: external rewrite instead of patching nxsbuild
The C++ builder is a Qt project that writes node textures as JPEG
(`nexusbuilder.cpp`, `save()`). Modifying it means recompiling the whole
toolchain and threading an encoder through `extractNodeTex`. The `.nxs` layout
makes a post-process far cheaper, so the prototype rewrites an existing file.

On-disk layout (little-endian, confirmed against `src/common/dag.h` and the JS
reader `nexus3d/src/Mesh.js`):

```
Header (88)  | Node[n] (44 each) | Patch[n] (12) | Texture[n] (68) | <pad 256>
| node geometry chunks ... | texture blobs (each padded to 256) ...
```

- All file offsets are stored in units of `NEXUS_PADDING = 256`.
- The texture table has `n_textures` entries; the last is a **sentinel** whose
  offset marks end-of-data. Real textures = `n_textures - 1`. Texture `i` spans
  `[textures[i].offset*256, textures[i+1].offset*256)`.
- A `Texture` entry is a `u32` offset followed by a 64-byte projection matrix;
  only the offset changes on rewrite.

Because texture blobs are the **tail** of the file (after all geometry), the
rewrite is clean: keep bytes `[0, textures[0].offset*256)` verbatim, patch the
`u32` offset field of each texture-table entry, and append the new KTX2 blobs
(each zero-padded to 256). Node offsets are unaffected.

The script shells out to the `ktx` CLI (POC-grade `exec`, per the brief).
Default codec is **ETC1S (`basis-lz`)** — on the test model it produced
textures smaller than the source JPEGs (e.g. 58 KB → 31 KB) while being
GPU-native. `--encode uastc` (UASTC + zstd) is available for higher quality.

### Texture orientation
The JPEG path uploads with `UNPACK_FLIP_Y_WEBGL = true`. Compressed textures
cannot be flipped at upload, so the bake stores them bottom-up via
`ktx create --convert-texcoord-origin bottom-left`. The decoded KTX2 then
matches the existing UV convention with no shader/UV changes (verified: KTX2 and
JPEG renders are visually identical in orientation and content).

### Format detection: magic bytes
Per the brief, no format field was added to the `.nxs` header. The renderer
sniffs the first 12 bytes of each texture blob for the KTX2 identifier
(`AB 4B 54 58 20 32 30 BB 0D 0A 1A 0A`); anything else takes the existing image
path. This is intentionally minimal, not future-proof.

### Rendering: reuse KTX2Loader, extract the raw GL handle
Nexus does **not** use THREE's material/texture system for node textures — it
uploads them with raw `gl.texImage2D` and binds raw `WebGLTexture` handles
(`m.texids[texid]`) during its own draw pass. So a THREE `CompressedTexture`
can't be used directly. The integration:

1. `loadNodeTexture` (nexus.js) sniffs the first 12 bytes of the blob. KTX2 +
   an available loader → `loadNodeTextureKTX2`; otherwise the existing
   `createImageBitmap` path (refactored out as `loadNodeTextureImage`).
2. `loadNodeTextureKTX2` calls `KTX2Loader.parse(buffer)` to transcode, then
   `renderer.initTexture(texture)` to force the GPU upload, then stores
   `renderer.properties.get(texture).__webglTexture` in `m.texids[texid]` — the
   same slot the renderer already binds.
3. The THREE texture object is retained in `m.tex3d[texid]` so THREE keeps
   ownership of the GPU resource; the delete path calls `.dispose()` for those.

This reuses THREE's whole Basis transcoder worker pipeline with no fork.

### Injecting the loader (global-script constraint)
`nexus.js`/`nexus_three.js` are classic `<script>` libraries — they can't
`import` the `KTX2Loader` ES module. So the loader is **injected by the app**:
`NexusObject(url, onLoad, onUpdate, renderer, material, { ktx2Loader })` stashes
`{ renderer, loader }` on the per-gl context (`context.ktx2`), which
`loadNodeTexture` reads. The app (a module script, e.g. the demo) creates the
loader: `new KTX2Loader().setTranscoderPath(...).detectSupport(renderer)`.
No KTX2 loader injected → KTX2 blobs simply aren't decodable (graceful).

### Scope / shortcuts (intentional)
- Only THREE.js integration; no path for non-THREE consumers.
- The demo loads one shared THREE (CDN, via importmap), sets it as the global
  `window.THREE`, then loads the classic nexus scripts — avoiding two THREE
  copies (which would break `instanceof`/`initTexture`).
- The demo passes an **explicit material** so `nexus_three.js`'s legacy
  auto-material code (which uses `THREE.RGBFormat`/`VertexColors`, removed from
  modern three) is skipped.
- Transcoder path is set by the app on the `KTX2Loader` (demo uses a jsDelivr CDN).
- Source textures aren't multiple-of-four → benign transcoder warning (it pads).
- Deepzoom `.nxs` is rejected by the rewrite tool; corto-compressed geometry is
  orthogonal and unaffected (the test model is uncompressed).
- Color management differs slightly between paths: the legacy JPEG upload uses a
  linear `RGBA` internal format, while KTX2 (baked `*_SRGB`) is uploaded as
  sRGB by three. The KTX2 path is the more correct one; matching them is out of
  scope for the prototype.

## Usage

Bake:
```
node tools/nxs_ktx2.mjs in.nxs out.nxs            # ETC1S (default)
node tools/nxs_ktx2.mjs in.nxs out.nxs --encode uastc
```

Verify in a browser:
```
node tools/serve.mjs . 8080
# open http://localhost:8080/html/ktx2.html?model=models/out.nxs
```

Headless screenshot:
```
node tools/shoot.mjs models/out.nxs /tmp/shot.png
```

## Files changed / added
- `tools/nxs_ktx2.mjs` — bake script (new)
- `tools/serve.mjs`, `tools/shoot.mjs`, `html/ktx2.html` — demo/verify (new)
- `html/js/nexus.js` — magic-byte sniff, `loadNodeTextureKTX2`, dispose path
- `html/js/nexus_three.js` — `ktx2Loader` injection via `NexusObject`

## Future (deferred)
- Add an image-format field to the `.nxs` header instead of magic-byte sniffing.
- Encode KTX2 directly in `nxsbuild` instead of post-processing.
