# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 74 | 1.754 | 2.854 | 4.608 | 3.204 |
| divisor1 | 0 | 2 | 62 | 1.466 | 1.059 | 2.524 | 2.313 |
| divisor2 | 0 | 2 | 70 | 1.665 | 1.993 | 3.659 | 2.854 |
| round1 | 0 | 0.5 | 152 | 3.510 | 11.604 | 15.114 | 7.524 |
| divisor1 | 0 | 0.5 | 132 | 3.052 | 4.394 | 7.445 | 5.442 |
| divisor2 | 0 | 0.5 | 141 | 3.255 | 7.996 | 11.251 | 6.365 |
| round1 | 0 | 0.1 | 217 | 4.859 | 28.271 | 33.129 | 14.226 |
| divisor1 | 0 | 0.1 | 217 | 4.859 | 17.472 | 22.331 | 12.048 |
| divisor2 | 0 | 0.1 | 217 | 4.859 | 25.983 | 30.842 | 13.875 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.23 | 45.827% | 0.99970 |
| round1 / source | 0 | 2 | shaded | 27.14 | 19.795% | 0.99972 |
| divisor1 / round1 | 0 | 2 | textured | 32.90 | 12.041% | 1.00000 |
| divisor1 / source | 0 | 2 | textured | 25.96 | 50.361% | 0.99970 |
| divisor1 / round1 | 0 | 2 | shaded | 36.81 | 2.670% | 1.00000 |
| divisor1 / source | 0 | 2 | shaded | 26.76 | 21.264% | 0.99972 |
| divisor2 / round1 | 0 | 2 | textured | 40.42 | 2.334% | 1.00000 |
| divisor2 / divisor1 | 0 | 2 | textured | 33.29 | 10.319% | 1.00000 |
| divisor2 / source | 0 | 2 | textured | 26.26 | 45.890% | 0.99970 |
| divisor2 / round1 | 0 | 2 | shaded | 60.01 | 0.019% | 1.00000 |
| divisor2 / divisor1 | 0 | 2 | shaded | 36.84 | 2.651% | 1.00000 |
| divisor2 / source | 0 | 2 | shaded | 27.14 | 19.804% | 0.99972 |
| round1 / source | 0 | 0.5 | textured | 27.23 | 37.952% | 0.99991 |
| round1 / source | 0 | 0.5 | shaded | 27.73 | 17.319% | 0.99993 |
| divisor1 / round1 | 0 | 0.5 | textured | 34.97 | 8.691% | 0.99991 |
| divisor1 / source | 0 | 0.5 | textured | 26.99 | 41.250% | 0.99981 |
| divisor1 / round1 | 0 | 0.5 | shaded | 46.92 | 0.246% | 0.99993 |
| divisor1 / source | 0 | 0.5 | shaded | 27.70 | 17.398% | 0.99986 |
| divisor2 / round1 | 0 | 0.5 | textured | 37.59 | 4.154% | 0.99993 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 36.95 | 5.461% | 0.99998 |
| divisor2 / source | 0 | 0.5 | textured | 27.12 | 39.054% | 0.99984 |
| divisor2 / round1 | 0 | 0.5 | shaded | 48.52 | 0.188% | 0.99995 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 52.03 | 0.058% | 0.99998 |
| divisor2 / source | 0 | 0.5 | shaded | 27.72 | 17.361% | 0.99988 |
| round1 / source | 0 | 0.1 | textured | 27.63 | 34.492% | 1.00000 |
| round1 / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 38.01 | 4.706% | 1.00000 |
| divisor1 / source | 0 | 0.1 | textured | 27.58 | 35.159% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | 43.69 | 1.135% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 38.58 | 4.138% | 1.00000 |
| divisor2 / source | 0 | 0.1 | textured | 27.63 | 34.582% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
