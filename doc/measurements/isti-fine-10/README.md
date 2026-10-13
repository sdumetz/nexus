# Round 3: dimensions in multiples of four

**Historical benchmark:** reproduce with builder and driver from `e3d884c`. Current exports always use reconstruction error and cannot generate these footprint-mode controls. Existing CSVs and captures remain unchanged.

Compare round 1 (original sizes), round 2 (halving), and fine sizing, all exported from the **same hierarchy per model**. Ten models were chosen deliberately: the two previous lion cases, four prior quality outliers, and four cases with modest/no previous savings. This is not a representative collection estimate. Selection, source hashes, and binary hash are in `selection.json`.

At ratio 1, search a proportional sequence of dimensions with both axes rounded upward to multiples of four. Select the smallest candidate satisfying the existing maximum texel-footprint target. Minimum dimensions are 4x4. Zero targets, texture-dominated nodes, and unsupported unaligned baked inputs preserve their original dimensions. Current builders bake square power-of-two atlases; every fine texture in this sample is aligned. No changes to geometry, UVs, baking, JPEG quality, format, or traversal. Existing JS texture upload paths already support non-power-of-two images: WebGL2 generates mips; the WebGL1 fallback uses linear filtering without mips. This benchmark uses WebGL2 and counts full mip chains. `--texture-sizing halving` reproduces round 2; `fine` is the new default.

Same fixed 2.5-radius camera, 1280x800 viewport, unbounded cache, targets 2/0.5/0.1 px. Logical live WebGL allocations include complete mip chains; every allocation audit passed. All geometry payload hashes match, and fine/round 2 have identical geometry bytes, resident node counts, and shaded images at all 30 views.

| Requested error (px) | Median cache savings, fine vs halving | Byte-weighted savings | Models with >1% changed foreground pixels |
|---|---:|---:|---:|
| 2 | 0.00% | 6.73% | 3/10 |
| 0.5 | 7.56% | 9.67% | 6/10 |
| 0.1 | 22.92% | 21.69% | 9/10 |

Pixel changes mean maximum RGB difference >8/255, measured over the union of model foregrounds. These savings are **not equivalent-quality results**. Finer sizing exposes substantial slack in the halving rule, especially at fine views, but the unchanged ratio-1 footprint criterion permits visible detail loss. At 2 px six models still have identical images and no additional savings. Median source-relative PSNR changes versus halving are 0.000 dB at 2 px, -0.001 dB at 0.5 px, and -0.049 dB at 0.1 px; the worst decrease is -0.264 dB. These small PSNR changes coexist with larger pixel differences because both variants already differ from the source. Viewed rock captures show slight texture softening; the Kake difference image shows changes spread across its detailed surface.

`graph.csv` gives MiB and percentage columns; `aggregate.csv` gives summary statistics. `results.csv` is a long-form plotting table: one model/variant/requested-error row, bytes, exported texels, savings against earlier variants, and image comparisons including the original source. Empty PSNR with `identical=True` means infinite PSNR. Per-model JSON retains static artifacts and compact audited browser measurements. `screenshots/MODEL/gallery.html` provides side-by-side captures and differences.

Reproduce:

```sh
python3 tools/benchmark/build-pair.py BUILD_DIR --compile-only /tmp/nexus-fine-pair
python3 tools/benchmark/texture-rounds.py --dataset /path/ISTI_dataset --pair /tmp/nexus-fine-pair --node /path/node --out OUTPUT --scratch /tmp/nexus-texture-fine-10
```

Analytical sizing checks cover square/rectangular atlases, target satisfaction, minimality, zero targets, no upscaling, and the minimum dimensions. Binary exports test actual JPEG dimensions, orientation, geometry preservation, and legacy halving.
