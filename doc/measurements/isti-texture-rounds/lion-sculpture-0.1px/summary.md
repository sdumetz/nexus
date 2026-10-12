# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 0.1 | 296 | 6.822 | 128.166 | 134.988 | 33.052 |
| round2 | 0 | 0.1 | 296 | 6.822 | 70.166 | 76.988 | 24.656 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 0.1 | textured | 40.07 | 1.872% | 0.99934 |
| round1 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 51.19 | 0.000% | 0.99962 |
| round2 / source | 0 | 0.1 | textured | 39.86 | 1.906% | 0.99949 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
