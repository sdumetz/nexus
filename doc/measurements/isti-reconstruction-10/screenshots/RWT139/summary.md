# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| fine | 0 | 2 | 69 | 1.835 | 1.437 | 3.273 | 2.939 |
| reconstruction | 0 | 2 | 33 | 0.954 | 0.687 | 1.642 | 1.521 |
| reconstructionFine | 0 | 2 | 33 | 0.954 | 0.687 | 1.642 | 1.521 |
| round1 | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| fine | 0 | 0.5 | 158 | 3.886 | 9.916 | 13.802 | 8.078 |
| reconstruction | 0 | 0.5 | 106 | 2.694 | 2.583 | 5.278 | 4.435 |
| reconstructionFine | 0 | 0.5 | 106 | 2.694 | 2.583 | 5.278 | 4.435 |
| round1 | 0 | 0.1 | 296 | 6.822 | 128.166 | 134.988 | 33.052 |
| fine | 0 | 0.1 | 296 | 6.822 | 50.138 | 56.960 | 21.077 |
| reconstruction | 0 | 0.1 | 296 | 6.822 | 128.166 | 134.988 | 33.052 |
| reconstructionFine | 0 | 0.1 | 296 | 6.822 | 50.138 | 56.960 | 21.077 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| round1 / source | 0 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| fine / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | textured | 31.34 | 21.812% | 0.99870 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 38.54 | 1.633% | 0.99949 |
| reconstruction / round1 | 0 | 2 | textured | 30.11 | 25.446% | 0.99902 |
| reconstruction / fine | 0 | 2 | textured | 30.11 | 25.446% | 0.99902 |
| reconstruction / source | 0 | 2 | textured | 29.70 | 29.809% | 0.99814 |
| reconstruction / round1 | 0 | 2 | shaded | 34.61 | 5.636% | 0.99921 |
| reconstruction / fine | 0 | 2 | shaded | 34.61 | 5.636% | 0.99921 |
| reconstruction / source | 0 | 2 | shaded | 33.44 | 7.323% | 0.99893 |
| reconstructionFine / round1 | 0 | 2 | textured | 30.11 | 25.446% | 0.99902 |
| reconstructionFine / fine | 0 | 2 | textured | 30.11 | 25.446% | 0.99902 |
| reconstructionFine / reconstruction | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | textured | 29.70 | 29.809% | 0.99814 |
| reconstructionFine / round1 | 0 | 2 | shaded | 34.61 | 5.636% | 0.99921 |
| reconstructionFine / fine | 0 | 2 | shaded | 34.61 | 5.636% | 0.99921 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 33.44 | 7.323% | 0.99893 |
| round1 / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| round1 / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| fine / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | textured | 36.61 | 5.792% | 0.99925 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 44.38 | 0.326% | 0.99994 |
| reconstruction / round1 | 0 | 0.5 | textured | 32.62 | 14.927% | 0.99915 |
| reconstruction / fine | 0 | 0.5 | textured | 32.62 | 14.927% | 0.99915 |
| reconstruction / source | 0 | 0.5 | textured | 33.06 | 14.562% | 0.99908 |
| reconstruction / round1 | 0 | 0.5 | shaded | 46.25 | 0.205% | 0.99992 |
| reconstruction / fine | 0 | 0.5 | shaded | 46.25 | 0.205% | 0.99992 |
| reconstruction / source | 0 | 0.5 | shaded | 42.53 | 0.552% | 0.99987 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 32.62 | 14.927% | 0.99915 |
| reconstructionFine / fine | 0 | 0.5 | textured | 32.62 | 14.927% | 0.99915 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | textured | 33.06 | 14.562% | 0.99908 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | 46.25 | 0.205% | 0.99992 |
| reconstructionFine / fine | 0 | 0.5 | shaded | 46.25 | 0.205% | 0.99992 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 42.53 | 0.552% | 0.99987 |
| round1 / source | 0 | 0.1 | textured | 40.07 | 1.872% | 0.99934 |
| round1 / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 38.68 | 3.303% | 0.99926 |
| fine / source | 0 | 0.1 | textured | 39.68 | 1.896% | 0.99936 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | 38.68 | 3.303% | 0.99926 |
| reconstruction / source | 0 | 0.1 | textured | 40.07 | 1.872% | 0.99934 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 38.68 | 3.303% | 0.99926 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 38.68 | 3.303% | 0.99926 |
| reconstructionFine / source | 0 | 0.1 | textured | 39.68 | 1.896% | 0.99936 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 50.10 | 0.024% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
