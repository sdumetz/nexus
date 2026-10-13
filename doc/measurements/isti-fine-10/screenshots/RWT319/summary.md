# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 28 | 0.632 | 2.396 | 3.027 | 2.201 |
| round2 | 0 | 2 | 28 | 0.632 | 2.396 | 3.027 | 2.201 |
| fine | 0 | 2 | 28 | 0.632 | 1.566 | 2.197 | 1.818 |
| round1 | 0 | 0.5 | 46 | 1.008 | 20.396 | 21.403 | 9.570 |
| round2 | 0 | 0.5 | 46 | 1.008 | 8.146 | 9.153 | 5.461 |
| fine | 0 | 0.5 | 46 | 1.008 | 4.970 | 5.978 | 4.108 |
| round1 | 0 | 0.1 | 46 | 1.008 | 20.396 | 21.403 | 9.570 |
| round2 | 0 | 0.1 | 46 | 1.008 | 8.146 | 9.153 | 5.461 |
| fine | 0 | 0.1 | 46 | 1.008 | 4.970 | 5.978 | 4.108 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 27.24 | 31.156% | 0.99993 |
| round1 / source | 0 | 2 | shaded | 35.20 | 6.450% | 0.99996 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 27.24 | 31.156% | 0.99993 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 35.20 | 6.450% | 0.99996 |
| fine / round1 | 0 | 2 | textured | 32.71 | 11.160% | 0.99998 |
| fine / round2 | 0 | 2 | textured | 32.71 | 11.160% | 0.99998 |
| fine / source | 0 | 2 | textured | 27.90 | 31.437% | 0.99993 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 35.20 | 6.450% | 0.99996 |
| round1 / source | 0 | 0.5 | textured | 31.90 | 15.035% | 0.99996 |
| round1 / source | 0 | 0.5 | shaded | 35.38 | 6.317% | 1.00000 |
| round2 / round1 | 0 | 0.5 | textured | 37.71 | 3.849% | 0.99999 |
| round2 / source | 0 | 0.5 | textured | 32.18 | 14.971% | 0.99997 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 35.38 | 6.317% | 1.00000 |
| fine / round1 | 0 | 0.5 | textured | 31.53 | 17.374% | 0.99996 |
| fine / round2 | 0 | 0.5 | textured | 32.68 | 11.814% | 0.99997 |
| fine / source | 0 | 0.5 | textured | 32.55 | 16.374% | 0.99997 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 35.38 | 6.317% | 1.00000 |
| round1 / source | 0 | 0.1 | textured | 31.90 | 15.035% | 0.99996 |
| round1 / source | 0 | 0.1 | shaded | 35.38 | 6.317% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 37.71 | 3.849% | 0.99999 |
| round2 / source | 0 | 0.1 | textured | 32.18 | 14.971% | 0.99997 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 35.38 | 6.317% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 31.53 | 17.374% | 0.99996 |
| fine / round2 | 0 | 0.1 | textured | 32.68 | 11.814% | 0.99997 |
| fine / source | 0 | 0.1 | textured | 32.55 | 16.374% | 0.99997 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 35.38 | 6.317% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
