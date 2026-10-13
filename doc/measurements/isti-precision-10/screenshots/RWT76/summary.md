# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 80 | 2.473 | 3.167 | 5.639 | 5.420 |
| divisor1 | 0 | 2 | 45 | 1.465 | 0.937 | 2.403 | 2.471 |
| divisor2 | 0 | 2 | 89 | 2.744 | 3.917 | 6.660 | 6.352 |
| round1 | 0 | 0.5 | 154 | 4.487 | 24.833 | 29.320 | 21.066 |
| divisor1 | 0 | 0.5 | 129 | 3.827 | 13.500 | 17.327 | 13.742 |
| divisor2 | 0 | 0.5 | 156 | 4.545 | 25.500 | 30.044 | 21.605 |
| round1 | 0 | 0.1 | 221 | 6.077 | 95.166 | 101.244 | 60.142 |
| divisor1 | 0 | 0.1 | 221 | 6.077 | 60.205 | 66.283 | 42.176 |
| divisor2 | 0 | 0.1 | 221 | 6.077 | 85.436 | 91.514 | 54.803 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.39 | 48.681% | 0.99879 |
| round1 / source | 0 | 2 | shaded | 29.20 | 20.090% | 0.99884 |
| divisor1 / round1 | 0 | 2 | textured | 24.73 | 50.515% | 0.99916 |
| divisor1 / source | 0 | 2 | textured | 24.70 | 60.598% | 0.99821 |
| divisor1 / round1 | 0 | 2 | shaded | 33.41 | 6.156% | 0.99920 |
| divisor1 / source | 0 | 2 | shaded | 28.02 | 23.752% | 0.99825 |
| divisor2 / round1 | 0 | 2 | textured | 33.92 | 7.041% | 0.99970 |
| divisor2 / divisor1 | 0 | 2 | textured | 24.41 | 55.408% | 0.99886 |
| divisor2 / source | 0 | 2 | textured | 26.55 | 47.825% | 0.99896 |
| divisor2 / round1 | 0 | 2 | shaded | 42.27 | 0.643% | 0.99968 |
| divisor2 / divisor1 | 0 | 2 | shaded | 32.97 | 6.681% | 0.99888 |
| divisor2 / source | 0 | 2 | shaded | 29.38 | 19.702% | 0.99899 |
| round1 / source | 0 | 0.5 | textured | 29.65 | 28.911% | 0.99970 |
| round1 / source | 0 | 0.5 | shaded | 29.88 | 18.344% | 0.99976 |
| divisor1 / round1 | 0 | 0.5 | textured | 30.95 | 16.790% | 0.99978 |
| divisor1 / source | 0 | 0.5 | textured | 28.28 | 35.605% | 0.99957 |
| divisor1 / round1 | 0 | 0.5 | shaded | 42.66 | 0.721% | 0.99983 |
| divisor1 / source | 0 | 0.5 | shaded | 29.75 | 18.796% | 0.99959 |
| divisor2 / round1 | 0 | 0.5 | textured | 45.16 | 0.639% | 0.99996 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 30.80 | 17.385% | 0.99974 |
| divisor2 / source | 0 | 0.5 | textured | 29.71 | 28.727% | 0.99974 |
| divisor2 / round1 | 0 | 0.5 | shaded | 49.70 | 0.093% | 0.99996 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 41.85 | 0.813% | 0.99978 |
| divisor2 / source | 0 | 0.5 | shaded | 29.91 | 18.300% | 0.99981 |
| round1 / source | 0 | 0.1 | textured | 31.92 | 19.423% | 0.99998 |
| round1 / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 32.70 | 16.745% | 0.99996 |
| divisor1 / source | 0 | 0.1 | textured | 31.64 | 21.067% | 0.99998 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | 36.51 | 7.135% | 0.99998 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 33.94 | 12.135% | 0.99998 |
| divisor2 / source | 0 | 0.1 | textured | 31.84 | 19.701% | 0.99996 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 30.19 | 17.501% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
