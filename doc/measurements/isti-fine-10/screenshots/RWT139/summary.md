# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| round2 | 0 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| fine | 0 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| round1 | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| round2 | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| fine | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| round1 | 0 | 0.1 | 296 | 6.822 | 128.166 | 134.988 | 33.052 |
| round2 | 0 | 0.1 | 296 | 6.822 | 70.166 | 76.988 | 24.656 |
| fine | 0 | 0.1 | 296 | 6.822 | 50.138 | 56.960 | 21.077 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| round1 / source | 0 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| round1 / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| round1 / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| fine / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| round1 / source | 0 | 0.1 | textured | 40.07 | 1.872% | 0.99934 |
| round1 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 51.19 | 0.000% | 0.99962 |
| round2 / source | 0 | 0.1 | textured | 39.86 | 1.906% | 0.99949 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 38.68 | 3.303% | 0.99926 |
| fine / round2 | 0 | 0.1 | textured | 38.76 | 3.170% | 0.99938 |
| fine / source | 0 | 0.1 | textured | 39.68 | 1.896% | 0.99936 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
