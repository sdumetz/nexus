# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| divisor1 | 0 | 2 | 33 | 0.954 | 0.687 | 1.642 | 1.521 |
| divisor2 | 0 | 2 | 56 | 1.531 | 1.167 | 2.697 | 2.456 |
| round1 | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| divisor1 | 0 | 0.5 | 106 | 2.694 | 2.583 | 5.278 | 4.435 |
| divisor2 | 0 | 0.5 | 124 | 3.116 | 4.583 | 7.699 | 5.660 |
| round1 | 0 | 0.1 | 296 | 6.822 | 128.166 | 134.988 | 33.052 |
| divisor1 | 0 | 0.1 | 296 | 6.822 | 50.138 | 56.960 | 21.077 |
| divisor2 | 0 | 0.1 | 296 | 6.822 | 94.805 | 101.627 | 28.653 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| round1 / source | 0 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| divisor1 / round1 | 0 | 2 | textured | 30.11 | 25.446% | 0.99902 |
| divisor1 / source | 0 | 2 | textured | 29.70 | 29.809% | 0.99814 |
| divisor1 / round1 | 0 | 2 | shaded | 34.61 | 5.636% | 0.99921 |
| divisor1 / source | 0 | 2 | shaded | 33.44 | 7.323% | 0.99893 |
| divisor2 / round1 | 0 | 2 | textured | 40.22 | 2.692% | 0.99983 |
| divisor2 / divisor1 | 0 | 2 | textured | 30.41 | 23.514% | 0.99911 |
| divisor2 / source | 0 | 2 | textured | 31.18 | 22.614% | 0.99864 |
| divisor2 / round1 | 0 | 2 | shaded | 45.28 | 0.373% | 0.99987 |
| divisor2 / divisor1 | 0 | 2 | shaded | 34.95 | 5.187% | 0.99934 |
| divisor2 / source | 0 | 2 | shaded | 37.85 | 2.067% | 0.99947 |
| round1 / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| round1 / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| divisor1 / round1 | 0 | 0.5 | textured | 32.62 | 14.927% | 0.99915 |
| divisor1 / source | 0 | 0.5 | textured | 33.06 | 14.562% | 0.99908 |
| divisor1 / round1 | 0 | 0.5 | shaded | 46.25 | 0.205% | 0.99992 |
| divisor1 / source | 0 | 0.5 | shaded | 42.53 | 0.552% | 0.99987 |
| divisor2 / round1 | 0 | 0.5 | textured | 37.93 | 4.778% | 0.99934 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 33.85 | 10.776% | 0.99977 |
| divisor2 / source | 0 | 0.5 | textured | 35.47 | 8.371% | 0.99915 |
| divisor2 / round1 | 0 | 0.5 | shaded | 49.13 | 0.117% | 0.99998 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 49.01 | 0.094% | 0.99994 |
| divisor2 / source | 0 | 0.5 | shaded | 43.40 | 0.452% | 0.99992 |
| round1 / source | 0 | 0.1 | textured | 40.07 | 1.872% | 0.99934 |
| round1 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | 38.68 | 3.303% | 0.99926 |
| divisor1 / source | 0 | 0.1 | textured | 39.68 | 1.896% | 0.99936 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | 40.97 | 1.962% | 0.99926 |
| divisor2 / divisor1 | 0 | 0.1 | textured | 40.47 | 2.021% | 0.99974 |
| divisor2 / source | 0 | 0.1 | textured | 39.87 | 1.810% | 0.99943 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
