# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 74 | 1.754 | 2.854 | 4.608 | 3.204 |
| fine | 0 | 2 | 74 | 1.754 | 1.746 | 3.500 | 2.994 |
| reconstruction | 0 | 2 | 62 | 1.466 | 2.167 | 3.632 | 2.523 |
| reconstructionFine | 0 | 2 | 62 | 1.466 | 1.059 | 2.524 | 2.313 |
| round1 | 0 | 0.5 | 152 | 3.510 | 11.604 | 15.114 | 7.524 |
| fine | 0 | 0.5 | 152 | 3.510 | 6.528 | 10.038 | 6.784 |
| reconstruction | 0 | 0.5 | 132 | 3.052 | 9.437 | 12.489 | 6.172 |
| reconstructionFine | 0 | 0.5 | 132 | 3.052 | 4.394 | 7.445 | 5.442 |
| round1 | 0 | 0.1 | 217 | 4.859 | 28.271 | 33.129 | 14.226 |
| fine | 0 | 0.1 | 217 | 4.859 | 17.472 | 22.331 | 12.048 |
| reconstruction | 0 | 0.1 | 217 | 4.859 | 28.271 | 33.129 | 14.226 |
| reconstructionFine | 0 | 0.1 | 217 | 4.859 | 17.472 | 22.331 | 12.048 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.23 | 45.827% | 0.99970 |
| round1 / source | 0 | 2 | shaded | 27.14 | 19.795% | 0.99972 |
| fine / round1 | 0 | 2 | textured | 36.87 | 6.308% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.24 | 47.963% | 0.99970 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 27.14 | 19.795% | 0.99972 |
| reconstruction / round1 | 0 | 2 | textured | 35.13 | 5.710% | 1.00000 |
| reconstruction / fine | 0 | 2 | textured | 32.91 | 12.029% | 1.00000 |
| reconstruction / source | 0 | 2 | textured | 25.96 | 48.214% | 0.99970 |
| reconstruction / round1 | 0 | 2 | shaded | 36.81 | 2.670% | 1.00000 |
| reconstruction / fine | 0 | 2 | shaded | 36.81 | 2.670% | 1.00000 |
| reconstruction / source | 0 | 2 | shaded | 26.76 | 21.264% | 0.99972 |
| reconstructionFine / round1 | 0 | 2 | textured | 32.90 | 12.041% | 1.00000 |
| reconstructionFine / fine | 0 | 2 | textured | 35.13 | 5.719% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 2 | textured | 36.84 | 6.350% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 25.96 | 50.361% | 0.99970 |
| reconstructionFine / round1 | 0 | 2 | shaded | 36.81 | 2.670% | 1.00000 |
| reconstructionFine / fine | 0 | 2 | shaded | 36.81 | 2.670% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 26.76 | 21.264% | 0.99972 |
| round1 / source | 0 | 0.5 | textured | 27.23 | 37.952% | 0.99991 |
| round1 / source | 0 | 0.5 | shaded | 27.73 | 17.319% | 0.99993 |
| fine / round1 | 0 | 0.5 | textured | 38.10 | 4.833% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 27.18 | 39.650% | 0.99991 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 27.73 | 17.319% | 0.99993 |
| reconstruction / round1 | 0 | 0.5 | textured | 37.67 | 3.897% | 0.99991 |
| reconstruction / fine | 0 | 0.5 | textured | 34.94 | 8.633% | 0.99991 |
| reconstruction / source | 0 | 0.5 | textured | 27.03 | 39.621% | 0.99981 |
| reconstruction / round1 | 0 | 0.5 | shaded | 46.92 | 0.246% | 0.99993 |
| reconstruction / fine | 0 | 0.5 | shaded | 46.92 | 0.246% | 0.99993 |
| reconstruction / source | 0 | 0.5 | shaded | 27.70 | 17.398% | 0.99986 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 34.97 | 8.691% | 0.99991 |
| reconstructionFine / fine | 0 | 0.5 | textured | 37.78 | 3.948% | 0.99991 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | 37.83 | 5.253% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | textured | 26.99 | 41.250% | 0.99981 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 46.92 | 0.246% | 0.99993 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 46.92 | 0.246% | 0.99993 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 27.70 | 17.398% | 0.99986 |
| round1 / source | 0 | 0.1 | textured | 27.63 | 34.492% | 1.00000 |
| round1 / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 38.01 | 4.706% | 1.00000 |
| fine / source | 0 | 0.1 | textured | 27.58 | 35.159% | 1.00000 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | 38.01 | 4.706% | 1.00000 |
| reconstruction / source | 0 | 0.1 | textured | 27.63 | 34.492% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 38.01 | 4.706% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 38.01 | 4.706% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | textured | 27.58 | 35.159% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 27.84 | 17.010% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
