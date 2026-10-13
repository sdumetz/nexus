# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| divisor1 | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| divisor2 | 0 | 2 | 55 | 1.787 | 1.333 | 3.121 | 3.455 |
| round1 | 0 | 0.5 | 127 | 3.852 | 18.896 | 22.748 | 19.316 |
| divisor1 | 0 | 0.5 | 104 | 3.203 | 8.229 | 11.433 | 11.331 |
| divisor2 | 0 | 0.5 | 136 | 4.078 | 19.896 | 23.974 | 20.958 |
| round1 | 0 | 0.1 | 194 | 5.570 | 81.229 | 86.799 | 63.329 |
| divisor1 | 0 | 0.1 | 186 | 5.348 | 51.803 | 57.151 | 43.703 |
| divisor2 | 0 | 0.1 | 194 | 5.570 | 74.430 | 80.000 | 58.534 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| round1 / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| divisor1 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| divisor1 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| divisor2 / round1 | 0 | 2 | textured | 24.78 | 45.101% | 0.97592 |
| divisor2 / divisor1 | 0 | 2 | textured | 24.78 | 45.101% | 0.97592 |
| divisor2 / source | 0 | 2 | textured | 24.51 | 58.499% | 0.98536 |
| divisor2 / round1 | 0 | 2 | shaded | 22.78 | 29.582% | 0.98601 |
| divisor2 / divisor1 | 0 | 2 | shaded | 22.78 | 29.582% | 0.98601 |
| divisor2 / source | 0 | 2 | shaded | 22.94 | 43.230% | 0.99248 |
| round1 / source | 0 | 0.5 | textured | 27.60 | 36.398% | 0.99162 |
| round1 / source | 0 | 0.5 | shaded | 23.91 | 39.489% | 0.99937 |
| divisor1 / round1 | 0 | 0.5 | textured | 32.32 | 13.982% | 0.99390 |
| divisor1 / source | 0 | 0.5 | textured | 26.71 | 43.267% | 0.99016 |
| divisor1 / round1 | 0 | 0.5 | shaded | 36.81 | 2.764% | 0.99958 |
| divisor1 / source | 0 | 0.5 | shaded | 23.82 | 39.887% | 0.99895 |
| divisor2 / round1 | 0 | 0.5 | textured | 34.73 | 9.556% | 0.99705 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 30.76 | 20.109% | 0.99223 |
| divisor2 / source | 0 | 0.5 | textured | 27.90 | 35.644% | 0.99120 |
| divisor2 / round1 | 0 | 0.5 | shaded | 37.42 | 1.780% | 0.99979 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 34.85 | 3.602% | 0.99979 |
| divisor2 / source | 0 | 0.5 | shaded | 23.98 | 39.447% | 0.99916 |
| round1 / source | 0 | 0.1 | textured | 28.24 | 33.606% | 0.99120 |
| round1 / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 36.25 | 7.477% | 0.99726 |
| divisor1 / source | 0 | 0.1 | textured | 28.13 | 34.171% | 0.99225 |
| divisor1 / round1 | 0 | 0.1 | shaded | 40.12 | 1.048% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 24.12 | 39.493% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | 43.84 | 1.203% | 0.99979 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 36.40 | 7.098% | 0.99747 |
| divisor2 / source | 0 | 0.1 | textured | 28.21 | 33.836% | 0.99141 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | 40.12 | 1.048% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
