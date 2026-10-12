# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| control | 0 | 0.5 | 99 | 2.525 | 2.062 | 4.587 | 4.026 |
| round1 | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| round2 | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| control / source | 0 | 0.5 | textured | 31.88 | 19.179% | 0.99908 |
| control / source | 0 | 0.5 | shaded | 42.05 | 0.682% | 0.99987 |
| round1 / control | 0 | 0.5 | textured | 31.22 | 20.460% | 0.99915 |
| round1 / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| round1 / control | 0 | 0.5 | shaded | 45.24 | 0.309% | 0.99992 |
| round1 / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| round2 / control | 0 | 0.5 | textured | 31.22 | 20.460% | 0.99915 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| round2 / control | 0 | 0.5 | shaded | 45.24 | 0.309% | 0.99992 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |

[Image gallery](gallery.html) · [Full measurements](results.json)
