# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| round2 | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| fine | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| round1 | 0 | 0.5 | 127 | 3.852 | 18.896 | 22.748 | 19.316 |
| round2 | 0 | 0.5 | 127 | 3.852 | 18.896 | 22.748 | 19.316 |
| fine | 0 | 0.5 | 127 | 3.852 | 18.779 | 22.631 | 19.181 |
| round1 | 0 | 0.1 | 194 | 5.570 | 81.229 | 86.799 | 63.329 |
| round2 | 0 | 0.1 | 194 | 5.570 | 71.229 | 76.799 | 56.605 |
| fine | 0 | 0.1 | 194 | 5.570 | 61.470 | 67.039 | 49.947 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| round1 / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| round1 / source | 0 | 0.5 | textured | 27.60 | 36.398% | 0.99162 |
| round1 / source | 0 | 0.5 | shaded | 23.91 | 39.489% | 0.99937 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 27.60 | 36.398% | 0.99162 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 23.91 | 39.489% | 0.99937 |
| fine / round1 | 0 | 0.5 | textured | 60.17 | 0.042% | 1.00000 |
| fine / round2 | 0 | 0.5 | textured | 60.17 | 0.042% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 27.60 | 36.419% | 0.99162 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 23.91 | 39.489% | 0.99937 |
| round1 / source | 0 | 0.1 | textured | 28.24 | 33.606% | 0.99120 |
| round1 / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | 57.86 | 0.000% | 0.99979 |
| round2 / source | 0 | 0.1 | textured | 28.21 | 33.669% | 0.99141 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 40.72 | 2.930% | 0.99874 |
| fine / round2 | 0 | 0.1 | textured | 40.81 | 2.867% | 0.99895 |
| fine / source | 0 | 0.1 | textured | 28.16 | 34.402% | 0.99204 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
