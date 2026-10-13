# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 53 | 1.452 | 4.042 | 5.493 | 4.506 |
| divisor1 | 0 | 2 | 28 | 0.779 | 0.583 | 1.362 | 1.421 |
| divisor2 | 0 | 2 | 50 | 1.374 | 1.854 | 3.228 | 3.156 |
| round1 | 0 | 0.5 | 87 | 2.349 | 15.437 | 17.786 | 12.813 |
| divisor1 | 0 | 0.5 | 70 | 1.893 | 6.452 | 8.344 | 6.766 |
| divisor2 | 0 | 0.5 | 87 | 2.350 | 15.437 | 17.788 | 13.188 |
| round1 | 0 | 0.1 | 119 | 3.100 | 51.104 | 54.204 | 33.115 |
| divisor1 | 0 | 0.1 | 119 | 3.100 | 34.858 | 37.958 | 24.465 |
| divisor2 | 0 | 0.1 | 119 | 3.100 | 49.600 | 52.701 | 31.970 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.75 | 42.024% | 0.99945 |
| round1 / source | 0 | 2 | shaded | 31.18 | 14.640% | 0.99974 |
| divisor1 / round1 | 0 | 2 | textured | 25.29 | 43.278% | 0.99939 |
| divisor1 / source | 0 | 2 | textured | 25.07 | 53.959% | 0.99907 |
| divisor1 / round1 | 0 | 2 | shaded | 34.48 | 5.235% | 0.99974 |
| divisor1 / source | 0 | 2 | shaded | 29.69 | 18.543% | 0.99948 |
| divisor2 / round1 | 0 | 2 | textured | 33.67 | 6.069% | 0.99980 |
| divisor2 / divisor1 | 0 | 2 | textured | 24.92 | 45.481% | 0.99919 |
| divisor2 / source | 0 | 2 | textured | 26.62 | 43.898% | 0.99959 |
| divisor2 / round1 | 0 | 2 | shaded | 43.18 | 0.804% | 0.99988 |
| divisor2 / divisor1 | 0 | 2 | shaded | 34.33 | 5.591% | 0.99962 |
| divisor2 / source | 0 | 2 | shaded | 31.26 | 14.446% | 0.99985 |
| round1 / source | 0 | 0.5 | textured | 29.29 | 29.082% | 0.99939 |
| round1 / source | 0 | 0.5 | shaded | 31.67 | 13.345% | 0.99997 |
| divisor1 / round1 | 0 | 0.5 | textured | 30.57 | 15.106% | 0.99983 |
| divisor1 / source | 0 | 0.5 | textured | 28.16 | 33.786% | 0.99945 |
| divisor1 / round1 | 0 | 0.5 | shaded | 44.92 | 0.459% | 0.99997 |
| divisor1 / source | 0 | 0.5 | shaded | 31.52 | 13.814% | 0.99994 |
| divisor2 / round1 | 0 | 0.5 | textured | 38.91 | 3.577% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 30.64 | 14.386% | 0.99983 |
| divisor2 / source | 0 | 0.5 | textured | 29.39 | 28.595% | 0.99939 |
| divisor2 / round1 | 0 | 0.5 | shaded | 54.02 | 0.023% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 45.03 | 0.453% | 0.99997 |
| divisor2 / source | 0 | 0.5 | shaded | 31.66 | 13.350% | 0.99997 |
| round1 / source | 0 | 0.1 | textured | 32.04 | 18.838% | 0.99971 |
| round1 / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 32.61 | 14.399% | 0.99977 |
| divisor1 / source | 0 | 0.1 | textured | 31.65 | 20.960% | 0.99965 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | 36.05 | 6.404% | 0.99980 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 34.14 | 9.856% | 0.99985 |
| divisor2 / source | 0 | 0.1 | textured | 31.95 | 19.175% | 0.99968 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
