# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 77 | 2.025 | 22.432 | 24.457 | 6.732 |
| divisor1 | 0 | 2 | 57 | 1.482 | 1.096 | 2.578 | 2.481 |
| divisor2 | 0 | 2 | 64 | 1.677 | 2.164 | 3.841 | 3.108 |
| round1 | 0 | 0.5 | 122 | 3.121 | 114.682 | 117.803 | 21.156 |
| divisor1 | 0 | 0.5 | 122 | 3.121 | 27.963 | 31.084 | 10.128 |
| divisor2 | 0 | 0.5 | 122 | 3.121 | 48.086 | 51.208 | 13.744 |
| round1 | 0 | 0.1 | 151 | 3.822 | 224.349 | 228.171 | 38.365 |
| divisor1 | 0 | 0.1 | 151 | 3.822 | 46.264 | 50.085 | 15.675 |
| divisor2 | 0 | 0.1 | 151 | 3.822 | 106.476 | 110.298 | 25.389 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 11.33 | 43.246% | 0.99915 |
| round1 / source | 0 | 2 | shaded | 27.29 | 21.611% | 0.99934 |
| divisor1 / round1 | 0 | 2 | textured | 32.72 | 15.291% | 0.99868 |
| divisor1 / source | 0 | 2 | textured | 11.30 | 49.631% | 0.99832 |
| divisor1 / round1 | 0 | 2 | shaded | 36.96 | 2.541% | 0.99885 |
| divisor1 / source | 0 | 2 | shaded | 26.82 | 23.139% | 0.99846 |
| divisor2 / round1 | 0 | 2 | textured | 34.17 | 10.628% | 0.99951 |
| divisor2 / divisor1 | 0 | 2 | textured | 36.34 | 6.861% | 0.99910 |
| divisor2 / source | 0 | 2 | textured | 11.28 | 47.556% | 0.99900 |
| divisor2 / round1 | 0 | 2 | shaded | 41.52 | 0.837% | 0.99966 |
| divisor2 / divisor1 | 0 | 2 | shaded | 38.82 | 1.681% | 0.99915 |
| divisor2 / source | 0 | 2 | shaded | 27.13 | 22.341% | 0.99911 |
| round1 / source | 0 | 0.5 | textured | 11.33 | 38.938% | 0.99970 |
| round1 / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| divisor1 / round1 | 0 | 0.5 | textured | 38.79 | 3.389% | 0.99998 |
| divisor1 / source | 0 | 0.5 | textured | 11.31 | 39.058% | 0.99972 |
| divisor1 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| divisor2 / round1 | 0 | 0.5 | textured | 39.66 | 2.512% | 0.99998 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 39.98 | 2.590% | 1.00000 |
| divisor2 / source | 0 | 0.5 | textured | 11.29 | 38.979% | 0.99972 |
| divisor2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| round1 / source | 0 | 0.1 | textured | 11.33 | 38.250% | 0.99987 |
| round1 / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 37.99 | 3.969% | 0.99996 |
| divisor1 / source | 0 | 0.1 | textured | 11.31 | 38.431% | 0.99991 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | 38.39 | 3.319% | 0.99996 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 39.93 | 2.539% | 1.00000 |
| divisor2 / source | 0 | 0.1 | textured | 11.29 | 38.314% | 0.99991 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
