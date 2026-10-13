# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 40 | 0.913 | 1.021 | 1.933 | 1.921 |
| divisor1 | 0 | 2 | 27 | 0.626 | 0.562 | 1.188 | 1.248 |
| divisor2 | 0 | 2 | 39 | 0.895 | 0.937 | 1.833 | 1.855 |
| round1 | 0 | 0.5 | 88 | 1.936 | 7.833 | 9.769 | 6.782 |
| divisor1 | 0 | 0.5 | 78 | 1.721 | 5.338 | 7.059 | 5.303 |
| divisor2 | 0 | 0.5 | 85 | 1.873 | 7.333 | 9.207 | 6.471 |
| round1 | 0 | 0.1 | 105 | 2.283 | 13.500 | 15.783 | 9.673 |
| divisor1 | 0 | 0.1 | 105 | 2.283 | 9.901 | 12.184 | 8.191 |
| divisor2 | 0 | 0.1 | 105 | 2.283 | 13.500 | 15.783 | 9.673 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 23.15 | 48.578% | 0.99120 |
| round1 / source | 0 | 2 | shaded | 34.90 | 3.138% | 0.99480 |
| divisor1 / round1 | 0 | 2 | textured | 25.00 | 37.561% | 0.98726 |
| divisor1 / source | 0 | 2 | textured | 22.07 | 57.054% | 0.98353 |
| divisor1 / round1 | 0 | 2 | shaded | 31.40 | 6.232% | 0.99015 |
| divisor1 / source | 0 | 2 | shaded | 30.08 | 9.068% | 0.98665 |
| divisor2 / round1 | 0 | 2 | textured | 31.86 | 7.545% | 0.99862 |
| divisor2 / divisor1 | 0 | 2 | textured | 25.17 | 38.783% | 0.98791 |
| divisor2 / source | 0 | 2 | textured | 23.57 | 47.462% | 0.99078 |
| divisor2 / round1 | 0 | 2 | shaded | 39.24 | 0.707% | 0.99874 |
| divisor2 / divisor1 | 0 | 2 | shaded | 31.62 | 6.468% | 0.99092 |
| divisor2 / source | 0 | 2 | shaded | 34.42 | 2.982% | 0.99414 |
| round1 / source | 0 | 0.5 | textured | 26.94 | 20.102% | 0.99622 |
| round1 / source | 0 | 0.5 | shaded | 42.01 | 0.575% | 0.99976 |
| divisor1 / round1 | 0 | 0.5 | textured | 35.54 | 6.699% | 0.99862 |
| divisor1 / source | 0 | 0.5 | textured | 26.92 | 20.422% | 0.99568 |
| divisor1 / round1 | 0 | 0.5 | shaded | 53.72 | 0.048% | 0.99982 |
| divisor1 / source | 0 | 0.5 | shaded | 41.78 | 0.605% | 0.99958 |
| divisor2 / round1 | 0 | 0.5 | textured | 58.32 | 0.036% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 35.55 | 6.669% | 0.99862 |
| divisor2 / source | 0 | 0.5 | textured | 26.94 | 20.078% | 0.99622 |
| divisor2 / round1 | 0 | 0.5 | shaded | 66.30 | 0.006% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 54.32 | 0.048% | 0.99982 |
| divisor2 / source | 0 | 0.5 | shaded | 41.99 | 0.587% | 0.99976 |
| round1 / source | 0 | 0.1 | textured | 27.54 | 16.649% | 0.99628 |
| round1 / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| divisor1 / source | 0 | 0.1 | textured | 27.51 | 17.110% | 0.99592 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| divisor2 / source | 0 | 0.1 | textured | 27.54 | 16.649% | 0.99628 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
