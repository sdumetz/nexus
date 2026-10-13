# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 40 | 0.913 | 1.021 | 1.933 | 1.921 |
| fine | 0 | 2 | 40 | 0.913 | 1.021 | 1.933 | 1.921 |
| reconstruction | 0 | 2 | 27 | 0.626 | 0.562 | 1.188 | 1.248 |
| reconstructionFine | 0 | 2 | 27 | 0.626 | 0.562 | 1.188 | 1.248 |
| round1 | 0 | 0.5 | 88 | 1.936 | 7.833 | 9.769 | 6.782 |
| fine | 0 | 0.5 | 88 | 1.936 | 6.421 | 8.357 | 6.150 |
| reconstruction | 0 | 0.5 | 78 | 1.721 | 6.750 | 8.471 | 5.935 |
| reconstructionFine | 0 | 0.5 | 78 | 1.721 | 5.338 | 7.059 | 5.303 |
| round1 | 0 | 0.1 | 105 | 2.283 | 13.500 | 15.783 | 9.673 |
| fine | 0 | 0.1 | 105 | 2.283 | 9.901 | 12.184 | 8.191 |
| reconstruction | 0 | 0.1 | 105 | 2.283 | 13.500 | 15.783 | 9.673 |
| reconstructionFine | 0 | 0.1 | 105 | 2.283 | 9.901 | 12.184 | 8.191 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 23.15 | 48.578% | 0.99120 |
| round1 / source | 0 | 2 | shaded | 34.90 | 3.138% | 0.99480 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 23.15 | 48.578% | 0.99120 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 34.90 | 3.138% | 0.99480 |
| reconstruction / round1 | 0 | 2 | textured | 25.00 | 37.561% | 0.98726 |
| reconstruction / fine | 0 | 2 | textured | 25.00 | 37.561% | 0.98726 |
| reconstruction / source | 0 | 2 | textured | 22.07 | 57.054% | 0.98353 |
| reconstruction / round1 | 0 | 2 | shaded | 31.40 | 6.232% | 0.99015 |
| reconstruction / fine | 0 | 2 | shaded | 31.40 | 6.232% | 0.99015 |
| reconstruction / source | 0 | 2 | shaded | 30.08 | 9.068% | 0.98665 |
| reconstructionFine / round1 | 0 | 2 | textured | 25.00 | 37.561% | 0.98726 |
| reconstructionFine / fine | 0 | 2 | textured | 25.00 | 37.561% | 0.98726 |
| reconstructionFine / reconstruction | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 22.07 | 57.054% | 0.98353 |
| reconstructionFine / round1 | 0 | 2 | shaded | 31.40 | 6.232% | 0.99015 |
| reconstructionFine / fine | 0 | 2 | shaded | 31.40 | 6.232% | 0.99015 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 30.08 | 9.068% | 0.98665 |
| round1 / source | 0 | 0.5 | textured | 26.94 | 20.102% | 0.99622 |
| round1 / source | 0 | 0.5 | shaded | 42.01 | 0.575% | 0.99976 |
| fine / round1 | 0 | 0.5 | textured | 35.60 | 6.579% | 0.99910 |
| fine / source | 0 | 0.5 | textured | 26.93 | 20.356% | 0.99592 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 42.01 | 0.575% | 0.99976 |
| reconstruction / round1 | 0 | 0.5 | textured | 54.14 | 0.120% | 0.99952 |
| reconstruction / fine | 0 | 0.5 | textured | 35.54 | 6.699% | 0.99862 |
| reconstruction / source | 0 | 0.5 | textured | 26.94 | 20.174% | 0.99598 |
| reconstruction / round1 | 0 | 0.5 | shaded | 53.72 | 0.048% | 0.99982 |
| reconstruction / fine | 0 | 0.5 | shaded | 53.72 | 0.048% | 0.99982 |
| reconstruction / source | 0 | 0.5 | shaded | 41.78 | 0.605% | 0.99958 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 35.54 | 6.699% | 0.99862 |
| reconstructionFine / fine | 0 | 0.5 | textured | 54.11 | 0.120% | 0.99952 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | 35.60 | 6.581% | 0.99910 |
| reconstructionFine / source | 0 | 0.5 | textured | 26.92 | 20.422% | 0.99568 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 53.72 | 0.048% | 0.99982 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 53.72 | 0.048% | 0.99982 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 41.78 | 0.605% | 0.99958 |
| round1 / source | 0 | 0.1 | textured | 27.54 | 16.649% | 0.99628 |
| round1 / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| fine / source | 0 | 0.1 | textured | 27.51 | 17.110% | 0.99592 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| reconstruction / source | 0 | 0.1 | textured | 27.54 | 16.649% | 0.99628 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| reconstructionFine / source | 0 | 0.1 | textured | 27.51 | 17.110% | 0.99592 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
