# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 38 | 0.815 | 19.729 | 20.544 | 4.397 |
| round2 | 0 | 2 | 38 | 0.815 | 3.479 | 4.294 | 2.297 |
| fine | 0 | 2 | 38 | 0.815 | 1.987 | 2.802 | 1.911 |
| round1 | 0 | 0.5 | 57 | 1.207 | 87.062 | 88.269 | 15.157 |
| round2 | 0 | 0.5 | 57 | 1.207 | 9.562 | 10.769 | 4.595 |
| fine | 0 | 0.5 | 57 | 1.207 | 5.154 | 6.361 | 3.536 |
| round1 | 0 | 0.1 | 57 | 1.207 | 87.062 | 88.269 | 15.157 |
| round2 | 0 | 0.1 | 57 | 1.207 | 9.562 | 10.769 | 4.595 |
| fine | 0 | 0.1 | 57 | 1.207 | 5.154 | 6.361 | 3.536 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 36.29 | 5.596% | 0.99985 |
| round1 / source | 0 | 2 | shaded | 36.35 | 1.135% | 0.99989 |
| round2 / round1 | 0 | 2 | textured | 41.67 | 1.290% | 0.99999 |
| round2 / source | 0 | 2 | textured | 36.14 | 6.311% | 0.99986 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 36.35 | 1.135% | 0.99989 |
| fine / round1 | 0 | 2 | textured | 36.53 | 5.865% | 0.99997 |
| fine / round2 | 0 | 2 | textured | 37.76 | 3.806% | 0.99998 |
| fine / source | 0 | 2 | textured | 36.18 | 7.061% | 0.99986 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 36.35 | 1.135% | 0.99989 |
| round1 / source | 0 | 0.5 | textured | 38.56 | 3.356% | 0.99997 |
| round1 / source | 0 | 0.5 | shaded | 37.21 | 1.041% | 1.00000 |
| round2 / round1 | 0 | 0.5 | textured | 42.88 | 0.699% | 0.99999 |
| round2 / source | 0 | 0.5 | textured | 37.87 | 3.865% | 0.99998 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 37.21 | 1.041% | 1.00000 |
| fine / round1 | 0 | 0.5 | textured | 36.81 | 5.112% | 0.99998 |
| fine / round2 | 0 | 0.5 | textured | 37.71 | 3.801% | 0.99999 |
| fine / source | 0 | 0.5 | textured | 37.61 | 4.260% | 0.99999 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 37.21 | 1.041% | 1.00000 |
| round1 / source | 0 | 0.1 | textured | 38.56 | 3.356% | 0.99997 |
| round1 / source | 0 | 0.1 | shaded | 37.21 | 1.041% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 42.88 | 0.699% | 0.99999 |
| round2 / source | 0 | 0.1 | textured | 37.87 | 3.865% | 0.99998 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 37.21 | 1.041% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 36.81 | 5.112% | 0.99998 |
| fine / round2 | 0 | 0.1 | textured | 37.71 | 3.801% | 0.99999 |
| fine / source | 0 | 0.1 | textured | 37.61 | 4.260% | 0.99999 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 37.21 | 1.041% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
