# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 53 | 1.452 | 4.042 | 5.493 | 4.506 |
| fine | 0 | 2 | 53 | 1.452 | 4.042 | 5.493 | 4.506 |
| reconstruction | 0 | 2 | 28 | 0.779 | 0.583 | 1.362 | 1.421 |
| reconstructionFine | 0 | 2 | 28 | 0.779 | 0.583 | 1.362 | 1.421 |
| round1 | 0 | 0.5 | 87 | 2.349 | 15.437 | 17.786 | 12.813 |
| fine | 0 | 0.5 | 87 | 2.349 | 15.318 | 17.667 | 12.696 |
| reconstruction | 0 | 0.5 | 70 | 1.893 | 6.521 | 8.413 | 6.815 |
| reconstructionFine | 0 | 0.5 | 70 | 1.893 | 6.452 | 8.344 | 6.766 |
| round1 | 0 | 0.1 | 119 | 3.100 | 51.104 | 54.204 | 33.115 |
| fine | 0 | 0.1 | 119 | 3.100 | 34.858 | 37.958 | 24.465 |
| reconstruction | 0 | 0.1 | 119 | 3.100 | 51.104 | 54.204 | 33.115 |
| reconstructionFine | 0 | 0.1 | 119 | 3.100 | 34.858 | 37.958 | 24.465 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 26.75 | 42.024% | 0.99945 |
| round1 / source | 0 | 2 | shaded | 31.18 | 14.640% | 0.99974 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 26.75 | 42.024% | 0.99945 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 31.18 | 14.640% | 0.99974 |
| reconstruction / round1 | 0 | 2 | textured | 25.29 | 43.278% | 0.99939 |
| reconstruction / fine | 0 | 2 | textured | 25.29 | 43.278% | 0.99939 |
| reconstruction / source | 0 | 2 | textured | 25.07 | 53.959% | 0.99907 |
| reconstruction / round1 | 0 | 2 | shaded | 34.48 | 5.235% | 0.99974 |
| reconstruction / fine | 0 | 2 | shaded | 34.48 | 5.235% | 0.99974 |
| reconstruction / source | 0 | 2 | shaded | 29.69 | 18.543% | 0.99948 |
| reconstructionFine / round1 | 0 | 2 | textured | 25.29 | 43.278% | 0.99939 |
| reconstructionFine / fine | 0 | 2 | textured | 25.29 | 43.278% | 0.99939 |
| reconstructionFine / reconstruction | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 25.07 | 53.959% | 0.99907 |
| reconstructionFine / round1 | 0 | 2 | shaded | 34.48 | 5.235% | 0.99974 |
| reconstructionFine / fine | 0 | 2 | shaded | 34.48 | 5.235% | 0.99974 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 29.69 | 18.543% | 0.99948 |
| round1 / source | 0 | 0.5 | textured | 29.29 | 29.082% | 0.99939 |
| round1 / source | 0 | 0.5 | shaded | 31.67 | 13.345% | 0.99997 |
| fine / round1 | 0 | 0.5 | textured | 43.67 | 1.179% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 29.29 | 29.013% | 0.99939 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 31.67 | 13.345% | 0.99997 |
| reconstruction / round1 | 0 | 0.5 | textured | 30.76 | 14.098% | 0.99983 |
| reconstruction / fine | 0 | 0.5 | textured | 30.57 | 15.126% | 0.99983 |
| reconstruction / source | 0 | 0.5 | textured | 28.16 | 33.818% | 0.99945 |
| reconstruction / round1 | 0 | 0.5 | shaded | 44.92 | 0.459% | 0.99997 |
| reconstruction / fine | 0 | 0.5 | shaded | 44.92 | 0.459% | 0.99997 |
| reconstruction / source | 0 | 0.5 | shaded | 31.52 | 13.814% | 0.99994 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 30.57 | 15.106% | 0.99983 |
| reconstructionFine / fine | 0 | 0.5 | textured | 30.77 | 14.020% | 0.99983 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | 42.14 | 1.710% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | textured | 28.16 | 33.786% | 0.99945 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 44.92 | 0.459% | 0.99997 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 44.92 | 0.459% | 0.99997 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 31.52 | 13.814% | 0.99994 |
| round1 / source | 0 | 0.1 | textured | 32.04 | 18.838% | 0.99971 |
| round1 / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 32.61 | 14.399% | 0.99977 |
| fine / source | 0 | 0.1 | textured | 31.65 | 20.960% | 0.99965 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | 32.61 | 14.399% | 0.99977 |
| reconstruction / source | 0 | 0.1 | textured | 32.04 | 18.838% | 0.99971 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 32.61 | 14.399% | 0.99977 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 32.61 | 14.399% | 0.99977 |
| reconstructionFine / source | 0 | 0.1 | textured | 31.65 | 20.960% | 0.99965 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 32.00 | 12.535% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
