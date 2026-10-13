# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 53 | 1.452 | 4.042 | 5.493 | 4.506 |
| round2 | 0 | 2 | 53 | 1.452 | 4.042 | 5.493 | 4.506 |
| fine | 0 | 2 | 53 | 1.452 | 4.042 | 5.493 | 4.506 |
| round1 | 0 | 0.5 | 87 | 2.349 | 15.437 | 17.786 | 12.813 |
| round2 | 0 | 0.5 | 87 | 2.349 | 15.437 | 17.786 | 12.813 |
| fine | 0 | 0.5 | 87 | 2.349 | 15.318 | 17.667 | 12.696 |
| round1 | 0 | 0.1 | 119 | 3.100 | 51.104 | 54.204 | 33.115 |
| round2 | 0 | 0.1 | 119 | 3.100 | 45.104 | 48.204 | 29.878 |
| fine | 0 | 0.1 | 119 | 3.100 | 34.858 | 37.958 | 24.465 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.75 | 42.024% | 0.99945 |
| round1 / source | 0 | 2 | shaded | 31.18 | 14.640% | 0.99974 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 26.75 | 42.024% | 0.99945 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 31.18 | 14.640% | 0.99974 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.75 | 42.024% | 0.99945 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 31.18 | 14.640% | 0.99974 |
| round1 / source | 0 | 0.5 | textured | 29.29 | 29.082% | 0.99939 |
| round1 / source | 0 | 0.5 | shaded | 31.67 | 13.345% | 0.99997 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 29.29 | 29.082% | 0.99939 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 31.67 | 13.345% | 0.99997 |
| fine / round1 | 0 | 0.5 | textured | 43.67 | 1.179% | 1.00000 |
| fine / round2 | 0 | 0.5 | textured | 43.67 | 1.179% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 29.29 | 29.013% | 0.99939 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 31.67 | 13.345% | 0.99997 |
| round1 / source | 0 | 0.1 | textured | 32.04 | 18.838% | 0.99971 |
| round1 / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 47.97 | 0.041% | 0.99994 |
| round2 / source | 0 | 0.1 | textured | 31.91 | 19.465% | 0.99965 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 32.61 | 14.399% | 0.99977 |
| fine / round2 | 0 | 0.1 | textured | 32.75 | 13.757% | 0.99971 |
| fine / source | 0 | 0.1 | textured | 31.65 | 20.960% | 0.99965 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
