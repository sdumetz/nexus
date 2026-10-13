# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| fine | 0 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| reconstruction | 0 | 2 | 67 | 1.721 | 1.396 | 3.116 | 3.288 |
| reconstructionFine | 0 | 2 | 67 | 1.721 | 1.396 | 3.116 | 3.288 |
| round1 | 0 | 0.5 | 279 | 6.403 | 11.625 | 18.028 | 14.650 |
| fine | 0 | 0.5 | 279 | 6.403 | 11.625 | 18.028 | 14.650 |
| reconstruction | 0 | 0.5 | 212 | 4.979 | 6.041 | 11.021 | 10.206 |
| reconstructionFine | 0 | 0.5 | 212 | 4.979 | 6.041 | 11.021 | 10.206 |
| round1 | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| fine | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| reconstruction | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |
| reconstructionFine | 0 | 0.1 | 294 | 6.719 | 12.875 | 19.593 | 15.618 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| round1 / source | 0 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| reconstruction / round1 | 0 | 2 | textured | 27.81 | 32.349% | 0.99953 |
| reconstruction / fine | 0 | 2 | textured | 27.81 | 32.349% | 0.99953 |
| reconstruction / source | 0 | 2 | textured | 25.27 | 54.757% | 0.99905 |
| reconstruction / round1 | 0 | 2 | shaded | 38.47 | 2.023% | 0.99953 |
| reconstruction / fine | 0 | 2 | shaded | 38.47 | 2.023% | 0.99953 |
| reconstruction / source | 0 | 2 | shaded | 34.85 | 5.165% | 0.99905 |
| reconstructionFine / round1 | 0 | 2 | textured | 27.81 | 32.349% | 0.99953 |
| reconstructionFine / fine | 0 | 2 | textured | 27.81 | 32.349% | 0.99953 |
| reconstructionFine / reconstruction | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 25.27 | 54.757% | 0.99905 |
| reconstructionFine / round1 | 0 | 2 | shaded | 38.47 | 2.023% | 0.99953 |
| reconstructionFine / fine | 0 | 2 | shaded | 38.47 | 2.023% | 0.99953 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 34.85 | 5.165% | 0.99905 |
| round1 / source | 0 | 0.5 | textured | 32.45 | 17.954% | 0.99998 |
| round1 / source | 0 | 0.5 | shaded | 39.59 | 1.531% | 0.99998 |
| fine / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 32.45 | 17.954% | 0.99998 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 39.59 | 1.531% | 0.99998 |
| reconstruction / round1 | 0 | 0.5 | textured | 32.48 | 13.211% | 1.00000 |
| reconstruction / fine | 0 | 0.5 | textured | 32.48 | 13.211% | 1.00000 |
| reconstruction / source | 0 | 0.5 | textured | 30.34 | 26.248% | 0.99998 |
| reconstruction / round1 | 0 | 0.5 | shaded | 52.60 | 0.031% | 1.00000 |
| reconstruction / fine | 0 | 0.5 | shaded | 52.60 | 0.031% | 1.00000 |
| reconstruction / source | 0 | 0.5 | shaded | 39.44 | 1.559% | 0.99998 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 32.48 | 13.211% | 1.00000 |
| reconstructionFine / fine | 0 | 0.5 | textured | 32.48 | 13.211% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | textured | 30.34 | 26.248% | 0.99998 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 52.60 | 0.031% | 1.00000 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 52.60 | 0.031% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 39.44 | 1.559% | 0.99998 |
| round1 / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| round1 / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | textured | 32.68 | 17.277% | 0.99999 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 39.63 | 1.525% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
