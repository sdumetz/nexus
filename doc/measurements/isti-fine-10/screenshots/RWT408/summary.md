# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| round2 | 0 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| fine | 0 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| round1 | 0 | 0.5 | 279 | 6.403 | 11.625 | 18.028 | 14.650 |
| round2 | 0 | 0.5 | 279 | 6.403 | 11.625 | 18.028 | 14.650 |
| fine | 0 | 0.5 | 279 | 6.403 | 11.625 | 18.028 | 14.650 |
| round1 | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| round2 | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| fine | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| round1 / source | 0 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| round1 / source | 0 | 0.5 | textured | 32.45 | 17.954% | 0.99998 |
| round1 / source | 0 | 0.5 | shaded | 39.59 | 1.531% | 0.99998 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 32.45 | 17.954% | 0.99998 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 39.59 | 1.531% | 0.99998 |
| fine / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 32.45 | 17.954% | 0.99998 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 39.59 | 1.531% | 0.99998 |
| round1 / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| round1 / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
