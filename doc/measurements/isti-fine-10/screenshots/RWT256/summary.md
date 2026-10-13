# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 74 | 1.754 | 2.854 | 4.608 | 3.204 |
| round2 | 0 | 2 | 74 | 1.754 | 2.057 | 3.811 | 3.060 |
| fine | 0 | 2 | 74 | 1.754 | 1.746 | 3.500 | 2.994 |
| round1 | 0 | 0.5 | 152 | 3.510 | 11.604 | 15.114 | 7.524 |
| round2 | 0 | 0.5 | 152 | 3.510 | 8.495 | 12.005 | 7.063 |
| fine | 0 | 0.5 | 152 | 3.510 | 6.528 | 10.038 | 6.784 |
| round1 | 0 | 0.1 | 217 | 4.859 | 28.271 | 33.129 | 14.226 |
| round2 | 0 | 0.1 | 217 | 4.859 | 24.161 | 29.020 | 13.562 |
| fine | 0 | 0.1 | 217 | 4.859 | 17.472 | 22.331 | 12.048 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.23 | 45.827% | 0.99970 |
| round1 / source | 0 | 2 | shaded | 27.14 | 19.795% | 0.99972 |
| round2 / round1 | 0 | 2 | textured | 41.38 | 2.106% | 1.00000 |
| round2 / source | 0 | 2 | textured | 26.27 | 46.328% | 0.99970 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 27.14 | 19.795% | 0.99972 |
| fine / round1 | 0 | 2 | textured | 36.87 | 6.308% | 1.00000 |
| fine / round2 | 0 | 2 | textured | 39.10 | 3.196% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.24 | 47.963% | 0.99970 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 27.14 | 19.795% | 0.99972 |
| round1 / source | 0 | 0.5 | textured | 27.23 | 37.952% | 0.99991 |
| round1 / source | 0 | 0.5 | shaded | 27.73 | 17.319% | 0.99993 |
| round2 / round1 | 0 | 0.5 | textured | 42.46 | 1.559% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 27.23 | 38.658% | 0.99991 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 27.73 | 17.319% | 0.99993 |
| fine / round1 | 0 | 0.5 | textured | 38.10 | 4.833% | 1.00000 |
| fine / round2 | 0 | 0.5 | textured | 40.19 | 2.556% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 27.18 | 39.650% | 0.99991 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 27.73 | 17.319% | 0.99993 |
| round1 / source | 0 | 0.1 | textured | 27.63 | 34.492% | 1.00000 |
| round1 / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 49.59 | 0.190% | 1.00000 |
| round2 / source | 0 | 0.1 | textured | 27.62 | 34.719% | 1.00000 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 38.01 | 4.706% | 1.00000 |
| fine / round2 | 0 | 0.1 | textured | 38.24 | 4.243% | 1.00000 |
| fine / source | 0 | 0.1 | textured | 27.58 | 35.159% | 1.00000 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
