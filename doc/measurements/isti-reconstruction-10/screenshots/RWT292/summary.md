# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| round1 | 0 | 2 | 77 | 2.025 | 22.432 | 24.457 | 6.732 |
| fine | 0 | 2 | 77 | 2.025 | 9.331 | 11.356 | 4.112 |
| reconstruction | 0 | 2 | 57 | 1.482 | 14.016 | 15.498 | 5.090 |
| reconstructionFine | 0 | 2 | 57 | 1.482 | 1.096 | 2.578 | 2.481 |
| round1 | 0 | 0.5 | 122 | 3.121 | 114.682 | 117.803 | 21.156 |
| fine | 0 | 0.5 | 122 | 3.121 | 27.963 | 31.084 | 10.128 |
| reconstruction | 0 | 0.5 | 122 | 3.121 | 114.682 | 117.803 | 21.156 |
| reconstructionFine | 0 | 0.5 | 122 | 3.121 | 27.963 | 31.084 | 10.128 |
| round1 | 0 | 0.1 | 151 | 3.822 | 224.349 | 228.171 | 38.365 |
| fine | 0 | 0.1 | 151 | 3.822 | 46.264 | 50.085 | 15.675 |
| reconstruction | 0 | 0.1 | 151 | 3.822 | 224.349 | 228.171 | 38.365 |
| reconstructionFine | 0 | 0.1 | 151 | 3.822 | 46.264 | 50.085 | 15.675 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| round1 / source | 0 | 2 | textured | 11.33 | 43.246% | 0.99915 |
| round1 / source | 0 | 2 | shaded | 27.29 | 21.611% | 0.99934 |
| fine / round1 | 0 | 2 | textured | 39.59 | 3.037% | 0.99992 |
| fine / source | 0 | 2 | textured | 11.31 | 43.273% | 0.99911 |
| fine / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 2 | shaded | 27.29 | 21.611% | 0.99934 |
| reconstruction / round1 | 0 | 2 | textured | 33.71 | 12.207% | 0.99878 |
| reconstruction / fine | 0 | 2 | textured | 32.73 | 15.216% | 0.99870 |
| reconstruction / source | 0 | 2 | textured | 11.31 | 49.606% | 0.99834 |
| reconstruction / round1 | 0 | 2 | shaded | 36.96 | 2.541% | 0.99885 |
| reconstruction / fine | 0 | 2 | shaded | 36.96 | 2.541% | 0.99885 |
| reconstruction / source | 0 | 2 | shaded | 26.82 | 23.139% | 0.99846 |
| reconstructionFine / round1 | 0 | 2 | textured | 32.72 | 15.291% | 0.99868 |
| reconstructionFine / fine | 0 | 2 | textured | 33.70 | 12.262% | 0.99876 |
| reconstructionFine / reconstruction | 0 | 2 | textured | 39.51 | 3.092% | 0.99991 |
| reconstructionFine / source | 0 | 2 | textured | 11.30 | 49.631% | 0.99832 |
| reconstructionFine / round1 | 0 | 2 | shaded | 36.96 | 2.541% | 0.99885 |
| reconstructionFine / fine | 0 | 2 | shaded | 36.96 | 2.541% | 0.99885 |
| reconstructionFine / reconstruction | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 2 | shaded | 26.82 | 23.139% | 0.99846 |
| round1 / source | 0 | 0.5 | textured | 11.33 | 38.938% | 0.99970 |
| round1 / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| fine / round1 | 0 | 0.5 | textured | 38.79 | 3.389% | 0.99998 |
| fine / source | 0 | 0.5 | textured | 11.31 | 39.058% | 0.99972 |
| fine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| reconstruction / round1 | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.5 | textured | 38.79 | 3.389% | 0.99998 |
| reconstruction / source | 0 | 0.5 | textured | 11.33 | 38.938% | 0.99970 |
| reconstruction / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| reconstructionFine / round1 | 0 | 0.5 | textured | 38.79 | 3.389% | 0.99998 |
| reconstructionFine / fine | 0 | 0.5 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.5 | textured | 38.79 | 3.389% | 0.99998 |
| reconstructionFine / source | 0 | 0.5 | textured | 11.31 | 39.058% | 0.99972 |
| reconstructionFine / round1 | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.5 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.5 | shaded | 27.63 | 20.078% | 0.99981 |
| round1 / source | 0 | 0.1 | textured | 11.33 | 38.250% | 0.99987 |
| round1 / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |
| fine / round1 | 0 | 0.1 | textured | 37.99 | 3.969% | 0.99996 |
| fine / source | 0 | 0.1 | textured | 11.31 | 38.431% | 0.99991 |
| fine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| fine / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |
| reconstruction / round1 | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | textured | 37.99 | 3.969% | 0.99996 |
| reconstruction / source | 0 | 0.1 | textured | 11.33 | 38.250% | 0.99987 |
| reconstruction / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstruction / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |
| reconstructionFine / round1 | 0 | 0.1 | textured | 37.99 | 3.969% | 0.99996 |
| reconstructionFine / fine | 0 | 0.1 | textured | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | textured | 37.99 | 3.969% | 0.99996 |
| reconstructionFine / source | 0 | 0.1 | textured | 11.31 | 38.431% | 0.99991 |
| reconstructionFine / round1 | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / fine | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / reconstruction | 0 | 0.1 | shaded | identical | 0.000% | 1.00000 |
| reconstructionFine / source | 0 | 0.1 | shaded | 27.80 | 19.229% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
