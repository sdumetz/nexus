# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 40 | 0.913 | 1.021 | 1.933 | 1.921 |
| round2 | 0 | 2 | 40 | 0.913 | 1.021 | 1.933 | 1.921 |
| fine | 0 | 2 | 40 | 0.913 | 1.021 | 1.933 | 1.921 |
| round1 | 0 | 0.5 | 88 | 1.936 | 7.833 | 9.769 | 6.782 |
| round2 | 0 | 0.5 | 88 | 1.936 | 7.833 | 9.769 | 6.782 |
| fine | 0 | 0.5 | 88 | 1.936 | 6.421 | 8.357 | 6.150 |
| round1 | 0 | 0.1 | 105 | 2.283 | 13.500 | 15.783 | 9.673 |
| round2 | 0 | 0.1 | 105 | 2.283 | 13.500 | 15.783 | 9.673 |
| fine | 0 | 0.1 | 105 | 2.283 | 9.901 | 12.184 | 8.191 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 23.15 | 48.578% | 0.99120 |
| round1 / source | 0 | 2 | shaded | 34.90 | 3.138% | 0.99480 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 23.15 | 48.578% | 0.99120 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 34.90 | 3.138% | 0.99480 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 23.15 | 48.578% | 0.99120 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 34.90 | 3.138% | 0.99480 |
| round1 / source | 0 | 0.5 | textured | 26.94 | 20.102% | 0.99622 |
| round1 / source | 0 | 0.5 | shaded | 42.01 | 0.575% | 0.99976 |
| round2 / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | textured | 26.94 | 20.102% | 0.99622 |
| round2 / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.5 | shaded | 42.01 | 0.575% | 0.99976 |
| fine / round1 | 0 | 0.5 | textured | 35.60 | 6.579% | 0.99910 |
| fine / round2 | 0 | 0.5 | textured | 35.60 | 6.579% | 0.99910 |
| fine / source | 0 | 0.5 | textured | 26.93 | 20.356% | 0.99592 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 42.01 | 0.575% | 0.99976 |
| round1 / source | 0 | 0.1 | textured | 27.54 | 16.649% | 0.99628 |
| round1 / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| round2 / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | textured | 27.54 | 16.649% | 0.99628 |
| round2 / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| fine / round2 | 0 | 0.1 | textured | 33.01 | 11.771% | 0.99868 |
| fine / source | 0 | 0.1 | textured | 27.51 | 17.110% | 0.99592 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / round2 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 43.43 | 0.407% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
