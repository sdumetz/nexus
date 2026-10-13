# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| fine | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| reconstruction | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| reconstructionFine | 0 | 2 | 24 | 0.877 | 0.500 | 1.377 | 1.497 |
| round1 | 0 | 0.5 | 127 | 3.852 | 18.896 | 22.748 | 19.316 |
| fine | 0 | 0.5 | 127 | 3.852 | 18.779 | 22.631 | 19.181 |
| reconstruction | 0 | 0.5 | 104 | 3.203 | 8.229 | 11.433 | 11.331 |
| reconstructionFine | 0 | 0.5 | 104 | 3.203 | 8.229 | 11.433 | 11.331 |
| round1 | 0 | 0.1 | 194 | 5.570 | 81.229 | 86.799 | 63.329 |
| fine | 0 | 0.1 | 194 | 5.570 | 61.470 | 67.039 | 49.947 |
| reconstruction | 0 | 0.1 | 186 | 5.348 | 71.562 | 76.911 | 57.084 |
| reconstructionFine | 0 | 0.1 | 186 | 5.348 | 51.803 | 57.151 | 43.703 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| round1 / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| reconstruction / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| reconstruction / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| reconstructionFine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 23.19 | 61.271% | 0.97313 |
| reconstructionFine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 20.51 | 49.146% | 0.98313 |
| round1 / source | 0 | 0.5 | textured | 27.60 | 36.398% | 0.99162 |
| round1 / source | 0 | 0.5 | shaded | 23.91 | 39.489% | 0.99937 |
| fine / round1 | 0 | 0.5 | textured | 60.17 | 0.042% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 27.60 | 36.419% | 0.99162 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 23.91 | 39.489% | 0.99937 |
| reconstruction / round1 | 0 | 0.5 | textured | 32.32 | 13.982% | 0.99390 |
| reconstruction / fine | 0 | 0.5 | textured | 32.32 | 13.940% | 0.99390 |
| reconstruction / source | 0 | 0.5 | textured | 26.71 | 43.267% | 0.99016 |
| reconstruction / round1 | 0 | 0.5 | shaded | 36.81 | 2.764% | 0.99958 |
| reconstruction / fine | 0 | 0.5 | shaded | 36.81 | 2.764% | 0.99958 |
| reconstruction / source | 0 | 0.5 | shaded | 23.82 | 39.887% | 0.99895 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 32.32 | 13.982% | 0.99390 |
| reconstructionFine / fine | 0 | 0.5 | textured | 32.32 | 13.940% | 0.99390 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | textured | 26.71 | 43.267% | 0.99016 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 36.81 | 2.764% | 0.99958 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 36.81 | 2.764% | 0.99958 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 23.82 | 39.887% | 0.99895 |
| round1 / source | 0 | 0.1 | textured | 28.24 | 33.606% | 0.99120 |
| round1 / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 40.72 | 2.930% | 0.99874 |
| fine / source | 0 | 0.1 | textured | 28.16 | 34.402% | 0.99204 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 24.16 | 39.619% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | 38.17 | 4.512% | 0.99852 |
| reconstruction / fine | 0 | 0.1 | textured | 36.26 | 7.435% | 0.99726 |
| reconstruction / source | 0 | 0.1 | textured | 28.22 | 33.375% | 0.99141 |
| reconstruction / round1 | 0 | 0.1 | shaded | 40.12 | 1.048% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | 40.12 | 1.048% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 24.12 | 39.493% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 36.25 | 7.477% | 0.99726 |
| reconstructionFine / fine | 0 | 0.1 | textured | 38.17 | 4.508% | 0.99853 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 40.72 | 2.929% | 0.99874 |
| reconstructionFine / source | 0 | 0.1 | textured | 28.13 | 34.171% | 0.99225 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | 40.12 | 1.048% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | 40.12 | 1.048% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 24.12 | 39.493% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
