# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| divisor1 | 0 | 2 | 67 | 1.721 | 1.396 | 3.116 | 3.288 |
| divisor2 | 0 | 2 | 122 | 2.997 | 2.604 | 5.601 | 5.768 |
| round1 | 0 | 0.5 | 279 | 6.403 | 11.625 | 18.028 | 14.650 |
| divisor1 | 0 | 0.5 | 212 | 4.979 | 6.041 | 11.021 | 10.206 |
| divisor2 | 0 | 0.5 | 252 | 5.829 | 9.375 | 15.204 | 12.887 |
| round1 | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| divisor1 | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| divisor2 | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| round1 / source | 0 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| divisor1 / round1 | 0 | 2 | textured | 27.81 | 32.349% | 0.99953 |
| divisor1 / source | 0 | 2 | textured | 25.27 | 54.757% | 0.99905 |
| divisor1 / round1 | 0 | 2 | shaded | 38.47 | 2.023% | 0.99953 |
| divisor1 / source | 0 | 2 | shaded | 34.85 | 5.165% | 0.99905 |
| divisor2 / round1 | 0 | 2 | textured | 32.86 | 10.964% | 0.99982 |
| divisor2 / divisor1 | 0 | 2 | textured | 27.01 | 39.496% | 0.99937 |
| divisor2 / source | 0 | 2 | textured | 27.17 | 43.046% | 0.99950 |
| divisor2 / round1 | 0 | 2 | shaded | 44.49 | 0.412% | 0.99982 |
| divisor2 / divisor1 | 0 | 2 | shaded | 37.54 | 2.565% | 0.99937 |
| divisor2 / source | 0 | 2 | shaded | 37.63 | 2.285% | 0.99950 |
| round1 / source | 0 | 0.5 | textured | 32.45 | 17.954% | 0.99998 |
| round1 / source | 0 | 0.5 | shaded | 39.59 | 1.531% | 0.99998 |
| divisor1 / round1 | 0 | 0.5 | textured | 32.48 | 13.211% | 1.00000 |
| divisor1 / source | 0 | 0.5 | textured | 30.34 | 26.248% | 0.99998 |
| divisor1 / round1 | 0 | 0.5 | shaded | 52.60 | 0.031% | 1.00000 |
| divisor1 / source | 0 | 0.5 | shaded | 39.44 | 1.559% | 0.99998 |
| divisor2 / round1 | 0 | 0.5 | textured | 37.37 | 4.955% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | textured | 34.19 | 8.227% | 1.00000 |
| divisor2 / source | 0 | 0.5 | textured | 31.65 | 21.227% | 0.99998 |
| divisor2 / round1 | 0 | 0.5 | shaded | 57.86 | 0.004% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.5 | shaded | 54.14 | 0.027% | 1.00000 |
| divisor2 / source | 0 | 0.5 | shaded | 39.54 | 1.534% | 0.99998 |
| round1 / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| round1 / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| divisor1 / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| divisor1 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor1 / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| divisor2 / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| divisor2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / divisor1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| divisor2 / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
