# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 80 | 2.473 | 3.167 | 5.639 | 5.420 |
| round2 | 0 | 2 | 80 | 2.473 | 3.167 | 5.639 | 5.420 |
| fine | 0 | 2 | 80 | 2.473 | 3.167 | 5.639 | 5.420 |
| round1 | 0 | 0.5 | 154 | 4.487 | 24.833 | 29.320 | 21.066 |
| round2 | 0 | 0.5 | 154 | 4.487 | 24.833 | 29.320 | 21.066 |
| fine | 0 | 0.5 | 154 | 4.487 | 24.833 | 29.320 | 21.066 |
| round1 | 0 | 0.1 | 221 | 6.077 | 95.166 | 101.244 | 60.142 |
| round2 | 0 | 0.1 | 221 | 6.077 | 76.166 | 82.244 | 50.638 |
| fine | 0 | 0.1 | 221 | 6.077 | 60.205 | 66.283 | 42.176 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.39 | 48.681% | 0.99879 |
| round1 / source | 0 | 2 | shaded | 29.20 | 20.090% | 0.99884 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 26.39 | 48.681% | 0.99879 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 29.20 | 20.090% | 0.99884 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.39 | 48.681% | 0.99879 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 29.20 | 20.090% | 0.99884 |
| round1 / source | 0 | 0.5 | textured | 29.65 | 28.911% | 0.99970 |
| round1 / source | 0 | 0.5 | shaded | 29.88 | 18.344% | 0.99976 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 29.65 | 28.911% | 0.99970 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 29.88 | 18.344% | 0.99976 |
| fine / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 29.65 | 28.911% | 0.99970 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 29.88 | 18.344% | 0.99976 |
| round1 / source | 0 | 0.1 | textured | 31.92 | 19.423% | 0.99998 |
| round1 / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 47.95 | 0.006% | 1.00000 |
| round2 / source | 0 | 0.1 | textured | 31.78 | 20.139% | 0.99998 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 32.70 | 16.745% | 0.99996 |
| fine / round2 | 0 | 0.1 | textured | 32.78 | 16.297% | 0.99996 |
| fine / source | 0 | 0.1 | textured | 31.64 | 21.067% | 0.99998 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
