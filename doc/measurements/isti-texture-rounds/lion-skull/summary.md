# Nexus cache and image comparison

GPU values are audited logical allocations in MiB, including exact mip chains. CPU heap and driver overhead are excluded. Cache budget is unbounded; below-target prefetch and FPS adaptation are disabled.

| Model | View | Tau | Resident nodes | Geometry MiB | Texture MiB | Total MiB | Legacy estimate MiB |
|---|---:|---:|---:|---:|---:|---:|---:|
| control | 0 | 2 | 10 | 0.283 | 0.208 | 0.491 | 0.529 |
| round1 | 0 | 2 | 37 | 0.984 | 0.771 | 1.755 | 1.873 |
| round2 | 0 | 2 | 37 | 0.984 | 0.771 | 1.755 | 1.873 |
| nexus3 | 0 | 2 | 3 | 1.082 | 10.659 | 11.741 | 10.057 |
| control | 1 | 2 | 50 | 1.304 | 1.042 | 2.346 | 2.488 |
| round1 | 1 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| round2 | 1 | 2 | 100 | 2.502 | 2.146 | 4.647 | 4.809 |
| nexus3 | 1 | 2 | 12 | 4.410 | 48.236 | 52.646 | 35.762 |
| control | 2 | 2 | 143 | 3.468 | 3.104 | 6.572 | 6.684 |
| round1 | 2 | 2 | 201 | 4.754 | 5.125 | 9.879 | 9.493 |
| round2 | 2 | 2 | 201 | 4.754 | 5.125 | 9.879 | 9.493 |
| nexus3 | 2 | 2 | 12 | 4.410 | 48.236 | 52.646 | 35.762 |

Pixel comparisons use the union of model pixels, with an 8/255 maximum-channel difference threshold. No automatic quality-equivalence claim is made.

| Compared / reference | View | Tau | Mode | PSNR dB | Pixels over 8/255 | Silhouette IoU |
|---|---:|---:|---|---:|---:|---:|
| control / source | 0 | 2 | textured | 22.39 | 70.638% | 0.99267 |
| control / source | 0 | 2 | shaded | 25.46 | 28.283% | 0.99267 |
| round1 / control | 0 | 2 | textured | 22.87 | 66.130% | 0.99336 |
| round1 / source | 0 | 2 | textured | 25.17 | 57.364% | 0.99792 |
| round1 / control | 0 | 2 | shaded | 26.75 | 20.869% | 0.99336 |
| round1 / source | 0 | 2 | shaded | 31.34 | 10.938% | 0.99792 |
| round2 / control | 0 | 2 | textured | 22.87 | 66.130% | 0.99336 |
| round2 / round1 | 0 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | textured | 25.17 | 57.364% | 0.99792 |
| round2 / control | 0 | 2 | shaded | 26.75 | 20.869% | 0.99336 |
| round2 / round1 | 0 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 0 | 2 | shaded | 31.34 | 10.938% | 0.99792 |
| nexus3 / control | 0 | 2 | textured | 21.93 | 72.277% | 0.99287 |
| nexus3 / round1 | 0 | 2 | textured | 24.31 | 60.215% | 0.99742 |
| nexus3 / round2 | 0 | 2 | textured | 24.31 | 60.215% | 0.99742 |
| nexus3 / source | 0 | 2 | textured | 30.29 | 26.243% | 0.99881 |
| nexus3 / control | 0 | 2 | shaded | 26.05 | 24.004% | 0.99282 |
| nexus3 / round1 | 0 | 2 | shaded | 32.92 | 7.438% | 0.99747 |
| nexus3 / round2 | 0 | 2 | shaded | 32.92 | 7.438% | 0.99747 |
| nexus3 / source | 0 | 2 | shaded | 33.82 | 6.563% | 0.99886 |
| control / source | 1 | 2 | textured | 24.81 | 57.575% | 0.99867 |
| control / source | 1 | 2 | shaded | 33.66 | 6.300% | 0.99868 |
| round1 / control | 1 | 2 | textured | 26.59 | 40.764% | 0.99890 |
| round1 / source | 1 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| round1 / control | 1 | 2 | shaded | 36.02 | 3.125% | 0.99891 |
| round1 / source | 1 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| round2 / control | 1 | 2 | textured | 26.59 | 40.764% | 0.99890 |
| round2 / round1 | 1 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 1 | 2 | textured | 26.56 | 46.456% | 0.99935 |
| round2 / control | 1 | 2 | shaded | 36.02 | 3.125% | 0.99891 |
| round2 / round1 | 1 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 1 | 2 | shaded | 36.88 | 2.811% | 0.99935 |
| nexus3 / control | 1 | 2 | textured | 24.35 | 59.777% | 0.99867 |
| nexus3 / round1 | 1 | 2 | textured | 25.94 | 49.306% | 0.99935 |
| nexus3 / round2 | 1 | 2 | textured | 25.94 | 49.306% | 0.99935 |
| nexus3 / source | 1 | 2 | textured | 34.58 | 10.270% | 1.00000 |
| nexus3 / control | 1 | 2 | shaded | 34.77 | 4.558% | 0.99868 |
| nexus3 / round1 | 1 | 2 | shaded | 39.60 | 1.204% | 0.99935 |
| nexus3 / round2 | 1 | 2 | shaded | 39.60 | 1.204% | 0.99935 |
| nexus3 / source | 1 | 2 | shaded | 39.57 | 1.545% | 1.00000 |
| control / source | 2 | 2 | textured | 27.11 | 41.663% | 0.99987 |
| control / source | 2 | 2 | shaded | 38.90 | 1.731% | 0.99987 |
| round1 / control | 2 | 2 | textured | 31.21 | 13.395% | 0.99988 |
| round1 / source | 2 | 2 | textured | 29.29 | 32.452% | 0.99998 |
| round1 / control | 2 | 2 | shaded | 48.49 | 0.111% | 0.99988 |
| round1 / source | 2 | 2 | shaded | 39.37 | 1.586% | 0.99998 |
| round2 / control | 2 | 2 | textured | 31.21 | 13.395% | 0.99988 |
| round2 / round1 | 2 | 2 | textured | identical | 0.000% | 1.00000 |
| round2 / source | 2 | 2 | textured | 29.29 | 32.452% | 0.99998 |
| round2 / control | 2 | 2 | shaded | 48.49 | 0.111% | 0.99988 |
| round2 / round1 | 2 | 2 | shaded | identical | 0.000% | 1.00000 |
| round2 / source | 2 | 2 | shaded | 39.37 | 1.586% | 0.99998 |
| nexus3 / control | 2 | 2 | textured | 27.15 | 39.866% | 0.99987 |
| nexus3 / round1 | 2 | 2 | textured | 29.37 | 30.067% | 0.99998 |
| nexus3 / round2 | 2 | 2 | textured | 29.37 | 30.067% | 0.99998 |
| nexus3 / source | 2 | 2 | textured | 38.68 | 3.058% | 1.00000 |
| nexus3 / control | 2 | 2 | shaded | 46.87 | 0.142% | 0.99987 |
| nexus3 / round1 | 2 | 2 | shaded | 51.05 | 0.034% | 0.99998 |
| nexus3 / round2 | 2 | 2 | shaded | 51.05 | 0.034% | 0.99998 |
| nexus3 / source | 2 | 2 | shaded | 39.56 | 1.559% | 1.00000 |

[Image gallery](gallery.html) · [Full measurements](results.json)
