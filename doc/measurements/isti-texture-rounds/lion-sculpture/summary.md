# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| control | 0 | 2 | 3 | 0.112 | 0.062 | 0.174 | 0.165 |
| round1 | 0 | 2 | 16 | 0.517 | 0.333 | 0.851 | 0.803 |
| round2 | 0 | 2 | 16 | 0.517 | 0.333 | 0.851 | 0.803 |
| nexus3 | 0 | 2 | 1 | 0.108 | 6.873 | 6.981 | 3.795 |
| control | 1 | 2 | 21 | 0.639 | 0.437 | 1.076 | 1.003 |
| round1 | 1 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| round2 | 1 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| nexus3 | 1 | 2 | 5 | 1.444 | 111.344 | 112.788 | 44.403 |
| control | 2 | 2 | 79 | 2.064 | 1.646 | 3.709 | 3.306 |
| round1 | 2 | 2 | 133 | 3.314 | 5.833 | 9.147 | 6.219 |
| round2 | 2 | 2 | 133 | 3.314 | 5.833 | 9.147 | 6.219 |
| nexus3 | 2 | 2 | 8 | 2.897 | 241.669 | 244.565 | 83.802 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| control / source | 0 | 2 | textured | 22.16 | 69.029% | 0.93435 |
| control / source | 0 | 2 | shaded | 14.73 | 60.183% | 0.93520 |
| round1 / control | 0 | 2 | textured | 23.08 | 63.710% | 0.93409 |
| round1 / source | 0 | 2 | textured | 28.37 | 39.155% | 0.99762 |
| round1 / control | 0 | 2 | shaded | 14.98 | 56.056% | 0.93564 |
| round1 / source | 0 | 2 | shaded | 28.21 | 23.060% | 0.99833 |
| round2 / control | 0 | 2 | textured | 23.08 | 63.710% | 0.93409 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 28.37 | 39.155% | 0.99762 |
| round2 / control | 0 | 2 | shaded | 14.98 | 56.056% | 0.93564 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 28.21 | 23.060% | 0.99833 |
| nexus3 / control | 0 | 2 | textured | 22.40 | 67.372% | 0.93044 |
| nexus3 / round1 | 0 | 2 | textured | 27.94 | 40.493% | 0.99071 |
| nexus3 / round2 | 0 | 2 | textured | 27.94 | 40.493% | 0.99071 |
| nexus3 / source | 0 | 2 | textured | 31.34 | 19.402% | 0.99119 |
| nexus3 / control | 0 | 2 | shaded | 14.99 | 50.499% | 0.93119 |
| nexus3 / round1 | 0 | 2 | shaded | 26.57 | 22.632% | 0.99155 |
| nexus3 / round2 | 0 | 2 | shaded | 26.57 | 22.632% | 0.99155 |
| nexus3 / source | 0 | 2 | shaded | 24.88 | 34.158% | 0.99179 |
| control / source | 1 | 2 | textured | 27.94 | 39.572% | 0.99738 |
| control / source | 1 | 2 | shaded | 29.50 | 16.121% | 0.99815 |
| round1 / control | 1 | 2 | textured | 28.51 | 36.135% | 0.99804 |
| round1 / source | 1 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| round1 / control | 1 | 2 | shaded | 29.97 | 14.707% | 0.99832 |
| round1 / source | 1 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| round2 / control | 1 | 2 | textured | 28.51 | 36.135% | 0.99804 |
| round2 / round1 | 1 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 1 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| round2 / control | 1 | 2 | shaded | 29.97 | 14.707% | 0.99832 |
| round2 / round1 | 1 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 1 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| nexus3 / control | 1 | 2 | textured | 27.61 | 40.986% | 0.99684 |
| nexus3 / round1 | 1 | 2 | textured | 30.42 | 25.472% | 0.99778 |
| nexus3 / round2 | 1 | 2 | textured | 30.42 | 25.472% | 0.99778 |
| nexus3 / source | 1 | 2 | textured | 37.50 | 3.662% | 0.99783 |
| nexus3 / control | 1 | 2 | shaded | 29.82 | 13.690% | 0.99768 |
| nexus3 / round1 | 1 | 2 | shaded | 34.31 | 3.740% | 0.99853 |
| nexus3 / round2 | 1 | 2 | shaded | 34.31 | 3.740% | 0.99853 |
| nexus3 / source | 1 | 2 | shaded | 34.64 | 3.546% | 0.99870 |
| control / source | 2 | 2 | textured | 30.27 | 25.347% | 0.99940 |
| control / source | 2 | 2 | shaded | 41.15 | 0.896% | 0.99984 |
| round1 / control | 2 | 2 | textured | 30.54 | 22.463% | 0.99957 |
| round1 / source | 2 | 2 | textured | 34.90 | 9.644% | 0.99947 |
| round1 / control | 2 | 2 | shaded | 44.43 | 0.328% | 0.99988 |
| round1 / source | 2 | 2 | shaded | 43.49 | 0.482% | 0.99993 |
| round2 / control | 2 | 2 | textured | 30.54 | 22.463% | 0.99957 |
| round2 / round1 | 2 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 2 | 2 | textured | 34.90 | 9.644% | 0.99947 |
| round2 / control | 2 | 2 | shaded | 44.43 | 0.328% | 0.99988 |
| round2 / round1 | 2 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 2 | 2 | shaded | 43.49 | 0.482% | 0.99993 |
| nexus3 / control | 2 | 2 | textured | 29.90 | 26.900% | 0.99938 |
| nexus3 / round1 | 2 | 2 | textured | 34.08 | 11.642% | 0.99943 |
| nexus3 / round2 | 2 | 2 | textured | 34.08 | 11.642% | 0.99943 |
| nexus3 / source | 2 | 2 | textured | 42.34 | 0.737% | 0.99968 |
| nexus3 / control | 2 | 2 | shaded | 41.55 | 0.825% | 0.99984 |
| nexus3 / round1 | 2 | 2 | shaded | 44.26 | 0.434% | 0.99993 |
| nexus3 / round2 | 2 | 2 | shaded | 44.26 | 0.434% | 0.99993 |
| nexus3 / source | 2 | 2 | shaded | 49.10 | 0.040% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
